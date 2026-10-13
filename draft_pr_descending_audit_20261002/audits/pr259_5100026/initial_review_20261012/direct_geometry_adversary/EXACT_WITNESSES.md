# Exact independent Cartesian controls

These constructions were derived independently before reading the submitted
PROOF.md or any submitted verification code.

## Four-bounce control

For a=5,b=3,c=4, points (5,0),(0,3),(-5,0),(0,-3) give
the strict nested caustic parameter lambda=225/34<9. At each point the
incoming and outgoing unit directions reflect in the ellipse tangent.
The outer tangent vertices are (5,3),(-5,3),(-5,-3),(5,-3), and their
antipedal about (4,0) is (-4,6),(-6,0),(-4,-6),(14,0).
Its arithmetic mean is (0,0). This alone is an exact special control.

## Repeated odd-period counterexample

Set a=5,b=3,c=4, D=sqrt(481), t=(D-9)/16, s=sqrt(1-t^2)>0.
Then 16t^2+18t-25=0 and 0.8<t<0.82 (direct evaluation of the polynomial
at the rational endpoints, and its positive derivative, certify the bounds).
The original billiard triangle is

P0=(5,0), P1=(-5t,3s), P2=(-5t,-3s).

It has three distinct points and least period 3. Its positive chord-length
witness between P0 and P1 is L=s(25+16t)/(3t); the other nonvertical chord
has the same length, and P1P2 has length 6s. Quotient-ring reduction modulo
16t^2+18t-25=0 and s^2+t^2=1 certifies all boundary, unit-direction,
specular-reflection and equal-caustic identities. The common caustic is

lambda=25(1-t^2)=225(D-17)/128.

Since 21<D<22, 0<lambda<1125/128<9: it is strictly nested, elliptical,
and nondegenerate. The central reflection of this triangle gives a second
physical orbit with exactly the same caustic. Neither is centrally symmetric
as a point list of least period 3.

Writing h=3(1+t)/s, the first outer triangle is (5,h),(-5/t,0),(5,-h).
Direct normal-line intersections about the ORIGINAL focus (4,0) give

Gplus_x=[5+9(1+t)/(1-t)-10/t]/3, Gplus_y=0.

The centrally reflected original triangle gives

Gminus_x=[-5-(1+t)/(1-t)+10/t]/3, Gminus_y=0.

Their difference is 20(2t-1)/(3t(1-t))>0. In particular, these two phases
of the same caustic family do not share the arithmetic mean. Gplus_x>0
already follows from t>0.8: (1+t)/(1-t)>9 and 10/t<12.5, so
Gplus_x>(5+81-12.5)/3>0. Thus the opposite-focus sign also fails for
this odd least period. All vertices and intersections are finite.

Repeating either triangle twice produces an even list with nominal N=6.
Every R and U repeats twice, so the arithmetic mean remains the same.
Consequently an even *listed count* does not suffice for the general
phase-invariance/sign assertion. This exact example does not refute the
primitive even least-period theorem. The source's use of N-periodics must
be interpreted or qualified so that even least period is required.

## Reproduction

Run `python exact_controls.py` with SymPy. Output
`exact_cartesian_witnesses.json` records all exact residuals, coordinates,
formulas and script hash. The rational quotient denominators are nonzero:
t,s,L,1-t,5-4,5+4 are positive, and 5/t+4 and 5/t-4 are positive under
0.8<t<0.82. The positive t,s choices eliminate extraneous algebraic roots.
No universal statement is inferred from finite numerical controls.
