# A rotational obstruction to prescribed-end Veech realization

Problem 30002555 / OWR-12875-003. Author candidate, 7 October 2026.

## 1. Result and precise scope

The universal realization assertion in Ferrán Valdez's Question 4, printed
page 887 of Oberwolfach Report 15/2014 [OWR], has a **negative answer**.
The following explicit admissible pair is a counterexample:

\[
 X=\{0,2/3,1\}\subset C,\qquad
 A=\frac15\begin{pmatrix}3&-4\\4&3\end{pmatrix},\qquad
 G=\langle A\rangle\leq\mathrm{GL}^{+}(2,\mathbb R).
\]

Here C is the usual middle-thirds Cantor set. The group G is countably
infinite and has no contracting elements. Nevertheless, no tame
infinite-genus translation surface S with no planar ends and
\(\operatorname{Ends}(S)\cong X\) has Veech group G. In fact its Veech
group cannot even contain A.

The obstruction is a direct consequence of classical uniformization and
proper discontinuity of conformal automorphisms, combined with a
three-ended compact core. The relevant translation-surface finiteness
principle is already explicitly proved in Artigiani, Randecker, Sadanand,
Valdez and Weitze-Schmithüsen [ARSVW, Theorem 1.8; Corollary 2.19].
This note gives a full reduction, an explicit rational matrix, and the
underlying proper-discontinuity argument. **No mathematical priority or
new general classification is claimed.**

## 2. Conventions and the metric bridge

A surface here is connected, orientable, second countable, and without
boundary. Genus is infinite when there are compact subsurfaces of
arbitrarily large genus. An end is a compatible choice of a component
outside each sufficiently large compact set. An end is accumulated by
genus if every end-neighborhood has positive genus. There are no planar
ends precisely when every end has this property.

A translation structure has transition maps z -> z+c on its regular
locus. Its Euclidean length metric may be incomplete. In the convention
including finite cone points, those points form a discrete subset of
the underlying surface and have angles 2*pi*k for positive integers k.
The complex structure extends across such a point using a local
coordinate w with translation coordinate proportional to w^k. Thus the
underlying surface is a Riemann surface, possibly with zeros of its
holomorphic one-form. If instead the underlying S in a convention
omits those points, S itself already has a Riemann surface structure;
we do not silently change its end space by adjoining them.

Tameness restricts the metric completion: its missing points have only
finite or infinite conical local models, with no wild singularities.
Infinite-angle completion points are not adjoined as ordinary surface
points in this argument. The proof uses the exact underlying topological
surface in the end-space condition. Its conformal structure exists on
that surface, whether or not the flat metric is complete. No assertion
that the metric completion is a surface is used.

Let Aff^+(S) be the orientation-preserving affine automorphism group,
and let D be its constant derivative. We use the full matrix Veech group

\[
 \Gamma(S)=D(\operatorname{Aff}^{+}(S))\leq\mathrm{GL}^{+}(2,\mathbb R),
\]

not its projectivization. Define
\(I(S)=D^{-1}(\mathrm{SO}(2))\).
An element of I(S) preserves flat lengths: in every regular chart its
linear part is orthogonal, and applying the inverse proves equality of
intrinsic distances. Its local formula is z -> lambda*z+b with
|lambda|=1, hence it is conformal. At included finite cone points it
extends conformally in the w-coordinate; equivalently the bounded local
holomorphic map extends across the puncture, as does its inverse.
Consequently

\[
 I(S)\leq\operatorname{Aut}_{\mathrm{hol}}(S),\qquad
 D(I(S))=\Gamma(S)\cap\mathrm{SO}(2).                 \tag{1}
\]

This is exactly the isometry subgroup convention of [ARSVW, Section 3.1].
It neither supposes trivial translation kernel nor requires a chosen
homomorphic lift of the Veech group. Surjectivity onto the intersection
in (1) is enough.

The source's contraction convention is strict shortening of every
nonzero Euclidean vector, equivalently Euclidean operator norm less
than one. We do not confuse it with determinant less than one. Our
witness has determinant one and preserves every vector norm, so it is
noncontracting under either potentially relevant strict-shortening
convention. No area hypothesis or area normalization is added.

## 3. Proper discontinuity, with completeness accounted for

**Lemma 1.** If R is an infinite-genus Riemann surface, then its group of
holomorphic automorphisms acts properly discontinuously in the compact-set
sense: for every compact K in R, only finitely many automorphisms f satisfy
f(K) intersect K nonempty.

**Proof.** We use the classical Poincaré--Koebe uniformization theorem and
elementary facts about covering maps and Möbius transformations. The
fundamental group of an infinite-genus surface is nonabelian. Its simply
connected conformal cover cannot be the sphere: a nonidentity holomorphic
Möbius transformation of the sphere has a fixed point, whereas a nonidentity
deck transformation acts freely. It cannot be the plane either: a
holomorphic automorphism of the plane is z -> az+b, and if a != 1 it has
a fixed point. A freely acting deck group on the plane therefore consists
of translations and is abelian. Both alternatives contradict infinite
genus. Thus R=H/Lambda, where H is the upper half-plane and Lambda is a
nonabelian discrete group of real orientation-preserving Möbius
transformations acting freely.

Let N be the normalizer of Lambda in PSL(2,R). Every automorphism of R
lifts to a conformal automorphism of H, and every such lift normalizes
Lambda; conversely a normalizing transformation descends. Therefore
Aut_hol(R)=N/Lambda.

We check that N is discrete. Choose noncommuting a,b in Lambda. If N
were nondiscrete there would be distinct nonidentity n_j in N with
n_j -> 1. Then n_j*a*n_j^(-1) -> a, with all terms in the discrete group
Lambda, so these terms eventually equal a. The analogous assertion holds
for b. Thus eventually n_j commutes with both a and b. The centralizer
in PSL(2,R) of any nonidentity element is abelian: after conjugacy this
is the rotation subgroup, the diagonal subgroup, or the parabolic
translation subgroup, according to its elliptic, hyperbolic, or parabolic
type. If n_j were nonidentity, a and b would belong to its abelian
centralizer, contradicting their choice. Hence such a sequence cannot
exist, and N is discrete.

A discrete subgroup of PSL(2,R) acts properly discontinuously on H in
the compact-set sense. For completeness, PSL(2,R) acts properly on H:
a compact set of possible image positions together with the compact
rotation stabilizer of a point confines its transporter between two
compact subsets of H to a compact subset of PSL(2,R). A discrete subgroup
meets such a compact transporter in finitely many points.

Now let K be compact in R. Finitely many relatively compact evenly
covered coordinate neighborhoods produce a compact L in H whose image
contains K. If an automorphism coset [n] satisfies [n](K) intersect K
nonempty, choose lifts u,v in L of a witnessing pair of points. For
some lambda in Lambda, n*u=lambda*v, so lambda^(-1)*n has its L-image
meeting L. There are only finitely many such elements of N, and hence
only finitely many cosets [n]. This proves the lemma. No completeness of
the original flat metric was assumed. QED.

This is the uniformization mechanism behind [ARSVW, Theorem 2.18 and
Corollary 2.19]. It is restated here to make the bridge to incomplete
flat metrics explicit; it is not a new proper-discontinuity theorem.

## 4. The nondisplaceable finite-ended core

**Lemma 2.** Let S be an infinite-genus surface with exactly n ends, all
accumulated by genus, where 3 <= n < infinity. There is a compact connected
subsurface K such that h(K) intersects K for every homeomorphism h of S.

**Proof.** Take a compact connected genus-zero surface with n boundary
circles, and attach along each boundary a one-ended infinite-genus
surface with one boundary circle. Call the resulting surface B_n, and
let K be the compact central surface. The complement B_n minus K has
n connected components U_1,...,U_n, each carrying exactly one end.
All those ends are accumulated by genus. The classical classification
of orientable surfaces by genus and the nested end/genus-end spaces
identifies S with B_n; see the precise classification recalled in
[RMV, Theorem 1.2]. Transport K to S.

Suppose h(K) were disjoint from K. Since h(K) is connected, it lies
inside one component U_i of S minus K. The connected set consisting of
K together with all U_j for j != i is disjoint from h(K). It therefore
lies in a single component of S minus h(K), and carries at least
n-1 >= 2 distinct ends. On the other hand h is a homeomorphism, so
S minus h(K) has n components, each carrying exactly one end, just as
S minus K does. This is a contradiction. QED.

There is no assertion here that every compact subsurface is
nondisplaceable, or that the analogous core works when n=1 or n=2.
For two ends the last inequality fails, exactly where it should.

**Proposition 3.** Under Lemma 2's hypotheses, I(S) is finite for every
translation structure on S. In particular,
\(\Gamma(S)\cap\mathrm{SO}(2)\) is finite.

**Proof.** By (1), I(S) consists of holomorphic automorphisms of the
Riemann surface S. By Lemma 1, only finitely many of them can move the
compact set K to meet itself. Lemma 2 says that every one of them must
do so. Thus I(S) is finite, and so is its derivative image (1). QED.

Proposition 3 is the finite-ended specialization of the already-credited
nondisplaceable-subsurface theorem [ARSVW, Theorem 1.8].

## 5. An exact noncontracting infinite cyclic matrix group

Direct multiplication gives A^T*A=I and det(A)=1. Thus all integral
powers of A lie in SO(2), and every element of G preserves Euclidean
length. The integer parametrization of G makes it countable.

We prove that A has infinite order without a numerical assertion about
its rotation angle. Write B=5*A, so

\[
 B=\begin{pmatrix}3&-4\\4&3\end{pmatrix},\quad
 B^2-6B+25I=0.
\]

For u_n=tr(B^n), Cayley--Hamilton gives

\[
 u_0=2,\qquad u_1=6,\qquad
 u_{n+1}=6u_n-25u_{n-1}\quad(n\geq1).
\]

Modulo 5, u_1=1 and u_{n+1}=u_n, so induction yields u_n=1 modulo 5
for every n>=1. If A^n=I for some n>=1, then B^n=5^n I and
u_n=2*5^n=0 modulo 5, a contradiction. Hence G is infinite cyclic,
and in particular countably infinite and admissible in the source.

Now X={0,2/3,1} is a nonempty closed three-point subset of the Cantor
set. Any surface satisfying the source's topological requirements for
this X falls under Proposition 3 with n=3. If its Veech group contained
A, its intersection with SO(2) would contain the infinite subgroup G,
contradicting Proposition 3. Therefore no such surface realizes G.
This is a genuine nonempty-end counterexample, not the vacuous empty-X
edge case. It disproves the universal assertion. QED.

## 6. What this does and does not settle

- The negative answer covers the question's exact embedded matrix-group
  formulation. It does not classify all groups realizable for each X.
- It does not prohibit an abstract infinite cyclic Veech group generated
  by a nonorthogonal matrix. Replacing prescribed matrices by abstract
  group isomorphism changes the question.
- The obstruction also survives conjugating the entire prescribed group:
  postcomposing translation charts by an invertible positive-determinant
  matrix conjugates Veech groups and preserves topology. The resulting
  flat metrics are bilipschitz equivalent, which identifies their metric
  completions. Tameness is preserved for an additional geometric reason:
  a finite or infinite cyclic cone developing map to a punctured round
  disk, followed by the linear change, becomes the same cyclic cover
  over a punctured ellipse. Restrict to a sufficiently small round disk
  inside that ellipse. With the new pulled-back Euclidean metric this
  is precisely the required finite or infinite cyclic cone neighborhood.
  Regular points remain regular. Thus bilipschitz equivalence alone is
  not being used to assert preservation of an exact conical local model.
  Alternatively the compact-core argument works directly for an
  invariant positive-definite quadratic form.
- It says nothing negative about the tame Loch Ness monster or blooming
  Cantor-tree realizations, which have no such finite-ended core.
- No conclusion about the lattice realization question on Jacob's ladder
  follows, and no finite-area lattice existence claim is made.
- The proof does not rely on the translation kernel being trivial,
  finiteness of the cone set, finite area, a complete flat metric,
  finite generation of G beyond the chosen witness, or a surface action
  of the derivative group itself.

The deep classical dependencies are uniformization and the topological
classification of orientable surfaces. All remaining reductions and
matrix calculations are proved above. The existing finite-isometry
result gives an independent source-level check of the reduction.
Bounded exact computations in CHECKS.py supplement, but do not prove,
the universal statements in Lemmas 1--2 or the induction in Section 5.

## References

[OWR] Ferrán Valdez (joint work with Camilo Ramírez Maluendas), contribution
“Veech groups of infinite type surfaces,” in *Flat Surfaces and Dynamics
on Moduli Space*, Oberwolfach Reports 11 (2014), 869--941; contribution
885--888, Question 4 at 887. DOI: https://doi.org/10.4171/OWR/2014/15 .
Primary PDF: https://ems.press/content/serial-article-files/46504 .

[RMV] Camilo Ramírez Maluendas and Ferrán Valdez, *Veech groups of
infinite-genus surfaces*, Algebraic & Geometric Topology 17 (2017),
529--560. https://doi.org/10.2140/agt.2017.17.529 .
Primary PDF: https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf .

[ARSVW] Mauro Artigiani, Anja Randecker, Chandrika Sadanand, Ferrán Valdez,
and Gabriela Weitze-Schmithüsen, *Realizing groups as symmetries of
infinite translation surfaces*, arXiv:2311.00158v2 (23 February 2026).
https://arxiv.org/abs/2311.00158v2 . The inspected author's publication
page labels it “To appear in Algebraic & Geometric Topology”; no final
journal version was used: https://m-artigiani.github.io/research/papers/ .
