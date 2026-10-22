# Independent derivations and falsification certificate

Audit mechanism: literal-source scope and dependency verification, then an orbit-coset classification. Initial challenges are frozen separately in SOURCE_FIRST_FREEZE.md. These are the auditor's own calculations; no submitted verification program was run or imported.

## 1. Precisely quantified family

Let E have axes a>b>0 and focal distance c=sqrt(a^2-b^2). Fix a strictly nested nondegenerate confocal ellipse C with axes alpha>beta>0, alpha^2-beta^2=c^2. Set k=c/alpha, k'=beta/alpha, with 0<k<1. In this document Jacobi functions have modulus k; software mpmath receives parameter k^2. K=K(k), K'=K(k').

The canonical parametrization credited to Stachel is

    P(u)=(-a sn u,b cn u),
    a=alpha dn(v)/cn(v), b=beta/cn(v), 0<v<K,
    delta=2v.

The existence and uniqueness of v in this real interval also follow from cn(v)=beta/b in (0,1), since cn decreases strictly from 1 to 0 on (0,K). Confocality then gives the formula for a. The parameter pair (sn u,cn u) is injective modulo 4K on the real line. Thus least period N means

    N delta=4K tau, gcd(N,tau)=1, 0<tau<N/2.

No simple-polygon hypothesis appears: all these coprime turns are allowed, and reversal only reverses/reindexes the same outer vertices.

## 2. Direct tangent geometry and denominators

Put s=sn u, z=cn u, d=dn u, h=sn v, C=cn v, D=dn v and D0=1-k^2 s^2 h^2. The tangent at P(w) is

    -X sn(w)/a + Y cn(w)/b = 1.

The addition identities applied to w=u-v,u+v reduce the two equations to

    -X s C D/a + Y z C/b = D0,
    -X z/a - Y s D/b = 0.

The second equation divides by h d. This is legal: h>0, C>0 and d>=k'>0 for real u. Also D0>=1-k^2 h^2>0. The determinant of the two original tangent normals has absolute value

    2 h C d/(ab D0)>0.

The unique tangent intersection is therefore

    Q(u)=(-a D sn u/C, b cn u/C).

The actual outer-vertex sequence has phases u0+v+j delta. Absorbing the fixed v in u0 preserves exactly the product in k115. Moreover

    (Qx/a)^2+(Qy/b)^2-1 = h^2 dn^2(u)/C^2 > 0.

Hence every real Q is finite, outside E and different from either interior focus. Its Euclidean focal distances are strictly positive. Solving the tangent equations did not introduce a real excluded phase at s=0 or z=0.

## 3. Paired-distance polynomial independently expanded

Write A=aD/C, B=b/C. Define

    H(u)=((Qx-c)^2+Qy^2)((Qx+c)^2+Qy^2).

This is the square of the product of the two positive focal distances on the real line. Set t=sn^2 v, q=1-t, kappa=k^2 and

    U=1-2 kappa t+kappa t^2 = (1-kappa)+kappa q^2 >0,
    V=1-2t+kappa t^2,
    W=1-kappa t^2 > 1-kappa >0.

Then

    A=alpha(1-kappa t)/q, B=alpha k'/q,
    A^2-B^2=alpha^2 kappa V/q^2,
    B^2+c^2=alpha^2 U/q^2.

For S=sn^2 u, expansion gives

    H=alpha^4/q^4 [(U+kappa V S)^2
                            -4 kappa(1-kappa t)^2 q^2 S].

Since U+V=2q(1-kappa t), the coefficient of S is

    2 kappa UV-kappa(U+V)^2 = -kappa(U^2+V^2).

The constant and quadratic coefficients agree immediately with

    H=alpha^4/q^4 (1-kappa S)(U^2-kappa V^2 S).

The independently authored symbolic program expands the difference to the zero polynomial; this exact algebra check is additional to the displayed coefficient proof. The double-angle formulas give cn(delta)=V/W and dn(delta)=U/W. Thus

    H=Cv dn^2 u J(u),
    J(u)=dn^2(delta)-k^2 cn^2(delta) sn^2 u,
    Cv=alpha^4 W^2/q^4>0.

No division by V or cn(delta) has occurred in deriving this identity.

## 4. Divisor and the exceptional degree drop

Use T=C/(2K Z+2iK' Z) and p=iK'. The function sn^2 has precisely one double pole per T, at p. DLMF's correct shifts give dn(u+2K)=dn u and dn(u+2iK')=-dn u, so dn^2 has both T periods. Its divisor is 2[p+K]-2[p]. This also follows from dn^2=1-k^2 sn^2 and the simple zero of dn at p+K.

The relevant quarter shift is

    sn(z+K+iK')=dn z/(k cn z).

For cn(delta) nonzero, substituting z=+/-delta gives J(p+K+/-delta)=0. These two zeros are distinct on T unless 2delta=0 on T, which for real 0<delta<2K forces delta=K. J has one double pole at p; hence these two distinct zeros exhaust its degree and are simple. Neither is p or p+K. Consequently

    div H=2[p+K]+[p+K+delta]+[p+K-delta]-4[p].

For delta=K, cn(delta)=0 and J=k'^2 is constant. In the primitive even family delta=4K tau/N=K and coprimality force N=4,tau=1. The correct divisor is then only

    div H=2[p+K]-2[p].

This is an actual degree drop; using a generic order-four pole for N=4 would be an error. The submitted proof separates it correctly. The outer locus becomes a circle exactly in this case (V=0).

## 5. Orbit-coset classification: both parity directions

For any primitive even N>=4, put m=N/2. Since tau is odd, the delta-translation has order m on T, and Q(u+m delta)=-Q(u). If R_N(u) is the one-focus product over the N outer vertices, then

    R_N(u)^2=F_m(u):= product_{j=0}^{m-1} H(u+j delta).

All factors are positive on the real line. Let G be the m-element subgroup generated by delta in T. In the generic case the complete divisor is

    div F_m = 4 sum_{g in G}[p+K+g] - 4 sum_{g in G}[p+g].

This expression follows because the +delta and -delta zero families are permutations of the same K-shifted orbit; no counting by just the number of zeros is being assumed.

If N=0 mod4, m is even. In units of 2K, G consists of j tau/m modulo 1; tau is invertible modulo m, so G contains 1/2, that is K. The two cosets above are identical and every divisor coefficient cancels. For N=4 the same argument applies with coefficient 2 in place of 4. Thus F_m has no poles on the compact torus and is constant. Its positive real square root R_N is constant, with no complex square-root branch choice. Pairing also shows the two one-focus products have the same value.

If N=2 mod4, m is odd and K is not in G. The two cosets are disjoint and div F_m is nonzero. Delta=K cannot occur here. Hence F_m is nonconstant meromorphic. It cannot be constant on the real line, since then the identity theorem would make it constant on T. Positivity again transfers this nonconstancy to R_N.

Therefore for every noncircular strictly nested confocal-ellipse family of primitive even period N>=4, the outer one-focus product is constant if and only if N is divisible by 4. This is a checkable audit deduction, without a novelty claim.

## 6. Exact repeated-period obstruction

Choose any 0<k<1, alpha>0, beta=alpha sqrt(1-k^2), and v=K/3. The canonical axes a=alpha dn(v)/cn(v), b=beta/cn(v) define a strictly nested nondegenerate confocal ellipse. Delta=2K/3 has least period 6 on P's 4K real period, and m=3. Its p-orbit and p+K-orbit are disjoint. Section 5 proves R_6(u) is nonconstant.

Traverse that orbit twice and call the word length N=12. Its nominal k115 product is R_12(u)=R_6(u)^2, which remains nonconstant. Thus the source's row cannot be literally extended to all traversal lengths divisible by four. The primitive convention is mathematically necessary, not a cosmetic convention. Conversely, repeating a primitive orbit whose product is already constant simply raises that constant to a power.

For a concrete diagnostic, the independent program takes k=.65, alpha=2 and phases u/K=0,.37,1.13. The nominal 12-factor double-cover products are approximately 25632.34717, 25600.35347, 25610.27499. These decimals illustrate the exact divisor argument; they are not offered as interval certificates.

## 7. Scope and boundary inventory

- Hyperbolic caustics: excluded by the primary target's explicit confocal-ellipse definition and by Stachel's cited theorem. No conclusion follows here for their billiard component structure or periods.
- Focal-segment and collapsed caustics: beta=0 or k=1 destroys the stated torus/positivity assumptions; excluded.
- Coincident billiard/caustic: v=0 gives no genuine positive-length step and invalidates h>0; excluded.
- Circular billiard: k=0 is outside the divisor proof, but a separate Euclidean argument gives a fixed outer radius for each regular star rotation; constancy is immediate.
- Grazing and separatrix limits: limiting statements do not assert inclusion at their singular endpoints.
- Primitive star trajectories: explicitly covered for every coprime 0<tau<N/2, including when adjacent tangent intersections lie on apparently inverted edges. Direct tangent-line geometry uses complete lines and positive distances, so no convexity of the outer polygon is assumed.
- Orientation: reversing the orbit reverses the same cyclic intersections and does not change a product. Either focus is equivalent by antipodal pairing.
- Signed areas and interior/exterior angle conventions: absent from these derivations. No source area or angle invariant is imported.

## 8. Computational scope and reproducibility

The independently authored check_quantifiers.py uses 65 decimal digits and freshly constructs the two tangent lines; it does not substitute the derived Q formula as its distance-product input. For all coprime turns at N=4,8,12,16,20,24, k=.05,.65,.98 and three phases per family, it checks direct product constancy, two-focus equality, canonical caustic tangency, reflection, and Q-formula agreement. check_results.json contains the full family list and residuals. It also checks the factorization exactly in a polynomial ring and finite rational translation-orbit identities through N=100. These finite tests supplement, and do not replace, the all-N analytic argument above.
