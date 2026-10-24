# Independent adversarial audit of the finite-holonomy filter

UTC: 2026-10-24T22:28:25Z. Reviewer: internal subagent
`p21124_holonomy_adversary`, which did not author the input. Bounded review
completion estimate: **100%**. This percentage measures this audit, not progress
toward a complete resolution of Kourovka 21.124.

**Verdict: PASS at the expressly restricted scope below.** No mathematical
objection remains against the frozen note. No complete resolution of 21.124,
virtual RAAG obstruction, originality determination, publication approval,
human review, or formal proof verification follows from this verdict.

The audited proof is `negative_geometric/FINITE_HOLONOMY_FILTER.md`, SHA256
`481cc37164a61084fee43241cd65965ddfaf808978e913b470f0b9fbf36f5dc0`.
Exact input and output hashes are in `RECEIPT.json`. I read only that family's
specified materials, the priority source contract and directly relevant primary
sources, and not other 21.124 mathematical family notes. I did not modify the
author's inputs, use git, publish, or communicate externally.

## Claims accepted, with quantifiers

For integer k>2 and

    G_k = <a,b,c,t | tat^-1=a, tbt^-1=ba^k,
                       tct^-1=caba^-1b^-1>,

the following are established by the input's arguments:

1. G_k is a genuine rank-three free-by-infinite-cyclic CAT(0) group.
2. For every finite-dimensional real vector space V and every homomorphism
   rho:G_k -> V semidirect Q, where Q is finite and acts linearly, if the
   **linear action** of rho(a) is identity, then its translation part is zero.
   In the input's narrower formulation, the finite label of rho(a) is identity,
   so rho(a) itself is identity. No faithfulness, discreteness, or properness is
   required. The dimension-zero case is immediate.
3. Every finite-index normal subgroup H of G_k **containing a itself** satisfies
   [a]=0 in H_1(H;Q). The same holds for an arbitrary finite-index H if the
   entire coset action of a is trivial, equivalently a belongs to its normal
   core. Merely fixing the base coset is insufficient.
4. If q:G_k -> Q is a finite abelian quotient and a^e belongs to ker(q), then
   [a^e]=0 in H_1(ker(q);Q). This is the input's separately justified abelian
   projection extension, not a consequence of item 3 alone.
5. G_k is not RFRS, with the standard definition starting the chain at G_k.
   This does **not** exclude a finite-index RFRS subgroup.

## Exact algebra and sign audit

Write w=aba^-1b^-1 and beta=bab^-1. The free-group automorphism fixes a and
beta: (ba^k)a(ba^k)^-1=bab^-1. It consequently fixes w=a beta^-1. Thus a,w
commute with t. The defining relations imply, with exactly the stated
tat^-1 convention,

    b^-1 t^m b = a^(km) t^m,
    c^-1 t^m c = w^m t^m.

There is no interchange of b and b^-1 in these formulas. Let t^m act by
translation T after killing its finite linear part. Let a act by translation
A, and let B,C be the linear parts of b,c. Conjugating translations gives

    B^-1 T = T+km A,
    C^-1 T = T+m(A-BA).

Translations in b,c do not appear in these identities. Eliminating A yields

    C^-1 T = (1-2/k)T + (BT+B^-1T)/k.

This reproduces the proposed formula. Averaging any positive-definite inner
product over Q makes B,C orthogonal. The coefficients are strictly positive
for k>2. For lambda_0=1-2/k, lambda_1=lambda_2=1/k and
x_0=T,x_1=BT,x_2=B^-1T, the exact identity is

    ||T||² - ||sum_i lambda_i x_i||²
      = sum_(i<j) lambda_i lambda_j ||x_i-x_j||².

The left side is zero because its second norm is ||C^-1T||=||T||. Every term
on the right is nonnegative with positive coefficient. Hence T=BT=B^-1T,
and km A=0, so A=0. This also covers T=0. This argument is a proof for every
finite holonomy, not an inference from the bounded computation below.

The original statement assumes that a's abstract finite label is identity.
Only its linear action was used. For a nonfaithful action, the stronger version
is obtained either directly from the same calculation or by factoring Q by the
kernel of its action. This distinction makes the abelian projection legitimate.

## Character induction, with an explicit cocycle convention

For H normal of finite index, let Q=G_k/H. Choose representatives r_q with
r_1=1. Define h(g,q) in H by

    g r_q = r_(bar(g)q) h(g,q).

For a character f:H -> R, use the permutation action
(P_g v)(q)=v(bar(g)^-1 q), and set

    v(g)(q)=f(h(g,bar(g)^-1 q)).

The identity h(g_1g_2,q)=h(g_1,bar(g_2)q)h(g_2,q) gives
v(g_1g_2)=v(g_1)+P_(g_1)v(g_2). Therefore (v(g),bar(g)) is an actual affine
homomorphism. If a is in H, its finite label is identity, and the coordinate
v(a)(1) is f(a). The filter therefore gives f(a)=0. Since H is finitely
generated, all real characters vanishing on a is equivalent to [a]=0 in its
rational abelianization. This fills the input's intentionally abbreviated
permutation-convention sentence; it does not change its mathematical content.

For a possibly nonnormal H whose core K contains a, restricting any f:H -> R
to K suffices. K is finite-index normal and contains a, so f(a)=0. No transfer
argument is needed, and no conclusion follows when a is merely in H but not K.

## Abelian quotient extension is valid

Let H=ker(q), Q abelian, and use the affine representation just constructed
from any character of H. Let D=P_a, of finite order d, and let

    E=(I+D+...+D^(d-1))/d.

It is the orthogonal projection onto W=Fix(D). Every Q matrix commutes with
D and hence with E. Thus W is Q invariant, and (E v(g),P_g|W) is a
homomorphism to W semidirect image(Q|W). The linear image of a there is
identity. The filter gives E v(a)=0. If a^e is in H, then d divides e, and

    v(a^e)=(I+D+...+D^(e-1))v(a)=e E v(a)=0.

Its identity-coset coordinate is f(a^e), which consequently vanishes. The
abelian assumption is used at the exact invariant-subspace step. Dropping it
is unjustified and is in fact false as a blanket extension, as the example
below shows.

## RFRS deduction and source scope

The relation tbt^-1=ba^k gives k[a]=0 in the abelianization of G_k, so a is
in its rational-derived subgroup. In a standard RFRS chain H_i normal in
G_k, containing a at stage i implies its rational homology class is zero by
the normal-cover theorem. The chain condition forces a into stage i+1.
Thus a is in the entire intersection, contradicting residuality because the
free fiber embeds and a has infinite order.

This normality convention agrees with [Agol, Definition 2.1 and the following
core-normalization argument](https://arxiv.org/pdf/0707.4522), and with
[Wu–Ye, §7](https://arxiv.org/html/2504.14192v2#S7). The existence of a
virtual RFRS subgroup does not supply such a chain starting with G_k. Wu–Ye
also explicitly exhibit a CAT(0) free-by-cyclic group that is not RFRS but is
virtually RFRS. This logical distinction is correctly retained in the note.

## CAT(0) eligibility rechecked against the primary theorem

[Delage, arXiv:2602.08759v3, Theorem 4.1](https://arxiv.org/html/2602.08759v3#S4)
has the same monodromy convention. For w=aba^-1b^-1 the word is cyclically
reduced, b balanced, not in <a>, with b height 1 and weights N_(a,0)=1,
N_(a,1)=-1, starting level 0. Its first sufficient inequality is 0<2k,
which holds for all k>0. Thus every family member used here meets the CAT(0)
hypothesis. This audit checks the application of that published theorem; it
does not independently reconstruct its geometric construction.

The theorem is the corrected source identified in the source contract.
Samuelson's erroneous general assertion is not a premise of this audit.

## Independently reproduced computations

The checker `independent_check.py` imports none of the author's scripts.
It contracts a spanning tree of each covering presentation, solves the
resulting exact rational equations for all character weights, and tests
a-orbit loops against the full character nullspace. This differs from the
author's full-edge boundary-row-space computation. Its unitriangular examples
are constructed through independent 4-by-4 matrix multiplication and matrix
inversion before converting to point permutations. Its results are:

- 10,188 exact signed-permutation/vector/k cases verify the squared-norm
  identity and its equality criterion for dimensions 1 through 4, k=3,...,8.
- 2,340 connected cyclic quotient covers, all degrees at most 5 and k=3,...,8,
  have all a-power loops homologically invisible, including 1,056 cases with
  a nontrivial cyclic quotient label. This only supports the separately proved
  abelian-quotient theorem.
- The author's two explicit k=1 and k=2 integer cocycles evaluate to zero on
  every lifted relator and to one on the specified a-loop.
- The four nonabelian affine covers (k,p)=(3,2),(4,3),(5,2),(5,3) satisfy
  every relator exactly and have no visible a-orbit loop; their first rational
  Betti numbers are respectively 9,21,9,21.

No bounded computation is used as a substitute for the theorem's all-Q proof.

The checker also constructs direct affine counterexamples at the omitted
parameters. For k=2 take V=R, a as translation -1, b and c as reflection
x -> -x, and t as translation 1. For k=1 take V=R², B a quarter-turn,
C=-I, T=(1,0), and A=B^-1T-T=(-1,-1), with zero translation part for b,c.
All three relators evaluate to identity exactly. The respective finite
linear groups have orders 2 and 4. Thus k>2 is necessary for this filter.

## Concrete falsifier for wider finite-index claims

The author subsequently supplied, separately from the frozen note, a
four-sheet nonnormal cover for k=4 with generator permutations

    a=(2 3), b=(0 1), c=(0 2)(1 3), t=1.

I independently verified its relators, connectedness, rank and character
space, rather than importing the author's computed output. Its rational
b_1 is 7. The following integer weights (a,b,c,t), for vertices 0,1,2,3,
are an independently obtained character certificate:

    ( 1,0,0,-2),
    (-1,0,0, 2),
    ( 0,2,0, 0),
    ( 0,0,0, 0).

All 12 lifted relators have zero total weight. The a-loop at vertex 0 has
weight 1. The subgroup H at vertex 0 contains a, and this character defines
a retraction H -> <a> by h -> a^f(h). Thus the statement obtained by deleting
the word "normal" from the main homology consequence is false. This does
not construct a virtual RAAG embedding.

Moreover the permutation image is D8 of order 8. Its normal core N has
index 8, contains a² but does not contain a. Restricting the preceding
character gives f(a²)=2. An independently generated regular D8 action and
full character computation confirm b_1(N)=12 and give an explicit integral
character evaluating to 1 on a² at its identity vertex. Consequently the
potential claim "every power of a in every finite-index normal subgroup is
homologically invisible" is already false for k=4. The exact permutation
and integral-character certificate is in `independent_results.json`.

This makes the missing finite-holonomy case substantive: replacing a by a
power does not recover the filter for arbitrary nonabelian finite images.

## Promotion decision

The normal/core and abelian-quotient restrictions survive adversarial review.
They are useful partial constraints. They do not exclude every finite-index
subgroup, and the explicit D8 example blocks a blanket a-power extension.
No virtual specialness conclusion, complete answer to 21.124, or claim of
original priority is approved. A further research mechanism must address
arbitrary finite-index subgroups with nontrivial a-holonomy or use a different
invariant. There are no outstanding substantive objections to the **frozen,
restricted** result.
