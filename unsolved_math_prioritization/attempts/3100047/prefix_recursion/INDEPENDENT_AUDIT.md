# Independent audit: unbounded prefix-complete inversion-disjoint families

**Verdict: ACCEPT.** The frozen proof establishes its stated arbitrary-cardinality abstract construction and establishes nonrealizability of each constructed family of cardinality at least four by a symmetric binary pressing matrix. No mathematical correction to the frozen proof is required. This is a negative result about a generic combinatorial proof route, not a pressing counterexample or a proof of general pressing balance.

Date: 2026-10-12 UTC. At the original audit stage, no repository, commit, push, pull-request, or publication action was taken. Source files were preserved; audit evidence was retained separately.

## 1. Frozen inputs and acceptance boundary

The audited proof is the author's explicitly frozen edition:

- Original frozen construction proof, identified by the following byte count and SHA-256
- 12,276 bytes; SHA-256 `57525c4830b88ec8f7e291b9103984d2fb2accf27a60cc9aadb44062f7f58981`.

All 14 files identified by the producer's freeze manifest were independently checked against its byte counts and SHA-256 values before snapshotting. The original manifest is retained with the accepted evidence; its identity is recorded in ORIGINAL_INPUT_PINS.json. Preliminary discovery files are provenance, not premises for the theorem and not evidence of an exhaustive search.

The corrected weighted note requested for the audit is separately pinned:

- Original corrected weighted-identity report, identified by the following byte count and SHA-256
- 14,116 bytes; SHA-256 `6b643be0ea2c513d165750c500d0c06cb615f37fba7ee00259509397f5d240eb`.

The frozen proof instead names its prose-only publication-preparation copy. That copy was also checked and snapshotted:

- Authored prose-only edition, [A four-letter weighted identity for full-length pressing families](../sparse_weighted/FOUR_LETTER_WEIGHTED_IDENTITY.md)
- 14,185 bytes; SHA-256 `c8b49247ff354352a44121a6092213f8ba746e3724d7e933d9d98cf84b457d1f`.

The two weighted files differ only in one verification-boundary sentence saying that the verifier is retained with the accepted audit and omitted from the prose-only edition. Their mathematical theorem and proof text are identical. Thus this citation difference does not change the dependency being audited.

The original input-pin inventory records all 17 snapshotted input files. The original final audit manifest additionally pins the authored audit, independent tester, and independent results. Their identities are recorded in ORIGINAL_INPUT_PINS.json. Original mathematical acceptance applies only to those exact original bytes; this editorial edition has separately pinned identities.

## 2. Definition check: full singleton-addition paths

For a family L of permutations of [n], form the union P(L) of all prefix sets. Its complete language C(P(L)) consists of permutations w such that every set of the first k letters of w belongs to P(L), for k=0,...,n. Equivalently, these are paths from the empty set to [n] whose edges add exactly one label.

This definition is used throughout this audit. It is not replaced by arbitrary maximal chains in the inclusion poset of P(L). An inclusion-poset cover can skip ranks, and mere maximality would not guarantee a full permutation path. The frozen proof correctly uses complete singleton-addition paths and classifies edges only between consecutive ranks.

## 3. Independent extension proof and every cross-level edge

Let L be prefix-complete on [n], n>=3, containing the identity. Set N=n+2 and define

L' = {12(w+2): w in L} union {3,4,...,n+1,1,2,n+2}.

Call prefix sets of the inherited words old states. Besides the empty set and {1}, each is `{1,2} union (S+2)` for S in P(L). Their induced complete language is exactly `12(L+2)` because the first two labels are forced.

The new word has private states

- Q_k={3,...,k+2}, for 1<=k<=n-1;
- Q_n={1,3,...,n+1}.

It then reaches Q_(n+1)=[n+1] and Q_(n+2)=[n+2]. These last two states already occur among old states because the old identity is present. Every private state lacks 2; the rank-one private state is {3}, distinct from old {1}.

The complete list of possible cross-type singleton-addition edges is as follows.

1. Old to Q_1: the only old rank-zero state is empty, and the intended edge exists.
2. Old rank one to Q_2: impossible. For n>=3, Q_2={3,4}, while the old state is {1}.
3. Old rank k-1 to Q_k, for 3<=k<=n: impossible. Every old state at rank at least two contains 2, whereas Q_k does not.
4. Q_k to old rank k+1, for 1<=k<=n-1: impossible. Q_k contains neither 1 nor 2, but any old state of rank k+1 contains both. One addition cannot supply two missing labels.
5. Q_n to old rank n+1: the only possible extra label is 2. The endpoint must therefore be [n+1], which is an old state. This intended edge exists.

There is exactly one private state at each private rank, and consecutive private states are nested. Hence a path entering the private states is forced until it merges at [n+1]; only the final label n+2 remains. There are no intermediate cross-type entries or exits and no hybrid complete words. Thus C(P(L'))=L', with exactly |L|+1 words.

The n=3 boundary is covered without an empty-range gap: the private states are {3}, {3,4}, and {1,3,4}; they merge at {1,2,3,4} and end at [5].

The condition n>=3 is genuinely needed for the stated general lemma. Starting from the closed singleton language {12} at n=2 gives inherited word 1234 and added word 3124. Their prefix union also permits 1324, through the cross edge {1} to {1,3}. This negative control was checked computationally.

## 4. Inversions, counts, and exact finite examples

Each inherited word has inversions only among {3,...,N}, exactly the shifted inversions of its old word. The new word has precisely

{(1,b),(2,b): 3<=b<=N-1}.

These sets are disjoint, so pairwise inversion disjointness is preserved. The identity is inherited. The added word begins with 3, so it is distinct from every inherited word.

Use cardinality T rather than the author's index m=T-2. The seed at T=3 is {123,132,213}, with six prefix states and seven singleton-addition edges. Its inversion sets are empty, {(2,3)}, and {(1,2)}. Iterating the lemma yields all integers T>=3, with

- n=2T-3 labels;
- T words;
- T^2-2T+3=(T-1)^2+2 prefix states;
- T^2-T+1 singleton-addition edges;
- 2T^2-10T+14=2+2(T-3)(T-2) pairs inverted in exactly one word;
- 3T-8 pairs inverted in no word.

For the state recurrence, the old system is embedded at rank shifted by two, two initial states are added, and n private states are added. Thus an extension increases states by N. For edges, it adds two initial edges and n+1 private-branch edges, while the final shared edge is already old. Thus it increases edges by N+1. These recurrences give the displayed formulas. The edge formula is additional audit evidence, not a claim in the source proof.

The variable-pair count is two seed singleton inversions plus successive new inversion-set sizes 4,8,...,4(T-3). Subtracting from binomial(2T-3,2) gives 3T-8. Every variable pair has minority count exactly one, since T>=3. Therefore the maximum minority probability is exactly 1/T, and every T>=4 family lacks a 1/3–2/3-balanced pair. At T=3, the two variable pairs have minority probability 1/3; this boundary is not an unbalanced example.

The exact T=4 family is {12345,12354,12435,34125}. The exact T=5 and T=6 families and all inversion sets listed in the source were independently verified. They have 18 and 27 prefix states, respectively; their variable-pair counts are 14 and 26.

## 5. General state uniqueness and subfamilies

The frozen report includes the unique-off-baseline-state lemma and does not claim a subfamily-closure or compatibility-graph theorem.

Its state-uniqueness lemma is correct even without assuming the identity is a member. If |S|=k and S differs from [k], choose a in [k] minus S and b in S minus [k]. Then a<b, and every word through S puts b before a. Two such words would share inversion (a,b), contradicting disjointness. Thus every noninitial prefix state belongs to at most one word.

A useful additional, independently proved corollary is limited as follows. If L is prefix-complete and inversion-disjoint and K is a subfamily, then

C(P(K)) is contained in K union {identity}.

Indeed, C(P(K)) is contained in C(P(L))=L. Any omitted nonidentity word has at least one noninitial prefix state, unique to that word, so it cannot survive in P(K). In particular, every identity-containing subfamily K is prefix-complete. It is false that arbitrary subfamilies are always closed: {132,213} acquires the word 123. This distinction avoids silently deleting the baseline in a closure reduction. The corollary is not needed for acceptance of the construction.

## 6. Independent matrix argument

The following local result is credited to, and checked against, the pinned corrected weighted note. Its support-only consequence is reproduced in the frozen construction proof.

Let B be symmetric over F2 on a,b,c,d. If abcd, abdc, and cdab are successful pressing words, then at least one of bacd, acbd, cdba, or dcab is successful.

Here is an independent verification of the proof. If bacd or acbd is already successful, the conclusion holds. Otherwise success of abcd gives the unique unit upper triangular factor B=U^T U in that order. Write its strict-upper entries as p,q,r in row a, s,t in row b, and u in row c. In a successful order, exchanging adjacent pivots succeeds exactly when the corresponding current off-diagonal, equivalently the relevant strict-upper factor entry, is zero. The stated two failures and abdc success therefore force p=s=1 and u=0.

The initial diagonal at c is 1+q+s=q. Since cdab starts with a legal c, q=1. The successful prefix c,d,a has nonsingular principal matrix B[{a,c,d}], with determinant one. Because det B=1, the cofactor identity gives its determinant as (B^-1)_bb. Row b of U^-1 is (0,1,1,t), and its F2 self-product is t. Hence t=1. Only r remains free.

The resulting two matrices are exactly

B_0 = [[1,1,1,0],[1,0,0,1],[1,0,1,1],[0,1,1,0]],
B_1 = [[1,1,1,1],[1,0,0,0],[1,0,1,0],[1,0,0,1]].

Direct pressing yields the complete languages

- B_0: {abcd,abdc,cdab,cdba};
- B_1: {abcd,abdc,cdab,dcab}.

These also confirm the stronger classification in the corrected weighted note. No assertion that every nonsingular principal subset is reachable was used.

For a fixed successful outside prefix and suffix, eliminate the prefix first. Local pivot legality on these four labels depends only on their principal residual. After all four labels have been pressed, the remaining residual is the same Schur complement for every successful local order. Thus any locally forced alternative has the same successful suffix. This is the exact substitution argument needed below.

For T=4, three target words 12345,12435,34125 give the local successes abcd,abdc,cdab on labels (1,2,3,4), with common suffix 5. The absent words 21345 and 13245 imply the corresponding local failures: if either local order were successful, the unchanged final residual would allow suffix 5. The local theorem forces 34215 or 43125, both absent from the exact target. Hence no symmetric binary matrix realizes that four-word language.

For every T>=5, the full target subfamily starting with 12 is exactly 12 followed by the shifted previous family. In any purported realizing matrix, prefix 12 is legal because the identity is successful. Every complete successful residual word after that prefix extends to a full successful word, and conversely every full word starting with 12 supplies such a residual word. Therefore the residual would realize exactly the previous family. Iterating reaches the impossible T=4 target. This proves nonrealizability for all constructed T>=4; interactions with eliminated labels do not invalidate the residual argument.

As a boundary check, the T=3 seed is actually realizable by [[1,0,1],[0,1,0],[1,0,0]], whose complete successful language is exactly {123,132,213}. This extra audit check does not extend nonrealizability below T=4.

## 7. Separate computational tests

The independent verifier retained with the accepted evidence, and omitted from this prose-only edition, imports no producer code. It uses a closed-form family constructor and rank-by-rank propagation through prefix states, rather than the producer's recursive constructor and path DFS. All checks use explicit exceptions, so Python optimization cannot remove validation.

Successful independent checks recorded in the original retained independent results, whose identity and aggregate counts are given in VERIFICATION.json:

1. For every T=3,...,48, corresponding to n=3,...,93, exact language equality, cardinality, state and edge counts, pair counts, inversion disjointness, identity membership, recurrence, and every cross-type prefix edge. At T=48: 2,211 states, 2,257 edges, 4,142 variable pairs, and 136 fixed pairs.
2. Direct scans of all 6, 120, 5,040, and 362,880 permutations in dimensions 3,5,7,9.
3. All identity-containing inversion-disjoint seed subfamilies in dimensions 3 and 4: 9 and 92 total candidates, of which 5 and 20 are prefix-complete. Every closed seed passes the extension lemma. These finite checks supplement, rather than replace, the general proof.
4. Every identity-containing subfamily of each constructed T=3,...,10 example, plus the negative arbitrary-subfamily example above.
5. All 1,024 symmetric four-label binary matrices using direct rank-one pressing. Six satisfy the three positive local hypotheses; all satisfy support forcing. Exactly two satisfy the additional two negative hypotheses, and their matrices and complete languages agree with the proof.
6. All 32,768 symmetric five-label binary matrices. Exactly 1,024 admit the identity and therefore need complete-language comparison; none realizes the T=4 target. All 32 matrices satisfying the relevant positive and negative fixed-suffix tests supply one of the two forced alternatives. Matrices failing the identity cannot realize a language containing it, so the filter does not omit any potential target realization.
7. Negative controls confirm the n=2 extra path, the nonclosed identity-deleted example, and an intentional validator failure.

The same independent script was run under normal Python, -O, and -OO with byte-identical output. The producer's own verifiers use assertions; equal -O/-OO producer outputs alone would not certify that those assertions executed. That limitation does not affect acceptance, which rests on the written proof and independent optimization-safe tests above.

## 8. Scope, integrity, and stopping point

This audit establishes that prefix completeness plus pairwise-disjoint inversion sets admits arbitrary cardinality, even when the majority identity is included. Consequently those hypotheses alone cannot rule out exactly five or six words or imply a finite cardinality bound.

It does not classify every small-cardinality pressing language, establish a balanced pair for every pressing family, prove a universal weighted-context coverage bound, establish minimal dimensions for every cardinality, or supply a pressing counterexample. The constructed countermodels themselves are excluded from pressing realization by the independent argument above.

The original sealed manifest contains every original audit member except the manifest itself. An original external seal pins that manifest, and an original external receipt records fresh normal/-O/-OO verification plus mutation controls. Mutation controls run only on copies and test altered input bytes, missing files, altered results, and extra unmanifested files. No original input or sealed packet member is edited by these controls. These are records of the original audit; the present public edition has a separate closed MANIFEST.json and separate preservation inventory.
