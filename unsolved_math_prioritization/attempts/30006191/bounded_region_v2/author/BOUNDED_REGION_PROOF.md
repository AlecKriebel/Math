# A bounded-region counterexample for continuum fermions

Problem 30006191 / OWR-14299085-005. Author-stage revision 2, 7 October 2026.

## Claim, scope, and relationship to the literature

We give a self-contained proof for the spatially restricted interaction appearing in the Oberwolfach question: the kinetic energy acts on all of \(\mathbb R^3\), while both interaction variables lie in one fixed bounded region \(\Lambda\). The interaction potential is smooth, nonnegative, even, and compactly supported. No ultraviolet smearing is used. The orbit of one fixed annihilation operator fails pointwise operator-norm continuity, with norm differences tending to the maximum possible value.

The question and its topology are documented on printed pages 364–365 and 371 of [Oberwolfach Report 7/2025](https://ems.press/content/serial-article-files/51350), DOI [10.4171/owr/2025/7](https://doi.org/10.4171/owr/2025/7). Oliver Siebert's [*Discontinuity of Continuum Fermion Dynamics*, arXiv:2609.34402v1](https://arxiv.org/abs/2609.34402v1) supplies relevant full-space results. Its full-space theorem alone does not establish the bounded-region claim proved below. We make no assertion of priority over all existing literature.

### Theorem

Let \(\mathfrak h=L^2(\mathbb R^3)\), \(h=-\Delta\), and \(\mathcal F=\bigoplus_{n\ge0}\bigwedge^n\mathfrak h\). Set \(\Lambda=B(0,4)\) and \(L=d\Gamma(1_\Lambda)\). There exists a real even \(V\in C_c^\infty(\mathbb R^3)\), \(0\le V\le1\), equal to one on \(\Lambda-\Lambda\), such that the density-density interaction in \(\Lambda\times\Lambda\) is \(L^2\).

For \(\sigma\in\{0,1\}\), define sectorwise

\[
H^{(\sigma)}=d\Gamma(h)+L(L-\sigma).
\]

Here \(\sigma=0\) is the density-density convention including diagonal pairs; \(\sigma=1\) is the normal-ordered convention. There are a fixed normalized \(f\in C_c^\infty(B(0,1/2))\) and explicitly specified unit Slater states \(\Xi_N\in\bigwedge^{N+1}\mathfrak h\) such that, with

\[
t_N^{(\sigma)}=\frac{\pi}{2N+1-\sigma},\qquad
D_N^{(\sigma)}=e^{it_N^{(\sigma)}H^{(\sigma)}}a(f)e^{-it_N^{(\sigma)}H^{(\sigma)}}-a(f),
\]

one has

\[
\lim_{N\to\infty}\|D_N^{(\sigma)}\Xi_N\|=2,
\qquad
\lim_{N\to\infty}\|D_N^{(\sigma)}\|=2.
\]

The same operator-norm conclusion holds for \(a^*(f)\). In particular, the Heisenberg orbit is not norm-continuous at zero.

## 1. Explicit potential and self-adjoint Hamiltonians

Write \(b(s)=e^{-1/s}\) for \(s>0\), and \(b(s)=0\) for \(s\le0\). Define

\[
V(x)=\frac{b(81-|x|^2)}{b(81-|x|^2)+b(|x|^2-64)}.
\]

The denominator never vanishes. This is a smooth radial function, equal to one when \(|x|\le8\), zero when \(|x|\ge9\), and between zero and one elsewhere. Hence \(V=1\) on \(\Lambda-\Lambda=B(0,8)\).

On the \(n\)-particle sector, let

\[
T_n=\sum_{j=1}^n h_j,\qquad L_n=\sum_{j=1}^n1_\Lambda(x_j),\qquad M_n=n-L_n.
\]

The rigorous density-density multiplication operator is

\[
\sum_{i,j=1}^n1_\Lambda(x_i)1_\Lambda(x_j)V(x_i-x_j)=L_n^2.
\]

Omitting \(i=j\) instead gives \(L_n(L_n-1)\). This defines both field-expression conventions without multiplying distribution-valued fields informally.

Define

\[
H_n^{(\sigma)}=T_n+L_n(L_n-\sigma),\qquad
K_n^{(\sigma)}=T_n+n(n-\sigma).
\]

The sector potentials are real bounded multiplication operators, of norm at most \(n^2\), so the sector Hamiltonians are self-adjoint on \(D(T_n)\). Their direct sums are self-adjoint on their maximal direct-sum domains. The vacuum-sector operators are zero. In particular the Fock-space Heisenberg evolutions exist on \(B(\mathcal F)\). No claim that they preserve the CAR algebra is needed.

Because \(M_n\) has spectrum in \(\{0,\ldots,n\}\),

\[
H_n^{(\sigma)}-K_n^{(\sigma)}
=-M_n(2n-\sigma-M_n),
\qquad
\|(H_n^{(\sigma)}-K_n^{(\sigma)})\Phi\|\le2n\|M_n\Phi\|.
\tag{1}
\]

For \(\sigma=0,1\), the factor \(2n-\sigma-M_n\) is nonnegative and at most \(2n\), for every \(n\ge1\). The comparison operator \(K\) is only a proof device; the claimed example is \(H\), with the fixed bounded interaction region.

## 2. Packed initial Slaters

Take \(f(x)=c_f b(1-9|x|^2)\), where \(c_f>0\) normalizes the \(L^2\) norm. Its support is the closed ball of radius \(1/3\), so \(f\in C_c^\infty(B(0,1/2))\). Let

\[
Q=2e_1+(-1/4,1/4)^3,
\]

which is disjoint from \(\operatorname{supp}f\) and contained in \(B(0,3)\). Fix a normalized \(\varphi\in C_c^\infty((0,1)^3)\); for example, normalize the product \(\prod_{k=1}^3 b(1-16(x_k-1/2)^2)\).

For \(N\ge1\), subdivide \(Q\) into \(m_N^3\) cubes, where \(m_N=\lceil N^{1/3}\rceil\). Choose the first \(N\) in lexicographic order. If \(c_{j,N}\) is the lower corner of the \(j\)-th selected cube and \(\ell_N=(2m_N)^{-1}\), put

\[
\psi_{j,N}(x)=\ell_N^{-3/2}\varphi((x-c_{j,N})/\ell_N),
\qquad 1\le j\le N.
\]

These orbitals have disjoint supports, are normalized and mutually orthogonal, and are orthogonal to \(f\). Their kinetic energies satisfy

\[
\sum_{j=1}^N\|\nabla\psi_{j,N}\|^2
=N\ell_N^{-2}\|\nabla\varphi\|^2
\le C N^{5/3},
\tag{2}
\]

using \(m_N\le2N^{1/3}\). Let

\[
\Psi_N=\psi_{1,N}\wedge\cdots\wedge\psi_{N,N},\qquad
\Xi_N=a^*(f)\Psi_N.
\]

Our exterior products use the normalized Slater convention. Both vectors have norm one. Adding the fixed orbital \(f\) preserves the kinetic-energy bound with \((N+1)^{5/3}\) on the right and a uniform constant. The orbitals of both Slaters lie in \(B(0,3)\).

## 3. Free leakage, with uniform constants

Choose a fixed real \(\chi\in C_c^\infty(\Lambda)\), \(0\le\chi\le1\), equal to one on \(B(0,3)\). Set \(q=1_{\Lambda^c}\). If \(g\in C_c^\infty\) is one of the initial orbitals, then \(\chi g=g\). The free group is isometric on \(H^1\), and

\[
[h,\chi]u=-(\Delta\chi)u-2\nabla\chi\cdot\nabla u,
\qquad
\|[h,\chi]u\|\le C_\chi\|u\|_{H^1}.
\tag{3}
\]

For these smooth \(g\), the commutator Duhamel identity gives

\[
(e^{-ish}\chi-\chi e^{-ish})g
=-i\int_0^s e^{-i(s-r)h}[h,\chi]e^{-irh}g\,dr.
\tag{4}
\]

To justify (4), differentiate \(e^{-i(s-r)h}\chi e^{-irh}g\). The free evolution preserves \(H^2\), multiplication by \(\chi\) maps \(H^2\) to itself, and the derivative is strongly integrable. Formula (3) then bounds the integral using only the \(H^1\) norm of \(g\), irrespective of its larger \(H^2\) norm. Thus the constants do not depend on the packed orbital or on \(N\).

Since \(q\chi=0\), equations (3)–(4) imply

\[
\|qe^{-ish}g\|
\le\|(1-\chi)e^{-ish}g\|
\le C_\chi |s|\|g\|_{H^1}.
\tag{5}
\]

Let \(\Phi_n\) denote either initial Slater above, with its actual particle number \(n=N\) or \(n=N+1\), and let \(\Phi_n(s)=e^{-isT_n}\Phi_n\). Free evolution preserves the Slater structure and orbital orthonormality. Its mean number of particles outside \(\Lambda\) is therefore

\[
\lambda_n(s):=\langle\Phi_n(s),M_n\Phi_n(s)\rangle
=\sum_{j=1}^n\|qe^{-ish}g_j\|^2
\le C s^2n^{5/3}.
\tag{6}
\]

The last constant is uniform over both families, by (2) and the fixed contribution of \(f\).

## 4. The Slater variance estimate

For any normalized Slater with occupied-space projection \(P=\sum_{j=1}^n|g_j\rangle\langle g_j|\), the first and second moments of \(M=d\Gamma(q)\) are

\[
\langle M\rangle=\operatorname{Tr}(Pq)=\lambda,
\qquad
\langle M^2\rangle=\lambda^2+\operatorname{Tr}(Pq)-\operatorname{Tr}(PqPq).
\tag{7}
\]

Indeed, the diagonal terms in \(M^2\) give \(\sum_j\langle g_j,qg_j\rangle\), because \(q^2=q\). Expanding the two-particle marginal of a Slater gives the off-diagonal terms

\[
\sum_{j\ne k}
\bigl(\langle g_j,qg_j\rangle\langle g_k,qg_k\rangle
-|\langle g_j,qg_k\rangle|^2\bigr).
\]

Adding diagonal and off-diagonal contributions proves (7). All traces are finite because \(P\) has rank \(n\). Consequently

\[
\operatorname{Var}(M)=\operatorname{Tr}(Pq(1-P)q)\le\lambda,
\qquad
\|M\Phi\|\le\sqrt{\lambda+\lambda^2}\le\sqrt\lambda+\lambda.
\tag{8}
\]

Applying this to the freely evolved Slaters and (6) yields

\[
\|M_n\Phi_n(s)\|\le C\bigl(|s|n^{5/6}+s^2n^{5/3}\bigr).
\tag{9}
\]

This second-moment control is essential: bounding only the probability of leakage without controlling the leaked number would not justify the following comparison.

## 5. Comparison with the constant-number reference

On each fixed sector, the difference \(H_n^{(\sigma)}-K_n^{(\sigma)}\) is bounded. The standard strong Duhamel identity therefore holds for all vectors; on the smooth initial Slaters it can also be obtained by differentiating the product of the two unitary groups on their common domain \(D(T_n)\). It gives, for \(t\ge0\),

\[
\begin{split}
E_n(t)&:=\|(e^{-itH_n^{(\sigma)}}-e^{-itK_n^{(\sigma)}})\Phi_n\|\\
&\le\int_0^t\|(H_n^{(\sigma)}-K_n^{(\sigma)})e^{-isK_n^{(\sigma)}}\Phi_n\|\,ds\\
&\le2n\int_0^t\|M_n\Phi_n(s)\|\,ds\\
&\le C\bigl(n^{11/6}t^2+n^{8/3}t^3\bigr).
\end{split}
\tag{10}
\]

In the third line, reference evolution differs from free evolution only by the scalar phase \(e^{-isn(n-\sigma)}\). Thus it is the free Slater to which (9) applies; no interacting state is incorrectly assumed to remain Slater.

At \(t=t_N^{(\sigma)}\), for both \(n=N\) and \(n=N+1\),

\[
E_n(t_N^{(\sigma)})\le C\bigl(N^{-1/6}+N^{-1/3}\bigr)\longrightarrow0.
\tag{11}
\]

The dimension-three powers follow directly from the packing energy. More generally this argument works for \(d>2\), with the two exponents \(-1/2+1/d\) and \(-1+2/d\). No conclusion in dimensions one or two is claimed by this estimate.

## 6. Matrix element and the maximal norm discontinuity

Use inner products linear in the second variable. Set \(A=a^*(f)\), so \(\|A\|=1\) and \(A\Psi_N=\Xi_N\). Define

\[
F_N^H(t)=\langle\Xi_N,e^{itH^{(\sigma)}}Ae^{-itH^{(\sigma)}}\Psi_N\rangle.
\]

Move both unitary groups to the vectors. Replacing the evolved \(\Xi_N\) and the evolved \(\Psi_N\) separately by their reference evolutions gives

\[
|F_N^H(t)-F_N^K(t)|\le E_{N+1}(t)+E_N(t),
\tag{12}
\]

since both groups are unitary and \(\|A\|=1\). This comparison does not require estimating a mixed state obtained by creating a particle in an already evolved interacting state.

For \(K^{(\sigma)}=d\Gamma(h)+\mathcal N(\mathcal N-\sigma)\), where \(\mathcal N\) is the total number operator, the sector difference of the scalar energies is \(2N+1-\sigma\). Free covariance and the CAR give

\[
F_N^K(t)=e^{it(2N+1-\sigma)}
\langle a^*(f)\Psi_N,a^*(e^{ith}f)\Psi_N\rangle
=e^{it(2N+1-\sigma)}\langle f,e^{ith}f\rangle.
\tag{13}
\]

For the last equality, use \(a(f)\Psi_N=0\) and
\(a(f)a^*(g)=\langle f,g\rangle-a^*(g)a(f)\). No orthogonality between \(e^{ith}f\) and the occupied orbitals is required.

Our choice of \(t_N^{(\sigma)}\) makes the phase in (13) exactly \(-1\). Strong continuity of the one-particle free group implies \(\langle f,e^{it_N^{(\sigma)}h}f\rangle\to1\). Equations (11)–(13) therefore show

\[
F_N^H(t_N^{(\sigma)})\longrightarrow-1.
\]

At time zero the matrix element is \(\langle\Xi_N,A\Psi_N\rangle=1\). Hence

\[
2\ge\|e^{it_NH^{(\sigma)}}Ae^{-it_NH^{(\sigma)}}-A\|
\ge|F_N^H(t_N)-1|\longrightarrow2.
\tag{14}
\]

Here and below \(t_N=t_N^{(\sigma)}\). Taking adjoints gives the same operator norm for the annihilation difference \(D_N^{(\sigma)}\). More precisely,

\[
\langle\Psi_N,D_N^{(\sigma)}\Xi_N\rangle
=\overline{F_N^H(t_N)-1}\longrightarrow-2,
\]

so \(2\ge\|D_N^{(\sigma)}\Xi_N\|\ge|F_N^H(t_N)-1|\to2\), proving every assertion of the theorem. \(\square\)

## 7. Explicit states, topology, and limitations

The normalized vector states

\[
\omega_N(B)=\langle\Xi_N,B\Xi_N\rangle
\]

satisfy \(\omega_N((D_N^{(\sigma)})^*D_N^{(\sigma)})\to4\). They exhibit the requested state-level witness. Both the interaction region and \(f\) are fixed; only the particle number, packed Slater state, and observation time vary.

There is no fixed-vector discontinuity. For any self-adjoint \(H\), bounded \(B\), and fixed vector \(\eta\),

\[
\|(e^{itH}Be^{-itH}-B)\eta\|
\le\|B\|\|(e^{-itH}-1)\eta\|+\|(e^{itH}-1)B\eta\|\to0.
\]

Thus the strong-operator topology remains continuous. The theorem concerns the stronger, pointwise operator-norm notion intended in the OWR discussion.

The construction proves an existential counterexample for one bounded ball and one smooth compactly supported potential. It does not prove failure for every potential, every bounded region, fixed-density thermodynamic states, or nonrelativistic dimensions one and two. It also does not prove non-invariance of the CAR algebra; that is unnecessary for the question addressed here.

This proof is one substantive mathematical approach: localized Slater packing, free leakage control, and sectorwise comparison with a number-dependent phase. Source retrieval, provenance checks, and packet assembly do not count as additional approaches. The result remains an author-stage candidate pending two independent audits.
