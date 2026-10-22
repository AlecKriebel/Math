# Attempt 3: exact discontinuous reduction to slopes, jumps, and spikes

Date: 20 October 2026. Candidate full reduction, subsequently audited and tested in Attempts 4–5.

## Do not assume continuity

Fix any grid size N divisible by every input breakpoint denominator and the denominator of f. Ultimately N=4q. A periodic piecewise-linear function h on that grid has, at t_k=k/N,

- slope s_i on (i/N,(i+1)/N);
- jump J_k=h(t_k+)−h(t_k−);
- spike P_k=h(t_k)−(h(t_k+)+h(t_k−))/2.

The point value is independent of both one-sided limits. These variables include every N-grid PL perturbation, even when the input is discontinuous from both sides at zero.

Set h(0)=0. Then h(0−)=−J_0/2−P_0 and h(0+)=J_0/2−P_0. For 0<k<N,

h(t_k−)=h(0+)+(1/N)sum_{i<k}s_i+sum_{1≤j<k}J_j,
h(t_k)=h(t_k−)+J_k/2+P_k,
h(t_k+)=h(t_k−)+J_k.

The periodic compatibility equation is

(1/N)sum_i s_i+sum_k J_k=0.

Thus slope/jump/spike variables and this one equation parameterize the entire normalized finite-dimensional space.

## Sparse coarse arrangement

Use the original sparse breakpoints, including f, to form the arrangement of vertical, horizontal, and diagonal lines. On each face F, the input slack Delta pi_F is affine and nonnegative. Its zero set is empty, a vertex, an edge, or all of F. Record the incident face F, not merely the zero set, because discontinuous input has different limiting slacks from different faces.

The complete refined tight system is equivalent to the following constraints.

### A. A fully zero two-dimensional face

The interval lemma forces h to be affine with one common slope on the interiors of the three projection intervals. Encode this by:

1. Identifying all slope cells within each projection and across the three projections.
2. Setting J_k=P_k=0 at all grid points strictly inside each projection.
3. Retaining the endpoint sector equations described below.

Conversely these constraints make Delta h constant across the open face; one appropriate endpoint limit equation sets the constant to zero. All boundary sectors are retained as well.

### B. A fully zero one-dimensional coarse face

For a horizontal or vertical edge, the identity is h(x+t)=h(x)+h(t). On the open variable interval, impose equality of paired slopes, equality of paired jumps, and equality of paired spikes.

For a diagonal edge, the identity is h(x)+h(t−x)=h(t). Paired slopes and jumps are again equal, but paired spikes are negatives. The reflected cell index is i -> Nt−i−1; the reflected point index is k -> Nt−k. Confusing these two index formulas is an off-by-one error.

Use point pairings only for grid points strictly inside the variable projection interval. Endpoint relations remain in the finite residual system.

The converse is exact: paired slopes make the edge expression constant within every elementary segment; paired jumps make these constants agree across grid points; paired spikes make the actual value at each grid point equal that same constant. One endpoint equation then sets it to zero.

### C. A zero boundary edge of a two-dimensional coarse face

Here the relevant relation is a limiting relation from the specified incident face, not necessarily an actual additive edge. Impose paired slope equality and force J=P=0 on the interiors of BOTH nonfixed projection intervals.

Why the forced regularity is necessary: consider a vertical boundary x=t with the incident face on x>t. At an interior grid point y=k/N and z=t+k/N, let A=h(t+). Feasible approaches from the open face give

A+Y−−Z−=0,
A+Y+−Z+=0,
A+Y−−Z+=0.

The third approach uses x−t>0 and y−k/N<0 of different relative magnitudes. These equations force both jumps to vanish. Paths with y=k/N exactly and with x+y=z exactly are also inside the incident open face near the limiting point. Their equations force Y0=Y+=Y− and Z0=Z+=Z−. Thus both spikes vanish too. The case x<t reverses the signs. Horizontal edges exchange x,y. For a diagonal boundary x+y=t approached from x+y>t, let A=h(t+). Feasible sign pairs (++), (+−), and (−+) give X++Y+−A=0, X++Y−−A=0, and X−+Y+−A=0, forcing both variable jumps to vanish. The rays with x or y exactly fixed force their point values to equal those limits. Approaching from x+y<t reverses the signs. Thus the diagonal case also forces both spikes to vanish, without presupposing continuity.

Conversely regularity on both variable projections and paired slopes make the limiting edge expression constant; the endpoint sector equations set this constant to zero.

### D. Zero vertices and all endpoint sectors

For each coarse face F and every vertex v of F with Delta pi_F(v)=0, include the limit equation for every feasible local direction from v into relint(F). The three states needed at v_x, v_y, v_x+v_y are determined by the signs of d_x,d_y,d_x+d_y.

A complete fixed list of representatives is

(0,0), (1,0), (0,1), (−1,0), (0,−1), (1,−1), (−1,1),
(1,1), (−1,−1), (2,−1), (1,−2), (−2,1), (−1,2).

Keep only directions for which v+epsilon d belongs to relint(F) for all sufficiently small epsilon>0. The zero direction is appropriate only for a zero-dimensional face. Rays are essential: omitting paths with one coordinate or the sum exactly fixed misses isolated point values.

These are precisely the finitely many refined-face sectors incident to the coarse vertex. There are at most 13 per coarse face/vertex incidence. Isolated zeros contribute no other equations.

## Equivalence argument

The refined grid triangulates every coarse face. The input slack is nonnegative affine on each coarse face, so every zero refined vertex lies in one of the zero strata above. Necessity follows from the full refined tight equations and the interval lemma. For sufficiency, cases A–C make every required zero-stratum relation hold along its entire relative interior, including point values and all one-sided limits; case D handles their endpoints and isolated zeros. Thus every row of the full refined system is satisfied.

No regularity of arbitrary competitors is assumed here. The reduction is solely an exact reformulation of the complete N-grid linear system, which can then be connected to unrestricted extremality by Part I Theorem 4.11 at N=4q.

## Encoding

Every identification is an integer interval pairing. Joining all slopes inside [a,b] uses the adjacent shift pairing [Na,Nb−2] -> [Na+1,Nb−1], plus finitely many representative links across projections. Jump/spike zero sets are integer intervals Na<k<Nb. Modulo-one wrap is split into a bounded number of pieces. Consequently all three families have polynomially many pairings and forced-zero ranges, with polynomial bit-length endpoints.
