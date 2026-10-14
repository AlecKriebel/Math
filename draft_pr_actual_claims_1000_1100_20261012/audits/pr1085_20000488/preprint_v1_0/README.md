# PR #1085: credited Robin half-space note, version 1.0

This edition gives a negative answer to the literal dimension-unrestricted AIM Problem 1.4: a specified nonzero smooth graph in R4 has spectrum [-1,infinity) at attractive Robin strength one. It also proves all-strength binding for connected smooth nontrivial compact half-space perturbations in ambient dimensions two and three, including overhangs and compact boundary components, and weak-strength absence for all compact Lipschitz graphs in dimensions at least four.

The title, paper and metadata credit Exner–Minakov's planar theorem **and** its physical exponential/Stokes normal-defect mechanism. Graph absence and the explicit example also follow from HHRV's published Theorem A.6 through the complete bounded H1/Fourier/compactness bridge in the paper. Frank–Laptev's flat Robin/relativistic duality, standard criticality/capacity and classical Hardy are credited. Exact remaining geometric historical priority, novelty, worldwide open status and independent discovery are UNKNOWN.

The convention is alpha=-beta<0, outward derivative beta u and threshold -beta². The printed HHRV journal formula permits theta=1/4 with denominator (1-2theta)²; its older arXiv v2 uses (1-4theta)² and does not permit that substitution. Magnetic BSZ's positive-field/large-strength model does not apply to zero field. The 2017 Robin passages are expectations, not theorems. There is no claim of all-strength absence for one fixed nonzero graph, a general higher-dimensional nongraph classification, or exclusion of embedded eigenvalues.

The paper is AI-assisted and unrefereed, with no human peer review or formal proof certificate. STATUS.json records readiness and all-issues-clearance false, zero **new** whole-package reviews, and a minimum of two fresh whole-package reviews plus root adoption. Publication services are held behind PR #1032's priority cursor. Dated historical records are not current readiness assertions.

## Portable reproduction

Use Python 3.10 or later; checks and ZIP builder use only its standard library. Extract the support ZIP into a fresh directory and enter it. External upload descriptors are omitted, so the default reports external_deposit_binding_verified=false. All declared payload, copies, mathematical scope and metadata are still verified. There is no nested copy of the ZIP.

    python3 -B verify_package.py
    python3 -B check_math.py
    python3 -B build_archive.py --output /ABSOLUTE/NEW/OUTPUT/pr1085_support_v1_0.zip
    python3 -B verify_package.py

Use an actual nonsymlink output directory: on macOS /tmp is a symlink, so use /private/tmp. The builder requires an output outside the canonical kit. It validates payload and produces a closed sorted deterministic deflate-9 ZIP, with 2026-10-14 00:00:00 timestamps and Unix regular mode0644. Compare the new archive's SHA-256 with the reviewed upload binding in the complete publication kit. Normal and python3 -O -B runs agree; every new guard uses explicit exceptions, not assertions.

The checker verifies selected rational coercivity, Hardy/trace coefficients, normal/Jacobian signs, Fourier-square identities, mass scaling and both margins. It is not a sampled proof of analytic theorems, numerical PDE certificate or cited theorem reproof. The original submitted edition had no executable. Exact historical checker copies retain their original environment assumptions and are **not these portable entry points**. The old Hardy reviewer used assertions and wrote a dated result; no optimized replay of it is claimed.

With Tectonic 0.16.9 or a compatible engine and its standard bundle, run:

    python3 -B build_pdf.py --out-dir /ABSOLUTE/NEW/OUTPUT/pdf

This compiles a disposable source copy with SOURCE_DATE_EPOCH=1791936000 and writes the PDF, source copy, log and receipt only to that output. The installed engine/bundle reproduced the exact canonical PDF. The built-in compiler first returned success, without exporting a PDF. Exact reproducibility across different engines/bundles is not promised. Every final page was rendered and viewed.

All output-writing CLI paths reject direct, resolved, symlink and existing-hardlink aliases to protected inputs **before** any write, directory creation or compiler invocation. Guards cover a supplied external descriptor too. This is a static local-file workflow, without concurrent adversarial filesystem race promises.

## Copies, exclusions and upload forms

PREPARATION_INPUT_PINS.json freezes every pre-authoring audit file. COPY_MAP.json records exact submitted/authored copies in evidence/; EXCLUSIONS.json individually accounts for every other frozen file. Full third-party bodies, derived source extracts/renders, duplicate frozen copies and unrelated repository captures are excluded. Hashes and access facts remain in authored records. Access failures never imply novelty. Historical source locators refer to the original local audit, not a promised distribution member.

SUPPORT_MANIFEST.json pins every allowlisted payload, including PAYLOAD_MEMBERS.txt; its own hash is excluded to avoid self-reference. The external archive hash binds it. Before JSON ingestion every allowlisted path, the bootstrap member list and manifest must be regular with no symlink ancestor. ZIP members, headers and CRC are verified when the archive is present.

The complete local publication kit also has zenodo-deposit.json (the repository tool's exact metadata/files-path schema) and UPLOAD_BINDINGS.json (exact metadata plus attachment filenames, sizes and SHA-256). Both are excluded from the support ZIP to avoid a circular archive hash. The bare .zenodo.json and metadata.json wrapper contain the same metadata. No metadata claims novelty, firstness, independent discovery or human refereeing; its preparation sentence is dated.

In the complete kit:

    python3 -B verify_package.py --require-deposit

A supplied descriptor must bind the actual canonical PDF and ZIP. Absent optional descriptors are reported absent, not verified; dangling/ordinary symlinks and mismatched bindings are rejected. PREPARATION_REPORT.md, FINAL_VERIFICATION.json, OUTPUT_PINS.json, PREPARATION_SEAL.json, render images and scratch are external preparation evidence, outside the archive's self-pinned content. The paper and new authored materials use CC BY4.0; exact historical copies retain provenance.
