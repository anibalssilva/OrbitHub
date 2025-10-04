import os
import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from joblib import dump
from .features import load_ucs_from_data_raw, engineer_features


def ensure_models_dir() -> str:
    models_dir = os.path.join("backend", "app", "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir


def build_pipeline(categorical_cols, numeric_cols) -> Pipeline:
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_cols),
            ("num", numeric_pipeline, numeric_cols),
        ]
    )

    model = KMeans(n_clusters=3, random_state=42, n_init=10)

    pipe = Pipeline(steps=[
        ("pre", preprocessor),
        ("kmeans", model),
    ])
    return pipe


def main():
    df, path = load_ucs_from_data_raw()
    feats = engineer_features(df)

    categorical_cols = ["PURPOSE", "OPS_STATUS_CODE"]
    numeric_cols = ["LIFETIME_YEARS", "CAPABILITIES_COUNT", "ENV_IMPACT_SCORE"]

    pipe = build_pipeline(categorical_cols, numeric_cols)
    pipe.fit(feats)

    # Persist artifacts
    models_dir = ensure_models_dir()
    # Extraia partes para usar na API
    pre: ColumnTransformer = pipe.named_steps["pre"]
    kmeans: KMeans = pipe.named_steps["kmeans"]

    # Para reuso simples, salve o preprocessor inteiro e o modelo
    dump(pre, os.path.join(models_dir, "preprocessor.joblib"))
    dump(kmeans, os.path.join(models_dir, "kmeans.joblib"))

    # Construir mapeamento de cluster -> label (OURO/PRATA/BRONZE)
    # Critérios: maior sustentabilidade = maior LIFETIME_YEARS, maior CAPABILITIES_COUNT,
    # menor ENV_IMPACT_SCORE, maior alinhamento de PURPOSE ao meio ambiente.

    def purpose_env_score(text: str) -> float:
        if not isinstance(text, str):
            return 0.0
        t = text.upper()
        keywords = [
            "ENV", "EARTH", "CLIMATE", "WEATHER", "ATMOS", "OCEAN", "ENVIRONMENT",
            "ECO", "SUSTAIN", "REMOTE SENSING", "IMAGING"
        ]
        return float(sum(1 for k in keywords if k in t)) / max(1, len(keywords))

    # Calcular métricas cruas e normalizar 0-1
    raw = feats.copy()
    raw["PURPOSE_SCORE"] = raw["PURPOSE"].apply(purpose_env_score)
    # Normalizações simples min-max
    def minmax(series: pd.Series) -> pd.Series:
        s = series.astype(float)
        mn, mx = s.min(), s.max()
        if pd.isna(mn) or pd.isna(mx) or mx == mn:
            return pd.Series(0.0, index=s.index)
        return (s - mn) / (mx - mn)

    mm_life = minmax(raw["LIFETIME_YEARS"])
    mm_caps = minmax(raw["CAPABILITIES_COUNT"])
    mm_env_inv = 1.0 - minmax(raw["ENV_IMPACT_SCORE"])  # menor impacto => maior score
    mm_purpose = minmax(raw["PURPOSE_SCORE"])  # já 0-1, mas normalize de novo

    composite = 0.4 * mm_purpose + 0.3 * mm_life + 0.2 * mm_caps + 0.1 * mm_env_inv

    # Atribuir clusters e computar média do score por cluster
    transformed = pre.transform(feats)
    clusters = kmeans.predict(transformed)
    comp_by_cluster = pd.DataFrame({"cluster": clusters, "score": composite}).groupby("cluster").mean()["score"]
    # Ordenar decrescente: melhor = OURO
    ordered = comp_by_cluster.sort_values(ascending=False).index.tolist()
    label_map = {}
    for idx, cl in enumerate(ordered):
        label_map[int(cl)] = ["OURO", "PRATA", "BRONZE"][idx] if idx < 3 else "BRONZE"

    # Salvar mapping e defaults para preencher ausências na API
    defaults = {
        "LIFETIME_YEARS_median": float(feats["LIFETIME_YEARS"].median()),
        "CAPABILITIES_COUNT_median": float(feats["CAPABILITIES_COUNT"].median()),
        "ENV_IMPACT_SCORE_median": float(feats["ENV_IMPACT_SCORE"].median()),
    }

    with open(os.path.join(models_dir, "cluster_label_map.json"), "w", encoding="utf-8") as f:
        json.dump(label_map, f)
    with open(os.path.join(models_dir, "feature_defaults.json"), "w", encoding="utf-8") as f:
        json.dump(defaults, f)

    print("Treinamento concluído. Artefatos salvos em:", models_dir)


if __name__ == "__main__":
    main()


