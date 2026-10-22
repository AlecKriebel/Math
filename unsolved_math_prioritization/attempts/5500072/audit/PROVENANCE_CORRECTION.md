# Audit provenance correction

## Corrected statement

This audit was performed by an independent AI assistant, supplemented by separately authored exact-arithmetic and adversarial artifact checks. It was not performed by a human reviewer. It is not human peer review or formal verification.

## Error and scope

The superseded audit's exact acceptance falsely described its proof review as human review. The replay script and its generated results repeated that attribution in their scope field. These statements were incorrect.

The updated packet corrects those fields, makes the reviewer type explicit in the written audit and README, and clarifies an ambiguous reference to manual inspection. The changes are limited to review provenance and descriptions of that correction. The authored mathematical findings, accepted model, unresolved status, three-approach count, exact arithmetic, source pins, and unchanged author artifacts remain the same.

`provenance_correction.patch` is the actual unified patch for the five changed existing audit members. It includes removed erroneous wording only as the historical deletion side of the correction. Applying the patch to the superseded five files reproduces the updated files exactly. This correction note is an added file.

## Superseded objects

The superseded audit and its companions are preserved privately and are not redistributed in the updated packet:

- ZIP: 37,523 bytes; SHA-256 `87d418f18f2947615b0845e39c442cf993848cac1c638a7c062360c53e3fbe97`
- External manifest: 2,441 bytes; SHA-256 `a13d19c5bb1f15760eebbbaae0776764c09f661a769e7c9d92abfcbed7e6be53`
- Bootstrap: 2,925 bytes; SHA-256 `928887363b085449cf701cdac8e834a2322a9e19c5ba25fae0aaca2ad83f7097`
- Receipt: 3,517 bytes; SHA-256 `331fab6bea45189eff50a2e6b15be76dd2ce37a744bb46ba8d0adab4bde70df0`

These are historical integrity references, not accepted publication candidates. The updated archive is separately pinned by its new external manifest and receipt.

## Unchanged exact acceptance target

The accepted author ZIP remains 14,851 bytes with SHA-256 `da58c09682631f3455d7ef0047ff20b137f2c8b14640752f9886bb4dfc4bfb62`. Its external manifest remains 1,680 bytes with SHA-256 `88771594f5b6c2aabe33513345ca2b70786984448cfa17d5ed7bbc5ffe122f95`.

Acceptance remains: bounded partial, unresolved 3/5, no global resolution and no novelty claim. No author mathematical edit was necessary or performed. The acceptance is an independent AI audit decision with the limitations stated above.
