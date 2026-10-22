# Exact greedy-staircase transfer and the two-sided completion bias

Scope: shared PASS2, row 1778 /30005770, 14 October 2026. This is an exact combinatorial reduction and an obstruction to a proposed simplification, not a proof of largest-cell concentration or of the target permuton limit. No novelty claim is made.

## 1. Statement and source dependence

Let C be the set of all nonempty 213-avoiding permutations. Write |A| for the size of A. Let S be reverse-complement-inverse, the geometric reflection (x,y) -> (1-y,1-x). Thus S is an involution, takes Av(213) bijectively onto Av(132), and fixes 1324.

For A,C in C define K(A,C) as follows. Place A in an upper cell and S(C) in a lower cell, choose their horizontal interleaving, and retain the interleaving exactly when:

1. The resulting two-cell permutation avoids 1324.
2. The highest point b of the lower cell is between the endpoints of an increasing pair in the upper cell, in horizontal order.

K(A,C) is the number of retained interleavings. All cells are nonempty. The second condition says that adding b to the upper cell creates a 213, with b as its 1. Since A avoids 213, it is equivalent to the upper cell being exactly the maximal top-value interval avoiding 213 of this two-cell permutation.

**Exact encoding theorem.** For every finite nonempty sequence A_1,...,A_r in C, the number of 1324-avoiders whose canonical greedy staircase has these normalized cell patterns is

    product_{i=1}^{r-1} K(A_i,A_{i+1}).                         (1)

Odd cells have pattern A_i and even cells have pattern S(A_i). An empty product is one. Consequently the ordinary generating function F(z) for all 1324-avoiders, including the empty permutation, is the coefficientwise identity

    F(z) = 1 + sum_{r>=1} sum_{A_1,...,A_r in C}
                 z^(sum_i |A_i|) product_{i<r} K(A_i,A_{i+1}). (2)

No independent-cell probability law is asserted. The product counts choices of edge interleavings for fixed states; the uniform law on size n weights state sequences by that product.

The only external structural input is the descending staircase and canonical greedy construction of Bevan, Brignall, Elvey Price and Pantone, Proposition 1 and its proof, pp.3-4:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

The previously inspected PDF has SHA256 1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d, 627368 bytes. The exact product representation below is proved here from that geometry, rather than attributed to a source statement not inspected.

## 2. Pair-local avoidance

In the descending staircase, any two points in cells whose indices differ by at least two are in northwest/southeast order. The first and last entries of an occurrence of 1324 are respectively its smallest and largest entries. They form an increasing pair, and must therefore lie in the same cell or adjacent cells.

Every intermediate entry of the occurrence is inside the open coordinate rectangle determined by these endpoints. If both endpoints are in one cell, that rectangle is in that cell. If they are in adjacent cells, every other cell is outside the rectangle. To see the latter explicitly, a cell at least two earlier than the later endpoint cell is northwest of that cell; a cell at least two later than the earlier endpoint cell is southeast of that cell. Any remaining earlier/later immediate neighbor is outside the rectangle in the other coordinate by the staircase row/column separation. Thus the whole occurrence is inside the union of the same adjacent pair.

It follows that a staircase permutation with the designated cell classes avoids 1324 if and only if each adjacent pair avoids 1324. A single cell automatically avoids 1324, since 1324 contains both 213 and 132.

## 3. Pair-local greedy witnesses, including their endpoint issue

For an upper 213-cell A and lower 132-cell B in one column, the local greedy witness is precisely condition 2 above. This witness and 1324-freeness force the leftmost point of the column to lie in A. Indeed, suppose that a point d in B were left of every A point. Let a<b<c be the horizontal order of the witness, with a,c in A and b the highest B point. The case d=b is impossible since a precedes b. Otherwise d has smaller value than b, and d,a,b,c form a 1324. This is a contradiction.

The reflected statement for a horizontal pair is: if the left 132-cell B has an increasing pair whose values bracket the leftmost point c of the right 213-cell A, then the row maximum lies in B. This follows by applying S to the preceding vertical argument. The same reflection sends the horizontal witness, a 132 using c as its 2, to a vertical 213 witness.

These endpoint consequences are needed; a witness in the preceding pair alone would not identify the first excluded point of the whole remaining staircase.

Now consider a staircase satisfying local avoidance and the forward greedy witness at every edge. At an odd cell j, every later cell is below that cell's row. The maximum of the remainder is in cell j+1: if cell j+2 exists, the horizontal edge (j+1,j+2) forces its row maximum into j+1; still later rows are lower. If j+2 does not exist, the claim is immediate. Therefore the witness in edge (j,j+1) uses the actual first excluded value of the whole remaining permutation. The current cell avoids 213 and adding that value creates 213, so the current cell is exactly the maximal top-value interval avoiding 213.

At an even cell j, the analogous statement holds for the leftmost point of the remainder. The vertical edge (j+1,j+2), when present, forces its column's leftmost point into j+1. Thus the witness in (j,j+1) uses the actual first excluded position, and the current cell is exactly the longest initial segment avoiding 132. A last cell is the entire remainder and needs no outgoing witness.

Induction proves that the given gridding is the canonical greedy gridding.

Conversely, in a canonical greedy gridding, the actual first excluded value/position is in the next cell, by the grid construction. In an odd step it creates 213 on adding one point below all points of the current cell, necessarily as the middle 1; the other two points form the required ascent. In an even step it creates 132 as the last 2, bracketed in value by an ascent of the current cell. Thus every canonical edge satisfies the local witness.

## 4. Independent reconstruction and homogeneous orientation

For fixed cell patterns and each odd edge, choose a vertical-pair horizontal interleaving. This fixes position order inside that column. For each even edge, choose a horizontal-pair vertical interleaving. This fixes value order inside that row. Columns themselves have their prescribed left-to-right order, and rows their prescribed bottom-to-top order. These interleavings and the within-cell permutations uniquely assign every point its global position and global rank. Conversely, those data are uniquely recoverable from a gridded permutation.

The choices do not conflict: the two incident edges at a cell interleave different coordinates, while preserving the specified within-cell position/value correspondence. Hence they reconstruct exactly one staircase permutation. Pair-local avoidance and the preceding greedy argument ensure that it is a 1324-avoider with the specified canonical cells. Different edge data cannot reconstruct the same ungridded permutation, because the greedy gridding is unique.

For an odd edge, the two original patterns are A_i and S(A_{i+1}), so the allowed edge count is K(A_i,A_{i+1}). For an even edge, the original pair consists of a left S(A_i) cell and a right A_{i+1} cell. Apply S to this entire pair: it becomes an upper A_i cell and lower S(A_{i+1}) cell. Avoidance is preserved and the horizontal forward witness becomes the vertical forward witness. Its allowed edge count is again K(A_i,A_{i+1}). This proves (1) and (2).

The kernel is not symmetric. For example K(1,12)=0 but K(12,1)=1. More generally a decreasing state J_m has zero outgoing row: it has no ascent and cannot supply a greedy witness. Such states can occur only as the final state. It would be incorrect to apply a reversible Markov-chain argument to this directed kernel without additional proof.

## 5. Exact marked-cell weights and convergence domain

Write w_A=z^|A|. Define h_A(z) as the sum over every finite continuation after a fixed current state A, including the empty continuation, with all successor weights and edge factors. Define ell_A(z) as the sum over every finite prefix before a fixed state A, including the empty prefix, with all predecessor weights and edge factors. Coefficientwise,

    h_A = 1 + sum_C K(A,C) w_C h_C,
    ell_A = 1 + sum_B ell_B w_B K(B,A).                         (3)

The marked-current-state factor is exactly

    w_A ell_A h_A.                                            (4)

It counts a permutation together with a distinguished canonical cell whose normalized pattern is A. This is a two-sided completion weight, not a uniform distribution on the cell's induced permutation.

For m>=1 let

    M_m(z) = sum_{|A|>=m} w_A ell_A h_A.                       (5)

If a_n=|Av_n(1324)|, then

    E[# canonical cells of size >=m in uniform Pi_n]
        = [z^n]M_m(z)/a_n,
    P(max cell size >=m) <= [z^n]M_m(z)/a_n.                  (6)

These are exact equalities/inequalities under the full uniform finite-class law.

All identities first hold as formal nonnegative series. For each total degree, every cell is nonempty and there are finitely many state sequences and edge choices. Let lambda=lim a_n^(1/n), whose finite existence follows from skew closure and the fixed-pattern exponential bound, and put rho=1/lambda. For every real 0<z<rho, F(z) and zF'(z) are finite. For fixed A, w_A h_A counts a subfamily whose first state is A, and w_A ell_A counts a subfamily whose last state is A; both are bounded by F(z)-1. Finally

    sum_A w_A ell_A h_A <= z F'(z),                            (7)

because a size-n permutation has at most n nonempty cells. Thus all displayed sums are finite in that domain. Formula (3) may be called an entrywise Neumann/path expansion, but no bounded, compact, self-adjoint or Hilbert-Schmidt operator on a specified normed space has been established. No assertion about convergence at z=rho is needed or made.

The first-cell frontier estimate controls coefficients of sum_{|A|>=m}w_A h_A. The arbitrary-cell expression (5) contains the additional ell_A. Dropping it is precisely the unjustified uniform-completion shortcut.

## 6. A rigorous exponentially large incoming bias

Let I_k be the increasing permutation and J_m the decreasing permutation. Both are in C, and S(J_m)=J_m. For k,m>=1,

    K(I_k,J_m)=binom(k+m-1,k-1)-1.                            (8)

Proof: every interleaving of the increasing upper block and decreasing lower block avoids 1324. An occurrence using two lower points would require those points in increasing order; an occurrence with one lower point would require a 213 in the upper block, and an occurrence with three lower points would require a 132 in the lower block. All are impossible. The highest lower point is its first point in position order. For greediness it must come after r upper points, where 1<=r<=k-1. After this first lower point, interleave the remaining k-r upper and m-1 lower points in binom(k-r+m-1,k-r) ways. Summing over r gives (8) by the elementary hockey-stick identity. It also covers k=1, with both sides zero.

Keeping only one-state prefixes I_k in (3) now gives, for 0<z<rho (and hence z<1),

    ell_{J_m}(z)
      >= 1 + sum_{k>=1} z^k [binom(k+m-1,k-1)-1]
       = 1 + z[(1-z)^(-m-1)-(1-z)^(-1)].                      (9)

Thus a uniform subexponential bound ell_A(z)=exp(o(|A|)), over all states, is false at every such fixed positive z. This statement is about actual 1324 completion weights, not an abstract comparison tree. It does not prove a macroscopic-cell event has significant uniform probability: the state-size weight z^m and normalization a_n are still essential, and h_{J_m}=1.

## 7. Outcome of this lane

The encoding and marked-cell identity give an exact local-interaction formulation of the escaping-index problem. They also establish a concrete exponentially growing boundary bias, which rules out a tempting shortcut.

No estimate proving [z^n]M_{ceil(epsilon*n)}(z)=o(a_n) has been obtained. In particular, ordinary two-cell domino counts do not establish a Hilbert-Schmidt bound for a size-symmetrized matrix: that would require the different sum sum_{A,C}K(A,C)^2 z^(|A|+|C|). The crude shuffle/Catalan bound certifies the open domain z<1/16. A valid improved squared-kernel bound reaching beyond rho, with the needed resolvent control, or a controlled non-reversible path comparison remains additional work.

Here is one precise sufficient analytic estimate, stronger than the weak-limit target. If there is eta>0 such that

    H(z,exp(eta)) := sum_A exp(eta*|A|) w_A ell_A h_A < infinity
                    for every real 0<z<rho,                    (10)

then the largest cell has an exponential tail at every fixed positive linear scale. Indeed, fix epsilon>0, put z=rho*exp(-eta*epsilon/2), and use nonnegative coefficients to get

    P(max cell size >=ceil(epsilon*n))
      <= z^(-n) exp(-eta*epsilon*n) H(z,exp(eta))/a_n
       = exp[-eta*epsilon*n/2+o(n)].                            (11)

The last equality is a bound on the logarithmic scale using log(a_n)=n*log(lambda)+o(n); its multiplicative constant is H at the fixed chosen z. Formula (10) has not been proved. Mere convergence H(z,u)<infinity when uz<rho follows trivially from H(z,u)<=uzF'(uz), but supplies no improvement for epsilon<=1 and cannot replace (10). Controlled exponential boundary weights could establish (10); subexponential boundary weights are not asserted necessary.

Finite regression script check_transfer.py compares the complete distribution of normalized greedy-cell state sequences, not just total counts, against (1) for all1324-avoiders through n=8. The counts are 1,2,6,23,103,513,2762,15793. TRANSFER_FINITE_CHECKS.json records the checks. Finite evidence is not a substitute for the proofs above.
