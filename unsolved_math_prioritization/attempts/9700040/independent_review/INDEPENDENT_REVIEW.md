# Independent review: 9700040, stationary drift–jump joint law

## Verdict and frozen version

**PASS_COMPLETE_EXPLICIT_JOINT_LAW_SOURCE_TARGET. No mandatory mathematical correction.**

This verdict binds the unchanged first-turn author `PROOF.md`, SHA-256 `c6e7d751931637e0f119cf6ba8adf71462adb321825be5df39f3f67f2ea61dc0`, and `FROZEN_MANIFEST.json`, SHA-256 `16c5c76a0304805610f69e1647dbed4b4ee0cf8a885bed727edd0b913325fa81`. All ten manifest entries and all six reading-source hashes were independently verified. The mathematics, interpretation and checks below were reviewed separately from the author's work. No author proof ingredient was supplied by this reviewer before the freeze.

The accepted result is an explicit convergent formula for every finite collection of **simultaneous stationary particle positions**, together with a finite rational error certificate. The generator, stationary construction, uniqueness, joint combinatorial weights and truncation argument all pass. There is no claim here of a multi-time joint formula, a spatial-index Markov property, an elementary density in general dimension, fast large-index computation, historical novelty, or acceptance by the problem's proposer.

## 1. Exact source and explicitness judgment

The [original problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html), independently reopened on October 1, 2026, specifies positive ordered particles, unit-intensity space-time events, nearest-right jumps when that particle exists, and velocity equal to position. Its requested output is a description of the stationary distribution. It imposes no elementary-density or finite-closed-form requirement.

The candidate gives a concrete description at the level of all joint probabilities: positive sums of factorial determinants, an explicitly known normalization, matrix size bounded by the queried indices, and an explicit deterministic error tending to zero. For rational queries, each requested accuracy is achieved by finitely many rational operations. No unknown limiting rank distribution, stationary function, implicit integral equation, or probability oracle remains. On this interpretation it meets the source target.

This is a source-scope judgment, not a claim that any computable representation would necessarily satisfy every researcher's intended meaning of explicitness. The [1999 paper](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf), Section 5.2, calls its expression for the constants c(i) implicit and does not present a useful general closed form for them. The present packet does not solve that stronger closed-form problem. Its coverage of arbitrary simultaneous joint queries and its certified fixed-size determinant evaluation are the concrete grounds for the positive verdict, rather than an inference from the mere existence of RSK or from the source page's continued listing.

The [1993 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf), Sections 4.1–4.2, already contain the Poisson-arrival representation, coupling argument and two-particle density. These credits in the candidate are correct and important. The review does not certify priority. The narrow current search found the original listing but was not an exhaustive literature search.

## 2. Dynamics, entrance construction and stationarity

The displayed finite-k generator has precisely one integration interval per particle, with length x_i-x_(i-1), and drift coefficient x_i. Events above the last particle have no effect. There is no insertion into this finite projection. Conditional on a finite initial state, the largest coordinate is at most its initial value times the exponential drift factor on any bounded time interval; the number of relevant events is therefore finite. This also proves pathwise uniqueness of the finite event construction.

For the quadrant construction, L(x,t) is finite on bounded rectangles. It is unbounded as x grows at each positive t: successive nonempty horizontal strips allow an increasing chain of any fixed length. Rational t and monotonicity extend the assertion simultaneously to all positive t. A rank threshold is attained at a Poisson spatial coordinate. Distinct spatial coordinates and the fact that adding a single point can increase the chain maximum by at most one give strictly ordered, locally finite Z_i(t). There is no finite accumulation of particle positions.

The pile-top identity used is the minimal-terminal-value identity for increasing subsequences. Its restriction to a bounded rectangle is consistent: a spatially farther-right mark cannot change an existing pile top inside that rectangle. Thus the infinite construction does not illegitimately enumerate infinitely many events in a time strip. Once t is bounded below by a positive value, every finite projection has finite initial coordinates and is localized by the preceding upper bound.

The inverse event transformation is u=x exp(-s), v=exp(s), whose Jacobian determinant is one. Hence the transformed driving field has unit intensity on positive space times all real s. Future s events correspond exactly to v greater than the present exp(s), so future noise is independent of the current state constructed from earlier points. Between jumps, Y_i(s)=exp(s) Z_i(exp(s)) has derivative Y_i(s); the event ordering and nearest-right rule are preserved. This verifies the process, not merely the law of a count at one time.

Finally, under (u,v) -> (exp(a)u,exp(-a)v), the new whole trajectory satisfies Y_new(s)=Y_old(s+a). The quadrant Poisson law is invariant under that area-preserving map. This proves joint-in-time stationarity of the construction, although formula (3) evaluates only its one-time joint particle distribution. It is not the translation-invariant equilibrium of a different Hammersley process.

## 3. Uniqueness and crossing configurations

The synchronous induction does not require the two entire initial configurations to be coordinatewise comparable. After the first i-1 coordinates have coupled, label the smaller current i-th value a and the common previous value b. Before the i-th coordinates meet, a jump of the smaller one would also move the larger one to the same event. A jump of the larger one that does not couple them remains above the smaller value. Therefore their smaller value keeps following a exp(s-tau), and the previous coordinate is bounded above by b exp(s-tau).

The deterministic strip between these bounds has cumulative area (a-b)(exp(s-tau)-1). Every event in that strip forces the remaining pair to meet, unless it met earlier. Its area tends to infinity. At the random coupling time tau the Poisson strong Markov property applies; conditional on the past, a-b is strictly positive. The probability of avoiding this strip forever is zero. Earlier coordinates remain coupled because their evolution is autonomous. Induction gives almost-sure finite coupling for any finite k.

To deduce uniqueness without an unstated ergodicity theorem, start two invariant laws independently and drive both with the common future field. They couple in finite time almost surely, so the total-variation distance of their time-s marginals is at most the probability that coupling has not occurred. It tends to zero; the invariant marginals are unchanged in time and hence equal. Consistency then fixes the infinite locally finite point-process law through all its finite coordinate marginals.

## 4. Joint RSK counting and determinant factors

Condition on counts d_j in the successive spatial strips. Ordering by spatial coordinate makes the time marks a uniform permutation of n letters. Increasing subsequences are precisely northeast chains. The prefix insertion shape has first row equal to L(x_j,1); this is a spatial prefix of the same permutation, not an independent Poissonized shape at each threshold.

For prescribed nested shapes, the recording tableau is counted by the product of standard skew-tableau counts for successive label blocks. Every block has its fixed consecutive labels, so there is no additional binomial factor. The final insertion tableau contributes f^(lambda_final). Dividing by n! gives the conditional uniform-permutation probability. The independent Poisson count probability supplies exp(-x_m) times product Delta_j^d_j/d_j!. Consequently the factor D_1(final/empty), and each increment D_Delta_j(next/previous), have exactly the factorials claimed. I independently checked these weights against direct enumeration of all permutations through size six and arbitrary, including nonmonotone, three-prefix index constraints.

The [skew Jacobi–Trudi formula](https://arxiv.org/pdf/math/0107056v3), Section 2.2.4 equations (7)–(8), and the [exponential specialization](https://www.math.umb.edu/~vuletic/Site/Research_files/PSASP.pdf), Section 6.3 equation (6.6), give the stated determinant and positivity. The sign of the index lambda_i-mu_j-i+j is correct. Extra zero padding adds a lower-right unit-upper-triangular block with zero lower-left block. Transposition preserves standard skew tableaux and containment, so the row bound becomes a length bound; the fixed dimension B is valid at every terminal size. B=0 correctly leaves only the empty chain. The determinant at t=0 has the usual identity specialization, including empty shapes.

The event equivalence X_r>x iff L(x,1)<=r-1 is correct. At a repeated threshold, the smallest index gives the strongest survival requirement. Nonpositive thresholds are vacuous because all positions are positive. No monotonicity of the list of indices is needed; inconsistent-looking combinations simply impose simultaneous inequalities on the same shape chain. Inclusion–exclusion then gives all finite joint distribution functions. All marginals are continuous at deterministic thresholds because a particle coordinate must be a Poisson spatial mark, which has no fixed atom.

## 5. Convergence and rational certification

Unrestricted shape chains at terminal size n exhaust all permutations and count allocations, so their raw total is x_m^n/n!. Nonnegativity justifies summation and makes constrained raw mass at most this total. The infinite sum is therefore absolutely convergent and normalized after multiplication by exp(-x_m).

Put E=exp(x_m)-T_N and H equal to the omitted constrained raw mass. Then 0<=H<=E<=R_N and the exact probability is (W_N+H)/(T_N+E). The lower bound is immediate. For the upper bound,

    (W_N+H)/(T_N+E) <= 1-(T_N-W_N)/(T_N+E)
                         <= 1-(T_N-W_N)/(T_N+R_N).

The direction in the second inequality is correct because T_N-W_N>=0. This gives exactly the claimed upper endpoint, without replacing the exponential by an incompatible approximation. Both endpoints lie in [0,1], their difference is R_N/(T_N+R_N), and the width tends to zero. The tail-ratio estimate needs N+2>x_m, exactly as stated and enforced by the evaluator.

For a fixed cutoff the number of allowed partitions and nested chains is finite. Transposition bounds each partition's length by B, so the dimensions do not secretly grow with N. Rational inputs give rational determinant entries and enclosures. Arbitrary real thresholds still define the mathematical law; no blanket effective-computability claim for noncomputable real inputs is made. The exact evaluator validates its documented strictly increasing positive rational query domain; merging arbitrary thresholds is a mathematical preprocessing rule, not an undocumented feature of its command-line interface.

## 6. Known low-index calibration and reproducibility

The first marginal is exponential of mean one. The (1,2) survival sum differentiates to exp(-y) times the series with coefficient (n+1)/(n!(n+2)!). On changing variable to the gap y-x, this is exactly equations (46)–(48) of the 1993 notes, including independence of the first position and first gap. I inspected the rendered original page. The draft's surrounding warning does not substitute for proof; here the density is independently derived from the accepted joint law.

The unchanged author checker replays byte-for-byte with **49,618 exact assertions**. The independent checker uses cell-poset linear-extension counts, a Leibniz determinant, quadratic-time direct LIS, exact transformed event histories and rational tail inequalities. It passes **15,580 exact assertions**. A separate comparison gives **42 exact coefficient matches** between independently enumerated joint events and the author evaluator. These finite controls supplement the analytic arguments above; they do not prove stationarity, coupling, arbitrary-index identities or source scope by themselves.

## 7. Disposition

The complete explicit-series description passes for the exact original process after one substantive author turn. Preserve the classical credits, the source-level explicitness explanation and the limits stated above in any result summary. There is no mandatory revision to the frozen author proof. Publication permission is a separate matter handled by the campaign owner.
