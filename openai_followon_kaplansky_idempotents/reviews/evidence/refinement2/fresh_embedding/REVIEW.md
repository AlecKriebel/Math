# Fresh independent embedding, algebra, and deterministic topology review

Reviewed 2026-10-07 UTC against `reviews/refinement2_manifest.json`.
Frozen `main.tex` SHA-256:
`a2d6f9dce6b65e23c0a325619ada4a50ba1fcbeb02fda555c0e9debb13b3b5b6`.

**Verdict: no substantive defect found within the scope below.** The
two-generator/r-relator realization, deterministic cone criterion,
scalar idempotent, right-module splitting, coefficient extension, and
K0 boundary claims survive the attacks performed. This is a scoped
review, not a replacement for the separately assigned complete
probabilistic/parameter-transfer review.

I read AGENTS.md and ORIGINAL_REQUEST.txt directly, all of main.tex,
CURRENT_THEOREM.md, DEPENDENCY_LEDGER.md and README.md. I independently
read the pinned October 4 paper source, introduction, algebra,
assembly, all topology, and the setup/types/weights portion of random;
I read the definition and deterministic hypotheses at the start of
planar. I also read the September 23 zero-divisor manuscript's full
topology and main introduction, its types as relevant to comparisons,
the earlier torsion construction's introduction and embedding section,
and family-197 Lean scope. Prior review verdicts were not used as proof.
`INSPECTED_SOURCE_HASHES.json` identifies the actual files.

## 1. Free associated subgroups and base embedding

Write B=G*F(x,y). For indices 0 through s, put
u_i=x^(-i)yx^i (including u_0=y). A reduced word in these generators
expands into alternating nonzero y-powers and x-powers separating
unequal indices. In a maximal same-index block, all signs agree:
opposite adjacent signs would have been a forbidden free cancellation.
Consequently every y-block remains nonzero. Distinct adjacent index
blocks have nonzero intervening x-powers. Thus the expansion is
nonempty and freely reduced after these block amalgamations, including
when the first or last index is zero. This directly proves that the
u_i are free, without assuming a free basis theorem.

For v_0=x and v_i=y^(-i)xg_i y^i, projection B->F(x,y) killing G maps
them to y^(-i)xy^i. The same expansion argument proves independence of
these projected words. A relation in the v_i would project to such a
relation, so the v_i are also free, even if a g_i is trivial or some
generators of G coincide. Hence u_i->v_i is an isomorphism of free
subgroups. HNN base injection applies; no disjointness of these two
subgroups is required. This embeds G in the claimed H.

The primary [HNN publisher PDF](https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms/s1-24.4.247)
was inspected through publicsource browsing: Theorem I/I' is the
subgroup-isomorphism adjunction result, and Theorem IV states the
two-generator embedding and preservation of the number of defining
relators. Its locally-infinite terminology is explicitly explained
as torsion-freeness. The manuscript's finite version is classical.
[Morozov--Schupp](https://ems.press/content/serial-article-files/44364),
Observation 3.4, p.151, explicitly uses a free product with F2 followed
by an HNN extension to express each original generator in two
generators. The exact displayed family in the current manuscript is
proved directly; identical encoding words in that reference are not
needed. Its downloaded PDF hash is recorded in
PRIMARY_SOURCE_RECEIPT.json. Direct local HNN download was blocked by
HTTP 403, while its complete primary theorem/proof text remained
available through publicsource browsing; no downloaded-PDF hash is
invented for that source.

## 2. Exact substitutions and relator count

The zeroth relation t^(-1)yt=x gives y=txt^(-1). For i>=1, multiplying
t^(-1)x^(-i)yx^it=y^(-i)xg_i y^i on the appropriate sides gives

g_i=x^(-1)y^it^(-1)x^(-i)yx^ity^(-i).

Substituting y=txt^(-1), using (txt^(-1))^i=tx^it^(-1), yields exactly

W_i=x^(-1)tx^it^(-2)x^(-i)txt^(-1)x^it^2x^(-i)t^(-1).

Thus x,t generate H. A separate fresh checker, independent of the
packaged verifier, checks the solved HNN relation and substitution for
every i=1,...,532, including both boundary indices, not only selected
examples. Each W_i is freely reduced and has length 4i+10. The maximum
checked length is 2138. Its receipt is INDEPENDENT_CHECK_RECEIPT.json;
the derivation above proves all positive indices.

For an aspherical presentation of G with s generators and r relators,
start with the aspherical graph-of-spaces HNN complex. In its subcomplex
containing only the original generator edges, x,y,t, and the s+1 HNN
cells, each positive-index cell has its own g_i appearing exactly once,
and no other HNN cell contains that g_i. These are definitional
edge-cell eliminations. Eliminating them gives a homotopy equivalence;
then eliminating y with the zeroth relation gives the x,t rose. Attach
the original r cells afterward and transport their attaching maps
through this equivalence. Their attaching words are R_j(W). Homotopy
invariance of attaching a finite collection of cells proves equivalence
with the displayed two-generator r-relator presentation complex. This
argument specifically avoids the false claim that arbitrary Tietze
transformations preserve asphericity.

The Euler characteristic is an independent consistency check: the
vertex space for B has chi(B)=chi(G)-2=r-s-1, the edge rose has
chi=-s, and the HNN total has chi=r-1, exactly the characteristic of
the two-generator r-cell presentation.

## 3. Finite two-dimensional classifying space and torsion

Collapse a maximal tree of the finite two-dimensional classifying
complex for G. Its wedge with the x,y rose is a finite K(B,1).
Represent both free subgroup inclusions by maps of the (s+1)-petal
rose; attaching its cylinder has dimension at most two and finite
cell count. The two maps are injective on fundamental groups by the
free-family proof above. In the universal cover the associated
Bass--Serre tree has contractible vertex spaces and contractible edge
spaces. A finite subtree gives an iterated homotopy pushout of
contractible spaces along contractible spaces, hence is contractible.
Compact images of sphere maps lie in a finite subcomplex and therefore
a finite such subtree. All homotopy groups vanish, and Whitehead gives
contractibility. No unsupported assertion that an immersed subgroup
rose embeds as a subspace is used.

This independently verifies the strengthened finite-classifying-space
claim; it is not imported from HNN Theorem IV alone. Torsion-freeness
also follows directly from this finite-dimensional K(H,1), so the
manuscript's usual HNN torsion-conjugacy argument is redundant, not a
hidden additional hypothesis. The s=0/r=0 case gives F2, agreeing with
all constructions. Repeated/trivial generators cause no exception.

## 4. Primary cone-picture criterion

The October 4 algebra and topology definitions fit the reduced
arrangement definition. Cones need not embed in the quotient; all
homotopies and surgeries instead factor through their abstract cones.

Replacing one abstract cone by its graph with disks on a free basis
is a relative homotopy equivalence: the substitute is simply connected
and acyclic, hence contractible; cellular extension constructs maps
and inverse homotopies fixing the common graph. Relative gluing thus
works for noninjective graph-to-rose maps. The PL regular-point picture
construction produces disk preimages and is compatible with a fixed
outer boundary. Constant inner loops can be removed through the same
contractible cone. Tightening an outer path preserves its actual graph
endpoints, and distinct endpoints exclude the empty path.

I checked the endpoints in all four shortening cases. If e:u->v,
the two inner words eP and e^(-1)Q have P:v->u, Q:u->v, so PQ closes.
For one inner word eP e^(-1)Q, P closes at v and Q at u; its two caps
are well defined. For an exterior P e R paired with inner e^(-1)Q,
Q goes u->v, so PQR has the original exterior endpoints. For exterior
P e Q e^(-1)R, Q closes at v and PR retains the original endpoints.
Restriction to the break-containing component does not require a
separate filling of Q. These formulas shorten by two before any
further tightening.

For splitting an essential sphere, the annulus and both caps factor
through a single lift of the same abstract cone, chosen to agree at
one point and then everywhere on the connected annulus by uniqueness
of lifts. The difference of the original and capped fundamental cycles
therefore bounds in that abstract cone. The resulting sum identity
in H2 of the simply connected universal cover forces a nonzero cap
class by Hurewicz. This establishes essentiality without assuming
asphericity in advance. For a disk failure the retained component has
the original exterior or the verified shorter path with the same
distinct endpoints. If it had no ordinary inner disk, its nonempty
freely reduced word would bound in the rose, impossible. Thus every
failure still supplies an ordinary cyclic boundary and a reduced
arrangement, contradicting the deterministic hypothesis.

After pi2 vanishes, the two-dimensional simply connected cover is
acyclic and contractible. Restricting its length-two ZG-free resolution
to any prime-order cyclic subgroup stays free. The cyclic periodic
resolution with maps u-1 and N gives nonzero cohomology with F_l in
every degree, contradicting that finite resolution. This torsion proof
is independent of either cited companion's conclusion. The relevant
September 23 zero-divisor companion reproduces compatible cone lifts
and endpoint surgeries; it uses three extras and is not a substitute
for the October 4 seven-extra one-sided inverse construction.

## 5. Scalar algebra, handedness, K0, and extensions

Put f=ba. From ab=1, f^2=f; then e=1-f satisfies e^2=e in every
unital ring, irrespective of characteristic. From ac=0, ec=c, so
c!=0 forces e!=0. If e=1, then ba=0 and a=a(ba)=0, contradicting
ab=1 in a nonzero ring. These are scalar, not matrix, identities.

Complementarity gives R_R=fR direct-sum eR. Since b=bab,
fR=bR. Left multiplication by b maps the right module R_R to bR
and has inverse left multiplication by a. The formulas
Phi(r)=(ar,er), Psi(u,p)=bu+p are right linear; their compositions
use ab=1, ae=eb=0 and ep=p and are exactly the identities. The right
annihilator of a is eR: er lies in the kernel; if ar=0, then
r=bar+er=er. This also confirms that c lies in P.

P=eR is nonzero, cyclic, and a finitely generated projective summand.
Its absorption gives [R]=[R]+[P], whence [P]=0 in the Grothendieck
group. This does not identify P with zero in the projective monoid.
The given explicit absorption is a failure of cancellation between
the two modules 0 and P. The augmentation R->F2 and scalar inclusion
F2->R compose to the identity. Their scalar-extension maps on K0
therefore split off Z=K0(F2), so the manuscript correctly excludes the
stronger claim K0(R)=0.

The fresh formal checker verifies these universal identities in
Z<a,b,c>/(ab-1,ac). It does not certify c!=0 in the target group ring.
As a consistency/falsification model, take the infinite vector space
with basis d_0,d_1,..., let b(d_i)=d_(i+1), a(d_0)=0,
a(d_(i+1))=d_i, and let c be projection onto d_0. Then ab=1,
ac=0, and e=c is nonzero. This model confirms that none of these
ring/module conclusions silently relies on finite dimensionality.

Coefficient extension is injective because distinct group elements
remain a basis and the prime-field map F2->K is injective. The same
argument verifies transport through G->H. Nonzero e and e-1 survive,
and the same a,b,c then reprove absorption over K[H]. No odd-
characteristic, characteristic-zero, analytic projection, central
idempotent, or nonzero K0-class conclusion is made or follows here.
A torsion-free group generated by at most one element is trivial or
infinite cyclic, with group algebra a field or a Laurent polynomial
domain. Hence two is the correct minimum generator count once this
H exists; this adds no new embedding mechanism.

The exact conjecture statement was verified in [Öinert v3](https://arxiv.org/html/1904.04847v3),
Problem 1(c). The classical implication from absence of nontrivial
idempotents to direct finiteness was independently read in the pinned
Gardam primary source, Proposition kaplansky_relations.
[Weibel Chapter II](https://sites.math.rutgers.edu/~weibel/Kbook/Kbook.ii.pdf),
Section 2, gives the stated K0 definition. The Ara report's identity
and right-module conventions were checked, but its exact p.9 text
could not be refetched during this pass; the self-contained proof
above establishes the cited algebra independently. This retrieval
limit is not a mathematical gap and is not a claim of independently
rechecking every historical citation page.

## 6. Explicitness and attribution

The selected matching and sufficiently large m are existential.
Reading tree words from roots x_A and x_B in their designated
components gives the parity witnesses with the correct identity
coefficient in c. Reading one relator per non-tree edge gives a finite
presentation. These are fully specified construction rules after the
selection; they are not a supplied numerical presentation or a
decidable successful-matching search. The text distinguishes these
notions accurately. The all-532 embedding checks do not change that
explicitness boundary or compute the reduced support of any witness.

I directly fetched the public frozen [triage report](https://raw.githubusercontent.com/AlecKriebel/Math/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/REPORT.md)
and [algebra notes](https://raw.githubusercontent.com/AlecKriebel/Math/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/agent_notes/algebra_groups.md).
They already state the core idempotent, absorption and vanishing-class
consequences conditionally on auditing the October 4 input. The note
acknowledges that duplication, attributes the construction to OpenAI,
and identifies its additional contribution as the model calibration.
The inspected October 4 setup fixes q=128 and the relevant zero-divisor
companion fixes q=128 with a different three-extra recipe; neither
supplies the current exact seven-extra threshold. No first-priority
claim or mathematical novelty of HNN machinery is asserted. This
limited comparison is affirmative evidence for framing, not proof
of absence from all literature. The independent full priority and
probability audits remain required for the final publication verdict.

## Artifacts and restrictions

- INSPECTED_SOURCE_HASHES.json: exact local input identities.
- PRIMARY_SOURCE_RECEIPT.json: successful primary PDF identities and
  precise failed local-download attempts.
- independent_checks.py and INDEPENDENT_CHECK_RECEIPT.json: separate
  universal algebra and 532-index free-word checks.
- RESEARCH_LOG.md: timestamp and completion estimate.

No frozen files, Git state, publication record or tracker were changed.
No external individual was contacted. Scoped review completion: 100%.
