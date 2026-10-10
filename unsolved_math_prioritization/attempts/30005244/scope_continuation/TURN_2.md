# Turn 2: the arbitrary-compact-support formulation is false

**Unreviewed scope-closure candidate.** This is the second substantive author turn for 30005244. The already reviewed turn-1 theorem under geometric consistency (G) is retained unchanged. This turn does not assert that (G) follows from the brief source. Instead it proves that a literal extension to every compact measurable particle is false, even for a fixed real positive frequency and a nonempty finite DDA matrix on every mesh.

## Result

For the explicit positive real frequency κ=1/10000, there exist a compact set Ω⊂R³ of positive volume and an isolated nonreal eigenvalue λ of the source-normalized volume operator

    S_κ^Ω=A_κ^Ω-I/3 on L²(Ω;C³),

such that, on the cubic grids hZ³ with h=1/n,

    Ω ∩ (1/n)Z³ = {0},
    T_κ^(1/n) = the 3×3 zero matrix, for every n≥1.

Consequently no discrete eigenvalue approaches λ. Since λ is nonreal, it lies outside the exact static lattice interval I_lat. This is an original-scope obstruction if “compact subset Ω” in the report is read without any geometric regularity or consistency requirement. It does not contradict the reviewed positive theorem for consistent particles, including all bounded Lipschitz particles.

The frequency is explicit. The construction is existential in a sufficiently advanced member of an explicitly given sequence of compact sets. No numerical spectral assertion is used.

## 1. An isolated static eigenspace of the unit ball

Let B be the open unit ball, H=L²(B;C³), and

    A_0 u = -∇ div ∫_B u(y)/(4π|x-y|)dy,
    S_0=A_0-I/3.

We need its isolated zero eigenspace, so we give the relevant classical spherical calculation rather than assume a material-resonance formula.

There is the orthogonal Helmholtz decomposition

 H = grad H_0¹(B) ⊕ grad H_harm¹(B) ⊕ (grad H¹(B))^⊥. (1)

Here constants in scalar potential spaces are factored out, and H_harm¹ denotes weakly harmonic H¹ functions. To obtain (1), project onto the closed gradient space grad H¹ using the variational Neumann problem and the Poincaré inequality. Then project its potential onto H_0¹ by the Dirichlet variational problem; the remainder is harmonic. These projections are orthogonal in the gradient norm. The last summand has distributional divergence zero and zero normal trace, equivalently the divergence of its zero extension vanishes.

On the first summand A_0 is the identity. Indeed the zero extension of a gradient of an H_0¹ potential is a whole-space gradient, and the Fourier symbol of -∇div(-Δ)^(-1) is the orthogonal projection ξξᵀ/|ξ|². On the last summand A_0 is zero.

For the middle summand use the complete solid-spherical-harmonic expansion. If H_ℓ(x)=r^ℓY_ℓ(x/r), ℓ≥1, then ∂_nH_ℓ=ℓY_ℓ on the unit sphere. The Newton single layer with density Y_ℓ equals r^ℓY_ℓ/(2ℓ+1) inside the ball. This follows directly by matching the interior r^ℓ and exterior r^(-ℓ-1) harmonic solutions continuously at r=1, with the unit jump in normal derivative. Since the divergence of the zero extension of ∇H_ℓ is -(∂_nH_ℓ)δ_(∂B),

    A_0 ∇H_ℓ = [ℓ/(2ℓ+1)] ∇H_ℓ.                  (2)

The solid-spherical-harmonic gradients form a complete orthogonal family in grad H_harm¹(B); completeness also follows by separation of variables in the harmonic expansion, with convergence in the Dirichlet integral. Thus the spectrum is obtained from the three summands in (1):

    σ(A_0)={0,1} ∪ {ℓ/(2ℓ+1):ℓ≥1} ∪ {1/2}.

In particular the zero eigenspace of S_0 is exactly the three-dimensional space V of constant vector fields (ℓ=1). All other spectral points have distance at least 1/15 from zero: the next positive one is 2/5-1/3=1/15, while the additional values are -1/3 and 2/3. Write P for orthogonal projection onto V.

## 2. A nonreal isolated eigenvalue at some small real positive frequency

For fixed bounded B, the dynamic correction C_κ=S_κ-S_0 is an entire analytic family of bounded operators. We give quantitative bounds, so the frequency can be chosen explicitly. The differentiated kernel from turn 1 gives

 C_κ = κ² C_2 - i κ³ J/(6π) + E_κ,                 (3)

where C_2 has kernel -(I+eeᵀ)/(8πr), and

    (Ju)(x)=∫_B u(y)dy.

For |κ|≤1/2 the following operator-norm bounds hold:

    ||C_2||≤1,  ||J/(6π)||=2/9,
    ||E_κ||≤2|κ|⁴,  ||C_κ||≤2|κ|².               (4)

Here is a direct verification. The Frobenius norm squared of I+eeᵀ is 6, and

 ∫_(B×B)|x-y|^-2 dxdy ≤ |B| ∫_(|z|≤2)|z|^-2 dz
                      =32π²/3,

so ||C_2||_HS²≤1. The two scalar numerators in the exact kernel are

    f(z)=exp(iz)(1-iz-z²)-1,
    g(z)=exp(iz)(z²+3iz-3)+3.

Their coefficients of z^n are respectively i^n(n-1)²/n! and -i^n(n-1)(n-3)/n! (for n≥2). For n≥4 both absolute values are at most n²/n!. Since

    ∑_(n≥4) n²/n! = 2e-9/2 < 1,

their remainders after degree three have absolute value at most |z|⁴ for |z|≤1. The Frobenius norms of I and eeᵀ have sum √3+1<3. Hence the remainder kernel has norm at most 3|κ|⁴r/(4π). Its Hilbert–Schmidt norm is at most 2|κ|⁴ because r≤2 and |B|=4π/3. These prove (4), including the final bound by the triangle inequality. The elementary inequality e<11/4 suffices for the series estimate.

Choose the circle |z|=1/30. The static resolvent norm is at most 30 there, by the spectral gap proved in Section 1. Put ε=||C_κ||. If ε≤1/60, the perturbed resolvent norm is at most 60. Its Riesz projection P_κ therefore satisfies

    ||P_κ-P|| ≤ (1/30)·60·ε·30 =60ε≤120|κ|².      (5)

This is ordinary norm-small perturbation of the fixed operator on L²(B), not of its globally zero-extended version. The latter has an additional infinite-dimensional zero eigenspace and is not being used here. When η=120|κ|²≤1/2, the projection has rank three and its range is the graph over V of an operator Γ_κ:V→V^⊥ with

    ||Γ_κ||≤η/(1-η)≤240|κ|².

For the graph bound, v∈ran(P_κ) satisfies ||(I-P)v||≤η||v|| and ||Pv||≥(1-η)||v||; the map P from ran(P_κ) onto V is an isomorphism because the projections have distance below one.

The restriction of S_κ to that invariant range, represented on V by projection along V^⊥, is

 H_κ=P S_κ(I+Γ_κ)|_V
     =P C_κ|_V + P C_κ Γ_κ,

since P S_0=0. Thus by (3)–(5),

 ||H_κ-[κ² P C_2|_V-iκ³ P J|_V/(6π)]||≤482|κ|⁴. (6)

On V, J is |B| times the identity. For real κ, the quadratic coefficient has real trace. As V has dimension three,

    Im tr(H_κ) ≤ -(2/3)κ³+1446κ⁴.                 (7)

Now fix **κ=1/10000**. It satisfies all the smallness conditions above, and 1446/10000<2/3. Therefore (7) is strictly negative. A finite matrix's trace is the sum of its eigenvalues with algebraic multiplicity; at least one eigenvalue λ of this isolated rank-three cluster has strictly negative imaginary part.

Its distance from I_lat is positive, because I_lat is real. It is an isolated finite-multiplicity eigenvalue of the full S_κ as well: S_κ is a compact perturbation of selfadjoint S_0, whose spectrum is real, or apply the reviewed compact-resolvent argument. Choose a small isolating circle Γ around λ with closed disk disjoint from I_lat.

No simplicity, rotational-symmetry splitting, or numerical identification of λ is needed. The argument works even if the cluster contains defective eigenvalues.

## 3. Compact positive-volume sets missing every rational grid point

Enumerate the countable set Q³∩closure(B) as q_1,q_2,... . For j≥1 define

    U_j = union_{k≥1} B(q_k, 2^(-j-k-4)),
    F_j = closure(B) \ U_j,
    Ω_j = F_j ∪ {0}.                               (8)

Each F_j and Ω_j is compact. Also

 |U_j| ≤ (4π/3)∑_{k≥1}2^(-3j-3k-12)
       = |B|·2^(-3j-12)/7.                         (9)

Hence F_j has positive volume and |B△F_j|→0. The sets increase with j, although monotonicity is not essential. Every rational point of closure(B) is excluded from F_j by its own open ball. Consequently

    Ω_j ∩ Q³={0},
    Ω_j ∩ (1/n)Z³={0} for every j,n≥1.             (10)

The isolated point 0 has volume zero, so L²(Ω_j) and the volume operator are unchanged by adding it. It is added solely to keep each DDA matrix nonempty. Thus the finite matrices are exactly the 3×3 zero matrices, because the source omits the only diagonal block.

## 4. The nonreal ball eigenvalue survives a sufficiently small volume removal

We must prove this step; it does not follow just from a small measure estimate for a strongly singular kernel.

Embed all continuum-support operators in L²(R³;C³), extending by zero. Let M_j and M_B be the masks of F_j and B. Put

    B_j=M_j D M_j,   B_B=M_B D M_B,
    C_j=M_j R_κ M_j, C_B=M_B R_κ M_B,

where D is whole-space convolution with p.v. K_0, and the dynamic terms are integral kernels supported on the bounded product domain. All B_j and B_B are selfadjoint with spectrum in [-1/3,2/3]⊂I_lat. Since M_j→M_B strongly,

    B_j→B_B strongly, and B_j*→B_B* strongly.       (11)

Furthermore

    ||C_j-C_B||_HS→0.                              (12)

Indeed the kernel R_κ(x-y) belongs to L²(B×B), and the product masks converge almost everywhere and are bounded by one. Dominated convergence applies to the squared kernel norm. This is convergence of only the weakly singular correction; no norm convergence of B_j is asserted.

Now apply the already reviewed abstract argument in Sections 5–6 of turn 1, with j in place of h. For clarity, its only inputs are the common selfadjoint spectral bound in I_lat, strong convergence in (11), and compact norm convergence in (12). The resolvents of B_j converge strongly and strongly in the adjoints away from I_lat. Their products with C_j converge in norm. The compact Fredholm factors are invertible on Γ for all large j, and the compact parts of the full resolvents converge in norm there. The analytic selfadjoint-resolvent terms integrate to zero inside Γ. Consequently the Riesz projections for B_j+C_j on Γ converge in norm to the nonzero finite-rank ball projection.

For all sufficiently large j their ranks are equal and positive. Fix one such finite j. Then the continuum operator on F_j, equivalently on Ω_j, has at least one eigenvalue inside Γ. Every point inside Γ is nonreal. Rename one such eigenvalue λ_j.

But by (10), every DDA matrix on Ω_j at h=1/n has spectrum {0}. Since the closed disk bounded by Γ misses the real interval and hence zero, no discrete eigenvalue is present near λ_j, for any n. This completes the counterexample.

## 5. What this settles, and what it does not

There are now two rigorously distinct proposed conclusions:

- **Positive result:** the reviewed turn-1 theorem proves spectral correctness outside the static interval for geometrically consistent cubic particle discretizations, including all bounded Lipschitz and boundary-measure-zero particles.
- **Negative result for literal unrestricted support:** the construction above refutes universal spectral approximation for arbitrary compact measurable supports, with a real positive frequency, a positive-volume compact particle, and nonempty matrices at every mesh.

Thus (G) cannot simply be dropped from the positive theorem. This does not prove (G) necessary for each individual problem, and it does not claim that the source intended fractal particles. Rather, it closes the exact ambiguity honestly: if the original wording is read unrestrictedly, it is false; if it is read in the usual consistent-particle numerical setting, the qualified theorem supplies the desired spectral conclusion.

The several hundred exact/numerical controls from turn 1 are not a substitute for this argument. This turn needs its own independent audit, especially the ball spectral decomposition, cubic Taylor coefficient, graph-of-Riesz-subspace trace, and use of continuum mask convergence rather than the invalid voxel consistency of Ω_j.
