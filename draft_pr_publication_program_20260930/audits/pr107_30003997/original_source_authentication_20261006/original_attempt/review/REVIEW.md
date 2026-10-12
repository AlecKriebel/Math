# Independent adversarial review: destination-dependent path-cost arborescences

**Verdict: PASS — complete proof of the stated hardness result and of the exact source target.** No mandatory correction was identified. The justified campaign status is **claimed_solved, 1/5 attempts**. This is a separate AI review, not human peer review; historical priority and novelty remain unestablished.

The frozen `PROOF.md` has SHA-256 `2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8`. The reviewed proof, verifier and submitted receipt are copied unchanged under `author_replay/`.

## Exact original objective

I read the complete short contribution by Volker Kaibel, *Open Problem: Arborescences and NP-hardness*, in [OWR50/2018](https://ems.press/content/serial-article-files/46772), printed pp.3014–3015, and inspected the rendered p.3015. Problem2 has a directed graph, one fixed root, and a separate arc-cost vector for each nonroot destination. Its objective is the sum, over destinations v, of **that destination's** costs along its root-to-v path in the arborescence.

The submitted objective is exactly this one. It is not a sum of a single common cost over tree arcs, nor the ordinary shortest-path tree problem. Every vertex needs its root path, so omitting inconvenient vertices as in a Steiner tree is not an option. The construction uses out-arborescences, consistent with the displayed directed root-to-v paths.

Problem1 on the preceding page instead concerns an undirected tree and all induced root orientations. It is a distinct optimization model. The submitted proof is directly for Problem2 and requires no equivalence or transfer from Problem1. The same high-level assignment/literal-selection idea in the two packages is explicitly credited. The supplied record30003998 is a literal duplicate of Problem2 and is not a separate mathematical target.

The classical NP-complete input problem is satisfiability with at most three literals per clause. [Karp's primary 1972 scan](https://www2.seas.gwu.edu/~simhaweb/champalg/tsp/papers/KarpOriginal.pdf), printed pp.94–95, gives the completeness theorem and item11 with exactly that input formulation; both rendered pages were inspected. The graph reduction below is independently verified, rather than inferred from a neighboring gadget.

## Independent reconstruction of all arborescences

Given a cleaned formula with n variables and m clauses, the four vertex layers have sizes 1,2n,n,m. Both literal-selector vertices t_i and f_i have only the root as a possible parent. Hence every feasible spanning arborescence contains both root arcs. The next vertex v_i has precisely t_i and f_i as possible parents, so its one incoming tree edge fixes a single Boolean value for variable i. This choice is shared by every later clause path using v_i.

Each clause vertex z_j can have as parent only a v_i whose variable occurs in that clause. Cleaning repeated literals and tautological clauses makes its sign unambiguous. Since every arc advances one layer, there are no cycles, alternate routes across layers, or extra paths by which a clause could avoid the variable choice. Conversely, every assignment of one parent to each variable and clause vertex, together with the forced first-layer arcs, is a rooted spanning arborescence. This covers **every feasible tree**, not only a preferred subclass of witnesses.

For destination z_j, the only potentially nonzero cost on its three-edge root path is its first edge. A positive occurrence of x_i charges r→f_i, and a negative occurrence charges r→t_i. Thus the selected path costs one exactly when its selected literal is false under the globally fixed assignment; it costs zero otherwise. Costs assigned to first edges for other variables cannot matter because those edges are absent from this particular root path. All non-clause destinations have zero cost vectors, including the selector and variable vertices that must nevertheless be spanned.

Therefore any tree costs the number of false **selected** clause witnesses. Fixing the variable parents fixes an assignment. Each clause then chooses its own parent independently: a satisfied clause can select a true literal, whereas an unsatisfied clause must pay one. Consequently

\[
\min_T C(T)=\min_\sigma\#\{\text{clauses unsatisfied by }\sigma\}.
\]

This proves both directions of the threshold-zero reduction. A zero-cost tree supplies one consistent satisfying assignment, and a satisfying assignment supplies a zero-cost tree. There is no opportunity to use different truth values for the same variable in different clauses.

## Preprocessing, boundary cases and encoding

Deleting a tautological clause preserves satisfiability and the number of unsatisfied clauses for every assignment, since such a clause is always true. Removing repeated occurrences of a literal inside a clause also preserves both. Repeated whole clauses may be retained and are correctly counted separately. Variables that occur nowhere cause no issue: their selector and variable vertices are still spanned and carry zero unshifted objective.

An input containing an empty clause is immediately unsatisfiable; an empty conjunction is immediately satisfiable. The candidate explicitly allows fixed instances for these trivial cases. Concrete instances satisfying all its graph promises are obtained from the one-variable formulas (x) and (x)∧(¬x): the resulting optima are zero and one, respectively. Thus there is no missing promise reduction at these boundaries.

The graph has 1+3n+m vertices and at most 4n+3m arcs. A full dense destination-by-arc cost table has polynomial size, and every entry is zero or one. The constructed graph is simple, has depth three, has no arc that skips a layer, and every nonroot vertex has indegree at most three. All vertices are reachable from the root before choosing a tree; feasibility itself does not encode satisfiability.

For the rationally encoded decision problem, a certificate consists of the selected arcs. Indegree and reachability checks verify the arborescence in polynomial time. Each root path has at most |V|−1 arcs, and exact sums and comparison of the binary-encoded rational costs have polynomial bit complexity. Hence the decision version belongs to NP. The special zero-threshold problem is NP-hard with all numerical entries bounded by one, so it is NP-complete and the optimization is **strongly NP-hard**. The source's allowance of arbitrary real vectors does not create an encoding problem for a hardness proof using this integer subclass.

## Strictly positive version

Adding one to every entry of every destination vector adds one per traversed arc, including paths of the non-clause destinations. The layered graph fixes the sum of all root-path lengths at

\[
(2n)\cdot1+n\cdot2+m\cdot3=4n+3m.
\]

Therefore every tree receives the same offset; the new costs belong to {1,2}. Satisfiability is equivalent to an optimum at most 4n+3m. Both the costs and the threshold are polynomially bounded, so the claimed strong hardness persists. The proof does not rely on negative values, large numerical weights, long paths, cycles, or infeasible graphs.

## Independent exact checks

The submitted verifier reproduced its JSON output byte for byte: **57,135 exact assertions**, **449 formulas**, and **12,696 arborescences** passed.

My separate standard-library checker imports no submitted code and uses an independently numbered graph with an explicit dense cost table. It does **not** generate trees by assignment or parent choices. Instead it enumerates all size-(|V|−1) edge subsets, tests indegrees and root reachability, and only then evaluates the actual paths. It examined **222,114 edge subsets** across **114 formulas**, finding and checking all **1,674 feasible arborescences** in those cases. **14,397 exact assertions** passed. These include the optimum for each global assignment, contradictory unit and binary clauses, repeated clauses, all eight signs of a three-literal clause, the positive-cost offset and the harmless preprocessing.

The subset checks provide a direct finite challenge to the possibility of noncanonical trees. The arbitrary-size characterization and NP reduction are proved in the preceding argument and in the frozen candidate; bounded tests alone are not treated as a hardness proof.

From this review directory:

```sh
python independent_checks.py > independent_results.replayed.json
cmp independent_results.replayed.json independent_results.json
```

For the submitted replay:

```sh
cd author_replay
python verify.py > verification.replayed.json
cmp verification.replayed.json verification.json
```

The eight publication files are listed in `review_summary.json`. Source hashes and inspected scopes are recorded in `source_verification.json`. Exclude downloaded PDFs, rendered pages and caches.

## Final scope

This is a complete proof of the NP-hardness requested by the literal directed path-cost Problem2, with the stated binary and positive-cost restrictions. It does not need the motivating identification with Wong's extended formulation, which is not independently re-proved here. It does not settle the adjacent undirected all-roots Problem1 by implication, nor create a second result for duplicate30003998. No approximation threshold, historical novelty or human peer-review claim is justified by this audit. Within the exact stated scope, no gap remains.
