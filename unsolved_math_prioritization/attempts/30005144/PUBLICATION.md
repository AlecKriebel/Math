# Accepted source-dependent finding: CMC min–max width

Problem 30005144 / OWR-10252937-007, rank 484. Accepted disposition: **already_solved, 1/5**. Date: 3 October 2026.

A fresh full independent mathematical audit passes the affirmative strict-width argument under the original referenced asymptotic convention. The full [audit report](audit/portable/PUBLIC_AUDIT_REPORT.md), its [expanded flat-end rigidity lemma](audit/portable/flat_end_rigidity.md), and portable controls are included. The six [original candidate files](public/README.md) remain byte-for-byte unchanged; their historical “pending audit” language records the earlier frozen state. This acceptance note supersedes that pending status without rewriting the record.

## Scope and credit

For a smooth, connected, complete, boundary-free, one-ended asymptotically flat three-manifold with nonnegative scalar curvature, not isometric to Euclidean space, the area-minus-c-volume mountain-pass width satisfies omega_c < 16 pi/(3 c^2) for every c>0. The asymptotic convention is the one printed in Mazurowski's 2022 Definition 26: unweighted smooth convergence plus the stated zeroth- and first-derivative rates. No weighted second- or third-derivative condition is added to the original manifold.

[Mazurowski–Zhu (2025)](https://arxiv.org/abs/2502.18455v1) provide the decisive smooth inverse-mean-curvature-flow theorem and strict-width mechanism under their weighted-C3 convention. Our packet adds the single auxiliary-metric transplantation bridge needed to reconcile the original convention, together with detailed local strictness and compact-parameter arguments. The whole original-convention proof is not quoted verbatim from their paper. No novelty, first-resolution, historical-priority, or human-peer-review claim is made. AI tools were used extensively, and this remains unrefereed.

## Additive advisory clarifications

1. In Section 4 of the frozen proof, volume tends to zero by spatial containment. Area tends to zero by the exact smooth-flow equation A'=A, which gives A(t)=A(t_0) exp(t-t_0). Containment alone would not bound area for arbitrary oscillating surfaces. These facts justify the zero initial terms in the integrated inequality and the empty endpoint's flat-plus-varifold continuity.
2. The spatial input is precisely Mazurowski–Zhu's Corollary 2.6, equation (2.11), with normalization min u on the boundary of D_1(q) equal to zero: D_{C^{-1} exp(t/2)}(q) minus {q} is contained in {u<=t}, which is contained in D_{C exp(t/2)}(q) minus {q}, for all t<=T once q is sufficiently far out. The constant C is fixed from metric equivalence; the far-out threshold may depend on T. Lemma 2.20 identifies the inner and outer level surfaces in the smooth regime. The frozen proof uses these precise sublevel bounds, not the t/T-mismatched spatial sentence printed in Theorem 1.5.
3. The expanded rigidity lemma supplies developing coordinates for an eventually flat original end and proves that their image contains a genuine Euclidean exterior. Scalar curvature is then compactly supported and integrable. The positive mass theorem is applied to that original manifold in exactly Euclidean coordinates, never to the auxiliary metric's cutoff annuli.

## Reproduction

From this directory, with Python 3 and SymPy 1.14.0:

```sh
python public/verify_algebra.py
python audit/portable/independent_controls.py
python -O audit/portable/independent_controls.py
python audit/portable/verify_frozen_packet.py public
```

The twelve author controls, sixteen independent controls, and six-file hash verification pass. The full audit reports separate mathematical dependency, source, topology, strictness, and portability checks. Finite algebra checks do not certify geometric analysis. No source PDFs, source-text extracts, raw corpora, screenshots, or private operational records are published.
