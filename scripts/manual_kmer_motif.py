#!/usr/bin/env python3

import argparse
from collections import Counter

# ---------- ARGUMENTS ----------
parser = argparse.ArgumentParser(description="Manual k-mer motif discovery from FASTA")
parser.add_argument("-i", "--input", required=True, help="Input FASTA file")
parser.add_argument("-k", "--kmer", type=int, default=7, help="k-mer size (default: 7)")
parser.add_argument("-top", "--top", type=int, default=20, help="Number of top motifs to show")
parser.add_argument("--validate", help="Validate a specific motif across sequences")

args = parser.parse_args()

k = args.kmer
top_n = args.top

# ---------- READ FASTA ----------
sequences = []

with open(args.input) as f:
    for i, line in enumerate(f):
        if i % 2 == 1:
            sequences.append(line.strip().upper())

print(f"\nTotal sequences: {len(sequences)}")

# ---------- COUNT KMERS ----------
kmer_counts = Counter()

for seq in sequences:
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if "N" not in kmer:
            kmer_counts[kmer] += 1

print(f"Total unique {k}-mers: {len(kmer_counts)}\n")

# ---------- PRINT TOP KMERS ----------
print(f"Top {top_n} {k}-mer motifs:\n")

top_motifs = kmer_counts.most_common(top_n)

for motif, count in top_motifs:
    print(f"{motif}\t{count}")

# ---------- SAVE ALL KMERS ----------
output_file = f"top_{k}mers.txt"
with open(output_file, "w") as out:
    for motif, count in kmer_counts.most_common():
        out.write(f"{motif}\t{count}\n")

print(f"\nSaved all k-mers to: {output_file}")

# ---------- VALIDATE MOTIF ----------
if args.validate:
    motif = args.validate.upper()
    count = sum(1 for seq in sequences if motif in seq)

    print(f"\nMotif validation:")
    print(f"{motif} found in {count} sequences ({(count/len(sequences))*100:.2f}%)")
