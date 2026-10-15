# Independent localization derivation

Audit target: original bounded_region_v2 author/BOUNDED_REGION_PROOF.md, SHA-256 2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350, 12,771 bytes. This reconstruction was completed before reading any old audit or candidate code. It is a verification of the supplied mechanism; no novelty is inferred.

## 1. Precisely defined operators

Use normalized exterior powers of h=L²(R³), and inner products linear in the second argument. On the n-particle sector, T_n is the restriction of -Σ_j Δ_j to the closed antisymmetric subspace. Its domain is H²(R^(3n)) intersected with that subspace. Permutations commute with the full Laplacian, so restriction to this reducing subspace is self-adjoint.

Let p=1_{B(0,4)} and q=1-p, L_n=Σ_j p_j and M_n=Σ_j q_j=n-L_n. They are bounded, permutation-invariant multiplication operators on each fixed sector. Set

\[
W_n^{(\sigma)}=L_n(L_n-\sigma),\quad
H_n^{(\sigma)}=T_n+W_n^{(\sigma)},\quad
K_n^{(\sigma)}=T_n+n(n-\sigma),\qquad \sigma\in\{0,1\}.
\]

For 0≤k≤n, k(k-σ) is real, nonnegative, and at most n². Thus H_n and K_n are self-adjoint on D(T_n) by the bounded self-adjoint perturbation argument. This does not require p, q, or W_n to map H² into H². The direct sum is self-adjoint on

\[
D(H)=\{(u_n):u_n\in D(H_n),\ \sum_n\|H_nu_n\|²<\infty\}.
\]

The direct-sum domain need not be equated with a more restrictive global kinetic/number intersection. The proof uses only fixed finite sectors. The vacuum is H_0=K_0=0.

Writing L_n=n-M_n gives the exact multiplication identity

\[
R_n:=H_n-K_n=-M_n(2n-\sigma-M_n).
\tag{L1}
\]

For every spectral value m∈{0,…,n}, 0≤2n-σ-m≤2n when n≥1, hence

\[
\|R_nu\|\le 2n\|M_nu\|.
\tag{L2}
\]

This holds for every u in the sector and is not a small global operator norm estimate: ||R_n|| can be O(n²).

## 2. The fixed bounded-region interaction is exact

The supplied b(s)=exp(-1/s) for s>0 and zero otherwise is C∞ on R. For r²≤64, b(81-r²)>0; for r²≥81, b(r²-64)>0; and between 64 and 81 both are positive. The denominator in the stated V is everywhere strictly positive. Therefore V is smooth, radial, real, even, between zero and one, equal to one on the closed B(0,8), and zero outside B(0,9).

Every difference x_i-x_j with x_i,x_j∈Λ=B(0,4) has length <8. Consequently, sectorwise,

\[
\sum_{i,j}p(x_i)p(x_j)V(x_i-x_j)=\left(\sum_i p(x_i)\right)^2=L_n².
\]

Deleting diagonal pairs gives L_n(L_n-1). The two definitions are rigorous multiplication operators, avoiding informal products of fields at coincident points. The kinetic operator still acts on all R³; there is no boundary condition or kinetic confinement to Λ.

## 3. Packing and a uniform H¹ sum

The fixed normalized f is smooth with support in the closed B(0,1/3), compactly contained in B(0,1/2). The cube Q centered at 2e_1 has side 1/2. Its furthest corner has distance sqrt((9/4)²+2(1/4)²)=sqrt(83)/4<3 from the origin; its nearest x_1 is 7/4, so it is disjoint from supp f.

For N≥1 choose m=ceil(N^(1/3)) and any N distinct subcubes in its m³ grid, as specified lexicographically by the candidate. The scaled compactly supported orbitals have support strictly inside their respective subcubes, including when subcubes share faces. Their normalization is unchanged by scaling, and disjoint supports give exact orthogonality. As m≤N^(1/3)+1≤2N^(1/3),

\[
\sum_{j=1}^N\|\nabla\psi_{j,N}\|²
=4Nm²\|\nabla\varphi\|²
\le16\|\nabla\varphi\|²N^{5/3}.
\tag{L3}
\]

Let E_φ=||∇φ||² and E_f=||∇f||². For either Ψ_N (n=N) or Ξ_N=f∧Ψ_N (n=N+1), with actual occupied orthonormal orbitals g_j,

\[
\sum_{j=1}^n\|g_j\|_{H¹}²
=n+\sum_j\|\nabla g_j\|²
\le Bn^{5/3},\quad B:=1+16E_\varphi+E_f.
\tag{L4}
\]

B is fixed. Every finite-N Slater is smooth and compactly supported in the finite configuration space, so belongs to D(T_n). H² norms may grow much faster than H¹ norms. The argument never uses their growth rate in a uniform estimate.

## 4. Cutoff commutator: domain and sign

One explicit admissible fixed cutoff is

\[
\chi(x)=\frac{b(49/4-|x|²)}{b(49/4-|x|²)+b(|x|²-9)}.
\]

It is one on the closed B(0,3), zero for |x|≥7/2, belongs to C_c∞(Λ), and satisfies 0≤χ≤1. Thus χg_j=g_j and qχ=0. Define

\[
a_\chi=\|\Delta\chi\|_\infty,\quad
b_\chi=\|\nabla\chi\|_\infty,\quad
C_\chi=(a_\chi²+4b_\chi²)^{1/2}.
\]

For u∈H²,

\[
[h,\chi]u=-(\Delta\chi)u-2\nabla\chi\cdot\nabla u,
\qquad \|[h,\chi]u\|\le C_\chi\|u\|_{H¹}.
\tag{L5}
\]

Put U(s)=exp(-ish). For fixed s and smooth g, differentiate in the strong L² sense

\[
F(r)=U(s-r)\chi U(r)g.
\]

U(r) preserves H², and multiplication by χ maps H² continuously into H². Therefore

\[
F'(r)=iU(s-r)[h,\chi]U(r)g,
\]

and the strongly continuous derivative is integrable on the interval between 0 and s. Integration with orientation yields, for either sign of s,

\[
U(s)\chi g-\chi U(s)g
=-i\int_0^s U(s-r)[h,\chi]U(r)g\,dr.
\tag{L6}
\]

The negative sign is correct. U(r) is an H¹ isometry by its Fourier multiplier exp(-ir|k|²). Applying L5 to L6 gives

\[
\|(1-\chi)U(s)g\|\le C_\chi|s|\|g\|_{H¹}.
\]

Since q vanishes where it is not outside Λ and χ=0 outside Λ, q=q(1-χ), and hence

\[
\|qU(s)g\|\le C_\chi|s|\|g\|_{H¹}.
\tag{L7}
\]

No commutator with the discontinuous indicator p or q is differentiated. Only the smooth fixed χ is differentiated. Arbitrarily fast Schrödinger tails are consistent with this small-norm leakage estimate.

## 5. Exact number fluctuation on the reference Slater

Free evolution U(s) preserves orbital orthonormality and maps a Slater to the Slater of the evolved orbitals. Scalar multiplication by exp(-isn(n-σ)) leaves its moments unchanged. Thus the K-reference state, not the H-interacting state, is the state to which the following identities apply.

Let P_s be the finite-rank occupied projection. Then

\[
\lambda_n(s)=\langle M_n\rangle=\operatorname{Tr}(P_sq)
=\sum_j\|qU(s)g_j\|²
\le\beta²s²n^{5/3},\qquad\beta:=C_\chi\sqrt B.
\tag{L8}
\]

To independently check the second moment, expand the normalized determinant's two-particle density: its direct term is P⊗P and its exchange term is (P⊗P) times the swap. With q²=q, the one-index terms in (Σq_j)² give Tr(Pq). The different-index terms give Tr(Pq)²-Tr(PqPq). Consequently

\[
\langle M_n²\rangle=\lambda²+\lambda-\operatorname{Tr}(PqPq).
\tag{L9}
\]

Equivalently C=PqP restricted to Ran(P) satisfies 0≤C≤1; if its eigenvalues are ν_1,…,ν_n, the variance is Σν_j(1-ν_j), between zero and λ. This gives a separate finite-matrix verification of the sign and exchange term. In particular,

\[
\|M_n\Phi_n(s)\|
\le\sqrt{\lambda+\lambda²}
\le\sqrt\lambda+\lambda
\le\beta|s|n^{5/6}+\beta²s²n^{5/3}.
\tag{L10}
\]

This is an actual second-moment bound. The weaker generic inequality M²≤nM would yield comparison growth O(N^(1/3)) at the chosen times and cannot replace L9. No assumption on the Slater nature of an interacting or mixed created state is used.

## 6. Strong Duhamel on each fixed sector

The perturbation R_n is bounded on the fixed sector. For u∈D(T_n), differentiate exp(-i(t-s)H_n)exp(-isK_n)u on the common domain and integrate. The resulting identity extends to all sector vectors by density and boundedness. Taking norms and using unitarity gives, for positive t,

\[
\|(e^{-itH_n}-e^{-itK_n})\Phi_n\|
\le\int_0^t\|R_ne^{-isK_n}\Phi_n\|\,ds.
\]

For negative t integrate the oriented interval and take absolute values. L2 and L10 therefore prove the universal estimate

\[
E_n(t)\le \beta n^{11/6}|t|²+\frac23\beta²n^{8/3}|t|³,
\quad n=N\text{ or }N+1,\ N\ge1,\ \sigma=0,1,\ t\in\mathbb R.
\tag{L11}
\]

The constant is independent of N, n, σ, and t. It depends only on the fixed f, φ, χ. The sectorwise n factors have not been silently replaced by an N-independent global perturbation norm.

Set t_N=π/(2N+1-σ)>0. Since t_N≤π/(2N) and n≤2N,

\[
E_n(t_N)\le C_1N^{-1/6}+C_2N^{-1/3},
\]

\[
C_1=\beta\,2^{11/6}\pi²/4,\qquad
C_2=\beta²\,2^{8/3}\pi³/12.
\tag{L12}
\]

Both powers tend to zero. This deduction holds for all N≥1, not just a numerically sampled subsequence.

## 7. Neighboring-sector phase and norm conclusion

Let A=a*(f), ||A||=1, Ξ_N=AΨ_N, and

\[
F_H(t)=\langle\Xi_N,e^{itH}Ae^{-itH}\Psi_N\rangle.
\]

With inner products linear in the second slot,

\[
F_H(t)=\langle e^{-itH_{N+1}}\Xi_N,Ae^{-itH_N}\Psi_N\rangle.
\]

Replacing both vectors separately by their K evolutions and using their unit norms gives

\[
|F_H(t)-F_K(t)|\le E_{N+1}(t)+E_N(t).
\tag{L13}
\]

Since K_n=T_n+c_n with c_n=n(n-σ), c_{N+1}-c_N=2N+1-σ. Free covariance and the CAR yield

\[
F_K(t)=e^{it(2N+1-\sigma)}\langle f,e^{ith}f\rangle.
\tag{L14}
\]

The CAR reduction uses only a(f)Ψ_N=0 at the initial time. It does not require the evolved f to be orthogonal to the packed orbitals. At t_N the scalar phase is -1. Since f∈D(h),

\[
|\langle f,e^{ith}f\rangle-1|\le\|(e^{ith}-1)f\|\le |t|\|hf\|.
\]

For D_N=e^{it_NH}a(f)e^{-it_NH}-a(f), adjunction gives

\[
\langle\Psi_N,D_N\Xi_N\rangle=\overline{F_H(t_N)-1}.
\]

Thus a useful quantitative version of the complete bridge is

\[
2\ge\|D_N\|\ge\|D_N\Xi_N\|
\ge2-2C_1N^{-1/6}-2C_2N^{-1/3}-\|hf\|\frac\pi{2N}.
\tag{L15}
\]

The lower bound may be negative for small N, which is harmless. It converges to 2 and the upper bound is the sharp triangle bound 2||a(f)||=2. The creation difference has the same norm because it is D_N*. The state expectation of D_N*D_N is exactly ||D_NΞ_N||² and tends to 4. Replacing t_N with -t_N also gives phase -1 and the same estimate.

## 8. Topology and units

For each fixed vector η and any bounded B, strong continuity of the unitary group gives

\[
\|(e^{itH}Be^{-itH}-B)\eta\|
\le\|B\|\|(e^{-itH}-1)\eta\|+\|(e^{itH}-1)B\eta\|\to0.
\]

There is no violation of strong-operator continuity or finite-sector norm continuity for the creation/annihilation blocks. Failure occurs in the Fock operator norm because the test vector and its particle sector depend on N. The relevant OWR meaning of strong continuity is pointwise norm continuity of the C*-algebra evolution, as explicitly distinguished on printed page 365 of the [official report](https://ems.press/content/serial-article-files/51350).

The equation h=-Δ uses mathematical units with ℏ=1 and the kinetic prefactor absorbed. Radii 4, 8, and 9 and plateau height 1 are fixed numerical choices in those units. No empirical prediction or physical calibration is asserted. The argument is three-dimensional; the packing exponent in d dimensions would be 1+2/d, giving errors N^(-1/2+1/d) and N^(-1+2/d). These decay only for d>2. This audit verifies d=3, not d=1 or d=2.
