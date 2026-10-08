# Independent audit packet: S5 rank-one isotropy

Verdict: correct partial work; full smooth question unsolved after 5/5 author approaches. No mathematical correction is required and no author file was edited.

- `AUDIT_REPORT.md`: full scope, source/category review, independent reasoning for all five approaches, edge cases, and limitations.
- `ACCEPTANCE.json`: machine-readable acceptance and unsolved disposition.
- `AUTHOR_PACKET.zip`: unchanged, externally pinned original author package.
- `AUDIT_SOURCE_METADATA.json`: public scholarly-source retrieval/inspection metadata only. No PDF contents or page images.
- `CORPUS_AUDIT.json`: dataset identity and match metadata only. No dataset contents.
- `independent_checks.py` and `INDEPENDENT_CHECK_RESULTS.json`: independently authored exact group/character/matrix/fusion checks. No import of the author code.
- `ORIGINAL_PACKET_CHECKS.json`: original ZIP/inventory/replay and mutation-test results.
- `AUDIT_MANIFEST.json`: complete audit inventory, with an external pin recorded in the freeze receipt.
- `verify_audit.py`: inventory verification and normal/optimized replay of both packages.

Run `python -I verify_audit.py EXTERNALLY_RECORDED_AUDIT_MANIFEST_SHA256` in this directory, or give an absolute script path. The manifest must be pinned outside the packet; a self-contained hash is not a signature. The verifier rejects unlisted files/directories/symlinks. It creates temporary extraction files outside the packet, so verification does not modify the frozen inventory.

The scope is acceptance of the authored partial arguments. This is not a solution, a formal proof-assistant certificate, journal peer review, or an exhaustive literature search. The packet contains no copied third-party source documents, dataset contents, private sources, or coordination material. No publication was performed by the auditor.

The original author status records its historical pre-audit state. The separate `ACCEPTANCE.json` records the completed independent audit without rewriting that evidence.
