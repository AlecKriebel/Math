# A four-letter weighted identity for full-length pressing families

Problem 3100047 / row 1747. Research date: 12 October 2026 UTC.

## Outcome and scope

This note proves an exact local classification and an ambient, uniform-count identity across two different instructional classes. It also gives a smaller abstract obstruction to using prefix splicing alone. It does **not** prove the general pressing 1/3–2/3 conjecture, or the assertion for every family with four, five, or six successful words. No novelty claim is made.

Throughout, matrices are symmetric over F2. A legal press of vertex v requires current diagonal 1 and adds the outer product of its current column to the current matrix. For a nonsingular matrix A, Sigma(A) is the set of successful full-length pressing permutations. All probability statements use the uniform measure on Sigma(A).

Main results:

1. A four-vertex residual that admits abcd, abdc, and cdab, but not bacd or acbd, has **exactly** one of the following success families:
   - {abcd, abdc, cdab, cdba};
   - {abcd, abdc, cdab, dcab}.
   In either case its two instructional classes have size 2 and 2. Every pair with one label in {a,b} and the other in {c,d} has probability 1/2.
2. For any fixed four labels in an arbitrary ambient matrix, every qualifying prefix-set/suffix context gives these four local words the same exact multiplicity F(S)G(S union Q). Summing over disjoint contexts gives an exact cross-pair count of 2W in **each** direction. If the contexts cover at least two thirds of all successful words, every one of the four fixed cross-pairs is balanced globally.
3. The four-word abstract family {12345, 12354, 12435, 34125} is closed under taking all maximal singleton-addition chains of its union of prefix sets, but has no balanced pair. The classification above excludes it as a pressing language, including with arbitrary fixed common prefix/suffix padding.

These are matrix-specific partial results. The coverage hypothesis in result 2 is not established for all matrices.

## 1. Exact local classification

### Theorem 1

Let B be symmetric on four distinct labels a,b,c,d. Suppose

abcd, abdc, cdab belong to Sigma(B),

while bacd and acbd do not. Then Sigma(B) is precisely one of the two four-word families stated above.

### Proof of the root constraints

Use a,b,c,d as coordinate order. Success of abcd gives a unique unit upper triangular instructional root U with B=U^T U. This follows directly by writing the press columns as rows of U: earlier coordinates are cleared, each pivot is 1, and the four rank-one updates sum to B. Conversely, such a triangular root makes the listed pivot order successful.

Write

U = [[1, p, q, r],
     [0, 1, s, t],
     [0, 0, 1, u],
     [0, 0, 0, 1]].

For two consecutive positions in a successful word, exchanging them is legal precisely when the corresponding strict-upper entry of U is 0. Indeed, with first pivot 1, both orders require the second diagonal before the first press to be 1 and their current off-diagonal to be 0; then the two rank-one updates commute. Therefore the three stated adjacent-exchange conditions imply

p=1, s=1, u=0.

The diagonal at c in the initial matrix is B_cc=1+q+s=q. The successful word cdab begins with c, so q=1.

The successful prefix c,d,a also forces t=1. Here is a direct complementary-minor calculation with no inaccessible-prefix assumption. Since det B=1, det B[{a,c,d}]=(B^{-1})_bb. The row of U^{-1} indexed by b is (0,1,s,t+su). With s=1 and u=0 its self-dot-product is 1+1+t=t. Because B^{-1}=U^{-1}U^{-T}, its b-diagonal is t. The prefix determinant is 1, hence t=1. The cofactor formula used here is just the inverse formula for an invertible matrix; signs vanish over F2.

Thus all six strict-upper entries are determined except r:

U_r = [[1,1,1,r],
       [0,1,1,1],
       [0,0,1,0],
       [0,0,0,1]],   r in {0,1}.

The two resulting matrices, displayed as ordinary 0/1 arrays, are

B_0 = [[1,1,1,0],
       [1,0,0,1],
       [1,0,1,1],
       [0,1,1,0]],

B_1 = [[1,1,1,1],
       [1,0,0,0],
       [1,0,1,0],
       [1,0,0,1]].

### Proof that these are the complete success families

For B_0, initially only a and c are black.

- Pressing a leaves b as the only black vertex. Pressing b next leaves c,d black and nonadjacent. Hence this branch gives exactly abcd and abdc.
- Pressing c leaves d as the only black vertex. Pressing d next leaves a,b black and nonadjacent. Hence this branch gives exactly cdab and cdba.

For B_1, initially a,c,d are black.

- Pressing a leaves b as the only black vertex; pressing b leaves c,d black and nonadjacent. This gives exactly abcd and abdc.
- Pressing c leaves d as the only black vertex. After c,d, vertex a is the only black vertex, followed by b. This gives cdab.
- Pressing d symmetrically forces c,a,b, giving dcab.

These descriptions exhaust the legal first presses and all subsequent branches. They prove the exact classification, without a census of ambient matrices.

In each matrix, abcd and abdc have the same instructional root by their legal adjacent commutation. The other two words likewise share a root. These roots differ: the first root has a strict instruction from a to c, whereas the second class places c before a. Thus there are exactly two instructional classes, each containing two words. Each word in the first class puts both a,b before both c,d; each word in the second class does the reverse. All four cross-pairs consequently have counts 2 and 2. QED.

### A support-only consequence with fewer hypotheses

If abcd, abdc, cdab are successful, then at least one of bacd, acbd, dcab, cdba is successful. If either of the first two is successful this is immediate; otherwise Theorem 1 applies and exactly one of the last two is successful. This implication remains true with any fixed common outside prefix and suffix, as proved next.

## 2. Exact ambient weights, including inaccessible sets

Let E be the label set of a nonsingular, successfully pressable A, and let Z=|Sigma(A)|. Fix an ordered quadruple (a,b,c,d) of distinct labels and put Q={a,b,c,d}.

For every subset S of E define F(S) to be the number of orders of S whose every leading principal submatrix in A is nonsingular. These are exactly legal pressing prefixes with label set S. Set F(empty)=1, and F(S)=0 if A[S] is singular. No claim that every nonsingular principal set has a legal ordering is being made.

For every nonsingular principal set T define R_T, the residual on E minus T, by

R_T = A[E minus T] + A[E minus T,T] A[T]^{-1} A[T,E minus T].

Let G(T)=|Sigma(R_T)|, allowing this count to be zero, and set G(T)=0 for singular A[T]. Set G(E)=1. Thus G counts possible complete suffixes after the set T; it does not assert that T is itself reachable. With D(T) the 0/1 nonsingularity indicator, the exact integer recurrences are

F(S) = D(S) sum over x in S of F(S minus {x}),          S nonempty,
G(T) = D(T) sum over x outside T of G(T union {x}),     T not E.

The recurrences count complete determinant flags; they do not use delta-matroid accessibility or greedoid augmentation. In particular F(E)=G(empty)=Z.

For S disjoint from Q, with F(S)>0, let B_S=R_S[Q]. Call S **qualifying** if G(S union Q)>0 and B_S satisfies Theorem 1's five local tests: the three specified successes and two specified failures. Such B_S is nonsingular by the successful abcd test. Therefore A[S union Q] is nonsingular as well.

Define the nonnegative integer

W = sum over qualifying S of F(S) G(S union Q).

### Theorem 2: exact weighted identity

Let H be the subfamily of Sigma(A) in which the four labels Q occur consecutively and the set S of labels before that block is qualifying. Then

|H| = 4W.

For each one fixed pair (x,y) in {a,b} times {c,d}, exactly 2W words in H put x before y, and exactly 2W put y before x. Hence

2W <= number of all successful words with x before y <= Z-2W.

In particular, if 6W>=Z, then all four of these fixed cross-pairs are globally 1/3–2/3-balanced. Equivalently, the sufficient condition is |H|/Z>=2/3.

### Proof of substitution and common multiplicity

A legal prefix with set S leaves the full residual R_S, independently of its ordering: symmetric scalar elimination, or summing its instructional rank-one updates, gives the displayed Schur complement. Thus there are exactly F(S) interchangeable prefixes.

In R_S, the diagonals and updates on Q while pressing only Q are precisely those obtained by pressing its principal restriction B_S. Vertices outside Q do not enter those internal pivot computations. Therefore any local word in Sigma(B_S) is legal in the full residual. After all Q is pressed, the full remaining state is R_(S union Q), independently of its local order; this is the same Schur-complement state property. There are exactly G(S union Q) interchangeable successful suffixes.

Consequently concatenation is a bijection between

legal orders of S × Sigma(B_S) × successful suffixes after S union Q

and full successful words with prefix set S immediately followed by all of Q. Each individual local word has multiplicity exactly F(S)G(S union Q). Theorem 1 supplies four local words, two in each cross-pair direction, giving the stated counts for this S.

These context families are disjoint as S varies: in a permutation with all four fixed labels consecutive, there is only one such four-label block, and its preceding label set is unique. Summing introduces no double counting. The ordered quadruple is fixed throughout, so the identity never averages different choices of a balanced pair. The two inequalities follow because the remaining Z-4W words contribute nonnegative counts to either direction. If 6W>=Z, both directions have count at least 2W>=Z/3. QED.

This is an identity for the actual uniform family counts, not arbitrary weights assigned to abstract classes. In every fixed outside-prefix/outside-suffix context, it pairs two words from one instructional class with two from a distinct class. Different contexts need not correspond to different global instructional classes; the count identity does not need that stronger, generally unjustified assertion.

### An exact-threshold ambient example

The criterion is not confined to contexts covering every successful word. On labels 1,...,5, take

A = [[1,1,0,0,1],
     [1,0,1,1,0],
     [0,1,0,0,0],
     [0,1,0,1,0],
     [1,0,0,0,0]].

Its complete success family is

12345, 12354, 14523, 15423, 41523, 42315.

For (a,b,c,d)=(2,3,4,5), the only qualifying context is S={1}, with F(S)=G(S union Q)=1. Thus W=1, Z=6, and H comprises exactly the first four displayed words. The coverage is exactly 2/3. The pair (2,4) is in the order 2 before 4 in exactly two words, so its global probability is exactly 1/3. This attains the endpoint of the count bound in Theorem 2; it is not a claim that the coverage condition is necessary.

## 3. A smaller abstract obstruction to prefix-splicing arguments

Let

L = {12345, 12354, 12435, 34125}.

Let P consist of all sets appearing as prefixes of words in L. Its levels are

0: empty;
1: {1}, {3};
2: {1,2}, {3,4};
3: {1,2,3}, {1,2,4}, {1,3,4};
4: {1,2,3,4}, {1,2,3,5};
5: {1,2,3,4,5}.

There are eleven sets. The complete singleton-addition paths through these levels are exactly the four listed words:

- Starting with 3 forces 4, then 1, then 2, then 5.
- Starting with 1 forces 2. The next letter is 3 or 4. After 1,2,4, the only possible fourth letter is 3. After 1,2,3, either 4 or 5 is possible.

Thus L already contains every complete singleton-addition chain of its union prefix system, including every allowed splice. Nevertheless, relative to 12345, its inversion sets are

empty;
{(4,5)};
{(3,4)};
{(1,3),(1,4),(2,3),(2,4)}.

They are pairwise disjoint. Every comparison has minority count 0 or 1 out of 4, and hence no pair is balanced. The majority order 12345 even belongs to L.

This disproves the proposed generic lemma that a prefix-complete family with pairwise-disjoint inversion sets has at most three words. It also shows that a generic complete-singleton-addition-chain countermodel need not wait until seven words or twelve labels.

### Why no pressing matrix realizes this language

Suppose L=Sigma(A). Work on the first four coordinates of the successful order 12345. Their residual principal matrix satisfies the hypotheses of Theorem 1 with (a,b,c,d)=(1,2,3,4):

- 12345, 12435, 34125 are successful;
- 21345 and 13245 are absent.

All these words have the same last label 5. The Schur-complement substitution argument shows that their first-four success tests are exactly the local tests. Theorem 1 forces 34215 or 43125 to be successful, contradicting the displayed exact language.

The same contradiction applies after inserting any fixed common prefix and any fixed common suffix around these five-letter words. Eliminate the prefix, apply the four-letter result, and use the common suffix state. It also applies if the four labels are embedded in a larger graph with arbitrary interactions: only the asserted common outside words are needed. No unlisted nonsingular principal subset is assumed to be accessible.

## 4. Verification boundary

The mathematical proofs are above. The authored verifier retained with the accepted audit, and not distributed in this prose-only edition, independently:

- checks the two local matrices by direct rank-one pressing;
- tests all 64 unit upper triangular 4×4 roots against the five stated hypotheses and the exact classification (this is an identity check, not a new exhaustive ambient balance search);
- recomputes the eleven-set abstract path family and its exact pair counts;
- compares the weighted formulas with direct full-word enumeration on deterministic ambient examples, including forced padding and nontrivial prefix/suffix counts;
- computes F and G independently from principal nonsingularity, preserving zeros for unreachable or uncompletable sets.

The general conjecture remains open. A missing step is an unconditional coverage bound, or another weighted identity that controls the family outside H. Likewise, the four-word obstruction does not classify every possible small-cardinality pressing family.
