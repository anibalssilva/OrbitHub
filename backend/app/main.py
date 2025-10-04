from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import json
import pandas as pd
from joblib import load
from .data_access import filter_satellites, persist_portal_request

app = FastAPI(title="Sustentabilidade de Satélites")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SatelliteInput(BaseModel):
    OBJECT_NAME: str | None = None
    PURPOSE: str | None = None
    OPS_STATUS_CODE: str | None = None
    LAUNCH_DATE: str | None = None
    LIFETIME_YEARS: float | None = None
    CAPABILITIES_COUNT: int | None = None


def get_models_dir():
    return os.path.join("backend", "app", "models")


def load_artifacts():
    models_dir = get_models_dir()
    pre = load(os.path.join(models_dir, "preprocessor.joblib"))
    model = load(os.path.join(models_dir, "kmeans.joblib"))
    with open(os.path.join(models_dir, "cluster_label_map.json"), "r", encoding="utf-8") as f:
        label_map = {int(k): v for k, v in json.load(f).items()}
    return pre, model, label_map


def map_cluster_to_label(cluster: int) -> str:
    mapping = {0: "OURO", 1: "PRATA", 2: "BRONZE"}
    return mapping.get(int(cluster), "BRONZE")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify")
def classify(items: List[SatelliteInput]):
    pre, model, label_map = load_artifacts()
    df = pd.DataFrame([item.dict() for item in items])
    X_num = pd.DataFrame(
        {
            "LIFETIME_YEARS": df.get("LIFETIME_YEARS", pd.Series([None] * len(df))).fillna(0),
            "CAPABILITIES_COUNT": df.get("CAPABILITIES_COUNT", pd.Series([0] * len(df))).fillna(0),
        }
    )
    X_cat = df[[c for c in ["PURPOSE", "OPS_STATUS_CODE"] if c in df.columns]].fillna("UNKNOWN")
    X = pd.concat([X_num, X_cat], axis=1)
    X_trans = pre.transform(X)
    clusters = model.predict(X_trans)
    labels = [label_map.get(int(c), "BRONZE") for c in clusters]
    return [{"label": label} for label in labels]


@app.get("/satellites")
def satellites(classification: str | None = None, purpose: str | None = None, delivery: str | None = None, limit: int = 50):
    return filter_satellites(classification=classification, purpose=purpose, delivery=delivery, limit=limit)


class PortalRequest(BaseModel):
    # Identificação do cliente
    name: str
    cnpj: str | None = None
    address: str | None = None
    email: str | None = None
    sector: str | None = None
    country: str | None = None
    # Solicitação de dados
    purpose: str
    purposeOther: str | None = None
    classification: str | None = None  # OURO/PRATA/BRONZE (opcional)
    delivery: str  # API ou Batch
    description: str | None = None
    language: str | None = None  # en ou pt
    selected_satellites: list | None = None  # Lista de satélites selecionados


@app.post("/portal/request")
def portal_request(payload: PortalRequest):
    path = persist_portal_request(payload.dict())
    return {"status": "received", "path": path}

