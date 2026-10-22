# PR 764 independent priority audit

Read `REPORT.md` for the verdict, chronology limits and mandatory publication
credits. `COMPARISON_DERIVATION.md` contains the auditor's mathematical checks;
`THEOREM_COMPARISON.json` fixes the exact scope map. The public receipts retain
bibliographic metadata, URLs and hashes, not third-party source bodies.

Offline artifact verification:

```sh
python3 verify_manifest.py
```

The verifier uses explicit checks even under Python optimization. It validates
this folder's complete authored-file inventory and the frozen proof identity
when that repository input is present. It does not rerun a literature search or
certify priority. `read_registry.py` is an optional network-based method record;
live results can change and must not overwrite a historical receipt for a
published audit. No credentials, messages or registry writes are used.

No PR, queue, branch, index, Zenodo or spreadsheet mutation occurred in this
auditor. Only the dedicated `priority_audit` folder was written. Private
read-only downloads/renderings were removed after completion. This review was
performed with AI tools; it is not human peer review or proof-assistant
certification.
