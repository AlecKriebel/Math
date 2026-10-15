# Exact pressing-balance verification through eight vertices

Date: 12 October 2026 UTC. Target: row 1747, 3100047 / AMR-030-0047.

## Result and exact scope

For every symmetric matrix A over F2 on at most eight vertices that has more than one full-length successful pressing sequence, there are distinct vertices i,j such that

T <= 3 P(i,j) <= 2 T,

where T is the number of full-length successful sequences and P(i,j) counts those placing i before j. Thus the full-rank pressing-balance assertion has no counterexample on at most eight vertices. This is a finite, exhaustive computational result, not a proof for arbitrary size or a claim about the best previously published search bound.

Here a legal press at i requires A_ii=1 and replaces A by A+(A e_i)(A e_i)^T. Success means reaching the zero matrix. The tested condition requires full-length sequences, which are permutations of all n vertices. A legal press drops rank by one: write A in pivot-first form [1 b^T; b C], congruent to diag(1,C+b b^T), while its pressed matrix is diag(0,C+b b^T). Consequently full-length success implies nonsingularity, and all successful sequences of a nonsingular matrix have length n. Nonsingular matrices with no successful sequence are excluded because they have no uniform successful-sequence distribution. Singular omitted-vertex conventions are not tested or used as refutations.

The author-maintained [Cooper problem list](https://people.math.sc.edu/cooper/combprob.html) states the probability question without resolving omitted-vertex conventions. Its archived statement and the earlier scope notes were inspected locally. [Cooper–Davis, arXiv:1502.07450v5](https://arxiv.org/abs/1502.07450v5), Proposition 3 and Theorem 8, give the leading-principal-minor characterization; Proposition 9 gives unique successful coloring for a fixed simple graph and permutation. These actual v5 statements were inspected, not the withdrawn stronger claims from older versions. The arguments and both computational implementations below are independently written. No source-author software was executed, and no public novelty or publication-status claim is made.

## Exact totals

For n=6 every one of the 2,097,152 labelled symmetric matrices was tested directly by the subset method, and an independent direct-press computation agreed.

For n=7,8 all underlying simple-graph isomorphism representatives and every diagonal coloring were tested. Orbit-weighted totals are literal labelled-matrix totals, not counts of colored isomorphism classes.

| n | Underlying representatives | Representative/coloring cases | Labelled matrices covered | Full-length pressable | Nonunique full-length | Uniquely full-length pressable |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 156 | 9,984 | 2,097,152 | 867,654 | 861,174 | 6,480 |
| 7 | 1,044 | 133,632 | 268,435,456 | 112,476,490 | 112,385,770 | 90,720 |
| 8 | 12,346 | 3,160,576 | 68,719,476,736 | 28,758,575,496 | 28,757,486,856 | 1,088,640 |

Both exact algorithms found zero counterexamples. At n=8 the direct algorithm processes 12,346*8! = 497,790,720 representative/permutation cases. Their weighted successful-sequence total is 8!*2^28 = 10,823,317,585,920. The corresponding n=6 and n=7 totals are 23,592,960 and 10,569,646,080.

Separate exhaustive labelled DP and direct-press runs were also completed for every order n=1,...,5. The n=5 labelled DP replay agrees with the earlier full enumeration: 13,498 full-length pressable, of which 12,778 nonunique. The independent validation script additionally compares all exact pair counts, all principal determinants and direct pressing for 100 fixed-seed matrices at each n=1,...,8. These sampled cross-checks are validation of the algorithms, not the source of exhaustive n=6,...,8 coverage.

## 1. Determinant recurrence

For S a vertex subset set d(S)=det A[S] in F2 and d(empty)=1. Fix i in S and put R=S\{i}. Then

d(S) = A_ii d(R) + sum over j in R of A_ij d(R\{j}) in F2.

Proof: expand the determinant as a sum over permutations. Signs disappear in characteristic two. Inverting a permutation leaves its monomial unchanged because A is symmetric. Every non-involution therefore cancels with its distinct inverse. The remaining permutations have only fixed points and transpositions. A transposition i,j contributes A_ij A_ji=A_ij^2=A_ij. Partition the involutions by whether i is fixed or transposed with j. This proves the formula. In particular, this is not an invalid Laplace-expansion simplification: symmetry, characteristic two, and binary entries are each used.

## 2. Successful words as paths in a subset DAG

A permutation v_1,...,v_n is successful exactly when d({v_1,...,v_k})=1 for every k.

Proof: elimination at a legal diagonal-one pivot gives the Schur complement C+b b^T. Applying determinant elimination to every successive principal prefix shows that a legal sequence has every prefix determinant equal to the product of its pivot values, hence one. Conversely, if all prefix determinants are one, induction gives pivot value det(prefix k)/det(prefix k-1)=1, so every press is legal. After n presses every row and column is zero. This also proves that success after a feasible prefix depends only on its vertex set: its residual matrix on the complement is the Schur complement A[V\S]+A[V\S,S] A[S]^{-1} A[S,V\S], independent of prefix order.

Let F(S) count feasible words whose vertex set is S. Then

F(empty)=1; F(S)=d(S) sum over i in S of F(S\{i}).

For a full-length pressable matrix define G(V)=1 and

G(S)=d(S) sum over i outside S of G(S union {i}).

Thus T=F(V)=G(empty). These count paths in the directed graph of determinant-one subsets, with edges adding one vertex. Subsets that have determinant one but are unreachable from the empty set have F=0 and cause no spurious sequences.

For distinct i,j the exact precedence count is

P(i,j)=sum over S contained in V\{i,j} of F(S) G(S union {i}).

Indeed, every word with i before j has a unique set S of vertices before i. Its prefix and suffix have F(S) and G(S union {i}) choices. Conversely each such pair concatenates to exactly one successful word. This proves the product formula and the check P(i,j)+P(j,i)=T. The implementation performs only integer tests T<=3P<=2T, including both endpoints. It does not estimate probabilities or use floating-point decisions.

## 3. Independent direct-press enumeration

Fix the ordinary off-diagonal edges and a permutation. There is exactly one initial diagonal coloring for which that permutation is a successful full-length sequence.

Here is a constructive proof. Begin with zero original diagonal. When the next chosen vertex i has current diagonal zero, toggle that diagonal to one and record that the original diagonal at i must be one; otherwise its original diagonal stays zero. Then perform the actual rank-one press. Altering an original diagonal at an as-yet unpressed vertex changes only that current diagonal and cannot change any earlier pivot column. Inductively, earlier press legality and states off that diagonal are unaffected. The forced current pivot is therefore legal. After all n presses the matrix is zero. At each step its original diagonal value is uniquely forced by the required current pivot one, proving uniqueness.

The separately retained independent direct-press program enumerates every permutation, performs those literal rank-one presses, and increments a counter for the forced original coloring and every ordered pair in that permutation. It does not compute principal minors or use subset DP. Comparing all colorings then tests every full-length pressable matrix for that underlying graph. Agreement of the two implementations includes full-length counts, unique/nonunique counts, total sequence counts, and zero failures of the exact inclusive balance test. The Python validator also compares the complete pair-count arrays on its stated sample.

## 4. Canonical generation and completeness

An n-vertex uncolored graph is encoded by appending adjacency bits between each newly ordered vertex k and its already ordered vertices 0,...,k-1. The degree sequence is sorted first. Among all vertex orders respecting that sorted degree sequence, the minimum adjacency code is its canonical code.

Two graphs are isomorphic if and only if they have the same canonical code. Any isomorphism preserves vertex degrees and transfers exactly the admissible orderings, proving one direction. Equal codes explicitly give an isomorphism, proving the other. The program enumerates all permutations within equal-degree classes. It prunes an unfinished ordering only when its already determined binary prefix exceeds the corresponding prefix of the best complete code; every extension is then larger, so no minimum is lost. No probabilistic graph hash is used for equality: unordered_set stores and compares the entire exact integer code.

Starting with the one-vertex graph, take every canonical representative on n-1 vertices and add a new vertex with each of its 2^(n-1) possible neighborhoods. Canonicalize and deduplicate the results. This is complete by induction: delete any vertex of any n-vertex graph, identify the remaining graph with its n-1 representative, and transfer the deleted vertex's neighborhood. The original graph occurs among these augmentations. This argument is independent of any published graph-count table.

The program independently canonicalizes every labelled simple graph through n=6 and verifies exact set equality with the recursively generated set. It returns 1,2,4,11,34,156,1044,12346 representatives at n=1,...,8. These numerical counts are internal checks, not the proof of completeness.

For an additional check it counts the degree-compatible permutations achieving the canonical code. Their number is |Aut(H)|: after fixing one isomorphism to the canonical graph, all other such isomorphisms correspond bijectively to automorphisms. Thus each uncolored representative has n!/|Aut(H)| distinct labelled copies. The sums of these orbit sizes are exactly 2^(n(n-1)/2) for every n<=8.

Every one of the 2^n diagonal colorings is tested on each representative. Relabeling conjugates A by a permutation matrix and conjugates the rank-one pressing update, so it gives a bijection between successful sequences and preserves their precedence counts after renaming vertices. Consequently testing every representative/coloring case covers every labelled symmetric matrix. For a fixed labelled underlying graph, an isomorphism from its representative bijects the complete set of colorings; therefore multiplying the aggregate counts over all representative colorings by that representative's uncolored orbit size gives the exact labelled totals in the table. No claim that the colored cases themselves are pairwise nonisomorphic is needed.

## 5. Arithmetic and reproducibility

All tested dimensions are at most eight. Each per-matrix word or precedence count is at most 8!=40320. Each DP product in a precedence sum counts an actual subset of successful words and is therefore at most 40320. Weighted aggregate sequence totals are at most 10,823,317,585,920. These, all endpoint multiplications by three, graph codes (at most 28 bits), and weighted labelled-matrix totals fit the unsigned 64-bit or explicitly smaller types used. The scanner's optional generic larger-dimension modes are not part of this exhaustive result.

Historical execution method and public reproducibility boundary:

1. The subset scanner, independent direct-press enumerator, and canonical graph generator were compiled with g++ -O3 -std=c++17. The frozen build metadata records g++ (Debian 14.2.0-19) 14.2.0 with -O3 -std=c++17 -Wall -Wextra, and Python 3.12.14.
2. The graph generator was run through maximum order 8. It emitted every graph representative and automorphism count, checked all labelled simple graphs n<=6, and reported orbit totals.
3. The subset scanner was run over all labelled matrices at each order 1 through 6, and over every representative and diagonal coloring at orders 6, 7 and 8.
4. The independent direct-press enumerator was run at each order 1 through 6 without a representative list, and at orders 7 and 8 with the corresponding complete graph representative lists.
5. The separate Python validator tested every principal determinant against independent F2 Gaussian elimination and compared all exact precedence arrays with a direct recursive rank-one implementation and the compiled subset scanner. Its seed was 1747. It also compared saved exhaustive aggregates. These were historical checks against separately retained programs and records, not commands executable from this edition.

VERIFICATION.json preserves the aggregate totals, check scopes, build metadata and byte/hash identities of the retained computational inputs. ORIGINAL_INPUT_PINS.json and EDITORIAL_MAP.json identify the original frozen reports and their public editions. The programs, raw graph representatives, full per-case records and certificates are not distributed here: this public prose edition is not an executable public replay package. All mathematical methods and proofs above are included. The original computational research stage performed no repository, queue or publication action; the present document is a transparently edited public prose edition of that report.

## Remaining gap

The general full-length balance assertion for arbitrary n remains unproved. No finite search establishes it beyond its tested dimensions. This packet does not settle the singular omitted-vertex formulation, count lifetime attempts, determine priority, or establish a new published research frontier.
