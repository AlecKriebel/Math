# Independent release acceptance: fixed-camera curve checkpoint

Review date: 2026-10-16. Catalogue ID 20000188; queue row 1792.

## Decision

**ACCEPTED FOR RELEASE PACKAGING. No release blockers found.**

This acceptance binds exactly the 25-file public package whose `MANIFEST.json` SHA-256 is `ca6901fad6b47c6d36c359855346306b4bb3e08f15ce2876b0c6ed54e5135db0` (205,331 total bytes, including the manifest). The accompanying 61,708-byte archive has SHA-256 `c261361e39167f367c84e60fd2cd7115191b3c613f47373bdc8d73ab17200b82`; its 25 regular file members reproduce the public package exactly.

This is a release, preservation, and reproducibility review. It is not a new mathematical research pass or a second proof of the theorem. Mathematical acceptance remains the previously completed independent audit, bound by acceptance-manifest SHA-256 `713520104c62adf26b0a6437b1ce1f2a1540e1489d4ec71b8eb15c9f0564a3af`.

## Accepted mathematical scope is preserved

The disposition remains **scoped_resolved1/5**. The contract concerns complex projective space, two fixed rank-three pinhole cameras with distinct centers, and reduced integral closed projective image and world curves. Both rational camera maps must be generically defined on the world curve, with the prescribed image closures. Singular images, epipoles, epipolar lines, centers, and baseline incidence are included as specified by the contract.

The release consistently preserves the accepted existence/degree classification and embedded-smoothness criteria, including the exceptional common-plane family, center multiplicities, and baseline scheme coefficients. It makes no novelty claim or claim to resolve every interpretation of AIM Reconstruction Problem 1.4. Unknown cameras, other camera models, real visibility, positive characteristic, and nonintegral-input conventions remain excluded.

The geometric statements hold over C. Terminating exact execution requires effective coefficient presentation and certified absolute decomposition. Only the finite fixture suite and monomial checker are implemented. No general-purpose reconstruction or arbitrary-input decomposition, normalization, or smoothness solver is represented as implemented.

## Preservation and public-edition review

- All 13 accepted artifacts match their original acceptance hashes and byte counts.
- Seven public artifacts are byte-identical to their accepted versions, including both checker scripts and their frozen outputs.
- Six public artifacts differ only by the disclosed presentation edits. Each exact transformation was independently reconstructed and compared byte for byte: administrative omissions, portable reproduction paths, completed-audit cross-references, and scope/implementation clarifications already supported by the accepted audit.
- No mathematical argument, formula, hypothesis, or proof obligation was removed or substantively altered by those edits.
- Public acceptance scope, decision, implementation boundaries, novelty limits, and unresolved-obligation fields agree with the original mathematical acceptance. All public artifact bindings match the actual public files.
- The package and all 19 sealed source files remained unchanged throughout this review.

## Independent reproduction and rejection tests

Two separate fresh-directory replays passed: one from a directory copy and one reconstructed from the verified archive. Each ran all 13 exact fixture groups and all 430 monomial tuples for degrees 1 through 12, reproducing both frozen JSON outputs byte for byte. The replayed package copies were unchanged afterward.

All 35 disclosed negative controls were independently recreated and rejected with exit code 1. Normal-mode rejections checked the intended integrity failures. Under `-O` and `-OO`, the verifier explicitly refuses before integrity processing or fixture execution because the unchanged fixture programs use assertions. These optimized runs establish fail-closed refusal, not execution of each downstream integrity gate under optimization. The verifier itself has no assert-based gates; its validation uses explicit exceptions.

Additional checks rejected `PYTHONOPTIMIZE=1`, `PYTHONOPTIMIZE=2`, and a coordinated document-plus-manifest replacement when supplied the trusted manifest digest. An external trusted digest is necessary to authenticate the frozen edition against coordinated replacement. The supported verification command is:

    python verify_package.py --manifest-sha256 ca6901fad6b47c6d36c359855346306b4bb3e08f15ce2876b0c6ed54e5135db0

The verifier copies the scripts to a temporary directory and compares generated output bytes with frozen bytes held in memory. Passing these finite computations does not establish mathematical generality; that rests on the preserved written proofs and prior independent mathematical acceptance.

## Content and provenance boundary

The released inventory contains only UTF-8 authored reports, Python checkers, requirements, and JSON verification metadata. No copied source PDF, extracted third-party body, dataset record/content, private source, private coordination material, or private personal data is included. Public scholarly names, titles, and URLs are bibliographic metadata.

The three source-metadata files are exact copies of their preparation records. Five retained source files independently match their reported hashes and byte counts. A normalized contiguous-text screen against 12 retained source-text/record files found no matching 18-token window. That screen supplements the inventory/content inspection and is not an exhaustive originality certificate.

Historical inspection limits are accurately retained: the later Agarwal–Pryhuber–Thomas retrieval is distinguished from preparation history; Ballico remains a publisher search-index check; successful retrieval is not presented as a full proof audit; dataset bindings are historical rather than a fresh latest-upstream download. No new literature-status or novelty certification is made by this review.

All 18 Markdown relative links resolve within the disclosed package.

## Queue boundary

The proposed queue file and patch were independently checked against the disclosed base, including its Git blob SHA `3bad7c6098ceed14505338d8f5ceba882eeaa1d8`. Applying the patch reproduces the proposed bytes exactly. Only queue row 1792 changes, and only its Status, Turns, and Findings cells. The resulting values are `scoped_resolved` and `1/5`, with findings that retain the exact scope, novelty, effectivity, and implementation limits. All unrelated bytes, including existing notes and links, remain identical.

The queue proposal is accepted against its recorded base only. Any later publication must preserve intervening unrelated remote changes. This review performed no publication or repository mutation.

## Evidence and placement

The accompanying public-safe evidence consists of `INDEPENDENT_RELEASE_CHECKS.json`, `INDEPENDENT_REPLAYS.json`, `INDEPENDENT_NEGATIVE_CONTROLS.json`, and `CONTENT_AND_SOURCE_METADATA_REVIEW.json`.

This review is separate from the frozen package. Adding it inside that package would change the exact inventory and invalidate the reviewed manifest binding; keep it as a sibling release-review artifact or obtain a fresh package review after any package change.
