# Source and scope gate

Checked 2026-10-03 UTC. Catalogue ID 30004773; source code OWR-8415341-012.

## Exact primary question

The required catalogue request to https://www.unsolvedmath.com/problems/30004773 returned HTTP 403 (the preceding HTTP 200 in the connection headers was the proxy connection, not the page response). The cached catalogue record was used only to identify the report and problem, not as mathematical or current-status evidence.

The authoritative source is [Computational Group Theory, Oberwolfach Report 38/2021](https://ems.press/journals/owr/articles/8415341), DOI 10.4171/OWR/2021/38, printed pp. 2081–2082, Tobias Rossmann's item in the problem session. The [publisher PDF](https://ems.press/content/serial-article-files/46914?nt=1) was retrieved and the complete item read, including its group presentation and its equivalence to alternating-matrix rank counting. The report's workshop took place in August 2021; the publisher gives publication as 26 November 2022. These dates are distinct.

The target fixes a finite simple graph and odd prime p, forms its class-at-most-two group with exponent dividing p by killing commutators at nonedges, and asks how counts of irreducible characters of each degree p^i, i>=1, depend on p. It is a descriptive question, not a stated universal polynomiality conjecture. The source expressly contrasts it with known polynomial counts of conjugacy classes by size.

## Relevant primary results and proof coverage

1. Tobias Rossmann, [Enumerating conjugacy classes of graphical groups over finite fields](https://doi.org/10.1112/blms.12665), Bulletin of the London Mathematical Society 54 (2022), 1923–1943. The [author manuscript](https://torossmann.github.io/files/csp.pdf) was read at §§1.1, 1.6, 2.4, 3 and 4, including the complete relevant proofs of Lemma 3.2 and Theorem A and the intervening class-size reduction. Question 1.10 is the prime-power character-degree question. Its character/rank reduction is recovered self-containedly in Attempt 1; the class-count result used here is derived directly in Attempt 4. Thus no dependence on the unread proof of O'Brien–Voll's general theorem remains.
2. The author's [publication list](https://torossmann.github.io/publications/) and complete [August 2025 HIM slides](https://torossmann.github.io/talks/him25.pdf) were inspected for updates. The complete two-page [2025 report, Orbits: tame and wild](https://torossmann.github.io/files/mfo25a.pdf), was also read. These newer sources describe conjugacy classes, class-counting zeta functions, joins, and averages of kernels. They were not treated as resolutions of character-degree rank counts. The introduction, definitions, and theorem scope of [Ask zeta functions of joins of graphs](https://torossmann.github.io/files/plumbing.pdf), arXiv:2505.10263, were checked for this distinction; no theorem or unread proof from that 60-page paper is invoked in the partial results.
3. Joel Brewster Lewis and Alejandro H. Morales, [Rook theory of the finite general linear group](https://arxiv.org/abs/1707.08192), Experimental Mathematics 29 (2020), 328–346. Example 6.4 and the normalization definitions were inspected. Its stated Fano example distinguishes even and odd q. This was used only to reject a candidate counterexample on the odd-prime domain. The manuscript also mentions more complicated counts via [KLM17], but that reference is explicitly listed as work in progress, without a theorem or proof to inspect; targeted searches did not recover a corresponding proof. The Fano enumeration itself, or any nonpolynomiality assertion on odd primes, is not imported as a result here. The bipartite rank-doubling formula is proved directly.
4. The rank-two parametrization, forest elimination, matching rank bound, moment recovery, polynomial-divisibility lemma, and Schur-complement identity are all proved in the five turn files. Elementary finite-group character orthogonality/regular-representation facts are the only standard representation-theoretic inputs; no specialized external theorem supplies the missing general step.

Literature searches included exact title/source-code terms and graph-supported alternating ranks, graphical-group characters, and finite-field rook counts. No retrieved source supplied a full resolution of the exact question. This is a bounded literature check and does not certify the absence of a solution or establish priority for the partial formulas.

## Actual prior-work checks

The current main-branch [queue](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md) showed rank 541 as queued, 0/5. The fetched queue blob was c87c275c638939b8008fd58db80657491d14971e. That label alone was not treated as proof of an unattempted problem.

Separate GitHub searches of AlecKriebel/Math across open and closed PRs used the ID, source code, graph/character terms, and the phrases Character Degrees, Graph-Defined, and graphical groups. No matching attempt PR was returned. Code, branch, and commit searches for 30004773 returned no matches. The repository root listing was inspected and contained no evident target folder. Two recursive-tree requests failed at transport and are not counted as successful checks. These are bounded negative observations: unindexed files or differently titled history may be missed.

## Source byte identities

Downloaded source copies are for local reading only and are not distributed. SHA-256 identities:

- OWR report PDF: ae3d49cc68f0425d5a334b5ab94bc72cf89f2e28202259a73cacb7c77090277c
- Rossmann 2022 author PDF: 9a9d099df27f514311e103b3e4932fd98c40c8ecdb38457261ef3e4a5dfe9099
- August 2025 HIM slides PDF: 34a439e401839e72ad865416b2924bc610ad527705005621d69e5adb4dafecb0
- 2025 Orbits: tame and wild report PDF: 8323d2d3d9eab3a5f06567d27028b5379c4891dc807ef17809fcdb31d6c3ac1f
- Lewis–Morales author PDF: fa0767dfa4e1337848616ec0acc7883b13e276a64de54d74f991ab6b1e6502e0

## Gate decision

PASS for the precisely scoped partial-results investigation. FAIL for a full-source resolution claim, a historical novelty claim, or an inference from symmetric-matrix wildness/even-characteristic variation to odd-prime alternating rank counts. Proposed disposition: unsolved, five substantive attempts. Independent review is still required before any public repository write.
