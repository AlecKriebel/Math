# Polar-zonoid intersection bodies: finite certificates and a restricted genericity theorem

Problem 20001306 / AIM-CONVEX_GEOMETRY-0038. Author-stage research note, 3 October 2026.

**Status: partial; the full Schneider genericity problem is not solved.** The principal concrete result below is an open-dense statement in the separate space of four-dimensional bodies of revolution about a fixed axis. It is a direct consequence of Alfonseca's published flat-top theorem; a normalized analytic derivation is included. No priority claim is made for that corollary or for the elementary certificate refinement.

## 1. The actual question and conventions

AIM's *Fourier analytic methods in convex geometry*, printed page 3, Problem 10, asks whether for most origin-symmetric convex bodies K, IK is not the polar of a zonoid, with most understood in the Baire-category sense. The imported leading `0` and trailing `1` are extraction debris. The title attached to the record describes a previous partial report, not the original target.

Fix an integer n >= 3. Let X_n consist of compact convex K in R^n, with nonempty interior and K = -K, in the Hausdorff metric. Origin symmetry and full dimension put 0 in the interior. Let rho_K(u) = max{r >= 0: ru in K}. Write dS for ordinary, unnormalized spherical area and

    Rg(u) = integral_{S^(n-1) intersect u-perp} g(v) dS(v),
    Cmu(u) = integral_{S^(n-1)} |u dot v| dmu(v).

A centered zonoid is a Hausdorff limit of finite Minkowski sums of centered line segments; equivalently its support function is Cmu for a finite positive even measure mu. The body IK here is the actual intersection body of the convex input K:

    rho_IK(u) = vol_(n-1)(K intersect u-perp)
              = R(rho_K^(n-1))(u)/(n-1).

Busemann's theorem makes IK convex. For L convex with 0 in its interior, L^circ = {x: x dot y <= 1 for every y in L}. Thus

    f_K(u) = h_(IK)^circ(u) = 1/rho_IK(u)
           = (n-1)/R(rho_K^(n-1))(u).                         (1)

Denote E_n = {K in X_n: (IK)^circ is a zonoid} and B_n = X_n minus E_n. The original target is that B_n is residual in X_n, for each n >= 3. It is not the assertion that some intersection body, in the larger radial-closure class, is not a polar zonoid. The closure class allows limits of IL with arbitrary star bodies L; it does not ensure a convex preimage. That distinction prevents several tempting shortcuts.

The planar reading is false: with J a quarter-turn, rho_IK(u) = 2 rho_K(Ju), so IK = 2 J^(-1)K. Every centered planar convex body, including (IK)^circ, is a zonoid. Dimension one is not the intended problem.

## 2. Closedness, topology, and a quantitative neighborhood

The centered compact convex hyperspace, allowing degeneracy, is complete for Hausdorff distance. Full-dimensional bodies form an open subset, so X_n is Baire. The zonoid support cone

    Z = {Cmu: mu finite, positive and even}

is closed in the even continuous functions with uniform norm. Indeed, if Cmu_j converges uniformly, integrating over the sphere bounds mu_j(S^(n-1)), since integral Cmu_j dS = c_n mu_j(S^(n-1)), c_n > 0. Weak-* compactness gives a positive limiting measure and the cosine kernel identifies its transform with the uniform limit.

Here is an explicit continuity estimate. Suppose r B_2^n is contained in K and d_H(K,L) <= delta < r. Put t = delta/r and m = n-1. Support-function comparison gives

    (1-t)K subset L subset (1+t)K.

Therefore the central-section volumes satisfy the same inclusions with factors (1 +/- t)^m, and

    ||f_L - f_K||_infinity
      <= ((1-t)^(-m)-1) ||f_K||_infinity
      <= ((1-t)^(-m)-1)/(kappa_m r^m).                      (2)

Here kappa_m is the volume of the Euclidean unit ball in R^m. Consequently E_n is closed and B_n is open. In this Baire space, B_n is residual if and only if it is dense. Closedness alone proves neither density nor the conjecture.

For A invertible,

    I(AK) = |det A| A^(-T) IK,
    (I(AK))^circ = |det A|^(-1) A (IK)^circ.                (3)

Thus E_n and B_n are invariant under linear equivalence. In the Banach-Mazur compactum, use distance log inf{a >= 1: K subset TL subset aK}. If classes converge, one can choose representatives between K and (1+epsilon_j)K. This proves closedness on that compactum. Conversely, a class within Banach-Mazur distance log(1+epsilon) of [K] has a representative in the corresponding Hausdorff neighborhood of K. Hence density in X_n and density in the compactum are equivalent for this invariant property. No openness of an arbitrary nonlinear map is being assumed.

## 3. Finite rational dual certificates

The standard Hahn-Banach certificate says that f not in Z if and only if there is a finite even signed measure nu satisfying Cnu >= 0 pointwise but integral f dnu < 0. This follows from closed-cone separation, Riesz representation, and symmetry of the cosine kernel. The older partial report already contains this reduction.

A finite refinement is useful. Extend an even continuous f on the sphere homogeneously by F(0)=0 and F(x)=|x| f(x/|x|) for x nonzero.

**Proposition 1.** The following are equivalent:

(a) f is not in Z.

(b) There are finitely many nonzero q_i in Q^n and a_i in Q such that

    P(v) = sum_i a_i |q_i dot v| >= 0 for every v in R^n,
    sum_i a_i F(q_i) < 0.                                  (4)

The first inequality may be required to be strict for v != 0.

**Proof.** If f=Cmu with mu positive, the second quantity equals integral P dmu and cannot be negative. Conversely, take a signed-measure witness with integral f dnu = -eta < 0. Finite partitions of its positive and negative parts, replacing points by nearby rational vectors and weights by rational numbers, produce a finite rational functional T(F)=sum a_i F(q_i) such that T(F)<-3eta/4 and its cosine polynomial P_0 differs uniformly on the unit sphere from Cnu by less than epsilon. Uniform approximation of the kernel is valid because | |q dot v|-|u dot v| | <= |q-u| uniformly in v; approximation of F uses its uniform continuity on a compact annulus. Weight approximation is also uniform because the finitely many kernels are bounded.

Choose a small positive rational d with d sum_j |f(e_j)| < eta/4, and make the approximation fine enough that epsilon < d. Add the functional d sum_j F(e_j). Its cosine polynomial is d sum_j |v_j|, at least d on the Euclidean unit sphere. The amended polynomial is strictly positive there, while the amended evaluation stays below -eta/2. Homogeneity proves the result. If f(e_j)=0 for all j, the same choice is unrestricted. Pairing atoms at +/- q_i/|q_i| gives the even sphere-measure interpretation. QED.

This is a finite existence theorem, not an effective bound on the number or size of coefficients and not a density proof. Once rational data in (4) are supplied, P >= 0 has a finite exact polyhedral check: on each cone defined by choices of signs of q_i dot v, P is linear. Intersect that cone with [-1,1]^n and test the finitely many rational vertices. The union of these pieces covers the box, and homogeneity covers R^n. Evaluating F(q_i) for a general body still requires certified section-volume data; floating-point sampling is insufficient.

If (4) holds for f=f_K with value -eta, put M=sum |a_i| |q_i|. Equation (2) shows it holds for every L with

    M ((1-delta/r)^(-(n-1))-1)/(kappa_(n-1) r^(n-1)) < eta. (5)

This certifies an explicit neighborhood rather than merely a point example.

## 4. An exact cube witness and its limitation

For every x in R^n,

    sum_{epsilon in {+1,-1}^n} |epsilon dot x|
       >= gamma_n sum_j |x_j|,
    gamma_n = 2 binom(n-1, floor((n-1)/2)).                  (6)

To prove this, use coordinate sign symmetry and homogeneity to reduce to x_j >= 0, sum x_j=1. The left side is a convex symmetric function on that simplex. Averaging its argument over coordinate permutations shows its minimum is attained at (1/n,...,1/n). Its value there is gamma_n, by the elementary binomial identity sum_j binom(n,j)|n-2j| = n gamma_n. This is Schneider's published obstruction, written as a finite certificate.

Let Q_n=[-1,1]^n. Then F_Qn(e_j)=2^(-(n-1)), and the diagonal section formula gives

    F_Qn(epsilon) = (n-1)! / D_n,
    D_n = sum_{j=0}^{floor(n/2)} (-1)^j binom(n,j)(n-2j)^(n-1).

For completeness the section formula follows from the density at zero of a sum of n independent uniforms on [-1,1], obtained by inclusion-exclusion for a sliced cube, together with the coarea factor sqrt(n).

The certificate evaluation is the rational number

    W_n = 2^n (n-1)!/D_n - gamma_n n/2^(n-1).              (7)

In dimension three W_3 = -1/3, so (IQ_3)^circ is not a zonoid. No numerical inference is needed. The exact verifier also finds W_n<0 for 5 <= n <= 64. This is a finite list, not a proof for every dimension. The n=4 value is exactly zero, so this witness does not decide the four-dimensional cube. Equation (5) supplies neighborhoods in every verified strict case. Schneider had already proved the cube obstruction in dimension three and all sufficiently large dimensions; these calculations are checks and explicit certificates, not a claim of a new cube theorem.

## 5. The harmonic perturbation route

The nonpositive-sign spherical Laplacian Delta has eigenvalue -l(l+n-2) on degree-l harmonics. With the unnormalized transforms used here, the distribution identity is

    (Delta+n-1) C = 2 R.                                  (8)

Indeed, for fixed v, away from u dot v=0 the function |u dot v| satisfies (Delta+n-1)|u dot v|=0. Across that equator its normal derivative has jump 2, giving exactly 2 times equatorial area measure. Integration against a smooth density proves (8), and duality extends it to distributions. On even harmonics the R multipliers are nonzero and have polynomially bounded inverses; the same holds for C. Thus the inverses make sense on even smooth functions and distributions. In particular

    C^(-1) R = (Delta+n-1)/2.                              (9)

Put m=n-1, A=|S^(n-2)| and rho_(K_s)^m=1+s q, for a fixed smooth even q and sufficiently small s. These radial functions define convex bodies for sufficiently small s, because their gauge functions converge in C^2 to that of the ball. Writing mu_s=C^(-1)f_(K_s), differentiation yields

    mu_0 = m^2/(2A^2),
    mu'_0 = -m (Delta+m)q/(2A^2).                          (10)

For a degree-l harmonic q,

    mu'_0/mu_0 = [l(l+n-2)-m] q/m.                        (11)

This calculates the exact first variation; it does not justify letting l increase while discarding nonlinear remainders. For any *fixed* q the generating density remains positive for sufficiently small s, by continuity of C^(-1) between sufficiently high differentiability norms. Hence an arbitrarily small fixed-frequency smooth perturbation cannot force the desired obstruction. Schneider already used this mechanism to produce nonellipsoidal exceptional bodies near the ball.

The convexity constraint also changes at the same derivative scale. If p_s=1/rho_(K_s), the tangential Hessian of its homogeneous extension is

    Hess_S(p_s)+p_s Id
      = Id - (s/m)(Hess_S(q)+q Id) + O_q(s^2).             (12)

Thus the frequency factor in (11) cannot be used independently of convexity or of a uniform nonlinear error estimate. Around general K, the first derivative instead contains

    -m C^(-1)[R(q)/R(rho_K^m)^2],

whose variable multiplier prevents cancellation (9). No uniform convexity-preserving, sign-changing perturbation near every exceptional K has been established here. This route remains blocked at precisely that global step.

## 6. Four-dimensional revolution bodies: a genuine relative genericity theorem

Fix the axis e_4. Let Y_4 be the closed relative subspace of X_4 of bodies invariant under all orthogonal transformations fixing e_4. It is Baire: include degenerate invariant bodies to obtain a complete space and then take its open full-dimensional part.

**Theorem 2.** B_4 intersect Y_4 is open and dense in Y_4. More concretely, if K belongs to Y_4 and 0<b<h=rho_K(e_4), then

    K_b = K intersect {x: |x_4| <= b}

belongs to B_4 intersect Y_4.

**Proof using the published flat-top criterion.** Near t=1, with t=u_4, the radial function of K_b is rho(t)=b/t. It is smooth there and rho(1)+rho'(1)=0. Alfonseca's Corollary 2 (2013) therefore gives (IK_b)^circ non-zonoid. The sandwich (b/h)K subset K_b subset K proves Hausdorff convergence K_b -> K as b increases to h. Openness follows from Section 2. QED.

Here the support height equals h because averaging the orbit of any (x',x_4) in K puts (0,x_4) in K. The exact near-pole radial formula follows from rho_K(1)>b and continuity. No smoothness of K away from the cap and no strict convexity assumption is needed.

### Normalized analytic verification of the strict sign

This reproduces the relevant Alfonseca mechanism without dropping positive constants. Let rho(t) be the even zonal radial function of a body L in Y_4, and H(x)=integral_0^x rho(t)^3 dt. If s=u_4 and x=sqrt(1-s^2), elementary integration on the equatorial S^2 gives

    rho_IL(s) = (4pi/3) H(x)/x,
    f_L(s) = (3/(4pi)) x/H(x).

For an even zonal function g on S^3,

    Rg(s) = (4pi/x) integral_0^x g(t) dt.

Its inverse, in distributions if necessary, is consequently

    R^(-1)f_L(t) = (3/(16pi^2)) G(t),
    G(t) = d/dt [t^2/H(t)].

By (8), the even generating distribution for f_L is

    mu_L(t) = (3/(32pi^2))
              [(1-t^2)G''(t)-3tG'(t)+3G(t)].             (13)

The inverse is unique: on even degree 2k spherical harmonics in S^3, R has eigenvalue 4pi(-1)^k/(2k+1). This also justifies the distributional use when the input is not globally smooth.

If rho(t)=b/t near 1, then H'(1)=b^3 and H''(1)=-3b^3. Direct differentiation gives

    G'(1)-G(1)
      = [-3H(1)H'(1)-H(1)H''(1)+2H'(1)^2]/H(1)^3
      = 2b^6/H(1)^3.

Therefore the locally smooth generating distribution has value

    mu_L(1) = -9b^6/[16pi^2 H(1)^3] < 0.                 (14)

It is negative on a nonempty open cap, so it cannot be a positive measure. Uniqueness of the even generating distribution rules out any different positive representing measure. This is a strict analytic certificate, not an inference from a plot. Pairing (13) with a nonnegative smooth test function supported in that cap and using C^(-1) gives a signed-measure witness as in Section 3; Proposition 1 further guarantees finite rational witnesses.

Theorem 2 is a separately specified restricted result. Y_4 is a proper symmetry-constrained class, and density in it does not imply density in X_4. The theorem neither proves the original conjecture even in unrestricted dimension four nor changes the all-n target.

## 7. Why the same cap proof does not settle dimension six

Alfonseca's six-dimensional flat-top sufficient condition has an additional moment requirement. With r(t)=rho(t)^5, h=integral_0^1 r(t)(1-t^2)dt and k=integral_0^1 t^2 r(t)dt, it requires

    h r(1) > 2 k^2.                                      (15)

Flattening only a cap of vanishing height changes these quantities continuously and cannot force a strict inequality when the limiting body has the reverse strict inequality. For the cylinder B_2^5 times [-1,1], rho(t)=(1-t^2)^(-1/2) below 1/sqrt(2) and rho(t)=1/t above it. Exact elementary integration yields

    r(1)=1, h=5/4, k=5/6,
    h r(1)-2k^2 = -5/36 < 0.                             (16)

For h, the lower integral is [t/sqrt(1-t^2)]_0^(1/sqrt(2))=1 and the upper integral of t^(-5)-t^(-3) is 1/4. For k, the lower integral is 1/3 and the upper one is 1/2. This directly checks the condition without relying on decimal quadrature. A printed cylinder h-value in the arXiv v1 example does not agree with its displayed defining integrals; the only conclusion needed here, failure of (15), is unchanged. We do not use that printed value.

Failure of a sufficient test does not prove the cylinder's intersection body is a polar zonoid; Alfonseca obtains its non-polar-zonoidality by a different, full inverse-transform calculation. It also does not disprove the possibility of another perturbation near the cylinder. It identifies the exact failure of extending the simple cap criterion to all revolution bodies in dimension six.

## 8. Final scope

Five materially different proof approaches have been completed as a bounded attempt: topology with quantitative stability, finite rational dual separation, finite cube witnesses, harmonic linearization, and cap surgery with inverse-transform analysis. They give checkable partial results and an exact restricted genericity theorem. The missing assertion remains:

    for every n >= 3, every K in E_n and every epsilon > 0,
    some L in B_n satisfies d_H(K,L)<epsilon.

No proof or counterexample to that assertion is claimed. The public package contains authored notes and exact-check code only. Sources and complete downloaded texts are not part of it.

## References

- AIM, *Fourier analytic methods in convex geometry*, Problem 10, printed p. 3: https://aimath.org/WWN/fourierconvex/fourierconvex.pdf
- R. Schneider, *On the Busemann Area in Minkowski Spaces*, Beitr. Algebra Geom. 42 (2001), 263–273. Conjecture and Theorems 1–2 on p. 264; closedness p. 266; cube witness pp. 270–272: https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.1/b42h1rsc.pdf
- M. A. Alfonseca, *Intersection bodies that are not polar zonoids: a flat top condition in dimensions four and six*, J. Math. Anal. Appl. 404 (2013), 326–337. Proposition 1 and Corollary 2, and Proposition 4/Corollary 5: https://arxiv.org/abs/1303.3813 ; https://doi.org/10.1016/j.jmaa.2013.03.032
- R. Schneider, *Crofton measures in projective Finsler spaces* (2005), Section 5 and its genericity conjecture: https://home.mathematik.uni-freiburg.de/rschnei/Wuhan.pdf
- D. Ryabogin and A. Zvavitch, *Zonoids whose polars are zonoids: the Banach–Mazur distance need not tend to one*, September 2026 preprint, especially Section 7.1: https://arxiv.org/abs/2609.10852 . This settles a different AIM asymptotic question; its broader intersection-body observation does not settle the present convex-preimage genericity question.
