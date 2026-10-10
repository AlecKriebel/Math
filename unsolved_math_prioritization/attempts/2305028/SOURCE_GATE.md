# Source and scope gate

## Exact target

[Catalogue entry 2305028](https://www.unsolvedmath.com/problems/2305028)
asks whether every function continuous on the closed unit disk and
holomorphic on the open disk satisfies a limit of 1 for the ratio of its
interior to its boundary modulus of continuity, using Euclidean chord
distance in both definitions.

The catalogue page could not be retrieved by the web tool on 2026-10-03.
A previously pinned catalogue record was used only to identify the problem
and source. Its generated open-status classification was not accepted as
evidence. The actual statement and update were checked in the primary
collection below.

## Primary evidence and classification

1. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*,
   [arXiv:1809.07200](https://arxiv.org/abs/1809.07200), Problem and Update
   5.28, printed p. 95 (PDF page 96). Update 5.28 attributes a negative
   answer to Rubel, Shields and Taylor, reference [679]. The statement and
   update were read directly, including the PDF.
2. L. A. Rubel, A. L. Shields and B. A. Taylor,
   *Mergelyan sets and the modulus of continuity of analytic functions*,
   Journal of Approximation Theory **15** (1975), 23–40,
   [DOI:10.1016/0021-9045(75)90112-4](https://doi.org/10.1016/0021-9045(75)90112-4).
   The [University of Michigan repository record](https://deepblue.lib.umich.edu/items/6c023c47-bf4b-4c8d-be84-2ac067221820)
   provided the full journal article. The introduction and the complete
   relevant proof in §4, especially Lemmas 4.1–4.2 and Proposition 4.3,
   pp. 35–39, were read. The displayed formulas were checked against page
   images because text extraction omitted several equations.

**Classification: already solved, negative answer, published in 1975.**
The exact problem is fully covered by Proposition 4.3. A stronger radial
numerator already has limsup ratio greater than 1. The closed/open disk
convention is reconciled explicitly in PROOF.md. No unresolved part of the
stated question is claimed. Optimal comparison constants are not this
problem and are not addressed.

## Reconstruction and source distinctions

PROOF.md verifies the mathematical construction in fresh notation and
wording. It replaces the source's cutoff asymptotics with a fixed cutoff
R = 2^24 and a rational strict-gap certificate, and supplies a detailed
compactness argument for the expanding-circle limit. Its geometric-series
choice makes the later perturbation budget explicit. These are expository
verification choices, not a claimed new mathematical result.

The proof does not depend on later improvements to comparison constants,
search snippets, or the generated catalogue research summary.

## Repository prior-attempt gate

On 2026-10-03 the live main-branch queue row at rank 523 was `queued`,
`0/5`, in
[unsolved_math_prioritization/QUEUE.md](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md).
The retrieved file blob was a34c276a8fd0251396fa3a3d2ad2400fe381733f.
Live all-state pull-request searches for `2305028`, `AMR-022-5028`,
`5.28`, and the author pair Rubel/Shields returned no matches; a branch
search for `2305028` also returned no matches. Main-branch code search for
`2305028` returned no matches. These are bounded negative checks, not a
claim that repository search is exhaustive. The queue label alone was not
treated as proof of no prior attempt.

## Reproduction and rights

Only the authored note, source references, research log, status, verifier,
and verifier output are intended for publication. Scholarly PDFs,
extracted source text, source-page images, catalogue data, and repository
lookup receipts are local-only research inputs and are excluded.
