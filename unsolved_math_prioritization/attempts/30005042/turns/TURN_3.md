# Turn 3: exact X log X controls and a logarithmic functional theorem

**Substantive author turn3/5, scoped partial, not independently reviewed.** The original exact-endpoint functional and simple-process-description questions remain unresolved. This turn proves endpoint statements about the actual source coupling, and strengthens the sufficient functional moment condition from a power above one to a logarithmic moment of every order strictly above two. Classical symmetrization, truncation, martingale and geometric-series methods retain credit; no novelty is asserted.

## 1. Setup and results

Retain the source's nondecreasing càdlàg integer offspring process X with E X(lambda)=lambda on I contained in(1,infinity), independent copies X_(n,i), and

    Z_(n+1)(lambda)=sum_(i<=Z_n(lambda)) X_(n,i)(lambda),
    W_n(lambda)=lambda^(-n) Z_n(lambda),     Z_0=1.

Fix a nontrivial compact[a,b] contained in I, and put Y=X(b). Each generation's endpoint copies are Y_(n,i)=X_(n,i)(b). Let F_n contain all generations strictly before n. In particular Z_n is F_n-measurable and all copies in generation n are independent of F_n.

Under the exact endpoint assumption

    E[Y log(e+Y)] < infinity,                                      (L)

the following hold:

1. The normalized maximum of every active endpoint offspring envelope vanishes uniformly:

    sup_(lambda in[a,b]) max_(i<=Z_n(lambda)) Y_(n,i)/lambda^n ->0
       almost surely.                                             (1.1)

   The maximum over an empty set is zero. This concerns a single active family's envelope, not an aggregate jump caused by activating several parents.

2. A generation-dependent truncation produces centered innovations D_n with

    sum_(n>=1) E ||D_n||_infinity² < infinity.                      (1.2)

3. For the actual normalized population process,

    sum_(n>=1) ||W_(n+1)-W_n||_infinity² < infinity
       almost surely.                                             (1.3)

   In particular consecutive generations become uniformly close. This is not a proof that the sequence is uniformly Cauchy or J1-tight.

Under the stronger, but still purely logarithmic, local assumption

    for every compact[a,b], some epsilon>0 satisfies
    E[X(b) log(e+X(b))^(2+epsilon)] < infinity,                     (Q)

the full functional conclusion does follow: W_n converge almost surely locally uniformly to a càdlàg W, and in expected supremum norm on each compact. Therefore they converge almost surely in local J1. No moment above one and no increment regularity are needed in this sufficient theorem.

## 2. The moving parameter partition

For each n>=1 set J_n=ceiling(n log_2(b/a)), at least1. Use endpoints

    alpha_(n,j)=a 2^(j/n),
    beta_(n,j)=min(b,a 2^((j+1)/n)),     0<=j<J_n,
    t_(n,j)=alpha_(n,j)^n=a^n 2^j.

These intervals cover[a,b], and

    beta_(n,j)^n <= 2 t_(n,j).                                   (2.1)

Boundary points may occur in both intervals, which causes no problem for the upper bounds. This mesh shrinks with n; it is not a fixed partition whose endpoint growth ratio would become exponentially large.

All suprema used below are measurable. At a fixed generation there are only Z_n(b)<infinity many active offspring copies. The relevant functions are càdlàg, so a countable dense set together with b determines their suprema.

## 3. Large active envelopes are summably rare under(L)

Fix eta>0. If for some lambda in an interval[alpha,beta] and some i<=Z_n(lambda) one has Y_(n,i)>eta lambda^n, then

    i<=Z_n(beta),     Y_(n,i)>eta t_(n,j).

Independence of the new copies from F_n, followed by E Z_n(beta)=beta^n, gives

    P(sup_lambda max_(i<=Z_n(lambda)) Y_(n,i)/lambda^n >eta)
       <=2 sum_(j<J_n) t_(n,j) P(Y>eta t_(n,j)).                    (3.1)

For fixed y, the geometric sum of t=a^n 2^j with t<y/eta is less than2y/eta. There are at most log^+(y/eta)/log(a) eligible positive integers n. Tonelli therefore bounds the sum over all n of(3.1) by a constant depending on a and eta times E[Y(1+log^+Y)]. It is finite under(L).

Borel–Cantelli, applied to every eta=1/r with r a positive integer, proves(1.1). No independence between these generation events is needed. The bound uses the envelope X(b), so it is valid without independent parameter increments or assumptions about where the offspring jumps occur.

## 4. Monotone generation-dependent truncation

Define

    U_(n,i)(lambda)
       =X_(n,i)(lambda) 1_(Y_(n,i)<=lambda^n),
    mu_n(lambda)=E[ X(lambda) 1_(Y<=lambda^n) ],
    r_n(lambda)=lambda-mu_n(lambda)>=0,

and

    D_n(lambda)=lambda^(-n-1)
       sum_(i<=Z_n(lambda)) [U_(n,i)(lambda)-mu_n(lambda)].          (4.1)

The truncation is increasing in lambda, not decreasing. Thus each U_(n,i) is nonnegative, nondecreasing and càdlàg, even though the cutoff depends on its own endpoint Y_(n,i). This dependence is within one process; independence between different i is preserved. Conditional on F_n, multiplying it by the known increasing activation indicator 1_(i<=Z_n(lambda)) preserves these properties and independence. Its conditional mean is the same indicator times mu_n(lambda).

Use Turn2's proved maximal inequality at p=2, with constant16. On a partition interval[alpha,beta], the endpoint square of a truncated copy is at most

    Y² 1_(Y<=beta^n).

Conditioning on F_n and then averaging gives

    E ||D_n||_infinity,[alpha,beta]²
       <=16 alpha^(-2n-2) beta^n E[Y² 1_(Y<=beta^n)]
       <=(32/a²) t_(n,j)^(-1) E[Y² 1_(Y<=2t_(n,j))].              (4.2)

Only the first moment E Z_n(beta)=beta^n is used, not a second moment of the population. The full supremum squared is at most the sum of the interval suprema squared.

For fixed y>=0, extending the j sum to infinity gives the elementary bound

    sum_(j>=0) y²/(a^n 2^j) 1_(y<=2a^n 2^j)
       <=4 min(y²/a^n,y).                                       (4.3)

Indeed the geometric tail starts at the first t>=max(a^n,y/2). Consequently, if

    B_n=E[Y min(Y/a^n,1)],

then

    E ||D_n||_infinity² <= (128/a²) B_n.                          (4.4)

For an integer y>=1 and q=floor(log_a y),

    sum_(n>=1) min(y²/a^n,y)
       <=y [q+a/(a-1)].                                         (4.5)

Split at n=q and sum the remaining geometric series. At y=0 both sides vanish. Equations(4.4)–(4.5) and Tonelli prove(1.2) under(L).

For each fixed parameter D_n has conditional mean zero given F_n. Its cumulative sums are therefore martingales there. This does not automatically give a supremum-norm martingale convergence theorem on the whole parameter interval.

## 5. Actual generation increments at the endpoint

Write b_n=E[Y 1_(Y>a^n)]. It is deterministic, nonincreasing, and

    sum_(n>=1) b_n <= E[Y log^+Y]/log(a) < infinity.               (5.1)

By Section3 with eta=1, almost surely there is a finite random n_0 such that for all n>=n_0 and every lambda, every active copy satisfies Y_(n,i)<=lambda^n. The actual discarded sum then vanishes simultaneously over the interval. Hence

    W_(n+1)(lambda)-W_n(lambda)
       =D_n(lambda)-[r_n(lambda)/lambda]W_n(lambda),
    0<=r_n(lambda)<=b_n.                                        (5.2)

Set M_n=||W_n||_infinity and d_n=||D_n||_infinity. Positivity of W_n and r_n gives

    M_(n+1)<=M_n+d_n,    n>=n_0.

Equation(1.2) implies sum d_n²<infinity almost surely. Cauchy–Schwarz therefore gives M_n²=O(n) on this probability-one event. Moreover

    sum n b_n² <= (sum b_n)² < infinity,                         (5.3)

since n b_n <=sum_(k<=n)b_k by monotonicity. Squaring(5.2) and summing its supremum norm bounds now proves(1.3). The finitely many earlier increments are finite almost surely and do not affect this conclusion.

The conclusion is almost-sure square summability, not an assertion of finite expected squared norms for the original increments; the untruncated offspring may have infinite variance.

## 6. Full functional convergence with a logarithmic moment above two

We prove the stronger absolute-summability estimate under(Q):

    sum_(n>=1) E ||W_(n+1)-W_n||_infinity < infinity.             (6.1)

First, for any epsilon>0, splitting at floor(log_a y) and estimating the geometric tail as in(4.5) gives

    sum_(n>=1) n^(1+epsilon) min(y²/a^n,y)
       <=C_(a,epsilon) y log(e+y)^(2+epsilon).                   (6.2)

For completeness, below the split the sum of n^(1+epsilon) is bounded by a constant times (1+log y)^(2+epsilon). Above it, write n=q+k; the convergent sums of a^(-k) and k^(1+epsilon)a^(-k) bound the remainder by a constant times y(1+q)^(1+epsilon). Thus(6.2) needs no power moment of y.

Equations(4.4), Cauchy–Schwarz and(6.2) yield

    sum E||D_n||_infinity
       <=sqrt(128/a²) sum sqrt(B_n)
       <=sqrt(128/a²)
          [sum n^(1+epsilon)B_n]^(1/2)
          [sum n^(-1-epsilon)]^(1/2) < infinity.                 (6.3)

It remains to control the centered discarded part C_n, defined by the exact identity

    W_(n+1)-W_n=D_n+C_n.

On[alpha,beta], its uncentered nonnegative sum is bounded by

    alpha^(-n-1) sum_(i<=Z_n(beta)) Y_(n,i) 1_(Y_(n,i)>alpha^n).

The absolute value of its conditional-mean term has the same expected bound. Thus

    E||C_n||_infinity
       <=(4/a) sum_(j<J_n) E[Y 1_(Y>a^n 2^j)].                  (6.4)

For a fixed y, the number of integer pairs n>=1,j>=0 with a^n 2^j<y is at most

    (1+log^+y/log a)(1+log^+y/log2).

Tonelli bounds the sum over n of(6.4) by C_a E[Y log(e+Y)²], which is finite under(Q). Combining this with(6.3) proves(6.1).

Tonelli now gives almost-sure absolute summability of the supremum increments. Consequently W_n converge uniformly, almost surely and in expected supremum norm on[a,b]. Their limit is càdlàg. Taking a countable compact exhaustion gives locally uniform convergence and hence local J1 convergence. At every fixed parameter it agrees almost surely with the mean-one scalar martingale limit. The interval-dependent epsilon and constants cause no problem for this countable-local conclusion.

This genuinely extends Turn2. For example, let an integer Y>=2 have tails

    P(Y>=m)=2(log2)^5/[m(log m)^5],    m>=2.

It has finite E[Y log(e+Y)^3] but no moment E Y^(1+delta) for any delta>0, by the tail-sum test. With mu=EY and an independent rate-one Poisson process P, the source-admissible process X(lambda)=Y+P_(lambda-mu), lambda>mu, has finite local third logarithmic moments and no moment above one. The present theorem applies; Turn2's power-moment theorem does not.

The earlier tail with logarithmic denominator power3 still has finite X log X but does not meet(Q). No assertion about its full functional limit is made here.

## 7. Why square-summable uniform innovations do not close the endpoint

The remaining issue is control of the *cumulative* innovations as functions, not large individual families or single consecutive-generation differences. The following countercontrol shows that even nonnegative continuous-parameter martingales with strong pointwise bounds need more than square-summable supremum increments. It is deliberately not asserted to be a branching-process counterexample.

On the ternary Cantor set choose the continuous digit-sign functions rho_k with values in{-1,1}, and extend each continuously to[0,1] by linear interpolation on complementary intervals. Every finite sign pattern is attained on the Cantor set, and |rho_k|<=1 everywhere. Let epsilon_k be independent fair signs, H_n=sum_(j=1)^n1/j, and for n>=2 put

    F_n(t)=product_(k=2)^n [1+epsilon_k rho_k(t)/(k H_(k-1))],
    F_1(t)=1.

For every fixed t this is a nonnegative mean-one martingale. Its second moment is bounded uniformly in n and t, since

    E F_n(t)² <= product_(k=2)^n [1+1/(k H_(k-1))²]
       <=exp(sum_(k=2)^infinity 1/k²)<infinity.

However, choosing all the favorable digit signs shows exactly

    ||F_n||_infinity=product_(k=2)^n H_k/H_(k-1)=H_n,
    ||F_n-F_(n-1)||_infinity=1/n.

Thus the squared supremum increments are summable, while the supremum diverges deterministically. The laws are not J1-tight, since every J1-compact set has bounded supremum norm. This family does not satisfy the source's monotone-population branching recursion. It only rules out an invalid general functional-martingale inference from(1.3).

## 8. Process-law information and remaining gap

Under(Q), Turn1's finite-dimensional uniqueness now determines the law of the existing càdlàg limit on D(I): coordinate evaluations on a countable dense set generate its Borel sigma-field. The usual finite-child root decomposition gives its process smoothing equation. This is a rigorous abstract process-law characterization in a wider weak-moment class.

It is not the source's requested simple description of the binary, geometric or Poisson limit processes. Those models already have strong moments; restating their smoothing equation does not answer that part of the problem.

The exact X log X functional endpoint and the simple-model description remain open in this attempt after3/5 turns. Possible next work is a genuinely branching-specific cumulative-innovation estimate, or an admissible endpoint counterexample. No unqualified complete-result status is justified by this checkpoint.

## 9. Controls and attribution

The proof uses the exact source coupling and the Turn2 maximal lemma, with independent-copy conditioning checked again above. The finite checker separately tests moving-grid arithmetic, tail counting, monotone adaptive truncation, conditional centering, square-summability estimates and the generic martingale countercontrol. These controls are finite diagnostics, not proofs of the infinite sums or a source counterexample.

The primary Mailler–Marckert/OWR and Kesten–Stigum sources and final-text access caveat remain those recorded in the earlier source gate. This turn introduces no additional external theorem beyond the explicitly proved estimates and classical finite martingale/summability facts.
