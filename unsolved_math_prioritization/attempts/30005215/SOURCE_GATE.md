# Source and prior-work gate

Checked 2026-10-04 UTC. ID 30005215; code OWR-11101919-002; rank 562.

## Catalogue identity

https://www.unsolvedmath.com/problems/30005215 returned HTTP 403 on direct
retrieval, and web retrieval failed. The denial was not bypassed. The matching
record was recovered from the public Ulam AI UnsolvedMath dataset at revision
372682f27c1b0d3d39e75fa63ad7932c7a2e1bde:

https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The locally available file contains 15,458 records and has SHA-256
37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252.
A fresh read of the pinned dataset tree confirms the same LFS object hash.
This record identifies the question; its generated August 2026 label “open”
is not mathematical evidence. Neither the dataset nor the extracted record is
part of this public packet.

## Exact primary question and context

Dirk A. Lorenz, “Adjoint mismatch,” printed pp.2250-2252 in *Mathematical Imaging
and Surface Processing*, Oberwolfach Report 38/2022:

- https://ems.press/journals/owr/articles/11101919
- https://doi.org/10.4171/OWR/2022/38
- https://ems.press/content/serial-article-files/46975?nt=1

The full contribution, including the surrounding motivation, proposed
stochastic iteration, bilinear formulation, and references, was read. Printed
p.2251 was rendered and visually checked. The report's volume is 2022; the
publisher records publication on 14 June 2023.

The two targets are the Euclidean operator norm from a forward oracle alone,
and the norm of A-V from separate A and V^T oracles. The report explicitly
imposes limited vector storage, so assembling the matrices or growing a sketch
would not answer its intended question. It proposes stochastic ascent but says
a full convergence proof was missing at that time. Our note addresses existence
of a convergent low-memory method in the finite-dimensional exact-oracle setting;
it does not assert convergence for all the source's proposed step-size choices.

## Current primary literature and theorem-level matching

1. Bresch, Lorenz, Schneppe, Winkler, *Matrix-free stochastic calculation of
   operator norms without using adjoints*, arXiv:2410.08297v3.
   https://arxiv.org/abs/2410.08297v3
   The current landing page identifies v3, 3 December 2025, as latest. First
   submission was 10 October 2024. Introduction: finite-dimensional Hilbert
   spaces, O(max(m,d)) storage, incremental accuracy. Algorithm 1 and the full
   convergence chain in Sections 2.1-2.2 were read, including Lemmas 2.8-2.18,
   Theorem 2.19 and Remarks 2.21-2.23 covering exceptional multiplicities.
   Theorem 2.19 states almost-sure convergence to ||A||. The publisher page
   confirms the paper and claim: https://doi.org/10.1137/25M1772277 .
   The paper also points to the mismatch sequel.
2. Same authors, *Computing adjoint mismatch of linear maps*,
   arXiv:2503.21361v2. https://arxiv.org/abs/2503.21361v2
   The current landing page identifies v2, 9 March 2026, as latest. First
   submission was 27 March 2025. The introduction precisely matches separate
   A and V^T oracles and O(max(m,d)) storage. Sections 2.1-2.4, Algorithm 1,
   Propositions/Lemmas through Theorem 2.26, Remarks 2.27-2.28, and the
   corresponding appendices A.1-A.3 were read. Theorem 2.26 claims almost-sure
   convergence to ||A-V||. Printed p.12 was rendered to verify Proposition 2.11.
   Publisher DOI: https://doi.org/10.1016/j.cam.2026.117853 . The publisher
   search result and the authors' institutional publication list identify
   Journal of Computational and Applied Mathematics 488, article 117853.
   The issue is dated December 2026; this packet relies on the already available
   March 2026 preprint, not on a future issue date as evidence of access.
   Institutional listing:
   https://www.math.uni-bremen.de/zetem/cms/detail.php?language=en&person=JonasBresch&template=publikationen_person

The exact inspected versions matter. In the mismatch v2 proof, a rank-one
counterexample invalidates the blanket projected-determinant assertion in
Proposition 2.11; the proof of Theorem 2.26 also uses an incorrect product-of-
failure-probabilities estimate. These are specifically documented and bypassed
in `PROOF.md`. We neither infer that the desired theorem is false nor certify
an unseen publisher revision. The complete argument in this packet establishes
the claimed finite-dimensional existence result with compact plane maximization.
The authors retain credit for the algorithms and the prior resolution program;
our presentation is not claimed novel.

## Actual repository and PR checks

The QUEUE.md row was read afresh and was `queued`, `0/5`, with no chat or
findings. Queue blob SHA: c87c275c638939b8008fd58db80657491d14971e.
The queue alone was not used to infer absence of a previous attempt.

Repository: https://github.com/AlecKriebel/Math . The root tree at
fd3ccfc6435ef2f76ad371c119756c8ce080dfed was inspected. A recursive whole-tree
response was truncated (38,028 entries), so it was not treated as exhaustive.
The root nonrecursive tree and a separate complete recursive tree of
unsolved_math_prioritization, SHA 87f87a1dee35388240c13ed30c39a43502c771bd
(14,699 entries, truncated=false), were then checked for the exact ID, source
code, and relevant title terms. No matching attempt path was found.

Authenticated all-state PR searches for `30005215`, `11101919`, `"Asymmetric"
"Norm"`, and `"operator norms"` returned no matches. Code searches for the ID,
source number, and “adjoint mismatch” also returned no matches. These bounded
checks found no previous repository proof/PR for this problem; they are not a
claim that all possible unindexed or differently named work has been excluded.
The repository's AGENTS.md was read. No third-party contact was made.

## Gate result and publication scope

Source identity and both mathematical targets are verified. The generated open
label is superseded by matching prior primary articles plus the complete proof
in this packet. Suggested status: `already_solved`, turns `1/5`, with no novelty
claim. Independent adversarial review is still required before remote writes.

Only the attempt's public files and this row's Status/Turns cells are within the
proposed publication change. No source PDFs, source-text copies, catalogue
record/corpus, or private context may be committed. No merge, release, or
external outreach is authorized by this packet.
