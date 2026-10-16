# Independent reconstruction of the odd origin area product

This document checks PR254 at immutable head `73efd1fb8ba2d3039ed6692b3ad1dfa1e3085755`. The conclusion is mathematical validity in the stated strict elliptical-caustic, primitive odd-period, signed-area domain. Historical priority is a separate gate. No fresh sibling review was read while reaching this conclusion.

## Claim, assumptions and a route to falsification

For an ellipse with center zero and a strictly nested nondegenerate confocal elliptical caustic, let the least billiard period be odd `N >= 3`. Both simple and coprime primitive star traversals are included. The pedal polygon consists of perpendicular feet from zero to the **original orbit side lines**. The antipedal polygon consists of intersections of consecutive lines `P_i dot X = P_i dot P_i`, with `P_i` the original orbit vertices. The claim is that the product of their ordered signed shoelace areas is independent of the phase. Neither derived area is divided out. Circular outer billiards are covered separately. Hyperbolic and collapsed caustics, nonprimitive padded parity, and unsigned region area are excluded.

Potential failures would include: wrong support lines, an incorrect support-line area identity, an unlisted complex determinant zero, a multiple determinant zero at an excluded endpoint, two simultaneous pole vertices, an uncancelled double pole, a third quotient pole, nonprimitive star arithmetic, a trace with cancelled residues, or a trace zero divisor insufficient to cancel the product poles. Each is checked below without assuming the desired invariant.

## Canonical input and complete chord divisor

Scale the caustic major semiaxis to one when convenient; retain `alpha` in the algebra to check dimensions. For a noncircular billiard, put `k' = beta/alpha`, `k^2 = 1-k'^2`, with `0<k<1`. Let `K,K'` be complete elliptic integrals, `p=iK'`, and

```
v = 2K tau/N, delta=2v, 0<tau<N/2, gcd(N,tau)=1,
a = alpha dn(v)/cn(v), b=beta/cn(v),
P(w)=(-a sn(w), b cn(w)).
```

The canonical orbit is `P(w+j delta)`. It closes because `N delta=4K tau`; least period and winding are explicit hypotheses. This is the classical Stachel canonical coordinate input, not an assumption of the area identity. From `cn²v=1-sn²v` and `dn²v=1-k²sn²v`, one gets `a²-b²=alpha²k²`. All of `s=sn v`, `c=cn v`, `d=dn v` are strictly positive.

Independent expansion of the Jacobi addition formulas gives

```
B(u)=det(P(u-v),P(u+v))
    = 2ab s c dn(u)/(1-k²s²sn²u).
```

The fresh exact checker reduces the full numerator using the four Jacobi quadratic relations, rather than substituting a sampled modulus. For real `u`, `dn(u)>0` and the denominator is at least `1-k²s²>0`. This proves every real consecutive determinant is positive. In particular the real antipedal intersections are unique and finite for every phase and star winding.

To enumerate the complex divisor, use the standard shift formulas from [DLMF Table 22.4.3](https://dlmf.nist.gov/22.4#T3):

```
sn(p+z)=1/(k sn z),
cn(p+z)=-i dn z/(k sn z),
dn(p+z)=-i cn z/sn z.
```

Thus the chord determinant in a chart around a common Jacobi pole is exactly

```
B(p+z)=-2iab s c cn(z) sn(z)/(sn²z-s²).              (A)
```

At `z=0`, it has a **simple zero**, not a pole:

```
B(p+z)=(2iab c/s) z + O(z³).
```

Both endpoints `P(p±v)` are finite and opposite, because `P(p-z)=-P(p+z)`. The coefficient is nonzero.

The equation `1-k²s²sn²u=0` is `sn²u=1/(k²s²)`. On the torus with periods `2K,2p`, the elliptic function `sn²` has a single double pole and hence degree two. The two distinct solutions `u=p±v` exhaust the roots; `2v` is strictly between zero and `2K`. Direct differentiation gives

```
D'(p+v)= 2cd/s, D'(p-v)=-2cd/s,
Res_(p±v) B = -iab s c/d.
```

Their denominators and residues are nonzero. Exactly one endpoint is a simple pole there. There is no hidden cancellation, multiple root, or simultaneous pole endpoint.

The remaining zero class is `r=K+p`, a simple zero of `dn`. The denominator is `c²`, while `dn'(r)=ik'`, so

```
B(r+z)=(2iab s k'/c) z+O(z²).
```

Here the endpoints are finite and coincide. Indeed `P(2r-z)=P(z)`, using the real/imaginary shift characters and ordinary parity. No other `dn` zeros or Jacobi common poles occur modulo the stated real and imaginary congruences. This is the complete list of singularity types needed for the rational antipedal function: endpoint poles, finite coincidence zeros, and finite opposition zeros.

The period rectangle `2K by 2p` classifies this divisor support; `B` itself changes sign under `2p`. The area functions are put on their genuine compact torus below. The argument does not falsely treat an antiperiod as a period.

## The support-line area formula is exact for the named polygon

Write `H(P)=P dot P`, with a bilinear complex dot product. For consecutive original vertices `P,Q`, define

```
F(P,Q) = [H(P)H(Q) - (H(P)+H(Q))(P dot Q)/2]/det(P,Q).
```

Let `R_prev` be the intersection of the lines for a previous vertex `R` and `P`, and `R_next` the intersection of those for `P,Q`. Set `J(x,y)=(-y,x)`. Solving the two line equations gives

```
R_next=P + [(H(Q)-P dot Q)/det(P,Q)] JP,
R_prev=P - [(H(R)-R dot P)/det(R,P)] JP.
```

Both line equations can be verified directly, without normalizing `P` by a complex square root. The single-vertex shoelace contribution is

```
det(R_prev,R_next)/2
  = H(P)/2 { (H(Q)-P dot Q)/det(P,Q)
             +(H(R)-R dot P)/det(R,P) }.
```

On cyclic summation, each original edge receives its two endpoint contributions; their sum is precisely `F(P,Q)`. Therefore the **actual** signed antipedal area is `U(w)=sum_j F(P_j,P_(j+1))`. This is a rational identity, valid for any finite polygon with nonparallel consecutive vertex vectors, so it also identifies the meromorphic continuation. No convexity, positive area, or original polygon area division was used. The fresh checker verifies the one-vertex identity and the edge assembly in six generic coordinate variables.

Simultaneous negation preserves `F`; swapping the arguments negates it; a simultaneous Euclidean reflection negates it. Consequently `U` has period `2K`, period `delta` by cyclic permutation, and antiperiod `2p` (the latter sends `P` to its reflection across the x-axis).

## Why the antipedal has only simple poles

There are exactly three local cases; there is no inference from the desired final invariant.

At finite coincident endpoints, the numerator has the identity

```
H(P)H(Q) - (H(P)+H(Q))(P dot Q)/2
 = [(H(P)+H(Q))H(P-Q)-(H(P)-H(Q))²]/4.
```

Since `P-Q=O(z)`, it vanishes to order at least two, while the complete chord divisor shows a simple zero in the denominator. The edge expression is removable. An isotropic complex vector with `H(P)=0` does not invalidate this factorization.

At finite opposite endpoints, the numerator is finite and the determinant has a simple zero. Thus this is at most a simple pole. It cannot be discarded as a removable coincidence. For the midpoint `u=p`, the two squared norms are in fact

```
H(P(p±v))=alpha²d²/(c²s²),
```

a nonzero value; the numerator at exact opposition is twice the square of this norm. This confirms the opposition pole is ordinarily genuine.

At a pole vertex `P(p+z)`, only its two incident edges require a double-pole check. The vertex is odd in `z`, and has leading vector

```
P(p+z)=R/z+O(z), R=(-a/k,-ib/k), H(R)=alpha².
```

Its neighboring vertices are regular: neither `delta` nor `-delta` is zero modulo `2K`. Each incident edge has denominator of order minus one and numerator of order at least minus three, so it has order at most two. An independent leading-coefficient check shows that the outgoing edge really has the possible double term

```
F(P(p+z),P(p+delta+z)) = C2/z²+O(1/z),
C2=-(a²-b²)(a²-b²dn(delta))
       /[2iab k²(dn(delta)-1)].
```

For the strict real family `dn(delta)<1`, so this denominator is nonzero. Cancellation must therefore occur in the cyclic sum, rather than being assumed term by term.

Define the outgoing term as `G(z)`. The incoming neighbor satisfies `P(p-delta+z)=-P(p+delta-z)` and `P(p+z)=-P(p-z)`. Antisymmetry and simultaneous negation then give the incoming term **exactly** as `-G(-z)`. Thus their sum is `G(z)-G(-z)`, which removes its even Laurent powers and leaves order at most one. This is an analytic identity, not an observation at sampled points.

For odd `N`, a vertex-pole phase has only one pole vertex modulo `2K`. Indeed `gcd(2tau,N)=1`, so `j delta=0 mod 2K` forces `j=0 mod N`. The finite opposite-endpoint edge may occur at the same phase, but has only its already allowed simple pole. No third singularity type remains.

## The small case N=3 does not break the cancellation

At `w=p`, the pole vertex is index zero. Solving the opposition-midpoint equation

```
v+j delta = 0 mod 2K
```

is equivalent to `1+2j=0 mod N`, since `tau` is invertible modulo `N`. Its unique solution in `0,...,N-1` is `j=(N-1)/2`. For `N=3`, this is the edge from index one to index two, exactly the two finite neighbors of the pole vertex. The two incident edges (indices zero and two) still form `G(z)-G(-z)`; the remaining edge is opposite-endpoint type with at most a simple pole. There is no edge with two pole endpoints and no double opposition zero. The zero midpoint class `r-v` equals `p+ell/2` modulo `ell` even in this smallest case, so it is regular for `U` and a pole phase for the other factor, as required below.

## The genuine quotient torus and its trace

Let `ell=2K/N`. The subgroup generated by `delta` modulo `2K` is exactly the subgroup generated by `ell`, because `delta/ell=2tau` is a unit modulo odd `N`. Bezout's identity also shows that any function with periods `2K,delta` has period `ell`. Use the actual compact torus

```
X=C/(ell Z+4p Z).
```

The trace `S(w)=sum_j dn(w+j delta)` has period `ell`, is even by `j -> -j` reindexing, and has antiperiod `2p`. On `X`, there are exactly two simple poles, at `p` and `3p`. At `p`, only index zero contributes before quotienting; the DLMF p-shift gives residue `-i`. It therefore cannot cancel. The second residue is `+i` by the antiperiod. This avoids the even-period double-contributor ambiguity.

Evenness, the real period and the antiperiod force zeros at `p+ell/2` and `3p+ell/2`: negation followed by `ell+2p` fixes the first argument but negates the function. Both are regular points, and they are distinct on `X`. A nonzero meromorphic function on a compact torus has equal total zero and pole orders. Since the pole order total is two, these exhaust the zero divisor and each zero is simple. Hence `S(w) S(w+ell/2)` has no poles anywhere. It is holomorphic on `X` and is constant. On the real axis both traces are positive, so the constant is nonzero.

There is also a genuine one-dimensional uniqueness statement. Any meromorphic function on `X` with only possible simple poles at `p,3p`, and with antiperiod `2p`, is a scalar multiple of `S`. Match the first residue and the antiperiod matches the second. The difference is holomorphic, hence constant, and its antiperiod forces that constant to zero. Removable poles and the zero function are included.

The finite opposition midpoint classes of `U` are `p-v-j delta`; since `v=tau ell`, all reduce to the already present vertex class `p`. Thus the complete preceding pole audit puts `U` in this one-dimensional space:

```
U(w)=c_* S(w).
```

Reality on real phases gives `c_*` real. Possible zero `c_*` does not obstruct the product theorem.

## The original-side pedal and the quarter shift

The canonical chord is the tangent line

```
n(u) dot X=1, n(u)=(-sn u/alpha, cn u/beta).
```

Independent substitution of **both original endpoints** verifies this equation. Its origin foot is

```
Q(u)=n(u)/(n(u) dot n(u))
    =(-alpha k'^2 sn u/dn²u, beta cn u/dn²u).
```

This is the original side foot, not a construction from an outer polygon. On the real axis its denominator is positive. Its cyclic area is `T(u)=sum det(Q_j,Q_(j+1))/2`; the actual original-orbit pedal area is `T(w+v)`.

At the common Jacobi poles `Q` vanishes and is regular. Its only possible poles are the simple zeros of `dn`, so its coordinate pole order is at most two. A fresh quarter-period chart, using `r=K+p`, is

```
Q(r+z)= cn z/[k sn²z] * (alpha dn z, i beta/k').       (B)
```

In particular it is an even function of `z`, with a double leading pole and no simple coordinate Laurent term. Its neighboring vertices are regular because `delta` is not zero modulo `2K`. The two incident shoelace terms combine as

```
det(Q(r+z),Q(r+delta+z)-Q(r-delta+z))/2.
```

By evenness around `r`, the neighboring difference is odd and of order at least one. Multiplying it by the order-two pole vector yields order at most one. This is the same local cancellation mechanism but at a different pole class; the checker independently verifies chart (B).

The transformations are `Q(u+2K)=-Q(u)` and `Q(u+2p)=diag(1,-1)Q(u)`. Therefore `T` has the same real quotient periods and imaginary antiperiod as `U`. Its only possible simple poles on `X` are `r,r+2p`. The shifted trace `S(u+K)` has exactly these pole classes. The residue-matching argument yields

```
T(u)=c_p S(u+K)
```

with real `c_p`, again permitting the zero case. This completes the pedal argument self-contained, while retaining its credit to the earlier campaign pedal mechanism. It does not import an unproved previous area invariant.

## Product, dimensions, reversal and boundary cases

The original pedal and antipedal product is

```
c_p c_* S(w+v+K) S(w).
```

Since `(v+K)/ell=tau+N/2` is a half-integer for odd `N`, this equals the constant half-period product above. Each coefficient has units of area, so the final invariant has units of length to the fourth power. Scaling the entire ellipse multiplies both areas by the square of the scale; reversal negates each signed area and preserves their product. No result is obtained by dividing by a possibly zero area or by an original shoelace area.

For a circle of radius `R`, primitive winding gives a regular star step `theta=2pi tau/N` with `0<theta<pi`. The original-side feet have radius `R cos(theta/2)` and the antipedal intersections radius `R/cos(theta/2)`. Both carry the same signed step `theta`, and the signed shoelace product is `(N²R⁴/4) sin²theta`. This directly treats the circular case; no torus with degenerate modulus is asserted.

Strict nesting excludes `v=0,K` and `k=1`, precisely where the nonzero local coefficients and regular-neighbor checks could otherwise fail. Arbitrarily close interior limits remain covered pointwise by the proof. The given exact four-periodic negative control is consistent: changing to even period prevents the opposition-midpoint classes from necessarily joining the vertex class. Thus no all-parity extension follows from the uniqueness argument.

## Verification limits

The fresh symbolic script verifies generic algebraic identities and local leading coefficients exactly, and checks finite primitive odd lattice families. The latter do not replace the Bezout and modular arguments above. The separate 220-digit script compares actual support-line intersections and original side feet with the meromorphic expressions at real, generic complex and very near singular phases; those diagnostics are not interval certificates. The universal conclusion comes from the complete divisor audit, exact local symmetries and compact-torus argument.

The mathematical route is unblocked. There is no central unsupported claim to which the area invariant has been transferred. Priority, submission wording and packaging remain for the parent workflow.
