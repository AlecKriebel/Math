# Independent audit package

Audit of the unchanged candidate for problem 4200010 / AMR-041-0010.

Verdict: PASS within its stated unrestricted smooth-symplectic and Koopman almost-periodic scope. No required proof correction. Keep `claimed_solved`, AI-assisted, unrefereed, and without a novelty claim.

Read `AUDIT.md` for the analytical and source-scope review. `AUDIT_RESULT.json` is the machine-readable finding. `AUDITED_INPUTS.json` binds all 12 candidate files, including their manifest. `SOURCE_CHECKS.json` records primary-source inspection and the raw-byte retrieval limitation. No source text, source PDFs, dataset records, or coordination files are included.

Place the original `submission` directory next to this `audit` directory, then run:

```
python3 audit/verify_audit_manifest.py
python3 audit/run_audit.py submission
```

Alternatively, run `python3 run_audit.py ../submission` from this directory. Python's standard library is sufficient. No network or candidate modification is needed. Manifest-failure tests mutate only temporary copies. The expected results are in `REPLAY_RESULTS.json` and `INDEPENDENT_CHECK_RESULTS.json`.

The audit is bound to the exact candidate hashes in its manifest. Changed proof bytes require a new review. These finite replays supplement the analytical audit and are not formal proof verification or historical-priority certification.
