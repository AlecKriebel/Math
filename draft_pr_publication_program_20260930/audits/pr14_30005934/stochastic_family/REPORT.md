# Independent stochastic-analysis audit of PR14

**Target:** problem 30005934 / OWR-14298374-003.  
**Frozen PR head:** `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`.  
**Inspected candidate SHA256:** `bf8d8a5dda2bfe36cd0c28b4a2d0fe9ee1d2ff0365f286de8cc4bd4daa4ccf1d`.  
**Audit family:** stochastic and infinite-dimensional analysis.  
**Status:** PASS for the narrow necessity claim; independent derivation and fresh conditional/determinant adversary complete.

## 1. Claim, assumptions, and audit boundaries

The exact hypothesis audited is the existence of a positive trace-class-valued adapted process $X$, continuous in trace norm, satisfying the candidate's scalar weak equations against every pair $g,h\in D(A)$, with real parameter $\alpha$, bounded positive self-adjoint injective $Q$, and arbitrary $C_0$-semigroup $S$ on a separable infinite-dimensional real Hilbert space. The driving process is the usual cylindrical Brownian motion on the **full real Hilbert space of Hilbert–Schmidt operators**, with respect to the solution filtration. Initial data are merely finite positive trace-class operators almost surely and measurable at time zero; no moment assumption is imposed.

The proposed conclusion is only

\[
\alpha\in\mathbb N_0=\{0,1,2,\ldots\}.
\]

This is a necessity assertion. It does not assert that all these integer parameters yield solutions for all $A,Q,X_0$. It does not construct solutions, classify ranks, prove uniqueness, or address noninjective $Q$. No novelty or priority conclusion is supplied by this mathematical audit. Historical review files and sibling audit findings were excluded as evidence.

**Current mathematical finding:** every stochastic-analytic step of the candidate can be justified under its stated assumptions. The only imported mathematical dependency in its displayed argument is the established finite-dimensional positive-scale parameter theorem, and its normalization matches. Section 8 gives a second checkable necessity route that avoids importing the full noncentral classification.

## 2. Bounded covariance and strict positivity without semigroup injectivity

For fixed $T>0$, let $M_T=\sup_{0\le s\le T}\|S(s)\|<\infty$. The form

\[
c_t(h,k)=\int_0^t\langle Q S(s)h,S(s)k\rangle\,ds
\]

satisfies $|c_t(h,k)|\le t\|Q\|M_T^2\|h\|\|k\|$. It therefore defines a bounded self-adjoint positive operator $C_t$. This construction uses a bounded bilinear form; no operator-norm Bochner measurability or trace-class integrability assumption is required.

For $h\ne0$, positivity and injectivity of $Q$ give $a=\|\sqrt Qh\|>0$. Strong continuity at zero gives a $\delta>0$ such that

\[
\|\sqrt Q S(s)h-\sqrt Qh\|<a/2,
\qquad 0\le s\le\delta.
\]

Consequently

\[
\langle C_t h,h\rangle
\ge \frac{a^2}{4}\min(t,\delta)>0.
\]

The interval may depend on $h$. No uniform coercivity is needed: if $J:\mathbb R^n\to H$ is injective, then for every nonzero $z\in\mathbb R^n$,

\[
z^T J^*C_tJz=\langle C_tJz,Jz\rangle>0,
\]

so its finite compression is positive definite. Vectors may be killed by $S(s)$ at later times without affecting this argument.

## 3. Domain density and moving-test approximation

### 3.1 The domain used by the proof is sufficiently large

Let $R_\lambda=(\lambda I-A)^{-1}$ for sufficiently large real $\lambda$. The standard resolvent approximation $\lambda R_\lambda\to I$ strongly, with the family uniformly bounded, gives $\lambda^2R_\lambda^2\to I$ strongly. Since $R_\lambda^2H\subset D(A^2)$, $D(A^2)$ is dense. Gram–Schmidt preserves this linear space, so it contains an orthonormal $n$-tuple for every finite $n$.

For $\ell\in D(A^2)$, domain invariance and generator commutation yield

\[
f(s)=S(s)\ell\in D(A^2),\quad
f'(s)=A S(s)\ell=S(s)A\ell,
\]

and

\[
(Af)'(s)=S(s)A^2\ell.
\]

Thus $f$ is $C^1$ as a path in the Banach space $D(A)$ with graph norm $\|h\|_A=\|h\|+\|Ah\|$. No analyticity, boundedness of $A$, or injectivity of $S(s)$ is used.

### 3.2 Finite fixed-test equations suffice

A continuous $D(A)$-valued path $f'$ can be approximated uniformly in graph norm by continuous polygonal paths $p_k$ with values in finite spans of elements of $D(A)$. Set

\[
f_k(s)=f(0)+\int_0^s p_k(r)\,dr.
\]

Then $f_k$ takes values in one finite-dimensional subspace of $D(A)$, is $C^1$ there, and

\[
\sup_{s\le T}\bigl(\|f_k(s)-f(s)\|_A+
\|f'_k(s)-f'(s)\|_A\bigr)\longrightarrow0.
\]

For a test of the form $v(s)=B(s)M(s)B(s)^*$, with finitely many such columns of $B$ and deterministic $C^1$ symmetric matrix $M$, apply this construction to every column. The approximants $v_k$ are linear combinations, with $C^1$ scalar coefficients, of finitely many fixed rank-one tests from $D(A)$. Their product rule follows directly from the fixed-test weak equations and scalar deterministic integration by parts.

Graph convergence implies uniform operator convergence of

\[
v_k\to v,\qquad v'_k\to v',\qquad Av_k\to Av,
\]

and of the adjoints $(Av_k)^*\to(Av)^*$. Each $Av$ is a bounded finite-rank operator; $vA^*$ means its bounded adjoint extension. There is no unbounded trace manipulation.

### 3.3 Explicit stopped estimates close the limiting argument

Put

\[
\tau_m=\inf\{s\ge0:\|X_s\|_1>m\},
\]

with $\tau_m=0$ on $\{\|X_0\|_1>m\}$. On any nonempty integration interval before $\tau_m$, $\|X_s\|_1\le m$. Drift errors involving $X_s$ are bounded by $mT$ times the respective uniform operator errors. The $Q$-drift is controlled by

\[
|\operatorname{tr}(Q(v_k-v))|
\le\|Q\|\|v_k-v\|_1\to0
\]

uniformly; the rank of $v_k-v$ is at most twice the fixed number of columns, so operator convergence also gives trace-norm convergence here.

For the martingale error, Section 4's integrand gives

\[
\|2\sqrt{X_s}(v_k-v)\sqrt Q\|_2^2
\le4m\|Q\|\|v_k-v\|^2.
\]

The Itô isometry and Doob inequality therefore give

\[
\mathbb E\sup_{r\le T}
|M_{r\wedge\tau_m}^{(k)}-M_{r\wedge\tau_m}|^2
\le16m\|Q\|T\sup_{s\le T}\|v_k(s)-v(s)\|^2\to0.
\]

Endpoint and initial terms converge pathwise. On the event with $\tau_m=0$, the stopped identity has no drift or noise increments; one does **not** require an integrable bound on the large initial value. Its finite trace norm almost surely is enough for the endpoint convergence. Countably many approximant test vectors permit a common full-probability set even if the original fixed-test equations were stated one test at a time.

It follows that the deterministic moving-test identity is

\[
d\operatorname{tr}(X_sv(s))
=\left[\alpha\operatorname{tr}(Qv(s))+
\operatorname{tr}\{X_s(Av(s)+(Av(s))^*+v'(s))\}\right]ds+dM_s.
\]

Trace-norm continuity makes $\sup_{s\le T}\|X_s\|_1$ finite almost surely, so $\tau_m>T$ eventually on each sample path. The stopped identities patch to the desired local identity. This is the needed analytic closure, rather than an assumption that the compressed process solves a closed matrix SDE.

## 4. Noise bracket and its factor four

For a deterministic self-adjoint finite-rank $v$, a Hilbert–Schmidt Brownian direction $E$ contributes

\[
\begin{aligned}
&\operatorname{tr}(v\sqrt X E\sqrt Q)
+\operatorname{tr}(v\sqrt Q E^*\sqrt X)\\
&\qquad=2\operatorname{tr}(\sqrt Qv\sqrt X E)
=\langle2\sqrt Xv\sqrt Q,E\rangle_{\mathrm{HS}}.
\end{aligned}
\]

The equal contributions use self-adjointness of $v,X,Q$ and the real trace pairing. Because $\sqrt X$ is Hilbert–Schmidt, its representing integrand is Hilbert–Schmidt even when $Q$ is not trace class. Its squared norm is

\[
4\|\sqrt Xv\sqrt Q\|_2^2
=4\operatorname{tr}(XvQv).
\]

Thus

\[
d[M]_s=4\operatorname{tr}(X_sv(s)Qv(s))\,ds.
\]

Replacing the full Hilbert–Schmidt Brownian motion by a differently normalized symmetric-matrix Brownian motion could change constants, but that is not the noise in the candidate or original source. The given factor four is correct.

## 5. Riccati identity, Itô cancellation, and a true conditional martingale

For $L:\mathbb R^n\to H$ with columns in $D(A^2)$, write

\[
B_s=S(s)L,\quad D_s=I+2\int_0^sB_r^*QB_r\,dr,
\quad\psi_s=B_sD_s^{-1}B_s^*.
\]

Then $D_s\ge I$, and

\[
D'_s=2B_s^*QB_s,\quad B'_s=AB_s,
\quad(D_s^{-1})'=-D_s^{-1}D'_sD_s^{-1}.
\]

Ordinary finite-rank product differentiation gives

\[
\psi'_s=A\psi_s+(A\psi_s)^*-2\psi_sQ\psi_s,
\qquad
\phi'_s=\alpha\operatorname{tr}(Q\psi_s),
\quad\phi_s=\frac\alpha2\log\det D_s.
\]

Apply Section 3's moving rule with $v(s)=\psi_{T-s}$. If

\[
Z_s=-\phi_{T-s}-\operatorname{tr}(X_s\psi_{T-s}),
\]

then its finite-variation part is

\[
-2\operatorname{tr}(X_s\psi_{T-s}Q\psi_{T-s})\,ds,
\]

and its bracket is four times the same nonnegative trace. Consequently Itô's formula cancels the drift of $F_s=e^{Z_s}$.

For every real $\alpha$, this local martingale has the deterministic bound

\[
0<F_s\le\exp\left(\sup_{0\le r\le T}|\phi_r|\right)<\infty.
\]

Its localizations are genuine martingales, and dominated convergence at stopped endpoints makes $F$ a genuine martingale. No first moment of $X_0$ or of $\sup\|X_s\|_1$ is used. It follows that

\[
\mathbb E[e^{-\operatorname{tr}(LL^*X_T)}\mid\mathcal F_0]
=\det D_T^{-\alpha/2}
\exp[-\operatorname{tr}(\psi_TX_0)].
\]

The random initial datum appears only inside a bounded exponential. The same argument handles negative $\alpha$; boundedness is finite for a fixed $T,L$, even though the resulting identity then leads to an impossibility.

## 6. Random initial values and simultaneous conditional transforms

Fix one finite $n,T,J$. Put

\[
Y=J^*X_TJ,\quad C=J^*C_TJ>0,
\quad b(x)=J^*S(T)^*xS(T)J.
\]

For $v\ge0$, use $L=J\sqrt v$. The bounded finite-dimensional identities give

\[
\mathbb E[e^{-\operatorname{tr}(vY)}\mid X_0]
=\det(I+2Cv)^{-\alpha/2}
\exp[-\operatorname{tr}\{b(X_0)v(I+2Cv)^{-1}\}].
\]

The cone of positive trace-class operators is closed in the separable trace-class Banach space and hence standard Borel. The finite matrix state space is also standard Borel. Thus a probability kernel $\kappa(x,dy)$ for $Y$ conditioned on $X_0=x$ exists, irrespective of whether the underlying probability space itself is standard Borel.

Take a countable dense set $D\subset S_n^+$. For each $v\in D$, the preceding identity holds outside an initial-law null set. Intersect these countably many full sets and also the set on which $\kappa(x,\cdot)$ is a probability measure. For every remaining $x$, bounded dominated convergence makes

\[
v\mapsto\int e^{-\operatorname{tr}(vy)}\kappa(x,dy)
\]

continuous, and the stated determinant-resolvent expression is continuous in $v\ge0$. Equality therefore extends to every $v\ge0$ for this same $x$. Its $b(x)$ is a finite positive matrix. No conditioning on a probability-zero singleton is being taken informally, and there is no uncountable null-set intersection.

Only one dimension $n>\alpha+1$ is needed to contradict a fixed noninteger $\alpha$, so even a simultaneous conditional kernel across all dimensions is unnecessary.

## 7. Matching the imported finite-dimensional theorem

The candidate's right side has precisely the noncentral Wishart normalization

\[
\beta=\alpha/2,\qquad\Sigma=2C>0,\qquad\omega=b\ge0.
\]

The displayed transform restriction in Graczyk–Małecki–Mayerhofer's Theorem 1.3 is a restriction on the existence of a **single matrix distribution**, not an assertion that the compressed process is Markov. It yields

\[
\alpha\in\{0,1,\ldots,n-2\}\cup[n-1,\infty).
\]

The extra rank restriction is unnecessary for this audit. Although Definition 1.1 initially writes a positive shape parameter, the theorem and subsequent arguments include zero explicitly, so zero is not lost through that convention.

Negative parameters require no imported classification: in dimension one, for $c>0$ and finite $b\ge0$,

\[
(1+2cr)^{-\alpha/2}e^{-br/(1+2cr)}
\longrightarrow\infty\quad(r\to\infty)
\]

when $\alpha<0$. A probability Laplace transform is at most one, a contradiction. For $\alpha\ge0$ noninteger, take $n=\lfloor\alpha\rfloor+2>\alpha+1$; the displayed positive-scale restriction excludes it. This proves the candidate's conclusion.

## 8. Independent finite-positivity route without the full noncentral theorem

This route is included as a check of the narrow parameter obstruction, not as a new classification claim.

### 8.1 Tilt and rescale to a central transform

Given one conditional matrix distribution from Section 6, whiten by $(2C)^{-1/2}$. The resulting positive matrix $Z$ has transform

\[
L(u)=\det(I+u)^{-\alpha/2}
\exp[-\operatorname{tr}\{\Omega u(I+u)^{-1}\}],
\qquad \Omega=(2C)^{-1/2}b(2C)^{-1/2}\ge0.
\]

For $t>0$, tilt its probability law by $e^{-t\operatorname{tr}Z}/L(tI)$, and under that law form $R_t=(1+t)Z$. Direct division of $L(tI+(1+t)u)$ by $L(tI)$ gives

\[
\mathbb E_t e^{-\operatorname{tr}(uR_t)}
=\det(I+u)^{-\alpha/2}
\exp\left[-\frac{\operatorname{tr}\{\Omega u(I+u)^{-1}\}}{1+t}\right].
\]

After separately excluding $\alpha<0$, these laws are tight. One elementary proof uses, for $s>0$, the uniform estimate

\[
\mathbb P_t(\operatorname{tr}R_t>K)
\le\frac{1-\mathbb E_t e^{-s\operatorname{tr}R_t}}{1-e^{-sK}}.
\]

The numerator tends to zero uniformly in $t>0$ as $s\downarrow0$, by the explicit scalar transform. First choose $s$ small, then $K$ large. Positive matrices with bounded trace form a compact subset of the finite symmetric-matrix space. Any weakly convergent subsequence as $t\to\infty$ therefore yields a positive random matrix with the central transform

\[
L_0(u)=\det(I+u)^{-\alpha/2}.
\]

This operation never requires a moment of the original conditional distribution. Alternatively, differentiating at $tI>0$ gives the uniform tilted mean $\mathbb E_t\operatorname{tr}R_t=n\alpha/2+\operatorname{tr}\Omega/(1+t)$.

### 8.2 A positive weighted determinant gives the obstruction

For a central positive matrix with the preceding transform and $s>0$, define the symmetric derivative matrix

\[
\mathcal D_{ii}=\partial_{u_{ii}},\qquad
\mathcal D_{ij}=\mathcal D_{ji}=\tfrac12\partial_{u_{ij}}
\quad(i<j).
\]

Then

\[
(-1)^n\det(\mathcal D)L_0(u)
=\mathbb E[\det Z\,e^{-\operatorname{tr}(uZ)}].
\]

Differentiation is justified in a neighbourhood of $sI>0$: for positive $Z$, every entry is bounded in absolute value by $\operatorname{tr}Z$, and polynomial factors of degree $n$ multiplied by $e^{-(s/2)\operatorname{tr}Z}$ are uniformly bounded. The half factors on off-diagonal derivatives account for $\operatorname{tr}(uZ)=\sum_i u_{ii}Z_{ii}+2\sum_{i<j}u_{ij}Z_{ij}$.

At $u=sI$, the derivative expression must have the form

\[
P_n(\alpha)(1+s)^{-n\alpha/2-n},
\]

where $P_n$ is a polynomial of degree at most $n$. Indeed the order-$n$ derivatives of $e^{-(\alpha/2)\log\det(I+u)}$ are polynomials of degree at most $n$ in $\alpha$. The substitution $u=sI+(1+s)w$ extracts the displayed scaling factor.

For every integer $m\ge n$, the random matrix $Z_m=\frac12GG^T$, with an $n\times m$ matrix of independent standard real Gaussian entries, has exactly this central transform with $\alpha=m$. Gram–Schmidt on the rows of $G$ gives

\[
\mathbb E\det(GG^T)=m(m-1)\cdots(m-n+1).
\]

This follows by successive conditioning: the squared residual of row $i$ has mean $m-i+1$. Tilting by $e^{-s\operatorname{tr}Z_m}$ rescales every Gaussian variance by $(1+s)^{-1}$ and contributes the normalizing factor $(1+s)^{-nm/2}$. Therefore

\[
P_n(m)=2^{-n}m(m-1)\cdots(m-n+1).
\]

The two polynomials agree at infinitely many integers, so for all real $\alpha$,

\[
\boxed{\mathbb E[\det Z\,e^{-s\operatorname{tr}Z}]
=2^{-n}\prod_{j=0}^{n-1}(\alpha-j)
(1+s)^{-n\alpha/2-n}.}
\]

No analytic continuation of probability distributions in $\alpha$ is assumed: polynomial interpolation concerns the explicit derivative identity only. For example $P_2(\alpha)=\alpha(\alpha-1)/4$ and $P_3(\alpha)=\alpha(\alpha-1)(\alpha-2)/8$, consistent with direct symmetric-coordinate differentiation.

For noninteger $\alpha\ge0$, choose $n=\lfloor\alpha\rfloor+2$. Exactly one factor in the product is negative and all others are positive. The right side is negative while the left side is nonnegative, a contradiction. Thus the same narrow necessity result follows independently of the full noncentral Wishart rank theorem.

## 9. Adversarial boundary cases and attempted escapes

| Attempt or boundary | Checkable outcome |
|---|---|
| Noninjective and even nilpotent semigroup | On $H=L^2(0,1)$, $S(t)f(x)=f(x+t)$ with zero extension beyond 1 is noninjective for every $t>0$, and $S(t)=0$ for $t\ge1$. Its unbounded generator is $Af=f'$, $D(A)=\{f\in H^1:f(1)=0\}$. With $Q=I$, $C_t$ is multiplication by $\min(t,x)$, strictly positive almost everywhere. It does not evade finite-compression positivity. |
| Non-trace-class covariance | The same multiplication $C_t$ is noncompact and therefore not trace class: on an interval away from zero it is bounded below by a positive constant, so an infinite orthonormal sequence there cannot have compact images. Every finite compression nevertheless has finite entries and positive determinant. |
| Loss of rank of $S(T)L$ | In the killed shift, $S(T)L=0$ for $T\ge1$, so the noncentral matrix $b$ becomes zero. $D_T$ remains positive definite and the transform becomes central; no inverse of $S(T)$ appears. |
| Unbounded generator with smoothing | On $\ell^2$, $Ae_k=-k^2e_k$, $Q=I$ gives $C_te_k=(1-e^{-2k^2t})/(2k^2)e_k$. The graph-domain/Riccati computations work on finite domain columns. This also shows that no lower spectral bound is required. |
| Injective $Q$ with spectrum accumulating at zero | Strict positivity is pointwise in $h$; the continuity interval may shrink. Finite-dimensional positivity is sufficient, so no bounded inverse of $Q$ is used. |
| Arbitrary heavy-tailed initial trace | A hypothetical $X_0=Ze\otimes e$ with $Z<\infty$ almost surely but $\mathbb EZ=\infty$ causes no failure: stops may equal zero on large initial events, noise/drift integrals then vanish, and the exponential martingale remains bounded. This is a test of the implication, not a solution construction for these data. |
| $\alpha<0$ | The scalar conditional transform diverges at large positive tests, contradicting its upper bound one. |
| $\alpha=0$ | $X_t=0$ is a valid weak solution for every $A,Q$ in scope. The audit supports $\mathbb N_0$, not the positive integers by a convention that would exclude zero. |
| Non-Markov finite compression | No closed dynamics or Markov property of $J^*XJ$ is asserted; only its fixed-time conditional probability transform is used. |

No attempted escape supplied an analytic counterexample under the exact hypotheses.

## 10. Reproducible finite checks and exact remaining gaps

`exact_checks.py` uses only Python standard-library rational arithmetic. Running `python3 exact_checks.py` reproduces `exact_check_results.json`: **11/11 pass**. The checks cover a nonsymmetric $A$, noncommuting $Q$, exact log-determinant derivative, both noise contributions in every matrix Brownian coordinate, factor four, exponential drift cancellation for a negative real $\alpha$, and singular as well as positive-definite terminal tests. They independently support the algebra but do not certify the stopped approximation or conditional probability arguments; those were derived above.

**Strongest verified result:** under the exact weak-solution assumptions, every admissible finite compression has the stated conditional positive-scale transform, and the parameter must lie in $\mathbb N_0$. The conclusion does not use semigroup injectivity or trace-class covariance.

**Current central mathematical gap:** none found in the narrow necessity proof. A fresh adversary independently verified Section 6 and Section 8, and its additional independent determinant reviewer confirmed the weighted determinant identity. Their 144 exact rational checks reproduce successfully. See `conditional_positivity_adversary/REPORT.md` and its saved verdict for the independent derivations; no historical candidate-review verdict was used.

**Scope limits:** the work does not validate solution constructions, the broader rank classification, unbounded $Q$, complex-noise normalizations, or processes assumed continuous only in a weaker operator topology without local trace-norm control. These are not claims of the candidate. There is no $L^p$ hypothesis in this necessity argument, so endpoint choices of $p$ do not arise.

One harmless wording improvement would explicitly say that $W$ is a Brownian motion **with respect to the solution filtration**. That is the standard meaning in a weak SDE and the original source states it explicitly. Treating an anticipative enlargement merely as an arbitrary filtration would not be the audited weak-solution notion.

## 11. Primary sources consulted directly

- [Cox–Cuchiero–Khedher, final published EJP paper](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf): printed pp. 5, 8, 14–15, 26–27 were inspected for the target, weak-equation topology and Brownian normalization. The candidate matches that continuous trace-class weak notion and weakens moment/covariance conditions for its own direct finite-rank proof.
- [Original Oberwolfach report](https://ems.press/content/serial-article-files/49484): printed p. 1480 identifies the injective-noise question separately from the degenerate-noise question.
- [Graczyk–Małecki–Mayerhofer, arXiv 1607.00206](https://arxiv.org/pdf/1607.00206): Definition 1.1 and Theorem 1.3 were inspected directly; shape $\alpha/2$, scale $2C$, and noncentrality $b$ match the candidate. No inspection of historical project verdicts supplied the mathematical finding.

No outside individual was contacted. All files generated by this family remain in its dedicated audit directory; no canonical source or Git state was changed.
