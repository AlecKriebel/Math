# Formulation gate: Möbius randomness, ratios, and primes

Historical unamended specification. The accepted theorem in audit/INDEPENDENT_ACCEPTANCE_AND_COMBINED_THEOREM.md supersedes its parameter range by 0<psi<=phi<1 and requires the corrected displaced B factor and explicit w(0) endpoint. This preserved specification is not certified unchanged.

## 1. Identity and source completeness

The authoritative queue position is **1795**, numeric ID **20000699**, problem number **AIM-ANALYTIC_NUMBER_THEORY-0063**. The imported title is “A quantitative Möbius–ratios–prime bridge.” It is a title for the imported progress, not the original problem's full wording.

The canonical source is [AIM, Moments of zeta and correlations of divisor sums, Section 6, Problem 6.2](http://aimpl.org/zetamoments/6/), attributed on the live page to **H. Iwaniec**. It asks for a Möbius-randomness input producing the surrounding calculations and, in the reverse direction, a way to recover information about primes from ratios-type formulas. Problem 6.1 supplies the Conrey–Keating context; Problem 6.3 separately asks for a prime random model producing Type II calculations. There is no attached remark on 6.2.

The complete served HTML, embedded canonical record, attribution, neighboring boundaries, and absence of remarks were checked. The embedded statement agrees byte-for-byte after JSON decoding with both pinned datasets and the desk-review statement hash. The source has an empty status field, which is not an openness certificate. Its current availability supersedes the imported report's historical July 2026 access-failure note.

Main was pinned at `4b72864f7c8b4a1cdd6cfb25979b17fad4433339`. Its QUEUE blob `b114c2268135f708499f96d8e1a71e717ce52310` lists this row queued, 0/5. Freshly retrieved catalog/state/assessments bytes match their pinned Git blobs. The catalog's rank 1786 is stale relative to QUEUE rank 1795. There is no state entry, no target directory in the untruncated 145-entry immediate attempts tree, and no target-ID PR or branch search hit. Search limitations are recorded separately; absence from these indexes does not certify absence from every remote branch.

The desk review has no readiness holds. It identifies noncircular hypotheses and adequate shift control as substantive requirements. The imported attempt is prior material, not a campaign pass.

## 2. Interpretation decision before mathematical work

The source is existential and open-ended. It does not specify rank, cutoff, weight, shift domain, arithmetic error, or the exact prime statistic. An all-rank, all-length theorem, unconditional Möbius cancellation, full microscopic zeta ratios, and individual fixed-shift Hardy–Littlewood would each be substantially stronger demands than the words alone impose.

**Proposed V1 is a precise low-rank witness to both requested arrows.** It must produce an explicit arithmetic prime-pair main term, rather than stop at a formal derivative. It concerns finite truncated ratios. Its success may be reported as a rigorous conditional answer in this declared interpretation, subject to explicit adoption of that interpretation. It must not be promoted to the unrestricted full-zeta or fixed-shift prime-pair claims. A stronger reading would require a separately declared target and is not established by this witness.

This is a proposed specification, not a theorem proved by source preparation.

## 3. Proposed target V1: quantitative two-arrow rank-one witness

### Parameters and actual objects

Fix A>0, c>0, a0>=0, and a real Schwartz function w with Fourier transform

hat w(u) = integral_R w(v) exp(2 pi i u v) dv

supported on [-A,A]. Fix 0<phi<1, psi>0, and

1 < lambda < 2,  lambda*phi < 1,  lambda*(1-psi) < 1.

Let T tend to infinity, N=floor(T^lambda), 0<=a<=a0, r=a/log N, rho=c/log N, and let D be the closed four-variable complex polydisc of radius rho about Delta_r=(r,r,r,r). Uniformity in a and every shift in D is required. No uniformity as lambda approaches one of the strict boundaries is promised.

For z=(alpha,beta,gamma,delta), use the finite divisor coefficients

I_(alpha,gamma)(n) = sum_(de=n) d^(-alpha) mu(e)e^(-gamma),
P_(alpha,gamma;N)(t) = sum_(n<=N) I_(alpha,gamma)(n)n^(-1/2-it),
R_(T,N)(z) = integral_R w(t/T) P_(alpha,gamma;N)(t) P_(beta,delta;N)(-t) dt.

The coefficient cutoff is sharp. This finite average is entire in the shifts. It is not the average of an untruncated quotient of zeta functions.

### Forward input must be arithmetic and explicit

Use the two oriented cumulative sums C^+(x,h)=sum_(n<=x) I_(alpha,gamma)(n)I_(beta,delta)(n+h), and C^- with the two coefficient pairs interchanged. A proposed hypothesis must specify these actual sums, the error constant, all endpoints, and holomorphy on a neighborhood of D. The intended baseline is

C^±(x,h) = m^±_z(x,h) + O(x^phi),  1<=h<=x^psi,  1<=x<=N,

uniformly in T,a,x,h and z in D, with a constant depending only on the fixed parameters. Hypotheses restricted to sufficiently large x must record that threshold and deal with omitted small endpoints.

The main profile is fixed independently of the desired ratios answer: the explicit Ramanujan-series profile in [Conrey–Keating 2016, Section 4, Conjecture 1](https://arxiv.org/pdf/1604.06124v2). For clarity, define e(v)=exp(2 pi i v), c_q(h)=sum_(b mod q,(b,q)=1)e(bh/q), and use their multiplicative factor F with F(1)=1,

F_(alpha,gamma)(p) = -p^(alpha-gamma)/(1-p^(-1+alpha-gamma)),
F_(alpha,gamma)(p^j) = 0 for j>=2.

Then m^+ is

[x^(1-alpha-beta)/(1-alpha-beta)]
 times [1/(zeta(1+gamma-alpha)zeta(1+delta-beta))]
 times sum_(q>=1) c_q(h)F_(alpha,gamma)(q)F_(beta,delta)(q)/q^2,

and m^- swaps the pairs. Convergence, combined holomorphy, and collision values must be proved or explicitly justified. An unspecified free profile M, or a hypothesis directly asserting the desired ratios/prime statistic, is not an acceptable replacement. If a valid refined arithmetic density is needed, it must be frozen explicitly, with the discrepancy from this source profile accounted for.

### Forward conclusion

Define H_T=floor(N(1-exp(-2 pi A/T))) and

K_h^±(x) = [x(x+h)]^(-1/2) hat w(±T log(1+h/x)/(2 pi)).

Let Q be the exact diagonal T hat w(0) sum_(n<=N) I_(alpha,gamma)(n)I_(beta,delta)(n)/n plus

T sum_(1<=h<=H_T) [integral_(1^-)^(N-h) K_h^+(x) dm^+_z(x,h)
                  + integral_(1^-)^(N-h) K_h^-(x) dm^-_z(x,h)].

Prove R=Q+O(N^phi) uniformly on D, or a fully explicit comparably useful bound that remains o(T/(log N)^2). Establish the correspondence of this arithmetic main functional with the zero/one-swap calculation of the CK source in the declared range, including every kernel-replacement or Mellin-contour error. Merely labeling Q a ratios main term is insufficient. The original source's GRH assumption on its arithmetic identity must be retained whenever that identity is imported, unless separately removed by proof.

### Reverse conclusion and a concrete prime endpoint

Independently of how a uniform estimate R=Q+E was obtained, prove the resulting asymptotic for

V_(Lambda,r)(T,N;w) = integral_R w(t/T) |sum_(n<=N) Lambda(n)n^(-1/2-r-it)|^2 dt,

with differentiated error bounded in terms of sup_D|E| and the explicit radius rho. Under the forward estimate, the desired scale is O(N^phi rho^(-2))=o(T).

The prime main term must be evaluated arithmetically. The prescribed benchmark is the exact diagonal

T hat w(0) sum_(n<=N) Lambda(n)^2/n^(1+2r)

plus the corresponding h-sum of the known Hardy–Littlewood singular series

S(h) = product_p [(1-nu_p(h)/p)/(1-1/p)^2],
nu_p(h) = number of residue classes among {0,-h} mod p,

against the displayed kernels and the density x^(-2r). Any difference between this benchmark and an alternative x^(-r)(x+h)^(-r) convention must be bounded, not silently discarded. This is an explicitly specified *smoothed aggregate* of prime-power pair correlations. An unevaluated derivative of an unknown Q does not meet the target; neither does an assertion of Hardy–Littlewood for every fixed h. The four numerator/denominator derivative sign identities from the imported report are consistency checks, not a substitute for this endpoint.

## 4. Acceptance and stopping conditions

Success for V1 requires both arrows, the explicit profile, actual hypothesis ranges, a nonempty admissible length interval, complex-uniform error control, collision holomorphy, and an evaluated prime-pair main term with o(T) aggregate error. All use of GRH or another conjecture must be visible in the theorem headline. The arithmetic conjecture itself need not be proved: the source asks for a version of randomness that would justify calculations.

A standard conditional deduction may meet this witness while being entirely prior art. Credit CK and the earlier differentiation/long-polynomial methods; novelty is a separate question. If an already-published theorem exactly covers all accepted conditions, report a credited prior resolution rather than reproduce it as new research.

A result for arbitrary unspecified M, real shifts alone, the absolutely convergent half-plane alone, just one direction, or formal unsummable Euler factors is incomplete. Any substantive baseline verification, repair, proof, extension, or counterexample belongs to the normal five-pass budget. No such work has begun here.

Preparation disposition: **SOURCE_COMPLETE; HISTORICAL_PROPOSED_V1_BEFORE_ADOPTION; 0 mathematical passes; no queue changes; no publication.**
