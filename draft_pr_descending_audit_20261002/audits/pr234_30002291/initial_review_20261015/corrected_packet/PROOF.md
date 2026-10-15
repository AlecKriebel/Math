# Quadratic variation limits under bounded pure-jump characteristics

30002291 / OWR-12337-002. **Mathematics verified. Qualified historical
classification: already_solved, because the original open-ended request
already had a substantial sufficient-conditions answer.** Author turn1/5.
This does **not** assert that the exact arbitrary-predictable-kernel theorem
below was proved earlier. Its exact novelty remains unresolved.

No certified new solution of a previously unanswered original target is
claimed. See [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md) for the precise historical
meaning, nonnested classes, mesh qualification and unresolved extension
priority. All17 original files and historical reviews/manifests are preserved
byte for byte under original_submission/. Mathematical Sections2–7 below
are unchanged. The current introduction and disposition supply updated credit.

AI tools were used extensively in solving, checking and auditing. This work
is unrefereed; AI adversarial reviews are not human peer review. This credited
packet is not a preprint and has no Zenodo deposit or tracker entry.

## 1. Known results and exact scope

The original OWR2013 contribution asks for an analogous limit for a rather
general pure-jump semimartingale under sufficient conditions; it defines no
maximal class. A broad adapted scalar-volatility answer is already in
Basse-O'Connor–Heinrich–Podolskij, arXiv1604.02307v2 (14October2016),
Theorem1.2(i), associated with Bernoulli24(4A) (2018),3117–3146,
DOI10.3150/17-BEJ956. At p=2,k=1 the jump coefficients agree exactly,
and reflection of independent uniforms reindexes its phase weight into
W_alpha. The prior result has a functionalM1 statement at its printed1/n
mesh; do not silently attribute an arbitrary-mesh theorem to that statement.

The2015 preprint associated with the2017 AOP paper10.1214/16-AOP1170
supplies the Levy antecedent. A2014 survey already announced that Levy
phase law. The2018 primary general-function preprint arXiv1806.10352,
associated with EJP24 (2019), article79, DOI10.1214/19-EJP336,
Theorem2.1(i) and Proposition2.3(i), formally covers nonsymmetric Levy
drivers below index2. These originals and the established truncation method
must be credited. Exact final-publisher PDF comparison was unavailable;
dated complete primary preprints control the theorem comparisons here.

The verified theorem below permits arbitrary predictable jump kernels and
some finite-quadratic-rate index2 drivers. Those are real distinctions from
the inspected predecessor hypotheses, but do not certify novelty. Its global
moment assumptions also exclude some earlier heavy-tail examples, so the
classes are nonnested. The original question's breadth is qualitative; the
historical catalog judgment concerns a prior substantive affirmative answer,
not proof of complete containment of the present class in an old theorem.

## 2. Driver and kernel assumptions

Work on a filtered probability space indexed by the real line, with the usual completeness and right-continuity conditions. Let mu be the jump measure of a real-valued pure-jump semimartingale driver: it is an integer-valued random measure on `R x (R\{0})`, with at most one nonzero mark at each time. Assume its predictable compensator is

    nu_s(dz) ds,

and that deterministic finite constants B,K satisfy, almost surely for Lebesgue-almost every s in R,

    |b_s| <= B,             integral z² nu_s(dz) <= K,             (H)

where b is predictable. In differential notation the driver is

    dY_s=b_s ds + integral z (mu(ds,dz)-nu_s(dz)ds).              (2.1)

The compensated integral is interpreted in L2 on bounded intervals, with all jumps compensated. Assumption (H) makes this legal, including the large-jump first moment. The notation concerns increments on bounded intervals; no improper integral of the unweighted driver from minus infinity is required. Equivalently one can start with a pure-jump Itô semimartingale with these characteristics. There is no continuous martingale part.

Choose `0<alpha<1/2`, and put

    g(x)=1_(x>0) x^alpha f(x),

where `f in C^1([0,infinity))`, `f(0)!=0`, and there are constants C,c>0 with

    |f(x)|+|f'(x)| <= C exp(-c x),    x>=0.                      (K)

For t>=0 define

    X_t=C0 + integral_(-infinity)^t g(t-s)b_s ds
             + integral_(-infinity)^t integral g(t-s)z (mu-nu ds)(ds,dz).  (2.2)

The first integral is absolutely convergent and the second is an L2 limit over finite past intervals, because g is in L1 and L2 and (H) holds. The random offset C0 may be any almost surely finite variable, since it cancels from increments. One may subtract the convolution's value at0 to use a literal prescribed initial value instead.

Let Delta_n>0 be any deterministic sequence tending to0, and set

    V_n(t)=sum_(i=1)^floor(t/Delta_n) |X_(i Delta_n)-X_((i-1)Delta_n)|².

Let (T_k,J_k) enumerate the jumps of Y on `(0,infinity)`, without repetitions. On an extension of the probability space let U_k be independent uniform[0,1] variables, independent of the entire original sigma field F. Define

    W_alpha(u)=sum_(l=1)^infinity [(l-u)_+^alpha-(l-1-u)_+^alpha]²,
    Z_t=f(0)² sum_(k:0<T_k<=t) J_k² W_alpha(U_k).                (2.3)

### Theorem

Under (H) and (K), for every finite list `0<t1<...<tr`,

    (Delta_n^(-2alpha) V_n(tj))_(j=1)^r
          converges F-stably in law to (Z_(tj))_(j=1)^r.         (2.4)

In particular this is the exact displayed OWR fixed-time limit for this class of drivers. The limit is finite almost surely at every finite horizon. Stable convergence means joint convergence tested against every bounded F-measurable random variable; the fresh uniform phases are independent of all original randomness, including jump sizes and predictable coefficients.

## 3. Deterministic kernel facts

Conditions (K) imply constants Cg such that, for every x>0,

    |g(x)|<=Cg x^alpha,       |g'(x)|<=Cg x^(alpha-1),

and also

    g in L1 cap L2,  g' in L1,
    integral_0^infinity min(x,T)|g'(x)|² dx < infinity            (3.1)

for every finite T. Near zero the last integrand is bounded by a constant times `x^(2alpha-1)`; at infinity it decreases exponentially.

The series W_alpha converges uniformly on [0,1]. For l>=3 the mean value theorem bounds its summand by `alpha²(l-2)^(2alpha-2)`, whose series converges. The first two terms are continuous and bounded. Thus W_alpha is bounded and continuous. Reindexing gives `W_alpha(0)=W_alpha(1)`, so it is also a continuous function of the phase on the one-dimensional torus.

For any Delta>0, horizon T, and 0<=s<=T, let

    k_(i,Delta)(s)=g(i Delta-s)-g((i-1)Delta-s),

where g is zero on the negative half-line. There is a constant Cg,alpha independent of Delta,s,T such that

    sum_(i=1)^floor(T/Delta) |k_(i,Delta)(s)|² <= Cg,alpha Delta^(2alpha).   (3.2)

To see this, write `s/Delta=j+u` with integer j and 0<=u<1. The first two possible nonzero increments are bounded by a constant times Delta^alpha. For every later increment, with index j+l and l>=3,

    |k_(j+l,Delta)(s)| <= Cg Delta^alpha (l-2)^(alpha-1).

Squaring and summing proves (3.2).

For fixed `0<s<t`, the more precise single-impulse formula is

    Delta_n^(-2alpha) sum_(i<=t/Delta_n) |k_(i,Delta_n)(s)|²
          - f(0)² W_alpha({s/Delta_n})  --> 0.                  (3.3)

For the first L increments, scale the arguments by Delta_n and use continuity of f at0; this approximation is uniform in u in [0,1]. The remaining scaled energy is uniformly bounded by a constant times `sum_(l>L)(l-2)^(2alpha-2)`. The time horizon contains all first L increments eventually because s<t. Let n then L tend to infinity. This proves (3.3), including mesh phases approaching either endpoint.

For any eta>0, the scaled impulse energy from grid endpoints later than s+eta tends to0: the same tail bound starts at `l` of order eta/Delta_n. Thus for any finite list of distinct positive jump times, the normalized inner products of the increment vectors of different impulses tend to0. Indeed retain each vector only on a short right-neighborhood of its own jump time, choosing these neighborhoods disjoint. The discarded scaled norms tend to0, the retained vectors have disjoint supports, and Cauchy–Schwarz plus (3.2) controls every remaining cross term.

## 4. Prehistory and absolutely continuous terms vanish

Split (2.2) at time0. The complete contribution of s<0, including all its jumps, has an absolutely continuous modification on [0,T] with square-integrable time derivative almost surely.

For its drift part, the derivative is bounded by `B ||g'||_1`. For the martingale part, its candidate derivative for u>0 is

    D_u=integral_(s<0) integral g'(u-s)z (mu-nu ds)(ds,dz).

The isometry and Tonelli give

    E integral_0^T |D_u|² du
      <= K integral_0^infinity min(x,T)|g'(x)|² dx < infinity.   (4.1)

Stochastic Fubini is justified by this square-integrability bound (Cauchy–Schwarz also gives the required integrated-kernel bound). It identifies the past increment from0 to t with `integral_0^t D_u du`. This defines the claimed absolutely continuous modification. No finite derivative at t=0 is assumed or needed.

For any absolutely continuous A with `integral_0^T |A'_s|² ds<infinity`, Cauchy–Schwarz on each mesh interval gives

    Delta_n^(-2alpha) V_n(A;T)
       <= Delta_n^(1-2alpha) integral_0^T |A'_s|² ds -->0.       (4.2)

Likewise, for a bounded predictable drift h, the future convolution `integral_0^t g(t-s)h_s ds` is absolutely continuous, with derivative bounded by `||h||_infinity ||g'||_1`. Thus it also satisfies (4.2). The assumptions alpha>0 and alpha<1/2 have distinct uses here: integrability of g' and the positive exponent in (4.2), respectively.

## 5. Jump-time phases for a general compensator

Fix epsilon>0 and a horizon T. The count of jumps with `|J|>epsilon` has predictable intensity

    lambda_s^epsilon=nu_s(|z|>epsilon) <= K/epsilon².             (5.1)

It is finite almost surely on [0,T], with expected count at most `KT/epsilon²`. There are no jumps at any fixed deterministic time, since the compensator is absolutely continuous in time.

We need more than nonatomic one-dimensional jump times. For every integer m and every nonnegative Borel h on the ordered simplex, repeated compensation and (5.1) give

    E sum_(0<S1<...<Sm<=T) h(S1,...,Sm)
       <= (K/epsilon²)^m integral_(0<s1<...<sm<=T) h(s1,...,sm) ds1...dsm.  (5.2)

The sum is over ordered distinct jumps of the truncated count. To prove (5.2), compensate the last jump; the sum over strictly earlier jumps is predictable. Bound its last intensity by K/epsilon², and iterate. A monotone-class argument extends the computation from rectangular test functions to nonnegative Borel h.

Consequently, on the event that there are exactly m such jumps, the joint subprobability law of their chronologically ordered times has a Lebesgue density. It is dominated by the factorial measure in (5.2). Multiplying by any bounded F-measurable variable and conditioning on these times still gives an L1 density.

The standard equidistribution argument now applies to any deterministic Delta_n tending to0: if an m-vector S has a Lebesgue density, the phases `{S/Delta_n}` converge stably to m independent uniforms, independent of F and of any F-measurable marks. For completeness, for a nonzero integer frequency vector q, the weighted Fourier coefficient is

    integral a(s) exp(2 pi i q·s/Delta_n) ds -->0,

by the Riemann–Lebesgue lemma, where a is the weighted L1 density. The zero-frequency coefficient is its integral. Trigonometric approximation yields the result for continuous functions on the phase torus, which suffices for W_alpha. Including additional F-measurable marks in the weights and approximating bounded continuous tests by sums of products gives joint stable convergence. Sum over the events with m jumps; the tail in m is controlled by (5.1).

This establishes the independent phases for the general predictable driver. No independent-increment, Poisson, Markov, or Lévy scaling assumption was used.

## 6. Fixed truncation and removal of small jumps

On (0,T], decompose the future driver into

    J^epsilon_t=sum_(0<s<=t, |J_s|>epsilon) J_s,
    M^epsilon_t=integral_(0,t] integral_(|z|<=epsilon) z (mu-nu ds),
    b^epsilon_s=b_s-integral_(|z|>epsilon) z nu_s(dz).

The drift is bounded by `B+K/epsilon`, since `|z|<=z²/epsilon` on the indicated set. By section4, its convolution and the full prehistory make negligible normalized quadratic variation for each fixed epsilon.

The convolution of J^epsilon is a finite random sum of impulses. Formula (3.3), the vanishing cross terms, and section5 give the joint fixed-time stable convergence

    Delta_n^(-2alpha) V_n(X^epsilon;t)
      --> f(0)² sum_(0<T_k<=t, |J_k|>epsilon) J_k² W_alpha(U_k),           (6.1)

where X^epsilon includes the past and drift just described. Almost surely no jump occurs at any of the fixed observation horizons, so indicator discontinuities do not obstruct this step.

The remaining difference is the future small-jump convolution R^epsilon. The martingale isometry, followed by (3.2), yields

    E[Delta_n^(-2alpha) V_n(R^epsilon;T)]
       <= Cg,alpha E integral_0^T integral_(|z|<=epsilon) z² nu_s(dz) ds.  (6.2)

The right side tends to0 as epsilon decreases to0, by dominated convergence and (H), uniformly in n. Dependence of nu_s on the entire past causes no difficulty: the integrands are predictable and the isometry applies to the compensated jump martingale.

For any two increment vectors, the reverse triangle inequality in Euclidean space gives

    |sqrt(Delta_n^(-2alpha) V_n(X;t))
       -sqrt(Delta_n^(-2alpha) V_n(X^epsilon;t))|
       <= sqrt(Delta_n^(-2alpha) V_n(R^epsilon;t)).              (6.3)

Thus the square-root statistics are uniformly close in probability as epsilon goes to0. The limiting sums can all be constructed with the same independent marks U_k. Since

    E sum_(0<T_k<=T) J_k² = E integral_0^T integral z² nu_s(dz)ds <= KT,

and W_alpha is bounded, their tails tend to0 almost surely. The stable converging-together argument applied to (6.1)–(6.3) gives convergence of the square-root vectors: test against a bounded F-measurable variable and a bounded Lipschitz function, first let n tend to infinity for fixed epsilon, then let epsilon go to0 using (6.2) and dominated convergence for the coupled limits. Squaring is continuous, proving (2.4).

## 7. Why the time-density and topology qualifications matter

A deterministic jump time is excluded by (H)'s absolutely continuous compensator. This is substantive. For a single unit jump at a fixed time s>0 and a mesh `Delta_n=s/n`, formula (3.3) gives the deterministic limit `f(0)² W_alpha(0)` at any fixed later horizon. It cannot in general be replaced by an independent uniform phase. For alpha=1/4, `W_alpha(0)>=1`, whereas Cauchy–Schwarz on the increments after the first one gives

    W_(1/4)(1/2)
      <= 2^(-1/2)+ integral_(1/2)^infinity (1/4)² x^(-3/2) dx
      =5/(4 sqrt(2)) <1.

Continuity makes W_(1/4)(U) nonconstant, so this deterministic-time driver disproves an unqualified assertion covering all pure-jump semimartingales. It does not contradict the OWR request for sufficient hypotheses.

The source target is fixed-time stable convergence. The theorem proves that and its finite-dimensional extension. It does not claim J1 convergence of the entire statistic: several microscopic positive contributions near one driver jump need not merge into a single jump in J1. The published LSS theorem already treats this issue using M1 and states the J1 failure. No functional extension beyond the present proof is being promoted here.

## 8. Disposition and limitations

The theorem under its explicit hypotheses passes independent mathematical
reconstruction, three fresh adversarial mathematical families and source-scope
review. The finite controls supplement the analytic proof. Its sufficient
conditions are not necessary or maximal, and no functional topology is
proved here. The restrictions and deterministic-time counterexample in the
preceding sections remain essential.

For the original open-ended request, a substantial earlier semimartingale
sufficient answer exists. The current catalog status already_solved has
that qualified historical meaning. It does not mean that the exact theorem
above is known, nor that every possible generalization of the original
question is settled. Independent priority searches did not establish either
full anticipation or novelty of this exact bounded-rate class. The remaining
question is a separately scoped extension-priority investigation.

Under the active claimed_solved-only publication workflow, skip this
corrected open draft. No new paper, DOI, deposit, tracker row, merge, closure
or PR comment accompanies this credit correction. The broader goal remains
active and incomplete. The original proof and older verdicts remain in the
immutable original_submission archive; current manifests bind this packet.
