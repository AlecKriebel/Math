# Real ternary zero threshold: a credited prior-result implication

Problem 30002562. Publication edition, 10 October 2026.

Project author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

For every integer k >= 3, the specified threshold satisfies alpha(k) >= k^2 + 1. Here alpha(k) is the least integer A such that every real positive semidefinite homogeneous ternary form of degree 2k with more than A distinct zeros in RP^2 has an indefinite square factor.

The existence input is Theorem 4.5 of Erwan Brugallé, Alex Degtyarev, Ilia Itenberg and Frédéric Mangolte, *Real algebraic curves with large finite number of real points*, European Journal of Mathematics 5 (2019), 686-711, [DOI 10.1007/s40879-019-00324-9](https://doi.org/10.1007/s40879-019-00324-9). This is a credited consequence of prior work, with a complete authored bridge from finite real curves to the threshold. No novelty is claimed.

## Read the result

- [Proof](PROOF.md): exact theorem dependency, real-equation descent, global sign, finite-zero factor exclusion, every residue class and the strict threshold.
- [Mathematical and source audit](AUDIT_REPORT.md): all substantive audit findings, adverse mathematical checks and precise source-inspection limits.
- [Acceptance](ACCEPTANCE.md) and [machine-readable acceptance](ACCEPTANCE.json): accepted assertion, conditions and exclusions.
- [Source metadata](SOURCE_METADATA.json): public citations, PDF hashes and sizes, retrieval/inspection history and the publication record.
- [Verification summary](VERIFICATION_SUMMARY.md): document identity and verification scope.
- [Manifest](MANIFEST.json): exact public membership and hashes of the other seven files.

## Qualifications

Theorem 4.5 and its patchworking foundations are imported mathematics. The complete implication is independently reviewed; the external construction is not independently reconstructed in full. Theorem 4.8's statement also implies the target, but its printed common-edge contact interface remains unreconstructed for k >= 4. The primary Theorem 4.5 route avoids that interface. Both statements belong to one paper, not two independent confirmations.

Theorem 4.5's displayed formula gives 42 at k = 6, while nearby prose mentions 43. Both exceed the required 37; this edition uses the displayed formula and retains the discrepancy. The publisher landing page was inspected for publication metadata; the full version-of-record PDF was not inspected.

The exposition and independent internal AI audit are AI-assisted and unrefereed. Acceptance is not external human peer review, journal acceptance of these documents, or formal proof-assistant certification. This does not compute alpha(k) exactly, establish a general SOS zero maximum, give coefficients in every degree, or reconcile historical exception lists.

Only authored mathematical prose, audit, acceptance and public citation/verification metadata are distributed. Preparing this edition authenticates the accepted documents and recorded metadata without adding a new source-inspection claim.
