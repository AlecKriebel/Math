# Exact small-width growth and a fixed-width domino lower bound

Shared PASS4, row1778 /30005770. Write b_(n,K) for the number of1324-avoiders with at most K canonical greedy cells and g_K=limsup_n b_(n,K)^(1/n). All earlier accepted bytes remain unchanged.

## 1. Fixed-width unrestricted paths have the same growth

Let C_0 include the empty213-avoiding state. As in the accepted PASS3 obstruction proof, D(A,C) counts unrestricted1324-free vertical interleavings of upper A and lower S(C), with no greedy witness. Define

    h_(n,K) = sum_(A_1,...,A_K in C_0; sum|A_i|=n)
                    product_(i=1)^(K-1) D(A_i,A_(i+1)).       (1)

Thus h counts labeled state paths and their independent edge words, not ungridded permutations. Empty states and repeated records are allowed exactly as specified by(1). The normalized orientation is the same homogeneous orientation used for K.

For every fixed K>=1 and n>=0,

    b_(n,K) <= h_(n,K) <= b_(n+2K,K).                        (2)

For n=0, take b_(0,K)=1. For the first inequality, encode the unique canonical path, use K(A,C)<=D(A,C), and append empty terminal states to reach K states. This is injective, because the nonempty initial segment recovers the canonical path.

For the second inequality, apply P(A)=12 skew-sum A to every state, including empty states. Apply the accepted symmetric four-point guard separately to every edge word. This maps a D(A,C) edge injectively into a K(P(A),P(C)) edge: prefix the color word upper,lower,lower,upper, with a12 guard above the old points within each color. The exact normalized kernel theorem then reconstructs one permutation whose canonical states are exactly P(A_1),...,P(A_K). Its size is n+2K. All adjacent edge constructions have consistent state patterns, because each use at a common state uses the same P(A). The row and column edge words are independent coordinates of the accepted encoding, so there is no further compatibility condition.

The map is injective. Read the output's canonical states and edge words. Delete the first two entries of every state pattern and the four initial guard positions in every normalized edge word. This recovers the full original labeled path, even when some original states were empty. For K=1 there are no edges and the same state deletion suffices.

The constant size shifts in(2) give

    limsup_n h_(n,K)^(1/n) = g_K.                            (3)

In particular, fixed-width constructions need not initially use greedy griddings: if they supply distinct normalized state paths and edge words, the guard converts them into canonical paths at a constant total size cost. This statement requires fixed K for the growth comparison. It gives no uniform growing-K probability conclusion.

## 2. Exact values for one and two cells

A permutation has one canonical cell exactly when it avoids213. Hence

    g_1=4.                                                  (4)

For K=2, h_(n,2) is exactly the number d_n of unrestricted vertical dominoes, including empty cells. Bevan, Brignall, Elvey Price and Pantone, Theorem2, prove

    d_n = 2(3n+3)! / [(n+2)!(2n+3)!],
    lim_n d_n^(1/n)=27/4.                                   (5)

Equations(2)-(3) therefore show

    g_2=27/4.                                               (6)

There is also the sharper direct sandwich b_(n,2)<=d_n<=b_(n+3,2): use the accepted three-point guard with states(12 skew-sum A,1 skew-sum C). The constant3 rather than4 is not needed for(6).

These are exact growth statements, not extrapolations from initial coefficients. Together with the primary upper bound lambda<=27/2, they imply

    log(lambda/g_1)<=log(27/8),
    log(lambda/g_2)<=log2.                                  (7)

The independent mass-profile lane can use(7) to test genuine optimal gaps at widths1 and2, separately from the weaker certified minimax gaps at larger widths.

## 3. A quantitative lower bound at widths3k

The construction in the proof of the same paper's Theorem9 can be made at fixed width. Fix k>=1 and let the independent size scale m tend to infinity. Use the first3k staircase cells, partitioned into k dominoes and k single connecting cells, with:

-14m points in each of the two cells of each domino;
-8m points in each connector;
-7m skew-indecomposable components in each connector;
-all neighboring domino points positioned between connector components.

The primary proof verifies1324-avoidance and independent choices of all edge interleavings. Its counting argument works without identifying k with m. It supplies distinct normalized3k-state paths of total size36mk, counted by

    B_(14m)^k C_(8m,7m)^k binom(21m,14m)^(2k-1),            (8)

where B_t counts balanced dominoes with t points in each cell, and C_(v,c) counts v-point213-avoiders with c skew components. The source proves in Proposition7 and uses in Theorem9 that

    B_t=(27/4)^(2t) theta(t),  theta(t)^(1/t)->1,
    C_(v,c)=(c/v) binom(2v-c-1,v-1).                         (9)

The fixed-width guard in Section1 converts every record in(8) injectively into a canonical3k-cell permutation of size36mk+6k. No division by a gridding multiplicity is required: the output's unique canonical path recovers the complete input gridding record.

Taking m-th root rates in(8), then dividing by36k, yields

    g_(3k) >= (81/8) (27/4)^(-7/(36k)).                     (10)

For clarity, log binom(21m,14m)/m tends to7log(27/4); log C_(8m,7m)/m tends to9log9-8log8. The numerator of the limiting logarithm is

    28k log(27/4) + k(9log9-8log8)
                       +(2k-1)7log(27/4)
      =36k log(81/8)-7log(27/4),

which proves(10). The fixed added6k points do not change that limit.

Since g_K is nondecreasing in K, (10) also yields, for K>=3 and k=floor(K/3),

    log(lambda/g_K)
       <= log(4/3) + [7/(36k)]log(27/4),                    (11)

using lambda<=27/2. Formula(11) is an upper bound on the true gap, complementary to the certified positive lower bound from QUANTITATIVE_WINDOW_GAPS.md. It does not tend to zero: the currently used primary global growth bounds leave the constant log(4/3). Thus it does not by itself defeat every large adaptive window or establish adaptive sufficiency.

## 4. Source and scope

Primary source: David Bevan, Robert Brignall, Andrew Elvey Price and Jay Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*.
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

Exact dependencies: Theorem2 and its domino enumeration, Proposition7 on balanced dominoes, Theorem8 on the upper bound27/2, and the all-size construction in the proof of Theorem9, PDF pages13-14. The retained source PDF is627368 bytes, SHA-2561264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d.

The new step here is the fixed-width use of the already accepted symmetric guard, followed by keeping k fixed while scaling m in the credited lower-bound construction. The earlier exact greedy kernel and guard proofs are inputs, not newly assumed facts. No weak-concentration theorem, positive probability for a deterministic profile, or uniform growing-width estimate follows from these calculations.
