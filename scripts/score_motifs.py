#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Score motifs by frequency in sequences")
parser.add_argument("-m", "--motifs", required=True, help="Merged motifs file")
parser.add_argument("-s", "--seqs", required=True, help="Sequences FASTA")
parser.add_argument("-o", "--output", default="scored_motifs.txt")

args = parser.parse_args()

# load sequences
seqs = []
with open(args.seqs) as f:
    for i, line in enumerate(f):
        if i % 2 == 1:
            seqs.append(line.strip())

# load motifs
motifs = [line.strip() for line in open(args.motifs)]

results = []

for motif in motifs:
    count = sum(1 for s in seqs if motif in s)
    results.append((motif, count))

# sort by count
results.sort(key=lambda x: x[1], reverse=True)

# save
with open(args.output, "w") as out:
    for motif, count in results:
        out.write(f"{motif}\t{count}\n")

print("Saved scored motifs →", args.output)
