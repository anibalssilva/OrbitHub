"""
OrbitHub - NASA Hackathon 2025
Data Access Layer for Satellite Classification System

Este módulo gerencia o acesso aos dados de satélites, incluindo leitura, filtragem
e persistência de requisições do portal.

This module manages access to satellite data, including reading, filtering,
and persisting portal requests.
"""

import os
import json
from typing import List, Optional, Tuple
from datetime import datetime

import pandas as pd

from .features import load_ucs_from_data_raw, engineer_features
from joblib import load


# Directory paths / Caminhos de diretórios
MODELS_DIR = os.path.join("app", "models")
CLASSIFIED_CSV = os.path.join("..", "data", "processed", "satellites_classified.csv")


def _load_artifacts():
    """
    Load trained ML model artifacts.
    Carrega artefatos do modelo ML treinado.
    
    Returns:
        tuple: (preprocessor, kmeans_model, label_map)
    """
    pre = load(os.path.join(MODELS_DIR, "preprocessor.joblib"))
    model = load(os.path.join(MODELS_DIR, "kmeans.joblib"))
    with open(os.path.join(MODELS_DIR, "cluster_label_map.json"), "r", encoding="utf-8") as f:
        label_map = {int(k): v for k, v in json.load(f).items()}
    return pre, model, label_map


def get_classified_satellites(force_recompute: bool = False) -> pd.DataFrame:
    """
    Get all satellites with sustainability classification.
    If cached CSV exists, load from cache; otherwise, compute and save.
    
    Obtém todos os satélites com classificação de sustentabilidade.
    Se CSV em cache existe, carrega do cache; caso contrário, computa e salva.
    
    Args:
        force_recompute: Force re-computation even if cache exists
        
    Returns:
        DataFrame with all satellite data plus SUSTAINABILITY_CLASS column
    """
    # Load from cache if available / Carrega do cache se disponível
    if (not force_recompute) and os.path.exists(CLASSIFIED_CSV):
        return pd.read_csv(CLASSIFIED_CSV)

    # Compute classification / Computa classificação
    df_raw, _ = load_ucs_from_data_raw()
    feats = engineer_features(df_raw)
    pre, model, label_map = _load_artifacts()
    X = pre.transform(feats)
    clusters = model.predict(X)
    labels = [label_map.get(int(c), "BRONZE") for c in clusters]

    # Add classification to raw data / Adiciona classificação aos dados brutos
    out = df_raw.copy()
    out["SUSTAINABILITY_CLASS"] = labels
    
    # Persist for quicker reads later / Persiste para leituras mais rápidas depois
    os.makedirs(os.path.dirname(CLASSIFIED_CSV), exist_ok=True)
    out.to_csv(CLASSIFIED_CSV, index=False)
    return out


def _find_col(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """
    Find a column in DataFrame by trying multiple candidate names.
    Useful for handling varying column names across datasets.
    
    Encontra uma coluna no DataFrame tentando múltiplos nomes candidatos.
    Útil para lidar com nomes de colunas variados entre conjuntos de dados.
    
    Args:
        df: DataFrame to search in
        candidates: List of possible column names
        
    Returns:
        Actual column name if found, None otherwise
    """
    # First try exact match (case insensitive) / Primeiro tenta match exato (case insensitive)
    lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    
    # Then try substring match / Depois tenta match de substring
    for cand in candidates:
        key = cand.lower()
        for c in df.columns:
            if key in c.lower():
                return c
    
    # Debug: print what we're looking for vs what's available
    print(f"Looking for: {candidates}")
    print(f"Available: {list(df.columns)}")
    return None


def filter_satellites(
    classification: Optional[str] = None,
    purpose: Optional[str] = None,
    delivery: Optional[str] = None,
    limit: int = 50,
) -> List[dict]:
    """
    Filter satellites by classification, purpose, and delivery method.
    Filtra satélites por classificação, finalidade e método de entrega.
    
    Args:
        classification: Sustainability class filter (OURO/PRATA/BRONZE)
        purpose: Purpose keyword filter
        delivery: Delivery method preference (API/Batch) - not currently used in filtering
        limit: Maximum number of results to return
        
    Returns:
        List of satellite records with detailed information
    """
    # Get all classified satellites / Obtém todos os satélites classificados
    df = get_classified_satellites()

    df_f = df
    
    # Filter by classification if provided / Filtra por classificação se fornecida
    if classification:
        df_f = df_f[df_f["SUSTAINABILITY_CLASS"].str.upper() == classification.upper()]

    # Filter by purpose: search in Purpose column or fallback to other columns
    # Filtra por finalidade: busca na coluna Purpose ou usa outras colunas como fallback
    if purpose:
        if "Purpose" in df_f.columns:
            mask = df_f["Purpose"].astype(str).str.contains(purpose, case=False, na=False)
        else:
            # Fallback: search in object-related columns
            # Fallback: busca em colunas relacionadas ao objeto
            search_cols = [c for c in ["OBJECT_NAME", "OBJECT_TYPE", "ORBIT_TYPE"] if c in df_f.columns]
            if search_cols:
                mask = False
                for c in search_cols:
                    mask = mask | df_f[c].astype(str).str.contains(purpose, case=False, na=False)
            else:
                mask = pd.Series([True] * len(df_f), index=df_f.index)
        df_f = df_f[mask]

    # Build response with expected semantic fields using exact column names from CSV
    # Constrói resposta com campos semânticos esperados usando nomes exatos de colunas do CSV
    records: List[dict] = []
    for _, row in df_f.iterrows():
        # Get satellite name and extract alternate name if exists
        # Obtém nome do satélite e extrai nome alternativo se existe
        full_name = _safe_get(row, "Name of Satellite, Alternate Names")
        current_name = _safe_get(row, "Current Official Name of Satellite")
        
        rec = {
            "name_of_satellite": current_name or full_name,
            "alternate_names": full_name if full_name != current_name else None,
            "country_un_registry": _safe_get(row, "Country/Org of UN Registry"),
            "country_operator_owner": _safe_get(row, "Country of Operator/Owner"),
            "operator_owner": _safe_get(row, "Operator/Owner"),
            "purpose": _safe_get(row, "Purpose"),
            "detailed_purpose": _safe_get(row, "Detailed Purpose"),
            "sustainability_class": _safe_get(row, "SUSTAINABILITY_CLASS"),
        }
        records.append(rec)

    # Apply limit if specified / Aplica limite se especificado
    if limit and limit > 0:
        records = records[:limit]

    return records


def _safe_get(row, column_name):
    """
    Safely get a value from a pandas row, handling NaN, NaT, and missing columns.
    Obtém com segurança um valor de uma linha pandas, tratando NaN, NaT e colunas ausentes.
    
    Args:
        row: Pandas Series (row from DataFrame)
        column_name: Column name to retrieve
        
    Returns:
        Cleaned value or None if invalid/missing
    """
    try:
        if column_name not in row.index:
            return None
        value = row[column_name]
        return _clean_value(value)
    except Exception:
        return None


def _clean_value(value):
    """
    Convert pandas NaN, NaT, and invalid float values to None for JSON serialization.
    Converte NaN, NaT e valores float inválidos do pandas para None para serialização JSON.
    
    Args:
        value: Value to clean
        
    Returns:
        Cleaned value (string or None)
    """
    if pd.isna(value):
        return None
    if isinstance(value, float):
        import math
        if math.isinf(value) or math.isnan(value):
            return None
    # Convert to string if it's a valid value / Converte para string se for valor válido
    if value is not None:
        return str(value)
    return None


def persist_portal_request(payload: dict) -> str:
    """
    Persist client portal request to JSON log and send email notification.
    Persiste requisição do portal do cliente em log JSON e envia notificação por email.
    
    Args:
        payload: Dictionary containing all request data
        
    Returns:
        Status message
    """
    # Create directories / Cria diretórios
    out_dir = os.path.join("..", "data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    
    # Save JSON version for processing / Salva versão JSON para processamento
    jsonl_path = os.path.join(out_dir, "portal_requests.jsonl")
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    
    # Log the request (since files are temporary in Render)
    print(f"REQUEST RECEIVED: {payload.get('name', 'Unknown')} - {payload.get('purpose', 'No purpose')}")
    
    return "Request logged successfully"
