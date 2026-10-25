# Literal original-claim proof and boundary ledger

| Obligation | Independent artifact / mechanism | Result and exact limit |
|---|---|---|
| One common undirected tree; every rooted orientation charged in full | Exact problem reconstruction in EARLY_DERIVATION.md; root-BFS and cut-side objective evaluators | Supported; separate root trees and terminal-path-only charges are different objectives |
| Ordinary finite encoding | Full 2N|E| binary table, finite simple connected graph, binary integer K | NP-membership bound explicitly includes bit lengths; arbitrary real-number encoding is not claimed to be in NP |
| Source problem is NP-complete | Karp actual scan Main Theorem p.94 and item 11 p.95, visually inspected after early seal | Exact at-most-three-literal restriction matched |
| Formula normalization | Delete duplicates/tautologies; empty/no-clause fixed instances; dense occurring labels | Truth-preserving, polynomial; sparse labels do not create exponentially many vertices |
| Graph and every table entry are constructible without tree data | Two hubs, variable and clause vertices; exact tables rebuilt independently | Connected/simple; N=n+m+2, |E|<=1+2n+3m; output O((n+m)^2) constant-sized entries |
| Arbitrary-tree structural identity | q>=m and p+q+h=n+m+1; symmetric t-root cost p+2q | F_t=K+(1-h)+(q-m) for all trees; nonnegative remaining costs give a unit exclusion gap |
| Clause leaves and unique hub attachments | q=m makes every positive clause degree one; leaf deletion leaves a tree; double hub attachment creates a triangle | Exact for every tree at threshold; no hidden maximum-penalty estimate required |
| Literal-root identity | At q_j only its selected variable points variable-to-hub; all other variable hub edges point the zero-cost reverse way | F=K+false-selected-literal count for structured trees only |
| Satisfiable => threshold tree | tf plus truth attachments and one true clause selection is connected with N-1 edges | Constructive all-size witness, cost exactly K |
| Threshold tree => satisfying assignment | Structural forcing first, then zero false-selected-literal count | Constructive all-size extraction; unsatisfiable inputs have every tree above K |
| NP verification | Tree test plus N traversals and sums of N(N-1) input entries | Polynomial operations and O(L+log(N(N-1))) aggregate bit length; N=1 handled separately |
| Strong NP-completeness | Costs in {0,1,2}, K=n+2m<=2N, explicit polynomial table | Hardness survives unary numerical encoding; no finite enumeration used as a hardness proof |
| Positive alphabet | Add one everywhere, increase K by N(N-1) | Exact every-tree shift to {1,2,3}; threshold stays polynomially bounded |
| Inward convention | Reverse both orientation and root cost table | Exact; independent wrong-convention witness demonstrates that reversing orientation alone changes the answer |
| B>=2 family | F_t=(n+Bm)+(1-h)+(B-1)(q-m) | Same forcing mechanism; at B=1 this particular bound loses its q-gap and no conclusion about that problem is claimed |
| Symmetric-cost boundary | Every direction gets the same root-specific edge charge | Ordinary edge-additive MST objective; no symmetric-table hardness claim |
| Integer interpretation of Martin lift | Summed indegrees give STP inequalities; integral edges yield tree; root orientation then unique | Independently derived in SUPPLEMENTARY_BOUNDARY_DERIVATIONS.md |
| Integral projection is not the full joint hull | Exact rational eight-vertex common-x/root-specific-mixture witness | Feasible joint-lift cost 10 versus integer minimum 11, consistent with the manuscript warning |
| Own computational controls | 54 formulas, 5752 tree/formula cases, exact matrix-tree census, two independent objective evaluations | PASS; corroboration and implementation falsification only |
| Supplied checker behavior | Full code read; isolated selected functions and negative guards under normal and -O Python | Selected checks PASS, same results; full suite/historical replay not claimed |
| Attribution to Kaibel Problem 1 | Actual EMS pp.3014-3015, whole-tree objective and Martin motivation | Matches; neighboring Problem 2 is explicitly a different path-cost problem and remains outside scope |
| Historical/continued novelty | Bounded search and accessible exact cited interfaces | Not certified; the author's dated negative-search audit was not independently reproduced |

No central defect or unsupported equivalent-hardness transfer was found. The supported result is the literal original theorem and positive-cost corollary with the given computational model. No narrower promotional replacement, source repair, new priority claim, degree/approximation/parameterized result, or answer to Kaibel Problem 2 is proposed.
