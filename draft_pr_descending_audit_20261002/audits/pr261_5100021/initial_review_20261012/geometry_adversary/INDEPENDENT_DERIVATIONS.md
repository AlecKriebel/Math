# Independent direct geometry (before proof exposure)

Timestamp begun: 2026-10-12 09:35:25 UTC. Audit completion estimate: 18%.

No submitted proof/checker/review has been read at this checkpoint.

## 1. Both constructions by linear algebra

Translate the chosen original focus to 0. For consecutive original vertices P,Q, put d=Q-P and k=det(P,Q). Let R(x,y)=(y,-x). The original side has equation R(d) dot X=k, so its foot from 0 is

    H = k R(d) / |d|².

The antipedal lines are P dot X=|P|² and Q dot X=|Q|². Cramer's rule gives

    Vx=(|P|² Qy-|Q|² Py)/k,
    Vy=(Px |Q|²-Qx |P|²)/k.

Equivalently V/2 is the circumcenter of the triangle (0,P,Q). These derivations use the ORIGINAL focus and ORIGINAL vertices/side lines, so there is no implicit change of pole.

## 2. Finiteness is geometric

For the outer centered ellipse x²/a²+y²/b²=1, write c²=a²-b². The caustic x²/(a²-lambda)+y²/(b²-lambda)=1, with 0<lambda<b², has the same foci (±c,0). Both lie strictly inside the caustic, since c²/(a²-lambda)<1. A line through an interior point cannot be tangent to a nondegenerate convex ellipse. Therefore no billiard side passes through either original focus: k never vanishes. A tangent from an outer boundary point meets the outer ellipse in two distinct points, so |d|² never vanishes either. Thus all antipedal consecutive intersections and pedal feet are finite throughout every admitted orbit. This does not use periodicity or a special-function denominator.

## 3. An additional conic fact: every pedal vertex lies on a fixed circle

For focus F=(c,0), write a caustic tangent as n dot X=h in CENTERED coordinates, |n|=1. The support equation is h²=(a²-lambda)nx²+(b²-lambda)ny²=(b²-lambda)+c²nx². The pedal foot is H=F+(h-n dot F)n. Set t=h-c nx. Then

    |H|²=c²+2c nx t+t²
          =c²+[h²-c² nx²]
          =a²-lambda.

Thus all original-side feet from either focus lie on the circle about the ORIGINAL ellipse center with radius sqrt(a²-lambda). This exact direct fact provides a useful independent numerical invariant. It does not itself prove constancy of pedal signed area, nor of the requested product.

## 4. Exact period-4 caustic and axial orbit

The axial diamond (a,0),(0,b),(-a,0),(0,-b) is a billiard orbit by axis reflection. A side x/a+y/b=1 is tangent to the confocal caustic precisely when

    (a²-lambda)/a²+(b²-lambda)/b²=1,
    lambda_4=a²b²/(a²+b²).

This lies in (0,b²). Put L=a²+b², c²=a²-b², d-=a-c, d+=a+c. For focus-relative coordinates, the ordered pedal vertices are

    ( b² d-/L,  ab d-/L),
    (-b² d+/L,  ab d+/L),
    (-b² d+/L, -ab d+/L),
    ( b² d-/L, -ab d-/L).

Their signed area is 4a³b³/L². The ordered antipedal vertices are

    ( d-,  b+ac/b),
    (-d+,  b-ac/b),
    (-d+, -b+ac/b),
    ( d-, -b-ac/b).

Their signed area is 4ab, including the regime b²<ac where the resulting polygon self-intersects. The axial signed-area product is therefore

    16a⁴b⁴/(a²+b²)².

For a=5,b=3,c=4 this gives pedal area 3375/289, antipedal area 60, product 202500/289. This exact calculation is not yet a general phase proof.

## 5. All four-period phases by direct trigonometric tangency

Write consecutive outer vertices as P(t)=(a cos t,b sin t), P(s)=(a cos s,b sin s). Their chord is

    (x/a) cos((t+s)/2)+(y/b) sin((t+s)/2)=cos((s-t)/2).

Substitution of lambda_4 into the support tangency equation simplifies to

    b² cos t cos s+a² sin t sin s=0.

For the positive branch, one may take

    cos s=-a² sin t/H,
    sin s= b² cos t/H,
    H=sqrt(a⁴ sin²t+b⁴ cos²t).

The next positive tangent then reaches -P(t), followed by -P(s), and the fourth returns P(t). This can be checked by the same bilinear equation and ordering; it is a direct construction of the full four-period family. Numeric area products at generic t will check whether the axial constant persists.

## 6. Direct conic orbit generator to be used independently

For P on the outer ellipse set Ac=sqrt(a²-lambda), Bc=sqrt(b²-lambda), W=(Px/Ac,Py/Bc), S=|W|²>1. Inner tangent contacts are

    T±=(Ac,Bc) * [W ± sqrt(S-1)(-Wy,Wx)]/S

(componentwise multiplication). For d=T-P, the second intersection with the outer ellipse is

    Q=P-2[(Px dx/a²+Py dy/b²)/(dx²/a²+dy²/b²)]d.

Choose the unique branch det(P,Q)>0; the center lies inside the caustic, so the forward angular increment lies strictly between 0 and pi. Check reflection independently by reflecting incoming unit direction in the outer normal (Px/a²,Py/b²). Find a desired primitive N,m caustic by solving total angular advance over N steps=2pi m, with gcd(N,m)=1 and 0<m<N/2. No Jacobi parametrization is used for orbit generation.
