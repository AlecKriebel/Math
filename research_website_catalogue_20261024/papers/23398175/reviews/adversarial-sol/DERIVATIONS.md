# Own source-first adversarial derivations — 23398175

These are this worker's derivations before current peer/root findings, archived support opinions/results or new foreign mathematical bodies. Prior related geometry exposure is disclosed in INITIAL. The manuscript itself contains historical/support assertions; reading that required source is not independent confirmation of those assertions. All mathematical formulas below use ordinary real Euclidean geometry unless explicitly continued bilinearly to the complex torus.

## 1. The actual object from Cartesian projection

Let A=a², B=b², c²=A−B>0 and P=(x,y) with x²/A+y²/B=1. The original tangent is n·X=1, n=(x/A,y/B). For e=±1, f_e=(ec,0), solving the perpendicular-foot equations gives

Q_e=f_e+(1−n·f_e)n/(n·n)
   =( A(x+ec)/(A+ecx), A y/(A+ecx) ).

The denominator is at least A−ca=a(a−c)>0. Squaring and using the ellipse equation gives |Q_e|²=A. No signed radial length or inverse vertex appears. For successive distinct nonantipodal original vertices P,P', actual outer-tangent intersection is

V=( A(y'−y)/det(P,P'), B(x−x')/det(P,P') ).

Thus the side V_(j−1)V_j is the original tangent at P_j. The independent exact controls solve these two tangent equations, reconstruct the actual outer side, and project from f_e onto that side; they do not insert the source's Jacobi focal-foot formula. Their equality to direct tangent-normal projection is an object-identification check.

The signed edge contribution has the useful purely Cartesian expression

det(Q_e(P),Q_e(P')) = A²[det(P,P')+ec(y'−y)] / [(A+ecx)(A+ecx')].

It keeps trajectory order. Sorting by geometric angle, replacing area by perimeter, using original chord feet, or treating Q as a unit inversion would change the object.

## 2. Canonical-coordinate and reflection interface derived independently

The source's standard Jacobi addition identities imply that the line through P(t−v),P(t+v), where P(w)=(-a sn w,b cn w), is the tangent to the caustic at (-alpha sn t,beta cn t):

(-sn t/alpha)x+(cn t/beta)y=1.

Indeed set s=sn t,C=cn t,D=dn t and s_v=sn v,c_v=cn v,d_v=dn v. Substitution of the addition formulas into the line equation cancels the opposite mixed terms and leaves [s² d_v²+C²]/[1−k²s²s_v²]=1. This verifies the actual chord rather than presuming uniform eccentric anomaly. The chord difference is a positive multiple of (-alpha cn t,-beta sn t), so it has the consistently oriented caustic tangent direction.

For any chord direction d from a point P on the outer ellipse, tangency to the confocal caustic is equivalent to

lambda |d|² = A B (n·d)², n=(x/A,y/B).

To derive it, use the normal (-d_y,d_x), the inner-ellipse support equation and (P×d)²−A d_y²−B d_x²=−AB(n·d)². The two tangent directions consequently have equal normal component in magnitude. Incoming and outgoing choices have opposite normal signs; the other-tangent continuation is exactly the Euclidean reflection d_out=d_in−2(n·d_in)n/(n·n) for unit d. This supplies a Cartesian check of the billiard interface for stars as well as convex orbits.

For a fixed strict confocal pair, beta/b∈(0,1) determines v∈(0,K) by cn v=beta/b. The displayed a=alpha dn v/cn v follows from confocality: a²−b²=c². Also lambda=beta² sn²v/cn²v, hence 0<lambda<b². P(w) is injective modulo4K on the real phase circle. Closure of least period N gives N delta=4K tau, gcd(tau,N)=1, delta=2v∈(0,2K). Thus 0<tau<N/2 and both directions are covered by reversal. Arbitrary N/tau are not asserted to occur for an independently prescribed pair. This is a construction/domain argument, not a numerical Poncelet extrapolation.

## 3. Main pole argument checked at its fragile points

The full Q vector has periods4K,4p with p=iK'; sn has periods4K,2p, while cn changes sign under2p. Common poles of sn/cn cancel in Q because the leading denominator is nonzero. The only remaining denominator zeros are r±v (r=K+p), and their2p translates. The source's quarter-period formulas differentiate consistently: the derivative of dn z/(k cn z) is k'² sn z/(k cn²z), exactly the product of the stated transformed cn and dn. At z=±v the numerator vectors both equal (−ab²/c,−i ab²/c), while denominator derivatives have opposite nonzero signs. Their residues are opposite collinear vectors; no Hermitian conjugation is permissible.

At each singular trace phase exactly two vertices are singular and adjacent modulo N. Coprimality prevents further coincident real translates; the other imaginary row cannot coincide by a real phase shift. The shared-edge double determinant coefficient is det(R,−R)=0. Other incident edges have at most one singular endpoint; for N=3 their common regular endpoint creates no extra product. The closing edge uses the true vector period N delta=4K tau. Therefore every pole is at most simple, including stars and the cyclic cut.

The trace has periods delta and4K; integer Bezout combinations yield L=4K/N. On the compact torus C/(LZ+4pZ) its only possible poles are b0+p,b0+3p, b0=K−v. Treating2p as a Q period would be a genuine error, but the source explicitly does not do this.

## 4. Reflection signs, zeros and oddness

Q(w+2p)=JQ(w), det J=−1, so T(w+2p)=−T(w). For Q(2K−w)=JQ(w), reflection and reversal of cyclic edge order give two minus signs, so T(2K−w)=T(w). Since delta=2v is a trace period, F(z)=T(K−v+z) is even: reflection maps it to T(K+v+z)=F(z) after one delta shift.

At z=p+L/2, evenness and the real period identify F(-p+L/2) with F(p+L/2), but the2p antiperiod negates it. That point is regular and distinct from p,3p, so its value is zero. The3p+L/2 point follows by translation. The possible poles of either factor in F(z)F(z+L/2) are canceled by zeros of the other. Orders at most one are essential here. This product is holomorphic on a compact torus and hence constant. The pole-free case is safe: an entire elliptic F is constant and the antiperiod forces0. No division by an area, residue or coefficient is required.

The actual focus relation is Q_-(w)=−Q_+(w+2K); central negation preserves shoelace sign, so B_-=T(w+2K), with no extra area minus sign. Odd N makes2K≡L/2 mod L; even primitive N makes it0. The former gives the original claimed product, the latter only equal areas. This is an all-admitted-period proof conditional on the standard Jacobi identities/period and degree facts, whose actual primary interfaces still need post-freeze checking.

## 5. Independent exact odd orbit and transformations

Deriving an isosceles3-period directly, write P0=(a,0), P1=(ax,b sqrt(1−x²)), P2=(ax,−b sqrt(1−x²)). Equality of the vertical-edge caustic parameter and the other two chord parameters yields

c²x²−2b²x−a²=0.

A new convenient choice a²=8,b²=3 gives x=−4/5 and lambda=72/25. It yields H=((sqrt8,0),(−4sqrt8/5,3sqrt3/5),(−4sqrt8/5,−3sqrt3/5)). A second same-caustic phase is V=((0,sqrt3),(−8sqrt3/5,−sqrt3/5),(8sqrt3/5,−sqrt3/5)). Exact boundary, confocal support, unit reflection, finite tangent intersections, actual-side projection, auxiliary-circle and perpendicularity checks give

B_±(H)=(12sqrt6±3sqrt15)/5, B_±(V)=27/5,
B_+B_-=729/25.

These are not the manuscript's21/16 example coordinates. Individual focal areas vary, while the product agrees. Reversal changes both signs. Repeating H twice has total list length6 but odd least period3; both areas double and product becomes2916/25. It is admitted by the repetition corollary and is not an even-primitive counterexample. A similarity with scale7/3, rotation90degrees and translation(3,−4), recomputed by actual line projections, gives B_±(V_transformed)=147/5 and product21609/25. Areas have length² units and their product length⁴, as required. These are finite exact controls, not the universal theorem.

## 6. A full even-primitive negative family

For every a>b>0, compare the diamond (a,0),(0,b),(−a,0),(0,−b) and the rectangle (±a²/d,±b²/d) in cyclic order, d=sqrt(a²+b²). Both are genuine primitive4 billiards, tangent to the same lambda=a²b²/(a²+b²). Reflection is immediate from axis symmetry for the diamond and45degree normals for the rectangle. Their chord support equations give the same strict elliptic caustic.

The diamond's two outer focal-pedal areas both equal2ab. For the rectangle, actual tangent lines are ±x±y=d. Projecting f_e onto those four lines gives vertices ((ec+d)/2,(d−ec)/2),((ec−d)/2,(d+ec)/2),((ec−d)/2,−(d+ec)/2),((ec+d)/2,−(d−ec)/2). Their shoelace area is d²=a²+b² for either focus. Product gap=(a²+b²)²−4a²b²=(a²−b²)²>0. The7-case exact script confirms this at8/3:96 versus121. Thus dropping odd least period is falsified without relying on the source's4/1 fixture. It tests hypothesis necessity, not a defect inside the original domain.

## 7. Additional Cartesian scrutiny of the advertised bicentric route

The inverse of the focal-foot projectivity is x=a²(X−c)/(a²−cX), y=b²Y/(a²−cX). Substituting the caustic equation and multiplying by alpha²/beta² gives the dual-circle conic

(R_b²−d_b²)X²+R_b²Y²+2a²d_b X−a⁴=0,
d_b=−c lambda/beta², R_b=alpha b²/beta².

A polar line Q·R=a² is tangent to the circle(center d_b,radius R_b) precisely when Q lies on this conic. The circle truly contains the radius-a auxiliary circle: R_b−|d_b|−a=(a−alpha)(alpha−c)(a−c)/beta²>0. The projectivity has positive denominator on the closed outer ellipse and maps its interior to the auxiliary disc; the original foci lie inside the caustic, so the image caustic contains0. Thus no real caustic tangent through0 gives an infinite polar vertex. This checks the geometric correspondence rather than assuming a projective map preserves Euclidean area.

For bicentric vertices r_j and contact angles whose consecutive half-angle tangents are t_j, closure gives sum t_j r_j/|r_j|²=0. The circumcircle equation |r_j|²=D+2d_b x_j, D=R_b²−d_b², therefore gives sum t_j=D sum t_j/|r_j|². Direct signed shoelace identities are Area(R)=a² sum t_j and Area(Q)=a⁴ sum t_j/|r_j|². Hence D Area(Q)=a² Area(R). For consistently oriented real Poncelet stars, local contact increments are chosen by the other-tangent continuation; this is not arbitrary angular resorting. The cross-multiplied identity avoids division through an area.

The polar vertex at midphase t=w+v is

r(t)=((alpha c−a² sn t)/(alpha−c sn t), alpha b² cn t/[beta(alpha−c sn t)]).

Algebra gives |r(t)|²−a²=(lambda b²/beta²)*(1+k sn t)/(1−k sn t), and t_M=b sqrt(lambda)/(alpha−c). With A0=(1−k)/(1+k), its positive tangent length divided by t_M is f(t)=sqrt[A0(1+k sn t)/(1−k sn t)]. This obeys f'²=((1+k)²/4)(1−f²)(f²−A0²), f(K)=1,f'(K)=0, f''(K)=−k. The standard analytic dn solution is consequently dn((1+k)(t−K)/2, m_b), with parameter m_b=4k/(1+k)². This checks the source's coefficient, modulus/parameter distinction, phase increment and focus shift. Actual classical primary identities and the source's stated inverse-area transfer still require selective post-freeze reading; no priority conclusion is inferred.

## 8. Numerical attacks and limits

One unchanged own script in a suitable local runtime performed three selected physical-reflection families, each at three eccentric-anomaly starts0,.37,1.11. No Jacobi function was used. A Cartesian tangent contact launches the ray, the quadratic outer-ellipse intersection advances it, and Euclidean unit-normal reflection continues it. Caustic lambda is found by260 bisections of the physical winding closure condition, then actual outer-side intersections/perpendicular feet produce the areas.

The selected primitive5/2 star at a=2,b=1, near-circle5/2 star at a=1.0001,b=1 and thin-caustic7/3 star at a=5,b=1 have respectively positive beta² about9.15e−5,.0954,4.43e−12. Their retained geometry residuals are below1.8e−69 and product spreads below2e−73 at90decimal digits. These are non-interval numerical diagnostics only; neither closure existence nor constancy for all phases/periods is proved by these samples. The analytic argument carries that quantifier. No fixed-N limiting statement at a collapsed/grazing caustic is silently assumed.

The circle boundary has a separate exact explanation: Q=P for the coincident center focus, so each regular star has area(Na²/2)sin(2pi tau/N) and its squared product is rotation invariant. At c=0 or beta=0 the nondegenerate torus argument cannot simply be substituted; the source separately treats the circle and excludes collapsed/grazing cases. Similarity scale must be positive and nonzero. No uniform near-boundary stability bound is claimed.

## 9. Status at this source-only checkpoint

No counterexample or critical core-proof gap was found inside the full original domain in these source-first checks. This is provisional: actual primary canonical/Jacobi interfaces, the close inverse/outer-pedal antecedents and selected source/native material have not yet been read in this effort. The advertised secondary transfer/priority assertions are not established by source wording alone. No blanket firstness/open-status claim or follow-up proposal is made. Preserve all finite evidence, runtime failure and numerical limitations; do not repair or narrow the original claim.
