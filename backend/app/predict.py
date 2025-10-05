import os
import json
import argparse
import pandas as pd
from joblib import load
from .features import load_ucs_from_data_raw, engineer_features


def get_models_dir() -> str:
    return os.path.join("app", "models")


def load_artifacts():
    models_dir = get_models_dir()
    pre = load(os.path.join(models_dir, "preprocessor.joblib"))
    model = load(os.path.join(models_dir, "kmeans.joblib"))
    with open(os.path.join(models_dir, "cluster_label_map.json"), "r", encoding="utf-8") as f:
        label_map = {int(k): v for k, v in json.load(f).items()}
    return pre, model, label_map


def main(output: str):
    df, _ = load_ucs_from_data_raw()
    feats = engineer_features(df)

    pre, model, label_map = load_artifacts()
    X = pre.transform(feats)
    clusters = model.predict(X)
    labels = [label_map.get(int(c), "BRONZE") for c in clusters]

    result = df.copy()
    result["SUSTAINABILITY_CLASS"] = labels
    if output.lower().endswith(".xlsx"):
        result.to_excel(output, index=False)
    else:
        result.to_csv(output, index=False)
    print(f"Arquivo salvo em {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=os.path.join("..", "data", "processed", "satellites_classified.csv"))
    args = parser.parse_args()
    main(args.out)


