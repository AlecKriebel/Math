# Prime ideals and coordinate-ring maps: audited counterexample

Problem **30001478 / OWR-4335-003**, rank 827. Queue status: **claimed_solved, 1/5 author turns**. Two independent mathematical reviews accept a complete counterexample to both literal assertions; no proof correction is required. The result remains unrefereed, with no novelty or priority claim.

## Result and mandatory scope

For the displayed six-relation algebra R(alpha,beta), the homogeneous two-sided ideal I=(x3-x1,x4-x2) satisfies 0 != I < R+ and is completely prime. Its quotient is B(P1,O(1),sigma), where sigma([s:t])=[s+beta*t:beta*s+t]. The quotient map is graded, unital, surjective and has infinite-dimensional image of GK-dimension 2.

The direct-presentation proof works over every field, for arbitrary alpha and beta squared unequal to 1, including the algebraically independent parameters of the question. **Read [the characteristic-scope addendum](first_audit/scope_addendum.md):** identification with the 2012 journal parameter family uses its fractional change only in characteristic different from 2. The characteristic-2 result concerns the directly presented algebra, not the collapsing journal parametrization.

This does not give a common graded quotient ring, a birational map, or a surface-dimensional image. The optional surface-target embedding in the second review is not needed for either literal counterexample.

## Proof, independent reviews, and history

- [Unchanged authored proof](author/proof.md)
- [First independent mathematical audit](first_audit/mathematical_audit.md) and [required scope addendum](first_audit/scope_addendum.md)
- [Second adversarial review](second_review/second_review.md)
- [Immutable archives and publication scope](PUBLICATION_METADATA.json)
- [Fresh source/corpus identity checks](SOURCE_CORPUS_CHECKS.json)

All three ZIPs in archives/ and all their extracted members are preserved byte-for-byte. Historical pending-review and no-publication statements inside them describe those earlier stages. The author confirmed one substantive linear-quotient approach; the refined projective-line quotient belongs to that route. Independent verification adds no author turns.

## Operative verification

Use the publication wrapper, not a frozen verifier as the first entrypoint. Obtain the expected wrapper and manifest SHA-256 pins from the draft PR's acceptance receipt. Verify the wrapper's own hash with a trusted local hash utility before executing it, then run from an ordinary, nonsymlinked extraction:

    python3 -I -B verify_publication.py --expected-manifest EXPECTED_SHA256
    python3 -I -B -O verify_publication.py --expected-manifest EXPECTED_SHA256

The wrapper rejects symlinked invocation ancestry and any nonregular or unexpected entry. It checks the externally supplied manifest pin, all publication hashes, fixed archive hashes, exact ZIP inventories and every extracted member before launching any frozen executable. Full runs replay all three gates and their 47, 16 and 20 named-control suites. The separate wrapper suite checks relocation, entrypoint/root/ancestor symlinks, other malformed inventory, wrong pins, archive corruption and source-metadata mutations.

The original author and first-audit verifiers resolve their own pathname. A self-symlink can therefore select another genuine tree; this narrow caveat remains documented rather than silently rewriting their freezes. The operative wrapper closes that invocation-path bypass for this publication. [The two-line patch](second_review/verifier_path_hardening.patch) is also applied with the actual patch command to a disposable first-audit extraction by test_path_patch.py; manifests are rebuilt inner-first, and normal/-O baselines and self-symlink rejection are replayed. Only code and results of that test are published. A future patched derivative would require new provenance, hashes and an audit gate before release.

These checks are ordinary local integrity and mathematical replay checks, not a sandbox against concurrent malicious filesystem changes. Finite computations do not replace the universal proof.

## Public sources and limits

- S. J. Sierra, joint with D. Rogalski, *Birationally commutative projective surfaces of GK-dimension 4*, Oberwolfach Report 22/2010, pp.1361-1362: [official report](https://ems.press/content/serial-article-files/46279).
- D. Rogalski and S. J. Sierra, *Some projective surfaces of GK-dimension 4*, Compositio Mathematica 148 (2012), 1195-1237, pp.1198 and1202: [published article](https://doi.org/10.1112/S0010437X12000188).

The archive contains authored proof, audits, verification code/results and public metadata only. No third-party PDFs, source-text extracts, dataset contents, private sources, personal data or private coordination files are included. Source inspections and bounded literature checks are documented in the immutable reviews; they do not establish novelty or exhaustive current literature status.
