# Author turn 5: determinant averaging and the feasibility obstruction

2026-10-03T06:50:00Z. Turn 5/5. **NO FULL RESOLUTION; AUTHOR BUDGET EXHAUSTED.** Completion estimate: 5%. No complete proof or counterexample has been obtained for the original unrestricted target, including its equality clause. No further proof-search turn is authorized by this five-turn attempt.

## 1. A final global algebraic route

Let U have the N=2n unit normals as rows. For an n-element row set I with invertible A_I=U_I, let x_I=A_I^{-1}1. These are intersections of supporting planes; they are vertices of the polar only when Ux_I<=1. I investigated determinant-weighted averaging over these intersections, hoping to avoid choosing a special vertex.

Assume initially that every n-row submatrix is invertible. Write G=U^T U and b=U^T1. Cauchy–Binet gives sum_I det(A_I)^2=det G. Cramer's rule, followed by Cauchy–Binet on each matrix obtained by replacing one column of U by 1, gives the exact identity

  [sum_I det(A_I)^2 ||x_I||^2]/det G
   = ||G^{-1}b||^2 +(N-b^T G^{-1}b) tr(G^{-1}).       (D)

For clarity, if W_j is U with column j replaced by 1, then

  sum_I det((A_I)^{(j)})^2=det(W_j^T W_j)
    =det G [((G^{-1}b)_j)^2
             +(N-b^T G^{-1}b)(G^{-1})_jj].

Summing over j proves (D). This is an identity, not an inequality inferred from numerical evidence.

When the normals are centered, b=0, so the right side is N tr(G^{-1})>=n^2, since tr G=N. This looks stronger than the desired bound n, but it averages many infeasible intersections. It cannot be applied to the actual vertex set without controlling exactly those terms.

## 2. Exact failure of the unfiltered-averaging inference

Use the rational six-normal non-antipodal example from Turn 2:

  U=[I; -Q],  Q=(2/3)11^T-I, in R^3.

All 20 three-row submatrices are invertible. Here G=2I and b=0. The exact calculation gives:

- total determinant weight: 8;
- weighted mean squared norm over all 20 plane intersections: 9;
- only 14 row subsets give feasible intersections;
- feasible determinant weight: 22/3;
- weighted mean squared norm after retaining feasible intersections: 57/11;
- largest actual vertex squared norm: 6.

Thus the mean 9 in (D) is larger than every actual vertex squared norm. This exactly refutes the attempted transfer of the all-bases mean to the feasible vertex maximum. The six infeasible intersections account for the excess. The example is not a counterexample to the original sqrt(3) bound.

Singular bases are another trap: at the cross-polytope, some determinant weights are zero while the corresponding Cramer numerators need not vanish. Dropping those bases and substituting the Cauchy–Binet identity as though nothing changed is invalid. General-position perturbation does not repair the feasibility obstruction.

## 3. The exact remaining algebraic inequality

Let F(U) be the n-row subsets with det(A_I) nonzero and U A_I^{-1}1<=1. One sufficient inequality would be

  sum_{I in F(U)} ||adj(A_I)1||^2
       >= n sum_{I in F(U)} det(A_I)^2.             (V)

Because the weights are nonnegative, (V) would force some feasible vertex to have squared norm at least n. It is a concrete, checkable polynomial inequality inside each feasibility chamber, with the unit-row constraints included. However, (D) is over all row subsets and does not prove (V). I have no proof or counterexample for the asserted universal (V), and establishing the original equality classification would still require additional work. I therefore record (V) as an unproved sufficient assertion, not as a resolution or a claimed equivalence.

## Final status

The five substantive turns have produced scope-safe reductions, checked restricted lemmas, exact failures of proposed shortcuts, and bounded diagnostics. They have not established either a new general proof or a counterexample. The unrestricted nonsymmetric n>=5 case and global cube-only equality remain unresolved in this work.

This attempt ends at five turns. All mathematical partial statements are WIP and have not received independent adversarial review; no novelty, priority, solved status, or publication-ready result is claimed.
