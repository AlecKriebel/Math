# Exact replacement and trajectory-fiber lemmas for successful pressing

This is an independently authored structural note. It makes no novelty claim and does not settle the Bixby–Flint–Miklós connectivity conjecture at four deletions plus four insertions.

Throughout, A is a symmetric n by n matrix over F_2. A legal press at vertex v, meaning A_vv=1 in the current state, replaces the current matrix M by M+(Me_v)(Me_v)^T. A successful word reaches the zero matrix. A vertex cannot occur twice in a legal word: its first press clears its row and column permanently.

## 1. Rank and radical quotient

A legal press decreases rank by exactly one. Indeed, ordering the pressed coordinate first writes the state as

M = [[1, b^T], [b, C]],

and elementary simultaneous row/column operations give a congruence to diag(1, C+bb^T). The pressed state is diag(0, C+bb^T). Consequently every successful word has length r=rank(A).

Let E=F_2^n with B(x,y)=x^T A y. Its radical is R=ker(A), and the induced form on V=E/R is nondegenerate, of dimension r. Write x_v for the image of the coordinate vector e_v in V. Then B(x_u,x_v)=A_uv. In particular x_v=0 if and only if the original row/column of v is zero.

Fix a successful word S=(s_1,...,s_r). Gram–Schmidt along this word gives

f_j = x_{s_j} + sum_{i<j} B(x_{s_j},f_i) f_i.

The legality of the j-th press says B(f_j,f_j)=1. Inductively the f_j are mutually orthogonal; since their number is dim(V), they form an orthonormal basis of V. The form is therefore isometric to the standard dot product on F_2^r. This conclusion comes from the successful coordinate word, not merely from abstract nonalternation of the form.

Set c_j(v)=B(x_v,f_j), and regard c_j as a column indexed by every original vertex. The exact state after the first k letters of S is

M_k = sum_{j>k} c_j c_j^T.                                    (1)

For a direct verification, A=sum_{j=1}^r c_j c_j^T by expansion in the orthonormal basis. Also c_j(s_i)=0 for j>i and c_i(s_i)=1, so M_{i-1}e_{s_i}=c_i; its press removes exactly the summand c_i c_i^T. Thus (1) is an equality of full n by n matrices, including omitted coordinates.

Equivalently, if pi_k denotes orthogonal projection onto span(f_{k+1},...,f_r), then (M_k)_uv=B(pi_k x_u,pi_k x_v).

## 2. Last-support replacement lemma

**Lemma.** For any vertex v with a nonzero original row, define

j = max{i : c_i(v)=1}.

Replacing s_j by v, in the same position of S, gives a successful word. If v was omitted from S, this is one deletion and one insertion. If v already belongs to S, the replacement is the identity.

**Proof.** The index j exists because the f_i form a basis and x_v is nonzero. After the first j−1 presses, the residual vectors of both v and s_j equal f_j. The original x_v can differ from f_j by any earlier f_i directions; any representative in E can additionally differ by a radical vector. All those differences disappear under the projection defining the residual state. More concretely, from (1),

M_{j-1} e_v = c_j = M_{j-1} e_{s_j},

and (M_{j-1})_vv=c_j(v)=1. Therefore pressing v is legal and subtracts exactly the same rank-one matrix as pressing s_j. The entire resulting state is M_j, not just a congruent matrix or a restriction to a chosen coordinate subset. In particular the row and column of the replaced s_j are cleared too. Every subsequent letter of S has exactly its original state and remains legal, ending in zero.

If v=s_i, triangularity gives max{k:c_k(v)=1}=i, so j=i. Hence the construction does not introduce a repeated letter. QED.

## 3. Complete Cartesian description of a trajectory fiber

For the fixed ordered matrix trajectory M_0,...,M_r, define disjoint layers

L_j = {v : c_j(v)=1 and c_k(v)=0 for every k>j}.

The layers are nonempty, contain s_j respectively, and partition all vertices with nonzero original row.

**Proposition.** The successful words giving this exact matrix trajectory are precisely

L_1 × ... × L_r.

In particular every combination (v_1,...,v_r) with v_j in L_j is a successful word, and all these letters are distinct. Two such words are connected by changing one coordinate at a time, with every step having longest-common-subsequence length at least r−1.

**Proof.** At step j, every v_j in L_j has M_{j-1}e_{v_j}=c_j and is black. It therefore gives state M_j. Disjointness of the layers prevents repeated vertices. Conversely, if a legal letter v gives the transition from M_{j-1} to M_j, then its update column d=M_{j-1}e_v satisfies dd^T=c_jc_j^T. Equality of diagonals over F_2 gives d=c_j. The vectors c_1,...,c_r are linearly independent: their entries on rows s_1,...,s_r form a unit lower-triangular matrix. Expanding d=sum_{k≥j}c_k(v)c_k therefore forces c_j(v)=1 and c_k(v)=0 for k>j, exactly v in L_j. QED.

This proposition is stronger than a statement about equal terminal Schur complements: every intermediate full matrix is identical. It licenses coordinate substitutions but does not license arbitrary changes of coordinate subsets under congruence.

## 4. A universal diameter-two bound, and the original bound in rank at most five

**Corollary.** For r≥2, join successful words when they have at least one common letter. This graph has diameter at most two, independently of n.

**Proof.** If two words S,T share a letter, they are adjacent. Otherwise choose any v in T. It has a nonzero original row because a zero row remains zero under every press and can never be pressed legally. The replacement lemma gives a successful S' differing from S in one position and containing v. S and S' share r−1≥1 letters, and S' and T share v. QED.


**Corollary (rank at most five).** If rank(A)≤5 and A has a successful word, the graph on successful words joining S,T when LCS(S,T)≥r−4 is connected. For r≤4 it is complete; for r=5 it has diameter at most two. This holds for arbitrary ambient vertex count n, including rank-deficient matrices and words omitting different vertices.

**Proof.** For r≤4 the required LCS lower bound is nonpositive. For r=5 it is one, so the preceding r≥2 result applies. For rank zero there is just the empty successful word. QED.

The general diameter-two argument uses up to r−1 deletions plus r−1 insertions in its second edge. It therefore proves no fixed-four bound beyond rank five.

## Scope and source normalization

Sections 1–4 above are the complete accepted excerpt of the original structural note. They apply to every symmetric binary matrix admitting a successful word, including rank-deficient matrices and arbitrary ambient vertex counts. General inter-fiber connectivity at the fixed-four deletion and insertion bound is not proved by those arguments. The separate conditional theorem and exact inter-fiber criterion appear in [INTER_FIBER_LEMMAS.md](INTER_FIBER_LEMMAS.md).

For equal-length words of length r, total insertion/deletion distance is 2(r−LCS). A longest common subsequence can be retained while deleting and reinserting every other letter, attaining that distance; any edit script can retain only a common subsequence, giving the matching lower bound. Thus the original Bixby–Flint–Miklós threshold LCS≥r−4 is four deletions and four insertions, a combined budget of eight. It is not a combined four-edit threshold.

All proofs in Sections 1–4 are elementary and reproduced in full above. The normalization is from Conjecture 6 on printed page 47 of Eliot Bixby, Toby Flint, and István Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9:1 (2016), 41–56, DOI 10.2140/involve.2016.9.41. [Publisher PDF](https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf). No external mathematical theorem is needed. See [SOURCE_METADATA.json](SOURCE_METADATA.json) for inspection limits and byte/hash metadata.
