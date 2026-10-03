# Author turn 3: weighted-mass search and a global stationarity certificate

2026-10-03T06:35:24Z. Turn 3/5. **NO FULL RESOLUTION.** Completion estimate: 5%; the global moment route now has explicit unresolved obstructions.

## 1. Testing the weighted active-mass route

Turn 2 reduced one sufficient condition to a vertex carrying at least half of the positive centered isotropic normal weight. I investigated whether the statement was merely a general fact about weighted polytopes with twice as many vertices as their dimension. It is not.

Here is an exact combinatorial counterexample to that proposed shortcut. In R^4 start with {0,e1,e2,e3,e4} and add

  (-1/100,1/4,1/4,1/4),
  (1/4,-1/100,1/4,1/4),
  (1/4,1/4,-1/100,1/4).

The three new vertices are stacked beyond three original simplex facets, and no facet contains two of them. Give each new vertex weight 1 and each of the five old vertices weight 1/5. Total weight is 4, whereas every facet has weight at most 1+3/5=8/5<2. The appended exact determinant enumeration verifies all facets and their weights. This example has neither the required unit-sphere normalization nor a claimed isotropic weighting. It disproves only the purely combinatorial shortcut, not the weighted geometric lemma or the original conjecture.

A small numerical diagnostic also generated 30 random raw configurations in each dimension 3,4,5,6, optimized the enclosing-ellipsoid dual, and retained only all-contact cases with positive weights and small unit-norm residual after whitening. The numbers of retained cases were 8,7,8,6. Their smallest maximum facet probability masses were approximately 0.50685, 0.59390, 0.58678, 0.59310. No numerical counterexample to the half-mass condition was found. These are floating-point diagnostics, not certificates, and 120 raw trials are not an exhaustive search. The original optimization target was not thereby resolved.

## 2. Stationarity for an unrestricted regular optimizer

I then attempted a different global route, deriving what a locally optimal configuration must satisfy. Assume Q=conv{u_i}_{i=1}^N is full dimensional with unit, distinct vertices, 0 in its interior, and is simplicial; work in a neighborhood preserving its facet structure. Let r=min_F r_F, where r_F is the positive distance from the origin to the facet's supporting plane. For each active facet F, write its inward contact point as

  r w_F=sum_i alpha_{F,i} u_i,

where ||w_F||=1, alpha_{F,i}>0 on its n vertices, alpha=0 elsewhere, and sum_i alpha_{F,i}=1. The contact point is in relative interior of F: another facet containing it would have support distance at most r and by Cauchy–Schwarz could equal r only with the same unit normal.

Differentiating u_i.w_F=r_F on F and using the barycentric identity and w_F.dw_F=0 gives

  dr_F=sum_i alpha_{F,i} w_F.du_i.

At a local maximum of min_F r_F on the product of spheres, separation of the finitely many tangent gradients supplies lambda_F>=0, sum_F lambda_F=1, supported on active facets, such that

  sum_F lambda_F alpha_{F,i}(w_F-r u_i)=0       for every i.

Define

  d_i=sum_F lambda_F alpha_{F,i},
  A_ij=sum_F lambda_F alpha_{F,i}alpha_{F,j}.

Then A is symmetric positive semidefinite and entrywise nonnegative, A*1=d, and

  sum_j A_ij u_j=r^2 d_i u_i.                 (S)

Summing (S) shows (1-r^2)sum_i d_i u_i=0. Since a full-dimensional inscribed finite polytope has r<1, the stationary weights d are centered. Multiplying by u_i and summing also yields the second-moment balance

  sum_F lambda_F w_F w_F^T = sum_i d_i u_i u_i^T.

Crucially this is equality of two generally anisotropic moments, not equality with I/n. Stationarity therefore does not provide the isotropic normalization missing in Turn 2.

## 3. Spectral form and why the proposed sharp trace proof fails

If all d_i>0, set D=diag(d_i) and B=D^{-1/2} A D^{-1/2}. B is positive semidefinite; sqrt(d) is an eigenvector with eigenvalue 1. Equation (S) supplies an n-dimensional eigenspace with eigenvalue r^2, via the rank-n coordinate matrix D^{1/2}U. Centering makes those eigenspaces orthogonal. Therefore

  tr B >= 1+n r^2.

A sharp proof along this route would follow from tr B<=2 when N=2n. However, I have not proved that inequality. It is not a consequence of positive semidefiniteness, stochasticity, or the displayed moment identities alone.

What can be proved directly is much weaker. Each active facet lies in the plane x.w_F=r, so its vertices have tangential components of common length sqrt(1-r^2). Their alpha-weighted sum is zero. The triangle inequality gives alpha_{F,i}<=1/2. Hence A_ii<=d_i/2, so tr B<=N/2. With N=2n this only implies

  r^2 <= (n-1)/n,

rather than the desired 1/n. It matches the right order only when n=2. When some d_i=0, those normals are absent from this stationary certificate, and the stated full-rank eigenspace argument must be restricted to the support; it cannot simply be applied with n unchanged without checking that support's rank. Non-simplicial optima also require additional nonsmooth analysis. These are further gaps, not reasons to assume genericity of a global optimizer.

## Outcome

The stationary matrix identity is a necessary condition in the precisely stated regular setting, not a solution. The trace<=2 assertion is an unproved replacement for the main difficulty and this route is blocked without a new mechanism. The numerical weighted-mass evidence does not fill that gap. No complete proof or counterexample to either clause of the original target has emerged.
