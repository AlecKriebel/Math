# Zero-free Dirichlet polynomial: audited partial results

**30003644 / OWR-15956-010: unsolved, five approaches used.**

The all-height question for `D(s)=1+2^(-s)+3^(-s)+5^(-s)` on `Re(s)=1`
remains unresolved. The independent audit accepts the scoped partial
results and requires no substantive correction.

- Nonvanishing for every `|t|<=10000`, independently certified with
  standard-library integer/rational arithmetic across 4,782 exact intervals
- A certified zero strictly to the right of the line, which is not a
  counterexample to the requested line assertion
- Zero infimum of `|D(1+it)|`, precluding a uniform-gap proof
- Transcendental-phase obstruction from six exponentials; complete
  nonvanishing only conditionally on Schanuel's conjecture

Read [the complete note](frozen/PROOF.md) and
[the independent audit](audit/AUDIT.md). The note credits the classical
Erdős–Ingham constructions. Yip's infinite-sequence disproof does not settle
the finite target. No novelty or priority certification is asserted.

## Verify

Python 3.12 and mpmath 1.3.0 are needed for the original replay; the independent
arithmetic verifier and adversarial tests require only Python's standard
library. No network or third-party source files are needed.

```sh
python verify_release.py
```

This checks the complete inventory and all nested manifests, exercises
strict-manifest negative controls, reruns the original and independent
verifiers, and compares all three outputs byte for byte. It re-exports
the interval leaves and compares them with the audited exact exports.
Use `python verify_release.py --integrity-only` for hashes and negative
controls without mathematical replay.

The eight original files under `frozen/` and the full audit are preserved
byte for byte. Snapshot fields such as the original pending-review status
and audit-time absence of remote writes describe those historical stages;
the accepted current disposition is stated here and in `RELEASE_BINDING.json`.

Only authored artifacts and authorized public-source verification metadata
are included. Third-party PDFs, OCR/full text, corpus contents, private
inventories, and private coordination records are excluded. This is an
AI-assisted unrefereed research checkpoint, not a full solution or a
proof-assistant formalization.
