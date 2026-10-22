# Two simultaneous rational chains

All varieties in this example are over the complex numbers. Stability conditions are on the bounded derived category of coherent sheaves. Divisor intersections are numerical, and ch_2 is identified with its degree on a smooth projective surface.

## The projective toric morphism

Let T=P(1,3,8). Its fan has primitive rays

v1=(1,0), v2=(0,1), v0=(-3,-8).

They satisfy v0+3v1+8v2=0, and the three consecutive cone determinants are 1,3,8. Thus the two singular charts have types 1/3(1,2) and 1/8(1,3), respectively. Refine the fan by the cyclic sequence

(1,0), (0,1), (-1,-2), (-2,-5), (-3,-8), (-1,-3), (0,-1).

Every consecutive determinant is 1, so the resulting toric surface S is smooth. The identity on the lattice gives a proper birational toric morphism f:S→T. The new rays give exceptional curves A1,A2,B1,B2, in that order. Each invariant curve on this smooth complete toric surface is P^1. The standard adjacent-ray relation gives the complete list of invariant self-intersections

0, 2, -2, -2, -1, -3, -3.

Consequently the exceptional intersection matrix, in order A1,A2,B1,B2, is

M = diag([[-2,1],[1,-2]], [[-3,1],[1,-3]]).

There are precisely two connected components, each a two-curve chain. The exceptional components satisfy C^2+valence(C)<0, with valence taken inside their respective exceptional chains. In particular this example fits the strict-chain case without needing a branching ADE argument.

For an explicit projectivity check, write the coefficients of the invariant divisor L in the seven-ray order as

L = (0,0,8,16,24,9,3).

The Cartier linear functions on the three coarse cones are (0,0), (8,0), (0,3), respectively, using the convention coefficient=-pairing. Thus L=f^*O_T(24). Its intersections with the seven invariant curves are

(3,8,0,0,1,0,0).

Let D=A1+A2+B1+B2. The lattice polygon of the divisor 4L-D has vertices

(0,0), (31,0), (29,1), (24,3), (8,9), (2,11), (0,11).

At each vertex exactly the corresponding two adjacent fan inequalities are equalities and all other inequalities are strict. Hence its normal fan is exactly the displayed smooth fan; the associated ample toric divisor makes S projective. This also directly verifies the ampleness criterion used below. The polygon area is 189 and (4L-D)^2=378.

The morphism is projective as a morphism from projective S to separated projective T. Its exceptional locus is precisely the four new ray divisors: it is an isomorphism over the torus and all unchanged cones and the subdivisions are confined to the two singular cones. This is the minimal toric resolution, since each exceptional component has self-intersection at most -2. Minimality is not needed for the strict-chain application.

## Pullback and beta

Set lambda=L and

beta = -(A1+A2)/4 - 3(B1+B2)/8.

The intersection computations give

lambda^2=24, lambda·D=0, D^2=-6, lambda·beta=0,

beta·A1=beta·A2=1/4,

beta·B1=beta·B2=3/4, beta^2=-11/16.

In particular lambda is big and nef and is the pullback of an ample Cartier class on T, while it is not ample on S.

Write n_C=-C^2. For every exceptional curve,

beta·C-n_C/2=-3/4.

Choose the integer k_C=0 in Vilches's notation. A connected subchain has length m=1 or 2, and the relevant quantity is

q = beta·(sum C) - (sum n_C)/2 = -3m/4.

It is nonintegral and satisfies

-m < q < -(m-1).

For m=1 this is -1<-3/4<0. For m=2 it is -2<-3/2<-1. These verify every instance of both Condition 4.1 and Condition 5.5, with k_C=0. There are six intervals in total, three in each chain. These strict inequalities also place beta in an open chamber, rather than on a numerical wall excluded by the construction.

## An explicit rational ample path

For 0<t<1/2, the invariant-curve intersections of lambda-tD are

(3-t, 8-t, t, t, 1-2t, 2t, 2t),

all positive. Hence lambda-tD is ample by the toric ampleness criterion. To keep square exactly 24 and all parameters rational, take rational 0<s<1/8 and put

a(s)=(1+s^2)/(1-s^2),

b(s)=4s/(1-s^2),

omega_s=a(s)lambda-b(s)D.

The ratio b/a=4s/(1+s^2) is between 0 and 1/2; thus omega_s is ample. The identity

(1+s^2)^2-4s^2=(1-s^2)^2

shows that omega_s^2=24a^2-6b^2=24. Moreover omega_s→lambda as s→0. At s=1/16, a=257/255 and b=64/255, so this also gives an explicit rational reference ample class omega_0 for the shared-heart description.

## The actual stability condition and its dependencies

Apply the strict-chain case of [Vilches, Theorem 1.3](https://arxiv.org/abs/2508.07019v1), with Conditions 4.1 and 5.5 just checked. It gives a genuine Bridgeland stability condition sigma on D^b(S) with central charge

Z(E) = -ch_2^beta(E) + 12 ch_0(E) + i lambda·ch_1^beta(E)

     = -ch_2(E) + beta·ch_1(E) + (395/32)ch_0(E) + i lambda·ch_1(E).

Here ch_1^beta=ch_1-beta ch_0 and ch_2^beta=ch_2-beta·ch_1+(beta^2/2)ch_0. The expansion uses lambda·beta=0 and beta^2=-11/16; it does not change the Chern-character convention.

One can specify the construction's skewed heart as

B=P_(beta,omega_0)((-1/2,1/2]),

where P_(beta,omega_0) is the slicing of the ample Arcara–Bertram condition. Vilches's common-heart lemma makes this independent of the selected ample reference of square 24. The pair (Z,B) uses this skewed phase window, not the conventional (0,1] window. Equivalently (iZ,B) is its rotated ordinary-heart description. The condition called sigma here has the original central charge Z and the corresponding slicing.

The cited theorem supplies the Harder–Narasimhan property, full support property on the Chern-character lattice, and convergence sigma_(beta,omega_s)→sigma in Stab(S). None follows from the displayed formula for Z alone. Those are credited mathematical inputs to this corollary, not claims of a new proof.

## The limit is outside the geometric chamber

Let C be any of the four exceptional curves and choose x∈C. In the usual heart of sigma, the torsion pair described in Vilches's Corollary 3.12 puts O_C in its torsion part and O_C(-1) in its torsion-free part, because the degree threshold is -3/4. Rotating the usual sheaf exact sequence gives an exact sequence in that heart:

0 → O_C → O_x → O_C(-1)[1] → 0.

Grothendieck–Riemann–Roch for C=P^1 embedded in S gives

ch(O_C(d))=(0,C,d-C^2/2).

Therefore

Z(O_C)=-3/4, Z(O_C(-1)[1])=-1/4, Z(O_x)=-1.

All three nonzero objects have phase one: a negative-real central charge of an object in the heart forces its HN factors to have phase one. The sequence has nonzero subobject and quotient. Thus O_x is strictly semistable. A geometric condition requires all skyscrapers to be stable of one phase, so sigma is not geometric, while the ample conditions approaching it are. It is therefore genuinely a boundary example of the requested kind.

## A limited exceptional support calculation

For a line bundle of multidegree (d_1,...,d_m) on one reduced connected subchain, viewed as a sheaf on S,

ch_2 = sum d_j + (sum n_j)/2 - (m-1).

The formula follows by normalization at the m-1 nodes, or by successive sheaf exact sequences. In this example

ch_2^beta = sum d_j + 1-m/4.

Consequently its charge never vanishes: the absolute real charge is at least 1/4 for m=1 and at least 1/2 for m=2. The possible negatives of the cycle squares are 2,2,3,4 for an A-singleton, A-pair, B-singleton, B-pair. It follows that, for these factors and their shifts,

(ch_2^beta)^2 + (1/48) ch_1^2 ≥ 0.

The general integer-degree bound follows from the two fractional residues, not from the finite degree range in the checker. This is a useful control on exceptional factors. It is not the full support theorem, which must also control positive-rank objects and objects extending outside the exceptional locus. That theorem remains a cited input.

## A separate example on the singular surface itself

Let X=P(1,1,2). The degree-two embedding realizes X as the quadric cone in P^3 given by u v=w^2. The vertex is its only singularity and has type A1. The minimal resolution is the Hirzebruch surface F_2, contracting its -2 section, and is crepant. Alternatively its toric fan is obtained by inserting (0,-1) between (-1,-2) and (1,0); the new curve has square -2.

Thus [Chou, Theorems 1.1 and 1.2](https://arxiv.org/abs/2411.19768v2) apply directly. They provide a genuine condition on D^b(X) compatible by derived pushforward with a weak condition on D^b(F_2), obtained from a path of genuine conditions on the resolution. The endpoint on F_2 is weak: Rf_*O_E(-1)=0, since H^0(P^1,O(-1))=H^1(P^1,O(-1))=0, so its pushforward-factored central charge kills O_E(-1)[1]. Crucially, this is a nonzero object of the fixed heart B^0, indeed a simple object by Chou's Lemma 3.15. An ordinary stability function on that heart cannot vanish on it. It would therefore be incorrect to call this particular endpoint an ordinary Bridgeland condition on D^b(F_2). Vanishing on an arbitrary derived object outside the heart would not alone justify that conclusion.

This separate application addresses the singular-category aspect without claiming Chou's single-ADE theorem applies to the mixed singularities of P(1,3,8).
