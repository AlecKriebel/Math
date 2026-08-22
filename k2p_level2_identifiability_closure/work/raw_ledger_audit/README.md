# Independent four-port raw topology/rank ledger audit

This folder rebuilds the complete directional presentation universe from the
primitive graph encodings in the current locked compiler.  Neither
`descriptors_4.pkl` nor `rank_certs_4.pkl` is opened by the generator.

The exact primitive universe is

```text
6 sources x (831 selected-incoming + 1,983 marginalized-incoming targets)
          x 24 physical port permutations
= 405,216 directional presentations.
```

The current regenerated partition is:

```text
topology excluded             377,382
rank excluded                  23,822
retained terminal               1,472 presentations / 934 classes
restoration obligation          2,540 presentations / 997 classes
```

The topology, descriptor, exact rank, class, and raw-row censuses are
reproducible.  Every one of the 4,379 exact point-rank lower minors is now
matched to a coefficientwise symbolic upper certificate.  The independent
binder recovers all descriptors from primitive graphs, replays 3,515 base
polynomial-vector-field certificates, recovers 75 exceptional
representatives by digest, and verifies 864 exact S4 transports.  It never
opens the frozen descriptor, lower-rank, or representative pickles.  A
one-point Jacobian rank is not used as an upper bound.

Generate and structurally replay with the pinned project environment:

```bash
../../.venv/bin/python generate_raw_ledger.py
../../.venv/bin/python verify_raw_ledger.py --quick
../../.venv/bin/python test_mutations.py
```

Omit `--quick` for a clean primitive regeneration into a temporary directory
and byte comparison of the four deterministic compressed artifacts.
The adversarial suite rehashes each modified artifact and still requires the
verifier to reject omitted and duplicated raw rows, a swapped topology reason,
a false rank exclusion, reassignment to a different retained class, and a
corrupted symbolic-upper binding.
