# Independent mechanism recorded before prior evidence

Recorded 2026-10-13T03:55:48.837986+00:00. Prior mathematical audit reports/scripts and acceptance reports have not been opened. The manuscript has been read; the following derivation is my own check route, rather than assuming its asserted identities.

## Exact target and possible falsifiers

For a noncircular ellipse `a>b>0`, strict confocal elliptic caustic `0<lambda<b²`, and primitive even Poncelet period, the ordered full-tangent feet have the stated phase-independent *signed* centroid on precisely the nonzero-area domain. Counterexamples would include an even primitive trajectory lacking antipodal pairing, a star where a consecutive normal crosses a half turn, a missing factor or conjugation in the first moment, a four-period boundary not equivalent to `d=0`, or an exact zero-area point outside the stated circle. Finite orbit tests do not prove this target.

## Topological route

The specified one-sided Poncelet map is an orientation-preserving circle homeomorphism. Central symmetry preserves this chosen tangent side, hence commutes with it. The generated group is finite because the commuting generators have orders `N` and `2`. Every nonidentity finite-order orientation-preserving circle homeomorphism acts without a fixed point: cut at a fixed point and use monotonicity of successive iterates. Consequently evaluation on one group orbit is faithful, and circular order embeds the group into the rotations of a finite cyclically ordered set. In a cyclic group the involution is unique; since `N` is even, `T^(N/2)` and the central symmetry must coincide. This remains valid when the primitive winding is greater than one. The least-period requirement is essential: doubling an odd primitive orbit cannot manufacture central symmetry.

A forward chord tangent to a strictly interior ellipse containing the origin has the origin on its left. Central convexity then puts its second endpoint strictly between the first endpoint and its antipode in boundary order. The Gauss map is increasing and antipode-equivariant, so `0<delta<pi` holds edgewise even for stars. Therefore the origin-pedal area is strictly positive.

## Algebra route

Let unit complex normals be `x,y`, positive supports be `h,k`, and doubled normals be `Z=x²,W=y²`. Tangency gives the real bilinear relation

`h k = D cos(delta)+e cos(psi+phi)` for `d!=0`, `D=F/d`.

This follows directly from the tangent chord equation in eccentric angles and `n=h(cos u/a,sin u/b)`. Square this relation and use `h²=H+e cos(2psi)` to derive the doubled-normal cosine relation. The support identity times `sin(delta)` telescopes its `e` term, giving `S0=D*SZ/2`; it also proves `SZ!=0` without invoking a centroid denominator.

For unit `U,V`, multiplying the cross product gives

`cross(U,V)*(U+V)=-i*(1+dot(U,V))*(V-U)`.

The constant part of the doubled-normal cosine relation telescopes. The remaining sum of `(X_i+X_j)*(Z_j-Z_i)` has zero real part and imaginary part `sum cross(Z_i,Z_j)`, hence `TZ=2v*SZ`. This division-free identity is valid for self intersections and zero signed area.

Projection, derived from `Q=M+(h-M dot n)n`, is `Q=z/2+V`, `V=h n-t n²`, `t=conj(z)/2`. Pairing opposite edges leaves only the terms with an even number of `h n` factors. Thus area has a constant term and a quadratic term; the first moment has linear and cubic terms. I will expand `2i*cross(V_i,V_j)*(V_i+V_j)` directly with formal conjugates `conj(x)=1/x`, `conj(t)=T`, average with the antipodal edge, and only then extract its coefficients. This gives a reproducible coefficient check independently of the printed coefficient reduction. Substituting support squares and products must reduce the linear coefficients to the sums of `r=Z/W-W/Z`, `s=Z²/W-W²/Z`, plus endpoint differences. The global sums are `sum r=-4i SZ`, `sum s=-2i TZ`; the cubic term is `-|t|² t TZ`. Translation contributes `6cS`, which will be checked directly using a general ordered polygon, including a crossing polygon. No division by a potentially zero pedal area is legitimate before the final centroid step.

## Boundary route

`F+ed=a²-lambda(a²/b²-1)>b²>0` and `F-ed=b²+lambda(1-b²/a²)>0` control the parameter denominators. The remaining centroid denominator is exactly signed area, `2F+d|M|²`. For simple winding one and `N>=6`, the first half of the normal polygon spans one half turn, so its squared normals make a distinct convex polygon traversed twice: `SZ>0`, hence `D>0`, `d>0`. For `N=4`, antipodal consecutive support equations force `d=0`; conversely `d=0` forces every normal increment to be `pi/2`, so least period four. Direct rectangle projection gives `S=2AB`, `T=4ABM` even outside the rectangle.

The exact eight-star will be independently checked from its Cartesian vertices: membership, chord tangency to the rational caustic, equal-angle reflection, distinctness, ray-crossing winding and unrestricted `X,Y` shoelace polynomials. This does not replace the all-period derivation.

## Evidence protocol

Now that the mechanism is pinned, archived proofs/scripts and bounded priority reports may be inspected for package coverage and replay. A fresh extractor will check paths and SHA-256, replay in the extraction directory, and verify that archived evidence stays byte-identical. Source/PDF/metadata/deposit consistency and all five PDF pages will be inspected. This review does not seek historical firstness.
