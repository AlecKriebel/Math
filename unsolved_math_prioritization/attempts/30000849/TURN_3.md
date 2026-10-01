# Turn 3: a nonlinear constant-input regime with finitely many clusters

**Unreviewed scoped theorem; original intended target remains unresolved.**
This turn treats the actual standard addition model from the primary source,
with constant input1, zero initial data and **1/2<p<1**. It proves a nonlinear
monomer asymptotic, not just a conditional transport formula. The resulting
regime differs from the report's formal exponent even after repairing its
unweighted amplitude. General input powers and general initial data are not
settled by this result.

## 1. Statement

Consider the standard equations

    c_1'=1-2c_1²-c_1 P,
    c_j'=(j-1)^p c_1c_(j-1)-j^p c_1c_j, j>=2,
    P=sum_(j>=2) j^p c_j,       c_j(0)=0.                 (1)

For every fixed p in(1/2,1), there is a global nonnegative classical
componentwise solution with total mass sum j c_j(t)=t. For every such
mass-conserving solution define tau(t)=integral_0^t c_1(s)ds. Then tau tends
to infinity and

    N_infinity:=integral_0^infinity c_1(t)²dt
              =lim_(t->infinity) sum_(j>=2)c_j(t)

exists and lies strictly between0 and infinity. The following limits hold:

    c_1(t) ~ N_infinity^(p-1) t^(-p),
    tau(t) ~ N_infinity^(p-1)t^(1-p)/(1-p),
    sigma(t):=[(1-p)tau(t)]^(1/(1-p)) ~ t/N_infinity.       (2)

With nu=p/(1-p), the off-front concentration profile is

    N_infinity sigma(t)^(2p)c_j(t)
       -> eta^(-p)(1-eta^(1-p))^(-nu), 0<eta<1,
       -> 0,                                    eta>1,   (3)

along any sequence j/sigma(t)->eta!=1. The mass-normalized measures satisfy

    (1/t) sum_(j>=2) j c_j(t) delta_(j/sigma(t))
       -> delta_1                                       (4)

weakly against bounded continuous functions. Thus the off-front profile does
not account for the leading mass; the mass concentrates at the front. There
is no claim here about pointwise concentrations on the front itself.

The standard-model source is da Costa2015, equation(123), internal p.57.
The pure-birth representation below is derived from that equation. The theorem
is an author deduction, not attributed to the unavailable unpublished notes.
No historical novelty is claimed; separate independent review is required.

## 2. Existence and exact mass, for each selected p

Use the same finite truncation construction as the first turn, now with
arbitrary fixed p in(1/2,1). The first-moment telescope is exactly

    M_n'=1-(n+1)n^p c_1 c_n <=1.

Consequently c_j<=t/j. The monomer sum tails are uniformly bounded on[0,T]
by T(L+1)^(p-1), tending to zero since p<1. Uniform coordinate derivative
bounds, Arzela-Ascoli and diagonal extraction therefore give an actual global
nonnegative componentwise C¹ solution, as written out in COUNTEREXAMPLE.md.
No mass identity is assumed in that compactness construction.

For the second moment S_n=sum j²c_j the finite identity is

    S_n'=1+2c_1 sum_(i=1)^(n-1) i^(p+1)c_i
             -(n²+1)n^p c_1c_n <=1+2t S_n,

because i^(p+1)<=i². Thus S_n is bounded on every fixed compact time interval
by the same finite H_T as in the first-turn proof. Mass tails are at most
H_T/(L+1), and the mass boundary flux is at most2T H_T n^(p-1), which tends
to zero. Passing to the full mass in the integrated finite equation gives
sum j c_j(t)=t. The strict-positivity argument from the first turn applies:
c_1(t)>0 and then c_j(t)>0 for every j and t>0.

All subsequent assertions apply to any nonnegative mass-conserving classical
solution of(1) with zero data. Uniqueness is not assumed or needed. For such a
solution, the scalar inequality c_1'<=1-2c_1² and c_1(0)=0 give

    0<c_1(t)<=1/sqrt2,     t>0.                           (5)

## 3. The clock cannot terminate at a finite value

Let M_h(t)=sum_(j>=2)j c_j(t). Differentiate only the finite sum up to n.
Dropping its nonpositive final loss and using i^p<=i gives

    (sum_(j=2)^n j c_j)' <=2c_1²+c_1 sum_(j=2)^n j c_j.

The integral inequality and then monotone convergence yield

    M_h(t)<=2 exp(tau(t)) integral_0^t c_1(s)²ds
           <=sqrt2 exp(tau(t))tau(t),                   (6)

where(5) was used in the last step. If tau had a finite limit, (5)-(6) would
bound c_1+M_h uniformly, contradicting c_1+M_h=t. Thus tau(t)->infinity.
Its inverse is C¹ for positive times. Put f(tau)=c_1(t(tau)) and
P(tau)=sum_(j>=2)j^p c_j(t(tau)). The monomer equation becomes

    f'=1/f-2f-P.                                         (7)

The function f is positive for tau>0, locally bounded through tau=0 and smooth
enough for the following differential comparisons away from0.

## 4. A first cohort forces an integrable monomer bound

Let Y_v be the pure-birth process started at2, with transition k->k+1 at
rate k^p. Its hitting time of j>=3 is

    T_j=sum_(k=2)^(j-1) E_k,    E_k independent Exp(k^p).

This process is nonexplosive. For instance its hitting-time means diverge
like j^(1-p)/(1-p), while the variance sum is bounded for p>1/2. Chebyshev
then gives P(T_j<=R)->0 for every finite R. Since T_j is increasing in j,
its limit is infinite almost surely. This argument concerns only a finite
sum at each j and its monotone limit.

Fix any tau_0>0. By positivity xi=c_2(t(tau_0))>0. Coordinatewise variation
of constants in the higher-cluster equations implies

    c_j(t(tau)) >= xi P(Y_(tau-tau_0)=j),  tau>=tau_0.     (8)

It simply follows the part of the existing2-cluster population; subsequent
births and other existing clusters add nonnegative terms. Induction on j
proves(8), so no infinite-system uniqueness is used.

For large v choose k=floor(((1-p)v/4)^(1/(1-p))). The elementary power-sum
bound E T_k <=k^(1-p)/(1-p)<=v/4 gives
P(Y_v>=k)>=3/4 by Markov's inequality. Therefore

    E Y_v^p >=(3/4)k^p >=c v^nu,   nu=p/(1-p)>1.

Summing(8) against j^p proves P(tau)>=c_0 tau^nu for large tau, with some
c_0>0 depending on the solution and the fixed cohort.

Choose K>=2/c_0 and u(tau)=K tau^(-nu). When f>=u, equation(7) gives

    f'<=1/u-P<=-(c_0/2)tau^nu.                           (9)

If f stayed above u forever after some large time, integrating(9) would
make f negative. Thus it enters below u. At every possible later upward
crossing f=u, the right side of(7) is, for sufficiently large tau, strictly
less than u'=-nu K tau^(-nu-1). An upward crossing is impossible. Consequently

    f(tau)<=K tau^(-nu) eventually.                       (10)

Since nu>1, its integral on[0,infinity) is finite. It is positive because
f>0 on every positive finite clock interval.

## 5. Exact cohort formula and growth moments

In the monomer clock the unweighted higher-cluster equations are linear:

    d c_2/dtau=f-2^p c_2,
    d c_j/dtau=(j-1)^p c_(j-1)-j^p c_j, j>=3.

Zero initial higher clusters and variation of constants give the exact formula

    c_j(t(tau))=integral_0^tau f(u) P(Y_(tau-u)=j)du.       (11)

This follows coordinatewise by induction. Summing its nonnegative terms and
using nonexplosion gives

    N(tau):=sum_(j>=2)c_j(t(tau))=integral_0^tau f(u)du.    (12)

Thus N(tau)->N_infinity in(0,infinity), with the equivalent physical expression
in Section1 because d tau=c_1dt. This proves the asserted finiteness without
assuming a monomer asymptotic.

We next need moments of Y_v. Define s(v)=[(1-p)v]^(1/(1-p)). The hitting-time
mean and variance estimates imply

    Y_v/s(v) ->1 in probability as v->infinity.           (13)

Indeed choose the integer levels just below(1-epsilon)s(v) and above
(1+epsilon)s(v). Their hitting-time means differ from v by fixed positive
fractions of v, while their variances are bounded. Chebyshev controls both
tail probabilities. Integer rounding changes neither estimate.

For expectation bounds, stop the process at level n and put
m_n(v)=E[min(Y_v,n)]. Its generator and concavity give

    m_n'(v)<=E[min(Y_v,n)^p]<=m_n(v)^p.

Since m_n(0)=2, comparison and monotone convergence yield

    E Y_v <=G(v):=[2^(1-p)+(1-p)v]^(1/(1-p)).              (14)

The same argument also justifies finiteness of the expectation before using
it. Since G(v)/s(v)->1, (13) gives E[Y_v/s(v)]->1. Nonnegativity upgrades
this to L¹ convergence: E|X-1|=EX+1-2E min(X,1), applied to X=Y_v/s(v),
and bounded convergence in probability for min(X,1) gives the result.
For0<p<1, |x^p-1|<=|x-1|^p and Jensen then imply convergence of the pth
moment as well. Hence

    E Y_v ~s(v),          E Y_v^p ~s(v)^p.                (15)

## 6. Moment asymptotics for the nonlinear solution

Set sigma(tau)=s(tau). For any fixed u, equations(15) and
s(tau-u)/s(tau)->1 give

    E Y_(tau-u)/sigma(tau) ->1,
    E Y_(tau-u)^p/sigma(tau)^p ->1.

Interpret these ratios as0 when u>tau. Equation(14) bounds the first ratio
uniformly for tau>=1 and0<=u<=tau; concavity bounds the second by
G(tau)^p/sigma(tau)^p, also uniformly bounded. The finite measure f(u)du
from(10)-(12) therefore permits dominated convergence in the exact cohort
formula(11). It follows that

    M_h(t(tau)) ~N_infinity sigma(tau),
    P(tau) ~N_infinity sigma(tau)^p.                       (16)

Since f is bounded and sigma tends to infinity, the exact mass t=f+M_h gives

    t(tau) ~N_infinity sigma(tau).

In physical time this yields

    P(t) ~D t^p,       D=N_infinity^(1-p)>0.              (17)

This deduction has not differentiated an asymptotic equivalence. It used exact
mass conservation, the cohort representation and dominated convergence.

## 7. Closing the monomer asymptotic

Write the exact physical monomer equation as

    x'=1-a(t)x,    x=c_1(t),    a(t)=P(t)+2c_1(t).

By(5) and(17), a(t)~D t^p. For any fixed epsilon in(0,1), use comparison
curves x_±(t)=(1±epsilon)/(D t^p). For sufficiently large t, the right side
1-a(t)x_+ is a negative constant bounded away from0, while x_+' tends to0.
Similarly1-a(t)x_- is a positive constant bounded away from0 while x_-'
 tends to0. Above the upper curve x decreases at a fixed positive rate;
below the lower curve it increases at a fixed positive rate. Each region
is left in finite time, and the derivative inequalities preclude re-entry
in the wrong direction. Thus x_-<=x<=x_+ eventually. Letting epsilon tend
to zero proves

    c_1(t) ~D^(-1)t^(-p)=N_infinity^(p-1)t^(-p).          (18)

Integrating this positive power law, with p<1, gives the clock asymptotic(2).
Equivalently, in the exact clock,

    f(tau) ~ C tau^(-nu),
    C=1/[N_infinity(1-p)^nu],   nu=p/(1-p).               (19)

The conditional transport theorem of Turn2 now applies with an actually
proved boundary asymptotic. Its amplitude is q=p+(1-p)nu=2p and its
constant A=1/[C(1-p)^nu]=N_infinity. This proves(3).

Finally the L¹ convergence following(15), combined with bounded continuous
test functions, gives
E[(Y_v/s(v))phi(Y_v/s(v))]->phi(1). The bound(14) again permits dominated
convergence over the finite cohort measure f(u)du. Dividing by the exact mass
asymptotic in(16) proves(4). This is weak convergence of mass measures;
it does not assert an unproved uniform density estimate near eta=1.

## 8. Relation to the report and remaining scope

At constant input the report's monomer-clock candidate is r_p=1/[2(1-p)].
For p>1/2 this differs from the proved nu=p/(1-p). For example p=3/4 gives
nu=3 instead of2, linear physical size growth instead of t^(4/3), and the
bulk amplitude2p=3/2. Thus merely repairing the missing conversion in the
unweighted amplitude cannot salvage the report's entire parameter range.
The difference is supported by actual nonlinear solutions and their moment
asymptotics, not by the printed birth-coefficient typo.

The bulk profile in(3) has a nonintegrable front singularity. This is compatible
with finite physical mass because its bulk scale sigma^(2-2p) is sublinear in
the mass scale t, and the leading mass appears in the weak front atom(4).
Integrating that bulk profile all the way to the front would be invalid.

No conclusion is claimed for p<=1/2, nonconstant power input, or the full
polynomial-tail initial-data class in the original source. The proof does not
assert uniqueness, an explicit value for N_infinity, a front pointwise profile,
or convergence for every hypothesized correction of the intended problem.
The original target remains unresolved after3/5 substantive turns.
