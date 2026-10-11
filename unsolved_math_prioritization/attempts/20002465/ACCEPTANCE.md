# Acceptance report: quadratic-chain Aubry characterization

This is an AI-assisted, unrefereed mathematical draft. Acceptance means one independent internal AI mathematical reconstruction accepted the stated partial result with a correction and explicit standard imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Disposition

ACCEPTED_PARTIAL_RESULT_WITH_CORRECTION for 20002465 / AIM-PDES-0077. The full original ordinary-chain question remains unresolved by this work.

Under the nonempty compact connected smooth boundaryless-manifold, smooth-metric and smooth-vector-field assumptions, the accepted claims are:

1. The projected zero-class Aubry set of L_f(x,v) = |v-f(x)|²/2 equals quadratic-chain recurrence, with every lower flight-time bound and arbitrarily small total squared jump cost.
2. The tangent Aubry set is the graph lift {(x,f(x)): x in R_2(f)}; its cotangent image is the corresponding zero section.
3. SCR(f) subset R_2(f) = A_f subset CR(f), and the first inclusion can be strict for a smooth circle flow.
4. Every critical viscosity solution is constant if and only if R_2(f) = M. With u(x_*) = 0, this is uniqueness of zero.
5. A_f = A_{-f} and R_2(f) = R_2(-f); the same constants-only criterion applies to the equation with reversed drift.

## Mandatory correction

The blanket viscosity-solution bijection u -> -u is rejected. The algebraic Hamiltonian identity alone does not preserve viscosity test inequalities. The smooth circle witness, including the bad supersolution test of value -1/2, is retained in full. The valid reversed-drift conclusion follows from path reversal of action kernels and independent application of the proven theorem to -f.

## Explicit limits

The unrestricted CR(f) subset R_2(f) implication is neither proved nor disproved. No claim is made outside the stated smooth compact boundaryless setting. Standard weak-KAM graph, common-derivative and pointed-Peierls facts are explicit imports. The known low-dimensional and Mather-disconnectedness results are credited, not independently reproved. Novelty and exhaustive literature coverage remain unestablished.

The original AIM PDF wording was compared through primary-domain parsed text. Its direct PDF-byte retrieval returned HTTP 403 and its screenshot was unavailable. Thus no direct visual inspection or byte authentication of that AIM PDF is claimed. Retained FFR and Cheng–Wei preprints have recorded hashes and selective page inspection; journal versions were not inspected.

PROOF.md contains the complete mathematical reconstruction. AUDIT.md is an editorial acceptance/dependency record of that same single independent internal AI reconstruction, not a second review. The public edition does not assert human peer review, formal proof-assistant certification, a full-target solution, or a new proof derived from finite tests.
