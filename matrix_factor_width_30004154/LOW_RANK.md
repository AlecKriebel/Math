# Exact low-rank factor-width certificates

Date: 2026-10-21. Scope: real symmetric PSD matrices, fixed original coordinate basis, exact zero-residual decomposition. These are self-contained deductions, not a novelty claim. The rank-two convex geometry is an application of established scalable-frame/diagram-vector theory.

## 1. Range reduction (all ranks)

Let Q=XX^T, with X an n by r real full-column-rank matrix. Then Q has factor width at most k if and only if

I_r = sum_j c_j v_j v_j^T,  c_j >= 0,  |supp(Xv_j)| <= k.

Indeed, decompose any supported PSD summands spectrally to obtain Q=sum_j y_j y_j^T. If z is in ker Q, then 0=z^TQz=sum_j(z^Ty_j)^2, so all y_j belong to range Q=range X. Write y_j=Xw_j. Applying a left inverse of X and its transpose gives I_r=sum_j w_jw_j^T. The converse follows by multiplication by X and X^T. Equivalently, for each support S, allowed v lie in ker X_{S^c}; these are exactly the preimages of range(Q) intersected with the coordinate subspace R^S.

There is a finite ray LP whenever every such kernel has dimension at most one: retain one nonzero representative v for each distinct nonzero kernel, and solve sum c_v vv^T=I_r, c_v>=0. This is stronger than simply restating the original lifted SDP: it removes PSD variables in this low-dimensional-intersection case.

A successful finite-ray certificate needs at most r(r+1)/2 distinct rays, by conic Caratheodory in Sym_r. A failure certificate is a symmetric H with tr H<0 and v^THv>=0 on all allowed rays (finite-dimensional cone separation). This compressed witness is sufficient by the range reduction; it should not be confused with an ambient dual matrix whose every k-principal submatrix is PSD.

## 2. Full-spark support obstruction and exact boundary LP

Assume n>=r>=1 and every r by r row minor of X is nonsingular (row-full-spark). Every subset of at most r rows is then independent: extend it to r rows. If v!=0, at most r-1 rows of X can annihilate it, hence |supp(Xv)|>=n-r+1. Conversely, for any r-1 selected rows, their kernel is one-dimensional, and every nonzero v in it has exactly those zeros (any extra zero contradicts row-full-spark). Thus the minimum nonzero support in range X is exactly n-r+1.

Consequently fw(Q)>=n-r+1. This does NOT assert equality. At k=n-r+1 all allowed directions are exactly the C(n,r-1) row-null lines, giving the finite ray LP above. For k<n-r+1 no nonzero allowed vector exists. For k>n-r+1, intersections can have dimension >1 and this ray enumeration no longer exhausts them.

The full-spark condition holds off the zero set of the product of all r-row determinants: a proper algebraic set, since Vandermonde rows at distinct real nodes give an explicit full-spark example. Hence it is open dense and holds with probability one for any distribution absolutely continuous with respect to Lebesgue measure on R^(nr). Mere full column rank is not enough for the support bound.

## 3. Complete real rank-two classification

Let r=2. Delete all zero rows of X, retaining N nonzero rows; this deletes zero rows and columns of Q and changes neither factor width nor the number of nonzero factors. If k>=N, membership is automatic, with minimum number of rank-one terms equal to 2. In the remainder assume 1<=k<N.

Partition the nonzero rows into parallel-line classes C_j, with multiplicities m_j. Choose a nonzero row representative a_j=(a_j1,a_j2), and its perpendicular column v_j=(-a_j2,a_j1)^T. A nonzero v can annihilate rows only from a single parallel class; it has support N-m_j exactly when it lies on the line Rv_j, and otherwise support N. Thus define

J_k = {j: m_j>=N-k}.

Then the following are equivalent:

1. fw(Q)<=k.
2. I_2 lies in cone{v_jv_j^T: j in J_k}.
3. 0 lies in conv{p_j: j in J_k}, where
   p_j = ((v_j1^2-v_j2^2)/(v_j1^2+v_j2^2), 2v_j1v_j2/(v_j1^2+v_j2^2)).
4. Those unit-circle points are not all contained in an open semicircle.

The empty convex hull does not contain 0. For (2)<->(3), put u_j=v_j/||v_j||. Then u_ju_j^T = (1/2)[[1+p_j1,p_j2],[p_j2,1-p_j1]]. Taking traces shows that I_2=sum_j lambda_j u_ju_j^T exactly when sum lambda_j=2 and sum lambda_j p_j=0. Thus convex weights alpha_j give lambda_j=2alpha_j and c_j=2alpha_j/||v_j||^2. Statement (4) is strict separation of a compact convex hull from the origin. The word OPEN is essential: antipodal points already succeed.

A geometric O(N log N) membership test groups row lines, retains eligible lines, and sorts doubled angles; the largest cyclic gap between the p_j is at most pi exactly when membership holds. Exact rational arithmetic can instead test all pairs/triples or solve the 3-row linear feasibility problem, avoiding floating-point angular decisions at the boundary.

### Minimal certificates

If membership holds, Caratheodory in R^2 gives at most three rank-one terms. The minimum is exactly two if and only if there are two eligible perpendicular directions; otherwise it is exactly three. A rank-two PSD matrix cannot have one term. A two-column matrix W satisfying WW^T=I_2 is orthogonal, forcing the two weighted directions to be perpendicular. Conversely an eligible orthonormal pair sums to I_2. In doubled-angle coordinates this means an antipodal pair.

For all k simultaneously, the exact factor width is N-t*, where t* is the largest integer t>=1 for which 0 belongs to the convex hull of p_j with m_j>=t, and t*=0 if no such t exists. Only the finitely many observed multiplicities need be tested. This covers repeated rows, signed parallel rows, and zero rows correctly.

### Invariances and field convention

The original coordinate basis matters. Nonzero diagonal congruence DQD and coordinate permutations preserve factor width and the minimum number of rank-one factors, since they preserve vector supports. In particular, arbitrary nonzero rescaling of rows of X leaves the parallel classes and allowed lines unchanged. Replacing X by XO with O orthogonal preserves XX^T and rotates/reflects the reduced problem without changing membership. An arbitrary invertible right transformation is NOT permitted while keeping target I_2: it changes the metric. Arbitrary orthogonal conjugation in the ambient n-coordinate space need NOT preserve factor width (a diagonal matrix can become dense rank one under such a conjugation).

These doubled-angle and three-term assertions are stated over R. For genuinely complex Hermitian rank-two matrices the analogous normalized projectors use the three-dimensional Bloch sphere, with a four-term Caratheodory bound, not the real planar criterion. Allowing complex factors for a real Q does not change membership: real and imaginary parts split each complex rank-one factor into two real factors with no larger support. That observation alone does not preserve the minimum number of factors.

### Rational formulation without square roots

If Q is rational PSD rank two, select two independent columns B and obtain a rational positive-definite 2 by 2 matrix G with Q=BGB^T (for example, choose a nonsingular principal 2 by 2 submatrix M and take B=Q[:,T], G=M^(-1)). Apply the row-class/ray construction to B and replace target I_2 by G. All coefficients of sum c_j v_jv_j^T=G are rational. A feasible system has a rational nonnegative solution with at most three positive entries. Hence certificates can be recorded as rational weighted rank-one matrices without square roots; the vectors sqrt(c_j)Bv_j need not themselves be rational. Two-term minimality is equivalent to an eligible pair satisfying v_i^T G^(-1)v_j=0. This follows by whitening the reduced target, not by incorrectly testing Euclidean perpendicularity in arbitrary B coordinates.

## 4. Exact positive example: width 3, minimum three terms

Let X have rows (0,1),(2,-1),(2,1),(1,1). These four nonzero rows are pairwise nonparallel, hence full-spark. Define

v1=(1,0), v2=(1,2), v3=(1,-2),
c1=3/4, c2=c3=1/8.

Then sum c_j v_jv_j^T=I_2. Their images are

u1=(0,2,2,1), u2=(2,0,4,3), u3=(-2,4,0,-1).

Consequently

Q = [[1,-1,1,1],[-1,5,3,1],[1,3,5,3],[1,1,3,2]]
  = (3/4)u1u1^T+(1/8)u2u2^T+(1/8)u3u3^T.

Every displayed image has exactly three nonzero coordinates, and row-full-spark gives fw(Q)>=3. Thus fw(Q)=3. The fourth eligible line has representative (1,-1); no two of the four eligible lines (1,0),(1,2),(1,-2),(1,-1) are perpendicular. Therefore the minimum number of width-three rank-one factors is exactly three, although rank Q=2.

## 5. Exact negative example with strict spectral-bound slack

Independently audited rational example. Let B have rows (1,1/2),(1,-1/2),(1,3/4),(1,-3/4), and Q=BB^T. All row directions are distinct, so at k=3 each allowed reduced line is v=(-t,1), t in {1/2,-1/2,3/4,-3/4}. Set H=diag(-1,3/4). Then tr H=-1/4, while v^THv=3/4-t^2 is either 1/2 or 3/16, strictly positive. Thus I_2 is not in the allowed ray cone, fw(Q)>3, and therefore fw(Q)=4. This also shows the full-spark lower bound n-r+1 need not be attained.

All entries of Q are positive. The diagonally normalized Q has nonzero eigenvalues 72/25 and 28/25: the two columns of the row-normalized B are orthogonal, with squared norms 2*(4/5)+2*(16/25)=72/25 and 2*(1/5)+2*(9/25)=28/25. Hence the largest eigenvalue of its entrywise absolute value is 72/25<3. The usual necessary normalized-absolute spectral bound does not suffice even in real rank two, n=4,k=3.

## 6. Edge cases

Rank zero: Q=0, empty decomposition (factor-width convention for zero may assign 0 or 1). Rank one: Q=xx^T has factor width exactly |supp x|, since all nonzero summand vectors must be parallel to x. Real rank two requires N>=2. At N=2, k=1 succeeds exactly when the two rows of X are perpendicular, equivalently Q is diagonal. At N=3, only k=1,2 are nontrivial and the same criterion applies. At N=4,k=3, Sections 4 and 5 exhibit both membership outcomes even under full-spark assumptions.

## 7. Priority and source audit

The above proof is independently written. No general open problem is claimed solved, and no novelty claim is established.

- Boman, Chen, Parekh, Toledo, *On factor width and symmetric H-matrices*, Linear Algebra Appl. 405 (2005), 239-248, DOI https://doi.org/10.1016/j.laa.2005.03.029 ; author PDF https://www.cs.tau.ac.il/research/doron.chen/Pubs/factorwidth.pdf . Establishes factor-width framework and width-two/scaled-diagonal-dominance characterization.
- Johnston, Moein, Plosker, *The Factor Width Rank of a Matrix*, https://arxiv.org/abs/2405.11556 ; journal DOI https://doi.org/10.1016/j.laa.2025.03.016 . Distinguishes width from minimal sparse factor count; inspected publisher text confirms general SDP formulation and special-class results. Its n=4 discussion leaves broader dense width-three factor-count cases open, but the present rank-two subclass is not a resolution of that whole question.
- Copenhaver et al., *Diagram vectors and Tight Frame Scaling in Finite Dimensions*, https://arxiv.org/abs/1303.1159 . Abstract inspected: planar diagram vectors and tight-frame scaling predate this work, including the geometric characterization.
- Kutyniok, Okoudjou, Philipp, *Scalable Frames and Convex Geometry*, https://arxiv.org/html/1310.8107 . Full HTML inspected, especially Sections 2 and 3: nonnegative rescaling, convex combinations of rank-one matrices, Caratheodory reductions, and orthogonal-basis characterization of minimal dimension-many scalings. These directly overlap the mathematical engine of Section 3; the rank-two factor-width criterion is an application after the support/range reduction.
- Naomi Shaked-Monderer, *On factor-width ranks*, DOI https://doi.org/10.1016/j.laa.2026.09.011 . Publisher abstract and section summaries inspected; journal issue date 1 January 2027, volume 752, pages 308-331. Search currently exposes it, but online publication date and full theorems were not established in this audit. Requires review before publication/priority claims.
