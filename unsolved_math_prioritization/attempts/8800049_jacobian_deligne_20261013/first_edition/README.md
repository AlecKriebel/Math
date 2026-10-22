# Detecting Jacobians through a counted Deligne model connection

First mathematical edition, 13 October 2026. Problem 8800049 / AMR-087-0049.

This edition proves an exact, terminating, all-characteristic decision procedure for Jacobian existence in a promised ordinary, absolutely simple abelian-threefold isogeny class over a finite field. The accepted result is an **aggregate connection**: an exact polarized Deligne count certifies that a separately enumerated set of geometric models is complete, and each model is then tested by Beauville–Ritzenthaler recognition.

The full argument is in [the integrated proof](INTEGRATED_PROOF.md). The [independent acceptance](FINAL_ACCEPTANCE.md) accepts that precise theorem relative to its credited established dependencies. The broader historical direction, including a useful direct criterion from a specified polarized ideal, remains unresolved here. This first edition records **one newly documented substantive pass**; the lifetime number of attempts is unknown.

## The mathematical result

Given an explicitly represented finite field Fq and a promised realizable ordinary absolutely simple degree-six Weil polynomial h, the procedure:

1. Computes the exact unweighted number N of principally polarized Fq-isomorphism classes, including noninvertible Deligne ideal classes and every principal-polarization orbit.
2. Enumerates certified theta-equipped projective models, filters by the exact Frobenius polynomial, and removes polarized duplicates until exactly N classes remain.
3. Applies exact geometric recognition to each model. Smooth theta intersections over odd-degree extensions, invariant differentials, and a finite rational-line test preserve the base-field descent decision in every characteristic.
4. Returns YES precisely when at least one model is a genus-three Jacobian over Fq, and otherwise returns NO.

The output model list is unlabeled by individual ideals. The manuscript proves why every search terminates; it gives no useful complexity bound. An implementation, practical performance, a marked-ideal inverse, worldwide novelty, and completion of the broader historical research program are not claimed.

## Reading guide

- [Integrated proof](INTEGRATED_PROOF.md): complete theorem, arithmetic count, exact model interface, all-characteristic recognition, composition, and verification limits.
- [Source target and dependencies](SOURCE_TARGET_AND_DEPENDENCIES.md): exact comparison with Howe's 2006 question and the role of each established theorem.
- [Exact count dependency audit](EXACT_COUNT_DEPENDENCY_AUDIT.md): arbitrary-order ideal enumeration, the scalar ideal-equality guard, and unconditional unit/class-group computation. The guard is not a claim that a published algorithm is erroneous.
- [Independent acceptance](FINAL_ACCEPTANCE.md): accepted identities, decisive checks, and limits of the review.
- [Public source provenance](PUBLIC_SOURCE_PROVENANCE.md) and [source metadata](PUBLIC_SOURCE_METADATA.json): scholarly references, versions, PDF byte identities, and bounded inspection scopes.
- [Count-source verification](SOURCE_VERIFICATION.json): the count audit's exact source identity and inspection record.
- [Public manifest](PUBLIC_MANIFEST.json): byte counts and SHA256 identities of this edition's other public files.

## Evidence boundary

The reported 71,472-form scalar/point-count checks and independent 622-form Clifford/line/scalar checks concern finite-field quadratic-form arithmetic only. The second collection includes a 78-form sample over F8. These are not end-to-end runs of the count-to-model search, theta intersections, or differential construction. The general result rests on the proof and its established dependencies.

The edition contains authored mathematics, acceptance, and public-source verification metadata. Source PDFs, extracted source text, datasets, programs, and private coordination material are not part of the edition. Hashes establish byte identity, not mathematical truth. The bounded literature inspection does not certify worldwide originality or current worldwide openness.
