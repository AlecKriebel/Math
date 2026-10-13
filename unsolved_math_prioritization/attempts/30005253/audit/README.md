# Portable independent audit

Target: **30005253 / OWR-11695855-006**, rank **627**.

Verdict: **Sound partial results; unsolved retained; no fatal error found.** Read AUDIT.md for independent proof checks and CORRECTIONS.md for narrowly scoped clarifications.

The immutable authored input is in `audited_packet/`. No scholarly PDF, source full text, imported catalogue, or private coordination material is included. The sources remain private; only bibliographic URLs and hashes are recorded.

Reproduce with Python 3 standard library:

```sh
sha256sum -c SHA256SUMS
python -B verify_audit.py --output /tmp/risk-audit-replay.json
cmp audit_results.json /tmp/risk-audit-replay.json
```

The optional direct-matrix simulation requires NumPy:

```sh
OPENBLAS_NUM_THREADS=1 python -B gaussian_sanity.py --output /tmp/risk-gaussian-replay.json
```

Finite exact tests and numerical simulations are not proofs of probabilistic limits. AUDIT.md separately verifies those arguments and explains why none resolves the unspecified full optimality question.
