# Turn5: a critical logarithmic regime and finite-support initial data

**Fifth and final substantive author turn. Original intended physical target
remains unsolved5/5.** The new scoped results are unreviewed until the full final
audit. This turn resolves the critical constant-input case p=1/2 for zero data,
then extends the proved regimes to finite-support initial data. It does not
claim the entire critical line, the subcritical region or the general tail class.

## 1. Critical theorem

Take the standard addition equations with p=1/2, input alpha>0 constant, and
zero initial data. There exists a global mass-conserving solution; the arguments
below apply to every such nonnegative classical solution. Define

    tau(t)=integral_0^t c_1(s)ds,
    f(tau)=c_1(t(tau)),
    N(tau)=sum_(j>=2)c_j(t(tau)),
    sigma(tau)=tau²/4.

Then tau and N both tend to infinity, and

    N(tau) ~2 sqrt(alpha log tau),
    f(tau) ~sqrt(alpha)/(tau sqrt(log tau)),
    t(tau) ~tau² sqrt(log tau)/(2 sqrt(alpha)).            (1)

Equivalently, in physical time,

    tau(t) ~2^(3/4)alpha^(1/4)t^(1/2)(log t)^(-1/4),
    c_1(t) ~2^(-1/4)alpha^(1/4)t^(-1/2)(log t)^(-1/4),
    N(t) ~sqrt(2alpha log t),
    sigma(t) ~sqrt(alpha/2) t/sqrt(log t).                 (2)

Off the front, along any sequence j/sigma(t)->eta!=1,

    t c_j(t) -> eta^(-1/2)(1-sqrt(eta))^(-1), 0<eta<1,
    t c_j(t) -> 0,                              eta>1.    (3)

Both cluster-count measures normalized by N and mass measures normalized by
alpha t converge weakly to a point mass at eta=1. This does not describe the
pointwise shape inside the front layer.

## 2. Existence and a borderline monomer bound

The finite-truncation proof of Turns1/3 works for p=1/2 and input alpha:
M_n<=alpha t; the weighted tails vanish as L^(-1/2); the second moment is
uniformly bounded on compact time intervals; the mass boundary flux tends
to0. Thus a genuine solution exists with M(t)=alpha t. Positivity follows
from variation of constants. The bound c_1<=sqrt(alpha/2), and the same
finite-clock contradiction as in Turn3, imply tau(t)->infinity.

The exact higher-cluster cohort formula is

    c_j(t(tau))=integral_0^tau f(u)P(Y_(tau-u)=j)du,       (4)
    N(tau)=integral_0^tau f(u)du,                         (5)

where Y starts at2 with pure-birth rates sqrt(k). Nonexplosion and the finite
moment bounds were proved for every0<p<1 in Turn4. A positive early cohort
gives P(tau):=sum_(j>=2)sqrt(j)c_j(t(tau))>=c tau eventually.
The clock monomer equation is

    f'=alpha/f-2f-P.                                     (6)

The barrier K/tau, with K sufficiently large, has strictly larger derivative
than the vector field at a late crossing, and a solution remaining above it
would have a negative derivative bounded above by -c' tau. The entry and
non-crossing argument of Turn3 consequently gives

    0<f(tau)<=C/tau eventually.                          (7)

This bound is borderline nonintegrable and alone does not determine N.

## 3. The number of clusters must diverge

Suppose to the contrary that N(tau)->N_infinity<infinity. It is positive by
(5). Pure-birth growth moments, the bound on their expectations and dominated
convergence over the finite measure f(u)du then give

    M_h(t(tau))~N_infinity tau²/4,
    P(tau)~N_infinity tau/2.                              (8)

These conditional finite-cohort implications, proved in Turns3–4, require
only0<p<1, not p>1/2. The latter restriction was used there to establish
finiteness, which is currently being assumed for contradiction.

For completeness, (6) and(8) force
f(tau)~2alpha/(N_infinity tau). Indeed the curves
2alpha(1±epsilon)/(N_infinity tau) have derivatives O(tau^(-2)); the vector
field at them differs from0 by a fixed multiple, with the appropriate sign,
of tau. The field is strictly decreasing in f. Eventual entry follows by
integrating these signed bounds, and later wrong-direction crossings are
impossible. This asymptotic makes integral f diverge, contradicting the
assumed finite limit in(5). Therefore

    N(tau)->infinity.                                    (9)

## 4. Slowly varying cohort count and moment asymptotics

Equation(7) implies that for each fixed h>0,

    |N(h tau)-N(tau)|<=C|log h|

for all sufficiently large tau (with an unimportant change of the constant
when integrating the interval in the opposite direction). By(9),

    N(h tau)/N(tau)->1.                                  (10)

This is proved directly; no Tauberian theorem is assumed.

Let s(v)=v²/4. The pure-birth moment estimates give

    E Y_v~s(v),      E sqrt(Y_v)~sqrt(s(v)),
    E Y_v<=G(v)=[sqrt2+v/2]².                            (11)

The convergence in probability used here follows from the exponential hitting
times: their mean is asymptotic to2sqrt(j), their variance is O(log j), and
the relative variance tends to0. The Jensen upper bound G then upgrades to
L¹ and square-root moment convergence as in Turn3.

Fix epsilon in(0,1). In(4), the cohorts with u<=epsilon tau have ages in
[(1-epsilon)tau,tau]. The moment asymptotics in(11) are uniform throughout
that interval for large tau, because the ordinary asymptotic equivalence
holds at every age above(1-epsilon)tau. Their total count is
N(epsilon tau)~N(tau). Their normalized mass moments are squeezed between
(1-epsilon)² and1; their normalized rate moments between1-epsilon and1.
The later cohorts have count N(tau)-N(epsilon tau)=o(N(tau)); by G they
contribute o(N(tau)sigma) to mass and o(N(tau)sqrt(sigma)) to P.
Letting epsilon decrease to0 gives

    M_h(t(tau))~N(tau)tau²/4,
    P(tau)~N(tau)tau/2.                                  (12)

Since f is bounded, the exact mass identity yields

    alpha t(tau)~N(tau)tau²/4.                           (13)

No asymptotic equivalence has been differentiated in these steps.

## 5. The coupled monomer equation fixes the logarithm

Set u_±(tau)=2alpha(1±epsilon)/(tau N(tau)). By N'=f and(7),

    u_±'=-u_±(1/tau+f/N)=O(1/(tau²N))

in absolute value, since N is bounded below by a positive constant at late
times. At u_+ the right side of(6) is a negative fixed fraction of tau N;
at u_- it is a positive fixed fraction of tau N, by(12). The negligible term
2u_± does not change these signs. Because the field alpha/f-2f-P is strictly
decreasing in f, the same entry and crossing argument yields

    f(tau)~2alpha/[tau N(tau)].                           (14)

For an interval where f stays above u_+, the derivative is bounded above
by -c tau N, forcing entry in finite time. Below u_- it is bounded below
by c tau N, also forcing entry (in particular contradicting(7) if it persisted).
At any attempted later crossing the derivative signs are stricter than those
of the comparison curves. Dependence of u_± on the actual N is harmless:
its derivative has just been estimated from the actual equality N'=f.

It follows from(5),(14) that

    (N²)'=2Nf~4alpha/tau.

Integrating upper and lower asymptotic bounds gives
N²~4alpha log tau. Equation(14) then gives the f asymptotic in(1), and(13)
gives the t asymptotic. Inverting it is legitimate through logarithms:
log t~2log tau, then substituting log tau~(log t)/2 gives all constants in(2).
The monomer formula in physical time is obtained by composing f with that
inverse, not by differentiating an asymptotic clock formula.

## 6. Off-front profile and leading mass atom

The exact weighted transport formula of Turn2 is

    sqrt(j)c_j(t(tau))=E[f(tau-S_j)1_(S_j<=tau)],

where S_j is the sum of exponentials with rates sqrt(2),...,sqrt(j).
Now f(tau)~sqrt(alpha)/(tau sqrt(log tau)). For every compact interval
of positive z values,

    f(tau z)/f(tau)->z^(-1) uniformly.

This follows immediately from the explicit power/log equivalent and
log(tau z)/log tau->1 uniformly there. Turn2's stretched-exponential
concentration controls the complement of the central event. Local boundedness
of f and1/f(tau)=O(tau sqrt(log tau)) make that tail negligible after
normalization. Thus the same argument, now with the explicit logarithm,
proves

    sqrt(j)c_j(t(tau))/f(tau)
       ->(1-sqrt(eta))^(-1), 0<eta<1,
       ->0,                         eta>1.

Since N tau f/(2alpha)->1 by(14), multiplying by
N sigma/alpha=N tau²/(4alpha) gives precisely the profile in(3).
Equation(13) permits replacing N sigma/alpha by t. This is not an assertion
that the bulk profile can be integrated across eta=1.

For the weak count and mass limits, split cohorts at epsilon tau as in
Section4. Late cohorts have negligible normalized count and mass. For old
cohorts, Y_(tau-u)/sigma lies in probability near[(1-epsilon)²,1], with
the same uniform first-moment bounds. A bounded continuous test function is
uniformly continuous on a compact neighborhood of that interval; the first
moment bounds and L¹ concentration control the complementary tails. Letting
first tau increase and then epsilon decrease to0 proves both delta_1 limits.

## 7. Extension to nonnegative finite-support initial data

The strict-regime theorem of Turn4 and the critical theorem above both extend
to arbitrary nonnegative finite-support initial data, including an arbitrary
finite initial monomer value. This is a genuine part of the fifth turn, not a
claim about all polynomial tails. Here are the extra verifications.

Let K0 bound the support, M0 be the initial mass and N0=sum_(j>=2)c_j(0).
Truncate above K0. The previous first/second-moment bounds now begin with
finite M0 and S0, giving an actual global solution with
M(t)=M0+kappa t^beta (or M0+alpha t in the critical case). The monomer bounds
hold with altered constants. Positivity and a positive early2-cluster cohort
still follow from the positive input, even if N0=0.

In the clock, add the finite initial-cohort sum to the representation:

    c_j(t(tau))=sum_(k=2)^K0 c_k(0)P(Y_tau^(k)=j)
                  +integral_0^tau f(u)P(Y_(tau-u)^(2)=j)du. (15)

Here Y^(k) starts at k. Its expectation is at most
G_k(v)=[k^(1-p)+(1-p)v]^(1/(1-p)), by the same stopped-process proof.
For any fixed k, Y_v^(k)/s(v)->1 in L¹, since omitting finitely many holding
times changes neither the mean asymptotic nor the concentration estimate.
Therefore the initial term satisfies all the required bounds with constants
depending on K0. In particular

    N(tau)=N0+integral_0^tau f(u)du.

The clock-divergence argument, the early-cohort lower bounds, and the strict
regime bootstrap are unchanged after adding finite constants. In the strict
regime N_infinity is now the total limit including N0; dominated-cohort
asymptotics and all constants in Turn4 use that total N_infinity. In the
critical case N diverges and the finite initial contribution is negligible
relative to N; the logarithmic constants in(1)-(3) are unchanged.

The initial terms also vanish in the off-front limits, rather than being
silently ignored. For fixed k and j/sigma->eta<1, the event Y_tau^(k)=j
requires the hitting time of j+1 to exceed tau, an exponentially unlikely
upper deviation. For eta>1 it requires hitting j by tau, an exponentially
unlikely lower deviation. The finite-sum concentration argument of Turn2
is unchanged on omitting a fixed initial segment. These stretched-exponential
bounds beat every power normalization and the logarithmic factor used here.
There are finitely many k. Thus the same off-front limits follow.

This extension does not cover infinite-support data with only the original
polynomial bound. Those may require different moment, tail and initial-semigroup
estimates; no reduction to finite support without an estimate is claimed.

## 8. A precise memory obstruction to an initial-data-independent size constant

In the strict regime, the proved size coefficient is kappa/N_infinity.
The limit N_infinity includes the initial higher-cluster number, so it is
at least N0. For example data c_2(0)=R, all other higher components zero,
are finite-support and satisfy every polynomial upper-bound condition for a
suitable rho. They give N_infinity>=R. Hence the leading physical size
coefficient cannot be one positive constant independent of all these data.

More explicitly, fix any proposed universal size coefficient K>0 for the
corrected strict-regime time exponent beta. Choose R>2kappa/K. Then the actual
front coefficient kappa/N_infinity is below K/2. Along j/(K t^beta)=3/4,
the ratio to the actual sigma tends to(3/4)K N_infinity/kappa>1. The proved
off-front theorem therefore gives zero after any fixed finite multiple of
the actual power normalization, whereas a proposed profile positive at3/4
with cutoff1 would require a positive limit. This rules out that particular
universal-constant formulation on the full finite-support initial class.
It does not rule out data-dependent self-similarity; indeed the strict theorem
proves it with the memory parameter N_infinity.

## 9. Final unresolved scope after five turns

The literal displayed normalization was refuted in Turn1 and independently
reviewed. The continued physical work now proves a conditional general
transport theorem, a strict nonlinear power-input finite-cluster regime, and
one critical logarithmic regime, with finite-support initial-data extensions.
These results have not supplied the full intended physical theorem.

The remaining source-target gaps include the entire d>1/2 nonlinear regime,
the rest of the critical line d=1/2, and the original general infinite
polynomial-tail initial-data class. A pointwise front-layer description is an
additional question, not a requirement of the original eta!=1 statement. The published p=0 results are
credited, not rediscovered. No blanket nonexistence of correctly normalized
self-similarity is claimed. The source's implicit constants and ambiguous
normalization cannot be silently replaced by a guessed global conjecture.

All five substantive author turns are used. The intended original status is
**unsolved5/5**, with the reviewed literal correction clearly distinguished.
No further author proof search is included after this turn. Full independent
review of the new analytic partials is required before any PR.
