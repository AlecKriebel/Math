# Independent physical geometry and exact algebra audit of k904,a

Scope: authenticated original/revised source bodies for PR211 / 5100063.
The exact claim and this family's raw-geometric falsification mechanism were
frozen before any candidate or old verdict was read. No old review or acceptance
label supplies proof authority. No historical checker was imported or executed.

## 1. Exact target and primary readings

Let E: x²/a²+y²/b²=1, a>b>0, c²=a²-b², with original foci f±=(±c,0).
The caustic is a strict proper nested confocal ellipse with axes alpha>beta>0
and alpha²-beta²=c². Fix an odd least period N>=3 and coprime turning number
0<tau<N/2, including stars. Q_i is the intersection of consecutive tangents
to E at original billiard vertices. Unit-invert Q_i about each original focus,
join the inverse vertices by straight segments in orbit order, and take signed
shoelace areas B±. The target is phase independence of B+ B−.

I independently fetched, extracted and visually read complete relevant pages of
[arXiv2004.12497v11](https://arxiv.org/pdf/2004.12497v11): Table10 p12
(k904,a, the primed dagger product, odd N); Section3.9 pp9–10 (unit circles,
original foci, outer vertices identified by primes, outer-locus foci carrying
different symbols); and Section2 p3 (signed cross-product area). The introduction
specifies a confocal ellipse pair. This supports the target above and excludes
substitution of original vertices, pedal projections, outer-locus foci, inverse
whole-edge arcs, or unsigned filled-star area. Hyperbolic, collapsed and grazing
caustics are outside this claim.

I independently read rendered p1614 of Stachel's published
[Theorem4.3/(4.9)](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf).
It supplies the canonical parameters below; its modulus is the caustic's
eccentricity. Mpmath's parameter is its square. A separately printed dn real-shift
sign typo in that source is unused: real dn is positive and has period 2K.

The fetched PDF hashes are c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da
(arXiv) and 9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8
(Stachel). HTTP receipts, private reading notes, PDFs, extracted text, and five
85-dpi page renders are excluded from the authored manifest. Web screenshots
failed; local Poppler renders were inspected instead. No broad literature or
historical novelty assessment is asserted.

## 2. Raw two-line tangent solve, transversality and reversed axes

Use modulus k=c/alpha in (0,1), k'=beta/alpha and complete real quarter period K.
Stachel gives

    P(w)=(-a sn(w), b cn(w)),
    v=2K tau/N in (0,K), delta=2v,
    h=sn(v)>0, C=cn(v)>0, d=dn(v)>0,
    a=alpha d/C, b=beta/C,
    t=h², q=C²=1-t.

Thus a²-b²=alpha²k²=c² and d²-C²=k'²t>0, proving strict nesting.
The real map (sn,cn) is one-to-one modulo 4K. Hence gcd(tau,N)=1 gives least
period N. Reversal allows taking the stated positive turning numbers.

Set s=sn(u), r=cn(u), e=dn(u), H=1-k²ts². Addition gives

    s±=(s C d ± h r e)/H,
    r±=(r C ∓ s h e d)/H.

The actual tangent equations are -X s±/a+Y r±/b=1. Their determinant, minus
row followed by plus row, is

    (s+ r− − s− r+)/(ab)=2hCe/(abH)>0.

Cramer's rule gives X/a=-d s/C, Y/b=r/C, so

    Q(u)=(-Ao sn(u), Bo cn(u)),
    Ao=a d/C=alpha d²/q, Bo=b/C=beta/q.

This is a line solve, not an assumed fitted locus. No real intersection is at
infinity. Independently, parallel tangents to a strictly convex centered ellipse
would require identical or antipodal vertices. The latter chord passes through
the origin, so cannot be tangent to a strict nested ellipse containing it.

Both Ao>a and Bo>b, and

    Qx²/a²+Qy²/b²=(d/C)²s²+(1/C)²r²>1.

Thus every real Q is outside E and avoids both original foci, which lie inside E.
These facts hold even when the outer axes reverse. Put

    U=1-2k²t+k²t², V=1-2t+k²t², W=1-k²t².

Then Ao²-Bo²=alpha² k² V/q². Since V=W cn(2v), the outer long axis is the
y-axis when v>K/2, including N3 and many stars. It is not legitimate to assume
that ±c on the x-axis are the outer locus's own foci.

## 3. Physical Euclidean inverse coordinates and distance factorization

The actual center-inclusive inverse is J_f(Q)=f+(Q-f)/D_f, D_f=||Q-f||².
For signed polygon area we may translate the entire inverse polygon by -f and
use I_f=(Q-f)/D_f. Translation terms telescope in the cyclic sum. Individual
center-inclusive edge determinants differ from the translated edge kernel;
their complete area sums agree.

For f+=(c,0), direct expansion from the raw Q gives

    D+(u)=alpha²/q² [(d²s+kq)²+k'²r²]
         =alpha²/q² (1+ks)(U+kVs).

Coefficient checks are d⁴-k'²=k²V, k'²+k²q²=U and U+V=2qd².
Consequently the actual translated Euclidean inverse is

    I+(u)=(q/alpha) (-(d²s+kq), k'r)/[(1+ks)(U+kVs)].

For real u, 1+ks>=1-k>0, W>0, U=W dn(2v)>0, and
U²-k²V²=k'²W²>0. All real inversion factors are positive.
Complex continuation uses bilinear sums of squares. Introducing conjugation
would destroy meromorphicity.

## 4. Exact edge determinant, the q^4 normalization and triple factors

Define

    L0=(U²-k²V²t)/d, L1=(V²-U²t)/C,
    C0=Bo h d q⁴/(alpha³ C).

Expanding the two raw outer vertices yields

    det(Q(u-v)-f+,Q(u+v)-f+)/2
      =alpha Bo h d e (d+kCs)/(C H).

The exact shifted products are

    (1+k s−)(1+k s+)=(d+kCs)²/H,
    (U+kV s−)(U+kV s+)=(d+kCs)(L0+kL1s)/H.

The second cross coefficient reduces to

    d²(V²-U²t)+q(U²-k²V²t)=2UV q d².

Therefore

    D+(u-v)D+(u+v)
      =(alpha⁴/q⁴)(d+kCs)³(L0+kL1s)/H²,

and the physical translated inverse edge is exactly

    E+(u)=det(I+(u-v),I+(u+v))/2
         =C0 e H/[(d+kCs)²(L0+kL1s)].

The factor is q⁴, with q already equal to C². There is no missing factor of two,
center translation, or edge-arc contribution. The dimensional check is E having
units length^(-2), and the product having units length^(-4). Under spatial
dilation by lambda, the unit inverse areas scale by lambda^(-2), the product by
lambda^(-4).

Put

    Z=W²-4k²t²q d²=W²[1-k²t sn²(2v)]>0,
    D3=UW-2k²tqV, C3=VW-2td²U.

Exact polynomial identities give

    U²-k²V²t=d²D3, V²-U²t=qC3,
    dn(3v)=d D3/Z, cn(3v)=C C3/Z,

using addition of v and 2v, whose denominator is Z/W². Thus

    L0=Z dn(3v), L1=Z cn(3v),
    L0²-k²L1²=k'² Z²>0,
    d²-k²C²=k'²>0.

Real dn is positive, so L0>0. Both d+kCs and L0+kL1s are strictly positive
for real u; so are C0,e,H. Hence E+(u)>0 everywhere on the real line.
No area is divided out. For odd N, L1 cannot vanish: in 0<3v<3K an interior
zero cn(3v)=0 would require 3v=K, hence N=6tau.

EXACT_ALGEBRA_RESULTS.json records twenty exact rational-identity checks modulo
the explicit relations h²=t, C²=1-t, d²=1-k²t, r²=1-s², e²=1-k²s²,
k'²=1-k². Nonzero denominators follow from the strict real domain above,
not from cancellation alone.

## 5. Phase indexing, opposite focus and the remaining meromorphic mechanism

If the raw billiard vertices are P(w+j delta), then the raw tangent
intersection is Q(w+(j+1/2)delta). Its inverse edge to the next raw intersection
is centered at w+(j+1)delta. Therefore

    B+(w)=sum_(j=0)^(N-1) E+(w+(j+1)delta).

The manuscript may absorb the fixed v into its outer phase. No variable phase
shift or wrong half-step is present.

Since Q(u+2K)=-Q(u), the actual construction gives

    J_f−(Q(u))=-J_f+(Q(u+2K)).

Central reflection has determinant +1, so B−(w)=B+(w+2K).
This derives the opposite-focus relation directly. It is not an area-ratio
transfer from original-vertex inversion.

The kernel identity alone does not prove cyclic constancy. The candidate's
remaining meromorphic mechanism uses a real quotient period L=4K/N and
imaginary antiperiod 2iK'. A reflected pair of possible double poles, separated
by delta, has opposite quadratic coefficients; these cancel in the cyclic sum.
The triple-angle denominator gives possible simple poles in the same cyclic
pole class. Positivity rules out the zero function. The quotient torus then
has two simple poles and two simple zeros, exchanged by shift L/2, so the
half-period product has no poles and is constant. Odd N is used to identify
2K with L/2 modulo L. This is a universal divisor claim; sampling areas is not
its proof. A separate independent complex-divisor family is the primary audit
of that part. This family's independently verified real construction, kernel,
strict positivity and focus shift supply the required physical input.

The critical short odd case is real and cannot be omitted. N3 gives v=2K/3,
cn(3v)=-1, dn(3v)=1, so L0=Z and L1=-Z. The triple factor is Z(1-k sn u).
Its double zero at a critical sn fiber meets a simple dn numerator zero,
leaving at most a simple pole. Assuming two distinct ordinary roots without
this cancellation would leave a gap. The candidate treats it explicitly;
the exact triangle constructions below also verify L0/Z=1,L1/Z=-1.

## 6. Exact geometric triangles and an exact even boundary witness

EXACT_GEOMETRY_RESULTS.json records all raw Q and center-inclusive inverse
coordinates, all signed areas, and exact zero residuals for ellipse membership,
tangency of every orbit side to the same caustic, and specular reflection at
every vertex. These constructions do not evaluate only the candidate kernel.

Triangle A has (a²,b²)=(21,16), (alpha²,beta²)=(189/25,64/25), foci ±sqrt(5).
Two exact phases are

    (sqrt(21),0), (-3sqrt(21)/5,16/5), (-3sqrt(21)/5,-16/5),
    (0,4), (-21/5,-8/5), (21/5,-8/5).

For the first, B±=(7sqrt(21)∓sqrt(5))/1920. For the second both areas are
1/60. Both products equal 1/3600 exactly. Here k²=125/189,t=21/25,q=4/25,
d²=4/9. The raw outer loci have reversed axes.

Triangle B has (a²,b²)=(8,3), (alpha²,beta²)=(128/25,3/25), foci ±sqrt(5).
Use

    (2sqrt(2),0), (-8sqrt(2)/5,3sqrt(3)/5), (-8sqrt(2)/5,-3sqrt(3)/5),
    (0,sqrt(3)), (-8sqrt(3)/5,-sqrt(3)/5), (8sqrt(3)/5,-sqrt(3)/5).

The first gives B±=sqrt(6)/40∓sqrt(15)/160; the second gives both areas 9/160.
Both products equal 81/25600 exactly. Here k²=125/128,t=24/25,q=1/25,d²=1/16.
Both families are strict, noncircular, nondegenerate N3 billiards.

The odd restriction cannot be dropped for every primitive period. Take
(a²,b²)=(2,1), (alpha²,beta²)=(4/3,1/3), foci ±1. Same-caustic primitive N4
phases are

    (0,1), (-sqrt(2),0), (0,-1), (sqrt(2),0),
    (2/sqrt(3),1/sqrt(3)), (-2/sqrt(3),1/sqrt(3)),
       (-2/sqrt(3),-1/sqrt(3)), (2/sqrt(3),-1/sqrt(3)).

They yield respectively B+=B−=sqrt(2)/2 and B+=B−=3/4. Products are
1/2 and 9/16 exactly. This is a genuine same-family counterexample to an
unrestricted even extension; it does not assert that all even families vary.

## 7. Independent physical numerical falsification, controls and limits

independent_check.py starts with a real billiard point and constructs a genuine
caustic tangent. For R=(Px/alpha,Py/beta), its contact is

    T=diag(alpha,beta)[R+sqrt(||R||²-1) R_perp]/||R||².

It then uses Euclidean reflection and the nonzero second ray intersection with
E to propagate a full orbit. Closure, caustic tangency, reflection, turning
number and the published canonical sequence are independently checked.
Only then are raw two-line tangent intersections, actual center-inclusive
Euclidean inversions, and signed shoelace sums computed. Neither the candidate
Q formula nor its edge kernel generates the test areas.

The 85-digit run covers 109 families / 763 closed orbits / 10374 vertices:
all coprime turning numbers at N=3,5,7,9,11,13,15,17 for k=.2,.65,.94;
near-circle k=1e-8; near-collapsed-caustic k=.999999; N31/tau15 and
N101/tau1,50; and five even controls. Sixty families have y as the outer long
axis. Maximum odd relative product variation is 1.56e-79. Maximum normalized
geometry/kernel comparison residual is 8.80e-75. These are finite-precision
diagnostics, not interval-certified evidence for a universal theorem.

precision_probe.py repeats four limiting families at 130 digits. Every stored
24-significant-digit phase area and product agrees with the 85-digit run.
The hardest k=.999999,N31,tau15 relative product variation falls from
1.56e-79 to 3.42e-124. Results, methods and all individual phase values are
preserved in the JSON outputs.

Reversal changes both signs. A fixed r-fold traversal repeats each shoelace
sum r times, multiplying the product by r²; it creates no new least period.
These follow exactly from the definition and were tested using reversal and
threefold repetition of every computed raw Q list. The exact spatial
lambda^(-4) law was tested too.

Wrong-object controls are discriminating: for k=.65,N5,tau2, original-vertex
inversion gives product about .00989119613, while correct outer inversion gives
.0001067454310. The original-vertex quantity also appears invariant, so
constancy alone does not identify the target. Outer-locus own-focus inversion
gives different values at the two tested phases. Passing k rather than k² to
mpmath produces order-one closing-edge caustic errors. No generic original-
to-outer inverse-area transfer is established or used.

At k=0 the foci coincide. For circular E of radius R, v=pi tau/N, the outer
radius is R/cos(v), the unit-inverse radius cos(v)/R, and the signed area is

    B=N cos²(v) sin(2pi tau/N)/(2R²).

Its product with itself is phase independent by rigid rotation. This is a
separate exact circular argument. Strict-domain denominator bounds deteriorate
as k tends to 1 or v tends to K; neither these bounds nor the numerical runs
assert a theorem at a collapsed or grazing endpoint.

## 8. Strongest verified result and exact boundary of acceptance

No physical construction, normalization, real denominator, axis, modulus,
orientation or exact-algebra defect was found. The universal real-geometric
identification with E+, the q⁴ factor, triple identities, positivity, half-step
indexing, opposite-focus identity and repetition/scaling laws are deductions.
Exact triangles and the N4 counterexample are independently checkable finite
constructions. Numerical runs remain additional falsification attempts only.

This evidence does not substitute for the independent complete complex
pole/divisor review. That is the exact remaining proof-review dependency of
this physical family; no unsupported area transfer fills it. Root separately
controls full package/custody, priority, publication and acceptance gates.
No novelty certification, proof-assistant formalization, human peer-review
claim or endorsement of old release/receipt statements is made. No external
person was contacted and no Git, ref, PR, provider or publication state changed.
