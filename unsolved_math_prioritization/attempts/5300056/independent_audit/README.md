# Independent audit packet: bounded Jacobian cocycles

Result: **scoped pass with one minor covering-proof correction**. The general holomorphic target remains unresolved; the five documented analytical routes are not a full solution.

- `AUDIT.md`: claim-by-claim independent review and limits.
- `CORRECTIONS.md`: precise old/new repair for singleton cover members in arbitrary metric spaces.
- `author_freeze/`: the nine original authored files, unchanged.
- `AUDIT_BINDING.json`: exact original archive and proof identities.
- `SOURCE_AUDIT.json`, `PROVENANCE_RESULTS.json`: source, full-corpus, review-hash and repository-check metadata only.
- `audit_checks.py`, `AUDIT_RESULTS.json`: independent exact finite controls.
- `verify_audit.py`, `AUDIT_MANIFEST.json`: closed-payload verification and replay.
- `verify_provenance.py`: optional verification using separately supplied omitted inputs.

Run:

    python3 verify_audit.py

This replays 21,193 original and 20,371 independent finite checks. They do not mechanically prove weak compactness, covering limits, or the general holomorphic implication.

Full-byte source and corpus matching was performed during the audit, but those bytes are excluded from this distributable package. Offline replay checks the included records, not the absent underlying inputs. Run `python3 verify_provenance.py --help` for the explicit-input path.

No PDFs, source extracts, images, raw corpus records, credentials, or private coordination are included. No remote write was performed. The original manuscript remains frozen; its historical unaudited labels have not been altered.
