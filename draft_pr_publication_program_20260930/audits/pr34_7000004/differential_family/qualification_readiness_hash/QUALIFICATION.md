# Additive correction: withdraw the readiness hash-role finding

The closed differential-family report's mandatory integration issue3 is **falsified and withdrawn**. I assigned the wrong meaning to `readiness.json`'s `review_hash`. That field binds the complete upstream raw problem record and its separate upstream research report. It does not bind the independent review Markdown document. The original readiness value is correct and must remain unchanged.

The actual repository importer in `unsolved_math_prioritization/queue.py`, function `score`, defines

    review_hash = SHA256(json.dumps([p,r], sort_keys=True).encode())

where p is the full raw upstream problem record, r is its full separate report, and Python JSON serialization uses its default ASCII escaping and spaced separators. `show` reproduces the same ordered-pair hash, and the v2 merge importer uses the same definition. The independent review document is bound separately by `review/verdict.json`'s `review_sha256`.

The independently repeated actual source/importer check gives:

| Binding role | Verified SHA-256 |
| --- | --- |
| Original readiness source-pair `review_hash` | `2e49912828f018ce3f85114143f107c8b3315172c5e5538a6231c128efb1d086` |
| Original independent review document `review_sha256` | `0d8a579e9273e3bd7e5bc170b7964b2754a0404896c35dc47e1512e4f46326a0` |
| Literal raw statement `statement_hash` | `3fba262110a123ef34d75b5cac921d5d24b3964782b23c2618a9725ed6f04d93` |

Fresh downloads of both complete pinned source files at revision37e53eabe540fb458758e198be61634bd02ee008 passed exact manifest byte-count/hash checks: problems.json68931837 bytes SHA04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf; research_results.json80334822 bytes SHA8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. The complete15458-record problem corpus contains exactly one numeric7000004 and exactly one AMR-069-0004 code. Its full raw record and separately selected report structurally match the frozen original source_record.json and prior_report.json, including all source metadata and triage fields.

`verify_hash_roles.py` actually imports the current queue module and calls its pure `score(p,r,policy)` function. It independently hashes the exact serialized pair and proves agreement with original readiness. It separately hashes the final independent review document and proves agreement with original verdict. No sync, rank, show, status, connect or shared mutation is invoked. Seven concrete binding/serialization controls distinguish the roles: changing raw source, changing/deleting report, changing only the review document, substituting the review-document hash into readiness, compact JSON serialization and reversed source-pair ordering.

The old report's issue3, the stale-hash characterization in ORIGINAL_INTEGRITY.json, and the03:44 closed research-log statement must now be read under this qualification. The numeric values in the old comparison were real; the assigned semantic role and claimed mismatch were wrong. Do not overwrite2e499128... with0d8a579e... in original or current source-pair readiness bindings. Both original source-pair and review-document bindings are valid.

The original closed24 members and MANIFEST.json remain byte-identical. This qualification is a separate additive record preserving the falsified historical finding. No mathematical proof, countermodel, scientific outcome or original-attempt accounting changes. The root's cumulative2/5 count is unaffected, and these checks add0 research attempts. The fresh whole-current gate should explicitly test the two hash roles independently.

To reproduce, run this qualification's program in a private copy with `--repo` pointing to the copied repository and `--problems`/`--reports` pointing to the two complete pinned files. It writes only RESULTS.json in its own qualification directory. The downloaded corpus is ignored source material, not an authored contribution or redistributed package member.
