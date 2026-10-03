# Source and scope gate

Checked on 3 October 2026.

## Identification and exact statement

- Catalogue: [2305039 / AMR-022-5039](https://www.unsolvedmath.com/problems/2305039), Research Problems in Function Theory, Problem 5.39.
- The direct catalogue request returned HTTP 403. A previously retrieved catalogue record was used only to identify the primary source; its generated research summary was not accepted as mathematical evidence.
- Primary source: W. K. Hayman and E. F. Lingham, [Research Problems in Function Theory (New Edition), arXiv:1809.07200](https://arxiv.org/abs/1809.07200), 2018. The statement is on printed p. 99, its continuation and Update 5.39 on p. 100; these are PDF pages 100–101. The definition of subordination begins on printed p. 98 and continues onto p. 99. Text and rendered pages were checked.
- The source definition requires g=f∘φ, φ(0)=0 and φ(D)⊂D. It does not require f to be univalent. The unknown is the optimal universal derivative-mean radius for each p>0.
- Update 5.39 says that no progress had been reported to the authors. This verifies the wording of the 2018 update only. It does not establish current open status by itself.

## Relevant published proof coverage

1. G. M. Goluzin, [On majorants of subordinate analytic functions. I](https://www.mathnet.ru/eng/sm5696), Mat. Sb. (N.S.) 29(71):1 (1951), 209–224. The bibliographic record was verified. The original full-text link returned a provider agreement page rather than PDF content, so the original proof was not inspected and is not represented as inspected.
2. Edgar Reich, [An inequality for subordinate analytic functions](https://msp.org/pjm/1954/4-2/pjm-v4-n2-p08-s.pdf), Pacific J. Math. 4(2) (1954), 259–274. The complete proofs of Lemma 5 (partial sums of squared coefficients, pp. 263–264) and Lemma 6 (weighted comparison, pp. 264–265) were inspected. These supply the coefficient ingredients needed for the classical p=2 derivative estimate. The present note also proves those ingredients directly.
3. R. S. Khasyanov, [Area functional and majorant series estimates in the class of bounded functions in the disk](https://arxiv.org/abs/2503.16313), arXiv:2503.16313v1 (2025). Section 2 and the complete proof of Theorem 1 on pp. 4–5 were inspected. This concerns weighted sums of squared coefficients and is not a determination of the arbitrary-p derivative-mean radius. The present proof does not rely on its extremal classifications.

The integral-mean contraction, local polynomial extension, extrapolation lemma, pointwise bound, limiting argument, and rational counterexample are all proved in `PROOF.md`. No inaccessible published argument is an unproved dependency of those results.

## Literature searches and their limits

Searches included combinations of “Goluzin”, “Duren”, “subordination”, “derivative means”, “integral means”, “radius”, “Hölder”, and the exact problem number and source title. Relevant hits above were inspected; numerous hits concerned other meanings of subordination or restricted geometric classes and were not used. No complete current resolution of this exact arbitrary-p problem was located in this search. That is a bounded negative search result, not a proof of novelty or an exhaustive bibliography.

## Prior repository work

The [AlecKriebel/Math repository](https://github.com/AlecKriebel/Math) was checked using:

- All-state PR searches for `2305039`, `"5.39"`, and `"derivative" "subordination"`: no matching PR returned.
- Default-branch code searches for `2305039` and `AMR-022-5039`: no matching result returned.
- Branch search for `2305039`: no branch returned.
- Direct inspection of `unsolved_math_prioritization/QUEUE.md`: the rank-524 row was `queued`, `0/5`, with no linked chat or findings.

The queue row was not used by itself as proof of no prior attempt. Searches may miss differently named unindexed material; this package makes no categorical claim that no prior work exists anywhere.

## Classification

- Exact primary statement: verified.
- Relevant classical proof ingredients: fully inspected in Reich and reproved here.
- Original Goluzin PDF: not inspected; bibliographic access only.
- Current full literature resolution: none located; completeness unclaimed.
- Mathematical result of this work: partial results; the full problem remains unresolved here.
- Historical priority: unclaimed.
- Public package content: original analysis and verification code only; no downloaded source PDFs or corpus files.
