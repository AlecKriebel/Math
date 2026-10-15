# A cardinality-doubling wrapper and the four-to-six-word obstruction

Problem 3100047 / row 1747. Authored research, 12 October 2026 UTC.

## Result and boundary

This report does **not** settle balance for all pressing matrices with four, five, or six successful permutations. It proves:

1. Every even-order full-rank pressable symmetric matrix M has an explicit four-vertex extension W(M) whose complete successful language consists of exactly two copies of the language of M, with two side pairs in opposite orders. Thus |Sigma(W(M))|=2|Sigma(M)|. The entire variable-order graph of W(M) is connected, and several comparisons have probability exactly 1/2.
2. There are variable-order-connected matrices of arbitrarily large order having exactly four successful words. The same holds with exactly six words. Consequently, even in these fixed-cardinality cases, no bound on variable-component size can depend only on word count. Thus a reduction based only on word count and variable-component size cannot apply to all matrices. A dimension bound restricted to hypothetical unbalanced families remains possible; these balanced examples do not obstruct it.
3. A hypothetical unbalanced family of four to six words has pairwise disjoint inversion sets relative to its transitive majority order; at most one nonsingleton instructional class, of size two or three; and no reachable/completable prefix state with both at least two prefixes and at least two suffixes. Non-minimum first-letter branches and non-maximum last-letter branches are singleton branches.

The first two statements are actual-matrix theorems. Their examples are explicitly balanced and are obstructions only to a proposed dimension bound, not counterexamples to balance. Nothing here bounds a quotient obtained by contracting common ordered blocks, or resolves the five-word case.

All matrices are symmetric over F2. A press at v with current diagonal 1 adds the outer product of its current column to the current matrix, clearing row and column v. A successful word is a full permutation completing this process. All counts and pair probabilities are uniform over the complete successful-word set.

## 1. A forced-prefix operation

For any full-rank pressable M on C, put c=diag(M), as a column vector, and define

P(M) = [[1, c^T], [c, M+cc^T]],

where the new label p comes first. The only loop of P(M) is at p: every old diagonal is M_xx+c_x^2=c_x+c_x=0. Its first press is therefore forced and leaves precisely M. Consequently

Sigma(P(M)) = {p sigma : sigma in Sigma(M)}.

The matrix is nonsingular, either by Schur complement or by its full successful word. Iteration adds any prescribed number of fixed first letters without changing word count. Two iterations preserve the parity of the order.

## 2. An alternating rank-one decomposition

Suppose M has even order r and is nonsingular. Put c=diag(M) and H=M+cc^T. Then H is alternating, because its diagonal is zero, and H is nonsingular.

For the latter assertion, M^{-1} is symmetric, and over F2

c^T M^{-1} c = sum_i c_i (M^{-1})_ii
              = trace(M M^{-1})
              = r mod 2 = 0.

The first equality cancels off-diagonal terms and uses c_i^2=c_i. In the second equality the off-diagonal terms in the trace also cancel in symmetric pairs. The determinant lemma therefore gives

det(H) = det(M) (1+c^T M^{-1}c) = 1.

The parity is essential: for odd nonsingular M the same determinant calculation gives det(H)=0.

## 3. The four-vertex doubling wrapper

Add distinct labels a,a',b,b' outside C. Define W(M) by:

- Its principal matrix on C is H=M+cc^T.
- The only loops outside C are at a and b.
- The only edges among the four outside labels are ab, aa', and bb'.
- Both a' and b' are coupled to C by c.
- The vertices a and b have no edges to C.

Thus, in the order (a,a',b,b',C), the matrix is

[[1,1,1,0,0],
 [1,0,0,0,c^T],
 [1,0,1,1,0],
 [0,0,1,0,c^T],
 [0,c,0,c,H]],

where zeros in the last column or row denote the corresponding zero vectors.

### Theorem

If M has even positive order and at least one successful full word, then

Sigma(W(M)) = {aa' sigma bb' : sigma in Sigma(M)}
               union {bb' sigma aa' : sigma in Sigma(M)}.      (1)

The two sets are disjoint, W(M) is nonsingular, and its successful-word count is twice that of M.

### Proof: first two letters

Because H is alternating, the only initial black vertices are a and b. By symmetry it suffices to consider first press a.

Pressing a makes a' black and b white, and creates edge a'b. All other unpressed diagonals are zero. Therefore a' is the uniquely legal second press.

After pressing a', the principal residual on C is H+cc^T=M. Both remaining outside vertices b,b' are coupled to C by c, and their principal block is

K_0 = [[1,1],[1,0]].

The only legal outside first choice at this point is b. We must rule out choosing it, or a later legal outside choice, before all of C has been pressed.

### Proof: invariant during central presses

After any k legal presses confined to C, write D for the remaining central matrix, d for both remaining central-to-outside columns, and q=k mod 2. The exact invariant is

diag(D)=d,
K_q = [[1+q,1+q],[1+q,q]].                                (2)

For k=0 this is diag(M)=c and the displayed K_0. If v is a legal central press, its diagonal is d_v=1. With z the current central column at v, the update changes D to D+zz^T, and both cross-columns d to d+z. Their equality to the central diagonal is preserved. The outside column at v has both entries 1, so all four entries of K_q toggle, giving K_(q+1). Clearing v completes the induction.

This invariant holds for every legal central prefix, including a prefix that ultimately has no completion. It does not identify a nonsingular or nonalternating residual with a pressable one.

### Proof: every early outside press is fatal

Suppose at least one central vertex remains.

If q=0, the sole legal outside vertex is b. Pressing b changes the central matrix to D+dd^T, which is alternating by (2). It makes b' black, and the new cross-column at b' is d+d=0. Thus the remaining graph is the disjoint union of an isolated black b' and a nonempty alternating central matrix. The only possible next press is b'; after it, the central matrix is still nonempty and entirely white. Completion is impossible.

If q=1, the sole legal outside vertex is b'. Its edge to b is zero. Pressing b' again changes the central matrix to the alternating matrix D+dd^T, while b stays white. The entire remaining matrix has zero diagonal, so there is no legal next press at all. Completion is impossible.

These arguments account for the remaining outside vertex explicitly; they do not merely stop when the central residual first becomes alternating.

Therefore every successful full word beginning aa' must press all of C before touching b or b'. The allowed central orders are exactly Sigma(M): central pivots and updates are those in the principal residual M, unaffected by unpressed outside coordinates.

After all r central vertices are pressed, q=0 because r is even. The remaining matrix is K_0, whose unique successful order is bb'. Every word aa' sigma bb' with sigma in Sigma(M) is consequently successful, and no other word beginning with a is successful. Symmetry gives precisely the other half of (1).

A full successful word makes all pivots 1, so W(M) is nonsingular. The halves in (1) have different first letters and cannot overlap. This proves the theorem.

### Pair probabilities and connected variable graph

Let Z=|Sigma(M)|. Every word in one half of (1) puts the a-pair before all of C and the b-pair; the other half reverses those block placements. Hence each of the following comparisons has probability exactly 1/2:

- any x in {a,a'} against any y in {b,b'};
- any central x against any of the four outside labels.

The orders a before a' and b before b' are fixed. For x,y both central, each central word appears twice, so p_W(x,y)=p_M(x,y).

In particular, the variable-order graph contains all edges between C and the four outside labels and all edges between the two side pairs. It is connected. This conclusion concerns the whole graph, even when M contains arbitrarily much forced-prefix padding.

## 4. Fixed-cardinality unbounded cores

### Exactly four words

Take M_2=I_2. It has exactly two successful orders. For k>=0 let

N_k = P^(2k)(M_2),    A_k=W(N_k).

Then A_k has order 6+2k, exactly four successful words, and connected variable-order graph. Every displayed half contributes two words, so the side-pair comparisons split 2 against 2.

This disproves any proposed bound of the form |C|<=f(4) for a variable-order component C of a four-word pressing family.

### Exactly six words

On labels 0,1,2 let

M_3 = [[1,1,0], [1,0,0], [0,0,1]].

The component on 0,1 has forced order 01 and the isolated black label 2 can be inserted in any of three gaps. Thus

Sigma(M_3)={012,021,201}.

For k>=0 let

N'_k=P^(2k+1)(M_3),    B_k=W(N'_k).

Now N'_k has even order 4+2k. The matrix B_k has order 8+2k, exactly six successful words, and connected variable-order graph. Its side-pair comparisons split 3 against 3.

Thus |C|<=f(6) is likewise impossible.

The forced letters of N_k or N'_k cannot be removed from the final matrix merely as separate fixed-order components: every one is variable with every outside label in the wrapper. A contraction theorem for always-consecutive ordered subwords could conceivably remove them; no such theorem is asserted here.

## 5. Necessary form of a four-to-six-word counterexample

Let L=Sigma(A), where A is full-rank and pressable, and assume 4<=T=|L|<=6. Suppose no pair has probability in [1/3,2/3].

### 5.1 Disjoint inversions

Each unordered pair has minority count at most one. Orient each pair in its strict majority direction. A directed triangle would require every word to violate at least one of its three edges, while the total number of violations is at most three. This is impossible because T>=4. A tournament without directed triangles is a transitive total order; label it 1,...,n.

Relative to this order, every pair can be inverted in at most one word. Consequently the inversion sets of different words are pairwise disjoint. The majority word itself need not be assumed successful.

### 5.2 A star of adjacent swaps

If two successful words differ by one adjacent swap, their inversion sets differ in exactly that one pair. Every other inversion would be shared by both words, which is impossible. Thus one endpoint is the majority word, and the other has exactly the single inversion supplied by that adjacent swap.

All successful adjacent-swap edges therefore form a star centered at the majority word. If two available swaps occur at disjoint adjacent-position pairs, both can be performed, in either order, to obtain another successful word with both inversions. One way to see this is that successful adjacent commutations preserve the instructional root, whose linear extensions are closed under commuting two disjoint adjacent swaps. Equivalently, the two independent local swaps do not change each other's prefix set or two-position residual test. The resulting word repeats each of the two minority inversions, a contradiction.

Hence available swap positions are pairwise overlapping. At most two adjacent-position pairs can be pairwise overlapping; when there are two, their positions are consecutive. The adjacent-swap component of the majority word therefore has size at most three, and every other component is a singleton. Using the exact instructional-class/adjacent-component identity, there is at most one nonsingleton instructional class, of size two or three.

### 5.3 No state can have multiplicity on both sides

For each subset S define F(S) to be the number of legal full-prefix orders ending at S, and G(S) to be the number of successful suffix orders after eliminating S. Set either count to zero when the relevant prefix or suffix does not exist; no accessibility assertion is made from nonsingularity alone.

If F(S)>=2 and G(S)>=2, two distinct prefixes differ in the order of some pair x,y in S. Schur-complement state independence lets each prefix extend by every suffix. There are therefore at least G(S)>=2 full words in each direction of x,y. Their counts lie between 2 and T-2, hence the pair is balanced for T in {4,5,6}, a contradiction.

Thus every reachable/completable state satisfies

min(F(S),G(S))=1.                                         (3)

In particular, two paths that diverge and later meet must have identical remaining suffixes after their first reunion. A merge cannot be followed by a genuine branch.

### 5.4 First and last branches

For any label x other than majority-minimum 1, every word beginning with x reverses (1,x). Such a first-letter branch has at most one word. Dually, every last-letter branch other than the majority-maximum n has at most one word. These are necessary conditions, not extension-existence claims about a looped first choice.

## 6. Verification boundary

The authored verifier retained in the accepted audit evidence, and not distributed in this prose-only edition, uses direct rank-one pressing, independently enumerating every legal first choice, including fatal branches. It checks the exact complete language, nonsingularity, pair counts, and variable connectivity of the stated fixed-cardinality families for k=0,...,16. It also checks the wrapper on all 64 unit-upper-triangular roots of order four and on 32 deterministic roots of order six, against separately enumerated central languages. Odd-order controls confirm the parity boundary.

A separate diagnostic enumerates abstract permutation families, not matrices: all pairwise-inversion-disjoint cliques of sizes four through six among permutations of n labels, for n=2,...,6, then checks whether every complete singleton-addition path of their union prefix system is already listed. Its precise counts are retained in the accepted audit evidence; aggregate counts are summarized in the separate full audit and VERIFICATION.json. It is not an ambient pressing census, does not replace matrix compatibility, and is not used in any theorem above.

During the original research, no prior freeze was modified and no repository or publication action was taken. General balance for all four-, five-, or six-word matrices remains open in this work. The new actual-matrix obstruction is to cardinality-only variable-component bounds, and the exact remaining counterexample restrictions are Sections 5.1–5.4.
