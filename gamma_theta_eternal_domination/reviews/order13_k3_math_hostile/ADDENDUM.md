# Revised-byte addendum

**Verdict:** `ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED`

The four documentation-only replacements recommended in `REVIEW.md` were
applied exactly.  No mathematical byte changed.

The revised files are:

| file | bytes | SHA-256 |
|---|---:|---|
| `math/lemmas/order13_k3_synthesis_target.md` | 26,303 | `7bec13620961adeaf61c60e88c8bc9366beecab7387e40c80083fe702484ab39` |
| `math/lemmas/order13_k3_hole11_exclusion.md` | 16,330 | `511432d00f43f602fd906b3b5e37ae0e5c85cbc1523bcd63c5b668a00f0d53f8` |

The addendum checker reverses the two replacements in each file.  The
resulting byte strings exactly reproduce the previously accepted sizes and
hashes:

| file | reconstructed bytes | reconstructed SHA-256 |
|---|---:|---|
| synthesis note | 26,112 | `02c661edf61db8f4b4a5769972e726ce8c1c693e418c1b97b2293e68765e0f44` |
| hole theorem | 16,303 | `ee492ff314ac2df5f9e1e80982c9bd455dcbce30106d54083d0cd7a930627408` |

This establishes the diff scope byte-for-byte, rather than relying on a
line-oriented comparison.  The original audit artifacts also retain their
frozen hashes.  The addendum re-executes all eleven independent mathematical
and finite-regression sections from the original clean-room checker; every
result remains identical to the frozen evidence.

The repaired wording now:

- distinguishes the abstract CNF theorem from the separately accepted
  constructor;
- records that the hostile mathematical review has passed;
- binds the independent regression checker by artifact path; and
- preserves all solver, certificate, remaining-branch, and parameter-slice
  limitations.

Three mutations—deleting or duplicating a revised block and altering a
mathematical byte elsewhere—are all rejected.

## Replay

From the campaign directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
  python3 -W error reviews/order13_k3_math_hostile/addendum_audit.py |
  cmp - reviews/order13_k3_math_hostile/addendum_evidence.json
```

This addendum transfers the frozen hostile mathematical acceptance to the
revised theorem-note bytes.  It makes no new theorem, novelty, solver, UNSAT,
certificate, or runner claim.

| artifact | bytes | SHA-256 |
|---|---:|---|
| `addendum_audit.py` | 12,336 | `51f070e3ecb653a3381603a09f78e5ce43540eac49a3d95e0ec106e789ea8cc2` |
| `addendum_evidence.json` | 3,456 | `e45d99d880af6350034d7ee9a4b83acb30cc4706c9aa4445d97a07a272d3dc14` |
