# Exact sharp-cutoff transfer from the fixed CK correlation hypothesis

Row 1795 / ID 20000699. Shared research pass 1 of at most 5. This is an authored forward-transfer lemma, not a proof of the correlation hypothesis or of the CK one-swap correspondence. No GRH is used in this lemma. Any GRH qualification needed in a separate source arithmetic identity remains in force there.

## 1. Fixed parameters and the arithmetic hypothesis

Following the explicit pass-1 amendment in CONTRACT.md, fix A,c>0, a0>=0, 0<psi<=phi<1, and

    1 < lambda < 2,
    lambda phi < 1,
    lambda(1-psi) < 1.

Let w be a real Schwartz function, with

    f(u) = hat w(u) = integral_R w(v) exp(2 pi i u v) dv,
    support(f) subset [-A,A].

Let T tend to infinity, N=floor(T^lambda), 0<=a<=a0, r=a/log N, rho=c/log N, and D_T be the closed four-variable polydisc of radius rho about (r,r,r,r). All constants below are independent of T,a and z=(alpha,beta,gamma,delta) in D_T. They may depend on the fixed parameters and on w.

For every integer n>=1 define the actual finite divisor coefficient

    I_(alpha,gamma)(n) = sum_(de=n) d^(-alpha) mu(e)e^(-gamma).

For real x>=1 and positive integer h define

    C_z^+(x,h) = sum_(1<=n<=x) I_(alpha,gamma)(n) I_(beta,delta)(n+h),
    C_z^-(x,h) = sum_(1<=n<=x) I_(beta,delta)(n) I_(alpha,gamma)(n+h).

The summation endpoints are inclusive. Coefficients at n+h are not separately cut off in this definition. The average below uses C only up to x=N-h, so both coefficients there have arguments <=N.

The density is fixed before the hypothesis is stated. Put

    c_q(h) = sum_(b mod q,(b,q)=1) exp(2 pi i b h/q),
    F_(alpha,gamma)(1)=1,
    F_(alpha,gamma)(p) = -p^(alpha-gamma)/(1-p^(-1+alpha-gamma)),
    F_(alpha,gamma)(p^j)=0 for j>=2,

with F multiplicative. Set

    S_z(h) = [zeta(1+gamma-alpha) zeta(1+delta-beta)]^(-1)
             * sum_(q>=1) c_q(h) F_(alpha,gamma)(q) F_(beta,delta)(q)/q^2,

    m_z^+(x,h) = S_z(h) x^(1-alpha-beta)/(1-alpha-beta),
    m_z^-(x,h) = m_(beta,alpha,delta,gamma)^+(x,h).

Powers of positive x use the real logarithm. The paired formula actually makes m_z^-=m_z^+, but retaining both symbols records the two distinct cumulative coefficient sums. The series and the reciprocals of zeta are interpreted by their jointly holomorphic continuations through their removable collision values. Their convergence and holomorphy are elementary analytic properties of this explicit density, separately verified in the arithmetic/collision proofs; they are not an extra conjecture. For sufficiently large T, |alpha+beta|<1/2 on a neighborhood of D_T, so the antiderivative denominator causes no singularity. The formula extends m smoothly to every real x>0.

Arithmetic hypothesis H_CK(phi,psi;x0,C_H): there are fixed constants x0>=1 and C_H<infinity such that, for all sufficiently large T, every a in [0,a0], every z in D_T, every real x satisfying x0<=x<=N, and every integer h satisfying 1<=h<=x^psi,

    |C_z^+(x,h)-m_z^+(x,h)| <= C_H x^phi,
    |C_z^-(x,h)-m_z^-(x,h)| <= C_H x^phi.

The constants and threshold in T are uniform in every displayed variable. The baseline in the formulation gate is x0=1. The explicit variant x0>1 shows exactly how a fixed omitted initial segment is handled. This hypothesis concerns actual Möbius-weighted divisor correlations and a prescribed Ramanujan-series profile. It contains no ratios average, prime statistic, or freely selectable main function.

## 2. Statement

Define

    P_(alpha,gamma;N)(t) = sum_(n<=N) I_(alpha,gamma)(n) n^(-1/2-it),
    R_(T,N)(z) = integral_R w(t/T) P_(alpha,gamma;N)(t)
                                    P_(beta,delta;N)(-t) dt,

and, with B=2 pi A,

    eta = exp(B/T)-1,
    H = floor(N eta/(1+eta)) = floor(N(1-exp(-B/T))),
    L_h = h/eta,
    U_h = N-h,
    u_h(x) = T log(1+h/x)/(2 pi),
    K_h^+(x) = [x(x+h)]^(-1/2) f(u_h(x)),
    K_h^-(x) = [x(x+h)]^(-1/2) f(-u_h(x)).

Let

    Q_(T,N)(z) = T f(0) sum_(n<=N) I_(alpha,gamma)(n)I_(beta,delta)(n)/n
               + T sum_(h=1)^H [integral_(1^-)^(N-h) K_h^+(x) dm_z^+(x,h)
                                + integral_(1^-)^(N-h) K_h^-(x) dm_z^-(x,h)].

Since m is continuous at 1, its displayed Stieltjes integrals have no atom at 1 and equal the ordinary integrals with density S_z(h)x^(-alpha-beta). The actual C integrals below do include their atom at n=1.

Under H_CK, uniformly for z in D_T and 0<=a<=a0,

    R_(T,N)(z) = Q_(T,N)(z) + O(N^phi).

More explicitly, writing M0=||f||_infinity, M1=||f'||_infinity and M*=M0+A M1, if H>=1 and T is sufficiently large for the stated hypothesis and range conditions, then

    |R-Q| <= [2 C_H M*/(phi(1-phi))] T eta^(1-phi) H^phi
           <= [2 C_H M* B exp((1-phi)B/T)/(phi(1-phi))] N^phi.       (2.1)

If H=0, the identity is exact with R=Q equal to the diagonal. In particular,

    sup_(z in D_T) |R-Q| = o(T/(log N)^2).

This theorem proves the exact arithmetic main-functional transfer. Identifying Q with a Mellin zero/one-swap main expression is a further theorem, not part of this proof.

## 3. Exact Fourier expansion and sharp support

All polynomial sums are finite, so termwise integration is justified by w in L1. The stated positive-sign Fourier convention gives exactly

    R_(T,N)(z)
      = T sum_(m,n<=N) I_(alpha,gamma)(m) I_(beta,delta)(n)
                      /(mn)^(1/2) * f(T log(n/m)/(2 pi)).            (3.1)

For n=m+h the argument is +u_h(m), and for m=n+h it is -u_h(n). Thus, without any linearization of the logarithm or replacement of a sharp endpoint,

    R = diagonal
        + T sum_(h=1)^(N-1) [integral_(1^-)^(N-h) K_h^+(x) dC_z^+(x,h)
                            + integral_(1^-)^(N-h) K_h^-(x) dC_z^-(x,h)].
                                                                    (3.2)

A nonzero kernel requires log(1+h/x)<=B/T, equivalently x>=L_h. On the sharp coefficient region x<=N-h this implies

    h/eta <= N-h,
    h <= N eta/(1+eta).

Consequently all terms with h>H vanish identically. The floor in H is exact. Since N is an integer and eta/(1+eta)<1, H<=N-1.

Moreover f is C-infinity and zero outside [-A,A]. Every derivative of f vanishes at both endpoints +/-A. Therefore K_h^+ and K_h^- and all their x derivatives vanish at x=L_h, and the kernels are identically zero for 0<x<=L_h. If h=N eta/(1+eta) happens to be an integer, U_h=L_h and the entire h term is zero, including a possible discrete endpoint atom. No strict-versus-nonstrict convention changes (3.2).

## 4. The hypothesis is available on the whole nonzero support

First make T large enough that

    eta <= 1/x0,

which holds whenever T>=B/log(1+1/x0). Then L_h>=x0 for every h>=1. Both the discrete kernel and the continuous main kernel vanish on the entire omitted small-x interval. There is no small-x error to estimate, even if the cumulative error bound is not asserted there.

The corrected substantive range has 0<psi<1. Put kappa=1-lambda(1-psi)>0. At every x>=L_h and 1<=h<=H,

    h/x^psi <= eta^psi h^(1-psi)
             <= eta^psi H^(1-psi)
             <= eta N^(1-psi)/(1+eta)^(1-psi)
             <= B exp(B/T) T^(-kappa).                              (4.1)

Here N<=T^lambda and exp(B/T)-1<=B exp(B/T)/T. The last quantity is <=1 for all sufficiently large T. A concrete sufficient threshold, in addition to the x0 threshold, is

    T>=max(1, B/log 2, (2B)^(1/kappa)).

Thus H_CK applies at every x needed in the integration-by-parts estimate, including U_h when L_h<=U_h. No hypothesis is invoked outside h<=x^psi or beyond x=N.

## 5. Exact uniform first-derivative kernel estimate

Let y=h/x>=0 and G_h(x)=[x(x+h)]^(-1/2). Direct differentiation gives

    G_h'(x) = -(2x+h)/(2[x(x+h)]^(3/2)),
    u_h'(x) = -T h/(2 pi x(x+h)),

    (K_h^sigma)'(x)
      = -(2x+h) f(sigma u_h(x))/(2[x(x+h)]^(3/2))
        - sigma T h f'(sigma u_h(x))/(2 pi [x(x+h)]^(3/2)),          (5.1)

where sigma is +1 or -1.

The first coefficient obeys

    (2+y)/(2(1+y)^(3/2)) <= 1.

Whenever either f(sigma u_h) or f'(sigma u_h) is nonzero, u_h<=A. The elementary inequality y/(1+y)<=log(1+y) gives

    T y/[2 pi(1+y)^(3/2)]
       <= [T log(1+y)/(2 pi)]/(1+y)^(1/2)
       <= A.

Outside that support both function values vanish. Consequently the global bounds, valid for every x>0, h>=1 and T>0, are

    |K_h^sigma(x)| <= M0/x,
    |(K_h^sigma)'(x)| <= (M0+A M1)/x^2 = M*/x^2.                   (5.2)

In particular the derivative constant has no hidden T, h, N, shift or small-endpoint dependence.

## 6. Stieltjes integration by parts and summation

Fix h<=H and an orientation. Write E_h(x)=C_z^sigma(x,h)-m_z^sigma(x,h). On every compact subinterval of (0,infinity), C is a finite right-continuous step function and m is smooth, so E_h has bounded variation. If U_h=L_h the weighted integral is zero. Otherwise the vanished lower kernel, the inclusive upper endpoint, and Stieltjes integration by parts give

    integral_(1^-)^U_h K_h^sigma dE_h
      = K_h^sigma(U_h) E_h(U_h)
        - integral_L_h^U_h (K_h^sigma)'(x) E_h(x) dx.              (6.1)

This remains true if L_h or U_h is an integer. A possible jump at L_h is multiplied by K_h^sigma(L_h)=0. No value of E_h below L_h is used.

By Sections 4 and 5, the absolute value in (6.1) is at most

    C_H [M0 U_h^(phi-1)
          + (M*/(1-phi))(L_h^(phi-1)-U_h^(phi-1))]
      <= C_H M*/(1-phi) L_h^(phi-1).                              (6.2)

For the last inequality use M*/(1-phi)>=M0. This estimate includes the entire upper-endpoint term; no approximation of U_h by N was made.

Because 0<phi<1,

    sum_(h=1)^H h^(phi-1) <= integral_0^H t^(phi-1) dt = H^phi/phi.

Add the two orientations, multiply by the exterior T, and use L_h=h/eta to obtain the first inequality in (2.1). For its second inequality,

    T eta^(1-phi) H^phi
       <= N^phi T eta/(1+eta)^phi
       <= B exp((1-phi)B/T) N^phi.

This proves the asserted complex-uniform error bound. Its dependence on shifts is entirely through the uniform C_H in the explicit arithmetic hypothesis.

## 7. Scale, nonempty length interval and analytic status

Since N<=T^lambda and lambda phi<1,

    N^phi (log N)^2/T
       <= lambda^2 T^(lambda phi-1)(log T)^2 -> 0.

There is a nonempty admissible length interval for every 0<psi<=phi<1. Explicitly let

    L*=min(2, 1/phi, 1/(1-psi)).

Then L*>1 and every lambda in (1,L*) satisfies all required strict inequalities. For example phi=3/4, psi=1/4 and lambda=6/5 are admissible. This observation does not prove that the unproved arithmetic hypothesis holds for any pair (phi,psi).

R is entire because its coefficients are finite sums of exponentials in the shifts. Once the independently verified holomorphic collision extension of S_z(h) is inserted, Q is holomorphic on a neighborhood of D_T: its h sum is finite and its x integrals are over compact intervals, with an integrand holomorphic and locally bounded in the shifts. Thus E=R-Q is also holomorphic there. The reverse theorem may apply Cauchy on the exact radius rho=c/log N, with the mixed two-variable loss rho^(-2).

## 8. Original-range correction and audit boundaries

The Fourier/Abel calculation is a formal implication for the wider original range 0<phi<1, psi>0 under the same strict length inequalities. When psi>=1 its support-range check is simply h<=x<=x^psi, using eta<=1. However, the unchanged CK cumulative profile on the full complex polydisc is inconsistent when psi>phi, as independently established in audit/INTERPRETATION_AMENDMENTS.md. Thus the substantive theorem above adopts the explicitly adopted necessary restriction 0<psi<=phi<1. The original gate is retained only as provenance. This correction does not establish the remaining conjecture.


- The CK density is the specified one. No free profile was substituted.
- The full cumulative arithmetic hypothesis is unproved; the theorem is conditional on it.
- Sharp cutoffs N-h and the exact logarithmic Fourier kernel are preserved throughout.
- The Fourier endpoint, equality case, possible Stieltjes atoms and small-x omission are all accounted for.
- No RH or GRH enters this finite transfer. A separate CK arithmetic identity may require GRH and must retain that qualification unless independently proved without it.
- This note does not identify Q with CK's zero/one-swap formula. Kernel replacements, Mellin transformations and source arithmetic identities require their own error audit.
- No conclusion about full zeta ratios or individual fixed-h prime-pair asymptotics is claimed.
