# Final exact strong-crossbridge certificate

This package certifies every one of the 204 graph-derived one-active
wrong-split four-port K3P target directions.  Its scope is the local
cross-bridge obstruction needed to rule out a target swallowing a source
bridge in the strongly tree-child level-2 classification.

The exact partition is:

| Certificate family | Count | Target directions |
|---|---:|---|
| Strict single minor | 180 | all directions outside the residual 24 |
| Signed pair of minors | 12 | `108,110,113,114,116,120,128,175,178,180,181,184` |
| Cyclic six-minor identity | 10 | `107,111,117,119,177,183,189,190,191,192` |
| Record-43 cyclic transport | 1 | `127` |
| Record-60 cyclic certificate | 1 | `174` |

These sets are pairwise disjoint and their union is exactly
`{0,...,203}`.

## Universe and split normalization

The universe is rebuilt directly from the frozen primitive switching-mask
records.  The frozen file has 216 labelled split entries.  Exactly 12 are
common displayed splits and are removed, leaving 204 wrong-split directions.
For every remaining split, its listed two labels are placed at normalized
ports 0 and 1 and its sorted complement at ports 2 and 3.  Every resulting
old-to-normalized map is checked to be a permutation, and every normalized
split is `01|23`.  Direction keys consisting of the primitive record id and
the unordered labelled split are all distinct.

This direct labelled enumeration supersedes the old
`audit_split_automorphisms.py` calculation, including its record-60
dummy-label mapping bug.  No automorphism orbit, dummy-label transport, or
representative reduction is used in this proof.

## Independent single-minor replay

The package independently recompiles all 64 K3P Fourier coordinates for every
target from the frozen switching masks.  It imports neither the exploratory
cross-bridge module nor the frozen atlas compiler.  For all 180 single-minor
directions it reconstructs the selected `2 x 2` block minor, removes its
strictly positive monomial factor, and recomputes every tensor-Bernstein
coefficient using exact rational arithmetic.

All coefficients are nonnegative and at least one is positive.  Thus the
minor is strictly positive throughout the open edge-spectrum and inheritance
cube, and consequently throughout the K3P principal domain.  A bridge cut
would make every Fourier character block rank one and force the minor to
vanish, giving the required contradiction.

## Artifacts

- `SINGLE_MINOR_REPLAY.json` — explicit exact replay of all 180 single-minor
  certificates, including reduced polynomials and nonzero Bernstein
  coefficients.
- `UNIVERSE_CERTIFICATE.json` — all 204 normalized labelled directions and
  the exact five-way proof partition.
- `STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json` — theorem-facing aggregate and
  byte hashes for every child proof package.
- `VERIFICATION_REPORT.json` — standalone independent verification report.
- `ADVERSARIAL_MUTATION_REPORT.json` — 34 verifier mutations, all rejected.
- `build_final_certificate.py`, `verify_final_certificate.py`, and
  `run_adversarial_mutations.py` — deterministic producer, verifier, and
  adversarial suite.

## Replay

No third-party Python dependency is required.

```sh
python3 build_final_certificate.py
python3 verify_final_certificate.py
python3 run_adversarial_mutations.py
```

The aggregate is deliberately fail-closed: its status is `BLOCKED` unless all
five proof families and their required replay/mutation evidence pass.  In the
current package all dependencies pass and the aggregate status is `PASS`.
This package proves the local 204-direction cross-bridge obstruction; it does
not alone assert the complete global identifiability theorem.
