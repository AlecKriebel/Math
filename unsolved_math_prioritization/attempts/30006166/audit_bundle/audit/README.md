# Independent wreath-product hyperfiniteness audit

The immutable author package is in `author/`. The independent review in `audit/REPORT.md` accepts the complete affirmative candidate with no required proof correction, subject to the stated AI-assisted, unrefereed status.

From any working directory, run `python3 /path/to/bundle/audit/verify.py`; `python3 -O` is also supported. Run `python3 /path/to/bundle/audit/integrity_tests.py` for isolated mutation and relocation controls. Python 3.10+ and its standard library suffice.

Verification checks exact file inventory, all payload hashes, frozen author identity, acceptance scope, original author diagnostics, and independent finite diagnostics. It is not a proof assistant and does not decide the infinite theorem.

Only authored work and public verification metadata are distributed. Primary PDFs, extracts, images, and dataset records remain excluded.
