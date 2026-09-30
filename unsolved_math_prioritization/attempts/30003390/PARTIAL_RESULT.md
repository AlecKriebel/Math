# CIR approximation: exact information reductions and a boundary-case conditional optimizer

**30003390 / OWR-15214-002. Scoped partial result; independent review pending.** The full parameter-range rate conjecture remains unresolved in this attempt. The known rate theorems are credited to their authors. The conditional-information formulas below are elementary reconstructions, with no priority claim.

## 1. Exact question and verified prior results

The original contribution of Hefter and Jentzen is in [OWR 9/2017, printed pp.466–469](https://ems.press/content/serial-article-files/46671), rather than a 2018 report. For
$$
dX_t=(a-bX_t)\,dt+\sigma\sqrt{X_t}\,dW_t,\qquad X_0=x,
$$
with $T,a,\sigma>0$ and $b,x\ge0$, define
$$
e_N(a,b,\sigma,x,T)
=\inf_{\varphi:\mathbb R^N\to\mathbb R\ \mathrm{Borel}}
 \mathbb E\left|X_T-\varphi(W_{T/N},\ldots,W_T)\right|.
\tag{1}
$$
The conjectured polynomial order is $\min\{2a/\sigma^2,1\}$. Equation (4) of the report gives actual two-sided constant-factor bounds in a restricted regime. A statement about the supremal polynomial exponent and a two-sided bound without logarithmic loss should not be silently identified at an endpoint.

Write $\delta=4a/\sigma^2$. The following are **verified baseline results**, not an assertion that every later improvement has been exhaustively classified.

- For $0<\delta<2$, [Hefter–Jentzen, Theorem 1](https://arxiv.org/abs/1702.08761) gives $e_N\ge cN^{-\delta/2}$, including $x=0$ and $b\ge0$.
- For $0<\delta<1$, their Corollary 2 combines this with [Hefter–Herzwurm, Theorems 2 and 3](https://arxiv.org/abs/1608.00410) to give $e_N\asymp N^{-\delta/2}$. The latter source gives the general upper bound $C(1+\mathbf1_{\{\delta=1\}}\log N)N^{-\min(1,\delta)/2}$ after normalization, and keeps the observation information admissible.
- For $\delta=1,b=0$, [Hefter–Herzwurm, Corollary 1](https://arxiv.org/abs/1601.01455) gives $e_N\asymp N^{-1/2}$ for every $x\ge0$. Its Remark 7 also gives a logarithmic-loss upper bound for a stronger supremum-path error when $b\ne0$. The conditional formula below does not claim a new rate theorem.
- For $\delta>4,x>0$, [Hefter–Herzwurm–Müller-Gronbach, Corollary 14](https://arxiv.org/abs/1710.08707), using [Alfonsi's order-one theorem](https://arxiv.org/abs/1206.3855), gives $e_N\asymp N^{-1}$. The displayed source hypotheses $x>0$ are retained. The general scalar lower-bound paper also gives an adaptive $c/N$ lower bound outside $\delta=1,b=0$; that lower bound is weaker than the boundary lower bound when $\delta<2$.

The dataset labels arXiv:1710.08707 as Hefter–Jentzen; it is actually the three-author scalar lower-bound paper just cited. The full CIR boundary lower-bound paper is arXiv:1702.08761.

Later-source qualifications matter. [Hefter–Herzwurm–Ritter, Journal of Complexity 90 (2025), 101959](https://doi.org/10.1016/j.jco.2025.101959) announces a new CIR upper bound through reflected Ornstein–Uhlenbeck approximation. Its publisher abstract was recovered, but its full theorem was not retrieved in this attempt; no claim that the older logarithmic bound is currently optimal is made. The full [2024 truncated-method preprint](https://arxiv.org/abs/2410.05614), Corollary 4.6, requires Feller index $2a/\sigma^2>5$ for its displayed CIR results. [Pavlis–Çetin's July 2026 paper](https://arxiv.org/abs/2607.07552) concerns weak error; its theorem is not a terminal strong-error bound of the form (1). These sources do not supply a verified full-range resolution here. See `SOURCE_AUDIT.md` for access and scope details.

## 2. A normalization that preserves the observed information

Let $c=\sigma^2T/4$, $z=x/c$, $\beta=bT$, and
$$
B_s=T^{-1/2}W_{Ts},\qquad Z_s=c^{-1}X_{Ts}\quad(0\le s\le1).
$$
Brownian scaling and the SDE give
$$
dZ_s=(\delta-\beta Z_s)\,ds+2\sqrt{Z_s}\,dB_s,\qquad Z_0=z.
$$
The observed vectors are related by the invertible deterministic map
$(W_{jT/N})_j=\sqrt T(B_{j/N})_j$. Multiplying or dividing every admissible estimator by $c$ therefore proves the exact equality
$$
e_N(a,b,\sigma,x,T)
 =c\,e_N(\delta,\beta,2,z,1).
\tag{2}
$$
This equality preserves the number and equidistance of evaluations. It does not remove $\beta$.

## 3. The exact conditional decision problem

Let $G=(W_{T/N},\ldots,W_T)$ and let $\mu_g$ be a regular conditional law of $X_T$ given $G=g$. Such a Borel probability kernel exists because both variables take values in standard Borel spaces. Since the CIR terminal variable is nonnegative and integrable, its lower conditional median
$$
m(g)=\inf\{q\ge0:\mu_g([0,q])\ge1/2\}
\tag{3}
$$
is Borel measurable and integrable, after an arbitrary definition on a null exceptional set. Borel measurability follows by testing rational thresholds; integrability follows from $m(g)\le2\int y\,\mu_g(dy)$ whenever the conditional first moment is finite.

For any probability law on the real line with finite first moment, a median minimizes the mean absolute deviation. For completeness, if $u<v$,
$$
\int\bigl(|y-v|-|y-u|\bigr)\,\mu(dy)
 =\int_u^v(2F(t)-1)\,dt,
$$
where changing the distribution function at atoms does not affect the Lebesgue integral. The integrand has the appropriate sign on either side of any median. Conditioning and then integrating proves
$$
e_N=\mathbb E|X_T-m(G)|.
\tag{4}
$$
Thus (1) has an admissible minimizing estimator. This is an information-theoretic statement, not an efficient algorithm for arbitrary CIR parameters.

On an extended probability space, let $X_T'$ be an independent copy of $X_T$ conditional on $G$, and put
$$
D_N=\mathbb E|X_T-X_T'|.
$$
Then
$$
\frac12D_N\le e_N\le
\mathbb E\left|X_T-\mathbb E[X_T\mid G]\right|\le D_N.
\tag{5}
$$
Indeed, the triangle inequality through the conditional median gives $D_N\le2e_N$. Median optimality gives the middle comparison. Conditional Jensen applied to $X_T-X_T'$ gives the final comparison. All variables are integrable.

A canonical realization replaces the Brownian bridges between the observed grid points by independent bridges, while keeping all endpoints fixed. A measurable strong-solution functional for CIR applied to the original and resampled Brownian paths gives the required conditional copies. The resampled path has Brownian law because its Gaussian endpoint/bridge decomposition has that law; no independence of the two full paths is asserted. This is the usual coupling-of-noise mechanism underlying information lower bounds, stated here with both inequalities and the exact observation sigma-field.

Consequently a constant-factor rate bound for (1) is equivalent to the same rate bound for $D_N$. This equivalence does not estimate $D_N$: obtaining its missing parameter-dependent upper bound retains the central difficulty.

## 4. A complete finite-grid conditional formula when $\delta=1,b=0$

In this section only, use the normalized diffusion coefficient $2$, drift $1$, arbitrary $T>0$, and $X_0=r^2$ with $r\ge0$. The known pathwise representation is
$$
R_t=r+W_t+L_t,\qquad
L_t=\max\{0,-\min_{0\le s\le t}(r+W_s)\},\qquad X_t=R_t^2.
\tag{6}
$$
This can also be checked directly: $R\ge0$, the finite-variation regulator $L$ increases only where $R=0$, and Itô's formula gives $d(R^2)=dt+2R\,dW$. Pathwise uniqueness identifies the solution. This is the reflected-Brownian representation used by Hefter and Herzwurm; it is not the formula $X_t=(r+W_t)^2$ for the same Brownian driver.

The following calculation allows any deterministic partition $0=t_0<\cdots<t_N=T$, and specializes to the equidistant one in (1). Condition on $W_{t_i}=w_i$, with $w_0=0$. Set
$$
y_i=r+w_i,\quad h_i=t_{i+1}-t_i,\quad
\ell_0=\max\{0,-\min_{0\le i\le N}y_i\},\quad c=y_N.
$$
The conditional distribution function of $L_T$ is zero below $\ell_0$, and for $\ell\ge\ell_0$ it is
$$
F_w(\ell)=\prod_{i=0}^{N-1}
 \left[1-\exp\left\{-\frac{2(y_i+\ell)(y_{i+1}+\ell)}{h_i}\right\}\right].
\tag{7}
$$
To prove (7), the event $L_T\le\ell$ is exactly that every bridge of $r+W$ stays above $-\ell$. For a bridge of duration $h$ from $u$ to $v$, with $u,v\ge-\ell$, reflection at the barrier gives crossing probability
$$
\frac{\exp(-(v+u+2\ell)^2/(2h))}
     {\exp(-(v-u)^2/(2h))}
 =\exp(-2(u+\ell)(v+\ell)/h).
$$
At a barrier endpoint the survival probability is zero, consistent with the formula. The bridge segments are conditionally independent, so their survival probabilities multiply.

The only possible atom of $L_T$ is at zero. If $\ell_0=0$ and $F_w(0)\ge1/2$, let $q(w)=0$. Otherwise there is a unique $q(w)>\ell_0$ satisfying
$$
F_w(q(w))=1/2.
\tag{8}
$$
Existence and uniqueness follow because every factor is strictly increasing above $\ell_0$, the product starts below $1/2$, and it tends to one. The threshold definition makes $q$ Borel measurable. Since $c+\ell_0\ge0$, the map $\ell\mapsto(c+\ell)^2$ is increasing on the support. Hence
$$
\widehat X_T(w)=(c+q(w))^2
\tag{9}
$$
is an exact terminal $L^1$ optimizer among all Borel functions of these observations. This is a finite-grid oracle formula in a subclass whose asymptotic rate was already established.

Its conditional minimum error is also explicit as a one-dimensional integral:
$$
\mathcal E(w)=
 2\int_{\ell_0}^{q(w)}(c+\ell)F_w(\ell)\,d\ell
 +2\int_{q(w)}^\infty(c+\ell)(1-F_w(\ell))\,d\ell.
\tag{10}
$$
This follows from the distribution-function formula for mean absolute deviation, followed by $y=(c+\ell)^2$. It includes the zero-atom case without an extra term. The Gaussian tail of each bridge-crossing factor makes the integrals finite. For the equidistant grid, $e_N=\mathbb E\mathcal E(G)$.

For example, when $N=1,r=0$ and $W_T=w$, the root is
$$
q(w)=\frac{-w+\sqrt{w^2+2T\log2}}2,
\qquad
\widehat X_T(w)=\left(\frac{w+\sqrt{w^2+2T\log2}}2\right)^2.
\tag{11}
$$
In the natural continuous conditional-law version at $w=0$, $X_T$ is exponential with mean $T/2$, and both the optimal conditional estimate and the conditional minimum absolute error are $T\log2/2$. This conditional diagnostic is not conditioning on an event of positive probability.

Even a single observed endpoint leaves a nondegenerate conditional law in (7). Thus a distributional representation as a square of a Gaussian cannot be substituted for the same-driver solution when computing (1). The known $N^{-1/2}$ rate is credited, not re-proved or improved by (7)–(11).

## 5. Why the standard mean-reversion time change is not an exact observation reduction

For the normalized equation $dU_t=(\delta-bU_t)dt+2\sqrt{U_t}\,dW_t$, define, when $b>0$,
$$
q_b(t)=\frac{e^{bt}-1}{b},\qquad
\widetilde W_{q_b(t)}=\int_0^t e^{bs/2}\,dW_s,
\qquad Z_{q_b(t)}=e^{bt}U_t.
\tag{12}
$$
The deterministic stochastic-integral clock makes $\widetilde W$ Brownian, and Itô's formula gives $dZ_s=\delta\,ds+2\sqrt{Z_s}\,d\widetilde W_s$. Nevertheless, values of $\widetilde W$ at the transformed grid are not determined by the observed values of $W$.

In fact, on an interval $[u,u+h]$, put
$$
J=\int_u^{u+h}e^{bs/2}\,dW_s,\qquad V=W_{u+h}-W_u.
$$
Gaussian regression gives
$$
\mathbb E[J\mid V]=\frac{V}{h}\int_u^{u+h}e^{bs/2}\,ds,
\qquad
\operatorname{Var}(J\mid V)
 =\int_u^{u+h}e^{bs}\,ds
  -\frac1h\left(\int_u^{u+h}e^{bs/2}\,ds\right)^2>0.
\tag{13}
$$
Strict positivity is strict Cauchy–Schwarz because $b>0$. Other grid increments are independent and do not remove this conditional variance. Thus no Borel function of the original endpoint vector supplies these exact transformed Brownian observations. Also the transformed times $q_b(jT/N)$ are not equidistant.

For reference, the positive variance in (13) equals
$$
e^{bu}\left[\frac{e^{bh}-1}{b}
 -\frac{4(e^{bh/2}-1)^2}{b^2h}\right]
 =e^{bu}\frac{b^2h^3}{48}+O(h^4)
\quad(h\downarrow0).
\tag{14}
$$
This does not prove that every approximate transfer must fail: the missing Gaussian integral can be approximated, and its effect must then be estimated through the solution map. It proves that the algebraic time-change identity alone is not an admissible exact reduction of (1) to the $b=0$ information problem.

## 6. Remaining gap and outcome

Two routes were investigated: conditional bridge resampling, which yields (5) and the exact dimension-one formulas but no general rate estimate; and elimination of mean reversion, whose exact-information step fails by (13). Neither provides the full parameter-range upper bound or a counterexample to the conjecture. In particular the explicit reflected-Brownian formula has not been extended to dimensions $\delta\ne1$, and the resampling bound for those dimensions is not established here.

Recommended outcome: **unsolved, 2/5 substantive approaches**. The source correction, information equivalences, and exact boundary-case optimizer are the deliverables. No new asymptotic rate, exhaustive current-literature classification, algorithmic running-time bound, or historical-priority claim is made.
