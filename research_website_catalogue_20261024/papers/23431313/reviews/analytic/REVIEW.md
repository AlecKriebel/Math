# Independent analytic review: Zenodo 23431313

**Conclusion: PASS at the manuscript’s exact smooth, local-frame scope.** I found no substantive proof gap in either direction of the classification. This is an AI mathematical review, not external human peer review, proof-assistant certification, or a certificate of novelty or priority. No source was repaired and no publication action was taken.

## 1. Reviewed object, independence and exact claim

Reviewed all five pages of **A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators**, Alec Kriebel, version 1.0, dated 15 October 2026, DOI [10.5281/zenodo.23431313](https://doi.org/10.5281/zenodo.23431313), together with the complete current `paper.tex` and current mathematical control code. The primary PDF is 69,486 bytes, SHA256 `a1e2da77dd739bcc7ddc4dd8ba916c99010450e4224ae7a52d01d34c98960e72`. The support ZIP is 1,864,645 bytes, SHA256 `21de02dcdc08c6cd804ccf6345ede97edbfe734469dcdd83ff3b7a65c3c20f02`. The fresh acquisition receipt SHA256 is `7d3d5076a69fda43f42c5d78cbda269d70fcbc8e907120dbe6bebdd59afd493c`.

The source binding in `evidence/source-binding.json` independently checks public asset sizes, SHA256 and MD5, metadata hash, all 129 extracted ZIP members, ZIP CRCs, and the current source TeX hash. The embedded main PDF and the PDF inside the one historical nested ZIP are byte-identical to the public main PDF: there is only one distinct reader PDF. The nested archive was inspected only for byte integrity and PDF identity, not for historical assessment text.

I reconstructed the proof and completed the fresh controls before reading the packaged helpers. No sibling report, code, or conclusion was consulted. Necessary manuscript reading exposed its own historical-audit/disclosure statements. Later inspection of current `scripts/verify_kit.py` incidentally exposed hard-coded prior whole-review no-finding counts, status flags and historical evidence paths. Those assertions were not adopted as evidence, the referenced historical assessment bodies were not opened, and that terminal-accounting verifier was not run. Current `run_checks.py`, `safety.py`, `build_support.py` and `build_pdf.py` were inspected as executable support; the last two concern packaging/build behavior, not the universal proof.

The precise theorem is:

* For every integer n ≥ 1 and every prescribed numerical real Jordan matrix J whose eigenvalues are all real, there is a globally C∞ real Nijenhuis (1,1)-tensor on Rⁿ with compact support, equal to J **in a smooth commuting local frame** on a nonempty open domain.
* Conversely, every eigenvalue at every point of any globally smooth, compactly supported real Nijenhuis tensor on Rⁿ is real.

The result allows changes of rank, type and eigenvalues away from the realization domain. It does not prescribe the ambient Cartesian matrix, assert a globally constant Jordan type, require semisimplicity or algebraic regularity, or supply a nonzero real-analytic compactly supported tensor. The zero matrix and n = 1 are included. It asserts existence, with a qualitative sufficiently small tubular radius; it is not a complexity or quantitative radius bound.

## 2. Reconstruction of the existence direction

### 2.1 Full collar equation and absence of hidden derivative conditions

On Tᵐ × (−1,1), m = n−1, take the global invariant angular fields e₁,…,eₘ and v = ∂t. These commute although global real-valued angular coordinate functions do not exist. If

L eᵢ = A(t)eᵢ, L v = b(t) + λ(t)v,

then each angular pair has zero torsion. The mixed brackets are

[Leᵢ,Lv] = −λ A′eᵢ, [Leᵢ,v] = −A′eᵢ, [eᵢ,Lv] = [eᵢ,v] = 0.

Substitution in the manuscript’s convention gives N_L(eᵢ,v) = (A−λI)A′eᵢ. The coefficient functions have no angular derivatives. In particular, neither b′ nor λ′ is inadvertently omitted: neither appears in these mixed brackets. Skew symmetry and tensoriality account for all other pairs. The displayed condition is therefore equivalent to zero torsion for this ansatz. The order of multiplication is essential and no invertibility, regularity or constant-rank hypothesis is used. See source lines 74–96.

A fresh independent component calculation used the full coordinate formula with arbitrary symbolic A, A′, b, b′, λ and λ′, checking all 85 torsion components in dimensions 2–5. These symbolic checks supplement the dimension-free bracket derivation. A separate Cartesian calculation also checked the nonconstant polynomial tensor

L(x,y) = [[x²+y²−xy, −y²], [x², x²+y²+xy]].

On an annulus, this is the pushforward of A = λ = r² and b = r in the circle collar frame (eθ,∂r); every Cartesian torsion component vanishes identically. This directly corroborates the naturality/commuting-frame step rather than only checking matrices in the original collar frame.

### 2.2 Every prescribed real Jordan matrix admits the ordered shutdown

Use the upper-superdiagonal Jordan convention. Move one whole block to the end and choose its final vector as v. The span of the other n−1 vectors is invariant, so J has the required block-upper-triangular form. Its angular A₀ consists of all the other blocks plus the selected block shortened by one. A size-one selected block disappears from A₀. The vector b₀ retains the terminal Jordan arrow, so the starting full matrix is exactly J, not a matrix with an arrow already lost.

First remove b while A and λ remain fixed. The collar equation permits this without restriction. For each remaining angular Jordan block μI+K, move λ to μ while A remains fixed. Write K = Σ aⱼEⱼ,ⱼ₊₁. Then

KK′ = Σ aⱼa′ⱼ₊₁Eⱼ,ⱼ₊₂.

Remove a₁, then a₂, and continue left to right. When a later arrow is changing, its predecessor is already identically zero. The first arrow has no predecessor. Thus KK′ vanishes throughout. Derivatives in all other blocks vanish, so the corresponding nonzero values of A−λI are immaterial. Once the active block is scalar, lower its scalar c to zero while setting λ = c; the only nonzero derivative lies in a block on which A−λI is zero. Repeating this leaves A, b and λ all zero.

This handles singleton blocks, repeated eigenvalues across blocks, zero and negative eigenvalues, arbitrarily long blocks, and every choice of the distinguished block. No eigenvalue difference or eigenvalue itself is divided by. For n ≥ 2 the angular space has positive dimension and its final scalar stage also sets λ to zero. A constant permutation of the full local frame restores the original requested block order and preserves commutation. See source lines 98–143 and 155–156.

The fresh finite controls exhaust all ordered compositions of every dimension 2–8, each possible distinguished block, and three eigenvalue families: all zero, all 3, and a repeated cycle −2,0,3. There are **3,069 paths and 34,362 stages**. For each affine stage A = A₀+uD and λ = λ₀+uδ, both coefficients

(A₀−λ₀I)D and (D−δI)D

were checked exactly. This verifies the polynomial identity over the whole stage parameter, not merely at sampled parameter values. Initial J and final zero were checked. All entries and products in this finite family are small integers; the NumPy int64 operations do not approach overflow. These are indexing controls, not an induction by experiment.

### 2.3 Smooth stages, two-sided collar and zero extension

H(u) = exp(−1/u) for u > 0 and zero otherwise is C∞ and flat at zero. The denominator H(u)+H(1−u) is positive everywhere, making S smooth, identically zero on (−∞,0] and one on [1,∞). Choosing an affine stage parameter whose endpoint values lie strictly below zero and above one gives genuine endpoint intervals of constancy. Finite concatenation therefore matches all derivatives, without merely assuming matching endpoint values are enough. Reparametrization multiplies A′ by a scalar, so the equation is preserved.

The specified q(t) = S(2(t²−1/16)) is smooth and even. It is zero for |t| ≤ 1/4 and one for |t| ≥ 3/4. Its argument equals zero and one at precisely those positive thresholds. Thus the central band has J and both end bands have the exact zero tensor. There is no absolute-value corner, no unsupported arbitrary scalar multiplication of J, and no need to check infinite jets of a numerical approximation. See lines 134–154.

For completeness, the claimed same-dimensional embedding is valid for every dimension. Start with a circle. Given an embedded Tᵈ⁻¹ in Rᵈ with unit normal ν, its inclusion in Rᵈ⁺¹ has trivial rank-two normal bundle spanned by (ν,0) and (0,1). A sufficiently small embedded normal disk bundle exists by the tubular-neighborhood theorem and compactness. Its circle boundary is Tᵈ and has the stated parametrization

F(p,φ) = (f(p)+ε cosφ ν(p), ε sinφ).

Uniqueness of tubular coordinates gives both injectivity and immersion. The explicit unit normal (cosφ ν,sinφ) is orthogonal to every tangent derivative, since ν·df = ν·dν = 0. Hence the induction preserves two-sidedness. There is no step that embeds Tⁿ in Rⁿ or requires globally defined angular coordinate functions. Fresh differential controls check this recursion through torus dimension four, including unit-normal and off-diagonal Gram identities; global injectivity and the general dimension follow from the tubular argument, not those finite checks.

A thin normal collar of Tⁿ⁻¹ in Rⁿ is diffeomorphic to Tⁿ⁻¹×(−1,1). Pushforward preserves the commuting frame and Nijenhuis torsion. The support lies in the image of compact Tⁿ⁻¹×[−3/4,3/4], a closed compact subset strictly inside the open collar. Every point outside the collar, including each collar-boundary point, therefore has a neighborhood disjoint from this support. Extension by zero is C∞ and retains zero torsion by locality; an exterior angular frame is unnecessary. A coordinate box inside the central band gives a connected open realization domain. For n = 1, a scalar plateau bump works because an alternating vector-valued two-form vanishes in dimension one. See lines 158–192.

## 3. Reconstruction of necessity and exact primary imports

The needed statement is the manuscript’s weaker zero-point rigidity lemma: a smooth real Nijenhuis tensor on a **closed connected** manifold, vanishing at one point, has real spectrum everywhere. No constant-type, semisimplicity, differential nondegeneracy or analytic-manifold assumption is inserted.

Suppose a nonreal eigenvalue exists. Let μ(x) be the largest positive imaginary part, zero at all-real spectra. Continuity of polynomial root multisets makes μ continuous. Compactness provides a positive global maximum μ₀. Among roots at that height, choose the largest algebraic multiplicity m₀. This maximum exists as a maximum of a nonempty finite set of possible integers. The locus E where a height-μ₀ root has multiplicity m₀ is nonempty and closed. Indeed, coefficients are bounded on the compact manifold, hence roots are uniformly bounded; for a convergent sequence of such points one can extract a convergent root subsequence. Vanishing polynomial derivatives up to order m₀−1 pass to the limit. The limiting multiplicity is at least m₀, and maximality on that height line forbids a larger value.

At p ∈ E, isolate λ₀ and its conjugate from the remaining roots by disjoint neighborhoods. In the pinned BKM author-v2:

* **Theorem 3.1, pp. 19–20**, allows admissible smooth characteristic-polynomial splitting near singular as well as generic points. It gives integrable complementary blocks and, critically, independence from the other block’s coordinates. I read its full proof, including its projector/functional-calculus setup in pp. 17–19 and the relevant polynomial and constant-rank integrability arguments in Propositions 2.1 and 2.5. The local cluster remains separated and avoids the real axis; the theorem does not require individual eigenvalues to be smooth.
* **Proposition 3.2 and Theorem 3.3, pp. 21–24**, apply to a smooth Nijenhuis block with no real eigenvalues. The canonical complex structure makes the block holomorphic with the upper-half-plane roots as its complex spectrum. Its proof uses the separated spectra of Lᶜ and its conjugate in the Sylvester equation; no diagonalizability is required. I read the statements and full proof, including Lemma 3.1. Local use is sufficient. An empty complementary block simply requires no splitting step.

Consequently the degree-m₀ complex characteristic factor P(z) has holomorphic coefficients in the block’s complex variables, independent of complementary real variables, and P(z) = (z−λ₀)^m₀ at p. Every nearby upper root has imaginary part ≤ μ₀. Hence −Im a₁ ≤ m₀μ₀ with equality at p. The harmonic maximum principle gives constant Im a₁ locally; the Cauchy–Riemann equations then give constant a₁. Equality of the sum forces each root’s imaginary part to equal μ₀, without selecting a holomorphic root branch. The shifted polynomial P(w+iμ₀) has real roots, so all its holomorphic coefficients are real-valued and therefore constant. This makes P locally constant and E open. Connectedness gives E equal to the entire manifold, contradicting the zero point.

This proof needs only the local splitting/holomorphic machinery and the elementary maximum argument. It avoids the concluding polynomial iteration in the stronger BKM **Theorem 6.1, pp. 41–43**, whose complete proof I also read. The manuscript accurately points out that its literal count of removed nonreal eigenvalues is imprecise: the constant rotation blocks with eigenvalues ±i and ±i/2 all have real image under z↦z²+1. I independently checked the image matrix diag(0,0,3/4,3/4). This is not a counterexample to the stronger theorem and is not a gap in the present weaker proof. This review does not certify the full stronger persistence argument or identify the unread Advances in Mathematics publisher body with the author-v2 PDF.

Finally, embed Rⁿ as the usual chart in Sⁿ. Compact support makes the tensor identically zero near the missing point, so the zero extension is smooth and Nijenhuis on closed connected Sⁿ. The zero-point lemma excludes nonreal spectrum. Compactness, connectedness, and the existence of a zero point each have an explicit role; arbitrary nonzero constant complex rotation tensors on a torus do not contradict the lemma. See current source lines 194–249.

The exact raw primary files, hashes, URLs, versions and reading scope are pinned in `evidence/primary-source-checks.json`. The load-bearing author text is [arXiv:1903.04603v2](https://arxiv.org/pdf/1903.04603v2), SHA256 `ea67f776ee5eab66a01ae6245ad0f61df960314e3fa21b49f9c0345bc0653084`. Its statement and full theorem bodies support the precise local imports used here.

## 4. Original question and bounded prior-result comparison

The original source is correctly identified as [author-v2 Problem 5.11, p. 29](https://arxiv.org/pdf/1804.03737v2), dated 14 January 2020, with [author-v1 Problem 4.10, p. 37](https://arxiv.org/pdf/1804.03737v1), dated 10 April 2018. I read both question bodies and the surrounding examples. They ask for compact support and a prescribed unchanged algebraic type on a domain; v2 explicitly asks for necessary and sufficient Segre-characteristic conditions. The source already gives the nonreal obstruction, real semisimple examples and a two-dimensional Jordan example. The present statement answers that printed historical question at its stated smooth scope; it does not establish that the question was still open in October 2026.

BKM Theorem 4.5 and the following p. 28 remark were read directly. Their independent characteristic-coefficient coordinates realize arbitrary algebraic types at local points while nearby generic points are semisimple with distinct eigenvalues. Thus that result is correctly credited and does not by itself provide a constant nonsemisimple type on an open region together with compact support.

I checked Geometry III’s author-v1 Theorem 1.4 and the final published issue’s Theorem 1.10 (printed p. 161), its layer definitions, and the proof passage on printed pp. 172–173. The regular layers have one Jordan block per eigenvalue, and the theorem constructs a local perturbation of a nonzero nilpotent Jordan block lying in a prescribed regular-layer closure. This is context, not a load-bearing import for the new collar proof. It supplies neither the stated arbitrary repeated-block compact transition nor a priority verdict about another possible construction. The distinct online-first PDF was hash-checked but not read; the final issue and author-v1 are separately identified.

I also checked Geometry IV author-v1 Theorems 1.2 and 1.4, formula (6), and the full proof of Theorem 1.4 on pp. 19–20. Singular or zero output symmetries are permitted. The functional coefficients nevertheless obey the displayed differential compatibility equations. In size three, expanding the stated formula gives coefficients

M = f₃(t)I + [f₂(t)+u²f₃′(t)]N + [f₁(t)+u²f₂′(t)+u¹f₃′(t)+(u²)²f₃″(t)/2]N²,

where t=u³. The unwrapped angular-coordinate terms indeed obstruct naïve periodic identification for arbitrary changing coefficient functions. This limited observation does not rule out a different use of that framework. No theorem of Geometry III or IV is needed to prove the present sufficiency direction. No exhaustive priority search or claim about unread newer literature was made.

## 5. Fresh falsification controls and unchanged published replays

Fresh `independent_controls.py` and `evidence/independent-controls.json` document the results described above. Deliberately invalid variants were rejected:

* Killing the second arrow first in a size-three angular block gives (A−λI)A′ = −E₁₃.
* Reversing the ordered product rejects a genuinely valid first-arrow removal.
* Multiplying the size-three nilpotent angular block by u gives residual uE₁₃.
* Moving an angular scalar without matching λ gives a nonzero residual u.
* Multiplying a two-dimensional complex rotation by the Cartesian function x yields nonzero torsion.

These controls detect the relevant identities rather than simply checking a positive example. Smoothness and all-dimensional validity come from the proof in Sections 2–3 of this review, not from finite controls.

The unchanged distributed `scripts/run_checks.py` was then replayed on an exact disposable copy under normal Python, `-O`, and `-OO`. **Each mode passed 576 schedule families, 4,778 stages, 515 direct-bracket stages, 1,575 sampled generic-jet scalar components and all five published negative controls.** The helper uses exact rational univariate polynomial arithmetic and explicit guards, so the successful optimized runs are not explained by disabled assertions. Its 1,575 generic-jet checks are finite sampled checks; the fresh arbitrary-symbolic computation is separate. Counts are recorded in each raw result, not inferred from historical output files.

The unchanged archive builder produced a ZIP byte-identical to the downloaded support ZIP. An existing-output sentinel and a tampered payload, both only in disposable copies, were rejected under `-OO`; originals remained unchanged. All 129 original extracted files and both public assets were rehashed afterward. The replay cache was removed. Raw stdout/stderr, outputs, commands, timings and guard evidence are in `evidence/`, summarized by `replay-summary.json`. The historical terminal-accounting verifier and PDF regeneration were not run; neither supplies evidence for this mathematical classification.

## 6. Strongest verified result, limitations and disposition

Both directions of Theorem 1 are supported at their exact stated scope: every prescribed numerical real-spectrum Jordan matrix is realizable on an open domain in a commuting smooth local frame of a globally C∞ compactly supported Nijenhuis tensor on Rⁿ, and all such compactly supported tensors have entirely real spectrum at every point. The ordered block path and the embedding/gluing argument cover all dimensions and all real Jordan block patterns; no unsupported finite-to-infinite extrapolation is needed. The nonreal obstruction is correctly credited and established here through the narrower zero-point proof using directly checked local primary imports.

**Substantive mathematical findings: none. Remaining central proof gaps: none identified.** Unestablished items remain full-result/method priority, whether the historical question remained open worldwide, external human peer review, formal certification, and the stronger persistence proof beyond the actual application. The manuscript expressly does not claim those items. No follow-up conjecture, repair, publication promotion, website/Sheet/Git action, or external communication was prepared or performed.
