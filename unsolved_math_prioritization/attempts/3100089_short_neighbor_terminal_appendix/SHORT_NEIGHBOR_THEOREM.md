# Four-deletion/four-insertion neighbors and the two-word case

## Status and scope

Authored proof, 12 October 2026 UTC, accepted in the accompanying [mathematical audit](SHORT_NEIGHBOR_AUDIT.md) with the named external theorem below. The review is AI-assisted and unrefereed. No novelty claim is made.

**Theorem A (square, full-rank case).** Let A be a nonsingular symmetric binary matrix with more than one successful pressing word. Every successful word S has a distinct successful word T with LCS(S,T) >= n-4.

**Theorem B (arbitrary ambient dimension).** Let A be a successfully pressable symmetric binary matrix of rank r with more than one successful word. Every successful word S has a distinct successful word T with LCS(S,T) >= r-4.

**Corollary.** If there are exactly two successful words, they are adjacent at four deletions plus four insertions. Thus an instance with exactly two successful words cannot disprove the original normalized conjecture, in any rank or ambient dimension.

Having a neighbor does **not** establish general connectivity. For at most three vertices, however, a graph without isolated vertices is connected; the complete proof and further rank-six corollaries appear in [audit Section 11](SHORT_NEIGHBOR_AUDIT.md#11-derived-corollaries-independently-verified-in-this-audit). Nothing here rules out two or more components each having at least two words. In particular, the general Bixby–Flint–Miklós connectivity conjecture remains unresolved by this argument.

All calculations below are over F_2. A press at a current diagonal-one coordinate v replaces M by M+(Me_v)(Me_v)^T. Success means the entire matrix becomes zero. Rank drops by one at every legal press.

## 1. External input and its exact use

The sole non-elementary input is the characterization of uniquely pressable graphs by Joshua N. Cooper and Hays W. Whitlatch, *Uniquely Pressable Graphs: Characterization, Enumeration, and Recognition*, author-hosted manuscript dated July 18, 2017:

https://people.math.sc.edu/cooper/uniquely-pressables.pdf

Definition 7 (printed p.10) and Theorem 1 (printed p.13) give the following characterization for the instructional unit-upper-triangular Cholesky root U of an order-pressable, connected, full-length uniquely pressable graph. Write w_j for column j's weight, with indices 1,...,m. The root belongs to their class M_m exactly when:

1. Column j has support {j-w_j+1,...,j}.
2. The weights are nondecreasing, starting at w_1=1.
3. If w_i>2, then w_{i+2}>w_i whenever i+2<=m.
4. If a noninitial column has odd weight, that column and every later column have full weight.

We use this named characterization, not any general pressing-connectivity theorem. We have not independently reproved the characterization.

For the present application, the connectedness qualification causes no gap: a nonsingular matrix with a unique full-length successful word must have a connected underlying graph, since two nonempty disconnected blocks allow interleaving their successful subwords in at least two ways. Conversely, the cited theorem says roots in M_m produce uniquely pressable graphs. Thus for every nonsingular unit-upper-triangular U, the Gram matrix U^T U has exactly one successful word if and only if U belongs to M_m. The case m=1 is immediate.

The primary manuscript's theorem statement and all four defining conditions were directly read. Source-page verification, hash, and retrieval details are recorded separately. Source text/PDF is research input, not an authored publication payload.

## 2. Elementary setup and local substitution

Fix a successful word and relabel it 1,...,n. Scalar Gram–Schmidt gives a unique unit-upper-triangular U with A=U^T U. Its column x_j is supported on 1,...,j with coefficient one at j.

If I={a,...,b} is a consecutive interval, after pressing 1,...,a-1 the principal residual on I is U[I,I]^T U[I,I]. Any successful permutation of this smaller nonsingular matrix can replace the interval a,...,b in the original word: it gives legal scalar pivots on I, and after all of I is pressed, the full remaining matrix is the same Schur complement as before. Therefore the original suffix b+1,...,n is still legal. This uses equality of the full Schur complement, including every external coordinate.

Suppose A has more than one successful word. Among consecutive intervals for which U[I,I]^T U[I,I] has more than one word, choose one of minimum length m. Such an interval exists, since the entire interval qualifies. If m<=4, any other successful word on that interval gives the required neighbor. Otherwise, both one-end truncations of this root have unique successful words, so both belong to M_{m-1} by Section 1.

It remains to prove the following overlapping-root lemma.

**Lemma.** If a unit-upper-triangular m by m matrix U has both one-end truncations in M_{m-1}, but U itself is not uniquely pressable, then the identity word has a distinct successful neighbor of deficit at most four.

Here and below 'U is uniquely pressable' is shorthand for the symmetric matrix U^T U being uniquely pressable; no nonsymmetric root is used as a pressing matrix.

## 3. Exhaustive division of overlapping-root possibilities

Assume m>=5. Let H=U[1:m-1,1:m-1], and let w_j be its column weights. Its columns are suffix intervals. If there is a noninitial odd-weight column, let k be the first such index. Then k is odd, k>=3, and every column from k through m-1 is full. Before k, all noninitial weights are even. If no such column exists, write k=infinity.

Because the trailing truncation belongs to M_{m-1}, the last column has the form

x_m = a e_1 + e_t+...+e_m,

where a is 0 or 1, 2<=t<=m, and q=m-t+1 is its weight below the first row.

If q=m-1 and a=1, the last column is full and U satisfies all four conditions, so U is unique. This is excluded.

If q=m-1 and a=0:
- When m is even, Section 4 gives a deficit-two neighbor.
- When m is odd and k=infinity, U again satisfies all four conditions and is unique.
- When m is odd and k is finite, necessarily k<=m-2. Section 6 gives a deficit-four neighbor.

Now suppose q<m-1. Since the last column of the trailing truncation is not full, condition 4 forces q to be even and every noninitial column of that truncation to have even weight. For 3<=j<=m-1, its column weight is w_j-1 when the H-column is full, and w_j otherwise. Consequently a full H-column with j>=3 can occur only at an odd index. If H has a noninitial odd column k, condition 4 on H makes all its successors full. There cannot be a following even index, so necessarily k=m-1 and m is even. Thus k is infinity or m-1.

If a=0 and k=infinity, no H-column with j>=3 is full (its weight is even, and a full even-indexed column was excluded). The unchanged weights w_3,...,w_{m-1}, followed by q, inherit monotonicity and the two-step condition from the trailing truncation. The initial weight w_2=2 causes no exception to the two-step condition. All weights except w_1 are even. Hence U satisfies all four conditions and is unique.

If a=0 and k=m-1, then m is even and the trailing penultimate weight is m-2. Its monotonicity gives q>=m-2, so q=m-2. This is exactly the special form treated in Section 5.

If a=1, m even is treated in Section 4; m odd is treated by inverse reversal in Section 7.

These cases exhaust both bits a and every possible q. No case has been inferred solely from the finite tests.

## 4. Even-order endpoint exchange

In either of these cases, the word

T=(m,2,3,...,m-1,1)

succeeds:

(E1) m even, a=0, q=m-1, with arbitrary H in M_{m-1};

(E2) m even, a=1, q<m-1, under the overlapping-root conditions.

It keeps 2,...,m-1 as a common subsequence, so its deficit is at most two.

Here is a direct determinant proof. For 1<=j<=m-1, let z_j be the unique vector supported on the first j coordinates satisfying

z_j dot x_1=1, and z_j dot x_i=0 for 2<=i<=j.

Because x_1=e_1, z_j has first coordinate one. From the interval conditions on H,

z_j=e_1+...+e_j if j<k,
z_j=e_1+...+e_{k-1} if j>=k.

Indeed, before k each noninitial column has even weight, so the all-ones vector has zero inner product with it. From k onward columns are full and k-1 is even, so the truncated all-ones vector is orthogonal to them as well. Triangularity gives uniqueness. Put d_j=z_j dot z_j. Thus d_j is j modulo 2 for j<k, and zero thereafter.

Write y=x_m, alpha_j=z_j dot y, and beta_j=sum_{l>j} y_l. Cauchy–Binet gives

det Gram(x_2,...,x_j,y) = alpha_j + beta_j d_j.       (1)

To verify (1), the (j-1) old columns vanish below row j. A nonzero j-row minor therefore either uses all rows 1,...,j, with determinant alpha_j, or replaces a single row i<=j by a row l>j, with determinant z_{j,i} y_l. The cofactor vector is z_j because its first entry is one and it is orthogonal to x_2,...,x_j. Sum squared minors; in F_2 the squares do not change their values.

For E1, alpha_j=d_j+1 and beta_j=m-j equals j modulo 2. Equation (1) is 1+d_j(1+j), always one: d_j=0 or d_j=j modulo 2.

For E2, q is even and t=m-q+1 is odd. By Section 3, k is infinity or m-1. For j<k, let L_j=max(0,j-t+1), the number of tail entries of y in rows <=j. Then alpha_j=1+L_j and beta_j=q-L_j=L_j modulo 2. Equation (1) becomes 1+L_j(1+j). For odd j this is one; for even j, L_j is even because t is odd, so it is also one. If k=m-1, the only remaining case is j=m-1. Now d_j=0 and alpha_j=1+(m-t-1)=1 because m-t-1 is even.

Thus every proper prefix determinant of T is one; the full determinant is det(U)^2=1. All its scalar pivots are legal and T succeeds.

## 5. Even-order two-end-block exchange

The special form from Section 3 has m even, k=m-1, a=0, q=m-2. Therefore

x_1=e_1, x_2=e_1+e_2,
x_{m-1}=e_1+...+e_{m-1}, x_m=e_3+...+e_m.

For 3<=j<=m-2, x_j has even weight and no e_1 coefficient. The latter follows because a full H-column at an index >=3 was excluded, except for column m-1.

The following word succeeds:

T=(m-1,m,3,4,...,m-2,1,2).                         (2)

Its first two Gram–Schmidt vectors are

a=e_1+...+e_{m-1}, b=e_1+e_2+e_m.

They are orthonormal. For a middle coordinate x_j, its projection after these two presses is

x'_j=x_j+(x_j)_2 b
    =[x_j+(x_j)_2 e_2]+(x_j)_2 h,

where h=e_1+e_m. The bracketed vectors are the original residuals after pressing 1,2. They lie in span(e_3,...,e_{m-2}); h is isotropic and orthogonal to that span. Thus their Gram matrix is unchanged. Their increasing order succeeds, and its Gram–Schmidt vectors have the form g_j=e_j+lambda_j h.

The projected vector of vertex 1 after the first two presses is

x'_1=e_1+a+b.

It has norm one, inner product zero with h, and coefficient one at every e_j for 3<=j<=m-2. Therefore x'_1 dot g_j=1 for every middle press. There are m-4 such presses, an even number, so vertex 1 still has residual norm one after them. It can be pressed. The full matrix is nonsingular and only vertex 2 remains unpressed; its last scalar pivot is one. This proves (2). Its common middle subsequence has length m-4.

## 6. Odd-order four-letter relocation

Suppose m is odd, a=0, q=m-1, and k<infinity. Then k is odd and 3<=k<=m-2. The word

T=(k,k+1,m,2,3,...,k-1,k+2,...,m-1,1)              (3)

succeeds. Deleting the four letters 1,k,k+1,m leaves the same subsequence in T and the identity.

Its first three Gram–Schmidt vectors are

a=e_1+...+e_k,
b=e_{k+1},
c=(e_2+...+e_m)+e_{k+1}.

They are orthonormal. Indeed, the last column x_m has inner product zero with a and one with b, giving the stated c. The oddness of k and m checks all three norms.

Put h=e_1+c. For 2<=j<=k-1, x_j has even weight, so its projection after the first three presses is x_j+(x_j)_1 c. Its Gram–Schmidt vector in increasing order is

g_j=e_j+h.                                         (4)

For a direct check, the original residual after pressing vertex 1 is u_j=x_j+(x_j)_1 e_1. The linear map e_i -> e_i+h on span(e_2,...,e_{k-1}) is an isometry: h has norm zero and has coefficient one in each of those coordinates. Since the sum of the coefficients of u_j is (x_j)_1, it maps u_j to x_j+(x_j)_1 c. The original triangular Gram–Schmidt vectors e_j therefore map to (4).

Let d=e_1+...+e_{k-1}. After these early-middle presses, orthogonal projection sends each e_l with l>=k+2 to e_l+d. To see this, its inner products with a,b are zero and with c and each g_j are one. Hence its projection is

e_l+c+sum_{j=2}^{k-1} g_j
=e_l+c+(e_2+...+e_{k-1})+h=e_l+d,

where k-2 is odd. Every column from k onward is full. Thus the remaining increasing middle vertices k+2,...,m-1 have Gram–Schmidt vectors

g_l=e_l+d.

These are orthonormal because d is isotropic and supported outside these coordinates.

Finally e_1 has inner products 1,0,0 with a,b,c, and inner product one with every early or late middle vector. The total number of its nonzero projection coefficients before the final press is

1+(k-2)+(m-k-2)=m-3,

which is even. Its final residual norm is therefore one. This proves (3).

## 7. The remaining odd case by inverse reversal

Suppose a=1, q<m-1, and m is odd. Section 3 gives q even and k=infinity for H.

For an invertible symmetric matrix B, a permutation W succeeds on B if and only if its reversal succeeds on B^{-1}. This follows from complementary principal nonsingularity: B[S] is nonsingular exactly when B^{-1}[S^c] is nonsingular. One direct proof identifies their kernels under x -> Bx, with x supported on S and Bx supported on S^c. Thus the zero-kernel conditions agree. Apply the leading-principal-determinant criterion to a word and its reversal.

Let J reverse the coordinate order and define V=J U^{-T} J. Then V is unit upper triangular and

V^T V=J (U^T U)^{-1} J.

Inverse reversal preserves uniqueness, takes the identity word to the identity after this relabeling, and preserves LCS. Both one-end truncations of V are uniquely pressable, since they are inverse reversals of the opposite one-end truncations of U.

The first row of U^{-1} has its first m-1 entries all one: this is the formula for z_{m-1} with k=infinity. Its last entry is the parity of the first m-1 entries of x_m, namely 1+(q-1)=q=0. Consequently the last column of V is (0,1,...,1)^T.

The matrix V is nonunique because U is. It is therefore precisely the odd a=0, q=m-1, finite-k case of Section 6; the infinite-k alternative would belong to M_m and be unique. Section 6 supplies a deficit-four neighbor. Reversing its word and undoing the relabeling gives the required neighbor for U.

This completes the overlapping-root lemma and, by local substitution, Theorem A.

## 8. Arbitrary rank, omitted coordinates, and exactly two words

Here we use the already proved full-state trajectory-fiber lemma from the companion [full-state trajectory and last-support replacement lemmas](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md). In a fixed successful word S of length r, its exact matrix trajectory has disjoint nonempty layers L_1,...,L_r partitioning every original vertex with a nonzero row. Every independent choice of one letter per layer gives a successful word with that exact trajectory.

If any layer has at least two vertices, replacing its selected vertex gives a distinct successful word at deficit one. This conclusion is for the full ambient matrix, not just a selected principal block.

If every layer is a singleton, there are exactly r nonzero-row vertices in the entire original matrix. Every other row/column is zero. The matrix on those r vertices has rank r and is nonsingular; its successful words are exactly the original successful words after ignoring the permanently zero vertices. Apply Theorem A if there is more than one word. This proves Theorem B for each S separately.

In particular, with exactly two successful words, either a fiber already provides the other word at deficit one, or there are r nonzero coordinates and the nonsingular result applies. Both words are adjacent. For r=0 there is only the empty word, so the nonunique hypothesis cannot occur.

The six-vertex matrix (56,22,14,5,3,1), whose entire language consists of two words with LCS two, shows that the constant four is sharp for Theorem B and the two-word corollary.

## 9. What the finite checks do and do not establish

The exploratory enumeration constructs all roots whose two one-end truncations satisfy the four cited conditions, through a declared finite order. Direct pressing finds the short-neighbor patterns and tests the formulas. Counts capped at three are labeled as >=3, not exact counts. All two-word outputs are fully enumerated because their count is below the cap.

The arbitrary-order proof is Sections 2–8, not extrapolation from these computations. Independent dense-matrix/orthogonal-projection tests and finite inverse-reversal tests accompany the proof. General connectivity with four or more successful words remains unsettled here; the at-most-three-word corollary is proved in the accompanying audit.
