# Homometric flowers: an accepted partial result

Problem 30002326 / OWR-12481-016. Research-note publication edition, 10 October 2026.

Project author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

For every integer n >= 20736, the note constructs a connected n-vertex flower G_n and proves

h(G_n) = floor((n - floor(log_2(log_12 n)) + 3)/4).

The entire flower family has asymptotic minimum h(G)/|V(G)| equal to 1/4, including arbitrary cores and tail proportions. The global question whether h(n)/n tends to zero is not resolved. No novelty or exhaustive current-status claim is made.

The convention is explicitly the minimum over connected n-vertex graphs of the maximum common size of disjoint ambient-distance-homometric sets. Equivalence with a universal exact-size convention is not assumed. The cone lemma requires k >= 2; localization requires pair size at least four, with the sharp smaller-size exception retained. The revised Axenovich–Özkahya paper already states the correct threshold.

## Read the result

- [Mathematical report](MATHEMATICAL_REPORT.md): full construction, proofs, exact integer rounding, the uniform flower obstruction, necessary structural conditions, convention caution and prior credit.
- [Independent mathematical audit](MATHEMATICAL_AUDIT.md): complete substantive proof audit, boundary cases, external theorem dependence and finite diagnostic summary.
- [Acceptance report](ACCEPTANCE.md) and [machine-readable acceptance](ACCEPTANCE.json): precise accepted scope and exclusions.
- [Source metadata](SOURCE_METADATA.json): public bibliographic links, source versions, PDF byte counts and hashes, retrieval and inspection limits.
- [Verification summary](VERIFICATION_SUMMARY.md): original/distributed document identities and what the diagnostics establish.
- [Manifest](MANIFEST.json): exact public membership and the other files' SHA-256 identities.

## Review, dependence and provenance

This is an AI-assisted note accompanied by an independent internal AI mathematical and source-credit audit. The authored note and audit are unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification is claimed. Acceptance refers only to the stated partial-result scope.

The graph-uniform theorem of Bollobás–Kittipassorn–Narayanan–Scott is a published external dependency for the flower obstruction and two-distance restrictions, not independently reproved here. The construction extends the Axenovich–Özkahya mechanism, with original credits preserved throughout.

The original manuscript was recovered with exactly its recorded 16,408 bytes and SHA-256. The original full working bundle and complete historical verification record were not restored. A separate independent audit records recovered public-source identities and fresh diagnostics. This edition preserves the full mathematical report and substantive audit; its preparation adds no fresh retrieval, inspection or mathematical-replay claim.

This prose edition contains authored mathematics, audit, acceptance and public citation/verification metadata. Programs, generated certificates, raw computational outputs, copied source documents/text/images, datasets and private coordination are excluded. The finite diagnostics are supplementary; the all-order arguments are contained in the report and audit together with their expressly cited published dependency.
