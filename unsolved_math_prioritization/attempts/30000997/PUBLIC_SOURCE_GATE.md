# Source and prior-attempt gate: 30000997

Checked 2026-10-03 UTC. Source gate recorded before the author attempt.

## Decision

Provisionally eligible for a first bounded attempt. The exact implication remains unresolved in the primary sources located. This is a bounded literature search, not a priority guarantee.

Live `unsolved_math_prioritization/QUEUE.md` blob `af6f0f2f386975404750e6baa9bbfea8831d9f16` has rank 428, ID 30000997 / OWR-2042-006, title **Degenerate Versus Full Ma–Trudinger–Wang Conditions**, queued, 0/5, blank Chat and Findings. Main was `b1dcffe4094e1e96200fa710566dd755722108f6` when checked.

## Original question and notation

Young-Heon Kim, joint work with Alessio Figalli and Robert McCann, *Continuity of optimal transport maps under a degenerate MTW condition*, Oberwolfach Report 31/2008, pp. 1751–1753, specifically p. 1752. Official source: https://ems.press/content/serial-article-files/46174 and https://doi.org/10.4171/owr/2008/31 . The page was downloaded and visually checked.

The question is whether MTW-perpendicular >= 0 implies MTW >= 0 for the Riemannian squared-distance cost. Let

S_c(x,y)[u,v] = (-c_ij,k'l' + c_ij,a' c^(a'b) c_b,k'l') u^i u^j v^k' v^l'.

The first condition tests only pairs with c_i,j' u^i v^j'=0; the conclusion tests every pair. These are A3w (weak regularity) and nonnegative cross-curvature (NNCC, sometimes B3w), respectively. This is not the implication from weak to strict MTW. Strict MTW/A3s adds strict positivity on nonzero orthogonal pairs. The normalization c=d_g^2/2 instead of d_g^2 preserves the signs.

### Scope distinction, not a silently strengthened statement

The single OWR question does not explicitly say complete, compact, CTIL, or a dimension. Its surrounding general-cost regularity discussion uses smooth bounded domains in R^n, c in C^4 on their product closure, twist/nondegeneracy, mutually uniformly c-convex domains, and bounded positive densities. Those hypotheses support the transport-regularity discussion; the curvature-implication question itself is geometric and does not quantify densities.

The cited Kim–McCann paper [5], *Towards the smoothness of optimal maps on Riemannian submersions and Riemannian products*, section 1.2, PDF p. 4, explicitly takes complete Riemannian manifolds and defines their A3w/A3s/NNCC conditions on N=(M×M) minus the cut-locus relation. Source: https://www.math.toronto.edu/mccann/papers/RiemSub.pdf . This supports the standard **global-manifold interpretation** adopted for the main attempt: smooth complete connected M of arbitrary finite dimension, c=d_g^2/2 on all N; A3w at every point of N and every null pair should imply NNCC at every point of N and every pair.

The original short wording also admits a possible **restricted-domain interpretation** if read only inside a smooth product chart. Retain such local results separately. A metric jet or local A3w example with negative full cross-curvature does not settle the standard global interpretation. Do not silently add compactness, CTIL, uniform c-convexity of the whole cut domain, or a small-neighborhood restriction. A positive proof requiring these would be conditional progress. A negative answer to the global reading needs a complete manifold with A3w verified everywhere off the cut locus and a full-cross-curvature violation somewhere there.

## Literature distinctions

- Kim's 2019 lecture notes, Definition 2.12 and Remark 2.13, pp. 6–7, identify MTW=A3w and NNCC and explicitly present their implication for Riemannian squared distance as a folklore conjecture. https://personal.math.ubc.ca/~yhkim/yhkim-home/research/revision-yhk-SMS-lecture-2019-revision.pdf
- Lebedeva–Petrunin–Zolotov, *Bipolar comparison*, section 8, Question 8.5, still leave the separation of MTW and MTW without perpendicularity unresolved, including the CTIL case. Its main theorem relates CTIL+NNCC to bipolar comparisons, not A3w alone to NNCC. https://arxiv.org/abs/1711.09423
- Léger–Todeschi–Vialard, *Nonnegative cross-curvature in infinite dimensions: synthetic definition and spaces of measures*, arXiv:2409.18112v3 / GAFA 35 (2025), section 4.1 Proposition 4.1, assumes both convex injectivity domains and full NNCC before deriving synthetic NNCC. It does not supply the requested implication. Its general-cost LMP counterexamples are not squared-distance Riemannian counterexamples. https://arxiv.org/abs/2409.18112
- The 2008 report's nearby low-regularity motivation is historically stale: Figalli–Kim–McCann, *Hölder continuity and injectivity of optimal maps*, obtains local regularity for A3w costs under domain and density hypotheses. This is not a proof of NNCC. https://arxiv.org/abs/1107.1014
- General costs already separate A3w from NNCC: the report gives |x-y|^(-2). The negative exponent was visually checked; a search excerpt incorrectly flattened it to +2. Such a cost cannot be used as the requested squared-distance example.
- The known nonnegative-sectional-curvature examples failing A3w do not help: they fail the antecedent. Round spheres, Euclidean space, their appropriate products and Riemannian submersions satisfy NNCC and are positive examples only.

Searches performed on the exact title/code, A3w/cross-curvature, MTW/NNCC, Riemannian orthogonality, and 2024–2026 developments located no full resolution as of 2026-10-03. This is not exhaustive proof of current openness.

## Reproducible corpus provenance

The exact statement was checked against the official OWR PDF, not accepted solely from the dataset. The repository manifest identifies ulamai/UnsolvedMath snapshot 37e53eabe540fb458758e198be61634bd02ee008. Both full cached files were independently hashed before extraction: problems.json SHA256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf (68,931,837 bytes); research_results.json SHA256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b (80,334,822 bytes). No research report was joined to this exact code.

Review hash: e897ad6b8bb02f99a54669af85e328b2b4de7c59899e2a89e90727ac71f918e9. Statement hash: d0e487abee28154faccd6476767c39b520b7d4fd5a621eee591c3023000a4634. Curation: UnsolvedMath Contributors, CC BY 4.0; underlying sources retain their own terms.
