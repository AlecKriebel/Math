# Priority and literature audit

**Audit date:** 26 July 2026

## Question and notation

Douglas West's eternal-domination problem page asks whether
\(\gamma^\infty\) is bounded below by the Lovász theta function. The same
question remains in the open-questions section of Wikipedia's
“Eternal dominating set” article. West's page separately uses \(\theta(G)\)
for clique-cover number, so the intended Lovász-theta question is
unambiguous.

This note avoids the collision:

- \(\vartheta(G)\) means the Lovász theta function;
- \(\operatorname{cc}(G)=\chi(\overline G)\) means clique-cover number.

## Known graph-theoretic input

Noga Alon, “Explicit Ramsey graphs and orthonormal labelings,” *Electronic
Journal of Combinatorics* 1 (1994), Research Paper 12, DOI
[`10.37236/1192`](https://doi.org/10.37236/1192):

- Corollary 2.3 gives explicit triangle-free Cayley graphs \(F_k\) on
  \(n_k=2^{3k}\) vertices, for \(k\geq2\) not divisible by three, with
  \(\vartheta(\overline{F_k})=\Theta(n_k^{1/3})\).
- Setting \(H_k=\overline{F_k}\) gives \(\alpha(H_k)=2\).

Wayne Goddard, Sandra M. Hedetniemi, and Stephen T. Hedetniemi, “Eternal
security in graphs,” *Journal of Combinatorial Mathematics and Combinatorial
Computing* 52 (2005), 169-180:

- Theorem 4 proves that \(\alpha(G)=2\) implies
  \(\gamma^\infty(G)\leq3\).
- Together with \(\alpha\leq\gamma^\infty\), this turns Alon's family into an
  explicit unbounded separation:
  \[
  \frac{\vartheta(H_k)}{\gamma^\infty(H_k)}
  =\Theta(n_k^{1/3}).
  \]

This is a direct synthesis of established theorems, not a new graph
construction.

Gary MacGillivray, C. M. Mynhardt, and Virgélot Virgile, “Eternal domination
and clique covering,” *Electronic Journal of Graph Theory and Applications*
10(2) (2022), 603-624, DOI
[`10.5614/ejgta.2022.10.2.19`](https://doi.org/10.5614/ejgta.2022.10.2.19):

- Fact 5.1 gives independence number three and clique-cover number four for
  the two listed graphs.
- Proposition 5.1 and its proof establish
  \(\gamma^\infty=3<4=\operatorname{cc}\).
- Proposition 5.2 reports a computer verification that every graph of order
  at most nine satisfies \(\gamma^\infty=\operatorname{cc}\).
- Table 9 lists `IEhbtj{ro` and `IEhbtn{ro`.
- The text identifies the second graph as the first plus edge \(67\), which
  identifies `IEhbtj{ro` as the 26-edge member used here.

The paper uses \(\theta\) for clique-cover number and does not state a
Lovász-theta calculation for this graph.

For the origin of the theta function and its semidefinite formulation, the
audit used László Lovász, “On the Shannon capacity of a graph,” *IEEE
Transactions on Information Theory* 25 (1979), 1-7, DOI
[`10.1109/TIT.1979.1055985`](https://doi.org/10.1109/TIT.1979.1055985).
For the modern convention and sandwich inequality, the audit also used Noga
Alon and Nabil Kahale, “Approximating the independence number via the
\(\theta\)-function,” *Mathematical Programming* 80 (1998), 253-264, DOI
[`10.1007/BF01581168`](https://doi.org/10.1007/BF01581168). It gives the
same primal semidefinite program used in the certificate and states
\[
\alpha(G)\leq\vartheta(G)\leq\chi(\overline G).
\]

## Search scope

The audit searched combinations and notation variants including:

- `eternal domination` with `Lovász number`, `Lovasz theta`, `vartheta`,
  `theta function`, `gamma infinity`, and `eternal security`;
- the 2022 paper's forward citation graph and related recent papers;
- sources citing Alon's 1994 construction and the 2005 eternal-security
  result, including searches for the two results in combination;
- arXiv, journal pages, general scholarly indexes, dissertations, and public
  problem lists.

The arXiv record for the 2022 paper was also checked: its latest revision is
21 February 2022.

## Conclusion

No indexed paper, preprint, thesis, or public webpage found in this search
explicitly combines the Alon and Goddard--Hedetniemi--Hedetniemi results to
answer the Lovász-theta question. No source found states the exact
ten-vertex certificate. Accordingly, the defensible language is:

> As of 26 July 2026, no prior public resolution was found in the sources
> searched. The connections and exact certificate appear unrecorded, but this
> is not an absolute priority claim.

A literature search cannot exclude unindexed code, private observations, or
an antecedent phrased in different language. No outside researcher was
contacted; independent expert review is deliberately left to the human
author.

## Public records checked

- Douglas West, “Eternal Domination Number”:
  <https://dwest.web.illinois.edu/regs/eterndom.html>
- Wikipedia, “Eternal dominating set,” open questions:
  <https://en.wikipedia.org/wiki/Eternal_dominating_set#Open_questions>
- MacGillivray-Mynhardt-Virgile journal article:
  <https://www.ejgta.org/index.php/ejgta/article/view/1525>
- arXiv record:
  <https://arxiv.org/abs/2110.09732>
- Alon, “Explicit Ramsey graphs and orthonormal labelings”:
  <https://doi.org/10.37236/1192>
- Goddard-Hedetniemi-Hedetniemi, “Eternal security in graphs”:
  <https://combinatorialpress.com/jcmcc-articles/volume-052/eternal-security-in-graphs/>
- Lovász, “On the Shannon capacity of a graph”:
  <https://doi.org/10.1109/TIT.1979.1055985>
