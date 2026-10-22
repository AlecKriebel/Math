# Independent derivation: martingale inputs and the polynomial coarse scale

This is the martingale/coarse-scale audit family for PR239, problem30001321,
HEAD7f17eef77c52b2d9b2ec3ad0803c016267fa6496. It verifies the estimates
(B)–(E), the coarse consequence (G), and their two numerical uses in
PROOF.md. It is not a priority determination or acceptance of the whole
all-scale theorem. I read no historical independent review or sibling
report before this assessment. All arguments below are derived directly
from the authenticated candidate.

## 1. Hypotheses and exact object being bounded

Let p(t,x) be independent, identically distributed, with 0<p<1 almost
surely. Set q=E p, a=q(1-q), delta=E[p(1-p)] and sigma²=Var(p).
Then 0<delta<=a<=1/4 and sigma²=a-delta. These are fixed-law constants;
none is claimed uniform as the law approaches deterministic arrows.
The annealed nearest-neighbor increments are independent signs with
right-step probability q: each new time layer supplies fresh variables,
regardless of the path's previous spatial visits. Its drift is v=2q-1.

F_s comprises layers before s. Therefore mu_s and
I_s=sum_x mu_s(x)² are F_s-measurable. At any finite horizon only finitely
many sites matter. All times and time blocks used here are deterministic.
The precise coarse-scale assertion audited is: for every fixed gamma>1/4,
epsilon>0 and K>0,
P(L_(n,M)>epsilon)<=C n^(-K) uniformly over integers M>=n^gamma and
deterministic alignments, for sufficiently large n. K and gamma may affect
the constants and threshold. This is a statement uniform in each
deterministic alignment, not a simultaneous supremum over
environment-selected alignments.

## 2. Backward overlap kernel, including the exceptional site

For two replicas independent given the environment, their half-difference
D=(X-Y)/2 is integer because their positions have common parity.
At nonzero differences, two fresh environmental variables are distinct,
so the probabilities of steps +1 and -1 are both a. At zero they are
both delta. The holding probabilities are respectively 1-2a and 1-2delta.

Let u_t(d)=P_d(D_t=0). Symmetry gives u_t(-d)=u_t(d). Define
b_t(d)=u_t(d)-u_t(d+1), d>=0. Direct subtraction of the *backward*
transition equations gives

    b_(t+1)(0)=(1-2delta-a)b_t(0)+a b_t(1),
    b_(t+1)(d)=a b_t(d-1)+(1-2a)b_t(d)+a b_t(d+1), d>=1.

Every coefficient is nonnegative: in particular
1-2delta-a>=1-3a>=1/4. Initially b_0(0)=1 and all other b_0(d)=0.
Thus u_t is radially nonincreasing and 0<=u_t(d)<=u_t(0)=g_t.
This is the needed hitting-profile bound, rather than an unjustified
claim that a forward transition mass is maximized at the origin.

For completeness the return bound can be derived independently from the
candidate's displayed Green function. If rho(z) is the bounded hitting
transform from 1 to 0 for the homogeneous walk off zero, its quadratic
equation is

    az rho²-[1-(1-2a)z]rho+az=0.

First-return decomposition at zero, followed by substitution of its
smaller root, yields for 0<=z<1

    G(z)=sum_t g_t z^t
        =1 / [(1-delta/a)(1-z)
                +(delta/a)sqrt((1-z)(1-(1-4a)z))].

Since 1-(1-4a)z>=4a, G(z)<=sqrt(a)/(2delta sqrt(1-z)).
A pointwise coefficient estimate requires an extra argument; a bound on
G alone is insufficient. The chain is reversible for pi(0)=a/delta and
pi(d)=1 otherwise. Its operator P is self-adjoint on l²(pi).
The operator 2P-Id is a Markov contraction because all original holding
probabilities are >=1/2. Consequently the spectrum of P lies in [0,1],
and the spectral representation of the return probability makes g_t
nonincreasing. This remains valid for the infinite, sigma-finite
reversible measure: contraction follows from Jensen's inequality and
stationarity, without normalizing pi to a probability measure.

It follows that
g_n(1-z^(n+1))/(1-z)<=G(z). Take z=n/(n+1), n>=1, and use
z^(n+1)<=exp(-1). Then g_n<=C/sqrt(n+1), with n=0 absorbed.
This justifies the precise pointwise input used subsequently.

## 3. Conditional overlap and all occupation moments

Conditioning on F_s fixes the starting pair law mu_s tensor mu_s and
leaves every later environment layer fresh. Hence exactly

    E[I_(s+t)|F_s]
      =sum_(x,y) mu_s(x)mu_s(y) u_t((x-y)/2)
      <=g_t.

The same parity is essential to the displayed integer argument.
At t=0 the inequality is I_s<=1; no independent-in-time assertion
about the overlaps is used.

Put A_L=sum_(j=0)^(L-1)g_j<=C sqrt(L).
For V=sum_(j=0)^(L-1) I_(s+j), expand V^k and sort the k indices,
paying at most k! even when there are repetitions. In each ordered
sum, condition at the penultimate selected time. All preceding factors,
including the overlap at that time, are measurable there and nonnegative.
Summing the conditional last factor over its remaining allowed times
costs at most A_L by the previous display, including time gap zero.
Repeat this elimination. This gives

    E[V^k|F_s]<=k! A_L^k.

The final k=1 step is exactly the conditional first-moment bound above.
Repeating equal indices does not require I_s to be independent of itself:
the last conditional time-zero factor is bounded by g_0=1.
For every fixed eta>0, Markov gives
P(V>N^eta sqrt(L))<=k! C^k N^(-k eta).
For each desired K choose a *fixed* sufficiently large k.
The event being bounded does not depend on that choice of k.
The constants are not uniform over k, and no such uniformity is needed.

## 4. Layer martingale and joint-event exponential inequality

For deterministic f and a terminal horizon n,
M_s=mu_s(T_(n-s)f) is the environmental exposure martingale.
Its increment is exactly

    D_s=sum_x mu_s(x)(p(s,x)-q)
          [T_(n-s-1)f(x+1)-T_(n-s-1)f(x-1)].

Conditional on F_s, the environmental variables in this sum are
independent and centered. Thus

    E[D_s²|F_s]
      =sigma² sum_x mu_s(x)² [gradient_s f(x)]²,
    |D_s|<=sup_x |gradient_s f(x)|.

These formulas distinguish a conditional variance from its expectation.
For a 1/r-Lipschitz f, the averaged translation semigroup preserves that
Lipschitz constant, so the last supremum is <=2/r and the predictable
variation is <=C r^(-2) sum_s I_s, exactly as in (D).

For the scalar exponential bound, let |D_j|<=b and
Q=sum_j E[D_j²|F_(j-1)]. When lambda b<=1, the elementary series bound
exp(x)<=1+x+x² for |x|<=1 shows that
exp(lambda sum_(i<=j)D_i-lambda² Q_j) is a nonnegative supermartingale
of expectation at most one. On the *joint event*
{sum D_j>=u,Q<=w}, its terminal value is at least
exp(lambda u-lambda²w). Taking lambda=u/[2(w+bu)] gives lambda b<=1/2
and lambda u-lambda²w>=u²/[4(w+bu)]. Repeat with -D_j. Hence

    P(|sum D_j|>=u,Q<=w)<=2 exp(-u²/[4(w+bu)]).

The argument never changes the law by conditioning on Q<=w or on the
future overlap event. Conditioning on such a future event would in
general destroy martingale centering; a finite countercontrol in the
verification program explicitly illustrates that danger.

## 5. Smoothing, dyadic blocks and the entropy cost

Fix 1/4<gamma<1/2 and write d=gamma-1/4>0,

    beta=1/4+d/2, eta=d/4,
    r=n^beta, ell=floor(n^(2beta)/(log n)²), m=n-ell.

For all sufficiently large n, 1<=ell<=n/2 and m>=n/2.
The averaged binomial law in its *binomial index* is unimodal.
Its one-index-shift L1 difference is twice its maximum mass.
For physical positions this is precisely a shift by two, so no false
aperiodic shift-by-one estimate is being used.

The maximum binomial mass is <=C_q/sqrt(t+1). One direct proof is Fourier
inversion: the squared modulus of the Bernoulli characteristic function
is 1-4a sin²(theta/2), and sin(|theta|/2)>=|theta|/pi on [-pi,pi].
The resulting Gaussian integral bounds the Fourier L1 norm by C_a/sqrt(t)
for t>=1; absorb t=0 in the constant. Therefore, for every |f|<=1,

    |T_t f(x+1)-T_t f(x-1)|<=C/sqrt(t+1).

Expose the first m layers in nu_n=E[mu_n|F_m].
All smoothing times t=n-s-1 are >=ell. Thus the increment bound is
b<=C/sqrt(ell), and Q<=C sum_(s<m)I_s/(n-s).

Let B_j be the deterministic block with
2^j ell<=n-s-1<2^(j+1)ell. Its indices are consecutive, its length
is <=h_j=2^j ell, and 1/(n-s)<=1/h_j throughout.
The occupation bound proves that the single event
E_n={sum_(s in B_j)I_s<=n^eta sqrt(h_j) for all j}
has superpolynomially small complement; the O(log n) blocks are charged
here once. On E_n,

    Q<=C n^eta sum_j h_j^(-1/2)
      <=C n^eta/sqrt(ell).

This event is independent of the chosen test f and is F_m-measurable,
though its measurability alone is not used as a license to condition
the martingale. The valid joint-event tail for a fixed u>0 is

    P(|nu_n(f)-alpha_n(f)|>u,E_n)
       <=2 exp(-c_u n^(beta-eta)/log n).

The window [vn-sqrt(n)log n,vn+sqrt(n)log n] meets at most
J<=C n^(1/2-gamma)log n+2 cells for every alignment and M>=n^gamma.
The L1 discrepancy on those complete cells is the maximum of 2^J
deterministic sign tests, each bounded by one. The exponent margin is

    beta-eta-(1/2-gamma)=5d/4>0.

Consequently the negative exponent dominates the positive entropy
J log2; n^(5d/4)/(log n)² tends to infinity for each fixed d>0.
Charge P(E_n^c) only once, outside that union. Outside the window,
the annealed tail is <=C exp(-c(log n)²); the expectation of the random
nu_n tail equals this annealed probability, and Markov's inequality
makes any fixed positive tail threshold superpolynomially unlikely.
This proves TURN_2 equation (13), uniformly in M and alignment.

The fixed-gamma restriction matters. This proof does not take gamma
depending on n, nor assert a common threshold as gamma decreases to 1/4.

## 6. Uniform boundary majorants, including biased nonintegral shifts

Extend an integer M-site partition to real half-open intervals
[a+jM,a+(j+1)M). The comparison endpoint x+v ell is generally real.
Let B contain starting integer x within distance r, after translation
by v ell, of a real boundary. As r/M<=n^(beta-gamma) tends uniformly
to zero, the strips of radius 2r are eventually disjoint.
A concrete periodic majorant is

    f_B(x)=max(0,min(1,2-dist(x+v ell,a+M Z)/r)).

It equals one on B, has Lipschitz constant <=1/r, and vanishes at
distance >=2r from the translated grid. In one period its support
has at most ceil(4r)+2 integer residues, uniformly in the real shift.

The residue estimate needs explicit parity treatment. For any nonnegative
unimodal probability sequence p_j and integer d>=1, a sum along a residue
class modulo d is <=1/d+2 max_j p_j. To see this, partition each monotone
side into disjoint d-term blocks on the side of each sampled point where
the entries are larger. Discard at most two sampled points neighboring
the mode; each costs at most max p. All other sampled values are bounded
by the corresponding block averages, whose disjoint total is at most 1/d.
Equivalently this is the unimodal upper-Riemann-sum bound.

Writing the physical position as -m+2j, a nonempty residue class modulo M
corresponds to one binomial-index class modulo M/gcd(2,M). Therefore its
probability is <=2/M+2 max p_j, including even M. The Fourier peak estimate
then yields, uniformly in all alignments and all M>=n^gamma,

    E mu_m(f_B)<=C(r+1)/M+C(r+1)/sqrt(m)
               <=C n^(beta-gamma)+C n^(beta-1/2) ->0.

There is no assumption that the physical binomial distribution is
unimodal without restricting to its parity lattice.

For this Lipschitz test, the martingale increment bound is 2/r and
Q<=C V_(0,m)/r². Off an event of superpolynomially small probability,
V_(0,m)<=n^eta sqrt(n). The joint-event exponential bound therefore gives
a fixed-upper-deviation exponent bounded below by a positive constant
times

    1 / [n^(eta+1/2-2beta)+n^(-beta)].

The essential margin is 2beta-1/2-eta=3d/4>0.
Together with the vanishing expectation, this proves the desired fixed
threshold bound on mu_m(B). No random choice of the test is involved.

For an endpoint y with |y-(x+v ell)|<=r, a change of partition cell can
occur only if x belongs to B; half-open endpoint conventions cause no
exception because equality at a boundary is included in B.
The annealed displacement of the last ell steps has tail
<=C exp(-c r²/ell)<=C exp(-c(log n)²), using fresh bounded independent
annealed increments and centering by the actual drift v.
Its quenched bad-displacement probability has the same expectation,
so Markov again yields a superpolynomial fixed-threshold environmental
tail. Coupling both the actual last segment and an averaged last segment
to x+v ell now bounds their coarse L1 discrepancy by four boundary masses
plus twice the actual bad-displacement probability and the deterministic
annealed tail. These are precisely the terms controlled above.

This proves (G) for 1/4<gamma<1/2. For gamma>=1/2, choose any fixed
gamma_0 in (1/4,1/2), for instance 3/8; the range M>=n^gamma is contained
in M>=n^gamma_0, so the same conclusion holds. This reduction preserves
uniformity in M and alignment.

## 7. Uses made by the full candidate, and the audit boundary

PROOF.md uses (G) at m=n-floor(n^(3/4)) and
H=ceil(n^(5/16)). Since m<=n and 5/16>1/4,
H>=m^(5/16); since m>=n/2, an O(m^(-K)) bound is O(n^(-K)).
Thus the stated auxiliary call has the required fixed exponent and is
uniform in its deterministic alignment.

The other numerical use is PROOF.md equation (I).
With r=n^(3/8), eta=1/32 and the common occupation event,
Q<=C n^(-7/32), b<=2 n^(-3/8), and u=(1/2)n^(-1/32).
Hence u²/[4(Q+bu)]>=c n^(5/32).
The mean C n^(-1/8)log n is o(n^(-1/32)); a deterministic collection
of O(n) intervals can be union bounded, charging the common occupation
failure once. These exponents and conditional uses are valid.

I found no mandatory mathematical defect in these inputs, the complete
TURN_2 proof of (G), or those two interfaces. This family does not audit
the final moving-strip independence argument or the full priority and
source-conjecture interpretation; those remain the responsibility of
other independent families and Root. No overall claimed-result
publication or merger is authorized by this bounded verdict alone.

## 8. Verification controls and their limits

The independent exact program imports no candidate code and performs no
simulation. It checks backward profiles through 70 steps, arbitrary old
probability measures with conditional future integration, occupation
moments through order 8, exact layer conditional means and variances,
physical-parity residue bounds, nonintegral biased translations and
real alignments, dyadic coverage, concentration algebra and positive
fixed-gamma margins down to gamma-1/4=1/1,000,000.
Four fixed strictly elliptic laws include biased, symmetric, near-arrow
and deterministic cases. Controls also demonstrate the failure of
unjustified future-event conditioning and of omitted delta hypotheses.
The exact assertion count and observed execution are in the two JSON
receipts. These finite checks test algebra and potential edge cases;
the asymptotic theorem follows from the analytic argument, not from
finite numerical evidence.

