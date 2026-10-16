# Independent reconstruction before saved review verdicts

Claim under review: for the fixed ball B4 in R3, ordered-pair density interaction with smooth plateau potential V, the orbit of one fixed annihilator has norm difference tending to 2 on times pi/(2N+1-k), k=0 or 1. The witnesses may change their particle number and energy. This is an existence claim in B(Fock), not an invariance claim about the CAR algebra.

The potential formula is smooth because its denominator never vanishes. For |x|<=8 the numerator is positive and the second summand zero; for |x|>=9 the numerator zero and second summand positive. Thus the density multiplication operator really is L^2; removing diagonal pairs gives L(L-1). The sector operators are bounded perturbations of the full-space Laplacian and their maximal direct sum is self-adjoint. No boundary condition at B4 is inserted.

All packed orbitals lie in a fixed cube with closure inside B3 and avoid f. Each is normalized; disjoint support makes them orthogonal. For m=ceil(N^(1/3)), ell=1/(2m), total gradient energy is 4Nm^2||grad phi||^2 <=16||grad phi||^2 N^(5/3). Adding the fixed f changes only a fixed constant. This explains the dimension restriction.

For chi=1 on B3 and supported inside B4, [h,chi]=-(Delta chi)-2 grad chi dot grad. Cauchy-Schwarz on the two H1 components gives the stated C_chi. The commutator Duhamel identity is valid on smooth H2 vectors and estimates only H1. Multiplying the identity by the outside projection q yields ||q exp(-ish)g||<=C_chi|s|||g||_H1. Neither q nor the interaction indicator is differentiated.

For the free evolved determinant, let B be the occupied-orbital matrix B_jk=<g_j,qg_k>. It is Hermitian with 0<=B<=I. Direct two-body contraction gives E[M^2]=(Tr B)^2+Tr B-Tr(B^2). In particular Var M<=E M. The mean is the sum of squared free leakage norms, <= beta^2 s^2 n^(5/3). Therefore ||M Phi(s)||<=beta|s|n^(5/6)+beta^2s^2n^(5/3). This reasoning applies to free Slaters only.

Writing M=n-L, H-K=-M(2n-k-M). For n>=1 and M in {0,...,n}, |2n-k-M|<=2n. Duhamel along the free reference, whose extra number term is scalar on each sector, gives E_n(t)<=beta n^(11/6)t^2+(2/3)beta^2 n^(8/3)|t|^3. For both n=N,N+1 and t<=pi/(2N), the terms have exponents -1/6 and -1/3. Their smallness does not require exp(-itT_n)Phi_n to approach Phi_n.

For A=a*(f), reference covariance gives exp(itK) A exp(-itK) on sector N as exp(it(2N+1-k))a*(exp(ith)f). The scalar is -1 at the chosen time. Since a(f)Psi=0, <a*(f)Psi,a*(g)Psi>=<f,g> for any g; no orthogonality of g to the occupied orbitals is needed. Taking the adjoint matrix element gives <Psi,D Xi> -> -2. Bounds ||D||<=2 and ||Psi||=||Xi||=1 force ||D Xi||->2 and ||D Xi+2Psi||->0. Creation follows by adjoint, and the varying vector-state value is ||D Xi||^2->4.

For a fixed vector, the strong unitary groups and boundedness of the annihilator give continuity by splitting the difference into two terms. For a fixed normal state, spectral decomposition and the uniform bound 4 give dominated convergence. This is consistent with the varying witnesses. Vacuum and N=1 are harmless; the proof uses N>=1 and needs no n=0 division. The mechanism does not yield decay in dimension two or one, and no conclusion there is drawn.

Strongest conclusion at this stage: the written continuum theorem has a complete chain of estimates under its explicit conventions. Priority and package publication readiness are separate questions, still unassessed.
