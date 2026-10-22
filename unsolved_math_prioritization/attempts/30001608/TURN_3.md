# Turn 3: an exact all-load local corrector and a complementary exit estimate

**Scoped partial; no global stability theorem for lambda>=2 is claimed.** This third substantive author turn attacks the high-load boundary regime in the exact2011 chain. Unlike the first two polynomial certificates, the new correction solves a finite birth–death Poisson equation. The comparison is pointwise in the actual generator, so it does not assume independence of a random sector-exit time and the rare-chunk process.

## 1. A finite increasing-cost Poisson equation

Fix any lambda>0 and set

 gamma=(lambda+1)/(lambda+2) in(0,1).

For an integer R>=1, consider the finite birth–death generator Q_R on{0,...,R} with birth rate gamma(k+1) for k<R and death rate k for k>0; births at R are suppressed. Its stationary probability weights are proportional to gamma^k, since adjacent flows obey

 gamma^k gamma(k+1)=gamma^(k+1)(k+1).

Let

 mu_R = [sum_(k=0)^R k gamma^k]/[sum_(k=0)^R gamma^k].

As R tends to infinity, mu_R tends to gamma/(1-gamma)=lambda+1. Therefore choose a finite R with mu_R>lambda. This choice depends only on lambda. Put epsilon=mu_R+1/2-lambda>1/2.

There is a nonnegative decreasing function g on{0,...,R}, normalized by g(R)=0, satisfying

 Q_R g(k)=k-mu_R.                                      (1)

For an explicit proof, define for0<=k<R

 d_k=[sum_(j=0)^k gamma^j(j-mu_R)]/[gamma^(k+1)(k+1)],
 g(k)=-sum_(j=k)^(R-1) d_j.

Every d_k is strictly negative: the mean of j conditioned on j<=k is strictly smaller than the full mean mu_R, because the omitted upper tail has positive weight and larger indices. Thus g is decreasing and nonnegative. Multiplying(1) by gamma^k makes the birth/death flux terms telescope, verifying it for k<R. The mean-zero identity sum_(k=0)^R gamma^k(k-mu_R)=0 verifies the final equation at R. No infinite-chain convergence theorem is needed for this finite calculation.

Extend g to Z_+ by g(k)=0 for k>=R.

## 2. Exact negative drift on a majority/cohort sector, at every load

Return to the source state(a,b,x,y), D=x+y+1 and S=a+b+x+y. Define the sector

 F_X={ x/D>=1/2, b/D>=gamma }.

On this sector the chunk0 population is the current majority, and the waiting room committed to the rare chunk is large relative to the visible population. Define the globally nonnegative coercive function

 H_X=S+g(y).

Then the exact source generator satisfies

 L H_X<=-epsilon on F_X.                               (2)

Indeed, the total departure rate is

 r_X+r_Y=[x(y+1)+y(x+1)]/D >= (2y+1)/2=y+1/2,

so LS<=lambda-y-1/2. The birth rate of Y is r_B=b(y+1)/D>=gamma(y+1), while its death rate r_Y=y(x+1)/D<=y. Because g is decreasing, increasing the birth rate can only lower Lg, and decreasing the death rate can only lower it as well. For0<=y<R, this gives Lg(y)<=Q_R g(y)=y-mu_R. At y=R, the upward increment of g is zero and the same bound follows from the death term and the final equation in(1). For y>R all increments of g vanish, and LS<=lambda-y-1/2<=lambda-mu_R-1/2, since mu_R<R. This proves(2), including all boundaries.

This is a comparison of generator terms at each actual state. It is not a replacement of Y by an independent stationary process, and it never substitutes a stationary mean at a stopping time. Symmetrically,

 F_Y={ y/D>=1/2, a/D>=gamma },    H_Y=S+g(x)

has the same drift bound.

In particular, the critical rays that defeated the quadratic family in Turn2 are now covered at every load: at(0,m,m,0), the sector condition holds as soon as m/(m+1)>=gamma, equivalently m>=lambda+1. The mirrored ray is covered by F_Y. This is a genuine improvement in treatment of those high-load states, but the test function changes between regions.

For clarity, if tau is the first exit from F_X and the starting state belongs to F_X, stopped Dynkin with finite-level localization gives

 E[S_(t wedge tau)]+epsilon E[t wedge tau] <= S_0+g(y_0),
 E[tau] <= [S_0+g(y_0)]/epsilon.                       (3)

The chain is nonexplosive and H_X nonnegative; the usual Fatou argument removes localization. Analogous statements hold for F_Y. These are sector-exit and accumulated-drift estimates, not returns to a fixed compact set.

## 3. A complementary strongly biased sector

Keep gamma as above and put

 K=2(1+gamma)/(1-gamma)=4lambda+6,
 v=(K-1)/(K+1)>0.

Consider

 E_X={ x>=K(y+1), b<gamma D }.

In this region the current majority is strong but the rare-chunk waiting room is too small for F_X. The exact cohort imbalance Z=a+x-b-y is nevertheless positive:

 Z>a+(1-gamma)x-(1+gamma)y-gamma
   >=a+(1-gamma)x-(1+gamma)(y+1)
   >=a+(1-gamma)x/2>0.                                (4)

Also D<=x(1+1/K) and x-y>=x(1-1/K), whence

 LZ=-(x-y)/D<=-v.                                    (5)

Let tau be the first exit from E_X. Until tau, Z is positive; at the exit it is at least-1 because each actual jump changes Z by at most1. Applying stopped Dynkin to Z+1 yields

 E[tau] <= (Z_0+1)/v.                                (6)

One can justify this directly without a population moment assumption: up to any fixed time the number of arrivals is Poisson, each peer makes at most two download transitions, and the total variation of Z is bounded by arrivals plus departures. Hence the stopped compensator is integrable. Finite-level localization and nonnegativity up to exit then give(6).

The population can increase only at arrivals. Optional stopping for the arrival counting process and E[tau]<infinity consequently give

 E[S_tau] <= S_0+lambda E[tau]
          <= S_0+lambda(Z_0+1)/v.                    (7)

The symmetric statement holds for E_Y. The right side of(7) can exceed S_0; it is an excursion-growth bound, not a contraction estimate.

## 4. What this settles and what it does not

The all-load local correction proves that the source's critical rare-chunk boundary behavior can be controlled by an exact finite-state Poisson equation. The complementary imbalance drift gives finite expected exit from a substantial neighboring cone. Both statements concern the actual stochastic generator with seed and invisible waiting rooms intact.

They do not yet imply positive recurrence at lambda>=2. A global argument must control transitions among the sectors and the remaining states, or construct a single suitable Lyapunov function. Alternating local functions cannot simply be summed or switched without accounting for changes at interfaces. Likewise, bounded g does not remove the possible cumulative cost of repeatedly switching sectors. No claim of instability follows from the absence of such a global argument so far.

The proved global range remains0<lambda<2 from Turn2. Original target remains unresolved after3/5 substantive turns. The continuing route now combines nonlinear Foster drift, a finite Poisson corrector and stopped sector estimates. Classical birth–death balance, finite Poisson equations and Foster/Dynkin arguments are credited; no historical novelty claim is made.
