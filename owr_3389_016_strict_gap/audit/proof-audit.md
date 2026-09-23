# Independent adversarial proof audit

Audit checkpoint: 2026-09-23 03:45 UTC. Scope: mathematical correctness of the supplied candidate, independently of problem-source matching and priority. Completion estimate for this audit: **100%**. This is a reasoned mathematical audit, not a machine-checked proof.

## Verdict

**The theorem in the candidate is correct, and its argument proves it.** No counterexample or substantive gap was found. The final exposition should explicitly define the Dirichlet Laplacian through its quadratic form and justify the elementary domain and convergence facts below. Those details fill presentation omissions; they do not require an additional hypothesis or a new mathematical mechanism.

Precisely, for every integer $n\geq1$, nonempty bounded open set $\Omega\subset\mathbb R^n$, and finite integer $J\geq1$, the Dirichlet eigenvalues counted with multiplicity satisfy

\[
\left(\frac{n+2}{nJ}\sum_{j=1}^J E_j\right)^2
-\frac{n+4}{nJ}\sum_{j=1}^J E_j^2
>\frac14(E_{J+1}-E_J)^2.
\]

Boundary smoothness, connectedness, and simplicity of the ground state are unnecessary.

## 1. Operator setup on an arbitrary bounded open set

Use the self-adjoint operator associated with the closed form

\[
q(u,v)=\int_\Omega\nabla u\cdot\nabla\overline v,
\qquad \operatorname{Dom}q=H_0^1(\Omega).
\]

Its operator domain is exactly

\[
\operatorname{Dom}H=\{u\in H_0^1(\Omega):-\Delta u\in L^2(\Omega)
\text{ distributionally}\}.
\]

Indeed, the distributional identity against compactly supported test functions extends to all $H_0^1$ test functions by density. Zero extension into a cube containing $\Omega$, followed by the compact embedding of $H_0^1$ of the cube into $L^2$, proves compact resolvent. The same cube gives a positive Poincaré lower bound, so $E_1>0$. Consequently eigenspaces and spectral subspaces below every finite threshold are finite dimensional. The real form admits a real orthonormal eigenbasis, including when eigenvalues have multiplicity.

For any coordinate $x_\alpha$, multiplication preserves $H_0^1(\Omega)$: approximate by compactly supported smooth functions and use the boundedness of the coordinate and its derivative on $\Omega$. For $u\in\operatorname{Dom}H$, the product rule gives

\[
-\Delta(x_\alpha u)=x_\alpha Hu-2\partial_\alpha u\in L^2(\Omega).
\]

Thus $x_\alpha u\in\operatorname{Dom}H$. This argument is valid even on highly irregular open sets; no boundary trace theorem or elliptic $H^2(\Omega)$ regularity is being assumed.

## 2. Sum rules and convergence

For a normalized real eigenfunction $u_j$, set $a_{jk}^\alpha=\langle u_k,x_\alpha u_j\rangle$. Since $x_\alpha u_j\in\operatorname{Dom}H$, the spectral theorem gives

\[
\sum_k(E_k-E_j)^2|a_{jk}^\alpha|^2=4\|\partial_\alpha u_j\|_2^2.
\]

The first moment is absolutely convergent by Cauchy–Schwarz and Parseval. It equals

\[
\sum_k(E_k-E_j)|a_{jk}^\alpha|^2
=-2\int_\Omega x_\alpha u_j\partial_\alpha u_j=1.
\]

For the last equality, approximate $u_j$ in $H_0^1$ by compactly supported smooth functions, integrate by parts for each approximation, and pass to the limit. The boundedness of $x_\alpha$ and convergence of the products in $L^1$ justify the passage. This avoids any assertion about a classical boundary normal derivative.

For a fixed finite $z$, $L=\{j:E_j<z\}$ is finite. Each series

\[
\sum_k(E_k-E_j)(z-E_k)|a_{jk}^\alpha|^2
\]

is absolutely convergent, because its coefficient is a quadratic polynomial in $E_k-E_j$ and the zeroth, absolute first, and second moments are finite. The cancellation within the finite set $L\times L$ and the passage to the nonnegative tail are therefore legitimate. They yield exactly

\[
4\sum_{j\in L}(z-E_j)E_j-n\sum_{j\in L}(z-E_j)^2
=\sum_{\alpha,j\in L,E_k>z}(z-E_j)(E_k-E_j)(E_k-z)|a_{jk}^\alpha|^2.
\]

There is no omitted factor of two: the internal terms cancel in ordered pairs, and the tail contains only $j\in L$, $E_k>z$. Terms with $E_k=z$ have zero coefficient.

## 3. Why equality is impossible

If $z>E_1$, then $1\in L$ and $z-E_1>0$. Equality forces $a_{1k}^\alpha=0$ whenever $E_k>z$, for every coordinate. Hence $x_\alpha u_1$ belongs to the finite spectral subspace for $E_k\leq z$. Applying $H-E_1$ and using the product rule shows

\[
\partial_\alpha u_1=-\tfrac12(H-E_1)(x_\alpha u_1)\in H_0^1(\Omega)
\]

for every coordinate. Applying $H-E_1$ is harmless here: a finite linear combination of eigenfunctions is in its domain and stays in the same finite spectral subspace.

Let $U$ be the zero extension of $u_1$. The zero-extension identity for $H_0^1$ functions gives

\[
\partial_\alpha U=\widetilde{\partial_\alpha u_1}.
\]

Because every $\partial_\alpha u_1$ itself belongs to $H_0^1(\Omega)$, the same identity can be applied again, giving

\[
\partial_\beta\partial_\alpha U
=\widetilde{\partial_\beta\partial_\alpha u_1}\in L^2(\mathbb R^n).
\]

Thus $U\in H^2(\mathbb R^n)$ and, globally in distributions, $-\Delta U=E_1U$. With a Fourier-transform convention for which the Laplacian multiplier is $|\xi|^2$, this says $(|\xi|^2-E_1)\widehat U=0$. The $L^2$ function $\widehat U$ vanishes outside a sphere of Lebesgue measure zero and therefore vanishes almost everywhere. This contradicts $\|U\|_2=1$.

All derivatives and equations in this argument are weak/distributional. The proof never assumes smoothness of the boundary, a Hopf lemma, or unique continuation across that boundary. It also works if the chosen ground-state eigenfunction is supported on only one component. In fact this proves strictness for **every real $z>E_1$**, not merely eigenvalue thresholds.

## 4. Quadratic endpoint deduction

For $A=J^{-1}\sum_{j\leq J}E_j$, $B=J^{-1}\sum_{j\leq J}E_j^2$, $M_1=(n+2)A/n$, and $D=M_1^2-(n+4)B/n$, direct expansion gives

\[
Q(t)=J^{-1}\sum_{j\leq J}\left((t-E_j)^2-\frac4n(t-E_j)E_j\right)
=(t-M_1)^2-D.
\]

At $y=E_J$, the first $J$ indices include every eigenvalue strictly below $y$, and any extra terms vanish; therefore $Q(y)\leq0$. At $z=E_{J+1}>E_1$, the same observation gives $Q(z)<0$, including when $E_J=E_{J+1}$. In particular $D>0$, $y\geq M_1-\sqrt D$, and $z<M_1+\sqrt D$. Since $z-y\geq0$, it follows that

\[
0\leq z-y<2\sqrt D,
\]

which gives the claimed strict squared inequality.

If $E_{J+1}=E_1$, all first $J+1$ eigenvalues equal $E_1$. The gap is zero while $D=4E_1^2/n^2>0$. This covers arbitrary ground-state multiplicity without any special simplicity assumption.

## 5. Adversarial checks and limits of the verdict

- **Rough boundaries:** handled by the form domain; no regularity assumption has entered secretly.
- **Disconnected domains and arbitrarily many components:** compactness follows by zero extension to a bounded cube. The chosen eigenfunction need not be positive everywhere.
- **Multiplicity at either endpoint:** zero summands handle partial inclusion of an eigenspace exactly.
- **Dimension one and $J=1$:** all identities remain valid. On an interval, $E_2=4E_1$, whereas Yang's first-threshold upper bound is $5E_1$, so there is no limiting equality anomaly.
- **Series rearrangement:** only a finite lower spectral block is paired; all relevant infinite series converge absolutely.
- **Fourier argument:** uses the absence of a nonzero whole-space $L^2$ Laplacian eigenfunction, established directly, rather than assumed as a boundary unique-continuation statement.
- **Circularity:** the remainder identity establishes Yang's inequality and its strictness directly. The quadratic step uses that proved inequality, not the desired gap claim.
- **Quantitative scope:** strict positivity is proved for each individual finite $J$. No positive uniform separation over domains or over all $J$ is claimed or follows from this audit.
- **Priority and source matching:** not assessed here. Mathematical validity alone does not certify that the result is new, still open, or exactly the question in the linked source.

The strongest verified result is the displayed strict gap inequality, plus strictness of the threshold Yang inequality for every real $z>E_1$. The remaining mathematical gap in this proof is **none**.

## 6. Independent audit of the shorter self-adjointness argument

Additional checkpoint: 2026-09-23 03:48 UTC. Completion estimate for the simplification audit: **100%**. Verdict: **valid**, and preferable for a short paper because it eliminates the whole-space Fourier step without weakening the domain generality.

Let $Hu=Eu$ with $u$ normalized, and suppose $w=x_\alpha u$ lies in a finite spectral subspace. Then $w\in\operatorname{Dom}(H^m)$ for every positive integer $m$, because it is a finite linear combination of eigenfunctions. In particular, putting

\[
v=(H-E)w=-2\partial_\alpha u
\]

gives $v\in\operatorname{Dom}H$. The interior eigenfunction equation can be differentiated in distributions: constant-coefficient differential operators commute, so

\[
(-\Delta-E)v=-2\partial_\alpha(-\Delta-E)u=0
\quad\text{in }\mathcal D'(\Omega).
\]

Since $v$ already belongs to the operator domain and $Hv=-\Delta v$ distributionally, this implies $(H-E)v=0$ as an $L^2$ identity. Self-adjointness now gives

\[
\|v\|_2^2
=\langle (H-E)w,v\rangle
=\langle w,(H-E)v\rangle=0.
\]

Both domain hypotheses for this use of symmetry have been proved: $w,v\in\operatorname{Dom}H$. No assumption that arbitrary derivatives preserve the Dirichlet operator domain is being made; domain membership of this particular derivative is a consequence of the finite spectral expansion.

There are two valid ways to close the contradiction:

1. Equality in the remainder supplies the finite spectral expansion for every coordinate, so every first derivative of $u$ vanishes. The form identity then gives $E\|u\|_2^2=\|\nabla u\|_2^2=0$, contradicting $E>0$.
2. A still shorter contradiction works using just the chosen coordinate. The already established first sum rule gives $\langle w,(H-E)w\rangle=1$, while $v=(H-E)w=0$ would make that inner product zero.

For the strict-threshold result take $u=u_1$ and any real $z>E_1$. Equality in the nonnegative remainder forces precisely the required finite spectral expansion of each $x_\alpha u_1$. The argument contains no eigenvalue-threshold assumption on $z$. It therefore establishes strict Yang inequality for all real $z>E_1$ and can replace Section 3's Fourier proof verbatim after the initial finite-span conclusion.
