# Portable intrinsic-invariants verifier

Run with Python 3.10 or later; no packages or installation are needed:

```text
python3 -B verify_intrinsic.py --spec construction.json
```

The program reads the supplied JSON and prints its findings. It does not write
files, import submitted code, use the network, or access private audit sources.
Its normal exit code is zero with `"status": "pass"`. The mathematical proof
and exact limitations are in `report.md`; finite controls do not certify a
universal statement or novelty.

The field control uses an odd degree extension and nonprime coefficients to
distinguish Frobenius from its inverse and detect omitted coefficient twists.
The low-rank controls include an elliptic module and a nonsplit rank-four
module with explicit duality isomorphisms. This folder is the portable public
portion of a larger audit namespace whose source copies and native receipts
remain private.
