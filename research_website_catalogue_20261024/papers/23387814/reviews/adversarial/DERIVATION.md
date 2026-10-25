# Independent proof reconstruction and adversarial boundaries

The target is the lower bound epsilon(S,L;x)>=1/(2+|K_S^2|^(1/4)) for a smooth minimal complex projective surface, an ample integral line bundle and an arbitrary point. The Szemberg 2007 final question, OWR2009 Conjecture2 and Primer Question6.1.6 were read directly. OWR printed p.1124 was visually inspected: the additive 2 is outside the radical, the point is arbitrary, and the statement is explicitly for arbitrary Picard number. These are the assumptions tested below.

## Integral plane curve and a wholly integral pencil

Write m=d−1. The polynomial f=Z(X^m−Y^m)+X^d is primitive as a polynomial in Z over C[X,Y]: any common divisor of X^m−Y^m and X^d would divide X and Y, which is impossible in that ring. It is linear and nonconstant over the fraction field, hence irreducible by Gauss's lemma. Homogeneity then gives an integral plane curve of degree d.

At p=[0:0:1], the affine equation is x^m−y^m+x^(m+1). Its lowest homogeneous term has degree m and factors into m distinct complex tangent lines; characteristic zero is essential to that squarefreeness. Thus this is an ordinary m-fold point and the multiplicity is exactly m. If a projective singularity has Y=0, f_Z=0 forces X=0 and gives p. If Y is nonzero, f_Y=0 forces Z=0; then f_Z=0 forces X nonzero, but f_X=d X^(d−1) is nonzero. No other singularity exists. There is no hidden singularity at infinity.

The space of degree-e forms up to scale has dimension N_e=e(e+3)/2. Every reducible or nonreduced degree-d form lies in a closed projective multiplication image P^(N_a)xP^(N_(d−a)) for some 1<=a<d. Its dimension is at most the source dimension, and the codimension lower bound is a(d−a)>=d−1. Taking the finite union does not change the bound. Joining this locus to [f] increases dimension by at most one; for d>=3 the resulting closed join remains proper. Since f itself is integral, choosing g outside that join ensures the entire projective pencil, not just a generic member, avoids the reducible/nonreduced locus.

The needed additional conditions on g are genuinely simultaneous nonempty opens. The complete degree-d linear system is basepoint free and separates first jets; Bertini gives smooth members, evaluation at p gives g(p)!=0, and restriction to the smooth locus of C0 gives transversality. Intersecting these opens with the nonempty join complement in the irreducible parameter space is nonempty. All intersections occur away from p, and Bezout gives d^2 distinct reduced basepoints. This is an existence proof at the actual finite degree d; it does not rely on an unproved effective threshold hidden in the older asymptotic construction.

At a transverse basepoint the two pencil equations are local parameters u,v. Every nonzero linear combination au+bv has nonzero differential. A single ordinary blowup resolves the rational map [u:v], its exceptional P1 maps isomorphically to the pencil parameter line, and the fibre is the strict transform rather than that transform plus an exceptional component. Hence every fibre of f:Y->P1 is integral and reduced and each E_i is a section. In particular there are no unnoticed vertical exceptional components or multiple fibres. Generic smoothness supplies a nonempty open set of smooth fibre values, so four distinct smooth values avoiding C exist over C.

## The intermediate polarization

In the blowup lattice H^2=1, H.E_i=0 and E_i.E_j=−delta_ij, the fibre is F=dH−sum E_i. Thus F^2=0, F.E_i=1 and A=2F+E_1 has A^2=3, A.E_1=1, A.F=1. It is an actual integral divisor class, not a rational polarization.

The all-fibres-integral condition is used exactly where needed. F is the pullback of O_P1(1), so is nef. For an integral D different from E_1, the intersection E_1.D is nonnegative on the smooth surface. If D is horizontal, F.D>0 gives A.D>0. If F.D=0, its map to P1 has degree zero and D is contained in a fibre; since the fibre is integral and reduced, D is that whole fibre and A.D=1. The separate E_1 case gives degree one. Nakai–Moishezon therefore proves ampleness. Dropping the factor 2 would give (F+E_1).E_1=0, and allowing a vertical component missed by E_1 would give A.D=0; neither erroneous shortcut is used.

## Smooth, integral and projective base change

A double cover B->P1 branched simply at four distinct points exists from a squarefree quartic. Its connectedness follows from the odd valuations at its branch points, and Hurwitz gives genus one. It is finite flat of degree two. Its base change pi:S=Y x_P1 B->Y is likewise finite flat and projective.

Away from the four chosen fibres, pi is etale, even over the singular points of other fibres: etaleness is a base-change property and does not require the original fibration to be smooth there. Since Y is smooth, S is smooth on that region. At a branch fibre, f is smooth by construction, so in local smooth coordinates (u,t), S has equation t=v^2 and coordinates (u,v); it is smooth there too. Branching at the marked singular fibre instead would give a vanishing Jacobian and is deliberately excluded.

Each fibre of S->B is the corresponding connected integral fibre of f. Properness and connectedness of B then imply connectedness of S: a clopen decomposition of S would have disjoint closed images covering B, because a fibre cannot meet both parts. A smooth connected variety has one irreducible component (regular components cannot meet and components are locally finite). Thus S is integral. Independently, the base-change quadratic extension cannot split over C(Y), since a smooth reduced branch fibre has odd valuation in its branch function; this also excludes a disconnected split cover. This additional observation checks the construction rather than changes it.

## Canonical ampleness and minimality

The branch divisor is four disjoint fibres, linearly equivalent to 4F; the associated half-branch bundle is O_Y(2F). The double-cover Hurwitz identity is K_S=pi^*(K_Y+2F), in agreement with the actual canonical formula in Fuentes Garcia Section2. It is also obtained locally from the reduced ramification divisor R with O_S(R)=pi^*O_Y(2F).

Since K_Y=−3H+sum E_i, put N=K_Y+2F=(d−3)H+F. Every exceptional curve has N.E_i=1. Any other integral curve maps to a genuine plane curve of positive degree e, and N.D=(d−3)e+F.D>0 for d>=4. Moreover N^2=3(d−1)(d−3)>0. These inequalities cover every integral curve, so Nakai–Moishezon proves N ample, and finite surjective pullback proves K_S ample.

Ample canonical bundle implies general type. If S contained a smooth rational curve of self-intersection −1, adjunction would give canonical degree −1, contradicting ampleness. Thus S is minimal. This does not infer minimality merely from the cover degree, and does not try to descend A along a blowdown. A useful sanity check is that the preimage of an exceptional section is a genus-one curve of self-intersection −2 and canonical degree 2, not a rational (−1)-curve. A singular rational fibre also does not violate minimality: its arithmetic genus, rather than its normalization genus, enters adjunction.

## The degree-one pointed curve and exact inequality

The chosen singular fibre lies above an unbranched base value. Its inverse image is literally C x {b_1,b_2}, the disjoint union of two schemes isomorphic to C. This follows from the fibre product and is stronger than merely saying that a general etale double cover of a curve must split (which would be false). Choose one component C' and its point x above p. The isomorphism preserves multiplicity d−1, and projection gives L.C'=A.C=1 for L=pi^*A. The entire inverse image has degree two over C, but the selected component has degree one. Confusing these produces the wrong quotient.

The finite pullback L is ample and integral, L^2=2A^2=6, and K_S^2=2N^2=6(d−1)(d−3). Thus epsilon(S,L;x)<=1/(d−1). No equality with the exact Seshadri constant is needed or claimed.

For d>=4, all quantities used in the root comparison are positive. The required strict inequality is equivalent to d−3>[6(d−1)(d−3)]^(1/4), hence to (d−3)^3>6(d−1). At d=7 the margin is 64−36=28>0. Its forward difference is 3(d−3)^2+3(d−3)−5>0 for every d>=7. Therefore the contradiction holds for every d>=7. For d=4,5,6 this curve does not give a strict contradiction. At d=7, K^2=144 and 144<4^4 gives 1/6<1/(2+144^(1/4)) exactly, without floating roots.

## Scope and independent conclusion

The point x is special, L need not be canonical or adjoint, and the Picard group is not restricted to rank one. The minimal surface varies with d. Therefore the result neither contradicts the very-general-point lower bound nor resolves positivity of the infimum over all integral ample bundles and points on one fixed surface. It supplies the requested kind of counterexample to the exact historical arbitrary-point formula.

No substantive defect was found. The algebraic existence argument uses standard Bertini/transversality and Nakai–Moishezon; finite symbolic checks support identities and detect particular invalid changes but do not certify those universal geometric theorems or choose an explicit generic companion g. The construction proves existence, with the singular member explicit and the companion selected from a proved nonempty open set. No priority or first-discovery conclusion follows from this adversarial review.
