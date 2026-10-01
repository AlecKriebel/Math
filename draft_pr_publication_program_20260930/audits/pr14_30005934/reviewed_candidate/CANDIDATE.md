# The noninteger obstruction does not require an injective semigroup

**Target:** 30005934 / OWR-14298374-003, OWR Open problem 1 (p. 1480), corresponding to Cox–Cuchiero–Khedher Open Problem 1.2 (EJP p. 5).
**Status:** three independent acceptance-audit families pass; fresh complete acceptance review pending. Proposed QUEUE disposition: already_solved, credited partial research record.
**Original attempt:** 30 September 2026, gpt-6-astra, xhigh, response 1/5. **Acceptance candidate:** 1 October 2026. Independent AI audits are extensive; no human peer review or formal certification is claimed.

**Attribution boundary.** The negative answer below was already claimed by Anonymous (2026) in version 0.1.0-candidate of the unrefereed manuscript *Reachable noise and existence of operator-valued Wishart processes*, dated 22 September 2026, Lemma 3 and Corollary 2, [versioned source](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md), [DOI](https://doi.org/10.5281/zenodo.22892681). We found that manuscript during the required current-literature check and credit its finite-rank-transform argument. This note checks and isolates the narrow conclusion requested by the queue. **No novelty, priority, or verification of that manuscript's broader classification is claimed.**

## 1. Exact claim and source scope

Let $H$ be a separable infinite-dimensional real Hilbert space; let $S(t)$ be a strongly continuous semigroup with generator $A$; and let $Q$ be a bounded positive self-adjoint injective operator. Let $\alpha\in\mathbb R$. Suppose there is an adapted process $X_t$ with values in the positive trace-class operators, continuous in trace norm, which solves

$$
dX_t=(\alpha Q+X_tA+A^*X_t)\,dt
+\sqrt{X_t}\,dW_t\sqrt Q+\sqrt Q\,dW_t^*\sqrt{X_t},
$$

in the following weak sense: for every $g,h\in D(A)$,

$$
\begin{aligned}
\langle X_tg,h\rangle={}&\langle X_0g,h\rangle+
\int_0^t\bigl(\alpha\langle Qg,h\rangle+
\langle X_sAg,h\rangle+\langle X_sg,Ah\rangle\bigr)\,ds\\
&+\int_0^t\langle\sqrt{X_s}\,dW_s\sqrt Qg,h\rangle
+\int_0^t\langle\sqrt Q\,dW_s^*\sqrt{X_s}g,h\rangle.
\end{aligned}
$$

Here $W$ is cylindrical Brownian motion on the full real Hilbert space of Hilbert–Schmidt operators, Brownian with respect to the solution filtration; the scalar integrals may be defined locally. The initial value can be random and measurable at time zero.

**Proposition.** Under these assumptions,

$$\boxed{\alpha\in\mathbb N_0.}$$

In particular, an unbounded generator with a noninjective semigroup cannot produce a solution with a noninteger parameter. The proof does not impose a trace-class condition on the integrated covariance. We explicitly use $\mathbb N_0=\{0,1,2,\ldots\}$; the zero process with $\alpha=0$ is not excluded by a convention about natural numbers.

**Literal notation boundary.** The primary source prints $\alpha\notin\mathbb N$, without an explicit convention for $\mathbb N$ found in this audit. If it includes zero, the proposition gives the literal negative answer. If it means positive integers, $\alpha=0$, $X_0=0$, $X_t=0$ gives a trivial affirmative example for any allowed $A,Q$, including an unbounded noninjective shift generator. The negative answer recorded here concerns the intended noninteger target $\alpha\notin\mathbb N_0$. No author convention is asserted.

The original question is on [Oberwolfach Report 26/2024, p. 1480](https://ems.press/content/serial-article-files/49484). It also appears as Open Problem 1.2 on p. 5 of the [final published Cox–Cuchiero–Khedher paper](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf). Its separate degenerate-noise question and the full existence classification are not addressed here.

## 2. Positivity of the integrated covariance

For $t>0$ define the bounded positive operator $C_t$ by

$$
\langle C_th,k\rangle=\int_0^t\langle Q S(s)h,S(s)k\rangle\,ds.
$$

Boundedness follows from the uniform bound on $\|S(s)\|$ for $0\le s\le t$. For $h\ne0$, injectivity and positivity of $Q$ imply $\|\sqrt Qh\|>0$. The function $s\mapsto\sqrt Q S(s)h$ is continuous at zero. It therefore has norm bounded below by a positive number on some interval $[0,\varepsilon]$. Consequently

$$
\langle C_th,h\rangle=\int_0^t\|\sqrt Q S(s)h\|^2\,ds>0.
$$

Thus every compression $J^*C_tJ$ to a finite-dimensional subspace is positive definite. No assertion that $S(s)h$ remains nonzero for all positive times is needed.

## 3. A finite-rank Laplace-transform lemma

We need only tests with range in $D(A^2)$, which is dense in $H$. Let $L:\mathbb R^n\to H$ have columns in $D(A^2)$, put $u=LL^*$, and set

$$
D_s=I_n+2L^*C_sL,\qquad
\psi_s=S(s)L D_s^{-1}L^*S(s)^*,\qquad
\phi_s=\frac\alpha2\log\det D_s.
$$

Then for any fixed $T>0$,

$$
\mathbb E\left[e^{-\operatorname{tr}(uX_T)}\mid\mathcal F_0\right]
=\det D_T^{-\alpha/2}\,
\exp\{-\operatorname{tr}(\psi_TX_0)\}. \tag{1}
$$

### Proof of the lemma

The matrices $D_s$ are positive definite with $D_s\ge I_n$. Since $L$ has finitely many domain-admissible columns, all following derivatives are derivatives of bounded finite-rank operators. Differentiation gives

$$
\psi_s'=A\psi_s+\psi_sA^*-2\psi_sQ\psi_s,
\qquad
\phi_s'=\alpha\operatorname{tr}(Q\psi_s). \tag{2}
$$

In (2), $\psi_sA^*$ denotes its bounded finite-rank extension, the adjoint of $A\psi_s$. Indeed, for $B_s=S(s)L$ one has $B_s'=AB_s$ and $D_s'=2B_s^*QB_s$; differentiating $B_sD_s^{-1}B_s^*$ proves (2).

For a deterministic self-adjoint finite-rank test $v$ with range in $D(A)$, the martingale part of $\operatorname{tr}(vX_s)$ has quadratic variation

$$
d[\operatorname{tr}(vX)]_s
=4\operatorname{tr}(X_s vQv)\,ds. \tag{3}
$$

To check the factor, the two noise terms combine to the scalar stochastic integral defined by the functional $E\mapsto2\operatorname{tr}(\sqrt Q\,v\sqrt{X_s}E)$. Under the Hilbert–Schmidt pairing $\langle K,E\rangle=\operatorname{tr}(K^*E)$, its representing integrand is $2\sqrt{X_s}v\sqrt Q$. Its squared Hilbert–Schmidt norm is the right-hand side of (3).

The weak equation also allows the moving finite-rank tests in (2). Here are the analytic details. Each column $f(s)=S(s)Le_i$ is continuously differentiable as a path in $D(A)$ with graph norm, because $Le_i\in D(A^2)$, $f'=Af$, and $(Af)'=A^2f$. On a compact time interval, approximate $f$ and $f'$ uniformly in graph norm by continuously differentiable paths with values in finite-dimensional subspaces of $D(A)$: approximate $f'$ by finite linear combinations with continuous scalar coefficients and integrate, including $f(0)$ in the chosen span. For these approximants the product rule follows from finitely many fixed-test weak equations.

Stop when $\|X_s\|_1$ first exceeds $m$, with the stopping time set to zero if $\|X_0\|_1>m$. Up to this time, graph-norm convergence controls the drift integrals. The scalar Itô isometry controls the stochastic integrals, since their squared integrands are bounded by a constant times $m\|Q\|$ times the squared errors of the test vectors. This proves the moving-test rule by passage to the limit. Trace-norm continuity ensures that these stopping times tend to infinity almost surely on every finite time interval.

Now apply the scalar Itô formula to

$$
F_s=\exp\{-\phi_{T-s}-\operatorname{tr}(\psi_{T-s}X_s)\},
\qquad 0\le s\le T.
$$

Equations (2) and (3) cancel its drift: the remaining drift of its exponent is $-2\operatorname{tr}(X_s\psi_{T-s}Q\psi_{T-s})$, and half its quadratic variation is the opposite quantity. Thus $F$ is a local martingale. It is bounded by the deterministic constant $\exp(\sup_{r\le T}|\phi_r|)$ because $X_s,\psi_{T-s}\ge0$. It is therefore a true martingale, for every real $\alpha$, and its endpoint conditional expectation is (1). This proves the lemma.

This proof uses no infinite-dimensional determinant and no assumption that $C_t$ is trace class.

## 4. Reduction to finite-dimensional noncentral Wishart laws

Fix $T>0$ and choose an isometry $J:\mathbb R^n\to H$ whose range lies in $D(A^2)$. Such isometries exist for every $n$, since $D(A^2)$ is dense and $H$ is infinite-dimensional. For $v\in S_n^+$, take $L=J\sqrt v$ in (1). Put

$$
Y=J^*X_TJ,\qquad C=J^*C_TJ>0,\qquad
b=J^*S(T)^*X_0S(T)J\ge0.
$$

Finite-dimensional determinant and resolvent identities give

$$
\mathbb E[e^{-\operatorname{tr}(vY)}\mid X_0]
=\det(I_n+2Cv)^{-\alpha/2}
\exp\{-\operatorname{tr}[b\,v(I_n+2Cv)^{-1}]\}. \tag{4}
$$

These identities follow, for example, from

$$
\sqrt v\,(I_n+2\sqrt vC\sqrt v)^{-1}\sqrt v
=v(I_n+2Cv)^{-1},
$$

and the equality of the determinants of $I+AB$ and $I+BA$.

For random $X_0$, a regular conditional distribution of the finite matrix $Y$ given $X_0$ exists because the positive trace-class cone is a standard Borel space. First enforce (4) simultaneously on a countable dense subset of positive matrices and then use continuity in $v$. Thus, for almost every initial value, its right-hand side is the Laplace transform of a probability measure on $S_n^+$.

We now use the established positive-scale noncentral Wishart parameter theorem of Graczyk–Małecki–Mayerhofer: a transform of the form (4), with $C>0$ and $b\ge0$, can occur only if

$$
\alpha\in\{0,1,\ldots,n-2\}\ \cup\ [n-1,\infty), \tag{5}
$$

with the additional rank condition in the discrete range. See [Theorem 1.3 and Definition 1.1](https://arxiv.org/pdf/1607.00206), published in *Stochastic Processes and their Applications* **128** (2018), 1386–1404, [DOI](https://doi.org/10.1016/j.spa.2017.07.010). This is a theorem about each fixed-time distribution; the compressed process need not be Markov.

For completeness, negative $\alpha$ is already impossible in dimension one: if $C=c>0$, the right-hand side of (4), at the scalar test $v=r$, tends to infinity as $r\to\infty$, since its exponential factor tends to $e^{-b/(2c)}>0$. A probability Laplace transform cannot exceed one.

If $\alpha\ge0$ is noninteger, choose an integer $n>\alpha+1$. Then $\alpha<n-1$ and $\alpha\notin\{0,\ldots,n-2\}$, contradicting (5). Hence $\alpha\in\mathbb N_0$. This proves the proposition.

## 5. What has and has not been established

- The argument covers an arbitrary strongly continuous semigroup, including one with a nontrivial kernel at every positive time
- It covers noninteger real parameters of either sign and random positive trace-class initial values
- No semigroup injectivity, Markov property of compressions, or global Fredholm determinant is used
- No solution construction, full rank classification, strong existence, pathwise uniqueness, or degenerate-noise classification is claimed
- The wider claims of the 22 September candidate were not audited here
- The conclusion is already present as an external unrefereed claim; this note supplies a narrow checkable proof audit and does not claim a new discovery

The stochastic-analysis family independently justified the moving-test approximation, localization, quadratic variation and random-initial conditional laws. The primary-source family matched the finite-dimensional theorem and exact earlier archived claim; the reproduction family reproduced both historical suites and 29 fresh exact check groups. See ACCEPTANCE_AUDIT.md for their separate evidence and boundaries. A fresh complete adversary is the remaining acceptance gate. Matrix checks alone do not certify stochastic analytic steps. No new paper, Zenodo deposit or tracker row is planned for this credited partial outcome.
