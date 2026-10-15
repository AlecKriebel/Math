# PR523 acceptance gate — draft for independent falsification

## Decision under examination

Close the currently eligible `claimed_solved` PR without merging or depositing a preprint, after completion of independent mathematical, source, priority, and disposition reviews. This recommendation concerns acceptance as a new resolution of the original open problem. It is not a finding that the exact algebra is false.

## Strongest verified candidate claim

For every real matrix A and y=As with s in the unit cube, expansion of the objective gives a quadratic term plus nonnegative coordinate terms. Consequently the unprojected objective has unique optimizer zero. For the projected objective, every optimizer lies in ker(A^T) and every backprojection is zero. The full-row-rank row/column examples and the all-size construction meet their stated hypotheses. Root reproduced both frozen author/audit verifiers; independent reviewers are completing additional checks.

## Source and priority blocker

The candidate expressly limits its answer to the literal exact-minimizer formulation and disclaims refuting a separately specified numerical procedure. Its own source gate dated October4 already acknowledges scalar degeneracy in the original paper. Alper Ferudun, *A Negative Answer to the Kadu–van Leeuwen Conjecture on Dual Binary Tomography*, [DOI10.5281/zenodo.23110494](https://doi.org/10.5281/zenodo.23110494), Lemma2.1, gives the same universal box-feasible/projected theorem. The primary PDF hash is b374bbc76792418e60fa96a329a5ae6b6f5e596b12b5572b69466d6467bab43b. DataCite independently records registration and issue on October2,2026, before the candidate source check. No numerical claims from that preprint are needed for this theorem overlap.

## Reasonable repair evaluated

Keeping the exact formulation repairs no missing novelty or original numerical scope. Extending the draft from row/column examples to a three-direction unique binary image with a fractional feasible competitor would address a stronger obstruction: a nonzero feasible cube-tangent c in kerA prevents the binary image from equaling sign(A^T mu) for any mu. Root independently checked such an extension with exact arithmetic and exhaustively enumerated6250 row-conditioned images. Its concrete construction is Ferudun Theorem4.2, already published; the verified certificate has11 movable and14 fixed coordinates. Thus this extension cannot be presented as a new solution here. Other numerical procedures or auxiliary-primal outputs require independent formulations and proofs; the draft does not supply them. A new result would require materially new research rather than an editorial or reasonable local repair.

## Required safeguards

Before any disposition, finish the pending independent reports, have a fresh adversary attempt to overturn this inference, and recheck the live exact claimed_solved status, draft/open state and unchanged head. If the status ceases to be claimed_solved, skip further processing. Do not change the PR head status and then act on an excluded status. Preserve authored originals and publish checkable audit findings, with a concise evidence-linked closure comment only if this recommendation survives review. No acceptance DOI or tracker row is warranted for a rejected candidate.
