# Audited negative answer: equator-averaging inverse Wasserstein bound

Problem 30000999 / OWR-2042-008. Queue accounting: **claimed_solved, 2/5** substantive approaches. The original assertion is negatively resolved by the argument below; this remains AI-assisted, unrefereed work pending human verification. No novelty or historical priority is claimed.

## Result and scope

- For the source-defined dual of normalized equator averaging, antipodal point masses have identical transforms and spherical Wasserstein distance pi. This classical parity obstruction rules out a uniform reverse inequality on all probability measures.
- For every ambient n>=3 and fixed finite p>=1, the reverse inequality also fails for smooth, strictly positive, even densities uniformly bounded above and away from zero. The explicit harmonic family yields input/output distance ratios bounded below by a positive constant times k^((n-2)/(2p)). This is a sufficient divergence rate, not a sharp-rate claim.
- For n=2 the transform is an isometry on even probabilities. No even-density W_infinity result, restricted-support theorem, derivative-bounded-class result, or optimal inverse modulus is claimed.

## Read the work

- [Proof with exact hypotheses](release/PROOF.md)
- [Primary-source and prior-work gate](release/SOURCE_GATE.md)
- [Two-approach research log](release/RESEARCH_LOG.md)
- [Complete independent adversarial AI audit](independent_audit/AUDIT.md)
- [Independent source and duplicate review](independent_audit/SOURCE_REVIEW.md)
- [Machine-readable audit disposition](independent_audit/disposition.json)

The complete independent audit passed without corrections. The parent publication review accepted the full audit and source review. These are AI reviews, not journal peer review or a proof-assistant certificate.

## Integrity and reproducibility

The seven frozen author files and all eight independent-review files are unchanged. Their preserved manifests are [FROZEN_AUTHOR_MANIFEST.json](release/FROZEN_AUTHOR_MANIFEST.json) and [AUDIT_MANIFEST.json](independent_audit/AUDIT_MANIFEST.json). Their SHA-256 digests are respectively:

- 9aad6a1d1eca15937701fcce5969be07ad5a1b901fe3b75bdfb7c1f13744006e
- 7e57703fecf8edef0278f2a014988edde986f96fda71268e6bf1440e1e0f9cc8

Both portable standard-library scripts were rerun from the publication layout and reproduced their recorded outputs byte-for-byte: 591 author controls and 3,812 independent controls. Finite controls support transcription and algebra; the continuous transport and asymptotic arguments are audited in full prose.

From this directory:

    python3 release/check_exact.py
    python3 independent_audit/independent_exact.py

PUBLICATION_MANIFEST.json binds the complete public payload except itself. The only existing repository file changed is this problem's QUEUE.md row: status, approach count, and previously blank Findings. All other queue bytes, including its pre-existing header and links, are preserved.

The source_checks.json artifact contains only sanitized bibliographic metadata and bounded public search scope. No source PDF, page image, full source extraction, corpus dump, credential or private conversation is included. This publication adds a draft PR only; it does not merge, deposit a paper, create a DOI, or claim first discovery.
