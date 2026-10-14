# Independent adversarial audit: rank 455 / problem 20001515

Completed 2026-10-03 UTC by a fresh reviewer not involved in the construction.

## Verdict and exact scope

**PASS.** The frozen construction proves that the group with presentation

    G = <a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>

acts freely, properly, and cocompactly by cubical isometries on a locally finite
three-dimensional CAT(0) cube complex. The finite quotient has the stated cell
counts (1,7,8,2). This is the exact automorphism in archived AIM Problem 5.2.
There is no mathematical repair required. The newly recovered primary-source
provenance should be incorporated before the packet's final source-status update.

This is an independent internal mathematical audit, not formal verification,
external peer review, or historical-priority certification. It does not prove
virtual specialness, a minimal cubical dimension, or any statement about the
workshop's different b -> aba automorphism. It does not certify current live AIM
availability or independently certify the remote branch beyond the supplied local
freeze. No public files or remote state were changed by this audit.

## Freeze and independence

All five public-file SHA-256 values match FROZEN_MANIFEST.local.json. In particular:

    ATTEMPT_1.md
    c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6

The associated supplied remote WIP identifier is
bb7dac6872a680735897b1701a1a41d22e19f562.

The reviewer reconstructed the geometry in independent_audit.py and the target
semidirect-product arithmetic in independent_algebra.py before reading the author's
verify.py. Neither independent program imports or executes that verifier. The
reviewer did not use the contributing cyclic-hull worker's notes. The later reading
of the author's program found it consistent with the independent results.

## 1. Base complex and involution

From each square word, an incoming letter l followed by m contributes the link
edge {l^-1,m}. Applying this to xyXY and bxBY gives exactly the four signed x/y
pairs and the four additional edges b-/x+, b-/x-, b+/y+, b+/y-. All eight edge
occurrences are distinct, there are no loops, and the graph is bipartite with
parts {x+,x-,b+} and {y+,y-,b-}. Thus it is a flag simplicial graph.

The map lambda(x)=y, lambda(y)=x, lambda(b)=B is genuinely cubical, not merely
an automorphism of the presentation. On the first square it is a diagonal
reflection. On the second square, with corners numbered consecutively 0,1,2,3
starting before b, it exchanges 0 with 1 and 2 with 3. Its boundary becomes
BybX, a cyclic shift of the reversed original boundary. Both face maps square
to the identity and agree on common edge cells. Hence lambda is a cubical
involution fixing the single vertex.

## 2. Q, including repeated vertices in a characteristic square

The first Q-square has vertex sequence B,A,C,D. The second has vertex sequence
A,B,A,C. The second occurrence of A is essential and is allowed in a cube complex
whose characteristic cubes are not globally embedded. It does not cause a local
fold: the two link corners contributed at A are distinct.

The independently computed link images are exactly:

- A: b- -- x- -- y+ -- b+
- B: b- -- x+ -- y+
- C: x- -- y- -- b+
- D: x+ -- y-

At each vertex, both directions and link edges map injectively. The displayed
edges are all of the edges of the K-link induced by those directions. These are
full simplicial subcomplexes, so j is a local isometry. Composing with the cubical
isometry lambda preserves that conclusion. In particular Q is NPC and each
fundamental-group map is injective. This is a finite local calculation; no claim
about an unspecified convex hull is needed.

The edges p,q,s form a connected three-edge tree on the four vertices. After its
collapse, the two relators are r^-1 and d e^-1. Therefore the group is exactly
infinite cyclic. Based at A, dp gives a generator, and its two based images are
bx and B y. Both end maps have the same specified basepoint in K, so no omitted
basepoint path is hiding a conjugation.

## 3. Full quotient-cell reconstruction and flagness

Write z_A,z_B,z_C,z_D for the upward vertical edges. For any oriented Q edge
e:u->v with bottom label l, its product square has boundary

    l z_v lambda(l)^-1 z_u^-1.

Thus the six additional square words are

    p: x z_A Y z_B^-1
    q: y z_C X z_A^-1
    r: x z_C Y z_D^-1
    s: y z_D X z_B^-1
    d: b z_B b z_A^-1
    e: b z_A b z_C^-1.

The independent program takes these six words together with the two K-square
words as the actual 2-skeleton. All 32 square-corner occurrences are distinct
link edges with distinct endpoints; hence there are no unrecorded loops or
multiple link edges.

For each of the two Q-squares, the reviewer then used its actual four coordinate
corners and both interval endpoints to obtain all eight corner triangles of the
corresponding 3-cube. At the bottom, a corner consists of its two j-labelled
horizontal germs and z_v+. At the top, it consists of the lambda-transformed
horizontal germs and z_v-. Every triangle has three distinct germs and its three
boundary edges exist in the computed 2-skeleton link. All 16 triangle occurrences
are distinct. Each of the four vertical faces of each cube agrees, up to square
symmetry, with its specified product-square cell; the two horizontal faces agree
with the appropriate K-square. This checks the identifications rather than
assuming an abstract cone description is already realized by cubes.

The resulting link has 14 vertices, 32 edges, and 16 triangles. Exhaustive exact
clique enumeration in this finite graph gives 16 three-cliques and no clique of
size 4 or larger. The three-cliques are exactly the 16 actual cube corners. Thus
the link is a flag simplicial complex. Deleting each one of these triangle
occurrences separately fails this check. Replacing lambda(b)=B by lambda(b)=b
fails the K-square attachment check. The 17 controls are corroborative only;
the incidence calculation and clique proof establish the finite claim.

Equivalently, the link is obtained by adjoining eight cones along the four full
Q-link images and their lambda-images. There is no edge between two cone apices,
so a clique either lies in the flag K-link or lies in a single one of those cones.
This supplies a short proof of flagness independently of the enumeration.

The quotient has one vertex, 3+4 edges, 2+6 squares, and two cubes. All attaching
maps are facewise isometries. Global noninjectivity of j causes no defect: it is
the usual cube-complex convention allowing identifications in characteristic
cube boundaries. For the stricter convention of embedded cubes with facewise
intersections, one can take the second cubical subdivision. This changes the
cell counts but not the metric conclusion or group. Leary's Theorem C.9 and
Corollary C.11 explicitly cover this distinction:
https://arxiv.org/pdf/1009.1540 . No subdivision is needed for the asserted
ordinary NPC cube-complex formulation.

## 4. Exact group identification, with a reverse implication

A homomorphism from the cube-complex presentation into the target group would
not alone prove the needed isomorphism. Here are reversible eliminations of the
actual product-square relations.

Put z=z_A. The p,q,s relations eliminate three vertical generators as

    z_B = x z Y,
    z_C = Y z x,
    z_D = Y x z Y x.

The r relation then holds using xy=yx. For example its equality
x z_C Y=z_D becomes xY z xY=Yx z Yx, and commutation of x and y makes both
sides identical. The d relation is

    b x z Y b = z,

or equivalently

    z^-1 b x z = B y.

The e relation is b z b=Y z x, or equivalently

    z^-1 y b z = x B.

But the base relation bxB=y gives both yb=bx and xB=B y. Consequently e is
exactly the same remaining relation as d. No additional relator remains.
The two 3-cells have no effect on pi_1. This yields precisely

    <x,y,b,z | xy=yx, bxB=y, z^-1 b x z=B y>.

Now set t=x, a=xY, c=(zx)^-1. The inverse substitutions are x=t,
y=a^-1 t, z=c^-1 t^-1, so this is a reversible generator change. The first
base relation becomes [a,t]=1. The second becomes b t B=a^-1 t, which is
equivalent to t b t^-1=a b.

For the last relation, the base relation gives B y=xB. Put u=B x and v=bx.
Then B y=x u x^-1. Thus

    z^-1 v z = x u x^-1
    <=> (zx)u(zx)^-1=v
    <=> c^-1 B t c = b t
    <=> t c t^-1 = b c b.

Every displayed step is reversible. This proves the exact target presentation,
not merely a quotient, a finite-index subgroup, or a mapping torus of a power.
The convention t f t^-1=phi(f) is maintained throughout.

For independent arithmetic corroboration, the reviewer implemented the normal
form f t^n with multiplication (f,n)(g,m)=(f phi^n(g),n+m). The inverse
substitution phi^-1 is a->a, b->Ab, c->BacBa. Both compositions with phi reduce
to the identity on the three generators. The two K-relators, all six actual
product-square relators, and the HNN relator evaluate to identity under the
proposed substitutions. The original a,c,t are also recovered. This program
checks the forward map; the reversible argument above supplies the reverse map.

## 5. Optional lifted involution and ribbon claims

The unique lift of lambda fixing the identity vertex of the universal cover
acts on vertices by h->lambda(h). It squares to the identity. With f=B lambda,

    f^2 = B lambda(B) = B b = 1,
    f u f^-1 = B lambda(Bx) b = y b = b x = v.

Thus the claimed involution and conjugacy are correct.

For the ribbon description choose the lift A_i=(bx)^i. The other chosen
vertices in that period are B_i=A_i X, C_i=A_i y, D_i=A_i Xy. The torus square
has vertices B_i,A_i,C_i,D_i. The other square joins A_i,B_(i+1),A_(i+1),C_i,
using yb=bx. It therefore joins the right side of the ith flat square to the
bottom side of the next, as claimed. The local isometry gives a convex embedding
of the universal cover of Q, and the cyclic deck action has quotient Q. These
optional claims are consistent, but the main proof does not depend on them.

## 6. CAT(0), properness, and cocompactness

The finite unit cube complex Z is a complete length space. The verified flag
link gives local CAT(0), and cubical Cartan-Hadamard gives a CAT(0) universal
cover. The cover has the lifted cube structure, dimension three, and finite
vertex links. It is locally finite, with finitely many unit-cube shapes, hence
proper. Deck transformations preserve that structure and its metric and act
freely. Compact sets meet only finitely many cells; consequently only finitely
many deck transformations can translate one compact set to intersect another.
The action is proper. Its quotient is the finite, therefore compact, complex Z,
so the action is cocompact. This supplies all parts of a geometric cubulation.

The hypotheses of the standard link and Cartan-Hadamard criteria are met; no
unsupported general cocompactness theorem, product of actions, or cubulation of
an abstract quasi-isometric space is invoked.

## 7. Exact AIM source gate

An ordinary, default-TLS urllib request to the archived section succeeded. The
requested approximate timestamp redirected to the actual August 2024 capture:

https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/

The response is 200, 25,734 bytes, SHA-256

    9dfa1624c5743d114c671ea69201a9ea46fe577e707239e245cc7f22b30b8121.

The displayed Problem 5.2 and its embedded AIM record both give a->a, b->ab,
c->bcb, attribute the question to Rylee Lyman, and ask for a geometric action
on a CAT(0) cube complex. The embedded record is
0df1011a6fa8a3c46e2c977b7e12c66f, revision
6-d5a22eda9ed96ccdc8327e2e9395bb3e. Its attached remark says that a geometric
action on a CAT(0) space was already known; that is weaker than the asked
cubulation.

The response's memento metadata exposed a later capture, which was also
independently retrieved with default TLS:

https://web.archive.org/web/20260310215532id_/http://www.aimpl.org/freebycyclic/5/

It is byte-identical, including the same question and remark. This establishes
archived source identity. It does not certify that the current live page works,
that no author has solved the problem since, or that this construction is new.

The workshop report's printed page 2 instead has b->aba and c->bcb, and describes
a three-dimensional candidate. It was independently read:
https://aimath.org/pastworkshops/freebycyclicrep.pdf . The frozen proof correctly
keeps it distinct. The source discrepancy is resolved as two genuinely different
written formulas; it is not a reason to replace the target formula.

## 8. Repairs, packaging, and evidence ceiling

No mathematical repair or additional author proof attempt is requested.
Before source-status promotion, add the two exact archive URLs, actual retrieval
provenance, and the distinction between archived source verification and current
live-page availability to SOURCE_GATE.md. Update ATTEMPT_1.md's source-recovery
qualification and the review status in a dated addendum or narrowly scoped edit.
Keep the original mathematical construction fixed. Any new freeze should make
these documentation-only differences auditable.

Keep raw archived HTML, raw source records, and HTTP headers outside the public
packet as already required by its publication boundary. The short source
provenance and these original independent proofs/checks may be summarized or
included as appropriate. This report does not authorize remote writes or final
promotion; it supplies the requested independent mathematical/source decision.

The bounded literature inspection still supports caution: Hagen-Wise's current
version distinguishes free cubulation from proper/cocompact cubulation, and the
workshop already records a nearby candidate. No first-resolution claim follows.
