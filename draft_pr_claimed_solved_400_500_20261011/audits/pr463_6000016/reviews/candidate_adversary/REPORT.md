# Fresh whole-candidate adversarial review

Reviewer `/root/pr463_candidate_adversary`; eligible frozen PR 463 head `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`; problem 6000016 / AMR-059-0016. Final review sealed 2026-10-12T16:13:46.152082+00:00. The entire final priority-family package and proposed DISPOSITION_SYNTHESIS.md have been read. This is a whole-candidate mathematical/priority review and a conceptual check of the proposed status disposition; it is not an operational-helper audit or a preprint/package review. Original proof-search attempts: 0.

## Independence and source interpretation

INITIAL_INTERPRETATION.md was written before reading the supplied proof, historical audit, root claim ledger or new peer reports. I then independently downloaded and visually inspected the original question p. 126 and Baues–Goldman v2 p.20, reconstructed the family and arbitrary-metric Stokes argument, and recorded INDEPENDENT_RECONSTRUCTION.md. Only afterwards did I read PROOF.md, CLAIM_LEDGER.md, the historical full audit and the new mathematical-family reports.

The original universal assertion permits a compact locally Hessian Riemannian central manifold and asks for some Hessian metric on every sufficiently small affine deformation. Its separately known hyperbolic case imposes a developing domain containing no full line; the unrestricted question has no such condition, fixed-holonomy condition or excluded dimension. The whole-plane affine torus falls within the unrestricted question. A single family with arbitrarily small noncentral members lacking every positive Hessian metric disproves the universal assertion; it need not classify every deformation or construct a smoothly varying family of metrics.

The source definition is local. A single global real-valued strictly convex function on a compact manifold would be impossible and is not a hidden requirement. Smoothness of the developing maps/affine atlas, rather than differentiability in an additional normalized period coordinate, suffices. The cubic reparameterization meets even the latter smoothness condition while preserving arbitrarily small counterexamples.

## Direct mathematical falsification attempts

For the global torus frame X,Y, the candidate connection has D_X X=tY and all other frame derivatives zero. The difference from the standard connection is a tensor, so it is globally meaningful although x,y are only angular coordinates. Constant coefficients and the nilpotent connection matrix prove flatness. The developing diffeomorphism F_t and its conjugation of translations prove free proper compact quotient and affine completeness. Thus no hidden quotient or completeness failure invalidates the example.

All-metric nonexistence follows by evaluating Codazzi on X,Y,X. Both covariant tensor slots were checked: (D_X g)(Y,X)=B_x-tC and (D_Y g)(X,X)=A_y. The global one-form g(X,.) therefore has exterior derivative tC dx wedge dy. Periodicity is a descent consequence for arbitrary smooth tensor coefficients, not an invariance assumption. Positive definiteness makes C>0; Stokes forces t=0. No ansatz or upper/lower bound independent of a hypothetical metric is required.

Boundary counterexamples show exactly what the proof does not assert. The positive cover metric F_t^*(du²+dv²) is locally Hessian with determinant 1, but its cross coefficient tx is not periodic. The indefinite descending metric 2dxdy has C=0 and determinant−1, and its affine potential is uv−tu³/3. Semidefinite dx² also survives; neither is Riemannian. These examples would defeat an assertion omitting positivity or compact descent. They do not defeat the actual claim. The signs of holonomy and tangent parallel transport are opposite conventions but both are nontrivial shears, so no gauge change converts a noncentral connection to the central trivial-holonomy connection.

An averaging argument is legitimate as an independent diagnostic: translations on the original torus preserve the constant-coefficient connection, so the compact average of a positive Codazzi metric is still positive and Codazzi. Its constant C coefficient remains positive, giving tC=0. This verifies that a constant-metric reduction could be justified, but the frozen proof already handles arbitrary metrics directly and requires no averaging lemma.

## The exact older all-metric implication

A nontrivial shear preserving no positive inner product is insufficient by itself. Positive Hessian metrics need not be parallel. I tested the proposed bridge rather than assuming it.

Delanoë's 1989 theorem 3 on printed p. 67 applies to any compact locally Hessian manifold and any nondegenerate density. It produces another positive locally Hessian metric g′ cohomologous to the assumed g, with determinant C times the square of the chosen density, for C>0. I independently downloaded the institutional version of record and visually inspected the complete theorem page. The chosen density |dx wedge dy| is nondegenerate and D_t-parallel, and becomes |du wedge dv| under F_t because det(F_t′)=1. The theorem therefore gives constant determinant C in global developing coordinates. Its stated hypotheses impose no need for a global potential for g on the compact torus; only the correction g′−g has a global potential there.

On full developing R², write the lifted g′ as h_ij. Codazzi makes each column one-form sum_i h_ij du_i closed. Poincaré gives global primitives p_j. Symmetry makes sum_j p_j du_j closed, so Poincaré again yields a global smooth Phi with Hess Phi=h. The Hessian is everywhere positive definite; on each affine line its second derivative is positive, so Phi is strictly convex on the entire plane. Scale by sqrt(C): z=Phi/sqrt(C) has Hessian determinant 1. No growth condition or affine-volume assumption on the potential is added.

The inspected primary Jörgens 1954 p. 130 states a local third-derivative bound at the center of every radius-R disk for a C² solution of determinant-one in dimension 2. Its two nonnegative left sides are |gradient(z_uu)|² and |gradient(z_vv)|²; the right sides are fixed center-value factors times 24/R². For a fixed point of an entire smooth solution, arbitrary R is allowed and its center values remain fixed. Sending R to infinity forces both diagonal Hessian entries to have zero gradient at that point. The point is arbitrary. Mixed-partial identities then force both derivatives of z_uv to vanish, so all entries of Hess Phi are constant. This step does not presume uniform Hessian bounds over expanding balls. The complete Jörgens proof was not accessed, and no full reproof of that published PDE theorem is claimed; the displayed theorem statement and its applicability suffice for this historical implication.

Now a constant positive metric H on developing R² must descend. The linear deck shear S_t=[[1,0],[t,1]] gives S_t^T H S_t=H. For H=[[a,b],[b,c]], the difference is [[2tb+t²c,tc],[tc,0]]. Hence tc=0, whereas positivity gives c>0. This contradicts every nonzero t. The older theorem chain excludes all hypothetical Hessian metrics by replacing them; it does not only test an existing invariant or parallel candidate.

## Given-metric trap and access boundaries

The torus metric (1+epsilon cos(2pi x))dx²+dy², for 0<epsilon<1, is positive and locally Hessian for the standard affine connection. Its global cover potential is (x²+y²)/2−epsilon cos(2pi x)/(4pi²). Its derivative is nonzero, so the standard affine connection is not the Levi-Civita connection of that given metric, despite preserving a volume form. An unrestricted historical claim asserting equality for the given metric would fail this control.

The valid Delanoë route supplies a different metric. The conditional Shima 2007 corollary route and the Fox 2013 corroboration likewise use an existential replacement. Lack of a readable Shima page image or the complete original Cheng–Yau chapter therefore need not be concealed or treated as decisive evidence. The primary inspected Delanoë–Jörgens chain is sufficient independently. Modern claims about every parallel-volume affine manifold being Riemannian are not used; the explicitly known shear family itself would contradict those broader claims.

## Priority classification adversarial alternatives

1. **The family was known but Hessian exclusion was new.** The historical theorem chain supplies arbitrary-metric exclusion, so known-family attribution alone is not the basis of classification. The central exclusion gap is already covered by published general results.
2. **The problem was still listed as open in 1998.** The exact smoothly marked family was publicly available in arXiv v1 on 20 January 2004; no assertion that the question was already answered before its 1998 printing is needed. I independently downloaded v1 and visually inspected its printed pp. 24–25, as well as the official submission history.
3. **A new short proof can count as a new resolution.** A shorter elementary derivation can be a useful exposition. It cannot certify that this original unrestricted problem remained unresolved where its full negative conclusion is a routine application of older results. The present workflow requires correct problem status and a paper framed as solving an originally unsolved problem.
4. **No earlier paper explicitly mentions item 5(b).** No located earlier explicit answer or first solver is claimed. The conclusion is the narrower checkable inference that the required result is already implied by historical published components. The status rationale must use that precise wording.
5. **The theorem chain imports a missing hypothesis.** Compactness, smooth positivity, affine flatness/torsionlessness, nondegenerate chosen density and the full affine-plane developing domain all hold independently. The replacement metric, global cover potential, dimension 2 and determinant rescaling are explicit. No unresolved applicability gap was found.
6. **A proof of every cited classical theorem is mandatory.** This review checks primary statements, exact applicability and the intervening deductions, while acknowledging access limits. It does not claim to have re-refereed all historical PDE theory. The exact local Jörgens estimate displayed on the inspected primary page already implies the needed entire rigidity.

Final mathematical assessment: PASS with no proof repair. Final priority assessment: CONFIRMED prior-theorem coverage. The already-known implication prevents acceptance as a new open-problem resolution. The sealed priority recommendation and its limited attribution are supported. Correcting only the selected queue classification and then immediately excluding the PR would obey the user's strict status gate. The mathematical proof and frozen source artifacts need not be revised, and no paper, publication, tracker entry, merge, close or comment should follow an actual already_solved status.

## Computation scope

check_candidate.py independently binds all 14 frozen source objects, the frozen eligibility receipt and four byte-exact historical script replays. It checks generic Codazzi expressions, positive/indefinite cover boundaries, both shear sign conventions, the given-metric counter-control, determinant rescaling and the large-radius bound limits.65 controls pass in normal and optimized Python with byte-identical 4349-byte output SHA-256 aa3b4e799d850b78a3a16367bccfca54787f84d28a37093cbfeb926bdf011369. Explicit exceptions remain active under optimization. These counts are neither65 mathematical theorems nor a proof of published PDE statements, global positivity or historical priority. Those steps are separately explained above.


## Faithful findings and concrete disposition

There is **one retained publication blocker**: the original unrestricted conclusion already follows from the exact historically available family and inspected older general results, so publication as a new resolution of a previously open problem is unsupported. This is a priority issue, not a mathematical falsification. There is **one required classification change** before acceptance under that framing: correct only the selected queue status/findings to the precise prior-theorem-coverage rationale. Do not silently report that this blocker never existed just because a different disposition resolves it.

The proposed conceptual disposition is acceptable: one selected-row priority correction while the frozen/live status is still exactly claimed_solved, followed by immediate exclusion when already_solved is actually read back. Mathematical gaps: 0. Source-proof repairs: 0. Unresolved blockers to that proposed disposition: 0. Required repairs to its mathematical or priority rationale: 0. A separate live exact-head/status gate and operational-helper review are required before implementing it; neither is asserted completed by this reviewer.

Preserve the original proof and all 14 frozen artifacts, 1/5 accounting and blank DOI. Once corrected, the user's exact status rule forbids further processing. No paper, Zenodo record, tracker row, ready/merge, close or comment is recommended after that exclusion. This reviewer changed none of those resources and contacted no individual.

Six actual in-memory false-claim subprocesses independently exercised the checker guards: wrong Codazzi sign, false Jörgens radius-limit value and false given-metric parallelism, each normally and optimized. All returned nonzero with explicit RuntimeError and zero success stdout. Invalid fixtures and environments are not publication payloads.

An independently retrieved official Jörgens preview has a raw-byte variant (79123 bytes, SHA-256 92949b331356aaa080bb97ab585b52c376e1358a0f28d76f785efd7e5241c515) relative to the priority-obtained copy (79117 bytes, SHA-256 c05ccd1a88e7f83a509308d0d79b1665b57549f0b464334657fa7ca8690a5574). Both printed p. 130 images, independently rendered with the same command, are byte-identical PNGs (98253 bytes, SHA-256 7d58b93457bed7667405b2ac3214383a77a1a88313a63fc43ece335249ffc2f6). Both full-page views were inspected. The theorem statement and estimate agree; no assertion of identical PDF files or full historical proof access is made.

Exact reviewed authored inputs and all 14 frozen source hashes are bound in INPUT_RECEIPT.json. Independent primary-source retrieval/inspection and raw-byte variation are separately bound in PRIMARY_SOURCE_RECEIPT.json. All foreign PDFs, complete texts and renderings remain private and excluded from PUBLIC_FILES.json. No recursive publication should be used.

## Primary source links

- [Original 1998 question](https://doi.org/10.4036/iis.1998.125), item 5(b), printed p. 126.
- [Exact family in Baues–Goldman v1](https://arxiv.org/pdf/math/0401257v1), printed pp. 24–25; [official submission history](https://arxiv.org/abs/math/0401257v1), 20 January 2004.
- [Baues–Goldman v2](https://arxiv.org/pdf/math/0401257v2), printed p. 20, 14 June 2005.
- [Delanoë 1989 primary version of record](https://ir.library.osaka-u.ac.jp/repo/ouka/all/7541/ojm26_01_03.pdf), theorem 3, printed p. 67.
- [Jörgens 1954 official preview](https://page-one.springer.com/pdf/preview/10.1007/BF01361114), Satz 1, printed p. 130; [publisher metadata](https://link.springer.com/article/10.1007/BF01361114).

Completion: 100% of this fresh candidate review. There is no certificate of human peer review, novelty of the short proof, first explicit historical answer, or the identity of a first solver.
