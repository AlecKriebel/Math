# Independent global meromorphic derivation, frozen before inherited checks

Audit: PR211 / 5100063 / k904,a. Author of this audit: independent meromorphic-divisor adversary subagent. This is a verification artifact, not publication or priority clearance. No inherited review, checker, PASS assertion, or other PR is used below.

## 1. Precisely verified conditional claim

Let 0<k<1, k_c=sqrt(1-k²), K=K(k), K_c=K(k_c), p=iK_c. Let N>=3 be odd, gcd(tau,N)=1, 0<tau<N/2, v=2K tau/N. Thus 0<v<K and delta=2v=4K tau/N. Set

```
h=sn(v), C=cn(v), d=dn(v), t=h², q=C²,
W=1-k²t², U=1-2k²t+k²t², V=1-2t+k²t²,
L0=(U²-k²V²t)/d, L1=(V²-U²t)/C,
T(u)=1-k²t sn²(u), H1(u)=d+kC sn(u),
H2(u)=L0+kL1 sn(u),
E(u)=C0 dn(u) T(u)/(H1(u)² H2(u)), C0>0.
```

For F(u)=sum_{j=0}^{N-1} E(u+j delta), the independently reconstructed conclusion is

```
F(u) F(u+2K) = a positive real constant.
```

This statement follows without any geometric divisor assumption. The geometry-to-E normalization is also reconstructed algebraically below, assuming Stachel's real canonical parametrization. The source statement's interpretation is independently checked only to the extent described in the report; this audit does not decide literature priority.

## 2. Published identities and signs actually checked

Official primary sources consulted 2026-10-15 UTC: [DLMF 22.4](https://dlmf.nist.gov/22.4), [22.8](https://dlmf.nist.gov/22.8), [22.13](https://dlmf.nist.gov/22.13). Table 22.4.3, equations 22.8.1–3, Table 22.13.1 and equation 22.13.13 fix the conventions. The exact transforms used are

```
sn(z+2K)=-sn z; cn(z+2K)=-cn z; dn(z+2K)=dn z;
sn(z+2p)=sn z; cn(z+2p)=-cn z; dn(z+2p)=-dn z;
sn(K+p+z)=dn z/(k cn z);
cn(K+p+z)=-i k_c/(k cn z);
dn(K+p+z)=i k_c sn z/cn z;
sn(p+z)=1/(k sn z); cn(p+z)=-i dn z/(k sn z);
dn(p+z)=-i cn z/sn z.
```

In particular dn has period 2K, not real antiperiod 2K. A conflicting auxiliary line in the Stachel paper is not used. These transforms, plus odd sn and even cn,dn, determine all signs below.

On the genuine common torus T4=C/(4K Z+4p Z), the complete simple pole list of each of sn,cn,dn is p,2K+p,3p,2K+3p. Their respective simple zeros are

```
sn: 0,2K,2p,2K+2p;
cn: K,3K,K+2p,3K+2p;
dn: K+p,3K+p,K+3p,3K+3p.
```

On the smaller sn torus Ts=C/(4K Z+2p Z), sn has two simple poles and degree two. Its complete finite critical fibers are value +1 at K, -1 at 3K, +1/k at K+p, -1/k at 3K+p, each with multiplicity two. This follows from sn'=cn dn, the preceding zeros, and sn''=-(1+k²)sn+2k²sn³; the four values are distinct for 0<k<1 and the second derivatives there do not vanish. Infinity is unramified because both poles are simple. Thus there are no additional critical values or unexamined fiber points.

## 3. Independent algebra connecting real inverse edges to E

Let alpha>0, c=alpha k, A=alpha d²/q, B=alpha k_c/q and Q(u)=(-A sn u,B cn u). Set f=(c,0) and the bilinear squared norm

```
D_f(u)=(Q_x(u)-c)²+Q_y(u)²
      = alpha²/q² (1+k sn u)(U+kV sn u).
```

Indeed A²-B²=alpha²k²V/q², B²+c²=alpha²U/q², and U+V=2qd², so the coefficients in sn u agree. For real u the norm is the ordinary positive Euclidean norm; its complex continuation uses no conjugation. Each component of I(u)=(Q(u)-f)/D_f(u) is a quotient of meromorphic functions. It is therefore meromorphic globally, including at poles where a quotient initially has a removable presentation. The equality theorem extends identities first obtained away from denominators across their entire meromorphic domains.

For s=sn u, x=cn u, y=dn u, addition gives

```
s_±=(s C d ± h x y)/T,
c_±=(x C ∓ s y h d)/T,
s_+ c_- -s_- c_+ = 2h C y/T,
c_- -c_+ = 2s y h d/T.
```

Consequently the half determinant of the untranslated focal vectors equals

```
det(Q(u-v)-f,Q(u+v)-f)/2
 = AB h C y/T + cB s y h d/T
 = alpha B h d y (d+kC s)/(C T).
```

The two distance-factor products are

```
(1+k s_-)(1+k s_+) = H1²/T,
(U+kV s_-)(U+kV s_+) = H1 H2/T.
```

To check these without treating an addition denominator as a premise, multiply by T² and reduce x²=1-s², y²=1-k²s². The first identity is a polynomial identity. In the second, constant and quadratic coefficients give the stated L0,L1, and its linear coefficient reduces to

```
d²(V²-U²t)+q(U²-k²V²t)-2UV q d²=0.
```

Dividing the determinant by D_f(u-v)D_f(u+v) produces E exactly, with

```
C0=B h d q⁴/(alpha³ C)>0.
```

This is the straight-edge inverse polygon's signed edge area. Translation by f changes individual half determinants but its added terms telescope in the closed shoelace sum. Thus computing with I instead of f+I does not change the polygon area.

## 4. Triple-angle reduction and positivity

The double-angle quantities are sn(2v)=2hCd/W, cn(2v)=V/W, dn(2v)=U/W. Let

```
Z=W²-4k²t² qd²
 = W²(1-k²t sn²(2v))>0,
D3=UW-2k²tqV, C3=VW-2t d²U.
```

Direct substitution in the addition formulas gives

```
dn(3v)=d D3/Z, cn(3v)=C C3/Z,
U²-k²V²t=d² D3, V²-U²t=q C3.
```

Hence L0=Z dn(3v), L1=Z cn(3v), and

```
L0>0, L0²-k²L1²=k_c² Z²>0,
d²-k²C²=k_c²>0.
```

Since |sn u|<=1 on the real axis, H1,H2,T,dn(u),C0 are all positive there. Therefore E(u)>0 and F(u)>0 for real u. No later divisor assertion is vacuous through F identically zero.

The potentially troublesome coefficient L1 cannot vanish: cn(3v)=0 requires 3v=K in 0<3v<3K, so N=6tau, incompatible with odd N and gcd(tau,N)=1. The excluded 3v=3K occurs only at v=K. Also V=0 would force 2v=K, i.e. N=4tau, likewise impossible. We do not divide by V in the global proof, but V!=0 sharpens the local controls.

## 5. All possible poles, with exact orders

Let r=3K+p and a_±=r±v. By the checked quarter shifts,

```
sn(r±a)=-dn(a)/(k cn(a)).
```

For H1 the two points are a_±. They are distinct on Ts because their separation is 2v in (0,2K). Their sn value has magnitude greater than 1/k, since d²-C²=k_c²h²>0. It is therefore not a critical value. Both H1 zeros are simple, and degree two exhausts the fiber.

The values at a_± are more informative than just the fiber count:

```
sn(a_±)=-d/(kC), cn(a_±)=i k_c/(kC),
dn(a_±)=±i k_c h/C,
H1'(a_±)=∓k_c² h/C,
T(a_±)=V/q,
H2(a_±)=L0-d L1/C=4 k_c² h² d W>0.
```

The last equality follows from C L0-d L1=W(U²-V²)/(Cd)=4 k_c²t C dW. Thus the first and second denominator fibers do not collide, with no geometric assumption. The exact quadratic Laurent coefficients of E are

```
A2(a_±)=±i C0 V/(4 k_c⁵ h³ C d W).
```

For allowed odd N they are nonzero. These are actual double edge poles, and their coefficients are opposite.

For H2, the two fiber points are b_±=r±3v, counted with multiplicity. Since cn(3v)!=0 the factor is genuinely linear in sn. The target sn value cannot equal ±1 because dn²(3v)-k²cn²(3v)=k_c²>0. It equals ±1/k only if sn(3v)=0, namely 3v=2K in this interval. Absent this exception the two points are distinct and simple; degree two exhausts H2's zeros. Equality b_±=a_± on Ts would require 2v or 4v to lie in 4K Z, impossible for 0<v<K. This also follows from the positive H2(a_±) identity.

At the exceptional 3v=2K, 3tau=N and primitivity forces (N,tau)=(3,1). Then L0=Z,L1=-Z, b_+=b_-=b=K+p on Ts, and H2=Z(1-k sn u). For z=u-b,

```
sn(b+z)=1/k + k_c² z²/(2k)+O(z⁴),
dn(b+z)=i k_c z+O(z³),
H2(b+z)=-Z k_c² z²/2+O(z⁴),
T(b)=q, H1(b)=d+C>0.
```

It follows that E has an actual simple pole with residue

```
-2i C0 q/(Z k_c (d+C)²) != 0.
```

This is one double H2 zero canceled by one simple dn zero; it is not two separate simple roots silently summed.

For completeness, the numerator T cannot vanish at b_± for an allowed primitive odd pair. If it did, sn(b_±)=±1/(kh). The quarter shifts show the complete T-zero list on Ts is p±v,2K+p±v. Equating it with r±3v gives 2v or 4v congruent to an odd multiple of K, or the excluded endpoints. These relations force N to divide 4 or 8 after gcd(tau,N)=1, and no odd N>=3 qualifies. Thus the nonexceptional b_± are also actual simple edge poles. No stronger assertion about their residues is required for F.

At any common Jacobi pole z0, sn~s_{-1}/z, dn~d_{-1}/z with both coefficients nonzero. The numerator dn T has order three and H1² H2 has order three because k,C,L1 are nonzero. More explicitly, their quotient tends

```
-C0 t/(k C² L1) * (d_{-1}/s_{-1}),
```

which is finite and nonzero. There is no unaccounted pole there. At other dn zeros all denominator factors are nonzero, except the N=3 point already examined; such points give zeros, not poles. At cn or sn zeros nothing can blow up: they are real points or their 2p translates and the checked antiperiod signs preserve denominator nonvanishing. This exhausts all potential poles of the rational expression in sn,dn.

The proof only needs the following upper bound, now justified pointwise: E has double poles at a_±, simple poles at b_± (coalescent simple pole for N=3), their 2p translates, and no others on T4.

## 6. Cancellation at every translated point with multiplicities

The exact shifts imply sn(2r-u)=sn u and dn(2r-u)=-dn u, hence E(2r-u)=-E(u). If

```
E(a_++z)=A/z²+B/z+O(1),
```

then E(a_-+z)=-A/z²+B/z+O(1). This agrees with the explicit A2 above. At the 2p translates both coefficients change sign by antiperiodicity; the opposite pairing remains exact.

delta has order exactly N on the real 4K circle: j delta=0 mod 4K iff N divides j, by primitivity. For every point x=a_+-j delta (j mod N), precisely one summand E(u+j delta) supplies the a_+ quadratic term, and precisely one, indexed j-1 mod N, supplies the a_- term. They cancel. This is a pointwise bijection of the two complete double-pole lists; no generic-position assumption or uncounted multiplicity is used.

All b-poles lie in the same orbit: b_+=a_++delta and b_-=a_+-2delta. They contribute no quadratic term. In N=3 these two labels describe one actual local pole, already of order one; it is counted once as a singular point of each summand. At x+2p the identical cancellation holds with every sign reversed. No other point can be singular in the finite sum. Thus F has at most simple poles in these two real orbit classes.

## 7. Reduced torus, actual divisor, and product

F has period delta by cyclic reindexing using N delta=4K tau, and period 4K because E does. Choose integers a,b with a tau+bN=1. Then a delta+b4K=4K/N=L is a period. This is a proved period, without needing to claim it is the minimal one. Also F(u+2p)=-F(u), so 4p is a period. On X=C/(L Z+4p Z), the preceding singularity classes become just

```
R=r+v, R+2p,
```

each of order at most one. They are distinct because 2p is not in L Z+4p Z. If F had no poles, compactness would make it constant; its antiperiod would make the constant zero, contradicting F>0 on the real line. Antiperiodicity pairs these two possible poles, so both are actual simple poles.

Reindexing the reflection gives F(2r-u)=-F(u). Since 2v=delta is a period, F is also odd about R: F(2R-u)=-F(u). At Z0=R+L/2, reflection maps Z0 to Z0-L; hence F(Z0)=-F(Z0). Z0 is not a pole because it differs from the only pole R by L/2, not a lattice vector, and its imaginary displacement from R+2p cannot be a lattice vector. Thus F(Z0)=0. Antiperiodicity gives the distinct second zero Z0+2p. A nonzero meromorphic function on a compact torus has equally many zeros and poles, counted with multiplicity. The two simple poles force these to be exactly the two zeros, both simple:

```
div(F)=[R+L/2]+[R+L/2+2p]-[R]-[R+2p].
```

Translating u by L/2 exchanges this divisor's zeros and poles. The product F(u)F(u+L/2) therefore has neither zeros nor poles. It is a nonzero holomorphic function on compact X, hence a nonzero constant. At real u both factors are positive, so the constant is positive real. No area or possibly vanishing function was divided out.

## 8. Original opposite-focus relation

Q(u+2K)=-Q(u). For J_f(x)=f+(x-f)/||x-f||², using the bilinear norm under complex continuation,

```
J_{-f}(Q(u))=-J_f(Q(u+2K)).
```

Central reflection multiplies each vector by -1 and preserves every determinant; it therefore preserves signed shoelace area, including stars. For Q_i=Q(w+i delta), the first focal area is F(w+v), and the second is F(w+v+2K). These are the ORIGINAL foci ±alpha k; no focus of the outer locus is substituted. Since N is odd,

```
2K=N L/2 = L/2 mod L.
```

The verified analytic constant is consequently the claimed product of focal inverse outer areas. Reversing the vertex order reverses both signed areas, leaving the product unchanged.

## 9. Boundaries and adversarial attempts

The analytic proof requires 0<k<1, C>0, odd primitive N. Each use of them is explicit. In the circle case k=0, the foci coincide at the center. A periodic billiard is a rotating regular star, the outer polygon has radius R=a/cos(pi tau/N), and its inverse is a regular star of radius 1/R; its signed area is N sin(2pi tau/N)/(2R²), independent of rotation. Thus the coincident-focus product is constant separately.

If an odd N notation describes r repetitions of a least-period n orbit, N=rn implies r,n odd. Shoelace area multiplies by r, so the product multiplies by r² and remains constant. The primitive proof therefore does not exclude repeated odd orbits from the conclusion, although its analytic reduction uses the primitive n.

A nondegenerate confocal hyperbola has equation x²/A_h²-y²/B_h²=1 with 0<A_h<c<a. A finite tangent at (x_t,y_t) crosses the x-axis at x0=A_h²/x_t, so |x0|<=A_h<a; its asymptotes cross at zero. This point lies strictly inside the billiard ellipse. Therefore the chord endpoints have nonzero, opposite y signs. Any periodic real billiard tangent to this hyperbola has even period. There is no odd nondegenerate hyperbolic counterexample to add to the elliptic proof. For the focal-segment separatrix, every nonaxial edge similarly crosses that segment and reverses y sign; an axial edge forces the two-axis endpoint orbit of period two. These degenerations do not provide a nontrivial odd finite orbit. Coincident successive vertices or outer tangents at infinity are outside the ordinary nondegenerate polygon definition and cannot be inserted by assuming a limiting area exists.

Counterexample mechanisms explicitly attacked: (i) omitted common Jacobi poles, (ii) L1=0 and fiber at infinity, (iii) branch values ±1 and ±1/k, (iv) collisions of first and second fibers, (v) numerator cancellation concealing a higher-order N=3 pole, (vi) translated double-pole multiplicity, (vii) F identically zero, (viii) half-period fixed points also being poles, (ix) wrong imaginary/real Jacobi signs, (x) original foci accidentally changed to locus foci. No counterexample was found in the exact analysis. Independent numerical controls are diagnostics only and are written after freezing this derivation.
