# Independent direct telescoping derivation for the focal-inversion area product

Status: an independently derived exact route, checked by rational polynomial certificates and separate Euclidean diagnostics. Novelty is unestablished. This artifact does not promote or modify the submitted candidate. Created 2026-10-16 UTC.

## Claim and assumptions

Let an outer ellipse have axes `a>b>0` and foci `(±c,0)`. Its caustic is a strictly nested nondegenerate confocal ellipse with axes `alpha>beta>0`. Suppose a billiard has least period `N=4n`, turning number `tau`, `gcd(N,tau)=1`, and `0<tau<N/2`. The polygon area is the signed shoelace area, with self-intersections counted algebraically. Invert vertices, rather than whole sides, in unit circles about either focus and again take the straight-edge signed shoelace area. The product is constant along the one-parameter family; the two focal inverse areas agree.

The canonical parametrization is the published Stachel Theorem 4.3 and Eq. (4.9), using the modulus convention rather than its square:

```
k=c/alpha,  kp=beta/alpha=sqrt(1-k^2),  0<k<1,
K=K(k),  v=2K tau/N,  delta=2v,
a=alpha dn(v)/cn(v),  b=beta/cn(v),
P(w)=(-a sn(w), b cn(w)).
```

Standard Jacobi addition and differentiation formulas are the only special-function input to the direct telescoping step. A separate Fourier argument below supplies the cyclic product identity and avoids complex pole counting throughout this route.

## 1. Exact focal and shoelace identities

Put `h=sn(v)`, `t=h^2`, `q=cn(v)^2=1-t`, `d_v=dn(v)`, and

```
U=1-2k^2 t+k^2 t^2,
V=1-2t+k^2 t^2,
W=1-k^2 t^2,
C=b h d_v q^2/alpha^3,
C_A=ab h cn(v)/d_v.
```

Then `cn(delta)=V/W`, `dn(delta)=U/W`, `U-V=2t kp^2`, and `U^2-k^2 V^2=kp^2 W^2`.

For a real phase `w`, the ordinary distance to `(c,0)` is `d(w)=a+c sn(w)>0`. This follows by squaring; the lower bound is `a-c>0`. Its algebraic continuation is `a+c sn(w)`, rather than a complex Euclidean norm. Let `I(w)=(P(w)-(c,0))/d(w)^2`. For a side centered at `u`, set `s=sn(u)`, `d=dn(u)`, `D=1-k^2 t s^2`. Direct Jacobi addition yields

```
d(u-v)d(u+v)=alpha^2 (1+ks)(U+kVs)/(qD),
det(P(u-v)-(c,0),P(u+v)-(c,0))
    =2alpha b h d_v d(1+ks)/D.
```

Thus the half-cross-product of the inverted endpoints is exactly

```
E(u)=C d D/((1+ks)(U+kVs)^2).
```

These identities are polynomial/rational identities after substitution of the addition formulas, so they also hold meromorphically. They are not justified using complex conjugation. Independently reducing their numerators in the quadrics `cn^2=1-sn^2`, `dn^2=1-k^2 sn^2` gives zero; see `algebra_check.py`.

Pair antipodal sides. The pair contribution `B(u)=E(u)+E(u+2K)` is

```
B(u)=2C(1-k^2 t s^2)[U^2+k^2 V(V+2U)s^2]
       /(dn(u)[U^2-k^2 V^2 s^2]^2).                 (A)
```

The ordinary endpoint cross product is `2ab h cn(v) dn(u)/D`. Since the sum of endpoint `dn` values is `2dn(u)d_v/D`, summing the half-cross-products gives

```
A(w)=2C_A S(w),
S(w)=sum(j=0,...,m-1) dn(w+j delta),  m=N/2.
```

The `m`-step displacement is `2K tau`; coprimality makes `tau` odd, so the other half is antipodal and the full `N`-term `dn` sum is twice this `S`.

## 2. A direct identity whose shifted terms telescope

Define `F(u)=1/dn(u)` and

```
Lambda = U [k^4 t^3+k^4 t^2-5k^2 t+k^2+2]/(2 kp^4 W^3),
a0 = q/(U-V)^2,
a1 = (Lambda-a0)/2,
a2 = (V^2-U^2 t)/(4 h cn(v) d_v (U^2-k^2 V^2)(U-V)).
```

Then the following identity holds meromorphically:

```
B(u)/(2C) = a0 F(u)
          + a1 [F(u+delta)+F(u-delta)]
          + a2 [F'(u+delta)-F'(u-delta)].           (B)
```

Here the prime differentiates the argument, and `F'=k^2 sn cn/dn^2`. This is the main independent derivation: it replaces the submitted proof's double-pole cancellation and residue-matching steps by an explicit rational identity.

To check it, put `x=sn(u)^2`, `H=U^2-k^2 V^2 x`, and use addition:

```
F(u+delta)+F(u-delta) = 2WU dn(u)/H,
F(u+delta)-F(u-delta)
    =2k^2 sn(delta)cn(delta)W^2 sn(u)cn(u)/H.
```

Since `d(sn cn)/du=dn(1-2x)` and `dx/du=2sn cn dn`, the derivative of the difference is

```
2k^2 sn(delta)cn(delta)W^2 dn(u)
       [U^2+(k^2 V^2-2U^2)x]/H^2.
```

Let `b0=2WU a1` and `d0=4k^2 h cn(v)d_v V a2`. Multiplying (B) by `dn(u)H^2` leaves only the polynomial identity

```
(1-k^2 t x)[U^2+k^2 V(V+2U)x]
 = a0 H^2 + b0(1-k^2 x)H
   + d0(1-k^2 x)[U^2+(k^2 V^2-2U^2)x].            (C)
```

`telescoping_certificate.py` verifies the generic identity exactly, its coefficient reduction to `Lambda`, the addition denominator factorization, and the derivative conversion. No numerical sampling is used in that certificate.

Now sum (B) over `u+j delta`, `j=0,...,m-1`. Because `F` and `F'` have real period `2K` and `m delta=2K tau`, each shifted `F` sum equals the unshifted sum and the derivative difference sums to zero. Therefore

```
R(u)=sum(j=0,...,m-1) B(u+j delta)
    =2C Lambda sum(j=0,...,m-1) F(u+j delta)
    =(2C Lambda/kp) S(u+K),                       (D)
```

where `dn(u+K)=kp/dn(u)` follows immediately by putting the second argument equal to `K` in the addition formula. In the submitted notation, this explicitly gives `C_R=2C Lambda/kp`.

## 3. Real nonvanishing and the four-periodic case

For `0<v<K`, one has `0<t<1`, `h,cn(v),d_v>0`, `kp>0`, `U>0`, `W>0`, `U-V=2t kp^2>0`, and `U^2-k^2 V^2=kp^2W^2>0`. All coefficient denominators in (B) are nonzero. For real `u`, `dn(u)>=kp`, `D>=1-k^2t>0`, `1+k sn(u)>=1-k>0`, and `U>|kV|`. Consequently the original inversions and the displayed identities have no real singularity. This does not assert a uniform condition bound as `k->1` or `v->0`.

There is no division by `V` in `a0,a1,a2`. At `V=0`, `delta=K` and primitive closure forces `N=4,tau=1`. The generic coefficient `b0` becomes `t`, `d0=0`, and `a0=q/U^2`. The shift difference `F(u+K)-F(u-K)` and its derivative vanish identically, so (B) remains valid with the finite coefficient `a2=-t/(4h cn(v)d_v U)`. Formula (A) reduces directly to

```
B(u)=2C/U^2 [q/dn(u)+t dn(u)].
```

Thus the direct telescoping route covers the exception without a separate limiting argument. The axial orbit has ordinary area `2ab` and focal inverse area `2/(ab)`, so its product is `4`.

## 4. An independent Fourier proof of the cyclic half-shift product

Coprimality gives `gcd(tau,m)=1`; the phases `j delta` modulo `2K` are a permutation of `2Kj/m`. Hence `S` is the uniform real-grid sum, with period `ell=2K/m`.

Write the elliptic nome as `q_e=exp(-pi K'/K)`, to distinguish it from `q=cn(v)^2`. The standard absolutely convergent Fourier expansion of `dn` for real arguments is DLMF 22.11.3. Summing it on the uniform grid removes every Fourier mode whose index is not a multiple of `m`. Let `kappa` be the real modulus with nome `q_e^m`, let `K_m=K(kappa)`, and put `lambda=m K_m/K`. Comparing the surviving coefficients with the same expansion at modulus `kappa` gives exactly

```
S(w)=lambda dn(lambda w,kappa).
```

There is no interchange of two infinite sums: the grid has finitely many terms, and the one Fourier series converges absolutely on the real line. The half-grid shift maps `w` to an argument displacement `lambda ell/2=K_m`. The quarter-shift identity therefore yields

```
S(w) S(w+ell/2)=lambda^2 sqrt(1-kappa^2)>0.         (E)
```

The existence and parametrization of `kappa` may equivalently be read directly from DLMF 22.2.2: `kappa=theta_2(0,q_e^m)^2/theta_3(0,q_e^m)^2`, `K_m=pi theta_3(0,q_e^m)^2/2`, and its complementary modulus is `theta_4^2/theta_3^2`. The constant in (E) is also `(m pi/(2K))^2 theta_3(0,q_e^m)^2 theta_4(0,q_e^m)^2`.

This supplies the target cyclic identity from Fourier filtering and a standard quarter shift, independently of compact-torus pole arguments. No novelty is asserted for this classical multiplication mechanism.

## 5. Completion, period and boundary controls

The inverse polygon area is `A_+^dagger(w)=R(w+v)`. Combining (D) with the shoelace identity gives

```
A(w) A_+^dagger(w)
 =2C_A (2C Lambda/kp) S(w)S(w+K+v).
```

For `N=4n`, `m` is even and `tau` odd, so `(K+v)/ell=(m+tau)/2` is a half-integer. Equation (E) proves constancy. It also gives an explicit value:

```
A A_+^dagger = (4C_A C Lambda/kp) lambda^2 sqrt(1-kappa^2).
```

Central negation is an ordered cyclic shift by `m` vertices. Focal inversion about `-c` is the central negative of inversion about `+c` of those shifted vertices, so the two signed inverse areas agree. Reversing the vertex order changes both signed areas' signs and preserves their product.

The real Jacobi parametrization is injective modulo `4K` because its amplitude is strictly increasing and `(sn,cn)` determines that amplitude modulo `2pi`. Thus the least return is the smallest `r>0` with `r tau/N` integral; it is exactly `N/gcd(N,tau)`. This is the reason a repeated period-six orbit labeled period twelve must not be used as a target case.

Physical similarity by a positive factor `s` multiplies the ordinary area by `s^2` and the unit focal inverse area by `s^-2`, so normalization `alpha=1` in the diagnostic code loses no product information. At the circular endpoint the focus is the center: the explicit product is `(N sin(2pi tau/N)/2)^2` for a regular star. The endpoint `k=1` and zero caustic minor axis remain outside this theorem; the proof does not infer a degenerate extension by numerical continuity.

## Primary mathematical inputs and verification

- Stachel, *On the motion of billiards in ellipses*, Theorem 4.3 and Eq. (4.9): https://doi.org/10.1007/s40879-021-00524-2 . Only the canonical-coordinate and closure formulas are imported.
- DLMF 22.8, Jacobi addition: https://dlmf.nist.gov/22.8 . Differentiation and quarter shifts also follow from those formulas.
- DLMF 22.11.3, the `dn` Fourier expansion: https://dlmf.nist.gov/22.11.E3 . Used as the input to the independently derived finite-grid Fourier filtering argument.
- DLMF 22.2.1–3, nome and theta normalization: https://dlmf.nist.gov/22.2 .

Run `algebra_check.py`, `telescoping_certificate.py`, `euclidean_check.py`, `meromorphic_check.py`, and `telescoping_numeric.py` with the installed `/opt/homebrew/bin/python3.11`. The exact certificates establish the rational reductions; the high-precision programs are independent diagnostics, not interval certificates. This derivation has not yet received a fresh independent adversarial review. No broad priority or novelty search has been performed.
