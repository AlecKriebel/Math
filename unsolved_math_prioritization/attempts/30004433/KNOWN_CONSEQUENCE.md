# Ordinary graph ends in inverse-square long-range percolation

**Problem 30004433 / OWR-17474-007.** A credited consequence of classical percolation theorems gives a negative answer to both literal assertions, when “ends” has its usual graph-theoretic meaning. Separate adversarial review is pending. No novelty or human-peer-review claim is made.

## 1. Exact source and conclusion

Noam Berger's contribution “Survey on long-range percolation,” in [Oberwolfach Report 11/2020](https://ems.press/content/serial-article-files/46847), printed pp. 625–627, defines independent **undirected** edges on $\mathbb Z^d$, with displacement probabilities $p_j=p_{-j}\in(0,1)$. It then focuses on $d=1$ and $p_j\sim\beta |j|^{-s}$. Problem 2 on p. 626 asks whether the infinite cluster has two ends at criticality when $s=2$, and infinitely many ends in the supercritical case. No alternative definition of “ends” appears in that contribution.

For an infinite connected locally finite graph $C$, we use the standard criterion: $C$ is **one-ended** if deleting any finite vertex set leaves exactly one infinite connected component. This is equivalent to having one equivalence class of rays under finite vertex separation. Finite edge separation gives the same end notion for such graphs.

**Conclusion.** In the source's independent inverse-square model, every infinite cluster is almost surely one-ended, at every fixed parameter value at which such a cluster exists. This includes a critical parameter with positive percolation probability. The conclusion is conditional on existence, not an assertion that every critical model percolates. Section 4 supplies a concrete one-parameter family with a genuine critical infinite cluster, so the negative critical answer is not vacuous.

The key imported result is Aizenman–Kesten–Newman's uniqueness theorem [AKN, Proposition 1.1, p. 507]. It applies to long-range models, including the one-dimensional inverse-square critical case; its scope is not restricted to supercritical parameters. The deduction of one-endedness is given completely below.

## 2. A finite-set isolation lemma

Let $V$ be countable and let an undirected random graph on $V$ have independent edge indicators, with probabilities $p_e<1$. Suppose

1. almost surely there is at most one infinite connected component;
2. for every finite $S\subset V$, $\sum_{e:e\cap S\ne\varnothing}p_e<\infty$.

Then every infinite connected component is almost surely one-ended.

**Proof.** For each vertex $x$, the expected open degree is finite by assumption 2. Its open degree is therefore finite almost surely. Countability makes the entire open graph locally finite on one probability-one event.

Fix a finite deterministic $S\subset V$. Write $I_S$ for the countable set of all potential edges with an endpoint in $S$, and define

$$
 A_S=\{\text{every edge of }I_S\text{ is closed}\}.
$$

Countable independence and continuity from above give

$$
 a_S:=\mathbb P(A_S)=\prod_{e\in I_S}(1-p_e)>0. \tag{1}
$$

For completeness, summability implies that only finitely many $p_e$ exceed $1/2$. Their factors in (1) are positive. On the remaining edges,
$\log(1-p_e)\ge-2p_e$, so the tail product is bounded below by the positive number $\exp(-2\sum p_e)$. This proves strict positivity even though $I_S$ can be infinite.

Let $B_S$ be the event that the induced open graph on $V\setminus S$ has at least two infinite components. It depends only on edges outside $I_S$, and hence is independent of $A_S$. Measurability follows, for example, by writing infinitude and connectivity using countably many finite paths and finite vertex sets. On $A_S\cap B_S$ the full graph also has at least two infinite components: every vertex in $S$ is isolated, and no outside component gains an edge to $S$. Assumption 1 therefore implies

$$
 0=\mathbb P(A_S\cap B_S)=a_S\mathbb P(B_S),
 \qquad \mathbb P(B_S)=0. \tag{2}
$$

There are countably many finite subsets of $V$. Thus, simultaneously for every finite $S$, the graph outside $S$ has at most one infinite component, almost surely.

On this same probability-one event, suppose $C$ is an infinite connected component. If $S\cap C=\varnothing$, then $C$ remains connected. Otherwise, every component of $C\setminus S$ has an edge to $S\cap C$: follow a path in $C$ to that set. There are only finitely many such open edges, by local finiteness. Consequently $C\setminus S$ has finitely many components. It has infinitely many vertices, so at least one of those components is infinite. There is at most one by (2). This proves one-endedness. $\square$

The positive-probability step is an explicit infinite-product calculation. Applying ordinary finite-edge “finite energy” without addressing the infinitely many potential edges incident to $S$ would leave a gap; (1) closes it.

## 3. Application to the source model, including criticality

More generally, consider independent translation-invariant undirected bond percolation on $\mathbb Z^d$ with $0\le p_j<1$, symmetric probabilities, irreducible support, and

$$
 M:=\sum_{j\ne0}p_j<\infty.
$$

Irreducibility means that any two vertices have positive probability of being connected; in the source it is immediate because every $p_j>0$. These are precisely within the bond-model setup on p. 507 of [AKN]. If desired, its parametrization $p_j=1-\exp(-\beta J_j)$ is obtained by choosing $\beta=1$ and $J_j=-\log(1-p_j)$; no additional restriction is imposed.

Let $\theta=\mathbb P(|C(0)|=\infty)$. If $\theta=0$, translation invariance and countability imply that almost surely there is no infinite cluster. If $\theta>0$, [AKN, Proposition 1.1] gives exactly one infinite cluster almost surely. Thus assumption 1 of the lemma holds in both cases. For finite $S$,

$$
 \sum_{e:e\cap S\ne\varnothing}p_e\le |S|M<\infty,
$$

where edges internal to $S$ may be counted twice on the right. The lemma applies.

For $d=1$, $s=2$ and $p_j\sim\beta |j|^{-2}$, the sum $M$ is finite. No limiting argument in the percolation parameter was used. In particular, at any fixed critical value satisfying the same model assumptions, the theorem holds. When $\theta>0$ it also gives

$$
 \mathbb P\bigl(C(0)\text{ is one-ended}\mid |C(0)|=\infty\bigr)=1.
$$

When $\theta=0$ this conditional probability is not defined, and no such conditioning is asserted. An incipient infinite cluster obtained through a different limiting measure is outside this statement.

## 4. A nonvacuous critical and supercritical family

For $t\in(0,1)$, set

$$
 p_j(t)=
 \begin{cases}
 t,&|j|=1,\\
 1/64,&2\le |j|\le8,\\
 1-\exp(-2/|j|^2),&|j|\ge9.
 \end{cases} \tag{3}
$$

All probabilities lie strictly between zero and one, and $|j|^2p_j(t)\to2$. Only the nearest-neighbor probability varies. Let

$$
 \theta(t)=\mathbb P_t(|C(0)|=\infty),\qquad
 t_c=\inf\{t\in(0,1):\theta(t)>0\}.
$$

**A genuine transition.** For $0<t\le1/64$, using $1-e^{-x}\le x$ and the integral bound $\sum_{k=9}^{\infty}k^{-2}\le\int_8^\infty x^{-2}\,dx=1/8$ gives

$$
 \sum_{j\ne0}p_j(t)
 \le\frac{16}{64}+4\sum_{k=9}^{\infty}\frac1{k^2}
 \le\frac34<1. \tag{4}
$$

To see directly that (4) precludes percolation, let $M_t$ denote that sum. The expected number of open self-avoiding paths of length $n$ from 0 is at most $M_t^n$: independence applies to their distinct edges, and dropping the self-avoidance restriction in the sum only increases it. An infinite locally finite connected cluster contains paths of every finite length. Thus its probability is at most $M_t^n$ for every $n$, and is zero. In particular $t_c\ge1/64>0$.

Newman–Schulman [NS, Theorem 1.2, p. 549], applied with all site variables present and all $p_j$, $|j|>1$, fixed as in (3), gives percolation for $t$ sufficiently close to 1, since $\liminf j^2p_j=2>1$. Therefore $t_c<1$. Monotonicity then gives $\theta(t)>0$ for every $t>t_c$.

**Percolation at the critical point.** Aizenman–Newman [AN, Proposition 1.1, pp. 613–614] states that, for an independent translation-invariant regular one-dimensional model, positive percolation density satisfies $\beta\theta^2\ge1$, where $\beta=\limsup_{j\to\infty}j^2p_j$. Regularity here means all edge probabilities are less than 1. Consequently

$$
 \theta(t)\ge 1/\sqrt2\quad\text{for every }t>t_c. \tag{5}
$$

We justify passage to $t_c$ without assuming left continuity. For $R\ge1$, let $E_R$ be the event that 0 is connected to a vertex outside $[-R,R]$. A witnessing path can be stopped at its first exit, so $E_R$ depends only on edges with an endpoint in $[-R,R]$. Among them, only finitely many nearest-neighbor edges have probabilities depending on $t$; all other edges have a fixed joint law. Conditioning on those finitely many Bernoulli variables shows that $\mathbb P_t(E_R)$ is a polynomial, hence continuous, in $t$. Moreover

$$
 \theta(t)=\inf_{R\ge1}\mathbb P_t(E_R).
$$

It follows that $\theta$ is upper semicontinuous; since it is nondecreasing, it is right-continuous. Taking $t\downarrow t_c$ in (5) yields $\theta(t_c)\ge1/\sqrt2>0$.

Thus (3) at $t=t_c$ is a source-admissible critical model with a unique infinite cluster, and that cluster has **one** end almost surely. At any $t\in(t_c,1)$, for example $(1+t_c)/2$, it likewise has one end. This disproves both proposed end counts in ordinary graph terminology.

## 5. Attribution and exact scope

This is a consequence of [AKN], together with the elementary isolation argument; [NS] and [AN] make the critical example explicit and nonvacuous. It is not a claim of a newly discovered uniqueness, phase-transition, or discontinuity theorem. No published erratum to the workshop contribution or author endorsement was located. We do not infer what alternative question the speaker may have intended.

The conclusion does not address directed paths, a specially conditioned incipient law, spanning-tree ends, or any alternative use of “ends” that would require a different definition. The original contribution specifies none of these. Its separate triangle-condition Problem 1 is untouched.

The exact checks in `verify.py` audit finite probability factorizations, component deletion, tail estimates and finite-parameter continuity identities. They do not simulate or certify an infinite-cluster end count; that conclusion rests on the proof and the credited classical theorems.

### References

- **[OWR]** N. Berger, “Survey on long-range percolation,” Oberwolfach Report 11/2020 (published 2021), pp. 625–627, Problem 2 on p. 626. [Full report](https://ems.press/content/serial-article-files/46847), [DOI](https://doi.org/10.4171/OWR/2020/11).
- **[AKN]** M. Aizenman, H. Kesten and C. M. Newman, “Uniqueness of the infinite cluster and continuity of connectivity functions for short and long range percolation,” *Communications in Mathematical Physics* **111** (1987), 505–531. Proposition 1.1, p. 507; critical-case discussion, p. 506; proof reduction, pp. 524–525. [DOI](https://doi.org/10.1007/BF01219071), [full primary paper, university-hosted copy](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/aizenman_kesten_newman.pdf).
- **[NS]** C. M. Newman and L. S. Schulman, “One dimensional $1/|j-i|^s$ percolation models: the existence of a transition for $s\le2$,” *Communications in Mathematical Physics* **104** (1986), 547–571. Theorem 1.2, p. 549. [DOI](https://doi.org/10.1007/BF01211064), [full primary paper, university-hosted copy](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/newman_schulman_1d_long_range.pdf).
- **[AN]** M. Aizenman and C. M. Newman, “Discontinuity of the percolation density in one dimensional $1/|x-y|^2$ percolation models,” *Communications in Mathematical Physics* **107** (1986), 611–647. Proposition 1.1, pp. 613–614. [DOI](https://doi.org/10.1007/BF01205489), [full primary paper, university-hosted copy](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/aizenman_newman_1d_long_range.pdf).
