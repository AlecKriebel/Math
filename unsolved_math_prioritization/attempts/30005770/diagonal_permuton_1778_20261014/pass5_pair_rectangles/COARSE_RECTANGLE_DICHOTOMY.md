# A fixed coarse-grid occupied/sparse rectangle dichotomy

Final shared PASS5, row1778 /30005770, 14 October2026. This gives a rigorous finite-choice geometric reduction. The companion counting theorem and comb obstruction determine what this reduction does and does not currently prove under the exact uniform law.

## 1. Setup and constants

Let Inc(pi) count increasing position pairs in a permutation pi of size n. Represent its entries by the point centers

    ((i-1/2)/n, (pi(i)-1/2)/n).

Fix epsilon,theta>0 and put

    Q=ceil(max{2,8/epsilon,8/theta}),
    beta=epsilon/(2Q^4).                                   (1)

Partition each coordinate into the Q half-open intervals[r/Q,(r+1)/Q), r=0,...,Q-1. All point centers lie strictly below1. Each coordinate strip therefore contains at most ceil(n/Q) entries.

For a southwest cell A with column r and row c, and a northeast cell B with column s and row d, where s>=r+2 and d>=c+2, define the common core

    R(A,B)=[(r+1)/Q,s/Q) x [(c+1)/Q,d/Q).                   (2)

The half-open convention avoids ambiguities when a point lies exactly on a grid line. Every point in R(A,B) lies strictly between the coordinates of every pair(a,b) with a in A and b in B. Both endpoints' cell populations are finite sets of actual permutation entries.

## 2. Deterministic dichotomy

Assume n>=8/theta and Inc(pi)>=epsilon*n^2. Then there exist cells A,B as above with

    |A||B|>=beta*n^2.                                      (3)

If pi avoids1324, their common core is increasing, and one of the following holds:

OCCUPIED: R(A,B) contains at least theta*n points. Every cross pair(a,b) in A x B has at least theta*n interior points in its open rectangle.

SPARSE: R(A,B) contains fewer than theta*n points. Every one of the at least beta*n^2 cross pairs in A x B has fewer than2 theta*n interior points in its open rectangle.

Thus the witness involves only one of at most Q^4 ordered cell pairs, with Q and beta fixed before n grows. Each endpoint cell itself contains at least beta*n points, since the other contains at most n.

### Proof of the endpoint selection

The number of pairs whose position difference is at most2n/Q is at most2n^2/Q: for each first position there are at most floor(2n/Q) possible later positions. The same bound holds for pairs whose value difference is at most2n/Q. Discarding both types removes at most4n^2/Q<=epsilon*n^2/2 increasing pairs.

At least epsilon*n^2/2 pairs remain. Their two cells differ by at least two column indices and at least two row indices, because points in the same or neighboring coordinate bins have coordinate difference less than2/Q. Partition the remaining pairs by their ordered cell pair. Some pair of cells receives at least epsilon*n^2/(2Q^4) retained pairs. All points in A are southwest of all points in B, so every pair in A x B is increasing, and(3) follows.

### Proof of branch coverage

Fix any a in A and b in B. The common core(2) is inside the open rectangle(a,b). In a1324-avoider that open rectangle is increasing, since its endpoints together with any internal decreasing pair would form1324. Hence the core is increasing.

An interior point of rectangle(a,b) outside the core must be in one of the two endpoint columns or one of the two endpoint rows. Those four coordinate strips contain at most4ceil(n/Q) points. Therefore, writing m_(a,b) for its interior count and m_R for the common core count,

    m_R<=m_(a,b)<=m_R+4ceil(n/Q).                            (4)

Our choices of Q and n give

    4ceil(n/Q)<=4n/Q+4<=theta*n.                            (5)

If m_R>=theta*n, the occupied conclusion is immediate. Otherwise(4)-(5) give m_(a,b)<2theta*n for every cross pair, proving the sparse conclusion. These two cases exhaust the possibilities. QED.

## 3. How the exact count applies

The occupied branch supplies a linear increasing interior and many possible marked endpoints. It does NOT supply a small allocation cost. For each selected pair one must retain the actual strip counts p,q from RECTANGLE_DELETION_AND_ENTROPY.md. That note proves exponential suppression if

    m log lambda-e(m,p)-e(m,q)>=c n

for some fixed c>0. For example, m>=theta*n and p+q<=m are sufficient. The coarse-grid lemma does not imply this contamination condition.

The canonical comb mountains in COMB_RECTANGLE_OBSTRUCTION.md show that this omission is substantive: they have positive increasing-pair density and every occupied rectangle with at least20 interior entries has unfavorable raw allocation score. Their endpoint grid regions can be chosen as above, but no adaptive choice of macroscopic occupied rectangle makes that score positive.

The sparse branch provides a quadratic number of pairs with very small interiors. Deleting those interiors yields the exact empty marked skeletons of the companion note, with an admissibility indicator for every insertion record. When m=0 this is already the original marked permutation. There is no positive interior deletion loss to pay even a small allocation cost.

The permutation J_a direct-sum J_b, consisting of two decreasing blocks with every value in the first smaller than every value in the second, avoids1324 and has exactly a*b increasing pairs. All these pairs have empty open rectangles: later points in the first block lie below the first endpoint, and earlier points in the second block lie above the second endpoint. Thus positive pair density does not force the occupied branch or a long increasing subsequence. This family is a deterministic geometry test, not an asserted nonnegligible uniform family.

## 4. Outcome

The reduction has fixed constants, a fixed finite family of candidate endpoint regions, and complete occupied/sparse branch coverage. It does not suppress either branch merely by naming it. The occupied dense-contamination subcase is exponentially rare by the exact count, while the actual comb construction blocks a universal inference from occupied mass to a favorable raw-allocation score. The sparse branch requires direct control of actual empty or near-empty increasing-pair incidence, rather than a chain-length argument.

All earlier completion weights are represented by the full marked skeleton count and its admissibility test. No independent-cell distribution, source asymptotic extrapolation, or omitted shuffle factor is used. The uniform1324 limit and the universal fixed-alpha target remain unresolved by this lane.
