# Attempt 4: reconstructing a correction from the move calculus

## Mechanism

The original problem suggests that branching and charge data might encode the extra structure. We tried to formalize precisely what a normalization depending only on a proposed decoration datum would have to satisfy. The distinction between an arbitrary representative and an independently specified geometric structure is essential.

Fix N and one original triple with K_N≠0. Give every fully specified decorated triangulation T a definite state-sum value H(T), so that H(T)^N=K_N. For an allowed move e:T→T', write

    H(T')/H(T) = ζ^a(e),    a(e) in Z/NZ.

This notation is only used where H is nonzero. On every closed path in the full graph of fully specified triangulations, the product of these ratios is automatically one, because it telescopes. Consequently, testing those ratios on loops cannot by itself reveal a new obstruction: defining them from the actual H values already makes them an exact coboundary.

In particular, choosing a base triangulation T_0 and setting q(T)=H(T)/H(T_0) trivially makes H(T)/q(T) constant. This is circular as a proposed solution: it requires the original state sums, an arbitrary base representative, and no geometric interpretation of the normalization.

## Exact descent criterion

Suppose we insist on a correction q(T)=ζ^(b(d(T))) depending only on a candidate datum d(T) in a set D. Form a directed multigraph on D with an edge d(T)→d(T') for every allowed move and label it by a(e). Retain parallel edges and loops; inverse moves receive opposite labels.

There exists a function b:D→Z/NZ satisfying

    a(e) = b(d(T'))−b(d(T))

for all moves exactly when the sum of edge labels around every closed path in this D-graph is zero. The proof works for composite as well as prime N. Necessity follows by telescoping. For sufficiency, choose a base vertex in each connected component, set its b to zero, and let b(d) be the label sum along any path from the base to d. The zero-cycle hypothesis makes this independent of the path. Then H(T)/ζ^(b(d(T))) is invariant under all moves being considered.

This is a usable conditional theorem, not a construction of the missing b. For an invariant of triples endowed with a particular geometric structure, the allowed moves must connect all presentations of that same structure, and the labels d(T) and their transitions must be independently defined. Neither connectivity nor the required phase law may be assumed from the existence of the unrefined K_N.

## Why discarding data creates a real test

Consider three formal states T_0→T_1→T_2 with values 1,ζ,ζ. Their Nth powers all equal one. The full state graph is a path, so every full-graph cycle condition holds. Now identify d(T_0)=d(T_2)=A and d(T_1)=B. The projected edges have labels 1 from A to B and 0 from B to A. They require both b(B)−b(A)=1 and b(A)−b(B)=0, a contradiction for N>1. Thus equality of Nth powers and full-state consistency do not imply that a correction depends only on a coarser datum.

This is a formal countermodel to an invalid inference, not a realization by quantum-hyperbolic triangulations. It shows exactly what would need checking for a proposed combing, framing, spin structure, or charge class. Merely naming one of those structures does not prove the descent condition.

The exact verifier implements the path-sum construction on finite directed graphs, accepts a consistent triangle, rejects a conflicting parallel edge and a nonzero loop, and rejects the projected-path example for N=3,5,7,9. These finite tests check the algebraic criterion; they are not an enumeration of the QHI move groupoid.

## Outcome

The remaining task is to derive actual phase labels for a generating move calculus, determine their dependence on the candidate geometric datum, and prove the projected cycle relations and presentation connectivity. We did not obtain those phase labels. Replacing the datum by the full triangulation or by a chosen root would make the criterion tautological and would not explain the phase.

**Result:** a precise normalization/descent criterion and a checked failure mode for an overly coarse datum. The original question remains unresolved.
