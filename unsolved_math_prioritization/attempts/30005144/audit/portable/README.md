# CMC width audit and portable controls

Audit result: **PASS**, subject to the clearly identified imported theorem dependencies. See `PUBLIC_AUDIT_REPORT.md` for the full conclusion and credit distinction; `flat_end_rigidity.md` supplies an expanded geometric lemma.

## Run

Requires Python 3 and SymPy (tested with SymPy 1.14.0).

```sh
python independent_controls.py
python -O independent_controls.py
python verify_frozen_packet.py /path/to/the/six-file/candidate
```

The first two commands require only this program and SymPy, and must reproduce `independent_results.json`. The last command checks the six original file hashes and byte lengths recorded in `candidate_manifest.json`; it needs the unchanged candidate files, not any private freeze or PDFs. Controls fail with explicit exceptions rather than optimized-away assertions. None makes a network call or writes to the candidate.

The sixteen controls verify exact algebra/tensor identities. They do not certify geometric analysis, topology, imported theorems, or the existence of an IMCF. No source PDFs or private research data are included.
