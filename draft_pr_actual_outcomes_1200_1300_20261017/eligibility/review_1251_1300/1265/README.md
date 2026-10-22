# Finite-force equilibrium rigidity on the line

Problem AMR-099-0003 / 10000003. Public proof and AI-assisted audit, 11 October 2026.

## Result and attribution

For `1 < s <= (3+sqrt(5))/2`, a set of at least two distinct particles on the real line is a positive-spacing bi-infinite arithmetic progression if each one-sided inverse-power force is finite and the two one-sided forces are equal at every particle. Local finiteness follows from these assumptions. An affine formula for particle labels requires strictly increasing enumeration.

The prior range `1 < s <= 2`, including inverse-square repulsion, is due to Alper Ferudun, [*Equilibria of Inverse-Square Repulsion on the Line Are Arithmetic Progressions*, arXiv:2610.06944v1](https://arxiv.org/abs/2610.06944v1), Theorem 1.2. The additional range `2 < s <= (3+sqrt(5))/2` is the deduction checked here: finite force yields a little-o point count, and power concavity makes the spatial-cutoff energy vanish, including the upper endpoint. The network and cutoff mechanism is credited to Ferudun. This packet makes no literature-priority claim for the extension.

The standalone theorem explicitly excludes singleton configurations, which have zero finite forces but are not positive-spacing bi-infinite lattices. The complete proof and audit retain this scope correction.

## Reading order

- [Corrected standalone proof](CORRECTED_EXPONENT_EXTENSION.md): the full theorem, network construction, recurrence argument, energy estimates, endpoint deduction, lower range, and limitations.
- [Independent AI-assisted audit](AUDIT.md): separate examination of the prior theorem and extension, including infinite tails, finite row normalization, small gaps, and the endpoint.
- [Acceptance report](ACCEPTANCE.json): separate verdicts bound to exact source, proof, and audit hashes.
- [Source verification](SOURCE_VERIFICATION.json): public titles, URLs, versions, byte counts, SHA-256 hashes, retrieval history, inspection scope, and access limits.
- [Editorial map](EDITORIAL_MAP.json): exact byte ranges and hashes for the editorial export; all mathematical sections are byte-identical to their reviewed versions.
- [Research log](RESEARCH_LOG.md): dated results and scope of completion.
- [Public manifest](PUBLIC_MANIFEST.json): exact membership and hashes of the public files.

## Review status and limits

The source author's [public record](https://eulersolve.org/papers/amr-099-0003/) describes the manuscript as an unrefereed, AI-assisted preprint. This exposition, extension, and independent review are also AI-assisted. Here “independent” describes a separate check of the mathematical argument; it does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

No result is asserted for principal-value cancellation of infinite one-sided forces, arbitrary labels, every decreasing force law, or exponents greater than `(3+sqrt(5))/2`. The failure of the stated estimate beyond that exponent is not a counterexample to rigidity there. No global literature-priority search is certified.

This packet contains authored proof and audit material plus public verification metadata. Source documents, source text, datasets, diagnostic programs, and raw computational checks are not included. The mathematical proof, rather than finite diagnostics, supports the universal claim.
