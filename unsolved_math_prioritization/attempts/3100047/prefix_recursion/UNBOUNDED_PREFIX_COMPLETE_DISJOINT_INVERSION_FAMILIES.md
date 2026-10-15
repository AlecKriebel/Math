# Unbounded prefix-complete families with disjoint inversion sets

Problem 3100047 / row 1747. Authored research, 12 October 2026 UTC.

## Result and scope

The proposed abstract cardinality obstruction is false. There are prefix-complete permutation families with pairwise disjoint inversion sets of **every cardinality at least three**. In particular:

- Exactly five words occur on seven labels.
- Exactly six words occur on nine labels.
- The majority permutation belongs to every family in this construction.
- For every cardinality at least four, every pair has minority count zero or one, so none is 1/3–2/3-balanced.

These are **abstract path-system countermodels**, not pressing counterexamples. In fact, none of the constructed families of cardinality at least four can be the complete successful language of a pressing matrix. This follows from the established four-letter local forcing theorem, reproduced in support-only form below, and taking a legal fixed-prefix residual.

At the original research stage, no previous file was changed and no repository or publication action was taken.

## 1. Definitions

For a family L of permutations of [n], let P(L) be the union of all their prefix sets, including the empty set and [n]. Its complete singleton-addition language consists of all permutations whose every prefix set belongs to P(L). Call L **prefix-complete** when it equals this language.

Relative to the order 1<2<...<n, the inversion set of a permutation w consists of pairs (a,b), a<b, for which b occurs before a in w.

The following observation is valid but does not bound cardinality. If the inversion sets in L are pairwise disjoint, any subset S that is not an initial interval [k] lies on at most one word of L. Indeed, there are a<b with a outside S and b inside S; every word through S inverts (a,b).

## 2. A two-label extension lemma

**Lemma.** Suppose L is prefix-complete on [n], n>=3, contains the identity permutation, and has pairwise disjoint inversion sets. Set N=n+2. Shift all old labels up by two, and define

L' = {12 (w+2) : w in L} union {3,4,...,N-1,1,2,N}.

Then L' is prefix-complete, contains the identity, has pairwise disjoint inversion sets, and has exactly |L|+1 words.

### Proof of complete singleton-addition closure

Call the prefix sets of the inherited words 12(w+2) the **old states**. There is only one old rank-one state, {1}. Every old state of rank at least two contains both 1 and 2. Their induced singleton-addition language is exactly the inherited language, since the first two letters are forced and the rest is a relabeled copy of L.

Write B_k for the rank-k prefix of the newly added word. Its private states are precisely

- B_k={3,4,...,k+2} for 1<=k<=N-3;
- B_(N-2)={1,3,4,...,N-1}.

The last two states are B_(N-1)=[N-1] and B_N=[N]. They were already old states, because the identity belongs to L. Every displayed private state omits 2, so it is distinct from every old state at the same rank; the rank-one private state {3} is also distinct from {1}.

We classify **all** possible edges between the private and old states. An edge is a containment between consecutive ranks.

1. An old-to-private edge can enter B_1 only from the empty set, giving the intended new first letter 3. It cannot enter B_2 from the old rank-one state {1}, because B_2 omits 1 (N>=5). For k>=3 it cannot enter B_k from an old rank-(k-1) state, because the old state contains 2 and B_k omits 2.
2. For 1<=k<=N-3, there is no private-to-old edge out of B_k: every candidate old rank-(k+1) state contains both 1 and 2, neither of which is in B_k. Such an edge would therefore have to add at least two labels.
3. Any private-to-old edge out of B_(N-2) must add the missing label 2, since old states contain it. The only possible endpoint is [N-1], and this is the intended merge. Its remaining step to [N] is forced.

There is one private state at each private rank, and their consecutive containments give the new word's chain. Edges among old states are unchanged. Thus the only new full path is the stated word: it branches at the empty set, follows its forced private chain, and merges at [N-1] for the last step. Hence the full language is exactly L'.

### Proof of inversion disjointness

An inherited word has 1 and 2 first, so its inversions are exactly the shifted old inversions, entirely within {3,...,N}. The new word's inversion set is exactly

{(1,b),(2,b): 3<=b<=N-1}.

This is disjoint from every inherited inversion set. Inherited inversion sets remain pairwise disjoint. The new word starts with 3, whereas every inherited word starts with 1, so the new word is distinct. The identity is inherited. This proves every assertion. QED.

## 3. Explicit infinite family

Start with

L_1={123,132,213}.

Its union prefix sets are the empty set; {1},{2}; {1,2},{1,3}; and {1,2,3}. The complete paths are exactly the three listed words. Its inversion sets are empty, {(2,3)}, and {(1,2)}.

Apply the extension lemma repeatedly. For each integer m>=1 this gives L_m on 2m+1 labels with

|L_m|=m+2.

Equivalently, L_m consists of:

1. The identity on [2m+1].
2. Its adjacent swap of 2m and 2m+1.
3. Its adjacent swap of 2m-1 and 2m.
4. For each j=1,...,m-1, the word

(1,...,2j-2, 2j+1,...,2m, 2j-1,2j, 2m+1).

The inversion sets in item 4 are

{(a,b): a in {2j-1,2j}, 2j+1<=b<=2m}.

They have sizes 4(m-j). Their smaller endpoints are in disjoint pairs, so these inversion sets are disjoint from one another and from the two singleton inversion sets.

The number of distinct prefix states is (m+1)^2+2. For the base m=1 there are six states. An extension embeds the previous prefix system and adds two initial states (the empty set and {1}), then adds N-2 private states; it therefore increases the count by N=2m+1. Summing these increases gives (m+1)^2+2.

Exactly 2+2m(m-1) unordered pairs have minority count one; the remaining 3m-2 pairs have minority count zero. These counts sum to binomial(2m+1,2). For m>=2, the minority probabilities are 0 or 1/(m+2)<1/3, and the natural order is the strict majority order. Thus these families are uniformly unbalanced for every cardinality >=4. In terms of cardinality T=m+2, the dimension is 2T-3, the prefix-state count is (T-1)^2+2, the number of variable pairs is 2+2(T-3)(T-2), and the maximum minority probability is exactly 1/T.

### Exactly five words

On [7],

L_3={1234567,1234576,1234657,1256347,3456127}.

The respective inversion sets are

- empty;
- {(6,7)};
- {(5,6)};
- {(3,5),(3,6),(4,5),(4,6)};
- {(1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6)}.

There are exactly eighteen prefix sets, exactly these five complete singleton-addition paths, fourteen variable pairs with minority count one, and seven fixed pairs.

### Exactly six words

On [9],

L_4={123456789,123456798,123456879,123478569,125678349,345678129}.

The inversion-set sizes are 0,1,1,4,8,12. There are exactly twenty-seven prefix sets, exactly these six complete paths, twenty-six variable pairs with minority count one, and ten fixed pairs.

## 4. Why these examples cannot be pressing languages

The needed matrix-specific implication is the support-only consequence of Theorem 1 in the accepted authored note [A four-letter weighted identity for full-length pressing families](../sparse_weighted/FOUR_LETTER_WEIGHTED_IDENTITY.md). A self-contained proof is included here to make the nonrealizability conclusion independent of merely citing that file.

### Four-letter local forcing

For a symmetric four-label matrix B over F2, if abcd, abdc, and cdab are successful full pressing words, then at least one of

bacd, acbd, dcab, cdba

is successful.

To prove this, suppose bacd and acbd are unsuccessful. Success of abcd gives a unit upper triangular instructional factor B=U^T U, where

U=[[1,p,q,r],[0,1,s,t],[0,0,1,u],[0,0,0,1]].

An adjacent exchange in a successful pivot order is successful exactly when the corresponding strict-upper entry of U is zero. Therefore failure of bacd and acbd, and success of abdc, give p=s=1 and u=0. Success of cdab makes c initially black. Since B_cc=1+q+s=q, this forces q=1. Its successful three-letter prefix cda also forces t=1: det B=1 and the complementary principal-minor identity gives det B[{a,c,d}]=(B^-1)_bb; row b of U^-1 is (0,1,1,t), whose self-dot-product is t.

Only r is undetermined. The two resulting matrices are

B_0=[[1,1,1,0],[1,0,0,1],[1,0,1,1],[0,1,1,0]],
B_1=[[1,1,1,1],[1,0,0,0],[1,0,1,0],[1,0,0,1]].

Direct pressing gives cdba for B_0 and dcab for B_1. For B_0, the branch c,d leaves a,b as nonadjacent black vertices; for B_1, the branch d forces c,a,b. This proves the implication.

The implication remains true with a fixed successful outside prefix and suffix around these four labels. Eliminate the fixed prefix. The four-label principal residual determines the legality of the four local pivots. After all four labels have been pressed, the remaining Schur-complement state is independent of their order, so every locally successful alternative admits the same suffix.

### Excluding the base four-word family

The constructed L_2 is exactly

{12345,12354,12435,34125}.

If it were the complete successful language of a matrix A, use the four labels (a,b,c,d)=(1,2,3,4) with fixed suffix 5. The words 12345,12435,34125 supply the three positive hypotheses. The words 21345 and 13245 are absent. The local implication forces 43125 or 34215, neither of which belongs to L_2. Contradiction.

### Excluding all larger constructed families

For m>=3, the complete subfamily of L_m beginning with 12 is exactly 12 followed by the shifted family L_(m-1); the newly added word begins with 3.

Suppose a pressing matrix realizes L_m. Its prefix 12 is legal because the identity is successful. After pressing this prefix, its Schur residual has complete successful language exactly the shifted L_(m-1): every successful residual word extends that legal prefix, and every full word with that prefix restricts to a successful residual word. Iterating gives a pressing realization of L_2, which is impossible.

Equivalently, the fixed initial interval 1,2,...,2m-4 leaves a five-label residual with successful language L_2 after relabeling. Thus none of L_m for m>=2 is realizable. This is a conclusion about the displayed construction, not a classification of all abstract unbalanced families.

## 5. Verification and search coverage

Two separate exact implementations retained in the accepted evidence, and omitted from this prose-only edition, verify the finite examples:

- `verify_construction.py` independently constructs the union of prefix states and enumerates **all** complete singleton-addition paths, then compares the resulting set with the claimed word list. It checks pairwise inversion disjointness and exact pair counts for m=1,...,32, corresponding to n=3,...,65 and cardinalities 3,...,34. The full output is retained with the accepted evidence; the present edition distributes only its identity and aggregate verification metadata.
- `verify_small_independent.py` does not use the recursive constructor or the first verifier's path DFS. It exhaustively scans all 7!=5,040 and all 9!=362,880 permutations against prefix sets taken directly from the two displayed word lists. It independently computes every pair's inversion count. Its complete small-case outputs are retained with the accepted evidence and omitted from this prose-only edition.

A preliminary n=7 C++ search had an upfront 100-second search bound and a 115-second process cap. It formed a pairwise-compatibility graph, then stopped at the first five-word candidate after six recursion nodes. It was **not** an exhaustive enumeration of all five- or six-word families. Its output is only discovery evidence; the countermodels are established by the independent checks and the arbitrary-dimension extension proof. No claim about the search graph's sufficiency is needed or made.

The prior no-five/no-six diagnostic through n=6 is consistent with this result: the displayed first five-word countermodel has n=7. The first six-word example in this construction has n=9; no assertion is made about minimal dimension for six words.

General pressing balance, including its unresolved small-cardinality cases, is not settled by these abstract countermodels or their particular nonrealizability. What is settled is that prefix completeness plus inversion disjointness cannot by themselves rule out exact cardinalities five or six, or impose any finite cardinality bound.
