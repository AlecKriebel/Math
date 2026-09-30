# 30005451: corrected affine comparison, research checkpoint

2026-09-30 09:57 UTC. One substantive coupling approach is in progress. Completion estimate: 55%; no reviewed solution claim.

The exact OWR question on printed pp. 649–650 asks for the relation between Bernoulli preferential attachment and an appropriately adapted random-outdegree model. Its proposed matching model uses **i.i.d. Poisson outdegrees**, not the deterministic outdegree asserted in the dataset's clean statement. Attachment must use indegree alone. The latest arXiv:2212.05551v4 (2 March 2026), Section 1.5, still identifies the Bernoulli model as an extension; its total-degree theorem cannot simply be substituted.

For the source-valid affine rule $f(k)=ak+b$, $0\le a<1$, $0<b\le1$, the matching mean is $\lambda=b/(1-a)$. Compare the original Bernoulli model from a single isolated vertex with a no-self-loop model having i.i.d. Poisson($\lambda$) outgoing edges and indegree weights $f$. Both frozen-within-step weights and sequential updating are under consideration.

A complete proof is being written around the following quantitative steps:

1. Independent Poisson row counts have exactly the desired i.i.d. Poisson total and normalized preferential targets.
2. A Bernoulli($p$)/Poisson($q$) coupling has expected count discrepancy at most $p^2+|p-q|$.
3. If $D_n$ counts edge-multiplicity discrepancies, then the weight comparison contributes $aD_n/n$. The Poisson graph's total number of edges gives a separate normalization error of order $n^{-1/2}$ in expectation. The Bernoulli squared-weight moment makes its Poissonization error vanish.
4. The recursion $\mathbb E D_{n+1}\le(1+a/n)\mathbb E D_n+o(1)$ gives $\mathbb E D_n=o(n)$ because $a<1$.
5. A uniform averaged degree moment of order $p>1$ upgrades sublinear edge discrepancy to matching radius-$r$ neighborhoods for all but $o(n)$ vertices, for each fixed $r$.
6. Sequential within-step reinforcement adds only $O(1/n)$ expected row discrepancy, because the Poisson outdegree has a finite second moment.

The next artifact must make every model, moment bound, coupling and local-probability statement explicit. General nonlinear concave rules are not covered by this affine normalization argument, and no fixed-outdegree equality is claimed.
