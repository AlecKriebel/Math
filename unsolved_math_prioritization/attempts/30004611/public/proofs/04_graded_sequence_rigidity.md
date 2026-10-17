# Fixed-term obstructions and rigidity of graded lattice restriction maps

14 October 2026 UTC. Row 1775 / 30004611, shared substantive pass 4.
Authored mathematical component; not an independent acceptance report.

## 1. Result and exact scope

This pass proves a map-independent obstruction for the previously specified
three-term sequences, not merely failure of their canonical arrows. It also
classifies **all coefficient-degree-zero S-linear sheaf maps** from D to the
ordinary restriction, and from E to the Ziegler restriction, on the accepted
common poset. The Ziegler classification proves that changing the arrow
cannot repair any canonical Ziegler surjectivity defect, even without any
extra naturality across arrangements. A block-decomposition argument proves
the same epimorphism rigidity for the ordinary target, including reducible
restrictions. Stronger naturality across marked arrangements reduces the
classified map families further to the stated scalar formulas.

These are scoped impossibility theorems. They do not exclude changing the
terms, allowing non-degree-preserving maps, passing to a different category,
or supplying a different comparison space with a separately proved
cohomology identification. They do not solve the broad original constructive
Problem 6.3. No freeness criterion from Mucksch's retained v3 is used.

## 2. Setup

Let A be central and essential in V over K, let dim V=ell>=3, let H be a
marked hyperplane with fixed equation alpha, and put S=Sym(V*), R=S/(alpha).
Use coefficient grading: coordinate derivations have degree zero.

Let P be the nonzero flats of A with inclusion order; Q={X in P:X subset H};
i:Q->P is its closed inclusion. Let B=A^H with Ziegler multiplicity m.
The accepted functors are

- D_X=D(A_X);
- F_X=D((A minus H)_X), the closure/direct-image deletion transport;
- E_X={theta in D_X:theta(alpha)=0};
- T_X=D(B_X), and Z_X=D(B_X,m), on Q;
- I_X=alpha S on Q and S off Q, with the actual inclusions.

All maps below are morphisms of covariant graded S-module functors, of degree
zero. In particular every target inclusion T_X->T_H and Z_X->Z_H is injective.
Write rho:D->i_*T and pi:E->i_*Z for canonical reduction. On Q define

    nu_X(theta) = theta(alpha)/alpha modulo alpha.

It has degree -1 as a scalar-valued map; multiplication by a linear
coefficient derivation makes nu into a degree-zero map. It is defined only
where H belongs to A_X, exactly where it is used. It is invariant under
rescaling alpha. Let epsilon_H be the Euler derivation of R.

Define

    End_B(H)={A in End_K(H): A(K) subset K for every K in B}.

A corresponds to the linear vector field t->A(t) in D(B)_1. Equivalently,
for an equation beta_K of K there is a scalar lambda_K(A) with
beta_K composed with A=lambda_K(A) beta_K.

## 3. Complete classification on the fixed poset

### Theorem 3.1: ordinary target

There is a natural vector-space parametrization

    Hom^0_S-sheaves(D,i_*T)
       = { Phi_(A,v)= A rho + v nu :
                  A in End_B(H), v in D(B)_1 }.                 (3.1)

Here A acts on the coefficient-vector of a derivation, while v nu means the
scalar nu(theta) times the derivation v. The values off Q are zero. The
parameters are unique. No naturality across different arrangements is an
assumption of this theorem.

Proof. At the top H of Q choose a complement of H and coordinates alpha,t.
There D_H=D({H})=S alpha partial_alpha direct-sum (S tensor H), whereas
T_H=Der_K(R)=R tensor H. A degree-zero S-linear map at H is uniquely
specified by a constant coefficient endomorphism A of H and by the image v,
a linear vector field, of alpha partial_alpha. Thus it has the displayed
form before imposing tangency.

For X in Q, naturality of X->H and injectivity of T_X->T_H force Phi_X to
be the restriction of Phi_H to D_X. Thus the top map determines the entire
sheaf map.

For each K in B, K is a nonzero flat of A because ell>=3. Choose coordinates
z=alpha, t=beta_K, u on K. The other members of A_K have equations t+c_j z,
and with q=product_j(t+c_j z) one has

    D_K = S(z partial_z+t partial_t) direct-sum S q partial_t
                  direct-sum sum S partial_u.

The constant derivations along K force A(K) subset K. Applying Phi to the
Euler vector z partial_z+t partial_t then forces beta_K(v) divisible by
beta_K. Hence v belongs to D(B)_1. Conversely these conditions imply that
A preserves D(B_X) and v belongs to D(B_X) for every X. Therefore (3.1)
lands in every required target and gives a sheaf map. This proves necessity,
sufficiency and uniqueness. Although the proof used a complement, rho and
nu are intrinsic, so the resulting parametrization is complement-independent.

### Theorem 3.2: Ziegler target from its standard domain

    Hom^0_S-sheaves(E,i_*Z)
                = { A pi : A in End_B(H) }.                    (3.2)

Proof. At H the source is S tensor H, so a degree-zero map is a constant
matrix A. Injectivity of target maps to H again determines all other
components. At K the common constant directions force A(K) subset K.
Conversely beta_K(A eta)=lambda_K(A) beta_K(eta), so A preserves every
multiplicity divisibility condition. This proves sufficiency too.

In particular, a sheaf epimorphism E->i_*Z exists if and only if pi is an
epimorphism. Indeed any epimorphism is onto at H in degree zero, forcing A
invertible. Such an A and its inverse preserve all restricted hyperplanes,
so A is an automorphism of Z and coker(A pi) is isomorphic to coker(pi).

### Theorem 3.3: direct maps from D to Z

All degree-zero sheaf maps D->i_*Z still have the form A rho+v nu, now with
A in End_B(H), v in D(B)_1, and the additional conditions

    lambda_K(A)+lambda_K(v)=0 whenever m(K)>1.                 (3.3)

Here lambda_K(v) means beta_K(v)/beta_K, a scalar for a linear logarithmic
vector field. To verify the condition, use the same rank-two basis: the
image of its degree-one Euler vector has beta_K-component
(lambda_K(A)+lambda_K(v)) beta_K, which must be divisible by beta_K^{m(K)}.
The q-generator reduces to beta_K^{m(K)}, and the common directions have
zero beta_K-component. These checks are also sufficient, since membership
in Z_X is tested one restricted factor at a time and D_X is contained in
D_K for each K containing X.

### Theorem 3.4: ordinary epimorphism rigidity, including reducible B

A degree-zero S-linear sheaf epimorphism D->i_*T exists if and only if rho
itself is an epimorphism. This strengthens the classification without adding
any naturality across arrangements or fixing the proposed kernel.

Proof. The global restriction B is essential because A is essential. Split
its normal configuration into indecomposable spans, giving H=direct_sum H_j.
Then End_B(H) consists of independent scalars a_j on H_j, and a linear
logarithmic vector field has the form v=sum b_j epsilon_j. Here epsilon_j
is the Euler vector in block H_j. A self-contained verification of the
normal-configuration decomposition appears in Section 4.

Choose any complement to H. Every original hyperplane lying over a
restricted factor in block j has equation beta_j(t_j)+c alpha, involving
only that tangential block and alpha. Therefore the normal-annihilating
module E_X, for every X in Q, splits into its tangential block projections:
each block projection preserves all its tangency conditions. Its reduced
image M_X=im(pi_X) consequently splits into corresponding blocks too, as
does the ordinary target T_X. This statement concerns the image inside T_X;
no identification with an ordinary target is being made for the Ziegler
map. The same reduction of E is an ordinary logarithmic derivation as well.

Let C_X=T_X/M_X, with its resulting block decomposition. The canonical
ordinary image modulo M_X is generated by the class e of
sum epsilon_j=epsilon_H. For Phi=A rho+v nu to be a sheaf epimorphism, its
H-stalk must be onto in degree zero, forcing every a_j nonzero. The block
scalings A preserve M_X. Formula (4.2) block by block then shows that the
image of Phi_X modulo M_X is generated by

    h=sum_j (a_j+b_j) [epsilon_j].

Let B0 be the diagonal block endomorphism of C_X whose j-th scalar is
a_j+b_j. Thus h=B0 e. If R h=C_X, then B0 is surjective on C_X. On any block
with zero scalar, this is possible only if that block of C_X is zero;
on all other blocks B0 is invertible. It follows that B0 is an automorphism
of C_X. Applying its inverse gives R e=C_X. Hence rho_X is onto for every
X, as required. The converse takes Phi=rho. This reasoning remains valid
when individual localized blocks acquire free common directions or zero
quotients; no local irreducibility hypothesis is imposed.

## 4. What additional naturality does and does not imply

The fixed-poset result (3.1) genuinely allows more than scalar multiples of
rho. For example even rho+b epsilon_H nu is a different morphism, and
reducible B allows separate component coefficients. It would be false to
assert uniqueness of rho from the word 'natural' alone.

Here is a precisely stronger condition under which there is rigidity.
Consider an assignment of degree-zero sheaf maps for marked arrangements
in a fixed ambient dimension over K. Require it to be defined for their
possibly nonessential localizations as well, to commute with localization
at flats containing H's defining equation (in particular localization at
the flat H, which gives the arrangement {H}), and to commute with every
linear isomorphism of marked arrangements. The localization condition means
that the stalk map at H is the assigned map for ({H},H); it is stronger than
merely commuting with arrows of the one fixed P. One can equivalently
include the nonessential localizations with geometric nonzero-flat posets,
since their H-stalk is present. No cohomology identification for those
nonessential posets is needed.

Under these explicit assumptions, the ordinary assignment has the form

    a rho+b epsilon_H nu,                                    (4.1)

and the E-to-Z assignment has the form a pi. The constants a,b depend only
on the ambient dimension and field, not on A. To prove this, the top map for
({H},H) must be equivariant under all GL(H) linear isomorphisms (extended by
the identity on a normal complement). Its constant matrix A therefore
commutes with GL(H), hence is a scalar matrix. The same holds for the matrix
of its linear vector field v. This centralizer assertion is valid over
every field for dim H>=2, by commuting with the elementary transvections.
The scalar formulas are themselves equivariant under the whole stabilizer
of H, including changes of complement. Compatibility under field extensions,
if additionally required, transports a,b to the same scalars in the larger
field. No unstated claim about arbitrary non-flat base changes is made.

For (4.1), at each X in Q use the actual module splitting

    D_X=S epsilon_V direct-sum E_X.

It gives

    Phi(f epsilon_V+eta)
              =(a+b) f-bar epsilon_H+a pi(eta).               (4.2)

Consequently im Phi_X is contained in im rho_X for every X; if both a and
a+b are nonzero, those images are equal. Thus no such natural family can
repair an ordinary restriction defect. For a direct D-to-Z assignment
valid for all marked arrangements, (3.3), tested on an arrangement with a
multiple restriction fiber, forces b=-a. Its map is precisely reduction
after subtracting the normal Euler component,

    theta -> a [theta-nu(theta) epsilon_V] modulo alpha,

where before reduction the coefficient is theta(alpha)/alpha. Its image
is a times im pi. Thus it cannot repair a Ziegler defect either.

For a single fixed poset the ordinary scalar conclusion also holds whenever
B is irreducible. More explicitly, if B decomposes as an essential product
of r irreducible factors, End_B(H)=K^r acting by a scalar on each factor.
To see this without importing an arrangement theorem, choose a basis from
the spanning restricted normals. All are eigenvectors for A^*. Any further
normal forces equality of the eigenvalues of every basis component in its
support. The equivalence classes generated by these supports are precisely
the indecomposable spans of the normal configuration. This proves the
asserted product description.

## 5. Exact ordinary defect in the credited seven-plane example

Work over any field of characteristic different from two; the original
credited source example is over the reals, and the earlier pass used Q.
Put S0=K[x,y,z] and take the seven equations

    z, x, y, x-z, y-z, x-y+z, x-y-z,

marked by z. Its ordinary restriction has R0=K[x,y] and basis

    epsilon=x partial_x+y partial_y,
    eta=x(x-y) partial_x.

Write p=x(x-z), q=y(y-z), r=(x-y)^2-z^2. An element of E_z is exactly a pair

    (a,b)=(p u,q v) with p u-q v=r h.                          (5.1)

The ordinary image contains R0 epsilon. Modulo this summand its image is
J eta for a homogeneous ideal J of R0. For a pair (a0,b0) after restriction,
the eta coefficient is

    g=(a0/x-b0/y)/(x-y).                                      (5.2)

There are no degree-two E_z elements: the quadratics p,q,r are linearly
independent when 2 is invertible. Thus J_0=0. Solving the linear syzygies
in (5.1) gives the one-dimensional solution

    u=-x+3y-z,   v=3x-y-z,   h=-x+y,

up to a scalar. More explicitly, write u=a x+b y+c z, v=d x+e y+f z,
h=g x+j y+k z. The cubic equations give k=0, g=c=a, j=-e, f=e,
b=-e-2a, d=-a-2e, and d=b; hence e=a and b=d=-3a. This proves
the one-dimensional assertion over the stated fields without a numerical
specialization. By (5.2) this vector
maps to -(x+y) eta modulo Euler. Hence J_1=K(x+y).

The Koszul pair (a,b)=(p q,p q) belongs to E_z and has eta coefficient -xy.
Thus J contains (x+y,xy). That ideal contains every homogeneous polynomial
of degree at least two, since its quotient is K[x]/(x^2). The established
degree-zero and degree-one equalities therefore prove the exact identity

    J=(x+y,xy),
    C_ord=R0/(x+y,xy)(-2),
    Hilb(C_ord;t)=t^2+t^3.                                   (5.3)

This is a full cokernel calculation, not merely the familiar nonlifting
quadratic witness. The underlying arrangement and the dimension-two
ordinary defect are credited to Abe-Kawanoue Example 4.3(3); no novelty
claim is made.

Here are exact Hilbert series of all the terms as a further check. The
ideal (p,q,r) has the following Groebner basis for graded lexicographic order
x>y>z, with the middle polynomial divided by 2 if made monic:

    x^2-xz,  2xy-xz-yz+z^2,  y^2-yz,  xz^2+yz^2-z^3.

Its leading ideal is (x^2,xy,y^2,xz^2). Buchberger reductions are zero; the
last polynomial belongs to the ideal because xyz belongs to it and
z(2xy-xz-yz+z^2)=2xyz-(xz^2+yz^2-z^3). The standard monomials give dimensions
1,3,3,2,2,... in degrees 0,1,2,3,4,... . The syzygy presentation (5.1) gives

    Hilb(D(A7);t)=(t+t^3+2t^4-t^5)/(1-t)^3.

Using the independently proved canonical kernel z D(A7 minus H), together
with (5.3), then gives

    Hilb(D(A7 minus H);t)=(t+2t^3+t^4-t^5)/(1-t)^3.            (5.4)

Now promote by the separate equation w=0 in V=K^4. The nonzero flat
X={x=y=z=0} is retained, and w=0 drops from its localization. At X the extra
derivation partial_w is free and reduction is onto on that summand. Hence

    Hilb(D_X)=(1+t+t^3+2t^4-t^5)/(1-t)^4,
    Hilb(F_X)=(1+t+2t^3+t^4-t^5)/(1-t)^4,
    Hilb(T_X)=(1+t+t^2)/(1-t)^3,
    Hilb(T_X)-Hilb(D_X)+t Hilb(F_X)=(t^2+t^3)/(1-t).           (5.5)

In particular there exists **no** degree-zero exact sequence of graded
S-modules 0->F_X(-1)->D_X->T_X->0, whatever either arrow is. Exactness would
force the final expression to be zero. Consequently no sheaf short exact
sequence 0->I tensor F->D->i_*T->0 exists with these terms and any maps.

There is an additional arrow-independent epimorphism obstruction in this
example, without fixing the kernel at all. Its global restricted arrangement
has equations x,y,x-y,w, so End_B(H) consists of diag(a,a,d), and v has the
form b epsilon_xy+e w partial_w. At the bad X, projection of any map (3.1)
to its x,y components is a rho_7+b epsilon_xy nu. By (4.2) its image is
contained in the defective canonical ordinary image. Thus **no degree-zero
S-linear sheaf epimorphism D->i_*T exists** in this example.

## 6. Exact Ziegler Hilbert obstruction

For the credited factor xyz(x+y+z), marked by z, the elementary presentation
of E_z has three degree-two generators and a single degree-three relation:

    (xy,-xy), (x(x+y+z),0), (0,y(x+y+z));
    (x+y+z) g1-y g2+x g3=0.

This presentation and its full relation module were proved independently in
pass 3. The pass-2 tangency calculation gives the entire Ziegler defect
K(-1), over every field. After promotion by w=0, at the retained w-axis,

    Hilb(E_X)=(1+3t^2-t^3)/(1-t)^4,
    Hilb(Z_X)=(1+t+t^2)/(1-t)^3,
    Hilb(Z_X)-(1-t)Hilb(E_X)=t/(1-t).                          (6.1)

Thus no degree-zero exact sequence 0->E_X(-1)->E_X->Z_X->0 exists with
any arrows, and no corresponding sheaf sequence using I tensor E can exist.
Theorem 3.2 proves more: no degree-zero sheaf epimorphism E->i_*Z exists
at all, regardless of its proposed kernel.

One must not confuse this with the direct shape using D and deletion F:
in this four-plane example the Ziegler multiplicities are all one, so
Z=T, and the ordinary D/deletion sequence actually is exact. The obstruction
in (6.1) concerns the correctly named normal-annihilating Ziegler domain E.

## 7. Why a different rank-one grading twist cannot fix these terms

Suppose J is any graded sheaf with each stalk graded-free of rank one,
J_X isomorphic to S(-a_X). No condition on its transition maps is imposed.
If a degree-zero short exact sequence

    0->J tensor F->D->i_*T->0                                (7.1)

exists, then necessarily a_X=1 for every X in Q and a_X=0 off Q. The same
conclusion holds with F,D,T replaced by E,E,Z.

Here is a characteristic-free Hilbert proof. For a simple arrangement of
n hyperplanes in ell variables, the tangency presentation gives

    Hilb D = ell/(1-t)^ell - n/(1-t)^(ell-1)
                                     + O((1-t)^(-(ell-2))).

The error bound holds because the tangency cokernel vanishes at all primes
of height at most one: at height one at most one distinct hyperplane row
survives and that row is hit by a constant derivative. Thus if N_D(t) denotes
(1-t)^ell Hilb D, then N_D(1)=ell and N_D'(1)=n.

At X in Q write n=|A_X|. The left deletion has n-1 hyperplanes and rank ell;
the R-target has rank ell-1. The Hilbert equality of (7.1), differentiated at
t=1 after putting over denominator (1-t)^ell, therefore gives

    n=a_X ell+(n-1)-(ell-1),

so a_X=1. This is equality of integer Hilbert coefficients, not an equation
in the coefficient field. Off Q the target is zero and D_X=F_X, forcing
monomial t^{a_X}=1 and hence a_X=0. For the E sequence its S-rank is ell-1,
and the identical calculation gives a_X(ell-1)=ell-1 on Q; off Q use the
nonzero Hilbert series of E_X. The argument allows negative shifts too.

It follows that the nonzero discrepancies (5.5) and (6.1) rule out every
such stalkwise graded-free rank-one twist J, regardless of how its stalks
are glued. It is not merely the particular transitions of I that fail.
This does not classify higher-rank, non-free, or non-tensor modifications.

## 8. A direct original/deletion/Ziegler three-term shape

A proposed direct sequence 0->J tensor F->D->i_*Z->0 also forces the same
shifts 1 on Q and 0 off Q, by the first-order calculation above. If a
restricted hyperplane K has multiplicity m>1, at its nonzero rank-two flat
one has, with c=ell-2,

    Hilb(D_K)=(t+t^m+c)/(1-t)^ell,
    Hilb(F_K)=(t+t^(m-1)+c)/(1-t)^ell,
    Hilb(Z_K)=(t^m+c)/(1-t)^(ell-1).

The second formula uses m>=2 and the elementary rank-two basis for the
deletion of m distinct lines. Consequently

    Hilb(Z_K)-Hilb(D_K)+t Hilb(F_K)
                         =(t^m-t)/(1-t)^(ell-1),              (8.1)

which is nonzero. Thus that three-term shape is impossible already at a
rank-two stalk whenever some Ziegler multiplicity exceeds one. If every
multiplicity is one, it reduces to the ordinary shape and its previously
proved positives and obstructions apply. No conclusion here relies on
confusing Euler multiplicity with Ziegler multiplicity.

For completeness, moving the restriction to the submodule position cannot
help: it is annihilated by alpha and has no nonzero map into a torsion-free
S-module. Reversing the torsion-free terms in a shape
0->J tensor D->F->i_*T (or i_*Z)->0 forces at H
ell a_H=ell-2, impossible for an integer a_H when ell>=3. This only treats
the stated rank-one twist shapes, not arbitrary alternative terms.

## 9. Exact and finite controls

The authored script rigidity_checks/check_rigidity.py checks all six
S-polynomial reductions of the displayed Groebner basis over Q, the explicit
syzygy and its ordinary-image coefficients, and the two promoted Hilbert
discrepancies as exact rational-function identities. It also independently
constructs homogeneous tangency matrices and compares the original and
deleted seven-plane module dimensions with (5.4) in degrees 0 through 6
over F3, F5, and F7. All 21 field/degree controls and all exact controls pass.
The result file is rigidity_checks/RESULTS.json. These are author controls,
not the independent audit and not a substitute for the symbolic proof.

## 10. Base change, remaining freedom, and source credit

A field extension is faithfully flat and commutes with every finite
polynomial divisibility kernel used above. It transports the nonzero
explicit defects and their Hilbert series, so it cannot remove the
obstructions. Adjoining independent polynomial variables likewise tensors
the displayed defects, as in the rank-four promotion. The fixed-poset
classification and Hilbert obstructions impose no unmentioned naturality
hypothesis; Section 4 expressly identifies the stronger assumptions used
for the universal-family conclusion.

What remains open at source level is a genuinely different three-term
construction with non-tautologically identified named terms and a proved
comparison to the desired lattice-sheaf cohomology. The accepted all-rank
six-term and tangency-complex constructions retain their validity; this
pass does not turn those into three original-sheaf terms or discard their
nonzero corrections. Alternative comparison spaces must change or remove
these bad stalks, or change the actual modules there; any claimed
cohomology preservation then needs its own proof. Ungraded maps, shifts of
multiple different terms, and broader constructions are not classified.

Primary sources already retained and inspected in the source-readiness
packet and accepted passes:

- Paul Mucksch, arXiv:2008.13700v3, Problem 6.3:
  https://arxiv.org/abs/2008.13700v3 . The broad source question is not a
  prescribed assertion that either of our fixed sequences is exact.
- Takuro Abe and Hiraku Kawanoue, arXiv:2406.00305v2, Example 4.3(2)-(3):
  https://arxiv.org/abs/2406.00305v2 . The four- and seven-plane arrangements
  and the dimensions of their corresponding defects are credited examples.

No version-of-record claim, current exhaustive literature claim, or novelty
certificate is made. No retained-v3 unrestricted freeness inference is used.
