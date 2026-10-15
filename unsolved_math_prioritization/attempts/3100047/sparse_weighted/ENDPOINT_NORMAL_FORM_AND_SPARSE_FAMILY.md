# Endpoint normal form and a connected sparse pressing family

Problem 3100047 / row 1747. Authored research, 12 October 2026 UTC.

## Scope and result

The unrestricted full-length pressing 1/3–2/3 assertion remains unresolved. This report gives two arbitrary-order results:

1. An exact normal form and solution count for the affine endpoint-exchange constraints of an isolated instructional word. The existence test concerns **some choice of the final column**; the success test concerns a **specified final column**. The extension counts range over different matrices, not word weights in a fixed matrix.
2. A nonsingular symmetric family of order 2m, for every m >= 2, with exactly m successful words, m singleton instructional classes, and connected variable-order graph K_(2,2m−2). Its exact pair probabilities prove balance. Thus the number of isolated classes is unbounded even in a genuinely variable-order-connected family with only linearly many words.

A general one-moving-block criterion explains the balance of the second result. Neither result bounds the weights of multiple arbitrary instructional classes. No external source theorem is needed for the proofs below, and no novelty claim is made.

All matrix arithmetic is over F_2. For a symmetric matrix M, a legal press at a vertex x with M_xx=1 replaces M by M+(M e_x)(M e_x)^T. Successful full-length words are permutations pressing a nonsingular matrix to zero. For uniform successful words, p(x,y) denotes the probability that x precedes y.

## 1. Local setup and determinant identity, independently derived

Suppose the identity word is successful. Its instruction matrix is unit upper triangular U and satisfies A=U^T U: each press removes the outer product of its current column, and these columns, transposed into rows, form U. Conversely, a unit upper U gives a successful identity word for U^T U by eliminating its first row and then continuing inductively.

A word is successful precisely when all its leading principal determinants are 1. Indeed, sequential scalar Schur-complement pivots multiply to those determinants; their successive ratios are the pivots. Over F_2 a nonzero pivot is 1.

Consider exchanging positions i and i+d, d >= 1. Eliminate the common preceding prefix. The restriction to this interval is the Gram matrix of the corresponding principal block of U: block elimination removes its earlier rows, and all later rows in these columns are zero. A successful replacement of the local order leaves the same suffix state because Schur complements depend only on the eliminated set. Thus it suffices to use local indices 0,...,d.

Write R=U[0:d,0:d], let v=(v_0,...,v_(d−1)) be the first row of R^(-1), and put

H_k = sum_(r=0)^(k−1) v_r,    1 <= k <= d,
x_r = U_(r,d),                 0 <= r <= d,
T_k = sum_(r=k)^d x_r,         0 <= k <= d.

Here x_d=1. The leading k-by-k block of R has the same initial inverse first-row entries, because R is upper triangular. For the changed prefix set {1,...,k−1,d}, its principal determinant is

D_k = sum_(r=0)^(k−1) v_r x_r + H_k T_k,    1 <= k <= d.       (1)

For completeness, apply Cauchy–Binet to the Gram matrix on those k columns. All columns except the final one vanish below row k−1. The row set {0,...,k−1} contributes sum_(r<k) v_r x_r by the column-replacement formula. Any other nonzero minor replaces one row r<k by one row s>=k; its contribution is v_r x_s. Summing gives H_k T_k. Squares disappear over F_2. This proves (1) directly.

## 2. Exact endpoint-exchange normal form

Since v_0=1,

D_1 = T_0.

Using x_k=T_k+T_(k+1), subtract consecutive instances of (1) to obtain

D_(k+1)+D_k = H_(k+1) T_k + H_k T_(k+1),  1 <= k < d.         (2)

Therefore the **specified** final column x makes the endpoint exchange successful if and only if

T_0=1,
H_(k+1) T_k + H_k T_(k+1)=0 for k=1,...,d−1.                 (3)

These conditions are equivalent to every D_k=1, so they are both necessary and sufficient. In another useful description, successive vectors (H_k,T_k) and (H_(k+1),T_(k+1)) have zero determinant. Over F_2, consecutive nonzero vectors must therefore be equal; a zero vector can separate different nonzero vectors.

### 2.1 An isolated word: existence of an extension

The identity word is isolated under successful adjacent swaps exactly when U_(r,r+1)=1 at every consecutive position. To see this, if x then y are consecutive successful presses, swapping them is legal exactly when their current edge is 0: the second pivot relation is M_yy+M_xy=1, so both first choices are legal exactly when M_xy=0. That current edge is the corresponding entry of U.

Assume these consecutive entries are 1 within the interval. For d>=2, R_(0,1)=1 gives v_0=v_1=1 and hence H_1=1,H_2=0. The final consecutive entry is x_(d−1)=1, so

T_(d−1)=0, T_d=1.

The last equation in (3) becomes H_(d−1)=0. Conversely, if H_(d−1)=0, choose

T_0=1, T_1=...=T_(d−1)=0, T_d=1.

All equations (3) hold. This choice corresponds to the column

x_0=1, x_1=...=x_(d−2)=0, x_(d−1)=x_d=1.                    (4)

Thus, for fixed R and d>=2, there exists **some** final column, with final consecutive entry 1, for which the endpoint exchange succeeds if and only if

H_(d−1)=0.                                                  (5)

Equation (5) alone is not a test for a given column; that test is (3).

Boundary distances:

- d=1: the consecutive entry 1 prevents the adjacent swap. There is no feasible column under this condition.
- d=2: H_(d−1)=H_1=1, so no column is feasible. This recovers the three-position obstruction for an isolated root.
- d=3: H_(d−1)=H_2=0 automatically, so every such R has feasible extensions.

### 2.2 Exact affine dimension

Suppose d>=3 and (5) holds. Let h=(H_1,...,H_(d−1)). It starts with 1,0 and ends with 0. Let r(h) be the number of maximal runs of 1s in h, and let

z(h) = #{k : 2 <= k <= d−2 and H_(k−1)=H_k=H_(k+1)=0}.

Then the number of final columns with x_(d−1)=x_d=1 for which the endpoint exchange is successful is exactly

2^(r(h)+z(h)).                                              (6)

Proof. The variables T_1,...,T_(d−2) parametrize the free final-column entries bijectively once T_0=1,T_(d−1)=0,T_d=1 are fixed. On each run of 1s in h, equations (3) force the associated T entries to be constant, with one freely chosen bit. A zero entry of h adjacent to a 1 forces its own T entry to be zero. Every other zero entry is unconstrained, except the already fixed final entry T_(d−1)=0. Exactly the z(h) listed indices contribute those remaining bits. These independent choices prove (6).

This is an arbitrary-length restriction on isolated-root endpoint exchanges. It does not show that a resulting alternative word is isolated, and it does not count additional successful words created by the selected column. In particular, the power of two in (6) is not an instructional-class weight.

## 3. An arbitrary-order connected sparse family

Fix m>=2 and n=2m. Let U have diagonal entries 1, superdiagonal entries 1, one additional entry U_(0,2)=1, and all other entries zero. Define A_m=U^T U.

Since det U=1, A_m is symmetric and nonsingular. Its underlying graph is the path

1 – 0 – 2 – 3 – ... – (2m−1),

with loops exactly at 0 and 2. This follows directly from its columns: column 0 is e_0, column 1 is e_0+e_1, column 2 is e_0+e_1+e_2, and column j for j>=3 is e_(j−1)+e_j.

Write B_r=(2r,2r+1) for 0<=r<m. The complete successful-word set is

W_t = B_1 ... B_t B_0 B_(t+1) ... B_(m−1),   0<=t<m.         (7)

Empty strings in (7) are omitted. In particular, W_0 is the identity word.

### 3.1 Complete-language recurrence

Initially only 0 and 2 are looped, so every successful word must start with one of them.

If the first press is 0, vertices 1 and 2 are its neighbors. The press makes vertex 1 looped, removes the loop at 2, and creates edge 1–2. The residual is the path 1–2–3–... with its only loop at endpoint 1. Such a path has exactly one legal next press, at that endpoint; removing it moves the unique loop to the next endpoint. Induction forces the suffix 1,2,...,2m−1. This gives W_0.

If the first press is 2, its neighbors are 0 and 3. The press removes the loop at 0, creates the loop at 3, and creates edge 0–3. The only loop is now at 3, so the next press must be 3.

For m>=3, pressing 3 toggles loops on at 0 and 4 and creates edge 0–4. After removing 2 and 3, the residual is the same family on the relabeled vertices (0,1,4,5,...,2m−1). Its successful words, by induction, are all insertion positions of B_0 among B_2,...,B_(m−1). Prefixing B_1 gives W_1,...,W_(m−1).

For m=2, after pressing 2 and 3 the residual is the edge 0–1 with its only loop at 0, forcing 0,1. Together with the first branch, this gives exactly W_0=(0,1,2,3) and W_1=(2,3,0,1).

This proves (7) and excludes every other word, including legal prefixes that do not complete. In this even-order family, all branches of the displayed recurrence do complete. The successful-word count is exactly m.

### 3.2 Every instructional class is a singleton

For t<s, W_t and W_s differ on all positions occupied by B_0,B_(t+1),...,B_s, which is 2(s−t+1)>=4 positions. Hence no two distinct words in (7) differ by one adjacent transposition.

For clarity, the standard instructional-class argument is short. For a fixed label-indexed instruction root Q with A=Q^T Q, its successful words are exactly the linear extensions of the acyclic relation generated by the nonzero strict entries Q_xy. Indeed, those orders make Q upper triangular, and triangular Gram elimination is unique in a fixed order. Any two extensions of a finite poset are connected by adjacent swaps of incomparable letters: move the first letter of the target extension left to its place, then repeat on the remaining suffix. Thus a nonsingleton instructional class would contain an adjacent-swap edge. There is no such edge in (7), so all m classes are singletons.

The verifier also checks directly that every successful word's instruction root has every consecutive entry equal to 1.

### 3.3 All exact pair probabilities and variable-order connectivity

The order 0 before 1 is fixed. All labels in {2,...,2m−1} retain their numerical order. These are precisely the fixed unordered pairs; their number is

1 + binomial(2m−2,2).

For x in {0,1}, y in B_r, 1<=r<m, x precedes y in W_t exactly when t<r. Therefore

p(x,y)=r/m,   p(y,x)=(m−r)/m.                               (8)

There are 2(2m−2)=4m−4 variable unordered pairs. The variable-order graph is exactly K_(2,2m−2), and is connected for every m>=2. Consequently none of this variable behavior can be removed as fixed-order block padding.

The greatest minority probability is

delta(A_m) = floor(m/2)/m.                                  (9)

Choosing r=floor(m/2) gives a balanced pair for every m>=2. For m=3 the value is exactly 1/3, while m=2 gives 1/2. The number of successful words is only n/2, but the order and number of isolated classes are unbounded.

This example refutes the stronger hypotheses that connected variable-order families have boundedly many singleton classes, or that many such classes must split into fixed-order factors. It is not a counterexample to pressing balance: its balanced pairs are explicitly given by (8).

## 4. A general one-moving-block balance criterion

Let B be a fixed nonempty ordered block and C=(c_1,...,c_L) a fixed ordered word on the other labels. Suppose the entire successful-word set consists of inserting B into some q>=2 distinct gaps of C, with all words used uniformly. The permitted gaps need not be consecutive.

List the gap indices as 0<=t_1<...<t_q<=L, where t means insertion after t letters of C. Put k=floor(q/2). Since k<q, t_k<L, and for any x in B the pair (x,c_(t_k+1)) has probability exactly k/q: precisely the first k gap choices put x before that letter. For q>=2, k/q lies in [1/3,1/2]. Thus this whole-language hypothesis implies balance.

The family (7) is a genuine symmetric-matrix example of this criterion in which every instructional class is isolated and the variable-order graph is connected. Applying the criterion only inside one conditional fiber or one subfamily would not imply global balance.

## 5. Verification, coverage, and remaining obstruction

The direct rank-one-pressing checker for the normal form exhausts all chain roots R and final columns at distances 1 through 6. At distance 7 it checks 100 distinct prior roots selected with deterministic seed 147, and all 64 final columns for each. For every tested column it compares direct pressing against (3), then compares the exact successful-column count against (5)–(6). It does not reuse the determinant identity to test success. There are 40,267 specified columns in this fixed test scope.

For distances 1 through 6, the histograms (successful-column count : number of prior roots) are:

- d=1: 0:1
- d=2: 0:1
- d=3: 2:2
- d=4: 0:4, 2:4
- d=5: 0:32, 4:32
- d=6: 0:512, 4:384, 8:128

The sparse-family checker independently constructs the path matrix, recursively enumerates every successful word by pressing, checks the entire language (7), checks every instruction root's consecutive entries, checks every pair's exact integer numerator, and checks the complete variable-order graph. Its fixed stopping condition is completion of all even orders 4,6,...,40, plus odd controls 5,7,...,21. The odd controls have one forced final vertex and the same even variable core; they are not used for the connected-family theorem. Full words and exact rational pair counts were retained in the accepted audit evidence for orders 6 and 12; those raw evidence files are not distributed in this prose-only edition.

These finite checks corroborate the arbitrary-order proofs; they do not establish a search bound for arbitrary pressing matrices. Exploratory scripts are not proof evidence.

The unresolved issue remains a fixed-matrix one: how do the alternative roots and their numbers of linear extensions constrain the global pair distribution? The affine normal form counts possible roots after changing a matrix column, and the sparse family settles one exact language pattern. Neither controls mixtures of several different moving-block patterns or arbitrary instructional classes.
