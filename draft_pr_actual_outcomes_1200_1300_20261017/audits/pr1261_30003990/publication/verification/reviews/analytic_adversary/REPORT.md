# Independent analytic adversarial audit of PR 1261 / problem 30003990

Audit date: 2026-10-17 UTC. Verdict: **PASS for the exact scoped mathematical theorem and the square-pyramid supplement.** No actionable mathematical defect or required proof repair was found. Completion estimate: 100% of this assigned mathematical review. This is neither a formal proof assistant certificate nor novelty, current-openness, priority, or publication clearance.

## Inputs and review discipline

The input is the immutable seven-file submission recorded in `../../SUBMITTED_SNAPSHOT.json`, original head `d1ecd7c4368f4909653a44db0c9ca4a5463e6552`. I read all of `PROOF.md`, `MOMENT_FORMULATION.md`, `AUDIT.md`, `RESULT.md`, `SOURCE_VERIFICATION.json`, `ACCEPTANCE.json`, and `PUBLIC_MANIFEST.json`. The original proof is 8,867 bytes, SHA256 `a49d5c37e132810d22219271cd225f9519618b1eb8ae8b63ce424e5eaa00a03a`. The supplement is 3,099 bytes, SHA256 `b1988e13ab99ba0614d0695c67448bbf6538267ed75c271c5be48eb7c8f3cc37`. The independent checker verifies the size and digest of every submitted file against the snapshot.

Prior acceptance and historical execution claims were treated as claims to test, not premises. No old checker bodies were supplied among those seven files; none was inferred or silently replayed. The present exact checker is newly authored and was actually executed. No originals, other reviews, root records, Git state, PRs, trackers, releases or Zenodo records were changed. No individuals or other agents were contacted. All authored outputs are at this review folder's root; source copies and mechanically derived renderings are in ignored `_local/`.

## Exact strongest verified theorem

Let n >= 1, let K be a compact convex subset of R^n with nonempty interior, and let f be a fixed real polynomial. All integrals in the following display are n-dimensional Lebesgue integrals. For every integer r >= 1 define

    H_r = inf { integral_K f q : q is a global sum of squares,
                deg(q) <= 2r, integral_K q = 1 }.

For any minimizer a of f on K put

    H = max_K ||Hess f||_op,   gamma = 1 + H/2,
    ell(x) = gradient f(a) dot (x-a),
    g(x) = ell(x) + gamma ||x-a||^2,
    G = max_K g,   L = n+2,
    C_n = 4 L^2 (pi/2)^(2L) (1 + 2^(n+2)).

Then G is finite and strictly positive, and

    0 <= H_r - min_K f <= C_n G/r^2     for every integer r >= 1.

A single global square witnesses the upper bound. The same proof works for f of class C^2 on an open neighborhood of K. The theorem is an upper rate for fixed K,f,n; it does not assert a positive matching lower bound for every objective, an exact asymptotic coefficient, arbitrary reference measures, the hierarchy restricted to s(f), or efficient identification of a minimizing point. There is **no remaining mathematical gap in this precise statement** identified by this review.

The stronger constant obtained below in an independent integral cross-check is audit evidence only. No submitted proof was changed or repaired.

## Complete analytic reproduction

### 1. Quadratic upper estimator and constrained minimum

Compactness supplies a minimizing a. For d=x-a and x in K the segment a+td, 0<=t<=1, is in K. The differentiable function f(a+td) has a one-sided minimum at t=0, so ell(x)>=0. This does not assume that a is interior or that gradient f(a)=0.

Taylor's integral remainder is

    f(x)-f(a)-ell(x)
      = integral_0^1 (1-t) d^T Hess f(a+td) d dt
      <= (H/2)||d||^2.

Minimality gives the lower bound f(x)-f(a)>=0, while gamma>0 and ell>=0 imply g(x)>0 for x!=a in K. Nonempty interior ensures such an x exists. Continuity and compactness give 0<G<infinity. Consequently u=g/G is a polynomial of degree at most two, u(a)=0, and 0<=u<=1 on K. There is no requirement that u be nonnegative off K.

For 0<=alpha<=1,

    g(a+alpha(x-a)) = alpha ell(x)+alpha^2 gamma||x-a||^2
                    <= alpha g(x).

Only polynomial regularity, the segment property and the Hessian operator bound were used. An open-neighborhood C^2 hypothesis suffices for the optional extension because the same segments lie in K and the continuous Hessian is bounded there.

### 2. Sublevel growth with the correct direction

For every t>0 write S_t={x in K:u(x)<=t} and F(t)=vol(S_t). These sets are measurable. For 0<s<=t, homothety by alpha=s/t about a takes S_t into S_s and has Jacobian alpha^n. Thus

    F(s) >= (s/t)^n F(t), equivalently F(t) <= (t/s)^n F(s).

The proof works without change when t>1, for which F(t)=vol(K). In particular, F(h)>=h^n vol(K)>0 for 0<h<=1. The upper bound on a larger sublevel set **relative to the same F(h)** is crucial. It does not use differentiability of F, any local volume asymptotic, a uniform solid angle, a simplex decomposition or boundary regularity.

### 3. Endpoint polynomial, signs and the core

For m>=1, N=2m+1 and

    A_m(t) = [1+2 sum_(k=1)^m T_k(1-2t)]/N,

the degree is m and A_m(0)=1. With v=arcsin(sqrt(t)), 0<t<=1, the finite geometric series gives

    A_m(t) = sin(Nv)/(N sin(v)) = sin(Nv)/(N sqrt(t)).

The defining cosine sum yields |A_m|<=1, and the sine formula yields |A_m|<=1/(N sqrt(t)). Hence

    |A_m(t)| <= min(1,(N sqrt(t))^-1).

Set h=N^-2. Convexity of arcsin places its graph below its endpoint chord, so v<=pi sqrt(t)/2. If t<=h, then Nv<=pi/2; also v>=sqrt(t). Concavity of sine on [0,pi/2] gives sin(Nv)>=2Nv/pi. Thus A_m(t)>=2/pi on [0,h], including t=0 by continuity. The direction of the convexity/chord inequality is correct. Neither monotonicity of A_m nor absence of zeros in its tails is assumed.

The independent exact binomial identity

    N A_m(t) = sum_(j=0)^m (-1)^j binom(N,2j+1) t^j (1-t)^(m-j)

comes from the imaginary part of (cos(v)+i sin(v))^N divided by sin(v). It supplies a separate coefficient-level check of the Chebyshev construction. In particular A_1(t)=1-4t/3, A_2(t)=1-4t+16t^2/5 and A_m(1)=(-1)^m/N. The sign changes are real and are harmless only because the density power is even.

### 4. Submitted all-mass shell argument

Take L=n+2 and Q=A_m(u)^(2L). Then Q=[A_m(u)^L]^2 globally, including outside K. On K it satisfies Q<=1 and Q<=(h/u)^L for u>0. Its normalization Z obeys

    Z=integral_K Q >= (2/pi)^(2L) F(h)>0.

The core u<=h contributes at most hF(h) to M=integral_K uQ. On each disjoint shell 2^j h<u<=2^(j+1)h,

    integral_shell uQ
      <= 2^(j+1)h 2^(-jL) F(2^(j+1)h)
      <= h F(h) 2^(n+1) 2^(j(n+1-L)).

Every point with u>h belongs to exactly one such shell, including a point on a dyadic endpoint in the preceding shell. Since u<=1 only finitely many shells are nonempty. Extending nonnegative upper bounds to all j>=0 is valid, including the final shell with upper endpoint above 1. Since L=n+2 the ratio is 1/2 and its sum is 2. Therefore

    M <= h F(h)(1+2^(n+2)),
    M/Z <= (pi/2)^(2L)(1+2^(n+2))/N^2.

Both integrals are over the entire original K. No mass is discarded, and both estimates use the identical F(h); that factor cancels exactly. This is not an unverified equivalence to a harder concentration theorem.

### 5. Independent integral cross-check of the cancellation

Let nu be the push-forward of Lebesgue measure under u; F is its cumulative function. This is just a change of notation for the same original integrals, not the restricted s(f) hierarchy. The pointwise envelope implies

    M <= h F(h) + h^L integral_(h,1] t^(1-L) dF(t).

For L>1, integration by parts yields

    integral_(h,1] t^(1-L) dF(t)
      = F(1)-h^(1-L)F(h)+(L-1) integral_h^1 t^(-L)F(t) dt.

This identity remains valid for a cumulative function with atoms. It can instead be proved by Tonelli from t^(1-L)=1+(L-1) integral_t^1 s^(-L)ds, so no density of the push-forward is assumed. The negative boundary term cancels the initial core bound. Applying F(t)<=h^(-n)t^n F(h) and F(1)<=h^(-n)F(h) then gives, for L=n+2,

    M <= h^2 F(h) [1+(n+1) integral_h^1 t^-2 dt]
      = [(n+1)h-nh^2] F(h)
      <= (n+1)h F(h).

This independently confirms the normalization mechanism, with the smaller numerator constant n+1. The submitted larger constant is therefore safe. The new exact checker also verifies this stronger inequality in all 60 finite power-law examples, independently of its individual shell checks.

### 6. Degree, global SOS, normalization, and small orders

For r>=2L set m=floor(r/(2L)). Then m>=1,

    deg(A_m(u)^L) <= 2mL <= r,
    deg(Q) <= 4mL <= 2r.

Since Z>0, q=Q/Z=[A_m(u)^L/sqrt(Z)]^2 is a global square with exactly unit Lebesgue mass on K. Off-K signs or growth of u never enter feasibility. For every feasible density, integral f q>=min_K f; the explicit witness gives

    H_r-f(a) <= G M/Z.

For b=r/(2L)>=1, 2 floor(b)+1>=b, so 1/N^2<=4L^2/r^2. For 1<=r<2L, the constant density 1/vol(K) is feasible and its error is at most G. Since 4L^2/r^2>1 and the additional factors in C_n exceed 1, the same bound follows. All orders r>=1, not merely multiples of a dimension-dependent integer, are covered.

## Adversarial families and exact remaining gaps

| Approach or stress family | Mechanism tested | Status and evidence | Exact gap |
| --- | --- | --- | --- |
| Boundary minimum with nonzero gradient | One-sided derivative; linear term in g | PASS by segment calculation; exact affine and concave-objective examples | None for scoped theorem |
| Interior or boundary stationary minimum | Quadratic concentration; vanishing linear term | PASS analytically; exact f=(x-1/2)^2 and f=x^4 examples | No sharper objective-specific rate claimed |
| Nonconvex f | Taylor upper bound rather than convexity of f | PASS; exact f=x-x^2 on [0,1/2] | None |
| Constant f | G remains positive because gamma includes 1 | PASS; exact error zero | No positive universal lower bound |
| Sharp cone, nonsimple apex, thin fixed bodies | Relative homothety about a instead of local cube structure | PASS; cone homothety remains exact; square-pyramid all-mass checks below | No shape-uniform sharp constant claimed |
| Broad versus sharp sublevel growth | Exponent n/2 or n, and atoms without density | PASS; cumulative-measure arguments never differentiate F; power-law cases p=1,...,n checked exactly | No arbitrary-measure claim |
| Oscillating kernel and negative endpoints | Even exponent, absolute tail bound, positive core | PASS analytically and by separate binomial identity; odd-power control rejected | None |
| Degree or critical exponent shortcuts | L must exceed n+1; root degree must be <=r | PASS; erroneous L=n+1 shell summation and r=2L-1,m=1 controls rejected | Those shortcuts are invalid and unused |
| Source scope | Unit-mass Lebesgue global-SOS hierarchy | PASS within explicit normalized interpretation | Literal incomplete display alone is not a defined optimization problem |

No counterexample to the target theorem was found. These families are falsification attempts, not evidence that an empirical sweep proves a universal theorem. Convexity, positive full-dimensional Lebesgue volume and the fixed-instance interpretation are genuine hypotheses. Removing them would invalidate steps of this proof and is outside its claim.

## Independent square-pyramid reproduction

The set 0<=z<=1, |x|<=z, |y|<=z is the intersection of the displayed halfspaces and has nonempty interior. It is compact and convex. For f=z its unique minimizer is (0,0,0). Direct integration of monomials, or the independent transformation x=zu,y=zv with Jacobian z^2, gives

    mu(a,b,c)=0 if a or b is odd,
    mu(a,b,c)=4/[(a+1)(b+1)(a+b+c+3)] otherwise.

In particular the volume is 4/3. The tangent cone at the apex is pointed and has the four extreme rays (1,1,1), (1,-1,1), (-1,1,1), (-1,-1,1). Each arises by making two bounding inequalities tight. It has four incident facets. A three-dimensional cube or simplex vertex cone has three extreme rays, while a tangent cone at a nonvertex boundary point has nonzero lineality. Invertible affine transformations preserve pointedness, lineality and extreme-ray incidence. The stated local affine distinction from every cube/simplex boundary point is therefore valid, not just a comparison of vertex names.

Let v_r contain all monomials of total degree <=r. Then H=integral_K v_r v_r^T and Z=integral_K z v_r v_r^T have the submitted rational entries. A nonzero polynomial is nonzero at some interior point (it cannot vanish identically on a nonempty open set), so its square has strictly positive integral. Therefore H is positive definite for every r. The same argument gives positivity of Z and H-Z because 0<z<1 in the interior, though only H is needed for the formulation.

For a finite sum of squares q=sum p_j^2, the top homogeneous terms cannot cancel: a sum of their real squares that is the zero polynomial would make every term zero. Thus deg(q)<=2r forces each nonzero p_j to have degree <=r. The normalized objective is a weighted mean of their Rayleigh quotients, with positive weights integral p_j^2. Conversely a single square normalized by its positive integral is feasible. The minimum Rayleigh quotient exists on the compact H-unit ellipsoid. Consequently H_r=lambda_min(Z,H) exactly for all r; no numerical SDP or finite matrix test is needed to prove that identity.

As an independent exact low-order certificate, in basis (1,z,y,x) the determinant is

    det(Z-lambda H)
      = (2/9-4lambda/15)^2
        (2/75-4lambda/45+lambda^2/15).

The scalar modes have eigenvalue 5/6 and the other two are (10 plus or minus sqrt(10))/15. Thus H_1=(10-sqrt(10))/15. This supplies a checkable exact generalized-eigenvalue calculation beyond merely restating the moment formula. The checker computes the determinant by permutations and independently compares coefficients to the factored expression. It also reconstructs exact LDL factorizations with positive pivots for H,Z,H-Z at r=0,...,4 (dimensions 1,4,10,20,35).

For m>=1 the submitted witness A_m(z)^10 is the square of A_m(z)^5, of degree 10m and hierarchy order 5m. Slice area is 4z^2, so its full normalization is 4 integral_0^1 z^2 A_m(z)^10 dz and its objective is precisely the submitted ratio with numerator weight z^3. Also F(t)=4t^3/3 for 0<=t<=1. All pyramid mass is included. For m=1 the newly computed normalization is 5540/2814669 and the objective is 18769/116340; both are exact rational numbers. Six such witnesses, m=1,...,6, were computed exactly. Finite examples do not stand in for the all-order analytic argument.

## Reproducible finite checks and controls

Run the new standard-library checker from this directory with any of:

    python3 independent_exact_checks.py --output exact_results_normal.json
    python3 -O independent_exact_checks.py --output exact_results_optimized.json
    python3 -OO independent_exact_checks.py --output exact_results_double_optimized.json

All three executions completed successfully on Python 3.14, with explicit exception-based checks that cannot be removed by optimization. Their mathematical payloads are identical after excluding run timestamp, Python environment string and optimization flag. Per execution:

- 16 coefficient identities between separately constructed kernel polynomials;
- 1,536 rational grid cases for both upper envelopes and 780 rational core lower checks;
- 20,000 integer degree/floor and small-order cases;
- 60 exact all-mass power-law shell partitions, individual shell bounds and the independent integral bound;
- 567 exact pyramid monomial moments including odd moments;
- 15 exact positive-definite matrix factorizations with full reconstruction;
- 6 exact full-pyramid normalized witnesses and 20 exact proxy-family cases;
- 3 negative controls rejected: the critical shell exponent, insufficient degree and odd power of a sign-changing kernel.

The rational core grid uses 226/355, a weaker bound than 2/pi; the proof of the actual 2/pi inequality is the analytic argument above. Global nonnegativity is proved by the square identity, not by outside-K samples. Finite arithmetic is supplementary and neither approximates an SDP nor establishes all convex bodies by sampling. These checks test different algebraic representations, exact identities, entire mass partitions and failure controls; they do not mirror a numerical implementation of the theorem and call no source-author code.

## Source match and named imports

The mathematical proof imports only elementary compactness, one-variable Taylor's integral remainder, polynomial/finite trigonometric identities, Lebesgue change of variables under a homothety, nonnegativity of real squares, and finite-dimensional Rayleigh minimization. The independent integral check additionally uses Tonelli or Stieltjes integration by parts. Every substantive inequality and the moment identity are derived above. No external convergence, Christoffel-function, orthogonal-polynomial asymptotic or kernel-concentration theorem is assumed.

Primary sources actually retrieved and inspected in this review:

1. [Laurent's OWR contribution](https://ems.press/content/serial-article-files/46772?nt=1), full PDF retrieved; contribution PDF pp.23-25 / printed pp.2991-2993 visually read in full. Equation (2) uses probability measures. Printed equations (3)-(4) visibly omit the equality/value after the integral constraint. Item (2) specifically uses convex bodies and Lebesgue measure. The final paragraph asks for the general-convex-body convergence regime. Thus supplying unit mass is an explicit interpretation/repair of an incomplete mathematical display, consistent with its probability formulation; it is not an OCR repair or a result for a literal unnormalized formula. Retrieval: 590,481 bytes, SHA256 `a90207e0cadc310ab5a52a228c4b25a16f5e5f617542f006e9909cf90d4c72d2`.

2. [Slot-Laurent arXiv:1905.08142v2](https://arxiv.org/pdf/1905.08142v2), full PDF retrieved; PDF pp.2,5,6,17,29 visually read in full. Equation (3) supplies exactly the normalized global-SOS degree-2r hierarchy; Lemma 1 and Lemma 4 give the previously established constrained-gradient and quadratic-estimator ingredients. Theorem 11 gives the logarithmic convex-body rate, and p.29 asks about an O(r^-2) bound for all convex bodies. This confirms the upper-rate target match; it is not a proof that the question remains open today. Retrieval: 573,575 bytes, SHA256 `c8aebdfc6a1b6a65dbdebbea6b31edfcb4e4bd711d4fc80077a2485bd7e6764a`.

Source-inspection limits: the first browser screenshot of OWR p.23 timed out; local retrieval, rendering and visual inspection then succeeded. Full retrieval is not full reading or a source-proof audit. This reviewer did not independently retrieve the other papers in submitted `SOURCE_VERIFICATION.json`, did not repeat its 2026 overview or priority screen, and does not endorse those bounded historical/current-literature claims as fresh findings. Their truth is unnecessary for the elementary theorem. The submitted historical execution counts are not freshly reproduced counts; only the newly authored checks listed above were run.

## Disposition

PASS for the all-integer-order, fixed-instance, Lebesgue-normalized global-SOS upper theorem and the exact pyramid supplement. No proof correction, counterexample or missing central assumption was found. The normalized interpretation of the incomplete original display must remain explicit. There is no support here for widening the result to arbitrary reference measures or to the general original-objective s(f) hierarchy, or for claiming a two-sided rate for each f. Novelty, priority, current openness and publication readiness remain outside this mathematical verdict.
