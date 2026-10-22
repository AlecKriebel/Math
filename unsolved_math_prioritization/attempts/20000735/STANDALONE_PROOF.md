# A Chebyshev solution of an Andrews–Gordon Nahm system

## Scope and established dependencies

This is a family-level verification relevant to AIM Problem 2.4 in *Mock modular forms in combinatorics and arithmetic geometry* (2010), p. 2. It does not solve that problem's general program relating Bailey pairs, orthogonal polynomials, and Bloch groups. No novelty is claimed. The Andrews–Gordon identity, the dilogarithmic and algebraic-K-theoretic setting, and ADET torsion results are established prior work.

The proof below is elementary except for two clearly identified dependencies: the established Andrews–Gordon sum–product identity, and the number-field Bloch-group rank theorem (Borel–Suslin). The latter may be replaced here by the rank-zero consequence of Borel's calculation of K-theory and Suslin's surjection onto the ordinary Bloch group. Neither an exact torsion order nor a universal criterion for modularity is asserted.

## 1. Definitions and statement

Fix an integer r ≥ 1 and put M = 2r + 3. For 1 ≤ i,j ≤ r define

    A_ij = 2 min(i,j).

Let U_j be the Chebyshev polynomial of the second kind, characterized by

    U_0(c) = 1,  U_1(c) = 2c,
    U_{j+1}(c) = 2c U_j(c) − U_{j−1}(c).

Set θ = π/M, c = cos θ, and

    u_j = U_j(c) = sin((j+1)θ)/sin θ  (0 ≤ j ≤ r+1),
    x_i = u_{i−1}u_{i+1}/u_i² = 1 − u_i^(−2)  (1 ≤ i ≤ r).

For a = 1,…,r+1 also put B_i^(a) = max(0,i−a+1), and define an unshifted power series

    F_{r,a}(q) = Σ_{n_1,…,n_r ≥ 0}
        q^(Σ_{j=1}^r N_j² + Σ_{j=a}^r N_j)
        / ((q)_{n_1} ⋯ (q)_{n_r}),

where N_j = n_j + ⋯ + n_r and (q)_n = ∏_{m=1}^n (1−q^m). The second sum is empty for a = r+1. These are formal power series in q; the same identities hold analytically for |q| < 1. A normalization q^C, if needed for a modular-function statement, is outside the coefficient comparison here.

The claims are:

1. A is positive definite. The displayed x is the unique solution in (0,1)^r to

       1−x_i = ∏_{j=1}^r x_j^(A_ij).

2. K = Q(cos(π/M)) is a totally real number field, all x_i lie in K, and their ordinary Bloch symbol sum ξ_r = Σ_i[x_i] is a torsion element of B(K), in the precise convention fixed in §4.

3. Every F_{r,a} has quadratic matrix A, with linear vector B^(a), while the F_{r,a} are pairwise distinct. For a < b ≤ r+1 their coefficients agree below degree a, and

       [q^a]F_{r,b} − [q^a]F_{r,a} = 1.

Consequently the assignment retaining only A's distinguished positive solution and its ordinary Bloch element is noninjective on this family. This assertion concerns that assignment, not all possible enhanced constructions from Bailey data.

## 2. The elementary Chebyshev calculation

The sine addition formula proves the stated expression for U_j(c) by its recurrence and initial conditions. The identity

    sin²((j+1)θ) − sin(jθ) sin((j+2)θ) = sin² θ

gives

    u_j² − u_{j−1}u_{j+1} = 1.

This proves the two formulas for x_i agree. Since

    θ < (i+1)θ ≤ (r+1)θ < π/2,

we have u_i > 1 and hence 0 < x_i < 1. Also (r+2)θ = π−(r+1)θ, so u_{r+1} = u_r, and u_0 = 1.

For each i = 1,…,r, cancellation of consecutive factors gives

    ∏_{j=i}^r x_j
       = ∏_{j=i}^r (u_{j−1}u_{j+1}/u_j²)
       = u_{i−1}u_{r+1}/(u_i u_r)
       = u_{i−1}/u_i.

Define E_0 = 1 and E_i = ∏_j x_j^(2 min(i,j)). Then

    E_i/E_{i−1} = (∏_{j=i}^r x_j)² = (u_{i−1}/u_i)².

With x_0 = 0 as a notational device only, the same ratio holds for 1−x_i:

    (1−x_i)/(1−x_{i−1}) = u_{i−1}²/u_i².

Both sequences start at 1, so E_i = 1−x_i. This proves the Nahm equations exactly. The index 0 is not an extra unknown in the system.

The orthogonal-polynomial aspect is also literal. Substitution c = cos t shows

    ∫_{−1}^1 U_i(c)U_j(c)√(1−c²) dc
      = ∫_0^π sin((i+1)t)sin((j+1)t) dt
      = (π/2) δ_ij.

Thus the polynomials used here are an orthogonal family, rather than merely a suggestive recurrence. This does not establish an analogous construction for arbitrary orthogonal polynomials.

## 3. Positive definiteness and uniqueness

Let L be the r×r matrix with L_ij = 1 for i ≥ j and 0 otherwise. Direct multiplication gives A = 2LL^T. Since L is invertible, A is positive definite.

For t in the convex domain (0,∞)^r define

    Φ(t) = (1/2)t^TAt + Σ_i Li_2(e^(−t_i)).

The real dilogarithm on (0,1) satisfies

    d/dt Li_2(e^(−t)) = log(1−e^(−t)).

Therefore

    (∇Φ(t))_i = (At)_i + log(1−e^(−t_i)),
    Hess Φ(t) = A + diag(1/(e^(t_i)−1)).

The Hessian is positive definite everywhere. In particular, along any nonconstant line segment in the domain the gradient is strictly monotone, so Φ has at most one critical point. Writing x_i = e^(−t_i), the critical equations are exactly

    log(1−x_i) = Σ_j A_ij log x_j,

equivalent to the stated Nahm equations because all quantities are positive real numbers. The solution in §2 supplies existence, so there is exactly one such point. Strict convexity alone is not being used to assert existence or to classify nonpositive or complex solutions.

## 4. The ordinary Bloch group and torsion

We fix the ordinary Suslin convention, also used in Garoufalidis, Definition 1.2. Let P(K) be generated by symbols [z], z ∈ K\{0,1}, modulo the ordinary five-term relations. Let

    T(K) = (K* ⊗_Z K*) / ⟨a⊗b + b⊗a⟩,
    ∂: P(K) → T(K),  [z] ↦ z ∧ (1−z),
    B(K) = ker ∂.

In this notation ∧ is antisymmetric, but a∧a need not itself be zero: only 2(a∧a)=0 follows formally. The alternating exterior-square convention additionally kills a∧a. The present element has zero boundary already in the stricter antisymmetric convention, so there is no unresolved factor-of-two issue.

To see that K is a totally real number field, take ζ = exp(πi/M), a primitive 2M-th root of unity. Then c = (ζ+ζ^(−1))/2. Every embedding of Q(c) into C extends to the cyclotomic field and sends c to a real number (ζ^k+ζ^(−k))/2. Moreover each u_i is an integral polynomial in c, and x_i = 1−1/u_i² belongs to K. The denominators are nonzero by §2.

By the Nahm equations and bilinearity,

    ∂ξ_r = Σ_i x_i ∧ (1−x_i)
          = Σ_{i,j} 2min(i,j) x_i ∧ x_j.

For i < j the two cross terms cancel by antisymmetry. The diagonal term is 2i(x_i∧x_i)=0 because 2(x_i∧x_i)=0. Hence ξ_r ∈ B(K).

The established rank theorem for number fields states

    dim_Q(B(K) ⊗_Z Q) = r_2(K),

where r_2(K) is the number of conjugate pairs of non-real embeddings. Here r_2(K)=0, and therefore ξ_r is torsion. Indeed, for any abelian group G, an element maps to zero in G⊗Q exactly when some positive integer annihilates it. No finite-generation assumption is needed for this last implication.

For a primary-source route tailored to this rank-zero case, Borel's Proposition 12.2 gives the K-theoretic rank in degree 3, and Suslin's Theorem 5.2 gives a surjection K_3(K)_ind → B(K). Since K is totally real, the rational degree-three K-group is zero, so its indecomposable quotient and then B(K) are rationally zero. The familiar rank statement and its regulator interpretation are also set out by Zagier, printed pp. 18 and 59. These are dependencies, not claims to reprove Borel or Suslin.

No exact order of ξ_r follows from this argument. In particular, reading a denominator in a dilogarithm value is not a substitute for fixing an integral convention and proving an order statement.

## 5. Relation to the ADET theorem and complementary variables

Let T_r be the tridiagonal r×r matrix with off-diagonal neighbors −1, diagonal 2 except for the last entry 1. For r=1 this is the matrix (1). It is the tadpole Cartan matrix in the orientation with the loop at the last vertex. Directly,

    (T_r)^(-1)_ij = min(i,j),
    A = (2) ⊗ (T_r)^(-1) = C(A_1) ⊗ C(T_r)^(-1).

For example, multiplying the second-difference rows of T_r into min(i,j) gives the identity; the final row uses min(r,j)−min(r−1,j), which is 1 only for j=r.

Lee's Theorem 1.3 applies to matrices C(X)⊗C(X′)^(-1) for a pair of ADET diagrams. His equation is written

    y_i = ∏_j (1−y_j)^(A_ij).

Accordingly his variable here is y_i = 1−x_i = u_i^(−2). It is not x_i with the notation silently left unchanged. The theorem asserts torsion for all number-field solutions in the group defined in his §2, which rationalizes the boundary target and imposes [z]+[1−z] and [z]+[1/z] as relations. In Lee's convention the sums for complementary variables are negatives of each other.

In the ordinary convention of §4 one instead has

    [z] + [1−z] = c_K,
    ξ_r + Σ_i[1−x_i] = r c_K,
    6c_K = 0.

Suslin proves independence of c_K in Lemma 1.3 and 6c_K=0 in Lemma 1.5. This finite torsion distinction matters for exact-order questions. We do not silently identify Lee's group with the integral ordinary group. The ordinary torsion proof in §4 does not depend on such an identification.

Garoufalidis's extended Bloch group is different again: its generators include integer logarithm-branch data [z;p,q], with a lifted boundary involving logarithms. An ordinary class [z] does not specify those branches or all information of an extended class. Our noninjectivity result below does not assert that every extended construction also forgets the terminal choice.

## 6. Exact terminal-choice noninjectivity

Expanding the sums of squares and linear terms gives

    Σ_j N_j² = Σ_{i,k} min(i,k)n_i n_k = (1/2)n^TAn,
    Σ_{j=a}^r N_j = Σ_{i=1}^r max(0,i−a+1)n_i.

Thus the quadratic matrix is the same A for every a, while the linear vectors are distinct: if a<b then B_a^(a)=1 and B_a^(b)=0. The equations in §§2–3 depend only on A, so both the distinguished x and ξ_r are the same.

The established Andrews–Gordon identity, in Kirillov's Theorem C, equation (2.1.a), is

    F_{r,a}(q) = ∏_{m≥1, m not congruent to 0, a, −a modulo M} (1−q^m)^(-1).

Fix a<b≤r+1. Every positive integer m<a is allowed in both products: neither a nor b has yet occurred, and the complementary residues M−a and M−b are at least r+2>a. At m=a the a-product excludes the part a, whereas the b-product includes it. Factors of degrees greater than a cannot affect coefficients through q^a. Consequently, modulo q^(a+1), the b-product is the a-product multiplied by (1−q^a)^(-1). The shared lower-degree product has constant coefficient 1, giving

    F_{r,b}(q) − F_{r,a}(q) = q^a + O(q^(a+1)).

This proves all series are distinct and establishes the asserted noninjectivity exactly, including the endpoint a=r+1 when it is the larger index. The statement compares the unshifted series just defined. It does not compare differently shifted powers q^C as if their exponents were unchanged.

## 7. What this does and does not establish

This gives an explicit orthogonal-polynomial solution, a well-defined torsion class in a fixed ordinary Bloch convention, and a precise example of information lost by retaining only the distinguished A-dependent class. It does not construct a transformation dictionary for arbitrary Bailey pairs, compute a torsion order, recover the linear or constant exponent from ξ_r, or prove modularity of arbitrary Nahm data. Positive definiteness and a real distinguished solution are not by themselves a general modularity criterion. Lee's introduction explicitly records the failure of the original broad equivalence as formulated there.

The AIM source already remarks that one A may admit more than one B,C. The loss-of-parameters observation is therefore credited as an explicit instance of known structure, not a first discovery. The original broad AIM problem remains unresolved by this work.

## Sources and precise reading pins

1. AIM, *Mock modular forms*, workshop March 8–12, 2010: p. 2, Problem 2.4 and its surrounding Nahm-sum notation and multiple-B,C remark. https://aimath.org/WWN/mockmodular/mockmodular.pdf
2. A. N. Kirillov, *Dilogarithm identities*, arXiv:hep-th/9408113v2: printed/PDF p. 34, Theorem C and equation (2.1.a); p. 35 for N_i and the range/endpoints. The journal version is *Progress of Theoretical Physics Supplement* 118 (1995), 61–142. https://arxiv.org/abs/hep-th/9408113v2
3. A. A. Suslin, *K_3 of a field and the Bloch group*: printed p. 218/PDF p. 2, ordinary group and Lemma 1.3; printed p. 219/PDF p. 3, Lemma 1.5; printed p. 237/PDF p. 21, Theorem 5.2. https://www.maths.dur.ac.uk/users/herbert.gangl/Suslin_K3_Bloch_group.pdf
4. A. Borel, *Stable real cohomology of arithmetic groups*, Ann. Sci. École Norm. Sup. (4) 7 (1974), 235–272: Proposition 12.2, printed p. 271/PDF p. 38. https://numdam.org/item/10.24033/asens.1269.pdf
5. D. Zagier, *The Dilogarithm Function*, in *Frontiers in Number Theory, Physics, and Geometry II* (2007), 3–65: printed p. 18/PDF p. 16 and printed p. 59/PDF p. 57 state the Bloch rank/regulator theorem and explain torsion-convention issues. https://www.maths.dur.ac.uk/users/herbert.gangl/zagier_dilog.pdf
6. C.-H. Lee, *Nahm's conjecture and Y-system*, arXiv:1109.3667v3: p. 2, equation (1.1), Theorem 1.3, and caveat about the original conjecture; pp. 3–4, Definition 2.1 and regulator criterion; p. 6, §3.2 tadpole folding; p. 9, Proposition 4.1. https://arxiv.org/abs/1109.3667v3
7. S. Garoufalidis, *q-Terms, Singularities and the Extended Bloch Group*, author-hosted version dated August 31, 2010: p. 3, Definition 1.2 and equations (3)–(5); pp. 6–7, ordinary/extended distinction and Definition 3.1; p. 18, §6.3 comparison. https://people.math.gatech.edu/~stavros/publications/qtermssingularities.pdf

Finite exact computations accompanying this proof are reproducibility diagnostics, not replacements for the arbitrary-r arguments or the named theorems.
