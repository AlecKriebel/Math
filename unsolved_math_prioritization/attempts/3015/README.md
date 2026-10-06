# Kirby Problem 5.8: audited partial report

**Unsolved. Five substantive approaches completed (5/5). No novelty claim.**

This report concerns closed aspherical topological five-manifolds without simplicial triangulations. The independent mathematical audit accepts the unchanged author report as a valid partial, with no correction required. It constructs no such manifold and proves no impossibility theorem. The separate four-dimensional question is also unanswered.

## Accepted deductions and limitations

- For closed connected topological five-manifolds, nontriangulability is detected by the mod-two characteristic number obtained by evaluating the first Stiefel–Whitney class times the Kirby–Siebenmann class.
- Every product of a closed connected topological four-manifold with a circle is simplicially triangulable.
- Connected even-degree finite covers in dimension five are triangulable; connected odd-degree covers preserve triangulability status.
- With an orientable four-dimensional fiber, the mapping-torus characteristic number is orientation-reversal parity times the fiber's Kirby–Siebenmann number. The mapping torus is aspherical exactly when its fiber is. Spin fibers cannot furnish the required example.
- The checked hyperbolization constructions remain in dimensions at least six; the needed four-dimensional PL boundary step is not established.

These deductions are based on established results and do not resolve the remaining realization or universal-vanishing problem. Simplicial triangulation is not replaced by PL structure.

## Reading order

1. [Independent mathematical audit](audit/INDEPENDENT_MATHEMATICAL_AUDIT.md)
2. [Unchanged authored proof](audit/author/PROOF.md) and [five approaches](audit/author/APPROACHES.md)
3. [Independent acceptance](audit/ACCEPTANCE.json) and [current publication verdict](VERDICT.json)
4. [Public source inspection metadata](audit/AUDIT_SOURCE_METADATA.json), [corpus verification metadata](audit/CORPUS_VERIFICATION.json), and [publication integrity checks](PUBLICATION_CHECKS.json)

The two ZIP archives are the exact immutable author and independent-audit freezes. Their external manifests pin every member. The extracted `audit/` directory is byte-identical to the audit archive; its `author/` subdirectory is byte-identical to the author archive. Author-stage pending-audit fields and audit-stage unpublished fields remain historical records; the separate acceptance and publication records establish the later stages.

The public package contains authored mathematical prose and verification metadata only. It excludes copied source documents, extracted source text, screenshots, dataset contents, private sources, private coordination, and executable payloads. No mathematical machine verification is claimed. The external integrity harnesses each passed four configurations and rejected 22 corruptions under normal and optimized Python; the audit freeze also passed relocated hostile-module readback in both modes.

Only this target's queue Status and Turns cells are changed, to `unsolved` and `5/5`. Other queue bytes, scores, titles, links, and canonical state files are untouched. Publication is a draft PR only.
