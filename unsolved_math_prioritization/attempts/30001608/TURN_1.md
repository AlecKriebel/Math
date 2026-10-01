# Turn 1: low-load stability and an obstruction to affine drift certificates

**Scoped partial, original conjecture unresolved.** This is the first substantive author turn. The generator is exactly Figure2 of the January2011 Norros–Reittu–Eirola author proof, not the broader all-peer sampling variant. Classical continuous-time Foster reasoning is credited; historical novelty is not claimed.

Write s=(a,b,x,y), D=x+y+1, n=x+y, and fix lambda>0. The two arrivals have rates lambda/2. The other rates are

r_A=a(x+1)/D, r_B=b(y+1)/D, r_X=x(y+1)/D, r_Y=y(x+1)/D,

for A->X, B->Y, X->outside, Y->outside respectively. Let L be this conservative generator on Z_+^4.

## 1. Well-definedness and communication

There is a pathwise construction with a Poisson(lambda) arrival process. On every bounded time interval there are finitely many arrivals. Each initial or arriving peer makes at most two actual download transitions before departing. Thus the total number of actual state changes by time t is at most 3 times the arrival count plus twice the initial population. The rates are finite at every finite state. This gives nonexplosion without comparing to a potentially explosive polynomial rate bound. Null contacts are not state changes and need not be included in L.

For lambda>0, any finite state can reach the empty state through a finite sequence of allowed downloads/departures, using the permanent seed when a chunk is absent. Every required positive-population transition has positive rate. Conversely, from the empty state arrivals can create the necessary A/B populations and their first downloads can create arbitrary X/Y populations. Prescribing a finite sequence of these events and forbidding others until it completes has positive probability. Hence the chain is irreducible on Z_+^4.

## 2. Positive recurrence for 0<lambda<1

Choose c with 1<c<1/lambda, and put

V(s)=c(a+b)+x+y,     eta=(1-c lambda)/2>0.

An arrival adds c; a first download subtracts c-1; a final download subtracts1. Therefore the exact drift is

LV=c lambda - [(c-1){a(x+1)+b(y+1)}+2xy+x+y]/D.          (1)

The fraction in(1) is at least

[(c-1)(a+b)+n]/(n+1).                                  (2)

Choose an integer R so large that n/(n+1)>=c lambda+eta whenever n>=R. For n<R, choose an integer K so large that (c-1)K/(R+1)>=c lambda+eta. Outside the finite set

C={n<R, a+b<K},

(2) is at least c lambda+eta, and consequently LV<=-eta. The function V is nonnegative and has finite sublevel sets. Stopping Dynkin's identity at the first entrance into C, time t, and a finite V-level gives

E_s[tau_C] <= V(s)/eta

for s outside C, by Fatou and monotone convergence. Local stopping is legitimate because the finite-level state space has bounded rates; nonexplosion removes the local cutoff. The finite-set hitting-time criterion for irreducible continuous-time chains then gives positive recurrence and a unique stationary probability distribution. This is the same criterion stated in Section2 of the source. Thus the source conjecture holds at every fixed 0<lambda<1.

The estimate is deliberately a low-load result. It says nothing about lambda>=1, where the conjecture is most interesting.

## 3. No coercive affine Foster function can settle lambda>=1

Precisely, for lambda>=1 there is no affine function V on Z_+^4 with finite sublevel sets, bounded below, and LV<0 outside a finite set. Suppose such a function existed. Average it with its image under the chunk exchange (a,b,x,y)->(b,a,y,x). The generator commutes with that exchange; the averaged drift is negative outside the union of two finite sets. Its linear part is

V_sym=alpha(a+b)+beta(x+y),

where alpha,beta>0: boundedness below and finite sublevel sets force every original linear coefficient to be positive. At states (a,0,0,0),

LV_sym=lambda alpha+(beta-alpha)a.

Eventual negativity requires alpha>beta. But at states (0,0,x,0),

LV_sym=lambda alpha-beta x/(x+1) > lambda alpha-beta >0

when lambda>=1. This contradiction proves the claim, including the critical value lambda=1. This is an obstruction only to the indicated class of pointwise drift proofs. It is not an instability theorem and does not exclude nonlinear, piecewise or time-averaged Foster functions.

## 4. Exact balance and imbalance identities for later high-load work

Set U=a+x, W=b+y, Z=U-W. First downloads leave Z unchanged. Arrival increments are symmetric, and departures give

LZ=(y-x)/D,                                            (3)
L(Z^2)=lambda+(2xy+x+y)/D-2Z(x-y)/D.                   (4)

These formulas exhibit a seed-scale restoring term even on highly imbalanced boundary regions. They do not by themselves control the total population. In particular, Z need not have the sign of x-y because the waiting-room populations can dominate.

If a stationary probability law pi exists at any lambda>0, then

E_pi r_A=E_pi r_B=E_pi r_X=E_pi r_Y=lambda/2.           (5)

No first moment of the populations is assumed in this necessary condition. For A, use the bounded level indicator 1_{A>k}. Both nonzero terms of its generator are integrable: the up-rate is lambda/2 and the down-rate on A=k+1 is at most k+1. Stationarity gives

(lambda/2) pi(A=k)=E_pi[r_A 1_{A=k+1}].

Summing over k>=0 proves E r_A=lambda/2 by Tonelli, and similarly for B. Next use 1_{X>k}: its up-rate is r_A, now integrable, and its down-rate on X=k+1 is at most k+1. Sum the level balance to get E r_X=E r_A; do the same for Y. The use of stationarity on each bounded level indicator follows either from expected crossing counts over a finite interval or localized compensation; all boundary crossing rates just listed are integrable.

Since r_X+r_Y=(2xy+x+y)/D, equation(5) gives

E_pi[2XY/(X+Y+1)] = lambda-1+E_pi[1/(X+Y+1)],         (6)
E_pi[(X-Y)/(X+Y+1)] = 0.                              (7)

Thus any high-load stationary law must maintain a nontrivial average overlap of the two chunk populations. Equation(6) is a necessary balance relation, not evidence that such a law exists. It applies to the source's continuous-time chain; an embedded jump chain generally has a differently weighted stationary law.

## Remaining target and next route

The original conjecture is positive recurrence at every fixed lambda>0 despite the credited diverging large-system ODE trajectories. The unresolved range is lambda>=1. The low-load Foster function fails for a structural reason, not simply because a numerical coefficient was poorly chosen. A future argument must exploit nonlinear majority switching, a multistep drift, or a different rigorous mechanism; it must retain the source denominator and seed contributions and distinguish the two scaling regimes.
