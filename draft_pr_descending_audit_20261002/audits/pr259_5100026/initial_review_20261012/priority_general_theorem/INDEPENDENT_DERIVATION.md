# A checked bridge from the outer focal antipedal mean to classical cyclic identities

This derivation was obtained independently during the general-theorem priority audit on 12 October 2026, before sibling/current-candidate comparison. It uses the authenticated submitted theorem and parametrization as target context. It is a new derivation here, not evidence of prior recognition of k407. All coordinates use the submitted normalization: caustic semiaxes 1 and k′=sqrt(1−k²), with 0<k<1.

## 1. A Euclidean paired-chord identity

Let an original ellipse have semiaxes a>b>0 and focus M=(k,0), k²=a²−b². Let X,Y be two consecutive vertices of its actual outer polygon, so their joining line is a tangent to the original ellipse. Let their opposite vertices be −X,−Y. Write that tangent as n·Z=h, with n=(x,y) a unit normal and t=(−y,x). Write X=hn+rt, Y=hn+st, and M=mn+pt. Then

```
h²=a²x²+b²y², m=kx, p=−ky, h²−m²=b².
```

Let I_M(X,Y) be the intersection of the full lines through X and Y perpendicular to X−M and Y−M. Direct subtraction of the two equations gives its normal/tangent coordinates

```
I_M(X,Y) = [h−(r−p)(s−p)/(h−m)]n + (r+s−p)t.
```

The opposite chord has coordinates −h,−r,−s, hence

```
V := (I_M(X,Y)+I_M(−X,−Y))/2
   = [hp(r+s)−m(rs+p²)]/(h²−m²) n − pt.                 (G1)
```

This is an arithmetic pairing, with no area weight or area denominator. It is not the weighted circumcenter-of-mass identity. Indeed individually I_M(X,Y)=2 Circumcenter(M,X,Y)−M, but averaging these fan circumcenters uniformly differs from area-weighted CCM.

Suppose X,Y lie on the fixed concentric outer-vertex ellipse x_coord²/A²+y_coord²/B²=1. Its intersections with n·Z=h have tangent coordinates r,s. Put

```
D = y²/A²+x²/B²,
r+s = −2hxy(1/B²−1/A²)/D,
rs = [h²(x²/A²+y²/B²)−1]/D.
```

Substitution into (G1), using x²+y²=1 and h²−m²=b², yields

```
V = −M + α (n·M)n/[A²x²+B²y²],
α = (A²B²+A²b²−B²a²)/b².                              (G2)
```

All three steps are rational identities checked by `verify_reduction.py`.

## 2. Match the actual billiard and outer locus

Let K=K(k), v=2Kτ/N, δ=2v, 0<τ<N/2, gcd(N,τ)=1, and N even. Stachel, published Theorem 4.3 and (4.9), printed p.1614, gives

```
s=sn(v), c=cn(v), d=dn(v),
a=d/c, b=k′/c,
P(u)=(-a sn(u),b cn(u)), P_i=P(u+iδ).
```

The actual intersection of the two original tangents at P(u−v),P(u+v) is

```
R(u)=(-A sn(u),B cn(u)), A=ad/c=a², B=b/c.
```

This tangent-intersection formula is derived in the authenticated submitted proof; substitution of Jacobi addition formulas into both tangent equations independently checks it. Consecutive outer vertices R(u−v),R(u+v) lie on the original tangent at P(u). Its unnormalized normal is n₀=(−S/a,C/b), where S=sn(u), C=cn(u). Since A/a=d/c and B/b=1/c, both coordinate semiaxes of the outer locus exceed the corresponding original ones; every original tangent cuts that outer ellipse in two distinct real points. Moreover h>|m| by h²−m²=b²>0, so the two real antipedal normals have determinant (h−m)(s−r)≠0 in these axes. This supplies finiteness and uniqueness directly, for every real phase and star.

Since N is even and τ is odd, R(u+Nδ/2)=−R(u). Thus summing (G2) over all i gives exactly the target mean: no odd-orbit repetition is admitted by this pairing argument.

Set

```
D₀(u)=1−k²s²S²,
H₀=1−2k²s²+k²s⁴.
```

Then (G2) becomes

```
V_x(u)=k[-1+(H₀/c²) S²/D₀(u)],
V_y(u)=−k[a H₀/(b c²)] SC/D₀(u).                       (G3)
```

All real denominators here are positive: c>0, D₀≥1−k²s²>0 and 1−k²s⁴>0. No complex pole classification is needed for this real reduction.

## 3. The exact prior cyclic identity matches

Elementary Jacobi addition gives

```
sn(u−v)sn(u+v)=(S²−s²)/D₀(u),
S²/D₀(u)=[sn(u−v)sn(u+v)+s²]/(1−k²s⁴),                (G4)
SC/D₀(u)=[dn(u−v)−dn(u+v)]/(2k²sc).                    (G5)
```

Equation (G5) telescopes in the full cyclic sum because adjacent arguments differ by δ=2v, and dn(u+Nδ)=dn(u+4Kτ)=dn(u).

The remaining summand is **exactly** the rank-two cyclic sn-product trace proved in Khare–Lakshminarayan–Sukhatme, *Cyclic Identities Involving Jacobi Elliptic Functions. II*, arXiv:math-ph/0207019v2 (24 March 2003), PDF p.3, equation (5). Their parameter m is k², not k. Their nearest-neighbor step is 2K/p. Our step is δ=2Kτ/p with p=N/2. The product has period 2K, and gcd(τ,p)=1 permutes the sample grid. General neighbor shifts are explicitly discussed on pp.3–4. To cover all star directions and p=2 without relying on the appendix's coefficient typo, use the standard local zeta addition stated in *Local Identities Involving Jacobi Elliptic Functions*, arXiv:math-ph/0306028v1 (10 June 2003), PDF p.5, equation (12):

```
Z(z+δ)=Z(z)+Z(δ)−k² sn(z)sn(δ)sn(z+δ).
```

Here Z is the argument-form Jacobi zeta function; DLMF 22.16.32 defines it, 22.16.27 and the paragraph after 22.16.32 give its addition, and 22.16.34 gives Z(z+2K)=Z(z). Since 0<δ<2K, sn(δ)>0. Sum the rearranged identity over z_i=u−v+iδ. Because Nδ=4Kτ,

```
(1/N) Σ_i sn(z_i)sn(z_i+δ)=Z(δ)/[k²sn(δ)].              (G6)
```

This is a proved prior analytic identity whose precise summand and assumptions have been matched. It is stronger evidence than merely observing that a trace has vanishing poles. The new work in this audit is the explicit geometric bridge (G1)–(G4). Prior analytic tools alone would not justify asserting that k407 had already been recognized.

## 4. Explicit value and boundary checks

Combining (G3)–(G6) yields

```
C_x = k[-1 + H₀/(c²(1−k²s⁴)) · (s² + Z(2v)/(k²sn(2v)))],
C_y = 0.                                               (G7)
```

For the negative original focus the result negates by central symmetry. Thus the constant lies on the original focal axis. Reversal replaces τ by a reversed orientation and preserves the arithmetic mean. Repetition of an even least-period orbit only repeats its terms.

For N=4, τ=1, v=K/2, put q=k′. Then s²=1/(1+q), c²=q/(1+q), H₀/c²=2q, Z(2v)=Z(K)=0, and s²/(1−k²s⁴)=1/(2q). Equation (G7) gives C=0 exactly. The same real positive denominators apply, so N=4 needs no complex limiting argument.

The circular model k=0 is handled separately by antipodal symmetry; (G7) has explicit k² denominators and is not asserted as a numerically stable circular-limit representation. Strict nondegenerate elliptical caustics are assumed throughout. Hyperbolic and degenerate caustics are not covered. An even listed traversal of an odd least-period orbit lacks the opposite-vertex pairing; nothing in this derivation proves that false extension.

## 5. Validation and source caution

The independent checker verifies 13 symbolic identities and 552 actual tangent/antipedal cases at 90 decimal digits, over N=4,6,8,10,12,14,18,22,30, all coprime turning numbers tested, both original foci, three phases and k=0.1,0.6,0.95,0.999. Maximum observed error: 6.770621707e−87. These numerical checks are diagnostics, not interval certification; the identities above supply the all-period argument.

The cyclic paper's Appendix A equation (113), PDF p.22, prints `cs(a) Z` where its main-text equation (5) and direct zeta addition require `ns(a) Z`. This discrepancy is not silently propagated. The proof here relies on the correct main-text trace and the separately pinned local addition formula. No historical-firstness or recognition date is inferred from any deposit or update clock.
