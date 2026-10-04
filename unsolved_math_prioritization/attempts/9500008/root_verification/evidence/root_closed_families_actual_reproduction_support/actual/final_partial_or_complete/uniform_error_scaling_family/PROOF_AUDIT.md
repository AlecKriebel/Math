# Adversarial uniform-error and scaling audit

Frozen candidate: head `652b8115080e5e97b2274cb602de3faf8c551f20`, base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; `PARTIAL.md` SHA-256 `3ad42fdecc5a30ef00d6fec6c18d1f2b8299be999d609711459bb67823af9bc1`. Independent mechanism was sealed before candidate, old review, or readiness exposure. No sibling audit or root interpretation was read. Original substantive attempts: 2 of 5; new substantive attempts: 0; audit substantive attempts: 0.

**Verdict for this family: the displayed pathwise approximation and diffusive-limit claims are valid in their stated full nonidentical bounded-piece scope. Mandatory mathematical repairs: none.** This is an unrefereed probability audit, not an exact-shift solution or a novelty certificate. The probabilistic argument, not the finite diagnostics, establishes the conclusion.

## Operative assumptions and target

[The author's Problem 8](https://sites.math.washington.edu/~burdzy/open_mathjax.php) specifies independent stopped pairs, not iid pairs; nonnegative finite stopping times, possibly zero; divergence of duration sums in both directions; and one deterministic finite constant c with T_k<c almost surely for every integer k. The countable intersection makes all those inequalities simultaneous almost surely. Necessarily c>0. Each Brownian motion must be Brownian relative to the filtration for its stopping time; arbitrary anticipative cuts are not allowed. The negative chronological locations S_k themselves are not asserted to be stopping times.

The actual target permits a random real origin S: the two centered outward half-paths at that origin must be independent standard Brownian motions. There is no requirement that S be an endpoint or stopping time. A deterministic-origin weak scaling limit does not supply S. The extracted literal record lacked this definition; the current primary page resolves the omission. Dated triage remains quarantined and does not establish novelty or exhaustive current literature status.

## Brownian-law import and independent coverage

Standard imports are Brownian symmetry, the strong Markov property at an almost surely finite stopping time, reflection for the maximum on a deterministic finite interval, and Brownian scaling. The symmetry/scaling statements also follow immediately by checking Gaussian increments and path continuity. [Mörters–Peres, Brownian Motion](https://www.stat.berkeley.edu/~aldous/205B/bmbook.pdf), Lemma 1.7 and Theorems 2.14, 2.16–2.18 (printed pages 25 and 47–49), supplies the operative results and proofs. I inspected those portions, not the entire book. Filtration enlargement by independent earlier pieces preserves the Brownian property. No time reversal at a stopping time is imported.

For completeness the finite-to-infinite splicing deduction is as follows. Take finitely many independent stopped pairs in a specified forward order, and append a fresh independent Brownian continuation. A stopped Brownian path followed by an independent fresh Brownian has the original whole-path law by strong Markov. Apply this backwards from the last piece: the suffix is Brownian and independent of the preceding stopped pair, so appending it preserves the law. This proves the finite concatenation has Brownian law even when pair laws vary. It uses only stopped-pair independence; unobserved original tails need not be independent. The continuation is an auxiliary law-check device and is not required in the actual coupling.

Let A_j=sum_{i=1}^j T_{-i}. The finite j-piece concatenation agrees with the actual infinite concatenation through A_j. For each L, P(A_j<=L) tends to zero by almost sure divergence. Thus their restrictions to C([0,L]) have total-variation distance at most P(A_j<=L), using this direct coupling. The infinite path is Brownian on every finite interval and therefore on the half-line. A finite index covers each compact interval even with zeros; conditioning on which pieces are positive is unnecessary. The same argument proves the positive half of X is Brownian. Negative and nonnegative stopped-pair sigma-fields are independent, so their resulting entire half-paths are independent.

## Exact pathwise identity, temporal coverage, and tails

Set W on the negative outward clock by concatenating -B^{-1}, -B^{-2}, ... in their original internal forward direction. At negative junctions W(A_j)=X(-A_j). With a=A_{j-1}, T=T_{-j}, and 0<=u<=T, direct endpoint subtraction yields

    X(-(a+u)) = W(a)+W(a+T)-W(a+T-u),
    X(-(a+u))-W(a+u)
      = [W(a+T)-W(a+T-u)]-[W(a+u)-W(a)].

Each bracket involves two times separated by u<=T<c. If a+u<=R, all four times lie in [0,R+c], including the unseen end of a piece cut by R. Hence the exact bound is 2 omega_W(c;R+c). Repeated zero-duration endpoints agree, and their pathwise error is zero. A zero piece is never assigned a positive-length interval. The negative endpoint a+T is generally anticipative on X's forward clock; the proof uses no Markov property there. W's law is checked by running the original stopped pieces forward, rather than claiming that their internally reversed paths are Brownian.

For R_m=c2^m, each pair of times separated by at most c in [0,R_m+c] lies in [jc,(j+2)c] for one integer 0<=j<=2^m+1. This slightly redundant deterministic cover has 2^m+2 windows. If its increment exceeds r, at least one endpoint has absolute displacement >r/2 from W(jc). Reflection and Brownian symmetry yield

    P(sup_{0<=u<=2c}|W(jc+u)-W(jc)| > r/2)
      <= 4 P(N(0,2c)>r/2)
      <= 4 exp(-r^2/(16c)).

The final Gaussian inequality follows from the normal moment generating function and Markov's inequality, optimized at the threshold divided by variance. Union over the deterministic windows gives exactly the candidate's inequality (6). The windows overlap and are dependent; a union bound needs no independence. There is no bound on the random number of pieces and none is needed.

With r=8 sqrt(cm), the exceptional probabilities are at most 4(2^m+2)e^{-4m}. For m>=1 this is <=8(2e^{-4})^m. The first four terms in exp(4)'s Taylor series already total 71/3>16, so 2e^{-4}<1/8. The summable geometric majorant is 8(1/8)^m, with sum 8/7. First Borel–Cantelli follows directly from P(union_{m>=n} E_m)<=sum_{m>=n}P(E_m)->0; independence is unnecessary. It gives the bound for all sufficiently large dyadic m on one probability-one event. Monotonicity extends the bound to every real R between successive radii, and m is at most a c-dependent constant times log(2+R) for large R. This proves O(sqrt(log(2+R))) uniformly on the expanding interval [-R,R].

An eventual multiplicative constant can be chosen deterministic with a sample-dependent finite starting radius. An all-radius bound can absorb the finite initial interval into a sample-dependent constant. The candidate only claims almost-sure big-O as R grows and allows sample dependence, which is valid. It does not claim one uniform constant over all samples, all c, or all translated windows. Tiny durations can produce arbitrarily many pieces in a short interval; the cover is in physical time, so this does not affect the proof.

## Scaling topology and its precise limitation

Define Z(t)=X(t) for t>=0 and Z(-u)=W(u) for u>=0. The independent halves give Z the deterministic-origin two-sided Brownian law. For each finite L>0,

    sup_{|t|<=L} |r^{-1/2}X(rt)-r^{-1/2}Z(rt)|
      <= C(omega,c) sqrt(log(2+rL))/sqrt(r) -> 0 almost surely.

At L=0 the error is identically zero. Brownian scaling gives r^{-1/2}Z(r .) the required law for every r; Slutsky's metric-space argument gives the candidate's weak convergence in C([-L,L]) with the uniform norm. One can strengthen the topology to C_loc(R): use the metric sum_{n>=1}2^{-n} min(1,||f-g||_{[-n,n]}). On the same probability-one event every finite-n distance vanishes, and the metric's tail is deterministically small. Constant comparison law plus metric closeness gives weak convergence, for example by testing bounded Lipschitz functions.

Brownian scaling is equality in distribution, not convergence on the original Brownian sample. Already B(r)/sqrt(r) and B(2r)/sqrt(2r) have difference variance 2-sqrt(2)>0 for every r. Their nondegenerate fixed Gaussian difference cannot tend to zero in probability, so this family is not Cauchy in probability and cannot converge almost surely. The candidate correctly claims only weak convergence of the scaled X, while the X-versus-scaled-Z distance vanishes almost surely.

The coupling changes the interior of negative pieces. It does not establish exact equality after one finite time translation. Neither the coupling nor Brownian windows moving rightward establishes the random-origin property on the whole original path. The exact finite-shift target remains unresolved.

## Adversarial checks and reproducibility scope

`original_replay_receipts.json` compares entire generated JSON and raw bytes against the frozen receipts, preserves stdout and stderr, and records interpreter/dependency failures. The original executable source is retained unchanged under `frozen_original/` and `original_replay/`. Full submitted replay is byte-identical, not merely an agreement of pass counts. The previous independent verifier is also replayed in its documented SymPy version; any earlier missing-dependency attempt is preserved.

The new controls use exact fractions, finite enumeration, Gaussian covariance algebra, and rational tail majorants. They include zero/tiny pieces, horizons cutting through pieces, incorrect interior sign, incorrect tail rate, omitted boundary enlargement, dropped independence/divergence/uniform boundedness, the unwarranted almost-sure Brownian scaling limit, and an unwarranted uniform translated-window assertion. Whole mutated prose and programs, exit codes, receipts, stdout and stderr are retained. Their scope is explicit: controls check algebra and falsify weakened or strengthened variants; they do not replace the Brownian-law proof above.

The omitted-enlargement falsifier is also probabilistic, without relying on simulation or a zero-probability exact curve. Take the deterministic stopping duration T=1<c=2 and H=1/4. The event sup_{[0,H]}|W|<=1 has positive probability, since reflection/Chernoff bounds its complement by 4e^{-2}<1 (exp(2)>5). Independently the future increment W(1)-W(3/4)>6 has positive Gaussian probability. On their intersection, the interior error at H is greater than 5, whereas twice the past-only modulus is at most 4. Thus replacing R+c by R is actually false for a Brownian piece. The retained rational curve is a separate exact algebra witness.

Similarly the hypothesis controls have explicit mechanisms. Reusing one Brownian unit piece violates independence and makes the time-2 value have variance 4 rather than 2. Durations 2^{-j} violate divergence and stop covering time after their finite sum 1. Deterministic durations T_j=2^j violate only uniform boundedness among the relevant duration hypotheses: at u=T_j/4 the error is Gaussian with variance T_j/2, independent between pieces, and fixed-positive-probability threshold events occur infinitely often. The logarithmic rate cannot survive, since sqrt(2^j)/sqrt(j) diverges. For the all-origins upgrade, even deterministic duration 1/2 yields independent nondegenerate interior Gaussian errors, whose absolute maximum over all pieces is infinite almost surely. For these independent constant-probability events, the infinitely-often conclusion follows directly from (1-p)^n tending to zero on every tail; no empirical inference is made.

No mandatory mathematical correction is found in the frozen approximation theorem. Preserve its unresolved full-target disposition and lack of novelty claim. This family does not audit the detailed iid renewal theorem, historical priority, or the full proof of the published finite-moment counterexample; those imports are not needed for the proved uniform-error theorem.
