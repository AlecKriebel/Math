# Adversarial classical-priority audit

Author of audit: independent adversarial subagent. UTC completed: 2026-10-04. Scope: ordinary-renewal all-scale obstruction and classical priority only. Candidate and other reviewer reports were not read. No Git mutation or communication with an external individual occurred.

## Verdict and recommendation

The proposed classical route is mathematically valid. For every strictly positive, finite-a.s. increment law with an ultimately positive slowly varying tail r(t)=P(X>t), every positive deterministic scale phi for which D_t/phi(t) has a proper finite weak limit produces only the degenerate limit zero. Monotonicity of phi is unnecessary. The continuous law with r(t)=1/(1+log t) for t>=1 is an explicit admissible non-lattice infinite-mean counterexample to the universal existential question.

The needed renewal asymptotic is explicitly covered by Erickson's original 1970 article, including the alpha=0 endpoint. The implication from that theorem to the all-scale obstruction is an exact elementary corollary, proved below. This is a strong verified classical-priority obstruction, not a conjectural similarity.

Under the user's supplied operational definition of `already_solved` (the open problem was not actually open and the intake found a priority issue), recommend reclassifying the **general existential target** as `already_solved` and omitting it from the claimed-solved paper workflow. Preserve the qualifier: **already implied by a classical theorem; no prior author located explicitly announcing a solution of Thorisson's later named question.** Do not state that Erickson himself answered that later question, or make a global firstness claim. No-paper recommendation applies to the general negative answer alone; no conclusion is made about any extra contribution in the unread candidate.

## 1. Exact setting and renewal identity

Let X_1,X_2,... be iid copies of X with 0<X<infinity almost surely. Put S_0=0, S_n=sum_{j=1}^n X_j, N(t)=max{k:S_k<=t}, and D_t=X_{N(t)+1}, for each real t>=0. Set

\[
r(x)=\mathbb P(X>x),\qquad U(t)=\sum_{k=0}^{\infty}\mathbb P(S_k\le t).
\]

These quantities are well-defined. For lambda>0 let q=E[e^{-lambda X}]. Strict positivity gives 0<q<1, and

\[
\mathbb P(S_k\le t)\le e^{\lambda t}q^k,
\qquad U(t)\le \frac{e^{\lambda t}}{1-q}<\infty.
\]

The monotone sequence S_k diverges to infinity almost surely: for each fixed t, the same bound implies P(lim_k S_k<=t)=0, and taking a countable union over integer t rules out a finite limit. Thus N(t) is finite, and strict positivity makes its crossing interval unique.

For x>=t, the events

\[
E_k=\{S_k\le t,\ X_{k+1}>x\}
\]

are disjoint, because E_k implies S_{k+1}=S_k+X_{k+1}>t. Their union is exactly {D_t>x}. Independence and the finite nonnegative sum therefore give

\[
\boxed{\mathbb P(D_t>x)=r(x)U(t),\qquad x\ge t.}\tag{1}
\]

The strictness is essential and has been retained on both sides. At x=t, an increment exactly equal to t is excluded from both sides; an increment greater than t crosses even from S_0=0. At a renewal epoch S_k=t, the chosen interval is the following interval, matching N(t)'s <= convention. No continuity or absence of atoms was used.

## 2. Verified classical input and its consequence

Assume r is slowly varying at infinity, meaning r(at)/r(t)->1 for every fixed a>0, and ultimately positive. Finiteness of X implies r(t)->0. The classical input is

\[
U(t)r(t)\longrightarrow1.\tag{2}
\]

For M>=1, identity (1) yields

\[
\mathbb P(D_t>Mt)
=\frac{r(Mt)}{r(t)}U(t)r(t)\longrightarrow1.
\]

For 0<M<1, comparison with {D_t>t} gives the same conclusion. Thus, through **all real t**,

\[
\frac{D_t}{t}\longrightarrow+\infty\quad\hbox{in probability}.\tag{3}
\]

## 3. Complete all-scale argument

Let phi(t)>0 be arbitrary, without any monotonicity or regularity assumption, and suppose

\[
Z_t:=D_t/\phi(t)\Rightarrow Y
\]

for a proper finite random variable Y as real t->infinity. Since Z_t>0, weak convergence gives Y>=0 almost surely.

### Tightness forces phi(t)/t->infinity

If this ratio did not tend to infinity, there would be real t_n->infinity and finite C>0 such that phi(t_n)<=Ct_n. For every fixed K>0, (3) then gives

\[
\mathbb P(Z_{t_n}>K)
\ge\mathbb P(D_{t_n}/t_n>CK)\longrightarrow1.
\]

This contradicts tightness of a sequence weakly converging to a proper finite law. Hence

\[
\phi(t)/t\longrightarrow\infty,\qquad \phi(t)\longrightarrow\infty.\tag{4}
\]

This is a subsequence contradiction, so oscillations of phi cannot evade it.

### All positive limiting survival probabilities coincide

Let a,b>0 be continuity points of the distribution of Y. By (4), a*phi(t)>=t and b*phi(t)>=t eventually, so (1) gives

\[
\mathbb P(Z_t>a)
=\frac{r(a\phi(t))}{r(b\phi(t))}\mathbb P(Z_t>b).
\]

Slow variation, with the base argument b*phi(t)->infinity, makes the ratio tend to one. Weak convergence at the chosen continuity points consequently implies

\[
\mathbb P(Y>a)=\mathbb P(Y>b).\tag{5}
\]

This argument never divides by a limiting survival probability: it remains valid if that probability is zero.

A probability law has at most countably many atoms, so positive continuity points exist arbitrarily far out and arbitrarily close to zero. Take such points a_j->infinity. Properness gives P(Y>a_j)->0, so (5) forces the common positive-continuity-point survival value to be zero. Next choose continuity points b_j decreasing to zero. Continuity of probability for increasing events gives

\[
\mathbb P(Y>0)=\lim_j\mathbb P(Y>b_j)=0.
\]

Together with Y>=0, this proves

\[
\boxed{Y=0\text{ almost surely}.}\tag{6}
\]

Thus neither a positive atom, a mixture with mass at zero, a positive constant, nor any other proper nondegenerate finite law is possible. Extended limits placing mass at infinity are outside the target; properness is exactly what excludes them.

## 4. Elementary admissible counterexample, independent of Tauberian theory

Define a probability law by the density

\[
f(x)=\frac{\mathbf1_{\{x>1\}}}{x(1+\log x)^2}.
\]

The substitution u=1+log x gives integral one. Its strict tail is one for 0<=t<1 and

\[
r(t)=\frac1{1+\log t}\qquad(t\ge1).
\]

It is strictly positive, finite almost surely, absolutely continuous and therefore non-lattice. Its mean is infinite because, for t>=2,

\[
\mathbb E[X]\ge\int_{t/2}^{t}r(x)\,dx
\ge\frac{t}{2(1+\log t)}\longrightarrow\infty.
\]

Its tail is slowly varying, since

\[
\frac{r(at)}{r(t)}=\frac{1+\log t}{1+\log t+\log a}\longrightarrow1
\]

for every fixed a>0.

For t>=1, the truncated first moment is

\[
\mu(t):=\mathbb E[X\mathbf1_{\{X\le t\}}]
=\int_1^t\frac{dx}{(1+\log x)^2}
\le\sqrt t+\frac{t}{(1+\tfrac12\log t)^2}.
\]

The split is at sqrt(t): the first integrand is at most one; on the second interval its denominator is at least (1+0.5*log t)^2. Consequently

\[
\frac{\mu(t)}{tr(t)}
\le\frac{1+\log t}{\sqrt t}
+\frac{1+\log t}{(1+\tfrac12\log t)^2}
\longrightarrow0.\tag{7}
\]

Let tau_t=min{n>=1:X_n>t} and T_t=S_{tau_t-1}, the time at which the first increment exceeding t starts. A direct Tonelli calculation, avoiding any optional-stopping assumption, gives

\[
\begin{aligned}
\mathbb E[T_t]
&=\sum_{i\ge1}\mathbb E[X_i\mathbf1_{\{i<\tau_t\}}]\\
&=\mu(t)\sum_{i\ge1}(1-r(t))^{i-1}
=\frac{\mu(t)}{r(t)}.
\end{aligned}
\]

If T_t<=t, all renewals before tau_t are at or before t, and the next increment exceeds t, so it is precisely the crossing interval. Markov's inequality and (7) give

\[
1\ge U(t)r(t)=\mathbb P(D_t>t)
\ge\mathbb P(T_t\le t)
\ge1-\frac{\mu(t)}{tr(t)}\longrightarrow1.
\]

This proves (2) for the explicit law without using a Tauberian theorem. Sections 2 and 3 therefore give a complete elementary negative answer for an admissible example. All estimates hold for real t, without a special subsequence.

## 5. Original-source authentication

Primary source: K. Bruce Erickson, *Strong renewal theorems with infinite mean*, Transactions of the American Mathematical Society 151 (September 1970), 263-291, DOI [10.1090/S0002-9947-1970-0268976-9](https://doi.org/10.1090/S0002-9947-1970-0268976-9). The independently retrieved [original-article PDF mirror](https://artefacts-discovery.researcher.life/full_text/DA-2/70/701906b973143f3a95ae9d71ba1f1921/full_text/2f02b7d15c78d9518a4b31fc4f6ed046.pdf) contains the identifying publication metadata, AMS copyright and printed page labels.

I visually read complete printed pages 263, 264, 265, 266, and 269. Verified locators:

- Page 263: n=0 is included; U(t)=U{[0,t]}.
- Page 264: r(t)=t^{-alpha}L(t), 0<=alpha<=1; nonarithmetic standing assumption.
- Page 265: Theorem 5, alpha=0 included: U(t)~t/[Gamma(1+alpha)Gamma(2-alpha)m(t)]; m(t)=integral_0^t r(x)dx.
- Page 266: Eq. (2.2) explicitly gives alpha=0 normalization, yielding U(t)~1/L(t)=1/r(t).
- Page 269: Lemma 1 gives t*r(t)/m(t)->1 at alpha=0.

Thus (2) is authenticated; the abstract's narrower scope does not restrict Theorem 5.

The publisher page was inaccessible to the browsing tool, and the attempted publisher PDF URL returned HTTP 404. The independently discovered mirror returned HTTP 200; bytes were saved as `evidence/erickson1970_original_article.pdf`, SHA256 `65716b4789f1f1b06400a286bb216fee368783c2eca7df750d2fe00d791b773b`. Exact URL, headers, status, final URL and UTC retrieval time are preserved in `evidence/source_retrieval.json`. The permitted other reviewer's article binary was not accessed.

## 6. Adversarial checks and exact historical boundary

| Challenge | Resolution |
|---|---|
| The old result might exclude alpha=0 | Original Theorem 5 and Eq. (2.2) explicitly include it. |
| Renewal function may omit the initial renewal or use a strict endpoint | Original uses n=0 and [0,t], exactly the present U. |
| Exact identity might fail at x=t or with atoms | Direct disjoint-event proof retains strict >x and weak <=t endpoints. |
| Non-lattice may secretly mean absolute continuity | Original definition is nonarithmetic; the general proof permits atoms. Explicit example is absolutely continuous. |
| Nonmonotone phi could evade large-scale comparison | Tightness forces phi(t)/t->infinity through all real t by a bounded-ratio subsequence contradiction. |
| A limiting atom could prevent comparison at 1 | Choose arbitrary positive continuity points; no particular threshold is privileged. |
| Limit with some mass at zero might survive | Common positive survival constant is zero by properness, forcing all mass to zero. |
| First-exceedance expectation might misuse Wald or independence | Direct Tonelli sum is displayed; each factor uses only iid independence. |
| Empirical finite-range observations might be promoted as proof | None used; conclusions follow from exact inequalities and limits. |
| Old theorem could be confused with an explicit prior answer | Keep implication and documentary prior-answer claim separate. |

The mathematical target is fully settled within this audit. The exact historical gap is whether a prior author explicitly stated the nonexistence of **any** deterministic multiplicative normalization for D_t, or explicitly resolved Thorisson's named later question. Targeted searches did not locate such an announcement, and this was not a comprehensive historical bibliography. The theorem's 1970 publication establishes the age of the sufficient classical input; it does not establish who first noticed this corollary.

The original Thorisson preprint URL was found independently through web search and its indexed first-section text matches the supplied renewal setting and Problem 1.2. Direct browsing timed out and native download failed with connection reset; that preprint was not visually inspected, so it is not used as an authenticated primary input for the proof or historical classification. Exact failed retrieval record is retained. The supplied ordinary-renewal statement is the audited target.

Recommended status in the current workflow: `already_solved`, qualified as **classical-corollary priority issue**, with **explicit_prior_named_answer_unverified**. No new paper on the general negative answer should be promoted from this audit. A genuinely additional claim would require its own statement and independent novelty review.

## 7. Reproducibility and independence

The independent first assessment was written before all article access and is frozen read-only in `00_independent_assessment_frozen.md`, SHA256 `498faee71b3ecde3fdb1c8cc94f78447e55307a95d790ef17e730c8a64956690`. Its hash was sent to the parent before primary-source retrieval. No candidate access occurred later.

`native_run.py` preserves exact argv, input/code hashes, UTC start/end times, exit status, and complete stdout/stderr for article downloads, rendering, and extraction in `executions/`. `retrieve_original.py` and `retrieve_thorisson.py` preserve their exact inputs. Source inspection was visual; extracted text was supplementary. No numerical mathematical computations or simulations were needed. This is a checkable analytic proof, not a claim of formal machine verification.
