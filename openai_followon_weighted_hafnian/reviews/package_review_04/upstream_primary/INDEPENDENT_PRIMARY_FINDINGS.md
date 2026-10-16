# Independent primary-source dependency audit — saved before package comparison

This document and `PRIMARY_RECEIPTS.json` were produced from the original request,
the project instructions, and the actual pinned source before opening the
follow-on package's upstream/formal audits or manuscript. The source clone was
read only; no build, dependency installation, Git mutation, publishing, or
communication with external people occurred. An internal Lean subtask was
attempted but unavailable because the agent concurrency limit had been reached.

The pinned checkout is `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in
`/Users/alec/Desktop/math`. The receipt gives SHA-256 values for the principal
manuscript/PDF, the entropy companion's complete TeX inputs, the actual Lean
import closure, scope document, comparator, toolchain, and lock manifest.

## Provisional verdict and limits

**No blocking mathematical gap found in the inspected primary FPRAS proof.**
This is an analytical dependency audit supported by exact finite tests and a
static Lean source inspection. It is not an independent kernel verification,
an execution of the FPRAS, a general-purpose test certificate, or a formalization
of any weighted hafnian follow-on. The main proof has been reconstructed through
its logical-hole, subdivision, cell/encoding, pair energy, replica gap, sampling,
annealing, statistical, and bit complexity stages. The entropy companion has been
read for its exact counting/weight scope, not independently reproved in full.

Relevant discovery/review completion at this checkpoint: primary-source
reconstruction 90%; package comparison 0%. These estimates are not evidence.

## Actual statement and actual proof architecture

The principal manuscript's Theorem 1.1 (`thm:main`, source lines 132–146) states
a uniform FPRAS for the **unweighted** count of every finite simple undirected
graph. Parameters are rational `0 < epsilon < 1`, `0 < delta < 1/2`.
Every execution returns a nonnegative rational, the relative-error event has
probability at least `1-delta`, the zero count is returned certainly, and worst
case bit time is polynomial in the complete input encoding length,
`epsilon^-1`, and `log(delta^-1)`. Empty graphs return one; the sparse binary
vertex-count case is screened before allocation by `n > 2|E|`.

The source does **not** use a perfect/near-perfect Broder chain or a conventional
canonical path congestion argument. Those occur as historical context and a
known obstruction. Its chain is a product of spaces of colored **perfect**
matchings on a subdivided tree-bag graph. Its pair energy proof uses a signed
cell identity, repaired encodings by two perfect matchings, and exchanges of
entire discrepancy cycles. Calling its encoding a four-hole near-perfect
canonical path proof would misidentify the dependency.

The source explicitly excludes compressed multiplicities from the theorem's
input model (lines 352–357), and its prescribed-degree/specified-size corollary
also excludes compressed weights/multiplicities. The weighted activities in the
proof are explicit internal algorithm data, not an independently stated FPRAS
for arbitrary binary rational input weights.

## Logical holes, subdivision, and inflation

1. **Four holes:** overlay a matching missing `a,b,c,d` with a perfect matching.
   The unique alternating path from `a` ends at one of the other holes. Layer
   exchange gives one of three products of two-hole families. Specifying the
   endpoint gives an inverse, and product weights are unchanged. This yields
   `g(abcd) <= g(ab)g(cd)+g(ac)g(bd)+g(ad)g(bc)`, including the empty-complement
   case. It does not assume independence of hole events.

2. **Strong-path relocation:** for activities `mu >= lambda` and row maxima
   in `[1/8,4]`, a maximizer `p` in the next path vertex's row cannot be the
   old hole, since the strong edge forces `g(az) < 1/8`. If `p` is also a hole,
   it is an isolated overlay vertex and cannot be the alternating path's
   endpoint. The three endpoint classes are exhaustive. Inserting `az` is
   reversible after removing this distinguished inserted edge; it was absent
   from both input layers. Divide by the *current* row maximum to telescope
   the relocation bound, rather than multiplying row-ratio errors along the
   path. Stop at the first fixed hole; the endpoint fill covers the final step.
   At most `n-2` moves give `g(U) <= 10^5 n/B_ij` for two/four holes.

3. **Bootstrap:** add activity `t B_ij/D0`, holding the bottleneck array fixed.
   Finite partition derivatives and the preceding two/four-hole bounds keep
   every row inside `[1/8,4]` by a first-exit argument. Integrated inflation is
   below two. Inserting a capacity-maximizing pairing of any even hole set
   using distinguished added copies is injective, and gives
   `g(U) Phi_B(U) <= 2 D0^(|U|/2)` with `D0=10^8(n+1)^4`.

4. **Subdivision:** each logical edge becomes a `4p+1` edge path with equal
   adjacent activity pairs and central activity `lambda_uv`. Even tilings
   leave both terminals unused; odd tilings use both. Their ratio is exactly
   `lambda_uv`. The common even baseline `C0` gives a global bijection and
   `Z'=C0 Z_lambda`. Noncentral effective strengths equal the real activities;
   central effective strength is the logical bottleneck. Incident effective
   strengths differ by at most two, so each vertex occupies one label or two
   adjacent labels.

5. **Deleted vertices:** successive internal holes must alternate parity.
   A first even hole consumes the left endpoint; a last odd hole consumes the
   right endpoint. One hole cannot do both. Remaining neutral pairs have odd,
   even indices. Same-half factors are inverse local strengths; cross-half
   factors are `lambda/(T_j T_k)`; away endpoint consumptions are `lambda/T_j`.
   The exact partition identity retains the important condition that every
   broken logical edge is forbidden. Consumed/deleted terminals must be
   distinct. The logical hole set is even and no larger than the real hole
   set. This handles central holes, length-three local runs, one hole,
   both endpoints, and cross-center pairs.

6. **Capacity lifting:** the pairing capacity's logarithm is the integral of
   threshold-class floor counts. A laminar bottom-up pairing attains every
   floor count simultaneously. Neutral-pair removals and away endpoint maps
   incur the stated charges; inactive internal vertices are singleton classes
   and cost zero. For `lambda<1`, replacing `log(lambda)` by `log(max(1,lambda))`
   only weakens the charge in the correct direction. Thus
   `F Phi_B'(U) <= Phi_B(R)`, and the real hole bound follows.

7. **Bag inflation/marks:** each virtual partial matching with `a` edges has
   mass at most `2(D0/D)^a`, and there are at most `N^(2a)` choices. With
   `D=100 N^2 D0`, inflation is at most `1+2/99<2`. Revealing collapsed real,
   virtual and probe portions recovers the original law. The all-real event
   has probability `1/I`; the sole central probe event has exact probability
   `g_lambda(uv)/(DI)` and leaves the expected weighted logical two-hole law.

These deductions require positive complete logical activities and balance
where explicitly invoked. The final algorithm creates positive completion;
the source does not assume that the original support is connected or dense.

## Local cycle identity, repaired encoding, and guide cancellation

All discrepancy cycles are even. A length-two cycle is a color change; a
simple cycle has length at least four. The quadrangulation operates on the
original full cycle's fixed label sets. Every cell side is an **odd** arc.
Even arcs are not legal through/closed comparisons and are excluded by the
odd/even split indices. Short arcs use their actual colored edge and have
zero gain. For a long arc, the through and closed patterns match the same
vertices, and a good arc has a valid leaf repair; length three has two
distinct leaves. The label-tree splitting distinguishes good/non-good
exteriors and supplies the two good-side properties needed by the repairs.
The compared boundary, chord and repair activities are within `1000D`, even
after a common clamp.

The cell identity includes context errors for two opposite long sides.
Those errors cannot be dropped for a general function. Complementary
diagonal gains do **not** cancel to zero: they contribute one whole-cycle
difference. There is one more cell than interior diagonals, yielding the
correct global signed identity. The six-cycle example in the source makes
this especially checkable. No long arc conversion is assumed to be a
single legal transition.

Switch demands encode into `(A_P,B)`. Repairing a good opposite pair in
the union of all four through patterns produces a legal perfect matching
`B`. In error context zero, inserting the two relevant chords and repairing
the other good opposite pair gives a guide containing `C_X` and `C_Y`.
In context one, exchange the `Y` patterns; the disjoint opposite arc `X`
retains its closed pattern. At most four equal-number added/dropped edge
occurrences in one comparable collection give the weight factor `A0^4`.
A tag with cell corners, occurrence lists, orientation and fixed flags
recovers the original colored multiset union and active cycle, then its
two layer orientations; unchanged outside layers retain their identities.
The explicit bound `128 N^4 (1+2N^2)^8 < (10N)^30` is polynomial. This is
a bounded repaired-encoding load, **not a canonical path congestion theorem**.

For errors, the guide constraint must be retained. For fixed `X,A`, summing
the encoding weights over guides yields `A0^4 T pi(A) p_X`, where
`p_X=pi{B:C_X subset B}`. Center both contexts about the conditional mean
of the second coordinate's arc derivative. Jensen introduces exactly
`1/p_X`; the demand mass cancels it. No lower bound on this potentially
rare event is used. Identities with `p_X=0` cannot be generated by an
error demand and are omitted. The through/closed overlay is an entire
discrepancy cycle, and marking a closing chord plus orientation gives
at most `2N` representations of one cycle. Cycle-swap energy therefore
pays for the error sum. The resulting inequality applies to additive
`f1(A)+f2(B)`, not arbitrary two-coordinate functions.

## Replica gap and sampling

The common clamp ladder has `c=1+N^-2` and
`T=O(N^2(K+log D+1))`. Adjacent normalized matching laws have density
ratio in `[1/2,2]`. Minimum Metropolis capacities hence transfer the
equal-tier additive inequality to unequal tiers with coefficient `2L`.
This comparison also covers unequal-tier cycle swaps; their acceptance
is **not** assumed to be one.

There are `q=32L` slots per tier, `M=Tq^2+q` allowed updates, with
`L=(10^4ND)^100`. Order slots from high tier to low. The martingale
increments account for the whole variance. The residual for allowed
pair `(x,y)` contains only ANOVA components whose last two positions
are `x,y`: all other component coordinates lie before `x`. Thus a
component can occur in at most one pair residual, even for pairs sharing
a slot. It is **this assignment** that justifies
`sum ||r_xy||^2 <= Var(f)`. A naive unstructured sum of overlapping
residuals would not justify absorption. Averaging over the `q` guides
gives the residual coefficient `8L/q=1/4`, so absorption proves gap
`3/(8M)`, and the advertised weaker `1/(20LM)` is valid.

The base unit-activity law is counted/sampled by polynomial convolution
tables: disjoint interfaces and exchangeable interface vertices justify
the scalar count index. The recurrence's apparent product of child
sums is evaluated as polynomial convolutions, never an exponential
enumeration of all child choices. Counts are bounded by `2^N N!`.
The positive table gives deterministic initialization. Point-mass
spectral mixing uses the explicit minimum stationary mass bound,
laziness, and `s=ceil(20LM(Lambda+ceil log2(1/xi)+1))`. The final top
coordinate is within `xi` ideally. Fixed-grid rational choices add at
most `xi`; they preserve feasibility because zero-probability outcomes
are empty intervals. No rejection sampling stopping time occurs.

## Counting, unsuccessful histories, and bit complexity

Start from complete graph activities one, suppress absent original edges
by `(1+1/n)^-j`, and telescope raw partition ratios. Vertex scaling has
a common factor on every complete matching and does not change its
normalized law. The initialized two-hole row maxima lie in `[1/4,1]`.
The all-real and weighted-all-real means are at least `1/2` and `1/4`
under balance; sole-probe means give the next-stage hole estimates.
Clipped estimates and the one-pass multiplicative constraints restore
balance after accurate observations. The tight neighbor chosen for a
row remains tight because a later decrease would violate that constraint.

At every adaptive successful history, the fresh ideal sample batch has
the required Hoeffding bound, and conditional couplings account for the
implemented law. Union over first unsuccessful stages gives trial failure
at most `13/1000`; all observable correlations within a sample are
allowed. The ratio accumulation and residual nonedge count give relative
error below epsilon. Independent-trial median amplification gives the
logarithmic confidence cost.

Bad observations cannot destroy termination: all estimated entries are
clipped into `[alpha,3]`, scales always multiply by `[alpha/2,2]`, the
global upper bound `lambda <= 4^K` holds unconditionally, and the bag
sampler never required balance. A same-trial fixed structural bound
therefore works on every history. Empirical contributions use one common
denominator `(n+1)^(n/2)`. Update dependencies strictly decrease their
order index, limiting each update vector to `n` small rational factors;
accumulating `K` stages has polynomial bit length. Bottleneck values
select entries or one (max–min Floyd–Warshall), and do not sum paths.
Tier powers, Metropolis products, DP normalizers, revelations and final
ratio products have bounded polynomial bit lengths. Fixed-grid random
choice budgets accumulate under conditional coupling. The source's
extremely large fixed exponents affect practicality, not the existence
of one uniform polynomial bound.

## Sampling theorem already present in the primary manuscript

`lem:deletion-sampler` (source lines 3203 onward) already converts the
FPRAS to an always-feasible approximate uniform sampler on explicit
simple unweighted graphs, in every-execution bit time polynomial in
full input length and `tau^-1`. It tests both deletion branches
deterministically, takes forced feasible branches exactly, calls the
counting theorem with fresh randomness only if both branches are
feasible, and rounds the inclusion ratio down to a fixed dyadic grid.
The all-zero-estimate fallback remains feasible. At most `|E|` decisions
occur; branch-law conditional error is at most
`eta/[2(1-eta)] + 2 gamma + 2^-t`, with
`eta=gamma=tau/(8 max(1,|E|))`. Coupling yields error at most `tau/2`.
This is a TV guarantee, polynomial in inverse tolerance; the source
does not assert exact or pointwise almost-uniform sampling.

## Entropy companion scope

For feasible marginals in loopless labeled multigraphs on `2m>=2`
vertices, it states `F-(2-2/m)B <= H <= F`, including boundary points;
the sharp face-codimension bound is also stated. The weighted variational
corollary is `q*-(2m-2)/ln2 <= log2 Z_beta <= q*` for finite real beta.
This is an exponential-factor analytical bracket, not an FPRAS.
Its explicit deterministic binary-multiplicity algorithm returns an
integer `A` with `N/512^n <= A <= N`, exact zero detection, and polynomial
input-bit cost. The singleton-loop extension has factor `2^(18n)`.
Neither supplies arbitrary-relative-error counting or the weighted
sampler requested by the follow-on. The entire entropy proof was not
used as a premise for the FPRAS reconstruction.

## Actual formal source and trust boundary

`OAI.Combinatorics.MatchingCount.Main` contains
`OAI.MatchingFPRAS.thm_main : MainStatement`, with a real proof obtaining
`LiteralPhysical.mainTime_bound`, `mainProgram_outputs`, and
`mainProgram_success`. `Model.lean` defines `GraphInput` as a finset of
increasing vertex pairs (finite simple undirected graph), `Perfect` as
exactly one incident selected edge at every vertex, and `Z` as the exact
finite count including the empty graph. The main statement quantifies
one fixed finite-state machine over alphabet `Fin 8`, all graphs,
rational epsilon/delta, and **all** fair-bit tapes of a polynomial length.
It states nonnegative rational encoded output on every tape, zero output
on every tape when `Z=0`, and good-tape fraction at least `1-delta`.
Each tick writes, moves, or halts. This is semantically the full
unweighted FPRAS theorem, not merely a free randomness oracle or a
counting-function definition with its cost hidden.

I read the actual immediate bridge declarations and compiler seal:
`PhysicalCost.mainTime_bound`, `MainLaw.mainProgram_outputs/success`,
`AlgorithmLaw.algorithm_proper/success`, and
`PhysicalProgramSeal.Realizes.run_all/run_mean`. These connect bounded
physical execution, encoded output and the fair-tape distribution.
The actual formal implementation has a guarded path to certain-zero
output; it need not be instruction-for-instruction identical to the
paper's preliminary Edmonds branch to establish the same theorem.

The recursive OAI import graph has **415** modules, no unresolved OAI
imports, and no uncommented `sorry`, `admit`, `axiom`, `sorryAx`,
`native_decide`, or `unsafe` tokens under the scanner. `Mathlib` is
the external root. The pinned toolchain is Lean `v4.34.1`; mathlib is
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The comparator's
`thm_main` deliberately contains `sorry`; it was read to distinguish it
from the actual implementation and is not in the scanned proof closure.
The selected source scope doc describes the same unweighted FPRAS and
selected entropy/triangle-face statements, not every manuscript theorem.

**No Lean kernel build or `#print axioms` replay was performed.** Static
closure inspection is weaker than either. I did not inspect every proof
line of all 415 files; the absence of scanned holes is not a replacement
for typechecking. The follow-on gadget, rational denominator scaling,
sampler, and final theorem have no formal certificate from this inspection.

## Exact finite check receipt

Run `python3 audit_primary.py` from any directory. It reads the pinned
source only and writes its owned receipt next to the script. It reproduced
96 rational four-hole inequality cases; 52,380 local broken-path
completions covering all internal deletion subsets for `p=1,2,3`,
activities below/at/above one, and both endpoint choices; 182 signed
cell identities on cycles of orders 4 through 12; and 5,027 ANOVA
subset assignment cases with shared-slot pairs. All passed. These tests
support the reconstructed identities and edge cases. They do not certify
the upstream algorithm or the general proof.
