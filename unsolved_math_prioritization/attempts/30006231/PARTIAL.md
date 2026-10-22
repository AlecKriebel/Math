# Finite-dimensional ground-state uniqueness: exact parameter tests and distinct state notions

**Problem 30006231 / OWR-14299094-001. Source-qualified partial results; separate review pending.** The finite-dimensional parameter test below is complete, including critical expectation values and degenerate ground spaces. The parameter geometry and semidefinite framework are credited prior mathematics. This attempt does not claim a new discovery or a complete answer to the dataset's expanded, ambiguous state-uniqueness request. The source's separate infinite-dimensional extension remains outside the result.

## 1. Exact source and classification hold

Penz's contribution, joint with van Leeuwen, in [OWR 15/2025, printed pp.626–629](https://ems.press/content/serial-article-files/51359?nt=1) assumes a finite complex Hilbert space, self-adjoint \(A,B_1,\ldots,B_m\), commuting \(B_i\), and linear independence of \(I,B_1,\ldots,B_m\). It asks uniqueness of the coupling parameter, proves the regular-value case, and cites degeneracy geometry for failures. Its explicitly open extension concerns infinite-dimensional Hilbert space. The dataset additionally asks for a unique ground-state representation, without specifying pure versus ensemble or uniqueness within a prescribed expectation fiber.

These distinctions matter even under all the original finite-dimensional hypotheses. Throughout, pure-state uniqueness means uniqueness of the rank-one projector, so scalar phase is ignored.

[Geometry of Degeneracy in Potential and Density Space, Quantum 7, 918 (2023)](https://quantum-journal.org/papers/q-2023-02-09-918/) supplies the weak common-ground-state theorem, degeneracy regions, and parameter nonuniqueness geometry. Appendices A–B of [arXiv:2206.12366v3 (2024)](https://arxiv.org/pdf/2206.12366v3) extend the discussion to complex Hamiltonians and arbitrary observables with linear coupling. Those appendices are absent from the journal version, as the publisher explicitly notes. [Constrained Search in Imaginary Time, Appendix A](https://arxiv.org/pdf/2504.05332v2), published as Phys. Rev. A 112, 032815 (2025), reproduces the finite-dimensional regular-value argument and explicitly distinguishes its pure-state discussion from an ensemble formulation.

The elementary criteria below are a self-contained semidefinite formulation, not a replacement claim for that literature. The maximal-support uniqueness test is the complex-Hermitian version of the standard SDP criterion in [Yinyu Ye, *Conic Linear Programming*, §2.5, Theorem 2.11](https://web.stanford.edu/class/msande310/sdpmain.pdf). We prove the version used here directly.

## 2. The complete representing-parameter set

Write
\[
H_\beta=A+\sum_{i=1}^m\beta_iB_i,\qquad
\mathcal D_b=\{\rho\succeq0:\operatorname{tr}\rho=1,\
                       \operatorname{tr}(B_i\rho)=b_i\}.
\]
Assume \(b\) is feasible. Define
\[
F(b)=\min_{\rho\in\mathcal D_b}\operatorname{tr}(A\rho),\qquad
\mathcal O_b=\{\rho\in\mathcal D_b:\operatorname{tr}(A\rho)=F(b)\}.
\]
Both minima and the nonempty optimal set exist by compactness. An ensemble represents \(b\) as a ground state of \(H_\beta\) precisely when it is supported on the lowest eigenspace of \(H_\beta\).

Put
\[
M_b(\beta)=A-F(b)I+\sum_i\beta_i(B_i-b_iI).
\tag{1}
\]

**Theorem 1.** The set of ensemble-ground-state representing parameters is exactly
\[
\mathcal R_b=\{\beta\in\mathbb R^m:M_b(\beta)\succeq0\}.
\tag{2}
\]
For every \(\beta\in\mathcal R_b\),
\[
\mathcal O_b
 =\{\rho\in\mathcal D_b:\operatorname{ran}\rho\subseteq\ker M_b(\beta)\}.
\tag{3}
\]
Consequently the complete ensemble fiber is independent of the choice of representing parameter.

**Proof.** If \(\rho\) is a representing ground state, then for every \(\sigma\in\mathcal D_b\),
\[
\operatorname{tr}(A\rho)+\beta\cdot b
 \le \operatorname{tr}(A\sigma)+\beta\cdot b.
\]
Thus \(\rho\in\mathcal O_b\), the ground energy is \(F(b)+\beta\cdot b\), and (1) is positive semidefinite.

Conversely, for any \(\rho\in\mathcal O_b\) and \(\beta\) satisfying (2),
\(\operatorname{tr}(M_b(\beta)\rho)=0\).
For positive semidefinite matrices \(M,\rho\), this equality implies
\(M\rho=0\): the positive matrix \(\rho^{1/2}M\rho^{1/2}\) has zero trace and hence is zero, so \(M^{1/2}\rho^{1/2}=0\).
Since \(\rho\) has trace one, the kernel is nonzero and its eigenvalue corresponds to the lowest energy. The same argument, in both directions, proves (3). \(\square\)

Let \(\widetilde F(b)\) denote the corresponding minimum over rank-one states, which exists in the source's commuting-observable setting. Replacing \(F(b)\) in (1) by \(\widetilde F(b)\) gives exactly the set \(\mathcal R_b^{\rm pure}\) of pure-ground-state representing parameters, by the same proof with a pure minimizer. In particular,
\[
\mathcal R_b^{\rm pure}=
\begin{cases}
\mathcal R_b,&\mathcal O_b\text{ contains a rank-one projector},\\
\varnothing,&\text{otherwise}.
\end{cases}
\tag{4}
\]
This does not assert that every ensemble-representable vector has a pure ground-state representative.

The \(B_i\) commute and \(I,B_i\) are independent, so their joint eigenvalue vectors affinely span \(\mathbb R^m\). Their convex hull \(\mathcal B\) is the common pure/ensemble expectation domain. For \(b\in\operatorname{int}\mathcal B\), the finite convex function \(F\) has a subgradient, and therefore \(\mathcal R_b\ne\varnothing\). On the boundary it may be empty. Formula (2) makes no interior or dual-attainment assumption.

## 3. An exact kernel test for parameter uniqueness

Fix a feasible \(\beta_0\), set \(M=M_b(\beta_0)\), and decompose
\[
\mathcal H=K\oplus K^\perp,\qquad K=\ker M.
\]
Let \(P,Q\) be the corresponding orthogonal projections. For \(d\in\mathbb R^m\), put
\[
D_d=\sum_i d_i(B_i-b_iI),\qquad C_d=(P D_d P)|_K .
\]

**Theorem 2.** The representing parameter \(\beta_0\) is unique if and only if there is no nonzero real \(d\) satisfying both
\[
C_d\succeq0,\qquad QD_dz=0\quad\text{for every }z\in\ker C_d.
\tag{5}
\]
This applies to all ensemble-representable \(b\), including critical values, and to pure representation whenever that exists.

The second condition is essential. Testing only positivity on the ground kernel, or only a first-order tangent cone, is insufficient.

**Proof.** We prove the finite-dimensional matrix fact
\[
M+tD\succeq0\text{ for some }t>0
\quad\Longleftrightarrow\quad
C=PDP|_K\succeq0,\quad QD(\ker C)=0.
\tag{6}
\]
Necessity of \(C\succeq0\) follows by restriction to \(K\). For \(z\in\ker C\),
\(\langle z,(M+tD)z\rangle=0\); positivity implies \((M+tD)z=0\), whence \(Dz=0\), in particular \(QDz=0\).

For sufficiency, let \(K_0=\ker C\) and \(K_1=K\ominus K_0\). The hypotheses imply \(D K_0=0\). Thus the full matrix is zero on \(K_0\) and has no couplings from that subspace. On \(K_1\oplus K^\perp\), it has block form
\[
\begin{pmatrix}
tC_1&tR^*\\
tR&M_Q+tD_Q
\end{pmatrix},
\tag{7}
\]
where \(C_1\) and \(M_Q\) are positive definite on their respective nonzero spaces. For sufficiently small \(t>0\), the lower block remains positive definite. Its Schur complement is
\[
tC_1-t^2R^*(M_Q+tD_Q)^{-1}R\succeq0
\]
for all sufficiently small \(t>0\), because the inverse remains bounded and \(C_1\) has a positive smallest eigenvalue. Empty blocks are simply omitted: if \(K_1=0\), there is only the positive lower block; if \(K^\perp=0\), there is just \(tC\). This proves (6).

If another parameter exists, take \(d=\beta_1-\beta_0\) and \(t=1\). Conversely (6) gives the distinct feasible parameter \(\beta_0+td\). Equation (4) handles pure representability. \(\square\)

For example,
\[
M=\begin{pmatrix}0&0\\0&1\end{pmatrix},\qquad
D=\begin{pmatrix}0&1\\1&0\end{pmatrix}
\]
has zero compression to \(\ker M\), but \(\det(M+tD)=-t^2<0\) for \(t\ne0\). This is itself a valid source example with \(A=M,B_1=D,b=0\): \(F(0)=0\), and \(\mathcal R_0=\{0\}\).

**Corollary 3 (nondegenerate ground state).** If \(K=\mathbb C\psi\), where \(\|\psi\|=1\) and \(g(\psi)=b\), then \(\beta_0\) is unique precisely when
\[
\psi,B_1\psi,\ldots,B_m\psi
\quad\text{are linearly independent}.
\tag{8}
\]
Indeed \(\langle\psi,D_d\psi\rangle=0\) for every \(d\), so (5) reduces to \(D_d\psi=0\). For the commuting Hermitian observables, the Gram matrix of the listed vectors is real. Therefore a complex dependence yields a real dependence. Taking its inner product with \(\psi\) converts it to \(D_d\psi=0\) with nonzero \(d\). Conversely such a direction is a dependence. The spectral-gap step in (6) supplies the converse that is unavailable from an eigenvector equation alone.

Condition (8) concerns this ground state. A regular expectation value requires every pure state in its expectation fiber to be regular, which is stronger.

## 4. Ensemble uniqueness and the precise pure-state distinction

Choose \(\rho_*\in\mathcal O_b\) of maximal rank, and let \(S=\operatorname{ran}\rho_*\). Such a state exists because ranks are integers in a finite range.

**Theorem 4.** If \(\mathcal R_b\ne\varnothing\), there is a unique ensemble ground-state representative of \(b\) if and only if
\[
X=X^*,\quad X=P_SXP_S,\quad
\operatorname{tr}X=0,\quad
\operatorname{tr}(B_iX)=0\ (1\le i\le m)
\quad\Longrightarrow\quad X=0.
\tag{9}
\]

**Proof.** Every optimal state has range in \(S\). Otherwise its average with \(\rho_*\) has larger rank, because the kernel of a sum of positive semidefinite matrices is the intersection of their kernels. For a representing parameter, (3) also gives \(S\subseteq K\), so
\[
\operatorname{tr}(AX)=F(b)\operatorname{tr}X-
\sum_i\beta_i\operatorname{tr}((B_i-b_iI)X)=0
\]
for any \(X\) satisfying (9). If such a nonzero \(X\) exists, \(\rho_*\) is positive definite on \(S\); thus \(\rho_*\pm\epsilon X\) are distinct optimal density matrices for sufficiently small positive \(\epsilon\). Conversely two distinct optimal states have a nonzero difference satisfying (9). \(\square\)

This is a real-linear injectivity test on the Hermitian matrices on \(S\). In particular ensemble uniqueness requires \((\dim S)^2\le m+1\). It is not a test for uniqueness of a pure state. Pure representatives are precisely the rank-one members of (3); a unique pure member can coexist with additional mixed members.

Here is an example satisfying every original hypothesis. On \(\mathbb C^7\), define the \(7\times2\) isometry
\[
V=\begin{pmatrix}
1/\sqrt6&1/\sqrt6\\
1/\sqrt6&-1/\sqrt6\\
1/\sqrt6&-i/\sqrt6\\
1/\sqrt6&i/\sqrt6\\
1/\sqrt3&0\\
0&1/\sqrt3\\
0&0
\end{pmatrix},
\quad
B_1=\operatorname{diag}(1,-1,0,0,0,0,0),
\]
\[
B_2=\operatorname{diag}(0,0,1,-1,0,0,0),\qquad
B_3=\operatorname{diag}(0,0,0,0,1,-1,0).
\]
Let \(e=e_7\), \(A=I-VV^*-ee^*\), and \(b=(0,0,0)\). The \(B_i\) commute and \(I,B_1,B_2,B_3\) are independent. The expectation domain is the octahedron with vertices \(\pm e_1,\pm e_2,\pm e_3\), so \(b\) is interior. Direct multiplication gives
\[
V^*V=I_2,\qquad V^*B_iV=\sigma_i/3,
\tag{10}
\]
with the three Pauli matrices. The ground space of \(A\) is
\(K=\operatorname{ran}V\oplus\mathbb Ce\).

A normalized ground vector has form \(V\xi+ze\). Its expectation is
\(\frac13(\xi^*\sigma_1\xi,\xi^*\sigma_2\xi,\xi^*\sigma_3\xi)\), whose squared Euclidean norm is \(\|\xi\|^4/9\). Hence \(e\), up to phase, is its unique pure representative of \(b\). Nevertheless both
\[
ee^*,\qquad \tfrac12 VV^*
\tag{11}
\]
are different ensemble representatives. Also \(\beta=0\) is the unique representing parameter: the compression of \(D_d\) to \(K\) is \((d\cdot\sigma)/3\oplus0\), which is indefinite for every \(d\ne0\). Theorem 2 applies. Finally \(b\) is a critical value because the state \(e\) is critical.

This construction is an elementary compression of commuting diagonal observables to Pauli matrices; it is a diagnostic example, without a historical-priority claim. It prevents substituting ensemble uniqueness for the dataset's unspecified pure-state uniqueness.

## 5. Boundary and critical-value controls

The following small examples further separate the quantifiers. All have commuting observables and independent identity/observable lists.

1. **Unique parameter, many pure states.** Let \(A=0\), \(B=\operatorname{diag}(-1,0,1)\), \(b=0\). Then \(F(0)=0\), and (2) gives only \(\beta=0\). Both \(e_2\) and \((e_1+e_3)/\sqrt2\), among others, are pure representatives.

2. **A unique state, many parameters.** Let \(A=B=\operatorname{diag}(0,1)\), \(b=0\). The only feasible density matrix is \(e_1e_1^*\), while \(\mathcal R_0=[-1,\infty)\). For every \(\beta>-1\), the Hamiltonian has a nondegenerate ground state. Thus a unique ground state does not imply a unique parameter.

3. **Critical value with both parameter and ensemble uniqueness.** Let \(B=\operatorname{diag}(-1,0,1)\), \(\psi=(e_1+e_3)/\sqrt2\), \(A=-\psi\psi^*\), \(b=0\). The optimal state is uniquely \(\psi\psi^*\). Its ground state at \(\beta=0\) is nondegenerate, and \(\psi,B\psi\) are independent, so Corollary 3 gives parameter uniqueness. Yet \(b\) is a critical value because \(e_2\) lies in the same expectation fiber and is critical.

4. **A boundary point with no finite representing parameter.** Let
\[
A=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
B=\begin{pmatrix}0&0\\0&1\end{pmatrix},\qquad b=0.
\]
The only feasible state is \(e_1e_1^*\), and \(F(0)=0\). But
\(\det M_0(\beta)=-1\), so \(\mathcal R_0=\varnothing\).
Compactness of the constrained state search does not force attainment in parameter space.

## 6. What this attempt establishes, and what it leaves open

Equations (2), (5), and (9) are exact, with full proofs; they require no genericity, strict complementarity, or nonsingular ground space. They characterize finite-dimensional ensemble parameter/state uniqueness once the constrained optimum and a maximal-support optimal state are supplied. Equation (4) gives the exact relation to pure representability. The critical and boundary examples are exact.

The general pure-state fiber still contains a rank-one feasibility condition. This note does not replace that condition by a new geometric classification or claim that the dataset's state-uniqueness addition has been fully resolved. Nor does it prove the source's infinite-dimensional extension. A separate review should assess the source correction independently of the supplemental deductions.

Recommended conservative campaign outcome: **unsolved, 2/5 substantive routes**, with an explicit source-status correction recording that the regular-value theorem and degeneracy geometry are prior results. No new theorem priority is asserted. Numerical or exact finite controls supplement, rather than establish, the universal matrix arguments.

