# Independent proof audit: second zeta moments near sigma = 1

Date: 2026-10-21. Scope: AIM 8.1 / queue row 1862. This is an audit of narrowly specified consequences and reductions, not a resolution of the original broad question or a novelty claim.

## 1. Definitions and fixed-parameter theorem

For 3/4 < sigma < 1 put q = 2 - 2 sigma,

C(q) = (2 pi)^(1-q) zeta(q)/q,
F_sigma(X) = integral_0^X |zeta(sigma+it)|^2 dt,
E_sigma(X) = F_sigma(X) - zeta(2 sigma) X - C(q) X^q.

The decomposition is exact by definition, not an exact two-term evaluation. For fixed sigma the integration from zero is finite. At sigma = 1 it is not.

Lau (2006), Corollary 1, pp. 447-448, with definition on p. 446, proves

A_sigma(X) := integral_1^X E_sigma(v) dv = D_sigma X + O_sigma(sqrt X),
D_sigma = -2 pi zeta(2 sigma - 1).

The paper explicitly fixes sigma and allows all implied constants to depend on it. At sigma = 3/4 the error is O(sqrt X log X). These claims were checked directly against the saved paper text; the DOI request failed in this audit, so no fresh live full-paper retrieval is claimed.

Take fixed psi in C_c^2((0,infinity)), with support in [c,d], 0<c<d. For sufficiently large T all integration occurs above 1. Two integrations by parts, with all boundary terms zero, give exactly

integral psi(t/T) dE_sigma(t)
= -T^(-1) integral psi'(t/T) E_sigma(t) dt
= T^(-2) integral psi''(t/T) A_sigma(t) dt.

The affine part contributes zero because integral psi''(u) du = integral u psi''(u) du = 0. Writing A_sigma(t)=D_sigma t+H_sigma(t), the remainder is bounded by

T^(-1/2) K_sigma integral_c^d sqrt(u) |psi''(u)| du.

Hence the claimed smoothed moment is valid with absolute error O_sigma,psi(T^(-1/2)):

zeta(2 sigma) T integral psi(u)du
+ (2 pi)^(2 sigma-1) zeta(2-2 sigma) T^(2-2 sigma) integral psi(u)u^(1-2 sigma)du.

Complex weights are allowed; positivity and unit mass are unnecessary. The formula is a classical corollary of Lau, not certified new research. A moving weight, shrinking support, or varying sigma requires new estimates for the displayed constants/norms.

## 2. Endpoint normalization and scale

Use R(X)=integral_1^X |zeta(1+it)|^2dt-zeta(2)X+pi log X. The BIR 1992 estimate is

R(X)=O((log X)^(2/3)(log log X)^(1/3)).

This normalization and bound were independently checked in the saved Matsumoto 1994 exposition, p. 15. The recovered original publisher response is verification HTML, not the original PDF; this audit does not promote it to an inspected original.

For fixed 0<a<b, subtracting the two endpoint identities proves

integral_(T^a)^(T^b) |zeta(1+it)|^2dt
= zeta(2)(T^b-T^a)-pi(b-a)log T
+ O_(a,b)((log T)^(2/3)(log log T)^(1/3)).

The error is o(log T), not o(1). On [T,2T], the exact identity instead has secondary term -pi log 2 and remainder R(2T)-R(T). Isolating that constant requires this increment to be o(1); the quoted estimate does not supply it. A bounded window ratio and polynomially separated endpoints are different regimes.

If psi is continuous and nonzero at zero, its endpoint weighted moment from zero diverges: |zeta(1+it)|^2 = t^(-2)+O(1). Compact support away from zero avoids this. Changing the primitive's fixed positive lower endpoint changes a constant, which cancels in window differences and compactly supported integration by parts.

## 3. Conditional endpoint smoothing

Ivic's ICM 2010 contributed abstract, p. 82, announces

integral_1^X R(v)dv = B X + O(X/log X).

The announcement itself was checked in the saved abstract; no complete proof is certified here. If this announced estimate is taken as an input, the same integrations by parts yield

integral psi(t/T)|zeta(1+it)|^2dt
= zeta(2)T integral psi(u)du - pi integral psi(u)/u du + O_psi(1/log T).

Indeed the exact remainder equals T^(-2) integral psi''(t/T) integral_1^t R(v)dv dt. The B term disappears. Its value is irrelevant. The conclusion must remain conditional on the unverified announced input, not described as RH-conditional or as a fully audited unconditional theorem.

## 4. Transition coefficient and exact missing estimate

Fix lambda>0 and 0<a<b, let sigma_T=1-lambda/log T, q_T=2lambda/log T. The exact secondary increment equals

C(q_T)[exp(2b lambda)-exp(2a lambda)].

Using zeta(0)=-1/2 and zeta'(0)=-log(2 pi)/2 gives

(2 pi)^(1-q) zeta(q) = -pi + O(q^2),
C(q) = -pi/q + O(q).

There is NO constant term in C(q). Therefore the secondary increment is

Phi(lambda) log T + O_(a,b,lambda)(1/log T),
Phi(lambda) = -pi[exp(2b lambda)-exp(2a lambda)]/(2lambda).

Phi extends continuously to Phi(0)=-pi(b-a). For each fixed positive lambda the desired moment asymptotic with o(log T) error is equivalent, not merely implied, to

E_(sigma_T)(T^b)-E_(sigma_T)(T^a)=o(log T).

For lambda in a compact subset of (0,infinity), the analytic coefficient expansion is uniform; the moment conclusion additionally requires the uniform little-o increment bound. The case lambda=0 uses the endpoint primitive separately, since F_1 from zero is divergent.

Keep the leading term zeta(2 sigma_T)(T^b-T^a) exactly. Replacing it by zeta(2)(T^b-T^a) introduces a term asymptotic to -2lambda zeta'(2)(T^b-T^a)/log T, which is much larger than log T. Any finite Taylor truncation likewise needs an explicitly adequate error analysis.

The fixed-sigma estimate does not justify substitution of sigma_T. Nor does a uniform bound on an integral of E control the endpoint increment without additional regularity or pointwise information. Smoothing and unsmoothing are distinct tasks.

## 5. Audited fixed-X pole subtraction

Let gamma be Euler's constant, q=2(1-sigma), D_q=-2pi zeta(1-q), and for fixed X>0 define

J(X)=integral_0^X (|zeta(1+it)|^2-t^(-2))dt-1/X.

The integrand extends continuously at zero. Write zeta(1+z)=1/z+gamma+z g(z), with g analytic near zero. With z=-q/2+it, the pole-square integral is pi/q-1/X+o(1). The pole-gamma cross term integrates to -pi gamma+o(1). After these two singular terms are removed, dominated convergence applies: g and z/conjugate(z) are bounded locally, and convergence away from zero is ordinary uniform convergence. Thus

F_sigma(X)=pi/q+J(X)-pi gamma+o(1).

Using C(q)X^q=-pi/q-pi log X+O_X(q) and D_q=2pi/q-2pi gamma+O(q), one obtains

E_sigma(X)-D_q -> J(X)+pi gamma-zeta(2)X+pi log X.

The signs and constants check. This is only fixed-X convergence, with no control for X growing exponentially in 1/q. It supplies neither the transition increment nor an endpoint mean estimate. No novelty assertion follows; related limit normalizations already appear in the classical literature cited by Matsumoto.

## 6. Attribution and disposition

Primary references:
- Y.-K. Lau, Journal de Theorie des Nombres de Bordeaux 18 (2006), 445-470, DOI https://doi.org/10.5802/jtnb.553 .
- R. Balasubramanian, A. Ivic, K. Ramachandra, L'Enseignement Mathematique 38 (1992), 13-25, DOI https://doi.org/10.5169/seals-59479 .
- A. Ivic, ICM 2010 contributed abstract, printed p. 82: https://www.mathunion.org/fileadmin/IMU/ICM2010/offline/www.icm2010.in/wp-content/icmfiles/abstracts/Contributed-Abstracts-5July2010.pdf .
- A. V. Zobnin, Sbornik: Mathematics 216:4 (2025), 485-493: https://www.mathnet.ru/eng/sm10113 , DOI https://doi.org/10.4213/sm10113e .

Corroborating exposition: K. Matsumoto (1994), p. 15, https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/0886-02.pdf .

The live MathNet page independently verifies Zobnin's title, publication date (June 17, 2025), and its Laplace/Gaussian scope. Its displayed local expansion explicitly says it is nonuniform in the parameter. This audit does not independently re-prove that paper's results or upgrade them to compact-weight endpoint/transition statements. The source gate's caution about small real shifts in shifted-moment results remains essential: shifts O(1/log T) about 1/2 do not move the real part to 1.

ACCEPT: fixed-sigma smoothing as a classical consequence; polynomial-window endpoint logarithm with its stated error; analytic transition coefficient; exact increment reduction; fixed-X pole subtraction.
CONDITIONAL ONLY: endpoint compact-weight constant from the ICM mean-error announcement.
NOT ESTABLISHED: transition increment estimate; unsmoothed constant on [T,2T]; general moments or full AIM resolution; global novelty or global openness claims.

This is a mathematical audit, not a certification of novelty or resolution.

## 7. Independent review of five-route research artifact

The complete RESEARCH.md was reviewed after the preceding audit was drafted. All five routes are accepted within their stated partial scope, with the following details checked independently.

### Explicit bump countermodel

Let h(v)=(1-v^2)^2(1-7v^2) on [-1,1], zero outside. Its polynomial expansion is 1-9v^2+15v^4-7v^6, and its primitive on that interval from -1 is v(1-v^2)^3. Both endpoint primitive values are zero; h and h' vanish at both endpoints. Thus the zero extension is C^1 and has zero integral. The elementary coefficient bound gives |h'| <= 18+60+42 = 120.

Fix a,b,lambda with 0<a<b and lambda>0. Set K=1000, x_q=exp(2b lambda/q), w_q=K/q, and

E_q^*(X)=D(q)+q^(-1)h((X-x_q)/w_q).

For all sufficiently small q the support is inside [x_q/2,3x_q/2]. Its centered primitive is zero outside the support and bounded by K/q^2 within it. Because q^(-2)exp(-b lambda/q) is bounded as q decreases to zero, that centered primitive is uniformly O(sqrt X). The uncentered primitive differs from D(q)X by the integration constant -D(q); this part is only O_q(sqrt X). The research artifact correctly distinguishes these assertions.

For T_q=exp(2lambda/q), the lower point T_q^a lies outside the bump and the upper point T_q^b is its center, giving increment 1/q and ratio 1/(2lambda) to log T_q. The required little-o conclusion therefore fails in this model.

For F_q^*(X)=A(q)X+C(q)X^q+E_q^*(X), its derivative is

A(q)+N(q)X^(q-1)+(1/K)h'((X-x_q)/w_q).

For 0<q<=q_0<1/2, A(q) is bounded below by a positive constant greater than 1 and N(q) is bounded. Choose a large fixed M to make the middle term small for X>=M. The final term has magnitude at most 0.12. Thus eventual positivity holds uniformly for small q. This is a valid counterexample to an inference from primitive control plus eventual positivity, NOT a counterexample to a zeta theorem. It is not claimed to be the actual primitive from zero.

### One-sided derivative argument

For the actual error, E_q'(X)>=-M_q on a sufficiently large range follows from nonnegativity of |zeta|^2 and boundedness of the explicitly subtracted density. If G=E_q-D(q), and its primitive is bounded by K_q sqrt X, integrate G(t)>=G(X)-M_q(t-X) on [X,X+h] for an upper bound on G(X). Integrating G(t)<=G(X)+M_q(X-t) on [X-h,X] gives a lower bound. Together these yield the research artifact's

|G(X)| <= 2 K_q sqrt(X+h)/h + M_q h/2

for h<=X/2 in the valid range. Taking h comparable to X^(1/4) gives O_q(X^(1/4)), insufficient to establish logarithmic-scale increments. This is a valid information-loss illustration, not an optimal zeta bound.

### Conditional smoothed transition

The proposed quantitative hypothesis |H_q(X)|<=K q^(-m)sqrt X would indeed yield error O_(psi,lambda)(T^(-1/2)(log T)^m). The explicit density then becomes -pi exp(2lambda) integral psi(u)/u du+O_(psi,lambda)(1/log T). The first-order contribution of u^q is generally nonzero despite N'(0)=0, so the stated O(1/log T), rather than an automatic O(1/log^2 T), is correct. The hypothesis is not supplied by a fixed-q theorem.

The research artifact's coefficient-expansion remainder O(lambda^2/log T) for bounded positive lambda extending toward zero is also correct: C(q)+pi/q=O(q), while exp(2b lambda)-exp(2a lambda)=O(lambda). This does not address uniform zeta errors at lambda=0.
