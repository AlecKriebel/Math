# A finite-time explosion example for the contact process

**Problem:** 30005044 / OWR-9790363-003. **Author turn:** 1 of at most 5; zero added by correction or review.
**Current assessment:** `already_solved` for the exact qualitative existential target, as an elementary consequence of established weighted-Galton–Watson explosion theory with the contact-process coupling written out in [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md). The accepted quantitative theorem below is preserved. Originality and research significance of its explicit bound are unestablished; no firstness, current-openness, new-mechanism, paper, merge or DOI clearance is claimed. Submitted `claimed_solved` remains a historical eligibility fact.

## 1. Exact target and theorem

Cardona–Tobón and Ortgiese's OWR 12/2022 contribution, pp. 618–620, equips a Galton–Watson tree with vertex fitnesses in $[1,\infty)$, infection rate $\lambda F_uF_v$ across an edge, and recovery rate 1. Only the root is initially infected. The question on p. 619 asks whether explosion **can** occur when the offspring mean is infinite. It does not assert that every infinite-mean offspring distribution must explode.

Let $\xi$ be the almost surely finite positive integer random variable specified by

$$
\mathbb P(\xi\ge m)=m^{-1/4}\quad(m=1,2,\ldots),\qquad
\mathbb P(\xi=m)=m^{-1/4}-(m+1)^{-1/4}.
$$

Let $T$ be its rooted Galton–Watson tree and initially infect only its root. Take $F_v=1$ at every vertex. For every $\lambda>0$, the minimal graphical contact process satisfies the explicit **annealed** bound

$$
\boxed{\quad
\mathbb P\bigl(|X_{1/(2\lambda)}|=\infty\bigr)
\ \ge\ \frac7{30}\exp\!\left(-\frac3{2\lambda}\right)>0.
\quad} \tag{1}
$$

The same lower bound holds after adding any finite fitnesses $F_v\ge1$. In particular it also holds for independent, identically distributed, unbounded fitnesses in the source model, if that additional feature is desired.

Moreover, for almost every realization of $T$, **for every $\lambda>0$** the conditional probability of explosion at some finite time is positive. This last assertion does not claim a uniform quenched lower bound or a common deterministic explosion time for all trees.

The offspring law is supported on finite integers, so the tree is locally finite almost surely; no infinite-degree vertex is used. It has $\xi\ge1$ almost surely and

$$
\mathbb E\xi=\sum_{m\ge1}m^{-1/4}=\infty.
$$

The proof below is self-contained. Rapid-growth infection rays and graphical monotonicity are established methods; see the specific credits in §7.

## 2. Graphical definition, including the explosive regime

Conditionally on the tree, put independent rate-$\lambda$ Poisson arrow processes on **ordered** adjacent pairs, and independent rate-1 recovery processes on vertices. A point $(v,t)$ is infected when there is a finite space-time path from the root at time 0 to $(v,t)$ that follows arrows forward in time and crosses no recovery mark. Equivalently, use the increasing union of the contact processes restricted to finite balls, coupled through these same marks. Every such ball is finite, since the offspring numbers are finite.

This is the finite-infection-path definition used in Bartha–Komjáthy–Valesin (2026), §3.1, equation (19), which explicitly permits finite-time explosion. It is our explicit choice of graphical extension in the potentially explosive regime; no uniqueness of post-explosion continuation is asserted for the OWR question or for the finite-mean author model. It requires no assumption that the total infected set is finite. We only exhibit ordinary finite infection paths to each of countably many vertices at a common time. No path originating at infinity and no continuation through infinitely many jumps is assumed.

It suffices to use downward arrows. Upward arrows and reinfections can only add infection paths. After the constant-fitness proof, the extra rate $\lambda(F_uF_v-1)\ge0$ can be added independently on each directed edge. All rates at an individual edge are finite.

## 3. A ray chosen without looking at recoveries

Fix $\lambda>0$ and define deterministic thresholds and times

$$
D_n=16^{n+2}=2^{4n+8},\qquad
\ell_n=\frac{2^{-n-2}}\lambda,\qquad
s_n=\sum_{j=0}^{n-1}\ell_j=\frac{1-2^{-n}}{2\lambda},\qquad
\tau=\frac1{2\lambda}.
$$

Thus $s_0=0$, $s_{n+1}-s_n=\ell_n$, and $s_n\uparrow\tau$.

Expose the root's offspring count. The event $H=\{\xi_\rho\ge D_0\}$ has probability $256^{-1/4}=1/4$. On $H$, set $v_0=\rho$. Suppose $v_n$ has been selected and its offspring count is at least $D_n$. Inspect only its first $D_n$ children, in the usual ordering of a Galton–Watson tree. A child $u$ is eligible if both

1. its own offspring count is at least $D_{n+1}$, and
2. the arrow process $v_n\to u$ has a point in the deterministic interval $[s_n,s_{n+1})$.

If there is an eligible child, select the first one as $v_{n+1}$; otherwise this construction fails. It never inspects a recovery process.

### Conditional independence at an adaptive vertex

When a vertex is selected, its offspring count may have been exposed and biased by selection. This is harmless: that count is known to be at least the required threshold, and only the first $D_n$ children are used. Their offspring counts have not been exposed at any earlier step. Neither have the outgoing arrow processes from the newly selected vertex. These variables are mutually independent and have their original laws, conditionally on the entire exploration history. Selection at the preceding step used only the vertex's own offspring count and its incoming arrow process. It did not use any of the variables now being inspected. This proves the needed conditional product law without asserting that the selected degrees themselves remain unconditioned iid variables.

For each inspected child the conditional success probability is exactly

$$
p_n=D_{n+1}^{-1/4}(1-e^{-\lambda\ell_n})
=2^{-n-3}(1-e^{-2^{-n-2}}).
$$

For $0\le x\le1$, $1-e^{-x}\ge x/2$ (for example, use $e^{-x}\le1-x+x^2/2$). Therefore

$$
p_n\ge2^{-2n-6},\qquad
D_np_n\ge2^{2n+2}=4^{n+1}.
$$

The conditional probability that stage $n$ fails is consequently at most

$$
(1-p_n)^{D_n}\le e^{-D_np_n}
\le e^{-4^{n+1}}
\le2^{-4(n+1)}. \tag{2}
$$

The last inequality follows from $4^{n+1}\ge4(n+1)$ and $e>2$.

No independence of the stage-success events is needed. Sum the probabilities of the disjoint first-failure events, using (2) conditionally at each stage. Given $H$, the probability of any failure is at most

$$
\sum_{n\ge0}2^{-4(n+1)}=\frac1{15}.
$$

Hence the event $G$ that the procedure constructs an infinite descendant ray has

$$
\mathbb P(G)\ge\frac14\left(1-\frac1{15}\right)=\frac7{30}. \tag{3}
$$

This entire event, the selected vertices, and all the arrow times depend only on the tree and arrows. They are independent of every recovery process, conditional on that tree and arrow data.

## 4. Summable recovery windows give simultaneous infections

On $G$, impose the following additional event $R$:

- no recovery at $v_0$ in $[0,\tau]$;
- for every $n\ge1$, no recovery at $v_n$ in $[s_{n-1},\tau]$.

The vertices $v_n$ are distinct. Conditional on the tree and all arrows, their recovery processes are independent rate-1 Poisson processes. The sum of the lengths of the forbidden intervals is finite and **deterministic**:

$$
\tau+\sum_{n=1}^\infty(\tau-s_{n-1})
=\tau+\tau\sum_{n=1}^\infty2^{-(n-1)}
=3\tau=\frac3{2\lambda}.
$$

Taking decreasing limits of the finite collections of no-recovery events gives

$$
\mathbb P(R\mid T,\text{all arrows})=e^{-3/(2\lambda)}\qquad\text{on }G. \tag{4}
$$

This is precisely where recovery must be accounted for. Requiring all ray vertices to avoid recovery throughout $[0,\tau]$ would have probability zero; the late vertices instead require only the shrinking windows specified above.

On $G\cap R$, the root stays infected until $\tau$. If $v_n$ is infected by $s_n$, an eligible arrow in $[s_n,s_{n+1})$ infects $v_{n+1}$ by $s_{n+1}$, and its recovery-free window started at $s_n$, before that arrow. Both vertices then remain infected until $\tau$. Induction proves that every $v_n$ is infected at $\tau$.

For each fixed $n$, this induction uses just $n$ arrows and finitely many vertical segments. Its infection path is contained in the finite ball of radius $n$. Thus the conclusion is valid for the minimal graphical process and is not merely a claim about infinitely many vertices infected at different earlier times. Combining (3) and (4) proves (1).

## 5. Almost-sure quenched possibility of explosion

This section strengthens, but is not required for, the existential source answer. Fix $\lambda>0$ and its $\tau=1/(2\lambda)$. Call a rooted locally finite tree *good* if its root-started contact process has positive probability of an infinite infected set at at least one of the deterministic times

$$
\tau,\ \tau+1,\ \tau+2,\ldots.
$$

This is a measurable property: configurations at each fixed time are given by countably many finite-path events, and the time set is countable. Let $q$ be the probability that a Galton–Watson tree with the specified law is good. Equation (1) implies $q>0$.

If a child subtree is good, the whole tree is good. Indeed, with probability at least $(1-e^{-\lambda/2})e^{-2}>0$, the root and this child have no recoveries during $[0,1]$ and there is an arrow from the root to the child in $[0,1/2]$. The child is then infected at time 1. The Poisson marks after time 1 are independent of this event. Suppress all edges outside its descendant subtree, restart there from only the child, and use graphical monotonicity. A positive-probability infinite configuration at its time $\tau+m$ yields one for the original process at $\tau+(m+1)$. If the good property was initially expressed as positive probability of the union over $m$, some particular $m$ has positive probability, by countability.

The descendant subtrees are independent copies of the original Galton–Watson tree. The above inheritance implies

$$
1-q\le\mathbb E[(1-q)^\xi].
$$

If $0<q<1$, then $\xi\ge1$ almost surely and $\mathbb P(\xi\ge2)>0$ give the strict inequality $\mathbb E[(1-q)^\xi]<1-q$, a contradiction. Therefore $q=1$.

First apply this argument to every positive rational infection rate and intersect the resulting countably many probability-one sets of trees. For any real $\lambda>0$, choose a positive rational rate below it and apply graphical monotonicity. This proves the asserted simultaneous-in-$\lambda$ quenched statement. Fitnesses $F_v\ge1$ again preserve it by adding arrows.

## 6. Scope and limitations

- This answers the source's existence question affirmatively with an explicit a.s.-finite offspring law of infinite mean. It does **not** classify all infinite-mean laws or claim that infinite mean alone is sufficient for every law.
- The quantitative bound (1) is annealed. The quenched conclusion is positive probability at some finite time for almost every tree; its time and probability need not be uniform in the tree.
- Explosion means infinitely many **simultaneously** infected vertices at a finite time. Mere survival forever or a finite-total-weight first-passage ray would not alone prove this conclusion.
- The construction uses $F\equiv1$, an allowed degenerate iid fitness distribution, and also works for every finite fitness assignment bounded below by 1. It does not extend the source question to fitnesses approaching zero.
- No infinite offspring value, external source of infection, change in recovery rate, or boundary condition at infinity is used.
- No scientific, biological, or computational simulation claim is intended; this is a probability theorem for the stated mathematical process.

## 7. Sources, prior implications and credit

1. **Historical question:** N. Cardona–Tobón and M. Ortgiese, “The inhomogeneous contact process on Galton-Watson trees,” OWR 12/2022, printed pp. 618–620, especially p. 619 (PDF pp. 42–44); [official report](https://ems.press/content/serial-article-files/46949), DOI [10.4171/owr/2022/12](https://doi.org/10.4171/owr/2022/12). The workshop was in 2022; the report was published 11 March 2023. Its existential wording and constant-fitness case define the target here.
2. **Original model and finite-mean results:** Cardona–Tobón and Ortgiese, [arXiv:2110.14537v1](https://arxiv.org/pdf/2110.14537v1), 27 October 2021, Definition 2.1 and pp. 4–5. Their later “The contact process with fitness on random trees,” [arXiv:2110.14537v4](https://arxiv.org/pdf/2110.14537v4), 14 July 2026, Theorem 3.2, p. 11; [publisher version](https://doi.org/10.1017/apr.2026.10066), online 13 July 2026, Theorem 3, p. 10. Complete original versions and the actual publisher paper were independently audited and retain finite offspring mean. Their nonexplosion statements do not apply to this example.
3. **Decisive older general theorem:** O. Amini, L. Devroye, S. Griffiths and N. Olver, “On explosions in heavy-tailed branching random walks,” *Annals of Probability* 41(3B) (2013), 1864–1899, DOI [10.1214/12-AOP806](https://doi.org/10.1214/12-AOP806); [arXiv:1102.0950v3](https://arxiv.org/pdf/1102.0950v3), reprint/PDF pp. 2, 6–7 and 12. Their printed Equivalence theorem and Theorem 1.3 concern weighted trees. Recovery-free vertex thinning preserves the required plump offspring tail; exponential downward arrow waits satisfy the criterion. The complete audit-written coupling in [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md) then gives positive annealed probability of infinitely many simultaneous infections at every fixed H>0 and lambda>0. This is category (b): an established general theorem plus a demonstrated elementary corollary. No exact older printed contact-process theorem was located in the bounded audit; no firstness of the coupling is asserted.
4. **Established infection-ray proof and finite-path definition:** Z. Bartha, J. Komjáthy and D. Valesin, “Degree-penalized contact processes,” [arXiv:2310.07040v1](https://arxiv.org/pdf/2310.07040v1), 10 October 2023, pp. 38–41; *Forum of Mathematics, Sigma* 14 (2026), e6, DOI [10.1017/fms.2025.10144](https://doi.org/10.1017/fms.2025.10144), Definition 1.7, p. 6, equation (19), p. 17, and Proposition 6.2/proof, pp. 46–48. The printed proposition states survival. Its existing degree-pool/rate estimates, with an independently verified timing and residual-recovery addendum, also imply qualitative simultaneous explosion. The 2023 v1 covers this law at penalty mu=1/2 and the classical process dominates it; the published proof also permits mu=0. Describing this as only a loosely related survival method understates its implication; calling the proposition a printed simultaneous-explosion theorem overstates it.
5. **Prior original-author anticipation:** N. Cardona–Tobón, M. Ortgiese, A. Seiler and A. Sturm, “The contact process on dynamical random trees with degree dependence,” [arXiv:2406.12689v1](https://arxiv.org/pdf/2406.12689v1), 18 June 2024, pp. 15–16; [v2](https://arxiv.org/pdf/2406.12689v2), 10 March 2026, p. 16. They discuss classical finite-time explosion for offspring mass exponent b in (1,2), identify the BKV route and suggest removing penalization. The present mass is asymptotic to (1/4)m^(-5/4), so b=5/4 belongs to that anticipated regime. This is affirmative prior anticipation in qualified discussion, rather than the exact theorem or bound printed here.

The direct proof in §§1–6 supplies the accepted explicit time 1/(2lambda) and bound (7/30)exp(-3/(2lambda)). The older-theory implications do not supply those constants; this does not establish their originality, sharpness, optimality, broader scope or research significance. The almost-every-tree/all-rates upgrade is also obtainable by an elementary hereditary argument from older-theory annealed positivity. The whole historical existential target is resolved by established theory. A future quantitative/refinement research contribution needs a separate exact target and affirmative originality/significance evidence. [CURRENT_ASSESSMENT.json](CURRENT_ASSESSMENT.json), [SOURCE_GATE.md](SOURCE_GATE.md) and [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) give operative status and limits.
