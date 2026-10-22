# Finite arbitrary sign factors can overcome partition-scale radial growth

Güntürk's [Theorem 1](https://arxiv.org/abs/math/0503373), specialized to \(\mu=0,M=1,f\equiv0\), supplies constants \(C_1,C_2>0\) and
\[
Q(z)=\sum_{n\ge0}q_nz^n,\quad q_n\in\{-1,1\},\qquad
|Q(r)|\le C_1e^{-C_2/(1-r)}\quad(0\le r<1).
\]
Negation if necessary normalizes \(q_0=1\). The result was published in [IMRN 2005(26), 1601–1610](https://doi.org/10.1155/IMRN.2005.1601). We inspected its theorem and construction; the cited proof is not independently certified here.

**Derived finite-product observation.** Use \(Q(q^m)\) as the active factor for \(1\le m\le K\), leaving every other factor positive. With \(C=\pi^2/6\) and \(H_K=\sum_{m=1}^K1/m\),
\[
P_K(q)=E(q)\prod_{m=1}^K(1-q^m)Q(q^m).
\]
The proved bound \(E(e^{-t})\le e^{C/t}\), together with \(1-e^{-mt}\le\min(1,mt)\), yields
\[
|P_K(e^{-t})|
\le C_1^K\exp\left(\frac{C-C_2H_K}{t}\right). \tag{1}
\]
Since \(H_K\to\infty\), choose a fixed finite \(K\) with \(C_2H_K>C\). Then (1) gives exponential radial decay despite the positive partition tail.

Thus partition-scale radial suppression is genuinely possible with finitely many arbitrary active factors. This does not establish bounded Taylor coefficients. The remaining difficulty must control coefficients or additional analytic information, rather than radial suppression alone. Both scoped continuation theorems remain unaffected. No author code was executed; no novelty claim is made.
