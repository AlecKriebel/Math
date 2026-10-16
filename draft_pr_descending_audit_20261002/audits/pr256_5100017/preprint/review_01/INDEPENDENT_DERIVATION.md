# Completed independent all-period derivation

Fresh preprint adversary 01, completed 2026-10-13 UTC. This derivation uses the mechanism recorded before earlier mathematical evidence was inspected. Formal calculations are independently reproducible in `fresh_exact_checks.py` (73 exact checks). Those calculations certify edge identities, not the unbounded geometric hypotheses; the arguments below supply the latter.

## Pairing, orientation, and admissible denominators

Let `T` be the chosen forward Poncelet map, of order the primitive period `N`, and `A` the central half turn. They commute: applying central symmetry to a tangent chord preserves its forward side of the caustic. Thus their generated group is finite. A finite-order increasing circle homeomorphism fixing a point is identity, by cutting the circle at that point and iterating any alleged strict movement. Evaluation at any point therefore gives a faithful finite circularly ordered orbit; its order-preserving permutation group is cyclic. The unique involution identifies `T^(N/2)=A`. This proof needs primitive even period, not an even written vertex count obtained by repeating an odd orbit.

Each forward chord has the origin strictly on the caustic side, since the strict elliptic caustic contains the origin. For a centrally symmetric strictly convex outer curve this places the second endpoint strictly before the first antipode in boundary order. The increasing, antipode-equivariant Gauss map therefore gives a lifted consecutive normal difference `0<delta<pi`, including primitive stars. In particular

`S0=(1/2) sum h_i h_(i+1) sin(delta_i)>0`.

Let `H=(a²+b²)/2`, `e=(a²-b²)/2`, `d=1-lambda(1/a²+1/b²)`, and `F=Hd+2lambda`. Elementary algebra gives

`F+ed=a²-lambda(a²/b²-1)>b²>0`,

`F-ed=b²+lambda(1-b²/a²)>0`.

Consequently `F>0` and `F²-e²d²>0`. When `d!=0`, `D=F/d` exists and `D²-e²>0`. No division by a signed pedal area has occurred.

The chord through eccentric angles `u,w` has equation `(cos(tau)/a)x+(sin(tau)/b)y=cos(q)`, where `tau=(u+w)/2`, `q=(w-u)/2` and `0<q<pi/2`. Its caustic-dual tangency equation is

`sin²(q)=lambda(cos²(tau)/a²+sin²(tau)/b²)`.

Expanding the double-angle identities, and substituting `n=h(cos u/a,sin u/b)`, gives

`d h k=(F+ed) n_x m_x+(F-ed) n_y m_y`.

Thus, for `d!=0`, `hk=D cos(delta)+e cos(psi+phi)`.

## Doubled normals and a division-free telescope

Put `Z_i=n_i²`, regarded as unit complex numbers. Squaring the support relation and using `h_i²=H+e Re(Z_i)` gives

`(D²-e²) cos²(delta)=H²-e²+e(H-D)(Re Z_i+Re Z_(i+1))`.

Therefore the adjacent doubled-normal dot product is `u+v(Re Z_i+Re Z_(i+1))`, where

`v=2e(H-D)/(D²-e²)=-4e lambda d/(F²-e²d²)`.

For any unit `U,V`, direct multiplication gives

`cross(U,V)(U+V)=-i(1+dot(U,V))(V-U)`.

Summing, the constant term telescopes. For `Z=X+iY`, the sum `(X_i+X_j)(Z_j-Z_i)` has zero real part, while its imaginary part equals `sum cross(Z_i,Z_j)` after removing the endpoint products `X_jY_j-X_iY_i`. It follows that

`T_Z=2v S_Z`.

Neither simplicity nor nonzero area is required for this identity.

Multiplying `hk=D cos(delta)+e cos(psi+phi)` by `sin(delta)`, the `e` term telescopes through `(sin(2phi)-sin(2psi))/2`. Thus

`S0=(D/2) S_Z`.

Since `S0>0`, this establishes `S_Z!=0` for `d!=0`, independently of the centroid computation.

## Full moment expansion

For `z=M_x+iM_y`, orthogonal projection onto `n dot Q=h` gives

`Q=z/2+V`, `V=h n-t n²`, `t=conj(z)/2`.

Opposite indices negate `h n` and preserve `n²`. Pairing cancels the mixed area terms, hence

`S(M)=S0+|t|² S_Z=(D/2+|z|²/4) S_Z`.

For a single edge, write the unit normals as `x,y`, their supports as `h,k`, and put `Z=x²,W=y²`. Expanding the actual moment from projection, using the formal conjugates `conj(x)=1/x`, `conj(y)=1/y`, yields the following antipodal average in `2i` times the edge moment:

- coefficient of `t`: `c=k²x²-h²y²+2hk(x³/y-y³/x)`;
- coefficient of `conj(t)`: `b=h²x²/y²-k²y²/x²+hk(x/y-y/x)`;
- coefficient of `t²conj(t)`: `-(W/Z-Z/W)(Z+W)`.

All other monomials vanish. This extraction was performed from the full projected edge, rather than assuming the printed coefficients.

Now substitute

`h²=H+(e/2)(Z+Z^(-1))`, `k²=H+(e/2)(W+W^(-1))`,

`hk=(D/2)(y/x+x/y)+(e/2)(xy+(xy)^(-1))`.

Direct multiplication gives, with `r=Z/W-W/Z` and `s=Z²/W-W²/Z`,

`c=Ds+(3e/2)r+(D+H)(Z-W)+e(Z²-W²)`,

`b=(D/2+H)r+(e/2)s+(e/2)(Z-W)+e(W^(-1)-Z^(-1))`.

Each last term is an explicit endpoint difference and telescopes in every closed ordered polygon. Also

`sum r=-4i S_Z`,

`s+2i cross(Z,W)(Z+W)=W-Z`, so `sum s=-2i T_Z=-4iv S_Z`.

The cubic coefficient is the negative scaled doubled-normal moment. Dividing the summed coefficient expansion by `2i` gives the complete polynomial identity

`T(V)=-2 S_Z [t(Dv+3e/2+v|t|²)+conj(t)(D/2+H+ev/2)]`.

For completeness the translation formula is also an edge identity with an explicit endpoint witness. For real vectors `p,q,c=(cx,cy)`, let

`Phi(p)=(cx px py-cy px², cx py²-cy px py)+2c cross(c,p)`.

Then

`cross(p+c,q+c)(p+q+2c)-cross(p,q)(p+q)-3c cross(p,q)=Phi(q)-Phi(p)`.

Summing proves `T(P+c)=T(P)+6c S(P)` for arbitrary ordered polygons, including crossing and zero-area polygons. There is no assumption of an unsigned region centroid.

Only when `S(M)!=0` do we divide by `6S(M)` and translate by `z/2`. The result is

`C=z/2-[z(D+2H+ev)+conj(z)(2Dv+3e+v|z|²/2)]/[3(2D+|z|²)]`.

Replacing `D=F/d` gives exactly the printed expression. The final conversion, the formula for `v`, and the area ratio were separately verified symbolically.

## Exact domain and four-period boundary

Since `S0>0` and `F>0`,

`S(M)=S0 (2F+d|M|²)/(2F)`.

Thus there are no zeros for `d>=0`; for `d<0` the entire zero set is precisely the circle `|M|²=-2F/d`. On that circle the signed quotient is undefined even at any possible simultaneous zero of its numerator.

When `N=4`, compare the two consecutive support identities through `n_2=-n_0`, `h_2=h_0`. Their right sides negate and their left sides are both `d h_0h_1`; addition gives `d=0`. Conversely `d=0` forces `cos(delta)=0`, and since `0<delta<pi`, each normal advances `pi/2`, giving least period four. The four feet in the rectangle frame have exact area `2AB` and first moment `4ABM`, for every real `M`, hence `C=M/3`. This also equals the continuous `F,d` formula at `d=0`.

For a simple winding-one even polygon with `N>=6`, the first `N/2` normals occupy one half turn in circular order. Their squares are at least three distinct unit-circle points in circular order. The full doubled-normal polygon traverses that convex polygon twice, so `S_Z>0`, and then `S0=D S_Z/2>0` implies `D>0`, hence `d>0`. This verifies definedness for every fixed point in the simple class.

## Exact physical star control

Using the printed eight rational normalized vertices and positive diagonal Cartesian scaling, the fresh script verifies each ellipse membership, the dual caustic tangency equation, the actual unit-vector specular reflection law, and the origin-left condition. All eight vertices are distinct. The exact half-open positive-x ray count has contributions `[0,0,1,0,1,0,0,1]`, giving winding three. A closed eight-step deterministic billiard orbit with eight distinct impact points has least period eight.

Unrestricted real-symbolic `X,Y` projection and shoelace produce exactly the printed area and both first-moment polynomials, not a sampled restriction. The supplied zero point gives exactly `S=0`, `T_x=221 sqrt(21930)/10368!=0`, `T_y=0`. The caustic semiaxes, `d`, `F`, `v`, and zero-circle radius also agree exactly.

The strongest result of this review is acceptance of the complete all-period proof under the explicit strict elliptic, primitive even, signed-moment hypotheses. The finite numerical controls are corroboration only. No unsupported claim equivalent to the original problem has been substituted into the derivation.
