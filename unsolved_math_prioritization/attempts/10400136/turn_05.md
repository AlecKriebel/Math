# A conditional Chern Simons transfer route for Problem 7.21

This route gives an explicit peripheral cancellation and a rigorous conditional transfer criterion. It does not prove the missing comparison or surgery theorem, and therefore does not solve the original problem.

## Starting point

Fix odd \(N>1\). For \(X=(W,L,\rho)\) in the original scope, Baseilhac–Benedetti prove

\[
K_N(X)=H(T_N)^N.
\]

See [QHI Theory I, Theorem 5.2](https://arxiv.org/pdf/math/0201240). Consequently, the required refinement is a geometrically meaningful choice among these roots, invariant under changes of presentation preserving specified extra structure. Choosing an arbitrary numerical root of \(K_N\) does not explain the state-sum phase.

McPhail-Snyder’s phase-unambiguous \(Z_N^\psi\) suggests such a choice. However, [§1.6.1, p. 8](https://arxiv.org/pdf/2509.02365) gives its comparison with BB only as an expectation. Moreover, §1.2, p. 4 explicitly leaves extension from tangle/link exteriors to general three-manifolds open.

## An actual cancellation

Use the knot-exterior notation \(C(\mu)=I^\psi(K,\rho,\mu)\ne0\), \(Z(\mu)=Z_N^\psi(K,\rho,\mu)\), and longitude eigenvalue \(\ell\ne0\). The preprint’s equations (1.1) and (1.3), pp. 3–4, imply

\[
C(\mu+1)=\ell^2C(\mu),\qquad
Z(\mu+N)=\ell^{-2}Z(\mu).
\]

Choose \(r(\mu)^N=C(\mu)\), transporting this root along an \(N\)-step logarithmic orbit by

\[
r(\mu+N)=\ell^2r(\mu).
\]

This is consistent because \(C(\mu+N)=\ell^{2N}C(\mu)\). Therefore

\[
F(\mu):=r(\mu)Z(\mu),\qquad F(\mu+N)=F(\mu).
\]

Thus a positive \(N\)th-root Chern–Simons factor cancels this particular peripheral multiplier exactly. Arbitrarily selecting roots independently would instead leave a multiplier in \(\mu_N\). Nothing here proves invariance under \(\mu\mapsto\mu+1\), changes of framing, or filling. The remaining logarithmic class modulo \(N\) is plausible extra data, not something this calculation removes.

A global root need not exist. On a connected parameter manifold \(U\) with continuous \(C:U\to\mathbb C^\times\), the covering-space lifting criterion says that \(r^N=C\) has a continuous solution exactly when every loop has \(C\)-winding divisible by \(N\). Indeed, continuation around winding \(w\) multiplies the root by \(\exp(2\pi iw/N)\). The pullback cover \(\{(u,r):r^N=C(u)\}\) supplies a concrete extra structure defined independently of \(K_N\). This resolves parameter monodromy on that cover; it does not establish compatibility with surgery moves.

## Conditional transfer proposition

Present \(X\) by surgery on a framed link \(J\subset S^3\), with a disjoint diagram representing \(L\). Pull back \(\rho\) to the complement. Let \(e\) comprise independently defined geometric data, including coherent root transport for the Chern–Simons line. Assume a presentation calculus connects all presentations of \((X,e)\), and suppose it supplies:

1. A scalar \(Z_p\), obtained by contracting the \(Z_N^\psi\) operators with explicitly specified filling tensors; a nonzero classical factor \(C_p\), including filling corrections; and a root \(r_p^N=C_p\) determined by \(e\).
2. An explicit nonzero normalization \(a_p\), prescribed independently of \(K_N\), satisfying the comparison
   \[
   K_N(X)=a_p^N C_p Z_p^N.
   \]
3. For every generating move \(m:p\to p'\), exact identities
   \[
   r_{p'}=u_mr_p,\quad Z_{p'}=v_mZ_p,
   \quad a_{p'}u_mv_m=a_p,
   \]
   with coherent transport around every relation in the calculus.

Then \(\widetilde H_N(X,e)=a_pr_pZ_p\) is presentation-independent and satisfies \(\widetilde H_N^N=K_N\). Indeed, condition 3 proves invariance for each generator, and condition 2 proves the power identity. Whenever \(H(T_N)\ne0\), their quotient belongs to \(\mu_N\); when it vanishes, both values vanish. This is a sufficient criterion, not a claim that its hypotheses are known.

## The exact remaining obstruction

A power comparison alone gives only

\[
\left(\frac{a_{p'}r_{p'}Z_{p'}}{a_pr_pZ_p}\right)^N=1
\]

where the denominator is nonzero. It leaves precisely the unknown root-of-unity multiplier. Nor can one pass a scalar comparison through surgery summation: over \(\mathbb C\), \((x+y)^N\ne x^N+y^N\) generally. Already \(x=y=1\) gives \(2^N\ne2\). Relative phases between summands must be controlled before contraction.

The missing theorem must therefore compare boundary operators and filling tensors coherently, prove exact handle-slide and stabilization identities with the Chern–Simons correction, and establish the displayed \(N\)th-power equality with the original normalization. It must include the representations pulled back from every flat \(B\)-bundle on \(W\), including reducible and degenerate cases, and handle any cut-component dependence. A generic comparison of knot-exterior numbers would not suffice. The peripheral computation makes the proposed normalization concrete; the filling-compatible comparison remains the substantive unresolved step.
