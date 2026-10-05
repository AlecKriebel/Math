# Monomial incidence for components of Hilbert schemes

## 1. Conventions and the recovered question

Let (k) be algebraically closed, let (S=k[x_1,\ldots,x_n]), and let
(H_d^n=\operatorname{Hilb}^d(\mathbb A_k^n)). An irreducible component always
means a maximal irreducible closed subset, with its reduced structure when a
scheme structure is needed. For a component (C), set
\[
\operatorname{Mon}(C)=\{I\subset S: I\text{ is monomial},\ \dim_k S/I=d,\ [I]\in C\}.
\]
The affine part of AIM Problem 16 asks whether this assignment is injective.
The projective part makes the same inquiry for
(\operatorname{Hilb}^P(\mathbb P^n)), using saturated homogeneous monomial
ideals. Fix the coordinates throughout. These are sets of closed points,
not fixed subschemes with multiplicities. Passing to the reduction does not
change the question.

Write (R_d^n) for the smoothable component. The classification input used
below is CEVV, Theorem 1.1: in characteristic different from 2 and 3 there is
one component for (d\leq7) or (d=8,n\leq3); for (d=8,n\geq4), there are
exactly (R_8^n) and the closure (G_8^n) of the local-algebra stratum with
Hilbert function ((1,4,3)). Their dimensions are (8n) and (8n-7).
Only this closure formulation is used in higher ambient dimension.

## 2. The universal smoothable signature

**Theorem 2.1.** In every characteristic:

1. Every component of (H_d^n) has a nonempty monomial signature.
2. Every finite-colength monomial ideal lies on (R_d^n).
3. (J_d=(x_1^d,x_2,\ldots,x_n)) lies on (R_d^n) and no other component.

Consequently, (R_d^n) is distinguished by its signature; every other
component has a proper nonempty subset of that signature, consisting of
ambient-singular points. Any affine counterexample to AIM Problem 16 must
involve two nonsmoothable components, and hence at least three components in
all. Whenever (H_d^n) has at most two components, the signature map is
injective.

**Proof.** The connected diagonal torus preserves every irreducible component:
a connected algebraic group cannot permute a finite set of components
nontrivially. For any ideal on a component, choose a positive integral weight
realizing a monomial initial ideal. Its flat Gröbner family has nonzero fibers
in that component because these fibers are torus translates. Closedness puts
the monomial special fiber in the same component.

Here is the classical distraction proof of (2), included with explicit indices.
Let (D\subset\mathbb N^n) be the finite down-set of standard exponent vectors
of (I). For each (i), choose pairwise distinct scalars
(c_{i,0},c_{i,1},\ldots) as far as needed. For every minimal generator
(x^a\in I), define
\[
f_a=\prod_{i=1}^n\prod_{j=0}^{a_i-1}(x_i-c_{i,j}).
\]
Every (f_a) vanishes at each distinct grid point
(p_b=(c_{1,b_1},\ldots,c_{n,b_n})), (b\in D): otherwise (b_i\geq a_i)
for all (i), contradicting (b\in D). For (K=(f_a)), leading monomials
are (x^a), so (I\subseteq\operatorname{in}(K)) and
\(\dim S/K\leq |D|\). Evaluation at the (|D|) distinct points gives the
reverse inequality and identifies (K) with their radical vanishing ideal.
Thus (\operatorname{in}(K)=I). Gröbner degeneration supplies the smoothing.
This is CEVV's published Proposition 4.15; it is not new.

For (3), (J_d/J_d^2\cong(S/J_d)^n) since its generators are a regular
sequence. Hence
\(\dim\operatorname{Hom}_S(J_d,S/J_d)=nd\). The point lies on (R_d^n)
by (2), so its local dimension is at least (nd\), while tangent dimension
is (nd\). Its local ring is regular. A regular local ring is a domain, so
exactly one irreducible component contains this point. This proves (3).
Any monomial point on another component also lies on (R_d^n); its local
ring has at least two minimal primes and cannot be regular. The conclusions
follow. ∎

This argument uses ambient smoothness. Being smooth on the reduced component
alone does not give the conclusion.

## 3. The complete length-eight signature

**Theorem 3.1.** Suppose (operatorname{char} k\notin\{2,3\}) and (n\geq4).
For a colength-eight monomial ideal (I), let (A=S/I) and let
\(\mathfrak m=(x_1,\ldots,x_n)A\). Then
\[
[I]\in G_8^n
\quad\Longleftrightarrow\quad
\mathfrak m^3=0\ \text{ and }\ \dim_k\mathfrak m/\mathfrak m^2\geq4.
\tag{1}
\]
Equivalently, its standard monomials have degrees at most two and their
Hilbert function is one of
\[
(1,4,3),\quad(1,5,2),\quad(1,6,1),\quad(1,7).
\tag{2}
\]
The full signature is therefore
\[
|\operatorname{Mon}(G_8^n)|=
\sum_{e=4}^{\min(7,n)}\binom ne\binom{e(e+1)/2}{7-e}.
\tag{3}
\]
Every ideal counted also belongs to (R_8^n). For (n=4), the two signatures
have sizes 684 and 120, respectively, and their intersection has size 120.

**Proof of necessity.** Work on the Hilbert scheme with its tautological
rank-eight algebra bundle (\mathcal A\). Multiplication by (x_i) is an
endomorphism (M_i\). Since 8 is invertible, define regular functions
\(a_i=\operatorname{tr}(M_i)/8\), and centered sections (y_i=x_i-a_i\).
On the local ((1,4,3)) stratum, (a_i) is the coordinate of the support
point: multiplication by a nilpotent has trace zero. The centered sections
lie in the maximal ideal. All triple products (y_i y_j y_\ell) vanish,
and the span of all pair products (y_i y_j) has dimension three.

The vanishing of these finitely many sections and the rank-at-most-three
condition on the bundle map
\(\mathcal O^{n(n+1)/2}\to\mathcal A\), (e_{ij}\mapsto y_i y_j\),
are closed conditions. They hold on the closure (G_8^n). At a monomial
point all (M_i) are nilpotent, so (a_i=0\). Hence all degree-three
monomials vanish and the degree-two piece has dimension at most three.
As (A) has length eight and (A_0=k), this is exactly (1).

**Proof of sufficiency.** Let (e=\dim A_1\geq4), let (q=\dim A_2=7-e\),
and relabel the (e) surviving coordinate variables. Let (Q) be the (q)
quadratic standard monomials. Choose a set (V) of four surviving variables
containing all variables appearing in (Q\). This is possible: when (e=4)
it is automatic, and when (e>4) there are at most two quadratic monomials,
which use at most four variables. Denote the other (r=e-4=3-q) variables
by (w_1,\ldots,w_r\). Choose distinct quadratic monomials
\(u_1,\ldots,u_r\) in (V) that do not belong to (Q\).

Construct a (k[t])-algebra (B), free as a module with basis
\[
1;\quad V;\quad w_1,\ldots,w_r;\quad z_m\ (m\in Q).
\]
This basis has (1+4+r+q=8) elements. Give it a unit and the following
commutative multiplication. A pair of variables in (V) multiplies to
(z_m) if its monomial is (m\in Q\), to (t w_j) if its monomial is
(u_j\), and to zero otherwise. Every product of a (w_j) or a (z_m)
with a nonunit basis element is zero. All triple products of nonunit
elements are zero, proving associativity directly.

Map the (e) surviving polynomial variables to their labels in (B),
and all unused variables to zero. This is a surjection: each (z_m) is
a product of two variables in (V\). Its quotient is free of rank eight,
so it gives a flat family of embedded length-eight schemes. At (t=0)
its quotient is exactly (S/I\). At (t\ne0), the maximal ideal squared
has the three-element basis ({z_m}\cup\{w_j}\), because
(w_j=t^{-1}u_j\). The four variables in (V) form a basis modulo that
square; assigning degree one to (V) and degree two to the (z_m,w_j)
makes the fiber a homogeneous algebra with Hilbert function ((1,4,3)).
Thus the nonzero fibers belong to its stratum and the special fiber belongs
to (G_8^n\).

For (3), choose the (e) surviving coordinate variables and then any (q=7-e)
of their (e(e+1)/2) quadratic monomials. Together with the unit and these
variables they form a down-set; the complementary monomials define exactly
one ideal. This is a bijective count. The size 684 of the full colength-eight
monomial set in four variables is separately obtained by exhaustive down-set
enumeration in the supplied verifier. ∎

**A necessary closure warning.** One cannot describe every point of (G_8^n),
for (n>4), by the generic Hilbert function alone. For example the free
algebra with basis
\(1,x_1,x_2,x_3,x_4,w,z_1,z_2\), nonzero nonunit products
\[
x_1^2=tw,\qquad x_1x_2=z_1,\qquad x_3x_4=z_2,
\]
and all other such products zero has function ((1,4,3)) for (t\ne0)
and ((1,5,2)) for (t=0). This is an explicit degeneration in five
ambient variables. The theorem describes the closed component, not just
its generic stratum.

**Corollary 3.2.** The signature assignment is injective for every (n\geq1)
and (1\leq d\leq8) in characteristic different from 2 and 3.

**Proof.** Apply the CEVV component count and Theorem 2.1. No assertion about
the classification in characteristics 2 or 3 is used. ∎

## 4. Collision controls

Let
\[
I_*=(x_1^2,x_2^2,x_3^2,x_4^2,x_1x_2,x_2x_3,x_1x_4).
\]
Its standard monomials are
\(1,x_1,x_2,x_3,x_4,x_1x_3,x_2x_4,x_3x_4\).
Thus it belongs to both components by Theorems 2.1 and 3.1. The verifier
builds the presentation of (operatorname{Hom}_S(I_*,S/I_*)) from all
pairwise monomial-generator syzygies. There are 56 scalar unknowns and
relation rank 23 over (mathbb Q), giving tangent dimension 33. The
smoothable and other component dimensions are 32 and 25.

The published CEVV Lemma 5.4 uses the variable permutation (x_2\leftrightarrow
x_4) of this ideal. The arXiv 2008 version numbers that lemma 5.9; its
Proposition 4.15 is a different statement from Proposition 4.15 in the
published 2009 paper. These versions must not be mixed when citing numbers.
The published lemma establishes the tangent dimension in every
characteristic; the rational computation independently verifies only
characteristic zero.

At (J_8=(x_1^8,x_2,x_3,x_4)) the same exact computation gives dimension 32.
This is the separating point. A shared singular point demonstrates overlap,
not equality, of signatures.

## 5. The projective boundary in arbitrary characteristic

**Theorem 5.1.** For every algebraically closed field, the component of
(operatorname{Hilb}^P(\mathbb P^n)) containing the saturated lexicographic
ideal is distinguished by its full monomial signature. If the Hilbert scheme
has at most two Borel-fixed points, all components are distinguished.

**Proof.** Reeves--Stillman prove that the saturated lexicographic ideal
is ambient-smooth. Its regular local ring has only one minimal prime,
so it is a separating monomial point.

Each projective component is preserved by the connected upper-triangular
Borel subgroup, and has a Borel-fixed point by the Borel fixed-point theorem.
With one such point, every component contains the lexicographic point, so
there is only one component. With two such points, Ramkumar's classification
and deformation analysis, together with Staal's arbitrary-characteristic
classification, show there are at most two components. In the reducible
case, only one contains the lexicographic point, which distinguishes their
signatures. Ramkumar v4, Introduction after Theorem A, explicitly explains
that the deformation computations are characteristic-independent and that
Staal's classification omits one characteristic-two case. The condition here
is the *actual* number of Borel-fixed points over (k), so that exception
is automatically respected. ∎

Borel-fixed implies monomial, but the converse is false. Strongly stable
and Borel-fixed are equivalent in characteristic zero, not in general.
Equality of generic initial ideals or of selected Borel-fixed points does
not establish equality of full monomial signatures.

## 6. Why the general argument stops

Even projectivity and smooth irreducible components do not make fixed-point
sets distinguish components for an arbitrary torus scheme. Over an
algebraically closed field choose (a\in k\setminus\{0,1\}), and let
\[
X=V((xz-y^2)(xz-a y^2))\subset\mathbb P^2.
\]
The action (t\cdot[x:y:z]=[t^2x:ty:z]) preserves both distinct irreducible
conics. Its only fixed points on either conic are ([1:0:0]) and
([0:0:1]\): the three coordinate points are the fixed points in the ambient
projective plane, and ([0:1:0]\) lies on neither conic. Thus the two
components have identical fixed-point sets. Both conics are smooth, including
in characteristic two (where the partials in (x,z), together with the
equation, preclude a singular projective point).

This is a control example for the logical method, not a counterexample
inside an ordinary Hilbert scheme. The unresolved affine case concerns two
nonsmoothable components. The work here neither produces such an equal pair
nor rules all such pairs out. The projective curve example suggested in the
AIM remark has not been verified from Liebling's thesis.

## 7. Separating the known equal-double-generic pair

Bertone--Cioffi--Roggero, Example 6.12, exhibits two distinct components of
(operatorname{Hilb}^{3t+2}(\mathbb P^3)) in characteristic zero with the
same double-generic initial ideal. Their general members are, respectively,
a disjoint plane conic and line ((Y_2), dimension 12), and a twisted cubic
with an isolated point ((Y_3), dimension 15). This is a genuine collision
of that smaller invariant. It does not imply a collision of full monomial
signatures.

**Proposition 7.1.** In (k[x_0,x_1,x_2,x_3]), the saturated monomial ideal
\[
M=(x_3,x_0^2)\cap(x_1,x_2)
 =(x_1x_3,x_2x_3,x_0^2x_1,x_0^2x_2)
\]
belongs to (Y_2) and does not belong to (Y_3).

**Proof.** The first factor defines a plane double line, with polynomial
(2t+1), and the second a line, with polynomial (t+1). They are disjoint:
the sum of their ideals has irrelevant radical. Each factor is saturated
and the intersection of saturated ideals is saturated. Their disjoint union
(Z) has polynomial (3t+2), and is pure one-dimensional and locally
Cohen--Macaulay (indeed each disjoint piece is a local complete intersection).

Replace (x_0^2) by (x_0^2+s x_1x_2) in the first ideal while keeping
the plane (x_3=0) and the second line fixed. For (s\ne0) this is a
smooth conic in characteristic zero. Its only possible intersection with
the other line is ([1:0:0:0]), which never satisfies its equation. This
is a flat family of disjoint conics and lines, so ([M]\in Y_2).

For exclusion, consider the projective flag Hilbert scheme of inclusions
(C\subset Z'), with Hilbert polynomials (3t+1) and (3t+2).
Projection to the second Hilbert scheme is proper and hence has closed
image. Every general member of (Y_3) is in that image, by taking its
twisted-cubic subscheme. Therefore every member of (Y_3) contains such
a subscheme (C\).

If our (Z) contained it, the kernel of
(\mathcal O_Z\twoheadrightarrow\mathcal O_C) would have Hilbert
polynomial 1, hence would be a nonzero finite-length subsheaf of
(\mathcal O_Z\). A pure locally Cohen--Macaulay curve has no such
subsheaf: locally, a nonzerodivisor in the maximal ideal acts injectively
on (mathcal O_Z), whereas a power annihilates any finite-length module.
This contradiction proves ([M]\notin Y_3\). ∎

Thus this published collision is rigorously ruled out as a full-signature
counterexample; the argument does not analyze every projective component.
