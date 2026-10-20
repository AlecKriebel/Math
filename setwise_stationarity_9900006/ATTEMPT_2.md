# Attempt 2: a rank-one obstruction to single aligned test proximity

2026-10-20. Target remains Thorisson Problem 3.2. Status: accepted obstruction lemma, with the independent checks in [AUDIT.md](AUDIT.md) and the cited mixing-theorem dependency retained. This obstruction is not by itself a general coupling characterization.

## Question tested

Does setwise convergence always admit a single coupling of the original X and stationary X′ satisfying, for every full-path measurable A,

P(1_A(θⁿX) ≠ 1_A(θⁿX′)) → 0 ?   (SC)

Attempt 1 established sufficiency and a non-TV Bernoulli example satisfying SC. This attempt tests necessity in a different dynamical class.

## Relevant inspected primary source

V. V. Ryzhikov, *Weakly homoclinic groups of ergodic actions*, arXiv:1901.09028, https://arxiv.org/pdf/1901.09028 . Theorem 8, pp. 9–11, states that a mixing probability-preserving rank-one automorphism has trivial weak homoclinic group. Its proof uses tower decompositions and near-diagonal measures. The published statement concerns automorphisms, not arbitrary coupling kernels. It therefore cannot directly be cited as the needed obstruction. Below is an extension argument written explicitly for arbitrary bistochastic couplings. The generalization and its application are checked separately in AUDIT.md; they are not imported from the graph-automorphism statement.

## Arbitrary bistochastic rigidity lemma

Let (E,ℰ,ρ) be a standard nonatomic probability space, and T an invertible mixing rank-one probability-preserving transformation. Let κ be ANY probability on E×E with both marginals ρ. If

(1/N) Σ_{n=0}^{N−1} (Tⁿ×Tⁿ)_*κ → Δ_ρ

on all measurable rectangles, then κ=Δ_ρ.

Here Δ_ρ is the diagonal coupling. κ need not be invariant or supported on the graph of a map.

### Tower notation and preliminaries

Choose rank-one towers with base B_j, height h_j→∞, levels L_{j,p}=TᵖB_j (0≤p<h_j), and remaining atom R_j. The tower partitions approximate every measurable set in ρ-measure, and h_jρ(B_j)→1.

For any family of probability measures on E×E whose marginals are bounded by Kρ, every sequence has a subsequence converging on all measurable rectangles. Indeed choose a countable generating algebra and diagonalize; approximation in ρ-measure gives convergence on arbitrary rectangles. The limits extend to probabilities, for example by realizing the standard space as a Borel subset of a compact metric space, using tightness, and then using marginal domination to recover all measurable rectangles. This compactness assertion is confined to standard probability spaces.

Fix a∈(0,1), let m_j=floor(a h_j), M_j=h_j−m_j, and U_j=union_{p<m_j}L_{j,p}. Let σ_j be the restriction of κ to U_j×U_j, and set

η_j=(1/M_j) Σ_{i=0}^{M_j−1}(Tⁱ×Tⁱ)_*σ_j.

For a fixed finite measurable partition P, let D_P be the union of C×C over its atoms. Since η_j is bounded above by the corresponding Cesàro average of κ, the hypothesis implies η_j(D_Pᶜ)→0.

### Decomposition into normalized tower diagonals

Put w_{j,p,q}=κ(L_{j,p}×L_{j,q}). Define γ_{j,p,q} as the probability obtained by choosing x with normalized ρ on L_{j,p}, pairing it with T^{q−p}x, and then applying Tⁱ to both coordinates with i uniform on {0,…,M_j−1}.

Every γ_{j,p,q} has both marginals bounded by

K_j ρ, where K_j=1/(M_jρ(B_j))→1/(1−a).

Its total-variation defect of invariance under T×T is at most 2/M_j (using the norm convention for signed measures; only convergence to zero matters).

For sets A,B which are unions of atoms of the j-th tower partition, the following identity is exact:

η_j(A×B)=Σ_{p,q<m_j}w_{j,p,q}γ_{j,p,q}(A×B).

The reason is that, while i<M_j, both coordinates remain inside specified tower levels; their memberships in A,B depend only on p+i and q+i, not on positions within the levels. For arbitrary fixed A,B the difference tends to zero: approximate by tower-measurable sets and use the uniform marginal bounds on both sides. Consequently this approximation also holds on D_Pᶜ for every fixed finite P.

### Separation of the nonzero offsets

Consider any subsequence of γ_{j,p_j,q_j} with p_j≠q_j. By the preceding compactness observation it has a rectangle-convergent subsubsequence. Its limit γ is invariant under T×T, by the vanishing invariance defect. Write d_j=q_j−p_j.

If d_j has a bounded subsequence, pass to a constant nonzero value d. Each γ_{j,p_j,q_j} is dominated by K_jΔ_d, where Δ_d is the law of (Z,TᵈZ) for Z∼ρ. Hence the limit is dominated by KΔ_d for some finite K. Since Δ_d is ergodic under T×T, invariance and normalization force γ=Δ_d.

If |d_j|→∞, mixing implies Δ_{d_j}→ρ×ρ on rectangles. The same domination implies γ≤K(ρ×ρ). Mixing also makes T×T ergodic, so invariance and normalization force γ=ρ×ρ.

Therefore all possible limit points are among {Δ_d:d∈ℤ\{0}}∪{ρ×ρ}. This set is compact for rectangle convergence, because Δ_d→ρ×ρ as |d|→∞, and it excludes Δ_ρ. There is a finite partition P and δ>0 such that γ(D_Pᶜ)>δ for every member of this compact set. To see this, each nondiagonal coupling has positive mismatch for some finite partition; the corresponding open sets cover the compact set, and joining a finite subcover's partitions gives one P with a positive minimum.

It follows by contradiction/subsequence compactness that, for all sufficiently large j and all p≠q,

γ_{j,p,q}(D_Pᶜ)≥δ/2.

The tower decomposition and η_j(D_Pᶜ)→0 now give

Σ_{p≠q}w_{j,p,q}→0.

### Conclusion

Let D_j be the union of L_{j,p}×L_{j,p} for all tower levels, together with R_j×R_j. The κ-mass outside U_j×U_j is at most 2ρ(E\U_j)→2(1−a), since κ has both marginals ρ. The preceding bound thus yields limsup κ(D_jᶜ)≤2(1−a).

For any fixed measurable A, approximate A by a union of tower-partition atoms. The κ-probability that its two coordinates disagree on membership in A is bounded by κ(D_jᶜ) plus twice the ρ-approximation error. Therefore that mismatch is at most 2(1−a). Let a↑1 to obtain zero mismatch for every A. A countable separating generator then gives κ=Δ_ρ. This proves the lemma.

## Application to the original single-coupling candidate

Choose such a mixing rank-one T, and any bounded nonconstant density f≥0 with ∫f dρ=1 (for example f=2·1_B with ρ(B)=1/2). Put η=fρ, X_k=TᵏZ for Z∼η, and X′_k=TᵏZ′ for Z′∼ρ.

Mixing and bounded-function approximation give full-path setwise convergence exactly as in Attempt 1: for each A in the path σ-field, pull it back through Φ(z)=(Tᵏz) and apply mixing to f and that indicator. The TV distance remains TV(η,ρ)>0 because T is invertible and the first state recovers Z.

Suppose a single whole-process coupling satisfied SC. Its initial states have some coupling π with marginals fρ and ρ. Taking path events determined by the first state shows that (Tⁿ×Tⁿ)_*π has vanishing mismatch on every finite measurable partition.

For C≥||f||∞+1 define

κ = [π + πᵀ + Δ_{(C−f−1)ρ}]/C.

The numerator is a nonnegative measure of total mass C. Each marginal is [f+1+(C−f−1)]ρ=Cρ, so κ is bistochastic. Its diagonal component never mismatches; transpose preserves mismatch. Thus κ also has vanishing mismatch on each finite partition and its pushed laws converge to Δ_ρ on rectangles. The latter follows because the first marginal is always ρ, and the error between the probability of A×B and ρ(A∩B) is at most the mismatch probability for B. Cesàro convergence follows too.

The lemma forces κ=Δ_ρ. Since π/C≤κ, π is supported on the diagonal and therefore has equal marginals. This says fρ=ρ, contradicting the choice of f.

Accordingly, with the lemma and its audit as stated, SC is NOT a necessary condition for the source's setwise convergence, even in a standard Borel state space. The promising criterion from Attempt 1 is too strong. This is an obstruction result, not a replacement coupling characterization and not a resolution of Problem 3.2.

## Audit closure and limits

1. AUDIT.md checks the extension from graph couplings to arbitrary bistochastic κ, including compactness with bounded marginals and uniform finite-partition separation.
2. The following subsection supplies explicit staircase parameters and verifies the hypotheses of a primary-source mixing theorem. Mixing itself remains an imported theorem, not a new proof here.
3. This obstruction is established on a standard nonatomic state space, which already suffices to refute necessity in the general problem. It is not an affirmative characterization. The separate arbitrary-space positive theorem appears in Attempt 3.

## Primary-source closure of the existence dependency

A directly inspected source supplies a concrete class: Darren Creutz and C. E. Silva, *Mixing on a Class of Rank One Transformations*, https://arxiv.org/pdf/math/0109159 . Their Section 2.1 specifies invertible probability-preserving transformations on a standard nonatomic space. Section 7.1 defines staircase spacers s_{n,i}=i and identifies restricted growth as r_n²/h_n→0. Theorem 10 (Adams), p. 23, proves mixing under that condition.

For an explicit choice take h₀=1, r_n=n+2, s_{n,i}=i, and h_{n+1}=r_n h_n+r_n(r_n−1)/2. Then h_n≥(n+1)!, so r_n²/h_n→0. The construction has finite total measure: if w_n denotes the level width at stage n, w_{n+1}=w_n/r_n and its added measure is w_n(r_n−1)/2; the series of these terms converges since w_n=w₀/(n+1)!. Normalize the finite measure to one. Thus this standard cutting-and-stacking transformation supplies the required mixing rank-one example using the cited mixing theorem. Its existence is no longer based only on a secondary reference to Ornstein.

The original Ornstein PDF endpoint returned 403; no access-control bypass was attempted. The independent Creutz–Silva preprint was accessible normally. Its proof of mixing is used as a cited theorem, not claimed to have been independently reproved in this attempt.
