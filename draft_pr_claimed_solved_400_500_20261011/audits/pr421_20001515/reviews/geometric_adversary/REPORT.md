# PR 421 independent geometric adversary report

Frozen head: `d5bf8b5a25cabb177433338fae60af52ebfecf1c`.
Assigned scope: the exact affirmative construction for

\[
G=\langle a,b,c,t\mid tat^{-1}=a,\ tbt^{-1}=ab,\ tct^{-1}=bcb\rangle.
\]

**Verdict: PASS for the assigned mathematical geometry scope.** The specified
finite cubical quotient is well-defined and locally CAT(0); its universal cover
is a locally finite, three-dimensional CAT(0) cube complex with a proper
cocompact deck action. The reversible presentation calculation identifies the
deck group with the displayed rank-three mapping torus. No geometric repair or
additional proof-search turn is needed. This report does not assess priority or
paper scope.

## Independence and evidence

`CRITERIA_SEAL.json`, `RECONSTRUCTION_SEAL.md`, and `FINITE_RESULTS_SEAL.json`
were written before reading the historical audit, verification addendum, author
verifier, or historical checker results. The reconstruction uses the raw
ATTEMPT_1 cell recipe and the permitted exact source statement. It uses no peer
or parent verdict. The original checker `geometric_check.py` derives signed
incidences from endpoints and actual boundary words; it imports no historical
program. `FINITE_RESULTS.json` preserves every product-square corner and every
cube corner and face.

After those seals, the historical material and all three source programs were
read fully. They were copied into the private reviewer directory, run only
there, and reproduced their saved outputs exactly. All thirteen frozen source
hashes still match the receipt. The original verifier does not by itself prove
the reverse group isomorphism or CAT(0) globalization; those are written
deductions, kept separate from its finite arithmetic checks.

## Actual attaching maps, including nonembedded boundaries

The K square words are `xyXY` and `bxBY`. Deriving a corner after incoming
letter h and before outgoing letter k as the pair `(h^-1,k)` gives eight distinct
K-link edges on six signed directions, with no triangle. It is a flag bipartite
graph. The involution `x↔y, b↔B` sends the first square to its reverse and the
second to a cyclic rotation of its reverse. These are face isometries, agree
on edges, and square to identity.

The Q square vertex cycles are `(B,A,C,D)` and `(A,B,A,C)`. Thus the second Q
square repeats the vertex A, and its product cube repeats the vertical edge
z_A on opposite boundary positions. Both product cubes also identify their two
horizontal faces to the same underlying K square cell. These identifications
are real and were retained in all corner multiplicities.

For h:S→T of image label ell, the product square has boundary
`ell z_T lambda(ell)^-1 z_S^-1`. The resulting six square words are:

| Q edge | Product-square boundary |
| --- | --- |
| p | x z_A Y z_B^-1 |
| q | y z_C X z_A^-1 |
| r | x z_C Y z_D^-1 |
| s | y z_D X z_B^-1 |
| d | b z_B b z_A^-1 |
| e | b z_A b z_C^-1 |

Each product cube has four side faces given by the four signed Q boundary
edges and the bottom/top faces given by j and lambda j. All twelve face
occurrences agree, up to the specified square symmetries, with the designated
square cells. They agree on the shared edges, so the characteristic maps are
consistent facewise Euclidean isometries. No cube interior is folded or
identified by this quotient recipe.

## Local isometries and the complete signed link

The independently derived Q link images are:

| Vertex | Induced link path in K |
| --- | --- |
| A | b- — x- — y+ — b+ |
| B | b- — x+ — y+ |
| C | x- — y- — b+ |
| D | x+ — y- |

Both direction and edge maps are injective, and each image equals the full
induced subcomplex on its directions. The K link has no higher simplices to
check. Consequently Q is NPC and j is a cubical local isometry; composition
with the verified cubical involution gives the second local isometry. The
injective/full-link formulation and the induced fundamental-group injection
are stated in Ben–Zvi, Kropholler and Lyman, §2 and Proposition 2.1.
[Primary paper](https://wrap.warwick.ac.uk/160721/1/WRAP-folding-like-techniques-CAT%280%29-cube-complexes-Kropholler-2021.pdf).

The actual eight square boundaries give 32 corner occurrences, all distinct
link edges with distinct endpoints. The two actual cubes give sixteen corner
occurrences, all distinct triangles with three distinct directions and all
their boundary edges present. The sole final vertex link has f-vector
`(14,32,16)`. Exact clique enumeration finds sixteen 3-cliques, precisely those
sixteen cube corners, and no 4-clique. Every larger clique would contain a
4-clique, so none exists. No multiplicity was discarded by representing the
link only as sets.

There is also a deductive flagness check: no two vertical directions are
adjacent. A clique with a vertical direction therefore lies in its single cone
on one of the full Q-link images; a clique without one lies in the flag K
link. Thus every clique is filled. Cell counts are `(1,7,8,2)`.

Five independent geometric negative controls are rejected for substantive
defects: removing the first Q square breaks fullness at all four Q vertices;
removing the first product cube while retaining its sides leaves eight unfilled
3-cliques; merging z_A and z_B produces four duplicate link edges; changing
r's x label to y fails a K-face attachment and folds a direction; changing
r's initial endpoint from D to B makes the Q boundary nonclosed. Reversing
the orientation of both Q squares preserves the accepted link and all triangles.

## Cubical convention and global metric hypotheses

This quotient is a cube complex with permitted characteristic-boundary
identifications, rather than an embedded-cell cubical complex. Leary's
Theorem C.9 applies to arbitrary cube-complex links and makes the verified flag
simplicial link exactly the local CAT(0) criterion. Theorem C.4 guarantees that
the CAT(0) universal cover has embedded cubes and single-face intersections;
Corollary C.11 supplies second cubical subdivision if that convention is wanted
already for the quotient. Thus the action space meets the stricter cubical
convention as well. [Primary paper, Appendix C](https://arxiv.org/pdf/1009.1540).

The finite connected quotient consists of unit Euclidean cells in dimensions
at most three. Its intrinsic metric is complete and has finitely many local
shapes. Its covering space has the lifted finite link incidences, uniform cell
sizes, and finite dimension. The lifted length metric is complete and locally
compact; the length-space Hopf–Rinow theorem makes it proper. Cubical
Cartan–Hadamard makes this simply connected locally CAT(0) cover globally CAT(0).
No infinite-dimensional, shrinking-cell, or accumulation exception is present.

For an explicit proper-action argument, put a compact set C inside B_R(v) for
a fixed vertex v. If gC intersects C, then d(v,gv)≤2R. The orbit of v is a
closed discrete covering fiber; its intersection with the compact ball
B_(2R)(v) is finite. A deck transformation is determined by v's image, so only
finitely many g can satisfy gC∩C≠∅. The action is free and isometric, and its
quotient is the finite complex Z, hence compact. This verifies properness and
cocompactness individually.

## Exact group domain and historical secondary claims

Collapsing Q's tree p,q,s gives relators `r^-1` and `d e^-1`, so pi_1(Q)
is infinite cyclic, with generator dp and based images bx and B y. Independently
checking the product-square presentation gives, for z=z_A,

\[
z_B=xzy^{-1},\qquad z_C=y^{-1}zx,\qquad
z_D=y^{-1}xzy^{-1}x.
\]

The r relation follows from xy=yx. The d and e relations each reduce to
`z^-1 b x z=B y`, using `yb=bx` and `xB=B y`. Thus no extra relator or
subgroup qualifier remains:

\[
\pi_1(Z)=\langle x,y,b,z\mid xy=yx,\ bxB=y,\ z^{-1}bxz=B y\rangle.
\]

The reversible substitutions `t=x, a=xy^-1, c=(zx)^-1`, with inverse
`x=t, y=a^-1t, z=c^-1t^-1`, turn the relations into the exact displayed
target. In particular `B y=x(Bx)x^-1` changes the final relation to
`c^-1(Bt)c=bt`, equivalent to `tct^-1=bcb`. The underlying free-group map
is an automorphism: its inverse sends `a→a, b→Ab, c→BacBa`, with both
compositions reducing to identity on the basis. No monodromy power, cover,
or different b image is being substituted.

The optional ribbon picture also checks: for v=bx and A_i=v^i, the chosen
vertices B_i=A_i X, C_i=A_i y, D_i=A_i Xy give the flat square, while the
other square has vertices A_i,B_(i+1),A_(i+1),C_i because yb=bx. The local
isometry lifts to a convex cubical embedding, with cyclic quotient Q. For
u=B x, the lifted involution f=B lambda satisfies f²=1 and
f u f^-1=y b=bx. These secondary claims introduce no remaining geometric
gap, and the main finite construction does not depend on the picture.

## Remaining gap and publication boundary

**Exact remaining mathematical gap in this assigned geometry scope: none.**
The evidence is an independent written verification plus exact finite
computation, with standard geometric theorems explicitly invoked; it is not a
proof-assistant certificate or external peer review. Assigned verification
completion estimate: 100%; author proof turns remain 1/5 and this review adds 0.

Positive public allowlist: this original report, original `geometric_check.py`,
its original `FINITE_RESULTS.json`, `VERDICT.json`, and the reviewer seal/log/
historical-comparison metadata. The privately copied historical packet, raw
foreign catalog record, source downloads, and unrelated statuses are excluded.
