"""Merge fastp features and k-mer features into final features.csv."""
import argparse
from pathlib import Path
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fastp", default="results/fastp_features.csv")
    parser.add_argument("--kmers", default="results/kmer_features.csv")
    parser.add_argument("--output", default="results/features.csv")
    args = parser.parse_args()

    fastp = pd.read_csv(args.fastp) if Path(args.fastp).exists() else pd.DataFrame()
    kmers = pd.read_csv(args.kmers) if Path(args.kmers).exists() else pd.DataFrame()

    if fastp.empty and kmers.empty:
        raise ValueError("No feature files found. Run feature_extraction.py and kmer_extraction.py first.")
    elif fastp.empty:
        df = kmers
    elif kmers.empty:
        df = fastp
    else:
        class_cols = [c for c in ["class"] if c in kmers.columns and c in fastp.columns]
        kmers_no_dup = kmers.drop(columns=class_cols, errors="ignore")
        df = fastp.merge(kmers_no_dup, on="sample_id", how="outer")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(df.head())
    print(f"Saved final features file: {output}")


if __name__ == "__main__":
    main()
