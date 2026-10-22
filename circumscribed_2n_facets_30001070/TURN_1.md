# Author turn 1: exact normalization and local variational route

2026-10-03T06:24:00Z. Turn 1/5. **NO FULL RESOLUTION.** Completion estimate toward the unrestricted discovery goal: 3% (a planning estimate, not a probability of truth). The source/prior gate was completed before this author work. No remote state is changed.

## Exact target and source correction

For every positive integer n and every bounded, full-dimensional convex polytope P in R^n having exactly 2n facets and containing the origin-centered Euclidean unit ball B, prove R_0(P):=max_{x in P}||x|| >= sqrt(n), and prove equality occurs only for orthogonal images of [-1,1]^n. Alternatively, give an exact counterexample to either assertion. The objective is the outer radius about the specified origin, not volume, surface area, a freely centered circumradius, or a Banach–Mazur distance. There is no symmetry assumption.

The primary source is Zong's Conjecture 2 in OWR 44/2008, printed p2547. Its note says open for n>=5. The upstream literature paragraph instead describes the adjacent blocking-number Conjecture 1. The 2026 paper of Litvak–Sonnleitner–Szczepanski, printed p1295, still calls the corresponding 2n-point spherical-covering optimum conjectural. The known n<=4 and antipodal results receive prior credit.

## 1. Normalization, boundedness, facets, and polarity

Write the irredundant facet presentation P={x:u_i.x<=h_i, i=1,...,2n}, with ||u_i||=1. Ball containment gives h_i>=1. Distinct facets have distinct oriented normals. Set T={x:u_i.x<=1 for all i}. Then B subset T subset P. T is bounded: its recession cone {v:u_i.v<=0 all i} is the same as that of P, which is {0}. It is full dimensional because it contains B. Every displayed inequality remains a facet: x=u_i satisfies it at equality and every other inequality strictly, because distinct unit vectors have dot product strictly below 1. Hence T has exactly 2n facets.

For Q=conv{u_1,...,u_{2n}}, boundedness is equivalent to 0 in int Q. Indeed, failure of interior containment gives a nonzero separating v with all u_i.v<=0, and conversely such v is a recession direction of T. Every u_i is a vertex of Q, exposed by u_i itself. Thus Q has exactly 2n vertices on the unit sphere and 0 in its interior. Directly from the definitions T=Q^polar.

For a unit v let h_Q(v)=max_i u_i.v and r_0(Q)=min_{||v||=1}h_Q(v)>0. The ray tv lies in T exactly when 0<=t<=1/h_Q(v). Therefore R_0(T)=1/r_0(Q). Also r_0(Q) is precisely the largest radius of an origin-centered ball contained in Q: containment is equivalent to the support-function inequalities r<=h_Q(v) for every unit v.

Consequently the normalized full target is:

  r_0(Q)<=1/sqrt(n), with equality only for a regular cross-polytope,

for all such unrestricted Q. Equivalently min_{||v||=1}max_i u_i.v<=1/sqrt(n), with the same equality classification. The least angular cap covering radius for centers u_i is arccos(r_0(Q)). Configurations not positively spanning have r_0<=0 and cannot produce a strict counterexample; they are outside the bounded-polytope equality case.

The equality reduction back to P is important. If the normalized theorem holds and R_0(P)=sqrt(n), then R_0(T)=sqrt(n), so T is a cube and its normals are +/-an orthonormal basis. In that basis P is a box -h_{i,-}<=x_i<=h_{i,+}, all h>=1. Its squared radius is sum_i max(h_{i,-},h_{i,+})^2. Equality n forces every h=1, and therefore P=T. Conversely that cube has radius sqrt(n). Thus neither containment nor equality has been weakened.

## 2. Antipodal baseline, explicitly prior credit

If Q=conv{+/-a_i:i=1,...,n}, its spanning hypothesis makes the matrix A with rows a_i invertible. T=A^{-1}[-1,1]^n. Averaging the squared norms of its 2^n vertices gives

  E_s ||A^{-1}s||^2 = tr((A A^T)^{-1}) >= n^2/tr(A A^T)=n.

The inequality is the scalar arithmetic–harmonic mean inequality for the positive eigenvalues, and every a_i is unit. Thus R_0(T)>=sqrt(n). Equality of the radius forces equality of the average, hence A A^T=I, so the normals are orthonormal and T is a cube. This is an elementary verification of an established special case, not a new unrestricted result. Borodachov's Theorem 2.2 proves the antipodal covering result and cannot be applied to general configurations.

## 3. A local variational computation at the cube

This turn also explored whether cube optimality can be extended by deformation. Label the normals near +/-e_i as

  u_{i,s}(t)=(s e_i+t a_{i,s})/sqrt(1+t^2 ||a_{i,s}||^2), s in {+1,-1},

where (a_{i,s})_i=0. Put p_i=(a_{i,+}+a_{i,-})/2 and q_i=(a_{i,+}-a_{i,-})/2, and let P,Q be the row matrices p_i,q_i (both with zero diagonal). For each sign vector s, the intersection x_s(t) of its selected n facet planes is feasible for sufficiently small t: at t=0 its unselected facet inequalities have margin 2, and there are only finitely many selectors. The matrices remain invertible. Thus every x_s(t) is an actual vertex.

Let D_s=diag(s), M_s=D_s P+Q, and b_s have entries ||p_i+s_i q_i||^2. Direct expansion of the selected linear equations gives

  x_s(t)=s-t M_s s+t^2(M_s^2 s+(1/2)D_s b_s)+O(t^3).

Averaging independently uniform signs yields

  F(t):=2^{-n} sum_s ||x_s(t)||^2
      = n+t^2[2||P||_F^2+2||Q||_F^2+2 tr(Q^2)]+O(t^3)
      = n+t^2[2||P||_F^2+4||Sym Q||_F^2]+O(t^3).

Details: the first-order average vanishes; E||M_s s||^2=||P||_F^2+||Q||_F^2; E s^T M_s^2 s=tr(Q^2), since odd sign moments vanish and the D_s P D_s P term reduces to sum_{ij}P_ij P_jj=0; E sum_i b_{s,i}=||P||_F^2+||Q||_F^2. Finally ||Q||_F^2+tr(Q^2)=2||Sym Q||_F^2.

This Hessian is positive semidefinite, with kernel exactly P=0 and Q skew-symmetric, the infinitesimal common rotations. The configuration space is the smooth product (S^{n-1})^{2n}; F is smooth and invariant under common rotations near this labeled configuration. A smooth local slice transverse to the rotation orbit has a positive-definite Hessian. Taylor's theorem on that slice therefore proves a strict local minimum modulo rotations: in some neighborhood of the cube, F>=n, with equality exactly on its rotation orbit. Since R_0(T)^2>=F, no sufficiently small nonsymmetric deformation gives a counterexample, and local equality is rigid. This is a fixed-dimension neighborhood statement, with no dimension-uniform radius asserted.

The local result is not claimed novel. It is compatible with the prior area/triangulation treatment of cross-polytopal combinatorics (Borodachov pp2 and5). Its purpose here is to identify what a genuinely different approach must overcome.

## Exact remaining gap

The local Hessian does not control configurations far from the cross-polytope or changes of Delaunay/face combinatorics. Applying the antipodal trace argument to arbitrary paired normals has no valid inverse-matrix reduction. No global symmetrization preserving both the number of facets and the objective has been proved. The unrestricted covering inequality and its equality clause are still unresolved in this work.

Next route: investigate a genuinely global variational certificate or a nonsymmetric family beyond cross-polytopal combinatorics, rather than re-solving the antipodal case.
