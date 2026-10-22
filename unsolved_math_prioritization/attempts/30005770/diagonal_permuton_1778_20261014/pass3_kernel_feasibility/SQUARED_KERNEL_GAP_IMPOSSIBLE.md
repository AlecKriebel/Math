# The strict squared-kernel growth gap is impossible for the exact staircase kernel

Shared PASS3, row1778 /30005770, 14 October2026. This is an obstruction to a sufficient method, not a disproof of the1324 anti-diagonal permuton conjecture. All accepted PASS2 files remain unchanged.

## 1. Exact statement

Use the accepted greedy kernel K on nonempty213-avoiding states and the involution S=reverse-complement-inverse from PASS2. Put

    a_n=|Av_n(1324)|,
    S_n=sum_{|A|+|C|=n}K(A,C)^2,
    T_n=sum_{|A|+|C|=n}K(A,C)K(C,A),
    lambda=lim a_n^(1/n),  beta=limsup S_n^(1/n).

The sums defining S_n and T_n run over nonempty213-avoiding states.

**Theorem.** For every n>=0,

    a_n <= S_(n+3),                                           (1)
    a_n <= T_(n+4) <= S_(n+4).                                (2)

Consequently beta>=lambda. In particular, the strict beta<lambda hypothesis of the accepted PASS2 conditional theorem cannot hold for this exact kernel.

The reciprocal-product inequality in (2) has a stronger use than the slightly smaller shift in (1): the factors from any positive diagonal similarity cancel in K(A,C)K(C,A). Analytic consequences of that observation are treated separately; no weak-limit failure follows from (1) or (2).

## 2. An unrestricted domino kernel, including empty states

Let C_0 be the213-avoiding permutations including the empty permutation. Define D(A,C), for A,C in C_0, to count all position interleavings of an upper copy of A and a lower copy of S(C) whose union avoids1324. There is no greedy-witness condition. In particular D(A,empty)=D(empty,A)=1.

For nonempty states, K(A,C)<=D(A,C), but equality is not assumed. The second collapse below naturally has the reversed orientation D(C,A), not a second copy of D(A,C). Both distinctions are essential.

We use this elementary domino observation throughout: if an upper cell avoids213 and a lower cell avoids132, a1324 occurrence must consist of two increasing points in each cell, interleaved in position order as

    lower, upper, lower, upper.                              (3)

Indeed, with three upper points and one lower point, the upper points would form213. With three lower points and one upper point, the lower points would form132. An occurrence wholly in one cell is excluded as well. With two points in each cell, the lower points must be the1,2 and the upper points the3,4, proving (3).

## 3. The two-collapse injection

Take the canonical descending staircase of pi in Av_n(1324). Color its odd cells blue and its even cells red. Each color's cells are ordered by skew sum. Thus all blue points have a213-avoiding induced pattern A; all red points have a132-avoiding induced pattern B. Write C=S(B), so A,C belong to C_0.

First collapse: keep the original position order, the relative value order within each color, and place all blue values above all red values. This gives a domino counted by D(A,C).

To prove its avoidance, suppose it had a1324. By (3), the occurrence has an increasing pair of each color. Same-color cells are nonadjacent in the staircase and in skew order, so each increasing pair lies inside one original cell. If those two cells are nonadjacent, their positions are separated and cannot alternate as in (3). If they are horizontal neighbors, their positions are again separated. The only remaining possibility is a vertical neighbor pair, with the blue cell above the red cell. Within that pair the collapse changes no pattern relation, so the alleged1324 was already in pi. Contradiction.

Second collapse: first reflect the original colored plot by S, which preserves1324-avoidance. Original red points now have pattern S(B)=C and are designated upper; original blue points have pattern S(A) and are designated lower. Collapse these two colors vertically, retaining their position order after the reflection. The resulting domino is counted by D(C,A).

The preceding avoidance argument applies to this reflected staircase as well. S preserves northwest/southeast order, takes original horizontal neighbor pairs to vertical neighbor pairs, swaps the213/132 cell types, and swaps the two colors. The reflected staircase may begin with a lower cell; this is harmless because the argument only used skew order of same-color cells, adjacent row/column geometry and the designated upper/lower types of vertical neighbors. A supposed new1324 again reduces to one original neighbor pair. Equivalently, this second collapse detects the horizontal-neighbor restrictions of the original staircase.

Injectivity is exact. The first domino records the original position color word. The second records, in its position order, the original value color word read from largest value to smallest, with the colors swapped. Together A and B=S(C) give the matching of each color's position ranks to its value ranks. These two words and two induced patterns uniquely reconstruct pi. Nothing requires either collapsed domino to have a greedy divider.

Empty states cause no problem. A one-cell permutation has C empty and is still encoded. The empty permutation uses both states empty. Therefore, writing

    R_n=sum_{A,C in C_0, |A|+|C|=n} D(A,C)D(C,A),
    U_n=sum_{A,C in C_0, |A|+|C|=n} D(A,C)^2,

we obtain for every n>=0

    a_n <= R_n <= U_n.                                       (4)

The second inequality is Cauchy-Schwarz, since swapping A,C permutes the finite index set. It can also be seen by summing 2xy<=x^2+y^2. It does not require D to be symmetric.

The structural staircase input is credited to Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition1 and proof, pp.3-4. Their Theorem8 proof, pp.11-12, already gives the first collapse; the second collapse and the precise reciprocal indexing are proved here. Primary author manuscript:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

## 4. A three-point guard repairs any unrestricted domino

Let p be an unrestricted domino counted by D(A,C), with n=|A|+|C| and b=|C|. Its lower values are1,...,b. Form q by placing three new points first in position order, with values

    n+2, b+1, n+3,

and then every old point, retaining order and replacing its value v by v if v<=b and by v+1 if v>b. Define

    A'=12 skew-sum A,   C'=1 skew-sum C.

The upper pattern of q is A', and its lower pattern is1 skew-sum S(C)=S(C'). Both cell classes are preserved because213 and132 are skew indecomposable and their avoidance classes are skew closed. This also works when either old cell is empty.

There is no new1324. The first and third guard points are larger than every old point. The first point can only be the1 of a1324, which is impossible at its value; the third point could only be the4 of a1324, but has only two predecessors. The middle guard point can only be the first point of a new occurrence: the first guard point cannot be its preceding1, and there are too few earlier positions for other roles. Since the third guard point cannot belong to the occurrence, its remaining three points would be old upper points. They would need to form213, impossible in A. Occurrences using only old points are unchanged and were excluded.

The middle guard point is the highest lower point. The first and third guard points form an increasing upper pair bracketing it. This is precisely the greedy witness defining K. Thus

    D(A,C) <= K(12 skew-sum A, 1 skew-sum C).                  (5)

The map of state pairs is injective, as are the individual shuffle maps: delete the known first two upper-pattern entries and first lower-pattern entry to recover the states, and delete the first three global positions to recover p. Applying the same guard independently to two shuffles with fixed old states gives

    U_n <= S_(n+3).                                          (6)

Together (4) and (6) prove (1).

## 5. A symmetric four-point guard preserves reciprocal pairs

The asymmetry of the preceding state transformation is unnecessary when a reciprocal pair is needed. Put

    P(A)=12 skew-sum A.

For any unrestricted domino p counted by D(A,C), prefix the fixed four-point domino3124: its upper pattern is12, its lower pattern is12, and its color order is upper, lower, lower, upper. All guard positions precede all old positions. Within each color, put the guard values above all old values. More explicitly, with n=|A|+|C| and b=|C|, the new prefix values are

    n+3, b+1, b+2, n+4,

and old upper values increase by2 while old lower values are unchanged.

The new upper pattern is P(A), and the new lower pattern is12 skew-sum S(C)=S(P(C)). To verify avoidance, use (3). Every increasing pair of a fixed color lies wholly in the guard or wholly in the old domino, because these two parts are in skew order within that color. If both increasing pairs are in the same part, the guard3124 or the old domino would already contain1324, which neither does. If they are in different parts, their positions are separated and cannot alternate as in (3). Thus the new domino avoids1324.

Its highest lower point is the third guard point, bracketed by the two upper guard points in positions1 and4. It therefore satisfies the greedy witness, and

    D(A,C) <= K(P(A),P(C)).                                  (7)

The map P is injective, and the old shuffle is recovered by deleting the four guard positions. Crucially, applying exactly this construction to the reversed pair gives

    D(C,A) <= K(P(C),P(A)).                                  (8)

Consequently the two-collapse code injects into a reciprocal pair of genuine greedy-kernel shuffles, with total state size n+4. Summing gives

    a_n <= R_n <= T_(n+4).                                   (9)

Finally T_N<=S_N by Cauchy-Schwarz over ordered nonempty state pairs, proving (2).

## 6. Consequence and limits

The fixed shifts in (1) or (2) do not affect exponential growth. Since a_n^(1/n)->lambda and a_n<=S_(n+3), we have beta>=lambda. In fact unrestricted and greedy squared-kernel counts have the same upper exponential growth: K<=D gives beta<=limsup U_n^(1/n), while (6) gives the reverse inequality.

The PASS2 conditional theorem remains a correct implication, but its strict hypothesis is impossible for the actual unweighted kernel. This is a reason to abandon certification of beta<lambda for this encoding. It is not evidence against the conjectured anti-diagonal weak limit, and does not imply a macroscopic cell has positive probability.

The reciprocal encoding in (9) supports an additional obstruction for diagonally reweighted Hilbert-Schmidt approaches. That consequence must retain the cancellation of reciprocal weights and the proper convergence radius; it is not needed for the unweighted theorem proved here.

Finite script check_obstruction.py independently tests both collapses and reconstruction through n=8, and guards on every unrestricted domino of total size at most7. These checks are indexing regressions, not the all-size proof. No queue, ledger or remote edits are made, and no novelty or human peer-review claim is made.
