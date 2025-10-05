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
from functools import lru_cache

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
        return load_classified_df()

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
    # refresh in‑memory cache / atualiza cache em memória
    try:
        load_classified_df.cache_clear()  # type: ignore[attr-defined]
    except Exception:
        pass
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
    # Special branch: Pending classification → list from Celestrak CSV
    # Ramo especial: Pendente de classificação → lista do CSV Celestrak
    norm_class = (classification or "").strip().upper()
    if norm_class in {"PENDENTE", "PENDENTE DE CLASSIFICAÇÃO", "PENDING", "PENDING CLASSIFICATION"}:
        return _list_pending_from_celestrak(limit=limit)

    # Get all classified satellites / Obtém todos os satélites classificados
    # Use cached DataFrame / Usa DataFrame em cache
    df = load_classified_df()

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
    # select only necessary columns before iterating / seleciona apenas colunas necessárias
    needed_cols = [
        "Name of Satellite, Alternate Names",
        "Current Official Name of Satellite",
        "Country/Org of UN Registry",
        "Country of Operator/Owner",
        "Operator/Owner",
        "Purpose",
        "Detailed Purpose",
        "SUSTAINABILITY_CLASS",
    ]
    available = [c for c in needed_cols if c in df_f.columns]
    df_sel = df_f.loc[:, available]

    # apply limit early to reduce iteration cost / aplica limite cedo
    if limit and limit > 0:
        df_sel = df_sel.head(limit)

    records: List[dict] = []
    for _, row in df_sel.iterrows():
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

    return records


def _list_pending_from_celestrak(limit: int = 50) -> List[dict]:
    """
    Load a lightweight list of satellites from Celestrak CSV for the
    "Pending Classification" category. Missing fields are returned as "--".

    Carrega uma lista leve de satélites do CSV Celestrak para a categoria
    "Pendente de Classificação". Campos ausentes retornam "--".
    """
    # Load cached Celestrak CSV / Carrega CSV Celestrak em cache
    df = load_celestrak_df()

    # Ensure we only take up to limit rows
    if limit and limit > 0:
        df = df.head(limit)

    records: List[dict] = []
    for _, row in df.iterrows():
        name = row.get("name")
        rec = {
            "name_of_satellite": str(name) if pd.notna(name) else "--",
            "alternate_names": "--",
            "country_un_registry": "--",
            "country_operator_owner": "--",
            "operator_owner": "--",
            "purpose": "--",
            "detailed_purpose": "--",
            "sustainability_class": "PENDENTE DE CLASSIFICAÇÃO",
        }
        records.append(rec)

    return records


# ---------- Lightweight cached loaders (performance) ----------

@lru_cache(maxsize=1)
def load_celestrak_df() -> pd.DataFrame:
    """Load Celestrak CSV once and keep in memory."""
    csv_path = os.path.join("..", "data", "raw", "Celestrak_data.csv")
    try:
        return pd.read_csv(csv_path, sep=";", engine="python")
    except Exception:
        return pd.read_csv(csv_path)


@lru_cache(maxsize=1)
def load_classified_df() -> pd.DataFrame:
    """Load classified satellites CSV once; compute if missing."""
    if os.path.exists(CLASSIFIED_CSV):
        return pd.read_csv(CLASSIFIED_CSV)
    # compute and return if file not present
    return get_classified_satellites(force_recompute=True)


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
    Persist client portal request to both JSON log and human-readable TXT file.
    Persiste requisição do portal do cliente em log JSON e arquivo TXT legível.
    
    Args:
        payload: Dictionary containing all request data including:
                - Client info (name, cnpj, address, email, sector, country)
                - Request details (purpose, classification, delivery, description)
                - Selected satellites list
                - Language preference (en/pt)
                
    Returns:
        Path to the created TXT file
    """
    # Create directories / Cria diretórios
    out_dir = os.path.join("..", "data", "processed")
    requests_dir = os.path.join("..", "solicitacoes")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(requests_dir, exist_ok=True)
    
    # Save JSON version for processing / Salva versão JSON para processamento
    jsonl_path = os.path.join(out_dir, "portal_requests.jsonl")
    with open(jsonl_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    
    # Create a human-readable TXT file / Cria arquivo TXT legível
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    client_name = payload.get('name', 'unknown').replace(' ', '_')[:30]
    txt_filename = f"solicitacao_{client_name}_{timestamp}.txt"
    txt_path = os.path.join(requests_dir, txt_filename)
    
    # Format the content based on language / Formata o conteúdo baseado no idioma
    lang = payload.get('language', 'en')
    selected_satellites = payload.get('selected_satellites', [])
    
    with open(txt_path, "w", encoding="utf-8") as f:
        if lang == 'pt':
            # Portuguese format / Formato em português
            f.write("=" * 80 + "\n")
            f.write("SOLICITAÇÃO DE DADOS DE SATÉLITES\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Data da Solicitação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("INFORMAÇÕES DO CLIENTE\n")
            f.write("-" * 80 + "\n")
            f.write(f"Nome: {payload.get('name', 'N/A')}\n")
            f.write(f"CNPJ: {payload.get('cnpj', 'N/A')}\n")
            f.write(f"Endereço: {payload.get('address', 'N/A')}\n")
            f.write(f"Email: {payload.get('email', 'N/A')}\n")
            f.write(f"Ramo de Atividade: {payload.get('sector', 'N/A')}\n")
            f.write(f"País: {payload.get('country', 'N/A')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("DETALHES DA SOLICITAÇÃO\n")
            f.write("-" * 80 + "\n")
            f.write(f"Finalidade: {payload.get('purpose', 'N/A')}\n")
            f.write(f"Classificação Ecológica: {payload.get('classification', 'Todas')}\n")
            f.write(f"Tipo de Entrega: {payload.get('delivery', 'N/A')}\n")
            f.write(f"Descrição: {payload.get('description', 'N/A')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"SATÉLITES SELECIONADOS ({len(selected_satellites)})\n")
            f.write("-" * 80 + "\n")
        else:
            # English format / Formato em inglês
            f.write("=" * 80 + "\n")
            f.write("SATELLITE DATA REQUEST\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Request Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("CLIENT INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Name: {payload.get('name', 'N/A')}\n")
            f.write(f"Company ID: {payload.get('cnpj', 'N/A')}\n")
            f.write(f"Address: {payload.get('address', 'N/A')}\n")
            f.write(f"Email: {payload.get('email', 'N/A')}\n")
            f.write(f"Business Sector: {payload.get('sector', 'N/A')}\n")
            f.write(f"Country: {payload.get('country', 'N/A')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("REQUEST DETAILS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Purpose: {payload.get('purpose', 'N/A')}\n")
            f.write(f"Ecological Classification: {payload.get('classification', 'All')}\n")
            f.write(f"Delivery Type: {payload.get('delivery', 'N/A')}\n")
            f.write(f"Description: {payload.get('description', 'N/A')}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"SELECTED SATELLITES ({len(selected_satellites)})\n")
            f.write("-" * 80 + "\n")
        
        # Write selected satellites details / Escreve detalhes dos satélites selecionados
        if selected_satellites:
            for idx, sat in enumerate(selected_satellites, 1):
                f.write(f"\n{idx}. {sat.get('name_of_satellite', 'Unknown')}\n")
                if sat.get('alternate_names'):
                    f.write(f"   Alternate Names: {sat.get('alternate_names')}\n")
                if sat.get('sustainability_class'):
                    f.write(f"   Ecological Classification: {sat.get('sustainability_class')}\n")
                if sat.get('country_un_registry'):
                    f.write(f"   UN Registry: {sat.get('country_un_registry')}\n")
                if sat.get('country_operator_owner'):
                    f.write(f"   Country/Operator: {sat.get('country_operator_owner')}\n")
                if sat.get('operator_owner'):
                    f.write(f"   Owner: {sat.get('operator_owner')}\n")
                if sat.get('purpose'):
                    f.write(f"   Purpose: {sat.get('purpose')}\n")
                if sat.get('detailed_purpose'):
                    f.write(f"   Detailed Purpose: {sat.get('detailed_purpose')}\n")
        else:
            f.write("\n(No satellites selected)\n")
        
        # Footer / Rodapé
        f.write("\n" + "=" * 80 + "\n")
        if lang == 'pt':
            f.write("FIM DA SOLICITAÇÃO\n")
        else:
            f.write("END OF REQUEST\n")
        f.write("=" * 80 + "\n")
    
    return txt_path
