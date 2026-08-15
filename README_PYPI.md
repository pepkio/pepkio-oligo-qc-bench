# Pepkio Oligo QC Bench

Comprehensive thermodynamic quality control library for PCR primers and oligonucleotides featuring multi-method Tm algorithms, secondary structure prediction, and 3′-end risk screening.

# What It Does

The `pepkio-oligo-qc-bench` Python package evaluates biophysical properties, melting temperatures, and secondary structures of synthetic DNA primers and probes. It identifies hazardous hairpins, self-dimers, and 3′-terminal hybridization stems to ensure robust PCR and qPCR performance across standard and high-fidelity buffer conditions.

# Features

- **Multi-Method Tm Prediction**: Computes Wallace rule, SantaLucia 1998 unified nearest-neighbor, and Owczarzy 2008 salt/divalent cation-corrected melting temperatures.
- **Buffer & Cosolvent Modeling**: Accurately simulates $\text{Na}^+$, $\text{Mg}^{2+}$, dNTP chelation, and DMSO (0–20%) effects on duplex stability.
- **Secondary Structure Thermodynamic Scan**: Quantifies hairpin, homodimer, and heterodimer folding free energies ($\Delta G$ at 37°C).
- **3′-End Risk Assessment**: Automatically flags stable 3′-terminal secondary structures ($\Delta G < -2.0\text{ kcal/mol}$) prone to primer-dimer extension.
- **Biophysical Property Calculator**: Determines single-stranded DNA molecular weight, GC content, and sequence-specific UV extinction coefficients ($\varepsilon_{260}$).
- **Polymerase Buffer Presets**: Standard Taq, qPCR Master Mix, Q5/Phusion High-Fidelity, and Custom buffers.
- **Batch Processing & CLI**: Evaluate single primers, forward/reverse pairs, or batch lists up to 50 oligonucleotides via Python or the command line.

# Installation

```bash
pip install pepkio-oligo-qc-bench
```

Or using `uv`:

```bash
uv add pepkio-oligo-qc-bench
```

# Quick Example

```python
from pepkio_oligo_qc_bench import PepkioClient

with PepkioClient() as client:
    # Evaluate a primer pair in Standard PCR buffer
    qc = client.run({
        "mode": "single",
        "sequence": "GAAGGTGAAGGTCGGAGTC",
        "partner_sequence": "GAAGATGGTGATGGGATTTC",
        "preset_id": "standard_pcr"
    })

    primer = qc.result["single"]
    print("Primer:", primer["sequence"])
    print("Owczarzy Tm (°C):", primer["tm_owczarzy"])
    print("GC Content (%):", primer["gc_pct"])
    print("3'-End Risk Level:", primer["risk_level"])
```

# Typical Use Cases

- **PCR & qPCR Primer Validation**: Verify primer Tm matching, GC content, and secondary structure stability prior to synthesis.
- **Multiplex PCR Cross-Dimer Screening**: Screen multiplex primer pools against heterodimer formation to eliminate non-specific amplification.
- **High-Fidelity Reaction Optimization**: Predict accurate annealing temperatures in Q5 or Phusion buffers with added DMSO.
- **NGS Adapter Quality Control**: Screen custom barcoded sequencing adapters for inhibitory hairpin structures.

# Scientific Background

Melting temperature calculations rely on SantaLucia (1998) unified nearest-neighbor enthalpy ($\Delta H^\circ$) and entropy ($\Delta S^\circ$) values. Salt and divalent magnesium adjustments are modeled using Owczarzy (2008) parameterizations, accounting for competitive dNTP chelation of $\text{Mg}^{2+}$. Secondary structure folding free energies ($\Delta G$) are computed at 37°C; structures overlapping the last 5 nucleotides of the 3′-hydroxyl terminus with $\Delta G < -2.0\text{ kcal/mol}$ are classified as high-risk elongation hazards.

# Web Application

For graphical primer analysis, interactive buffer adjustment, and printable worksheets, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/oligo-qc-bench

# Documentation and Resources

- GitHub Repository: https://github.com/pepkio/pepkio-oligo-qc-bench
- Web Application: https://www.pepkio.com/tools/oligo-qc-bench
- PyPI Package: https://pypi.org/project/pepkio-oligo-qc-bench/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

oligo QC, PCR primer Tm calculator, SantaLucia nearest neighbor, Owczarzy salt correction, primer hairpin delta G, primer dimer analyzer, 3-prime end stability, oligo molecular weight, primer extinction coefficient, qPCR primer design, Taq annealing temperature, Q5 buffer Tm, Phusion buffer Tm calculator, DMSO primer Tm adjustment, dNTP magnesium chelation, primer heterodimer screening, degenerate primer Tm, IUPAC primer analysis, DNA duplex thermodynamics, Wallace rule calculator, nmol per OD260, ssDNA MW calculator, multiplex PCR primer QC, primer dimer prevention, high-fidelity PCR optimization, reverse transcription primer QC, synthetic DNA quality check, primer GC percentage, amplicon design tools, NGS adapter secondary structure
