# Independent root/cut audit

This directory contains a clean-room audit of the two load-bearing claims
requested in `repair/reviews/ROOT_CUT_GATE_REVIEW.md`.

The programs here use only the Python standard library and SymPy.  They do
not import any historical project implementation.  Historical JSON and
literal certificate expressions are parsed as untrusted data.

All generated failures are retained under `failures/`; a later successful
repair does not delete or overwrite an earlier fixture.
