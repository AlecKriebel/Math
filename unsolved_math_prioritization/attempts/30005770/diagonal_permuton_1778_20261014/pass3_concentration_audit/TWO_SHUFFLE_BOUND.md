# Two-shuffle obstruction to the strict squared-kernel growth gap

Date: 14 October 2026. Shared PASS3. This reviewer-authored argument requires complementary independent review before being treated as accepted. It concerns the exact canonical1324 kernel, not an abstract generating tree.

## Statement

Use the accepted PASS2 notation: C is the set of nonempty213-avoiders; S is anti-diagonal reflection; K(A,C) counts greedy,1324-free vertical shuffles of upper A and lower S(C). Set

    a_n = |Av_n(1324)|,
    S_n = sum_(A,C nonempty, |A|+|C|=n) K(A,C)^2.

Then, for every n>=1,

    a_n <= S_(n+2).                                             (1)

Consequently beta=limsup S_n^(1/n) is at least lambda=lim a_n^(1/n). In particular the strict squared-kernel hypothesis beta<lambda in the accepted conditional PASS2 theorem cannot hold for this exact kernel.

This does not contradict that conditional implication, which remains logically correct. It makes the hypothesis unavailable. It proves neither a weak-limit counterexample nor the failure of largest-cell concentration.

## 1. Raw dominoes

For nonempty A,C in C, let D(A,C) count all1324-free vertical shuffles of upper A and lower B=S(C), without the greedy-witness condition. The states and orientations are exactly those of K. We will prove

    a_n <= Cat_n + sum_(|A|+|C|=n) D(A,C)D(C,A)                 (2)
         <= Cat_n + sum_(|A|+|C|=n) D(A,C)^2
         <= S_(n+2).

The middle inequality is the summed elementary inequality 2xy<=x^2+y^2. Exchanging A and C preserves the index set. No symmetry of D or K is assumed.

## 2. Odd/even aggregation in the actual canonical staircase

Take any1324-avoider with at least two canonical greedy staircase cells. Colour every odd cell upper and every even cell lower. Let A be the induced pattern of all upper-coloured points and B the induced pattern of all lower-coloured points. Both colours are nonempty.

Cells of the same parity are nonadjacent and lie in northwest/southeast order. Therefore A is a skew sum of213-avoiders and B a skew sum of132-avoiders. The patterns213 and132 are both skew-indecomposable, so their avoidance classes are skew-closed. Hence A avoids213 and B avoids132. Put C=S(B), so C belongs to C as required.

Every increasing pair within either colour lies in a single original cell: pairs from distinct same-parity cells are inverted. This fact controls both flattenings below.

### Horizontal-order flattening

Keep the original global position order, but move all upper-coloured values above all lower-coloured values, preserving the value order within each colour. This gives a vertical shuffle of A above B.

It avoids1324. A putative occurrence with one lower point would require a213 in A; one with three lower points would require a132 in B. A monochromatic occurrence is also impossible. Thus the only case is two points of each colour: the lower pair occupies occurrence positions1,3 and the upper pair positions2,4. Both pairs are increasing, so each belongs to one original cell. Their positions alternate, forcing these two cells into the same staircase column. They must therefore be a vertically adjacent pair, with the odd upper cell above the even lower cell. Within this pair the flattening did not change any comparison. The same four points would form1324 in the original permutation, a contradiction.

The first flattening is therefore counted by D(A,C).

### Value-order flattening

Keep the original global value order, but move all lower-coloured positions to the left of all upper-coloured positions, preserving position order within each colour. This gives a horizontal shuffle with left B and right A.

It also avoids1324. Three left points would require a132 in B; three right points would require a213 in A; monochromatic cases are impossible. In the remaining two-and-two case the left pair and right pair are each increasing and their values alternate. Each pair lies in one original cell, and the value alternation forces these cells into the same staircase row. They must be horizontally adjacent, with the even cell on the left and odd cell on the right. Again their original comparisons already give1324, a contradiction.

Applying S to this second flattening gives a vertical shuffle with upper S(B)=C and lower S(A), so it is counted by D(C,A). This reversed order is essential.

### Injectivity

The two shuffles together retain the full original relative position order and full original relative value order of the two colours, with the within-colour correspondence supplied by A and B. They reconstruct the original coloured permutation uniquely. Equivalently, undo S on the second shuffle to obtain the original values in the order "all B positions, then all A positions"; the first shuffle then restores their original mixed position order. No record of internal cell boundaries is needed for reconstruction.

Thus the map from actual permutations to these ordered pairs of raw shuffles is injective. A permutation with exactly one greedy cell is a213-avoider, and there are Cat_n of them. This proves (2). The encoding need not be surjective for the upper bound.

## 3. Two-point padding makes every raw domino greedy

Fix a raw shuffle p counted by D(A,C), with k=|A|>=1 and m=|C|>=1. Its lower entries are1,...,m and upper entries m+1,...,m+k. Prepend two new entries, a new upper minimum a and a new lower maximum b. Explicitly,

    p' = (m+2, m+1, p_1',...,p_(m+k)'),
    p_i' = p_i+2 if p_i>m, and p_i'=p_i otherwise.

Its upper pattern is A'=1 direct-sum A, which avoids213 because a newly prepended minimum cannot participate in that pattern. Its lower pattern is B'=1 skew-sum B, which avoids132 because a newly prepended maximum cannot participate in that pattern. Anti-diagonal reflection preserves this skew-sum decomposition, so C'=S(B')=1 skew-sum C.

No new1324 occurrence is created. If the first new point a participates, it must be the first entry of the occurrence, hence its smallest value. All three later points must then be old upper points and would form213 in A. If the second new point b is the first occurrence entry, the same argument applies. If b is the second occurrence entry, the only earlier point is a>b, contradicting the required increase from the first to second entry of1324. Its global position2 prevents it being a later occurrence entry. All cases are excluded.

The new lower maximum b lies between the new upper minimum a and any old upper point c, and a,b,c form213. Thus b supplies the exact forward greedy witness. The full upper pattern avoids213, but adjoining the highest lower value creates213, so the upper pattern is the maximal top-value interval required by K. Therefore

    D(A,C) <= K(1 direct-sum A, 1 skew-sum C).                 (3)

Deleting the first two points and standardizing recovers p. The padded state pair also uniquely determines the original ordered state pair by deleting its indicated first singleton in each component. Therefore the padding is injective both within each multiplicity and across distinct state pairs. Squaring (3) and summing gives a lower bound on a subset of the terms in S_(n+2).

## 4. Single-cell cases occupy disjoint padded states

For each A in Av_n(213), use the state pair (1 direct-sum A,1). The explicit vertical word

    (2,1,A_1+2,...,A_n+2)

is1324-free by the same argument and has the same greedy213 witness. Its kernel multiplicity is at least one, and distinct A give distinct state pairs.

These terms are disjoint from every padded nonempty raw pair in Section3: here the second state has size1, whereas there it has size at least2. Consequently

    Cat_n + sum_(|A|+|C|=n) D(A,C)^2 <= S_(n+2).

Together with (2) and AM–GM, this proves (1), including n=1.

## 5. Growth and scope

The actual class growth lambda exists and is finite by skew closure and the fixed-pattern exponential bound. The elementary shuffle/Catalan bound makes beta finite. Taking limsups of nth roots in (1), and noting that the fixed index shift does not change exponential growth, yields lambda<=beta.

Thus the Hilbert–Schmidt series sum_n S_n z^n has radius at most rho=1/lambda. In particular there is no open Hilbert–Schmidt radius margin beyond rho of the type required in the PASS2 sufficient criterion. This does not determine convergence or divergence exactly at rho, strict inequality beta>lambda, concentration of the actual largest cell, or the actual weak permuton limit. Other norms or other ways of controlling the exact two-sided marked-cell weights are not excluded.

## Finite diagnostics and source dependence

The all-size proof uses the already accepted canonical descending staircase geometry and exact kernel definition, not a new external structural theorem. The relevant frozen input is `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 `dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03`.

The separately written checker `check_parity_padding.py` tests all1324-avoiders through size7. Its normal run reports2785 two-shuffle images without collisions,625 single-cell images and10831 raw-shuffle padding checks. It checks reversed state orientation, both flattenings, padded avoidance and exact greediness, and the finite count inequalities. These checks are finite diagnostics only. The proof above, once independently reviewed, is what establishes the all-size comparison.
