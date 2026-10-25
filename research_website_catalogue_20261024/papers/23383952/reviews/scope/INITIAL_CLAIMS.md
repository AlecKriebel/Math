# Independent initial reconstruction before foreign bodies or archived opinions

The actual deposited four-page PDF was read completely, including references, together with the complete13427-byte controlling note.tex. All four page renders were inspected. No foreign primary body, current/historical scientific assessment, archived audit narrative or supplied program has been read or executed. ZIP names, nested-container identities and hashes are custody only. The target's own attribution statements are hypotheses to check, not independent priority findings.

## Literal claim, category and success criterion

For the unit round S^n with positive Laplacian, Y0=Delta+n(n-2)/4 and YW=W^(-1/2)Y0W^(-1/2) on L2(dV0). The conjecture as quoted by the target quantifies over all smooth positive W with integral W^(n/2)dV0=vol(S^n), asking whether max_(t>0) t^(n/2)Tr exp(-tYW) is bounded by the round maximum. The target supplies one W on S^3, defined through a finite cylinder length L=10000 and explicit C-infinity caps, with exact normalization and t*=4a>0 such that

    t*^(3/2) Tr exp(-t*YW) > 1106714561/1700054750 >13/20,
    max_(t>0) t^(3/2) Tr exp(-tY0) <321/500.

It also claims both maxima occur at finite strictly positive times. This is a counterexample to a universal n≥3 statement through n=3; it does not settle n≥4 or the separate source monotonicity question. The original precise operator, normalization, quantifiers and unrestricted weight class must be checked in the actual historical question. The finite construction is not an asymptotic L→infinity claim or a numerical search over weights/times. Its time and normalization may be specified by the given convergent real integral rather than by a rational closed form.

## Independently rederived mechanism

1. **Geometry and actual pole extension.** On the twice-punctured round sphere, r=e^s gives g0=sech²s(ds²+gS2). With q=|s|-L/2, the usual flat step chi(q) and u=exp(-chi(q) log cosh(q)) give u=1 on the entire closed cylinder and u=sech(q) beyond q=1. The absolute-value corner lies in a neighborhood where u is constant. At q=0 the flat jets of chi give matching to1; at q=1 the flat jets of1-chi give matching to sech(q). At either pole rho=exp(-|s|), direct substitution gives u=2e^(L/2)rho/(1+e^Lrho²), hence

       WL=e^L(1+rho²)²/(1+e^Lrho²)²,
       gL=4e^L/(1+e^Lrho²)² (d rho²+rho²gS2).

   These are smooth strictly positive Cartesian radial coefficients at rho=0. Every quantity is finite for this fixed L; no machine representation of exp(10000) is needed. The volume is VL=4pi integral u³ds. The exact cylinder contributes4pi L. Each end contributes at most1+integral_1^infinity8exp(-3q)dq<2, since0<u≤1 on0≤q≤1 and sech(q)≤2exp(-q) afterward. Thus4pi L≤VL<4pi(L+4).

2. **Normalization and operator identity.** Put a=(2pi²/VL)^(2/3), h=a gL, W=a WL, t*=4a. Then volume(h)=a^(3/2)VL=2pi² exactly. In dimension3, conformal covariance has exponents Yh=W^(-5/4)Y0W^(1/4), since h=Wg0, while the unitary L2(dVh)→L2(dV0) is multiplication by W^(3/4). Composing exponents gives precisely UYhU^(-1)=W^(-1/2)Y0W^(-1/2). All multipliers and inverses are smooth and bounded on the compact sphere, so the closed forms and spectra agree. For f, its form is the round form on W^(-1/2)f and is at least3/(4 max W)||f||². Thus the spectrum is strictly positive regardless of a possibly negative transition scalar curvature. Constant metric scaling gives Yh=a^(-1)YgL.

3. **Trial subspaces and trace direction.** The exact cylinder has scalar curvature2 and Yamabe potential1/4. The S2-constant sine functions sin(pi k(s+L/2)/L) have zero boundary trace; their zero extensions lie in global H1, which is the form domain. Their first weak derivatives are piecewise ordinary derivatives, without a boundary delta because the functions themselves vanish at the boundary. A jump of second derivative/operator-domain behavior is irrelevant to the form min–max argument. Norm and form matrices on the first K modes are diagonal, with highest Rayleigh quotient1/4+(pi K/L)². The kth full-manifold eigenvalue therefore satisfies lambda_k≤that quantity, with all full-spectrum multiplicities included. Consequently, at time4, the heat trace is bounded **below** by exp(-1)sum_(k≥1)exp(-4pi²k²/L²).

4. **Finite lower bound, including the scaling prefactor.** For the decreasing Gaussian, the integer sum is at least its integral from1 to infinity, while the missing0-to1 integral is at most1. The whole Gaussian integral is L/(4sqrt(pi)). Hence Tr exp(-4YgL)≥exp(-1)(L/(4sqrt(pi))-1). Because (4a)^(3/2)=16pi²/VL, the scaled weighted trace is strictly larger than

       (sqrt(pi)/e) (L-4sqrt(pi))/(L+4).

   Strictness follows from the strict volume upper bound and positive numerator. Using sqrt(pi)>1772/1000, sqrt(pi)<1773/1000 and e<2719/1000 separately in the positive factors gives the stated rational product1772/2719*(10000000-7092)/10004000. The displayed reduced fraction and exact difference from13/20 remain explicit arithmetic checks to reproduce after this early seal. No assertion about a limiting cylinder is used.

5. **Round spectrum and all-time partition.** Round degree j-1 harmonics on S3 have multiplicityj² and Laplace eigenvaluej²-1, so Y0 has eigenvaluej²-1/4. Starting with the full Gaussian theta sum, Poisson summation and differentiation give

       F0(t)=sqrt(pi)/4 exp(t/4)
             [1+2 sum_(m≥1)(1-2pi²m²/t)exp(-pi²m²/t)].

   The sign of every nonzero correction is negative for0<t≤7/5. This bounds all such t by(1.773/4)exp(7/20). For t≥2, every individual scaled spectral term is nonincreasing, since its derivative has sign3/2-t lambda_j and lambda_j≥3/4. It remains to cover the compact interval[7/5,2], not a numerical grid on an unbounded interval.

6. **Intermediate intervals and the infinite tail.** Write F0=A+B with A=t^(3/2)exp(-3t/4) the first mode. A increases through t=2. Every term in B (j≥2) decreases once t≥2/5. Thus on[a,b]⊂[7/5,2], F0(t)≤A(b)+B(a). In the tail j≥3, the consecutive ratio is at most(16/9)exp(-7a)<1/2: for j≥3 the squared multiplicity ratio is at most16/9 and the exponential eigenvalue gap at least7. Therefore B(a)≤a^(3/2)[4exp(-15a/4)+18exp(-35a/4)]. Six adjacent intervals with endpoints7/5,3/2,8/5,17/10,9/5,19/10,2 cover the compact region. The largest claimed rational upper enclosure is641202/10^6, below321/500. The exact seven table rows are still certificate obligations to recompute; the monotonicity/tail mechanism itself has been rederived without consulting code.

7. **Rational certificate direction.** Positive partial sums PN(x) bound exp(x) from below for every x≥0. Hence1/P50(x) bounds exp(-x) from above; there is no direction reversal. The exponential upper tail bound follows by a geometric comparison of successive Taylor terms once x<N+2. The stated x=7/20 and1 satisfy that condition at N=14. Replacing sqrt(a) by(floor(10^8 sqrt(a))+1)/10^8 is a strict upper bound, including when the scaled square root is integral. The integer floor can be certified by rational squaring or integer square roots. For the pi enclosure, tan(2atan(1/3))=3/4, and adding atan(1/7) gives tangent1 with an angle in the first quadrant. Thus pi=8atan(1/3)+4atan(1/7). The24-term alternating lower sums and next-term remainders give rational pi brackets; squaring gives sqrt(pi) bounds. Supplied code and table arithmetic have not yet been inspected or accepted.

8. **Maxima really are attained.** The small-time heat coefficient for either normalized smooth geometric Yamabe operator is volume/(4pi)^(3/2)=sqrt(pi)/4. Unitary equivalence transfers this limit to the weighted presentation. The positive spectral gap gives Tr exp(-tY)≤exp(-(t-1)lambda1)Tr exp(-Y) for t≥1, so the scaled trace tends to0 at infinity. The weighted value>13/20 exceeds the zero-time limit. For the round trace, its first mode at2 is2sqrt(2)exp(-3/2)>sqrt(pi)/4, equivalently128>pi e³. These strict comparisons, continuity and endpoint limits put both suprema on compact positive-time intervals. They do not require uniqueness of a maximizing time.

I presently find no central conceptual contradiction in this finite construction. The exact table arithmetic and all source applicability/priority statements remain unverified at this initial checkpoint. This is not assent from a historical PASS, and it does not treat finite tests as universal proof.

## Materially distinct attack families

| Family | Proposed failure | Independent evidence already obtained | Exact remaining check |
|---|---|---|---|
|A: historical operator/category|The source asks a different weighted operator, weight norm, dimension range or maximum|Literal target claim isolated above|Read actual Morpurgo item(16), including adjacent conjecture, not a paraphrase|
|B: finite geometry and endpoints|Caps are only asymptotic, |s| or pole singularity destroys smoothness, or weight vanishes|Explicit Cartesian pole coefficients and flat matching rederived for finite L|Check cited cylindrical prior construction and attribution; source claims may not be inherited blindly|
|C: volume and scaling|Missing sphere area, wrong W exponent, wrong t prefactor invalidates separation|VL bound, a^(3/2)VL=2pi² and(4a)^(3/2)=16pi²/VL derived|Exact constant/fraction replay and negative controls|
|D: weighted/geometric operator|Different L2 measure, wrong conformal exponents, closed-form domains or negative cap curvature|Unitary exponent composition and positive round quadratic form independently checked|Actual primary covariance/min–max/heat assumptions and proof interfaces|
|E: spectral trial spaces|Zero extension is not in the operator domain, eigenvalue index/multiplicity or inequality direction is wrong|Only global form domain H1 is required; K-dimensional diagonal trial space gives lambda_K≤mu_K|Selected exact support code may check arithmetic only, not replace domain proof|
|F: lower Gaussian estimate|Finite sum/integral error or reversal makes the lower bound too optimistic|Decreasing-function integral bound and correct Gaussian integral derived|Recompute all rational constants independently; numerator positivity and strictness|
|G: all-time upper bound|A finite t-grid misses an interior peak, small-time image correction has wrong sign, or large-time terms not monotone|Poisson formula, sign range, six closed intervals and termwise monotonicity derived|Exact seven enclosures, endpoint rounding and tail-ratio controls|
|H: rational arithmetic|Taylor remainder domain, reciprocal direction, Machin branch, square-root flooring or optimized asserts are wrong|Directions and tangent identity independently derived|Read supplied certificate program before isolated execution; use a materially separate Fraction implementation and meaningful mutants|
|I: endpoints and attainment|Supremum sits at t=0, diverges, or lambda1 is nonpositive|Positive form bound, standard heat limit and strict interior comparison identify needed hypotheses|Check actual imported heat/min–max statements; do not claim a reproduced formal certificate|
|J: novelty and scope|Classical Pinocchio geometry or Morpurgo trace inequalities already contain the asserted application, or a separate conjecture is conflated|The target credits the geometry and says firstness/current openness are unestablished|Inspect actual AJ/Morpurgo versions and bound access limits/priority honestly; no inference from search silence|

A substantive defect found later will be documented with exact evidence and a defer recommendation, without repairing the manuscript or substituting a narrower public result. Default follow-up is none.
