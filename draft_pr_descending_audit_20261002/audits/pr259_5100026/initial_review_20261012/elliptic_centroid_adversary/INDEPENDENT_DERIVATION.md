# Independent elliptic-trace derivation (pre-submission-read)

UTC 2026-10-12T11:47:30.682515+00:00; best-guess completion 70% for independent math audit (not a novelty assessment). No submitted proof, submitted controls, historical review, or other new-family conclusion has been read.

## Claim and domain

Let the original ellipse be x²/a²+y²/b²=1, a>b>0, caustic axes sqrt(a²-lambda),sqrt(b²-lambda), 0<lambda<b². Original focus M=(f,0), f=sqrt(a²-b²). Define R_i as the intersections of original tangents at consecutive billiard vertices. Define U_i by (R_i-M)·U_i=|R_i|²-M·R_i and the analogous equation for R_{i+1}. Centroid is the arithmetic mean of N U_i, not an area centroid. Let N be the least period, even, and winding p with gcd(p,N)=1, 1≤p<N/2. All occurrences of p are integer winding; below S² uses a different symbol z when necessary.

The independently established conclusion is phase invariance, zero y component, and all real intersections finite. The additional claimed opposite-sign/inside-foci statement is false for permitted primitive stars: an exact 8/3 example is given below. No conclusion about novelty is drawn.

## Uniformization and independent geometry

Use Jacobi modulus k, q=sqrt(1-k²), K=K(k), K'=K(q), and choose v∈(0,K) with S=sn(v), C=cn(v), D=dn(v). Scale b to 1 temporarily. Parameters are

    a=D/q, f=k C/q, lambda=S²,
    P(u)=(a sn u, cn u), delta=2v=4K p/N.

This is the classical billiard translation input; the exact caustic and tangent construction are checked here. With s=sn u,c=cn u,d=dn u,Q=1-k²s²S², addition gives

    sn(u±v)=(s C D ± S c d)/Q,
    cn(u±v)=(c C ∓ s S d D)/Q.

The chord of P(u−v),P(u+v) has equation

    (s D/C) x/a + (c/C) y =1.

Its caustic support-square is (a²-lambda)s²D²/(a²C²)+(1-lambda)c²/C²=1: indeed 1-lambda=C² and (a²-lambda)D²/a²=C² using a²=D²/q². Thus the chosen confocal caustic is correct. Reflection-law correspondence/constant translation is credited to the canonical billiard uniformization, not rebranded as new.

Solving original tangent equations yields the independently derived outer-vertex locus

    R(u)=(A sn u,B cn u), A=a D/C=D²/(qC), B=1/C.

In particular, A²−B² is generally not f², and A can be smaller than B. Keeping M as an original focus is essential.

## Real normal determinant

For U(t) from R(t−v),R(t+v), set

    X=A s C D/Q, Z=A S c d/Q,
    Y=B c C/Q, W=−B s S d D/Q.

Thus the endpoint vertices are (X−Z,Y−W),(X+Z,Y+W). Their normal equations reduce to

    (X−f) Ux+Y Uy=H=X²+Z²+Y²+W²−fX,
    Z Ux+W Uy=J=2XZ+2YW−fZ.

The determinant in these reduced equations is

    Delta=(X−f)W−YZ = (B S d D/Q)(f s−a).

This follows from c²+s²D²=Q. For real t, Q≥D²>0,d≥q>0. Further a−f|s|≥a−f>0, since D²−k²C²=q²>0. Hence Delta never vanishes; the actual two-normal determinant is 2Delta. Original tangents likewise have determinant proportional S C d/Q with every factor nonzero. All real R,U are finite, including stars.

## Why no dn(t) denominator is needed

In the displayed system Z,W,J each has a factor d; dividing the second equation by it removes d. H contains d² only. Substitute c²+s²=1,d²=1-k²s². The resulting Ux,Uy are rational in s,c, with no d. In particular, the apparent dn-zero determinant at t=K+iK' is removable unless another independent denominator vanishes there, which it does not in 0<v<K.

## Complete complex pole classification and trace

Work on the common torus Lambda=4K Z+4iK' Z. The standard shifts imply

    sn(t+2iK')=sn t, cn(t+2iK')=−cn t,
    sn(2K−t)=sn t, cn(2K−t)=−cn t,
    dn(2K+2iK'−t)=−dn t.

Therefore the involution I(t)=2K+2iK'−t preserves s,c and swaps the two R endpoints. Directly U(I(t))=U(t).

Potential nonremovable poles come only from:

1. Endpoints R(t±v) at base poles w∈{iK',2K+iK',3iK',2K+3iK'}: t=w±v.
2. The focal factor f sn t−a=0, equivalently sn t=D/(kC): t=K±v+iK', and their 2iK' shifts, modulo Lambda.

No class is omitted:

* R(t±v) has no simultaneous pole because 0<2v<2K.
* A pole of sn/cn at t itself (t=w) leaves both R endpoints finite. The limiting normal determinant is nonzero for f>0, as Delta tends a nonzero imaginary constant. Thus these points are regular.
* dn zeros t=K+iK',3K+iK' and 2iK' translates make endpoint differences vanish, but the d factor divides out. Q=C²≠0 and f sn−a=(±C−D)/q≠0 there, so regular.
* The Q roots, sn²t=1/(k²S²), are exactly the endpoint class via sn(u+iK')=1/(k sn u).
* Focal roots are exactly the two sn preimages noted above since sn(K±v)=C/D; their derivatives are nonzero. At K±v+iK', cn=−i q/(kC), dn=±i qS/C, so sn' = ±q²S/(kC²).
* Endpoint and focal locations coincide only when 2v=K, i.e. v=K/2. To see this, their real parts are ±v,2K±v versus K±v; equality requires 2v=K in (0,2K).

For v≠K/2 all listed poles are at most simple. For a focal pole this follows from the simple focal factor. At an endpoint pole, one R is r/z+O(1), r=(A/k,−iB/k), while the other is a finite w. The coefficient determinant det(r,w−M) is nonzero except v=K/2. Writing w=(A/(k sn 2v),−iB dn 2v/(k sn 2v)), it is proportional a kS−f (or its nonvanishing sum counterpart); equality a kS=f is equivalent S²D²=C², whose unique solution is v=K/2. The normal equation's RHS has at most order 2 while its matrix determinant has order 1, so U has at most order 1.

Every simple pole p pairs with I(p). Involution invariance makes their residues opposite. For endpoint p=iK'±v, I(p)=2K+iK'∓v, and the difference is 2K∓delta. For a focal p=K+iK'±v, I(p)=K+iK'∓v, difference ∓delta. The same is true in the other imaginary band.

Primitive even N forces winding p odd. Thus (N/2)delta=2K p≡2K modulo 4K, and I(p) lies in the same delta orbit as p. Consequently every polar contribution cancels in

    T(t)=sum_{j=0}^{N−1} U(t+j delta).

T is a holomorphic elliptic function, hence constant. The reflection t↦2K−t preserves Ux and negates Uy (it reflects the outer vertices across the x axis and fixes M). Hence the constant Ty=0. This proof handles all coprime primitive stars; reversing winding merely reverses endpoint order.

Potential cancellation overlap at N=4 is handled directly below. There is no other primitive even period with v=K/2: delta=K forces least period 4, including orientation reversal.

## Antipodal x identity and direct four-period control

Let U_f be computed with M=(f,0). Since R(t+2K)=−R(t), U_f(t+2K)=−U_{−f}(t). Cramer's rule gives

    Ux(t)+Ux(t+2K)
      =2f (W²−Y²)(Z²+W²)/(Delta_0²−f²W²), Delta_0=XW−YZ.

Use A²c²+B²s²D²=(D²/C²)(a²−f²s²), and factor

    S²D²s²(1−k²s²)−C²(1−s²)
       =(1−k²S²s²)(D²s²−C²).

The exact identity simplifies to

    Ux(t)+Ux(t+2K)=2f (D²sn²t−C²)/(C²[1−k²S²sn²t]).                 (* )

At v=K/2, S²=1/(1+q),C²=q/(1+q),D²=q and A=B. The function in (*) is negated by t↦t+K because sn²(t+K)=(1−sn²t)/(1−k²sn²t). Thus sum Ux over four phases is zero.

For full vector zero, independently check four circle vertices r0=(s,c),r1=(c/d,−q s/d),−r0,−r1 after scaling outer circle radius to 1. Focus square is F²=(1−q)/(1+q). For any unit-circle opposite pair of edge bisector vectors V=r0+r1,W=r1−r0, the sum over four antipedal vertices is

    2F(1−F²)[ Vx V/((1+r0·r1)²−F²Vx²)
             +Wx W/((1−r0·r1)²−F²Wx²)] −4(F,0).

Substitution c²=1−s²,d²=1−(1−q²)s²,F²=(1−q)/(1+q) reduces both numerator coordinates identically to zero. The exact-control script preserves this polynomial calculation. Since all real denominators were already shown nonzero, this proves N=4 centroid=(0,0), without relying on unresolved double-pole cancellation.

## Exact primitive 8/3 counterexample to sign and focal-segment claims

Take b=1,k=3/5,q=4/5,v=3K/4,N=8,winding=3. gcd(8,3)=1, so least period is 8. Set

    z=S²=(25−10sqrt(5))/3,
    a²=(−25+15sqrt(5))/8,
    f²=(−33+15sqrt(5))/8,
    lambda=z.

These satisfy a²>1,0<lambda<1, and k²=(a²−1)/(a²−lambda)=9/25. Jacobi duplication gives sn²(K/2)=5/9 and the polynomial

    (9z²−150z+125)(9z²−30z+5)=0.

The stated root is the unique relevant sn²(3K/4) branch, z>sn²(K/2); complementary quarter-shift gives the same branch. For phase t=0, the four antipodal pair arguments 0,3K/2,3K,9K/2 have sn² values 0,5/9,1,5/9. Identity (*) yields exactly

    centroid_x/f = (11+5sqrt(5))/8 >1,
    centroid_y=0.

Thus centroid is positive for positive original focus and lies beyond that focus. This is an exact admissible strict-caustic primitive star, not a numerical counterexample and not a repeated odd orbit. The table's bare phase-invariance claim remains compatible; the stronger geometric-location assertion is not.

## Boundary controls and exact remaining gaps

* lambda=0 and lambda=b² are excluded. Corresponding v=0,K invalidate S or C and are not silently included.
* Circular a=b gives f=0,k=0 and must use the k→0 geometry; no division by k from the strict derivation is valid there. Direct circle analysis has centroid at origin for even nondegenerate regular/star outer polygons with finite normals.
* Repeating an odd primitive orbit into an even list does not supply the 2K phase shift and invalidates the trace-pairing argument. Source qualification and an exact/numeric control remain to be checked after freeze.
* Classical billiard uniformization is the only imported structural input; source/page details and Jacobi identities require primary-source confirmation. All antipedal geometry and cancellation are independently derived here.
* Exact primitive-even phase invariance is proved subject to that standard uniformization input. No unsupported all-period identity is invoked. Exact adverse sign/segment result is proved by the paired identity.
