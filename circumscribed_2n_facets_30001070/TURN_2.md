# Author turn 2: global moment certificate and its exact obstruction

2026-10-03T06:29:42Z. Turn 2/5. **NO FULL RESOLUTION.** Completion estimate: 6%. This turn addresses a genuinely global moment route, beyond the antipodal trace calculation. The lemmas below are not claimed novel; neither substitutes for the original unrestricted target.

## 1. A global centered tight-frame theorem

Let u_1,...,u_N be unit vectors in R^n with 0 in the interior of their convex hull. Suppose

  sum_i u_i=0,             sum_i u_i u_i^T=(N/n) I.

Let T={x:u_i.x<=1}. If a vertex x has k active facets, then k>=n. Set t_i=u_i.x. The active entries equal 1, while sum_i t_i=0. Cauchy–Schwarz on the N-k inactive entries gives

  (N/n)||x||^2=sum_i t_i^2 >= k+k^2/(N-k)=Nk/(N-k).

Here k<N, since all t_i=1 would contradict their zero sum. Consequently

  ||x||^2>=nk/(N-k)>=n^2/(N-n).

This is a bound on every vertex, not an averaging argument and not an assumption about the number of vertices.

For N=2n it gives R_0(T)>=sqrt(n). If R_0(T)=sqrt(n), all vertices must have k=n and equality in Cauchy–Schwarz, so every inactive t_i equals -1. Thus -1<=u_i.x<=1 for every vertex and hence for all x in T. It follows -T subset T; negating gives T subset -T, so T is centrally symmetric. Exactly 2n facets then occur in n opposite pairs. Boundedness makes their n directions independent, so the antipodal argument in Turn 1 forces an orthonormal system and T=[-1,1]^n up to rotation.

Thus the full inequality and equality clause hold under the additional equal-weight centering and isotropy assumptions. No central symmetry was assumed. The unrestricted target does not supply either moment identity.

## 2. The moment identities are not an innocuous normalization

Rotations preserve the eigenvalues of sum_i u_i u_i^T and the length of sum_i u_i. Therefore an arbitrary configuration cannot be made centered and isotropic by the transformations that preserve the target objective. A general invertible linear map followed by individual renormalization changes the centered inradius. Translating a polar configuration changes the distinguished origin. Neither operation is an admissible without-loss-of-generality reduction.

An exact example shows that the theorem includes genuinely non-antipodal configurations. In dimension 3 take the union of the coordinate basis with the negatives of the rows of

  Q=(2/3)J-I,

where J is the all-ones matrix. Q is orthogonal and Q*1=1. The six vectors have zero sum and frame operator 2I, but Q has no entry +/-1, so there are no antipodal pairs between the two triples. Their polytope T={x_i<=1, Qx>=-1} has a vertex x=(-2,1,1) with norm sqrt(6)>sqrt(3). (The defining equations and feasibility are exact.) This example is not a counterexample to the conjecture; it checks that the new route really covers a nonsymmetric case and that equality rigidity is necessary.

## 3. Weighted decomposition and a precise missing global lemma

A possible extension uses positive weights c_i satisfying

  sum_i c_i u_i=0,       sum_i c_i u_i u_i^T=I.

Taking traces gives sum_i c_i=n. For a vertex x with active set A and active weight a=sum_{i in A}c_i, weighted Cauchy–Schwarz gives

  ||x||^2=sum_i c_i (u_i.x)^2 >= a+a^2/(n-a)=na/(n-a).

Therefore a vertex whose active facets have total weight at least n/2 would give the desired R_0(T)>=sqrt(n). In the equal-weight case c_i=1/2 and |A|>=n, this is automatic. With unequal weights, merely knowing |A|>=n does not prove a>=n/2.

Two independent gaps prevent promoting this route:

1. The target does not assume a centered isotropic positive weighting of its unit normals, and no objective-preserving reduction to one has been established.
2. Even under such a weighting, no proof has been obtained that some vertex has active weight at least n/2. This is an explicit geometric lemma to investigate, not an established combinatorial fact.

It would be circular to label either missing statement a normalization and conclude the original conjecture.

## 4. A quantitative anisotropic bound

If only sum_i u_i=0 is assumed, let S=sum_i u_i u_i^T. The same vertex calculation gives

  lambda_max(S) ||x||^2 >= Nk/(N-k),

and hence R_0(T)^2>=Nn/((N-n)lambda_max(S)). For N=2n this is 2n/lambda_max(S). Since tr S=2n, lambda_max(S)>=2, and this reaches the sharp n bound only in the isotropic case. It does not prove the desired inequality for arbitrary centered configurations.

## Result and next route

The centered equal-weight tight-frame class is settled here with equality, as a scoped lemma only and without a novelty claim. The general statement remains unresolved. The next turn will examine the weighted active-mass condition and whether exact nonsymmetric configurations defeat its natural combinatorial surrogates, rather than assuming arbitrary normals can be isotropized for free.
