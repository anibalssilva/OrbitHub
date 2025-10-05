import os
import pandas as pd
from typing import Tuple, Optional


def load_ucs_from_data_raw() -> Tuple[pd.DataFrame, str]:
    # Go up one level from backend to project root, then to data/raw
    data_dir = os.path.join("..", "data", "raw")
    excel_path = os.path.join(data_dir, "UCS-Satellite-Database 5-1-2023.xlsx")
    if not os.path.exists(excel_path):
        raise FileNotFoundError("Arquivo UCS XLSX não encontrado em data/raw")
    df = pd.read_excel(excel_path, engine="openpyxl")
    return df, excel_path


def _find_col(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        key = cand.lower()
        if key in cols_lower:
            return cols_lower[key]
    # busca por substring
    for cand in candidates:
        key = cand.lower()
        for c in df.columns:
            if key in c.lower():
                return c
    return None


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df_proc = df.copy()

    # PURPOSE: supomos que exista uma coluna de propósito; normalize texto
    if "PURPOSE" not in df_proc.columns:
        # Tente inferir a partir de OBJECT_NAME/ORBIT_TYPE se necessário
        df_proc["PURPOSE"] = "UNKNOWN"
    df_proc["PURPOSE"] = df_proc["PURPOSE"].astype(str).str.upper().str.strip()

    # Impacto ambiental (proxy): menor apogeu/perigeu e presença de decaimento
    # Crie um score simples a partir de colunas se existirem
    for col in ["APOGEE", "PERIGEE"]:
        if col not in df_proc.columns:
            df_proc[col] = pd.NA

    # Coagir APOGEE/PERIGEE a numérico antes de calcular score
    for _col in ["APOGEE", "PERIGEE"]:
        df_proc[_col] = pd.to_numeric(df_proc[_col], errors="coerce")
    apo_med = df_proc["APOGEE"].median(skipna=True)
    per_med = df_proc["PERIGEE"].median(skipna=True)
    if pd.isna(apo_med):
        apo_med = 0.0
    if pd.isna(per_med):
        per_med = 0.0
    df_proc["ENV_IMPACT_SCORE"] = (
        df_proc["APOGEE"].fillna(apo_med) + df_proc["PERIGEE"].fillna(per_med)
    )
    # Normalizar impacto (menor = melhor). Vamos inverter depois pelo scaler.

    # Tempo de vida útil
    # 1) tentar datas de lançamento/decay com heurística de nomes
    launch_col = _find_col(df_proc, ["LAUNCH_DATE", "DATE OF LAUNCH", "LAUNCH"])
    decay_col = _find_col(df_proc, ["DECAY_DATE", "DATE OF DECAY", "REENTRY", "RE-ENTRY", "DEORBIT", "DECAY"])

    if launch_col is not None:
        df_proc[launch_col] = pd.to_datetime(df_proc[launch_col], errors="coerce", utc=True)
    if decay_col is not None:
        df_proc[decay_col] = pd.to_datetime(df_proc[decay_col], errors="coerce", utc=True)

    if launch_col is not None:
        today = pd.Timestamp.now(tz="UTC").normalize()
        if decay_col is not None:
            decay_series = df_proc[decay_col].fillna(today)
        else:
            decay_series = pd.Series([today] * len(df_proc), index=df_proc.index)
        lifetime_days = (decay_series - df_proc[launch_col]).dt.days
        df_proc["LIFETIME_YEARS"] = (lifetime_days.fillna(0) / 365.25).clip(lower=0)
    else:
        # 2) fallback: usar coluna de vida útil declarada
        life_col = _find_col(df_proc, ["LIFETIME", "EXPECTED LIFETIME", "LIFETIME (YRS)", "LIFE (YRS)"])
        if life_col is not None:
            df_proc["LIFETIME_YEARS"] = pd.to_numeric(df_proc[life_col], errors="coerce").fillna(0).clip(lower=0)
        else:
            df_proc["LIFETIME_YEARS"] = 0

    # Capacidades (proxy): contar quantas colunas chave não nulas por linha
    capability_cols = [
        c for c in [
            "OBJECT_TYPE",
            "OPS_STATUS_CODE",
            "ORBIT_TYPE",
            "ORBIT_CENTER",
            "DATA_STATUS_CODE",
        ]
        if c in df_proc.columns
    ]
    if capability_cols:
        df_proc["CAPABILITIES_COUNT"] = df_proc[capability_cols].notna().sum(axis=1)
    else:
        df_proc["CAPABILITIES_COUNT"] = 0

    # Coagir APOGEE/PERIGEE a numérico para cálculo estável do score
    for col in ["APOGEE", "PERIGEE"]:
        df_proc[col] = pd.to_numeric(df_proc[col], errors="coerce")

    # Selecionar features finais para ML
    base_cols = [
        "PURPOSE",
        "LIFETIME_YEARS",
        "CAPABILITIES_COUNT",
        "ENV_IMPACT_SCORE",
    ]
    features = df_proc[base_cols].copy()
    if "OPS_STATUS_CODE" in df_proc.columns:
        features["OPS_STATUS_CODE"] = df_proc["OPS_STATUS_CODE"].fillna("UNKNOWN")
    else:
        features["OPS_STATUS_CODE"] = "UNKNOWN"

    return features


