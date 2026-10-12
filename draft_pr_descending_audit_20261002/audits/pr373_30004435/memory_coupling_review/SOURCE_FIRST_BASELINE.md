# Independent source-first reconstruction: memory coupling

This document was written before reading candidate mathematics, programs,
receipts, old reviews, or another audit's proof. The only candidate files read
before this document's seal were SOURCE_MANIFEST.json and TURN_3_SOURCE.json,
used solely for source locators and hash metadata. The frozen candidate head
specified by the parent is 4e635c77d7399d671ea58700e41bbd92cbdeeb46.

## Exact target and source boundary

The target is a probability-only proof, without entropy, of equality modulo
null sets of the past and future tails for **every stationary finite-alphabet
process**. Equality itself is stated as known in Steif's Question C, EMS Report
11/2020, PDF page 32, printed page 632. A proof imposing additional continuity,
overlap, irreducibility, or mixing assumptions leaves the target gap open.

Al-Najjar/Shmaya, arXiv:1406.6670, PDF pages 13-14, states the completed-tail
identity, credits an entropy argument, and gives an infinite-outcome failure.
Bressaud/Fernandez/Galves, arXiv:math/9806132, supplies the normalized-chain
definitions (PDF pages 2-5), maximal-coupling and agreement-length machinery
(pages 6-8), and return renewal formulas (pages 10, 13-15). Its weaker condition
for coordinate relaxation is distinguished from the summable regime.

Fresh bytes were downloaded directly from each primary URL. Critical EMS page
32, Al-Najjar/Shmaya pages 13-14, and BFG pages 7, 8, 10 were rendered and
visually inspected. Extracted text and renders remain ignored private material.
Source URLs, fresh hashes, retrieval times, and read locators are in the seal.

## Definitions and claim reconstructed independently

Let A be a finite alphabet, H=A^{Z_{<=0}}, and let g(a|h) be a measurable
probability vector for **every** h in H. A stationary two-sided law mu is
compatible with g when g is a version of its conditional next-symbol law.
No existence assertion is needed: the theorem below assumes such a law exists.

Use TV(p,q)=(1/2) sum_a |p(a)-q(a)|. Set

    eta = inf_{h,h'} sum_a min(g(a|h),g(a|h')) > 0;
    v_m = sup_{h,h': same last m symbols} TV(g(.|h),g(.|h'));
    b_0 = 1-eta;  b_m = min(1-eta,v_m)  (m>=1).

Assume sum_{m>=1} v_m < infinity. Because the sets of admissible pairs shrink,
v_m and b_m are nonincreasing. Thus 0<=b_m<=b_0<1 and sum_m b_m<infinity.
If the v_m are only supplied upper bounds, a nonincreasing upper bound must be
specified or justified before using the domination below. For true moduli the
monotonicity is automatic. With all-histories uniform bounds the infimum need
not be attained.

**Scoped theorem.** Under these hypotheses:
(i) any two fixed histories can be coupled so their generated futures disagree
only finitely often almost surely, with a history-independent last-failure tail;
(ii) TV between the full futures starting at n tends to zero uniformly in both
histories; (iii) every stationary compatible law has trivial completed past and
future tails, hence those completed tails coincide. This is a subclass theorem.

## Maximal coupling, including zero probabilities

For p,q put d_a=min(p_a,q_a), t=1-sum d_a=TV(p,q). If t=0, take only the
diagonal matrix M(a,a)=p_a. If t>0 take

    M(a,a)=d_a;
    M(a,b)=(p_a-d_a)(q_b-d_b)/t  for a!=b.

The residual supports are disjoint; hence the off-diagonal formula has zero
diagonal even if extended to all pairs. Its row sums are p, its column sums q,
and its agreement probability is 1-t. A measurable sampling rule follows from
finite inverse transforms. One uniform chooses whether agreement occurs and
independent uniforms choose the conditional symbols. Pairwise overlap does
not imply a common history-independent minorizing symbol measure: the three
vectors (1/2,1/2,0), (0,1/2,1/2), (1/2,0,1/2) have pairwise overlap >=1/2 but
sum_a inf_h g(a|h)=0. The construction needs only pairwise maximal coupling.

## Pathwise agreement-length domination

At output time t>=1, apply that coupling to the two current history vectors.
Let L_0=0 and let L_t be the number of consecutive generated agreements ending
at t. Given the complete joint past, mismatch probability q_t<=b_{L_{t-1}}.
The process L need not be Markov; the inequality is conditional on the full
coupling filtration. Equal initial history suffixes can only improve the bound.

Use the same independent uniform U_t to choose actual agreement (U_t<=1-q_t)
and to define S_0=0 and

    S_t = S_{t-1}+1 if U_t<=1-b_{S_{t-1}}, else 0.

The S process is a Markov chain. Inductively L_{t-1}>=S_{t-1} implies
q_t<=b_{L_{t-1}}<=b_{S_{t-1}}. If S advances, L advances; if S resets, L>=0.
Consequently L_t>=S_t for every t. In particular every actual mismatch at t
forces S_t=0. This proves the needed **pathwise** implication, not merely
one-time stochastic domination.

## Product, stopping times, and defective renewal

Put

    c = product_{m>=0}(1-b_m) > 0;
    f_j = b_{j-1} product_{m=0}^{j-2}(1-b_m), j>=1.

The empty product for j=1 equals 1. Positivity of c follows by treating finitely
many early factors separately and using -log(1-x)<=2x for all late x<=1/2.
The first strictly positive return to zero has probabilities f_j and probability
c of no return. Thus sum_j f_j=1-c. Define successive **finite return times**
T_1,T_2,..., each a stopping time. Strong Markov at those times makes the
excursion laws independent and identical. The event that an excursion will
never return is not a stopping time, and no strong Markov claim at the last
return or eventual-success time is needed.

If N is the number of positive returns, P(N>=r)=(1-c)^r. Hence N<infinity
almost surely and E N=(1-c)/c. All of its realized finite excursion lengths are
finite, so F=max({t>=1:S_t=0} union {0}) is finite almost surely. This conclusion
is uniform in the two initial histories because S has a fixed law.

Writing u_t=P(S_t=0), u_0=1, the renewal equation is

    u_t=sum_{j=1}^t f_j u_{t-j}, t>=1;
    sum_{t>=0}u_t = sum_{r>=0}(1-c)^r = 1/c.

By conditioning on the event S_t=0 and then using future independent uniforms,

    P(F=t)=c u_t, t>=0;
    delta_n=P(F>=n)=c sum_{t>=n}u_t -> 0, n>=1.

The weaker union bound delta_n<=sum_{t>=n}u_t also suffices. All series
identities have nonnegative terms, so exchanging them uses Tonelli.

## Full infinite future, not only coordinates

Let Q_h be the path law generated by g from history h. The coupled restriction
to [n,infinity) has probability of any discrepancy bounded by delta_n, because
all discrepancies are included among the S returns. For every measurable
future event B the indicator difference is bounded by that discrepancy event.
Therefore

    sup_{h,h'} TV(Q_h|_[n,infinity),Q_{h'}|_[n,infinity)) <= delta_n.

This step works on the full countable product sigma-field, not merely finite
words. Eventual equality gives it directly. In contrast, coordinate discrepancy
probabilities tending to zero do not control the event of **any** later
discrepancy. A simple logical control is P=Dirac at all-zero sequences and
Q=product Bernoulli(1/(t+1)), t>=1. Coordinate TV tends to zero, while every
full future has TV=1, since Q has a 1 somewhere after n with probability one.
This control is nonstationary and is not a counterexample to the scoped theorem.

## Conditional law version, stationary mixing, and completion

The finite-alphabet product space is standard Borel. Conditional on the past,
the compatible stationary process has the successive g transition products,
by the tower property. Use the countable collection of finite words and time
indices to remove a single null set; then cylinder uniqueness proves that Q_h
is a regular conditional law of the entire future for almost every past h.
The all-histories bounds apply to that version, including paths of histories
generated in the coupling. Almost-sure continuity without a coherent
extension stable under those paths would need additional work.

Integrating one side of the pairwise bound gives, for B in F_{>=n},

    |Q_h(B)-mu(B)|<=delta_n

for almost every past h, simultaneously at the level of conditional measures.
For A in F_{<=0} this yields

    |mu(A intersect B)-mu(A)mu(B)|<=mu(A)delta_n<=delta_n.

Thus the past/future alpha coefficient is at most delta_n (and the directional
phi coefficient has the same bound). Stationarity translates this estimate
to any separated cuts. To prove future-tail triviality, take a future-tail
event E and any finite cylinder C whose right edge is m, represent E at every
cut n>m, and let n tend to infinity. The estimate gives independence of E from
C. A monotone class then gives independence from the full process field,
in particular from E, so mu(E)=mu(E)^2. For a past-tail event do the same with
E as the left event and C as the right event. The covariance expression is
symmetric; no time-reversed continuity assumption is asserted or required.

Null representatives do not change any probability in this argument. Also,
for decreasing sigma-fields F_n, an event in every completed F_n has
representatives E_n in F_n differing from it by null sets. The limsup of the
E_n lies in their raw intersection and differs from the original event by a
countable union of null sets. Therefore completing the intersection or
intersecting the completions gives the same completed field here. Each tail
completion is the completed trivial field; hence they coincide.

Nothing in this one-sided mixing proof identifies the **two-sided** tail
intersection_n sigma(X_t:|t|>=n). One cannot split conditioning on a joint
remote past/future into the preceding one-sided estimates. Any bilateral-tail
claim requires a separate argument. The primary target itself warns that
trivial one-sided tails can coexist with a full two-sided tail.

## Expected last-failure time: stronger hypothesis needed

The geometric number of finite returns does not make their lengths integrable.
From the renewal generating series, or summing the independently restarted
defective excursions, the extended-value identity is

    E F = (sum_{j>=1} j f_j)/c.

Since c<=product_{m=0}^{j-2}(1-b_m)<=1, this is finite exactly when
sum_{m>=0}(m+1)b_m<infinity. Under b_m=1/[2(m+1)^2], the unweighted sum is
finite and c>0, but the weighted sum is half the harmonic series. E F=infinity.
The theorem asserts finite F almost surely; it does not assert finite E F.

## Boundary controls and exact remaining gap

* A stationary random constant bit has both tails equal to sigma(Z), nontrivial.
  Its deterministic transition vectors violate eta>0 even though v_m=0 for
  m>=1. This excludes all-stationary universality of the subclass argument.
* A random alternating binary phase similarly violates overlap and has equal,
  nontrivial tails. Irreducible periodic Markov behavior is not covered by an
  aperiodic mixing conclusion without an added assumption.
* Without stationarity, a random constant past followed by an independent iid
  future can have unequal finite-alphabet tails.
* Without finite alphabet the stationary register process X_t=(Z_t,Z_{t-1},...)
  from iid binary Z has a trivial past tail and a full future tail: every remote
  future symbol stores the whole past. This source example validates the target
  boundary and is outside the reconstructed finite-alphabet theorem.

The strongest reconstructed result is the scoped theorem above, with explicit
full-future total-variation convergence and both completed tails trivial.
The exact unsolved gap in this audit is removal of the all-histories overlap
and summable continuity assumptions while retaining an entropy-free proof for
arbitrary stationary finite-alphabet processes. No claim of novelty, current
openness, or peer-review status is made.
