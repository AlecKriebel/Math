# Proof audit for the attracting edge application

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed. It is an audit of the prior Cotar–Thacker result, whose journal publication is bibliographically verified. The report itself has no journal peer review or proof-assistant certification.

## Scope and disposition

This is an authored verification of an existing result of Cotar–Thacker, using their finite count-vector/order-statistic method. It is not a new solution claim or a new proof-search turn. The full relevant edge-reinforcement argument in arXiv:1509.00807v3, pp.7–19, and the auxiliary summability statements on pp.36–37 were read. The original question, theorem pages, and disputed formula were also inspected as rendered PDF pages.

**Verified here:** fixation on every finite connected simple graph when every initial-offset reciprocal series converges; and on every infinite connected bounded-degree simple graph when the initial offsets take finitely many values and the reciprocal series converges for each such value. In particular, this verifies the original triangle and ordinary common-integer-initialization target without any monotonicity assumption. The argument includes the finite-state induction, a summable coercive function, the finite-range estimate with the initial-step correction, and the confinement-to-fixation step.

**Not certified here:** every real edge-dependent initial state allowed by the statement of Theorem 1.1 solely under (6),(8); the published proof as distinct from the inspected manuscript; the vertex-reinforcement results; or the unrelated extensions in Remarks 2.6 and 2.10. A precise problem with the manuscript's displayed formula (36) is documented in Section 5. Sections 3–4 repair the needed ordinary-initialization argument without relying on that formula.

## 1 A summable increasing test function

For a finite family of nonnegative summable sequences \(a_e(r)\), \(r\ge0\), let \(A(r)=\sum_e a_e(r)\). Choose increasing integers \(b_j\to\infty\) such that \(\sum_{r\ge b_j}A(r)\le2^{-j}\). Then

\[
g(r)=1+\sum_{j\ge1}{\bf1}_{\{r\ge b_j\}}
\]

is finite for finite r, nondecreasing, tends to infinity, and satisfies

\[
\sum_{r\ge0}g(r)A(r)
=\sum_{r\ge0}A(r)+\sum_{j\ge1}\sum_{r\ge b_j}A(r)<\infty.
\]

All sums contain nonnegative terms, so their exchange is legitimate. This proves the precise summability fact needed from manuscript Lemmas 3.10–3.11. No increase assumption on any reinforcement weight is used.

## 2 Finite graph proof checked from the count-vector recursion

Let H be finite, connected, and have m edges, with a nonisolated starting vertex. Write

\[
W_e(r)=w(\ell_e+r),\quad a_e(r)=W_e(r)^{-1},\quad
A_e=\sum_{r\ge0}a_e(r)<\infty.
\]

The term at r=0 is finite by positivity. Define

\[
K=\frac{\prod_{e\in E(H)}W_e(0)}{\min_{e\in E(H)}W_e(0)}.
\]

For a vector \(r\in\mathbb N_0^{E(H)}\) with \(\sum_e r_e=n\), set

\[
q_n(r,v)=\mathbb P(N_e(n)=r_e\ \forall e,\ I_n=v).
\]

We verify the Cotar–Limic/Cotar–Thacker count-vector bound

\[
q_n(r,v)\le K\Bigl(\sum_{e\ni v}W_e(r_e)\Bigr)\prod_{e\in E(H)}a_e(r_e).\tag{A}
\]

At n=0, the bound is zero-versus-positive unless v is the starting vertex; there its right side is the sum of the incident initial weights divided by the minimum initial edge weight, hence at least one.

For the induction, a predecessor of (r,v) must end at a neighbor u and have counts \(r-\mathbf1_e\), where \(e=\{u,v\}\) and \(r_e\ge1\). Multiply (A) for that predecessor by its transition probability

\[
\frac{W_e(r_e-1)}{\sum_{f\ni u}W_f(r_f-\mathbf1_{f=e})}.
\]

The incident sum and \(W_e(r_e-1)\) cancel exactly. The resulting term is at most

\[
K\prod_{f\ne e}a_f(r_f)=K W_e(r_e)\prod_f a_f(r_f).
\]

Sum over possible incoming e. Enlarging to all edges incident to v gives (A). The argument uses the undirected count convention and the actual transition rule. It does not compare adjacent reinforcement values.

Suppose m≥2. Let \(R_2(r)\) denote the second-largest coordinate of r. Use Section 1 to choose a common nonnegative, nondecreasing, unbounded g for the finite family \(a_e\), and put

\[
M_e=\sum_{r\ge0}g(r)a_e(r)<\infty.
\]

For each omitted edge j,

\[
g(R_2(r))\le\sum_{i\ne j}g(r_i).\tag{B}
\]

Indeed, among the coordinates other than j at least one is as large as the second-largest coordinate. In (A), expand the incident sum, so its j term cancels \(a_j(r_j)\). In the sum over \(\sum r_e=n\), all coordinates other than j uniquely determine \(r_j\). Thus removing the nonnegativity constraint on that determined coordinate gives an upper bound by the unrestricted sums over the other coordinates. Using (B),

\[
\mathbb E_H g(R_2(N(n)))
\le K\sum_{v\in V(H)}\sum_{j\ni v}\sum_{i\ne j}
M_i\prod_{e\notin\{i,j\}}A_e=:C_H<\infty.\tag{C}
\]

An empty product is one. This supplies a bound independent of n and also treats m=2. It is a reorganization of the paper's finite count-vector method, avoiding the longer intermediate convolution notation.

Each edge count is nondecreasing in n, hence so is its second order statistic. Monotone convergence and (C) give a finite expectation for \(g(R_2(\infty))\), where \(g(\infty)=\infty\). Therefore \(R_2(\infty)<\infty\) almost surely. Since infinitely many total traversals are distributed among finitely many edges, at least one edge has unbounded count. At most one does, because two unbounded coordinates would force the second order statistic to diverge. Each other edge has a finite total count, so the finite union of their traversal times has a last element. Thereafter the walk traverses the unique remaining edge forever. When m=1, this conclusion is deterministic.

This proves the finite theorem needed for the triangle, including arbitrary finite initial offsets for which the shifted reciprocal sums converge. It does not use any infinite-graph lemma.

## 3 Corrected frontier trapping bound for finite sets of offsets

Now let G be infinite, connected, and have maximum degree D<∞. Suppose all initial offsets lie in a finite set \(\Lambda\subset[0,\infty)\), and

\[
S_0=\max_{\lambda\in\Lambda}\sum_{j=0}^{\infty}\frac1{w(\lambda+j)}<\infty.
\]

Set

\[
B_0=\max_{\lambda\in\Lambda}w(\lambda),\qquad
B_1=\max_{\lambda\in\Lambda}w(\lambda+1),\qquad
A=B_1+D B_0.
\]

These constants are finite. In particular, for common offset L, \(B_0=w(L)\), \(B_1=w(L+1)\), and \(S_0=\sum_{j\ge0}1/w(L+j)\). Define \(p=\exp(-A S_0)>0\).

Center graph distance at the starting vertex. For every integer n≥1, let V_n contain the vertices at distance n having a neighbor at distance n+1, and let \(\tau_n\) be the first time the walk visits V_n. For an infinite locally finite connected graph, every V_n is nonempty. On \(\{\tau_n<\infty\}\), the reached vertex v has never been visited before, because any earlier visit would already have hit V_n. Its selected neighbor v' at distance n+1 has also not been visited: reaching any such vertex earlier would first cross V_n. Choose v' by a fixed deterministic rule.

Exactly one edge at v, the arrival edge, has been traversed once; the other edges at v have not been traversed. Every edge at v' is untraversed. For the target edge \(f=\{v,v'\}\), at v the total competing reinforcement is at most \(B_1+(D-2)B_0\), and at v' it is at most \((D-1)B_0\). Both are at most A. On the path which always uses f from now onward, these competing weights remain unchanged. At the jth proposed traversal of f its weight is \(w(\ell_f+j)\), including j=0.

Conditioned on the history through \(\tau_n\), the probability of immediately using f forever is consequently at least

\[
\prod_{j=0}^{\infty}\frac{w(\ell_f+j)}{w(\ell_f+j)+A}
\ge\exp\left(-A\sum_{j=0}^{\infty}\frac1{w(\ell_f+j)}\right)
\ge p>0.\tag{D}
\]

For finite products this is the chain rule; passage to the infinite event follows from continuity of probability for decreasing events. The inequality uses \(\log(1+x)\le x\). The arrival edge's once-incremented weight is explicitly included, and the j=0 factor is retained. No monotonicity of w is used.

Let \(\mathcal R=\sup_{k\ge0}d(I_k,I_0)\). If \(\mathcal R>n+1\), then \(\tau_n<\infty\) and the immediate trapping event in (D) failed. Moreover \(\tau_n<\infty\) implies \(\mathcal R>n-1\). Taking conditional expectations at \(\tau_n\), justified by partitioning over finite values of that stopping time, gives

\[
\mathbb P(\mathcal R>n+1)\le(1-p)\mathbb P(\tau_n<\infty)
\le(1-p)\mathbb P(\mathcal R>n-1).
\]

For r≥2 take n=r−1≥1 in this recurrence. The initial bounds at r=0 and r=1 are both one. Iterating separately over even and odd r therefore gives \(\mathbb P(\mathcal R>r)\le(1-p)^{\lfloor r/2\rfloor}\) for every integer r≥0. No arrival-edge assertion is made at the starting vertex (n=0). Hence the range is almost surely contained in a finite ball. Bounded degree ensures each ball is finite.

## 4 From confinement to eventual single-edge motion

One must not identify the law conditioned on never leaving a ball with the unrestricted reinforced walk on the induced finite graph. Here is a direct comparison that avoids that mistake.

Fix a finite induced ball H of radius at least one. For any finite path staying in H, the probability of that path under the G-walk is at most its probability under the H-walk with the same initialization: the target edge and its count coincide, while the transition denominator in G includes every incident edge in H and possibly more edges. Therefore, writing \(\Theta_{H,n}\) for confinement through time n,

\[
\mathbb E_G[g(R_2(N_H(n)));\Theta_{H,n}]\le
\mathbb E_H[g(R_2(N_H(n)))]\le C_H.
\]

Use the g and finite constant from Section 2 for H. On the event \(\Theta_{H,\infty}\) of permanent confinement, replace \(\Theta_{H,n}\) on the left by this smaller event, and then use monotone convergence. It follows that \(R_2(N_H(\infty))<\infty\) almost surely on permanent confinement. The finite-graph conclusion now yields eventual fixation there. A one-edge H is immediate. Take the countable union over balls and use Section 3. This establishes fixation almost surely for the stated finite-offset scope.

For common finite integer initialization, ordinary reciprocal summability verifies all these hypotheses. More generally, if offsets are nonnegative integers and conditions (6),(8) hold together with \(\sum_{k\ge1}1/w(k)<\infty\), then \(w(k)\to\infty\); (8) bounds the offsets to a finite set. This deduction also verifies that integer-state scope. Arbitrary real offsets need not have this finite-set consequence.

## 5 Exact discrepancy in the inspected manuscript

On manuscript p.14, the proof of Lemma 2.7 correctly states that the arrival edge at the newly reached v has count \(\ell_e+1\). On p.15, formula (36) instead bounds competing weights by the initial values \(w(\ell_e)\), omitting the arrival edge's increment. Its last product-to-exponential step also changes the product's starting index from 0 to a sum beginning at 1.

The first claimed lower bound is not valid in general, even with common integer initialization. To verify this concretely, take G=\(\mathbb Z\), initial offset zero, and \(w(j)=10^j\). Condition on the first step from 0 to 1. The new forward edge is \(\{1,2\}\). The probability of immediately using that forward edge forever is at most the probability of its first traversal, namely \(1/(10+1)=1/11\). But the first product asserted as a lower bound in (36) becomes

\[
\prod_{j=0}^{\infty}\left(\frac{10^j}{10^j+1}\right)^2
\ge\frac14\exp\left(-2\sum_{j=1}^{\infty}10^{-j}\right)
=\frac14e^{-2/9}>\frac1{11}.
\]

The strict inequality follows, for example, from \(e^{-2/9}\ge1-2/9=7/9\), giving the rational lower bound \(7/36>1/11\). This is an exact counterexample to that displayed estimate, **not a counterexample to attracting-edge fixation**. The omitted zero-index factor gives another reason not to accept its final exponential as written.

Sections 3–4 provide the needed repair for finitely many initial offsets. They do not purport to repair Theorem 1.1 for every real edge-dependent initial state under (6),(8) alone. No journal version containing this proof was retrieved, so this report makes no claim that its formula has the same issue. The existence of this manuscript-level estimate error must be retained whenever describing the depth of the audit.

## 6 Audit acceptance

The complete argument above verifies the exact original attracting-edge target for common finite integer initial count, including nonmonotone reinforcement and the triangle. Every stochastic estimate needed for that scoped conclusion is given explicitly. Attribution remains to the established Cotar–Thacker result and its credited Cotar–Limic bound. The finite theorem itself is independently checked for all its finite initial-offset hypotheses. The manuscript's full arbitrary-real-initial-state proof is not certified, and a corrected common-initial proof must not be described as a line-by-line endorsement of all of Section 2 or of the uninspected journal article.
