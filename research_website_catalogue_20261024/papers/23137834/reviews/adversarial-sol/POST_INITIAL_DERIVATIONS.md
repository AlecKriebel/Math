# Post-INITIAL adversarial closure

This is the continuation of the immutable source-first hand results. The source
claim was a hypothesis at that gate. This document uses the selected actual
primary passages recorded in PRIMARY_READINGS.json, after that gate. No current
root/peer findings, archived reports, README, acceptance or result bodies were
read. The separate scope family's methods and conclusions were not requested.

## Geometry: components, denominators and all finite parameters

Use the manuscript's r, phi, c, d, m, lambda, A, B, C. Put H0=5phi+lambda,
J0=5phi^3+2lambda, N0=c+lambda. Then

 B^2-4AC = 320X^6-128H0X^5+80J0X^3-40N0X+(J0^2-4H0N0).

Writing a=40+20r+8lambda, one has H0=(a-20)/8, J0=a/4,
N0=(a+4)/8. The constant is a+5=b. Multiplication by
(4X^2+2X-1)^2 gives the displayed sextic from 20X^2-aX+b, coefficient
by coefficient; its X^4 and X^2 coefficients vanish. Also
a^2-80b=64lambda(lambda+5r). Thus the first quadratic extension is
nontrivial on every proposed allowed fibre, not just generically.

Here is a compact cleared certificate for the other rational substitution.
It avoids treating numerical fibres as a proof. With z=t+d and l=lambda, set

 D=4rz+8l=4r(z+gamma*l),
 N=-z^2+2dz+8l,
 R=2rz^2+8lz-40l,
 H=15+5r+(alpha+gamma)l.

Then X=N/D, V=R/D and

 A_num=10N+H0*D=-10(z+alpha*l)(z-H),
 H_num=(4N^2+2ND-D^2)R+20N^3-2H0*N^2*D+J0*D^3
       =-4m(z-H)z^2 F(z).

These are finite polynomial identities in Q(r)[l,z], r^2=5. They supply
an explicit coefficient-checkable certificate: N,D,R above, followed by the
four-term expression for H_num, require no geometric assumption. For example
the leading coefficient is 8r-20=-4m, its constant and linear coefficients
are zero, and the remaining factor is exactly the displayed cubic F.
Substitution in Y^2=H_num/(2*A_num*D^2) gives

 Y^2=m*z^2*F(z)/(400*(z+gamma*l)^2*(z+alpha*l)).

This is an algebraic derivation, not a claim that geometry.py was executed.
The full original geometry.py was read afterwards as a static, executable
certificate of these same identities. It was not used as a replacement
for the function-field argument.

Expand F(s-alpha*l)=s^3+C2*s^2+C1*s+C0. Independently collecting gives

 C2=-(6+2r/5)l-40-20r,
 C1=((38-2r)/5)l^2+(100+60r)l+900+400r,
 C0=(-16/5+16r/25)l^2(l+5r).

The printed coefficients are a0=m, a1=m*C2, a2=m*C1, a3=m*C0.
In particular a3 is nonzero on the allowed range. The substitutions
s=a3/xi and eta=xi*w therefore yield the asserted cubic, and the inverse
fractions cancel on dense open charts. The recovered X identity is just the
original quartic divided by h^2; the recovered Y cancels literally. These
are maps of the entire function fields, extended uniquely to their smooth
projective curves, not a promise that every affine fraction is defined at
every point of a singular plane model.

For the global component objection, A has only X0=-H0/10. Direct substitution
gives B(X0)=l(l+5r)(l+5(phi+1))/25. The only additional possible common root
outside the two line members is l=-5(phi+1); there X0=1/2 and
C(X0)=1/16-5/16+5/4-2=-1. Thus A,B,C are primitive, including this
tempting false-positive counterexample. The quartic has a nontrivial conic
square root and then four odd branch points: three roots of F and s=0.
This proves irreducibility over the algebraic closure of the coefficient
field and genus one. Primitivity promotes the function-field assertion to
the whole affine curve. The nonzero restriction at T=0 excludes an extra
projective T component.

## Twist sign and discriminants without a j-invariant shortcut

Set L=l+5r, A0=(11-5r)/2=-phi^-5 and B0=(-112+48r)/5=-32phi^-4/5.
Then beta=A0*l/L, a3=B0*l^2*L, q=Q0*L^2 with Q0=16d/5,
and m=r*phi^-3, d=r*phi^3. Expanding the completed Tate cubic after
x=xi/q+beta gives

 q^3*T_beta(xi/q+beta)/4
 =xi^3 + q*(beta^2+6beta+1)*xi^2/4
        +q^2*beta^2*(beta+1)*xi/2 +q^3*beta^4/4.

For the linear coefficient Q0^2*A0^2/(2B0)=-4; hence division by a3
gives -4*((A0+1)l+5r), exactly a1. The constant identity is
m*B0^2=Q0^3*A0^4/4. For the quadratic coefficient the polynomial before
multiplication by Q0/4 is

 ((191-85r)/2)l^2+(175r-375)l+125,

which gives exactly a2. This independently fixes the sign, translation and
scale of the twist. The ordinate multiplier must be (k*delta)^3; a mere
delta, or an equality of j-invariants, would not establish the claim.

The parameter relation is
 beta^2-11beta-1=125*A0*(l+c)/L^2.
Consequently q^6*Delta_beta is

 125*Q0^6*A0^6*l^5*L^5*(l+c)
 =2^24*(161-72r)*l^5*L^5*(l+c),

using Q0*A0=-16phi^-2/r and phi^-12=161-72r. This proves the printed
Weierstrass discriminant uniformly. For a monic cubic q_s=s^3+C2*s^2+C1*s+C0,
the reciprocal-root substitution xi=m*C0/s gives
disc(f_W)=m^6*C0^2*disc(q_s). Combining this with Delta_W=16disc(f_W)
and the above C0 gives

 disc(F)=2^10*phi^8*l*L^3*(l+c)
        =(24064+10752r)*l*L^3*(l+c).

At l=-c this discriminant has a simple zero as a polynomial in l, while
C0 is nonzero. A triple cubic root would force discriminant order at least
two (depress the cubic: disc=-4p^3-27q^2 with p=q=0 there). Thus exactly
one double root, not a triple root, occurs; it is not s=0. Cancelling its
square leaves two odd branch points and genus zero. At 0 and -5r one
has the two actual five-line products. The infinite pencil member TQ^2
is outside the theorem. At the allowed plane cusp parameter
-(25+10r)/4 neither nonzero discriminant factor vanishes. A singular plane
picture therefore cannot be used to exclude that elliptic normalization.

The origin check is also uniform: at cubic infinity ord(xi)=-2,
ord(eta)=-3. The inverse X is finite and Y has a simple pole, giving
[0:1:0], whose plane X partial equals 10. No additional origin shift was
silently made. The five distinct slopes at infinity are 0, +/-delta,
+/-r/delta; they are smooth and cyclically permuted by the pentagon rotation.
An order-five automorphism has trivial origin-fixing part in characteristic
zero, hence is a nonzero five-torsion translation. Its orbit is the known
subgroup. The original source already observes that subgroup.

## Exact fifth kernel and bad-characteristic controls

The hand chord calculation of the four marked points is frozen in INITIAL.
The actual Morton v4 section 2 residual table, with b=-beta, matches all
eleven coefficients of R_beta, including signs of its odd powers. The
general division-polynomial recurrence in the actual Sutherland passages
gives psi5=T_beta^2*H6-psi3^3=x(x-beta)R_beta. This is not an appeal to a
stored native PASS. The whole native division_chord.py was additionally read
as a static independent doubling/tripling certificate, but not executed.

For nonsingular characteristic-zero D_beta, [5] is separable of degree 25.
Thus the nonzero kernel has 24 distinct points, paired by negation into
12 distinct abscissae. A nonzero point of order 5 cannot also have order 2
or 3, which independently rules out vanishing branch and chord denominators.
The two marked abscissae are distinct because beta is nonzero, and
R(0)=5beta^8, R(beta)=5beta^12 exclude their recurrence in the residual
factor. Hence its ten roots and both distinct ordinate branches give
exactly twenty additional points. The source resultants Delta^6 and
Delta^8 agree with this denominator argument; completeness does not require
accepting an unexecuted resultant calculation as its sole justification.

The inverse-chart identity gives z+gamma*l=(gamma-alpha)l*x/(x-beta).
At residual roots x is neither 0 nor beta, so the printed inverse has no
new excluded affine denominator. Its extension at normalization poles is
separate from a false everywhere-affine formula. Morton u denominators
u+zeta^j require u^5=-1, which corresponds to the already excluded
l=-5r; zero numerators require u^5=c^2, corresponding to l=0. The u=0
boundary is l=-c. None supplies a missing allowed finite fibre or a j=0,
1728 exception. Characteristic 5 is explicitly outside the theorem; the
leading coefficient and separability argument fail there. The frozen F7
calibration shows geometric 25 is not a rational-point count, and was not
misrepresented as a characteristic-zero pentagon counterexample.

## Specialization and the full field: necessity as well as sufficiency

The potentially serious issue was transfer from a generic radical identity
to every allowed specialization. The actual Fisher section 2 describes
Y(5) as (E,P,Q) with prescribed Weil pairing, its five translations Q+jP,
and quotient by that action. Aut(E,P) is trivial for a point of order 5.
Lemma 3.4's printed arithmetic statement is over Q; I do not misquote it
as itself a theorem for every field. Its rational parameter identity and
the fine moduli cover extend in characteristic zero to the cusp complement.
Two normal finite etale covers with that function field coincide there,
including unmarked exceptional j-values. This explains the specialization
step in the source's proof.

More decisively, the actual scanned Verdure Theorem 5 and its proof at
printed pp.84-88 explicitly apply to every nonsingular parameter over
characteristic different from 5. Proposition 3/Corollary 1 at pp.80-81
give cyclic degree 1 or 5 and equality of full/x-coordinate fields after
adjoining the fifth roots of unity. In that convention

 alpha5=8+5(zeta+zeta^4)=c,
 beta5=3-5(zeta+zeta^4)=-c^-1,
 (beta-c)/(beta+c^-1)=-c*(l+c).

Since -c=(-phi)^5, this has the fifth-power class of a=l+c. The actual
resolvent proof specializes polynomial projective coordinates with nonzero
Delta and the two nonzero cusp factors; it does not assume irreducibility
of each specialized quintic. Morton's actual radical ratio is c*a, giving
u_M=phi*theta. Fisher's coordinate instead gives -1/a and u=-1/theta.
The last Kummer class is the INVERSE of [a], not an equality of fixed
nontrivial classes. The fields coincide. These different conventions are
consistent after explicitly stating the coordinate inversion.

Over L=K(delta,zeta), the twist is an isomorphism, and Verdure proves the
Tate fifth field is L(theta). Necessity follows either from the fine
cover or from cyclic prime degree and the non-fifth-power criterion.
The image of P0 has ordinate -k^3*d*delta*beta/2, a nonzero K multiple
of delta, so the full W field contains delta. The actual nondegenerate,
Galois-equivariant Weil pairing supplies zeta. Therefore it already
contains L and equals K(delta,zeta,theta), in both the split and nonsplit
cases. This avoids the incorrect inference from a rational infinity line
or a semisimplification to the full extension.

The remaining constant-field and group arguments can be checked by hand.
N(d)=5 prevents d from being a square in K. M=K(delta) is real quadratic
over K and K(zeta) is imaginary quadratic, so [L:K]=4. If v^5=a in L,
N(v)^5=a^4 and (a/N(v))^5=a, so a becomes a fifth power in L iff it was
one in K. In the nonsplit case the cyclic order-five radical extension
over K(zeta) is inverted by complex conjugation fixing the real radical.
Its group over K is D10; its unique quadratic subfield is K(zeta), so it
is disjoint from M over K. The full group is D10 x C2, or C2 x C2 in
the split case. The generic valuation at l=-c is one, proving the generic
degree twenty without imposing generic irreducibility on every fibre.

The independent delta involution acts by -I, so the K fixed subspace in
E[5] is zero. Over the real field M, E(R)[5] has only five elements and
the known infinity subgroup already supplies them. In a basis with that
generator first, the cyclotomic involution can be diagonalized to
diag(1,-1); the Kummer generator is a nonzero transvection, normalized to
upper-right entry one. With the delta -I these are exactly the printed
representation, and it has the advertised group and fixed spaces.

## One finite falsification route, and its exact limits

The sole ordinary native execution was arithmetic.py in the owned directory
with its byte-identical source copy, no arguments and no optimization.
Its exact standard-library arithmetic, finite-field group law, cover root
counts and matrix fixed spaces were read before execution. Actual exit 0,
1669-byte stdout and empty stderr are retained. There was no program,
environment or mutation campaign and no second scientific run.

For primes with r in Fp, cyclotomic chi is +/-1. Let psi be the d twist
character. When chi=1, an untwisted split/unipotent Frobenius fixes 25/5
elements; twisting by -1 fixes only the identity. When chi=-1, the two
eigenvalues are 1,-1 even after twisting, so five elements are fixed.
This independent matrix prediction agrees with every actual reported
category, including cases where twisting does NOT remove the finite-field
five-line. Thus the global K-rational zero is not incorrectly inferred
from every nonsquare finite-field twist. The run checked 1364 good fibres,
306424 affine points and 1364 cover fibres. These are implementation
checks, not a proof of all characteristic-zero specializations. The
hand proof and actual primary specialization theorem supply that proof.

No substantive defect in the original quantified theorem was found by
these attacks. No repaired or narrowed substitute is promoted. This is
bounded independent mathematical and computational checking, not a formal
proof-assistant certificate, human peer review or a new priority survey.
