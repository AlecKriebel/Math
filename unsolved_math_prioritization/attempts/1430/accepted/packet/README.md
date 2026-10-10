# Word-representable graphs: half-order letter-copy bound

Problem 1430 / GRAPH-043; rank 1015. Checkpoint 2026-10-08 UTC.

**Disposition: unresolved in the intended N>=4 regime after five substantive mathematical approaches.** The literal unqualified wording has elementary exceptions at N=1,2,3; these are not presented as a solution to the research problem.

Read STATEMENT_AND_STATUS.md for the exact target and scope, PROOFS.md for retained mathematics, and FIVE_APPROACHES.md / ATTEMPT_LEDGER.json for the budget and precise gaps. LITERATURE_AND_GATE.md records live duplicate reconciliation and the credited September 2026 bipartite preprint result. SOURCE_METADATA.json and CORPUS_VERIFICATION.json contain only public verification metadata, not source contents.

The bounded verifier checks 1,099 authored small-graph witnesses, 10,395 normalized six-letter double words, seven crown-plus-apex constructions, 570 twin insertions, 121 component combinations and 75 padding cases, plus arithmetic and malformed-input controls. Its expected output is DIAGNOSTICS.json. Checks use explicit exceptions, not assertions, and are intended to agree under normal Python, -O and -OO. The verification receipt outside the frozen packet records which final-byte executions actually passed.

To verify: first authenticate the separately supplied bootstrap.py and AUTHOR_MANIFEST.json against externally supplied SHA-256 pins. Then run `python -I -S -B freeze/bootstrap.py packet`. Optional -O or -OO can be inserted among the Python flags. The bootstrap checks exact inventory, file types, sizes, hashes and JSON shape before executing the pinned verifier. The manifest is external to the payload and its digest is pinned in the bootstrap; the bootstrap's own digest must come from outside this directory. Self-consistent hashes alone do not authenticate a packet. No defense against a concurrently hostile filesystem is claimed.

The authored witnesses are not copied corpus data. No source PDFs, extracts, images, source records, private coordination material, credentials or repository-write arguments are included. No remote writes, merge, release, DOI registration, outside outreach, novelty claim, or formal proof certification was performed. This corrected packet has undergone an independent mathematical and computational audit; see the accompanying AUDIT_REPORT.md for its scope and limitations.
