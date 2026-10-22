# Independent mathematical and artifact audit

## Decision and exact scope

**ACCEPT_ORIGINAL_SCOPED_PARTIAL**, problem 2950 / KP-4.74, rank 921, unsolved after four of five allowed substantive approaches. All eight frozen author members are accepted without modification. No repair patch or derivative is required. The acceptance is for the specified reductions and diagnosis of the gap, not for a solution of the problem or a claim of novelty. This is AI-assisted and unrefereed.

The original archive is 11,204 bytes, SHA-256 `c49cd7cd07b7691f1504c99cb6e8bfa03f27c00fe94171b0730e1051a718d556`. Its external manifest is 1,632 bytes, SHA-256 `8159de4db930160353ee17c2e01ecf82d51f75a7389e3b06d771a5d98f219198`. Acceptance is bound to those exact bytes, not an unpinned working directory. The original `independent_audit: pending` value is retained as historical author-state metadata; the separate acceptance supersedes it for review status only.

## Target, categories and quantifiers

The primary K3 Problem 4.74 and its stabilization convention were checked on actual PDF page 251, including a visual inspection. The object sought is a closed smooth four-manifold and a smooth self-diffeomorphism smoothly pseudo-isotopic to the identity whose endpoint is never smoothly trivial after any allowed choice of ball-fixing isotopic representative and any finite number of S² × S² summands. Producing a difficult particular pseudo-isotopy does not suffice: the endpoint may have a different representative with zero first obstruction. Neither a relative-boundary example nor ordinary non-isotopy alone proves the required assertion.

The author's scope restriction is essential and correct. Gabai's Theorem 2.5 is explicitly for compact oriented smooth four-manifolds. K3's printed question does not explicitly assume orientation. The reduction and all negative conclusions here are confined to the closed connected oriented case; an oriented positive example would answer the existence question, while an oriented nonexistence result would leave the nonorientable case untreated. No nonorientable extension is inferred.

## Endpoint fibre and the existing obstruction

For homomorphisms e: P → E and s: P → A, where A is abelian, let J = ker(e), R = s(P), L = s(J). With e(p) = y, if e(q) = y then q p⁻¹ belongs to J and s(q) − s(p) belongs to L. Conversely, any j in J gives e(jp) = y and s(jp) = s(j) + s(p). Thus s(e⁻¹(y)) = s(p) + L. A zero-valued representative exists precisely when s(p) belongs to L. This proves the stated lemma for arbitrary groups P and E; no commutativity of P or E is used.

In the geometric application P is the smooth pseudo-isotopy group and e is top restriction. J consists of pseudo-isotopies with identity endpoint, and the first Hatcher–Wagoner obstruction is additive. Singh's inspected Section 9 already defines the endpoint quotient by Σ(J), establishes its independence of the representative, and gives the zero-representative implication in Lemma 9.3. The author expressly credits this; it is not presented as a new invariant. An isotopy trace has zero first obstruction, so the quotient depends only on the endpoint isotopy class. Projection of a pseudo-isotopy to X provides a homotopy of its endpoint to identity, verifying Gabai's homotopy assumption. Gabai's notation Diff₀ denotes homotopy to identity, not the identity component.

Applying the actual biconditional in Gabai's theorem, an oriented endpoint provides the desired separation exactly when its realized first obstruction is outside L. The obstruction takes values in the realized quotient R/L, embedded in the larger ambient quotient A/L. The author does not assert that all of A is realized on a fixed X.

## Realization is insufficient

Both algebraic countermodels are valid. For P = A = Z and s = identity, taking e to the trivial group makes J = Z and L = Z, so every endpoint has a zero representative despite surjectivity of s. Taking e to be reduction modulo two gives J = 2Z, L = 2Z and an odd endpoint fibre without zero. The same surjective realization map is compatible with opposite endpoint outcomes. These are logical countermodels, not proposed four-manifolds.

Singh's Theorem E realizes any chosen Whitehead element only after potentially stabilizing the underlying compact four-manifold. A candidate then lives on the resulting Y, and exclusion must be proved from Σ(J(Y)), not from a kernel image on an earlier manifold or merely from zero in the ambient group. The packet correctly identifies this as an unresolved geometric step. No computation of a nonzero realized quotient for an actual closed X is supplied.

## Norm quotient, sign and indeterminacy

For an abelian R with involution τ, the inclusion (1 + τ)R ⊆ L ⊆ R makes the natural map R/(1 + τ)R → R/L well defined and surjective. If τ is the identity on R, then R/L is a quotient of R/2R and is killed by two. If R itself is 2-divisible, it vanishes. More generally, surjectivity of 1 + τ on R forces vanishing. These are sufficient conditions only. A nonzero norm quotient need not give a nonzero endpoint quotient, since the inertial image L may be strictly larger than the norm image. For example, R = Z, τ = identity and L = Z give a nonzero R/2R but zero R/L.

The needed geometric hypotheses are actually supported by the inspected source. Singh's dual pseudo-isotopy construction (Definition 9.5) remains in P(X). Proposition 9.8 gives Σ(dual F) = (−1)^dim(X) times the Whitehead involution of Σ(F); in dimension four the sign is positive. Hence the involution preserves R. Proposition 9.11 puts every a + conjugate(a), for a in R, inside Σ(J), exactly the required lower inclusion. Both formulas were visually inspected because bars can be lost in extracted text. There is no asserted equality of the norm image with the inertial image, no assumed vanishing of indeterminacy, and no replacement of the realized group R by the ambient Whitehead group without justification.

Singh's Proposition 9.9 supplies a different, upper symmetry bound only when X = M³ × I. The author correctly refuses to transfer it to a general closed manifold. The secondary-obstruction discussion is accepted only in its stated endpoint-obstruction sense: raw nonzero Θ(F) for a chosen pseudo-isotopy does not itself remove its own quotient indeterminacy. In any event an endpoint possessing a zero-Σ representative is stably trivial in the oriented setting by Gabai, so such secondary ordinary-isotopy examples cannot settle this problem. No gluing-survival or smoothing theorem is silently assumed.

## Literature dependencies and review boundary

The author's three PDF sources were independently retrieved from their stated official URLs and matched in full, not just in extracted snippets. The source inspection metadata gives exact locations and byte pins.

- K3: actual page 251 and stabilization remarks checked. [Author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- Gabai: Definitions 2.1 and 2.3, Theorem 2.5, Remark 2.12, Corollary 2.13, and notation/orientation conventions checked in [arXiv:2212.02004v2](https://arxiv.org/abs/2212.02004v2). The cited theorem remains an external theorem; this audit does not re-prove all of its geometric proof.
- Singh: Theorem E and Section 9, especially Lemma 9.3, Definition 9.5 and Propositions 9.8, 9.9 and 9.11 checked in [arXiv:2111.15658v3](https://arxiv.org/abs/2111.15658v3). The publisher's public record confirms December 23, 2025 publication and August 20, 2025 acceptance. Full-text publisher access was not obtained; no equality between preprint and published theorem numbering is claimed. [Publisher record](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/topo.70043).
- Gabai–Gay–Hartman–Krushkal–Powell: the March 3, 2026 publication date, Theorem 1.1 and Remark 1.4 were independently inspected in [publisher HTML](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/pseudoisotopies-of-simply-connected-4manifolds/76BC09B6D1CF91456A4189800D2B0494). This distinguishes stabilization of a given pseudo-isotopy from stabilization of its endpoint, and is restricted to the simply-connected case.
- Galvin–Nonino: [version-pinned HTML](https://arxiv.org/html/2506.11905v1), Lemma 6.3 and Section 9 checked. Stable smoothing of specified realizations does not compute the required inertial exclusion. The Section 9 constructions use the secondary obstruction and concern ordinary isotopy.
- Lin–Xie–Zhang: [arXiv:2602.09454v1](https://arxiv.org/abs/2602.09454v1) abstract and version record independently checked; no full-text theorem audit. The stated relative mapping-class and concordance-group rank claims do not establish survival of every stabilization on a closed four-manifold.
- Additional bounded search: Orson–Powell–Randal-Williams, [arXiv:2507.16984v1](https://arxiv.org/abs/2507.16984v1), abstract and version record only. Its comparison of topological with smooth pseudo-isotopy does not by itself supply the required already-smooth pseudo-isotopy endpoint. This is contextual exclusion, not a new mathematical approach or a full audit of that paper.

This bounded review verified no solution. It is not an exhaustive novelty or current-open-status certificate. The audit does not certify correctness of every cited paper or inspect the full Lin–Xie–Zhang and Orson–Powell–Randal-Williams papers. All relevant source limitations remain explicit.

## Full input and history review

All three complete input corpora were read and rehashed: catalog 21,735,099 bytes, problems 68,931,837 bytes, research results 80,334,822 bytes. All match their expected full-file SHA-256 values. Catalog and problems each have 15,458 records; research results has 6,701 keys. Exactly one problem/candidate row has ID 2950, rank 921 and problem number KP-4.74.

The entire exact problem record, including background and literature triage, was inspected. There is no research-result key for KP-4.74, so the report part of the prescribed pair is the empty object. The full pair hash is `81b4b9cb5a480c8dfbc00462cc890d43edcc424a07568d2b642c82b731a91020`, computed as UTF-8 Python `json.dumps([complete_problem_record, report_or_empty_object], sort_keys=True)` with default serialization options. The statement hash is `2ab0530ff6f2e7e4105b1ecf66fd99fe4a853a0c95c9cd46dcae76dd1e1d1774`. The inherited material is source context and literature triage, not a substantive attempted proof or computation. This is not evidence of novelty.

Repository searches were independently repeated on default-branch code, all-state pull requests, named branches and indexed commit messages with the same identity and terminology queries. No matching prior attempt was identified; four returned pull requests under the broad word 'pseudo' concern unrelated subjects. Branch results have no continuation cursor. This bounded index search neither reads every branch file nor certifies absence from deleted or unindexed history. Only concise public search metadata is retained, not copied PR bodies or private coordination.

## Complete member and artifact assessment

Every frozen member was read and its exact bytes compared with both the separate manifest and its corresponding working copy:

1. `MATHEMATICAL_REPORT.md`: all definitions, lemma, countermodels, conditional norm argument, scope and rejected shortcuts examined above.
2. `APPROACH_LOG.md`: four substantive approaches agree with the mathematical report. Retrieval and integrity work do not inflate the approach count; no fifth approach is claimed.
3. `STATUS.json`: identity, rank, unsolved 4/5 disposition and all false solution/novelty/construction flags are consistent. Pending review is historical.
4. `README.md`: limitations, AI-assisted/unrefereed status and exclusion of source contents are accurate.
5. `SOURCE_AUDIT.json`: three PDF hashes, exact versions, publication records, inspection locations and limits checked. Source proof dependencies are not mistaken for new results.
6. `PROVENANCE.json`: all full-input pins and exact pair/statement digests independently reproduced; repository-history findings reproduced within their bounded scope.
7. `verify_packet.py`: every line reviewed. It uses explicit exceptions rather than optimization-sensitive assertions; checks strict manifest keys, exact eight-member names, member sizes/hashes, duplicate JSON keys, duplicate ZIP entries, nonregular modes, encryption, UTF-8 and scoped status. Its trusted-external-manifest requirement is real: it does not authenticate a maliciously replaced manifest by itself and does not verify theorem validity.
8. `INTEGRITY_TESTS.json`: original receipts are historical records, not proof. Independent positive replay and eight corruptions per mode reproduce the packaging claims on the final frozen archive.

The new outer verifier also pins the original ZIP and original external manifest independently of the mutable test manifests, rejects nonregular/missing/extra/duplicate members and inconsistent acceptance scope, and runs only the hash-pinned author checker from the nested archive. The portable negative-control script tests both packets under normal Python and `-O`: missing member, extra member, modified payload, duplicate member, symlink member, resealed solution claim, duplicate manifest key and bad archive hash. There are 32 rejecting CLI controls, eight per packet per mode. Positive runs and tests are repeated from relocated final artifacts. Full-input pin checks are repeated under both modes, including tampered-input rejection.

No test enumerates manifolds, verifies a finite range of a mathematical theorem, or constructs a geometric example. The finite controls establish only software packaging behavior for the tested faults. External manifests and their hashes must be independently trusted; byte integrity is not a proof of authorship, truth or publication permission.

## What remains unresolved

An affirmative solution still needs an actual closed smooth four-manifold X and smooth pseudo-isotopy F such that the first obstruction avoids the full inertial image Σ(J(X)), with the cited oriented hypotheses when using Gabai. The packet supplies neither such a geometric calculation nor a universal equality R = L. A universal negative resolution would additionally need the nonorientable case addressed. All source PDFs, extracted source text, corpus contents and private coordination are excluded from this safe artifact. No publication was performed by this audit.
