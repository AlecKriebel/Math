# Acceptance and publication scope

## Accepted result

The complete original candidate (11,969 bytes, SHA-256
5251358434993a8021986f760f9a99710fededdd98d842bc9de14b1d2dd947e4) and complete
independent audit (18,269 bytes, SHA-256
b6fd0021e1cacbdf5f4493c73ca72a4fe2b6060ebce4177cd19aa144a073575f) support an
accepted, correctly attributed, published negative resolution of Bandeira's
Open Problem 9.5 under its exact original Gaussian hypotheses.

For symmetric W with independent centered Gaussian upper-triangular entries
of variance 1/n, let p(W) maximize x^T W x over x >= 0, ||x||_2 = 1, and let
s(W) maximize Tr(WX) over X positive semidefinite, entrywise nonnegative,
and Tr(X) = 1. The accepted conclusions are:

1. s(W) converges to 2 in probability and expectation.
2. p(W) <= sqrt(2) + o(1) with probability tending to one, by a proved Gaussian
   comparison and concentration argument.
3. With probability tending to one s(W) > p(W), so no optimal SDP matrix has
   rank one. Both original conjectures are false.

The construction and prior negative resolution are credited to Bandeira,
Kunisky and Wein, PMLR 145, 153–171, Theorem 4:
https://proceedings.mlr.press/v145/bandeira22a.html . The publisher's citation
year is 2022; the conference/PDF header uses 2021. The original preprint was
submitted December 3, 2020: https://arxiv.org/abs/2012.02243v1 . No mathematical
novelty or first-resolution claim is made.

The full limit p(W) -> sqrt(2) is an attributed consequence of
Montanari–Richard's Theorem 2 and the proved diagonal transfer:
https://arxiv.org/abs/1406.4775 . The audit checked its normalization,
definitions, assumptions, and beta-zero specialization, but did not
independently reprove its approximate-message-passing lower bound. That
stronger result is not needed for the accepted negative answer.

## Explicit qualifications retained

The proof first defines invariant GOE with off-diagonal variance 1/n and
diagonal variance 2/n. It then proves the probability and expectation
operator-norm transfer to the original all-upper-entry-variance-1/n model.
It does not use Haar eigenspaces for a noninvariant ensemble.

The published PDF's reversed variance display was visually verified during
the audit. Calling it a typo is a supported mathematical diagnosis, not an
author-confirmed erratum. No author confirmation was obtained. Correctness
of the reconstruction is independent of that label.

Gaussian concentration, Sudakov–Fernique, and the global semicircle theorem
are named inputs accepted after statement/hypothesis checks. The complete
authored application arguments, including the all-negative comparison case,
flooring of the projector rank, fixed-parameter order of limits, expectation
bound without a uniform-integrability assertion, and rank-one equivalence,
remain in PROOF.md and AUDIT.md.

The scope excludes planted recovery thresholds, finite-n cutoffs, arbitrary
non-Gaussian universality, unrelated low-degree hardness, and an independent
proof of the classical input theorems. No author-provided code was executed.
The manuscript and audit are AI-assisted and unrefereed; acceptance is not
external human peer review, journal acceptance, or formal certification.

## Edition and verification

The original audit requested no mathematical correction. Public preparation
made only the changes recorded in EDITORIAL_CHANGES.json. All mathematical
sections, qualifications, and the full audit are preserved. The original
audit's metadata and verdict are reproduced byte for byte, including their
historical status fields.

Preparation authenticated the complete audit inventory against its detached
manifest pin and rehashed the retained source captures. Retrieval and visual
inspection histories in SOURCE_METADATA.json describe the audit. Preparation
does not claim a fresh scholarly-source download, new source-text inspection,
new literature search, or a mathematical program run. Integrity checks
establish file identity and edition preservation, not mathematical truth.

## Distribution boundary

Exactly eight authored proof/audit/acceptance/editorial or public-verification
metadata files are included. Source documents, source text extracts, page
images, datasets or catalogue records, executables, raw outputs, and private
coordination material are excluded. Source filenames in SOURCE_METADATA.json
are identifiers for the historically inspected captures; those source files
are not distributed. The written proof needs no omitted executable or data.

This packet does not claim that a branch, pull request, queue update, merge,
release, DOI deposit, or outside communication has occurred. Any queue edit
is a separate publication proposal and must preserve unrelated committed
content. At least one substantive reconstruction is evidenced; the total
historical attempt count is unknown. Editorial preparation adds no proof turn.
