# Pressing balance: exact mixing obstructions and an endpoint-exchange identity

Scope: nonsingular symmetric matrices over F2 with at least one full-length successful pressing permutation. This note does not prove or disprove the full pressing 1/3–2/3 conjecture. The examples below are countermodels to insufficient abstract reductions, not pressing counterexamples. No assertion of novelty is made.

## 1. The source decomposition and its limit

Cooper, Gartland, and Whitlatch, *A New Characterization of V-Posets*, Lemma 4 and Section 5, supply the relevant instructional-poset decomposition: successful pressing orders are a disjoint union of linear-extension classes of instructional Cholesky roots. The uniform weight of a class is its number of linear extensions divided by the total number of successful orders. Their autonomy characterization concerns graphs with just one such class; it does not say that every instructional poset in a multiclass graph is a V-poset.

Primary source: https://people.math.sc.edu/cooper/VPosets.pdf ; official preprint https://arxiv.org/abs/1810.07276 . The source was directly inspected. The following examples and identity are authored here, independently of the source.

### Equal-sized, individually balanced V-poset classes do not suffice

Take sixteen labels arranged in eight consecutive two-label blocks

(a1,b1), (c1,d1), (a2,b2), (c2,d2), (a3,b3), (c3,d3), (a4,b4), (c4,d4).

For each i=1,2,3,4, define P_i by ordering all blocks as displayed, reversing the fixed order of (ai,bi), leaving (ci,di) incomparable, and fixing the displayed within-block order in every other block. Each P_i is a V-poset: it is a two-element antichain with a chain appended below and another above. It has exactly two linear extensions, and (ci,di) is an exactly 1/2-balanced pair within that class.

The four extension sets are pairwise disjoint. Their union has eight orders. In its uniform distribution, a reversed (ai,bi) occurs in exactly two orders, and a reversed (ci,di) in exactly one. Every other pair has constant order. Thus every pair's minority probability is 0, 1/8, or 1/4; there is no 1/3–2/3-balanced pair.

Moreover, the four classes are exactly the connected components under adjacent transpositions: each class is one edge, while orders from different classes differ on at least two disjoint two-label blocks and cannot be adjacent. They cannot be related by a one-letter relocation either. Consequently equal class weights, internal V-poset balance, and separation into the correct sort of local-swap components do not alone prove global balance. This union is not asserted to be the language of maximal chains of a set system or to be realizable by a symmetric matrix.

## 2. A stronger countermodel for generic prefix-set path arguments

Let k>=2, with labels 1,...,2k. Let e=(1,2,...,2k). For 1<=i<=k let s_i be obtained from e by swapping the entries i and i+k. Let W={e,s_1,...,s_k}. Define F to be precisely the union of all prefix sets of the words in W, including the empty and full sets. Here and below, references to maximal chains mean complete singleton-addition chains from empty to full; no assertion about arbitrary maximal chains of the inclusion poset is intended.

Claim: the maximal singleton-addition chains from empty to full in F are exactly W.

Write B_t={1,...,t}. The prefix of s_i at level t is B_t except when i<=t<i+k, when it is

C_i(t)=(B_t\{i}) union {i+k}.

Within this active range, C_i(t) is contained in B_(t+1) only at t+1=i+k. Conversely B_t is contained in C_j(t+1) only at t+1=j. There are no edges C_i(t) -> C_j(t+1) for i!=j. Indeed, if j<=t then j belongs to C_i(t) but not C_j(t+1). If j=t+1, then i+k>k>=t+1, and i+k is absent from C_j(t+1). These exhaust the possibilities because j<=t+1 whenever C_j(t+1) is active.

A path therefore stays on the baseline, or enters exactly one branch at its starting level i and exits at i+k. A second branch cannot be entered afterward: all branches start by level k, while every branch ends after k. This proves the claim. In particular, W is the exact family of complete singleton-addition chains from empty to full, and hence is closed under every splice at a common prefix set.

Every pair's order differs from e in at most two of the k+1 words. For the explicit classification, put a_i=i and b_i=i+k. If i<j, the pair (a_i,a_j) reverses only in s_i, and (b_i,b_j) only in s_j. The pair (a_i,b_i) reverses only in s_i. For i<j, (a_i,b_j) never reverses; for i>j, it reverses exactly in s_i and s_j.

At k=6, there are twelve labels, forty-nine feasible prefix sets, and exactly seven maximal chains. Every minority probability is 0, 1/7, or 2/7, strictly below 1/3. Thus even the uniform distribution on all maximal chains of a finite prefix-set system need not have a balanced pair.

There are no adjacent-transposition edges between distinct words of W. Nor can two distinct words differ by a one-letter relocation: e and s_i differ by a nonadjacent transposition, whereas s_i and s_j differ by two disjoint transpositions. Thus every nonempty fixed-order one-letter insertion fiber is a singleton, hence an interval; all other fibers are empty. All local-swap components are singleton linear-extension classes. These properties do not rescue a generic path-family proof.

This example is NOT claimed to be a pressing language. In particular, the family F is not silently identified with the complete family of nonsingular principal subsets of a hypothetical matrix. Additional nonsingular subsets need not lie on successful full chains.

## 3. An exact binary-symmetric endpoint-exchange identity

Assume the identity order is successful for A, and write A=U^T U over F2, with U unit upper triangular. Use one-based indices. Fix i<=k<j and set

R=U[{1,...,k},{1,...,k}],
c=U[{1,...,k},{j}],
h=(R^(-1) 1)_i,
t=sum_(s=k+1)^j U_sj.

Then

det A[({1,...,k}\{i}) union {j}]
  = (R^(-1)c)_i + h t.                                      (1)

All quantities and sums in (1) are in F2.

Proof. Let C=({1,...,k}\{i}) union {j}. Cauchy–Binet gives

det(U[:,C]^T U[:,C]) = sum_(|S|=k) det(U[S,C])^2.

Over F2 the square of each determinant is itself. Every column indexed by C other than j is zero beyond row k. Hence a nonzero minor can use at most one row beyond k. The row set S={1,...,k} contributes (R^(-1)c)_i by the column-replacement formula. Any other contributing row set has the form ({1,...,k}\{r}) union {s}, with s>k. Expanding along row s contributes U_sj times the (r,i)-cofactor of R, which is (R^(-1))_ir because det R=1 and signs disappear in F2. Summing over r and s gives h t. Terms with s>j vanish by upper triangularity. This proves (1).

Corollary. The order obtained from identity by exchanging positions i and j is successful if and only if the right-hand side of (1) equals1 for every k=i,...,j-1. All other prefix sets agree with identity, so this is exactly the leading-principal-minor criterion.

For fixed columns1,...,j-1 of U, these conditions are an affine linear system in column j. The coefficients involve only those earlier columns; the diagonal U_jj=1 is fixed. This is an actual algebraic constraint on matrix-realizable languages, absent from an arbitrary maximal-chain family.

As an immediate check, j=i+1 reduces to U_i,i+1=0, the usual commuting adjacent-swap criterion. For j=i+2, writing a=U_i,i+1, b=U_i,i+2, c=U_i+1,i+2, the conditions reduce to b=c and b+ac+a=0. Hence a=b=c=0: exchanging the endpoints of a three-position interval is possible exactly when all three entries commute in that instructional root. This conclusion holds regardless of vertices before or after the interval.

## 4. A genuine forbidden exchange pattern for singleton classes

The generic seven-word countermodel above is not matrix-realizable. This follows from a short algebraic argument, rather than a solver verdict.

### Proposition

Suppose identity is a successful order and its unit upper instructional root U satisfies U_(r,r+1)=1 at every consecutive position. There cannot be three successful orders obtained from identity by individually exchanging positions

(i,i+6), (i+2,i+8), and (i+4,i+10).

The statement holds in any ambient dimension for which those positions exist. It also holds when the consecutive-entry hypothesis is imposed just throughout that eleven-position interval.

Proof. After eliminating positions before an exchange window, restrict to its seven positions. This leaves the Gram matrix of the corresponding seven-by-seven principal block of U. Indeed, block Gaussian elimination of U^T U removes the earlier rows of U, and later rows are zero in these seven columns by upper triangularity. Thus local computations below apply to a window anywhere in U, regardless of entries outside it.

Use local indices0,...,6. Write x_r=U_(r,6) for 0<=r<=4. The next two entries of this column are U_(5,6)=U_(6,6)=1. Let v_r be entry(0,r) of the inverse of the leading six-by-six block of U. The initial entries of these inverse rows agree for every smaller leading block, by upper triangularity. In particular v_0=v_1=1. Define H=v_0+...+v_4.

For the order exchanging0 and6 to succeed, every intermediate replacement determinant from (1) is1. At prefix cardinalities1 and2, (1) gives respectively

D_1=x_0+x_1+x_2+x_3+x_4,
D_2=x_0+x_1.

Consequently

x_2+x_3+x_4=0.                                               (2)

At prefix cardinality5, the tail sum is U_(5,6)+U_(6,6)=0. Writing V=sum_(r=0)^4 v_r x_r gives D_5=V. At cardinality6, the tail is just U_(6,6)=1, so

D_6=V+v_5+(H+v_5)=V+H.

As D_5=D_6=1, we obtain H=0.

The inverse recurrence vU=e_0^T gives v_2=1+U_(0,2) and

v_4=U_(0,4)+U_(1,4)+v_2 U_(2,4)+v_3,

because U_(3,4)=1. Hence

H=1+U_(0,2)+U_(0,4)+U_(1,4)+U_(2,4)
    +U_(0,2)U_(2,4)=0.                                     (3)

Return to the original indices. Suppose the exchanges starting at i and i+2 both succeed. From (2) for the first exchange,

U_(i+2,i+6)+U_(i+3,i+6)+U_(i+4,i+6)=0.

Apply (3) to the second exchange. With f=U_(i+2,i+4) and x=U_(i+4,i+6), substitution of the preceding zero sum reduces it to

1+f+f x=0, or f(1+x)=1.

Over F2 this forces f=1 and x=0. Therefore exchanges starting at i and i+2 force U_(i+4,i+6)=0. On the other hand, exchanges starting at i+2 and i+4 force U_(i+4,i+6)=1 by the same argument. This is the required contradiction.

### Consequence for the seven-word generic path family

If that family were the exact success set of a matrix A, identity would be successful. Its instructional root must satisfy U_(r,r+1)=1 for every r: otherwise swapping those consecutive entries of identity would also succeed, by the adjacent case of (1), but no such word belongs to the proposed family. Yet that family contains the exchanges(1,7), (3,9), and (5,11), contrary to the proposition. Thus no symmetric matrix realizes this exact success language. No assumption was made about hidden nonsingular principal subsets.

### Independently replayable finite corroboration

The proof above is general. A complete small check additionally treats a chain root's last six positions as a state. Such a six-by-six unit upper matrix has ten free entries, so there are1024 states. Appending the next column adds five free entries and the two fixed final ones. Equation(1) determines the allowed transitions; shifting the seven-by-seven window produces the next six-position state. The independently implemented direct-press C++ checker gives exactly the same weighted path counts as the affine-constraint Python checker:

length0:1024; length1:2560; length2:6400; length3:11520; length4:23040; length5:0; length6:0.

There are2560 directed transitions. The certificate assigns each of the1024 states a rank in{0,1,2,3,4}, strictly decreasing on every allowed transition. Rank counts are512,256,128,64,64 respectively. The affine checker recomputes every edge and validates the stored certificate, and the direct checker performs1425408 local transition tests without using the affine formula. These are finite corroborations of the explicit algebraic proposition, not a bounded search promoted to the full balance conjecture.

## 5. What remains

The endpoint-exchange identity does not bound the relative cardinalities of different instructional classes, and the two countermodels do not satisfy matrix realizability merely by construction. A full proof still needs an inequality or structural theorem for the actual symmetric-matrix language. A counterexample still needs an explicit nonsingular A with an exact successful-word count and all pair marginals outside the closed balance interval.

The verifier retained with the accepted audit independently checks the finite countermodels and the identity by direct F2 determinants and rank-one pressing. It is not distributed in this prose-only edition. Those checks support the authored proofs; they do not extend any finite exhaustive search or prove the general conjecture.
