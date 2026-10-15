# Row 1760 / 2800905: negative answer to positive-PCA tightness

## Claim and attribution

For a symmetric Gaussian Wigner matrix with independent upper-triangular entries of variance 1/n, let

p(W) = max { xᵀWx : x ≥ 0, ||x||₂ = 1 },
s(W) = max { Tr(WX) : X ⪰ 0, X ≥ 0 entrywise, Tr(X) = 1 }.

Then s(W) converges in probability and in expectation to 2, while p(W) ≤ √2 + o(1) with high probability. In particular, with probability tending to one s(W) > p(W), and no optimal SDP matrix has rank one. Both conjectures in Bandeira's Open Problem 9.5 (the expectation √2 + o(1), and high-probability rank-one optimality) are false.

This is a **credited reconstruction/application of a known resolution**, not a novelty claim. Bandeira, Kunisky and Wein prove the SDP limit in *Average-Case Integrality Gap for Non-Negative Principal Component Analysis*, PMLR 145 (2022), 153–171, Theorem 4, and explicitly identify Open Problem 9.5 on printed page 157. Their projector-plus-all-ones construction is used below. The original preprint is arXiv:2012.02243v1, December 3, 2020 (Theorem 3 there); the PDF proceedings header says the 2021 conference, whereas the official publisher's citation year is 2022. Montanari and Richard's earlier work gives the sharper limit p(W) → √2. The upper bound needed for the negative answer is proved below without relying on their approximate-message-passing analysis.

Sources:
- Original author notes, October 10, 2016, printed pp.130–131, equations (103)–(104) and Open Problem 9.5: https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf
- Original 2015 blog entry: https://afonsobandeira.wordpress.com/2015/11/28/10l42psbm/
- Published result and citation metadata: https://proceedings.mlr.press/v145/bandeira22a.html
- Actual published PDF: https://proceedings.mlr.press/v145/bandeira22a/bandeira22a.pdf
- Montanari–Richard: https://arxiv.org/abs/1406.4775

Replacing the trace-one, entrywise-nonnegative feasible set by diagonal-one matrices or inserting a planted spike changes the original question. Neither change is present in the original target. We do not address a planted recovery threshold here.

## Explicit standard inputs and normalization

Use first the orthogonally invariant Gaussian model G with independent entries G_ij ~ N(0,1/n) for i<j and G_ii ~ N(0,2/n), with G_ji=G_ij. Three standard inputs are used:

1. The global semicircle law: the empirical spectral measure of G converges in probability to the probability density (1/(2π))√(4−t²) on [−2,2]. Benaych-Georges–Knowles, *Lectures on the local semicircle law for Wigner matrices*, Definition 2.2 and Theorem 2.4 (actual v3 PDF pp.8–10), apply: upper-triangular entries are independent, centered, off-diagonal variance 1/n, diagonal variance O(1/n), and all moments of √n G_ij are uniformly bounded. https://arxiv.org/abs/1601.04055 ; exact inspected PDF https://arxiv.org/pdf/1601.04055v3 . We invoke this theorem, not a new proof of the semicircle law.
2. Sudakov–Fernique Gaussian comparison: centered Gaussian processes on the same compact index set with the first process's increment variances at most those of the second have ordered expected suprema. The actual author notes above state the applicable version as Theorem 5.10, printed p.84. All processes below are continuous and bounded on their compact parameter sets.
3. Gaussian concentration: for an L-Lipschitz function of an independent standard Gaussian vector, P(|f−Ef|≥t) ≤ 2 exp(−t²/(2L²)). The same notes state this as Theorem 4.7, printed p.61. We check the needed Lipschitz constants below. These named inputs are not claimed to have received independent full-proof audits in this packet.

**Source defect recorded rather than hidden.** The published integrality-gap PDF, printed p.154, and its v1 preprint interchange the displayed diagonal and off-diagonal variances in the sentence defining GOE. The displayed variances there would not give the stated spectral edge 2 or an invariant ensemble. The actual proof uses Haar eigenspaces and the variance 2/n for a unit-vector quadratic form, which identify the invariant convention just defined. We visually inspected the published p.154, so this is not merely OCR. Our argument is explicitly for the normalized invariant ensemble G, then transfers to the original notes' all-upper-entry variance 1/n model; it does not silently apply a contradictory literal definition.

## 1. Basic optimization facts

Both feasible sets are nonempty and compact. For the SDP, positive semidefiniteness and trace one bound every eigenvalue by one and bound the Frobenius norm; the constraints are closed. For any real symmetric D and feasible X, diagonalize D to obtain

|Tr(DX)| ≤ ||D||op Tr(X) = ||D||op.

The same inequality holds for xxᵀ. Consequently both p and s are 1-Lipschitz with respect to operator norm, and p(W) ≤ s(W) ≤ λ_max(W).

A rank-one feasible X has the form xxᵀ with ||x||₂=1. Entrywise nonnegativity says x_i x_j ≥0 for all i,j. All nonzero coordinates have one common sign, so replacing x by −x if needed makes it nonnegative. Thus a rank-one optimal SDP solution exists if and only if p(W)=s(W). In particular a strict value gap excludes every rank-one optimizer, without requiring uniqueness.

## 2. A Gaussian-comparison upper bound for the true problem

For a unit vector x, define A_x=xᵀGx. A direct sum over independent entries gives

E[A_x A_y] = (2/n)(xᵀy)²,
E[(A_x−A_y)²] = (4/n)(1−(xᵀy)²).

Let g be a standard n-dimensional Gaussian vector and B_x=(2/√n)gᵀx. Its increment variance is (8/n)(1−xᵀy). Since 1−t² ≤ 2(1−t) for every t≤1, Gaussian comparison gives, on the positive part of the unit sphere,

E p(G) ≤ (2/√n) E sup_{x≥0, ||x||=1} gᵀx
        ≤ (2/√n) E ||g_+||₂
        ≤ (2/√n) √(E ||g_+||₂²) = √2.

The middle bound also holds when all coordinates of g are negative, when the supremum is negative. No claim of equality in that exceptional case is needed. Here E(g_i)_+²=1/2 by symmetry.

Parameterize G by independent standard Gaussian coordinates z_ij: G_ii=√(2/n)z_ii and G_ij=z_ij/√n for i<j. The coefficient vector of the linear functional xᵀGx has squared norm

(2/n)Σ_i x_i⁴ + (4/n)Σ_{i<j}x_i²x_j² = 2/n.

A supremum of linear functionals whose coefficients have norm at most √(2/n) is √(2/n)-Lipschitz. Gaussian concentration therefore gives, for every fixed t>0,

P(p(G)>√2+t) ≤ 2 exp(−nt²/4).

Using comparison on the whole unit sphere similarly gives E λ_max(G) ≤ (2/√n)E||g||₂ ≤2. The same Lipschitz computation gives P(λ_max(G)>2+t) ≤2 exp(−nt²/4). Hence s(G)≤2+o(1) with high probability and E s(G)≤2.

## 3. Uniform small off-diagonal entries of a Haar projector

Fix δ in (0,1), let r=⌊δn⌋, and let P be the projection onto a uniformly random r-dimensional subspace. We prove that

max_{i≠j}|P_ij| = O_δ(√(log n/n))

with probability tending to one. For any fixed unit vector u, rotational invariance gives

uᵀPu = (Z₁²+...+Z_r²)/(Z₁²+...+Z_n²)

in distribution, for independent standard Gaussian Z_i where u is the fixed unit vector. The standard chi-square Chernoff bounds are

P(A_k−k ≥2√(kt)+2t)≤e^(−t),
P(k−A_k ≥2√(kt))≤e^(−t),

where A_k=Σ_{i=1}^k Z_i². They follow from E exp(θA_k)=(1−2θ)^(−k/2), θ<1/2, by Markov's inequality and minimization in θ; the lower-tail version uses θ<0. Apply these bounds to the numerator and denominator with t=6 log n. Their deviations are O(√(n log n)); the denominator is at least n/2 for all sufficiently large n on this event. Subtracting r/n from the ratio proves

|uᵀPu−r/n| ≤ C_δ √(log n/n)

outside a set of probability at most 4n^(−6). Dependence between numerator and denominator causes no problem, since this step only uses a union bound.

For each pair i<j apply this to u_+=(e_i+e_j)/√2 and u_−=(e_i−e_j)/√2. The identity

P_ij = (u_+ᵀPu_+ − u_−ᵀPu_−)/2

and a union bound over fewer than n² vectors establish the assertion. The estimate allows r=⌊δn⌋, so no integrality subsequence is omitted.

## 4. A feasible SDP witness approaching the spectral edge

G has density proportional to exp(−n Tr(G²)/4), invariant under orthogonal conjugation, and has simple spectrum almost surely. Thus its top-r eigenspace has the invariant probability distribution on the Grassmannian. Its orthogonal projector P has the distribution considered in Section 3. Independence of P from eigenvalues is not needed for the following intersection of high-probability events.

Fix α,δ in (0,1), and set

X = (1−α)P/r + α 11ᵀ/n.

Both summands are positive semidefinite and have trace one before multiplication by their weights, so X is positive semidefinite and has trace one. Its diagonal is nonnegative. Off the diagonal,

X_ij ≥ α/n − ((1−α)/r) C_δ √(log n/n).

Because r/n→δ>0, the subtracted term is o(1/n). Hence X≥0 entrywise with probability tending to one. This is the known Bandeira–Kunisky–Wein witness, with the flooring and feasibility estimate made explicit.

Order eigenvalues decreasingly. On the feasibility event,

s(G) ≥ Tr(GX) = (1−α)(1/r)Σ_{j=1}^r λ_j(G) + α (1ᵀG1/n).

For every fixed η>0 smaller than 2, the semicircle law puts a positive limiting fraction m_η of eigenvalues in (2−η,2). Choose 0<δ<m_η. With probability tending to one at least r eigenvalues exceed 2−η, and the displayed average is at least 2−η. Also 1ᵀG1/n is centered Gaussian of variance 2/n, so it tends to zero in probability. It follows that

s(G) ≥ (1−α)(2−η) − o(1)

with high probability. Given ε>0, choose η and then α small enough that (1−α)(2−η)>2−ε/2, and then choose δ as above. This proves s(G)≥2−ε with high probability. Section 2 supplies the upper bound, so s(G)→2 in probability.

Expectation convergence does not require an unproved uniform-integrability assertion. I/n is feasible, so s(G)≥T:=Tr(G)/n, and E T²=2/n². If E_n is the event s(G)≥2−ε, then

E s(G) ≥ (2−ε)P(E_n) + E[T 1_{E_n^c}]
       ≥ (2−ε)P(E_n) − √2/n.

Thus liminf E s(G)≥2−ε for every ε>0. Together with E s(G)≤2 this gives E s(G)→2.

## 5. Transfer to the exact Gaussian Wigner convention and conclude

Couple the original matrix W to G with identical off-diagonal entries and diagonal entries W_ii=z_ii/√n, G_ii=√2 z_ii/√n. Their difference is diagonal and

||W−G||op = (√2−1) max_i |z_ii|/√n.

The union bound P(max_i|z_ii|>a)≤2n exp(−a²/2) shows this tends to zero in probability. Moreover E max_i|z_ii|≤√(2 log(2n)): for t>0, E exp(t max_i|z_i|)≤2n exp(t²/2), then use Jensen and optimize in t. Hence E||W−G||op→0. Section 1's Lipschitz bounds transfer the probability limits and expectation limit to W, including p(W)≤√2+o(1) with high probability.

Choose t>0 so small that √2+2t<2−2t. With probability tending to one, s(W)≥2−t and p(W)≤√2+t; there is a strict gap. Every rank-one feasible matrix corresponds to a feasible nonnegative vector, as proved in Section 1. No optimal SDP matrix is rank one on that event. This answers the original question negatively under its exact unspiked Gaussian hypotheses.

## Scope of validation

The original problem, the published Theorem 4 and its entire short Section 2 proof, the relevant Gaussian-comparison/concentration statements, and the semicircle theorem's hypotheses were inspected. The proof above checks the application and supplies the stated elementary lemmas. It does not claim an independent proof of every classical probability theorem, a full audit of the unrelated hardness section, or a new result. It makes no assertion of a numerical finite-n threshold or of universality over arbitrary non-Gaussian Wigner distributions. No author code was executed.
