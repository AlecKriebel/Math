# Independent bridge/cut package

This directory is a clean-room bridge and cut-split verification package for
the landmark level-2 JC closure program.  It imports no historical project
implementation.

The package is locked to `docs/DEFINITIONS_LOCK.md` at SHA-256
`c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09`.
The full verifier fails closed if that convention file changes.

Run from the repository root:

```bash
python3 s_tc_jc_landmark_closure/independent/bridge_cut/verify_bridge.py \
  --output s_tc_jc_landmark_closure/independent/bridge_cut/bridge_certificate.json

.venv/bin/python s_tc_jc_landmark_closure/independent/bridge_cut/verify_cut.py \
  --output s_tc_jc_landmark_closure/independent/bridge_cut/cut_certificate.json
```

The second command regenerates the primitive graph universe and all exact
sign certificates; it takes several minutes on the reference machine.

To run the complete package and print all SHA-256 hashes:

```bash
bash s_tc_jc_landmark_closure/independent/bridge_cut/verify_all.sh
```

- `PROOF.md` contains the general proofs and status labels.
- `FINAL_REPORT.md` records the bounded-task verdict and exact replay hashes.
- `bridge_certificate.json` contains exact universal-factorization
  regressions.
- `cut_certificate.json` contains the complete primitive graph-to-polynomial
  chain used by the cut proof.
- `failures/` is reserved for preserved counterexamples or failed records.

The files certify bridge/no-compensation and one-sided cut preservation only.
They do not claim the final local observational-equivalence classification.
