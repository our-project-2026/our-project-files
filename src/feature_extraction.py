"""Extract useful QC features from fastp JSON reports."""
import argparse
import json
from pathlib import Path
import pandas as pd


def clean_sample_name(json_path: Path) -> str:
    name = json_path.name
    for suffix in ["_fastp.json", ".fastp.json", ".json"]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return json_path.stem


def extract_fastp_features(json_path: Path) -> dict:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    before = data.get("summary", {}).get("before_filtering", {})
    after = data.get("summary", {}).get("after_filtering", {})
    duplication = data.get("duplication", {})

    return {
        "sample_id": clean_sample_name(json_path),
        "before_total_reads": before.get("total_reads"),
        "after_total_reads": after.get("total_reads"),
        "before_total_bases": before.get("total_bases"),
        "after_total_bases": after.get("total_bases"),
        "before_q20_rate": before.get("q20_rate"),
        "before_q30_rate": before.get("q30_rate"),
        "after_q20_rate": after.get("q20_rate"),
        "after_q30_rate": after.get("q30_rate"),
        "before_gc_content": before.get("gc_content"),
        "after_gc_content": after.get("gc_content"),
        "duplication_rate": duplication.get("rate"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastp-dir", default="results/fastp")
    parser.add_argument("--metadata", default="sample_metadata.csv")
    parser.add_argument("--output", default="results/fastp_features.csv")
    args = parser.parse_args()

    fastp_dir = Path(args.fastp_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = [extract_fastp_features(p) for p in sorted(fastp_dir.glob("*.json"))]
    df = pd.DataFrame(rows)

    metadata_path = Path(args.metadata)
    if metadata_path.exists() and not df.empty:
        meta = pd.read_csv(metadata_path)
        df = df.merge(meta, on="sample_id", how="left")

    df.to_csv(output, index=False)
    print(df)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
