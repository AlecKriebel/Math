# Independent mathematical and artifact audit: KP-1.65

Date: 6 October 2026. Problem ID 2724; rank 905.

## Decision

Accept the corrected derivative as a bounded local diagnostic and a source-scope audit. Keep the problem **unsolved**, with **one mathematical attempt out of five**. The argument establishes a specific gap in automatic Morse slicing. It provides no global decomposition theorem, no counterexample to KP-1.65, and no novelty claim.

The author's immutable input was not accepted verbatim: the realization-theorem summary omitted a nonempty-end hypothesis and the elementary-piece terminology could be read as asserting that an arbitrary literal Legendrian-isotopy trace is already Lagrangian. Those precision issues are repaired in an actual, replayed correction patch. Neither changes the local calculation or the unresolved conclusion.

Exact artifact identifiers, rather than filenames alone, determine acceptance. See EXACT_ACCEPTANCE.json. The author ZIP and its external manifest retain their original bytes. The corrected ZIP has nine authored files, and its external manifest binds every member. No repository or queue mutation, publication, human peer review, or formal proof-assistant certification is claimed.

## 1. Independent reconstruction of the local proof

Use coordinates (t,x,y,z), with alpha = dz - y dx, lambda = exp(t) alpha, and omega = d lambda. The author fixes all of these conventions explicitly; in particular the coordinate named y is not confused with the height t.

For F(s,u) = (s,u,s,(s+1)u), projection onto (t,x) recovers (s,u). It follows that F is injective, is a smooth immersion, and has a continuous smooth inverse on its image. Thus it is an embedding, not merely an immersed parametrized surface.

The tangent vectors are F_s = (1,0,1,u) and F_u = (0,1,0,s+1). Direct evaluation gives alpha(F_s) = u and alpha(F_u) = 1, hence F*alpha = u ds + du. Multiplication by exp(s) gives exactly d(exp(s)u). The primitive is globally defined on the parameter plane. Differentiating proves F*omega = 0; the embedded surface has dimension two inside a symplectic four-manifold, so it is Lagrangian. As a cross-check, omega/exp(t) = dt wedge alpha - dy wedge dx evaluates to 1 - 1 = 0 on (F_s,F_u).

The restricted height is exactly s, and its differential is ds, which never vanishes. There are no height-critical points of any index. On a fixed level s=c, the projected curve is (u,c,(c+1)u), and its tangent evaluates to 1 under dz-y dx. The curve is therefore nowhere Legendrian. Its primitive exp(c)u is correspondingly nonconstant.

For the general criterion in the authored proof, a fixed-height projection is a diffeomorphism from the ambient level to contact three-space. On a tangent vector to that level, the relation i*lambda = df gives alpha(d(pi composed with i)(v)) = exp(-c)df(v). The contact tangent condition is thus equivalent to vanishing of df along the slice. On each connected smooth component of a regular level, this is equivalent to constancy of the primitive. The regular-value and connected-component qualifications are both necessary and are both present.

This is a symbolic proof for all real parameters. It does not depend on the finite executable checks.

## 2. Exactly what the example does and does not establish

The example disproves the inference from local exactness plus regular height to automatically Legendrian height slices. It is not a cobordism between compact cylindrical Legendrian ends: its fixed-height sections are noncompact, non-Legendrian lines. Consequently it is not an example in the global class quantified over by KP-1.65.

A bad slice of one representative also does not obstruct deforming that representative to another with useful slices. The audit therefore must not infer nondecomposability, nonregularity, or failure of Lagrangian isotopy from this calculation. The authored text explicitly avoids all three inferences.

The remaining gap is geometric: one needs Legendrian intermediate levels and the permitted elementary exact pieces with compatible primitive conventions and a justified Lagrangian-isotopy conclusion. Smooth Morse decomposition alone supplies none of those additional conclusions. The local diagnostic does not establish that this gap is impossible to close.

## 3. Primary-source review and repairs

The accompanying PRIMARY_SOURCE_REVIEW.md records the detailed independent scope review. The primary K3 book, rather than the unrelated four-page AIM workshop summary, supports the exact/no-index-2/Lagrangian-isotopy formulation. All seven retained source PDFs were independently checked against their declared SHA-256 values and byte counts.

The corrected derivative makes these changes:

1. State the nonempty negative-end hypothesis of Etnyre–Leverson Theorem 1.2 and the two nonempty-end hypotheses of Question 1.8. Their smooth realization after stabilization remains insufficient for the prescribed unstabilized Lagrangian-isotopy problem.
2. Describe the Lagrangian concordances associated with Legendrian isotopies rather than unqualified literal traces. Section 4, footnote 1 of that source explains the needed perturbation.
3. Replace the direct K3 question quotation with an authored paraphrase preserving the mathematical quantifiers and assumptions.
4. Record that Guadagni's exhibited construction has a splitting saddle followed by a cap. This shows an index-2 point in the displayed movie; it is not asserted to prove an obstruction for every isotopic representative. The general move theorem's possible nonexactness remains separately stated.
5. Update review-status prose and STATUS.json without changing the local verifier, attempt count, or unresolved outcome.

Golovko–Komarek v3 was also checked through its version-pinned HTML and retains the positive-index-2 obstruction. The original v2 PDF provenance was not relabeled. The source review distinguishes stronger non-ribbon obstructions from merely nonregular examples and does not conflate smooth, Lagrangian, exact-Lagrangian, and Hamiltonian isotopies.

Neither the source review nor this acceptance constitutes a dependency-by-dependency proof audit of the cited papers or an exhaustive current literature search. The original report's bounded GitHub history observations are historical metadata; they were not independently rerun as part of this acceptance and are not novelty evidence.

## 4. Corpus and inherited-work verification

The catalog, problems dataset, and research-results dataset all match the published verification metadata's full-file byte counts and SHA-256 values. The exact catalog record is rank 905 and ID 2724. The statement digest matches d00667dd787ea2d394581482f57d04bea21b732e712611f06aafb3290bf98214.

The entire problem record and entire associated report were inspected. The report defaults to the empty object. Serialization with json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True), Python's default separators and escaping, and UTF-8 gives 72311e16f13d244065f389ce503a5af85376238d8f1e482695b41ace714c0b59. This matches the catalog and author metadata. The record contains literature triage, not a prior mathematical proof attempt. Removing a record field, altering the report, or changing to compact JSON serialization changes the digest; the review did not hash a truncated selection of fields.

Only public verification metadata is in the audit deliverable. Dataset rows, source documents, extracted text, and private coordination are excluded.

## 5. Executable and adversarial replay

The author's rational-polynomial verifier is unchanged by the correction. Its 135 checks pass under normal Python, -O, and -OO, including execution from an unrelated working directory with the script relocated and renamed. An independent direct call to its false-premise guard fails under all three interpreter modes.

Five semantic mutations are each rejected in all three modes: incorrect local y, incorrect local z, wrong symplectic sign, a false Legendrian-slice assertion, and an insufficient condition for the parameter family. Four artifact-integrity controls also fail as intended: archive byte corruption, an unexpected archive member, an altered internal digest, and a consistently rehashed false full-solution status.

Erasing the verifier's guard is a different threat model. A self-disabling program cannot be trusted to detect its own disablement; the independent pinned-byte check rejects that change. The replay does not claim semantic self-rejection for that mutation.

The auxiliary family has y=A s and z=B s u+C u. Independently differentiating gives the coefficient of F*omega/exp(s) as (B-A)s+(C-A), which vanishes identically exactly when A=B=C. The finite test grid is consistent with this identity, but the grid alone is not a proof for all coefficients.

The complete independent harness was itself run under normal Python, -O, and -OO for both the author and corrected archives, including the full corpus and PDF pin checks. Its JSON results are identical across optimization modes for each artifact. The patch was applied to a fresh author extraction; after deterministic internal-manifest regeneration, all nine resulting files exactly match the corrected derivative. See PATCH_REPLAY.json and OPTIMIZATION_REPLAY_SUMMARY.json.

## 6. Acceptance boundary

Accepted: the embedded exact local example, primitive-constancy slice criterion, automatic-slicing gap, corrected primary-source scope comparisons, and the exact artifact and replay results identified in the acceptance receipt.

Not established: a global collaring theorem, normalization of arbitrary saddles, a Lagrangian isotopy to a decomposable cobordism, any no-index-2 global counterexample, novelty, exhaustive status, or a resolution of KP-1.65. The correct task disposition remains unsolved / stalled partial, 1/5 attempts.
