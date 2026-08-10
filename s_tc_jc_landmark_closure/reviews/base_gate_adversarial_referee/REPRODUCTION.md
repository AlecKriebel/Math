# Reproduction

The referee uses only the Python standard library and imports no code from
`primary/` or another review directory.

From this directory:

```sh
bash verify_all.sh
```

The run should finish in a few seconds. It regenerates `certificate.json` and
`mutation_results.json` in a temporary directory, compares them byte-for-byte
with the committed copies, verifies every locked input hash, checks the two
reviewed commits exist, and validates `MANIFEST.sha256`.

Direct invocation:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 referee.py \
  --certificate certificate.json \
  --mutations mutation_results.json
```
