# Topological family — terminal synthesis

Timestamp: 2026-10-24T23:23:51.144813+00:00.

Full discovery completion estimate: **5%**. This is a subjective estimate of progress toward a complete resolution; it is not a claim that a proof has been completed. **Kourovka 21.122 remains unresolved by this family.** No original solution, positive or negative, is claimed.

## Strongest supplied mathematical artifacts

1. A self-contained reduction from an infinite small image on an arbitrary profinite group to a **countably infinite** compact word image on a countably based profinite quotient. No assumption on the value of the continuum is used.
2. The exact finite inverse-limit formulation: for a surjective finite-group chain `Q_n`, `(lim Q_n)_w = lim (Q_n)_w`. Uniformly bounded finite image sizes are equivalent to a finite limit image.
3. An explicit non-word continuous map exhibiting countable thin splitting. It satisfies compactness, conjugacy equivariance, compatibility with all integer powers, finite output conjugacy classes, and dense local constancy. It invalidates attempts to prove the target from those properties alone.
4. An explicit genuine `x^p` word-map example showing that infinitely many values need not occur on any abelian source subgroup. The class-two profinite construction has continuum many p-th powers but at most `p` p-th powers on every abelian subgroup. Finite stages show that even a uniform bound on all abelian restrictions does not bound the full image.

Items 1–3 are frozen in `FROZEN_CHECKPOINT_01.json`; fresh independent review was assigned by the parent. Item 4 and its checker/certificate are frozen separately in `FROZEN_DELTA_01.json`; the parent will arrange a separate fresh review. These are reductions and failed-route obstructions, with no priority or novelty claim. Neither computational certificate is evidence for the full conjecture: each checks the stated finite construction only.

## Mechanism ledger

| Family/mechanism | Evidence | Status | Exact gap |
|---|---|---|---|
| Cantor fusion from nowhere local constancy | DKS Proposition 2.1; elementary binary splitting | Valid conditional mechanism | Small image yields constant open regions; no proof that an infinite genuine word image has a restricted nowhere locally constant region |
| Scattered compact image / metrizable quotient | Self-contained reduction in checkpoint 1 | Reduction only | Must exclude countably infinite compact word images |
| Increasing finite word-image sizes | Exact inverse-limit equality | Reduction only | Unbounded widths allow a countable thin tree for abstract maps; a fixed-word algebraic obstruction is missing |
| Conjugacy equivariance / FC values / power compatibility | Explicit first-nonzero map meets all of them | Blocked as a sufficient mechanism | Additional genuine word algebra is essential |
| Infinite variation extracted on an abelian subgroup | Delta 1 gives a class-two counterexample | False as a general mechanism | Must handle combinations of noncommuting preimages |
| Arbitrary central-valued word map has bounded polynomial degree | Metabelian primary source proves its own restricted theorem | Blocked without new evidence | Cannot remove metabelianity without a proof |
| Periodic profinite group has bounded exponent | A separate conjecture in primary literature | Blocked | Would transfer the difficulty to an unsupported stronger claim |

## Primary scope and exact theorem boundary

The target is finite cardinality of the **set** of word values, not finiteness of the closed verbal subgroup. Shumyatsky's 2024 theorem gives finiteness only for `w(w(G))` under the small-image hypothesis. It does not settle the target. The de las Heras–Zozaya 2025 theorem requires a dense equationally Noetherian subgroup; none is supplied by the general topological reduction. The 2026 metabelian theorem applies to that subclass and its polynomial-map argument has not been generalized here.

Primary sources inspected locally and/or browsed during this run:

* [Detomi–Klopsch–Shumyatsky, arXiv:1907.01344v2](https://arxiv.org/abs/1907.01344v2).
* [Shumyatsky, arXiv:2401.15707v2](https://arxiv.org/abs/2401.15707v2).
* [De las Heras–Zozaya, arXiv:2502.07427v1](https://arxiv.org/abs/2502.07427v1).
* Zozaya, arXiv:2608.02237v1, local primary copy provided by parent.
* [Khukhro–Shumyatsky, *Words and pronilpotent subgroups in profinite groups*](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1671B034189A39CD04EBC7D32BC25843/S1446788714000317a.pdf/words-and-pronilpotent-subgroups-in-profinite-groups.pdf), for the separate bounded-exponent conjecture boundary.

A further current search lead, [arXiv:2609.25448](https://arxiv.org/abs/2609.25448), concerns measures of definable/verbal sets. Only its abstract was inspected; no theorem from it was used.

No external communication, outreach draft, branch creation, Git commit, push, or release was performed by this subagent. All files remain in this dedicated effort folder. The parent owns publication and independent review.
