# Independent audit packet: problem 30005078

Verdict: scoped results pass; the general module problem remains unresolved after five of five approach families.

Read AUDIT.md and CORRECTIONS.md. The original author freeze is a separate immutable input. No source material or raw corpus records are included here.

Numerical replay (Python standard library):

    python replay_audit.py /path/to/MULTIGRADED_REGULARITY_30005078_AUTHOR_SAFE_FREEZE.zip

This verifies the archive hash, extracts it into a temporary directory, reruns the author tests, confirms byte-identical author outputs, and runs the independent checker. It writes deterministic audit results beside the audit scripts. The original archive is not modified.

Optional provenance replay, with separately authorized complete source inputs:

    python verify_provenance.py PROBLEMS_JSON REPORTS_JSON CATALOG_JSON SOURCE_DIRECTORY AUTHOR_ZIP

The expected corpus hashes are tied to the pinned public dataset manifest. The source directory needs the seven PDF basenames and the software basename identified in the verifier; their contents are never emitted. This replay only rehashes those source inputs. SOURCE_AUDIT.json separately records the live inspections performed during the audit.

Files:
- AUDIT.md: mathematical, implementation and provenance findings
- CORRECTIONS.md: minor box-interface completion and provenance clarifications
- independent_checks.py: independently implemented checks
- frontier_box.py: wrapper exposing the already-proved minima box
- replay_audit.py: immutable-input author and independent replay
- verify_provenance.py: complete-input hash and record-identity checks
- INDEPENDENT_RESULTS.json, AUDIT_REPLAY.json, PROVENANCE_RESULTS.json: results
- SOURCE_AUDIT.json: public source and prior-attempt verification metadata
- AUDIT_MANIFEST.json: allowlisted distribution hashes

No external algebra system was executed. A finite test suite is not a substitute for the proof audit. No novelty, priority, or general all-frontier algorithm is claimed.
