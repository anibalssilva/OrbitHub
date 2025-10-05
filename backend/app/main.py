"""
OrbitHub - NASA Hackathon 2025
FastAPI Backend for Satellite Sustainability Classification

Este módulo implementa a API REST para o sistema de classificação de sustentabilidade
de satélites, permitindo consultas e requisições de dados via portal web.

This module implements the REST API for the satellite sustainability classification
system, enabling data queries and requests via web portal.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import json
import pandas as pd
from joblib import load
from .data_access import filter_satellites, persist_portal_request, load_celestrak_df, load_classified_df
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.responses import ORJSONResponse
from starlette.middleware.gzip import GZipMiddleware
from fastapi.concurrency import run_in_threadpool

# Initialize FastAPI application / Inicializa aplicação FastAPI
app = FastAPI(title="Sustentabilidade de Satélites", default_response_class=ORJSONResponse)

# # Configure CORS middleware for cross-origin requests
# # Configura middleware CORS para requisições cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins / Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods / Permite todos os métodos HTTP
    allow_headers=["*"],  # Allow all headers / Permite todos os headers
)
app.add_middleware(GZipMiddleware, minimum_size=800)
# FRONTEND_ORIGIN = os.getenv("CORS_ORIGIN", "https://orbithub-lx4e.onrender.com")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[FRONTEND_ORIGIN],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=False,  # deixe False a menos que realmente use cookies/autenticação
# )


class SatelliteInput(BaseModel):
    """
    Pydantic model for individual satellite classification input.
    Modelo Pydantic para entrada de classificação individual de satélite.
    """
    OBJECT_NAME: str | None = None
    PURPOSE: str | None = None
    OPS_STATUS_CODE: str | None = None
    LAUNCH_DATE: str | None = None
    LIFETIME_YEARS: float | None = None
    CAPABILITIES_COUNT: int | None = None


def get_models_dir():
    """Get the models directory path / Obtém o caminho do diretório de modelos"""
    return os.path.join("backend", "app", "models")


def load_artifacts():
    """
    Load ML model artifacts (preprocessor, kmeans model, cluster labels).
    Carrega artefatos do modelo ML (preprocessador, modelo kmeans, labels de cluster).
    
    Returns:
        tuple: (preprocessor, kmeans_model, label_map)
    """
    models_dir = get_models_dir()
    pre = load(os.path.join(models_dir, "preprocessor.joblib"))
    model = load(os.path.join(models_dir, "kmeans.joblib"))
    with open(os.path.join(models_dir, "cluster_label_map.json"), "r", encoding="utf-8") as f:
        label_map = {int(k): v for k, v in json.load(f).items()}
    return pre, model, label_map


def map_cluster_to_label(cluster: int) -> str:
    """
    Map cluster ID to sustainability label (GOLD/SILVER/BRONZE).
    Mapeia ID de cluster para label de sustentabilidade (OURO/PRATA/BRONZE).
    """
    mapping = {0: "OURO", 1: "PRATA", 2: "BRONZE"}
    return mapping.get(int(cluster), "BRONZE")


# @app.get("/health")
# def health():
#     """
#     Health check endpoint.
#     Endpoint de verificação de saúde.
#     """
#     return {"status": "ok"}

@app.get("/", include_in_schema=False, tags=["meta"])
def root():
    # Se preferir, troque por: return {"service": "orbithub-backend", "status": "ok"}
    return RedirectResponse(url="/docs")

@app.get("/health", include_in_schema=False, tags=["meta"])
def health():
    return JSONResponse({"status": "ok"})


@app.post("/classify")
def classify(items: List[SatelliteInput]):
    """
    Classify one or more satellites based on sustainability criteria.
    Classifica um ou mais satélites baseado em critérios de sustentabilidade.
    
    Args:
        items: List of satellite data inputs
    
    Returns:
        List of classification labels (OURO/PRATA/BRONZE)
    """
    # Load ML artifacts / Carrega artefatos ML
    pre, model, label_map = load_artifacts()
    
    # Convert input to DataFrame / Converte entrada para DataFrame
    df = pd.DataFrame([item.dict() for item in items])
    
    # Prepare numeric features / Prepara features numéricas
    X_num = pd.DataFrame(
        {
            "LIFETIME_YEARS": df.get("LIFETIME_YEARS", pd.Series([None] * len(df))).fillna(0),
            "CAPABILITIES_COUNT": df.get("CAPABILITIES_COUNT", pd.Series([0] * len(df))).fillna(0),
        }
    )
    
    # Prepare categorical features / Prepara features categóricas
    X_cat = df[[c for c in ["PURPOSE", "OPS_STATUS_CODE"] if c in df.columns]].fillna("UNKNOWN")
    
    # Combine and transform / Combina e transforma
    X = pd.concat([X_num, X_cat], axis=1)
    X_trans = pre.transform(X)
    
    # Predict clusters and map to labels / Prediz clusters e mapeia para labels
    clusters = model.predict(X_trans)
    labels = [label_map.get(int(c), "BRONZE") for c in clusters]
    
    return [{"label": label} for label in labels]


@app.on_event("startup")
def _warmup():
    # Pre-load datasets into memory for faster first-hit latency
    try:
        load_celestrak_df()
        load_classified_df()
    except Exception:
        pass


@app.get("/satellites")
async def satellites(classification: str | None = None, purpose: str | None = None, delivery: str | None = None, limit: int = 50):
    """
    Get filtered list of classified satellites.
    Obtém lista filtrada de satélites classificados.
    
    Args:
        classification: Filter by sustainability class (OURO/PRATA/BRONZE)
        purpose: Filter by satellite purpose
        delivery: Delivery method preference (API/Batch)
        limit: Maximum number of results
    
    Returns:
        List of satellite records with detailed information
    """
    # run filtering on a worker thread to avoid blocking the event loop
    result = await run_in_threadpool(lambda: filter_satellites(classification=classification, purpose=purpose, delivery=delivery, limit=limit))
    # add short-lived HTTP cache to speed up repeated identical queries
    return ORJSONResponse(result, headers={"Cache-Control": "public, max-age=300"})


class PortalRequest(BaseModel):
    """
    Pydantic model for client portal data requests.
    Modelo Pydantic para requisições de dados do portal do cliente.
    """
    # Client identification / Identificação do cliente
    name: str
    cnpj: str | None = None
    address: str | None = None
    email: str | None = None
    sector: str | None = None
    country: str | None = None
    # Data request details / Detalhes da solicitação de dados
    purpose: str  # Purpose of data request / Finalidade da requisição
    purposeOther: str | None = None  # Custom purpose if "Other" selected / Finalidade customizada se "Outro" selecionado
    classification: str | None = None  # Sustainability filter: OURO/PRATA/BRONZE (optional) / Filtro de sustentabilidade (opcional)
    delivery: str  # Delivery method: API or Batch / Método de entrega: API ou Batch
    description: str | None = None  # Additional request description / Descrição adicional da requisição
    language: str | None = None  # Interface language: en or pt / Idioma da interface: en ou pt
    selected_satellites: list | None = None  # List of selected satellites / Lista de satélites selecionados


@app.post("/portal/request")
def portal_request(payload: PortalRequest):
    """
    Process and persist client data request from portal.
    Processa e persiste requisição de dados do cliente do portal.
    
    Args:
        payload: Client request data including filters and selected satellites
    
    Returns:
        Status confirmation and file path of saved request
    """
    path = persist_portal_request(payload.dict())
    return {"status": "received", "path": path}

