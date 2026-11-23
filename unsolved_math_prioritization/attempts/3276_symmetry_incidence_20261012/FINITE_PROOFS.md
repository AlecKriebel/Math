Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Sound endpoint-incidence propagation for obstruction-cycle completion

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Fourth confirmed pass.

## Exact target and credited necessary structure

The target is: every nonempty finite tournament with at most three arc colors has a directed cyclic rainbow triangle, or a vertex reaching every other vertex by a monochromatic directed path. The color may depend on the destination. A transitive rainbow triple does not count.

We use Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2 (17 April 2009), https://arxiv.org/pdf/0904.1967v2. Its Lemma 2.1 (crediting Shen) supplies the following structure for an induced-minimal counterexample: a directed Hamilton cycle C with each vertex failing monochromatic reachability precisely to its predecessor. Lemma 2.5 strengthens each other distinct ordered pair x,y to a monochromatic path inside the proper forward interval xCy. Proposition 2.4 requires at least two colors among the incoming arcs and at least two among the outgoing arcs of each vertex. Theorem 3.1 requires all three colors incident at every vertex.

The source PDF and extracted text were re-inspected locally; their identities are recorded without redistributing either source. The incidence theorems are credited dependencies, not newly claimed or independently recertified proofs. The earlier accepted interval-propagation packet already established the bounded search through order nine and the soundness of interval propagation. This packet reconstructs all pruning needed to understand the added computation. There is no novelty or current-literature-status claim.

## 1. State and separation of actual arcs from virtual paths

Fix an order n>=3 and a cyclic word w in {0,1,2}^n. Put actual arcs i -> i+1 of color w_i, with indices modulo n. An unordered chord has up to six states: either direction and one color. A search state contains only assigned actual arcs and three transitive, positive-length monochromatic reachability relations R_c. The relations can also contain previously proved mandatory path assertions. Positive cycles may put diagonal pairs into these relations; initially an isolated vertex contributes no diagonal pair.

A completion consistent with a state must realize every assigned arc and every R_c assertion. It must contain no cyclic rainbow triangle, must have no monochromatic i-to-(i-1) path, must satisfy every proper forward-interval requirement, and must have all three incident colors and at least two incoming and two outgoing colors at every vertex. This is a necessary class containing every induced-minimal counterexample with this obstruction cycle. A state surviving the rules is not a completion certificate.

An actual-arc proposal is rejected if it creates an actual cyclic rainbow triangle or if its color-reachability closure contains a forbidden predecessor pair. A virtual path assertion is tested only by the second condition. It is never treated as an actual arc in the rainbow test or as an edge in the possible interval graph.

Adding one c-link u -> v to a transitive relation can be done by connecting each old ancestor of u, together with u itself, to each old descendant of v, together with v itself. This ancestor-by-descendant product is exactly the new closure, including when a positive cycle is created. The second engine instead inserts the link and runs Boolean Warshall closure. Either operation is committed only if no predecessor pair results; rejection leaves the old state unchanged.

## 2. Incidence-domain rule

For each unassigned chord e, form its current domain D_e by the actual-arc test above. Fixed pairs contribute their one actual arc. For a vertex x and each direction/color category, count how many incident pairs can supply that category. A category is possible exactly when its count is nonzero. These are counts of possible actual arcs, not of virtual paths.

Let I_x and O_x be the sets of possible incoming and outgoing colors. The union-incidence predicate is

- I_x union O_x = {0,1,2};
- |I_x| >= 2;
- |O_x| >= 2.

This is only a necessary relaxation: separate possible categories might require incompatible choices on the same pair. The implementation does not claim that this predicate is sufficient for an actual incident-edge assignment.

First reject when the predicate fails at any vertex. Then for every e={u,v} and each q in D_e, temporarily replace the entire contribution of D_e by the singleton state q. Delete q if the predicate then fails at u or v. Return the original domain contribution after testing, narrowed to its retained values. Reject an empty domain. Repeat sweeps until no domain changes.

### Theorem 1. Completion preservation

The incidence-domain rule preserves every completion satisfying all three vertex-incidence requirements and the supplied actual domains.

**Proof.** Fix such a completion T whose pair values are still in the domains. At each vertex every incoming or outgoing color actually used in T remains possible. Therefore the initial union-incidence predicate cannot fail. Consider a tested q which is T's value on its pair. After fixing that pair to q, every other actual value of T is still in its domain, so the actual incoming and outgoing color sets of T remain subsets of the possible sets. T's incidence requirements therefore ensure that both endpoint tests pass. Thus no value belonging to T is deleted, and no domain becomes empty while T remains a completion. Induction over the sequential deletions proves the claim. QED.

All count contributions are per pair/category, with zero or one contribution for a given directed color from an unassigned pair. Removing a domain contribution, adding a tested singleton, removing that singleton, then restoring the narrowed domain implements exactly the rule above. Counts are never reachability counts.

### Theorem 2. Termination and interaction with other pruning

Incidence sweeps terminate and can be soundly interleaved with triangle, forbidden-predecessor, and interval pruning.

**Proof.** A changing sweep removes at least one of the finitely many pair values. No sweep adds a value. All constituent rules separately preserve any valid completion, so their composition does too. The search may recompute domains from the current actual arcs and R after committing a forced arc or mandatory path; this may restore earlier relaxed possibilities before deleting them again, but cannot discard a valid completion. Every such outer-loop restart commits at least one previously unassigned actual arc or previously missing reachability pair. Only finitely many such commitments exist. If no commitment occurs, the procedure returns its branch domain. Hence the outer propagation also terminates. QED.

## 3. Proper-interval propagation after incidence filtering

From the narrowed actual pair domains construct P_c, the possible actual c-arc graph. Include actual assigned arcs. Do not insert virtual R_c links as graph edges.

For every x and forward distance d=1,...,n-2, let y=x+d and I={x,x+1,...,y}. Retain color c only if:

1. P_c[I] has an x-to-y path;
2. adjoining x R_c y and taking closure creates no forbidden predecessor pair.

Reject if no color remains. If exactly one remains, add its global path assertion to R_c and close it. If two or three remain, do not assert a particular color. Forced singleton chord domains are committed as actual arcs before continuing interval propagation.

### Theorem 3. Soundness of interval propagation

These rules preserve every completion satisfying the proper-interval requirements.

**Proof.** Such a completion has an actual monochromatic x-to-y path inside I. All its actual arc states survive sound domain filtering, so that path is in P_c[I] for its color c. Its true global endpoint relation can safely be added to R_c: composing true same-colored paths produces a true path between distinct endpoints, and cannot create a predecessor reachability forbidden in the completion. Thus at least one of its real witness colors survives. If only one remains, the completion must realize that endpoint relation. Adding it is sound. QED.

The graph P_c can become stale during one interval sweep after a virtual assertion is added. Such an assertion can only remove otherwise possible chord values on the next recomputation. The stale graph is therefore an overapproximation; it cannot remove the witness supplied by a valid completion. On a changing sweep the graph is recomputed. This is sufficient for soundness, without claiming strongest possible propagation.

## 4. Exhaustive reduced search and symmetry

After propagation, if every chord is assigned, count a completion. Otherwise branch on an unassigned chord with smallest retained domain, breaking ties in fixed lexicographic pair order. Explore every retained orientation/color value. Along a branch, the number of unassigned chords strictly decreases whenever recursion occurs. Therefore this finite DFS covers every reduced completion in its stated scope.

For the general scope generate every cycle word up to arbitrary permutation of the three color names and rotation of the obstruction cycle. Normalize colors in first-occurrence order and retain the lexicographically least rotated normalized word. These transformations preserve all constraints. Reflection is not used. The independent literal word oracle enumerates all 3^n raw words and all six color permutations and n rotations, confirming the representative count without calling the candidate canonicalizer. At order ten there are 59,049 raw words and 1,002 representatives.

A `--periodic` run fixes the single word 012012...; it cannot establish a general order bound. An explicit `--word` run is likewise only one word. The output records all scope flags, including incidence, and the validator rejects a periodic or selected-word row presented as general.

## 5. Deduction of the finite tournament theorem

Suppose all reduced minimal-counterexample scopes at orders 3 through b are completely enumerated with zero completions. If a tournament of order at most b violates the target, take a nonempty induced-minimal violating subtournament D. Orders one and two trivially have a universal monochromatic source. Hence |D|>=3. The credited source results place D in one of the reduced cycle-word scopes of its order and give every imposed incidence and interval condition. Sound pruning cannot remove it, and exhaustive branching would count it. This contradicts the zero result. Consequently the target holds through order b.

The conclusion depends on complete executions, not on the finite harnesses alone. The unrestricted conjecture, general orders larger than the completed bound, and all-size strict-periodic exclusion are not established.

## 6. Verification scope and limitations

The two reachability engines compare all recorded bounded-scope counters. A separate literal completion oracle uses no partial-state pruning and direct graph searches on complete fixed-cycle tournaments at orders three, four, and five. It counts all 32 choices of canonical/raw word scope and the four enabled/disabled requirements: triangle, predecessor, interval, incidence. Both candidate engines must match all 192 oracle comparisons.

The complete-model harness tests actual-arc and virtual-link closure, nonmutation on rejection, and soundness of propagation against sampled full models. Its new small-order incidence-positive sample is small; it is not misrepresented as abundant positive models for jointly impossible scopes.

The separate incidence harness addresses that limitation. It compares the predicate on all 1,296 directed colored four-edge stars (144 valid), then constructs 3,000 incidence-satisfying full tournaments of orders five through ten. For each, four arbitrary actual-domain boxes containing the known model must preserve every actual value. These 12,000 boxes exercise real pruning and singleton creation; a second filter call must be idempotent. The graph generator uses balanced cyclic orientations with random colors and rejection sampling; it is not uniform enumeration of all tournaments. It deliberately does not require rainbow-freeness, forbidden predecessors, or proper-interval paths, because it isolates the incidence rule's generic preservation theorem.

Hostile source mutations exercise old reachability/interval failure modes and new incidence failure modes. CLI gates reject malformed scopes. Result mutations check missing coverage, inflated bound, periodic laundering, omitted incidence, missing canonical words, nonzero completions, weak controls, and orbit corruption. Integrity checks bind file bytes; they do not substitute for executing the search. No proof assistant, SAT/DRAT certificate, or exhaustive enumeration of every labeled order-ten tournament is claimed.
