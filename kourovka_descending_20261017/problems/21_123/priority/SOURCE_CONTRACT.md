# 21.123: source contract before research

UTC cutoff: 2026-10-24 23:02. Preparation completion estimate: **100%**; discovery toward a new complete solution: **0%**. No original mathematical investigation has been attempted. This is source preparation for the root agent's selection audit, not a problem-status decision.

## Authoritative question

The current official source is *The Kourovka Notebook*, No. 21, editors E. I. Khukhro and V. D. Mazurov, Novosibirsk, 2026, printed page **198**, problem **21.123**, proposed by **A. Smoktunowicz**. The official homepage's current post links the October update-3 PDF and was last updated October 20, 2026. Both official PDFs were fetched afresh for this audit.

In normalized wording, the question asks whether Smoktunowicz's extension of the Agrachev–Gamkrelidze group-of-flows construction always produces a group from a pre-Lie ring in its stated domain. The Notebook identifies the extension by **Definition 66** and cites:

- A. A. Agrachev and R. V. Gamkrelidze, *Chronological algebras and nonstationary vector fields*, J. Soviet Math. **17** (1981), 1650–1675, [DOI](https://doi.org/10.1007/BF01084595).
- A. Smoktunowicz, *An extension of the group of flows method for finite pre-Lie rings*, J. Pure Appl. Algebra **229**, no. 12 (2025), 108128, [DOI](https://doi.org/10.1016/j.jpaa.2025.108128).

There are no separately lettered subquestions. The following brace/Yang–Baxter discussion records a consequence of an affirmative answer; it is not a second open assertion.

The original exact wording is preserved in the freshly downloaded official PDF and its text derivative, at `sources/notebook21_fresh.txt`, lines 9499–9506. Do not replace the underlying construction by a more convenient operation without stating and justifying that change.

## Domain hidden by the short Notebook statement

The reference is to a finite pre-Lie ring \((A,+,\cdot)\), with \(|A|=p^n\), \(p>3\) prime, \(n\) a natural number as in the source, and **Property 3**. Addition is abelian, multiplication biadditive, and

\[
(a\cdot b)\cdot c-a\cdot(b\cdot c)
=(b\cdot a)\cdot c-b\cdot(a\cdot c).
\]

Write \(m=\lfloor(p-1)/4\rfloor\) and \(A[p^i]=\{x:p^i x=0\}\). Property 3 requires, for every \(a_1,\ldots,a_m\) and \(i\geq1\),

\[
a_1\cdot(a_2\cdot\ldots\cdot a_m)\in pA,
\qquad
L_{a_1}\cdots L_{a_m}(A[p^i])\subseteq p(A[p^i]),
\quad L_a(b)=a\cdot b.
\]

All products are right nested. The second right-hand side is the image of the torsion subgroup under multiplication by \(p\); it is not shorthand for the intersection \(pA\cap A[p^i]\).

A function \(d:pA\to A\), with \(p d(x)=x\), replaces division by \(p\). Additivity and normalization \(d(0)=0\) are not hypotheses. For \(j\geq1\), define \(s_j=v_p(j!)\), \(\eta_j=m s_j\), and \(j!=\gamma_jp^{s_j}\), with \(\sigma_j\gamma_j\equiv1\pmod{p^n}\). The source then uses divided iterates of \(L_a\), an adjoined unit, maps \(W(a)\), \(W(a,b)\), and the claimed inverse \(\Omega=W^{-1}\), to prescribe

\[
a\circ' b=a+b+W(\Omega(a),b).
\]

Associativity and total, well-defined evaluation on the full specified domain must be part of any claimed group construction. A different transported group law is insufficient without an equivalence argument.

## Version contract: do not silently correct formulas

The arXiv source is the combined manuscript [2410.20440v2](https://arxiv.org/html/2410.20440v2), last revised March 29, 2025; its second part has the numbering quoted by the Notebook. The actual journal article has a separately numbered [accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/586346195/AS_submitted_manuscript.pdf). The institution labels it an accepted author manuscript, not the publisher's final PDF. The latter was not retrieved.

| Object | Combined arXiv v2 | Accepted manuscript |
|---|---:|---:|
| Property 3 | Definition 59 | Definition 18 |
| Divided operators on \(A\) | Definition 60 | Definition 19 |
| Pullback movement claim | Remark 63 | Remark 22 |
| \(W\) | Definition 64 | Definition 23 |
| Claimed bijectivity of \(W\) | Theorem 65 | Theorem 25 |
| Proposed law | Definition 66 | Definition 26 |
| Pseudobrace assertion | Theorem 67 | Theorem 27 |

Formula differences were checked against the raw arXiv HTML and PDF and the accepted PDF, including visual inspection of accepted printed pages 12–13. See `VERSION_COMPARISON.md`. There is no retrieved official erratum assigning an intended correction. Resolving the exact mathematical reading is a prerequisite to comparing a proposed solution with prior work.

## Official marks are not an openness certificate

The current entry has neither a solution star nor an AI-claim sharp. The separate update file has **zero occurrences of 21.123**. This establishes only the absence of a listed solution notice in those fetched files. A subsequent preprint explicitly claiming a resolution was found, so unstarred status does not establish genuine openness.

The linked update PDF calls itself a **November 2026 update**, despite its October URL and the current October 24 retrieval date. This source-date inconsistency is recorded rather than resolved by inventing a chronology. Its bytes match the official linked file; no 21.123 notice occurs in it.

Recommendation is deferred to `PRIORITY.md`: a prior claimed solution and the version issue require audit before treating 21.123 as a fresh open research target. No top-level problem STATUS file has been created.
