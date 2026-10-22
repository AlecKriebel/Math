# Independent Cartesian and domain derivation for PR254

This derivation was made from the frozen mathematical claim, direct geometry, and authenticated classical sources, without reading new sibling reviewers' conclusions. Numerical checks are diagnostics; the final universal argument is a separately inspected meromorphic proof.

## 1. Actual constructions and the support-line area formula

Put the ellipse center at zero. For a consecutive pair of original vertices `P,Q`, the original side is the line through them. Write `e=Q-P`, `n=(-e_y,e_x)`, and `h=n·P`. Its actual perpendicular origin foot is

`q=h n/(n·n)`.

The actual origin-antipedal lines are `P·X=P·P` and `Q·X=Q·Q`. Their intersection is obtained by solving that two-by-two linear system, and it is finite exactly when `det(P,Q) != 0`. These are neither caustic-contact antipedals nor outer tangent polygon antipedals. All dot products in the complex continuation are bilinear; no Hermitian norm is introduced.

Let `J(x,y)=(-y,x)`, `H=P·P`, and use `c=det(P,Q)`, `d=P·Q`. Solving the line equations in the basis `(P,JP)` gives the next intersection as `P + ((Q·Q-d)/c) JP`. With previous vertex `R`, the previous intersection is `P - ((R·R-R·P)/det(R,P)) JP`. Therefore its shoelace edge contribution is

`det(X_previous,X_next) = H[(R·R-R·P)/det(R,P) + (Q·Q-P·Q)/det(P,Q)]`.

Summing one half of these contributions groups the two pieces belonging to each original edge into

`F(P,Q) = [H(P)H(Q) - (H(P)+H(Q))(P·Q)/2]/det(P,Q)`.

Thus the submitted formula computes the actual ordered antipedal area, including stars, reversed orientation, and self-crossing derived polygons. The local identity was checked afresh with six independent Cartesian symbols. No convexity or nonzero polygon area is needed. Polarization gives the additional exact numerator identity

`4 numerator(F) = (H(P)+H(Q)) H(P-Q) - (H(P)-H(Q))^2`.

The submitted coincident-endpoint cancellation follows from this identity even when a finite complex endpoint has zero bilinear squared norm.

## 2. Real domain and primitive star geometry

Normalize the caustic semiaxes to `(1,b0)`, with `b0^2=1-k^2`, `0<k<1`. With `v=2K tau/N`, outer semiaxes are `a=dn(v)/cn(v)` and `b=b0/cn(v)`. The real vertex is `P(w)=(-a sn(w),b cn(w))`, and successive vertices are separated by `delta=2v`. The authenticated Stachel Theorem 4.3 covers primitive coprime turning numbers, not merely convex traversals. Reversal permits `0<tau<N/2`; hence `0<v<K` and `0<delta<2K`.

For chord midpoint parameter `u`, direct Jacobi addition gives

`det(P(u-v),P(u+v)) = 2ab sn(v) cn(v) dn(u) / [1-k^2 sn(v)^2 sn(u)^2]`.

Every factor has the stated positive real sign. The denominator is bounded below by `1-k^2 sn(v)^2>0`. Consequently every consecutive original pair has positive determinant and every antipedal intersection is finite. The real side length is nonzero. The chord's caustic line is

`(-sn(u),cn(u)/b0)·X=1`.

Solving its origin projection independently gives

`q(u)=(-b0^2 sn(u)/dn(u)^2, b0 cn(u)/dn(u)^2)`.

The normal is nonzero. Its direction angle increases strictly, since the determinant of the normal and its derivative is `dn(u)/b0>0`, and its direction advances by pi over a real interval of length `2K`. Since `0<delta<2K`, every successive pedal normal turns by an angle strictly between zero and pi, including the closing star edge after using the lifted parameter. The foot is a positive multiple of this normal. Hence each ordered pedal cross product is positive and the positively oriented origin-pedal signed area is strictly positive. This extra observation does not prove or require positivity of the antipedal signed area.

The primitive least period is controlled by `N delta=4K tau` and `gcd(N,tau)=1`. A repeated list has the same geometric least period; it must not be reclassified as a new parity case. Repeating a valid list `r` times scales each signed area by `r` and its product by `r^2`. Reversing it changes both signs and leaves the product unchanged. Translating the ellipse and origin together preserves areas, and scaling lengths by `L` scales the product by `L^4`.

## 3. Independent inspection of the universal analytic completion

The Cartesian formula itself does not imply phase constancy. Here is the required full completion, checked separately rather than inferred from the diagnostics.

For odd `N`, put `ell=2K/N`, `p=iK'`, and `S(w)=sum_j dn(w+j delta)`. Since `delta/ell=2tau` is coprime to `N`, cyclic reindexing makes `S` periodic with `ell`. It has period `4p`, anti-period `2p`, and is even. On the torus with lattice `<ell,4p>`, exactly one summand contributes to each representative vertex pole at `p` and `3p`; their simple residues are nonzero and opposite. No repeated-index cancellation has been assumed. Evenness and the anti-period force zeros at `p+ell/2` and `3p+ell/2`. They are distinct nonpoles. Equality of total pole and zero order implies these are the only zeros and are simple. The translated factor `S(w+ell/2)` therefore cancels exactly the pole divisor of `S(w)`, so their product is holomorphic on the compact torus and constant.

For the antipedal, the midpoint chord determinant has simple poles at `p±v` and simple zeros at `p` and `K+p`, modulo real/imaginary half periods. This classification is complete: the denominator `1-k^2 sn(v)^2 sn(u)^2` has one double pole and the two distinct simple roots `p±v`; `dn` has a pole at `p` and a zero at `K+p`. The quotient gives the listed divisor. Strict `0<v<K` excludes root collision and vanishing of the necessary derivative.

At `u=K+p` the finite endpoints coincide; the polarization identity makes the numerator order at least two, while the chord determinant has a simple zero. The singularity is removable. At `u=p` the finite endpoints are opposite. Here the numerator is merely regular and the denominator has a simple zero: this pole is generally genuine and must be retained. Its phase class is `p-v-j delta`. For odd `N`, `v=tau ell`, so it lies in the same allowed torus classes as the vertex poles. For `N=3` the edge not incident to a pole vertex supplies precisely this separate opposite-endpoint mechanism; it is not omitted by the incident cancellation.

At an actual vertex pole, its two adjacent vertices are regular and a single `F` term has order at most two: `H(P)` has order at most two, `P·Q` order at most one, and the incident denominator a simple pole. The half-period parity identity `P(p-z)=-P(p+z)` makes the two adjacent edge terms exactly `G(z)-G(-z)`. Their double pole cancels, leaving at most a simple pole. Odd coprime order prevents two pole vertices in one edge. The opposite-endpoint term at the same quotient phase was separately bounded above. No other denominator zero or endpoint singularity remains.

The resulting actual antipedal area `U(w)` has period `ell`, anti-period `2p`, and at most the two simple poles of `S`. Matching the first residue and using the anti-period for the second leaves a holomorphic compact-torus remainder. Its anti-period forces the constant remainder to zero. Therefore `U(w)=c_* S(w)`; evaluation on the real axis makes `c_*` real. No step divides by `U` or asserts that `c_*` is nonzero.

For the actual side-pedal area, the coordinate poles of `q` occur only at `r=K+p`, where `dn` has a simple zero; they have order at most two. The common Jacobi poles are removable because the denominator has higher order than the numerator. The point-reflection identity about `r` makes `q(r+z)` even. Its two neighboring values are regular and their difference vanishes to first order, so the two incident area terms have order at most one. The normal half-period reflection changes the area sign for a shift by `2p`; reindexing and the real half period provide `ell`-periodicity. Residue uniqueness now gives `T(u)=c_p S(u+K)`. The actual original side pedal uses midpoint `u=w+v`.

Finally `(v+K)/ell=tau+N/2` is a half integer. The product is consequently `c_p c_* S(w)S(w+ell/2)`, which is constant by the independently established divisor identity. This proves the universal result for every primitive odd period and star in the strict elliptical-caustic domain. No finite enumeration was used to establish universal quantification.

## 4. Circular and signed-area boundaries

For an outer circle of radius `R`, a primitive forward star has step `theta=2pi tau/N` in `(0,pi)`. Solving the actual side and antipedal lines gives respectively the radii `R cos(theta/2)` and `R/cos(theta/2)`, with the same midpoint rotation. Their signed areas are each `N rho^2 sin(theta)/2`. Their product is `N^2 R^4 sin(theta)^2/4`; the cosine is positive, so every intersection is finite. This proves the circular endpoint directly rather than taking a singular elliptic-torus limit.

Reversal gives genuinely negative signed areas but the same product. The theorem allows zero antipedal area and never divides by it. The tested forward families had positive antipedal areas; this observation is not promoted to a universal nonvanishing theorem or a numerical exclusion of isolated zeros. The all-domain argument remains sound regardless of such a zero. Strict caustic, noncollapsed outer ellipse, and primitive least odd period are retained throughout. The limits `k -> 0`, `k -> 1`, `v -> 0`, or `v -> K` are not substituted into the noncircular analytic proof at their degenerate endpoints.

## 5. Exact constructed controls

Two distinct symmetric triangles in the same ellipse `a^2=8,b^2=5` and caustic `alpha^2=32/9,beta^2=5/9` are:

`(0,sqrt(5)),(-8/3,-sqrt(5)/3),(8/3,-sqrt(5)/3)`;

`(2sqrt(2),0),(-4sqrt(2)/3,5/3),(-4sqrt(2)/3,-5/3)`.

Every outer membership, side tangency, contact's strict segment location, reflection law and forward direction, distinctness, actual foot and antipedal intersection, reversal, and repetition is verified exactly. The gap is `lambda=40/9`, strictly between zero and `b^2`. Their origin-pedal areas are `70sqrt(5)/81` and `112sqrt(2)/81`, and antipedal areas are `98sqrt(5)/5` and `245sqrt(2)/8`. Both products are exactly `6860/81`. These two samples corroborate the universal proof; they do not replace it.

For the excluded primitive four-periodic family `a^2=5,b^2=3`, caustic squared axes `25/8,9/8`, the axis diamond and the rectangle of vertices `(±sqrt(25/8),±sqrt(9/8))` are both exactly reflected, strict-caustic trajectories. All intersections are finite and areas positive. Their products are respectively `225/4` and `289/4`. Therefore dropping the odd restriction would produce a false statement. The actual differing midpoint-pole classes explain why the submitted proof retains that restriction.
