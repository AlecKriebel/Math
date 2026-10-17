# Source, scope, and parameter audit — shared pass 1

Target: row 1795 / ID 20000699, adopted two-arrow rank-one witness V1.
Disposition: **DIRECT PRIOR ART; NOT AN EXACT PRIOR-THEOREM COVERAGE CERTIFICATE.**
No novelty claim, publication, queue change, or stronger target is made here.

## 1. What the primary sources already supply

The following sources were inspected as primary mathematical sources, not through a secondary description.

1. Conrey–Keating, *Pair correlation and twin primes revisited*, [arXiv 1604.06124v2](https://arxiv.org/pdf/1604.06124v2), and the [final published version hosted at AIM](https://aimath.org/~kaur/publications/92.pdf), Proc. R. Soc. A 472 (2016), 20160548, DOI 10.1098/rspa.2016.0548. The final version numbers its results Theorems 1.1 and 1.2 and Conjecture 5.1; the arXiv copy uses Theorems 1 and 2 and Section 4 Conjecture 1. Both introduce the same singleton coefficient family, its numerator derivative giving minus von Mangoldt, the explicit Ramanujan correlation profile, and the conditional truncated-ratios comparison. The final version's pp. 2–9 were inspected, including the arithmetic proof and correlation conjecture. Its source restrictions and displayed identities still need the audit described below.
2. Conrey–Keating, *Averages of ratios of the Riemann zeta-function and correlations of divisor sums*, [arXiv 1611.09198v1](https://arxiv.org/pdf/1611.09198v1), Nonlinearity 30 (2017), R67–R80. Introduction and Theorems 1–2 identify the one-swap contribution for general shift sets. They do not establish arbitrary swap rank at arbitrary polynomial lengths. The first paragraph expressly puts denominator shifts in the positive-real-part region.
3. Conrey–Snaith, *Applications of the L-functions ratios conjectures*, [arXiv math/0509480v2](https://arxiv.org/pdf/math/0509480v2), Proc. London Math. Soc. 94 (2007), 594–646. Conjecture 2.1, conditions (2.11), Remark 2.4, and Theorem 2.5 already use shift-uniform ratios estimates and differentiation to obtain logarithmic-derivative averages. The denominator conditions are of size at least a positive constant times 1/log T, and Theorem 2.5 keeps the differentiated arguments to the right of the critical line.
4. Keating–Smith, *Twin prime correlations from the pair correlation of Riemann zeros*, [arXiv 1903.07057v1](https://arxiv.org/pdf/1903.07057v1), explicitly describes its reverse Fourier calculation as formal/heuristic. It is not an error-controlled fixed-h inversion theorem.

The first three are direct prior art for the intended mechanism. They do **not** provide an inspected theorem with every part of adopted V1 simultaneously: the exact full-real Fourier-support cutoff, every stated exponent, sharp endpoints, the centered four-variable disc including a=0, the differentiated O(N^phi rho^-2) error, and the evaluated aggregate prime main term. A completed V1 would be a credited conditional adaptation/error audit unless independent evidence supports a distinct novelty claim. Failure to find the simultaneous package in a bounded search is not a priority or openness certificate.

The original AIM question asks for *some version*. The adopted finite rank-one witness is a legitimate declared interpretation; it must not be relabeled as full-zeta microscopic ratios, all-rank CK, or individual fixed-shift Hardy–Littlewood.

## 2. GRH is a real source qualification

CK2016 Theorem 1 / final Theorem 1.1 explicitly assumes GRH. The proof uses it when identifying poles of additive-twist Dirichlet series after decomposition into characters: only principal-character poles are retained near the point 1. CK2017 Theorem 1 has the same qualification.

Therefore an argument that imports that pole-extraction theorem must retain GRH in its headline. An independent proof of a local Euler-product identity involving the already-frozen Ramanujan density would not, by itself, need GRH, but that is a separate proof and must be identified as such. It does not silently remove GRH from the source's additive-twist interpretation.

Moreover, the source's displayed s-dependent identification cannot be accepted merely because its s=0 Euler factors agree. With q_z(h) denoting the displayed density coefficient and v=alpha+beta+s,

D_z(v) = sum_(h>=1) q_z(h) h^(-v)
       = zeta(v)/[zeta(1+gamma-alpha) zeta(1+delta-beta)]
         times product_p [1 + F_(alpha,gamma)(p) F_(beta,delta)(p) (p^(1-v)-1)/p^2].

On a common absolute-convergence domain, and then by continuation, multiplying out the reciprocal-zeta factors yields

chi(1-v) D_z(v)
 = zeta(1-alpha-beta-s)
   times product_p [1-p^(-1+alpha-gamma)-p^(-1+beta-delta)+p^(-1-s-gamma-delta)].

This is the shifted object B_(-beta,-alpha-s,gamma+s,delta)(1), equivalently
B_(-beta,-alpha,gamma+s,delta+s)(1-s), rather than a naive B_(-beta,-alpha,gamma,delta)(1+s). This audit flags the discrepancy for the independent arithmetic/main-term proof; it does not certify an unexamined contour identity from the printed source. The corrected shifts also follow directly by applying Perron shifts to the full ratios one-swap expression before combining the Perron variables.

## 3. The allowed complex neighborhood is safe for finite objects, unsafe for full zeta ratios

For fixed N the coefficient I and finite polynomial are entire in all shifts. Taking a finite t-integral against a Schwartz weight preserves entire dependence locally uniformly. Hence no zero-avoidance condition is needed for R_(T,N).

For the arithmetic profile, all differences gamma-alpha and delta-beta have modulus at most 2c/log N. On an expanded neighborhood of the closed disc, 1/zeta(1+u) is holomorphic, with its removable value 0 at u=0; the pole of zeta at 1 is a zero of the reciprocal, not an obstruction. For large N, the local factors 1-p^(-1+alpha-gamma) cannot vanish because Re(alpha-gamma)<1. For fixed h, the Ramanujan series is normally convergent near the disc: away from the finitely many primes dividing h its local terms are O(p^(-2+4rho)); at primes dividing h they are finite holomorphic factors. The factor 1-alpha-beta is bounded away from zero for large N. This supplies local holomorphy, not an unproved uniform-in-h bound.

The full quotient is different. The adopted range includes a=0, and the independent denominator shifts then include points on either side of the critical line. At t equal to an ordinate of a critical-line zero, varying gamma independently creates a pole through the neighborhood. Cancelling numerator and denominator at the exact diagonal does not give a holomorphic neighborhood of independent shifts. Even under RH, a disc centered at r=a/log N stays strictly to the right only when a>c; V1 expressly includes a=0. The CS2007 denominator restrictions therefore cannot be directly invoked on V1's full disc. This obstruction is avoided by the specified finite polynomial; it must not be used to reject or change that object.

Cauchy's mixed-derivative loss is rho^(-2)=(log N)^2/c^2. With lambda phi<1, N^phi rho^(-2)=o(T). This is elementary bookkeeping following the earlier uniform-differentiation method, not a new mechanism.

## 4. Nonempty length range and a necessary compatibility warning

The formal length interval is

1 < lambda < min(2, 1/phi, 1/(1-psi)) if 0<psi<1,
1 < lambda < min(2, 1/phi) if psi>=1.

It is nonempty for every formal pair 0<phi<1, psi>0. For example phi=3/4, psi=1/4, lambda=6/5 works: both products are 9/10. Strict margins, not uniformity at their boundaries, are required.

There is, however, an additional **nonvacuity obstruction to the unrefined density**: the full complex-uniform hypothesis as written is impossible if psi>phi. This does not alter the conditional transfer theorem and does not preclude the compatible example above. It does mean that the whole formally allowed parameter set must not be presented as a plausible conjectural arithmetic range.

### Proof of the obstruction when psi>phi

Use the a=0 member of the adopted family, and let X=N/2. Choose
phi < b < min(psi,1), h=2 floor(X^b/2), and r=c/(4 log N).
For all x in [X,2X], h<=x^psi for large N. The points Delta_0 and Delta_r, and fixed fractions of rho around their alpha,beta coordinates, lie inside the original disc centered at 0. Cauchy differentiation of the assumed uniform error gives, for u=0 and u=r,

A_u(x,h):=sum_(n<=x) Lambda(n)Lambda(n+h)[n(n+h)]^(-u)
 = S(h) x^(1-2u)/(1-2u) + O(X^phi (log N)^2),

uniformly throughout that interval. Here the elementary collision derivative of the prescribed profile is S(h), since F_(r,r)(p)=-p/(p-1) and the two reciprocal zeta factors have first derivatives -1 in alpha and beta. This step is independent of a full-zeta conjecture.

Now apply Stieltjes integration by parts to A_0 on (X,2X], with
f_r(x)=[x(x+h)]^(-r). Positivity and monotonicity give bounded total variation, and hence

A_r(2X,h)-A_r(X,h)
 = S(h) integral_X^(2X) [x(x+h)]^(-r) dx
   + O(X^phi (log N)^2).

The directly assumed formula for A_r gives instead S(h) integral_X^(2X) x^(-2r) dx with the same error. Their main-term difference is positive and, because h=o(X), is at least a fixed multiple of S(h) r h. For even h, S(h)>=2 product_(p>2)(1-1/(p-1)^2)>0. Also x^(-2r) is bounded below by a positive constant independent of N on this interval. Thus the two claims would force

h/log N << X^phi (log N)^2,

contradicting h asymptotic to X^b with b>phi.

The discrepancy comes exactly from replacing n^(-r)(n+h)^(-r) by n^(-2r) over the *entire hypothesis range*, not from the small h/n region used by the Fourier kernel. If a theorem only needs the kernel range h/x=O(1/T), that discrepancy can be negligible there, but one must not silently weaken the stated arithmetic hypothesis to that range. Nor may one silently refine the fixed density. A restricted compatible parameter choice or an explicitly adopted refined density is needed for a nonvacuous formulation outside this obstruction.

## 5. Whole-real weight, parity, and the t=0 contribution

A real Schwartz w with compactly supported smooth Fourier transform extends to an entire function. Both w(u) and w(-u), restricted to positive u, satisfy the analytic/rapid-decay type of smoothing appearing in CK. The whole-real finite average splits exactly into positive-time averages with those two weights and the coefficient pairs interchanged. But real w need not be even, and its transform need not be real. The two orientations must be kept until their symmetric arithmetic main profiles have been combined.

For the density main term the relevant Fourier combination is
W(u)=hat w(u)+hat w(-u) for u>0.
Its Mellin transform is
M_W(v)=integral_0^infinity W(u)u^(v-1)du, Re(v)>0.
It has rapid vertical decay on closed positive-real-part strips. The usual cosine-transform identity reads

M_W(v)=chi(1-v) integral_0^infinity [w(t)+w(-t)]t^(-v)dt

in the ordinary integral strip 0<Re(v)<1. Outside that strip the right-hand side must mean meromorphic continuation, with its polar terms retained. In particular CK's displayed Re(s)=2 inner t-integral is not an ordinary convergent integral for V1 when w(0) is nonzero.

For the linearly approximated density functional, the direct absolutely-convergent starting representation is

T (T/(2pi))^(-alpha-beta) /(2pi i)
 times integral_(sigma) [(2pi N/T)^s/s]
 M_W(alpha+beta+s) D_z(alpha+beta+s) ds,

with sigma chosen so Re(alpha+beta+s)>1 and with ordinary Perron endpoint conventions handled separately. This expression comes directly from the Fourier kernel and does not require an invalid t=0 interchange.

The pole at v=1 is important. The Euler product above gives
Res_(v=1) D_z(v)=1/[zeta(1+gamma-alpha)zeta(1+delta-beta)],
while M_W(1)=w(0) by Fourier inversion. Moving this Mellin contour from Re(v)>1 to an ordinary time-Mellin strip Re(v)<1 therefore contributes the explicit residue

2pi w(0) N^(1-alpha-beta)
 /[(1-alpha-beta)zeta(1+gamma-alpha)zeta(1+delta-beta)].

At Delta_r, its alpha,beta derivative is
2pi w(0) N^(1-2r)/(1-2r).

For lambda>1 it can exceed T, so it cannot be discarded as a lower-order error. Keeping the weight transform meromorphically continued on the original line encodes it; writing a convergent time-integral on a line to the left requires displaying it. This is a contour/weight adaptation requirement, not a change to V1's arithmetic benchmark. The benchmark already contains the corresponding low-time mass.

The source's positive-time presentation, its factor of 2 in the off-diagonal, and its formal Mellin identity are therefore not a substitute for the exact two-orientation and residue audit under V1.

## 6. Prior-art search and evidence limits

On 16 October 2026 a bounded fresh web search was made for the exact Möbius/ratios/band-limited combination and for CK ratios/correlations follow-ons. Broad combined-keyword queries produced many irrelevant hits and are not absence evidence. Targeted title queries returned the two CK papers, the formal Keating–Smith inversion, and unrelated numerator-only moment results. The final CK2016 journal PDF was then retrieved directly from its author-hosted AIM URL and inspected. Its public metadata is recorded separately; copied source bytes remain private.

No exact all-conditions prior theorem was identified in the inspected primary sources. That statement neither certifies novelty nor rules out a standard unpublished adaptation. The arithmetic-identity discrepancy and the weight pole must be repaired explicitly before any final acceptance of V1.
