# Independent audit bundle

Read `AUDIT_REPORT.md` for the mathematical verdict, `CLARIFICATIONS.md` for narrow wording improvements, and `AUDIT_BINDING.json` for the exact frozen input and scope.

Verdict: accept the authored packet as unresolved after five substantive approaches. No solution or counterexample is certified. The F11 pair's stable-Morita status remains undetermined; the F3 deformation pair is excluded by HH1 dimensions 8 versus 7.

## Reproduce

Python 3.8+ and its standard library suffice.

1. Run `python verify_audit.py` to verify this audit bundle's inventory.
2. Optionally bind the original packet with `python verify_audit.py --input-zip /path/to/rank668-30001222-authored-packet.zip`.
3. Run `python independent_checks.py > /tmp/rank668-independent-replay.json` and compare the result byte-for-byte with `independent_results.json`.
4. To reproduce the author's 204,097 assertions, separately unpack the original packet, run its `verify.py`, and compare with `replay_results.json`. The replay is distinct from the independent implementation.

No original source PDF, source-text extraction, dataset contents, or private coordination material is included. `source_retrieval.json` records public source titles, URLs, byte counts, hashes and inspection history. This archive does not claim human peer review or global novelty verification.
