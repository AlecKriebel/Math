# Source-first control design (sealed before candidate inspection)

Started 2026-10-03 03:14 UTC. At this stage I have read primary sources and path names only. I have not opened candidate proofs, candidate executable code, historical review reports, sibling family reports, or root verdicts. Parent task supplied the target SHA, broad claimed mechanisms and replay totals; those are task context, not independent evidence.

The original claim quantifies over all finite mono-constrained tripartite graphs, all integers k>=1, and x,y in (0,1]. The conditions are x+k y>1 (strict) and k x+y>=1 (weak). The conclusion is one C vertex with at least 1/k of the distinct A vertices as two-step predecessors. Direction multiplicity is irrelevant: a predecessor is counted once. The diagonal question x=y>1/(k+1) is only a subcase. Reverse degree constraints belong to psi, and its theorem is not a proof for phi.

Primary access: EMS46780 raw PDF and published EJC P2.47 raw PDF were fetched successfully. OWR p46–47 contains the question and psi contrast; the report belongs to the January2019 meeting but EMS displays publication27Feb2020. Published EJC3Jun2022 p21 identifies Conjecture5.1. I read the published definitions, simple bounds, weighted graph equivalence/LP dual mechanism, symmetry and rotation, and the biconstrained maximal-disjoint-neighborhood argument before designing controls. This source reconstruction makes no current exhaustive novelty claim.

Independent mechanisms prepared in independent_controls.py:

1. Literal actual-graph exhaustive tests: all nonempty rows for A<=4,B<=3,C<=3, direct OR unions, every k<=6, and a rational k1 equality counterexample to replacing strict by weak.
2. Weighted primal/dual controls: positive unequal A weights, exact rank<=2 support families, all strictly admissible union sets, separately optimized A->B and B->C bottlenecks; exact rational feasible primal and complementary-transpose dual certificates. This tests arbitrary weights/topology without trusting floating point.
3. Disjoint/laminar partition controls: every set partition through six A vertices, equal and unequal positive weights, independently derived nonvacuous block bounds and endpoint equalities.
4. Conditional deletion on actual graphs: exact surviving A->B and B->C degree fractions, denominator preservation and epsilon mass identities on all nonempty three-by-three cuts.

These are adversarial finite controls, not universal proofs. They cannot settle arbitrary overlapping, higher-rank, unbounded-size graphs. No sixth author search is performed. All writes remain within final_adversary; there is no external communication.

Progress estimate toward this audit:30%; toward the general conjecture:unknown, package is expected to remain unsolved5/5. Timestamp and hashes will be sealed when the new full outputs finish, before candidate inspection or comparison.
