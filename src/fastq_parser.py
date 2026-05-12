"""FASTQ parser using Biopython.
Usage: python src/fastq_parser.py data/sample.fastq
"""
import argparse
from pathlib import Path
from Bio import SeqIO


def parse_fastq(file_path: str, limit: int = 5):
    reads = []
    for i, record in enumerate(SeqIO.parse(file_path, "fastq")):
        reads.append({
            "id": record.id,
            "sequence": str(record.seq),
            "quality": record.letter_annotations["phred_quality"],
        })
        if limit and i + 1 >= limit:
            break
    return reads


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fastq", help="Path to FASTQ file")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    path = Path(args.fastq)
    if not path.exists():
        raise FileNotFoundError(f"FASTQ file not found: {path}")

    reads = parse_fastq(str(path), args.limit)
    print(f"Displayed reads: {len(reads)}")
    for read in reads:
        print("-" * 60)
        print("Read ID:", read["id"])
        print("Sequence:", read["sequence"][:100])
        print("Quality:", read["quality"][:20])


if __name__ == "__main__":
    main()
