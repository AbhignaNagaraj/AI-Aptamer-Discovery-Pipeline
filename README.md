# AI-Assisted Aptamer Discovery Pipeline

Computational SELEX-NGS workflow for RNA aptamer discovery integrating motif analysis, RNA structure prediction, thermodynamic filtering, and protein–RNA docking.

![Pipeline](workflow/pipeline_overview.png)

---

# Project Overview

This project implements an end-to-end computational aptamer discovery workflow targeting the HPV-16 L1 protein using SELEX-NGS data and structural bioinformatics approaches.

The pipeline integrates:

- NGS preprocessing
- Variable region extraction
- Sequence normalization
- Motif discovery
- RNA secondary structure prediction
- Tertiary structure modeling
- Protein–RNA docking
- Candidate prioritization

---

# Workflow Summary

## 1. NGS Preprocessing
- Adapter trimming using fastp
- Read merging (~99.13%)
- Primer trimming using Cutadapt
- RNA conversion (T → U)

## 2. Sequence Filtering
- Length filtering (45–60 nt)
- RPM normalization
- Duplicate removal

## 3. Motif Discovery
- 7-mer and 8-mer motif extraction
- Consensus motif reconstruction
- Family-level motif analysis

Consensus motif identified:

```text
UUGAGCGUUUAUUCUUGUCUCC
```

## 4. Structural Filtering
- ViennaRNA secondary structure prediction
- MFE filtering
- GC content filtering
- Similarity scoring

## 5. Structural Bioinformatics
- RNA tertiary structure prediction using RNAComposer
- HPV-16 L1 structural preparation using AlphaFold
- Protein–RNA docking using Schrödinger PIPER

## 6. Candidate Prioritization
Top aptamer candidates selected based on:
- MFE
- RPM
- GC%
- Structural stability
- Docking interactions
- vdW clashes
- Hydrogen bonding

---

# Key Results

- Processed >121,000 candidate aptamer sequences
- Identified conserved motif families
- Generated 22-nt consensus motif
- Reduced candidates to 13 high-confidence aptamers
- Identified AHL4 and AHL5 as top docking candidates
---

# Output Files

| File | Description |
|---|---|
| final_sequences.pdf | Final filtered high-confidence aptamer candidates |
| final_aptamer_analysis.png | GC%, thermodynamic stability, and structural analysis |
| secondary_structures.txt | RNA secondary structure predictions |
| unique_aptamers.fasta | Non-redundant aptamer candidate sequences |
| consensus_motif_aptamers.fasta | Aptamers containing conserved consensus motifs |
---

# Repository Structure

```text
AI-Aptamer-Discovery-Pipeline/
│
├── scripts/
├── workflow/
├── docs/
├── data/
├── results/
├── README.md
├── requirements.txt
└── LICENSE
```

---

# Scripts

| Script | Function |
|---|---|
| manual_kmer_motif.py | k-mer motif extraction |
| discover_consensus_motifs.py | consensus motif reconstruction |
| score_motifs.py | motif frequency scoring |
| filter_mfe_structures.py | thermodynamic filtering |
| analyze_structures_final.py | GC%, MFE & similarity analysis |
| rank_final_aptamers.py | final candidate ranking |

---

# Tools & Technologies

- Python
- Linux
- FastQC
- fastp
- Cutadapt
- CD-HIT
- ViennaRNA
- RNAComposer
- AlphaFold2
- Schrödinger PIPER
- Biopython
- RDKit

---

# Future Improvements

- Dockerized workflow
- Nextflow implementation
- ML-based aptamer scoring
- Automated docking analysis