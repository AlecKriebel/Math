# Manifest

Author: **Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol**.

All mathematical claims are provisional and unreviewed. Alec Kriebel is a
complete amateur and cannot independently verify them.

This is the canonical consolidated package. Explorations 01 and 02 are
archival provenance, not separate current papers.

## Public artifacts

| File | Purpose |
|---|---|
| `symmetric_keller_and_vanishing.md` | Human-readable research note |
| `symmetric_keller_and_vanishing.tex` | PDF source |
| `construction.py` | Six-variable and 44-variable constructions |
| `stable_reduction.py` | Self-contained 13-variable stable reduction |
| `compressed_construction.py` | 22-variable rank-compressed cubic map |
| `export_certificate.py` | Deterministic certificate exporter |
| `verify.py` | Exact SymPy verifier |
| `verify_exported_stdlib.py` | Python standard-library collision checker |
| `verify_exported_node.mjs` | Independent Node.js BigInt collision checker |
| `PRIORITY_AUDIT.md` | Source-specific priority correction and comparison |
| `output/symmetric_potential_sparse.json` | Expanded 204-term six-variable potential |
| `output/symmetric_collision.json` | Exact three-point gradient fiber |
| `output/potential_sparse.json` | Expanded 538-term 44-variable quartic |
| `output/collision.json` | Exact two-point collision for `Z-gradient(P)` |
| `../discovery_01_symmetric_monodromy/verify.py` | Exact checker for Appendix A's uniform rational collision |

## SHA-256

```text
1e0c97e1c4965c3ef7d85cdfb115d468f79d8b5195a7f34f498015c3c3f5fdd4  output/symmetric_potential_sparse.json
6b5b546f24e839a10ab330ae9b05d1d03d23a6fbbbff8cfa6d1ce742768f7169  output/symmetric_collision.json
2a912728161888849e77d607ea1f635233576543ed12d5fe8b2a65e0751789f4  output/potential_sparse.json
aeab7adb021c07dea396d2c0eca0cc7880b93dc7b09b74f60289936a711addd0  output/collision.json
```

## Exploratory record

The `search_*.py` programs record failed attempts to obtain a still smaller
graph extension, affine correction, invariant collision subspace, direct
symmetrizer, or proper gradient-closed subspace. Their negative outputs are
not mathematical impossibility theorems outside the searched ansatz.
