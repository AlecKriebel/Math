# Reconstruction of the alternate telescoping proof

This is an independently reconstructed argument for the exact pinned input in `RESEARCH_LOG.md`. No earlier review was used. Symbols follow the reviewed draft. The exact algebra is also reproducible with `independent_exact.py`; it imports neither the submitted checker nor its generated results.

## Mathematical domain and canonical input

For a strictly nested confocal pair with outer axes `a>b>0` and caustic axes `alpha>beta>0`, put `c^2=a^2-b^2=alpha^2-beta^2`, `k=c/alpha`, `kp=beta/alpha`. Thus `0<k<1`. The exact Stachel published Theorem 4.3 and (4.9), printed p.1614, give

```
P(w)=(-a sn(w,k), b cn(w,k)),
v=2K tau/N, delta=2v,
a=alpha dn(v)/cn(v), b=beta/cn(v).
```

Choose the forward representative `0<tau<N/2`; reversal handles the opposite orientation. Then `0<v<K`. If `N=4n` is least and `gcd(N,tau)=1`, `tau` is odd. Define `m=N/2` and `ell=2K/m`.

The map `w -> P(w)` is injective modulo `4K`: on the real line the Jacobi amplitude has derivative `dn(w)>0`, and `(sn,cn)` specifies its value modulo `2pi`. Therefore the least return of the vertex sequence is the smallest positive integer `r` with `r tau/N` integral, namely `N/gcd(N,tau)`. This verifies that the proof's primitive indexing is essential, not a labeling convention.

## Area reconstruction and factors

Write `s=sn(u)`, `d=dn(u)`, `h=sn(v)`, `cv=cn(v)`, `dv=dn(v)`, `t=h^2`, `q=1-t`, `D=1-k^2 t s^2`, with `U,V,W,C,C_A` as in the pinned draft.

The Euclidean focus distance is exactly `a+c sn(w)`, because its square equals `(-a sn(w)-c)^2+b^2 cn(w)^2` and `a-c>0`. Thus there is no branch choice on the real line. The algebraic continuation used in the draft is appropriate for identities, and no complex Euclidean norm is invoked.

Direct substitution of the Jacobi addition formulas gives

```
det(P(u-v),P(u+v)) = 2ab h cv d/D,
dn(u-v)+dn(u+v) = 2d dv/D,
(a+c sn(u-v))(a+c sn(u+v))
  = alpha^2 (1+ks)(U+kVs)/(qD),
det(P(u-v)-(c,0),P(u+v)-(c,0))
  = 2 alpha b h dv d (1+ks)/D.
```

Each side contributes half its determinant. Dividing the last determinant by twice the square of the distance product gives precisely the draft's `E(u)`. Translating a focal inverse polygon by the focus does not change its closed shoelace area, so the draft's relative-coordinate inversion has the correct physical area.

For the original area, each half-determinant is `(C_A/2)` times the sum of the endpoint `dn` values. Summing edges counts each vertex twice, giving `C_A sum_{j<N}dn(w+j delta)`. Since `m delta=2K tau` and `dn` has period `2K`, this is `2 C_A S(w)`, with `S(w)=sum_{j<m}dn(w+j delta)`. There is no missing factor of two.

Since `tau` is odd, `P(w+m delta)=-P(w)`. Pairing side `j` with side `j+m` therefore replaces `s` by `-s` while keeping `d` fixed. The two rational terms combine to

```
B(u)/(2C)
 = (1-k^2 t s^2)[U^2+k^2 V(V+2U)s^2]
   /(d [U^2-k^2 V^2 s^2]^2).
```

The second half of the actual edge set is exactly that antipodal partner, including star windings. The centers of the edges of a polygon starting at `P(w)` are `w+v+j delta`, so its inverse area is `R(w+v)`, not `R(w)`.

## Independent coefficient reconstruction

Let `x=s^2`, `H=U^2-k^2 V^2 x`, and `F=1/dn`. The dn addition formula, with both plus and minus shifts, gives

```
F(u+delta)+F(u-delta) = 2WU dn(u)/H,
F(u+delta)-F(u-delta)
 = 2k^2 sn(delta)cn(delta) W^2 sn(u)cn(u)/H.
```

The common denominator factorization was independently reduced in the Jacobi quadrics in the exact checker. Differentiate the second equation. Since `d(sn cn)/du=dn(1-2x)` and `x'=2 sn cn dn`, its numerator is

```
(1-2x)H+2k^2 V^2 x(1-x)
  = U^2+(k^2 V^2-2U^2)x.
```

For abstract `U,V,k,t`, solve the three coefficient equations in

```
(1-k^2 t x)[U^2+k^2 V(V+2U)x]
 = A H^2+B0(1-k^2 x)H
   +D0(1-k^2 x)[U^2+(k^2 V^2-2U^2)x].
```

The independent solve yields exactly

```
A=(1-t)/(U-V)^2,
D0=k^2 V(V^2-U^2 t)/[(U^2-k^2 V^2)(U-V)],
B0=U[U^3 t+U^2 V k^2 t-2U^2 V-2UV^2 k^2 t+UV^2+V^3 k^2]
   /[(U^2-k^2 V^2)(U-V)^2].
```

Exact re-substitution into the polynomial identity gives zero. After specializing `U,V,W`, the cyclic coefficient satisfies `A+B0/(WU)=Lambda` with exactly the displayed draft formula for `Lambda`. Thus `A=a0`, `B0=2WU a1`, and the derivative's prefactor `2k^2 sn(delta)cn(delta)W^2=4k^2 h cv dv V` converts `D0` to exactly the draft's `a2`. The sign of the derivative difference is positive, as written in the draft.

Now `F` and `F'` are `2K` periodic, and `m delta=2K tau`. Summing each shifted `F` over the cycle merely reindexes it, while the difference of shifted derivative sums is zero. The sum is therefore

```
R(u)=2C(a0+2a1) sum_{j<m}F(u+j delta)
    =(2C Lambda/kp) S(u+K).
```

The last equality follows from `dn(z+K)=kp/dn(z)`, obtained by the dn addition formula at `K`.

## Coefficient domains, signs, and V=0

On the full real physical domain,

```
U=1-k^2+k^2(1-t)^2>0,
W=1-k^2 t^2>0,
U-V=2t kp^2>0,
U^2-k^2 V^2=kp^2 W^2>0.
```

Consequently `U>|kV|`, `H>=kp^2 W^2>0`, `D>=1-k^2 t>0`, and `1+k sn(u)>=1-k>0`. Also `h,cv,dv,kp` are positive. Every coefficient denominator in the actual pointwise identity is nonzero; no inverse focus distance vanishes. There is no division by `V` in the displayed coefficients. `a0>0`; `a1,a2` can change signs, and their signs are not used. `Lambda>0`: putting `r=k^2`, its bracket is `P(t)=r^2(t^3+t^2)-5rt+r+2`. Its derivative is `r[r(3t^2+2t)-5]<0` on `0<t<1`, and `P(1)=2(1-r)^2>0`. Hence the forward signed areas and explicit product are positive.

If `V=0`, `cn(delta)=0` and `0<delta<2K` give `delta=K`, so `tau/N=1/4`. Primitivity forces `N=4,tau=1`. The independent coefficient solve gives `B0=t`, `D0=0`, and `a0=q/U^2`. The finite `a2=-t/(4h cv dv U)` multiplies the identically vanishing difference `F'(u+K)-F'(u-K)`. The pair reduces to

```
B(u)=(2C/U^2)[q/dn(u)+t dn(u)].
```

This establishes the exact exception by substitution; a limiting argument is unnecessary.

At phase zero the original vertices are `(0,b),(-a,0),(0,-b),(a,0)`, of area `2ab`. Relative to focus `(c,0)`, their inverse vertices are

```
(-c,b)/a^2, (-1/(a+c),0), (-c,-b)/a^2, (1/(a-c),0).
```

Their signed area is `(b/a^2)[1/(a+c)+1/(a-c)]=2/(ab)`, giving product `4` as claimed.

## Fourier filter, theta normalization, and final product

Because `gcd(tau,m)=1`, the `m` points `j delta` modulo `2K` are exactly the uniform grid `2Kj/m` in permuted order. DLMF 22.11.3 with DLMF 22.2.3 is

```
dn(w,k)=pi/(2K)+(2pi/K) sum_{r>=1}
        [q_e^r/(1+q_e^(2r))] cos(r pi w/K).
```

For real `w` and `0<q_e<1`, the nonconstant terms are bounded in absolute value by `(2pi/K)q_e^r`, a convergent geometric series uniformly in `w`. Thus the finite grid sum can be exchanged with this series. The roots-of-unity filter removes indices not divisible by `m`, giving

```
S(w)=m pi/(2K)+(2m pi/K) sum_{r>=1}
     [(q_e^m)^r/(1+(q_e^m)^(2r))] cos(r pi m w/K).
```

Let `kappa` have nome `Q=q_e^m`, let `K_m=K(kappa)`, and `lambda=m K_m/K`. Such a real `0<kappa<1` exists: the nome map runs continuously and strictly increasingly from zero to one as `k` runs from zero to one, since `K(k)` strictly increases while `K(sqrt(1-k^2))` strictly decreases. Alternatively the exact inverse formulas are DLMF 22.2.2. Comparing the complete Fourier coefficients gives exactly `S(w)=lambda dn(lambda w,kappa)`. Both the constant term and every nonconstant coefficient agree; the argument frequency is `lambda/K_m=m/K`.

Since `lambda ell/2=K_m`, the quarter-shift identity gives

```
S(w)S(w+ell/2)=lambda^2 sqrt(1-kappa^2).
```

DLMF 22.2.2 gives `K_m=pi theta3(0,Q)^2/2` and `sqrt(1-kappa^2)=theta4(0,Q)^2/theta3(0,Q)^2`; hence the alternative constant is exactly `(m pi/(2K))^2 theta3(0,Q)^2 theta4(0,Q)^2`.

Finally `(K+v)/ell=(m+tau)/2` is a half-integer because `m` is even and `tau` odd. The period `ell` of `S` therefore gives

```
A(w) A_+^dagger(w)
 = (4 C_A C Lambda/kp) S(w) S(w+K+v)
 = (4 C_A C Lambda/kp) lambda^2 sqrt(1-kappa^2),
```

which is exactly the pinned explicit value.

Central negation is the ordered vertex shift by `m`. Its focal inverses about the opposite focus are central negatives of the shifted original focal inverse vertices, so both inverse signed areas agree. Reversal negates both signed areas. A positive physical similarity multiplies the original area by the square of its ratio and the unit inverse area by its reciprocal square. These three reductions preserve the claimed product and do not alter the period argument.

The circular endpoint can also be checked directly: an outer circle of radius `a` has inverse vertex radius `1/a`, and regular-star signed area `N a^2 sin(2pi tau/N)/2`, giving the pinned circular product. This is a separate endpoint check; the strict noncircular theorem and its algebra do not need that endpoint. Zero caustic minor axis and `k=1` remain excluded.

Primary inputs: [Stachel, published theorem and equation](https://doi.org/10.1007/s40879-021-00524-2), [DLMF addition formulas](https://dlmf.nist.gov/22.8), [DLMF dn Fourier series](https://dlmf.nist.gov/22.11.E3), and [DLMF nome/theta normalization](https://dlmf.nist.gov/22.2). No novelty or priority claim follows from this audit.
