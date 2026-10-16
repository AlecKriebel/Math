# Independent adversarial mathematics review: PR #1098

Completed 2026-10-15 UTC. Problem 3000018 / AMR-029-0018.
Audited Git head: `f37a3ff66595fcf75bb18bf859be8594c3662242`.

**Decision: the complete main theorem and oriented strengthening withstand this
independent review. No actionable candidate P0–P3 issue remains.** This is
mathematical acceptance of the exact written arguments, subject to the later
priority and whole publication-package reviews. It is AI-assisted and
unrefereed, with no human peer-review, formal-certification, current-openness or
first-in-literature claim. No candidate file was edited.

## Independence, authentication and interruption

Nine submitted files were authenticated against the actual pinned Git object,
not merely against a historical manifest. The claim, full main proof and full
oriented appendix were read before the prior audit's acceptance labels were
used. INDEPENDENT_DERIVATION_FROZEN.md and its timestamp/hash receipt preserve
that pre-label derivation. The task was interrupted after source inspection
and a completed normal-runtime control suite. This resumed review kept the
frozen derivation intact, read the remaining historical audit and source
records only afterward, and did not read a sibling review's conclusions.

REPRODUCTION_RECEIPT.json freshly reauthenticates all nine Git files, both
retained primary PDFs, and the frozen derivation. The submitted eight-member
hash list agrees with those exact bytes. No omitted historical executable or
aggregate computation is adopted as a newly reproduced experiment. The fresh
programs import only this reviewer's implementation and standard Python.

An early pre-interruption harness retaining large reduction state spaces was
aborted by killing only its own process; it is explicitly not a pass. Its
bounded replacement uses exact period witnesses or stabilizing count bounds
for larger reduction schedules and retains exhaustive exploration only on
small state spaces. On resumption, one optimized execution passed all checks
but failed its final file write with ENOSPC. A stdout-only pass and then fresh
saved normal/optimized executions supersede that failed recording attempt.
No candidate mathematical defect is inferred from these harness limitations.

## Exact conclusion and target reconciliation

HALTING is NP-complete under polynomial-time many-one reductions on finite
loopless simple strongly connected conservative directed graphs with at least
two vertices and nonnegative binary configurations. The main graph permits
antiparallel arcs; the appendix removes them. Hardness holds when deleting a
specified root leaves only counter-to-return arcs, hence an acyclic graph of
depth at most one, and when the total initial chip count is polynomial
numerically in the SAT input length. Thus unary chip encoding also retains
hardness. No Eulerian restriction is claimed.

The directly read primary FL Section 3.1 asks the simple-directed hardness
question against the full strongly connected halting model. Its model and
question match this affirmative resolution. The loopless and oriented
subclasses only strengthen the hardness assertion. The precise Egres URL was
inaccessible on the fresh resumed attempt; its old page observations are
preserved as historical observations. The full explicit question in FL,
independently checked against the submitted target, supplies the necessary
mathematical scope. This review does not infer present-day openness from it.

SOURCE_INTERFACE_DERIVATION.md gives the checked primary-source interfaces,
Laplacian sign convention, source limitation and full corrected certificate
argument. Bibliographic history beyond those interfaces remains a separate
priority task.

## Bank identity and Boolean encoding

For modulus `q>=2`, periodic indicator `h` of nonempty `A`, and
`c_a=1+h(-a-1)-h(-a)`, each multiplicity is 0, 1 or 2 and the sum is exactly
`q`. These are distinct vertices, including repeated offsets. With
`S(k)=sum_a c_a ((a+k) mod q)`, the offsets wrapping at step `k` are exactly
`a=-k-1`. Consequently

    S(k+1)-S(k) = q-q c_(-k-1) = q(h(k+1)-h(k)).

The average of `S` is `q(q-1)/2`; the average of `q h` is `|A|`. Therefore
`S(k)=K+q h(k)` for `K=q(q-1)/2-|A|`. The maximum `K+q` is attained precisely
on `A`. Full `A` is a valid constant-storage boundary case. Empty `A` is not
used; otherwise the chosen maximum would not be attained. Negative `k` in the
identity is only a residue parameter. A negative `K` for some modulus-two
boundary cases is not a negative initial chip count.

Normalize 3-SAT by removing duplicate literals and tautological clauses,
checking empty clauses, and relabeling the distinct variables actually
occurring. The usual encoding has `n<=L`; a huge binary variable name or unused
declaration need not be expanded. Malformed source strings can be rejected
and sent to a fixed valid NO instance, making the reduction total.

Use distinct variable primes at least three and variable allowed sets `{0,1}`.
A clause on at most three distinct variables uses the product of only those
primes, with the CRT representatives of its satisfying Boolean assignments.
There are at most eight local assignments, and a nonempty normalized clause
has `2^t-1` satisfying ones. The clause set is nonempty and proper. All
predicates agree at an integer `k` exactly when the original formula has a
satisfying assignment. Both directions are exact: variable banks reject
non-Boolean residues, while CRT extends any satisfying assignment. No
exponentially large global period is expanded in the reduction algorithm.

## Graph, conservation and canonical checkpoints

Let `Q=sum q_b`, `P=max q_b`, and `B=sum(K_b+q_b)`. The main construction has
one root, `Q` distinct counters and `P-1` return vertices. Root-to-counter,
counter-to-root, counter-to-return and return-to-root arc types are disjoint.
Each ordered pair occurs once. Every modulus-`q` counter has outdegree `q`,
the root has outdegree `Q`, and each return has outdegree one. A maximum-bank
counter reaches all return vertices. Every vertex reaches the root, so strong
connectivity holds. Deleting the root leaves only counter-to-return arcs.

Initialize counters with their offsets, returns with zero and the root with
`Q+B-1-S(0)`. Since `S(0)<=B`, the root is nonnegative. Total mass is exactly
`C=Q+B-1` and firing conserves it. Return vertices are ordinary vertices with
arcs to the root; they never delete chips.

Analyze one legal order: at a checkpoint keep all non-root vertices stable;
fire root if legal, process counters and then returns. A stable counter gains
one chip from that root firing and has no other incoming arc, so it fires
zero or one times. After the counter phase, each return fires exactly as many
times as its current chips. Those phases are finite and legal, even if root
becomes active before they finish. Delaying an active root is permitted.

At checkpoint `k`, counters contain `(a+k) mod q`, returns are empty and root
contains `C-S(k)`. Hence root stability is equivalent to

    Q+B-1-S(k)<Q  <=>  S(k)>B-1  <=>  S(k)=B.

Integrality and the proven upper bound `S(k)<=B` justify the middle step.
Each bank's deficit is either zero or its positive modulus. There is no
cancellation: total equality means every predicate holds.

A satisfying CRT representative implies a stable checkpoint unless the
canonical process already stopped earlier, which also proves halting. If the
formula is unsatisfiable, every checkpoint permits another root firing, and
the finite legal blocks concatenate into an infinite legal word. Its possible
exponential length or global period is a proof device, never an algorithmic
operation of the reduction.

## Arbitrary schedules and least action

The canonical schedule alone is not substituted for ordinary halting. Suppose
`f>=0` is any stabilizing vector with stable `z=x-Delta f`. In any legal word,
at the first firing that would exceed `f_v`, the count at `v` is exactly
`f_v`, all other counts are at most their `f` values, and nonnegative incoming
arc multiplicities imply at most `z_v<d_v` chips. That firing is impossible.
Every legal word is bounded coordinatewise by `f`, whether or not `f` was
legally realized. This proves termination of every maximal play when a stable
checkpoint exists, and rules out any stabilization when an infinite legal
word exists. There is no fairness assumption and no silent replacement of
some-play halting by an unrelated scheduling model. Early voluntary stopping
at an active state does not count as halting.

## Polynomial size, totality and oriented graphs

The standard polynomial bound on the first `n` primes gives
`U=O(n log(n+1))`. With `H=O(L)` banks, each expanded modulus is at most `U^3`,
`P<=U^3`, `Q<=HP`, vertex count is `Q+P`, and arc count is
`Q+sum q_b^2+P-1`. Offset scans, explicit simple adjacency lists or matrices,
and local CRT computations are polynomial in `L`. Numeric total chips obey
`C<=Q+sum q_b(q_b+1)/2`, also polynomial. There is no binary-to-unary expansion
of an exponential multiplicity, no exponential vertex list and no simulation
of the global period as part of the reduction.

For all nontrivial reduction banks `q>=3`, consistency with stable capacity
can be checked directly:

    (E-N)-C = sum_b [q_b(q_b-3)/2+|A_b|] >= 0.

That observation is credited prior work, not the SAT equivalence itself.
Empty clauses and malformed source inputs map to the two-cycle `(1,0)` NO
case; an empty conjunction maps to `(0,0)` YES. The latter may be reached
after tautology deletion. Both preserve the graph restrictions.

The oriented appendix instead has `P` returns and replaces every
counter-to-root arc by one more counter-to-return arc. All arcs follow
root-to-counter-to-return-to-root; no opposite pair remains. Outdegrees,
conservation, offset evolution, root storage and both SAT implications are
unchanged. Its vertex and arc counts each increase by one, preserving capacity
and polynomial bounds. Three-cycle `(0,0,0)` YES and `(1,0,0)` NO instances
replace the preprocessing cases; deleting root leaves one arc. The appendix
is therefore proved for every case, rather than only for nontrivial formulas.

## Polynomial-bit NP certificate and source defect

Section 7 correctly supplies a self-contained specialization of the credited
FL membership method. A nonnegative binary vector `f` with
`0<=x-Delta f<d` is a polynomially checkable stabilizing certificate by least
action. On a halting instance take the actual odometer and primitive positive
period `pi`. Rooted-tree counts give `pi_v<=(N-1)^(N-1)`. At least one
coordinate `w` has `f_w<pi_w`, since otherwise `f-pi` would be a smaller
nonnegative stabilizing vector contradicting the actual word's least-action
bound.

For each arc `u->v`, final balance, nonnegative `x` and integral stable `z`
give `f_u+1<=d_v(f_v+1)`. Following a simple path from `u` **to** `w` yields
`f_u+1<=(N-1)^(2N-2)`. Thus certificate coordinates have `O(N log N)` bits,
independently of how long the actual firing word is. Input chip bits are
included in verification cost. For `N=2`, only the two-cycle occurs and
halting nonnegative input and odometer are zero; the bound is exact.

Direct inspection found that FL PDF page 10's informal edge inequality omits
the stable residual slack. That intermediate statement is false for arcs
`0->1, 1->0, 1->2, 2->0`, initial `(1,0,0)` and terminating word `(0)`: it
would require `1<=2*0`. The candidate already uses the corrected additive
one, which gives `1+1<=2*(0+1)`. The complete derivation and exact control are
in SOURCE_INTERFACE_DERIVATION.md and both saved checker outputs. This is a
source-line limitation, not a candidate gap or a claim that the established
membership conclusion is false. No proof repair is needed.

## Fresh exact controls and their limits

Both saved resumed normal and optimized executions return exactly identical
JSON bytes. The principal result also matches the completed pre-interruption
normal output byte for byte. Four positive runs and four expected explicit
guard failures are recorded in REPRODUCTION_RECEIPT.json. No `assert` is used
for the control guards, and deliberate invalid runs fail in both modes.

The main fresh implementation checks:

- All 501 nonempty residue sets for moduli 2 through 8, at 10,647 negative,
  zero and positive positions, including constant/full-set boundaries.
- Every strongly connected loopless simple graph on 2 through 4 vertices:
  1,625 graphs, 56,580 configurations of total mass zero through three,
  293,008 reached states and 330,564 individual legal edges. Exhaustive
  successor graphs test terminal/cycle dichotomy and stable uniqueness.
  The 46,391 halting inputs check odometer least action, tree orientation,
  period reduction and the candidate bit bound. There are 6,480 rooted-tree
  coordinate checks and 357,152 corrected edge-inequality checks.
- 183 independently supplied nonnegative stabilizing vectors on small graphs,
  showing that certificate soundness does not assume the supplied vector is
  itself a legal firing word.
- 704 explicit main/oriented reduction graphs from 283 small predicate pairs
  and 69 three-variable formula cases, including inconsistent units and all
  eight forbidden-assignment clauses. There are 498 YES and 206 NO cases,
  641,442 individual legal firings, 10,256 canonical root firings and 1,722
  deterministic noncanonical schedules. Larger nonhalting schedule checks use
  exact positive period witnesses rather than a speculative cutoff verdict.
- A separate full-successor exploration on 18 small reduction inputs,
  216 states, checking SAT equivalence against every legal successor.
- Four fixed two/three-cycle totality cases and seven damaged controls
  covering the storage sign, root threshold, parallel arc, invalid certificate,
  kernel orientation, missing source slack and conservation.

The original conservation negative control is only a direct local mass
identity check. It is not misrepresented as an entire damaged-game experiment.
The new semantic addendum supplies that stronger experiment: on inconsistent
modulus-three banks, conservative main and oriented graphs have explicit
legal lassos of lengths 21 and 27. Replacing return firings by deletion of
their chips makes those same inputs terminate, losing four and six chips.
This detects an actual semantic change of outcome.

The addendum also checks ten malformed source encodings, five preprocessing
and relabeling cases (including a 1,001-digit variable identifier), and
128-, 1,024- and 16,384-bit nonnegative inputs whose mass exceeds the
two-cycle's stable capacity. The latter are exact mass certificates; no
exponentially long firing simulation is claimed. The addendum is byte-identical
under normal and optimized execution and its explicit invalid guard fails in
both modes.

These finite controls are supporting evidence. They cannot certify all graphs,
all SAT inputs, the general prime bound, all possible literature, or the
complete publication package. The analytic arguments above and in the frozen
derivation establish the unbounded theorem. Previously omitted programs were
neither recovered nor rerun; their historical aggregate claims remain labeled
historical.

## Disposition

No candidate P0, P1, P2 or P3 concern remains in this full mathematics family.
The exact main and oriented theorems may advance to extensive priority review
and, if appropriately framed, preprint preparation and fresh whole-package
reviews. This report authorizes no conclusion of novelty and performs no
publication, tracker mutation, PR disposition, branch/index mutation or
external contact. The immutable submitted edition and queue status are
unchanged.
