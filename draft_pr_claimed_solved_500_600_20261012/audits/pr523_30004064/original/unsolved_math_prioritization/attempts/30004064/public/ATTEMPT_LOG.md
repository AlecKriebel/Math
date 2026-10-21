# Attempt log

Date: 2026-10-04. Problem: 30004064 / OWR-16766-003.

## Source and prior-work gate

Recovered and read the original report contribution, its exact Theorem 1 and Conjecture 1, the cited paper's Section II and relevant Appendix A proofs, the latest arXiv revision, the experimental discussion, and the author's CVX demonstration. The exact catalogue record was recovered from the public dataset after the website returned HTTP 403. Its generated status assessment was not treated as mathematical evidence. Separate repository and all-state PR searches found no prior attempt for this target; the queue was independently read and showed 0/5.

## Attempt 1: direct dual optimality and a line-sum counterexample

Start with noiseless data \(y=As\). Expanding the objective at zero yields the exact identity
\[
F_y(\mu)-F_y(0)=\tfrac12\|\mu\|^2+
\sum_j\bigl(|(A^T\mu)_j|-s_j(A^T\mu)_j\bigr).
\]
Every summand is nonnegative for \(|s_j|\leq1\). This proves that zero is the unique minimizer, including full-row-rank tomography. The result already defeats unique-image recovery. The source's scalar example shows that this endpoint obstruction itself was previously recognized.

To test the multiple-solution clause in the actual tomography class, construct a 3-by-3 image with all 1s outside a bottom-right checkerboard. Row/column sums force exactly two binary solutions with five common 1s. Remove one redundant column measurement to obtain a 5-by-9 full-row-rank system; prove the rank and solution classification by hand. Its dual sign vector is zero and loses all five common coordinates. Extend the example to arbitrary square size, so undersampling does not remove the obstruction.

Check the general projected objective to ensure that retaining redundant line sums changes nothing: every minimizer has zero back-projection. Finally, derive noiseless strong duality directly from the Lagrangian and explain why equality of values does not identify the primal minimizer at a zero multiplier.

## Result and stopping condition

Complete negative resolution of the explicitly stated exact-minimizer formulation in attempt **1/5**. Additional proof attempts were not spent after a full resolution. No historical-priority claim is made. A conjecture about a specified finite-iterate selection, smoothing procedure, or auxiliary primal variable would be a different target; it has not been proved or disproved by this note.

Exact checks separately verify the matrices, ranks, binary solution sets, common-coordinate vectors, rational objective identity, and projected-matrix identity. No numerical optimizer is used, and there is no mathematical gap in the exact-minimizer argument being claimed. Independent review remains a publication gate.
