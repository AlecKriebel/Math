# EP-642: bounded investigation report

Date: 2026-10-06. Identifiers: UnsolvedMath 2228; Erdős 642.

## Result

Partial, stalled after three approaches. No solution, counterexample to the conjecture, asymptotic improvement, or novelty claim is made. The accompanying proof note establishes an exact classification at maximum degree four and records the missing global step in the constant-core route.

## Formulation verification

The inherited statement was matched to the exact problem identifier and to the publicly indexed revision history of Erdős 642. The relevant edges are existing graph chords joining nonconsecutive cycle vertices. The forbidden condition is at least as many chords as cycle vertices, including equality; the admissible condition is strictly fewer. Graph order and cycle length must not be conflated.

The direct UnsolvedMath problem URL and direct Erdős tracker page returned HTTP 403 during this run. The tracker's indexed history and forum entry supplied the matching mathematical formulation and its open label. This is a bounded verification limitation, not a claim that the direct pages were read successfully.

## Primary literature inspected

1. Draganić, Methuku, Munhá Correia, Sudakov, Cycles with many chords. Theorem 1.1 in arXiv:2306.09157v2, PDF page 2, was read as text and visually inspected. For sufficiently large n, at least n(log n)^8 edges force a cycle with at least its length in chords. This supplies O(n(log n)^8), not O(n). The published-paper PDF was also retrieved, but is distinguished from the visually inspected arXiv version.

2. Draganić and Girão, Cycles with almost linearly many chords, arXiv:2601.08769v1. Theorem 1.1 on PDF page 2 was read and visually inspected. Its constant-minimum-degree hypothesis yields a cycle with a positive constant multiple of l/(log l)^c chords, for some cycle length l and absolute c>0. This preprint does not state the chord-density-one conclusion. Its introduction describes the linear-fraction question as open. This report checks that statement and its quantifiers; it does not independently certify the paper's proof.

3. Letzter, Methuku, Sudakov, Nearly Hamilton cycles in sublinear expanders, and applications, arXiv:2503.07147 and published in 2026. Corollary 7.2 on PDF page 30 was read and visually inspected. The sufficient edge count is n(log n)^130 for sufficiently large n. This alternative method does not improve the exponent eight result.

The source cited by the tracker as Erdős, Some recent problems and results in graph theory, Discrete Mathematics 164 (1997), 81-85, p.84, was identified bibliographically. Its exact historical page was not obtained: the publisher/DOI route failed, and a candidate institutional archive URL returned 404. Likewise, the 1996 Chen-Erdős-Staton paper was identified on the publisher's indexed record but its full text was not inspected. No claim about exact historical wording rests on having read either unavailable PDF.

## Bounded current-status search

The search covered the exact problem number, named chord papers, the authors' primary paper pages, and 2026 chord-cycle results. It also surfaced a September 2026 paper on Erdős 767 and a July 2026 paper on other cycle/chord questions; their abstracts describe different targets. No primary source settling EP-642 was verified. This is a search result, not proof that no later, unpublished, or unindexed resolution exists.

## Bounded repository history check

Read-only searches in AlecKriebel/Math covered commit messages and PRs for 2228 and EP-642, default-branch code for 2228, and branch names for 2228. All six returned empty results. These checks do not establish exhaustive historical absence and provide no evidence of mathematical novelty. No repository file or queue row was changed in this run.

## Mathematical work

- The chord identity converts the target into finding a cycle vertex set inducing average degree at least four.
- The global linear bound is equivalent to an absolute minimum-degree threshold, or bounded degeneracy of the admissible class.
- In graphs of maximum degree at most four, the forbidden cycle exists exactly when a component is four-regular and Hamiltonian.
- An explicit eleven-vertex four-regular graph with a cut vertex defeats threshold four and the corresponding longest-cycle shortcut.
- K_{3,n-3} is an admissible linear-density family, proving f(n)>=3n-9 for n>=6.
- The exact missing step is a cycle whose degree surplus over four covers all its outgoing boundary edges. Neither the core reduction nor the almost-linear chord theorem supplies it.

All mathematical claims above have self-contained proofs in proof_note.md. A finite sanity check covers all 1,100 labeled graphs of orders zero through five, the eleven-vertex obstruction, and six members of the bipartite family. No finite computation is presented as settling the infinite problem.

## Audit request

Review the proofs independently, including the equality case in the maximum-degree-four classification, arbitrary-subgraph heredity, and the average-degree/minimum-degree constants. Rerun validation.py. Confirm that the status remains partial and that the literature claims are stated with their source-access limits. The archive contains authored material and public verification metadata only; source documents are not included.

## Public source links

- Problem and history: https://unsolvedmath.com/problems/2228 ; https://www.erdosproblems.com/history/642 ; https://www.erdosproblems.com/forum/thread/642?embed=1
- Erdős historical source DOI: https://doi.org/10.1016/S0012-365X(96)00044-1
- Chen, Erdős, Staton, Proof of a conjecture of Bollobás on nested cycles: https://doi.org/10.1006/jctb.1996.0005
- Cycles with many chords: https://arxiv.org/abs/2306.09157 ; https://doi.org/10.1002/rsa.21207
- Cycles with almost linearly many chords: https://arxiv.org/abs/2601.08769
- Nearly Hamilton cycles in sublinear expanders, and applications: https://arxiv.org/abs/2503.07147 ; https://doi.org/10.1112/jlms.70452
- Distinct 2026 problems: https://arxiv.org/abs/2609.15330 ; https://arxiv.org/abs/2607.15501
