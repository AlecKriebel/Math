# Independent reconstruction before comparative verdicts

Saved 2026-10-14 04:44:17 UTC. Inputs read: root AGENTS.md; frozen source/author/PROOF.md, SOURCE_METADATA.json, README.md; inspected read-only queue.py show implementation and a read-only SQLite reproduction of its target output; official original report, visually and in text, printed pages 421-422. No prior audit or second-review verdict has been read.

Target identity: PR 822, original head c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c; immutable author proof in sibling source. Source dataset review hash is 0f73b6392b73ca2e1294a961a56b4729d60540884ab899fd488c8e11885a718c. Original report PDF has 638962 bytes and SHA256 a3ab668409f786c7c1783150d9f937b2d6e06471a48b76c5721b58a49bf3a683. Public source: https://ems.press/content/serial-article-files/46205.

## Exact target and falsifiable success criterion

The source asks whether, for every n>=3 and every smooth positive W on the round unit sphere with integral W^(n/2) equal to round volume, the maximum of t^(n/2) Tr(exp(-t W^(-1/2) Y0 W^(-1/2))) is at most its value for W=1. Here Y0=positive Laplacian+n(n-2)/4, acting in round L2. The source imposes no constant scalar curvature, minimizing, curvature bound, or size restriction on W. A single admissible W in dimension three with a value strictly exceeding the round all-time bound disproves this universal statement. It does not settle its n>=4 restriction or Conjecture 2 / 30001169.

The falsification checks are: W must extend smoothly and remain positive at both poles; its conformal metric must be on S3 itself; the weighted operator must have the specified exterior powers and measure; trial modes must belong to the closed-manifold form domain; rescaling must preserve both the exact heat time and prefactor; the comparison must control every round positive time, rather than only selected times or the zero-time limit.

## 1. Smooth finite geometry

In stereographic polar radius r=e^s, the round metric is sech(s)^2 (ds^2+g_S2). This is the full twice-punctured S3, not a new topology. Put c=L/2 with L=10000, q=abs(s)-c, and u=exp(-chi(q) log(cosh(q))), where chi is the submitted standard smooth step. The denominator defining chi is nonzero for every real q; chi=0 for q<=0 and chi=1 for q>=1. Its flat derivatives at 0 and 1 ensure smooth pasting. The nonsmooth abs(s) is harmless because u=1 on the open neighborhood (-c,c) of zero. Thus u is smooth and positive on the punctured sphere, and equals one on the exact cylinder [-c,c] x S2.

Near the positive pole set rho=e^(-s). There q=s-c and u=sech(s-c). Direct substitution gives

    g_L = [4 exp(L)/(1+exp(L) rho^2)^2] (d rho^2+rho^2 g_S2),
    W_L = u^2 cosh(s)^2
        = exp(L) (1+rho^2)^2/(1+exp(L) rho^2)^2.

Writing rho^2=x1^2+x2^2+x3^2 proves that both are smooth at rho=0, with strictly positive coefficient 4 exp(L) for the metric and strictly positive pole value exp(L) for W_L. The negative pole uses rho=e^s and the same formulas. L is one fixed finite integer, so exp(L) is a finite real number and these are nonsingular charts. No uniform bound as L tends to infinity is invoked.

Since 0<u<=1 and u(q)=sech(q) for q>=1, each cap contributes at most 1+8/(3e^3)<2 to integral u^3 ds. The product area is 4pi, giving

    4pi L <= V_L=4pi integral_R u^3 ds < 4pi(L+4).

The lower bound proves V_L>0; the upper bound is the needed direction. Curvature in transitions can be large or negative. This creates no obstruction because the argument uses only local trial support plus global conformal positivity.

## 2. Conformal covariance, measure, and strict positivity

For h=exp(2omega)g in dimension three, with the positive Laplacian convention, the local formulas are

    Delta_h f = exp(-2omega)[Delta_g f - <grad omega, grad f>],
    R_h = exp(-2omega)[R_g+4 Delta_g omega-2 |grad omega|^2].

Applying the positive-Laplacian product rule to exp(omega/2)f gives

    Y_g(exp(omega/2) f)
      = exp(omega/2)[Delta_g f-<grad omega,grad f>
          +(R_g/8+(Delta_g omega)/2-|grad omega|^2/4)f].

Hence Y_h=exp(-5omega/2)Y_g exp(omega/2)=W^(-5/4)Y0 W^(1/4) when h=Wg0. This checks the sign and coefficient R/8 against the round value 6/8=3/4 and product-cylinder value 2/8=1/4. The local conformal formulas can also be verified from the Levi-Civita connection; their use is an imported standard differential-geometric identity, not a new hypothesis.

The volume relation is dv_h=W^(3/2) dv_g0. Multiplication U:f -> W^(3/4)f therefore satisfies ||Uf||_round=||f||_h. Conjugating exactly gives

    U Y_h U^(-1)
      = W^(3/4) W^(-5/4)Y0 W^(1/4) W^(-3/4)
      = W^(-1/2)Y0 W^(-1/2).

All powers act as smooth multiplication on the compact sphere, so this identity extends from smooth functions to the self-adjoint elliptic realization. The form domain is H1, and U maps it to H1, since W and its reciprocal are smooth and bounded together with their derivatives on this fixed compact manifold.

For the weighted operator and psi in its form domain,

    q_W(psi)=integral [|grad(W^(-1/2)psi)|^2
                           +(3/4)|W^(-1/2)psi|^2] dv_g0
             >= (3/[4 max(W)]) ||psi||_round^2.

This is a strict positive spectral gap. In particular negative scalar curvature in a cap is not an unproved positivity assumption. Compactness and smooth ellipticity give a discrete spectrum, compact resolvent, and a heat trace for all t>0. Trace class may be checked without a new geometric bound: the inequality |a+b|^2 >= |a|^2/2-|b|^2 gives q_W >= (1/[2 max W])||grad psi||^2-C||psi||^2, where C=||grad(W^(-1/2))||_infinity^2. Min-max and the explicitly known round Laplacian spectrum then imply eigenvalue growth at least of order k^(2/3), which makes every positive-time heat sum convergent.

## 3. Form-domain trial functions and spectral order

Let D=(-L/2,L/2)xS2. Each sine mode phi_j=sin(pi j(s+L/2)/L), constant in S2, belongs to H1_0(D). Its zero extension belongs to H1(S3,g_L). In local collar coordinates, its value is continuous at each interface, and its weak first derivative is the piecewise derivative; the distributional derivative has no surface delta because the value, rather than the normal derivative, vanishes at the interface. Equivalently use continuity of zero extension from H1_0(D) to H1 of the ambient manifold. A derivative jump excludes H2 in general but does not exclude the quadratic-form domain. No integration by parts across the seam is needed.

On D the metric is exactly the product and R=2. Direct sine orthogonality yields

    <phi_i,phi_j> = 2pi L delta_ij,
    q(phi_i,phi_j) = 2pi L [1/4+(pi j/L)^2] delta_ij.

Both forms integrate only over D; the zero extension contributes zero outside D. Thus the maximum quotient on the k-dimensional span of the first k modes is mu_k=1/4+(pi k/L)^2. The min-max theorem for the closed, lower-bounded form gives lambda_k(g_L)<=mu_k for every k>=1, with full multiplicities and indexing from one. The monotonicity of exp(-4x) then yields finite partial-sum inequalities. Taking increasing limits, justified by positivity and trace class, gives

    Tr(exp(-4Y_gL)) >= e^(-1) sum_(k>=1) exp(-4pi^2 k^2/L^2).

This is not an unsupported decoupling assertion, not an assertion of actual cylinder eigenfunctions on the sphere, and not spectral convergence in L. Dirichlet trial functions give the correct direction, an upper bound for eigenvalues and therefore a lower bound for the heat trace.

For G decreasing and nonnegative, G(k)>=integral_k^(k+1)G. Summing yields sum_(k>=1)G(k)>=integral_1^infinity G>=integral_0^infinity G-1. The last Gaussian integral is L/(4sqrt(pi)). Thus the trace is at least e^(-1)(L/(4sqrt(pi))-1), positive for the chosen L.

## 4. Normalization and time

Define a=(2pi^2/V_L)^(2/3)>0, h=a g_L, W=aW_L, and t_star=4a. The unknown exact volume is a well-defined explicit finite integral, not a fitted numerical estimate. Metric scaling gives dv_h=a^(3/2)dv_gL and Y_h=a^(-1)Y_gL, since both the Laplacian and scalar curvature scale by a^(-1). Hence

    integral W^(3/2) dv_g0 = a^(3/2)V_L = 2pi^2,
    t_star^(3/2) Tr(exp(-t_star Y_W))
        = 8a^(3/2) Tr(exp(-4Y_gL))
        = (16pi^2/V_L) Tr(exp(-4Y_gL)).

Using the upper bound on V_L in the denominator, and a positive trace lower bound, gives

    F_W(t_star) >= [sqrt(pi)/e] [L-4sqrt(pi)]/[L+4].

Using sqrt(pi)>1772/1000, sqrt(pi)<1773/1000 and e<2719/1000 separately, with the latter two controlling the numerator difference and reciprocal exponential in the correct direction, gives

    F_W(t_star) > (1772/2719) (9992908/10004000)
               = 1106714561/1700054750 > 13/20.

The final rational inequality is independently checkable. No floating-point realization of exp(10000), numerical integration of a, curvature estimates, or cap eigenvalue calculation is needed.

## 5. Round side and maxima

The degree j-1 spherical harmonics on S3 have Laplacian eigenvalue j^2-1 and multiplicity j^2. Thus the relevant round trace is sum j^2 exp(-t(j^2-1/4)), including the +3/4 potential. Differentiating the Gaussian Poisson identity gives the submitted small-time formula. Its correction terms are strictly negative for 0<t<=1. The upper bound sqrt(pi)e^(1/4)/4 < 1773/3000 <129/200 is valid because the exponential Taylor series is strictly less than the geometric series 4/3.

For each of the 100 intervals [k/100,(k+1)/100], k=100,...,199, the interval upper bound in the author proof uses increasing t^(3/2) and decreasing exponentials correctly. Starting at j=4, the ratio of the j+1 summand to the j summand is at most (25/16)e^(-9)<1/2, so 32e^(-63a/4) bounds the full tail. Finite rational comparisons for these 100 intervals remain to be independently replayed in a newly authored checker. This is a finite arithmetic obligation, not an analytic one.

For t>=2 each individual summand t^(3/2)e^(-lambda t) is nonincreasing because lambda>=3/4 and its derivative has sign 3/2-lambda t. Sum domination is enough to conclude monotonicity; an interchange of differentiated infinite series is unnecessary. The last closed interval includes t=2. These facts complete the all-time reduction once the 100 arithmetic bounds are checked.

For each fixed normalized smooth h, the standard local heat asymptotic gives lim_(t->0) t^(3/2)Tr(exp(-tY_h))=vol(h)/(4pi)^(3/2)=sqrt(pi)/4. The source itself states the same normalized leading coefficient. Trace class makes the scaled trace continuous on positive times. The strictly positive gap gives decay to zero at infinity, for example Tr(exp(-tY))<=exp(-(t-1)lambda_1)Tr(exp(-Y)) for t>=1. The constructed value exceeds the small-time limit. The round value at t=2 also exceeds that limit, as its first summand gives 2sqrt(2)e^(-3/2)>sqrt(pi)/4; squaring reduces this to 128>pi e^3. Thus both suprema are attained on positive compact time intervals, making literal maxima legitimate.

## Status at this independence checkpoint

The geometric and analytic mechanism reconstructs without an identified gap. Imported standard theorems/identities are conformal metric formulas, H1_0 zero extension, min-max for compact elliptic forms, Gaussian Poisson summation, round harmonics spectrum, and the leading local heat coefficient. They are applied with their hypotheses checked above. Remaining finite task: independently verify the constant enclosures and 100 rational intervals. Remaining audit task: run explicit adversarial controls and record a final required-fixes/CLEAR decision. This is an audit of an authored counterexample, without claims of firstness, journal publication, or human peer review.
