# Independent review of the version 2 completion

Baseline: repository commit `5ec53ad70`, the five completion commits after `cc320ba38`, and the exact final local ZIP. This review preserves production files and the supplied archive.

## Provisional verdict pending fresh complete reproduction

The independent semantic reviews support completion of the three requested model bridges. No actionable mathematical defect was found in their implementation or composition, and the reported earlier verification evidence matches the actual sources and archive. One publication-readiness correction remains: the standalone manuscript does not identify a retrievable version of its proof package.

The full fresh extracted reproduction is in progress. The final verdict will record its actual outcome; existing receipts and successful bounded probes are not represented as that new complete run.

## Finding: add a proof-package retrieval link before publication

Priority P2; `paper/main.tex:1785–1800`, in both repository and frozen package. The manuscript describes an “accompanying repository” and local filesystem paths, but supplies no explicit repository URL or companion DOI. The bibliography and verification appendix do not supply one either. A person receiving the PDF alone cannot identify the certified proof snapshot from those references.

Add a verified fixed-commit repository link now, or the actual companion version DOI when preparing the linked Zenodo release. Link the version containing the expanded proofs, not an old deposit. Rebuild both PDFs and update manuscript/package bindings. This is a discoverability and publication-readiness finding, not a failure of the Lean proof. Detailed evidence is in [the manuscript review](manuscript_review.md).

The current date line accurately calls this a working revision. Adding the original deposit date and actual revised-release date remains minor publication metadata work. No fictitious version 2 DOI appears in the package.

## Mathematical checks

- **Stochastic processing:** normalized product weights choose a complete deterministic response assignment for every source outcome at every input on both parties. A single distribution reconstructs the whole table. Physical PVM coarsening and convex-hull closure are proved, without falsely asserting raw-PVM closure.
- **Finite labels:** independently defined outcome-indexed measurements, behaviors, and strategy classes transport reversibly to the cardinal model. Both raw-set and ordinary convex-hull correspondences are proved. Empty outcome alphabets and absent inputs are distinguished.
- **Hilbert spaces:** source states/effects are genuine endomorphisms; positivity uses the source Hermitian form; normalization and probabilities use linear-map traces. The tensor form is basis independent. Isometric transport preserves joint probabilities, and complement allocation preserves normalized PVMs. Zero-dimensional normalized states are excluded by proof, not by hidden assumptions.
- **Combined conventions:** both bridges act on the same physical source strategy. Simulation yields one finite mixture of complete Hilbert-space PVM branches with the original output labels. The branches may use different states and qubit carriers, as the claim allows.
- **Independent compiled probes:** fresh review-only contracts expand the resulting table into actual tensor-Born traces. One composes all three bridges, including stochastic processing; another checks source dimension boundaries and the combined mixture. Both passed with only `propext`, `Classical.choice`, and `Quot.sound`.

See [Hilbert review](hilbert_review.md) and [stochastic/label review](stochastic_labels_review.md). These are independent AI-agent reviews, not external human peer review. They review the new mathematical work; they do not independently rederive every unchanged rank-case argument from scratch.

## Artifact and manuscript checks

The exact ZIP SHA-256 is `b301f82654bbebfdc3d91c3b0c7569d7a83e9cff9ffd0eb2b420cf6e82b52104` (11,427,095 bytes). Independent checks confirmed 1,269 safe unique members, all 1,268 root-manifest and 1,002 Lean-manifest hashes, all 104 protected inputs, all ten LaTeX archive members, and consistency with current production sources.

Both earlier successful runs have 138 authenticated command logs; their only failing command is the deliberately invalid compiler control. The recorded 68 production-module builds, 78 examples across seven contracts, and 826 standard-axiom reports were counted independently. Fresh manifest negative controls rejected seven invalid classes. See [package review](package_review.md) and its machine-readable evidence.

The revised manuscript correctly identifies the original strict-domain correction, supporting role of the known 3×2 architecture, stronger non-optimality-claiming SOS bound, and replacement proof routes. The new multiplier proof's deterministic reset and score-gap factor/sign match the formal declarations. Related-work claims were checked against [Zhu et al. v2](https://arxiv.org/html/2608.01317v2). No newly introduced mathematical error was found in this bounded changed-manuscript review.

Both 37-page PDFs were independently rendered and inspected, including all pages in contact sheets and individual verification/multiplier pages. No clipping, missing glyphs, overlap, or line-number collisions were found. Fingerprints and method are recorded in [pdf_review.json](pdf_review.json).

## Scope of the completion claim

The intended claim is completion of formal proofs of the principal results and stated model conventions. It is not formalization of every mathematical assertion in the paper. General duality/KKT, full manifold/Hessian/inertia statements, and the other disclosed auxiliary arguments remain manuscript-only. Their truth does not follow merely from a formal proof of the final theorem by another route.

The pinned Lean compiler/runtime and the compiled dependency-cache producer remain trusted. All project modules are to be freshly rebuilt in this review; Mathlib is not independently rebuilt, and online dependency bootstrap is not independently exercised. These limits are consistent with the supplied certificate.
