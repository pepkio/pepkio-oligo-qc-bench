# pepkio-oligo-qc-bench

Python client for Pepkio [Oligo QC Bench](https://www.pepkio.com/tools/oligo-qc-bench) tool.

## Installation

```bash
pip install pepkio-oligo-qc-bench
```

## Quick Start

```python
from pepkio_oligo_qc_bench import PepkioClient

client = PepkioClient(api_key="YOUR_PEPKIO_API_KEY")

# Fetch tool manifest
manifest = client.get_manifest()

# Run single-oligo QC
result = client.run({
    "mode": "single",
    "sequence": "GAAGGTGAAGGTCGGAGTC",
    "partner_sequence": "GAAGATGGTGATGGGATTTC",
    "preset_id": "standard_pcr",
})

print("Status:", result.status)
print("Result:", result.result)
```

## CLI Usage

```bash
# Get manifest
pepkio-oligo-qc-bench manifest

# Run example
export PEPKIO_API_KEY="YOUR_API_KEY"
pepkio-oligo-qc-bench run --example single_standard_pcr
```
