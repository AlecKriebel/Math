# Independent adversarial verification of the sealed derivation and sharpness proposal

Prepared 2026-10-17 UTC by an AI research subagent. This is an independently staffed mathematical review and exact-computation supplement. It is not human verification, formal proof-assistant verification, a novelty assessment, or a publication/workflow assessment.

**Verdicts: PASS for the complete upper derivation; PASS for the separate optional known lower-bound clarification. No actionable mathematical concern was found.** The integer polynomial index and imaginary unit in the lower proposal must be read as distinct symbols, as its own prose already specifies. The unambiguous formula appears below; that acknowledged notation collision does not invalidate the mathematics or require changing the frozen input.

## Independence, authentication, and exact question

Only the nine files enumerated by `INPUT_FREEZE.json`, the explicit task, and the primary/authoritative sources identified in `source_inventory.json` were used. The submitted candidate, root analysis, and other reviews were not read. No individual or other agent was contacted; no further agent was spawned. No original/input file, Git index/ref/branch, actual PR, external tracker, GWS object, or Zenodo record was mutated.

The supplied anchor SHA256 is

    cbdb81ab64d954e664788f82d378a9853903586c70ed6ad40dabd4bd8e01cee9

It and all nine file sizes/digests were authenticated before substantive review. `start_authentication.json` records the result. All seven entries of the source family's manifest were separately checked against their literal paths and bytes. The final authentication is recorded in `end_authentication.json`; this review is sealed only after that check. No frozen input was repaired.

The upper hypothesis tested is exactly this: for each fixed integer n>=1, fixed compact convex K in R^n with nonempty interior, and fixed real polynomial f, define

    H_r = inf { integral_K f q dx : q is a global real SOS,
                deg q <= 2r, integral_K q dx = 1 }.

Then there is a finite C=C(K,f,n) such that, for every integer r>=1,

    0 <= H_r-min_K f <= C/r^2.                         (U)

This is an existence statement for the full normalized ambient-Lebesgue hierarchy. It does not require q=s(f), arbitrary reference measures, a minimizer algorithm, or positive objectivewise Theta behavior. The feasible set is nonempty at every r because the constant density 1/volume(K) is a global square. All relevant integrals are finite by compactness.

If the reference Lebesgue measure itself is normalized to dx/volume(K), multiplying a density for dx by volume(K) preserves its global SOS degree, normalization, and objective value. Thus the hierarchy and conclusions are unchanged under that convention.

The lower proposal is a distinct statement for fixed examples: K=[0,1], f(t)=t, and, for each fixed n>1, K=[0,1] x [-1,1]^(n-1), f(t,y)=t. It proposes the known coarse lower bound H_r>=1/[4(r+1)^2]. This is an explanatory sharpness example, not a new lower-rate discovery.

## Upper proof: reconstruction and attempts to break each link

### 1. The surrogate really works for nonconvex objectives and boundary minima

Compactness gives a minimizer a. Let L=max_K ||Hess f||op, M=1+L/2, ell(x)=grad f(a).(x-a), and g(x)=ell(x)+M||x-a||^2. All are well defined and L is finite. For fixed x in K, the one-sided derivative at zero of h(u)=f(a+u(x-a)) is nonnegative: h(u)>=h(0) on [0,1]. Thus ell(x)>=0. No unconstrained stationarity assertion grad f(a)=0 is made.

Twice integrating h'' on the feasible segment yields

    f(x)-f(a) = ell(x) + integral_0^1 (1-u)
                   (x-a)^T Hess f(a+u(x-a)) (x-a) du
              <= ell(x)+(L/2)||x-a||^2 <= g(x).

Therefore 0<=f-f(a)<=g on K. A polynomial's Hessian need not be positive semidefinite; the operator-norm upper bound suffices. g is a globally strictly convex quadratic and g(a)=0, although it need not be globally nonnegative. Only its nonnegativity on K is needed before the explicit global squaring step.

Let B=max_K g. Since g(x)>=M||x-a||^2 on K and K contains a point distinct from a, B>0. Hence t=g/B is a degree-two real polynomial with 0<=t<=1 on K. Affine and constant f cause no degeneracy because M>=1. Multiple or flat minimizers cause no change: choose any a. This entire step works at vertices and boundaries having no tangent plane. The argument never differentiates the boundary of K.

The constant may be expressed without an implicit choice of a if desired: with D=diam(K) and G=max_K ||grad f||, B<=GD+MD^2. Consequently the displayed constant below is genuinely allowed to depend only on K,f,n. This is a quantifier clarification, not a repair to the family's valid choice-dependent construction for a fixed instance.

**Negative control:** replacing g by the original nonconvex f would be invalid. On [0,1], f(x)=x(1-x)^2 has a=0 as a minimizer and f(1)=0, while f(1/2)=1/8>f(1)/2. Thus the radial inequality needed for the next step fails for f. The reviewed proof explicitly uses g and avoids this failure.

### 2. Relative volume growth has the right direction and includes saturated endpoints

Write V(u)=volume{x in K:t(x)<=u}. For 0<s<=u<=1 let lambda=s/u. For every x counted in V(u), the injective homothety T(x)=a+lambda(x-a) lies in K, and

    t(T(x)) = [lambda ell(x)+lambda^2 M||x-a||^2]/B
             <= lambda t(x) <= s.

Its determinant is lambda^n, so lambda^n V(u)<=V(s). Equivalently

    V(u) <= (u/s)^n V(s).                            (V)

The direction is essential: the inner volume controls the outer volume after a polynomial scale factor. Taking u=1 shows V(s)>=s^n volume(K)>0. If u>1 and 0<s<=1, V(u)=V(1)<=s^(-n)V(s)<=(u/s)^nV(s). If s>=1 as well, both volumes equal volume(K), so the same inequality is also true. Thus the shell endpoint above one is harmless. There is no assumption that V has a density, a power asymptotic, or a regular boundary.

The minimum may be on an arbitrarily thin-looking convex tip: the homothetic copy still has positive ambient volume at every positive scale. Full dimensionality is used exactly here and in feasibility. A lower-dimensional set with ambient Lebesgue measure zero is excluded by (U).

### 3. Odd sine-quotient polynomial, uniform envelope, and the core floor

For m=2s+1 with integer s>=0 define

    R_m(z) = (1/m) sum_{j=0}^s (-1)^j binom(m,2j+1)
                                 z^j(1-z)^(s-j).

The sine multiple-angle expansion, divided by m sin(theta), gives R_m(sin^2 theta)=sin(m theta)/(m sin theta). Indeed the cosine exponent in each term is m-2j-1=2(s-j), making it a polynomial in z. R_m has degree s, value 1 at zero, and R_m(1)=(-1)^s/m. The identity includes zero by continuity and theta=pi/2 literally. No hidden square-root factor remains. Oddness of m is a substantive part of this algebra.

The exact geometric sum

    sin(m theta)/sin(theta)
      = sum_{h=0}^{m-1} exp(iota (m-1-2h)theta)

has m terms of modulus one whenever the quotient is defined, and the removable endpoints follow by continuity. Therefore its absolute value is <=m. Also |sin(m theta)|<=1. For k=n+2 and Q_m=R_m^(2k),

    0<=Q_m(z)<=min(1,(m^2 z)^(-k)),  0<z<=1.         (K)

Set delta=1/(4m^2). If 0<=z<=delta and theta=arcsin sqrt(z), then theta<=pi sqrt(z)/2, hence m theta<=pi/4. The chord inequality sin(v)>=2v/pi on [0,pi/2] and theta>=sin(theta) give R_m(z)>=2/pi>1/2 (with z=0 direct). Thus

    Q_m(z)>=4^(-k),  0<=z<=delta.                    (C)

Every statement covers m=1: R_1=Q_1=1 and delta=1/4. There is no large-m cutoff. The bound in (K) is used only on [0,1], while global SOS feasibility will follow from the literal square, not from an inference about interval nonnegativity.

### 4. Normalizer and shell constants were independently recomputed

Let D_m=integral_K Q_m(t)dx and N_m=integral_K t Q_m(t)dx. From (C), (V), and compactness,

    0<4^(-k)V(delta)<=D_m<=volume(K)<infinity.

On t<=delta, tQ_m(t)<=delta, contributing at most delta V(delta). On the disjoint shell 2^j delta<t<=2^(j+1)delta, j>=0, (K) gives

    tQ_m(t)<=2^(j+1)delta * 4^k 2^(-jk).

By (V), even when the upper shell endpoint exceeds one, its volume is at most 2^(n(j+1))V(delta). Multiplying these two bounds and summing gives

    N_m <= delta V(delta)
          [1+2^(n+1+2k) sum_{j>=0} 2^(-j(k-n-1))].

For k=n+2 the geometric ratio is 1/2 and the sum is 2. Thus the bracket equals

    A_n=1+2^(n+2k+2)=1+2^(3n+6).

It follows that N_m/D_m<=4^k A_n/(4m^2), exactly the family's stated bound. All shell boundaries are covered: the core contains delta and every shell is open at its lower endpoint and closed at its upper endpoint. At most finitely many shells meet [0,1]; extending their nonnegative upper bounds to an infinite geometric sum is valid.

The pivotal cancellation is of V(delta) itself, rather than a standalone lower estimate delta^n volume(K). This is a proved local-to-larger-volume comparison. It does not assume the endpoint concentration theorem it seeks to establish. There is no unsupported theorem equivalent to (U) hidden in this step.

**Negative control on the proof envelope:** choosing k=n+1 would make this infinite majorizing series have ratio one. The reviewed proof uses k=n+2 and therefore avoids that divergence. This control does not assert that all kernels at the smaller exponent necessarily fail; it detects invalid reuse of this particular summation argument.

### 5. The global square and degree budget cover every positive order

For an integer r>=1 put s=floor(r/(2k)), m=2s+1, and p=R_m(t)^k. Since deg t=2 and deg R_m<=s,

    deg p<=2ks<=r;  deg p^2<=4ks<=2r.

Define q=p^2/D_m=(p/sqrt(D_m))^2. This is a real global square, even though g may be negative outside K. Its integral on K is exactly one. No cancellation, truncated positivity certificate, local SOS, or restricted s(f) property is needed.

For a=r/(2k)>=0, 2floor(a)+1>=a: it is immediate for a<1, and for a>=1 it follows from floor(a)>=a-1 and 2a-1>=a. Hence m>=r/(2k) for every positive integer r. When r<2k, s=0,m=1 and q is the uniform density, still satisfying all the same estimates.

Consequently

    H_r-f(a) <= integral_K (f-f(a))q dx
              <= B N_m/D_m
              <= B 4^k A_n/(4m^2)
              <= B k^2 4^k A_n/r^2.

Every feasible q is nonnegative on K and has mass one, so H_r>=f(a). Thus (U) holds with

    C=B(n+2)^2 4^(n+2)(1+2^(3n+6)).

The estimate is coarse but finite and independent of r. Its construction uses a minimizer existentially and imposes no algorithmic claim. Degree f is fixed; all its derivative and size information is absorbed into C. Constant f has exactly zero gap, rather than a positive two-sided rate.

## Separate lower proposal: self-contained verification

### 1. SOS degree reduction is legitimate in every dimension

If q=sum_j p_j^2 has degree <=2r, every nonzero summand may be taken to have degree <=r. In fact any finite real SOS representation already has this property: if d=max_j deg p_j, the top homogeneous part of q is sum_j (p_{j,d})^2. It cannot be identically zero unless every p_{j,d} is zero, since it is a sum of real squares at every real point. Thus deg q=2d, proving d<=r. This also applies before fixing a fiber in the product example.

### 2. Rodrigues, norm, and the literal integral formula

Use the integer index j>=0 and write iota for the imaginary unit, iota^2=-1. Rodrigues' definition is

    P_j(x)=(2^j j!)^(-1) d^j/dx^j (x^2-1)^j.

The polynomial (x^2-1)^j has a zero of multiplicity j at each endpoint. Integrating by parts j times against a polynomial of degree <j therefore has no boundary terms and gives zero. This proves orthogonality to every lower degree polynomial. The leading coefficient of P_j is c_j=(2j)!/[2^j(j!)^2]. Integrating against x^j instead gives

    integral_-1^1 x^j P_j(x)dx
      = 2^(-j) integral_-1^1 (1-x^2)^j dx.

The last integral I_j obeys I_0=2 and I_j=(2j)/(2j+1) I_{j-1}, by elementary integration by parts. Thus I_j=2^(2j+1)(j!)^2/(2j+1)!, and orthogonality of P_j-c_j x^j to P_j yields

    integral_-1^1 P_j(x)^2 dx = c_j 2^(-j) I_j=2/(2j+1).

The unambiguous Laplace identity needed for the bound is

    P_j(x)=(1/pi) integral_0^pi
                 (x+iota sqrt(1-x^2) cos(theta))^j dtheta,
    j a nonnegative integer, -1<=x<=1.              (L)

This is [NIST DLMF 18.10.5](https://dlmf.nist.gov/18.10.E5) after x=cos(theta). A branch extension is unnecessary: sqrt(1-x^2) is the nonnegative real square root and the exponent is an integer. The endpoint cases x=+-1 are literal; j=0 means the constant integrand one.

For an independent algebraic verification, expand the finite power. Odd cosine moments vanish, and the mean of cos^(2h) is binom(2h,h)/4^h. Its right side is the real polynomial

    L_j(x)=sum_{h=0}^{floor(j/2)} binom(j,2h)
            binom(2h,h) x^(j-2h)(x^2-1)^h/4^h.

As formal power series its generating function is

    sum_{j>=0} L_j(x) z^j
     = (1-xz)^(-1) sum_{h>=0} binom(2h,h)/4^h
                       [z^2(x^2-1)/(1-xz)^2]^h
     = (1-2xz+z^2)^(-1/2).

The middle equality follows by the binomial series, coefficient by coefficient, so no convergence interchange is needed. Differentiating the final series shows

    (j+1)L_{j+1}=(2j+1)xL_j-jL_{j-1}, L_0=1,L_1=x.

The explicit coefficient formula obtained directly from Rodrigues,

    P_j(x)=2^(-j) sum_{h=0}^{floor(j/2)}
       (-1)^h (2j-2h)!/[h!(j-h)!(j-2h)!] x^(j-2h),

satisfies the same recurrence by substitution. Induction proves L_j=P_j for every integer j. This establishes (L) independently of citation. The exact suite separately compares its finite expansion with Rodrigues through j=24.

For each integrand base in (L),

    |x+iota sqrt(1-x^2) cos(theta)|^2
       =x^2+(1-x^2)cos^2(theta)<=1.

The triangle inequality thus gives |P_j(x)|<=1 on [-1,1], including both endpoints. This addresses the intended formula in the proposal; interpreting both occurrences of its typographic `i` as the integer index would be an incorrect reading already explicitly disallowed by its following sentence.

### 3. Cauchy-Schwarz gives the exact cap used in the proposal

On [0,1], ell_j(t)=sqrt(2j+1)P_j(2t-1), j=0,...,r, is an orthonormal basis for polynomials of degree <=r: the substitution x=2t-1 contributes the required factor 1/2. If p=sum_j a_j ell_j, then

    |p(t)|^2 <= (sum_j a_j^2)(sum_j ell_j(t)^2)
              <= (integral_0^1 p(s)^2 ds) sum_{j=0}^r(2j+1)
              = (r+1)^2 integral_0^1 p(s)^2 ds.

Summing over the SOS summands of a normalized q proves 0<=q(t)<=M=(r+1)^2. This is the unnormalized Lebesgue convention in the question. There is no missing interval length or square-root factor.

The pointwise cap itself cannot be reduced from (r+1)^2 to r+1 by this argument. The endpoint reproducing polynomial p_r(t)=sum_{j=0}^r(2j+1)(-1)^jP_j(2t-1) has p_r(0)=(r+1)^2 and squared norm (r+1)^2, so its normalized square attains q(0)=(r+1)^2. This provides an independent targeted negative control on a common normalization error.

### 4. The tail estimate, product extension, and worst-case quantifiers are valid

Set alpha=1/(2M), which lies in [0,1]. Then integral_0^alpha q<=M alpha=1/2. Absolute continuity eliminates endpoint-mass ambiguities, so integral_alpha^1 q>=1/2. Thus

    integral_0^1 t q(t)dt >= alpha integral_alpha^1 q(t)dt
                           >=1/(4M).

This holds for every feasible density and therefore for their infimum. It holds at r=0 too, although the target needs r>=1 only. The aside about the stronger coarse constant is also true: layer cake gives E[t]=integral_0^1 Pr(t>s)ds>=integral_0^(1/M)(1-Ms)ds=1/(2M). It is optional and not needed for the stated 1/4 bound.

For a fixed n>1 and a global SOS on [0,1]xY, Y=[-1,1]^(n-1), apply the univariate inequality to p_j(.,y) for each y. Its degree in t is at most its total degree, hence <=r. Sum and integrate in y to obtain for the marginal m(t)=integral_Y q(t,y)dy,

    0<=m(t)<=M integral_Y integral_0^1 q(s,y)ds dy=M,
    integral_0^1 m(t)dt=1.

The same tail proof gives integral t q>=1/[4(r+1)^2]. The fiber volume 2^(n-1) does not create an extra factor, because the integrated squared norms sum to the single global mass one. All integrations involve continuous polynomials on compact rectangles, so Fubini is legitimate. No assertion that a marginal must itself have an SOS representation is used or needed.

For every fixed n, these examples satisfy H_r>=1/(16r^2) for r>=1, while (U) supplies H_r<=C/r^2 on that same fixed instance. They therefore have Theta(r^-2) error, and no proposed o(r^-2) rate sequence can bound all fixed instances even with constants depending on the instance. This excludes a better universal exponent; it does not assert that every body/objective has a positive Theta rate. For f constant the gap is identically zero. No bound uniform over arbitrarily rescaled f is claimed.

The known nature of this example should be credited to [de Klerk and Laurent, *Worst-case examples for Lasserre's measure-based hierarchy for polynomial optimization on the hypercube*, arXiv:1804.05524v1, Section 3.1](https://arxiv.org/html/1804.05524). I inspected Theorem 3.1 and Corollaries 3.2-3.3: they treat the full SOS hierarchy, linear interval objectives, Jacobi weights including Lebesgue, and product lower examples. The published paper is *Mathematics of Operations Research* 45(1), 86-98 (2020), [DOI 10.1287/moor.2018.0983](https://doi.org/10.1287/moor.2018.0983). This attribution is for the known sharpness regime, not an assertion that the exact elementary 1/4 constant is printed there. No firstness or present-openness claim was assessed.

## Reproducible computation and falsification evidence

`replay_source_checks.py` authenticates the original source-family script, copies it under ignored `_local/`, removes PYTHONOPTIMIZE from the child environment, and runs the normal interpreter without `-O`. Its output is stored at this review root. The replay returned code zero, and `replay_results.json` is byte-identical to the frozen source-family result, SHA256 `fac59a6e7983ebecd7d2eec30949748a2750777adb3c50282efb7cbd8852c15c`. The original script's digest was unchanged. This replay confirms the actual assertions in that finite program ran; no optimized-interpreter assertion claim is made.

The separate `independent_checks.py` does not import source-family code. It uses exact rational arithmetic throughout and explicit checks. `independent_results.json` records:

- 51 odd-kernel polynomial identities, m=1,...,101, comparing a Chebyshev cosine-sum construction with the declared finite binomial formula; 124 exact Pythagorean-angle quotient checks; 1035 rational core/envelope checks including m=1.
- 120000 integer degree/order budgets, 1<=n<=60 and 1<=r<=2000; dyadic constants for 60 dimensions; 184 exact relative-volume checks, including upper endpoints above one.
- 11 exactly integrated global-square witnesses for nonconvex f=x(1-x)^2 on [0,1] with two boundary minima, and f=(x^2-1/4)^4 on [-1,1] with two quartic-flat interior minima. For the latter, ||f''||<=243/8, M=259/16, B=2331/64, and t=(2x-1)^2/9. They exercise small orders and degree transitions, normalization, surrogate domination, and the final bound.
- Rodrigues versus Laplace identities for all j=0,...,24; all 625 pairwise Legendre inner products over [-1,1]; 13 exactly cap-saturating endpoint examples for r=0,...,12.
- Exact positive LDL pivots of the Hilbert moment matrices (1/(i+j+2)-c/(i+j+1))_(i,j=0)^r with c=1/[4(r+1)^2], r=0,...,12. Each finite matrix check directly verifies the claimed lower moment inequality for every polynomial of that finite degree, independently of the Legendre argument.
- A mixed two-variable global SOS and its exactly integrated fiber marginal, checked against the degree-two lower bound and cap.
- Six negative controls, all detected: using raw nonconvex f for homothety; treating interval nonnegativity as global SOS; using r+1 in place of (r+1)^2; forgetting the quadratic-composition degree factor; using the divergent k=n+1 infinite envelope; and asserting positive objectivewise Theta behavior for constants.

These computations could expose algebra, normalization, endpoint, degree, and quantifier mistakes, but the universal proof is the analytic chain reconstructed above. Neither finite testing nor the source family's own verdict was used as a substitute for that proof. No code from the authors of the cited research papers was obtained or claimed to have been run.

Reproduce from this review folder with the normal commands `python3 replay_source_checks.py` and `python3 independent_checks.py`, before resealing any changed outputs. The replay touches only scratch and this review's outputs, never the source family.

## Final mathematical disposition and exact remaining gap

| Component | Strongest verified result | Status | Exact mathematical gap |
|---|---|---|---|
| Sealed source-question-only upper derivation | Full (U), explicit finite C, every r>=1, arbitrary fixed polynomial and full-dimensional compact convex K, including nonsmooth boundary minima | PASS | None identified |
| Optional separate lower clarification | H_r>=1/[4(r+1)^2] on one fixed Lebesgue/linear product instance in every fixed dimension; consequently worst-case exponent two is sharp | PASS | None identified; retain known-result attribution and use j/iota in final typesetting as already intended |
| Original submitted candidate | Not inspected | Outside scope | No verdict on its consistency or correctness |
| Priority, novelty, publication readiness, arbitrary reference measures, restricted s(f) densities, minimizer algorithms, objectivewise positive Theta | Not established or claimed here | Outside scope | Separate questions, not gaps in (U) |

No new equivalent unsupported assertion is being promoted to proof. The upper chain reduces to Taylor's formula, feasible chords, Lebesgue scaling, exact finite trigonometric identities, and a convergent geometric series. The lower chain has a complete elementary derivation of the needed Legendre facts and a normalized tail estimate. Final completion estimate for this bounded adversarial review: 100%; this percentage does not estimate completion of any broader research or publication program.

All authored files are frozen by `manifest.json`, with path, byte count, and SHA256. Its own digest and this report/verdict digests are supplied outside the manifest in the final review return. Ignored `_local/` contains the authenticated source-code copy and optional scratch only, excluded from authored deliverables. The input anchor is an existing read-only input and is authenticated rather than treated as authored output.
