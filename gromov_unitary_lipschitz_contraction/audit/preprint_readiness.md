# Preprint readiness — version 1.1

**Verdict:** ready for submission as an unrefereed preprint after two fresh sequential adversarial reviews. No unresolved actionable issue was identified. This is an internal AI-assisted assessment, not external peer review, formal proof certification, or a guarantee of first priority.

## Review sequence

1. [Round 1](preprint_round1.md) independently examined the proof before earlier reviews. It found no mathematical or framing defect and suggested three optional improvements.
2. All three were adopted: the angle derivative variable is explicit, the paper links to its companion materials, and the PDF contains title/author/subject metadata. [Revision response](preprint_revision_response.md).
3. [Round 2](preprint_round2.md), by a new reviewer, checked the revised manuscript through spectral functional calculus and tangent geometry before consulting previous reports. It found **no actionable issue at any severity**.

The theorem, assumptions, Lipschitz coefficient, proof inferences, and verification algorithms are unchanged from version 1.0. No journal submission was prepared.

## Frozen mathematical artifacts reviewed in round 2

- `paper/main.tex`: `954d45001560d29f3286383a40ff9c477a257d9359e02ada7477eac67a0cda4e`
- `paper/main.pdf`: `3e8c052065110ec412a3e01e80f0c789f663ce6a9eb74c31aa8fdd99915fc02b`

These same artifacts are used in the version-1.1 packages and the public site. Adding this review receipt and the round-2 report does not change the paper.

## Release checks

The four-page PDF was rebuilt and every page visually inspected. There are no TeX warnings or missing references. Embedded metadata and the companion link were checked. Both reviewers replayed the 10 exact and 7,679 numerical diagnostics successfully; the diagnostics remain supplementary to the analytic proof.

The release archives have SHA-256 manifests, all local public copies match their sources, and rebuilding from a clean extraction reproduces both archives byte for byte. The final archive includes the two new review reports and this readiness record. The repository research log separately records publication checks.
