# k407 first-turn checkpoint

**Unreviewed full mechanism; first substantive author turn in progress.** The target is the vertex centroid of the **outer polygon's focal antipedal**, for even least period. It is not a signed-area centroid. Thus zero signed area is harmless, while finite line intersections must be verified. The focus belongs to the original billiard ellipse, not the generally different outer-vertex locus ellipse. Both source Table5 editions agree.

## Canonical objects and real domain

Scale the caustic's major semiaxis to1, put k=sqrt(1−beta²), k'=beta, and use Stachel's parameter v=2K tau/N, delta=2v, a=dn(v)/cn(v), b=k'/cn(v). Original vertices P(w)=(-a sn w,b cn w). The original foci are M=(±k,0). The outer tangent intersections have the explicit parametrization

R(u)=(-A sn u,B cn u), A=a dn(v)/cn(v), B=b/cn(v).

This follows by solving the two original tangent equations at P(u−v),P(u+v). Consecutive outer vertices R(u−v),R(u+v) lie on the original tangent at P(u).

For M=(k,0), let U(u) be the intersection of antipedal lines through those two outer vertices. Their normals are q_±=R(u±v)−M and their equations relative to M are q_± dot(U−M)=q_± dot q_±. With D0=1−k² sn²(v)sn²(u), direct addition formulas give

det(q_−,q_+)=2B sn(v)dn(v)dn(u)[a+k sn(u)]/D0.

For real u, a>k, dn(u)>0 and D0>0, so every intersection is finite and unique. The opposite focus is analogous. This domain statement does not use a nonzero polygon area.

## Complete complex pole mechanism for N>=6

Set p=iK'. A coordinate of U is a meromorphic elliptic function of u. Its only potential singularities come from poles of R endpoints or zeros of the displayed determinant:

- At u=K+p and translates, dn(u)=0 and the two regular R endpoints coincide. The determinant has a simple zero; both Cramer numerators vanish, so U extends holomorphically
- At u=p and translates, the Jacobi functions have common simple poles, D0 has order two, and the focus term contributes another pole. The determinant therefore has a finite nonzero limit. The two R endpoints are finite, so U is regular
- At a+k sn(u)=0, the common original tangent line passes through M. It is an isotropic complex tangent: its normal n=(-sn(u)/a,cn(u)/b) satisfies n dot n=0 because k²=a²−b². Both endpoint vectors q_± lie along this isotropic line, so q_± dot q_±=0. Both Cramer numerators vanish while the determinant has a simple zero, giving another removable singularity
- Remaining possible poles arise when one R endpoint has a simple pole. Cramer numerators have order at most two and the determinant a simple pole, so U has at most a simple pole.

The focus roots are simple and distinct from the endpoint poles except when v=K/2. Since the period is primitive, that exceptional case is exactly N=4 and is treated separately below. Algebraically the overlap equation is sn(v)dn(v)=cn(v), whose unique real solution in(0,K) is K/2.

Now sum all N antipedal vertices, using outer vertex phase w. At a pole of R(w+i delta), the opposite outer vertex is also a pole because N is even and R(w+(i+N/2)delta)=-R(w+i delta). The two regular neighbors at the first pole are Q and−Q, by oddness of R about p. Write the first pole's Laurent coefficient as L. The residue V(M,Q) of its incident antipedal intersection is characterized by

L dot V=L dot L,       (Q−M) dot V=0,
so V(M,Q)=−(L dot L) J(Q−M)/det(L,Q−M), J(x,y)=(-y,x).

At the opposite pole the leading vector is−L and the neighbors are−Q,Q. Hence the four incident residues sum to

V(M,Q)+V(M,−Q)−V(−M,Q)−V(−M,−Q)=0,

since V(M,−Q)=V(−M,Q). For N>=6 the four incident antipedal vertices are distinct and every relevant denominator is nonzero at the pole. Thus the complete cyclic centroid has no poles. It is holomorphic on the compact torus with periods4K,4iK' and therefore constant. A horizontal reflection forces this constant onto the focal axis; central symmetry relates the two focal constants by negation. It need not be O (direct six-period diagnostics give−M/3).

## N4 and circles

For N4 the canonical outer locus is a circle, and the centrally symmetric outer quadrilateral is a rectangle circumscribed about the original ellipse. Let its orthogonal side normals define coordinates and halfwidths H1,H2, and let the original focus have coordinates(m,n). The focus/support identities are H1²−m²=H2²−n²=b².

Direct line intersection gives the antipedal vertex centroid

(m/2[(H2²−n²)/(H1²−m²)−1], n/2[(H1²−m²)/(H2²−n²)−1])=(0,0).

This handles the degenerate complex-pole overlap without a limiting assertion through nonperiodic data. For a circular original billiard, the foci coincide withO, and ordinary antipodal symmetry gives centroidO for every even primitive family.

## Status and next work

The source gate and these deductions are the first substantive author turn. Direct40-digit line-intersection probes at two moduli and N4,6,8,10,12 are consistent but not proof. Next: write the full derivation and complete overlap/root classification, exact Cramer/residue/rectangle checks and separately labeled primitive-star diagnostics; then freeze for a separate reviewer. Preserve the focus-vs-outer-locus distinction and vertex-vs-area-centroid domain. No claimed result PR or QUEUE update before independent review.
