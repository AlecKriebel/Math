# Approach 4: direct cyclotomic calculation and a lattice obstruction

The preceding methods use general integral p-adic Hodge theory. This approach tests the conjecture through explicit crystalline characters, and asks whether decomposition into characters could supply a reduction.

## A rank-independent split-lattice theorem

Assume the chosen lattice, as an integral representation, is

\[
\Lambda=\bigoplus_{i=1}^d\mathbb Z_p(\psi_i\chi^{h_i}),
\]

where \(\chi\) is the cyclotomic character, each \(\psi_i\) is an unramified \(\mathbb Z_p^\times\)-valued character, and \(0\leq h_i\leq r\). These are crystalline representations in the convention fixed earlier. This is a condition on the actual lattice, not just on \(V=\Lambda[1/p]\).

Choose a finite unramified extension \(U/K\) killing all \(\psi_i\bmod p^n\). Every character is trivial on \(G_{U(\zeta_{p^n})}\), so

\[
L\subseteq U(\zeta_{p^n}).
\tag{1}
\]

Let \(M=U(\zeta_{p^n})\). For \(\zeta=\zeta_{p^n}\),

\[
\Phi_{p^n}'(\zeta)=\frac{p^n\zeta^{-1}}{\zeta^{p^{n-1}}-1},
\qquad v_K\bigl(\Phi_{p^n}'(\zeta)\bigr)
=e\left(n-\frac1{p-1}\right).
\tag{2}
\]

The denominator is a primitive \(p\)-th root minus one, with \(v_K=e/(p-1)\).

For completeness, the different bound from (2) does not assume \(\mathcal O_M=\mathcal O_U[\zeta]\). Let \(f\) be the minimal polynomial of \(\zeta\) over \(U\); it and the monic quotient \(g=\Phi_{p^n}/f\) lie in \(\mathcal O_U[X]\). The codifferent of the monogenic order \(A=\mathcal O_U[\zeta]\) is \(f'(\zeta)^{-1}A\). Since \(A\subseteq\mathcal O_M\), its trace dual contains the trace dual of \(\mathcal O_M\), so

\[
\mathcal D_{M/U}^{-1}\subseteq f'(\zeta)^{-1}\mathcal O_M,
\quad\text{hence}\quad
f'(\zeta)\mathcal O_M\subseteq\mathcal D_{M/U}.
\]

Moreover \(\Phi_{p^n}'(\zeta)=f'(\zeta)g(\zeta)\), with \(g(\zeta)\) integral. Therefore

\[
v_K(\mathcal D_{M/U})\leq
v_K(f'(\zeta))\leq e\left(n-\frac1{p-1}\right).
\tag{3}
\]

The extension \(U/K\) is unramified, and transitivity plus (1) yields

\[
v_K(\mathcal D_{L/K})\leq e\left(n-\frac1{p-1}\right)<B.
\tag{4}
\]

The last inequality follows because

\[
B-e(n-1/(p-1))
=1+e\left(a+b+\frac1{p-1}\right)-p^{-s}>0.
\]

This proves every integrally split case above, at arbitrary rank and arbitrarily large weights. It is an explicit calculation in a classical family, without a novelty claim.

## Rational splitting is not integral splitting

Fix \(m\geq1\) and let \(K=\mathbb Q_p(\zeta_{p^m})\), so
\(e_K=(p-1)p^{m-1}\). Take the rational crystalline representation

\[
V=\mathbb Q_p e_1\oplus\mathbb Q_p e_2,
\quad g(e_1)=\chi(g)e_1,\quad g(e_2)=e_2.
\]

Define the lattice

\[
\Lambda_m=\mathbb Z_p e_1\oplus\mathbb Z_p v,
\qquad v=(e_2-e_1)/p^m.
\]

Because \(\chi(g)\in1+p^m\mathbb Z_p\) for \(g\in G_K\), this is stable, and in the displayed integral basis

\[
\rho(g)=
\begin{pmatrix}
\chi(g)&(1-\chi(g))/p^m\\
0&1
\end{pmatrix}.
\tag{5}
\]

The kernel modulo \(p^n\) is exactly \(\chi(g)\equiv1\pmod{p^{m+n}}\), so the corresponding field is

\[
L=K(\zeta_{p^{m+n}}),
\qquad [L:K]=p^n.
\tag{6}
\]

For the standard split lattice, the field is instead \(K(\zeta_{p^n})\), which is even \(K\) when \(n\leq m\). Thus rational diagonalization cannot be used to assert (1) for an arbitrary stable lattice in the same rational representation.

Modulo \(p\), both diagonal characters of (5) are trivial, while its off-diagonal character is nontrivial and the inertia image has order \(p\). The semisimplification is trivial, but the original residual representation is wildly ramified. This is an actual crystalline example, not an abstract matrix that has not been realized by a local Galois group.

There is no counterexample to the proposed bound here. The classical cyclotomic different formula is

\[
v_{\mathbb Q_p}(\mathcal D_{\mathbb Q_p(\zeta_{p^q})/\mathbb Q_p})
=q-\frac1{p-1}\qquad(q\geq1).
\]

Subtracting the formulas at \(q=m+n\) and \(q=m\), and multiplying by \(e_K\), gives

\[
v_K(\mathcal D_{L/K})=e_Kn.
\]

For the weight bound \(r=1\), \(a=0,b=1/(p-1)\), so the remaining margin is

\[
B-e_Kn=1+\frac{e_K}{p-1}-p^{-n}>0.
\]

**Outcome:** a complete explicitly split-lattice theorem, and a concrete obstruction to reducing arbitrary crystalline lattices to their rational characters or residual semisimplification. The general extension/lattice problem remains.
