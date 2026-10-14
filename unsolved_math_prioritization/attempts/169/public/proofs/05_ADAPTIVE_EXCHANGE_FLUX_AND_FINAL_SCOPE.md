# Stage 5: exact adaptive exchange flux and the final bounded-score frontier

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 5.

## Result

The original covering question is **not resolved**. This argument directly analyzes the bounded score on the true adaptive convolution by exchanging one element of the random set A. An exact finite-population identity isolates the adaptive selection term that a Poisson or compound-Poisson substitution would omit. A one-sided estimate for that term would force a positive score without any distributional approximation. The estimate has not been proved.

The identity and its conditional consequence are new unrestricted reductions. They do not establish an unconditional lower bound for the optimal residual, an upper bound at a smaller budget, or a further excluded algorithm class. The final missing estimate is stated explicitly below.

## 1. Exact model and the fixed-size score minimum

Let p be prime, k=floor(sqrt(p)), c=floor(100sqrt(p)), and A uniform over all k-subsets of G=Z/pZ. The argument below applies to any integers 1<=k,m<p, and we subsequently take m=c for sufficiently large p.

For a deterministic selector A -> T(A) with |T(A)|=m, set

f_{A,T}(x)=(1_A*1_T)(x),
H_q(A,T)=p^(-1) sum_x q^{f_{A,T}(x)},
g_q(n)=(1-n)q^n,  0<q<=1/2.

Let X be uniform in G, independently of A, and put Z=f_{A,T(A)}(X). Write

F=E q^Z,  M=E Zq^Z,  M_2=E Z^2q^Z,
lambda=km/p,  K=k(p-k).

These expectations include the actual adaptive selection. In particular E Z=lambda exactly, because sum_x f_{A,T(A)}(x)=km for every A. No independence of A and T is assumed.

For the target use a canonical minimizer among the finite family of exactly c-element sets:

B_q^=(A)=min_{|T|=c} sum_x g_q(f_{A,T}(x)).

This is not identified with the at-most-c score minimum from Stage 4. Nevertheless, if a cover exists with at most c centres, it can be padded to exactly c centres, and every cover has score <=0. Consequently

{R_c=0} subset {B_q^=<=0},
R_c-q^2p <= B_q^= <= R_c.

The second statement follows by minimizing the pointwise score sandwich over exactly c sets; the residual minimum itself is unchanged by padding. The score need not be monotone under padding.

## 2. Stationary exchange, with the selector movement retained

Sample y uniformly from A and z uniformly from G\\A, independently conditional on A, and put A'=A\\{y} union {z}. The distribution of A' is again uniform over the k-subsets.

Define the normalized reoptimization flux

D_q(T)=E[H_q(A',T(A'))-H_q(A',T(A))].                 (2.1)

The old and new selectors are evaluated on the same new A'. This distinction is essential. Stationarity says

0=E[H_q(A',T(A'))-H_q(A,T(A))]
 =D_q(T)+E[H_q(A',T(A))-H_q(A,T(A))].              (2.2)

It does not say D_q(T)=0.

Conditional on fixed A,T=T(A),X and n=f_{A,T}(X), the old-selector multiplicity rises by one with probability

b_n=(k-n)(m-n)/K,

and falls by one with probability

d_n=n(p-k-m+n)/K.

These are exact counts of the deletion/insertion choices relative to the fixed m-set X-T. Thus the expected old-selector change of q^n is

(q-1)q^n b_n+(q^(-1)-1)q^n d_n
=(1-q)/(qK) * q^n[(1-q)n^2+(p-(1-q)(k+m))n-qkm].

Averaging and applying (2.2) proves the exact identity

(1-q)M_2+[p-(1-q)(k+m)]M-qkmF
 =-qK D_q(T)/(1-q).                               (2.3)

Equivalently, the expected bounded score is

E g_q(Z)
 =(1-lambda q)F
  -(1-q)[(k+m)M-M_2]/p
  +qk(p-k)D_q(T)/[(1-q)p].                         (2.4)

This holds for every selector, including one chosen after inspecting all of A to minimize the bounded score. It uses the real additive convolution and finite uniform-k law throughout.

## 3. A conditional one-sided theorem requiring no Poisson law

Since q^n is decreasing, the covariance inequality gives

M<=lambda F.                                     (3.1)

For completeness, if Z' is an independent copy of Z, then

2 Cov(Z,q^Z)=E[(Z-Z')(q^Z-q^{Z'})]<=0.

Also Jensen's inequality for the convex function q^x gives

F>=q^lambda.                                     (3.2)

Since 0<=Z<=min(k,m), the finite-population correction in (2.4) is nonnegative and satisfies

0<=(1-q)[(k+m)M-M_2]/p
 <=lambda(1-q)(k+m)F/p.                           (3.3)

Define

alpha=1-lambda q-lambda(1-q)(k+m)/p,
C_q=qk(p-k)/[(1-q)p].

Whenever alpha>=0, (2.4)-(3.3) imply

E g_q(Z)>=alpha q^lambda+C_q D_q(T).              (3.4)

This is an actual finite-model bound. Its unknown term is the signed flux, not an assumed occupancy law.

### Applying it at the exact cap

Take m=c and fix any q in (0,1/100), for example q=1/200. The exact mean satisfies lambda=kc/p<=100 and lambda->100. Also (k+c)/p->0, so

alpha->1-100q>0,
C_q/k->q/(1-q),
q^lambda->q^100.

Choose T_q(A) to minimize the exactly-c bounded score. A sufficient, but unproved, hypothesis is

liminf_{p->infinity, p prime} k D_q(T_q)>=0.        (3.5)

It could be weakened to a sufficiently small fixed negative lower bound. Under (3.5), equation (3.4) gives

liminf p^(-1) E B_q^=(A) >=(1-100q)q^100>0.        (3.6)

The same conclusion along an unbounded prime subsequence already suffices to contradict the original affirmative limit.

The score minimum has the same exchange Lipschitz bound c(1+q^2) as in Stage 4: take minima over the common exactly-c family. Its uniform-subset exposure inequality therefore yields

Pr[R_c=0]
 <=exp[-(E B_q^=)^2/(2kc^2(1+q^2)^2)]

when E[B_q^=(A)]>0. Consequently (3.5) would in fact imply noncoverage with probability tending to one. It is a substantially stronger sufficient premise than the minimal p^(3/4)-scale mean bridge.

No estimate (3.5), no weaker sufficient flux bound, and no conclusion (3.6) is asserted unconditionally. The very small fixed constant q^100 is mathematically positive but is not a practical finite-size estimate.

## 4. What direct factorization and exchange bounds actually provide

For 0<q<=1/2, n q^{n-1}<=1 for every n>=1. The positive death contribution in the old-selector drift is therefore at most (1-q)/k. The magnitude of its negative birth contribution is at most (1-q)m/(p-k). Equation (2.2) gives the unconditional bounds

-(1-q)/k <= D_q(T) <= (1-q)m/(p-k).               (4.1)

They hold for every adaptive selector. At m=c, the scaled negative bound is only

k D_q(T)>=-(1-q),

which is far too weak for (3.4) to force a positive score: substitution leaves a negative term tending to -q, while the available positive lower bound is approximately (1-100q)q^100.

Thus the natural stationary-exchange calculation does produce the correct order 1/k of the adaptive correction, but it does not make its negative part little-o(1/k) or sufficiently small. Discarding that order-1/k term changes the normalized score by order one because C_q has order k. This is the precise place where a naive Poisson argument would lose the whole possible covering advantage.

### A finite actual-additive sign check

A blanket nonnegative-flux statement is false even under uniform A. Take p=5,k=2,m=3,q=1/2 and, for each A, choose a lexicographically first m-set minimizing H_q(A,T). All 2-subsets are affine equivalent. A cover exists with profile four entries equal to 1 and one entry equal to 2, and this minimizes H_q because every other admissible profile has more zeros. Hence

F=9/20, M=1/2, M_2=3/5, lambda=6/5, K=6.

Equation (2.3), or direct enumeration of all exchanges, gives

D_q=-1/30<0.

The same selector minimizes the bounded score, whose normalized value is -1/20. This is a check on the sign and necessity of the correction. It is not an asymptotic counterexample at the operational cap, and it does not refute (3.5) in the square-root prime regime.

## 5. How the identity separates clustering from zero-free drift

This section interprets the exact identity; it is not a limit theorem for adaptive selectors.

Suppose m/k->C, k^2/p->1, and along some sequence the actual law of Z has a weak limit W. Its mean is at most C by Fatou, and q^n, nq^n and n^2q^n are bounded. Passing to the limit in (2.3) gives

lim kD_q=(1-q)/q * [Cq E q^W-E Wq^W],            (5.1)

whenever the displayed limit is considered along that subsequence. The finite-population correction vanishes. Weak convergence already determines the right-hand side and therefore the scaled-flux limit.

If W is drift-free compound Poisson with jump intensities beta_j and mean mu=sum_j j beta_j<=C, then

E Wq^W=(E q^W) sum_j j beta_j q^j
       <=Cq E q^W.

Thus its scaled flux is nonnegative, including parity and other clustered laws. A Poisson(C) limit has zero scaled flux. A drift-free clustered law can have strictly positive scaled flux. Exact Poisson matching is not needed for the sufficient sign.

On the other hand, if W is zero-free, then E Wq^W>=E q^W. For q<1/C, (5.1) gives

lim kD_q <=-(1-q)(1-Cq)E q^W/q<0.                 (5.2)

The limiting F is positive, with E q^W>=q^C. A deterministic positive drift plus a compound-Poisson component is one instance of a zero-free limit, but no infinitely divisible representation is needed for (5.2).

This identifies the substantive issue: all possible zero-free limiting laws require a persistent negative selection flux. Proving that random-A additive factorizations exclude enough of that negative flux would be a genuine additional theorem. The identity itself does not exclude it, and finite stationarity or the mere total-mass condition does not supply the sign.

Weak zero-free limits alone concern zero density of holes, not their number. A sequence may have p^(3/4) holes while its random-site law converges to a zero-free distribution. Conversely a positive fixed-q score bound of order p would force positive-density holes. Those scales must not be conflated.

## 6. Final missing statements and honest conditional scope

The unchanged target is whether a uniform floor(sqrt(p))-set A admits at most floor(100sqrt(p)) translates covering every point with probability tending to one along all primes.

The available unconditional estimates still do not settle either direction:

- At the full budget, 0<=E R_c<=p binom(p-k,c)/binom(p,c)=(e^(-100)+o(1))p. No positive unrestricted lower bound at order c sqrt(k) was obtained.
- The new exchange identity exactly retains the arbitrary dependence T(A); its sufficient one-sided flux estimate is not proved.
- Fixed-candidate hypergeometric expectations, or a drift-free compound-Poisson calculation applied without an adaptive approximation theorem, do not control E min_T G_q(A,T).
- Taking q=o(p^(-1/8)) makes the bounded-score mean differ from E R_c by o(c sqrt(k)); this remains the same unresolved expectation problem at the needed scale.
- No upper bound E R_(33k)=o(p^(5/6)) or E R_(49k)=o(p^(3/4)) was established. The audited amplification-and-repair constructions remain conditional on those respective smaller-budget estimates.

A precise sufficient negative missing statement remains

E R_c>=a c sqrt(k)

for a fixed a>0 along an unbounded sequence of primes. It is sufficient, not necessary for a negative answer. The bounded-score variant E[B_q^=(A)] >= a c sqrt(k) is also sufficient. The flux hypothesis (3.5) is a stronger, structurally explicit route to such an estimate, not a proof or an equivalent reformulation claimed to be easier.

A precise sufficient positive missing statement remains either of the two smaller-budget mean estimates just listed, or an actual construction giving full coverage within the exact cap with high probability. No full proof or verified counterexample survives this final argument. The original problem remains unresolved by the five-pass program.

