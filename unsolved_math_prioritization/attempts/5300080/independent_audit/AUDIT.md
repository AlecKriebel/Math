# Independent audit: boundary fixed points in rank-zero Hénon components

Problem 5300080 / AMR-052-0080; rank 793. Audit date: 2026-10-05.

## Verdict

**PASS for the explicitly scoped partial results and honest unresolved disposition.** The unrestricted historical problem remains **UNSOLVED by this investigation**, with **five of five substantive approaches used and zero original solution credit**. No mathematical correction to the frozen authored exposition was required. This is an independent AI-assisted audit, not human peer review, a formal proof certificate, or a worldwide open-status determination.

The author's ZIP is preserved byte for byte: 19,789 bytes, SHA-256 `6f7d74f0cd6157fb207d846f7404d22de2b16d09b7e16fdf6f1c2a1a4faed0f6`. Its manifest has SHA-256 `cc3bcf24fd192eeaa676963370f8e360c0039d86a2ded951fbb80ab6240cd60f`. The audit has its own files and manifest; it does not update the author's historical “independent review pending” labels.

## The governing quantifier

The primary source was checked in an independently extracted text, the actual image of printed page 10, and the official PDF reader. Milnor selects one convergent subsequence before asking the boundary rank-zero question. Passing to the return map makes the component invariant; the desired eigenvalue is 1 for that same chosen map. This does not permit replacing one subsequence by all iterates or taking an additional iterate merely to turn a root of unity into 1.

Source: B. Bielefeld (editor), *Conformal Dynamics Problem List*, IMS 1990/1, section 4, p. 10: https://www.math.stonybrook.edu/preprints/ims90-1.pdf .

An additional terminology check supports the distinction. Eric Bedford's notes define a rank-zero **component** by requiring every limit map to have rank zero. Their Proposition 7.2 and subsequent boundary statement therefore concern the stronger hypothesis. Their terminology cannot be substituted into Milnor's earlier existential formulation. Section 7, printed pp. 17–18: https://www.math.stonybrook.edu/~ebedford/ClassNotesHenon.pdf . No complete proof review of these notes is claimed.

## Mathematical audit

### 1. Fixedness, determinant contraction, and boundary exclusion

The argument is valid. For fixed z in the invariant U, both sides of

f^{n_j}(f(z)) = f(f^{n_j}(z))

converge, respectively, to p and f(p). Thus p is fixed. Local uniform holomorphic convergence to a constant gives derivative convergence to zero by Cauchy estimates. A polynomial automorphism has a constant nonzero Jacobian determinant δ, and the determinant of the iterate is δ^{n_j}; hence 0 < |δ| < 1. These facts imply at least one nonzero multiplier of modulus below 1.

If both multipliers contracted, an attracting neighborhood of p would lie in int K⁺. A boundary point of a component of an open subset of C² cannot be inside that open subset: a connected ball around such a point would join it to U in the same component. Sink exclusion is therefore sound. Neither the determinant argument nor sink exclusion rules out a saddle or proves a unit-modulus multiplier.

The triangular reduction also checks out. The diagonal entries of the iterate derivative are a^n and b^n, so a constant subsequential limit on an open set forces |a|, |b| < 1. The inhomogeneous geometric-series recurrence converges for every starting point. Its finite prefix tends to zero and its tail is uniformly bounded by a small forcing error divided by 1−|a|. Hence K⁺ is all of C² and no finite component boundary remains. The affine reduction and preservation of bounded sequences under polynomial conjugacy are valid.

### 2. The two sufficient conditions for full convergence

The bounded-gap argument is valid with its stated extra hypothesis. For n_j ≤ n < n_{j+1}, write n=n_j+r with 0 ≤ r < M. Only finitely many continuous maps f^r must be controlled near the fixed point. Uniform convergence on any compact subset of U therefore extends from the subsequence to the full sequence.

The all-rank-zero argument is also valid under the explicitly stated relative compactness, bounded-orbit, and finite-fixed-point hypotheses. Each map limit is constant and fixed. Every orbit cluster point is a value of some map limit, because relative compactness permits refining a subsequence of iterates. Successive jumps tend to zero: a subsequence of nonvanishing jumps would refine to x_{n_j}→q fixed, contradicting continuity of f. A bounded sequence with finitely many candidate cluster points and vanishing jumps cannot keep moving between disjoint small neighborhoods of distinct candidates. Thus it converges. Relative compactness then upgrades pointwise identification to compact-open convergence.

The existential premise in Milnor's question does not supply the universal premise of this argument. Finite arithmetic tests are not offered as proof of this topological statement.

### 3. Full-convergence and neutral-dynamics inputs

The December 2012 Lyubich–Peters preprint separates the cases exactly as the author says: Theorem 5 imposes full convergence for the eigenvalue-1 conclusion; Theorem 1 imposes |δ| < d⁻² for its invariant-component classification. Theorems 27 and 34 and Lemmas 31–33 were checked in the actual preprint. These are credited inputs, not new results of this packet. The final journal PDF was not independently obtained in this audit. Source: https://www.math.stonybrook.edu/preprints/ims12-07.pdf .

In the full-convergence case, nonrecurrence follows because the unique orbit limit p is outside U. A saddle's global stable set is a countable union of images of complex one-dimensional local stable manifolds, so it cannot contain the open set U. This proof requires full convergence, not arbitrarily close returns.

The exclusion of a locally holomorphically linearizable semi-neutral boundary point is valid: in linearizing coordinates a sufficiently small product disk is forward invariant and bounded. The point is consequently in int K⁺.

The hedgehog input is correctly restricted. Theorem C assumes an orbit stays in the selected neighborhood, while Corollary C.1 obstructs convergence outside the strong stable manifold. They do not exclude an orbit which repeatedly leaves the neighborhood between returns. Source: Lyubich, Radu and Tănase, https://arxiv.org/abs/1611.09840 . No full hedgehog construction is certified here.

### 4. Stable-curve obstruction and the threshold control

Proposition 4 is valid as a conditional analytic argument. Its explicit holomorphic factorization h=ψ∘η is important: it avoids silently treating the inverse of an immersed global stable curve as a globally continuous ambient inverse.

Set u=G⁻∘ψ. The assumed stable curve is contained in K⁺. If u vanished identically, the curve would lie in the compact set K⁺∩K⁻, contradicting Liouville's theorem for the nonconstant entire parametrization. Pullback of the Green function is nonnegative subharmonic and satisfies u(λ⁻¹ζ)=d u(ζ). Iterating the identity until |λ^nζ|≤1 gives a growth bound with exponent log d / log(1/|λ|), including complex λ because only its modulus enters the radius estimate.

The connected set η(U) is nontrivial. Injectivity of ψ and equality f(h(U))=h(U) imply λη(U)=η(U), hence also invariance under λ⁻¹. A nonzero point then has arbitrarily large inverse-scaling iterates inside this connected zero set. The strict bound |λ|<d⁻² gives growth order below 1/2, contradicting the imported subharmonic Wiman theorem. The spectral estimate |λ_s|=|δ|/|λ_c|≤|δ| is correctly directed.

The endpoint example is valid. Away from zero, a local square-root branch is holomorphic, and the absolute value of its real part is subharmonic. It agrees with sqrt((|z|+Re z)/2) across branch choices and extends continuously at zero. The removable-singularity argument is legitimate. Its maximum on the circle of radius r is exactly sqrt(r), so its growth order is exactly 1/2, not merely at most 1/2. Its zero set is the negative real ray, and positive scaling by d² multiplies its value by d. Thus strictness cannot be removed from this abstract analytic step. This function is not asserted to be a Hénon Green function or a dynamical counterexample.

### 5. Prescribed-multiplier controls and the remaining gap

For H(z,w)=(z²+(λ+μ)z−λμw,z), the origin is fixed, the determinant is λμ, and the characteristic polynomial at the origin is (t−λ)(t−μ). The displayed inverse is correct. These algebraic facts admit both expanding/contracting and irrational-neutral/contracting multiplier pairs. For λ=(3+4i)/5, the trace λ+λ⁻¹=6/5 is a rational noninteger. If λ were a root of unity, this trace would be an algebraic integer; contradiction. This control does not construct an invariant Fatou component.

The remaining mixed-rank/unbounded-excursion gap is genuine in the proposed reasoning. Nothing retained in the packet closes it for arbitrary dissipative Jacobian. The more recent papers were inspected only to test whether their hypotheses supplied that missing result: the partially hyperbolic theorem retains additional restrictions; the wandering examples do not give an invariant component; the escaping examples are transcendental with limits at infinity. Their scope was not silently broadened.

## Reproducibility and provenance

- All nine archive members were matched to the frozen author ZIP, and all eight manifest payload entries were independently hashed.
- The author's 14,006 assertions pass in normal mode, optimized mode, and an independently extracted, relocated directory with spaces in its path.
- Fourteen adversarial package mutations are rejected, including altered/missing/unexpected files, a symlink, duplicate/unsafe paths, duplicate JSON keys, rehashed scope/credit/budget/rank changes, and a rehashed false test result.
- A separately implemented Gaussian-rational checker passes 42,428 finite assertions. It includes both inverse compositions, exact central-difference Jacobians, iterate determinants, multiplier controls, exhaustive bounded-gap words of length four for bounds 1 through 6, strict-order comparisons, and threshold-function checks on 409 Pythagorean grid inputs. It does not import the author's arithmetic routines.
- Both complete public dataset files were streamed through SHA-256 and matched the independently read repository manifest. The selected ID and code each occur once. The statement hash, full catalog SHA-256, catalog Git object hash, and rank match.
- The audit additionally recomputed the descriptor review hash using the exact formula inspected in repository queue.py. It matches `e97a8eb02f3fdd31ea65947bad980189b3b9f8923a4af6e46cc55c1c37817330`.
- All seven cached scholarly PDFs match the claimed complete byte counts and hashes. Fresh text extractions were used for scope checks. Rehashing cached bytes is not claimed as an independent live redownload, and downloading or parsing a PDF is not full proof review.
- The repository snapshot was independently confirmed as the current main snapshot when checked. The 63-entry attempts directory contains no target entry; target state/history entries and related-target-group matches were absent. Exact-ID PR, commit and branch searches and exact-code code search returned no results. The imported report explicitly describes its work as unverified triage. These are bounded observations, not exhaustive absence claims.

Detailed public metadata is in PROVENANCE.json and reproducible output in RESULTS.json. Source PDFs, extracted text, images, raw corpora, copied source records, and private coordination are excluded from the audit archive. No remote write was performed.
