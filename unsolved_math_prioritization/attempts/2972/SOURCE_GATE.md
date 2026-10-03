# Source and scope gate: 2972 / KP-4.96

Checked 2026-10-03 (UTC). **Closed target unresolved; public result is partial.**

## Primary identification

The requested catalogue URL, https://www.unsolvedmath.com/problems/2972, returned HTTP 403 in direct retrieval and was unavailable through the web reader. It was not used as a mathematical authority.

The primary replacement is the author-hosted K3 manuscript:
https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

Locations checked: §4.9 introduction (printed p.263), Problem 4.96 and its two remarks (pp.269–270), and the closed-manifold cross-reference in Problem 4.108 (p.281). The exact problem, rather than just a title or catalogue summary, was inspected. The target sentence omits a compactness qualifier. The closed interpretation is therefore explicit in this package and is not asserted to be a verbatim hypothesis in that sentence.

The often-cited https://aimath.org/pastworkshops/kirbylistrep.pdf is a four-page workshop report, not the full problem list; it does not establish the exact statement. No primary PDF or extracted source text belongs in the public payload.

## Evidence used and what it establishes

- Salamon, [arXiv:1211.2940v5](https://arxiv.org/abs/1211.2940v5), §§2.1–2.7, pp.2–7: full Corollary A proof and its stated Seiberg–Witten inputs checked. The imported conclusion is equality of canonical Spin-c structures for closed cohomologous four-dimensional forms. The full foundational gauge-theory proofs are not re-proved here.
- Hajduk–Walczak, [arXiv:math/0312465](https://arxiv.org/abs/math/0312465), Corollary 2.11, p.9: checked as a prior stronger result covering the elementary T³-invariant calculation. No novelty claim for Proposition 4.
- Lin–Wu, [arXiv:2507.14636v2](https://arxiv.org/abs/2507.14636v2), Theorem 1.2 and full construction/proof in §3, pp.8–9: checked. The explicit pullback formula is enough to exclude this construction from the requested all-diffeomorphisms counterexample, independently of the deep non-isotopy proof.
- Ning, [arXiv:2505.09550v1](https://arxiv.org/abs/2505.09550v1), complete paper, especially Theorem 1.3 and §4: read through. Its six-dimensional stabilization has neither the required dimension nor matching first Chern classes. No theorem descending that construction to dimension four was found.
- Fine–He–Yao, [arXiv:2503.05272v2](https://arxiv.org/abs/2503.05272v2), Theorem 1.2 and §§2–3: its proof of the symmetry-restricted result was inspected. It assumes a hypersymplectic triple and a circle symmetry; those hypotheses are not available for arbitrary target forms.
- Li–Ning, [arXiv:2607.18778v1](https://arxiv.org/abs/2607.18778v1), §§1.2–1.4: the exact domains and conclusions of Theorems 1.8–1.9 were inspected. They concern restricted types of forms. This package does not purport to certify every dependency in their 29-page paper.
- Iida, [arXiv:2608.09361v2](https://arxiv.org/abs/2608.09361v2), §§1,7,9–10: checked the closed-question reduction and the non-equivalence proofs together with their named cap-extension and Floer inputs. Theorem 1.8 reports an affirmative normalized, unmarked relative filling construction; it explicitly leaves the closed problem unanswered. The 56-page preprint is treated as current literature, not as an independently re-proved result of this package. Its foundational dependencies were not independently certified here.

All claimed new deductions in PROOF.md have their own proofs. The declared Taubes–Seiberg–Witten input is the only deep imported result needed for the equivalence between the two closed formulations. The other literature is used to prevent incorrect promotion of restricted results to full solutions.

## Prior-attempt check

Before this investigation, the public repository's queue row was `queued | 0/5`. This was not treated as sufficient evidence of a fresh target. Direct checks also found:

- No directory at `unsolved_math_prioritization/attempts/2972` (404), and no 2972 entry in the attempts directory listing.
- No matches in all-state pull-request searches for `2972`, `KP-4.96`, or `4.96`.
- No matching repository code-search result for `2972`, and no root directory named for this problem.
- No 2972 entry in the related-target groups file.

These are bounded negative checks, not a guarantee about unindexed or unpushed work. Broad recursive tree reads failed with a transport error; those failed reads are not counted as successful checks.

## Claim gate

A full positive solution would require a closed four-dimensional pair and a proof excluding every symplectomorphism. A full negative solution would require transitivity of the appropriate diffeomorphism action for every closed target. Neither criterion is met. Isotopy obstructions, dimension-six examples, scale changes, and inequivalent fillings do not by themselves pass this gate.
