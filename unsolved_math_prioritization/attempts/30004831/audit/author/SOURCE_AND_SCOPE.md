# Source and scope audit

## Exact target

The target is problem 30004831, OWR-8415347-009, rank 784. The inspected original is Bichon's Question 1 on printed page 2413 of Oberwolfach Report 44/2021, PDF page 17, DOI https://doi.org/10.4171/owr/2021/44 . It asks whether Hopf algebras with equivalent linear tensor categories of comodules have the same cohomological dimension. The next sentence identifies that dimension with both global and Hochschild dimension. The finite, smooth, and cosemisimple cases are subsequent positive results, not hypotheses of Question 1.

The live problem URL could not be inspected: the web reader reported inaccessible and the HTTP request returned 403. The complete locally supplied problems dataset has exactly one matching ID and its statement SHA-256 matches the catalog's statement hash. Thus the target is pinned to the exact supplied record and independently checked report, without claiming live-site text verification. The record's longer source extraction garbles the large-characteristic exponent; that extraction is not used as mathematical evidence.

## Relevant dimensions and assumptions

- For an algebra A, Hochschild dimension means pd over A tensor A^op of A. It need not equal global dimension for an arbitrary algebra.
- For a Hopf algebra, left/right global dimensions, Hochschild dimension, and projective dimensions of the trivial left/right modules coincide. This is the invariant in the question.
- Gerstenhaber-Schack dimension, injective dimension, and Gorenstein global dimension are different invariants. No substitution among them is made.
- The equivalence is k-linear and monoidal between comodule categories. Compatibility with the forgetful functors to vector spaces is not assumed. Equivalence between algebra-module categories would be a different condition.
- Bichon's 2022 article explicitly works over an algebraically closed field. The counterexample here uses C, so this convention is respected.
- The reconstructed antipodes satisfy S^4=id. Bijective antipodes alone do not rescue the unrestricted assertion.

## Resolution and current literature

Zhu's Example 4.11 supplies the negative answer. The inspected arXiv manuscript is v2, dated 12 December 2025; publication metadata identifies J. Pure Appl. Algebra 229 (2025), issue 12, article 108123. Bichon's February 2026 introduction independently attributes the 1-versus-infinity counterexample to Zhu. This packet credits that existing result.

Bichon 2026, Theorem 3.5, proves equality when both global dimensions are finite over a fixed base field, without a bijective-antipode hypothesis. Its title's finite case means finite global dimensions, not finite-dimensional Hopf algebras. The inspected arXiv record has only v1 and no journal reference. This is reported as a preprint, without an acceptance claim.

Bichon 2022 proves positive smooth and cosemisimple cases. Neither restricts the original question retroactively. Our counterexample is not cosemisimple and one algebra has infinite dimension in the homological sense; hence it does not contradict those theorems.

The supplied August 2026 triage cites the February note but describes only positive results. The actual introduction already records the negative resolution. A dataset classification is not proof and was not used to determine the outcome.

## Convention reconciliation

The inspected v2 PDF, printed page 22, has two literal display issues relevant to reconstructing Example 4.11:

1. Its stated coproduct for y is 1 tensor y + y tensor g, while its left coaction on t is g tensor t + y tensor 1. These two choices do not satisfy left coassociativity together. Our proof uses the co-opposite coproduct y tensor 1 + h tensor y and the matching antipode -h^{-1}y. It directly checks coassociativity and the bi-Galois maps, so it does not assume the inconsistent pair of displays.
2. The range for the proposed normal-basis prescription includes j=n. Literal use of that endpoint sends x^n to t^n, although x^n=1-g^n and t^n=-g^n. The correct normal basis has 0<=j<n. We use j=0,1 at n=2. Bijectivity of an arbitrary comodule linear map alone is not a proof of convolution invertibility. We do not need that inference: the canonical maps have explicit inverses.

The two corresponding finite negative controls are included in the executable verification. These observations do not constitute a claim that Zhu's negative result fails. A consistent specialization is proved in full in PROOF.md. We do not claim an erratum exists or that the publisher's final typesetting has the same displays; the final journal PDF was not retrieved.

## Proven result and stopping rule

The exact unrestricted assertion is false, with an explicit attributed counterexample. Stop the new-proof search under the existing-resolution gate: zero of five new research approaches are charged. Reconstruction, source verification, and bounded algebra checks are verification work rather than an attempted new solution. No open gap remains for this original yes/no target once the standard bi-Galois equivalence theorem is admitted. Separate positive-subclass questions are not substituted for it.

Actual repository checks found no prior attempt for this exact target in the inspected default-branch directory, code, branches, commit messages, or PR searches. Those searches are bounded; they do not certify exhaustive priority. A fresh independent audit of this packet remains a separate step.

## Sources

- Original report: https://publications.mfo.de/handle/mfo/3899
- Zhu, inspected version: https://arxiv.org/abs/2501.02828v2
- Zhu, journal DOI: https://doi.org/10.1016/j.jpaa.2025.108123
- Publisher-deposited metadata: https://api.crossref.org/works/10.1016/j.jpaa.2025.108123
- Bichon 2026: https://arxiv.org/abs/2602.12731v1
- Bichon 2022: https://www.numdam.org/articles/10.5802/crmath.329/
