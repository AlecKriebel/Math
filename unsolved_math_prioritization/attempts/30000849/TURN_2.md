# Turn 2: exact transport and a conditional corrected scaling theorem

One reviewed turn has refuted the source's literal normalization. The continuing
physical problem is not thereby solved. This second substantive turn derives an
exact transport formula and the consequent normalization **from the equations**.
It does not assign an unverified corrected statement to the source authors.

## 1. Source-supported model and the remaining problem

The primary input is da Costa's2015 survey, equation(123), internal p.57:

    c_1'=J(t)-c_1^2-c_1 sum_{j>=1}j^p c_j,
    c_j'=(j-1)^p c_1 c_{j-1}-j^p c_1 c_j, j>=2, p<1.       (1)

The original OWR pp.2754–2756 and the survey pp.58–60 introduce the monomer
clock by integrating c_1. The rigorous constant-rate result identifies a power
law for the monomer concentration in that clock before deriving the profile.
The variable-rate paragraph supplies no proof of that nonlinear step. The
unpublished2007/2008 notes were not located; searches did not recover a source
that resolves their intended corrected normalization. No such theorem is assumed.

This turn treats solutions with zero initial concentrations for j>=2 and a
positive monomer concentration at positive physical times. It is already an
interesting subproblem, but it does not cover the original general initial-data
class. Assume the monomer clock tau(t)=integral_0^t c_1(u)du tends to infinity.
Set f(tau)=c_1(t(tau)) and g_j(tau)=j^p c_j(t(tau)). For j>=2, direct
application of the chain rule to(1) gives

    g_j'=j^p(g_{j-1}-g_j),     g_1=f.                       (2)

These g_j are **new weighted variables**. They are not the source's unweighted
c-tilde_j. This distinction is essential to the normalization calculation.

## 2. Exact exponential-sum representation

For every k>=2 let E_k be independent exponential random variables of rate k^p,
so mean b_k=k^(-p). Put S_j=E_2+...+E_j. Then

    g_j(tau)=E[f(tau-S_j) 1_{S_j<=tau}].                  (3)

This identity needs no asymptotic approximation. For j=2 it is the ordinary
variation-of-constants formula with the density 2^p exp(-2^p u). Repeated
substitution in(2), Tonelli for a nonnegative f, and convolution of the
exponential densities prove(3) by induction. Each formula is a finite
convolution, so there is no limit in j hidden in its derivation. Equivalently,
for a Laplace-transformable f, its transfer factor is the exact product

    product_{k=2}^j k^p/(z+k^p).                            (4)

The probability notation describes that finite convolution. It does not add
randomness to the deterministic physical model.

## 3. A concentration estimate strong enough for power-law amplitudes

Let m_j=sum_{k=2}^j b_k, v_j=sum_{k=2}^j b_k^2, and
B_j=max_{2<=k<=j}b_k. For |lambda|B_j<=1/2, independence and the elementary
power series for -log(1-x) give

    log E exp(lambda(S_j-m_j))
       =sum_k[-log(1-lambda b_k)-lambda b_k]
       <=lambda^2 v_j.                                   (5)

Indeed the absolute tail of the logarithm series is at most
x^2/[2(1-|x|)]<=x^2. Applying the exponential Markov inequality with either
sign of lambda and choosing lambda=min(x/(2v_j),1/(2B_j)) gives

    P(|S_j-m_j|>=x)
       <=2 exp(-min(x^2/(4v_j),x/(4B_j))).                (6)

For p<1, integral comparison of power sums yields

    m_j ~ j^(1-p)/(1-p),
    v_j=O(j^(1-2p)) if p<1/2,
         O(log j) if p=1/2,
         O(1) if 1/2<p<1.

Also B_j=j^(-p) for p<0 and B_j=2^(-p) for p>=0. Consequently for any
fixed epsilon>0 and any tau comparable to j^(1-p), there are constants
c,C>0 such that, for all sufficiently large j,

    P(|S_j-m_j|>=epsilon tau)
       <=C exp(-c j^gamma),  gamma=min(1,1-p)>0.          (7)

At p=1/2, the first exponent is order j/log j and dominates j^(1/2),
so the same conclusion holds. This stretched-exponential estimate, rather
than a bare variance estimate, makes all polynomial amplitude errors harmless.

## 4. Conditional off-front limit

**Theorem.** Fix p<1. Let f be nonnegative, continuous and bounded on compact
subintervals of[0,infinity), with

    f(tau) ~ C tau^(-r),       C>0, r real.                 (8)

Define g_j by(3), c-tilde_j=j^(-p)g_j, and

    sigma=[(1-p)tau]^(1/(1-p)),
    q=p+(1-p)r,       A=1/[C(1-p)^r].                     (9)

As j and tau tend to infinity with j/sigma=eta fixed and eta!=1,

    A sigma^q c-tilde_j(tau)
      -> eta^(-p)(1-eta^(1-p))^(-r),  0<eta<1,
      -> 0,                                    eta>1.    (10)

Proof. Since j/sigma=eta, the power-sum estimate gives
m_j/tau -> eta^(1-p). Suppose first0<eta<1. Fix a small epsilon>0 with
2epsilon<1-eta^(1-p). On the event |S_j-m_j|<=epsilon tau, the quantity
(tau-S_j)/tau stays in a compact subinterval of(0,infinity), and (8)
holds uniformly there: the relative error bound in the definition of an
ordinary asymptotic equivalence applies for every argument above a fixed
multiple of tau. Thus f(tau-S_j)/(C tau^(-r)) is squeezed between the
nearby values of (1-S_j/tau)^(-r), up to a vanishing relative error.
Equation(7) makes the probability of the complementary event tend to zero.

To discard that event in **expectation**, not merely probability, note that
(8) and local boundedness imply
sup_{0<=u<=tau} f(u)<=C_0(1+tau)^max(0,-r). After division by C tau^(-r)
this is at most a fixed polynomial in tau. Equation(7) beats that polynomial,
because tau is comparable to j^(1-p). First let j tend to infinity and then
let epsilon tend to zero. The result is

    g_j(tau)/(C tau^(-r)) -> (1-eta^(1-p))^(-r).

If eta>1, m_j-tau is at least a fixed positive multiple of tau for large j.
The event S_j<=tau in(3) is then a lower-deviation event controlled by(7).
The same polynomial bound on f makes g_j(tau)/(C tau^(-r)) tend to zero.
Finally j^p=(eta sigma)^p and tau^r=sigma^((1-p)r)/(1-p)^r give(10).
The same proof works along any sequence j/sigma tending to eta!=1, since
only the limit m_j/tau is used. This also permits the asymptotically equivalent
physical size scale in Section5. This proves the theorem for every real r, as a statement about the prescribed
boundary forcing f. It proves no nonlinear asymptotic assumption(8).

## 5. Physical time and the source exponents

For a global physical solution satisfying(8) with r>-1, dt/dtau=1/f(tau)
can be integrated using elementary upper/lower power bounds:

    t ~ tau^(r+1)/[C(r+1)].                               (11)

Thus sigma(t) is asymptotic to K t^s, where

    s=1/[(1-p)(r+1)],
    K=(1-p)^(1/(1-p)) [C(r+1)]^s.                         (12)

Take the report's value r=r_p=[1-omega(1-p)]/[(omega+2)(1-p)]. It satisfies
r_p+1=(3-2p)/[(omega+2)(1-p)]>0 in the reported parameter range. Then(12)
gives exactly its physical **size exponent** s=(omega+2)/(3-2p), while
(9) gives the different physical **concentration amplitude**

    q=p+(1-p)r_p=[1-omega+2p(omega+1)]/(omega+2).           (13)

For p=1/4,omega=0 this is q=3/4. It is derived from the actual weighted
transport equation and monomer-clock conversion, rather than selected only
because it passes a mass-dimension test. When p=0 it reduces to q=r_0 and
recovers the known constant-rate normalization.

For the value(13), elementary algebra gives s(2-q)=omega+1. This compatibility
with monomer mass input does not prove tightness or justify passage to the mass
integral. In particular a front-singular profile requires a separate audit.
We do not determine the unknown constant C or claim (8) from this identity.

## 6. Exact gap and disposition after two turns

The theorem rigorously solves the transport part **conditional** on the
monomer-clock asymptotic and zero initial higher clusters. The hard nonlinear
problem remains: prove or refute(8), its exponent and constant, and the required
clock growth for the coupled monomer equation, with the correct input regimes
and initial-data hypotheses. The original polynomial-tail class has not been
handled here, and no claim about eta=1 is made.

The previously reviewed source correction remains unchanged. It is insufficient
for a complete resolution of this continuing physical target. Two substantive
author turns are now used; three remain. The exact checks supplement, and do
not replace, the elementary concentration and conditional asymptotic proof.
