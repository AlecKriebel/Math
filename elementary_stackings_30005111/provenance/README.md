# Publication preparation provenance

The authored Python generators were copied and each AST Assert(test, msg) replaced by If(Not(test), Raise(AssertionError(msg))). Condition expressions and control flow are preserved; ast.unparse reformats source and removes comments. Unified patches and original/publication hashes record the exact changes. The independent cochain validator is separately authored, assertion-free, and copied verbatim after its final review.

Original normal execution passed, but original optimized execution would remove assertions and is not validation evidence. Publication normal and -O replay outputs are retained. The backtracking receipt remains byte-identical to its independently audited original.

The backtracking audit reproduction command was changed from a workspace-relative research path to package-relative audit/independent_backtracking/verify_ababa.py. Its original script hash is explicitly labeled historical. SOURCE_GATE.md preserves the source interpretation and historical pending gate while replacing its local preservation paragraph with public metadata-only publication wording. SOURCE_METADATA.json includes only public PDF identity/hash/size/URL and inspection history. No copied PDFs, source extracts, rendered source pages, dataset contents, or private coordination files are shipped.

The README, acceptance report, manifest verifier, and serialized-certificate validator are newly authored packaging artifacts. Replay outputs are regenerated from the publication scripts, not copied claims of execution.
