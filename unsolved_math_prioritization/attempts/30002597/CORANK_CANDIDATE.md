# A complete decision criterion via free quotients

**Complete candidate from substantive author attempt 1; separate review pending.**
This is an application of classical theorems, not a claimed new algorithm,
historical first, or proof of a new classification of cobordism classes.
It addresses existence for every prescribed curve, rather than merely
disproving universal existence. The earlier source-only audit did not contain
this argument; its unresolved-by-that-audit qualification must not be treated
as a theorem that no decision algorithm is known.

## 1. Exact theorem and input

Let S be a closed, connected, oriented smooth surface of genus g, and let
gamma: S^1 -> S be a generic smooth immersion. Its only self-intersections
are finitely many transverse double points. Let

```
G_gamma = pi_1(S) / <<[gamma]>>,
```

where `<< >>` is normal closure. A choice of path to a basepoint changes the
element by conjugation, so this quotient does not depend on that choice.
Define `corank(G)` as the greatest rank of a free group which is an epimorphic
image of G; the trivial free group has rank zero.

**Theorem.** The following conditions are equivalent:

1. There is a compact 3-manifold M with boundary identified with S and a
   smooth map `f: D^2 -> M` restricting to the prescribed parametrized gamma,
   with `f^-1(boundary M)=boundary D^2`, and only the usual stable generic
   surface-to-3-manifold singularities
2. There is an oriented genus-g handlebody H with boundary identified with S
   in which gamma is null-homotopic
3. `corank(G_gamma)=g`

Orientability of M need not be assumed in (1). A coefficient-free
equation-system algorithm computes the corank in (3), giving a terminating
yes/no procedure for every finite combinatorial encoding of `(S,gamma)`.
No bound on the number of crossings, genus, or allowed singularities is imposed.

For the decision input, one can give a triangulated surface with a finite PL
curve diagram, or equivalently the genus together with the word of gamma in
a standard marked surface group. The latter is computable from the former.
The criterion applies mathematically to every smooth generic curve, since it
depends on its finite homotopy word. No algorithm is claimed for an unspecified
noncomputable oracle representation of a smooth map.

## 2. Stable maps and null-homotopies

Every disk map is a null-homotopy of its boundary. Conversely, if gamma is
null-homotopic in a smooth 3-manifold with gamma on its boundary, use a collar
`S x [0,epsilon)` to prescribe the map near the disk boundary by
`(z,t) -> (gamma(z),t)`. The inner collar circle is still null-homotopic, so
extend it across the remaining disk. Push the interior away from the manifold
boundary, smooth relative to the prescribed collar, and apply relative
general position on the interior.

The resulting map has regular sheets, normal-crossing double curves, isolated
normal-crossing triple values, and isolated simple branch points (Whitney
umbrellas). The collar gives exactly the regular and double half-sheet models
at the boundary, because gamma is already a generic immersion. The boundary
map is unchanged, not merely replaced by a homotopic curve, and the source
remains a disk. These are the stable local models in the source problem.
Relative general position is explicitly recalled in Funar, proof of Lemma 4.1,
pp. 302–303; the model/stability description is also in Ben Hadar,
Definition 1.1, pp. 1675–1676. See the linked references below.

In particular this argument does **not** remove branch points by adding
handles to the source. Such a change of source would invalidate the disk
condition. It also does not claim an everywhere immersed or embedded disk.

## 3. Removing the ambient-orientability ambiguity

Suppose (1) holds in a nonorientable M. Retain its connected component
containing S and take its orientation double cover. Since the outward normal
line to S is trivial and S is orientable, that cover restricts on S to two
disjoint copies of S. The disk map lifts, because D^2 is simply connected.
Its boundary lies on one copy and is the prescribed gamma under the covering
identification. Cap the other copy by an oriented handlebody. This gives a
compact oriented 3-manifold with exactly the selected S as boundary, without
changing the lifted disk. The boundary-preimage condition is preserved.
Reorient the cover, if needed, to induce the prescribed orientation on S.

Thus existence in arbitrary M implies existence in an oriented filling. The
reverse implication is immediate.

## 4. Any oriented filling can be replaced by a handlebody

We spell out the standard boundary-compression argument behind the handlebody
reduction noted by Carter on p. 879.

Let W be a compact connected oriented 3-manifold with boundary S. Begin with
an inward collar of S. Successively compress its inner boundary along
compressing disks in the remaining part of W, adding neighborhoods of those
disks to the collar region C. Stop when no positive-genus inner boundary
component admits a compressing disk. This process is finite: a compression
strictly decreases the sum of `2*genus(F)-1` over positive-genus inner
components F. Sphere components contribute zero and need not bound balls in W.

The resulting C is a (possibly sphere-punctured) compression body with outer
boundary S. Every component F of its inner boundary is pi_1-injective into
the remaining piece: for positive genus this is the Loop Theorem, and for a
sphere it is automatic. Each F is also pi_1-injective into C, as follows from
the description of a compression body as products on its inner boundary with
1-handles attached. If the complement has several components, retain all of
them in this decomposition.

Van Kampen describes W as a graph of groups with vertex group pi_1(C), other
vertex groups from the remaining components, and edge groups pi_1(F). Both
edge maps are injective. The amalgam/HNN normal-form theorem therefore makes
`pi_1(C) -> pi_1(W)` injective. Consequently **every** loop in S that is
null-homotopic in W is already null-homotopic in C. This does not assume that
`pi_1(S) -> pi_1(W)` is surjective or that W is irreducible.

Now fill every inner boundary component of C by a handlebody, using a 3-ball
for a sphere. These are newly chosen fillings; no assertion that a sphere
bounded a ball inside W is needed. Reversing the compression-body handle
description shows that the filled manifold H is a connected handlebody whose
outer boundary is S, hence whose genus is g. Loops killed in C remain killed
in H. Applying this to gamma proves `(1) => (2)`, after Section 3.
Section 2 gives `(2) => (1)`.

## 5. Handlebody equivalence with maximal free corank

First, `corank(pi_1(S))=g`. For completeness, a surjection to F_r induces an
injection of r-dimensional rational H^1 into H^1(S;Q). Its image has zero cup
product, since H^2(F_r;Q)=0. The surface intersection pairing is symplectic
of dimension 2g, so r<=g. The standard handlebody quotient attains g.
Therefore every quotient G_gamma also has corank at most g.

If gamma is killed in a genus-g handlebody, the boundary epimorphism to
`pi_1(H)=F_g` factors through G_gamma. Thus its corank is at least g, proving
`(2) => (3)`.

Conversely suppose (3). Compose an epimorphism `G_gamma -> F_g` with the
quotient from pi_1(S). Leininger–Reid, Lemma 2.2, states precisely that every
epimorphism `pi_1(S_g) -> F_g` is induced by inclusion into a genus-g
handlebody after a boundary homeomorphism. Identify that boundary with the
prescribed S. The composite kills gamma, so gamma is null-homotopic there.
This gives `(3) => (2)`.

The genus-zero case is immediate: S is a sphere, G_gamma is trivial, and any
gamma is null-homotopic in a 3-ball. For genus one the same statement applies
with F_1=Z. More explicitly, if gamma has homology vector `(p,q) != (0,0)`,
the primitive slope `(p/d,q/d)`, `d=gcd(p,q)`, can be the meridian of a solid
torus. If `(p,q)=(0,0)`, any solid-torus filling suffices.

## 6. The terminating decision algorithm

Choose the standard presentation

```
pi_1(S_g) = <a_1,b_1,...,a_g,b_g | R_g = product_i [a_i,b_i] = 1>,
```

and compute a word w representing gamma. Introduce **2g unknowns**, with no
fixed group coefficients, and form the finite system

```
R_g(X_1,Y_1,...,X_g,Y_g) = 1,
w(X_1,Y_1,...,X_g,Y_g) = 1.
```

Razborov's rank of this system is the maximum rank of the free subgroup
generated by a solution tuple in a free group. His Section 9, Theorem 3,
gives an algorithm that computes this integer and terminates for every such
finite coefficient-free system.

This is exactly `corank(G_gamma)`, not ordinary generator rank, abelianization
rank, matrix rank, or merely the existence of a nontrivial solution. Indeed:

- Every solution tuple defines a homomorphism from the ordinary finitely
  presented G_gamma onto the subgroup generated by that tuple; that subgroup
  is free and has the solution's rank
- Every free quotient of G_gamma supplies such a solution by taking images
  of the 2g generators in a free group

Razborov also uses a radical coordinate group in his paper. It does not change
this argument: the above two statements concern the actual solutions, and his
Lemma 1.2 and its following remark explicitly allow the ordinary finite
presentation. No assumption that G_gamma itself is residually free is made.

The algorithm is therefore:

1. For g=0 return YES
2. Form the system above and run the published rank algorithm to obtain r
3. Return YES if r=g, otherwise return NO

By Section 5, `r<=g`. By Sections 2–5, the answer is correct in both
directions and handles a prescribed parametrized boundary with stable
singularities. The decision step is a genuine terminating imported algorithm,
not an endless enumeration of successful examples or an undecided rank oracle.
No feasible complexity bound or runnable implementation of Razborov's
algorithm is claimed by this package.

If a positive algebraic witness is desired, after a YES one may enumerate
2g-tuples of words in F_g, check the two relations by free reduction, and
check generation of F_g by Stallings folding. A successful tuple must occur.
The geometric-realization theorem then supplies H. Blackwell–Kirby–Klug–Longo–
Ruppik (2025), Theorem 2.10 with b=0, additionally supplies an explicit
algorithm for constructing its diagram from this epimorphism. This optional
witness recovery is not needed to make the yes/no decision terminate.

## 7. Consequences, checks, and attribution

This criterion decides the existence question for arbitrary finite inputs; it
does not assert that all inputs receive YES. Carter's genus-two counterexample
has NO, consistently with its nonzero u-polynomial. Nor does it classify all
virtual-string cobordism classes or supply an efficient small list of
diagrammatic obstructions. Such questions are different from disk-existence
decision for a prescribed curve.

The toy verifier checks the coefficient-free word encoding, positive free
quotient witnesses in all tested genera, normal-closure invariance controls,
and the primitive-slope genus-one calculation. It does not implement or test
the complete rank algorithm. The old three-crossing calculation remains an
independent negative control, not a substitute for the decision theorem.

The main ingredients are classical. Carter already states the handlebody
reduction; maximal-rank surface epimorphisms are classical geometric
realizations; Razborov's rank algorithm predates the OWR report. Sikora
explicitly notes computability of finitely presented-group corank. Therefore
this package makes **no claim of a new algorithm or historical priority**.
Its contribution is a checked reduction resolving the imported existence/
decision formulation by established results, if the separate audit confirms
the argument and exact scope.

## References and exact access

- J. S. Carter, *Closed curves that never extend to proper maps of disks*,
  Proc. Amer. Math. Soc. 113 (1991), 879–888, p. 879 and Theorem 1.1.
  [Author-posted primary text](https://www.researchgate.net/publication/243064762_Closed_Curves_That_Never_Extend_to_Proper_Maps_of_Disks)
- C. J. Leininger and A. W. Reid, *The co-rank conjecture for 3-manifold
  groups*, Algebraic & Geometric Topology 2 (2002), 37–50, Lemmas 2.1–2.2,
  pp. 39–40. Complete PDF recovered and relevant page rendered.
  [Paper](https://arxiv.org/pdf/math/0202261)
- A. A. Razborov, *On systems of equations in a free group*, Math. USSR-Izv.
  25 (1985), 115–162; Russian original 1984. Section 9 begins p. 151;
  Theorem 3 and its proof are pp. 156–158; finite-presentation remark p. 117.
  Complete 48-page primary PDF text was accessible in the web reader; local
  PDF download returned HTTP 403. The exact theorem and its rank definition
  were read, rather than inferred from a secondary abstract.
  [Primary PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=im&paperid=1492&what=fullteng)
- A. S. Sikora, *Cut numbers of 3-manifolds*, Trans. Amer. Math. Soc. 357
  (2005), 2007–2020, introduction; corroborates arbitrary finite-presentation
  corank computability with an explicit reference to Razborov Section 9.
  [Complete preprint](https://arxiv.org/pdf/math/0112106v2)
- S. Blackwell, R. Kirby, M. Klug, V. Longo, B. Ruppik,
  *A group-theoretic framework for low-dimensional topology*, Algebraic &
  Geometric Topology 25 (2025), 4667–4718, Definition 2.1 and Theorem 2.10.
  Complete published PDF recovered; used only for optional diagram recovery.
  [Publisher PDF](https://msp.org/agt/2025/25-8/agt-v25-n8-p07-s.pdf)
- L. Funar, *Surface cubications mod flips*, Manuscripta Math. 125 (2008),
  285–307, proof of Lemma 4.1, pp. 302–303.
  [Primary paper](https://www-fourier.univ-grenoble-alpes.fr/~funar/2008manuscripta.pdf#page=18)
- D. Ben Hadar, *The intersection graph of an orientable generic surface*,
  Algebraic & Geometric Topology 17 (2017), 1675–1700, Definition 1.1.
  [Publisher PDF](https://msp.org/agt/2017/17-3/agt-v17-n3-p08-p.pdf)
