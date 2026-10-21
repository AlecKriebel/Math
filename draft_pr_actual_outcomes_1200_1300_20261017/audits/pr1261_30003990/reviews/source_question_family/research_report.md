# Independent source-question family: surrogate and volume-doubling route

Prepared 2026-10-17 UTC. Author identity for this independent review: an AI research subagent. This is a mathematical derivation and finite exact-computation supplement, not human or formal verification, a full publication review, or a novelty/priority judgment.

## Independence and exact target

The only problem-specific inputs were the original Oberwolfach question, the supplied normalized hierarchy interface, and the target below. No candidate proof, audit, acceptance/result material, root analysis, other family report, or submitted artifact was read. No repository/index/ref, GitHub, tracker, Zenodo, or original/input mutation occurred. No individual or other agent was contacted. No subagent was spawned. Primary source bodies and rendered inspection images are scratch under `_local/`; all authored deliverables are at this family's root.

Let K be any fixed compact convex subset of R^n with nonempty interior, n >= 1, and let f be a fixed real polynomial. Define

    H_r = inf { integral_K f(x) q(x) dx :
                q is a global sum of squares,
                deg(q) <= 2r,
                integral_K q(x) dx = 1 }.

The target is: a finite constant C depending on K, f, n exists such that, for every integer r >= 1,

    0 <= H_r - min_K f <= C/r^2.                         (T)

**Independent result:** the derivation below proves (T), with an explicit (very nonoptimal) C. The witness uses a univariate polynomial of a convex quadratic surrogate of f at a minimizer. It makes no claim that a density depending only on f always suffices. It is an existence argument; a global minimizer is used in the witness and is not computed by this argument.

## Source question and normalization

The [Oberwolfach contribution](https://ems.press/journals/owr/articles/16633), printed pp. 2991-2993, introduces general supported reference measures, then lists Lebesgue convex-body bounds. Its closing question asks for the exact convergence regime on general convex bodies. I visually inspected printed p. 2991: displays (3) and (4) really do leave the terminal density-integral constraint incomplete; this is not merely extraction loss. Its probability-measure setup and assertion of a single affine constraint point toward unit mass, but they do not alone repair the printed formula. The closing sentence is broader wording than the precise target (T).

The [primary full hierarchy paper](https://arxiv.org/abs/1905.08142), v2, p. 2, equations (2)-(3), explicitly imposes `integral_K q dmu = 1` and defines the SOS cone at order r by degree at most 2r. I visually inspected that page. These are exactly the normalization and degree convention in (T). Scaling Lebesgue measure by any fixed positive constant leaves this hierarchy unchanged after rescaling the density.

The [2026 overview](https://ir.cwi.nl/pub/36052/36052.pdf), equations (13)-(14) and Table 1, uses the same normalization and still lists the logarithmic-square loss for unrestricted convex bodies, with a pure quadratic rate for round bodies. This gives context for the supplied target; no exhaustive priority check was attempted.

Scope assessment: (T) settles the natural Lebesgue upper-rate component of the original convex-body question. It does not establish a quadratic rate for every supported reference measure, a two-sided rate for every objective, exact asymptotic constants, or a minimizer-finding algorithm. In particular a constant objective has zero error at every order. The original brief question should not be promoted to those stronger interpretations. The cited sources discuss interval linear examples establishing quadratic worst-case order; no new lower-bound theorem is needed for (T).

## Mechanism and status

| Step | Mechanism | Evidence/status | Exact gap |
|---|---|---|---|
| Replace arbitrary f | A first-order term at a minimizer plus a positive quadratic dominates its gap | Taylor formula on segments; proved below | None for fixed polynomial f |
| Control pushforward measure | Convex homothety yields a scale-relative volume-growth bound | Direct set inclusion and Lebesgue Jacobian | None for convex full-dimensional K |
| Build endpoint concentration | An odd sine quotient is a polynomial, raised to an even power | Exact finite formula, elementary trigonometry, rational identity checks | None analytically |
| Bound normalized first moment | Dyadic shells use the volume ratio at the kernel's own scale | Explicit convergent geometric series | None analytically |
| Respect hierarchy | Compose with quadratic and normalize a single square | Exact degree allocation for every positive order | None analytically |
| Publish/priority/candidate audit | Outside this family's remit | Not performed | Requires separate review |

The key distinction from an unsupported generic pushforward argument is that sublevel-volume doubling is proved for the **surrogate**, not assumed for the original nonconvex objective. The scale-relative estimate also avoids replacing the normalizer by a standalone power bound and paying a logarithmic factor to suppress all distant mass uniformly.

## 1. Convex quadratic surrogate at an arbitrary minimizer

Choose a in K with f(a) = f_* := min_K f. Let

    L = max_{x in K} || Hess f(x) ||_op,
    M = 1 + L/2,
    ell(x) = gradient f(a) dot (x-a),
    g(x) = ell(x) + M ||x-a||^2.

Compactness and polynomial regularity make L finite. For each x in K the segment a+t(x-a) lies in K. Since t=0 minimizes f along that segment on [0,1], the right derivative gives

    ell(x) >= 0.                                      (1)

The integral Taylor formula on the same segment gives

    f(x)-f_* = ell(x) + integral_0^1 (1-u)
                  (x-a)^T Hess f(a+u(x-a)) (x-a) du
              <= ell(x) + (L/2)||x-a||^2
              <= g(x).                               (2)

Consequently

    0 <= f-f_* <= g on K;  g(a)=0;  g >= 0 on K.

The polynomial g has degree two and is convex on all of R^n. Its possible negativity outside K is immaterial. Let B = max_K g. Since K has nonempty interior and M>0, B>0. Set

    t(x) = g(x)/B,     so 0 <= t <= 1 on K.            (3)

Using M with a positive additive margin handles affine and constant objectives without a division-by-zero case. For a constant objective the target is also immediate from the uniform density.

## 2. Sublevel-volume growth from convex homothety

For u >= 0 define

    V(u) = volume_n {x in K : t(x) <= u}.

For 0 < s <= u <= 1 put lambda=s/u. If x is counted by V(u), convexity of K places a+lambda(x-a) in K. The specific quadratic gives

    t(a+lambda(x-a))
       = [lambda ell(x) + lambda^2 M||x-a||^2]/B
       <= lambda t(x) <= s.                           (4)

The map has Jacobian lambda^n, and is injective. Therefore

    V(u) <= (u/s)^n V(s).                             (5)

For u>1 the same estimate holds with V(u)=V(1), by applying (5) at u=1. Also the image a+s(K-a) is counted in V(s) for 0<s<=1, so

    V(s) >= s^n volume_n(K) > 0.                     (6)

No surface measure, tangent plane to the boundary, curvature, inner ball, local semialgebraicity, or differentiability of the boundary was used. A minimizer may lie at any vertex or nonsmooth boundary point. More abstractly this step works for every convex surrogate vanishing at a, but only the present degree-two surrogate is used in the hierarchy construction.

## 3. A single-square algebraic endpoint kernel

For every odd positive m=2s+1 define the real polynomial

    R_m(z) = (1/m) sum_{j=0}^s (-1)^j binom(m,2j+1)
                                      z^j(1-z)^(s-j). (7)

It has degree at most s and R_m(0)=1. If z=sin^2(theta), 0<=theta<=pi/2, the sine multiple-angle expansion gives

    R_m(z) = sin(m theta)/(m sin(theta)),              (8)

with the continuous value 1 at theta=0. Odd m is essential: the finite polynomial in (7) has only integer exponents. Fix the integer

    k = n+2,
    Q_m(z) = R_m(z)^(2k).                            (9)

This is globally the square of the real polynomial R_m^k. The identity

    sin(m theta)/sin(theta)
        = exp(i(m-1)theta) + exp(i(m-3)theta)
          + ... + exp(-i(m-1)theta)

and the triangle inequality give absolute value at most m. Bounding the numerator in (8) by 1 also gives, for 0<z<=1,

    0 <= Q_m(z) <= min(1,(m^2 z)^(-k)).              (10)

For delta=1/(4m^2) and 0<=z<=delta, use arcsin(v)<=pi*v/2 to get m*theta<=pi/4. The chord inequality sin(v)>=2v/pi on [0,pi/2], together with theta>=sin(theta), yields

    R_m(z) >= 2/pi > 1/2,
    Q_m(z) >= 4^(-k) on [0,delta].                  (11)

Both assertions include m=1: R_1=Q_1=1, with delta=1/4. Thus the polynomial witness need not be treated as a large-order-only construction.

## 4. Relative normalizer and a dyadic first-moment estimate

Let

    D_m = integral_K Q_m(t(x)) dx,
    N_m = integral_K t(x) Q_m(t(x)) dx.

By (6) and (11),

    0 < 4^(-k) V(delta) <= D_m < infinity.           (12)

Partition K into t<=delta and the shells

    2^j delta < t <= 2^(j+1) delta, j=0,1,2,... .

Only finitely many shells are nonempty, but extending estimates to all j is useful. On the first region, t Q_m(t)<=delta. On shell j, (10) gives

    t Q_m(t) <= 2^(j+1) delta * 4^k * 2^(-jk),

and (5), including its u>1 extension, bounds the shell volume by

    V(2^(j+1)delta) <= 2^(n(j+1)) V(delta).

Hence

    N_m <= delta V(delta) [1 + 2^(n+1+2k)
                                sum_{j>=0} 2^(-j(k-n-1))].

With k=n+2 the sum equals 2. Define

    A_n = 1 + 2^(n+2k+2) = 1 + 2^(3n+6).

Combining with (12) gives the fully explicit estimate

    N_m / D_m <= 4^k A_n / (4m^2).                  (13)

The crucial denominator is the actual V(delta) at the kernel scale. It cancels against the same quantity in each volume-growth estimate. We do not assume a fixed power asymptotic for V, and we do not need to estimate a density of its pushforward.

## 5. Global SOS, degree, every order, and final bound

For a specified integer r>=1 choose

    s_r = floor(r/(2k)),
    m_r = 2s_r+1,
    p_r(x) = R_{m_r}(t(x))^k,
    q_r(x) = p_r(x)^2 / D_{m_r}.                    (14)

The polynomial R_{m_r} has degree at most s_r in its scalar argument, and t has degree two in x. Thus

    deg p_r <= 2k s_r <= r,
    deg q_r <= 4k s_r <= 2r.                        (15)

The normalizer D is positive. Therefore q_r is a **global** square, q_r>=0 on R^n, and integral_K q_r dx=1. No assertion that an interval-nonnegative polynomial remains globally SOS after arbitrary composition is used; its explicit even power gives the square directly.

For every a>=0, 2 floor(a)+1>=a: this follows from floor(a)=0 if a<1 and from 2a-1>=a if a>=1. Applying this with a=r/(2k) gives

    m_r >= r/(2k).                                  (16)

For r<2k, m_r=1 and (14) is simply the feasible uniform density. Thus (15)-(16) cover all small positive orders without an asymptotic exception.

Now (2), (3), and (13)-(16) imply

    H_r-f_* <= integral_K (f-f_*) q_r dx
              <= B N_{m_r}/D_{m_r}
              <= B 4^k A_n/(4 m_r^2)
              <= [B k^2 4^k A_n]/r^2.              (17)

Finally, every feasible density is nonnegative on K and normalized, so its objective integral is at least f_*. Taking an infimum proves the other half of (T). For instance an admissible explicit constant is

    C = B (n+2)^2 4^(n+2) (1+2^(3n+6)),             (18)

with B and M defined in Section 1. This completes the independent analytic proof of the target.

## Supplementary exact computations

`exact_checks.py` requires only Python's standard library. Running it writes `exact_results.json`; all asserted mathematical quantities are `fractions.Fraction` rational numbers. Decimal fields are explicitly marked display-only. It checks:

1. The finite formula (7) against an independent recurrence for sin((2s+1)theta)/sin(theta), for all odd m from 1 through 65, as exact polynomial identities. Constant and endpoint values and degrees are also checked.
2. The degree budget and m>=r/(2k) for 20,000 pairs 1<=n<=40, 1<=r<=500. These are finite stress checks of formulas already proved for all orders.
3. Twenty exact endpoint first-moment examples with volume distribution V(z)=z^n, n in {1,2,3,6}, m in {1,3,5,9,17}. These include the largest allowed volume-growth exponent n, realized by a linear objective cap on an n-simplex. Every positive normalizer and moment estimate passes.
4. A nonconvex objective f(x,y)=x+y^2(1-y)^2 on the nonsmooth triangle x,y>=0, x+y<=1. Its boundary minimizers include (0,0) and (0,1). At a=(0,0), ell=x and the Hessian norm on the triangle is at most 2. Taking M=2 gives g=x+2(x^2+y^2), B=3. The code expands the witness as a literal polynomial square and integrates exactly using integral x^i y^j = i!j!/(i+j+2)!. Orders 1,7,8,15,16,24 cover the first degree transitions. Positive normalization, degree, surrogate objective domination, and the bound all pass.

Result: `ALL EXACT ASSERTIONS PASSED`. These examples could detect sign, indexing, normalization, and degree mistakes. They cannot establish the universal claim by themselves and are not described as an SDP experiment or formal verification.

## Adversarial self-check and scope limits

The assigned task forbids further delegation, so the following is a self-check, not an independently staffed adversarial review.

| Potential failure | Check |
|---|---|
| Nonconvex f invalidates volume doubling | The sublevel sets belong to convex g, and (4) is proved directly. No property of f-sublevels is assumed. |
| Boundary minimizer has nonzero gradient | Formula (1) makes its linear term nonnegative along every feasible chord; that term is retained in g. |
| Arbitrarily nonsmooth or nonalgebraic convex boundary | Only inclusion of chords and n-dimensional Lebesgue Jacobians appear. |
| Zero normalizer from a boundary-supported witness | The kernel is positive on a scaled full-dimensional copy of K, by (6),(11). |
| Very small caps or geometry-dependent log factors | The proof uses scale-relative volume ratios; V(delta) cancels. |
| Kernel is nonnegative only on an interval | Its composition is explicitly squared globally, so interval positivity is not used for SOS feasibility. |
| Half-degree loss after a quadratic composition | Equation (15) counts degree before and after composition and squaring. |
| Small r falls below a construction threshold | The m=1 witness is uniform; the same inequality covers it. |
| Flat or multiple minima | Choose any a; strict M>0 ensures B>0. No uniqueness assumption. |
| K has zero n-volume | Excluded by nonempty interior. A lower-dimensional set with ambient Lebesgue measure would make the stated normalization impossible and is outside the target. |
| Arbitrary supported reference measure | Not covered: homothetic n-volume scaling does not transfer automatically to it. |
| Degree of f grows with r | Not part of the fixed-objective statement. The witness constant contains Hessian and size data of fixed f. |
| Circular use of target hierarchy rate | None: only Taylor, convex homothety, sine identities, and a geometric series are used. |
| Hidden need for an algorithm to locate a | No such algorithm is claimed. Existence of a follows from compactness. |
| Objectivewise exact r^-2 regime | Not claimed; constants and some special objectives converge faster. |

No blocked equivalent central difficulty remains for the exact existence target (T) within this derivation. Candidate consistency, independent adversarial review of this new derivation, originality, and publication sufficiency remain outside the work performed. A later candidate comparison must retain the fact that this report was sealed first and must not rewrite this family to mimic candidate reasoning.

## Reproduction and seal

Run `python3 exact_checks.py` from this family folder before sealing. The report, exact check code, exact results, verdict, and timestamped log are enumerated with size and SHA256 in `manifest.json`. The manifest does not hash itself. Its own digest and the report/verdict digests are reported outside it in the final family return. No authored file is to be changed after that seal.
