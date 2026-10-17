# Independent acceptance and combined conditional theorem

## Decision

**ACCEPTED: complete conditional two-arrow witness in the explicitly amended V1 interpretation.** The accepted parameter range is `0<psi<=phi<1`. The original overbroad gate is retained as provenance and is not certified unchanged. The main arithmetic density, exact finite ratios object, and evaluated prime-power aggregate are unchanged.

The accepted result includes a corrected displaced one-swap factor and an indispensable whole-line `w(0)` endpoint term. It does not certify the source's literal printed s-dependent formula. No arithmetic randomness conjecture is proved. No unrestricted full-zeta, all-rank, individual fixed-shift prime-pair, or novelty claim is accepted.

The independent reviewer read the actual proof files, independently checked the source page-4 display, reconstructed the local Euler identity and low-time residue, independently proved the parameter obstruction, and reran all four available control scripts. Component hashes and byte counts are frozen in `FROZEN_REVIEW_MANIFEST.json`; this decision applies to those bytes.

## 1. Combined theorem: arithmetic hypothesis and exact objects

Fix `A,c>0`, `a0>=0`, a real Schwartz function `w` with

hat w(u) = integral_R w(v) exp(2 pi i u v) dv,
support(hat w) subset [-A,A],

and constants

0 < psi <= phi < 1,
1 < lambda < min(2,1/phi,1/(1-psi)).

For sufficiently large real T, put

N=floor(T^lambda), L=log N, 0<=a<=a0, r=a/L, rho=c/L,
D={z=(alpha,beta,gamma,delta): every coordinate is within rho of r}.

Every constant and error below is uniform in `a` and `z in D`; constants may depend on the fixed parameters, w, and the arithmetic hypothesis constant. No uniformity at the strict lambda boundaries is asserted. The stronger summatory profile estimate in the reviewed final comparison file is used below.

Define the finite divisor coefficients and polynomials

I_(alpha,gamma)(n)=sum_(de=n) d^(-alpha) mu(e)e^(-gamma),
P_(alpha,gamma;N)(t)=sum_(n<=N) I_(alpha,gamma)(n)n^(-1/2-it),
R_(T,N)(z)=integral_R w(t/T)P_(alpha,gamma;N)(t)P_(beta,delta;N)(-t)dt.

Define the actual oriented cumulative sums, with inclusive integer endpoints,

C_z^+(x,h)=sum_(n<=x) I_(alpha,gamma)(n)I_(beta,delta)(n+h),
C_z^-(x,h)=sum_(n<=x) I_(beta,delta)(n)I_(alpha,gamma)(n+h).

The coefficient at n+h is not independently cut off in these hypothesis sums. In the moment calculation they are used only up to x=N-h.

Fix the arithmetic profile independently of R. For squarefree q use the multiplicative F given by

F_(alpha,gamma)(1)=1,
F_(alpha,gamma)(p)=-p^(alpha-gamma)/(1-p^(-1+alpha-gamma)),
F_(alpha,gamma)(p^j)=0 for j>=2,
c_q(h)=sum_(b mod q,(b,q)=1) exp(2 pi i b h/q).

Write `d=alpha+beta`, `u=gamma-alpha`, `v=delta-beta`, `G(u)=1/zeta(1+u)`, with `G(0)=0`, and

D_z(h)=G(u)G(v) sum_(q>=1) c_q(h)F_(alpha,gamma)(q)F_(beta,delta)(q)/q^2,
m_z(x,h)=D_z(h)x^(1-d)/(1-d).

The squarefree-q series converges absolutely and locally normally near D for every fixed h. The combined expression, including every collision, is holomorphic there. The two oriented main profiles coincide, although the two actual cumulative sums need not.

**Explicit arithmetic hypothesis H_CK:** there are constants `C_H<infinity` and `T0` such that, for all `T>=T0`, all `a in [0,a0]`, all `z in D`, every real `1<=x<=N`, and every integer `1<=h<=x^psi`,

|C_z^+(x,h)-m_z(x,h)| <= C_H x^phi,
|C_z^-(x,h)-m_z(x,h)| <= C_H x^phi.

The proof also allows the same statement only for `x>=x0`, for any fixed specified x0>=1, since all nonzero kernels eventually lie above x0. This is an optional explicit threshold variant, not an unstated omission. H_CK is the sole unproved input to the theorem below. It is an actual arithmetic correlation hypothesis, not a free main profile or an assumption of the desired ratios/prime conclusion.

## 2. First arrow: sharp finite-polynomial ratios and its evaluated one-swap correspondence

Put

H=floor(N(1-exp(-2 pi A/T))),
K_h^+(x)=[x(x+h)]^(-1/2) hat w(T log(1+h/x)/(2 pi)),
K_h^-(x)=[x(x+h)]^(-1/2) hat w(-T log(1+h/x)/(2 pi)).

Let Z be the exact diagonal and Q the sharp arithmetic functional:

Z_z=T hat w(0) sum_(n<=N) I_(alpha,gamma)(n)I_(beta,delta)(n)/n,

Q_z=Z_z+T sum_(h=1)^H D_z(h)
              integral_1^(N-h) x^(-d)(K_h^+(x)+K_h^-(x))dx.

This is the gate's Stieltjes main functional with its continuous profile. Any profile convention creating an atom at 1 gives the same result for large T because the Fourier kernel is zero there.

Under H_CK,

sup_D |R_z-Q_z| <= C N^phi = o(T/L^2).                 (A)

The entire sharp coefficient cutoff, exact logarithmic Fourier kernel, floor in H, equality cases, and both orientations are retained in (A).

For the explicit corrected zero/one-swap correspondence, define

H_w(k)=integral_R w(t)|t|^(-k)dt  (0<Re k<1),
J_z(k)=sum_(h>=1)D_z(h)h^(-k)   (initially Re k>1),

V_z(k)=product_p [1+(p^(1-k)-1)
 p^(-2-u-v)/((1-p^(-1-u))(1-p^(-1-v)))].

Then `J_z(k)=G(u)G(v)zeta(k)V_z(k)`, continued meromorphically through `Re k>=1/2`. Its sole possible pole there is k=1, with residue G(u)G(v).

For the rank-one Rankin-Selberg function

B_(a,b,c,e)(s)=sum_(n>=1)I_(a,c)(n)I_(b,e)(n)n^(-s)

initially in its ordinary absolute-convergence half-plane, let

B_z^*(k)=B_(-beta,beta-k,gamma+k-d,delta)(1)
        =zeta(1-k)G(u)G(v)V_z(k).

The second expression specifies its combined meromorphic continuation on the required contour. If s=k-d, its shifts are exactly

B_(-beta,-alpha-s,gamma+s,delta)(1).

This is the corrected displacement, not the printed `B_(-beta,-alpha,gamma,delta)(1+s)`.

Define the endpoint and one-swap functional

E_z=2 pi w(0) N^(1-d)G(u)G(v)/(1-d),

S_z=T N^(-d)/(2 pi i) integral_(Re k=1/2)
       (2 pi N/T)^k H_w(k)B_z^*(k)/(k-d) dk.

The k integral after the t-Mellin transform is absolutely convergent. An equivalent expression placing the t integral outside must use the finite-height, t-integrated convention proved in the Euler note; absolute convergence of the raw double integral is not asserted.

Uniformly on D,

Q_z=Z_z+E_z+S_z+O(N/(T L^2)),                            (B)

and hence

R_z=Z_z+E_z+S_z+O(N^phi).

For the last absorption, psi<=phi and lambda(1-psi)<1 imply lambda(1-phi)<1, so N/(T L^2)=o(N^phi). Both errors are o(T/L^2). The zero-swap Z remains the exact finite diagonal; its optional Perron representation uses cutoff N+1/2 or the corresponding exact half-weight correction. All functions in (B), combined as specified, are holomorphic on a neighborhood of D.

Formula (B) is a derived correspondence, not a relabeling of Q. The sharp-to-linear comparison costs the displayed O(N/(T L^2)); after two shift derivatives its cost is O(N/T)=o(T). The following Mellin step is exact: its contour moves from Re k=2 to Re k=1/2, crosses only k=1, and gives precisely E_z. The proved vertical and horizontal tails tend to zero with explicit polynomial-height bounds. The whole real line and w(0) are retained. In particular E_z cannot generally be absorbed in the error when lambda>1.

No GRH is used in (A) or (B): the prescribed-density Euler identity was independently proved from convergent products and the zeta functional equation. This does not remove GRH from CK's separate additive-twist pole-extraction interpretation, which is not imported in this theorem. If that additional identification is asserted, its GRH assumption must be stated.

## 3. Second arrow: evaluated aggregate prime-power statistic

Independently of H_CK, if the same specific Q obeys

sup_D |R_z-Q_z| <= epsilon(T,N),

then the mixed Cauchy estimate gives the exact error bound

|V_(Lambda,r)(T,N;w)-B_r(T,N;w)| <= epsilon(T,N)/rho^2,   (C)

where

V_(Lambda,r)=integral_R w(t/T)
              |sum_(n<=N) Lambda(n)n^(-1/2-r-it)|^2 dt,

B_r=T hat w(0) sum_(n<=N) Lambda(n)^2/n^(1+2r)
    +T sum_(h=1)^H S(h) integral_1^(N-h)
                       x^(-2r)(K_h^+(x)+K_h^-(x))dx,

S(h)=product_p [(1-nu_p(h)/p)/(1-1/p)^2],
nu_p(h)=number of residue classes in {0,-h} modulo p.

This is an evaluated arithmetic main term. Equivalently,

S(h)=0 for h odd,
S(h)=2 product_(p>2)(1-1/(p-1)^2)
       product_(p|h,p>2)(p-1)/(p-2) for h even.

The singular series depends only on the prime divisors of h; all prime powers in the moment coefficients are preserved by Lambda. Its absolute Ramanujan series at each h is `sum_q mu(q)^2 c_q(h)/phi(q)^2`.

Under H_CK, (A) and (C) give

V_(Lambda,r)=B_r+O(c^(-2)N^phi L^2)=B_r+o(T),           (D)

uniformly in a. The four signed identities are

partial_alpha partial_beta R = partial_gamma partial_delta R = V_(Lambda,r),
partial_alpha partial_delta R = partial_gamma partial_beta R = -V_(Lambda,r)

at Delta_r. They follow from the exact finite identities `partial_alpha I=-Lambda(n)n^(-r)` and `partial_gamma I=+Lambda(n)n^(-r)` at pair collision. The main term in (D) follows because both derivatives hit the two simple reciprocal-zeta zeros, leaving exactly S(h)x^(-2r).

If the off-diagonal density x^(-2r) is instead written as x^(-r)(x+h)^(-r), leaving the diagonal unchanged, the difference is explicitly at most

2T ||hat w||_infinity r (exp(2 pi A/T)-1) H
 =O(N/(T log N))=o(T).

The proof uses the elementary bound `sum_(h<=H)S(h)<=H`. The difference vanishes identically when r=0. Thus the density convention is accounted for, not silently changed.

The reverse theorem establishes this smoothed aggregate. It does not invert a single ratios average to recover individual gaps or claim a full-zeta ratios formula.

## 4. Independent acceptance checks

1. **Hypothesis and nonvacuity:** actual sums, a fixed profile, uniform constants, all real x endpoints and integer h ranges are present. The explicitly adopted correction psi<=phi is necessary for this density; the obstruction and its proof are recorded in `INTERPRETATION_AMENDMENTS.md`. The admissible example (phi,psi,lambda)=(3/4,1/4,6/5) passes every strict condition. This does not prove the remaining H_CK.
2. **Sharp forward proof:** the exact support gives x>=h/(exp(2 pi A/T)-1), hence the exact floor in H. Fourier flatness handles equality and Stieltjes atoms. The hypothesis range covers every nonzero kernel. Summation by parts gives O((Th)^(phi-1)) per gap and O(N^phi) after summation. Explicit constants and the x0 threshold are supplied.
3. **Complex uniformity and collisions:** the normal squarefree-q product and local reciprocal-zeta expansion prove holomorphy on a neighborhood of the closed polydisc. No full-zeta zero-avoidance is smuggled into the finite argument. Cauchy costs exactly rho^(-2).
4. **Main-functional correspondence:** the sharp-to-linear replacement and cutoff strips are explicitly bounded; normal Euler products identify the displaced B factor; the Mellin contour and every crossed pole are accounted for. The zero-swap retains an exact sharp diagonal. Real non-even w is treated through both orientations. The ordinary t-Mellin strip and finite-height interpretation prevent the invalid Fubini step found during review.
5. **Source discrepancy:** the arXiv page-4 display was visually checked. At all four zero shifts the printed swapped B equals 1 and introduces an extra order-T Perron contribution, while the actual polynomial is identically 1 and its off-diagonal is zero. The corrected displacement passes independent local algebra. The endpoint residue is independently reproduced from `M_W(1)=w(0)` and `Res_(k=1)J=G(u)G(v)`.
6. **Prime endpoint:** all four derivative signs, exact diagonal, evaluated singular series, odd-gap obstruction, prime powers, aggregate scope, and the alternative-density error were checked independently.
7. **Controls:** all scripts in `exact`, `reverse`, `euler`, and `audit` were executed successfully. The independent audit script separately checked divisor/logarithm identities through n=2000, exact rational Hardy-Littlewood local factors, and the corrected-vs-printed Euler factor. These finite controls supplement, and do not replace, the infinite convergence and contour proofs.
8. **Attribution and claims:** the method and coefficient profile are credited to Conrey–Keating; uniform ratios differentiation is prior art including Conrey–Snaith. The source review found no inspected theorem covering every amended specification, but made no exhaustive literature, openness, or novelty claim.

## 5. Findings closed during review

- Original psi>phi range: rejected as inconsistent for the unchanged complex-uniform cumulative density; explicitly narrowed in the amended interpretation.
- Printed one-swap displacement: rejected as a literal identity; replaced by independently proved correct shifts.
- Arbitrary-weight low-time mass: retained as E_z; not hidden in an error or avoided by changing w.
- Complex denominator majorant in the sharp-comparison proof: an equality was corrected to the required inequality.
- Raw t/k double-integral Fubini claim: removed; finite-height integrated convention and absolutely convergent combined Mellin integral are now explicit.
- Shifted Mellin variable in Psi_d: explicitly stated, removing a transform-notation ambiguity.

There are no remaining mathematical blockers to this amended conditional witness in the frozen reviewed bundle. Proof of H_CK, an unrestricted full-zeta result, inversion to individual gaps, and a novelty determination remain outside the accepted theorem.

## References

- B. Conrey and J. P. Keating, *Pair correlation and twin primes revisited*, https://arxiv.org/pdf/1604.06124v2 ; final published version https://aimath.org/~kaur/publications/92.pdf .
- B. Conrey and J. P. Keating, *Averages of ratios of the Riemann zeta-function and correlations of divisor sums*, https://arxiv.org/pdf/1611.09198v1 .
- B. Conrey and N. C. Snaith, *Applications of the L-functions ratios conjectures*, https://arxiv.org/pdf/math/0509480v2 .
- AIM, *Moments of zeta and correlations of divisor sums*, Section 6, Problem 6.2, http://aimpl.org/zetamoments/6/ .
