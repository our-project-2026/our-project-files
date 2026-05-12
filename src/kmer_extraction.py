"""Extract k-mer frequencies from FASTQ files."""
import argparse
from collections import Counter
from pathlib import Path
import pandas as pd
from Bio import SeqIO


def sample_id_from_fastq(path: Path) -> str:
    name = path.name
    for suffix in [".fastq.gz", ".fq.gz", ".fastq", ".fq"]:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def kmers(sequence: str, k: int):
    sequence = sequence.upper()
    return [sequence[i : i + k] for i in range(len(sequence) - k + 1) if "N" not in sequence[i : i + k]]


def kmer_frequency_for_file(path: Path, k: int) -> dict:
    counts = Counter()
    total = 0
    for record in SeqIO.parse(str(path), "fastq"):
        parts = kmers(str(record.seq), k)
        counts.update(parts)
        total += len(parts)

    row = {"sample_id": sample_id_from_fastq(path)}
    if total == 0:
        return row
    for kmer, count in sorted(counts.items()):
        row[f"kmer_{kmer}"] = count / total
    return row


def find_fastq_files(input_dir: Path):
    files = []
    for pattern in ["*.fastq", "*.fq", "*.fastq.gz", "*.fq.gz"]:
        files.extend(input_dir.glob(pattern))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data")
    parser.add_argument("--metadata", default="sample_metadata.csv")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", default="results/kmer_features.csv")
    args = parser.parse_args()

    rows = [kmer_frequency_for_file(p, args.k) for p in find_fastq_files(Path(args.input))]
    df = pd.DataFrame(rows).fillna(0)

    metadata_path = Path(args.metadata)
    if metadata_path.exists() and not df.empty:
        meta = pd.read_csv(metadata_path)
        df = df.merge(meta, on="sample_id", how="left")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(df)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
