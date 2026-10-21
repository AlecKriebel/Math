# Dimension three Klein sail face frequency finiteness

Problem 1900017, Karpenkov Problem 17, dimension-three case. Prepared 11 October 2026.

This packet contains a completed, AI-assisted reconstruction of the proof that the sum of origin-sensitive geometric relative face frequencies is finite in ambient dimension three. The reconstruction repairs specific intermediate steps of Aggarwal and Andritsch's *Generalised Gauss–Kuzmin Distribution for Klein sails in R³*, arXiv:2608.05853v1. Their Theorem 1.9 already states the target finiteness result. No novelty or result in dimensions four and higher is claimed.

## What is accepted

The geometric reduction and the summable planar upper estimate have both been reconstructed. The cross-section/Haar identification is established in the accompanying reduction audit. The established specialized import is G. K. White's 1964 Theorem 2: its original publisher statement and hypotheses were checked, but its full proof was not independently re-proved. Standard Haar measure, the finite invariant volume of the unimodular planar lattice space, and Tonelli's theorem are also used explicitly. No unresolved specialized intermediate lemma remains in this reconstructed target proof.

The source is a 50-page preprint submitted 6 August 2026; the inspected version-pinned arXiv record showed v1 and no journal reference. The entire manuscript and the original printed proof are not certified verbatim. Lower bounds, all-lattice pointwise statements, generic ergodic and periodic-sail conclusions remain outside the accepted scope. This review is AI-assisted, without independent human referee review or proof-assistant formal verification.

## Full mathematical reports

- [AUDIT.md](AUDIT.md): target, result, repairs and exact disposition.
- [REDUCTION_AUDIT.md](REDUCTION_AUDIT.md): full origin-sensitive geometric reduction, face-adapted chart, local first-contact flow boxes, group/Haar identification and bounded multiplicity.
- [MEASURE_AUDIT.md](MEASURE_AUDIT.md): full reduced-basis and witness construction, checked White application, support cuts, radial integral and summable upper estimate, with the full defect ledger.
- [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): accepted dependency chain and limitations.
- [ACCEPTANCE_SCOPE.json](ACCEPTANCE_SCOPE.json): exact accepted-original and public-report byte/hash bindings.

The reports are complete. Editorial changes only resolve companion-report scope and public-relative references, remove local operational references, and identify review provenance. [EDITORIAL_PROVENANCE.json](EDITORIAL_PROVENANCE.json) records every change and hashes the unchanged protected mathematical regions.

## Quantitative conclusion

With compatible fixed Haar normalization and for almost every unimodular planar lattice L, the radial translation-area integrals satisfy

    I_1(L) <= 3 sqrt(3),
    I_k(L) <= 1080 sqrt(3) H_(k-1) / [k(k-1)]  for k >= 2.

Tonelli and the telescoping identity give

    sum_(k>=2) H_(k-1) / [k(k-1)] = zeta(2),

so the total affine-lattice measure is at most 3 sqrt(3) + 1080 sqrt(3) zeta(2), up to the stated fixed Haar normalization. The geometric comparison has a face-independent normalization factor B and multiplicity at most six:

    sum_[f] rel([f]) <= 6 B mu_C(C) < infinity.

No canonical absolute numeric normalization for the original Möbius frequency measure is asserted.

## Sources and integrity

[PUBLIC_SOURCE_METADATA.json](PUBLIC_SOURCE_METADATA.json) records primary-source titles, versioned public URLs, PDF sizes and hashes, and retrieval/inspection scope. [VERIFICATION_METADATA.json](VERIFICATION_METADATA.json) records aggregate checks. [MANIFEST.json](MANIFEST.json) gives the exact public file inventory and SHA-256 hashes; it excludes itself to avoid a circular hash.

No third-party source PDF, source-text extraction, rendering, dataset content, verification script or private coordination material is included. Finite computational checks support error detection; the universal mathematical arguments are in the full reports.
