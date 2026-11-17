# Source-first scope/import derivations

These are my own checks after reading the full authored manuscript/PDF/native metadata and five fresh images, before any supporting programme, archived audit body, current findings or new foreign proof. They do not certify the unseen historical question or the earlier Siebert papers.

## 1. Exact interaction and self-adjointness

On the antisymmetric n-particle space, multiplication by L_n=Σ_i 1_Lambda(x_i) has integer spectrum in {0,…,n}. For x_i,x_j in Lambda=B(0,4), |x_i-x_j|<8. The displayed V is one there, including V(0)=1. Therefore the ordered pair interaction including diagonal is exactly L_n^2, while excluding diagonal subtracts Σ_i 1_Lambda(x_i)=L_n. This gives both kappa choices with coefficient one and no factor 1/2. It does not impose a wall on kinetic motion or replace the full-space Laplacian.

For r^2≤64, b(81-r^2)>0; for r^2≥81, b(r^2-64)>0; between those thresholds both are positive. Thus the denominator never vanishes. The quotient is smooth across both thresholds, one on the closed radius-eight ball and zero for radius at least nine. It is a single fixed real, radial, nonnegative compactly supported potential, independent of N and of kappa.

The real bounded symmetric sector perturbation has norm at most n^2 and preserves antisymmetry. The bounded-perturbation theorem gives the self-adjoint realization on D(T_n). The maximal Hilbert direct sum is self-adjoint on the square-summability domain displayed in the note. No uniform bound over all sectors is used. Unitariy conjugation of the bounded CAR operator is defined on all Fock space, regardless of whether it stays inside the CAR C*-algebra or preserves D(H).

Boundary hand controls: for n=0, both interactions vanish. For n=1, the normal-ordered interaction is identically zero, while the diagonal interaction is 1_Lambda. For n=2 with one particle in Lambda, the two interactions are 1 and 0; with both inside they are 4 and 2. These distinguish ordered pairs, diagonal subtraction and a missing half-factor.

## 2. Packing and quantifiers

The support of f lies in the radius-one-third closed ball. Q has x_1 between 7/4 and 9/4 and |x_2|,|x_3|<1/4, so every point has squared norm below 83/16<9 and is separated from supp f. The model bump phi has support [1/4,3/4]^3, compactly inside the unit cube. Its scaled translations sit strictly inside disjoint cells; hence all packed orbitals and f are orthonormal. The normalized wedge conventions give ||Psi_N||=||Xi_N||=1 and a(f)Psi_N=0 for every integer N≥1, including the first cell N=1.

With m=ceil(N^(1/3)), ell=1/(2m), each gradient norm squared scales as ell^-2. Since m≤2N^(1/3), their sum is at most 16||grad phi||^2 N^(5/3). For n=N+1, adding the fixed f contribution and all n normalization terms still gives the displayed C_0 n^(5/3). There is no density or energy cutoff; the kinetic cost grows with N. Thus the construction cannot by itself make any fixed-density/energy or fixed-state claim.

## 3. Smooth cutoff and leakage

The displayed chi equals one for r≤3 and zero for r≥7/2, hence is compactly supported inside Lambda and is one on every initial orbital support. Its denominator is positive by the same two-threshold argument. Write A=||Delta chi||_infinity, B=||grad chi||_infinity. Triangle and Cauchy–Schwarz give A||u||+2B||grad u||≤sqrt(A^2+4B^2)||u||_(H^1). No extra sqrt(2) is needed in the manuscript's constant.

Differentiating e^(-i(s-r)h) chi e^(-irh) on a smooth H^2 vector gives the stated commutator identity. Multiplication by chi preserves H^2; the free group preserves H^2 and the H^1 norm. Multiplying by q=1_(Lambda complement), using q chi=0 and chi g=g, yields ||q e^(-ish)g||≤C_chi |s| ||g||_(H^1). No derivative of the discontinuous indicator or kinetic confinement has been smuggled into this step. Both signs of s are covered by reversing the integral.

## 4. Slater second moment from occupied-space compression

Let A=PqP restricted to the n-dimensional occupied space, with eigenvalues p_j in [0,1]. A unitary rotation among the occupied orbitals changes their wedge only by a scalar phase, so choose orbitals diagonalizing A. Decomposing their q and (1-q) components then gives orthogonal inside/outside alternatives with leaked-number generating polynomial Π_j(1-p_j+p_j z). Therefore E M=Σ p_j=lambda and E M^2=lambda^2+lambda-Σ p_j^2. In a non-diagonal occupied basis this last sum is Tr(PqPq). This proves the identity by a different occupied-space calculation and identifies why it applies to free evolved Slaters.

Explicit two-orbital control: take g_1=sqrt(p)e_1+sqrt(1-p)e_3 and g_2=sqrt(q)e_2+sqrt(1-q)e_4, with q_out projection onto e_1,e_2. Then probabilities for M=0,1,2 are (1-p)(1-q), p(1-q)+q(1-p), pq; E M^2=p+q+2pq. This agrees with lambda^2+lambda-(p^2+q^2), including p,q=0 or 1.

Hypothesis-necessity control: a correlated superposition sqrt(1-epsilon)|all n inside>+sqrt(epsilon)|all n outside> has lambda=n epsilon and E M^2=n^2 epsilon. At epsilon=1/n it gives n, exceeding lambda+lambda^2=2 for n≥3. Hence using the Slater bound on arbitrary interacting or correlated states would fail. The note applies it only to free reference Slaters, so that attempted import exposes a necessary restriction already respected by its proof.

## 5. Two-sector Duhamel scaling

Writing L=n-M gives L(L-kappa)-n(n-kappa)=-M(2n-kappa-M). For 0≤M≤n and kappa=0,1, its magnitude is bounded by 2n M; the n=0 sector is zero separately. Sector boundedness makes Duhamel available without a common Fock-space perturbation norm. Reference evolution is a scalar phase times free evolution, so the second moment is used at free states only.

The leakage sum is lambda≤beta^2 s^2 n^(5/3). Its square-root bound is beta|s|n^(5/6)+beta^2s^2 n^(5/3). Multiplying by 2n and integrating gives beta n^(11/6)t^2+(2/3)beta^2 n^(8/3)|t|^3. For n=N or N+1 and t=pi/(2N+1-kappa)≤pi/(2N), the exponents are -1/6 and -1/3. Constants are independent of N and kappa, so both adjacent sectors converge together. Replacing only one sector, assuming the interacting state remains Slater, or assuming the changing free state stays near its initial vector would be unjustified; none is required by this comparison.

For general spatial dimension d, packing gives total H^1 cost n^(1+2/d) and these two errors become N^(-1/2+1/d), N^(-1+2/d). Both decay in d=3. They give constants in d=2 and growing powers in d=1, so this route does not settle those dimensions. This is a method limit, not a counterexample to a theorem restricted to dimension three.

## 6. CAR phase and maximality

For c_n=n(n-kappa), c_(N+1)-c_N=2N+1-kappa. Replacing the evolved bra and ket separately costs at most E_(N+1)+E_N because creation has norm one. Free covariance and inner products linear in the second argument give F_N^K(t)=exp(it(2N+1-kappa))<a*(f)Psi_N,a*(e^(ith)f)Psi_N>. CAR reduces the last factor to <f,e^(ith)f> because a(f)Psi_N=0. It does not require the evolved mode to be orthogonal to all occupied modes.

At the specified times the phase is exactly -1. The fixed mode overlap tends to one, with error at most |t| ||hf||. Hence <Psi_N,D_N Xi_N> tends to -2 after the appropriate conjugation. Since ||D_N||≤2, both norm limits follow by squeezing. The stronger vector claim follows from ||D_N Xi_N+2Psi_N||^2≤8+4 Re<Psi_N,D_N Xi_N>, and the changing vector-state values tend to four. Taking adjoints gives exactly the creation-difference norm, not a separately assumed estimate.

## 7. Topology and import limits

For any fixed eta and bounded B, split (U_t B U_t*-B)eta as U_t B(U_t*-1)eta+(U_t-1)B eta. Strong continuity of the two unitary groups yields the displayed fixed-vector limit. For fixed positive trace-class rho=Σ p_j|eta_j><eta_j|, each ||D_t eta_j||^2 tends to zero and is bounded by four; dominated convergence gives Tr(rho D_t*D_t)→0. Supremum over varying normal states need not commute with t→0. Choosing omega_N from a changing particle sector is precisely outside that fixed-state limit.

The source thus distinguishes point-norm continuity of the orbit of one fixed observable from strong continuity on every fixed vector. It does not establish a norm-continuous CAR dynamical system, CAR non-invariance, fixed-density thermodynamic evolution or a universal theorem for every potential/region. Actual OWR wording and the relationship to the earlier 2026 proof remain post-INITIAL primary-reading questions. The source's historical/priority assertions are hypotheses here, not imported findings.
