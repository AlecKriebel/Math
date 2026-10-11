# Reproduction and verification scope

The paper is a standalone main.tex with its bibliography embedded. Compile with the built-in Codex LaTeX editor/compiler, or run `tectonic main.tex` (tested with Tectonic 0.16.9). Rename main.pdf to paper.pdf. No separate bibliography program or additional project file is needed.

Run `python3 upstream_finite_checks.py` using Python 3.10 or later. It performs exact-rational checks on dyadic transport, covariance, recursive colors and admissibility; these finite checks are corroboration, not a proof over every group element or an analytic verification.

The nonamenability dependency was audited manually against its pinned original proof by two independent AI agents with different emphases, and by the lead agent. Its finite boundary argument and the published Benyamini–Sternfeld displacement input were checked. The actual Lean declaration/import closure and standard-PL/invariant-mean semantics were inspected. The project has **not reproduced a Lean kernel build**: the disk filled before dependency setup. No claim here relies on reproduced formal verification, and neither the C*-simplicity note nor its trace consequences have been formalized by this effort. An unrun build is not counted as a passing check.

Sources are pinned at OpenAI commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. Source manifests record the bytes inspected. Obtain the upstream repository separately for source reinspection; no third-party source/PDFs are redistributed in this deposit.

The verification archive records manual proof audits, primary-source theorem chains, priority queries, finite exact checks, hashes and actual checks completed. Automated reviews do not replace human refereeing. All claims are inspectable and subject to the validity of the cited external theorems.
