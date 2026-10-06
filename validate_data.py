"""Check release integrity, split membership and row alignment."""
from pathlib import Path
import hashlib
import json

import pandas as pd

ROOT = Path(__file__).resolve().parent


def main():
    inventory = json.loads((ROOT / "file_manifest.json").read_text())
    for item in inventory:
        path = ROOT / item["file"]
        assert path.stat().st_size == item["bytes"], item["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], item["file"]

    manifest = json.loads((ROOT / "data/f008_split_manifest.json").read_text())
    dataset_path = ROOT / "data/explainability_dataset2.csv"
    assert hashlib.sha256(dataset_path.read_bytes()).hexdigest() == manifest["dataset"]["sha256"]
    data = pd.read_csv(dataset_path)
    assert len(data) == manifest["dataset"]["n_rows"] == 8239
    assert data.consumer_id.nunique() == manifest["dataset"]["n_consumers"] == 324
    assert data.row_id.is_unique
    split = manifest["split"]
    train_consumers, eval_consumers = set(split["train_consumers"]), set(split["eval_consumers"])
    assert train_consumers.isdisjoint(eval_consumers)
    assert train_consumers | eval_consumers == set(data.consumer_id)
    train = data[data.consumer_id.isin(train_consumers)]
    evaluation = data[data.consumer_id.isin(eval_consumers)]
    assert len(train) == split["n_train_rows"] == 6589
    assert len(evaluation) == split["n_eval_rows"] == 1650
    assert evaluation.label_attack.value_counts().to_dict() == split["eval_rows_per_class"]
    lookup = evaluation.set_index("row_id")

    files = sorted((ROOT / "results/predictions").glob("*.parquet"))
    for path in files:
        predictions = pd.read_parquet(path)
        assert predictions.row_id.is_unique, path.name
        assert set(predictions.row_id) <= set(evaluation.row_id), path.name
        expected_consumers = lookup.loc[predictions.row_id, "consumer_id"].to_numpy()
        assert (predictions.consumer_id.to_numpy() == expected_consumers).all(), path.name

    gemini = pd.read_csv(ROOT / "results/gemini/gemini_zeroshot_full_results.csv")
    assert len(gemini) == 1650 and gemini.row_id.is_unique
    assert set(gemini.row_id) == set(evaluation.row_id)
    for column in ["consumer_id", "query_day", "label_attack", "label_binary"]:
        assert (gemini[column].to_numpy() == lookup.loc[gemini.row_id, column].to_numpy()).all(), column
    assert gemini.error.fillna("").eq("").all()
    print(f"Verified {len(inventory)} files; 8,239 rows; 259/65 disjoint consumers; "
          f"6,589/1,650 train/evaluation days; {len(files)} prediction files; Gemini alignment.")


if __name__ == "__main__":
    main()
