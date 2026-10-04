# Independent literal/source/priority adversarial audit of PR45

Verdict: PASS_SCOPED_PARTIAL_OBSTRUCTION. No mandatory mathematical correction
was found in the frozen original PARTIAL.md. One current source-access addendum
is required if the new reviewed package describes the present access state:
Asmussen (1992) is now accessible and was read as specified below. This is an
independent AI audit; it supplies no human peer-review, historical novelty,
full-source solution, or future acceptance certificate.

## Provenance and early independence

The source/quantifier seal was written and set literally 0444 before candidate
PARTIAL/SOURCES/source_record/helper/results/ledger/old review reading.
SOURCE_SEAL_BINDING.json records its exact bytes and time. Primary Section 3
was recovered independently through current indexed author-preprint text on
preprint pp. 3–4. No original full PDF/pixels were recovered. The original
published 2011 source remained metadata/subscription material. This distinction
is preserved; there is no full published/preprint line-by-line comparison.

All 18 original bodies were read in full into the byte binding. Unique prose
and code were inspected; byte-identical duplicate review copies were checked.
The two 42-window receipts were inspected in full; the large historical
3,044-entry receipt was fully parsed, all values and systematic key groups
inspected. Those historical counts were not re-executed by this family.
Neither production nor candidate helper code was imported, compiled or run.

EXPORT_COMPARISON.json verifies every source_snapshot size, SHA and literal
0444 mode against snapshot_manifest.json (SHA
7180aa194d0fe99806e8aed1a92cbbc456676f26e0b2a18ad24cfcef4cd77833).
The head is d9b4acf5d070d1f04ffac86a4f08916a5629ff16;
the GitHub base is c6975ca76f9f667f1250ba403d0e6da2aafe14d0;
the actual merge base is 01358d66fc67d1c462bddf31c0d4ee5b120e6737.
These two bases are distinct. No native/index/branch/QUEUE writes, commits,
pushes or outside communication occurred.

## Literal source matching and exact target gap

The primary Section 3 defines general one-sided discrete-time processes and
deterministic shifts, then separable metric state/Borel/product path topology.
It does not require homogeneity, adaptedness, Markovian joining, ergodicity of
the limit or stationarity of X. The candidate's inhomogeneous X and nonergodic
stationary mixture limit are therefore admissible.

The original question seeks some two-process characterization and gives
synchronous shifted metric convergence as an example, with no explicit mode.
The candidate correctly proves failure even in probability, hence a.s., while
leaving the broad characterization unsolved. An illustrative-condition
counterexample is not an impossibility theorem for all conceivable relations
between two coupled processes. No current primary-source search establishes
absence of a prior result.

As a category boundary control, if X itself were stationary then its shifted
law is constant and any weak limit has the same law; the diagonal coupling
would succeed. The source does not impose that hypothesis. Every X_n being
fair is likewise not joint stationarity: the adjacent flip rates differ.

## Independent reasoning: all fixed joint constructions

For a finite prefix ending at m, the conditional sign at n has correlation
rho(m,n)=m(m+1)/(n(n+1)), including the zero factor at m=0. This follows
from the independent future transition signs under the marginal law alone.

For any bounded full-path function g, approximate g in L1 by conditional
expectations on finite prefixes. The error is uniform in n because |X_n|=1;
the finite-prefix part is bounded by rho(m,n)||g||_1. Sending n then m to
infinity gives E[X_n g] -> 0. Given any fixed joining, B may depend on all
of X and extra randomness; take g=E[B|sigma(X)]. The tower identity gives
E[X_n B] -> 0, and the exact sign identity gives mismatch probability ->1/2.
Conditioning on B does not preserve flip independence, and the proof does
not make that invalid step.

An independent obstruction to a single B is the two-time relation:
P(X_n != X_(2n))=(3n+1)/(4(2n+1)) ->3/8. If X_n -> B in probability
for one fixed B, the mismatch between n and 2n would vanish by the union
bound. An n-dependent maximally coupled B_n can evade this argument but
does not supply a joint construction of one fixed original X′.

Local windows have TV error r/(n+r+1). Compact product topology upgrades
window convergence to weak path-law convergence by uniform cylinder
approximation. No independent-per-window copies are identified as one path.

## Metrics, offsets, setwise premise

The pointwise metric comparison uses only binary indicator arithmetic and
works for every B. Summable geometric weights plus local flip bounds give
E|D_n-I_n| <=1/(n+1), so D_n converges in law to the fair mixture of 0 and 1.
This numerical limiting law concerns the stated metric. Every product-
compatible metric on compact binary path space is uniformly equivalent, so
none restores convergence to zero in probability; there is no assertion that
every alternative metric has the same numerical endpoints.

An offset T may depend on both complete paths. On {T<=M}, the error is
bounded by the sum over deterministic offsets s<=M, without conditioning
on T. The expected deterministic s-error is <=s/(n+1). Tightness lets n
then M tend to infinity. This establishes finite offsets and uniformly tight
nonnegative offset families, not arbitrary escaping time changes. Offsets
in X′ do nothing because it is constant.

The eventual-constancy event is Borel and shift invariant. Independent
switches have divergent probability sum, so that event has X probability 0
and limit probability 1. All shifted X laws therefore fail setwise convergence
(and in fact have TV distance 1 from the limit). This is not a counterexample
to distinct Problem 3.1 / ID9900005.

## Independently executed finite controls and exact limits

Own independent_controls.py builds full finite path laws from adjacent
transition probabilities in bit notation, marginalizes coherent windows,
checks all finite histories, and checks sharp maximal finite-prefix correlation
for arbitrary bounded joining functions. It also checks pointwise metric and
dependent-offset ingredients. Healthy run: 1,871 exact rational assertions PASS.

Four actual fault launches were rejected with nonzero child exit codes:
wrong window denominator; wrong conditional-moment index including m=0;
reset/homogeneous transition schedule; false joint stationarity of X.
The source, operator, prelaunch record, child PID, UTC, complete stdout,
complete stderr and all failures are retained in actual_runs/. These finite
controls support local identities; the infinite all-joining quantifier rests
on the written L1-density reasoning above.

The original candidate and old reviewer mathematics agree with this analysis.
No mandatory mathematical defect, circularity, hidden causality hypothesis,
shift-consistency substitution or incorrect metric/offset extension was found.

## Completion and strongest result

Assigned adversarial audit completion estimate: 100%.
Scoped obstruction proof verification: 100%.
Broad source characterization discovery: 0% achieved by this package.
Strongest verified result: general weak shift convergence does not force
one fixed synchronous asymptotic coupling, even in probability, in the
source's permitted binary product category; all joinings have asymptotic
mismatch one half, and tight finite offsets cannot repair it.
Exact remaining gaps: alternative two-process characterization, exhaustive
historical priority, and line-by-line full published-original comparison.
The bundled original source status must remain UNSOLVED/PARTIAL.
