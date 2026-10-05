# Independent audit: monotone gradient distance

Problem 30005995 · OWR-14298587-010 · rank 803 · 5 October 2026

## Verdict

**PASS as an unresolved, five-approach partial-results packet.** No fatal mathematical error was found in Propositions A–E or in conditional Theorem F. The unrestricted distance-continuity problem is **not solved or disproved**. The conditional theorem requires every blow-up at the singular point to be differentiable at every nonzero point; this requirement is not established in general.

The mathematical addendum supplies a complete local compactness/flux-passing argument, spells out the all-blow-ups quantifier, proves the continuous-representative consequence, and clarifies the finite-bad-set citation. These are explanatory strengthening and scope precision, not a claim to have closed the original gap. The author freeze remains byte-for-byte unchanged.

## Material findings

1. **Nonlinear compactness is justified.** Locally uniform convergence plus equi-Lipschitz bounds does not by itself pass a nonlinear flux. Here, testing differences of solutions and using strict monotonicity away from the diagonal proves strong local gradient convergence and strong local flux convergence. No quantitative ellipticity is inserted.
2. **The flatness estimate is strong enough.** The cited March 2026 estimate controls essential gradient suprema for every slope. Its threshold is fixed before taking the approximating index large. This supports the moving-witness proof rather than an average-to-uniform shortcut.
3. **The extra hypothesis must retain both universal quantifiers.** A single regular blow-up is insufficient for the contradiction argument, and an H¹-negligible singular set does not rule out the selected off-center limit point.
4. **Representatives are handled correctly after clarification.** At the global level, use the derivative at differentiability points and assign distance zero at singular points. The addendum proves actual continuity of this representative. Arbitrary null-set modifications are not continuous by fiat.
5. **Bad-set and exclusion calculations check out.** The reciprocal denominator, closures, skew example, failure of uniform strict contraction, two-state obstruction, ridge rigidity, and equal-trace uniqueness are correctly scoped. The cited finite-set theorem uses the closed bounding gradient ball.
6. **The spike is a valid control, not a PDE counterexample.** Its W¹,² energy, vanishing density, positive-area height-one plateaus, and failure of every continuous representative are all consistent. It blocks a generic inference, not the conjecture.

## Source and identity verification

- The author archive has 13,801 bytes and SHA-256 fac2c25e4ee91ba0dbf2c930151705894447b22bbe29ce05a82f32becb88d9cb. All seven archive entries match the author manifest/receipt.
- All 22,185 author assertions reproduce unchanged. A separately written checker passes 40,249 further controls, including five coefficient-level symbolic polynomial identities and differently parameterized exact rational tests.
- All three full supplied corpora were read and hashed. They contain 15,458 catalog records, 15,458 problem records, and 6,701 research-result records. ID, number, title, source URL, statement hash, and the complete-record review hash match. No target research-result record was found. Raw records are not included.
- Review SHA-256: 7c925aa681287218956181c440c73f3822612bad00ad0967eaf9b7d9a0dce8ba. Its serialization is recorded and replayable in the metadata and optional identity verifier.
- The official OWR report and all three cited arXiv PDFs were freshly retrieved as full files. Every PDF byte count and digest matches the author evidence. OWR printed pp. 2138–2139 were visually inspected; they are PDF pages 26–27.
- Lacombe's January 2026 result establishes approximate continuity/localization; the source explicitly retains the continuous-representative issue. Lamy–Tione v2 is dated 31 March 2026 and provides the flatness input, with stronger curve-dependent conclusions. No unrestricted resolution was located in the bounded current search.
- The publisher still lists the Lacombe–Lamy paper as forthcoming in Analysis & PDE. The author homepage lists it among preprints. This is public status metadata, not acceptance of the proof of the present conjecture.

## Prior-attempt search limitation

Fresh GitHub code, PR, and branch searches returned no exact-target mathematical attempt. The root and problems-directory listings showed no exact-target entry. The connector's recursive-tree request failed with a transport error; a public read-only HTTP fallback returned 38,609 tree entries with `truncated=true` and no target candidate. Consequently this is a bounded negative search, not an exhaustive history certificate. The original report's conservative limitation remains appropriate; no skip was triggered.

## Release scope and acceptance boundary

The audit ZIP contains authored mathematical reports, exact verification code and results, public verification metadata, and the unchanged safe author payload. It contains no source PDFs, source extracts, images, raw corpora, private sources, credentials, or private coordination files. No remote writes were performed.

Run `python verify_audit.py` in the extracted audit directory. It verifies exact membership and hashes, checks the frozen author's original verifier, and reproduces both finite result sets. Optional corpus identity verification requires separately supplied full corpus files and never emits their records.

This is a mathematical/release-scope review, not a formal proof certificate, a novelty opinion, or manuscript publication approval. Imported literature proofs are not formally verified. Acceptance applies only to the honest unresolved packet and its explicitly conditional statements.
