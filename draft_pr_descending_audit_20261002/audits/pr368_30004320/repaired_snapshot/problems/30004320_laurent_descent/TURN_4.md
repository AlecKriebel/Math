# Author turn 4: multiplicative-type stabilizers through smooth envelopes

Status: partial, 4/5 substantive author turns. The positive class now includes
all multiplicative-type geometric stabilizers, even non-smooth ones, for
smooth affine acting groups. This does not resolve arbitrary stabilizers.
All structural group-scheme and gerbe inputs below are credited, and no
historical novelty is asserted.

Throughout k has characteristic p>0, K=k((t)), and L is the full Puiseux
union L_all from turn 3. In particular each finite stage of L is a Laurent
field over the unchanged coefficient field k.

## 1. Gerbes with torus identity component and tame finite component group

**Lemma.** Let C be an algebraic gerbe over k whose geometric automorphism
group is smooth, has a torus as identity component, and has finite component
group of order prime to p. Every object of C(L) is isomorphic to the base
change of an object of C(k).

This is essential surjectivity on objects. It is not an equivalence of
whole groupoids: a positive-dimensional torus has additional L-automorphisms.
The component group need not be commutative, and its action on the torus
need not be trivial.

For every local object of C, take the identity component of its automorphism
group. These tori are characteristic, smooth, closed, normal and compatible
with base change and isomorphisms. Rigidify by this subgroup of inertia.
The resulting map

    C → D                                                   (1)

has D a finite étale gerbe whose geometric inertia has prime-to-p order.
This use of normal, possibly noncentral, inertia is justified by
Abramovich–Olsson–Vistoli, *Tame stacks in positive characteristic*,
Appendix A, Theorem A.1; its hypotheses are flatness and finite presentation,
not finiteness of the removed subgroup. Locally (1) is BH→B(H/H^0).

Let xi in C(L) have image delta_L in D(L). The extension L/L_tame, where
L_tame is the union restricted to n prime to p, is purely inseparable:
raising an element from a stage of ramification degree m p^e to its p^e-th
power puts it in the m-stage. Purely inseparable extensions do not change
finite étale gerbes or their object categories. Thus turn 1's finite-gerbe
lemma gives delta in D(k), together with an isomorphism of its base change
with the image of xi.

The 2-fiber C_delta=C×_D Spec(k) is a gerbe whose automorphism groups are
tori. Its canonical commutative band is therefore a k-torus T. The chosen
isomorphism puts xi in C_delta(L). By turn 3's H2 injectivity this gerbe
is neutral over k; by its H1 isomorphism for T, twisting a k-object makes
its L-base change isomorphic to xi in the fiber. Forgetting to C proves
the lemma. This two-step argument retains the prescribed full object,
not just a neutral gerbe or an unlabelled point of D.

Consequently, if Y is a smooth homogeneous space under any smooth affine
k-group G with such a stabilizer, every point of Y(K) is G(L)-equivalent
to a point of Y(k). Indeed apply the lemma to [Y/G] and use the constant
G-torsor injectivity from turn 3, exactly as in that turn's §5.

## 2. A smooth multiplicative-type envelope inside a smooth affine group

**Envelope lemma.** Let J be a smooth affine k-group and H a closed
subgroup of multiplicative type. There exists a smooth subgroup S of
multiplicative type with

    H⊆S⊆J,         S/H a k-torus.                          (2)

No connectedness, reductivity or torality assumption on J or H is added.
In particular, H need not itself lie in a torus.

Let C=Z_J(H), the scheme-theoretic centralizer. It is smooth even when H
is not smooth: see Conrad, *Reductive Group Schemes*, Lemma2.2.4,
printed pp.64–66. Take a geometrically maximal k-torus T in C^0; it exists
by Grothendieck's theorem in the same source, TheoremA.1.1, p.267.

We use the classical fact that a central multiplicative-type subgroup Z
of a smooth connected affine group lies in every maximal torus. Here is
the reduction that includes infinitesimal Z. It suffices to extend to an
algebraic closure. The centralizer of a maximal torus is smooth connected
with that torus central and as its unique maximal torus. Its quotient by
the torus is unipotent (the usual Cartan-group structure). Z lies in this
centralizer, and its map into that unipotent quotient is zero, since a
quotient of a multiplicative-type group cannot be a nontrivial unipotent
group. Hence Z is contained in the torus, schematically. These Cartan facts
are recalled in Conrad, DefinitionA.1.5 and its discussion, pp.268–269;
torus centralizer connectedness is Theorem1.1.19(1).

Apply this fact to H^0⊆Z(C^0). It gives H^0⊆T. As T centralizes all of H,
the product S=H T is a closed commutative subgroup and is of multiplicative
type: it is the image of H×T with kernel the anti-diagonal H∩T. Further,

    S/T = H/(H∩T)

is a quotient of H/H^0, hence a finite étale group of order prime to p.
(The latter assertion is the connected-component description of a
multiplicative-type group, checked after a separable splitting field.)
The extension of this étale group by T is smooth, so S is smooth and
S^0=T. Finally

    S/H = T/(T∩H)

is a torus. By character duality its character module is a subgroup of a
free lattice, and so is free; this also handles infinitesimal H∩T.
This proves (2).

A useful caution: even in PGL_2 over an algebraically closed field of odd
characteristic, the projective classes of diag(−1,1) and the coordinate
swap generate a multiplicative-type C2×C2 that is not contained in a torus.
The envelope lemma does not incorrectly place it in one: S may have a
nontrivial finite étale component group. For an infinitesimal example,
mu_p embedded in GL_2 by z↦diag(z,1) has smooth diagonal centralizer and
is contained in the diagonal torus, whose quotient by it is again a torus.
The exact controls include both examples.

## 3. Descent for every multiplicative-type geometric stabilizer

**Theorem.** Let G be a smooth affine k-group and X a smooth homogeneous
G-variety whose geometric stabilizer is of multiplicative type. Then

    X(k((t))) nonempty implies X(k) nonempty.              (3)

The geometric stabilizer is commutative, so the quotient gerbe [X/G] has
a canonical band M of multiplicative type over k. This is fppf descent of
the commutative automorphism group; multiplicative-type forms split étale-
locally, including non-smooth diagonalizable groups (Conrad Appendix B).
The K-point makes the corresponding class in H2(k,M) vanish over K, and
turn 3's H2 injectivity implies it is already zero over k. Thus there is
a G-torsor E over k with an equivariant map E→X.

Let J=Aut_G(E), a smooth affine inner form of G. The automorphism subgroup
H of the gerbe object E→X is a k-subgroup of J of multiplicative type.
One has X=H\E as an fppf quotient. Apply the envelope lemma to H⊆J and
choose S. Set

    Y=S\E,       q:X=H\E → Y=S\E.                      (4)

These homogeneous quotients are schemes of finite type; their construction
can be checked after a faithfully flat trivialization of E, using the
standard homogeneous quotients of an affine algebraic group. Because S
is smooth of multiplicative type, its identity component is a torus and
its finite component group has order prime to p. Section1 therefore gives
orbit-controlled descent on Y.

Given x in X(K), let y=q(x). There exist y_0 in Y(k) and g in G(L) such
that g transports y_L to (y_0)_L. By G-equivariance, it transports x_L
to an L-point of the fiber Z=q^−1(y_0).

Since H is normal in the commutative group S, the fiber Z is a torsor
under the k-torus S/H. More explicitly, the pullback of E→Y at y_0 is
an S-torsor, and its quotient by H is Z. The point in Z(L) is defined at
a finite Laurent stage of L; the credited torsor theorem gives Z(k)
nonempty. Its points are points of X(k), proving (3).

The non-smooth stabilizer was not reduced or discarded. It was absorbed
into a smooth envelope, and the remaining fiber was a genuine torus torsor.
The failure of mu_p-object descent in turn 3 is therefore compatible with
(3): the embedding geometry and fiber argument supply what bare object
descent could not.

## 4. Remaining scope and the next mechanism

The theorem does not cover arbitrary unipotent or noncommutative geometric
stabilizers. In particular, it is not an unqualified solution of the source
problem. The envelope is multiplicative-type because H is; applying the
same product construction to a general H would not prove its required
commutativity, smoothness or torus quotient.

The broader gerbe lemma in §1 suggests enhancing a gerbe by choices of
maximal tori when its stabilizer is connected reductive. The automorphism
group then becomes a torus normalizer, whose finite component is a Weyl
group. The prime-to-p condition on that component must still be checked;
wild Weyl groups are not automatically covered.

## Primary version check

Conrad's complete primary PDF was inspected at the exact cited results:
https://math.stanford.edu/~conrad/papers/luminysga3smf.pdf .
For rigidification we inspected the published AOV AppendixA, TheoremA.1
and its proof, pp.1087–1089:
https://www.numdam.org/article/AIF_2008__58_4_1057_0.pdf .
The 2014 corrigendum (DOI10.5802/aif.2869) concerns the Lie-algebra method
in Lemma2.14 and a deformation calculation in Proposition3.6; it does not
alter the cited AppendixA theorem. No nonreduced deformation argument
from the invalidated method is used here.
