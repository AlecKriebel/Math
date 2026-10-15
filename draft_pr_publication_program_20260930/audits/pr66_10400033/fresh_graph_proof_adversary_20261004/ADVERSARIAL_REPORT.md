# PR66 fresh adversarial graph-proof report

## Verdict

**VALID CONDITIONAL GRAPH LEMMA.** The universal tournament-completion argument is valid for the formal signed arrow evaluation defined by the candidate's exact P and T patterns and once-per-subset coefficients. No combinatorial error was found. The independently derived proof was saved before any original checker or any other graph opinion was inspected. No such checker or opinion was subsequently needed or inspected.

The resulting classical-knot claim remains conditional on the primary-source bridge: the imported formula must compute the specified normalized invariant using these directed patterns with coefficients 1/2 and 1 and this once-per-subset convention. This report certifies neither that bridge nor novelty, current open status, or publication readiness. The root owns those decisions and the separate bridge audit.

## Universal evidence and attacks

The detailed independent derivation is in `FIRST_CONCLUSION.md`, saved 2026-10-04T16:25:09.151331+00:00, SHA256 `5b78cac460c735cf787a7af4d2177cb6608374cfc10a845160235b45bfe8a022`.

| Attack | Independent finding | Residual condition |
|---|---|---|
| Could both intersecting arrows point to one another, or neither? | Fixing a tail at the cyclic origin leaves exactly two alternating orders; their tail-in-open-arc truth values are complementary. | Distinct endpoints, as in a Gauss diagram. |
| Could P have the wrong endpoint directions? | Exact endpoint word gives b→c→a, with {a,b} absent. | The imported P must be the candidate P. |
| Could T be transitive? | Exact endpoint word gives c→b→a→c. | The imported T must be the candidate T. |
| Could cyclic rotation or orientation reversal break the argument? | Rotation preserves arc membership; circle reversal reverses every fixed edge and preserves path/cycle types. | None for the graph step. |
| Could a symmetry multiply the triangle count? | Membership is Boolean on unordered triples. P and T are disjoint because their intersection graphs have two and three edges. | The primary formula must count subsets, not raw embeddings. |
| Could the fair completion fail on overlapping triples? | A fixed P triple uses one missing edge and has probability 1/2. T is already cyclic. Linearity does not require independent triple indicators. | A fair missing-edge marginal; the candidate's independent coins provide one. |
| Could extra paths or cycles invalidate domination? | Their probabilities are nonnegative; no converse pattern correspondence is used. | None. |
| Could mixed or unrealizable signs violate the bound? | Triangle inequality bounds every ±1 sign assignment by N_P/2+N_T. | None for the formal evaluation. |
| Could the degree identity count a triple twice? | Every transitive triple has one source with two outgoing edges; a cyclic triple has none. | The completed graph must be a tournament, which it is. |
| Could flooring E[C] be unjustified? | Integer flooring is applied to each deterministic completion, then averaged. No rounding of a fractional expectation is assumed. | None. |
| Could even-n subtraction be nonintegral or fail near zero? | Half-integer mean forces variance ≥n/4; n=2k gives k(k−1)(k+1)/3. The empty case is checked separately. | None. |

The argument proves, for any formal directed chord diagram with n arrows and crossing signs ±1,

\[
\left|\frac12\sum_{P(S)}\prod_{c\in S}\epsilon_c+
\sum_{T(S)}\prod_{c\in S}\epsilon_c\right|
\le \lfloor n(n^2-1)/24\rfloor,
\]

with the bound n(n²−4)/24 for even n. The formal evaluation can be a half-integer on nonrealizable input: the isolated P word has value ±1/2. No unjustified integrality assumption about this formal value is needed. Only the tournament cycle count is rounded pointwise.

## Independent exact diagnostics

`graph_diagnostics.py` was newly written for this audit without reading the original checker. It uses signed cyclic words (positive token = tail; negative token = head), scans cyclic arcs, stores directed edges as sets, recognizes pattern types by cyclic rotation and chord relabeling, and counts cycles by direct directed-triangle predicates. Its rational calculations use Python's exact `Fraction` arithmetic. It does not restrict inputs to realizable classical diagrams.

The diagnostic child ran with PID 44027, argv `["python3", "graph_diagnostics.py"]`, cwd equal to this audit output folder, start UTC 2026-10-04T16:28:14.889206+00:00, end UTC 2026-10-04T16:28:15.978716+00:00, exit code 0. Its complete stdout/stderr bodies and hashes are retained in `graph_diagnostics.stdout`, `graph_diagnostics.stderr`, and `graph_diagnostics.receipt.json`. Stderr was empty. Source SHA256: `5d249091940e06da5e28ef224248356bb329f59231ba5e3d6341ba9faec86a12`.

All checks passed:

| Domain | Coverage | Checks |
|---|---:|---|
| Directed chord diagrams | All 1,815 rooted chord words for n=0,1,2,3,4 (up to arbitrary chord labels) | Arc antisymmetry, full reversal, Boolean P/T subsets, exact fair-completion expectation |
| Crossing signs | All 27,893 assignments across those words | Signed absolute evaluation ≤ unsigned weight ≤ expectation ≤ bound |
| Graph completions | All 39,775 completions across those words | Direct cycle counts obey the floor and parity bounds |
| Tournaments | All 33,868 labeled tournaments for n=0,…,6 | Direct cycle count equals both degree formulas; pointwise bounds; observed maxima 0,0,0,1,2,5,8 |

For the 120 rooted three-arrow words, the local histogram includes six P words, each with cyclic probability 1/2, and two T words, each with probability 1. Other words can be paths with probability 1/2, consistent with the proof's one-way correspondence. Symmetry diagnostics find one cyclic automorphism of P and three of T, while subset counting still uses one membership indicator. The formal maximum absolute evaluation is 1 for n=3 and 2 for n=4.

These are bounded diagnostics. The universal statement is established by the independent symbolic counting proof, not by finite agreement.

## Scope, independence, receipts, and remaining gap

Read input hashes agree with the parent-supplied restricted candidate and source-record hashes. The authorized source-record file contains historical/open-status opinion metadata in `prior_upstream_report`; this was disclosed in the first conclusion and did not inform the graph verdict. The audit never read original `SOURCES.md`, original `README`, original `RESEARCH_LOG`, original checker code, sibling reports, root mathematical assessments, or the primary Ohtsuki PDF. The root's authenticated original head was treated as supplied provenance, not independently reauthenticated by accessing original Git data.

No original/native files, Git index/ref, PR state, editor state, remote publication, or external human communication were changed. All new outputs are contained in this dedicated folder. The first attempted tool process could not start because the requested new cwd did not yet exist; it produced no PID. The retry created the folder and recorded the successful input-read child (PID 39408). This startup failure does not affect the mathematical result and is recorded in the research log.

**Assigned graph audit completion: 100%.** No further graph work is required to answer this assignment. The exact remaining gap for promotion of the knot result is external to this assignment: independent primary verification of the imported v3 formula, arrow direction convention, coefficients, multiplicity convention, and normalization, plus the root's target/priority/publication assessment. No solved-label or publishing recommendation follows from graph validity alone.
