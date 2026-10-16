# Independent geometry and local algebra reconstruction

Frozen first reconstruction: 2026-10-15 10:21:22 UTC. This was written after reading the complete submitted PROOF.md and source_record.json and the relevant primary Stachel pages, but before reading any inherited reviewer report, submitted checker, or inherited checker output. Equations numbered below refer to the submitted proof. No result from PR200, PR206, or PR207 is used.

## Exact scope and conventions

The local claim is that (3)--(15) follow from actual consecutive outer tangent intersections, followed by Euclidean unit inversion about an original billiard focus and signed straight-edge shoelace area, for every real modulus 0<k<1 and 0<v<K(k). For a closed family, v=2K tau/N, gcd(tau,N)=1, 0<tau<N/2. This includes primitive stars. It does not include k=1, v=K, a hyperbolic caustic, or repetition as a means of changing primitive parity. The global meromorphic argument is outside this shard's certification.

Write m=k^2, g=1-m=k'^2, s=sn(u;k), y=cn(u;k), z=dn(u;k), h=sn(v;k), C=cn(v;k), d=dn(v;k), t=h^2, q=C^2=1-t, and D=1-m t s^2. Then y^2=1-s^2, z^2=1-m s^2, d^2=1-mt. All h,C,d,k',q,D are strictly positive on the stated real domain; D>=1-mt>0. Here m is the numerical *parameter* expected by mpmath; Stachel's letter m instead denotes the *modulus*, and equals this note's k.

The addition formulas, with their signs retained, are

    s_+ = (s C d + h y z)/D,   s_- = (s C d - h y z)/D,
    y_+ = (y C - s h z d)/D,   y_- = (y C + s h z d)/D.

They imply the following three useful identities without squaring away a sign:

    s_+ + s_- = 2sCd/D,
    s_+ s_- = (s^2-t)/D,
    s_+ y_- - s_- y_+ = 2hCz/D.

For example, the numerator in the last identity is 2hCz(s^2 d^2+y^2)=2hCzD. The product identity follows by substituting y^2=1-s^2 and z^2=1-ms^2.

## Primary canonical input and an independent incidence check

Stachel's published Theorem 4.3 and full proof, printed p.1614 (PDF p.13), use caustic semiaxes (a_c,b_c), linear eccentricity d_source=sqrt(a_c^2-b_c^2), modulus m_source=d_source/a_c, and step 2 Delta u. Its formula (4.9) is exactly a=a_c dn(v)/cn(v), b=b_c/cn(v), v=2 tau K/N, after alpha=a_c, beta=b_c, c=d_source, k=m_source. The theorem explicitly permits gcd(N,tau)=1 and does not restrict tau=1; that restriction appears only in the separate Corollary 4.5. The full one-paragraph theorem proof obtains b_c=b cn(v) from tangent incidence at the initial point (0,b), then obtains the a formula from confocality and the two quadratic Jacobi identities. The preceding canonical-flow construction on pp.1611--1613 supplies the constant shift. I read that construction, not merely the theorem statement.

There is a genuine printed typo on p.1613: the line dn(u+2jK)=(-1)^j dn(u) is false (take u=0,j=1). The correct real shift has no sign. The candidate does not repeat this typo. The modulus, canonical parametrization, and formula (4.9) are independently checked below and do not use it.

Set beta=alpha k', c=alpha k, a=alpha d/C, b=alpha k'/C. Then

    a^2-b^2=c^2,
    a^2-alpha^2=b^2-beta^2=alpha^2 g t/q>0.

The chord through P(u-v),P(u+v) lies on the tangent to the caustic at T(u)=(-alpha s,beta y): substitution into -X s/alpha+Y y/beta=1 reduces to

    (s d s_+ + y y_+)/C=(s^2 d^2+y^2)/D=1,

and likewise for the minus sign. This verifies the actual caustic incidence and all phases directly from addition. Since the caustic is strictly nested, the contact lies on the segment between the two intersections with the outer ellipse. The source theorem supplies the confocal billiard reflection interpretation. Since P is injective modulo 4K and delta=2v=4K tau/N, these N vertices are distinct and have least period N. The boundary parametrization is positively oriented: det(P,P')=ab dn(u)>0. The rotation number is tau/N. The same tangency construction works for every coprime tau, even when its edges cross. Reversal changes both signed areas by -1.

## Outer tangent intersections: equation (3)

The tangent to E at P(z) is -X sn(z)/a+Y cn(z)/b=1. Put A=a d/C and B=b/C. Substituting Q=(-A s,B y) gives

    d s s_+/C + y y_+/C=(s^2d^2+y^2)/D=1,

for each sign. The magnitude of the tangent coefficient determinant is

    |s_+ y_- - s_- y_+|/(ab)=2hCz/(abD)>0.

Thus the solution is the unique real finite consecutive tangent intersection; (3) is exact. Its axis lengths are

    A=alpha d^2/q, B=alpha k'/q.

Both A>a and B>b: d^2-C^2=g t>0 and 0<C<1. Consequently Q_x^2/a^2+Q_y^2/b^2>1 for all real u. Both original foci are strictly inside E, so Q never equals either focus and every real inversion exists.

No assumption A>B is valid in general. In fact A^2-B^2=alpha^2 m V/q^2, with V=1-2t+mt^2. Since V=W cn(2v), W=1-mt^2>0, the ordering reverses at v=K/2; primitive stars with tau/N>1/4 have B>A. At v=K/2 the locus is a circle (not an admissible odd primitive closure). The original focus (alpha k,0) is used throughout; it is not replaced by a locus focus, which can lie on the y axis when B>A.

## Double-angle abbreviations: equation (4)

Direct addition at v+v gives

    sn(2v)=2hCd/W, cn(2v)=V/W, dn(2v)=U/W,
    U=1-2mt+mt^2, V=1-2t+mt^2, W=1-mt^2.

Therefore (4), including U=W dn(delta) and V=W cn(delta), is correct. W>0 on the full domain.

## Focal distance: equation (5)

For f_+=(alpha k,0), direct Euclidean expansion yields

    |Q-f_+|^2 = (A^2-B^2)s^2+2Ac s+B^2+c^2.

The three polynomial identities

    d^4-g=mV,
    g+m q^2=U,
    U+V=2q d^2

give

    |Q-f_+|^2 = alpha^2/q^2 [U+2kq d^2 s+m V s^2]
                = alpha^2/q^2 (1+ks)(U+kVs).

This proves (5) from geometry. On the real line, 1+ks>=1-k>0, so its other factor is also strictly positive. This is a squared Euclidean distance only for real u; its complex extension is the bilinear sum of squares. No conjugation can be introduced into the meromorphic continuation.

## Actual inversion and the inverse edge: equations (6)--(11)

The geometric inverse is J_f(Q)=f+(Q-f)/|Q-f|^2. A fixed translation by -f sends it to I=(Q-f)/|Q-f|^2, as in (6). Such a translation preserves the *sum* of shoelace edge determinants because all translation terms telescope. It need not preserve each isolated edge determinant. Thus E_+(u)=det(I(u-v),I(u+v))/2 is an edge of a translated inverse polygon, and summing these E_+ is exactly the requested signed area.

For any constants X,Y, the addition identities give

    (X+kY s_-)(X+kY s_+)
      = [X^2-mY^2 t+2kXYCd s+m(Y^2-X^2t)s^2]/D.

With X=Y=1 this numerator is d^2+2kCd s+m q s^2=(d+kCs)^2, proving (9).

With X=U,Y=V define

    L0=(U^2-m V^2t)/d, L1=(V^2-U^2t)/C.

The constant and quadratic coefficients are dL0 and mCL1. The linear coefficient agrees with the product (d+kCs)(L0+kL1s), because

    d^2(V^2-U^2t)+q(U^2-mV^2t)=2UV q d^2.

This is an exact polynomial identity after q=1-t,d^2=1-mt. It proves (10), with no division by V, U, or L1.

The determinant before inversion, retaining the focus translation, is

    det(Q_- - f,Q_+ - f)/2
     = AB(s_+ y_- - s_- y_+)/2 + cB(y_- - y_+)/2
     = AB hCz/D + cB s h z d/D
     = alpha B h d z(d+kCs)/(C D).

This is (11). The distance product, from (5), (9), and (10), is

    |Q_- - f|^2 |Q_+ - f|^2
     = alpha^4/q^4 (d+kCs)^3(L0+kL1s)/D^2.

Dividing the preceding determinant by this exact distance product gives

    E_+(u)= [B h d q^4/(alpha^3 C)]
             z D /[(d+kCs)^2(L0+kL1s)].

This proves (7)--(8), and in particular the q^4 normalization. This factor comes from the product of the two alpha^2/q^2 distance normalizations. Dropping it would preserve constancy in a fixed family but give the wrong geometric area and wrong scale.

## Triple angle and positivity: equations (12)--(15)

Apply addition to 2v+v. Its denominator is

    1-m sn^2(2v) t=Z/W^2,
    Z=W^2-4m t^2 q d^2.

Since real |sn(2v)|<=1 and mt<1, Z>=W^2(1-mt)>0. Put

    D3=UW-2m t q V, C3=VW-2t d^2 U.

Then the unsquared signed addition formulas are

    dn(3v)=d D3/Z, cn(3v)=C C3/Z.

Two exact polynomial identities,

    U^2-mV^2t=d^2D3,
    V^2-U^2t=qC3,

give L0=dD3=Z dn(3v) and L1=C C3=Z cn(3v). Thus (12)--(13) are correct with no sign choice. Using dn^2(x)-m cn^2(x)=g gives

    L0^2-m L1^2=g Z^2>0, L0>0,
    d^2-m C^2=g>0, d>0.

In particular L0>k|L1| and d>kC; hence for every real u,

    L0+kL1s>=L0-k|L1|>0,
    d+kCs>=d-kC=g/(d+kC)>0.

All remaining factors in (8) are positive (including C0=B h d q^4/(alpha^3C)), proving every E_+(u)>0. This is a full-domain algebraic proof, not a finite numerical positivity check. It applies to stars as well as convex orbits.

For odd closure, L1=0 would require cn(3v)=0. As 0<3v<3K, the only permitted zero is 3v=K, giving N=6tau, impossible for odd N. The endpoint 3K is excluded. The N=3 critical case is 3v=2K (not a zero of cn); it has L0=Z,L1=-Z and remains strictly positive on the real line because 1-k sn(u)>0. Coprimality shows 3v=2K iff (N,tau)=(3,1).

## Boundary, dimensions, and interpretation controls

No lower bound uniform in excluded boundary limits is asserted. As v tends to 0, h tends to 0 and an edge tends to zero. As v tends to K, tangent determinants tend to zero and the outer axes diverge; at every strict v<K they remain finite. As k tends to 1 the strict bounds involving g can tend to zero, and beta degenerates at the excluded endpoint. For k tending to 0 with fixed v, the formulas have the circular limit E=sin(v) cos(v)^5/alpha^2: the actual outer circle radius is alpha/cos(v)^2, inverse radius cos(v)^2/alpha, and half its inverse cross product is exactly that expression. This independently checks the normalization and sign.

Under original-geometry scaling alpha -> lambda alpha with k,v fixed, A,B,c,a,b scale by lambda, D_f by lambda^2, translated inverse coordinates by lambda^-1, E and each B by lambda^-2, and B_+B_- by lambda^-4. C0 has dimension length^-2, consistent with every other factor in (8) being dimensionless. For inversion radius r, each inverse coordinate gets r^2 and each area gets r^4, so the product gets r^8. No normalization here treats signed area as arc area or substitutes unsigned filled regions for a star's shoelace sum.

Strongest verified local result: every real geometric and local algebraic assertion (3)--(15), including star scope, actual focus choice, inverse existence, q^4, triple-angle signs, and real positivity, follows by the displayed checkable derivation. No local counterexample or unresolved local algebraic gap was found. The global torus divisor argument, historical novelty, inherited review independence, and publication authority are deliberately not certified by this document.
