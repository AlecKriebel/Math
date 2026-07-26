# Priority and literature audit

**Audit date:** 25 July 2026

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

Gary MacGillivray, C. M. Mynhardt, and Virgélot Virgile, “Eternal domination
and clique covering,” *Electronic Journal of Graph Theory and Applications*
10(2) (2022), 603-624, DOI
[`10.5614/ejgta.2022.10.2.19`](https://doi.org/10.5614/ejgta.2022.10.2.19):

- Proposition 5.1 proves that the two listed ten-vertex graphs have
  \(\gamma^\infty=3<4=\operatorname{cc}\).
- Proposition 5.2 reports a computer verification that every graph of order
  at most nine satisfies \(\gamma^\infty=\operatorname{cc}\).
- Table 9 lists `IEhbtj{ro` and `IEhbtn{ro`.
- The text identifies the second graph as the first plus edge \(67\), which
  identifies `IEhbtj{ro` as the 26-edge member used here.

The paper uses \(\theta\) for clique-cover number and does not state a
Lovász-theta calculation for this graph.

For the theta convention and sandwich inequality, the audit used Noga Alon
and Nabil Kahale, “Approximating the independence number via the
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
- arXiv, journal pages, general scholarly indexes, dissertations, and public
  problem lists.

The arXiv record for the 2022 paper was also checked: its latest revision is
21 February 2022.

## Conclusion

No indexed paper, preprint, thesis, or public webpage found in this search
states the exact counterexample or resolves the Lovász-theta question.
Accordingly, the defensible language is:

> As of 25 July 2026, no prior public resolution was found in the sources
> searched. The observation appears novel, but this is not an absolute
> priority claim.

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
