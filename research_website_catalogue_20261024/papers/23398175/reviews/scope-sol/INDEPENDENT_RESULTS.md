# Independent source-first derivations and exact controls — 23398175

Completed before support comparison bodies/code/results, archived opinions, current root/peer findings or new foreign mathematical bodies. The native manuscript proof was necessarily read. Prior related geometry exposure is explicitly disclosed in INITIAL. No scientific program or numerical approximation was used for these results.

## 1. Canonical geometry independently reduced

Write s=sn(t), C=cn(t), d=dn(t), and s_v,C_v,d_v for v, using modulus k=c/alpha in (0,1), k'=beta/alpha. Given a strictly nested confocal pair, C_v=beta/b lies strictly between zero and one, giving a unique real v in (0,K). Confocality gives a=alpha d_v/C_v. Indeed
a^2-b^2=[alpha^2(1-k^2 s_v^2)-beta^2]/C_v^2=c^2,
and lambda=a^2-alpha^2=b^2-beta^2=beta^2 s_v^2/C_v^2>0.

A useful independent addition-formula check identifies the actual chord, rather than assuming eccentric anomaly is uniform. Set D=1-k^2 s^2 s_v^2>0. Jacobi addition gives
sn(t+/-v)=(s C_v d_v +/- s_v C d)/D,
cn(t+/-v)=(C C_v -/+ s s_v d d_v)/D.
For P(u)=(-a sn(u),b cn(u)), substitution shows BOTH endpoints P(t-v),P(t+v) satisfy
-s d_v x/a + C y/b = C_v,
or, using the above axes, -s x/alpha + C y/beta=1.
That is the tangent to the caustic at (-alpha s,beta C). Thus the chord step is exactly delta=2v. The two caustic tangents through P(w) lead to P(w-delta),P(w+delta); other-tangent continuation chooses a consistent orientation. Together with injectivity of real (sn,cn) modulo 4K this explains the canonical family representation. Closing with odd LEAST N means N delta=4K tau, gcd(tau,N)=1, 0<tau<N/2. Only admitted windings are claimed. Standard Jacobi addition/period conventions will still be checked against their actual primary source after this seal.

Since delta is strictly between 0 and 2K, consecutive vertices are neither equal nor antipodal. Their ellipse tangents are therefore distinct and nonparallel. If two consecutive outer vertices coincided, three distinct tangents to a nonsingular conic would concur, impossible by dual-conic degree two. Therefore all outer vertices/sides used by the definition are genuine and finite, for stars as well as simple polygons.

## 2. Actual perpendicular foot and auxiliary circle

The ellipse tangent at P(w)=(-a s,b C) is n.X=1, n=(-s/a,C/b). With F_+=(c,0),
n.n=(a^2-c^2 s^2)/(a^2 b^2)=(a-cs)(a+cs)/(a^2 b^2).
Projection F_++[(1-n.F_+)/(n.n)]n cancels the a+cs factor, giving
Q_+(w)=(a(c-a s)/(a-cs), ab C/(a-cs)).
This is a genuine Euclidean perpendicular foot on the OUTER SIDE LINE ell_j, not an antipedal vertex. For real phase a-cs>=a-c>0.

Using s^2+C^2=1 and b^2=a^2-c^2,
(c-a s)^2+b^2 C^2=(a-cs)^2.
Hence Q.Q=a^2. The complex continuation uses this BILINEAR identity, not a sum of absolute squares or a Hermitian dot product. Real feet lie on the origin-centered auxiliary circle of radius a.

Using sn(w+2K)=-sn(w), cn(w+2K)=-cn(w) gives Q_-(w)=-Q_+(w+2K). Multiplying all polygon coordinates by -1 preserves each determinant, so B_-(w)=T(w+2K), B_+(w)=T(w), where T is the actual ordered shoelace trace.

## 3. Complete pole count and order control

Put p=iK', r=K+p. At common simple poles of sn and cn, dividing numerator and denominator of Q by sn shows finite meromorphic limits; these points are removable. Other possible poles solve sn(w)=a/c=d_v/(k C_v).

The native quarter-period formulas are
sn(r+z)=dn(z)/(k cn(z)),
cn(r+z)=-i k'/(k cn(z)),
dn(r+z)=i k' sn(z)/cn(z).
A useful sign control: differentiating dn(z)/(k cn(z)) gives k'^2 sn(z)/(k cn(z)^2), which equals the product of the displayed cn(r+z) and dn(r+z). Thus the plus i sign in the last identity is internally consistent.

On the sn torus 4K,2p, degree two gives exactly the two roots r-v,r+v. They are distinct, since 0<v<K, and their cn/dn products are nonzero. In fact cn=-i b/c at BOTH roots, while dn has opposite nonzero values. The derivative of the denominator -c cn dn consequently has opposite signs. The numerator at BOTH roots is (-ab^2/c,-i ab^2/c), a nonzero common vector. Thus the two residues are opposite, collinear isotropic vectors.

The common VECTOR torus is 4K,4p. There are four Q poles there: the two above and their 2p translates. Treating 2p as a full period would lose an entire row and get the area character wrong.

At any singular phase of T, exactly TWO cyclic vertices in a given row are singular, at adjacent indices, because their pole locations differ by delta and coprimality makes the N real phases distinct modulo 4K. There are no simultaneous copies in the other imaginary row. If expansions are R/epsilon+A+... and -R/epsilon+B+..., the only potential double coefficient in the connecting edge is det(R,-R)=0. Every remaining edge has at most one singular endpoint. This includes N=3 and the edge crossing index N-1 to 0, since N delta=4K tau is an actual full-vector period. The translated row has the same conclusion. Thus all area poles are at most simple.

T has period delta by cyclic reindexing and period 4K. Bezout for coprime tau,N yields period L=4K/N. All the possible pole phases r-v-j delta collapse modulo L to b_0+p, b_0=K-v, with the second row b_0+3p. This gives precisely the stated at-most-two-simple-pole divisor on C/(L Z+4p Z). No claim that every possible pole actually survives is needed.

## 4. Reflection, zeros and the main universal product

The Jacobi shifts give Q(w+2p)=JQ(w) and Q(2K-w)=JQ(w), J=diag(1,-1).
The first reverses each determinant: T(w+2p)=-T(w).
For the second, Q(2K-w+j delta)=JQ(w-j delta); reflection negates determinants and reindexing the reversed cyclic order negates them again. Therefore T(2K-w)=T(w), with a plus sign.

Set F(z)=T(b_0+z). Since 2K-b_0=b_0+delta and delta is a period, F(-z)=F(z). F has periods L,4p, antiperiod 2p, and at most simple poles at p,3p.
At z_0=p+L/2, which is NOT a pole class, evenness and real periodicity give
F(p+L/2)=F(-p-L/2)=F(-p+L/2),
while the antiperiod makes the final expression -F(p+L/2). Hence F(z_0)=0, and similarly F(3p+L/2)=0.

The possible poles of G(z)=F(z)F(z+L/2) are p,3p,p+L/2,3p+L/2. At each, a zero in one factor cancels the other's at-most-simple pole. G is therefore holomorphic on a compact torus and is constant. If F has no poles it is constant and its antiperiod forces zero, which is already covered. No quotient by an area, no assumption that an area is nonzero, and no numerical inference occurs.

For odd N, 2K=(N/2)L is L/2 modulo L. Thus the actual focus switch has exactly the complementary shift needed, proving B_+B_- constant. For even primitive N it is an integer multiple of L and merely gives B_+=B_-, not constancy of their square. Coprime stars use the identical divisor argument; winding one was never assumed.

## 5. Exact triangular phases, actual reflection and side-line feet

Put a=sqrt(21), b=4, c=sqrt(5), lambda=336/25. The common caustic has alpha^2=189/25, beta^2=64/25.

For H=((a,0),(-3a/5,16/5),(-3a/5,-16/5)), the outer ellipse equations are immediate: 9/25+16/25=1 at the last two vertices. The chord H_0H_1 has line 2x+a y=2a; its caustic support-square is 4 alpha^2+a^2 beta^2=84=(2a)^2. The vertical chord x=-3a/5 has support-square alpha^2=189/25. The third is the reflected first. At H_1 the incoming unit vector is (-a/5,2/5), outgoing (0,-1); their difference is 7 times the ellipse normal (-3/(5a),1/5). At H_0 reflection flips the x component; the third vertex follows by symmetry. Thus H is a genuine primitive billiard triangle, not an arbitrary ellipse-inscribed triangle.

Its OUTER tangent lines are x=a and -3x/(5a)+/-y/5=1, with intersections (a,8),(-5a/3,0),(a,-8). Their actual focal feet are Q_0=(a,0), Q_1=(X,Y), Q_2=(X,-Y), where
X=a(5c-3a)/(5a-3c), Y=16a/(5a-3c).
Therefore B_+(H)=Y(a-X)=2688(a-c)/(5a-3c)^2=(49a+7c)/10.
Replacing c by -c gives B_-(H)=(49a-7c)/10.
Their product is (49^2*21-7^2*5)/100=12544/25.

For V=((0,4),(-21/5,-8/5),(21/5,-8/5)), the outer ellipse check is 21/25+4/25=1. Chord V_0V_1 is 4x-3y=-12, whose caustic support-square is 16 alpha^2+9 beta^2=144; its bottom chord is y=-8/5, tangent at the lower caustic vertex. At V_1 incoming/outgoing units are (-3/5,-4/5),(1,0), with difference 8 times the ellipse normal (-1/5,-1/10); V_0 is immediate y-reflection and V_2 is symmetric.

Its actual OUTER lines are y=4, -2x-y=10 and 2x-y=10, with outer vertices (-7,4),(0,-10),(7,4). Projecting F_+ yields
Q_0=(c,4),
Q_1=(c/5-4,-2-2c/5),
Q_2=(c/5+4,-2+2c/5).
Half the determinant of Q_1-Q_0,Q_2-Q_0 is (48-16c^2/25)/2=112/5. The same holds at F_-. Thus the product again is 12544/25. These computations independently distinguish actual tangent-side projection from merely manipulating the printed rational formula.

## 6. Distinct original-chord and inverse observables, by hand

On H, projecting F_+ to ORIGINAL chord lines gives (X,Y),(-3a/5,0),(X,-Y), with
X=(21c+4a)/25, Y=2a(a-c)/25.
Their signed area is Y(X+3a/5)=84(7a+c)/625. The other focus gives 84(7a-c)/625. The product is 84^2*(49*21-5)/625^2=7225344/390625.
On V, original-chord feet are
((9c-48)/25,(36+12c)/25), (c,-8/5),
((9c+48)/25,(36-12c)/25).
Their area is 2688/625 for either focus, giving the same chord product. This is NOT the outer-side product.

For unit inversion about F_+, translation of all inverse coordinates by -F_+ does not change area. On H the inverse vertices relative to F_+ are (1/(a-c),0),(X_I,Y_I),(X_I,-Y_I), with
X_I=-5(3a+5c)/(5a+3c)^2, Y_I=80/(5a+3c)^2.
Their area simplifies to D_+(H)=(7a-c)/576; D_-(H)=(7a+c)/576.
On V the relative inverse vertices simplify to
(-c/21,4/21), ((3c-19)/84,(c-3)/21),
((3c+19)/84,-(3+c)/21).
Their area is 1/18 at either focus. Consequently D_+D_-=1/324 in both phases, and B_e=(2016/5)D_(-e) for these exact finite inputs. This finite matching does not by itself prove a universal proportionality; the separate function-space/source interface below is needed.

## 7. Exact even negative controls and convention boundaries

For a=2,b=1,c=sqrt(3),lambda=4/5 the inner axes are alpha^2=16/5,beta^2=1/5.
D=((2,0),(0,1),(-2,0),(0,-1)) has chord x/2+y=1 and reflections at the axes; the caustic support-square is alpha^2/4+beta^2=1. Its outer side lines are x=+/-2,y=+/-1. Their ordered feet about F_+ are (2,0),(c,1),(-2,0),(c,-1), area 4. The other focus has the same area, product 16.

For C=((4t,t),(-4t,t),(-4t,-t),(4t,-t)), t=1/sqrt(5), each boundary equation is 5t^2=1. Its chords x=+/-4t,y=+/-t are precisely inner-ellipse tangent lines. At (4t,t) incoming unit (0,1), outgoing (-1,0) differ by (1,1), parallel to the ellipse normal (t,t); all vertices follow by symmetry. It is a genuine primitive four-orbit on the SAME caustic, not a mere arbitrary rectangle.

Its outer lines are +/-x+/-y=sqrt(5). The F_+ feet form a trapezoid of horizontal width sqrt(5) and vertical side lengths sqrt(5)-c and sqrt(5)+c. Signed shoelace area is their average times width, namely 5. F_- swaps those lengths and also gives 5, product 25. Thus even primitive constancy is genuinely false in this family. This does not assert that every even primitive family is nonconstant (the circular case is a separate constant example).

Repeating any ordered list s times multiplies every signed sum by s; reversing it negates each sum. At a circular boundary with a regular nonantipodal N-star, the focus is the center and its tangent feet are the original vertices; each area is N a^2 sin(2pi tau/N)/2, independent of rotation. This is a separate direct argument, not an extension of a complex torus at k=0. The original finite/noncollapsed outer-side convention and N>=3 remain relevant.

## 8. Independent partial secondary geometric reduction

This section precedes the native bridge body and foreign Landen source. It checks actual geometry rather than assuming Euclidean area is transported by a projective map.

Writing P=(x,y), the foot map is H(P)=(a^2(x+c)/(a^2+cx),a^2 y/(a^2+cx)). Its inverse is x=a^2(X-c)/(a^2-cX), y=b^2 Y/(a^2-cX). It maps the original caustic to
D X^2+(alpha^2 b^4/beta^2)Y^2-2a^2 c lambda X-a^4 beta^2=0,
D=a^2 b^2+c^2 lambda.
A line q.R=a^2 tangent to this image conic satisfies its dual conic equation. Direct adjugate calculation gives the circle
|R|^2+2c lambda R_x/beta^2-D/beta^2=0.
Hence its signed center is d_b=-c lambda/beta^2, its radius is R_b=alpha b^2/beta^2, and the contact circle radius is r_b=a, exactly as printed. The circles are genuinely strictly nested:
R_b^2-(|d_b|+a)^2=lambda(a-c)^2/beta^2>0.

For contact points Q_j on the circle radius r and intersections R_j of their adjacent tangents, let t_j=tan((theta_(j+1)-theta_j)/2). The signed area of the tangent polygon is r^2 sum t_j; the contact area is r^2 sum t_j/(1+t_j^2). The circumcircle equation gives
(R_b^2-d_b^2)-r^2(1+t_j^2)=-2 d_b.R_j.
Also t_j R_j/(1+t_j^2) is minus one half the 90-degree rotation of Q_(j+1)-Q_j. Its cyclic sum is zero. Multiplying and summing therefore gives
B_Q=(r^2/(R_b^2-d_b^2))*Area(R),
with a genuine geometric cancellation, not projective area preservation.

The real foot map is a degree-one orientation-preserving diffeomorphism onto its auxiliary circle. Direct differentiation gives its lifted angular derivative phi'(w)=b dn(w)/(a-c sn(w))>0; the projectivity and inverse have no real denominator zero on the two conics, so the circle is covered once. Admitted consecutive image points cannot be antipodal, since their chord is tangent to the image ellipse containing the origin. The continuous positive lifted angle increment cannot cross pi, and its phase average is 2pi tau/N<pi, so all increments are in (0,pi). Thus each t_j>0, the tangent/contact signed areas are nonzero in the chosen orientation, and the printed area ratio does not divide by zero even for stars.

The tangent-length extremes obey
t_M^2=(R_b+|d_b|)^2-r_b^2=lambda b^2(alpha+c)^2/beta^4,
t_m^2=(R_b-|d_b|)^2-r_b^2=lambda b^2(alpha-c)^2/beta^4.
Their ratio is (1-k)/(1+k), so the corresponding squared modulus is 4k/(1+k)^2, matching the stated m_b. Chord midpoint phase w+v=K gives the far dual-circle vertex and maximum tangent length, consistent with u=(1+k)(w+v-K)/2 vanishing there. The step transforms to 2K_b tau/N and the focus shift to K_b if K_b=(1+k)K.

The full tangent-length dn formula, ascending-Landen identity and arbitrary-order cyclic reduction still require actual source/body reading after this freeze. They are not assumed proved merely from these geometric checks.

## 9. Conditional inverse-transfer function-space mechanism

On a torus with periods L,4p, the space of meromorphic functions with antiperiod 2p and at most simple poles at p,3p has dimension at most one. Antiperiodicity makes the two residues opposite. Matching a residue of two such functions cancels both principal parts; the difference is holomorphic and constant, then its antiperiod forces zero. No quotient across zeros is needed.

The just-proved outer trace has this divisor. To apply the native proposed comparison, the cited inverse-area trace D_(-e) must have the same actual periods/poles/character after the exact phase alignment. Those are critical foreign proof interfaces, not a label equivalence. For real admitted trajectories, the focus lies inside the caustic, so each oriented chord has det(P_j-F,P_(j+1)-F)>0; dividing by the positive squared focal norms preserves that sign for each inverse determinant. Thus the real inverse area is nonzero. The outer contact area is likewise positive by the angle-increment argument above. If the actual source supplies the required inverse divisor facts, both nonzero functions are proportional by this argument, with a phase-independent scalar. Their mere generic projective relationship would not suffice.

## Source-first result and remaining interfaces

The complete main universal proof and all displayed finite fixtures have actual independent deductions here. No core analytic defect was identified. The standard canonical/Jacobi conventions, supplementary dn/Landen proof, actual inverse divisor alignment, exact source-label mappings and cited F62 rectangle error still require the finite post-INITIAL actual-source pass. No final full-original disposition is issued before that work. No repair programme, campaign, native scientific run or claimed numerical certification has occurred.
