# Independent analytic reconstruction before author code

Exposure: exact TURN_4.md only, SHA34e043b456ddc25cc37d86d3e5a39d10243de91c6a5d5002952252d2eab1b0fa,
first actual reading 2026-10-05T18:31:06.119437Z–18:31:06.120080Z.
No author code, prior reviewer, root mathematical adjudication or sibling
proof read. This reconstructs each estimate from the exact six rates, against
the earlier source-only objections, rather than importing any verdict.

## Rounded workload estimate

Z=a+x-b-y has first-download increments zero, arrival increments +/-1 and
departure increments -1/+1. Hence LZ=(y-x)/D and its quadratic jump rate is
lambda+d. W has increments +2,+2,-1,-1,-1,-1. The clipped derivative of h_m
is globally 1/m-Lipschitz; integration of its derivative along a real segment
proves the displayed Taylor upper bound, including intervals crossing +/-m.
Thus (1) is valid for integer Z and arbitrary real positive m. Combining the
terms gives beta=2lambda+lambda/8, q=1-1/8. Also |h_m'|<=1, so the residual
term is <=c. In the positive Z cone with x>=3(y+1),
(x-y)/D>=1/2, giving the required <=-c/2. The symmetric sign is identical.

## Finite chain rather than original-chain equilibrium

The independent frozen fast process previously gave geometric weights; the
candidate now truncates at R. Finite Q has pi proportional gamma^k, since
pi_k gamma(k+1)=pi_(k+1)(k+1). Its mean increases strictly to gamma/(1-gamma)
by conditioning a geometric distribution on successively larger initial
intervals. That limit equals theta+1, so a finite R with mu>theta exists;
increase R further to satisfy the other strict q bound. For k<R, let
S_k=sum_(j<=k)gamma^j(j-mu), t_k=S_k/[gamma^(k+1)(k+1)]. Since the conditional
mean on {0,...,k} is below the full finite mean, t_k<0. g(k+1)-g(k)=t_k,
while g(R)=0. The flux identity Qg(k)=k-mu follows from
gamma(k+1)t_k-k t_(k-1)=k-mu for 0<k<R, with the k=0 and k=R terminal
equations obtained directly; at R the mean-zero total sum gives
-R t_(R-1)=R-mu. This also proves finite nonnegative decreasing g.

For the actual Y coordinate, upward increments of g are nonpositive and
downward increments nonnegative. Birth >=gamma(y+1) and death <=y imply
Lg(y)<=Qg(y) when b/D>=gamma and y<=R. At y=R the upward increment is zero,
but the same death comparison applies. For y>R, including y=R+1 whose
departure reaches R, all increments vanish. This is an all-state pointwise
generator comparison. It neither initializes Y in equilibrium nor requires
fast mixing near b/x=1; r_n approaching 1 does not invalidate it.

## Exact product signs and endpoints

The post-jump factor g(y') in the product remainder is essential and is
kept exactly. A first download raises D and either keeps b fixed or lowers
it by one; b'/D'<=b/D for all valid such transitions, including b=0 at zero
rate. Thus its interface term is nonpositive. The matching main g term is
also nonpositive on first downloads. Both statements are global and require
no bound on empty-room sizes.

Arrivals have denominator fixed and increase only one numerator by one.
Their aggregate interface cost is <=lambda ell G/D. At a departure D>=2.
If w/D>=eta both cutoffs are one. Otherwise w<eta D and
0<=f(w/(D-1))-f(w/D)<=ell w/[D(D-1)]<=2ell/D.
Two post-jump g values at most G yield cost <=4ell G/D per departure.
At D=1 departure rates are zero, so division by D-1 is never used. These
arguments include t=gamma, t=eta and all one-jump crossings of either cutoff.
They give (9). Independently, each bounded J term lies in [0,G], first
downloads decrease it, arrivals affect one term and departures at most two;
this proves (10), including unbounded a,b with bounded visible population.

## Three exhaustive regions and finite constants for real lambda

All constants beta,c,m,theta are finite positive real functions of a fixed
finite lambda>0. gamma,eta lie strictly inside (0,1), ell finite. The two R
conditions have a finite integer solution from the geometric-mean limit and
unbounded q(R+1). With finite R and G, each N condition is a finite lower
bound, since 1-eta>0. Taking the ceiling of their maximum gives a finite
integer N. B is finite; no uniform-in-lambda statement is needed. The proof
does not restrict lambda to rational or integer values.

I: min(x,y)>=R+1 makes current and every successor g vanish, including
decrement R+1->R. For x>=y, D(d-y)=y(x-y)+x>=0. The symmetric identity covers
the other order. Thus beta+c-q(R+1)<-2 suffices.

II: y<=R,x>=N, and N>=R+2 make the symmetric correction identically zero
on current and successor states. Directly d<=2y+1<=2R+1. x>=3(y+1) gives
x/D>=3/4, (x-y)/D>=1/2 and qd>=(21/32)(2y+1)>=y. D>=N and the fourth N
bound make the interface error <=1. The actual-generator Poisson comparison
can be multiplied by f, since f>0 implies b/D>gamma; f=0 gives equality zero.
If b/D>=eta, f=1 and LV<=beta+c-mu+1<-3. Otherwise
Z>=x-eta(x+y+1)-y>=(1-eta)N-(1+eta)R-eta>=m, so the rounded term contributes
<=-c/2; f(y-mu)<=y gives LV<=beta-c/2+1-u=-3-u. No missing transition-band
case remains. Exchanging (a,x) with (b,y) preserves the chain and V.

III: the remaining states have min<=R and max<N, so x+y<=N+R. The global
bounded-correction estimate gives LV<=beta+c+G[lambda+2(N+R)]-u and
u>=(a+b)/(N+R+1). Thus a+b>B implies LV<-1. The stated finite F can include
some I/II states, which is harmless. These regions cover all integer states.

## Martingale and chosen-state recurrence hypotheses independently supplied

The initial workload jump-budget proof gives nonexplosion, irreducibility,
E[J(t)]<=W(0)+3lambda t, W(t)<=W(0)+2P_lambda(t). V>=W is coercive, and
h_m(z)<=|z|+m/2, |Z|<=W, 0<=J<=2G imply
V<=(1+c)W+c m/2+2G. Each jump of V has absolute size <=2+c+2G because
|h_m'|<=1 and J lies in [0,2G]. Consequently fixed-time jump sums and
compensators are integrable, without an invariant-moment assumption.
Localized Dynkin on finite population sets, stopped at tau_F and t, gives
E[tau_F wedge t wedge tau_M]<=V(s). N<=N(0)+P(t) implies tau_M tends to
infinity pathwise on each bounded horizon. Fatou/monotone convergence yields
E_s tau_F<=V(s). Alternatively the stated integrability justifies the same
bounded-time stopped identity directly. Neither argument assumes recurrence.

The terse finite-set conclusion can be expanded without invoking an unverified
criterion. For each state in finite F, prescribe its positive-rate drain path
to zero, with no arrivals and completion within one time unit. The minimum
success probability p over F is positive. If unsuccessful, at time one
E[V(S_1)] is uniformly finite by the linear upper bound and W_1<=W_0+2P(1).
Return to F has expectation <=V(S_1) outside F and zero inside. Repeated
strong-Markov trials thus have uniform positive success probability and
uniform finite expected durations, yielding finite expected zero hitting
from F, hence from every state. After leaving zero the chain has W=2, and
holding at zero has finite mean 1/lambda. This gives a genuine finite-mean
return cycle. Occupation measure divided by its finite mean cycle length
gives a stationary probability, and irreducibility gives uniqueness. No
stationary finite population moment, embedded-chain recurrence, uniform
load bound, or finite-truncation inference is used.

## Disposition of the frozen stochastic objections at this checkpoint

Nonexplosion/holding times: independently proved and applicable. Large
single cohort and critical r_n sequences: pointwise corrector comparison
works at initial Y=0, with no equilibration delay. Macroscopic empty initial
layers: monotone first-download interface terms can be arbitrarily large
but favorable; Region III handles bounded visible sizes. Balanced and
postjump endpoints: explicitly included by finite g support and global
product identity. Cone exits need not contract: the proposed single coercive
V and compact return bound supply the missing global mechanism instead.
No mandatory mathematical issue has been identified by analytic reconstruction.
Independent finite controls will test these statements before author-code
exposure; they supplement, not replace, the general derivations above.
Exact-original-problem resolution remains conditional on the separate final
primary-source correspondence gate; no novelty/publication authority.


## Expanded finite-mean regeneration and stationary-law argument

Let M=max_(s in F)W(s), finite, and C0=c m/2+2G. The already derived
upper bound is V(s)<=(1+c)W(s)+C0. From any s in F choose a valid internal
drain path of length at most M, and require no arrivals for one unit.
Conditional on that Poisson event, each chosen internal transition has positive
rate and finite total internal rate at its finite pre-state. Requiring each
selected waiting time at most1/(M+1) and the desired event gives a strictly
positive finite product. Zero succeeds immediately. Taking the minimum over
finite F gives p>0, without stationarity, mixing or fluid assumptions.

At a failed trial's one-unit endpoint W<=M+2P(1), so E[V(S1)] is uniformly
at most (1+c)(M+2lambda)+C0=:C1. Return to F from that endpoint has mean
at most V(S1), or zero inside F. Each trial plus return therefore has uniformly
bounded unconditional mean duration1+C1. Strong Markov gives conditional
success chance at least p. The probability of starting trial k is at most
(1-p)^(k-1), so Tonelli bounds expected total duration by(1+C1)/p. Extra
zero hits during the return to F only improve it. Starting anywhere adds
at most V(s) for its initial compact hit. At zero holding mean1/lambda is
finite; the next state has W=2. Its hitting-zero time has finite mean. This
establishes the genuine continuous-time finite-mean return cycle, including
holding and departure. Irreducibility makes positive recurrence a class property.

Expected occupation of each state during this conservative regenerative cycle
divided by the finite mean cycle length sums to one by Tonelli. The workload
budget bounds its expected total events by three times expected Poisson
arrivals, finite by the Poisson compensator at an integrable stopping time.
Thus bounded test-function jump sums are integrable and telescope to zero
over the cycle. This is the regenerative invariant occupation law; irreducibility
gives uniqueness and full support. No uniform-in-lambda constants, lambda0
claim, embedded-chain holding assumption or invariant finite-N moment is used.
