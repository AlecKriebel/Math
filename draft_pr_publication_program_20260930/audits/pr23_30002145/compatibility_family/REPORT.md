# PR23 independent compatibility-family audit

**Mathematical verdict: PASS for the scoped source-status correction.** No new result or paper is certified. One stale PR scope statement needs correction before publication of the review package.

Frozen PR: 23; target: 30002145 / OWR-12008-005; head: `ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`; frozen candidate root: `../source_snapshot/`; parent manifest: `../snapshot_manifest.json`. All fourteen frozen file hashes match that manifest after the audit. Candidate and canonical queue/state files were not altered.

The independent mathematical first pass was sealed at `2026-10-01T19:56:30Z`; its exact SHA-256 and input declaration are in `first_pass_seal.json`. Author code, historical reviews/results, and provenance were read only afterward. No sibling mathematical conclusions informed the derivation. This family used a direct distributional compatibility/normal-form mechanism and a full displacement-polynomial nullspace check. The historical reviewer used a finite Hessian compatibility rank calculation; reproducing that calculation is recorded separately and is not presented as new independent evidence.

## Claim and source scope

The imported target asks for the structure of sufficiently regular `u` with `Eu∈R(a⊙b)` and gives no domain or regularity threshold. The candidate expressly restricts its complete classification claim to whole space and local adapted boxes (`SOURCE_STATUS.md:9`, `:20`, `:86`, `:88`). The question in [OWR 36/2012, pp. 2247–2249](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1) occurs in an account of a published blow-up argument. It supplies no theorem of one global profile representation on arbitrary nonconvex domains.

[De Philippis–Rindler 2020](https://arxiv.org/pdf/1911.01356), Theorem 2.10, assumes whole-space `BD_loc` and a signed locally finite scalar measure. Parts (i)–(ii) give the two families; Lemma 2.1 supplies the rigid kernel. I read the complete theorem and proof, including the separate elliptic regularity argument in (iii). The proof runs through printed p. 15; the candidate's “pp. 12–14” link covers the relevant (i)–(ii) proof. Its positive tangent-measure refinement is a separate theorem and cannot replace the signed statement.

[Rindler's prior paper](https://arxiv.org/pdf/1008.2089), §4.4, Propositions 4.7 and 4.9 / Example 4.8 (printed pp. 33–34), covers the two-dimensional absolutely continuous version on whole space. The candidate cites it for that historical coverage and example, accurately.

These source summaries are deliberately limited; the checkable differential derivation below and in `FIRST_PASS.md` is the audit's own reasoning.

## Universal necessity and sufficiency

The full distributional identity

`∂jk u_i = ∂j E_ik + ∂k E_ij − ∂i E_jk`

implies

`∂kl E_ij + ∂ij E_kl − ∂il E_kj − ∂kj E_il = 0`.

For independent vectors, take an invertible congruence change of variables `x=By`, `w=B^T u(By)` with `B^T a=e1`, `B^T b=e2`. Its transverse columns can be chosen orthonormal and perpendicular to `a,b`. Then `y1=x·a`, `y2=x·b`, `E_yw=(e1⊙e2)f`, and pulling back a rigid field preserves skewness. This reduction is valid for nonorthogonal, nonunit, and signed choices of vectors; an orthogonal rotation alone would not justify it.

With only `E12=E21=f/2` nonzero, compatibility yields `f12=f1α=f2α=fαβ=0` for transverse indices. Thus on whole space or a product box, every transverse derivative is constant, and the remaining two-variable function has zero mixed derivative. The exact coefficient is

`f=h1(y2)+h2(y1)+2Σvα yα`.

Taking one-dimensional primitives produces exactly `SOURCE_STATUS.md:31`–`:40`. Conversely, direct differentiation shows that the two positive mixed quadratic pieces each create a cross term canceled by `−v(x·a)(x·b)`; the surviving strain is `2(x·v)(a⊙b)`.

For nonzero parallel vectors the line reduces, with scalar absorption, to `e⊗e` for a unit `e`. Compatibility says precisely that the transverse Hessian of `f` vanishes, so

`f=h(s)+Σt_j p_j(s)`.

Set `H'=h` and `P_j''=p_j`. The two mixed `e⊙v_j P_j'` pieces cancel. This recovers `SOURCE_STATUS.md:45`–`:55`, allowing arbitrary dependence of `p_j` on `s`.

Subtracting a constructed field with the same strain gives zero strain. The Hessian identity makes every first derivative constant on each connected open component; its affine part is skew. This is valid on arbitrary connected open domains without a topology assumption. It justifies every “modulo rigid motion” assertion and `SOURCE_STATUS.md:58`.

Profile integration ambiguities are harmless: in the independent case transferring a constant between coefficient profiles creates `(a⊗b−b⊗a)x`; profile constants add translations. In the parallel case an affine addition `A_js+B_j` to `P_j` creates a skew field plus a translation. The transverse component is unique in the independent coefficient, and longitudinal components can be absorbed into the two profiles directly.

## Distributional and boundary checks

For completeness, the distributional integration statements used above do not presume that the coefficient is smooth. On an interval, a distribution with zero derivative is constant: every compactly supported test function of integral zero has a compactly supported antiderivative. Applying this observation one variable at a time on a product box proves the zero-derivative tensor-product rule. The equation `∂12 f=0` can be integrated once in each variable to obtain the separated distributions; zero transverse second derivatives give the transverse-affine distribution with distributional coefficients. The same rules hold globally on the full Cartesian space.

If `f` is a signed measure, pairing with fixed compactly supported transverse test functions yields locally finite one-dimensional signed measures. In the independent case a test function of integral one isolates either profile up to a constant density. In the parallel case choose transverse test functions with independent zeroth and first moments to isolate `h,p_j`. Consequently `H_i,H∈BV_loc`, `P_j'∈BV_loc`, and `P_j∈W^{1,∞}_loc`. This proves the relevant regularity passage independently of a vague “mollify and pass to the limit” step. Positivity is unnecessary. New exact controls include a difference of Dirac measures and the signed transverse measure `2t δ_0(ds)dt`.

If the product vanishes, the inclusion is zero strain and the coefficient is nonunique. In dimension one a nonzero product spans all scalar strains and permits arbitrary one-variable fields; the kernel is constant. In dimension two the independent case has no transverse quadratic term.

Every interior point of an open domain lies in a sufficiently small adapted product box. This proves the candidate's local claim; it does not provide a global profile pair when slices disconnect. `FIRST_PASS.md` gives explicit smooth solutions on connected polygonal Lipschitz U-shaped domains contradicting such a global pair in both independent and parallel cases. The bump derivative witness `b'(1/2)=−16exp(−4/3)/9` is checked exactly. This is positive evidence for the exclusion at `SOURCE_STATUS.md:86`.

## Source typing qualification

The theorem's printed `a≠±b` condition is not literally an independence condition without normalization. For `a=e1,b=2e1`, the already-published polynomial `u=(4x1³x2,−x1⁴)` satisfies the line inclusion, yet its transverse coefficient depends nontrivially on `x1`, which cannot fit the independent-family quadratic term with constant `v`. The new suite verifies this counterexample exactly.

The candidate already handles this correctly at `SOURCE_STATUS.md:60`: it classifies rank-two products by independent vectors and rank-one products by parallel vectors after scalar absorption. Therefore this source wording issue is **not a defect in the candidate's mathematics**. The separate index/factor slips in the printed (ii) proof do not affect the displayed family; the independent compatibility derivation verifies its correct strain. I did not rely on part (iii), whose setting excludes all symmetric products, to prove any target claim.

## Reproducible checks and limits

Run the new controls with `/usr/bin/python3 exact_falsification_controls.py` from this folder. Environment: Python 3.9.6, SymPy 1.14.0. All nineteen grouped controls pass; results are in `exact_control_results.json`.

| Control | Evidence |
| --- | --- |
| Oblique coordinate change | Exact congruence covariance, nonorthogonal vectors `(2,1,0),(-3,4,0)`, negative transverse scale, skew covariance |
| Mixed-term adversary | Removing any one of the three quadratic blocks creates forbidden strain |
| Polynomial necessity | All displacement solutions of degree ≤4 in 2D and ≤3 in 3D are spanned by the normal forms plus rigid motions |
| Polynomial solution dimensions | Independent: 10 in 2D, 12 in 3D; parallel: 10 in 2D, 13 in 3D; oblique 3D independent: 12 |
| Local potential/kernel | Compatible coefficient integrated to a field; Hessian identity verified; rigid and nonrigid controls |
| Forbidden coefficients | Independent mixed and transverse-quadratic coefficients and parallel transverse-quadratic coefficients fail compatibility |
| Signed singular measures | Heaviside difference and parallel absolute-value/sign construction produce the correct signed Dirac strains |
| Boundary cases | Nonunit parallel scaling/sign, zero strain, dimension one, literal source branch counterexample, nonconvex bump witness |

The original eight-check verifier was copied into ignored `tmp/replays/` and rerun; its receipt matches `verification.txt` byte for byte. The historical eleven-check suite was rerun in that ignored copy; its JSON matches `review/independent_results.json` exactly. Neither historical artifact was edited. The suite's universal smooth symbolic identities establish sufficiency algebraically; finite polynomial completeness and mutation checks support falsification but do not establish the universal theorem. The independent distributional derivation is the necessity evidence.

Primary PDF SHA-256 hashes, independently retrieved into ignored `tmp/`:

- 2020 paper: `94e7831d88206dadee52b1f53cb28b285f262d6da27298757e16d5f0a041c343`.
- OWR 2012 report: `86543ad8c6411193f8a4a3f46a89fb0f85c72bf119cac238d2ef910b2bd15db7`.
- Prior Rindler paper: `70e8de4d3e7795a1a77982c1a7dd009b752bf6625e0589d9befbfc4d2726b3b5`.

These match the historical source receipts. Raw PDFs/text, copied scripts, and reproduction receipts remain ignored. Only first-party audit artifacts are in this family manifest.

## Actionable findings

**[P2] Correct the stale PR file-scope statement — `source_snapshot/PR_DRAFT.md:24`.** It says that only attempt files change and that there are no shared queue edits. The frozen parent manifest lists `unsolved_math_prioritization/QUEUE.md` among changed paths, and its head row changes the target to `already_solved`. Update the scope paragraph to include that queue status change and retain its source-correction qualification. This is a documentation inconsistency, not a defect in the verified classification. Root owns the actual PR/integration changes.

No mandatory mathematical correction is identified. Preserve `SOURCE_STATUS.md:3`, `:60`, `:64`, `:86`, and `:88`: scoped status, normalization handling, computational necessity limits, nonconvex-domain exclusion, and no-novelty disposition.

## Strongest verified result and exact remaining gap

Strongest verified result: the displayed smooth normal forms are necessary and sufficient on whole space and adapted boxes, modulo rigid motions, for arbitrary independent/parallel vectors and arbitrary signed coefficients; the signed-measure regularity reduction agrees with the established `BD_loc` theorem. Zero and one-dimensional cases are correct.

The domain-free imported record cannot certify an unrestricted arbitrary-domain global profile theorem. Connected nonconvex counterexamples show that unrestricted reading would be false. The draft explicitly avoids it. The remaining work is administrative: root must correct stale scope metadata and make the final scoped queue/publication decision. There is no unfinished central proof search and no paper to prepare. New substantive target attempts remain **0/5**. Completion of this compatibility-family audit: **100%**.
