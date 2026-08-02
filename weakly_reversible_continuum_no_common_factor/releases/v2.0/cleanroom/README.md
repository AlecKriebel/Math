# Clean-room verification

This directory contains an independently written exact verifier for the
frozen v1 construction and a separate audit of the structural proofs.

From the repository root, run:

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/cleanroom/verify_v1_cleanroom.py
```

The verifier requires Python and SymPy.  It uses exact integer and rational
arithmetic only.  It imports no project code and does not read the original
verifier.  The off-conic component is rediscovered by saturation, and the
claimed decomposition is replayed by an independent ideal-intersection
elimination.

Files:

- `verify_v1_cleanroom.py`: executable checks 1–17;
- `PROOF_AUDIT.md`: proof-level checks 18–20 and supporting algebra for the
  field-extension, positivity, and radical claims;
- `AUDIT_RESULTS.md`: explicit PASS/FAIL disposition for all twenty checklist
  items.
