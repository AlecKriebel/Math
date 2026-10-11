# Exact classical and nonsignalling values of the threefold Feige game

Problem 30006570 / OWR-14299906-007. Authored audit note, 11 October 2026.

## Review and edition status

This is an AI-assisted, unrefereed mathematical proof and audit edition. Its acceptance records an internal AI mathematical audit; it is not external human peer review or formal proof-assistant certification. No novelty is claimed. The exact classical and nonsignalling baseline values were already stated in the cited primary literature. The original quantum-comparison problem remains unresolved by this work.

This is a prose proof/audit edition, not a computational reproduction package. The complete elementary arguments and compact symbolic strategies are provided here. Executable programs, raw outputs, expanded event lists, copied source documents and private coordination material are not distributed. Historical computational checks are described with their scope and limits; they are not represented as new executions during edition preparation. The hand proofs do not depend on those omitted materials.

## Disposition

For the precise threefold game in the question, this note independently proves

\[
\omega_c(G_F^{\times3})=\frac5{16},\qquad
\omega_{ns}(G_F^{\times3})=\frac13,\qquad
\frac5{16}\leq\omega_q(G_F^{\times3})\leq\frac13.
\]

These two exact values are already stated in the primary literature. The contribution of this audit is a self-contained classical upper-bound proof replacing dependence on the reported exhaustive computer search, plus independently checkable exact certificates. No priority or novelty claim is made.

**The original question, whether the quantum value strictly exceeds the classical value, remains unresolved by this work.** A numerical search or the nonsignalling witness below is not a solution to it.

## 1. The exact problem and strategy models

The referee chooses independent uniform vectors
\(x=(x_1,x_2,x_3),y=(y_1,y_2,y_3)\in\{0,1\}^3\).
There are 64 equally likely pairs. Alice receives the entire vector \(x\), and Bob receives the entire vector \(y\). They cannot communicate. Their respective answers belong to \(\{0,1,\bot\}^3\). They win precisely when, for every \(i=1,2,3\),

\[
(a_i,b_i)=(\bot,x_i)\quad\text{or}\quad(a_i,b_i)=(y_i,\bot).
\tag{1}
\]

Thus all three coordinates must be won. The answers and measurement choices may depend jointly on all three local input bits. We impose no sequential, coordinatewise-product, synchronous, or three-player restriction.

A deterministic classical strategy is a pair of maps
\(f,g:\{0,1\}^3\to\{0,1,\bot\}^3\).
Every classical strategy, including shared and private randomization, is a convex combination of such pairs: one can sample a local response in advance for each of the finitely many possible questions and include these sampled tables in the shared random variable. The winning probability is linear, so its maximum is attained by a deterministic pair.

The quantum model is the finite-dimensional tensor-product model of the primary question: an arbitrary bipartite state \(\rho\) on \(H_A\otimes H_B\), and arbitrary local POVMs \(\{A_a^x\}_a,\{B_b^y\}_b\), with
\(p(a,b\mid x,y)=\operatorname{Tr}(\rho(A_a^x\otimes B_b^y))\).
The value is the supremum over all finite local dimensions, states, and measurements. No fixed-dimensional optimization in this note is promoted to a bound on this supremum.

A nonsignalling strategy is a nonnegative normalized conditional distribution whose Alice marginal \(p_A(a\mid x)\) is independent of \(y\), and whose Bob marginal \(p_B(b\mid y)\) is independent of \(x\). Every quantum strategy is nonsignalling, because summing a local POVM gives the identity. Every deterministic classical strategy is quantum-realizable in dimension one, which suffices for \(\omega_c\leq\omega_q\). General finite shared-randomness correlations also have finite-dimensional quantum realizations. Therefore \(\omega_c\leq\omega_q\leq\omega_{ns}\).

## 2. Classical upper bound without searching response tables

Fix any deterministic pair \((f,g)\). Make a bipartite graph with eight row vertices \(x\) and eight column vertices \(y\). Put an edge at exactly the winning pairs.

For \(k=0,1,2,3\), let \(R_k\) be the rows for which \(f(x)\) has exactly \(k\) occurrences of \(\bot\); let \(C_k\) be the columns for which \(g(y)\) has exactly \(3-k\) occurrences of \(\bot\). Write \(r_k=|R_k|\), \(c_k=|C_k|\).

A winning edge from \(R_k\) must end in \(C_k\): condition (1) requires complementary positions of \(\bot\). The edge set is consequently the disjoint union of four classes. Let \(e_k\) be the number of edges in class \(k\), and \(E=\sum_k e_k\).

For a fixed row \(x\in R_k\), Alice's \(3-k\) ordinary answers fix those \(3-k\) coordinates of \(y\). Only the other \(k\) coordinates are free. Hence at most \(2^k\) columns can win against that row, irrespective of Bob's map. Symmetrically, a column in \(C_k\) has at most \(2^{3-k}\) winning neighbors. Therefore

\[
e_k\leq 2^k r_k,\qquad e_k\leq 2^{3-k}c_k.
\tag{2}
\]

There is no assumption that these necessary inequalities are sufficient for an actual game strategy. An upper bound for this larger capacity class is still an upper bound for all strategies.

Define \(h(e)=\lceil e/2\rceil+\lceil e/4\rceil\) for nonnegative integers \(e\). We claim

\[
\left\lceil\frac{e}{2^k}\right\rceil+
\left\lceil\frac{e}{2^{3-k}}\right\rceil\geq h(e)
\quad(k=0,1,2,3).
\tag{3}
\]

For \(k=1,2\), this is equality. For \(k=0,3\), the left side is \(e+\lceil e/8\rceil\). The assertion is immediate at \(e=0,1\). For \(e\geq2\), \(\lfloor e/2\rfloor\geq\lceil e/4\rceil\), so already \(e\geq h(e)\). This proves (3).

By (2), (3), and \(\sum_i\lceil t_i\rceil\geq\lceil\sum_i t_i\rceil\),

\[
16=\sum_k(r_k+c_k)
\geq\sum_k h(e_k)
\geq\left\lceil\frac E2\right\rceil+
       \left\lceil\frac E4\right\rceil.
\tag{4}
\]

If \(E\geq21\), the right side is at least \(11+6=17\), a contradiction. Thus \(E\leq20\), and every classical strategy wins with probability at most \(20/64=5/16\).

This argument covers all \(27^{16}\) deterministic strategy pairs without enumerating them. In particular, it does not assume an a priori symmetry, a special response formula, a bounded number of local answer patterns, or a selected orbit of strategies.

## 3. An exact classical strategy attaining the upper bound

The following strategy is credited to Schmidt, Storgaard, Walter, and Zhao, Section 6.3 of their v3 manuscript [1]:

\[
\begin{aligned}
a_1&=\bot,& b_1&=y_2\wedge y_3,\\
a_2&=x_1\vee x_3,& b_2&=\bot,\\
a_3&=\begin{cases}\bot&x_1=0,\\1&x_1=1,\end{cases}
&b_3&=\begin{cases}y_2&y_2\wedge y_3=0,\\\bot&y_2\wedge y_3=1.\end{cases}
\end{aligned}
\tag{5}
\]

The first two coordinates win exactly when

\[
x_1=y_2\wedge y_3,\qquad y_2=x_1\vee x_3.
\tag{6}
\]

These conditions imply that the third coordinate wins. If \(x_1=0\), they give \(y_2\wedge y_3=0\) and \(x_3=y_2\); consequently \((a_3,b_3)=(\bot,x_3)\). If \(x_1=1\), they force \(y_2=y_3=1\), and \((a_3,b_3)=(y_3,\bot)\).

Among the sixteen quadruples \((x_1,x_3,y_2,y_3)\), exactly five satisfy (6):

- \(y_2=0\): \(x_1=x_3=0\), with either value of \(y_3\), giving two quadruples;
- \((y_2,y_3)=(1,0)\): \((x_1,x_3)=(0,1)\), giving one;
- \((y_2,y_3)=(1,1)\): \(x_1=1\), with either value of \(x_3\), giving two.

The unused bits \(x_2,y_1\) supply four choices each time. Exactly twenty of the sixty-four full input pairs win. This proves \(\omega_c(G_F^{\times3})=5/16\).

Exposition note on [1, pp. 21–22]: its conditional-probability presentation announces the event order \(W_2\mid W_1,W_3\), while the following displayed hypotheses directly establish \(W_1\cap W_2\Rightarrow W_3\). For (5), the reverse implication under \(W_1\) is also true, so \(W_1\cap W_2=W_1\cap W_3\). The printed probabilities and value are correct. The direct count above avoids any need to infer that unstated equivalence; this is a clarification, not a counterexample to the source's result.

## 4. Exact nonsignalling upper bound

Let \(p\) be any nonsignalling strategy. Define the total local marginal masses

\[
R_k=\sum_x\ \sum_{a:\#\bot(a)=k}p_A(a\mid x),\qquad
C_k=\sum_y\ \sum_{b:\#\bot(b)=3-k}p_B(b\mid y).
\]

These are real numbers, and \(\sum_kR_k=\sum_kC_k=8\). Define

\[
S_k=\sum_{x,y}\ \sum_{\substack{a,b:\text{(1) holds}\\\#\bot(a)=k}}
 p(a,b\mid x,y).
\]

Then the winning probability is \(64^{-1}\sum_kS_k\). For each fixed \(x,a\) with \(k\) bottom symbols, only \(2^k\) possible question vectors \(y\) can be compatible with winning. For each such \(y\), the total mass of compatible Bob answers is at most \(p_A(a\mid x)\). Nonsignalling makes this marginal the same for all those \(y\). Summing proves

\[
S_k\leq 2^kR_k.
\]

The corresponding argument at Bob's side proves \(S_k\leq2^{3-k}C_k\). Set
\(u=2^k\), \(v=2^{3-k}\). Taking the convex combination of these two inequalities with weights \(v/(u+v)\) and \(u/(u+v)\), respectively, yields

\[
S_k\leq\frac{uv}{u+v}(R_k+C_k)
=\frac8{2^k+2^{3-k}}(R_k+C_k)
\leq\frac43(R_k+C_k).
\tag{7}
\]

The four exact coefficients before the final relaxation are \(8/9,4/3,4/3,8/9\). Consequently

\[
\Pr[\mathrm{win}]=\frac1{64}\sum_kS_k
\leq\frac1{64}\frac43(8+8)=\frac13.
\tag{8}
\]

This is a dimension-independent upper bound for every nonsignalling strategy, and hence every quantum strategy. Unlike (4), it does not apply an integrality rounding to probability masses.

## 5. A rational nonsignalling strategy attaining 1/3

For each input \((x,y)\), assign probability \(1/3\) to each of the following first-coordinate output pairs:

\[
(a_1,b_1)=(\bot,x_1),\quad(y_1,\bot),\quad(1-y_1,1-x_1).
\]

In all three cases, set

\[
(a_2,a_3)=(\bot,x_2),\qquad (b_2,b_3)=(y_3,\bot).
\tag{9}
\]

All other outputs have probability zero. The three displayed events are distinct, so the distribution is normalized and nonnegative. Alice's first-coordinate marginal is uniform on \(\{0,1,\bot\}\), independent of \(y\); her remaining outputs depend only on \(x\). Bob's first marginal is likewise uniform, and his remaining outputs depend only on \(y\). Thus the full vector-valued marginals are nonsignalling.

The first coordinate wins in two of the three equiprobable events. The second and third coordinates both win precisely when \(x_2=y_3\), which holds for one half of uniformly chosen questions and is independent of the first-coordinate random choice. Hence the winning probability is \((2/3)(1/2)=1/3\). This is the product witness also described in [1, Section 6.3]. It is not asserted to be quantum-realizable.

## 6. Historical exact verification and search coverage

The accepted underlying audit included two separately implemented standard-library verification routes. Those programs and their expanded certificate records are not part of this prose edition. This section records historical verification scope; the full proofs in Sections 2–5 remain self-contained.

The first route used tuple-valued coordinates. It checked all 432 local question-answer degree cases, evaluated the classical strategy on all 64 question pairs, and enumerated all 165 nonnegative four-part compositions of 8 for each side. For each of the resulting 27,225 composition pairs it evaluated the sum over k of min(2^k r_k, 2^(3-k) c_k), whose maximum is 20. It checked normalization and both full-vector nonsignalling conditions by exact rational arithmetic.

The second route used bit masks for questions and bottom-position patterns. It rederived the Boolean strategy and symbolic nonsignalling support, checked the winning predicate in that encoding, and used a separate four-stage max-plus dynamic program over all row and column budgets at most 8. It also checked the integer vertex-cost inequality on the complete finite edge-count range relevant to the game.

The capacity enumeration covers every deterministic strategy because Section 2 proves that each strategy induces one of its composition pairs and satisfies its capacity constraints. This is a relaxation: fictitious capacity patterns can only enlarge the bound. For the dynamic program, induction on the stage shows that an entry (r,c) maximizes the sum of the processed class capacities over every allocation of precisely those budgets. Each transition considers every next-class row and column count. The fourth-stage entry (8,8) thus covers every allocation. Neither route relies on a source author's program, solver tolerance, randomized search, or unverified pruning.

The independent audit added a third reconstruction, importing neither prior implementation. It checked the game predicate, degree capacities, symbolic witnesses, integer vertex costs and exact rational marginals. Its historical coverage and malformed-input controls are detailed in AUDIT.md and summarized in VERIFICATION.json. Normal, -O and -OO runs were recorded separately, with explicit exception-based failures rather than removable assertions. These checks audit finite encodings and arithmetic; they do not replace the hand proofs or certify the unresolved quantum comparison.

## 7. What remains open

Nothing in the integer edge proof transfers the ceiling operation to quantum marginal masses. Applying (4) to fractional, quantum, or nonsignalling probabilities would be invalid. Likewise, (8) only yields the upper endpoint 1/3; the nonsignalling witness is not an entangled strategy.

Restricted numerical explorations of two-dimensional binary-outcome families and three-dimensional projective strategies did not produce a probability above 5/16 within floating-point tolerance. They are retained as exploration records only, are outside the exact proof dependency graph, and give no upper bound even for those dimensions. The heuristic also failed to recover the known one-copy optimum in a separate calibration, further underscoring that absence of a found advantage is not evidence of optimality. General POVMs, higher dimensions, and possible nonattainment of the supremum are not eliminated. The original comparison requires either a rigorously certified quantum strategy above 5/16, or a quantum upper-bound proof of 5/16 for the whole intended model. This note supplies neither.

## References and literature boundary

[1] Simon Schmidt, Sigurd A. L. Storgaard, Michael Walter, and Yuming Zhao, *Guess your neighbor's input: Quantum advantage in Feige's game*, arXiv:2510.08484v3, 25 February 2026. https://arxiv.org/abs/2510.08484v3 . Sections 2, 3, and 6.3 specify the model, game, and threefold baselines; pp. 4 and 18 explicitly state the unresolved quantum comparison.

[2] *Noncommutative Harmonic Analysis and Quantum Information*, Oberwolfach Reports 4/2026, DOI 10.4171/OWR/2026/4, published 21 July 2026; Simon Schmidt's contribution on printed pp. 239–241. https://ems.press/journals/owr/articles/14299906 . The exact threefold question appears on printed p. 241 (PDF p. 25).

The arXiv version page was checked on 11 October 2026 and still listed v3 as its latest revision. A bounded title/identifier/threefold search found no primary resolution of the exact quantum comparison. This is a scoped literature check, not proof that no other resolution exists and not a novelty certification. The authors' one-copy theorem, even-repetition results, and synchronous variant do not settle this threefold question and are not used as substitutes for it.
