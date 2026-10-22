# Advection–diffusion control: qualified prior-preprint thresholds

Problem **30003759 / OWR-16157-001**, rank 739. Overall disposition: **unsolved, 1/5**.

## Governing disposition

This wrapper and the [independent audit](advection_control_30003759_independent_audit/AUDIT_REPORT.md) govern interpretation of both preserved historical freezes. The audit requires **REVISE_REQUIRED** for any unqualified full-resolution disposition. The original endpoint-inclusive problem remains unresolved because positive critical endpoint boundedness is open. Neither `already_solved` nor an unqualified overall `prior_resolution_preprint` label is justified.

[Koike–Laheurte, arXiv:2609.35355v1](https://arxiv.org/abs/2609.35355), submitted 28 September 2026, determines the sharp **infimum** thresholds for the exact L²-cost problem:

- Positive drift M>0: threshold 2L/M. Cost diverges below this time and tends to zero above it. Boundedness at equality remains **open**.
- Negative drift M<0: threshold (2+2√2)L/|M|. Cost diverges below it and tends to zero at and above it, including the negative critical endpoint.

These are attributed preprint results. No journal acceptance, new full solution, or priority claim is made. The original problem is from Münch's contribution, printed pp. 951–952 of [Oberwolfach Report 16/2018](https://publications.mfo.de/bitstream/handle/mfo/3638/OWR_2018_16.pdf?isAllowed=y&sequence=1).

## Exact scope and mandatory corrections

The equation is y_t − ε y_xx + M y_x = 0 on (0,L), with left Dirichlet control v(t), homogeneous right endpoint, and zero terminal target. L>0 and nonzero M are fixed, while ε tends to zero through positive values. The cost takes the supremum over the **L²(0,L) initial unit ball** of the least L²(0,T) control norm. This is a uniform-in-data cost, including ε-dependent data. H⁻¹ state well-posedness does not establish an H⁻¹-unit-ball cost theorem.

The historical author's sentence that no further campaign is warranted records an **infimum-only stopping decision**. It does not dispose of the original endpoint-inclusive problem or bar future work on its remaining positive endpoint. The overall queue therefore stays unsolved at 1/5.

The later audit substantively reviewed the preprint's mathematical proof chain, independently verified retained elementary arguments, and checked a pivotal cited Bernstein inequality. It found no fatal defect within that stated scope. This is an **independent AI mathematical proof review**, not human peer review, journal acceptance, formal verification, or a machine-checked proof of continuum observability. Standard analytic foundations were assumed as described in the audit. Numerical and finite algebra checks are consistency/regression evidence only.

## Reproducibility and preservation

Run `python verify_publication.py` from this directory or by absolute path. It checks the closed file set, immutable archive and manifest pins, required disposition, exact archive-to-file correspondence, and all author/independent normal and optimized replays. No network or third-party package is needed. The strict publication verifier is controlling; the frozen author's weaker manifest checker is historical evidence.

Both ZIPs and all their allowlisted files are preserved byte for byte. Frozen author prose is not silently rewritten. `PUBLICATION_STATUS.json` records the qualified governing status. `PUBLICATION_MANIFEST.json` hashes every delivered file except itself. PDFs, source extracts, raw datasets, and private coordination material are excluded; public bibliographic and integrity metadata is retained.

The queue patch changes only this row's Status, Turns, and Findings. Chat, DOI, the stale embedded header, every other cell, and all other queue bytes are preserved.
