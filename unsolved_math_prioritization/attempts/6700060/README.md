# Mean-convex extremality: qualified credited preprint resolution

Target **6700060 / AMR-066-0060**, supplied queue rank 702. Current disposition, 2026-10-05: **claimed_solved, 1/5**, strictly in the ambient-smooth, face-preserving up-to-corners category described below. This guide controls the present interpretation of the unchanged historical packets.

## Exact result and attribution

For a compact full-dimensional convex Euclidean polyhedron, a face-preserving Euclidean competitor with nonnegative face mean curvature cannot decrease every corresponding interior dihedral angle weakly and at least one angle strictly, provided the correspondence and its inverse are smooth in the ambient-extension sense, with nonsingular differential through every corner. In this category, all corresponding dihedral angles must agree. In particular, Gromov's extremal convex polyhedra are mean-convexly extremal in this category.

The all-dimensional conclusion is credited to Yuchen Bi, [*Dihedral Rigidity for Convex Polytopes by Smooth Approximation*, arXiv:2608.06320v1](https://arxiv.org/abs/2608.06320v1), Theorem 1.1, posted 6 August 2026, together with the explicit Euclidean pullback/application bridge and separate planar argument. The independent proof audit found **no unresolved analytic gap** in the needed smoothing, logarithmic trace estimate, smooth-boundary index/existence, nonvanishing limit, closed-corner angle recovery, or Euclidean application route. It imports the published smooth-boundary analytic input of Simon Brendle, [*Scalar curvature rigidity of convex polytopes*, Inventiones Mathematicae 235 (2024), 669–708](https://doi.org/10.1007/s00222-023-01229-x), especially Propositions 2.14–2.15. The inspected Brendle manuscript is [arXiv:2301.05087v4](https://arxiv.org/abs/2301.05087v4), not the publisher PDF.

Bi's source remains a **recent preprint** in the checked public sources. No journal acceptance, human peer review, formal proof verification, community consensus, or new discovery is claimed. This is a qualified credited preprint-based resolution, not an unqualified already-solved classification. The proof audit is an AI-assisted mathematical assessment; finite code checks do not certify the analytic theorem.

Broader corner-singular notions of diffeomorphism, including facewise/interior smooth maps with degenerate corner differential, are **unverified** here. Smoothness of the inverse and nonsingularity up to every corner are essential to the positive-definite neighborhood pullback. The earlier ambient-extension convention in Gromov's [*Dirac and Plateau Billiards in Domains with Corners*](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/Plateauhedra_modified_apr23.pdf), September 20, 2013 author manuscript, §1 pp.2–3, supports this interpretation; see the independent audit §3.1. It does not settle every broader reading of the 2017 question.

## Source-status boundary

The original question is in M. Gromov, [*101 Questions, Problems and Conjectures around Scalar Curvature*](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf), 2017, §22, printed p.60. The correct title says **around Scalar Curvature**, rather than the historical packet's “about Scalar Curvature.” The original files remain byte-for-byte unchanged; this guide supplies the correction.

The Wang–Xie–Yu v6 route is not a proof dependency. [Bär–Hanke–Schick, arXiv:2202.05180v2](https://arxiv.org/abs/2202.05180v2), July 2026, says WXY v6 remains under verification; its counterexamples concern v2. That note neither refutes nor validates v6. The accepted argument uses Bi's smooth approximation and Brendle's published smooth-boundary theorem without importing a singular-polyhedral Fredholm theorem from WXY.

Current detail-page contents, full raw AI corpora and target-specific AI reports were not reverified. The bounded historical attempt search found no matching target attempt in its inspected scope; it is not exhaustive repository-history clearance. These provenance limits remain separate from the mathematical verdict and are documented in the frozen source-status and audit files.

## Reading order and unchanged records

1. This guide and `RELEASE_STATUS.json` state the controlling scope and status.
2. `public_packet/PROOF_APPLICATION.md` supplies the pullback, dimension and planar arguments; `PROOF_VERIFICATION.md` supplies the author's analytic checks.
3. `independent_audit/INDEPENDENT_AUDIT.md` supplies the full fresh adversarial proof/source audit, with exact boundaries and imported foundations.
4. The source metadata and audit bindings record public retrieval hashes, sizes, match results and inspection histories.

All **11 author files** and **7 independent-audit files** are preserved exactly. Historical statements such as “pending audit,” “no remote writes,” and “no queue changes” describe those frozen stages, not the present release stage. The audit's `qualified_pass` is the current mathematical assessment. Original manifests remain valid. Original ZIP archives were checked against every member and retained outside this publication; their sizes and hashes are recorded in `FROZEN_BINDINGS.json`.

## Turn accounting and checkpoint

The substantive research count is **1/5**: one source-verification/application route, stopped early for the credited preprint result. Internal checks, source substeps, tool calls, message exchanges and the independent audit are not additional substantive proof approaches. No five-approach exhaustion is asserted. At this 2026-10-05 checkpoint, the bounded goal of preparing and auditing the explicitly scoped credited result is complete (100%); no percentage of resolution is assigned to broader corner regularities.

Only this target's `Status`, `Turns` and previously blank `Findings` cells are changed in `QUEUE.md`. Chat, DOI, unrelated rows, formatting and the existing embedded header are preserved. No queue regeneration is part of this change.

## Reproduction

Requires Python 3 and SymPy 1.14.0. From this directory run:

```sh
python3 -B verify_release.py --self-test
python3 -B -O verify_release.py --self-test
```

The wrapper checks exact inventories, externally pinned inner manifests, content hashes and replay outputs. It runs all 4,293 author finite controls and 75 independent diagnostics directly in both normal and optimized Python; the original packet's seven actual corruption controls are rejected in both modes. The release self-test additionally mutates actual copied files and rejects changed, missing, extra, symlink and manifest-tampering cases. `REPLAY_RESULTS.json` records the relocated checks. These are reproducibility and finite-diagnostic checks, not PDE/index/compactness proof certificates. GitHub CI status must be reported separately; zero checks is not a CI pass.

Only authored proof/audit/code and public verification metadata are included. Source PDFs, source extracts or images, dataset records and private coordination files are excluded. This draft does not merge, create a release, issue a DOI, submit a manuscript or contact anyone.
