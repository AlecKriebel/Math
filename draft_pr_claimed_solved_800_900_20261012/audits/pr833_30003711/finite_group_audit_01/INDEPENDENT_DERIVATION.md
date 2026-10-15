# Derivation recorded before any earlier audit verdict was read

Scope: spectral Lemma 1 and cyclic-isotropy Corollary 2 in the frozen
author/PROOF.md, head 0e6e23213494ecb4a7208f920d25d7b49502a5cb.
The following derivation was reconstructed independently from the target
manuscript and primary source matrices. No earlier independent_audit or
second_review mathematical verdict has been read.

Write w for a primitive cube root of unity, use column vectors, and take the
four matrices A,B,C,D of Chen--Wan (2.4): A cycles the coordinates in the
direction (x,y,z) -> (z,x,y), B=diag(1,w,w^2), C=diag(1,1,w), and

    D = [ w^2  w   1 ]
        [ w    w^2 1 ]
        [ 1    1   1 ].

These are projectively unitary: A* A=B* B=C* C=I and D* D=3I.
The exact GL identities are BA=w AB, CAC^-1=AB, CBC^-1=B,
DA=w^2 B^2 D, DB=w^2 AD. Thus it would be wrong to replace every
projective identity by an equality of these chosen GL representatives.

All four matrices preserve the pencil spanned by f0=x^3+y^3+z^3 and
f1=xyz. For D, direct expansion gives f0(Dv)=3f0(v)+18f1(v) and
f1(Dv)=f0(v)-3f1(v). For C, f0 is unchanged and f1 is multiplied by w.
The projective group they generate is therefore a subgroup of the actual
Hessian group, whose order and affine description are independently stated
in Artebani--Dolgachev Proposition 4.1.

The nine points A^a B^b p0, p0=[1:-1:0], a,b in F3, are exactly

    [1:-w^b:0], [0:1:-w^b], [-w^b:0:1].

They are pairwise distinct and are all nine common flexes of the smooth
Hesse members. AD's p0 is [0:1:-1]; our p0 is AD's p6, so this is a
change of origin and labeling, not a change of configuration.
Their projective action is faithful: p0,Bp0,Ap0,ABp0 have no three
collinear and hence constitute a projective frame. Any projectivity fixing
all four is the identity.

Modulo projective scalars K=<A,B> is C3 x C3. Its action on these nine
points is regular, by the displayed coordinates. C and D both fix p0.
They normalize K and induce, on the coordinates (a,b), respectively

    U = [1 0;1 1],       R = [0 1;2 0].

The induced action of <C,D> is faithful: an element acting trivially on K
and fixing p0 fixes every kp0, hence the entire projective frame. U and R
generate SL2(F3), since U and RUR^-1 give the two elementary shear
directions and elementary row reduction generates SL2. Hence <C,D> has
order 24 and is precisely the p0 stabilizer. Its intersection with K is
trivial, because K acts regularly. Since it normalizes K, every generated
element has a unique form kh. The generated projective group has order
9*24=216 and is the entire classical Hessian group. This verifies the
actual splitting, embedding, origin, and affine action, rather than
assuming that an abstract affine group has the desired representation.

Now take gamma(v)=Lv+t in this action. A fixed point exists if and only if
t is in the image of I-L. If I-L is invertible there is a unique fixed
point. Thus a fixed-flex-free element has det(L-I)=0. Since det L=1,
its characteristic polynomial is (z-1)^2, so (L-I)^2=0.

If L=I, gamma is a nonzero translation A^a B^b. For a=0,b!=0 its
eigenvalues are 1,w^b,w^(2b), pairwise distinct. For a!=0 the matrix is
a weighted permutation matrix on one three-cycle. Its characteristic
polynomial is z^3-q, where q is the product of its three nonzero weights.
Since q!=0 and the characteristic is zero, it has no repeated root.

If L!=I, N=L-I has rank one and N^2=0, so im N=ker N. Choose nonzero
u in ker N and v so det(v,u)=1. Then Nv=c u for c=1 or 2. The
determinant-one basis (v,u) puts L in the form U^c. Both choices are
needed. In fact a determinant-one change of such a basis rescales c by a
square in F3^x, and both nonzero squares equal 1, so U and U^2 are not
SL2-conjugate. Their centralizers have order 6 and their classes have
size 4 each. This accounts for all eight nonidentity unipotents.

Lift this determinant-one coordinate change to the actual complement
Gamma0. Conjugating gamma by it gives A^a B^b C^c for arbitrary a,b
and c=1 or 2. For a=0, its affine action is

    (x,y) -> (x, y+cx+b),

so it fixes the three points with x=-b/c. Consequently a fixed-flex-free
element must have a!=0. Its matrix is again a weighted three-cycle;
in fact the chosen representative has characteristic polynomial z^3-w^c.
It has three distinct eigenvalues. Similarity and multiplication by a
nonzero scalar preserve multiplicities, so the conclusion holds for every
GL3 representative of the original projective element. This proves
Lemma 1 for the actual Hessian embedding.

For Corollary 2, H={class of diag(1,z,z): |z|=1} is an embedded circle
in PU3: its kernel in U1 is trivial. For any g in PU3,
J=Gamma intersect g^-1 H g is finite and cyclic. If J is trivial it fixes
every flex. Otherwise choose one generator gamma. It has a representative
conjugate to diag(1,z,z), z!=1, and hence has a repeated eigenvalue.
Lemma 1 implies that this generator fixes a flex p. Every element of J
is its power and fixes the same p. This establishes one common fixed
point, not merely a different point for each group element. The proof is
uniform in g and does not depend on a finite sample of conjugating
unitaries.

For the geometric interface, the fiber over gGamma of
PU3/Gamma0 -> PU3/Gamma consists of gkGamma0 and identifies with S by
gkGamma0 -> kp0. An h in H intersect gGamma g^-1 acts by g^-1 h g in J
under this identification. A common fixed flex therefore is exactly a
fixed point of that isotropy group in the fiber. Its H-orbit maps
homeomorphically onto the base H-orbit, and h(gGamma) -> h(e) gives a
section there. This justifies the point needed by the later tubular
neighborhood argument; it does not require free H action.

Finally C is a useful adversarial boundary example. It fixes x=0 (three
flexes) in the affine labeling and has two three-cycles on x=1 and x=2.
Its monodromy type is 1^3 3^2. Since C has a double eigenvalue, its
cyclic group lies in a conjugate of H and really can occur as nontrivial
circle isotropy. It supplies a section along that orbit while permuting
six sheets. Thus the mechanism selects one flex and cannot be promoted
to simultaneous trivialization of all nine sheets.
