# Final result: 30006078 / OWR-14298795-018

**Original question: unresolved after five substantive author turns (5/5).** No counterexample local system and no complete proof of the general characteristic-class formula has been obtained. The packet is frozen for independent review; its own verifiers are not independent review. No historical novelty claim is made.

## Exact target

Petrov's contribution with Pan to OWR45/2024, printed p.2658, asks whether the arithmetic odd characteristic class of a Hodge–Tate p-adic local system, after its B_dR comparison map, equals the weight-weighted Chern character of its Hodge–Tate graded bundle. The base is a finite extension K/Q_p; X is smooth algebraic, not necessarily proper. SOURCE_GATE.md gives the full statement, conventions, primary links, prior-attempt gate and the already known top-degree theorem.

## Strongest retained results

1. **All smooth bases, i>=2:** equality with both sides zero for systems which become filtered by arithmetic quotient systems after a finite étale cover. This includes finite geometric monodromy and potentially unipotent geometric monodromy. Each positive Chern character of each Hodge–Tate grade vanishes in this class. See TURN_1.md.
2. **Proper bases:** the total unweighted Hodge–Tate Chern character is the rank, as a credited consequence of Petrov Proposition5.1. The two candidate expressions obey matching tensor, dual and Tate-twist identities. Arithmetic tensor factors can be removed. End(V) detects even-index defects but is blind to odd-index ones. See TURN_2.md.
3. **An exact failed proof mechanism:** on P_K^{i−1}, cup product with the fixed kappa_i has kernel dimension [K:Q_p]−1; on an explicit good-reduction elliptic square over Q_5, the degree-three cup map has rank4 and kernel2. Alpha is injective on these domains. These are ambient cohomology classes, not realized local-system defects. See TURN_3.md.
4. **Proper bases, i>=2:** equality with both sides zero for scalar-geometric filtrations after finite étale cover. This includes finite projective geometric monodromy, rankone systems, and commuting geometric monodromy whose finite-dimensional algebra has split semisimple quotient over Q_p. A point-normalized determinant root plus published Hodge–Tate rigidity supplies the needed admissible twist. Arbitrary nonsplit coefficient extensions are not claimed. See TURN_4.md.
5. **Projective bases over Q_p:** using the report's credited positive-dimensional top-degree formula with its compatible normalization, the defect annihilates all products of rational divisor classes of complementary degree. Hence the formula holds when that complementary de Rham cohomology is divisor-generated; in particular in every higher degree for a surface with dim H_dR^2=1. Tensor-generated pullbacks from projective curves give another higher-degree class. Numerical testing still leaves a two-dimensional annihilator on the elliptic square. See TURN_5.md.

## Exact remaining gap

There is no comparison identifying the arithmetic regulator image with the proposed weighted class for arbitrary noncommuting semisimple geometric monodromy. Neither unweighted Chern vanishing, the fixed pro-étale Chern-class cup product, nor divisor-intersection tests kills the remaining cohomological directions. No global decomposition of arbitrary systems into the treated classes has been proved. The properness, base-Q_p and rational-splitting restrictions above cannot be removed by omission.

Degree one also has not been certified against an explicit alpha(log chi_cycl) convention in the short source report. We do not use a choice of sign to manufacture a negative answer. This does not remove the independent unresolved higher-degree obstruction.

The final disposition is **unsolved5/5**, with the restricted results above. The credited source theorems and basic comparison/duality machinery are dependencies; the packet does not re-prove them. The last completion estimate was30%, an informal progress estimate, not a correctness probability. No sixth author search is planned.

## Reproducibility

Run verify_turn1.py through verify_turn5.py with Python3; turns3–5 use SymPy. Each prints the bound TURN_n_CHECKS.json. FINAL_REPLAY.json records exact replay and historical-hash checks. The assertions test finite algebraic mechanisms, not p-adic cochains or the unrestricted conjecture.

All earlier proof, control, state and manifest bytes are preserved. TURN_STATE.json is the historical first-turn state; CURRENT_STATUS.json is the final state. Raw source PDFs, renders and imported records are local-only and excluded from publication.
