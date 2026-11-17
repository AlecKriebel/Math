# Independent mathematical derivation, first assessment

This derivation was made from the actual manuscript and original proof. It is not an uncontaminated first-seal review: the active native COUNTEREXAMPLE.md unexpectedly contained a ROOT priority synthesis, exposed before sealing. No priority_reviews/*.md or ROOT gate file was deliberately opened before this assessment. The conclusion below is justified by the derivation, not by that feedback.

## Claim and falsification targets

For each integer n>=3, let G_n be the determinants of the real binary mode Gram matrices of tensors with Frobenius norm <=1. The claim is that no real polynomial in those n determinant variables defines G_n by one condition P>=0 relative to C_n=[0,1/4]^n or H_n=C_n intersect {d_i<=sum_{j!=i}d_j}. A constant, identically zero, arbitrarily high degree, reducible or non-squarefree polynomial is allowed by the hypothesis and must all be excluded. The proof must not implicitly require strict positive determinants for the higher-n face reduction. Neither general marginal sufficiency at n>3 nor any finite computation is required.

## Trace normalization, including endpoints

Write s=||T||^2. If s>0, the normalized tensor T/sqrt(s) has Gram eigenvalues a_s(d_i)/s and 1-a_s(d_i)/s, where a_s(d)=(s-sqrt(s^2-4d))/2. Here 0<=d<=s^2/4 and 0<s<=1. The normalized polygon inequality multiplies by s to give a_s(d_i)<=sum a_s(d_j).

A direct independent differentiation uses a_s=2d/(s+sqrt(s^2-4d)). For d>0 and s>2sqrt(d), d log a_s/ds=-1/sqrt(s^2-4d). Therefore the derivative of log(a_s(d_j)/a_s(d_i)) is 1/sqrt(s^2-4d_i)-1/sqrt(s^2-4d_j)>0 when 0<d_j<d_i. If lambda(d_i)>sum lambda(d_j) at s=1, monotonicity of lambda forces d_i>d_j for all j and d_i>0. Every nonzero ratio is increasing with s; every zero d_j contributes an identically zero ratio. Thus sum a_s(d_j)/a_s(d_i)<=sum lambda(d_j)/lambda(d_i)<1 for all allowable s<=1. The denominator is positive even at s=2sqrt(d_i), so continuity handles that endpoint. If d_i=1/4, feasibility forces s=1 directly; the derivative is not invoked there. If T=0 all d_i=0. Hence the ball, rather than only the sphere, satisfies the trace-one polygons.

The normalized necessity is independently valid: projectors P_j onto the smaller eigenvectors commute on distinct factors, and N=sum P_j has kernel spanned by the complementary product vector w, with all other eigenvalues >=1. For a real Schmidt decomposition with a<=1/2 and orthonormal u,v, put p=|<w,u>|^2,q=|<w,v>|^2. Then p+q<=1, and a(1-p)+(1-a)(1-q)-a(2-p-q)=(1-2a)(1-q)>=0. This completes the necessity without presuming simultaneous diagonalization of the full tensor or complex realizability.

## Exact real three-factor sufficiency

For t_i in [0,1/2] satisfying all triangles, take support 000,011,101,110 and squared amplitudes w_0=1-(t_1+t_2+t_3)/2 and w_i given by the other triangle slacks divided by 2. All are nonnegative; their sum is 1, and w_0>=1/4. No two support words differ in a single bit, so every off-diagonal Gram entry is zero. The diagonal bit-one masses are w_2+w_3=t_1, w_1+w_3=t_2,w_1+w_2=t_3. Thus the eigenvalues are t_i,1-t_i and the determinants are t_i(1-t_i), including t_i=0 or 1/2 and vanishing amplitudes. All amplitudes are real square roots. This proves exact G_3 membership, not just its convex hull.

## Arbitrary polynomials and exact multiplicities

Assume a polynomial P cuts out G_3 in the cube. Pull it back via phi_i=t_i(1-t_i) to F=P(phi). On D=(0,1/2)^3, phi is an analytic diffeomorphism, since its derivative is diagonal with positive entries 1-2t_i. F is a polynomial and is globally invariant under each affine reflection t_i->1-t_i; the reflected point need not remain in D for this polynomial identity.

Along L=t_1-t_2-t_3=0 with b=t_2>0,c=t_3>0,b+c<1/2, the other triangles are strictly satisfied. Hence locally F>=0 for L<0 and F<0 for L>0, forcing F=0 on the entire relatively open plane patch. Expressing F as a polynomial in L,b,c proves that its constant L coefficient is identically zero. F is nonzero because D contains an infeasible open region, where F<0. Let F=L^m A with exact multiplicity m>=1. Exactness says A restricted to L=0 is a nonzero polynomial; its zero set cannot contain that entire relatively open patch. At a boundary point with A!=0, continuity leaves A of fixed nonzero sign in a neighborhood. This gives strict opposite signs of F on the two sides and forces m odd. Nonnegative, rather than positive, membership inside G_3 causes no loophole at that generic point.

The polynomial ring automorphism tau(t)=(1-t_1,t_2,t_3) fixes F and sends L to -L', with L'=sum t_i-1. Divisibility and nondivisibility both transfer under an involution, so the multiplicity of L' is exactly m, not merely at least m. Its plane has a relatively open patch about (1/3,1/3,1/3) strictly inside D and all three triangles. The residual factor F/(L')^m is nonzero at some point of that patch, by exact multiplicity. F>=0 in a whole ball about that point; an odd m would have opposite signs across L'. Thus m is even, contradiction. Reducible extra factors and intersections of factors are avoided by the generic nonzero residual point. No degree bound is imposed.

## Relative hull argument and zero restriction

On L=0 with t=(b+c,b,c), the three determinant slacks are 2bc,2c(1-b-c),2b(1-b-c)>0. On L'=0, each slack equals 2t_jt_k>0. Therefore all the local balls for both parity arguments can be chosen inside the open determinant hull. For the H_3 version F is still nonzero: t=(5/16,1/8,1/8) violates the first t triangle, but phi=(55,28,28)/256 has positive hull slacks (1,55,55)/256 and open cube coordinates. P=0 and any polynomial whose pullback vanishes identically are excluded by this explicit infeasible point.

## Exact higher-factor faces

A real 2-row flattening has Gram determinant zero exactly when its row rank is at most one (positive semidefiniteness/Cauchy-Schwarz). For a nonzero tensor it has rank one, so it factors S tensor u in that mode. Choose ||u||=1 by absorbing the nonzero length into S. Norms are preserved. In every other mode, summing the Gram products over the peeled mode multiplies each inner product by sum u_b^2=1; all other Gram matrices, including their zero determinants, are preserved. Iterating therefore produces a three-factor S with the same first three Gram matrices and norm. Reverse inclusion follows by tensoring any S with unit real vectors. T=0 is a separate harmless case. Thus G_n intersect {d_4=...=d_n=0}=G_3 times zero exactly, and H_n has the analogous H_3 face. Restricting P_n to this face yields an arbitrary three-variable polynomial; if the restriction is identically zero it includes the entire C_3 or H_3 face, already excluded above. This proves every n>3 claim within its closed domain. It does not prove all-positive n>3 impossibility, and the manuscript explicitly declines that stronger claim.

## Witness and small-n limits

For r=(49,36,36,1)/100 and d_i=r_i^2, every coordinate is strictly between 0 and 1/4. The first determinant hull slack is 0.0192>0, all others larger. The source product over all 16 signs, including its 1/2 coefficient, is rational and positive; the printed fractions require independent reproduction below. The claimed spectral separation is exact because d_1=2401/10000>6/25, d_2=d_3=81/625<5/36 and d_4=1/10000<99/10000. Since t(1-t) strictly increases on [0,1/2], lambda(d_1)>2/5 and the other lambdas sum to <103/300<2/5. A smaller norm cannot rescue this point by the normalization result. For n=2, real diagonal tensors sqrt(t)e_00+sqrt(1-t)e_11 realize each coincident determinant t(1-t) in [0,1/4], and -(d_1-d_2)^2 cuts out precisely the diagonal. For n=1 every flattening has a single column and determinant zero.

## First verdict and remaining concrete checks

No mathematical gap found in the stated single-polynomial theorem or the unrealizability part of the strictly positive witness. The proof is self-contained apart from the credited normalized polygon antecedent, which is also rederived correctly. The remaining tasks are exact product reproduction, source-formula/citation and overlap comparisons, external chronology evidence, full archive/metadata/native consistency, optimization and semantic false-variant controls, and PDF appearance. The first rendered PDF read covered all five pages: no clipping, overlap, malformed symbols or broken reference appears; the manuscript claim set agrees with the source read.

A material protocol/presentation issue is already identified: active native COUNTEREXAMPLE.md Section 8 contains ROOT's audit synthesis and recommendations. It should be separated from the active scientific proof, and any fresh first-seal reviewer should initially receive the manuscript and original proof only. This review cannot be used as an uncontaminated first-seal independent priority assessment. That exposure does not establish any flaw in the displayed theorem.
