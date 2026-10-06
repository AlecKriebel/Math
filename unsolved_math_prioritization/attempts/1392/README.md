# Graph coloring game monotonicity: audited bounded partial

Problem **1392 / GRAPH-005**, rank 880. Queue status: **unsolved, 4/5 approaches**. Result status: **PARTIAL**. The general question remains unresolved by this package.

The original Alice-first proper vertex-coloring game is used, with no passing or recoloring. The accepted deductions are:

- Palette monotonicity for disjoint unions of complete multipartite graphs, including singleton parts and arbitrary component interleavings.
- A sufficient reservation bound: if twice the number of vertices of degree at least q, minus one, is at most q, Alice wins with q colors.
- No palette-monotonicity counterexample on at most five vertices, with necessary degree/colorability restrictions for any counterexample.

No general counterexample, least-counterexample result, winning-palette characterization, novelty, or priority is claimed.

## Proof and independent review

- [Unchanged original proof](author/PROOF.md), [four approaches](author/APPROACHES.md), [claim boundaries](author/STATUS.json)
- [Full independent mathematical audit](independent_audit/audit/AUDIT.md) and [exact acceptance](independent_audit/audit/ACCEPTANCE.json)
- [Source metadata](author/SOURCES.json), [independent source inspection](independent_audit/audit/SOURCE_VERIFICATION.json), [provenance replay](independent_audit/audit/INTEGRITY_REPLAY.json)
- [Publication metadata](PUBLICATION_METADATA.json), [static test results](PUBLICATION_TEST_RESULTS.json), [inventory](PUBLICATION_MANIFEST.json)

The independent audit accepted the original six-member author freeze unchanged. The original author and twelve-member audit ZIPs and their external manifests are preserved in `archives/`; every member is unpacked byte-for-byte. No correction patch or corrected derivative was needed or fabricated. Frozen no-publication fields record their historical stage and remain unchanged.

The numeric ID is essential: GRAPH-005 is duplicated in the source corpus. ID 1392 was selected uniquely; the missing report-map key gives the prescribed empty-object default. All three complete input-file pins and the exact complete-record/report-pair digest were rechecked. Corpus contents are excluded.

Zhu's original source was inspected only through indexed introduction pages, not an acquired full PDF. Hollom's published paper and the Obszarski–Turowski–Zięba v2 PDF have matching stored bytes and public hashes. Hollom's ordered 3-to-4 result is not a counterexample in the original game. Other recent sources retain their stated abstract/HTML-only limits. The literature and repository searches are bounded; no exhaustive-current-literature guarantee is made.

Normal and optimized isolated Python runs check byte integrity, inventories, archive safety, provenance and acceptance bindings, with negative controls. They do not certify the mathematics. No game-state computation, heuristic play, executable mathematical certificate, formal verification or conventional human peer review is claimed. The mathematical basis is the written proof and independent AI-assisted audit.

Only the target row's Status and Turns cells change in QUEUE.md. All other queue bytes, existing notes and chat links are preserved. No source documents, source text/images, dataset contents, private material or checker fingerprints are published. This is a draft-PR package, with no merge, release, DOI or outreach. No CI-pass claim is made.
