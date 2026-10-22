# Turn 4: a global cutoff-Poisson Foster function

**Complete proof candidate, awaiting independent adversarial review.** This is substantive author turn 4 of the five-turn budget for problem 30001608. The live branch was verified at commit `1350019e1312d940ef483f09c424454da30c9498` before beginning. Its saved count is three prior substantive turns. Source retrieval, review and packaging are not additional author turns.

## 1. Exact target and theorem

The target is the stability conjecture for the deterministic-first-chunk model in Norros–Reittu–Eirola, *On the stability of two-chunk file-sharing systems*, Queueing Systems 67 (2011), 183–206, DOI [10.1007/s11134-011-9209-2](https://doi.org/10.1007/s11134-011-9209-2), Section 3.2, Figure 2 and Conjecture 3.6 of the January 5, 2011 author proof [HAL 00781341](https://hal.science/hal-00781341/document). It also appears in Norros's contribution to [Oberwolfach Report 48/2010](https://ems.press/content/serial-article-files/46306), printed pp. 2782–2783. The 2009 arXiv version states an opposite conjecture and is not the controlling edition. The exact source audit is preserved in `prior/SOURCE_AUDIT.md`.

Fix any real lambda > 0. The state is s=(a,b,x,y) in the nonnegative integer lattice. Put D=x+y+1. The two arrival transitions add one to a or b, each at rate lambda/2. The remaining transitions and rates are

- (a,b,x,y) -> (a-1,b,x+1,y), r_A=a(x+1)/D;
- (a,b,x,y) -> (a,b-1,x,y+1), r_B=b(y+1)/D;
- (a,b,x,y) -> (a,b,x-1,y), r_X=x(y+1)/D;
- (a,b,x,y) -> (a,b,x,y-1), r_Y=y(x+1)/D.

A rate is zero if the decremented coordinate is zero. The empty waiting rooms a,b are excluded from D, exactly as in the source. The seed is retained through every +1.

**Theorem.** For every fixed lambda > 0 this continuous-time chain is irreducible and positive recurrent, hence has a unique stationary probability law.

The proof below constructs one globally defined coercive function V with LV <= -1 outside a finite set. It uses neither a stationary-mean substitution in the original chain nor a sector-switching argument. The classical finite birth–death Poisson equation and continuous-time Foster criterion are credited tools; no historical novelty certification is asserted.

## 2. Basic identities and a rounded absolute value

Let

 Z=a+x-b-y,   W=2a+2b+x+y,
 u=r_A+r_B,  d=r_X+r_Y=(2xy+x+y)/D.

First downloads leave Z unchanged, and direct calculation gives

 LW=2 lambda-u-d,       LZ=(y-x)/D.

The sum of rates of jumps changing Z is lambda+d; each such jump changes it by +1 or -1. For a positive real m, define

 h_m(z) = z^2/(2m)+m/2  if |z|<=m,
          |z|          if |z|>=m.

This is continuously differentiable. Its derivative is z/m clipped to [-1,1], and is globally 1/m-Lipschitz. Thus for every real z and v,

 h_m(z+v)-h_m(z) <= h_m'(z)v + v^2/(2m).

In particular,

 L h_m(Z) <= h_m'(Z)(y-x)/D + (lambda+d)/(2m).       (1)

Set

 beta=17 lambda/8,  q=7/8,
 c=2(beta+4),       m=4c,
 theta=beta+c+4.

Combining (1) with LW and c/(2m)=1/8 gives the global bound

 L(W+c h_m(Z))
 <= beta-u-q d+c h_m'(Z)(y-x)/D.                    (2)

The final term has absolute value at most c. If Z>=m and x>=3(y+1), it is at most -c/2, since h_m'(Z)=1 and (x-y)/D>=1/2.

## 3. Finite Poisson corrector

Choose

 gamma=(theta+1)/(theta+2),    eta=(1+gamma)/2,
 ell=1/(eta-gamma).

Both gamma and eta are strictly between zero and one, and gamma<eta. On {0,...,R}, consider the finite birth–death generator Q with births gamma(k+1) for k<R and deaths k for k>0; births at R are suppressed. Its stationary weights are gamma^k. Let

 mu_R = [sum_{k=0}^R k gamma^k]/[sum_{k=0}^R gamma^k].

As R increases, mu_R increases to gamma/(1-gamma)=theta+1. Choose an integer R>=1 satisfying both

 mu:=mu_R>theta,       q(R+1)>beta+c+2.              (3)

Such a finite R exists. Define, for 0<=k<R,

 t_k = [sum_{j=0}^k gamma^j(j-mu)]/[gamma^(k+1)(k+1)],
 g(k)=-sum_{j=k}^{R-1}t_j,

and put g(k)=0 for every integer k>=R. Each t_k is negative, because the mean of j restricted to j<=k is strictly below the full mean mu. Consequently g is decreasing and nonnegative, with finite G:=g(0)>0. The flux-telescoping identity, including the mean-zero terminal equation at R, gives

 Qg(k)=k-mu,    0<=k<=R.                            (4)

For the actual chain, the y birth rate is (b/D)(y+1), while the y death rate is y(x+1)/D<=y. The monotonicity of g and (4) therefore imply

 Lg(y)<=y-mu   if 0<=y<=R and b/D>=gamma.           (5)

At y=R its upward increment is zero; the same inequality follows from the death term and the terminal equation in (4). At y>R all increments of g vanish, so Lg(y)=0. There is a symmetric statement for x with a/D in place of b/D.

## 4. Cutoffs and the signed interface estimate

Define the nondecreasing Lipschitz cutoff f on the nonnegative reals by

 f(t)=0                  for t<=gamma,
      (t-gamma)/(eta-gamma) for gamma<t<eta,
      1                  for t>=eta.

Its Lipschitz constant is ell. Define two bounded nonnegative corrections

 J_X=f(b/D)g(y),       J_Y=f(a/D)g(x),       J=J_X+J_Y.

The candidate is the single globally defined function

 V=W+c h_m(Z)+J.                                    (6)

It is nonnegative and coercive, since V>=W>=a+b+x+y.

For any transition s->s', use the exact product identity

 J_X(s')-J_X(s)
 = f(b/D)[g(y')-g(y)]
   +g(y')[f(b'/D')-f(b/D)],                         (7)

and its symmetric counterpart. The second summand is the interface error. For either first-download transition, D increases by one and neither waiting-room numerator increases. Both cutoff factors can only decrease. Since g is nonnegative, **all first-download interface errors are nonpositive**, irrespective of the magnitude of a or b.

An arrival changes just one cutoff, by at most ell/D, and hence contributes at most ell G/D times its rate to the interface error.

At a departure D>=2 and D decreases by one. For a fixed waiting-room numerator w, the cutoff difference satisfies

 0<=f(w/(D-1))-f(w/D)<=2 ell/D.                      (8)

Indeed it is zero if w/D>=eta. Otherwise w<eta D, and the Lipschitz bound is ell w/[D(D-1)]<=ell eta/(D-1)<=2ell/D. There are two cutoff factors, with post-jump g-values at most G, so the total interface error per departure is at most 4ell G/D.

Consequently the global product estimate is

 LJ <= f(b/D)Lg(y)+f(a/D)Lg(x)
       +ell G(lambda+4d)/D.                        (9)

For D=1 there are no departures, so (9) holds there too. Also, without any large-D restriction, first downloads make each J term nonincreasing. An arrival can increase J by at most G, and a departure can increase it by at most 2G. Thus

 LJ<=G(lambda+2d)                                   (10)

globally. Estimate (10) will handle a bounded visible population with arbitrarily many waiting peers.

Notice that (9) is a pointwise inequality for the actual six-rate generator. The unfavorable first-download rates do not appear in its error term. This is the step which makes the interface cost controllable.

## 5. Negative drift in the three exhaustive regions

Choose a finite integer N large enough that

 N>=R+2,
 N>=3(R+1),
 (1-eta)N-(1+eta)R-eta>=m,
 N>=ell G[lambda+4(2R+1)].                           (11)

### Region I: both visible chunk counts are large

If min(x,y)>=R+1, both g-values and every one-step successor g-value vanish. Therefore LJ=0 exactly. Also d>=min(x,y): for x>=y,

 D(d-y)=y(x-y)+x>=0,

and the other case is symmetric. From (2) and (3),

 LV<=beta+c-q(R+1)<-2.                              (12)

### Region II: one visible chunk count is bounded and the other is large

By symmetry it suffices to take y<=R and x>=N. Because x>=R+2, the J_Y term and all its one-step successor values vanish. We have

 d<=2R+1,
 (x-y)/D>=1/2,
 qd>=y.                                            (13)

For the last assertion, x>=3(y+1) gives x/D>=3/4 and

 d>=(2y+1)x/D>=(3/4)(2y+1),

so qd>=(21/32)(2y+1)>=y. The interface remainder in (9) is at most one by (11), since D>=N. Moreover (5), multiplied by f(b/D), gives

 f(b/D)Lg(y)<=f(b/D)(y-mu),                         (14)

including f=0.

If b/D>=eta, then f(b/D)=1. Combining (2), (9), (13) and (14) gives

 LV<=beta-u-q d+c+y-mu+1
    <=beta+c-mu+1<-3.                              (15)

If b/D<eta, then

 Z=a+x-b-y >= (1-eta)x-(1+eta)y-eta>=m

by (11). Hence the final term in (2) is at most -c/2. Since f(y-mu)<=y and qd>=y,

 LV<=beta-u-c/2+1=-3-u<=-3.                         (16)

Thus all of Region II has strictly negative drift. The argument includes the entire cutoff transition band; no free switching cost is omitted.

### Region III: the visible population is bounded

The remaining states satisfy min(x,y)<=R and max(x,y)<N, so n=x+y<=N+R. Since d<=n, equations (2) and (10) imply

 LV<=beta+c+G[lambda+2(N+R)]-u.

Since

 u=[a(x+1)+b(y+1)]/D>=(a+b)/(N+R+1),

put

 B=(N+R+1){beta+c+G[lambda+2(N+R)]+1}.              (17)

Then LV<=-1 whenever a+b>B in this last region.

The set

 F={ (a,b,x,y): x+y<=N+R, a+b<=B }

is finite. Equations (12), (15), (16) and (17) show that

 LV<=-1 outside F.                                  (18)

All constants depend only on the fixed lambda and are finite. No uniformity as lambda tends to infinity is claimed or needed.

## 6. Recurrence conclusion

For completeness, the chain is nonexplosive: on a finite time interval arrivals are dominated exactly by a Poisson(lambda) process, and each initial or arriving peer makes at most two download transitions. There are therefore at most twice the initial population plus three times the arrival count actual jumps. All finite-state rates are finite.

For lambda>0 the chain is irreducible. Any finite state can reach the empty state via a prescribed finite sequence of downloads and departures, each with positive rate because of the permanent seed. Conversely arrivals and prescribed first downloads build an arbitrary finite state from the empty state. Each such finite event sequence has positive probability.

Stop Dynkin's identity for V at the first hit of F, at time t and at a finite population level. On this localized finite state set every term is legitimate. Inequality (18) and V>=0 imply that the expected localized stopped time is at most V(s). Nonexplosion removes the population cutoff; Fatou and then monotone convergence yield

 E_s tau_F<=V(s),      s outside F.

The finite-set Foster criterion for irreducible countable-state continuous-time chains gives positive recurrence. Alternatively, the finitely many exit neighbors of F have uniformly finite V, so finite-set return times have finite mean, and irreducibility gives a finite-mean return cycle to any chosen state. This proves the theorem.

## 7. What changed from turn 3

Turn 3 supplied finite Poisson corrections in local majority/cohort sectors and expected exits in complementary biased sectors. Their interface cost was the gap. Turn 4 introduces a workload term, a rounded cohort imbalance, and monotone ratio cutoffs. Their first-download interface costs have the correct sign. All remaining interface costs are bounded by a constant times (lambda+d)/D, which tends to zero precisely on the one-chunk boundary where a correction is needed; both corrections vanish when both chunk counts exceed R. This gives one global Foster function and closes the stated all-load conjecture, subject to independent review of this proof candidate.

**Author count:** 4/5 substantive turns. **Best-guess completion:** 95% pending independent adversarial review and source/model verification. **Remaining mathematical gap identified by the author:** none in the displayed proof; external validation is pending. No GitHub changes have been made during this resumed turn.
