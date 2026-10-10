# Turn 4: common-cover geometry and a toroidal test case

Problem 2676, KP-1.17. Fourth substantive author turn. **Partial; the original
mixed-alternation question remains unresolved.** All links and involutions here
are tame/smooth. A homeomorphism may reverse orientation; reflecting a branch
link accommodates that possibility without changing alternation.

## 1. What is proved in this turn

1. Combining Turn 3 with the classical Seifert branching classification reduces
   any putative mixed pair to prime links with hyperbolic **exteriors**, whose
   common irreducible rational-homology-sphere L-space cover is either hyperbolic
   or toroidal and non-Seifert. Hyperbolicity of the branch exteriors does not
   imply hyperbolicity of their branched cover.
2. We give explicit gluing data for an irreducible toroidal L-space (Y), with
   (H_1(Y;\mathbb Z)=\mathbb Z/5), and construct a genuine involution with
   quotient (S^3). Its branch set is a prime hyperbolic knot.
3. No alternating link has cover (Y). Thus even irreducibility, the L-space
   property, finite cyclic first homology, and an actual spherical branch
   quotient do not ensure an alternating branch description.

The example belongs to the already classified small toroidal L-space setting
of Hanselman–Rasmussen–Watson. No novelty, exhaustive involution classification,
or counterexample to KP-1.17 is asserted. In particular, we have not found an
alternating branch description of the example: the proof rules all of them out.

## 2. Closing the Seifert common-cover sector

Turn 3 reduces a mixed pair, if one exists, to prime nonsplit nontrivial links

\[
 A\text{ alternating},\qquad B\text{ nonalternating},\qquad
 \Sigma_2(A)\cong\Sigma_2(B)=Y,
\]

where both link exteriors are hyperbolic and (Y) is irreducible and an L-space.
This reduction uses the precise degree-two Boyer–Gordon–Hu results stated there;
it does not assume their all-degree conjectures.

Suppose this common (Y) is Seifert fibered. The classification summarized in
Mecchia–Reni (2002), printed pp. 429–430, gives the following inputs.

* Spherical Seifert manifolds have a unique conjugacy class of involutions with
  underlying quotient (S^3), so their branch links are equivalent.
* In the nonspherical case a branching involution can be made fiber preserving.
  If it preserves fiber orientation, its branch link has Seifert-fibered
  exterior. If it reverses fiber orientation, the branch link is Montesinos.
* Montesinos branch links with the same Seifert cover are related by Conway
  mutations.

For the reduced pair, the fiber-orientation-preserving alternative is excluded
because the branch exteriors are hyperbolic. Thus both links are Montesinos and
are mutants. Menasco's mutation theorem preserves alternation, a contradiction.
K3 (2026), Problem 1.17, Remark (3), already explicitly records this Seifert
sector exclusion; Remark (1) gives the exact Menasco reference. We claim only
this credited consequence, not a new proof of the underlying action
classification or a classification of arbitrary graph-manifold actions.

Geometrization now says that an atoroidal such (Y) is hyperbolic: the Seifert
alternative has just been excluded. If it is not atoroidal, it is toroidal and
non-Seifert. This leaves two genuine common-cover sectors. In the hyperbolic
sector Turn 1 gives the finite isometry-group restrictions. In the toroidal
sector one must still understand the actual global action on the JSJ pieces
and their gluing; knowing the pieces alone does not identify the branch links.

## 3. A determinant-five alternating-cover lemma

**Lemma.** If (L) is an alternating link and

\[
 |H_1(\Sigma_2(L);\mathbb Z)|=5,
\]

then its cover is a lens space. More explicitly, up to reflection its reduced
diagram is the five-crossing two-strand torus diagram or the figure-eight
diagram. This statement includes links a priori, not just knots.

**Proof.** A split link has a free (\mathbb Z) summand in cover homology, so
(L) is nonsplit. Choose a connected reduced alternating diagram and its Tait
multigraph (G). The graph is connected, loopless and bridgeless; the determinant
equals its spanning-tree count (\tau(G)=5). The edge bound proved in Turn 3 is

\[
 |E(G)|\leq\tau(G)=5.                                             \tag{3.1}
\]

Tree counts multiply over cut-vertex blocks. Every nonempty block of a
bridgeless loopless graph contains a cycle and has at least two spanning trees.
Since 5 is prime, (G) has only one block.

If (G) has two vertices, its five edges are all parallel. If it is a cycle,
it is the five-cycle. Otherwise it has at least three vertices and, being
2-connected, has a cycle of length at least three. Start an open ear
decomposition from such a cycle. The first ear makes a theta graph with
positive arm lengths (a,b,\ell), where (a+b\geq3). Its spanning-tree count is

\[
 ab+a\ell+b\ell.
\]

For (a+b=c\geq3), this is at least (c-1+c\ell\geq2c-1). To be at most 5
requires (c=3), (\ell=1), and \(\{a,b\}=\{1,2\}\). Thus the theta graph is
\(\Theta(1,1,2)\), with exactly five spanning trees. Every additional ear
strictly increases the count, by the ear argument in Turn 3, so no further ear
is possible.

These are precisely three abstract graphs: the five-fold parallel pair, its
planar dual (C_5), and the triangle with one doubled edge
\(\Theta(1,1,2)\). Their plane embeddings yield, up to reflection, respectively
the standard (T(2,5)) diagram and the standard figure-eight diagram. One can
see this directly by replacing a parallel family by its twist region; for the
theta graph its dual has the same three arm lengths, producing the two
two-crossing twist regions. These are two-bridge links, with fractions 5 and
5/2 up to the usual two-bridge equivalences. Their covers are lens spaces with
first-homology order 5. This proves the lemma. ∎

The accompanying checker enumerates every loopless bridgeless multigraph with
at most five edges, independently comparing Laplacian determinants with direct
spanning-tree enumeration. It confirms the three graphs. The written graph
argument, not a finite sampling assumption, supplies completeness.

## 4. Explicit gluing of two trefoil exteriors

Let (E_1,E_2) be oriented exteriors of the right-handed trefoil in (S^3).
On each boundary fix the usual oriented meridian–preferred-longitude basis
\((\mu_i,\lambda_i)\). A rational slope (p/q) means the unoriented primitive
class (p\mu_i+q\lambda_i); the meridian is (\infty).

Choose an orientation-reversing boundary homeomorphism (h\) with

\[
 h_*(\mu_1)=3\mu_2+\lambda_2,\qquad
 h_*(\lambda_1)=-5\mu_2-2\lambda_2,
 \qquad
 A=\begin{pmatrix}3&-5\\1&-2\end{pmatrix}.                          \tag{4.1}
\]

Here columns are the images of the ordered basis. Since (\det A=-1), these
data specify the required boundary map. Set

\[
 Y=E_1\cup_h E_2.
\]

The boundary inclusions send (\lambda_i) to zero in (H_1(E_i;\mathbb Z))
and (\mu_i) to a generator. Mayer–Vietoris therefore presents first homology
by generators (x_1,x_2) with relations

\[
 x_1=3x_2,\qquad 5x_2=0.
\]

Consequently (H_1(Y;\mathbb Z)\cong\mathbb Z/5). This computes the whole
group, not just a determinant.

Trefoil exteriors are irreducible with incompressible boundary. Gluing two
irreducible manifolds along incompressible tori yields an irreducible manifold,
and the gluing torus remains incompressible. For example, put a sphere or a
purported compressing disk in minimal transverse position with the gluing
torus. An innermost intersection gives a disk in one piece; incompressibility
and irreducibility remove that intersection. A remaining sphere bounds a ball
in a piece and a remaining compression contradicts boundary incompressibility.
Thus (Y) is irreducible and toroidal. In particular, it is not a lens space.

## 5. The L-space calculation, including the meridian

The right trefoil's L-space filling slopes are

\[
 \mathcal L(E_i)=[1,\infty]\cap\mathbb QP^1,
 \qquad \mathcal L^\circ(E_i)=(1,\infty),                         \tag{5.1}
\]

where these intervals are the positive-side arc of the projective slope
circle. In particular (\infty) belongs to the closed interval, but is not an
interior point: approaching it from negative rational slopes gives non-L-space
fillings. This endpoint matters in the gluing calculation.

For a precise classical computation of (5.1), the three-generator right-trefoil
knot Floer staircase has (\nu=1) and
\(\operatorname{rank}H_*(\widehat A_s)=1\) for every integer (s). Substitution
in Ozsváth–Szabó (2011), Proposition 9.6, formula (40), gives, for coprime
(p\neq0\), (q>0\),

\[
 \operatorname{rank}\widehat{HF}(S^3_{p/q}(T_{2,3}))
   =p+2\max(0,q-p).                                               \tag{5.2}
\]

This equals (\lvert p\rvert\) exactly when (p\geq q\). For (p<0) it is
(2q-p>|p|\); for (0<p<q) it is (2q-p>p\). Zero surgery has positive first
Betti number, and meridional filling is (S^3\). Equation (5.1) follows.
Hanselman–Rasmussen–Watson's author manuscript also depicts the right-trefoil
curve in Figure 2 and uses the interval (5.1) in its small-toroidal-L-space
classification, Theorem 7.20. We use this established trefoil computation,
not a new Floer-homology algorithm.

The rational projective complement of the interior L-space interval is

\[
 D=(-\infty,1]\cup\{\infty\}.
\]

From (4.1) the slope map is

\[
 h(r)=\frac{3r-5}{r-2}=3+\frac1{r-2}.
\]

For real (r\leq1), this lies in ([2,3)\), and (h(\infty)=3\).
Consequently

\[
 h(D)=[2,3]\subset(1,\infty)=\mathcal L^\circ(E_2).                \tag{5.3}
\]

The Hanselman–Rasmussen–Watson L-space gluing theorem (author-manuscript
Theorem 1.14; published Theorem 13, also quoted as Boyer–Gordon–Hu v5
Theorem 4.4) applies because the pieces have incompressible torus boundary and
the gluing reverses orientation. Condition (5.3) is equivalent to

\[
 h(\mathcal L^\circ(E_1))\cup\mathcal L^\circ(E_2)=\mathbb QP^1.
\]

It proves that (Y) is an L-space. There is no use of the L-space conjecture,
left-orderability as a surrogate, or the false assertion that meridional
filling itself is a non-L-space. The meridian is in (D) only as an endpoint
of the complement of the **interior** interval.

## 6. An actual (S^3) quotient

It remains essential to realize a branching involution on this particular
(Y); an abstract matrix or a pair of nonequivariant fillings would not do.

In (S^3\subset\mathbb C^2\), realize the trefoil by

\[
 t\longmapsto 2^{-1/2}(e^{2it},e^{3it}).
\]

Complex conjugation
\(\iota(z,w)=(\overline z,\overline w)\) is an orientation-preserving
involution of (S^3\), with fixed unknotted circle (S^3\cap\mathbb R^2\).
It sends the trefoil parameter (t\) to (-t\) and meets the trefoil at just
(t=0,\pi\). Thus it is a standard strong inversion. The quotient (S^3/\iota)
is (S^3\), as is seen from the standard half-turn about this unknotted circle.
An invariant tubular neighborhood of the trefoil has quotient a regular
neighborhood of an arc, hence a ball. Its complementary quotient is also a
ball by the smooth Schoenflies theorem. Therefore

\[
 E_i/\iota_i=B^3
\]

with branch locus a two-string tangle, and the boundary action has four fixed
points. In appropriate marked torus coordinates it is (x\mapsto-x\).
One may choose these coordinates with the specified meridian and longitude:
after linearizing the elliptic involution, an integral change of marking
commutes with (-I\).

Take the **linear** representative of (4.1) in these coordinates. It commutes
exactly with (-I\), not just on homology, so (h\iota_1=\iota_2h\) on the
boundary. The two involutions consequently glue to a smooth involution
(\iota\) on (Y\). Boundary collars may be chosen equivariantly, and the
fixed tangle endpoints match to give smooth closed branch curves. Its quotient
is

\[
 Y/\iota=B^3\cup_{\bar h}B^3\cong S^3.
\]

This is an explicit finite tangle/pillowcase gluing construction of a link
(J\subset S^3\) with (\Sigma_2(J)=Y\). No identification by numerical
invariants, extension of an arbitrary boundary involution, or unproved
surjectivity of a quotient construction has been assumed.

In fact (J\) is a knot. For an (m\)-component link,

\[
 \dim_{\mathbb F_2}H_1(\Sigma_2(J);\mathbb F_2)=m-1.
\]

One elementary proof uses the abelianized branched Wirtinger presentation:
the Fox-coloring relations (2a_{\rm over}-a_{\rm under,1}-a_{\rm under,2}=0\),
with one base color fixed to zero, present cover homology. Modulo 2 these
identify the successive under-arcs on each link component, with no relations
between different components. There is thus one free color per component,
minus the fixed base color. Since (H_1(Y)=\mathbb Z/5\), the left side is zero.

Irreducibility of (Y\) and the connected-sum cover formula imply that (J\)
is prime: a nontrivial connected-sum decomposition would give nontrivial cover
summands, because the only link with cover (S^3\) is the unknot. It is
nontrivial since its cover has nontrivial first homology.

## 7. Every branch is nonalternating; the constructed exterior is hyperbolic

If any alternating link had cover (Y\), Section 3 would make (Y\) a lens
space. Section 4 supplies an essential torus, a contradiction. In particular
the concrete knot (J\) is nonalternating.

We can also determine the geometry of its **exterior**, using the exact
inputs already checked in Turn 3. If that exterior were toroidal, the
Boyer–Gordon–Hu degree-two theorem would make (Y\) a non-L-space. If it were
Seifert fibered, their Seifert-link theorem and the L-space property would force
an ADE link. The (D/E\) cases have determinant at most 4 (using our independent
Cartan/Goeritz calculation, including the v1 table correction retained in
Turn 3). The (A\) case is a two-strand torus link with lens-space cover.
Neither can give this toroidal (Y\) of homology order 5. Thus the prime knot
(J\) has hyperbolic exterior by geometrization.

This proves concretely that a prime hyperbolic nonalternating knot can have
an irreducible toroidal L-space double cover. It does **not** give a cover
shared with an alternating link, and it cannot be used as one.

## 8. Credit, checked source editions, and exact remaining gap

The full author manuscript of Hanselman–Rasmussen–Watson,
*Bordered Floer homology for manifolds with torus boundary via immersed curves*,
has gluing Theorem 1.14 and classification Theorem 7.20 on printed pp. 82–84.
The published paper is JAMS 37 (2024), 391–498; Boyer–Gordon–Hu's full v5
manuscript identifies the corresponding published statements as Theorems 13
and 57. There are precisely four prime toroidal L-spaces with first-homology
order 5, all glued from trefoil exteriors. Our example is within that already
known class. We do not assert a new classification or assign it a distinct
catalog name.

The downloaded full published Ozsváth–Szabó source is AGT 11 (2011), 1–68,
Proposition 9.6 on printed p. 51. The conventions, including negative (p\)
and the meridional endpoint, are made explicit above. The Seifert branching
classification is read in the full published Mecchia–Reni (2002) introduction
and separately in the exact K3 source remark. The precise BGH versions remain
the v1 2024 Seifert manuscript and v5 2026 toroidal manuscript described in
Turn 3; no full inaccessible publisher PDF is claimed.

The unresolved problem is still to transport alternation between *actual*
(S^3\)-quotient involutions on a possible common cover, or to construct a
mixed pair. The prime reduced cover may be hyperbolic, where the finite-group
restrictions of Turn 1 apply, or toroidal non-Seifert, where global JSJ-action
compatibility remains essential. The present example shows why replacing
that problem by the L-space condition cannot complete the proof.

No claim is made that every toroidal L-space has no alternating branch, that
all graph-manifold involutions are mutations, or that the nonalternating
branch's exterior geometry determines the cover geometry. Those would go
beyond what has been proved.
