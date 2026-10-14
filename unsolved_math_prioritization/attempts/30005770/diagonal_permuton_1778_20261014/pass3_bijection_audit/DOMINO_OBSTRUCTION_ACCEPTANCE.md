# Independent structural audit of the squared-kernel obstruction

Shared PASS3, 14 October 2026. This audit concerns the exact staircase kernel from the accepted PASS2 encoding. The final reviewed proof and exact hash are recorded in `DOMINO_OBSTRUCTION_RECEIPT.json`.

## Verdict and scope

**Accepted.** The two-collapse encoding, correct reversed orientation, unrestricted-to-greedy guard maps, and exact finite-size inequalities are valid. For every n >= 0, they prove

`a_n <= S_(n+3)` and `a_n <= T_(n+4) <= S_(n+4)`,

where a_n counts all 1324 avoiders, S is the ordinary squared-kernel sum, and T is the reciprocal-product sum over ordered pairs of nonempty states. Consequently beta >= lambda. The strict beta < lambda hypothesis of the PASS2 conditional theorem is impossible for this exact kernel.

The previously accepted conditional implication remains mathematically correct. This new obstruction rules out its hypothesis, not the conjectured weak limit. No macroscopic-cell event, failure of convergence, or negative result for all transfer methods is proved.

## 1. Why the unrestricted kernel is necessary

The first collapse has state orientation (A,C), while the reflected second collapse has orientation (C,A). A direct use of K(A,C)^2 would be unjustified. In addition, the reflected collapse need not have a greedy witness. The proof correctly introduces the unrestricted domino kernel D, with empty states allowed, before performing a separate guard construction.

The finite greedy example 213 already illustrates the distinction: its normalized states are A=12 and C=1, with K(A,C)=1 and K(C,A)=0. This does not obstruct the unrestricted two-collapse code.

## 2. Avoidance of both collapses

An upper Av(213) cell and a lower Av(132) cell can have a 1324 only as two increasing pairs, with color order lower–upper–lower–upper. Other allocations would force a forbidden 213 above or 132 below.

In the original staircase, all odd cells are in skew order, as are all even cells. Therefore each same-color increasing pair is contained in one original cell. Both color classes remain in their designated Catalan classes: 213 and 132 are skew indecomposable, so their avoidance classes are skew closed.

For the position collapse, two increasing pairs can interleave only if their original cells are vertical neighbors. Nonadjacent cells and horizontal neighbors have separated position intervals. On a vertical neighbor pair, moving all odd points above all even points changes none of the four selected pattern relations. A forbidden occurrence would therefore already have existed in the original avoider.

The second collapse first applies the anti-diagonal reflection S. It swaps the cell types and takes original horizontal neighbors to vertical neighbors. After designating original even points as the upper color, the same argument applies, even though the reflected staircase can begin with a lower cell. Its states are exactly (C,A), not (A,C).

## 3. Exact reconstruction and empty colors

The first domino contains the original position color word. The second domino contains the original value color word from largest to smallest, with the designated colors exchanged. The induced patterns A and B=S(C) then match position ranks to value ranks within each color. These data determine every original point and reconstruct the original permutation uniquely.

A one-cell permutation has the even color empty, and the empty permutation has both colors empty. Including these states in D handles both without an asymptotic remainder. The resulting exact code gives

`a_n <= sum_(|A|+|C|=n) D(A,C)D(C,A)`.

The index set is finite and invariant under exchanging A,C. Cauchy–Schwarz, or summing 2xy <= x^2+y^2, bounds this reciprocal sum by the ordinary square sum of D. Symmetry of D is neither true in general nor assumed.

## 4. Three-point guard

For an old domino with n points and b lower points, prefix the values `(n+2,b+1,n+3)`, shift old upper values upward by one, and leave old lower values unchanged. The resulting states are `(12 skew-sum A, 1 skew-sum C)`.

The first guard point cannot start a 1324 because too few larger values follow it. The third guard point is the global maximum and has too few predecessors to be the last point of a 1324. If the middle guard point belongs to a new occurrence, it must be the first point; after excluding the other guard points, the remaining three points would be old upper points forming 213. Thus there is no new occurrence. This explicit exclusion matters: the third guard point is also later and larger than the middle point, although it cannot belong to the occurrence. The author clarified that sentence during review.

The middle guard point is the lower maximum and is bracketed by an increasing upper pair. This supplies exactly the kernel's greedy witness. Removing the first three positions recovers the old shuffle; removing the fixed initial entries of the two state patterns recovers A and C. The state-pair map is injective, including empty input states. Applying it to both shuffles in each ordinary square gives the exact shift by three.

## 5. Symmetric four-point guard

The symmetric transformation is P(A)=12 skew-sum A. Prefix the colored domino 3124, with its first and fourth points upper and its middle two points lower. Both guard colors lie above their respective old colors in value, while all guard positions precede the old positions.

Any within-color increasing pair lies wholly in the guard or wholly in the old domino. Two pairs in different parts have separated position intervals and cannot interlock. Two pairs in the same part cannot create a 1324, since neither the fixed guard nor the old domino contains one. Thus the new domino avoids 1324.

Its lower maximum is the third guard point, bracketed by the upper ascent in positions one and four. Its states are precisely `(P(A),P(C))`, because S fixes 12 and preserves the order of skew-sum blocks. The same transformation applied to the reversed input gives `(P(C),P(A))`. State recovery and removal of the first four global positions are injective. Consequently reciprocal pairs are preserved with total size increased by four, proving the T inequality directly, without Cauchy–Schwarz at this step.

The final T_N <= S_N is again a finite Cauchy–Schwarz inequality over ordered state pairs. These are ordinary reciprocal products, not an assumption that K is symmetric or reversible.

## 6. Growth inference and analytic scope

The fixed index shifts do not change an exponential limsup. The fixed-pattern class has `a_n^(1/n) -> lambda`; hence `a_n <= S_(n+3)` proves beta >= lambda. Likewise the reciprocal coefficient sequence has upper exponential growth at least lambda. These conclusions use the exact all-size injections, not extrapolation of the displayed finite counts.

The reciprocal inequality is an appropriate input for a separate positive-diagonal-similarity obstruction because the two reciprocal similarity factors cancel. This report accepts the combinatorial inequality itself. Any further operator-domain and convergence-radius claims must retain their explicit analytic hypotheses and independent review.

## 7. Independent finite verification and credited source

The separately written `check_domino_obstruction.py` tests both collapse maps, their exact state orientations, avoidance, color-word reconstruction, and image distinctness for all 19,204 avoiders of sizes zero through eight. It tests every one of the 12,082 unrestricted dominoes of sizes zero through seven, including empty colors, under both guard maps. It checks resulting state patterns, avoidance, greedy witnesses, inverse deletion, and distinct images. All checks pass. `DOMINO_OBSTRUCTION_CHECKS.json` records the exact results. These tests are diagnostics only; the all-size arguments above establish the theorem.

The first collapse and its reconstruction by a value color word are credited prior constructions in the proof of Theorem 8 of Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, PDF pages 11–12. I independently inspected those primary pages, as well as the previously reviewed staircase convention. The retained PDF has 627368 bytes and SHA-256 `1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d`.

[Primary author manuscript, Theorem 8 proof](https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf#page=11)

No novelty or literature-exhaustive claim is part of this acceptance. All accepted PASS1 and PASS2 files and receipts are preserved.
