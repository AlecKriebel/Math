# Short-window count obstructions for full-length pressing families

Problem 3100047 / row 1747. Authored research, 12 October 2026 UTC.

## Result and boundary

This note gives arbitrary-ambient-dimension sufficient conditions for a balanced pair and necessary conditions for a hypothetical unbalanced family with four, five, or six full successful words. It does **not** establish balance for every such family. No novelty claim is made.

Let A be a nonsingular symmetric matrix over F2 with nonempty successful full-length pressing language Sigma(A), and let Z=|Sigma(A)|. Successful words are used uniformly. A press at x requires current diagonal 1 and adds the outer product of its current column to the matrix. A pair is balanced when each direction occurs in at least Z/3 successful words.

The main conclusions are:

1. If two successful words are PabcR and PcbaR, with the same ordered outside words P,R, all six permutations of a,b,c between P and R succeed. Every internal pair is therefore balanced whenever Z<=9, including equality.
2. If PabcdR, PabdcR, and PcdabR succeed, some pair has at least two successful words in each direction. Thus there is a balanced pair whenever Z<=6. No failure/absence hypothesis is needed for this conclusion.
3. If Pa b1...bk R and P b1...bk a R succeed, all k+1 insertion positions of a succeed. A middle comparison has at least floor((k+1)/2) words in each direction, proving balance whenever Z<=3 floor((k+1)/2). In particular, a relocation across at least three letters is incompatible with an unbalanced Z<=6 family.
4. In an unbalanced Z in {4,5,6} family, every possible first letter other than the first letter of the strict majority order begins exactly one successful word; the dual statement holds for last letters. These exceptional branches yield uniquely pressable residuals/principal restrictions, but no external characterization of uniquely pressable graphs is used here.

The local identities below detect obstructions, not an unconditional coverage theorem. A language can avoid all displayed short patterns in arbitrary dimension. The present work does not prove that a pressing language with four to six successes must contain one.

## 1. Setwise elimination and substitution

A permutation is successful exactly when every leading principal determinant is 1. This follows by scalar symmetric elimination: the successive pivots are the ratios of consecutive leading determinants. Over F2 a nonzero pivot equals 1.

A legal prefix with label set S leaves on the other labels the Schur complement

R_S=A[E minus S]+A[E minus S,S] A[S]^{-1} A[S,E minus S].

This state depends on S, not the order of the prefix. Let Q be disjoint from S. While pressing only labels in Q, internal pivot values are computed entirely in B=R_S[Q]. If a local order of Q succeeds in B, it is legal in the full residual. After all Q is eliminated the remaining state is R_(S union Q), independently of the local order. Consequently any local successful order can replace another one with the same outside successful prefix and suffix.

The argument never asserts that an arbitrary nonsingular principal set has a legal ordering, or that a nonsingular residual has a successful coordinate pressing order.

## 2. Three-position reversal forces six substitutions

### Theorem 1

If PabcR and PcbaR are successful, so is P tau R for every permutation tau of a,b,c. Each pair in {a,b,c} occurs in each direction in exactly three of these six distinct words. Therefore all three pairs are globally balanced if Z<=9.

### Proof

Eliminate P and restrict to Q={a,b,c}. Success of abc gives the unit upper instructional root

U=[[1,p,q],[0,1,r],[0,0,1]], with B=U^T U.

Indeed the three legal press columns, transposed into rows, give U; conversely any such root supplies the indicated successful order.

Success of cba requires B_cc=1. Since B_cc=1+q+r, this gives q=r. It also requires det B[{b,c}]=1. Using B_bb=1+p and B_bc=pq+r, this condition becomes

p+pq+r=0.

Substitution gives p+pq+q=0. For binary p,q this vanishes only when p=q=0: if p=0 it equals q, and if p=1 it equals 1. Hence p=q=r=0 and B=I_3. All six local orders succeed. Section 1 lifts them with the fixed P,R.

For each internal pair the six permutations split 3 and 3. Other words can only increase each count. Thus the global direction counts both lie between 3 and Z-3. When Z<=9, 3>=Z/3, proving the inclusive claim. QED.

### Diagnostic application

The abstract four-word prefix-complete language

{012435,012534,013425,230415}

has transitive majority order 012345, which is absent. It is not a pressing language: its first two words share prefix 012 and then have 435 versus 534, so Theorem 1 forces six distinct suffix substitutions. In particular 012345 is forced. This is an algebraic exclusion; prefix-splicing alone does not exclude the abstract language.

## 3. A support-only four-position criterion

### Theorem 2

Suppose PabcdR, PabdcR, and PcdabR all succeed. Then some fixed pair has at least two successful words in each direction. In particular the global family is balanced whenever Z<=6.

### Proof with explicit pairs

Work in the four-label residual principal matrix B after P.

Case 1: bacd also succeeds. Success of abcd and bacd means a,b can commute. Success of abcd and abdc means c,d can commute. In the instructional root of abcd the entries U_ab and U_cd are zero. These swaps are at disjoint positions, and carrying out both preserves that root. Therefore badc succeeds as well. The four words abcd,abdc,bacd,badc give two occurrences of each orientation of (a,b). Substitute the same P,R.

Case 2: bacd fails but acbd succeeds. The four known words abcd,abdc,acbd,cdab put (b,c) in each direction exactly twice. Substitute the same P,R.

Case 3: bacd and acbd both fail. Write the root of abcd as

U=[[1,p,q,r],[0,1,s,t],[0,0,1,u],[0,0,0,1]].

The adjacent-swap criterion is that the corresponding root entry is zero; it follows by evaluating the two pivot diagonals and current edge. The hypotheses give p=s=1 and u=0. Success of cdab gives initial diagonal B_cc=1, hence q=1. Its cda prefix has determinant 1. Since det B=1, that determinant is (B^{-1})_bb. The b row of U^{-1} is (0,1,s,t+su), and B^{-1}=U^{-1}U^{-T}; its self-dot-product is 1+s+t+su=t under s=1,u=0. Thus t=1.

Only r remains free:

U_r=[[1,1,1,r],[0,1,1,1],[0,0,1,0],[0,0,0,1]].

For r=0, directly pressing c,d leaves a,b both looped and nonadjacent, so both cdab and cdba succeed. For r=1, directly pressing d,c leaves a as the sole looped remaining vertex, so dcab succeeds in addition to cdab. Thus the four successful local words are at least

abcd,abdc,cdab,cdba for r=0,
or abcd,abdc,cdab,dcab for r=1.

Every cross-pair in {a,b} times {c,d} has two occurrences of each orientation in these four words. Substitute the same P,R.

All cases produce a fixed pair with both global direction counts at least 2. If Z<=6, this is at least Z/3. QED.

This strengthens the existing five-test local classification only in the sense of packaging it as a three-success support/count criterion: it removes the absence hypotheses by explicit additional cases. The root calculation itself is the one independently derived in the earlier weighted-window report.

## 4. One-letter relocation and an arbitrary-length count threshold

### Theorem 3

Let b1,...,bk be distinct labels different from a. If Pa b1...bk R and P b1...bk a R both succeed, then every insertion of a into the fixed word b1...bk succeeds with the same outside words. For any j in {1,...,k}, the pair (a,bj) occurs in the direction a before bj in j of these k+1 words and in the other direction in k+1-j.

For k>=1, choose j=floor((k+1)/2). Both counts are at least floor((k+1)/2), so this pair is globally balanced if Z<=3 floor((k+1)/2).

### Proof

After P, let a's diagonal be alpha, let B be the principal matrix on b1,...,bk, and let v be their adjacency vector to a. The first word gives alpha=1. The second gives a successful order b1,...,bk for B, hence B=C^T C for a unit upper triangular C. Write v=C^T z.

For each j, let B_j,C_j,v_j,z_j be the first-j restrictions. Triangularity gives v_j=C_j^T z_j. Both the b1...bj prefix in the second word and the a,b1...bj prefix in the first word have determinant 1. Their scalar Schur-complement equation is

1=alpha+v_j^T B_j^{-1}v_j=1+z_j^T z_j=1+sum_(i=1)^j z_i.

Consecutive equations force every z_i=0, and hence v=0. Vertex a is therefore looped and nonadjacent to all b_i in this residual. Pressing any of these b_i keeps a's column unchanged and pressing a leaves their internal state unchanged. Every insertion position is legal and leaves the same suffix state. Counting insertion gaps proves the formulas and threshold. QED.

At k=3 the conclusion gives a fixed pair with two words in each direction. At k=5 it gives three in each direction and the same Z<=9 threshold as Theorem 1. These are sufficient thresholds; additional local successful orders can only strengthen them.

## 5. Exact common-context multiplicities

The preceding theorems already hold from one fixed ordered prefix/suffix witness. They admit useful weighted versions without replacing completion counts by nonsingularity.

For a subset S define F(S) to be the number of legal orders of S, with F(empty)=1 and F(S)=0 when A[S] is singular. For a nonsingular principal set T let G(T)=|Sigma(R_T)|, allowing G(T)=0, and set G(T)=0 for singular T. Put G(E)=1.

Fix Q and fixed ordered local words. For every S disjoint from Q with F(S)>0 and G(S union Q)>0, let B_S=R_S[Q]. If a local support hypothesis holds in B_S, each individual local successful order has exactly

F(S) G(S union Q)

full successful realizations with Q consecutive and preceding set S. This is the Cartesian-product substitution bijection from Section 1. Different S give disjoint full-word families, because the consecutive block on fixed Q has one preceding label set.

For the three-label reversal, sum this multiplicity over qualifying S to obtain W. The six guaranteed orders contribute exactly 6W full words, and exactly 3W in each direction for each fixed internal pair. Therefore Z<=9W suffices for all three fixed internal pairs to be globally balanced.

For the relocation criterion, fix a,b1,...,bk and sum multiplicities over the qualifying contexts. The k+1 guaranteed insertions contribute (k+1)W words, with the fixed comparison (a,bj) counted jW and (k+1-j)W times. Hence Z<=3 floor((k+1)/2)W suffices.

For Theorem 2, the selected pair can depend on which case the residual has. It is therefore invalid to sum arbitrary case-dependent contexts and pretend they all certify the same pair. A single witness context suffices for Z<=6. A weighted sum is legitimate only after fixing a pair and restricting to contexts known to give at least two of each direction for that pair.

## 6. Necessary endpoint reductions for unbalanced Z=4,5,6

For these three cardinalities, a pair is balanced exactly when its minority direction occurs at least twice. Thus absence of a balanced pair means every comparison has minority count at most one.

Orient every pair by its strict majority direction. It is a transitive tournament: a directed triangle would have three probabilities strictly exceeding 2/3, whereas each permutation satisfies at most two of its three directed comparisons. A triangle-free tournament is transitive, so label its total order v1,...,vn.

Let x!=v1 begin at least one successful word. Every word beginning x puts x before v1, contrary to the majority direction. This is a minority event and occurs at most once. Therefore x begins exactly one successful word. The residual after pressing x has exactly one successful full word, because prefixing x is a bijection from its full successful orders to successful orders of A beginning x.

Dually, if y!=vn ends a successful word, it ends exactly one. A successful order of A[E minus {y}] can always be extended by y: this principal matrix is nonsingular because it occurs as a successful prefix set, and the final scalar Schur complement is det A/det A[E minus {y}]=1. Therefore A[E minus {y}] has exactly one successful word.

If one word has both exceptional endpoints x!=v1 and y!=vn, let U be its instructional root written in that word's order. The symmetric Gram matrix U[2:n,2:n]^T U[2:n,2:n] is the residual after pressing x, while U[1:n-1,1:n-1]^T U[1:n-1,1:n-1] is the original principal restriction A[E minus {y}]. Both symmetric Gram matrices are uniquely pressable in their induced orders, by the previous two bijections. The triangular root blocks themselves are not being called symmetric pressing matrices. This is a necessary structural constraint, not a classification theorem. This note does not use a characterization of unique pressability to draw additional conclusions.

## 7. Boundary against a stronger majority-closure shortcut

Transitive majority of three successful words need not be successful. Consider the symmetric matrix with binary row masks

(29,6,31,21,13),

on labels 0,...,4. Direct pressing verifies 01234,23104,24103. Their strict majority order is 21034, whose first two labels have principal determinant 0, so it fails. The whole matrix has 20 successful words; this does not give a counterexample at Z=4,5,6. It only prevents assuming majority success from a selected triple. The verifier retained in the accepted audit evidence records the full exact language and majority computation; its raw output is not distributed in this prose-only edition.

## 8. Verification and remaining obstruction

The authored verifier retained in the accepted audit evidence, and not distributed in this prose-only edition, uses direct rank-one pressing to check every three- and four-label unit triangular root against Theorems 1 and 2, and checks relocation independently of its Schur-complement proof. It also checks arbitrary ambient substitutions, the abstract-language exclusion, the majority-closure control, and a nonsingular uncompletable residual control.

These local finite checks corroborate arbitrary-dimension substitution proofs. They are not a new ambient census and do not establish a finite search bound. Exploratory code about two uniquely pressable truncations is not a theorem or a proof input, and is excluded from the results above.

A hypothetical unbalanced family with four to six words must avoid: a common-context three-letter reversal; the three four-letter support words of Theorem 2; a one-letter relocation across at least three letters; and any exceptional-endpoint branch containing two completions. The unresolved step is proving that these constraints, or stronger principal-minor constraints, force an impossibility in arbitrary dimension.
