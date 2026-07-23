# Reproducibility Manifest

Checkpoint: 2026-07-23T18:39:53Z

Environment used:

- macOS
- Python 3.14.6
- Git 2.38.2
- no third-party Python packages

SHA-256:

```text
968b88fe00a386c81cafa5182e5b5471d099148cc1b83e8c767a168aec49ca96  certificates/d5_roots.json
af4cded5a82b4ee5a4937c59dafc1eccb23586e8a3163c18f77d61b01e2cb7be  verifiers/verify_d5.py
b32168e4095e3bded767e58a9b34afcf6a79051162468547926d92ddef9cf8f8  tests/test_verify_d5.py
```

Verification commands:

```sh
cd kissing_number_5
python3 verifiers/verify_d5.py certificates/d5_roots.json
python3 -m unittest discover -s tests -v
```

Expected verifier summary:

```json
{"boundary_pair_count": 240, "dimension": 5, "maximum_integer_dot": 1, "minimum_integer_dot": -2, "pair_count": 780, "point_count": 40, "status": "PASS"}
```
