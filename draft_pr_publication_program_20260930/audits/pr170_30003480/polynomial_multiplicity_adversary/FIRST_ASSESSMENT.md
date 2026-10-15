Frozen UTC: 2026-10-12T11:45:23.046224+00:00

# First independently reconstructed assessment — frozen before comparison

Audit family: algebraic exact-multiplicity / affine-involution route.

This document records the first independent mathematical assessment, before any ROOT or sibling scientific conclusions, author verifier/results/review, PR body/comments, or programme conclusions were read. Only COUNTEREXAMPLE.md and source_record.json were read. No external individual was contacted, no Git state was manipulated, and no remote mutation was made.

Exact hypothesis: for each integer n>=3, with d_i(T)=det(M_i(T)M_i(T)^T) for a real binary n-tensor of Frobenius norm <=1, no real polynomial P in the n determinant variables satisfies G_n={d in B:P(d)>=0}, for either B=C_n=[0,1/4]^n or B=H_n={d in C_n:d_i<=sum_{j!=i}d_j for all i}.

Initial result: the stated full quantified impossibility claim is supported by an independently reconstructed proof. The assumptions are exactly real tensors, the closed norm ball, determinant-only polynomials, non-strict nonnegativity, and the given cube or determinant-polygon domain. No degree bound, genericity assumption, n-factor real sufficiency theorem, or finite computational evidence is required. Source interpretation has not yet been checked against external primary documents; this is a mathematical assessment, not a novelty or priority assessment.

## Reconstructed prerequisites

For normalized real tensors, let a be the smallest eigenvalue of mode 1, and choose a Schmidt expansion sqrt(a)|0>u+sqrt(1-a)|1>v. On the remaining modes, take projections onto the smaller-eigenvalue vectors and their sum N. In the product eigenbasis, N>=I-|w><w|, where w is the product of larger-eigenvalue vectors. Orthogonality of u,v gives p+q<=1 for p=|<w,u>|^2,q=|<w,v>|^2. Thus sum_{j>1}lambda_j>=a(1-p)+(1-a)(1-q)>=a(2-p-q)>=a. The a=0 and eigenvalue-tie cases cause no exception. The same applies to every mode.

For a tensor of squared norm s in (0,1], the unnormalized smaller eigenvalue at determinant d is a_s(d)=(s-sqrt(s^2-4d))/2. If the s=1 polygon inequality fails for mode i, then d_i is strictly larger than every other determinant. For each 0<d_j<d_i, the derivative of log(a_s(d_j)/a_s(d_i)) equals 1/sqrt(s^2-4d_i)-1/sqrt(s^2-4d_j)>0 on the nondegenerate interval. Therefore the ratio sum at every feasible s<=1 is at most its value at 1, which is <1. Zero determinants contribute zero, the lower trace endpoint is handled by continuity, and d_i=1/4 only permits s=1. This contradicts the normalized polygon inequality. The zero tensor is direct.

For n=3, triangle-admissible t_i in [0,1/2] are realized by an even-parity real tensor. Its squared amplitudes at 000,011,101,110 are 1-(t1+t2+t3)/2, (-t1+t2+t3)/2, (t1-t2+t3)/2, (t1+t2-t3)/2. They are nonnegative and sum to 1; each mode is diagonal with eigenvalues t_i,1-t_i. Hence, under d_i=t_i(1-t_i), G_3 is exactly the triangle region in [0,1/2]^3.

## Reconstructed obstruction

Put F(t)=P(t1(1-t1),t2(1-t2),t3(1-t3)). On D=(0,1/2)^3 the coordinate change is invertible and preserves local neighborhoods. F is invariant under t1 -> 1-t1. Let L=t1-t2-t3. A relatively open patch of L=0 with t2,t3>0 and t1=t2+t3<1/2 has the other triangle inequalities strict. Its two local sides are feasible and infeasible. Since F>=0 on the feasible side and F<0 on the infeasible side, continuity forces F=0 on the patch. The plane equation L divides F, because the restriction polynomial to that plane vanishes on an open two-dimensional set.

F cannot be zero: for instance t=(5/16,1/8,1/8) is infeasible yet its determinant vector (55/256,28/256,28/256) is strictly inside H_3 and C_3. Take the exact finite multiplicity m>=1 of L in F. The quotient restricted to L is not the zero polynomial, so it is nonzero at some point of the open boundary patch. At that point a transverse crossing changes sign and hence m is odd.

The polynomial automorphism tau(t)=(1-t1,t2,t3) sends L to -(t1+t2+t3-1). F=tau(F), so the factor L'=t1+t2+t3-1 has the same exact multiplicity m. Near (1/3,1/3,1/3), L'=0 lies within D and all triangle inequalities are strict, making F nonnegative on a full neighborhood. Exactness again gives a point on this open plane patch where the quotient is nonzero. A transverse crossing there forces m even. Contradiction.

For the H_3 version, the actual-boundary patch maps strictly inside H_3 because d2+d3-d1=2t2t3 and the other two margins are 2t3(1-t2-t3),2t2(1-t2-t3), all positive. On L'=0 the margins are 2t_jt_k>0. Thus both transverse crossings occur within the domain H_3. The argument does not incorrectly cross a boundary of the cube or of H_3.

For n>3, zero Gram determinant of a nonzero real tensor implies rank-one flattening and a real unit-vector factorization. Removing such a factor preserves norm and every remaining mode Gram matrix. Iteration proves G_n intersect {d4=...=dn=0}=G_3 times zero. The corresponding face of H_n is H_3 times zero. A proposed P_n restricts to a polynomial on that face; if the restriction vanished identically it would include the displayed infeasible point, and otherwise the three-mode contradiction applies. This proves all n>=3.

## Adversarial questions resolved initially

- Exact multiplicity, not only divisibility, is needed and exists because F is nonzero.
- A residual factor nonzero somewhere on each open plane patch follows from polynomial identity on an open set; its zero set cannot consume such a patch.
- The reflected plane is used as an algebraic factor, not as the image of the same real-domain boundary patch. The reflection need not preserve D.
- Nonnegative feasible values may contain zeros, but generic nonzero residual factors still force odd true-boundary multiplicity and even interior multiplicity.
- Rank-one slicing uses the closed determinant-zero face; it makes no claim about an all-positive higher-mode restriction.
- At d=0, d=1/4, s=0, s=2sqrt(d_max), and eigenvalue degeneracy, the prerequisites remain valid as described above.

Remaining work: verify the cited source domain and primary polygon theorem, independently retain reproducible symbolic/negative-mutation checks, and produce final review and complete retained-file inventory. No uncovered mathematical gap at this initial stage. Completion estimate: 55%.
