# Independent quantitative derivation and adversarial audit

AI-assisted and unrefereed. Scope is the frozen PR 563 proof for problem
2306072. This derivation was completed before reading its prior independent
audit. All constants below are exact integers or rationals. The executable
certificate is `quantitative_checks.py`; it does not replace the analytic
arguments given here.

## Claim, assumptions, and success criterion

Let E=10^-24 and h=10^-12, so E=h^2. The claim is that every maximizer of
Re[a2+iE(a4-3a3)] has an omitted arc on which continuous argument, signed
outward radial angle, and ordinary nonnegative outward radial angle all fail
monotonicity. Success for this family means that the exact differential, every
quantitative estimate, inverse construction, tip exclusion, and angle
implication hold uniformly for every maximizing map, with explicit positive
margins. A constructed formal trajectory alone would not meet this criterion.

Imported premises, reviewed by another audit family, are compactness of S,
|a_n|<=n for n=2,3,4, the exterior area theorem, and the precise support-slit
theorem: the omitted set is an analytic arc from a finite tip to infinity,
radially ordered, satisfying Q(w)dw^2>0 with the differential stated below.
The quantitative audit does not establish the published theorem's hypotheses
or historical priority. Local uniqueness near infinity can also be derived
directly below, once that differential applies to the actual omitted arc.

## 1. Coefficients and uniform near-Koebe uncertainty

For a generic perturbation L=a2+iE(c3*a3+c4*a4), solve
(f-w)H=f^2 in power series using u=1/w and the recurrence
H=-u*f^2+u*f*H. Coefficients through order four are

    H2=-u,
    H3=-2*a2*u-u^2,
    H4=-(2*a3+a2^2)*u-3*a2*u^2-u^3.

Thus Phi=-a/w-b/w^2-c/w^3 and Q=Phi/w^2, where

    a=1+iE[2*c3*a2+c4*(2*a3+a2^2)],
    b=iE[c3+3*c4*a2], c=iE*c4.

Setting c3=-3,c4=1 gives A=2*a3+a2^2-6*a2 and B=3*a2-3.
This coefficient identity is exact and independent of a4, though a4 is
needed to obtain the maximizing comparison. The sign comes from the negative
constant -w in the denominator, rather than from a convention for a slit.

Koebe's value of Re L is 2. A maximizer therefore has
Re a2 >= 2-E|a4-3*a3| >= 2-13E. Combined with |a2|<=2 this gives
|a2-2|^2<=52E<64E and 1-|a2|^2/4<=13E. The latter follows because
Re a2>0 and |a2|>=Re a2. No maximizing selection or differentiability in E
is assumed.

The odd transform g(z)^2=f(z^2), g'(0)=1, is univalent: equality of two
values implies equality of the squared inputs, and in the remaining opposite
input case oddness would force g=0, hence both inputs zero. The exterior map
1/g(1/zeta) is then univalent, with coefficients
zeta-(a2/2)zeta^-1+(3*a2^2/8-a3/2)zeta^-3+... . The area theorem gives

    |a3-3*a2^2/4| <= 2*sqrt(13/3)*h < 5h.

Since |a2+2|<=4, |a3-3|<29h. The identities
A+2=2(a3-3)+(a2-2)(a2-4) and B-3=3(a2-2) give
|A+2|<106h, |B-3|<24h. These enclosures need not be achievable
simultaneously: proving a conclusion for the whole enclosure is stronger.

## 2. The actual tip gate

H(z)=sqrt(z/f(z)), H(0)=1, is analytic because f(z)/z is analytic and
nonvanishing in the disk. It has H=1-(a2/2)z+sum_{n>=2}c_n z^n, and
the same area theorem gives sum_{n>=2}(2n-1)|c_n|^2<=13E.
For r=2/3, weighted Cauchy-Schwarz gives

    |H-(1-z)| <= 4hr+sqrt(13)*h*sqrt(sum r^(2n)/(2n-1)) < 5h,
    |H'+1| <= 4h+sqrt(13)*h*sqrt(sum n^2*r^(2n-2)/(2n-1)) < 10h.

The first tail is at most r^4/[3(1-r^2)]=16/135<1/4. For the second,
n^2/(2n-1)<=n, so the tail is at most (1-r^2)^-2-1=56/25<9/4.
Both bounds hold on the whole closed radius-r disk; termwise differentiation
and convergence are justified inside the analytic disk.

At zstar=-2/3, H0=5/3. The deviation <5h gives 3/2<|H|<11/6,
|H+H0|<7/2, and |H^2+HH0+H0^2|<11. The middle bound is one
unstated intermediate step in the frozen proof; it follows from the much
stronger proximity estimate, so it is not a defect. Exact division yields

    |f-k| < (2/3)*(14/5)h < 2h.

For f'=(H-2*zstar*H')/H^3, the numerator differs from 1/3 by
<(5+40/3)h<19h. Its division by H^3 contributes <6h. The remaining
(1/3)|H^-3-H0^-3| contributes at most (1/3)*5*11/(125/8) h<2h.
Thus |f'-k'|<8h.

The distance inequality dist(f(z),boundary Omega)<= (1-|z|^2)|f'(z)|
has the correct direction: if a radius-d disk about f(z) is contained in
Omega, compose its inverse with a disk automorphism and scale the d-disk.
Schwarz's lemma bounds the derivative d/[(1-|z|^2)|f'(z)|] by 1.
Taking d up to the boundary distance proves the assertion. At zstar,
k=-6/25,k'=9/125, so the actual omitted arc contains a point of modulus
less than 7/25+7h<3/10. Its radial ordering makes the tip no farther out.
This argument concerns the actual maximizing image, not a formal extension.

## 3. Holomorphic inverse and whole-disk estimates

With w=-v^-2 and dw=2*v^-3*dv, direct Laurent multiplication gives

    Q(w)dw^2=4[a-b*v^2+c*v^4]dv^2 = 4P(v)dv^2.

On |v|<=3, P=1+iE P0+e_P with P0=-2-3*v^2+v^4,
|e_P|<322Eh, |P0|<=110, and |P-1|<111E=delta<1/4.
P lies in the right half-plane and has the analytic square root p with
Re p>0. The identity (p-1)(p+1)=P-1 and |p+1|>1 imply
|p-1|<delta. The integral G(v)=integral_0^v p is analytic and
|G-v|<333E throughout this closed disk. Rouché on |v|=3 against v-t,
for any |t|<2, gives exactly one root of G(v)=t because |v-t|>1
and 333E<1. G'=p never vanishes, so these roots patch into a holomorphic
inverse V on the whole |t|<2 disk; |V-t|<333E, V'=1/p(V), and
V(0)=0,V'(0)=a^-1/2. Evenness of p implies oddness of G and V.

An independent check of injectivity does not need the zero count. For any
v1,v2 in the convex disk, integrate p-1 along the straight segment:
|G(v2)-G(v1)-(v2-v1)|<delta|v2-v1|. Thus G is injective.
The Rouché boundary argument supplies existence over the target disk, while
this Lipschitz argument supplies uniqueness separately.

No denominator bound degenerates near t=0. Schwarz's lemma applied to
V(t)-t on |t|<2 improves its bound to |V/t-1|<=333E/2. Also
|V'-1|<=delta/(1-delta)<112E. Consequently

    |Z-1| < (112+333/2)E/(1-333E/2) < 279E,
    Z=tV'/V,

for every 0<|t|<2. Z extends at zero with value 1. In particular Re Z>0
for the full real interval 0<t<=7/4. This independently establishes that
increasing t follows W=-V^-2 radially inward, since
d log|W|/dt=-2 Re Z/t<0.

For 0<t<=7/4, |V|<9/5 and |W|>25/81>3/10. There are no zeros of
V except zero, because G(V)=t. Q is regular and nonzero on W. W has
Q(W)W'^2=4 and approaches infinity as -a/t^2. Any actual support trajectory
near infinity lifts to a v coordinate near zero; its natural coordinate G
has constant imaginary part, and that constant must be zero because it
ends at G=0. The positive and negative real G rays map to the same W
because V is odd. This derives local simple-pole trajectory uniqueness
directly. Local uniqueness continues identification with the actual slit
until a zero, pole, or tip; none occur on W, and the actual tip is inside
3/10. Hence this whole segment belongs to the actual omitted arc, provided
the imported support-slit theorem is applicable. W is injective for t>0:
equal W values force V(t1)=+-V(t2), hence t1=+-t2 by oddness of G.

## 4. Taylor, composition, and division remainders

The exact square-root identity

    sqrt(1+x)-1-x/2 = -x^2/[2*(sqrt(1+x)+1)^2]

gives error <=|x|^2/2 on the chosen branch. Therefore
|p-1-(iE/2)P0|<162Eh, because 161+(111^2/2)h<162.
Since P0=-2d', with d=t+t^3/2-t^5/10, integration gives
G(v)=v-iE d(v)+R_G(v), |R_G|<486Eh.
On the disk |d'|<=55, so solving G(V)=t gives

    |V-t-iE d(t)| < 486Eh+55*333E^2 <487Eh.

This is an exact finite-error estimate, not differentiation of a small-o
term or a real numerical fit. For the reciprocal root, Taylor's integral
remainder is valid on the complex segment from 0 to x. The second
derivative is (3/4)(1+x)^-5/2. On |x|<=1/4 it has modulus <4,
as checked by squaring the inequality; the integral factor 1/2 thus gives
|(1+x)^-1/2-1+x/2|<2|x|^2. Substitution of P(V)-1 costs
161Eh+24642E^2, and replacing P0(V) by P0(t) costs at most
(126/2)*333E^2=20979E^2. Thus

    |V'-1-iE d'(t)| <161Eh+45621E^2<162Eh.

These comparisons cover complex points, not merely the two endpoint values.
They use the straight segment between t and V, which remains in the convex
disk. They do not require the unknown coefficient errors to be real.

For real 1<=t<=T=7/4, q=d'-d/t=t^2-2*t^4/5 and |q|<7.
Write R_V=V-t-iE d and R_D=V'-1-iE d'. Multiplication before division gives

    V*(Z-1-iE q)=t R_D-R_V-iE q(V-t).

With |V|>1/2, the full error is bounded by
1541Eh+4662E^2<2000Eh. There is no dropped product or division term.
The exact endpoint margins are

    Im Z(1)/E > 3/5-2000h > 1/2,
    Im Z(7/4)/E < -441/640+2000h < -1/2.

The positivity margins over 1/2 are respectively 1/10-2000h and
121/640-2000h, both strictly positive. Re Z>0 also follows from this
interval estimate and, more strongly, the whole-disk estimate above.

An independently tighter certificate can use |v|<=2 and |t|<=7/4.
Then |P0|<=30, coefficient uncertainty <=202Eh, and |P-1|<31E.
Rouché's boundary gap is 1/4, exceeding 62E. The same exact identities
give |V-t|<62E, |V-t-iE d|<205Eh, and
|V'-1-iE d'|<102Eh. Constants follow from |d'|<=15,
|P0'|<=44, and 101+(1364+1922)h<102. Division yields
|Z-1-iE q|<768Eh. Thus the conclusion survives a reconstruction that
does not depend on the frozen proof's 333,487,162,2000 constants.

## 5. Argument and signed/unsigned radial angles

The nonzero analytic curve W admits a continuous real argument lift on the
interval. W'/W=-2V'/V=-2Z/t, so its derivative is -2 Im Z/t.
It is strictly negative at t=1 and strictly positive at t=7/4. A differentiable
monotone function cannot have derivatives of these two signs. This remains
true if parameter orientation or the argument lift is changed.

Increasing t is inward; the outward tangent is -W'. Its ratio to the radius
vector is (-W')/W=2Z/t, not -2Z/t. Re Z>0 fixes its signed angle beta
uniquely in (-pi/2,pi/2), so beta=arg Z. Beta is positive at t=1,
negative at t=7/4, and tends to zero at infinity (t down to zero). A
nondecreasing beta with that initial limit cannot take the negative value;
a nonincreasing beta cannot take the positive value. No assertion that
opposite signs alone forbid monotonicity is being used.

There is a zero of beta strictly between the endpoints by continuity. The
ordinary angle between two nonzero vectors belongs to [0,pi]; here it is
|beta| since beta lies in (-pi/2,pi/2). It is positive at each endpoint and
zero at an interior point, so it cannot be monotone on even that compact
subarc. This addresses the sign-convention and unsigned-angle boundary cases.

## 6. Falsification attempts and exact scope

No quantitative falsification was found. We checked epsilon=0 explicitly:
the strict reversal then disappears, so the argument does not imply a false
Koebe counterexample. The general coefficient perturbation gives
q=(c3+6c4)t^2/3-2c4*t^4/5. An a3-only or a4-only perturbation lacks
opposite signs at the selected endpoints. These frozen controls are valid
first-order distinction tests, but do not verify analytic premises or actual
maximizer existence, and would not detect all implementation defects.

The independent certificate additionally rejects deliberately malformed
quotient signs, omitted -3a3, positive rather than negative double cover,
incorrect inverse first variation, inward tangent mistaken for outward,
dropped quartic q, enlarged parameter without reproof, and the zero-E
degeneracy. In particular an inverse sign flip still produces opposite
endpoint signs, so it must be detected by the inverse equation rather than
the endpoint predicate alone. All nine mutations are rejected.

Strongest verified result: the finite coefficient algebra, uniform complex
analytic estimates, inverse construction, tip-exclusion continuation, and
all three nonmonotonicity implications are correct conditional on the
imported classical support-slit and extremal premises. The exact remaining
gap for a whole-proof verdict is source-level verification that those
classical premises apply with the stated sign and global omitted-set
properties. That is outside this quantitative family's assigned remit.

No priority, novelty, peer-review, publication, or remote action is implied.

## 7. Supplemental limiting-case check after audit comparison

The preceding reconstruction was finished before reading the prior audit.
After comparison, we also checked the actual fixed-E expansion at infinity
to exclude using an interval-specific approximation down to zero. Direct
integration and inverse-series substitution give

    V(t)=a^(-1/2)t + b/(6*a^(5/2))*t^3 + O(t^5),
    Z(t)=1+b/(3*a^2)*t^2+O(t^4).

Here the O(t^4) is the analytic Taylor remainder for the fixed maximizer,
not the uniform E remainder in Section 4. With b=iE B, the leading imaginary
coefficient is E Re(B/a^2)/3. The already established enclosures imply
|A|<3, |a^-2-1|<7E, and |B/a^2-3|<25h. In the last estimate,
24h/(1-3E)^2+21E<25h, with E=h^2. Hence Re(B/a^2)>3-25h>0.
The actual angle has the positive leading t^2 coefficient sufficiently near
zero, and the argument derivative there is negative. Thus its limiting
behavior is consistent with eventual monotonicity near infinity, while the
bounded-subarc reversal remains strict. The qualitative first-order W and
argument displays in the frozen Section 7 also follow from substituting d
into W=-V^-2; they are not needed to certify either endpoint sign.
