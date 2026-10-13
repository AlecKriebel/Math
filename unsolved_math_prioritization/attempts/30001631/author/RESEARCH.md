# Takhtajan–Zograf curvature: five partial approaches

Problem identifier: 30001631 / OWR-4535-006.
Research date: 2026-10-05. Status: **NO RESOLUTION**.

This note does not prove or disprove curvature negativity for the finite-dimensional Takhtajan–Zograf metric. It contains elementary rigorous reductions, exact model calculations, and precise obstructions to five attempted routes. None is asserted to be new. The computations at the end check finite algebraic identities; they are not numerical evidence about an actual Riemann surface.

## 1. Target and conventions

The primary source is Kunio Obitsu's contribution to *Teichmüller Theory*, Oberwolfach Report 53/2010, pp. 3128–3130, specifically the third open problem on p. 3130 [O]. Its subject is negativity of TZ curvature on punctured moduli spaces. It does not choose between real sectional, holomorphic sectional, holomorphic bisectional, or Ricci curvature. The following problem asks about the negative Ricci form, but that does not remove the ambiguity. We do not silently replace the question by one of these inequivalent assertions.

Use the finite-dimensional cuspidal metric, not an elliptic/orbifold variant or the Weil–Petersson metric. Let X = Gamma\H have genus g and n punctures, n > 0, 2g - 2 + n > 0, and complex deformation dimension d = 3g - 3 + n > 0. The three-punctured sphere has d = 0 and no nonzero curvature directions. The n = 0 cuspidal sum is zero and is not the metric under discussion.

Normalize the fiber hyperbolic metric to ds_X^2 = y^(-2)|dz|^2 and each cusp generator to z -> z + 1. For harmonic Beltrami differentials mu,nu put

    g_a(mu,nu) = integral_X E_a(z,2) mu(z) conjugate(nu(z)) dA_hyp(z),
    g_TZ = sum_(a=1)^n g_a.

Here E_a is the cusp Eisenstein series with leading term y^2 in its normalized cusp. These are the conventions in [OTW, §1.1] and [PTT, §2.1.2]. Each g_a and their sum are Kähler. The sum is invariant under permutations of cusps by the mapping class group and descends to moduli. Individual g_a are naturally defined on Teichmüller space or the labeled/appropriate subgroup quotient. Local curvature calculations on the smooth orbifold charts and on Teichmüller space agree. No assertion about curvature at a coarse-space singularity is needed.

For Hermitian coefficient matrix G use omega = (i/2) G_(i bar j) dz_i wedge dbar z_j and the curvature convention

    R_(i bar j k bar l) = -partial_k partial_bar_l G_(i bar j)
       + sum_(p,q) G^(p bar q) (partial_k G_(i bar q))
                                      (partial_bar_l G_(p bar j)).       (1)

The expression H(v) = R(v,bar v,v,bar v)/G(v,bar v)^2 will be called the reduced holomorphic sectional curvature. Its sign is the real holomorphic sectional sign; in complex dimension one the Gaussian curvature of ds^2 = G|dz|^2 is 2H. Bisectional curvature uses R(v,bar v,w,bar w)/(G(v,bar v)G(w,bar w)). The Ricci coefficient matrix is -partial partial_bar log det G. Strictly negative bisectional curvature implies strictly negative holomorphic sectional and Ricci curvature. These do not settle the sign of every real two-plane merely by terminology. In dimension one all the relevant sign questions agree.

A positive constant rescaling G -> cG gives R -> cR, H -> H/c, and leaves the Ricci coefficient form unchanged. Thus a fixed positive normalization cannot reverse a sign. A nonconstant conformal factor can reverse it, as Approach 5 shows. The hyperbolic fiber metric is complete; the TZ metric on the deformation space is incomplete [OTW]. These are different completeness statements.

## 2. Approach 1: unfold the cusp, then try a Hilbert-space curvature argument

### Proposition 1 (exact unfolded norm and Fourier formula)

Normalize the cusp a to infinity and write a tangent representative as

    mu(z) = y^2 conjugate(q(z)),
    q(z) = sum_(m>=1) a_m exp(2 pi i m z).

Then

    g_a(mu,mu) = integral_0^infinity integral_0^1 |mu(x+iy)|^2 dx dy
               = 3/(128 pi^5) sum_(m>=1) |a_m|^2/m^5.                 (2)

In particular g_a is positive definite on the nonzero harmonic tangent space. Polarization gives the mixed pairing. The numerical coefficient in (2) uses mu = y^2 conjugate(q); replacing q by the common convention giving mu = -2y^2 conjugate(q) changes that coefficient by 4.

Proof. Let F be a fundamental region for Gamma and Gamma_a the normalized cusp subgroup. The function |mu|^2 is Gamma-invariant, as a scalar norm of an invariant Beltrami tensor. Substitute

    E_a(z,2) = sum_(gamma in Gamma_a\Gamma) Im(gamma z)^2

in the nonnegative norm integral and use Tonelli's theorem. Change variables w = gamma z in each summand. Hyperbolic area is invariant, and the translates gamma F tile Gamma_a\H up to measure zero. Therefore the integral is

    integral_(Gamma_a\H) Im(w)^2 |mu(w)|^2 dA_hyp(w)
      = integral_(0<x<1, y>0) |mu(w)|^2 dx dy.

The original integral is finite: on the compact core its integrand is smooth; at a cusp a harmonic representative from an integrable holomorphic quadratic differential decays as O(y^2 exp(-2 pi y)), whereas each Eisenstein series has at most quadratic growth. These bounds give integrability. In a width-one cusp q is periodic and is holomorphic in exp(2 pi i z), with zero constant term because it is a cusp form. Parseval on each horizontal circle gives

    integral_0^1 |q(x+iy)|^2 dx = sum_(m>=1) |a_m|^2 exp(-4 pi m y).

A second application of Tonelli and four integrations by parts give

    integral_0^infinity y^4 exp(-4 pi m y) dy
      = 4!/(4 pi m)^5 = 3/(128 pi^5 m^5).

This proves (2). Every coefficient weight is positive; if the norm vanishes all a_m vanish, so q and mu vanish. QED.

This is consistent with the cusp Fourier calculation in [Teo24, §6], after matching the normalization of the quadratic differential. It supplies an actual TZ norm identity, not a curvature computation.

### Lemma 2 (the tempting holomorphic Gram criterion)

Let u_1(z),...,u_d(z) be holomorphic maps into a fixed complex Hilbert space, linearly independent at each point, and G_(i bar j) = <u_i,u_j> (inner product linear in its first argument). Assume G is Kähler when it is viewed as a tangent metric. Let P be orthogonal projection to the span of the u_i. Then

    R(v,bar v,w,bar w)
      = -||(I-P) sum_(i,k) v_i w_k partial_k u_i||^2 <= 0.           (3)

Proof. Holomorphy gives partial_k G_(i bar j) = <partial_k u_i,u_j> and partial_k partial_bar_l G_(i bar j) = <partial_k u_i,partial_l u_j>. The inverse-Gram term in (1) is the inner product of the orthogonal projections of these derivatives. Subtracting it from the full inner product gives (3). This argument takes place in a finite-dimensional span plus the finitely many derivative vectors, so no infinite-dimensional convergence assertion is hidden. QED.

Attempt. Formula (2) identifies each tangent space with a weighted sequence space. If these embeddings formed a holomorphic Gram frame in a single fixed Hilbert space, (3) would give nonpositive bisectional curvature; strictness would require a nonzero normal derivative for every nonzero pair v,w.

Exact obstruction. Formula (2) is a fiberwise isometry. It does not prove holomorphic dependence of the harmonic Beltrami representatives or their cusp Fourier coefficients on deformation parameters. Harmonic projection, the uniformizing group, and the cusp normalization all vary. Indeed even a positive scalar metric can be represented fiberwise by the smooth one-vector Gram expression u(z) = sqrt(G(z)); this gives no curvature sign unless u is holomorphic. For G(z) = exp(-|z|^2), equation (1) gives R_(z bar z z bar z)(0) = 1 > 0, despite this smooth Gram representation.

The Bers/Velling–Kirillov relation [Teo06, Theorem 5.1] concerns the parabolic cyclic universal space; its Remark 5.3 explicitly distinguishes the finite-group Bers maps. We have neither established the required finite-dimensional holomorphic isometric identification nor controlled the relevant second fundamental form. No sign can be imported by identifying names of metrics. Route blocked at that holomorphic-variation/ambient-curvature step.

## 3. Approach 2: sum the cuspidal metrics without losing signs

### Proposition 3 (curvature of a positive sum)

Let G = sum_a G_a be a finite sum of positive Kähler metrics in one holomorphic coordinate chart. For fixed (1,0) vectors v,w, define the row covectors

    b_a = (partial_w G_a)(v,bar e_q)_q,
    b = sum_a b_a,  c = b G^(-1).

Then

    R_G(v,bar v,w,bar w) = sum_a R_(G_a)(v,bar v,w,bar w) - D,
    D = sum_a (b_a - cG_a) G_a^(-1) (b_a - cG_a)^* >= 0.            (4)

Proof. The second-derivative terms in (1) add. The difference between the sum of the individual first-derivative terms and the combined one is

    D = sum_a b_a G_a^(-1)b_a^* - bG^(-1)b^*.

Expand the squared expressions in (4). Their cross terms sum to -bc^* - cb^*, and their final terms sum to cGc^*. Since cG = b, the net result is the preceding expression for D. Every summand in (4) is a nonnegative squared norm because G_a is positive definite. QED.

Consequences. If all g_a have nonpositive bisectional curvature, so does g_TZ. Strict negativity of one summand on each tested pair suffices for strict negativity of the sum. The same statement for v=w only requires nonpositive holomorphic sectional curvature of the summands. More quantitatively, if H_a(v) <= -kappa_a for positive constants kappa_a, put x_a = G_a(v,bar v). Then

    H_G(v) <= -sum_a kappa_a x_a^2/(sum_a x_a)^2
            <= -1/(sum_a kappa_a^(-1)).                            (5)

The last inequality follows by Cauchy–Schwarz applied to sqrt(kappa_a)x_a and 1/sqrt(kappa_a). This is an exact tensor inequality; no assumption that summands share normal coordinates is necessary.

Attempt. Apply (4) to the n cusp metrics. Positivity and Kählerness of all summands are established for the actual metric, so the algebraic reduction is applicable.

Exact obstruction. The needed upper bounds for R_(g_a) are not proved here. The positive norm identity in Approach 1 gives values of g_a, not their second moduli derivatives. The correction D can help, but no bound shows that it dominates any positive cuspidal curvature contributions. Even knowing total Ricci information would not supply all the summand bisectional signs. The route is a sufficient reduction, not an equivalent reformulation and not a proof of negativity.

## 4. Approach 3: use the Kähler potential and isolate the missing fourth derivatives

### Proposition 4 (potential criterion)

Suppose locally G_(i bar j) = C partial_i partial_bar_j psi, C > 0, and write Psi for the positive complex Hessian of psi. Then

    R_(i bar j k bar l)/C = -psi_(i bar j k bar l)
             + sum_(p,q) Psi^(p bar q) psi_(i bar q k) psi_(p bar j bar l). (6)

For bisectional negativity the contraction of the fourth derivative on v,bar v,w,bar w must strictly exceed the nonnegative inverse-Hessian quadratic term in (6). In holomorphic normal coordinates at one point the first derivatives of G vanish, so (6) reduces there to minus C times that fourth derivative.

Proof. Substitute G = C Psi and G^(-1) = C^(-1) Psi^(-1) into (1); mixed derivatives commute for a smooth potential. Contracting the inverse-Hessian term with v,bar v,w,bar w produces b Psi^(-1)b^* >= 0. Holomorphic normal coordinates for a Kähler metric give partial G = 0 at the chosen point. QED.

### Proposition 5 (positive line-bundle curvature does not settle metric curvature)

For every real a the potential

    psi_a(z) = sum_(i=1)^d |z_i|^2 + a|z_1|^4

has positive Hessian on a sufficiently small neighborhood of the origin. Its metric has

    R_(1 bar 1 1 bar 1)(0) = -4a.                                 (7)

At the same time the Hermitian line metric h = exp(-psi_a) has positive Chern form proportional to i partial partial_bar psi_a throughout that neighborhood.

Proof. The Hessian is diagonal, with first entry 1 + 4a|z_1|^2 and all others 1; shrink the neighborhood if a < 0. All first derivatives of this matrix vanish at zero and its only relevant second derivative is 4a. Equation (1) gives (7). The Chern form of h is -(i/(2pi)) partial partial_bar log h = (i/(2pi)) partial partial_bar psi_a, which is positive because the Hessian is positive. Both signs of (7), and zero, are therefore compatible with positive Chern form. QED.

Attempt. The TZ potentials and tautological Chern-form identities in [PTT, §4] provide actual geometric potentials. One could differentiate them twice more and prove (6)'s strict inequality.

Exact obstruction. A potential's strict plurisubharmonicity is a second-derivative statement. The curvature question requires the fourth-order combination (6). The known local-index identities concern curvature of determinant/tautological line bundles, rather than the Riemann tensor of their associated TZ tangent metric. Proposition 5 rigorously rules out the implication based on positivity alone. No global fourth-derivative inequality for the actual cusp potentials was obtained. This route remains blocked.

## 5. Approach 4: plumbing asymptotics, with derivative and submanifold controls

### Proposition 6 (normal cusp model)

On 0 < |t| < exp(-L_0), put r = |t|, L = -log r and

    ds_p^2 = C |dt|^2/(r^2 L^p),    C > 0, p > 0.

Its Gaussian curvature is

    K_p = -p/(2C) L^(p-2).                                        (8)

Its radial distance to t=0 is finite if and only if p > 2; for p > 2 that distance from r_0=exp(-L_0) is

    sqrt(C)/(p/2 - 1) L_0^(1-p/2).                               (9)

Proof. For a conformal metric lambda|dt|^2, K = -(1/(2lambda)) Delta_0 log lambda. For any radial function F(L), Delta_0 F(L) = F''(L)/r^2. Here log lambda = log C + 2L - p log L, whose second derivative is p/L^2. This gives (8). The radial length is sqrt(C) integral_(L_0)^infinity L^(-p/2)dL, yielding precisely (9) and the convergence criterion. QED.

The exponent suggested by normal TZ plumbing behavior is p=4, giving K=-2L^2/C for this exact one-dimensional model. This is a statement about the displayed model only.

### Proposition 7 (a C^0 asymptotic can have both curvature signs)

Let lambda_0 = C/(r^2 L^4), h(L) = L^(-1)sin(L^3), and lambda = exp(h)lambda_0. Then lambda/lambda_0 -> 1 as r -> 0. Nevertheless the curvature of lambda|dt|^2 takes both signs arbitrarily close to zero.

Proof. Direct differentiation gives

    h''(L) = (2/L^3 - 9L^3) sin(L^3),
    K = -exp(-h)/(2C) L^4 [4/L^2 + h''(L)].                       (10)

At L_k = (pi/2 + 2pi k)^(1/3), the bracket is 4/L_k^2 + 2/L_k^3 - 9L_k^3, which is negative for all sufficiently large k. Hence K > 0 there. At M_k = (3pi/2 + 2pi k)^(1/3), the bracket is 4/M_k^2 - 2/M_k^3 + 9M_k^3, positive for all sufficiently large k, so K < 0. Both sequences tend to infinity, corresponding to r -> 0. Meanwhile |h| <= 1/L, proving the claimed metric asymptotic. QED.

A sufficient differentiated asymptotic for a conformal slice is lambda/lambda_0 -> 1 together with

    Delta_0 log(lambda/lambda_0) = o(1/(r^2 L^2)).                 (11)

Substituting in the conformal curvature formula then proves K ~ -2L^2/C. This implication is rigorous; its hypotheses have not been verified here for every actual TZ deformation direction.

### Proposition 8 (negative curvature of a holomorphic slice is insufficient)

There is a holomorphic curve in flat complex two-space whose induced Gaussian curvature is strictly negative. Therefore negativity computed on a plumbing curve does not by itself imply negative ambient holomorphic sectional curvature.

Proof. The curve F(t)=(t,t^2) in C^2 with its flat Hermitian metric has induced coefficient lambda=1+4|t|^2. The conformal formula gives

    K_curve = -8/(1+4|t|^2)^3 < 0.

The ambient curvature is identically zero. This is also the sign direction in the Kähler Gauss equation: intrinsic holomorphic curvature equals ambient curvature along the tangent minus a nonnegative second-fundamental-form term. QED.

Actual incompleteness, independently of a curvature sign, follows from the normal upper estimate in [OTW]: along a one-node plumbing ray its square norm is at most C_epsilon/(r^2 L^(4-epsilon)). Fix 0 < epsilon < 2. The ray has finite length by the integral in (9), approaches the missing nodal boundary, and yields an incomplete end. This agrees with the published incompleteness result and has no sign consequence.

Attempt. Use increasingly sharp plumbing and Eisenstein asymptotics, including the full-expansion program of [MZ], to control curvature near boundary strata.

Exact obstruction. We have not verified the differentiated remainder and inverse-metric estimates required for the entire TZ Riemann tensor, particularly its mixed tangential/normal directions. The OWR pointwise comparison alone cannot support differentiating error terms. Even a verified negatively curved induced slice would need transverse second-fundamental-form estimates to give an ambient upper bound; in dimensions greater than one there are also interior and mixed planes to address. The toy oscillatory metric is not an actual TZ counterexample. Route blocked at these explicit analytic estimates.

## 6. Approach 5: compare with WP by a scalar factor or determinant

### Proposition 9 (the exact dimension-one comparison)

On a complex one-dimensional deformation space, write g_TZ = f g_WP with f > 0. For the convention Delta_WP = lambda_WP^(-1) Delta_0, where Delta_0 = partial_x^2 + partial_y^2,

    K_TZ = f^(-1) [K_WP - (1/2) Delta_WP log f].                 (12)

For any nonzero harmonic mu spanning the tangent line,

    f = [integral_X (sum_a E_a(z,2)) |mu|^2 dA_hyp]
                       /[integral_X |mu|^2 dA_hyp].             (13)

Thus curvature negativity in this case is equivalent to

    Delta_WP log f > 2 K_WP.                                    (14)

Proof. Equation (13) is the quotient of the two defining norms; it is unchanged when mu is multiplied by a nonzero scalar. Write lambda_TZ = f lambda_WP and use

    K_TZ = -(2f lambda_WP)^(-1) Delta_0(log f + log lambda_WP),

which is (12). Since f is positive, (14) is exactly the strict negativity condition. QED.

The positive weight in (13) does not imply (14). To see the general logical failure, at any chosen coordinate origin take f_a=exp(a|z|^2). Then f_a(0)=1 and

    K_(f_a g_WP)(0) = K_WP(0) - 2a/lambda_WP(0).

The right side has either sign as a varies, even though f_a is everywhere positive. This example varies a generic conformal factor, not the actual TZ factor (13).

### Proposition 10 (higher-dimensional determinant comparison)

Let W and G be positive Hermitian matrices for WP and TZ in the same holomorphic coordinates and A = W^(-1)G. Then det A > 0 and

    Ric_TZ = Ric_WP - partial partial_bar log det A.              (15)

Proof. A is similar to the positive Hermitian matrix W^(-1/2) G W^(-1/2), so its determinant is positive. The identity det G = det W det A gives (15) on applying -partial partial_bar log. More explicitly, for any positive matrix metric G,

    partial_i partial_bar_j log det G
      = tr(G^(-1) partial_i partial_bar_j G
         - G^(-1)(partial_bar_j G)G^(-1)(partial_i G)),            (16)

by differentiating the determinant and partial G^(-1) = -G^(-1)(partial G)G^(-1). Thus (15) involves real second derivatives of a genuine scalar quantity, but not just its pointwise size. QED.

Attempt. For (g,n)=(1,1) or (0,4), dimension one might make (13) and variations of Eisenstein series manageable. More generally one might bound the Hessian of log det A and obtain Ricci negativity first.

Exact obstruction. Neither a lower Hessian bound for log f in (14), nor a matrix comparison for the Hessian in (15), was established for the actual TZ weights. Positivity and zeroth-order comparability of G and W provide no derivative sign. In higher dimension a Ricci result would still not settle holomorphic bisectional or arbitrary real sectional negativity. This final route ends with an explicit unresolved differential inequality, not a resolution.

## 7. What is and is not established

Established in this note: the normalized cusp Fourier norm formula; a sufficient holomorphic-Gram curvature criterion; the exact curvature-of-a-sum inequality with quantitative bounds; the potential fourth-derivative criterion; explicit counterexamples to three invalid general inferences; exact model curvature and distance formulas; and the scalar/determinant WP comparison identities. The Fourier norm and actual incompleteness statements concern TZ. Most other statements are general lemmas or model calculations, clearly labeled.

Not established: a negative or nonnegative curvature direction for an actual positive-dimensional finite-type TZ metric; a proof for either one-dimensional moduli space; global curvature sign of any of the four interpretations; a complete prior resolution; or novelty of the elementary partial results.

The five attempted families are stopped at their stated obstructions. No additional search turns are concealed as verification. A later audit may correct these lemmas but must not be described as a completed proof of the original problem.

## Sources and scope of inspection

[O] *Teichmüller Theory*, OWR 53/2010, DOI 10.4171/OWR/2010/53. Obitsu contribution pp. 3128–3130; question on p. 3130 inspected in text and rendered PDF. https://ems.press/content/serial-article-files/46312

[OTW] K. Obitsu, W.-K. To, L. Weng, *The asymptotic behavior of the Takhtajan–Zograf metric*, Commun. Math. Phys. 284 (2008), 227–261. Definitions §1.1 and the asymptotic statements were inspected. https://www3.math.kyushu-u.ac.jp/~weng/otw.pdf

[PTT] J. Park, L. A. Takhtajan, L.-P. Teo, *Potentials and Chern forms for Weil–Petersson and Takhtajan–Zograf metrics on moduli spaces*, Adv. Math. 305 (2017), 856–894; arXiv:1508.02102v2 (2015). Definitions and potential/Chern-form statements were inspected. Its introduction says the TZ curvature properties were unknown at that time. https://arxiv.org/abs/1508.02102

[MZ] R. Melrose, X. Zhu, *Boundary behaviour of Weil–Petersson and fiber metrics for Riemann moduli spaces*, arXiv:1606.01158v5 (2017). Introduction and §10 were inspected. Its WP curvature discussion is not a theorem of global TZ curvature negativity. We do not rely on its abbreviated tangential expansion as a verified differentiated TZ curvature estimate. https://arxiv.org/abs/1606.01158

[Teo06] L.-P. Teo, *Bers isomorphism on the universal Teichmüller curve*, arXiv:math/0607336. Theorem 5.1 and Remark 5.3 were inspected. https://arxiv.org/abs/math/0607336

[Teo24] L.-P. Teo, *Local Index Theorem for Cofinite Hyperbolic Riemann Surfaces*, arXiv:2401.12260v1 (2024). Introduction, §6 Fourier calculation, and conclusion were inspected. It computes local-index contributions and metric pairings, not a global TZ Riemann-curvature sign theorem. https://arxiv.org/abs/2401.12260

Searches through 2026-10-05 did not locate a full resolution in the inspected primary literature. This bounded negative search is not proof that none exists. Contemporary papers about Quillen/determinant curvature or hyperbolic fiber curvature must not be misclassified as solving the TZ tangent-metric question.
