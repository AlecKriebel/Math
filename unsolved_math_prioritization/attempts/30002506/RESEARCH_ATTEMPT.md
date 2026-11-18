# Bohr-radius characterization of ℓ¹: five approaches and their limits

Target: row 1882, ID 30002506, OWR-12866-016. Research date: 2026-10-21.

## Scope and outcome

Assume that X is a complex Banach sequence space with ℓ¹ ⊆ X ⊆ c₀ as sets and a canonical 1-unconditional Schauder basis. No permutation symmetry is assumed. Write X_F for a finite coordinate subspace, D_F = ||id:X_F→ℓ¹(F)||, and χ_m(X_F) for the monomial unconditional constant of its scalar m-homogeneous polynomials.

The target is NOT solved here. Five approaches below yield a quantitative non-symmetric special case and explicit obstructions to tempting proof shortcuts. No novelty claim is made for these elementary consequences or examples. They do not give a counterexample to the target. In particular, the Lorentz example below is not claimed to have positive uniform Bohr radius.

The inspected 2025 primary source explicitly calls the target open on PDF page 28. Proposition 2.28 and Theorem 2.29 on PDF page 32 identify the hypothesis with A := sup_{m,n} χ_m(X_n)^(1/m) < ∞. If k := inf_n K(B_X_n)>0, then A≤1/k; conversely K(B_X_n)≥1/(3A). These are the constants used below.

Every finite coordinate projection is contractive. Extending a polynomial on X_F by that projection preserves its norm and its coefficient-absolute norm. Consequently χ_m(X_F)≤χ_m(X_n) whenever F⊆{1,…,n}. This lets the arguments use arbitrary coordinate subsets, not just initial segments.

## Approach 1: a quadratic Hadamard witness, including varying-p blocks

This route succeeds for a broad block family without symmetry of the ambient space.

For d≥1, choose a symmetric Sylvester Hadamard matrix of size N, where d≤N<2d, and take its d×d principal submatrix H. Its entries are ±1, H is symmetric, ||H:ℓ¹_d→ℓ∞_d||=1, and ||H:ℓ²_d→ℓ²_d||≤√N≤√(2d). Complex interpolation gives, for 1≤p≤2,

    ||H:ℓᵖ_d→ℓᵖ′_d|| ≤ (2d)^(1/p′).

Let P(z)=zᵀHz. Hölder's inequality bounds its norm on B_ℓᵖ by (2d)^(1/p′). Because H is symmetric, its diagonal coefficients are H_ii and its off-diagonal coefficients are 2H_ij. Therefore replacing every coefficient by its absolute value gives exactly Q(z)=(Σ_i z_i)². Its norm is d^(2/p′). Hence

    χ_2(ℓᵖ_d) ≥ 2^(-1/p′) d^(1/p′),       1≤p≤2.       (1)

For 2≤p≤∞, the spectral estimate and ||z||₂≤d^(1/2−1/p)||z||p instead give

    ||P|| ≤ √(2d)d^(1−2/p),
    χ_2(ℓᵖ_d) ≥ √(d/2).                                  (2)

These are lower bounds, not asserted sharp asymptotics. They are uniform in p, including p approaching 1, and avoid a hidden dependence in probabilistic constants.

If a coordinate subspace Y satisfies a||z||p≤||z||Y≤b||z||p and L=b/a, ball inclusion gives

    χ_2(Y) ≥ L^(-2) χ_2(ℓᵖ_d).                            (3)

Combining (1)–(3) with χ_2(Y)≤A² shows that uniformly coordinate-isomorphic ℓᵖ blocks have bounded d^(1/p′) for p≤2, and bounded dimension for p≥2. In particular, a fixed p>1 cannot occur in arbitrarily large such blocks.

A precise characterization follows for X=(⊕_j ℓ^{d_j}_{p_j})_ℓ¹ with 1≤p_j≤∞, finite d_j, and consecutive coordinate blocks:

    inf_n K(B_X_n)>0  ⇔  sup_j d_j^(1/p_j′)<∞  ⇔  X=ℓ¹ as sets.

Indeed, for p_j≤2, (1) gives d_j^(1/p_j′)≤√2 A². For p_j≥2, (2) gives d_j≤2A⁴, hence d_j^(1/p_j′)≤2A⁴. The middle condition gives ||x||X≤||x||₁≤(sup_j d_j^(1/p_j′))||x||X. The reverse implication is the usual ℓ¹ argument recorded below. Thus making p_j approach 1 while enlarging finite blocks does not create a counterexample. No rearrangement invariance of X was used.

What remains: an arbitrary unconditional sequence lattice need not contain large coordinate blocks uniformly comparable to any ℓᵖ. The special case is not a reduction of the general target to these blocks.

## Approach 2: higher-degree random signs and a quantitative general inequality

Try to compare D_F with an ℓʳ embedding norm E_r(F):=||id:X_F→ℓʳ(F)||. Apply Theorem 2.22 of the inspected primary source in dimension d=|F| with c_α=m!/α!, for m≥2 and fixed 1<r≤2. The positive-coefficient polynomial is (Σ z_i)^m and has norm D_F^m by the lattice property. Moreover,

    max_α c_α(α!/m!)^(1/r) ≤ (m!)^(1/r′).

The theorem supplies signs for which the signed polynomial has norm at most

    C_r (d log m)^(1/r′)(m!)^(1/r′) E_r(F)^m.

It follows that

    D_F/E_r(F)
      ≤ A C_r^(1/m)(d log m)^(1/(m r′))(m!)^(1/(m r′)).  (4)

Taking m=max(2,ceil(log d)) and using (m!)^(1/m)≤m yields, with a constant depending on fixed r,

    D_F ≤ C'_r A (log(d+1))^(1/r′) E_r(F).               (5)

This is a real necessary condition under the hypothesis. For spaces with uniformly bounded E_r(F), it limits ℓ¹ distortion to a logarithmic power. It also recovers an obstruction to many polynomial-growth geometries.

Why this route does not finish: in an arbitrary X, E_r(F) is not uniformly bounded. Even with normalized coordinate vectors, interpolation gives only E_r(F)≤D_F^(1/r), since ||x||∞≤||x||X. Substituting into (5) gives D_F≤C_r A^(r′)log(d+1), not a uniform bound. Sending r to 1 is unjustified without control of C'_r and of the A^(r′) factor. Higher degree by itself has not removed the dimensional loss. The stronger published near-ℓ¹ estimate is therefore not replaced or improved by (5).

## Approach 3: test whether the published near-ℓ¹ bound implies equality

The published consequence D_n≤C_ε(log log n)^ε for every ε>0 does not, as a Banach-lattice statement alone, force X=ℓ¹. Here is an explicit family witnessing the gap.

Fix M=exp(exp(exp(2))) and put L(t)=log log log(t+M), w_k=1/L(k). Define X=d(w,1) as the completion of finitely supported sequences in the Lorentz norm

    ||x||X = Σ_{k≥1} w_k x*_k,

where x* is the decreasing rearrangement of |x|. The weights are decreasing, positive, tend to zero, and have divergent sum. This is a Banach sequence lattice with a 1-unconditional Schauder basis; its completion embeds into c₀ because ||x||X≥w_1||x||∞. It contains ℓ¹ continuously because w_k≤w_1.

Let W_n=Σ_{k≤n}w_k. For a decreasing nonnegative n-vector a, Chebyshev's sum inequality gives Σ w_k a_k≥(W_n/n)Σ a_k, with equality for a constant vector. Thus exactly

    D_n = n/W_n.

Since L is increasing, D_n≤L(n). Also W_n~n/L(n): the lower bound is W_n≥n/L(n), and splitting the sum at ceil(√n) gives W_n≤ceil(√n)w_1+n/L(ceil(√n)). Since L(n)/√n→0 and L(ceil(√n))/L(n)→1, the asymptotic follows. Hence D_n~L(n)→∞, while for every ε>0,

    D_n≤C_ε (log log n)^ε

for all sufficiently large n (or with harmless shifts for small n). The coordinate norms can be normalized by a single global rescaling if desired.

For completeness, unbounded D_n really implies X contains elements outside ℓ¹ here: choose positive finitely supported u_j of X-norm 1 and ℓ¹-norm at least 2^j. The series x=Σ_j 2^(-j)u_j converges in X; coordinate continuity and positivity give ||x||₁=∞ by Tonelli. Thus X is strictly larger than ℓ¹.

Outcome: the known almost-ℓ¹ estimate has a genuine logical gap to uniformity. This example does not satisfy any proved positive-Bohr hypothesis and is not a counterexample to Lempert's problem.

## Approach 4: transfer from unconditional constants to projection constants

Theorem 2.21 of the inspected source proves the desired conclusion under the stronger assumption sup_{m,n} λ(P_m(X_n))^(1/m)<∞. Its proof obtains bounded factorization constants γ₁(X_n), then a uniform absolutely-summing estimate for diagonal maps, and finally a uniform ℓ¹ embedding.

A tempting bridge would assert λ(P_m(X_n))≤C^m χ_m(X_n) uniformly. No such general bridge can hold for every m≥1: χ_1(X_n)=1 for every unconditional coordinate lattice, whereas λ(X_n*) or λ(X_n) can grow without bound, for example on Euclidean coordinate spaces. Thus unconditionality at degree 1 carries none of the projection information used by the theorem. This is a rigorous obstruction to that unqualified comparison, not a disproof of a more subtle all-degrees implication.

The all-degrees implication needed to exploit Theorem 2.21 is precisely the missing substantive step; quoting that theorem as if its hypothesis were monomial unconditionality would solve a different problem. No factorization or absolutely-summing bound sufficient to replace this step was established here.

## Approach 5: fundamental functions, symmetry, and coordinate localization

A natural attempt is to show that the fundamental function φ(n)=||Σ_{i≤n}e_i||X must be comparable to n, and then conclude X=ℓ¹. The second implication already fails without symmetry.

Take X=ℓ¹(odd coordinates) ⊕₁ c₀(even coordinates), with norm

    ||x||X = Σ_{i odd}|x_i| + sup_{i even}|x_i|.

It satisfies all the original structural assumptions, and its normalized canonical basis is 1-unconditional. Yet φ(n)=ceil(n/2)+1 for n≥2, so φ(n) is comparable to n, while X≠ℓ¹. On the even-coordinate subset F of cardinality d, X_F=ℓ∞_d and D_F=d. By (2), χ_2(X_F)≥√(d/2), so K(B_X_n) tends to zero along sufficiently large n. Thus the Bohr hypothesis correctly rejects this space, whereas an initial-segment fundamental-function argument misses its bad coordinates.

This establishes why one cannot import symmetric-space formulas using n/φ(n) as ||id:X_n→ℓ¹_n||. In this example φ(n)~n/2 but D_n grows linearly. Arbitrary-coordinate tests from Approach 1 or (4) are legitimate; simply averaging/rearranging the ambient norm would change the space and is not justified by unconditionality.

What remains: localization detects bad subsets but does not ensure that every unbounded D_F yields a sufficiently flat subset with a bounded ℓʳ embedding constant. The distribution of coordinate magnitudes can introduce logarithmic losses; no loss-free extraction was proved.

## Check of the easy direction and of set equality

If a||x||₁≤||x||X≤b||x||₁, let L=b/a. For m-homogeneous P on ℓ¹_d, its associated symmetric multilinear form T satisfies ||T||≤(m^m/m!)||P||. The ℓ¹ multilinear norm equals the maximum absolute coordinate entry of T, and the absolute-coefficient polynomial has norm at most ||T||. Hence χ_m(ℓ¹_d)≤m^m/m!≤e^m, and norm comparison gives χ_m(X_d)≤(eL)^m. The radius comparison yields K(B_X_d)≥1/(3eL), uniformly in d. These constants need not be optimal.

Conversely, a uniform D_n gives ||x||₁≤D||x||X for all x∈X by the Schauder partial sums and monotone convergence of absolute coordinate sums. Together with the assumed inclusion ℓ¹⊆X, this gives equality as sets. Equality as sets implies equivalent Banach sequence norms by the closed graph theorem. The unresolved issue is obtaining this uniform D_n from A<∞ in full generality.

## Sources and publication boundaries

Primary original source: A. Defant, Problem 6, Dirichlet Series and Function Theory in Polydiscs, Oberwolfach Report 06/2014, printed pp. 388–389: https://doi.org/10.4171/owr/2014/06

Primary recent source: Defant, Galicer, Mansilla, Mastyło and Muro, Local constants and Bohr's phenomenon for Banach spaces of analytic polynomials, arXiv:2509.26326v2: https://arxiv.org/abs/2509.26326 and https://arxiv.org/pdf/2509.26326v2. Used: Theorems 2.21–2.22, Proposition 2.28, Theorem 2.29, and the open-status discussion on PDF p. 28.

No new later-literature claim beyond SOURCE_GATE.md's dated gate is made. This authored report contains no dataset contents, source-document reproductions, or private coordination text. No publication or queue changes were performed in this task.
