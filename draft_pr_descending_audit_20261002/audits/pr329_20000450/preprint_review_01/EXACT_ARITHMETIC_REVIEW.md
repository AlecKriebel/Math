# Independent exact division and arithmetic assessment

This is review01's own proof assessment, written after the two genuine staged
freezes. Candidate formulas are hypotheses tested by new code and by direct
reading of primary proofs. Neither inherited PASS reports nor finite-field
samples are premises of this proof. The associated native actual receipts are
under `evidence/independent/` and `evidence/replays/`; computation failures are
retained. No publication clearance or seal is asserted.

## Division completeness from the group law

Complete the square on the Tate model with
`v=y+((1-beta)x-beta)/2`, so `v^2=f(x)=T_beta(x)/4` is a
monic cubic. For a point with `v != 0`, the tangent has slope
`f'(x)/(2v)`. Intersecting it with the cubic gives
`x(2P)=f'(x)^2/(4f(x))-c2-2x`, where `c2` is the quadratic
coefficient of `f`. Taking the secant from `P` to `2P` similarly gives
the triple abscissa as an exact rational function. These operations, rather
than an imported division polynomial, are implemented independently in
`tools/independent_torsion.py`. Clearing the difference of the double and
triple abscissae yields the printed fifth division polynomial. Independently
expanding it on the Tate curve gives each of the eleven printed coefficients
of `R_beta` and the factorization `psi5=x(x-beta)R_beta`.

The direct symbolic resultant computations give exactly
`Res_x(psi5,T_beta)=Delta_beta^6` and
`Res_x(psi5,psi3)=Delta_beta^8`. The Tate smooth locus has
`Delta_beta=beta^5(beta^2-11beta-1) != 0`, so neither the square-root
ordinate nor the tangent/secant denominator needed in this calculation
vanishes at a root of `psi5`. In particular, no order-two point occurs, and
`P != 2P` and `x(P) != x(2P)` whenever the secant construction is
needed. The equality `x(2P)=x(3P)` then says `3P=+/-2P` on the
completed-square cubic. The positive choice would imply `P=O`, impossible
for an affine point. Therefore `3P=-2P`, giving exact order five. Conversely,
order five implies the same abscissa identity. The argument is about points
on a smooth cubic, so equality of x-coordinates has exactly these two
possibilities and denominators have already been justified.

The standard separability fact is used in a precise way: multiplication by
five on a characteristic-zero elliptic curve has degree25, is separable and
has25 distinct geometric kernel points. I directly reread Sutherland
Lecture5, Theorems5.8 and5.25 and their proofs; the primary family also read
the operative division-polynomial sections. The24 nonzero points form12
pairs under negation and therefore have12 distinct abscissae. This proves
that the degree12 `psi5` has simple roots, not merely that a resultant is
nonzero. The directly checked values `R_beta(0)=5 beta^8` and
`R_beta(beta)=5 beta^12` separate its ten roots from the two marked
abscissae. Both distinct ordinate signs at every residual root give exactly
twenty points. Together with the four marked points and the origin, this is
the complete geometric kernel on every allowed member, including special
j-values and the cuspidal plane member's smooth normalization.

Own finite enumeration is a falsifiable diagnostic of this exact argument:
518 smooth fibers and32922 affine points on a grid including both j=0 and
j=1728 agree with an independently written completed-square group law.
Changing the residual constant coefficient, dropping the marked subgroup,
or retaining only one ordinate sign is rejected on all518 fibers. These
counts are deliberately broader than simply running supplied assertions;
they are still not a proof about every characteristic-zero fiber. The first
own run correctly failed its coverage assertion because the initial grid
missed j=0; the retained diagnostic and corrected second run document the
added explicit p=31 control. Characteristic5 makes the leading coefficient
degenerate and lies outside the theorem; the symbolic negative control
detects that boundary rather than silently extending the argument there.

## The exact all-fiber Kummer bridge

Let `h=(11-5r)/2=-c^-1`, so `beta=h lambda/(lambda+5r)`.
Direct cross multiplication gives

```
iota(beta)=-1/(lambda+c),
(beta-c)/(beta+c^-1)=-c(lambda+c),
(c-beta)/(beta+c^-1)=c(lambda+c).
```

The excluded values `lambda=0,-5r,-c,infinity` correspond to
`beta=0,infinity,c,-c^-1`; these are exactly the Tate cusps. For an allowed
lambda, `a=lambda+c` is nonzero. If `theta^5=a`, then
`(-1/theta)^5=-1/a`, `(-phi theta)^5=-ca` and
`(phi theta)^5=ca`. All three generate the same radical field. The fixed
Kummer class of `-1/a` is the inverse of that of `a`, not generally the
same class; the manuscript expressly distinguishes fields from classes.

I directly read Fisher printed172,179,181-182,194 and Verdure printed84-88
in original images, and the independent primary family read additional
theorem context. Fisher's normal-curve construction parametrizes labelled
triples and the action `Q -> Q+P` has quotient X1(5). The absence of a
marked-point stabilizer is essential and is stated in Fisher Lemma1.1(iii).
It avoids coarse-moduli ramification at j=0 or1728. Fisher's exact parameter
map is the printed `tau f/g`; newly written exact rational code verifies
the Mobius identity and derivative numerator `(tau^2-tau-1)^4`. Its only
ramification targets are the omitted cusps. On the smooth base, both this
complementary-basis scheme and the explicit Kummer scheme are finite etale
and normal, with the same generic function-field cover. Normalization of
the normal base in that common extension identifies them everywhere. A
split fiber is an etale product and does not invalidate this reasoning.

There is also a separate, direct specialization theorem. Verdure Theorem5
assumes characteristic different from five and a nonzero Tate discriminant.
Its proof pp84-88 works with polynomial projective formulas; the final
paragraph explicitly says the discriminant and required parameter
differences survive every permitted specialization. Its criterion is
exactly the second ratio above. His Proposition3/Corollary1 give coordinate
degree one or five once the marked point and fifth roots of unity are
present. Over any characteristic-zero field F containing zeta, the criterion
makes the entire torsion rational over F(theta). If theta is not in F,
the degree is five and the criterion excludes trivial coordinate extension,
so the coordinate field is precisely F(theta). This is a valid degree
argument after adjoining the radical, not the unsupported assertion that a
generic irreducible polynomial remains irreducible in every fiber.

Morton's original v1 already prints the exact residual table and radical.
I compared the original v1/v4 tables and v1 radical images; all eleven
coefficients agree under `b=-beta` and the radical is `ca`, with the
correct sign. These are old universal formulas. The candidate's credit
accurately limits its contribution to this plane-model bridge. No claim of
firstness follows from my source review or the supplied bounded audit.

## Recovering the exact field and its groups

The independent geometric proof verifies the actual signed isomorphism
over M=K(delta), not just equality of j-invariants. Thus for
L=K(delta,zeta), the preceding all-fiber result gives
`L(E[5])=L(theta)`. The mapped marked point has ordinate
`eta=-k^3 d beta delta/2`; its coefficient in K is nonzero on every
allowed fiber. Hence `K(E[5])` contains delta. The nondegenerate,
Galois-equivariant Weil pairing on a basis of the full kernel takes a
primitive fifth-root value and puts zeta in the coordinate field. I directly
reread Sutherland Lecture23, Theorem23.29 and Corollary23.30; this use is
exactly the stated corollary. These two lower inclusions give L inside the
coordinate field, whence the upper equality over L gives
`K(E[5])=K(delta,zeta,theta)`.

The quadratic extensions are independent. The rational norm of d is five.
If d were a square in K, its norm would be a rational square, which five is
not. Thus M/K is quadratic and real. K already contains the real quadratic
subfield of the fifth cyclotomic field; K(zeta)/K is imaginary quadratic.
It cannot equal the real extension M, so L/K has degree four.

For any v in L with `v^5=a` in K, put `n=Norm_L/K(v)`. Then
`n^5=a^4` and `(a/n)^5=a`. Therefore adjoining L does not change
the fifth-power criterion for a in K. Kummer theory over L gives degree one
or five, so the total coordinate degree over K is respectively four or
twenty. There is no omitted intermediate degree.

For nonsplit a, the normal splitting field B=K(zeta,theta) has degree ten;
the fifth-root rotation has order five and complex conjugation, fixing a
real choice of theta, inverts it. Thus its group is the order-ten dihedral
group. The unique quadratic subfield of B is K(zeta), because the unique
index-two subgroup is its order-five rotation subgroup. Since this differs
from M, `B intersect M=K` and the full group is `D10 x C2`.
For split a it is the biquadratic group. Generic a has valuation one at
lambda=-c in K(lambda), so it cannot be a fifth power; the generic degree
is twenty by the same argument.

The independent delta involution fixes B and acts through the twist as
`-I`, eliminating every nonzero K-rational fifth torsion point. M is real.
For any real elliptic curve, its identity component is a circle and its
other possible component has quotient of order two; odd five-torsion lies
in the circle and has exactly five points. The infinity subgroup already
provides those five, hence `E(M)[5]` is exactly it. With first basis vector
the marked point, complex conjugation has eigenvalues1,-1 and can be
diagonalized by altering the second vector (two is invertible modfive).
The order-five radical action has a nonzero upper transvection: it fixes
the first vector and is nontrivial on the complementary basis. The delta
action commutes as -I. These matrices and the omission of the transvection
in the split case match the manuscript. An additional independent finite
grid checks1136 fibers across all six twist/cyclotomic/radical categories;
those reductions diagnose signs but are not used for the field proof.

## Assessment

No substantive division, all-specialization, Kummer-sign, degree,
intersection, rational-subgroup or Galois-action defect is identified. The
proof depends on the directly checked classical elliptic/modular results
above, not a formal proof assistant. The source-family resolvent formulas
were read as a published theorem proof rather than reimplemented term by
term. The primary family had a source-first reading sequence but no
pre-candidate written family freeze; the geometric family first read the
candidate, then AIM. Neither saw inherited reports or supplied programs.
These limited family exposures are distinguished from this whole review's
genuine independent early freezes.
