# Source-first adversarial derivations — row 174

Derived after the complete actual native manuscript/PDF/pixels/metadata, before supporting code/results, archived reviews or new foreign mathematical bodies. Prior related geometry background is disclosed in INITIAL.md. These checks neither certify the unseen cited editions nor accept archival review dispositions.

## 1. Domain, geometry and units

Strict 0<lambda<b^2 and a>b>0 give alpha^2=a^2-lambda>c^2>0, beta>0, hence 0<k=c/alpha<1. In the source parametrization 0<v<K, so sn v, cn v and dn v are positive; D_0=1-k^2 sn^2(u)sn^2(v)≥1-k^2>0 for real u. Thus consecutive boundary tangents cannot become parallel or identical in this domain. The midpoint parameter offset is fixed and cannot affect phase constancy.

The outer locus is the polar reciprocal with semiaxes A=a^2/alpha and B=b^2/beta. Its focal parameter need not equal c; A can even cross B as the step changes. The products must use the ORIGINAL foci. At the exceptional period-four case the outer locus is a circle although the original ellipse is not; the theorem's circle exclusion refers to the original ellipse. Replacing the foci by those of the outer locus would test a different claim.

Scaling all lengths by s>0 scales lambda by s^2, leaves k and normalized shift unchanged, sends Q to sQ, H to s^4H and R to s^N R. The source's relation R_+^2R_-^2=F^(N/L) has units s^(4N) on each side, and R_+^2=F for even N has units s^(2N) on each side. There is no hidden squaring or signed-length convention.

## 2. Independent coefficient and positivity control

Directly from Cartesian Q=(-A sn u,B cn u), with S=sn^2 u, E=B^2+c^2 and D=A^2-B^2,

H=E^2+(2ED-4A^2c^2)S+D^2S^2.

For t=sn^2 v, q=1-t and the source U,V,W, this has coefficients alpha^4/q^4 times U^2, 2k^2UV-4k^2(1-k^2t)^2q^2, and k^4V^2. The identity U+V=2q(1-k^2t) changes the middle coefficient to -k^2(U^2+V^2), so the full polynomial factors exactly as (1-k^2S)(U^2-k^2V^2S). This checks every coefficient without selecting a parity or complex square root.

U=(1-k^2)+k^2(t-1)^2>0 and W=1-k^2t^2>0. For delta not K, the second root in S is S_1=dn^2(delta)/(k^2 cn^2(delta)). Since dn^2(delta)-cn^2(delta)=(1-k^2)sn^2(delta)>0, S_1>1/k^2>1. The first root S_0=1/k^2 is also outside real S∈[0,1]. Hence the factorization cannot introduce a real zero or a vanishing focal distance. This also checks that passing to squared paired distances loses no ordinary-positive-real constancy information.

## 3. A Cartesian four-period control independent of divisor arithmetic

The axial impacts (a,0),(0,b),(-a,0),(0,-b) form a billiard: at each axis point the two chord directions are reflected by its axis normal. Their common confocal caustic has lambda=a^2b^2/(a^2+b^2), alpha^2=a^4/(a^2+b^2), beta^2=b^4/(a^2+b^2); each chord line meets the caustic support equation exactly. This is strictly inside the stated domain. Boundary-tangent intersections are (±a,±b).

For F_+=(c,0), squared distances at X=±a are 2a(a∓c). The four-distance product is therefore 4a^2(a^2-c^2)=4a^2b^2, positive and with correct length-four units. Independently, at delta=K, k'=b^2/a^2, t=1/(1+k'), and the factorization's period-four constant gives C_v k'^3=4a^2b^2 using dn(u+K)=k'/dn u. This is an explicit control of the exceptional degree drop; it is not a universal constancy proof based on one phase.

## 4. Divisor and least-period collision attack

On the stated squared-function torus, sn^2 has degree two. Its branch value 1/k^2 corresponds to the double dn^2 zero p+K. For delta not K, the second factor has distinct zeros p+K±delta: coincidence requires 2delta∈2K Z, and 0<delta<2K then forces delta=K. Neither zero coincides with p or p+K otherwise. Thus the generic fourth-order pole cannot silently cancel. At delta=K those two zeros collide with p and remove two pole orders; keeping the generic degree-four divisor at N=4 would be wrong. The source treats that separately.

The physical P parameter has real period 4K, while H has real period 2K. With delta=4K tau/N and gcd(tau,N)=1, the shift's order on the latter circle is L=N/gcd(N,2). The half-period K lies in that subgroup exactly when L is even, equivalently 4 divides N. The cosets p+G and p+K+G are otherwise disjoint, so no partial or accidental cancellation is hidden by choosing another coprime generator. Translation signs in the divisor sum do not matter because G=-G.

Hand controls: N=3 gives L=3 and no K; N=4 gives L=2 with K and the reduced-order divisor; N=6 gives L=3 without K despite antipodal pairing in the PHYSICAL six-orbit; N=8 gives L=4 with K; star N=12,tau=5 still generates the same order-six subgroup and contains K. These are controls, not a finite enumeration promoted to all N. The all-N argument is the exact cyclic-group order calculation.

For odd N, the antipodal shift is a different phase, not another vertex of the same primitive orbit. However R_-(u)=R_+(u+2K) still holds as a function identity. If either is constant, both are constant, making the paired meromorphic power constant on a real interval. The identity theorem contradicts the nonzero divisor. Thus necessity does not assume an unavailable antipodal pairing. For even N, actual antipodal pairing makes R_+=R_- pointwise even when N is 2 modulo 4; equality of the two products alone is not phase constancy. For 4|N, F constant plus the positive real square root proves constancy without a complex branch choice.

## 5. Exact six-period physical fixture: tangency and reflection

For a=3,b=1,lambda=9/16, the caustic has alpha^2=135/16,beta^2=7/16,c^2=8. For the first displayed orbit, the oblique chord line is sqrt(7)x+3y=3sqrt(7); its support value on the caustic is squared 7(135/16)+9(7/16)=63, exactly the squared constant. The middle horizontal chord y=sqrt(7)/4 is tangent at the caustic's minor extremity. The other chords follow by reflections and central symmetry. All impacts lie on E.

At (9/4,sqrt(7)/4), incoming and outgoing unit velocities are (-3/4,sqrt(7)/4) and (-1,0). Their difference is (1/4,sqrt(7)/4), exactly the ellipse normal (x/9,y). Its squared norm is 1/2 and its dot with the incoming velocity is 1/4, giving the reflection formula's coefficient one. At (3,0) the incoming/outgoing x components are opposite and the y components equal. These check the reflection law at the orbit's inequivalent vertices, with symmetry covering all six.

For the second orbit, the vertical chord is x=-3sqrt(15)/4, the caustic's major tangent. The other chord line is x-sqrt(15)y=-sqrt(15), with support square 135/16+15(7/16)=15. At (-3sqrt(15)/4,1/4), incoming/outgoing unit velocities are (-sqrt(15)/4,-1/4) and (0,-1). Their difference is three times the ellipse normal (-sqrt(15)/12,1/4). The normal has squared norm 1/6 and incoming dot normal 1/4, again giving reflection coefficient three. At (0,1), vertical components change sign and horizontal components agree. Thus these are actual billiard orbits on the same caustic, not just inscribed/tangent polygons. Their six impacts are distinct and their listed cyclic orders are primitive.

## 6. Exact outer product and repetition control

Solving ordinary Cartesian boundary tangent lines gives exactly the six outer vertices listed in the source. For a pair ±Q, the product of its two positive distances to F_+ is sqrt(H_Q), with H_Q=(X^2+Y^2+c^2)^2-4c^2X^2.

First orbit: for Q_0=(3,1/sqrt(7)), H_0=288/49. For Q_1=(0,4/sqrt(7)), sqrt(H_1)=72/7; Q_2 has the same H as Q_0. Hence R_+=H_0 sqrt(H_1)=20736/343.

Second orbit: for Q_0=(-9/sqrt(15),1), H_0=864/25. For Q_1=(-12/sqrt(15),0), sqrt(H_1)=8/5; Q_2 again gives H_0. Hence R_+=6912/125. Their difference is 221184/42875>0. No floating computation or stored certificate is used. Both focal products agree within each even orbit by antipodal pairing, yet they differ across these two phases, as required for N=6.

Repeating either orbit twice raises its positive product to its square. The unequal products remain unequal at nominal length twelve. More generally x↦x^r is injective for positive x and integer r≥1, so repetition cannot restore constancy. This rejects the incorrect nominal-list-length reading without weakening the original least-period theorem.

## 7. Limiting cases and remaining primary interfaces

For c=0 the original foci coincide and regular-star outer radius is a/cos(pi tau/N), so all admitted periods have constant products. Noncircularity is necessary. The limit k→0 degenerates the complex torus, so the nonzero-divisor proof is not uniform in that limit and should not be used to assert a phase-variation lower bound independent of eccentricity. As lambda→0, v→0 and the finite-period closure degenerates; as lambda→b^2, k→1 and the proper ellipse/torus degenerates. Hyperbolic/collapsed caustics and N=2 remain excluded. No theorem is inferred by an endpoint limit.

New actual-primary checks still needed after sealing: canonical billiard/closure conventions, Jacobi complex period/shift and zero multiplicities, literal k115 editions and Ferudun's overlapping positive assertion. Those interfaces and dated provenance are not certified by the hand controls or by reading the candidate's attribution paragraphs. The source's mathematical claim remains the full target; no narrower substitute or repair is proposed.
