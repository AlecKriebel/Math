## Result and exact scope

Problem AMR-099-0003 / 10000003: for `1 < s <= (3+sqrt(5))/2`, a set of at least two distinct points on the real line is a positive-spacing bi-infinite arithmetic progression when each one-sided inverse-power force is finite and the two sides are equal at every point. Local finiteness follows from these assumptions. The indexed affine conclusion requires strictly increasing enumeration.

The at-least-two-points condition is essential: a singleton has zero finite forces and is not a positive-spacing bi-infinite lattice. The corrected standalone proof makes that exclusion explicit.

## Prior work and audited extension

Alper Ferudun's 2026 [*Equilibria of Inverse-Square Repulsion on the Line Are Arithmetic Progressions*, arXiv:2610.06944v1](https://arxiv.org/abs/2610.06944v1), Theorem 1.2, proves the prior range `1 < s <= 2`, including inverse-square repulsion. The author's [public manuscript record](https://eulersolve.org/papers/amr-099-0003/) describes it as an unrefereed, AI-assisted preprint.

The additional range `2 < s <= (3+sqrt(5))/2` is the deduction audited here, using Ferudun's network/cutoff mechanism, a little-o point count from finite force, and power concavity. The upper endpoint is included. The prior theorem and the extension receive separate, hash-bound verdicts in [ACCEPTANCE.json](https://github.com/AlecKriebel/Math/blob/b1f0bc241aa84d7bef150b77a50c986889970240/unsolved_math_prioritization/attempts/10000003/ACCEPTANCE.json).

[Complete corrected proof](https://github.com/AlecKriebel/Math/blob/b1f0bc241aa84d7bef150b77a50c986889970240/unsolved_math_prioritization/attempts/10000003/CORRECTED_EXPONENT_EXTENSION.md) · [Full independent AI-assisted audit](https://github.com/AlecKriebel/Math/blob/b1f0bc241aa84d7bef150b77a50c986889970240/unsolved_math_prioritization/attempts/10000003/AUDIT.md) · [Reading guide](https://github.com/AlecKriebel/Math/blob/b1f0bc241aa84d7bef150b77a50c986889970240/unsolved_math_prioritization/attempts/10000003/README.md)

The exposition, extension and independent audit are AI-assisted. External human peer review, journal acceptance, formal proof-assistant certification, novelty and literature priority are not established. No claim is made for principal-value cancellation of infinite one-sided forces, arbitrary labels, every decreasing force law, or exponents above the stated endpoint.

## Publication verification and boundary

Exactly eight authored proof/audit/acceptance and public-verification files, totaling 56,524 bytes, are added under `unsolved_math_prioritization/attempts/10000003/`. The mathematical sections are byte-identical to their reviewed versions, with the nonmathematical editorial export specified in EDITORIAL_MAP.json.

The sealed local packet validator passed. All eight remote blob contents and their exact membership were read back and matched before branch publication. The Git root tree is `a496294abe639e5e5f8c7e82d92945e8e3b0724f`; the target subtree is `9f6ae0fa5f7dd0bbf305a01f52462a85fce0d03f`. All sibling trees and the complete existing QUEUE.md blob remain unchanged.

No copied third-party source documents or source text, datasets, diagnostic code, raw computations, private sources, private personal data or private coordination files are included. Source titles, public URLs, PDF identities and inspection history are metadata only. Integrity checks verify packaging; the written proof and mathematical audit support the theorem.

## Exact public file identities

- `ACCEPTANCE.json`: 3,698 bytes; SHA-256 `cba4c33edd72f5544922981939c067434bf33f9a4f8b6d5defa5a7b1d3dd3e82`
- `AUDIT.md`: 11,942 bytes; SHA-256 `01a5e14e829186d7138cb2861f3f25f7c4d12c28e858b7257b69e993618080c5`
- `CORRECTED_EXPONENT_EXTENSION.md`: 13,892 bytes; SHA-256 `daf367025ba74a48b1e623047ffc67eb571cf4ac5c0d62d28f2cf45173f17d48`
- `EDITORIAL_MAP.json`: 10,547 bytes; SHA-256 `8332b358c9bfbbc774a64dcef6fe72041cc97e2792c02ce2bb39c5afd5865866`
- `PUBLIC_MANIFEST.json`: 1,686 bytes; SHA-256 `8e1936ec428c3f2457b52efee3aeeba1c80ca1ba6443b58e80963bf3df3b9b13`
- `README.md`: 3,381 bytes; SHA-256 `8a85c95b5e43bf3059b0bd3fb4de061c6164a5ff1481f38df4e504ca934b7029`
- `RESEARCH_LOG.md`: 1,339 bytes; SHA-256 `488d84ee6994e5c3404d5cc0c8e9ba8e9a143efb416e1139381cf26a22217559`
- `SOURCE_VERIFICATION.json`: 10,039 bytes; SHA-256 `c332c21ea593ddfbdba150b02bcd32b00b124bd7aee1b878139431a6e62e3160`

PUBLIC_MANIFEST.json lists exact membership and hashes the other seven files; its own identity is pinned above.

Draft for review. No merge, release or outreach is requested.
