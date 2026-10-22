# Balanced Ham Sandwich Line: bounded partial result and source audit

Problem ID 136, GREEN-048. Checked 6 October 2026.

## Status

The intended straight-line problem remains unresolved in this investigation. No full proof, counterexample, or verified prior solution was found. The result below is an elementary, degeneracy-aware partial theorem, with no novelty claim. The known general bound remains O(log log n) in the sources inspected. The pseudoline counterexamples do not settle the straight-line question.

The complete inherited problem record was read, including its background. Its associated research report is empty. The inherited background contains generic literature triage, not a substantive proof attempt. Targeted repository issue/PR, default-branch code, and branch searches found no earlier attempt at this particular problem. This is a bounded search result, not a proof of absence from all history.

## Exact mathematical target and conventions

For every finite set X of n distinct points in R^2, with n >= 2, ask whether there is a straight line through at least two distinct points of X whose two open half-planes contain numbers of X-points differing by at most 100.

Write L(X) for the lines determined by distinct pairs of X, and

    D(X) = min over ell in L(X) of | |X intersect H_plus(ell)| - |X intersect H_minus(ell)| |.

Points on ell contribute to neither count. Collinearities are allowed; there are no repeated points or weights. An admissible line need not be ordinary: it may contain more than two points. The quantifier is one line for each configuration, uniformly over all n. An n-dependent bound does not answer the question.

The raw formulation omits n >= 2. For n = 0 or 1 no admissible line exists. This trivial domain defect is recorded but is not presented as a resolution of the intended problem.

## Authored partial theorem

Let m be the largest number of X-points on a line and let e = n mod 2. Then

    D(X) <= m - 2 + e.

In fact a stronger local statement holds. For every exposed convex-hull vertex p, let m_p be the largest number of X-points on a line through p. A line through p and another X-point has discrepancy at most m_p - 2 + e. The proof in PROOF.md groups all simultaneous collinear crossings exactly; it does not discard them by a general-position assumption.

Consequences:

- The target 100 holds whenever some exposed hull vertex has m_p <= 101, or m_p <= 102 when n is even. The corresponding conditions on global m suffice as well.
- In general position, D(X) = 0 for even n and D(X) = 1 for odd n.
- If a line contains at least n - 100 points, that line already proves the target.
- Every centrally symmetric finite set with at least two distinct points has D(X) = 0, including configurations with a point at the symmetry center and arbitrarily large collinear blocks.
- Any counterexample to 100 must have every exposed hull vertex on a line containing at least 102 points; for even n, at least 103. It must also have at least 101 points outside every determined line. These are necessary conditions only.

These elementary special cases do not improve the known general asymptotic theorem. Their purpose is to make the exact obstruction in the usual rotating-line argument explicit.

## Literature and an inequality correction

The catalog target matches Problem 75 in the retrieved version of Ben Green's *100 Open Problems*, page 36. Green identifies the Kupitz-Perles conjecture and discusses both the logarithmic-logarithmic upper bound and the pseudoline distinction. The dataset identifier GREEN-048 is not the numbering of that retrieved source. [S1]

Pinchasi's primary paper gives the O(log log n) discrepancy consequence of its Theorem 1.2 and defines discrepancy using open half-planes. Its Section 7 also records a related stronger constant-additive formulation involving many points on each side; these formulations should not be silently identified without a reduction. [S2]

Conlon and Lim prove unbounded minimum discrepancy for generalized configurations of pseudolines, not for straight-line point configurations. Their construction shows why a proof using only unrestricted allowable-sequence axioms cannot establish a constant bound: additional straight-line realizability information would be needed. [S3]

There is a concrete threshold discrepancy in the survey: Green's comment says that replacing 100 by 2 is false. Pinchasi instead explicitly records an Alon example with D(G) = 2; Conlon-Lim say no stronger example is known. The 2025 paper of Subercaseaux, Mackey, Qian, and Heule likewise says that existence of a straight-line k-everywhere-unbalanced set for any k >= 3 remains open. Thus the verified lower-bound claim is that 1 fails, not that 2 fails. The evidence does not justify turning the survey sentence into a D(G) >= 3 example. These comparisons use the same absolute difference of open-half-plane counts, with no factor-of-two or parity renormalization. Counting both closed half-planes instead would add the same on-line count to both and leave the difference unchanged. Green's threshold is explicitly inclusive (at most), whereas failure at 2 would require integer discrepancy at least 3 for every determined line. No such example is verified here. [S1-S4]

The 2025 paper also reports a minimal odd-sized 21-point example with minimum discrepancy 2. That computational minimality result was not independently reproduced here. It does not furnish a counterexample to 100. [S4]

Kalai's September 2026 discussion and the July 2026 lecture material still discuss the Kupitz-Perles conjecture and Pinchasi's bound, and distinguish Conlon-Lim's pseudoline result. No subsequent straight-line resolution was located by the searches recorded in APPROACH_LOG.md. A dated search is not proof that an unindexed or later resolution does not exist. [S5-S6]

## What remains

Prove D(X) <= 100 for every finite distinct planar point set with n >= 2, or produce one genuine straight-line configuration for which every determined line has discrepancy >= 101. The reproduced elementary bounds do neither. The status must remain bounded partial / unresolved, without a claim of a new solution.

Citations and inspection scope are in SOURCES.md. Verification metadata contains hashes and sizes, not source documents or dataset contents. No executable mathematical certificate or finite enumeration is used for the partial theorem.
