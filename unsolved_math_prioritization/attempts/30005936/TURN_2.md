# Turn 2: high moments, meshwise maxima and explicit coefficient dependence

Substantive author turn **2/5**. The purpose is to obtain estimates usable in a later localization argument, rather than assume that a pointwise L² bound controls all grid points at once.

Retain turn 1's globally Lipschitz g, with g(0)=0 and Lipschitz constant L, and smooth deterministic initial data. For each fixed p>=2 there are constants C0,C1 depending on p,T,u0, but not on L,N,M, such that, under

                              NL²τ<=1,                            (9)

the following estimates hold. Write K_L=C0 exp(C1(1+L^4)). Then

 sup_{m,n} ||U_{m,n}||_p + sup_{t,x}||u(t,x)||_p
                         +sup_{t,n}||u_n^N(t)||_p <=K_L,           (10)
 sup_{m,n}||U_{m,n}−u_n^N(t_m)||_p <=K_L sqrt(τ/h),                 (11)
 sup_{m,n}||U_{m,n}−u(t_m,x_n)||_p <=K_L[h^(1/2)+sqrt(τ/h)].        (12)

Constants may be enlarged between displays while retaining that form. In particular, if c h²<=τ<=γh² with fixed positive c,γ, p>6, and hL²γ<=1, then

 ||max_{m,n}|U_{m,n}−u(t_m,x_n)||||_p
                         <= C exp(C(1+L^4)) h^(1/2−3/p).           (13)

The norm on the left means the L^p norm of the scalar maximum. This is a grid statement, not yet a continuous-path interpolation theorem. Without the lower comparison τ>=c h², the general cardinality factor in §5 must be retained.

## 1. Deterministic kernels and imported spatial input

Use the discrete kernel G_N of the primary paper, extended constantly in the integration variable on mesh cells, with G_N(t,x_i,x_j)=N(exp(tA_N))_{ij}. It uses exactly the Brownian-sheet cell coupling in SOURCE_SCOPE. Its eigenvalues are

 λ_{j,N}=4N² sin²(jπ/(2N)),  1<=j<N,
                    4j²<=λ_{j,N}<=π²j².                          (14)

The sine modes at grid points are bounded by sqrt(2) and orthonormal for the discrete mesh measure. Standard spectral summation gives

 sup_x∫G_N(r,x,y)²dy <=C r^(−1/2),                                (15)
 ∫_0^t∫|G_N(t−s,x,y)−G_N(t−floor_τ(s),x,y)|²dy ds
                     <=C min{sqrt(τ),Nτ},                        (16)

at grid t. For (16), integrate each exponential mode to bound the sum by CΣ_{j<N}(1−exp(−λ_{j,N}τ))²/λ_{j,N}. It is bounded by Csqrt(τ) by splitting at j≈τ^(−1/2), and by CNτ since each summand is at most τ. The identical spectral argument gives the old-noise/new-noise kernel sums for a time increment Δ, bounded by Cmin{sqrt(Δ),NΔ}. These are the deterministic estimates behind the published equations(24)–(25) and their appendices.

For the spatial kernel comparison we use a precise credited theorem, not an untracked nonlinear coefficient constant. Anton–Cohen–Quer-Sardanyons, arXiv1711.08340v1, Theorem2.1 and the following paragraph (pp6–7), quote Gyöngy's spatial L^{2p} error theorem; for C³ initial data the rate is h^(1/2), uniformly for t<=T. The spatial discretization and Brownian-sheet cells match the present ones. Apply that theorem only to:

- zero initial data, zero drift, additive coefficient identically1; Itô's isometry then yields

       sup_{t<=T,x grid} ∫_0^t∫|G_N(t−s,x,y)−G(t−s,x,y)|²dy ds <=C_T h;  (17)

- the noiseless heat equation with the fixed u0; this yields a deterministic initial-semigroup error <=C_{T,u0}h^(1/2).

These two constants concern fixed coefficients, hence are independent of the variable L in this turn. The original Gyöngy paper was not retrieved; its precise theorem is imported as stated in the cited primary numerical-analysis paper. We do not claim a new proof of that spatial approximation theorem.

The continuous heat kernel also satisfies (15). Its spatial-increment kernel sum, integrated in time, is <=C|x−y|: use the sine bound min{j|x−y|,1} and sum min{j²|x−y|²,1}/j². This supplies the spatial L^p increments used below.

## 2. BDG and a quantitative convolution argument

For deterministic K and a predictable integrand Z, the real martingale BDG inequality followed by Minkowski gives

 ||∫K(s,y)Z(s,y)dW||_p²
                <=b_p∫|K(s,y)|²||Z(s,y)||_p² dsdy.                (18)

The argument is first applied to bounded/localized integrands and then passed to the limit using the resulting bounds. This is the standard L^p replacement for Itô's isometry; no independence of the random integrand is assumed.

We shall use an elementary explicit discrete convolution bound. If nonnegative F_m satisfy

 F_m<=A+BτΣ_{k<m}(t_m−t_k)^(−1/2)F_k,

then multiplying by exp(−βt_m), taking the finite maximum, and using

 τΣ_{j>=1}(jτ)^(−1/2)exp(−βjτ)
                   <=∫_0^∞r^(−1/2)exp(−βr)dr=sqrt(π/β)

shows max_m F_m<=2A exp(βT) when Bsqrt(π/β)<=1/2. Take β=1+4πB². The same argument works for a continuous Volterra convolution. In particular B=C_p L² gives an exponential bound of the form exp(C_p(1+L^4)T). Fixed powers of L can be absorbed into this exponential.

## 3. Numerical and exact high-moment bounds

Between t_k and t_{k+1}, define the actual frozen stochastic substep

 V_n(s)=U_{k,n}exp(sqrt(N)f(U_{k,n})(W_n(s)−W_n(t_k))
                                  −N f(U_{k,n})²(s−t_k)/2).

This is a precise auxiliary definition; no ambiguous off-grid interpolation formula is needed. Conditional Gaussian integration yields

 E(|V_n(s)|^p | F_{t_k})
  =|U_{k,n}|^p exp[p(p−1)N f(U_{k,n})²(s−t_k)/2].                 (19)

Under (9), ||V_n(s)||_p²<=exp(p−1)||U_{k,n}||_p².

Unrolling the discrete recursion at grid times gives exactly

 U_m(x)=S_N(t_m)u0(x)
       +∫_0^{t_m}∫G_N(t_m−floor_τ(s),x,y)V(s,κ_N(y))
                                        f(U_{floor_τ(s)}(κ_N(y)))dW.   (20)

Here floor_τ(s) is the preceding grid time and κ_N is the left spatial grid projection. Apply (18), |f|<=L, (15), (19), and the deterministic contraction. For F_m=sup_n||U_{m,n}||_p² this gives

 F_m<=2||u0||_infinity²+C_p L²τΣ_{k<m}(t_m−t_k)^(−1/2)F_k.

The quantitative convolution argument proves (10) for U and V. The continuous and semidiscrete mild equations give the same bound for u and u^N, without condition (9). The constants are uniform in N because their kernel bound (15) is uniform.

Using their kernel increment bounds in (18) now gives

 sup_n||u_n^N(t)−u_n^N(s)||_p²
                     <=C exp(C(1+L^4))min{sqrt(t−s),N(t−s)},       (21)
 sup_x||u(t,x)−u(t,y)||_p²
                     <=C exp(C(1+L^4))|x−y|.                      (22)

The deterministic initial terms obey stronger bounds by u0∈C³. The stochastic substep itself satisfies, by its linear SDE and (18)–(19),

 sup_n||V_n(s)−U_{k,n}||_p²
                    <=C exp(C(1+L^4))Nτ,   t_k<=s<t_{k+1}.        (23)

No differentiability of g is used in these calculations.

## 4. Errors and their coefficient constants

Subtract (20) from the semidiscrete mild equation. Insert and subtract g(u^N(t_k)), g(U_k), and U_k f(U_k)=g(U_k). The four resulting terms are:

1. G_N(t_m−s)[g(u^N(s))−g(u^N(t_k))];
2. G_N(t_m−s)[g(u^N(t_k))−g(U_k)];
3. G_N(t_m−s)[U_k−V(s)]f(U_k);
4. [G_N(t_m−s)−G_N(t_m−t_k)]V(s)f(U_k),

inside the stochastic integral on each step. Apply (18) and the inequality for the norm of a sum of four terms. For E_m=sup_n||u_n^N(t_m)−U_{m,n}||_p², (16), (21), (23), and (10) imply

 E_m<=C exp(C(1+L^4))Nτ
                    +C_p L²τΣ_{k<m}(t_m−t_k)^(−1/2)E_k.           (24)

In passing from integral weights to the discrete weights, use

 ∫_{t_k}^{t_{k+1}}(t_m−s)^(−1/2)ds
                         <=2τ/(t_m−t_k)^(1/2).

The convolution bound proves (11). Keeping the sqrt(τ) alternatives instead gives the familiar companion bound K_L[τ^(1/4)+sqrt(τ/h)], but (11) suffices here.

For the spatial error, subtract the continuum and semidiscrete mild equations. Split the stochastic integrand into the kernel difference times g(u(s,y)), a coefficient difference at κ_N(y), and g(u(s,κ_N(y)))−g(u(s,y)). By (17), (10), (22), and (18), the square of the L^p spatial error F(t), maximized over grid x, satisfies

 F(t)<=C exp(C(1+L^4))h+C_p L²∫_0^t(t−s)^(−1/2)F(s)ds.

The deterministic initial error is included using §1. The same convolution bound gives sup F(t)<=C exp(C(1+L^4))h. Combining with (11) proves (12). This also explains rather than assumes the L-dependence needed later.

## 5. From individual nodes to the entire grid

For any finite family (X_j), ||max_j|X_j|||_p <=(Σ_j||X_j||_p^p)^(1/p). Therefore (12) implies

 ||max_{m,n}|U_{m,n}−u(t_m,x_n)||||_p
 <=(M+1)^(1/p)(N+1)^(1/p)K_L[h^(1/2)+sqrt(τ/h)].                 (25)

Under c h²<=τ<=γh², the number of space-time grid sites is at most C_{T,c}h^(−3), and the bracket is at most C_γ h^(1/2). This gives (13). In particular p>6 is required for a positive exponent in this elementary maximum bound. An arbitrarily fine temporal mesh cannot silently be treated as having only O(h^(−3)) sites.

## 6. Explicit cutoff family for the exact superlinear target

For R>=1 define g_R(v)=min(max(v,0),R)^(5/4). This equals the source coefficient v_+^(5/4) on [0,R], vanishes at zero, and has global Lipschitz constant L_R=(5/4)R^(1/4). It need not be C¹ at R, which is why the nonsmooth extension is useful. The coefficient bound is now quantitatively

 K_{L_R}<=C exp(CR),

and the frozen-variance condition becomes (25/16)Nτ R^(1/2)<=1. Under balanced refinement and that condition,

 ||max_{m,n}|U^R_{m,n}−u^R(t_m,x_n)||||_p
                           <=C exp(CR) h^(1/2−3/p).                (26)

Constants C depend on p,T,u0,c,γ, not on R or the mesh. This is the specific superlinear-cutoff estimate sought in this turn. Its proof required higher moments, the grid cardinality and explicit coefficient growth, not another approximation-packaging step.

The bound is not yet a theorem for the uncut coefficient. Removing R requires control of exact and numerical exit events; simply sending R to infinity in (26) is invalid. Original unresolved2/5.
