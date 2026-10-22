# Independent audit: exact pressing replacements and trajectory fibers

## Verdict and exact scope

**ACCEPT Sections 1–4 of the frozen structural note.** They prove the last-support single-letter replacement lemma, the complete Cartesian-product description of a fixed full-matrix trajectory fiber, and connectivity under the original four-deletion/four-insertion bound whenever the binary rank is at most five. The proof covers arbitrary ambient vertex counts and rank-deficient matrices. No substantive mathematical correction is required in those sections.

The reviewed original structural input was **7,461 bytes**, SHA-256 **834a488e71a321d82f6f2bac0eb029bc8a03d56cee63e61a6a7c5e0fe8952aa8**. Its Sections 1–4 are reproduced without alteration in the accompanying prepared structural note. This hash identifies the complete reviewed original, not the shorter publication edition. The inter-fiber claims receive their separate audit in INTER_FIBER_AUDIT.md. EDITORIAL_MAP.json records the edition mapping.

The reviewed structural note's Section 5 is omitted from the prepared proof. This acceptance is confined to Sections 1–4 and the precise residual stated below.

There is no novelty claim. This is a mathematical correctness and scope audit, not a literature-completeness determination. No conclusion here proves or refutes the full pressing-game connectivity conjecture in arbitrary rank.

## Target normalization and source check

The published source is Eliot Bixby, Toby Flint, and István Miklós, *Proving the Pressing Game Conjecture on Linear Graphs*, Involve 9 (2016), 41–56, DOI 10.2140/involve.2016.9.41. Printed page 47, Conjecture 6, uses adjacency when the longest common subsequence has length at least the common successful-word length minus four. The following explanation permits at most four deletions and at most four insertions. Thus, for successful words of length r, the target is

    LCS(S,T) >= r-4,

or total insertion/deletion distance at most eight. This is not a total-four-edit target. The source's successful-versus-valid distinction was checked on the same page. These facts were read from the local pinned published PDF/text and independently confirmed by opening the publisher's PDF through the web tool on 2026-10-11.

Publisher URL: https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf

The PDF is 886,918 bytes, SHA-256 ba3882a3bdd2688c411630a42cfa78348f0c4d8b0043124e5a0ea7b030e2b3ba. Public input hashes and inspection details are in SOURCE_METADATA.json and EDITORIAL_MAP.json. Source-author code was neither read nor executed. No outside theorem is needed for the accepted algebra below.

## Independent proof reconstruction

All vector spaces and matrices in this section are over F_2. Let A be a symmetric n by n matrix with at least one successful pressing word. A legal press of v in state M requires M_vv=1 and sends M to M+(Me_v)(Me_v)^T. Pressed coordinates remain present; all state comparisons below concern the entire n by n matrix.

### 1. Rank, zero coordinates, and the quotient

After moving the pressed coordinate first, write a legal state as

    M = [[1, b^T], [b, C]].

Simultaneous elementary row and column operations identify its rank with 1+rank(C+bb^T). Its pressed state is exactly diag(0,C+bb^T). Thus every legal press decreases rank by one, and every successful word has length r=rank(A).

The pressed row and column become zero. If a row is zero in a state, its corresponding entry in every update column is zero, so every later update leaves that row zero. This proves both that legal words never repeat a vertex and that a vertex with an originally zero row can never occur in any legal word.

Let E=F_2^n, B(x,y)=x^T A y, and R=ker(A). Symmetry gives the same left and right radical. If either representative changes by an element of R, the pairing does not change; hence B descends to E/R. If a class is orthogonal to all classes, its representative lies in R, so the quotient form is nondegenerate. Rank-nullity gives dim(E/R)=r. The image x_v of e_v is zero exactly when Ae_v=0, which is equivalent to the original row and column of v being zero.

This construction is valid in characteristic two, including isotropic nonzero vectors. No positive-definiteness argument or blanket assumption about nonalternating forms is used.

### 2. A noncircular Gram–Schmidt induction

Fix a successful word S=(s_1,...,s_r). Suppose f_1,...,f_{j-1} have already been constructed and are orthonormal. Set

    P_{j-1}x = x + sum_{i<j} B(x,f_i) f_i,
    f_j = P_{j-1}x_{s_j}.

The projection P_{j-1} annihilates the previously selected directions and projects onto their orthogonal complement. The induction invariant is

    (M_{j-1})_uv = B(P_{j-1}x_u, P_{j-1}x_v).

It holds initially. The legality of s_j gives B(f_j,f_j)=1. The construction makes f_j orthogonal to all previous f_i. Replacing P_{j-1} by P_j subtracts the f_j direction; because the field has characteristic two, direct bilinear expansion gives

    B(P_jx_u,P_jx_v)
      = B(P_{j-1}x_u,P_{j-1}x_v)
        + B(P_{j-1}x_u,f_j) B(P_{j-1}x_v,f_j).

The final product is exactly the rank-one pressing update. This proves the invariant and the legality/norm correspondence without assuming the later full-state formula.

The r orthonormal vectors are independent: pairing a linear relation with f_i recovers its i-th coefficient. Since the quotient dimension is r, they form a basis. Define c_j(v)=B(x_v,f_j). Expansion in this basis yields

    A = sum_{j=1}^r c_j c_j^T.

Also x_{s_i} belongs to span(f_1,...,f_i), and its f_i coefficient is one. Consequently c_j(s_i)=0 for j>i and c_i(s_i)=1. In particular, the matrix with rows indexed by s_i and columns by c_j is unit lower triangular, so c_1,...,c_r are linearly independent as vectors in F_2^n.

The exact states are therefore

    M_k = sum_{j>k} c_j c_j^T,

because at step i the full update column M_{i-1}e_{s_i} is c_i. This is equality on every original coordinate, including omitted vertices and radical-related duplicates. It is stronger than congruence or equality of a restricted Schur complement.

### 3. The replacement lemma, including both cleared vertices

For any v with nonzero original row, its quotient coordinate vector is nonzero. Its highest nonzero orthonormal coordinate

    j = max {i : c_i(v)=1}

exists. Projecting away the first j-1 directions leaves exactly f_j for both x_v and x_{s_j}. Equivalently,

    M_{j-1}e_v = c_j = M_{j-1}e_{s_j},
    (M_{j-1})_vv = 1.

So pressing v is legal and gives exactly M_j. Every later pivot sees precisely the old state and the original suffix finishes successfully.

The old and new vertices both clear: for w equal to v or s_j, the relevant column of the new state is c_j+c_j c_j(w)=0 because c_j(w)=1. Previously cleared rows stay zero. Thus there is no hidden issue involving the replaced vertex being left active.

If v=s_i already occurs in S, its triangular coordinate support has highest index i, so j=i and the operation is the identity. If v is omitted, replacing s_j by v creates no repetition. This is one deletion and one insertion, and S and its replacement share the ordered subsequence obtained by deleting position j, of length r-1.

This proves the stated insertion of any missing nonzero-row vertex. It does not prescribe an earlier position for that vertex.

### 4. The exact Cartesian fiber, including the converse

For the fixed trajectory define

    L_j = {v : c_j(v)=1 and c_k(v)=0 for all k>j}.

The sets are pairwise disjoint, nonempty, and partition the vertices with nonzero original row; s_j belongs to L_j. Every tuple in L_1 x ... x L_r consists of distinct letters. By induction, at step j its chosen letter has update column c_j in state M_{j-1}, so the tuple gives the same complete trajectory. Choices in different layers are independent.

Conversely, suppose a legal vertex v sends M_{j-1} to M_j. Set d=M_{j-1}e_v. Comparing the two transitions gives dd^T=c_jc_j^T. Taking diagonal entries gives d_i^2=c_j(i)^2; over F_2 these are d_i=c_j(i), so d=c_j. The full-state expansion gives

    d = sum_{k>=j} c_k(v)c_k.

Independence of the c_k forces coefficient one for k=j and zero for every k>j. Hence v belongs to L_j. Applying this at every step proves that no additional successful word can lie in the fiber.

The one-position replacement graph of a fiber is the Cartesian product of complete graphs on the L_j. Any two tuples can be connected by changing each differing coordinate once. Each nonidentity step has LCS at least r-1, so each fiber is connected under the original total-eight bound (indeed under total-two).

For r=0, A=0. There is exactly one successful word, the empty word; the empty Cartesian product is a singleton, and the union of the empty family of layers is the empty set of nonzero rows. These conventions correctly include n=0 and arbitrary ambient all-zero matrices.

### 5. Exact distance for the common-letter graph and rank five

Let r>=2 and join distinct successful words whenever they share at least one letter. For two disjoint words S,T, choose any v in T. Its original row is nonzero, since originally zero rows cannot ever be legally pressed. The replacement lemma produces a successful S' containing v and retaining r-1 letters of S. Since r-1>=1, both S--S' and S'--T are edges.

It follows that the graph distance between any two successful words is exactly:

* 0 if the words are identical;
* 1 if they are distinct and have a common letter;
* 2 if their letter sets are disjoint.

The last case has no direct edge by definition and has the constructed two-edge path. The hypothesis r>=2 is necessary for this common-letter graph statement: at rank one, distinct singleton words have no common-letter edges.

When r<=4, the original threshold r-4 is nonpositive, so every pair of distinct successful words is adjacent. Rank zero still has just one vertex. When r=5, the threshold is one; sharing a letter is exactly equivalent to having an LCS of length at least one. Therefore the displayed distance formula is also the exact rank-five metric of the original metagraph, and its diameter is at most two.

The bound two is sharp even for a single trajectory fiber. Take n=10 coordinate vectors

    e_1,e_2,e_3,e_4,e_5,e_1,e_2,e_3,e_4,e_5

in F_2^5, and take A as their Gram matrix. The disjoint successful words S=(1,2,3,4,5) and T=(6,7,8,9,10) have no common letter, while S'=(6,2,3,4,5) is successful. The LCS lengths for (S,S'), (S',T), and (S,T) are respectively 4,1,0. Thus their insertion/deletion distances are 2,8,10, and their original-metagraph distance is exactly two. The independent test artifact uses zero-based labels for this same example.

For arbitrary equal-length words of length r, minimum total insertion/deletion distance is 2(r-LCS). Retaining a longest common subsequence gives the upper bound, and any edit sequence can retain at most an LCS, giving the lower bound. Consequently the second edge of the general shared-letter construction requires at most r-1 deletions and r-1 insertions. At r=5 this is within four of each; at larger ranks the construction alone does not establish the conjectured fixed-four allowance.

## Independent bounded exact verification

An independent checker was authored for this audit from the matrix definition. It imports only Python standard-library modules and does not read or execute the proof author's checking code or source-author code. Its comparisons use explicit exceptions, not Python assertions, so optimization cannot silently remove tests.

The exhaustive portion covers all 33,867 symmetric binary matrices in ambient dimensions 0 through 5, including matrices with no successful word. For every successful word it checks exact legal evolution, one-unit rank drops, distinctness, exact coordinate expansion modulo the radical, all last-support replacements, and full trajectory equality. For every exact trajectory fiber it compares the full set of enumerated words with the full Cartesian product of layers. At each state it tests the transition converse against every legal vertex, including legal moves not compatible with that fixed successful suffix.

Eight additional exact Gram cases include ambient dimensions up to ten, ranks zero through six, repeated quotient coordinates, zero rows, mixed-coordinate vertices, and rank-deficient matrices. These cases cover the sharp rank-five example and rank-five words omitting different vertices. The pairwise distance checks are exhaustive for word sets of size at most thirty and otherwise use a deterministic bounded sample; they are not an exhaustive pairwise theorem proof.

Combined results:

* 33,875 matrices, of which 31,751 have successful words;
* 286,756 successful words;
* 202,317 exact trajectory fibers;
* 1,431,878 single-letter replacement checks;
* 196,888 missing-vertex insertions;
* 1,909,812 legal-column transition-converse checks;
* 3,613,585 word-pair checks, including 4,196 disjoint-pair bridge checks.

Every check passed. Aggregate counts, scope limits, and three-mode rerun metadata are in VERIFICATION.json. These finite results corroborate the independent proof; they are not used to establish any unbounded claim.

## Precise residual and publication boundary

The proved fiber description permits collapsing the original metagraph by equality of complete matrix trajectories, because each fiber is already connected. What remains unresolved by this audit is connectivity of that quotient at LCS threshold r-4 in general rank. The replacement lemma does not move an arbitrary selected vertex to a freely chosen position, does not identify different full-matrix trajectories, and does not lift unordered feasible-set exchanges to ordered successful words.

Accepted claim: original-bound connectivity for binary rank at most five, arbitrary ambient n, conditional only on existence of a successful word; complete trajectory fibers and last-support replacement for every rank.

Not accepted as a consequence of this structural audit: arbitrary-rank original-bound connectivity, a normalization refutation, any universal strict-descent property, an inter-fiber theorem, or novelty. The conditional inter-fiber results are reviewed independently in INTER_FIBER_AUDIT.md. The previous total-four normalization issue has no bearing on the correctness of the rank-at-most-five result proved here.

This prepared edition includes the complete independent mathematical reconstruction and its bounded-check description. Its editorial changes are limited to scope clarification, edition references, and removal of non-payload operational material. No executable checker, raw search output, third-party source document, or source extraction is included.
