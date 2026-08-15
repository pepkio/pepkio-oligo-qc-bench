# pepkio-oligo-qc-bench

Python client for Pepkio [Oligo QC Bench](https://www.pepkio.com/tools/oligo-qc-bench) tool.

## Installation

```bash
pip install pepkio-oligo-qc-bench
```

## Usage

```python
from pepkio_oligo_qc_bench import PepkioClient

client = PepkioClient(api_key="YOUR_PEPKIO_API_KEY")

result = client.run({
    "mode": "single",
    "sequence": "GAAGGTGAAGGTCGGAGTC",
    "partner_sequence": "GAAGATGGTGATGGGATTTC",
    "preset_id": "standard_pcr",
})

print(result.result)
```
