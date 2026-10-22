# Source and claim boundary

## Identification

Catalogue identifier: 2307054 / AMR-022-7054. Primary problem: P. J. Rippon's Problem 7.54 in W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, printed page 177 (PDF page 178).

- Primary record: https://arxiv.org/abs/1809.07200v2
- Primary full text: https://arxiv.org/pdf/1809.07200v2
- Catalogue: https://www.unsolvedmath.com/problems/2307054

Checked 2026-10-03. The catalogue endpoint returned HTTP 403. Cached catalogue material was used only to identify the primary problem, not as mathematical or status evidence. The complete primary problem and its adjacent update were inspected in text and page image.

The defining recurrence is `F₀=-1`, `Fₙ₊₁=exp(tFₙ)-1`. The question concerns every Taylor coefficient for every positive iterate. The primary display contains a typographical error: the second term of `exp(-t)-1` is printed as `t/2!`; its correct value is `t²/2!`. The recurrence itself is unambiguous and governs this investigation.

The 2018 update states: “No progress on this problem has been reported to us.” This is a dated status report, not evidence that no later solution exists.

## Prior work and bounded literature search

Repository and issue/pull-request searches in AlecKriebel/Math used the numeric ID, catalogue code, problem number, and Rippon's name. Commit and branch searches used the numeric ID. No prior actual proof attempt was located by these searches. The queue listed the problem as queued at 0/5; that queue entry alone was not treated as a prior attempt.

Public searches combining Rippon, coefficients, formal power series, exponential iteration, the proposed bound, and the problem number did not locate a later resolution or a directly applicable complete proof. This bounded search is not an exhaustive review and establishes no priority claim.

## Mathematical dependencies and outcome

The argument uses only the elementary exponential series, exact coefficient manipulation, and Cauchy's coefficient formula, with the needed estimates derived explicitly. No external research theorem is used as an uninspected proof dependency.

Outcome: partial bounds only; no full solution or counterexample. The exact remaining region is stated in `proof.md`. Original source PDFs, copied source corpora, and unrelated repository or personal material are not part of this package.
