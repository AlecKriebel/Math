# Independent adversarial audit: circular coloring partials

Audit date: 2026-10-20 UTC.

## Verdict and exact scope

**Accepted as partial results and a finite benchmark verification. The original universal conjecture is not proved or disproved. No novelty is asserted.**

The source gate fixes the target as finite simple triangle-free planar graphs of maximum degree at most three admitting a (20,7)-coloring. Squares, nonregular graphs, and degree-two vertices are included. This audit checks the supplied mathematics and executable artifacts, not the completeness of the literature search or present open status. It does not claim a fresh inspection of the original thesis or other external source documents.

## Mathematical audit

1. **Paths and tripods: accepted.** Exact sums of D={7,...,13} give S2 of size 13, S3 all nonzero residues, and Sm the whole residue group for m>=4. The forbidden-set union argument proves the stated universal tripod extensions, including coincident terminal colors or vertices. The failed boundary assignments are obstructions to arbitrary extension only.

2. **Sparse proposition: accepted.** A vertex-minimal counterexample in the hereditary class is connected, has minimum degree two, and has no cut vertex, since component colorings can be rotated to agree at that vertex. Pure cycles are colorable. A returning cubic thread would give a cut vertex; thus the thread endpoints used in the counting are distinct. Long threads and the two universal tripod configurations can be deleted and restored. The surviving length patterns imply 2n2<=3n3 and average degree at least 12/5, contradicting mad<12/5. The strict inequality is essential to this proof. The girth-at-least-12 planar corollary follows by applying Euler's inequality to the minimal counterexample, not by assuming the original arbitrary graph is 2-connected.

3. **Fully subdivided cores: accepted.** Greedily color the loop-deleted, parallel-edge-merged subcubic core with labels 0,1,2,3. Every distinct pair has difference in both S2 and S3. Nonloop threads of length at least two extend independently. Returning threads have length at least four by simplicity and triangle-freeness and accept equal endpoints. Isolated vertices and cycle components are handled separately. This includes the once-subdivided cubic boundary examples with average degree exactly 12/5; it does not require or imply the full conjecture.

4. **Failed local reductions: accepted in their stated negative scope.** The double-star, square, and pentagonal-face examples refute the claimed unrestricted boundary extensions, not colorability of their host graphs. No completeness claim for a planar discharging list is warranted.

5. **Phase method: accepted.** For each fixed even factor and biparity, unconstrained modular phases are just a bijective rewriting of colorings. At width at most nine, short edges require ordinary differences of absolute value at most three, and long edges require absolute difference at least seven. Orienting every long edge produces an exhaustive finite family of difference-constraint systems. The 30 even factors and all 1,920 oriented width-eight systems were checked again by a separately written Floyd–Warshall implementation. Every system has a negative cycle. The displayed width-nine phase vector is a valid coloring. This restriction therefore fails on the dodecahedron at width eight, not on the original unrestricted coloring problem.

6. **Exact finite dodecahedron value: accepted.** In computation/exact_dodecahedron_value.md, the maximum minimum edge distance is attained on a compact torus. If the tight directed graph were acyclic, a topological-height perturbation would increase every tight gap while preserving strict slack on all other gaps, contradicting optimality. A simple directed tight cycle of length k<=n yields M=q/k. The M=1/2 case is correctly treated by the directed two-cycle. Flooring scaled coordinates preserves every edge gap when its allowed endpoints are integers, proving the discrete coloring equivalence and numerator bound without an unproved attainment assumption. Exact fraction enumeration confirms that the largest k/q<20/7 with k<=20 is 17/6. The independently checked lack of a (17,6)-coloring, together with the explicit (20,7)-coloring, therefore establishes the known exact value 20/7 for this graph.

## Strengthening: minimum real phase width is also nine

The existing certificates support more than an integer minimum. Suppose a real phase lift of width W<9 existed for one of the considered even-factor/biparity choices. Translate all coordinates by their minimum, so 0<=phi(v)<=W. For each short edge, both inequalities have the form phi(v)<=phi(u)+3. Orient each long edge so that its constraint is phi(u)<=phi(v)-7. Whenever x<=y+m for integer m, floor(x)<=floor(y)+m. Therefore replacing each phase by its floor preserves all these inequalities. The new phases lie in {0,...,8}, yielding a width-eight lift, which the exhaustive certificate excludes. The displayed width-nine lift attains the remaining lower bound. Thus the minimum width is exactly nine even among real lifts, over all the enumerated factor/biparity choices. This does not assert that every (20,7)-coloring admits a narrow lift.

## Executed verification

The following all succeeded in this audit:

- check_extensions.py and check_square.py, using exact modular sets and boundary assignments.
- check_phase.py: 30 even-factor/biparity choices, all width-eight infeasible; explicit width-nine vector accepted.
- verify_certificate.py on all seven *_20_7.json files: 128 edges accepted in total.
- test_verifier.py: seven valid certificates accepted and 35 corruptions rejected.
- verify_unsat_certificate.py: 172 nodes, 108 contradiction leaves, target K_(17/6).
- test_unsat_verifier.py: all six deliberately corrupted certificates rejected.
- check_numerator_gap.py: exact maximum strictly below 20/7 is 17/6.
- sha256sum -c SHA256SUMS: all eight certificate files match.
- audit_check.py: independently compares the SAT and UNSAT edge sets, verifies their isomorphism to the explicit generalized Petersen graph G(10,2) used in the phase analysis and to the library dodecahedron, checks planarity/cubic degree/triangle-freeness, independently enumerates 30 even factors, and checks all 1,920 orientations via Floyd–Warshall negative cycles.

Run the additional audit with `python audit_check.py` from the package root. It requires NetworkX (tested with version 3.7), importable in the active Python environment. The principal certificate verifiers use only the standard library. Run assertion-based checks without Python's -O option.

## Trust boundary and presentation requirements

The UNSAT checker was read: it recomputes propagation from the graph and branch path, requires exhaustive distinct branch colors, and does not trust diagnostic domain snapshots to prove contradiction. Rotation and reflection restrictions preserve a representative of each coloring. The SAT and UNSAT artifacts specify exactly the same graph, so no graph-label mismatch enters the exact-value proof.

These are executable computational certificates, not proof-assistant formalizations. Python execution, checker code, and the graph identification remain part of the stated trust boundary. The separate graph isomorphism and alternate shortest-path implementation reduce, but do not erase, that boundary. The phase minimum is a statement about a restricted representation; the sparse and subdivided-core results are special classes. None supports changing the universal target to solved or claiming new literature priority. No external publication was performed by this audit.

Final synchronization check: the updated PHASE_ATTEMPT.md now includes the correct real-width-nine flooring proof, and the computation README links the exact-value argument with its limited scope. The added check_exact_benchmark.py also passed. The existing computation/SHA256SUMS covers only the eight unchanged JSON certificates, so these prose changes do not require altering that manifest.
