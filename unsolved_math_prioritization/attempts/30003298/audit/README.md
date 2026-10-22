# Independent review package

The independent review accepts the frozen top-degree theorem and the exact genus-two answer without a mathematical correction patch. The general question remains unsolved after five approaches. This is AI-assisted review, not human peer review or formal proof verification.

- `REPORT.md`: complete mathematical audit and source qualifications.
- `ACCEPTANCE.json`: precise accepted scope and review limits.
- `independent_verify.py`: independent source-free frozen-hash and finite diagnostic checker.
- `test_independent.py`: normal, -O, and -OO replay, actual read-only relocation, 40 hostile mutations per mode, and replay of the author's separate test harness.
- `CONTROL_RESULTS.json`: full observed test results.
- `AUDIT_MANIFEST.json`: hashes and byte counts of the review files.

Keep this `audit` directory beside the unchanged `public` author directory. From their common parent, run:

    python -B audit/independent_verify.py
    python -O -B audit/independent_verify.py
    python -OO -B audit/independent_verify.py
    python -B audit/test_independent.py

An explicit path to the frozen author packet can alternatively be supplied to `independent_verify.py`. The test harness uses the sibling `public` directory and writes only to temporary directories. None of these checks requires the dataset or scholarly PDFs. The exact original manifest digest is pinned in both the acceptance record and the independent checker.

The mathematical argument, including the limitations of its imported theorems, is evaluated in the report. Successful executable checks alone do not prove the theorem. The source-free archive includes only the original public packet and these review files.
