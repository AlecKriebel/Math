# Independent adversarial audit of every feasible arborescence in PR107

Target: 30003997 / OWR-16633-014, original draft head `cc2ae01897135b35bee135917819e782a220f2c1`.

Candidate input: sibling `original_source_authentication_20261006/original_attempt/PROOF.md`, SHA256 `2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8`, 8009 bytes.

Audit completed: 2026-10-06 UTC. This is independent verification of an already complete candidate, not an additional central proof-search attempt. Completion estimate: 100% of this delegated verification scope. No original review, author replay, original verifier, or other current family's report was read. No external outreach or Git/publication action was performed.

## Verdict and strongest verified scope

The mathematical reduction is valid for arbitrary formula size. In fact, it gives an exact bijection between **all** feasible spanning out-arborescences and pairs consisting of a Boolean assignment and one distinct variable selected from each nonempty, non-tautological clause. Every such tree has the cost claimed in candidate equation (6), and minimizing over all such trees gives the exact minimum number of unsatisfied clauses in equation (7).

The zero-threshold decision problem is NP-complete on simple four-layer DAGs with consecutive-layer arcs, all vertices reachable from the designated root, every nonroot indegree at most three, and every destination-by-arc cost in `{0,1}`. The optimization problem is strongly NP-hard on that class. Replacing every coefficient by coefficient plus one gives costs in `{1,2}` and preserves every minimizing tree, with the universal offset `4n+3m`, establishing strong NP-hardness at the positive threshold `4n+3m`.

No unsupported central lemma, equivalent-hardness transfer, hidden exponential encoding, or consistency failure remains. There is one minor boundary clarification needed in the written candidate: line 27 should explicitly handle an empty clause before asserting that every remaining clause is nonempty, and should exhibit the fixed promise-preserving yes/no instances it already acknowledges. Section 3 below supplies them. The claimed theorem does not depend on repairing the central construction; this is a total-input presentation correction.

Historical priority, novelty, literature completeness, related-target equivalence, and the source's motivational equivalence to Wong's formulation are outside this audit's result. No novelty conclusion follows from the theorem check. The source record's old prose about root-dependent spanning trees is stale triage prose for a different formulation; its displayed fixed-root directed statement and the candidate match the literal target.

## 1. Source reconstruction, assumptions, and independent pin

I independently extracted and rendered the complete relevant contribution in `owr.pdf`, PDF pages 46-47, printed pages 3014-3015. The heading is Volker Kaibel's *Open Problem: Arborescences and NP-hardness*. Problem 1, on printed page 3014, is the undirected all-roots tree problem. Problem 2, on printed page 3015, is the directed fixed-root problem under audit.

For Problem 2, the source gives a directed graph `D=(V,A)`, a root `r`, and a vector `c^v in R^A` for every `v != r`. It seeks an arborescence `T subset A` minimizing

\[
 C(T)=\sum_{v\in V\setminus\{r\}} c^v(P_T^v)
     =\sum_{v\ne r}\sum_{a\in P_T^v}c^v_a,
\]

where `P_T^v` is the directed path from `r` to `v` in `T`. Requiring such a path for every vertex makes the feasible object a spanning out-arborescence rooted at `r`: root indegree zero, every other vertex indegree one, and root reachability of every vertex. The cost is charged once per destination path using that destination's own vector. An early arc traversed by several paths can be charged several times and with different coefficients.

The original real-vector wording is an optimization formulation, not a finite-input decision language until a numeric representation is chosen. The candidate explicitly chooses binary rationals for its NP-membership claim and uses integer coefficients for hardness. This is appropriate: a hard integer subclass proves hardness of the original permitted objective without making a decision-complexity claim about unrepresented arbitrary reals.

I also independently rendered `karp-original.pdf`, PDF pages 10-11, printed pages 94-95. The main theorem on page 94 states completeness for the listed problems. Item 11 on page 95 is satisfiability with **at most three** literals per clause. Thus the reduction can use units and two-literal clauses; there is no need to pretend that every clause has exactly three distinct literals.

`SOURCE_FIRST.md` and `SOURCE_FIRST_PIN.json` were saved before candidate inspection. `INITIAL_COMPARISON.md` and `INITIAL_COMPARISON_PIN.json` were then saved after candidate inspection and before any other audit or review material. The pins record the chronology, exact bytes, and hashes. The first attempted nested instruction-file lookup in the isolated checkout failed because that file was absent there; the actual `/Users/alec/Documents/Math/unsolved_math_prioritization/AGENTS.md` was then read and hashed. This environment lookup failure did not affect source parsing or mathematics.

## 2. Exact computational claim and success criteria

Use an explicit finite directed graph, explicitly identified root, one binary-rational coefficient `c^v_a` for every relevant destination/arc pair, and a binary-rational threshold `K`. Rational denominators are positive. The decision question is whether there exists a spanning out-arborescence of objective at most `K`. General rational inputs can have negative coefficients; NP membership does not depend on sign. In the reduction all coefficients are nonnegative, so threshold zero is equivalent to optimum exactly zero.

Success requires a polynomial many-one reduction from finite at-most-three-literal CNF satisfiability, including trivial syntax cases. It also requires an exhaustive characterization of feasible trees, an exact objective derivation, a polynomial bound for the **dense** input representation, and polynomial-bit exact verification of a certificate. To justify the positive-cost transformation, the added unit cost must have the same total in every feasible tree, not merely in a selected canonical tree or an optimum. These checks have all been met below.

## 3. A total preprocessing rule and checkable fixed instances

Let the source formula be a conjunction of clauses, each of size at most three. A literal is a variable name and a sign. Perform these operations:

1. If any clause is empty, return the fixed no-instance described below. An empty disjunction is false, so the formula is unsatisfiable regardless of all other clauses.
2. Within each clause, discard repeated copies of the same signed literal. This preserves its Boolean value.
3. Discard any clause containing both signs of a variable. Such a disjunction is identically true.
4. If there are no remaining clauses, return the fixed yes-instance described below. The empty conjunction is true.
5. Otherwise discard unused variable names and rename the distinct variables that occur in remaining clauses consecutively as `x_1,...,x_n`. Every remaining clause is now nonempty, uses at most three distinct variables, and has one sign per variable.

These operations preserve satisfiability. They handle the zero-variable case: a literal-free formula is either the empty conjunction or contains an empty clause. Repeated clauses may be retained; they do not cause parallel arcs because clause vertices are distinct. Variables discarded with tautological clauses are harmless. An already explicit unused variable could instead be retained; the construction still works, but compact renaming makes the encoding bound immediate even for huge binary-encoded variable names.

The fixed yes-instance is the ordinary construction on the formula `(x_1)`. It has `n=1,m=1`, five vertices and five arcs. Its two trees have binary costs 0 and 1. The positive offset is 7, so its positive optimum is 7 and the positive decision threshold is 7.

The fixed no-instance is the ordinary construction on `(x_1) AND (not x_1)`. It has `n=1,m=2`, six vertices and six arcs. It has exactly two trees, and each has binary cost 1. The positive offset is 10, so each has positive cost 11 and the positive decision threshold is 10.

Both fixed instances have four **nonempty** layers, simple consecutive-layer arcs, root reachability of every vertex, and nonroot indegree at most three. Thus even if the four-layer promise is understood to require each layer to be nonempty, the total reduction satisfies it. All coefficients belong to the claimed set, and all thresholds are finitely encoded and bounded.

The candidate's phrase that deletion of tautologies and repeated literals leaves every clause nonempty is not literally true for an input already containing an empty clause. Its following sentence acknowledges fixed trivial yes/no handling, so this is not a central correctness failure. Nonetheless the explicit rule above should replace that implicit boundary branch for a fully checkable published many-one reduction.

## 4. Construction and polynomial encoding, including dense costs

For an ordinary preprocessed formula let `I_j` be the set of variables occurring in clause `C_j` and `k_j=|I_j|`, so `1 <= k_j <= 3`. There are vertices

\[
 L_0=\{r\},\quad L_1=\{t_i,f_i:1\le i\le n\},\quad
 L_2=\{v_i:1\le i\le n\},\quad L_3=\{z_j:1\le j\le m\}.
\]

Include arcs `r -> t_i`, `r -> f_i`, `t_i -> v_i`, `f_i -> v_i` for each `i`, and `v_i -> z_j` for each `i in I_j`. No other arcs exist. Write

\[
 N=|V|=1+3n+m,\qquad M=|A|=4n+\sum_j k_j\le4n+3m.
\]

For destinations `t_i,f_i,v_i`, every coefficient is zero. For `z_j`, the only possibly nonzero coefficients are

\[
 c^{z_j}_{r t_i}=\mathbf1[\neg x_i\in C_j],\qquad
 c^{z_j}_{r f_i}=\mathbf1[x_i\in C_j].
\]

All other coefficients are zero, including coefficients on selected variable-to-clause arcs. Coefficients on arcs not belonging to a destination's selected path simply do not enter its objective; there is no shared scalar-cost assumption.

Let `L` denote the source input bit length in the usual explicit clause-list representation. There are at most `L` literal occurrences and clause records. Compact renaming ensures `n,m=O(L)` regardless of the numerical size of original variable IDs. Building the graph takes polynomial time. Its endpoints take `O(log N)` bits each. The complete dense table has

\[
 (N-1)M=(3n+m)\left(4n+\sum_j k_j\right)
       \le(3n+m)(4n+3m)=O(L^2)
\]

entries, each a single constant-sized integer. Including arc/vertex labels and table metadata remains polynomial, e.g. `O(L^2 + L log L)` bits under an indexed dense representation. Constructing rows explicitly takes `O((N-1)M)` coefficient writes. No sparse/oracle representation is needed to obtain polynomial output size. This also proves the size claim for the positive-cost table.

## 5. Exhaustive characterization of all feasible trees

Let `T` be **any** feasible rooted spanning out-arborescence of the constructed graph.

For each `t_i` and `f_i`, the sole incoming arc in the full graph is from `r`. Each must have indegree one in `T`, so both `r -> t_i` and `r -> f_i` are forced.

The only incoming arcs of `v_i` are `t_i -> v_i` and `f_i -> v_i`. Its tree indegree is one, so exactly one is selected. Define `sigma_i=1` for the first choice and `sigma_i=0` for the second. In particular, a clause cannot use a different truth parent for a shared variable vertex: the selected parent of `v_i` belongs to one common tree and is fixed once for all paths using `v_i`.

The only incoming arcs of `z_j` are `v_i -> z_j` for `i in I_j`. Exactly one is selected; denote its index by `a_j in I_j`. No clause vertex has outgoing arcs. These are all the possible tree arcs; any supposed exotic path, skipped layer, alternative parent, or inconsistent reuse would need an arc outside the constructed graph or violate indegree one.

Conversely, choose any Boolean tuple `sigma in {0,1}^n` and any tuple `a_j in I_j`. Take all `2n` forced root-to-marker arcs, the indicated one parent of every `v_i`, and `v_{a_j} -> z_j` for every `j`. Each nonroot vertex has exactly one selected incoming arc, and the root has none. There are exactly `2n+n+m=N-1` selected arcs. Every vertex is reached by induction on its layer: markers from `r`, variable vertices from their selected marker, and clause vertices from their selected variable. All arcs strictly increase the layer, so cycles are impossible. This is a spanning out-arborescence.

The encoding in either direction is unique, hence a bijection:

\[
 \mathcal T\ \longleftrightarrow\
 \{0,1\}^n\times\prod_{j=1}^m I_j,
 \qquad |\mathcal T|=2^n\prod_j k_j.
\]

This is a formal arbitrary-size argument, not a finite-experiment inference. It also handles an explicitly retained unused variable, whose truth-parent choice affects no clause. For an empty conjunction the empty clause-choice product is 1; the raw construction then has zero objective, but the total reduction uses the fixed yes-instance to preserve nonempty layers.

## 6. Exact objective and global consistency

For the tree corresponding to `(sigma,a)`, every marker path has length one. The path to `v_i` is `r -> t_i -> v_i` if `sigma_i=1` and `r -> f_i -> v_i` if `sigma_i=0`. All costs for these destinations are zero.

The path to `z_j` must extend the selected path to `v_{a_j}` by its selected last arc. Let `ell_{j,a_j}` be the unique signed literal for this variable in `C_j`. There are four cases:

| Selected marker | Literal sign | Charged root-arc coefficient | Literal truth |
|---|---|---:|---|
| `t_i` / `sigma_i=1` | positive `x_i` | 0 | true |
| `t_i` / `sigma_i=1` | negative `not x_i` | 1 | false |
| `f_i` / `sigma_i=0` | positive `x_i` | 1 | false |
| `f_i` / `sigma_i=0` | negative `not x_i` | 0 | true |

The remaining two arcs of the three-arc clause path have coefficient zero. Thus, for every feasible tree,

\[
 C(T)=\sum_{j=1}^m\mathbf1[\ell_{j,a_j}\text{ is false under }\sigma].
\]

There is no cancellation: every summand is zero or one. For a satisfying assignment choose one true literal in each clause, yielding a zero-cost tree. For a zero-cost tree every selected literal is true, so every clause is true under the one global tuple `sigma` determined by its variable parents. This proves the zero-threshold equivalence in both directions.

For a fixed `sigma`, the admissible `a_j` choices are independent because they change only the incoming arc of the distinct sink vertex `z_j`. If `C_j` is true there is a zero-cost choice; if `C_j` is false every choice costs one. Hence

\[
 \min_{a\in\prod_j I_j} C(T_{\sigma,a})
   =\#\{j:C_j\text{ is false under }\sigma\},
 \quad
 \min_{T\in\mathcal T}C(T)
   =\min_\sigma\#\{j:C_j\text{ is false under }\sigma\}.
\]

A satisfiable formula can still have a positive-cost tree if it selects a false literal; the proof requires existence/minimization, and does not make an invalid assertion that every tree on a satisfiable formula has zero cost. Repeated clauses simply supply repeated, independently selectable sinks and are counted with their actual multiplicity.

## 7. Every graph promise

| Candidate promise | Exhaustive check |
|---|---|
| Simple directed graph | All ordered endpoint pairs are distinct; a clause has at most one incidence for a variable after preprocessing. There are no loops or parallel arcs. |
| Four layers | The four displayed sets partition the vertices. Ordinary nontrivial inputs have `n,m >= 1`; fixed constants also have four nonempty layers. |
| Every arc goes to the next layer | Root-marker arcs go `0->1`, marker-variable arcs `1->2`, and variable-clause arcs `2->3`. |
| Acyclic | Layer index strictly increases along every arc. |
| Every vertex reachable from `r` | Marker paths have length 1, either variable path has length 2, and every nonempty clause has an incident variable giving a length-3 path. Fixed instances also satisfy this. |
| Feasible tree always exists | The converse construction in Section 5 provides a tree for any assignment and any clause-parent selections. No satisfiability premise is needed. |
| Every nonroot indegree at most 3 | Marker indegree is 1; variable indegree is 2; clause indegree is `k_j <= 3`. |
| Every destination-arc cost in `{0,1}` | Every coefficient is an indicator or explicitly zero, including off-path and auxiliary-destination entries. |

Root outdegree and variable outdegree can be unbounded; neither is promised by the candidate. I make no added bounded-outdegree or bounded-occurrence claim.

## 8. Exact rational NP membership and bit complexity

Suppose the complete finite input has bit length `B`, `N` explicit vertices, and `M` explicit arcs. A certificate can give `N-1` arc indices, of length `O(N log(M+1))`. Reject invalid arc indices, repeats, wrong cardinality, root indegree other than zero, or nonroot indegrees other than one. A BFS/DFS on those arcs verifies that all vertices are reachable from `r`, which, with the indegree test, verifies a spanning out-arborescence. Equivalently a cycle test may be added, but root reachability already excludes any separate directed cycle component.

For the valid tree, reconstruct the root-to-destination paths from the certified parent pointers. They are simple and have length at most `N-1`. The total number `s` of coefficient terms is at most `(N-1)^2`. No coefficient `c^v_a` is used twice for the same destination because that path is simple; the selected destination-arc entries form a subset of the input table.

Let each selected term be `p_i/q_i` and let the threshold be `p_0/q_0`, with positive denominators. Form the exact common denominator

\[
 Q=q_0\prod_{i=1}^{s}q_i.
\]

Repeated denominator *values* are permitted but the input entries are distinct; all included bits are still bounded by the total input length. The bit length of `Q` is at most the sum of denominator bit lengths plus a constant, hence `O(B)`. The signed numerator of the objective is

\[
 S=\sum_{i=1}^{s}p_i(Q/q_i).
\]

Each term has `O(B)` bits and the sum has `O(B+log(s+1))` bits. Compare `S` with `p_0(Q/q_0)` using exact signed integers. Constructing `Q`, divisions by its known factors, additions, multiplications and comparison all take polynomial time in `B,N` with standard binary arithmetic. An iterative exact-fraction implementation also has denominator length bounded by the sum of the involved input denominator lengths; floating point or a presumed small common denominator is unnecessary.

This remains valid for zero, negative, unreduced, or unequal rational entries and for rational thresholds. Therefore the general explicitly encoded binary-rational decision problem is in NP. The reduced binary zero-threshold language is a subclass with an even simpler certificate cost check, so its NP-hardness yields NP-completeness. I do not assert NP membership for a problem where arbitrary real vectors are supplied without a finite representation.

## 9. Positive costs and strong NP-hardness

Define `d^v_a=c^v_a+1` for **every** destination-arc entry, including auxiliary rows and entries on arcs absent from that destination's path. In any feasible tree, a root-to-layer-`h` path has length exactly `h`, because the root is in layer zero and every arc increases its layer by one. This conclusion is about every feasible tree.

There are `2n` marker destinations at depth 1, `n` variable destinations at depth 2, and `m` clause destinations at depth 3. Hence for every feasible `T`,

\[
 D(T)=\sum_{v\ne r}\sum_{a\in P_T^v}(c^v_a+1)
     =C(T)+\sum_{v\ne r}|P_T^v|
     =C(T)+(2n+2n+3m)
     =C(T)+4n+3m.
\]

Thus the added term is constant on the complete feasible set. The positive and binary objectives have the same ordering and the same minimizing trees. Since `C(T)>=0`, existence of a tree with positive cost at most `4n+3m` is equivalent to existence of a zero-cost tree. All positive coefficients are 1 or 2. For the ordinary branch the threshold satisfies `4n+3m <= 3(N-1)` and is strictly positive. The explicit constant branches have thresholds 7 and 10.

This proves bounded-numeric hardness: the reduction is polynomial even if all coefficients and the threshold are written in unary. Binary coefficients are bounded by 1 with threshold 0; positive coefficients are bounded by 2 with threshold linear in graph size. Therefore the optimization problem remains NP-hard under polynomial bounds on every numerical input, which is the strong NP-hardness claim. The restricted decision versions are likewise NP-complete. There is no reliance on large numbers, negative costs, long paths, cycles, or unsatisfiable feasibility promises.

Adding one need not be a constant shift on arbitrary DAGs with unequal possible root-path lengths. The candidate only applies it to this consecutive-layer construction, where the formal calculation is valid.

## 10. Adversarial challenges and honest failed controls

| Challenge | Evidence / result | Exact remaining gap |
|---|---|---|
| Could a tree omit a root-to-false marker or include both truth parents? | Marker indegree one forces both root arcs; variable indegree one excludes both marker parents. | None. |
| Could different clauses assign opposite truth values to the same variable? | Their paths merge at the same `v_i`, which has one tree parent. | None. |
| Could a noncanonical tree bypass the encoded literal or use a cycle? | No other incoming arcs exist and layers strictly increase. Complete bijection proves exhaustion. | None. |
| Is cost charged only on selected last arcs rather than full destination paths? | Exact table evaluation charges the first root arc using `c^{z_j}`; last arcs have zero coefficients. | None. |
| Do satisfied clauses necessarily cost zero in every tree? | No; the proven statement is selectable zero cost and a minimum identity. Finite mixed-sign test includes bad selections. | None. |
| Does an empty clause remain reachable under the raw gadget? | **Failed negative control:** raw `(empty)` has a clause sink of indegree zero, giving 0 feasible trees. | Candidate should explicitly route this syntactic case to the fixed no-instance. |
| Does a tautology work if one skips deletion? | **Failed negative control:** raw `(x_1 or not x_1)` has Boolean optimum 0 but both tree costs are 1, since both root-marker coefficients are 1. | None after the deletion already specified by the candidate. |
| Do sparse huge variable names make a huge graph? | Total preprocessing relabels actual occurring names; a literal named `10^12` becomes `x_1`. | None under ordinary explicit SAT encoding; a compact-renaming sentence improves exposition. |
| Could exact rational denominators make NP verification exponential? | Product denominator bit length is bounded by the sum of input denominator bits, `O(B)`; arithmetic stays polynomial. | None. |
| Could the positive shift change a tree's relative cost? | Every feasible path length equals its layer, yielding the same `4n+3m` for every tree. | None. |
| Does hardness rely on an equivalent unsupported central claim? | Reduction is direct from the primary complete source SAT problem and has a total polynomial mapping. | None. |

The empty-clause and tautology failed controls are preserved in `FINITE_CHECK_RESULTS.json`; they have not been suppressed as inconvenient cases. They deliberately apply the raw gadget outside its nonempty/non-tautological assumptions, and reveal exactly why the preprocessing conditions matter. They do not falsify the corrected total reduction.

## 11. Independent finite computation and reproducibility

`AUDIT_CHECK.py` was independently written without reading the original verifier or any review. Its graph constructor creates explicit dense coefficient dictionaries. The main enumeration method tests **all** subsets of `|V|-1` arcs and accepts a candidate only using generic indegree and root-BFS arborescence tests. It does not enumerate a pre-assumed assignment-tree family. Larger supplementary cases use generic incoming-parent products and still pass each candidate through the same tree test.

Run `python3 AUDIT_CHECK.py` in this folder. The completed run on 2026-10-06 checked:

- all 165 clause multisets with up to three clauses over the eight canonical nonempty, non-tautological clauses on two declared variables; this includes repeated clauses and unused variables;
- the empty conjunction and all 26 one-clause canonical formulas on three variables;
- the eight-ternary-clause Boolean cube on three variables, whose every assignment falsifies exactly one clause, enumerating all 52,488 trees and obtaining optimum 1;
- a mixed-sign multi-clause case and 10 total-preprocessing boundaries, including empty clauses, no clauses, all tautologies, repeated literals, opposite units, tautology plus empty clause, and sparse huge variable names.

Overall: **194 regular formula cases, 10 boundary cases, 55,086 feasible trees checked; PASS.** For every feasible tree it checked the exact objective from actual paths and coefficients, the selected-false-literal identity, assignment/selection-key uniqueness, layer path lengths, and the positive offset. For each formula it also checked the exact tree count, every assignment's optimal cost, Boolean optimum, positive optimum, graph restrictions, and dense table dimensions.

`FINITE_CHECK_RESULTS.json` contains the full formula list, sizes, counts, optima, boundary routes and negative diagnostics. These computations supplement the universal proof in Sections 3-9; they do not establish an arbitrary-size claim by testing small instances. No test error occurred in the completed run.

## 12. Corrections, open concerns, and route status

Required minor candidate correction at `PROOF.md:27`: make the empty-clause and empty-conjunction branches explicit, with the fixed yes/no gadgets and thresholds of Section 3, before saying all remaining clauses are nonempty. This is an acknowledgment made concrete, not a new reduction mechanism. It takes no new proof-search turn.

Optional presentation improvements: mention relabeling occurring variable names and give the dense entry count; give the exact rational denominator bit argument; identify Karp's original item 11 explicitly. They are supplied in this audit and are not mathematical obstructions in the original conventional formulation.

The stale `source_record.json` prose describing root-dependent spanning trees should not be reused as a description of this target. The literal source, displayed record statement, and proof are unambiguous about fixed-root directed path costs. Whether curation metadata must be edited is a parent integration decision; no change was made here.

| Family | Mechanism | Evidence | Status | Exact gap |
|---|---|---|---|---|
| Independent all-trees reduction adversary | Characterize the complete feasible set; derive exact destination costs and finite bit bounds; attack preprocessing and positive shift | Primary-page visual parsing, pinned initial comparison, arbitrary-size proof, independent generic enumeration and failed assumption controls | Verified with minor boundary presentation correction | No central mathematical gap. Priority and novelty unassessed. |

No route was marked blocked because no step transfers the central difficulty to an unsupported claim. The strongest verified result is the restricted NP-completeness and strong NP-hardness theorem stated at the beginning. The remaining concern is presentation of the already acknowledged total preprocessing branch, plus nonmathematical priority questions expressly outside this verification.
