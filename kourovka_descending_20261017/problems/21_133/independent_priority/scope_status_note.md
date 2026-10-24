# Independent priority and scope check: Kourovka 21.133

Checkpoint UTC: 2026-10-24T18:13:55.741094+00:00
Bounded source/scope task completion: **100%**. Original research performed: **none**.

## Conclusion

**Exact prior-scope collision; do not select 21.133 for a new original solution.**
Brescia–Di Siena–Ingrosso–Trombetti, arXiv:2610.05415v1, publicly submitted
2026-10-04, states the negative answer for the class SJ. The authors' 2016
ADV–2B identifies SJ with the exact property asked in 21.133: having an abelian
subnormal series of unrestricted order type. The present AGTA problem collection
also explicitly credits those four authors and gives a negative answer, linking
this arXiv paper. The latest Kourovka PDF still lacks a solution annotation.

This is a priority/scope conclusion, **not an independent certification of the
22-page proof** or of journal acceptance/prize award.

## Exact definitions and comparison

The new paper's Definition 2.5 (printed p.4) uses a complete chain from 1 to G,
closed under subchain unions/intersections. Every nonidentity element must be
covered by a jump A<B; at each jump A is normal in B and B/A is abelian.
SJ further requires every term H to have finite subnormal defect in G.
Definition 2.3 (p.3) makes this a finite chain H=H_d normal in ... normal in
H_0=G. The integer d can depend on H: there is **no global uniform bound**.
Adjacent normality alone is only the general abelian-series requirement; it does
not supply this additional condition.

SI is the normal-series condition: terms normal in the whole group. Hartley's
1976 primary paper, printed p.1308, explicitly defines SI this way. Hence SI
implies SJ by defect at most one, rather than SJ being a stronger condition than
SI. Treating the finite-defect clause as a mismatch with the problem is unsupported:
ADV–2B (2016), printed p.128, expressly calls the unrestricted abelian subnormal
series property SJ. Its coauthors include the proposer of 21.133.

## The new theorem and explicit reference limits

The Main Theorem (p.2) asserts a G outside SJ whose every countable subgroup
belongs to SJ. Proposition 5.1 (p.16) supplies the global failure, and Proposition
5.5 (p.20) the countable-subgroup conclusion. The full text was read for scope,
including its definitions and final construction. The paper invokes ADV–2B and
the 2021 survey, but a text search finds no occurrence of Kourovka or 21.133.
Thus the link to 21.133 is an established terminology match, not an explicit
Kourovka-number claim made in the paper.

## Current primary status and cache discrepancy

- Official October 20, 2026 main PDF: printed p.199 = physical PDF page 199,
  21.133 remains unmarked; the updates-only PDF contains no 21.133 entry.
- Direct HTTPS AGTA OpenProblems.pdf retrieval at
  2026-10-24T18:12:30.893973+00:00: p.2 explicitly records the four authors as
  solvers and a negative answer, linking arXiv:2610.05415. The local rendered
  page visually confirms this. SHA-256:
  `d18ce9a125ec79382792e97793ff80e46084b2d7ffd1e52d7bc58374d37eac81`.
- The web-search browser extraction of the same AGTA URL returned an older
  text without that annotation. Preserve this discrepancy: use the timestamped
  direct bytes and local image as the checkable current observation.
- The arXiv abstract page lists only v1, submitted October 4; no journal reference
  or acceptance evidence was observed. AGTA's prize rules alone do not prove a
  prize was awarded or that the paper was accepted.

## Primary sources

1. https://arxiv.org/abs/2610.05415 and https://arxiv.org/pdf/2610.05415v1
2. https://www.advgrouptheory.com/journal/Volumes/2/ADV%20Perspectives%20in%20Group%20Theory%20-%20an%20open%20space.pdf (pp.127–128)
3. https://www.advgrouptheory.com/OpenProblems.pdf (p.2)
4. https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf (p.199)
5. https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-3.pdf
6. Hartley, *A conjecture of Bachmuth and Mochizuki on automorphisms of soluble
   groups*, Canadian J. Math. 28 (1976), 1302–1310, p.1308.
   https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8911BEC91D6393D2ADE1A00F9FECBE9E/S0008414X00020988a.pdf/conjecture_of_bachmuth_and_mochizuki_on_automorphisms_of_soluble_groups.pdf

All raw copies and extracted source text are in sources/. Timestamp, URL, byte
count, and SHA-256 receipts are in scope_status_receipts.json. Publisher access
to the 2021 survey failed (403/429); no finding depends on its cached excerpts.
No external individual was contacted. No Git, publication, release, or queue
mutation was made by this scope check.
