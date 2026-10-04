# Probability and metric audit of PR45 / 9900007

## Determination and exact scope

The frozen mathematical artifact `source_snapshot/PARTIAL.md`, SHA-256 `7123c345d3ecdf4fecb8941596687da54c44e169831eb23177ea485fa8386722`, is mathematically valid for its stated partial claim. Under its explicit one-sided binary construction, the shifted laws converge weakly to a stationary mixture of constant paths, yet every fixed joint construction with that limit has mismatch probability tending to 1/2. Its complete product-metric law and uniformly tight nonnegative-offset extension also hold. No mandatory mathematical correction to that artifact was found by this family.

This determination is independent of the historical review's PASS label. It is not a publication/merge/acceptance decision, a certificate of novelty, a formal proof certificate, or a resolution of the full original problem. The source's broader request for an alternative condition involving only two processes remains unresolved. Retain the original `unsolved`/partial and no-novelty disposition; this audit does not consume or invent an original-author attempt, expand the original candidate, create a paper/DOI, or alter a tracker.

The parent supplied PR45 head `d9b4acf5d070d1f04ffac86a4f08916a5629ff16` and actual base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. This family directly pinned all 18 exported source-snapshot files in `INPUT_PINS.json`; Git/export integrity and native acceptance gates are ROOT responsibilities.

## Independence, reading and source limits

I read actual root `AGENTS.md` and `unsolved_math_prioritization/AGENTS.md`, remained on main, and made writes only in `probability_metric_family`. The early note and `EARLY_SEAL.json` were saved at 2026-10-03T01:50:23.147222+00:00 before any candidate, historical review, helper, result, ledger, or source-record contents were read. Exposure before the seal was only filenames, parent-supplied identity/scope, and the literal target. The independent initial mechanism used distant duplicated iid bits, materially different from the candidate's rare-flip mechanism.

After the seal I fully read the candidate proof, README, SOURCES, research log, turn ledger, readiness/status/source manifest, pinned source record/prior report, both helper sources, the historical mathematical review and verdict, and finite results. Duplicate review copies of the proof/helper/author receipt were fully read by byte comparison and were identical to originals. I read the complete historical 3,044-entry result map programmatically and compared every key/value to its exhaustively reconstructed parameter schema: 2,026 conditional-history entries, 45 finite-history envelopes, 288 anticipative-sign entries, 60 windows, 128 metric pointwise controls, 360 offsets, 40 offset sums, 79 two-time gaps, and 18 normalization/fairness entries. The model-facing all-entry dump was truncated; the subsequent full structural comparison was untruncated and true. Those historical receipt labels are not evidence for this new mathematical determination, and neither historical nor author helper was executed/imported/copied.

The workflow README was read; the complete queue file was loaded and hashed and its selected row inspected (the current queue row was queued/0 turns, whereas the exported original artifact reports one partial attempt). No queue write was made. Related-target groups were loaded and no entry containing 9900007 appeared. The literal source transcription and primary-access limitations in the snapshot were read. This family obtained no fresh primary PDF or published full article, and claims no whole-primary-proof or literature-priority reading. Its mathematical finding is conditional on the literal source scope supplied by the parent and reproduced in the pinned record: separable metric state space, product path topology, weak convergence of deterministic shifts, no specified mode for the illustrative metric limit, and no added ergodicity/adaptedness/homogeneity assumption. ROOT's fresh primary-source audit must establish that scope independently.

No remote foreign PDF, extracted text, or pixels were downloaded or copied into this family; the corresponding foreign/publication-exclusion registers in `INPUT_PINS.json` are empty. Original source files were read in place and are outside this family's closure. No person was contacted and no outreach was prepared.

## Independent derivation of every candidate step

Write p_k=1/(k+2). The process is a fair initial sign multiplied by independent signs with flip probability p_k. It is a measurable random element of the compact binary product space. Its marginal sign at every time is fair: multiplication by a sign independent of the fair initial sign preserves fairness. The weighted Hamming distance is a metric generating the product topology; its tail beyond coordinate r is 2^{-r-1}, so agreement of a long prefix gives arbitrarily small distance. Coordinate shifts are continuous.

For a full window n through n+r, being a constant word is precisely absence of all r intervening flips. Even two flips cannot make the whole window constant, since each flip appears as an unequal adjacent pair. Thus noflip probability is

    ∏_{k=n}^{n+r−1}(k+1)/(k+2) = (n+1)/(n+r+1).

The two constant words each have half this mass; the limiting constant-word law assigns them 1/2 each. The deficit on constant words and surplus on all other words both total r/(n+r+1), giving that total-variation distance in the supremum-over-events convention. This includes r=0. For every continuous function on compact path space, replacing the infinite tail by a fixed tail changes it uniformly by a quantity tending to zero. Finite-prefix law convergence therefore proves weak convergence of shifted laws. No tightness theorem on a generic noncompact space is silently needed here.

For the finite-history sigma-field F_m=σ(X_0,...,X_m), independence of the future flips under the marginal law of X yields, for n>m,

    E[X_n|F_m]=X_m ∏_{k=m}^{n−1} k/(k+2)
               = X_m m(m+1)/(n(n+1)).

At m=0 the product contains a zero factor; the formula gives zero and introduces no division by zero. In an arbitrary joint construction, the same conditional identity with respect to F_m is determined by the marginal law of X; it does not assert that future flips remain independent after conditioning on a second process.

For each fixed bounded σ(X)-measurable g, set g_m=E[g|F_m]. The increasing finite histories generate the full path sigma-field. The upward L1 conditional-expectation theorem gives ||g−g_m||_1→0. Since |X_n|=1,

    |E[X_n g]| ≤ ||g−g_m||_1
                 + m(m+1)/(n(n+1)) E|g_m|.

First n→∞ with m fixed, then m→∞. This proves E[X_n g]→0. The order of limits is justified; uniformity over a sequence g_n is neither obtained nor required.

A process with the stipulated constant-path law equals C_B=(B,B,...) almost surely, by countably intersecting the probability-one coordinate equalities; B is fair. It can depend on the entire path of X and on extra joint randomness. On that joint space put g=E[B|σ(X)]. Then |g|≤1 and the tower property gives E[X_n B]=E[X_n g]→0. Therefore

    P(X_n≠B)=(1−E[X_nB])/2→1/2.

This is the correct all-couplings quantifier: for every fixed joint law with the two prescribed marginals, the limit is 1/2. It is not a uniform-in-coupling finite-n lower bound. For each prescribed N one can choose a different valid coupling B_N=X_N with mismatch zero at N. That does not give one fixed B working at all times. Our finite controls explicitly distinguish these quantifiers.

The simpler marginal two-time identity is

    P(X_n≠X_m)=1/2 (1−n(n+1)/(m(m+1)))  (m>n).

At m=2n it tends to 3/8. If one fixed B had X_n→B in probability, the union bound would force this mismatch to zero. This independently proves the failure of synchronous coupling before using the stronger projection argument.

For D_n=d(θ_nX,C_B) and I_n=1{X_n≠B}, the pointwise inequality

    |1{X_{n+j}≠B}−1{X_n≠B}|≤1{X_{n+j}≠X_n}

holds regardless of the dependence of B. Since weights sum to one, Tonelli and the probability of any intervening flip yield

    E|D_n−I_n|≤Σ_j 2^{-j-1} j/(n+j+1)≤1/(n+1),

using Σ_j j2^{-j-1}=1. Consequently D_n⇒(δ_0+δ_1)/2 and ED_n→1/2 under every fixed coupling. A random variable tending to zero in distribution would also tend to zero in probability, so even that mode is excluded. Almost-sure convergence is excluded because it implies convergence in probability. The original product metric is bounded, so all indicated expectation limits are valid.

Every other metric generating this product topology is uniformly equivalent on the compact binary path space. Hence convergence of distance to zero in probability would imply convergence for the original metric and is equally impossible. The numerical {0,1} law is tied to the specific original metric; the candidate does not assert it for arbitrary compatible metrics. This step uses compactness of the actual binary construction, not a false uniform-equivalence assertion for all separable noncompact spaces. The same binary construction embeds in any metric state space containing two distinct states; a singleton state space is a trivial boundary where such an obstruction cannot exist.

For each deterministic nonnegative s,

    E d(θ_{n+s}X,θ_nX)
       ≤Σ_j 2^{-j-1} s/(n+j+s+1)≤s/(n+1).

For arbitrary nonnegative T_n dependent on both full processes and on any extra randomness, on {T_n≤M} a discrepancy exceeding ε implies that one of the deterministic s-discrepancies, 0≤s≤M, exceeds ε. Union and Markov bounds give

    P(d(θ_{n+T_n}X,θ_nX)>ε)
       ≤P(T_n>M)+M(M+1)/(2ε(n+1)).

Uniform tightness means lim_{M→∞} sup_n P(T_n>M)=0. Thus the right side tends to zero by first n→∞ then M→∞. An a.s. finite fixed offset automatically meets the needed tail condition. The limiting process is constant, so its second offset has no effect at all. Independence of offsets is unnecessary; no conditional flip argument is used. Reverse triangle bounds then preserve the candidate metric-law limit. This does not establish the same theorem for arbitrary growing offsets, for signed offsets, or for unrelated stationary-limit processes.

The eventually-constant-path event is Borel and shift invariant. For each deterministic starting time n, the probability of no flip ever again is the limit of (n+1)/(m+1), hence zero. The countable union over n still has probability zero. The constant-path limit assigns it probability one. Setwise convergence therefore fails. This example cannot be transferred to distinct target 9900005 / Problem 3.1.

## Quantifier and mechanism boundary controls

A stationary starting process admits the trivial identity coupling to its own limiting law; the counterexample is nonstationary even though every one-dimensional marginal is fair. For continuous deterministic shifts on product space, any weak limit of successive shifted laws is itself stationary, since θ_*μ_n=μ_{n+1}. The candidate's stationary limit is therefore natural; its nonergodicity is allowed by the literal target. The independent early iid construction suggests an ergodic-limit obstruction as a separate audit-only result, not an extension to be attributed to the original author.

Unbounded offsets really can change this candidate. Couple X with an independent fair B and let T_n=min{s≥0:X_{n+s}=B}. The tail noflip product ensures T_n is finite almost surely. For M≥0,

    P(T_n>M)=(n+1)/(2(n+M+1))→1/2.

Thus this sequence is not uniformly tight. On {T_n=t}, the sign at n+t equals B and future flips are independent of this finite stopping event and the independent B. For any j, its probability of a subsequent mismatch is bounded by j/(n+t+j+1). Summing weights and then over t gives

    E d(θ_{n+T_n}X,C_B)≤1/(n+1)→0.

So growing dependent offsets restore convergence in probability in this particular construction. This is a check of the candidate's declared boundary, not an alternative full-target characterization and not a candidate amendment. The claim uses independent B deliberately; no independence after conditioning on an arbitrary anticipative B is assumed.

If flip probabilities are changed to 1/(k+2)^2, the process stabilizes almost surely because the sum is finite. Its eventual sign is fair by global sign symmetry and supplies a synchronous coupling with the same constant-path limit. The noflip product from n to N is ((n+1)/(n+2))((N+3)/(N+2)), whose positive limit shows why the original complete-history decorrelation fails here. Local freezing alone is insufficient; the divergent accumulated flips are essential.

The sealed independent long-duplicate-block mechanism is retained as provisional audit reasoning and control evidence. Choose block half-lengths 2^j. Each block consists of fresh fair iid signs followed by their identical copy. A fixed-width window has no repeated variable labels once half-lengths exceed its width, hence has exactly the iid law. Under every coupling to fair iid Y, each duplicated pair (a,b) obeys

    P(X_a≠Y_a)+P(X_b≠Y_b)≥P(Y_a≠Y_b)=1/2.

Both indices tend to infinity; limsup coordinate mismatch is at least 1/4. Compact first-coordinate cylinders give a metric threshold for every compatible metric. The constant is attained coordinatewise by selecting one of the two iid endpoint signs with an auxiliary fair coin. This does not certify optimal full-path metric distributions. ROOT/fresh adversarial verification would be needed before any promotion of this separate mechanism.

The early iid-offset note contained one imprecise sentence: a general joint event need not itself be approximable by cylinder events of Y. The corrected fixed-offset proof projects 1_E onto σ(Y), with h_E=E[1_E|σ(Y)], then approximates h_E in L1 by functions of finitely many Y coordinates. For fixed d and far duplicated a,b,

    E[1_E 1{Y_{a+d}≠Y_{b+d}}]→P(E)/2,

because the far iid pair is independent of each finite-prefix approximation. With E={T=t,S=s}, summing on finite offset sets and truncating gives the needed random dependent offset pair discrepancy. Hypothetical convergence at deterministic times implies convergence at a−T and b−T by the same finite truncation, contradicting the pair inequality. The original sealed note is preserved unchanged and this correction is recorded. This separate proof does not cover merely tight time-varying offsets for the iid duplicated-block construction; the offset at each paired time may select a different X coordinate. No such extension is attributed to that route.

## New controls and actual run provenance

`independent_controls.py` is handwritten and contains no imports or copied execution of author/historical helpers. It implements an independent pair-state recurrence; exhaustive antipodally fair nonlinear finite-history selectors (not just Walsh monomials); fixed-varying coupling comparisons; a growing first-hit-offset absorbing recurrence; a summable-flip boundary; and iid-block label/endpoint controls. The 13,928 finite exact checks completed; 12,181 are modest block-window label controls, not independent proofs. Counts are bookkeeping and do not certify infinite quantifiers. The equations and conditional-expectation proof above provide those.

`capture_controls.py` wrote a genuine prelaunch record before invoking the child. Actual operator PID 42225, child PID 42235; invocation `/opt/homebrew/opt/python@3.14/bin/python3.14 .../probability_metric_family/independent_controls.py`; working directory exactly this family; run began 2026-10-03T01:55:25.991432+00:00 and ended 01:55:26.336398+00:00; exit code 0. Full 434,639-byte stdout and empty stderr are preserved as raw files, with hashes and before/after program hashes in `independent_controls_run1/RECEIPT.json`. The child's own PID/argv/cwd/UTC are in stdout. No failed mathematical run occurred and no retry suppressed a failure.

An ancillary inventory initially resolved `Path('.').parent` incorrectly and produced zero source input pins. That output was detected before reliance, preserved as `INPUT_PINS_INITIAL_PATH_ERROR.json`, and corrected with `Path.cwd().parent` to all 18 inputs. The original mathematical controls were unaffected. An initial `wc` file inventory returned status 1 only because a directory was included; it was a file-size inventory, not a numerical or proof-control failure. No result was inferred from that status.

## Remaining gap and completion

Strongest verified original-candidate result: weak shift convergence on compact binary product space can hold while every fixed two-process coupling has a nonzero synchronous metric-error limit, unchanged under uniformly tight nonnegative offsets. Exact gap: no other two-process necessary-and-sufficient condition characterizing weak shift convergence is given or excluded. Independent iid evidence and non-tight offsets do not close that gap.

Audit completion estimate at report checkpoint: 95%, with only own closure/integrity checks remaining. Original full-target discovery estimate: 0% from this audit; original partial theorem is validated. No future acceptance, publication, whole-primary-proof reading, or novelty status is claimed.
