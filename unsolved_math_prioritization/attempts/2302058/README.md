# Hellerstein's natural-path question: known affirmative answer

Problem 2302058 / AMR-022-2058, Function Theory Problem 2.58.

**Current status:** already solved, affirmative, credited to A. E. Eremenko (1985). One substantive verification attempt. The complete [independent audit](audit/AUDIT_REPORT.md) returned PASS for the exact nonzero exceptional-value and circle-level formulation, with the published surface theorem retained as an explicit dependency.

## Files and review status

The eight files under [artifacts](artifacts/README.md) preserve the author-stage snapshot byte-for-byte. Their references to an audit being pending describe that earlier stage. The completed audit and [audit status](audit/AUDIT_STATUS.json) supply the subsequent review result. This is an internal mathematical audit, not external peer review.

The [verification](artifacts/PROOF_VERIFICATION.md) uses Eremenko's multi-line parabolic surface existence theorem on page 309 of [the 1985 paper](https://www.math.purdue.edu/~eremenko/dvi/naturalac.pdf). It explicitly transfers the forbidden rays by a bounded quasiconformal shear and uses F=1+1/q to obtain the exact level circle. It does not independently reconstruct every sewing detail or Volkovyskii's theorem. No self-contained new construction or novelty claim is made.

## Checker clarification

Section 6 of the preserved verification note says that the checker samples the deformation and its inverse. More precisely, the checker samples the forward deformation and determinant, checks the reciprocal circle identity, and tests a finite-order comparison path. It does **not** numerically invert the shear Ψ. Global invertibility and the inverse Lipschitz estimate are established analytically in Section 3 and in the independent audit.

The 2,593 passing checks are limited algebra/transcription controls, not a computational existence proof. Run `python3 artifacts/checks/check_normalization.py` from this directory. No new research paper, release, or DOI is proposed.
