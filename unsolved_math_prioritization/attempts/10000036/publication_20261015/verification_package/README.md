# Finite-energy lattice percolation with internal critical probability one

Alec Kriebel, independent researcher. ORCID 0009-0001-9320-500X. Version 1.0.0, October 15, 2026. Five-page unrefereed research note, extensively AI-assisted. No completed external human peer review or formal proof-assistant verification is claimed.

For each d>=2 the note constructs a full-automorphism-invariant, translation-mixing ordinary finite-energy bond law on nearest-neighbor Z^d with a unique infinite component and quenched internal bond/site thresholds one. It answers the historical BHS ordinary-energy question. It develops the summable finite-past mechanism of Haggstrom and Mester; the exact planar midpoint projection of their published model also gives the threshold-one conclusion by the supplied bounded-cutset deduction. No first-priority or certified-novelty claim is made. Read CURRENT_PRIORITY.md for the exact credit, chronology and literature limits. A uniform energy bound, or failure of all such marginal bounds, is not proved or asserted.

## Contents and evidence limits

The archive includes note.pdf and editable note.tex, exact deposit metadata, this guide, the portable verifier and deterministic builder, all 27 original files in source/ including three original evidence archives with 15 members, six independent analytical/priority families, and dated parent evidence. Downloaded publications, source extracts, rendered pages, raw imported corpora, credentials and private service state are excluded. Source/version locators and byte hashes identify inspected material.

This theorem is proved analytically. There is no computational infinite-volume proof checker, simulation, or formal certificate. Automated checks authenticate the closed package inventory and replay original source/archive relationships, with 11 parser/path rejection controls. They cannot certify the theorem, source interpretation, or priority. Those require independent reading of the note and recorded analytical reports. Dated root_evidence/ files may need the canonical audit context if executed individually; the promised complete portable entrypoint is verify_package.py.

## Trusted startup and portable verification

Obtain the index and startup-verifier SHA-256 pins from the final external acceptance receipt, independently of the downloaded archive:

https://github.com/AlecKriebel/Math/blob/main/draft_pr_claimed_solved_800_900_20261012/audits/pr838_10000036/FINAL_PREPRINT_ACCEPTANCE.json

Verify the archive inventory and verifier bytes before executing any downloaded program. The current verifier SHA-256 is 7e11f1eca98205e898a69047541b60ccefdf56f8cfa5cdcfcdf7b7d623547050. An executable cannot authenticate arbitrary replacement startup code by hashing itself. The final acceptance receipt is outside the archive to avoid a circular digest.

From the intact extracted archive root, substitute the externally trusted index digest for PIN:

    python3 -I -S -B verify_package.py PIN --full
    python3 -I -S -B -O verify_package.py PIN --full

Python 3.10+ standard library is sufficient. The verifier binds a closed regular-file inventory to the external index pin before and after the full replay. It copies 27 original files and the recorded integrity checker into a disposable directory, verifies all 3 archives/15 members and unpacked-copy/acceptance bindings, and checks the11 explicit rejection controls. It executes no original archive member. Both normal and optimized modes genuinely perform these checks. Package inputs remain unchanged.

## Rebuild the same archive

Use a new or empty output directory outside the intact input package:

    python3 -I -S -B build_verification.py --from-package . --trusted-index-sha256 PIN --output-root /absolute/new-output

In the assembled repository preprint folder, use --from-package ../verification_package instead. The builder checks that the input index is regular before reading it, binds the external index and verifier bytes before execution, and reproduces package_index.json and verification.zip byte for byte. Its default development assembly mode requires the canonical shard audit layout. LaTeX compilation is optional; regenerated PDF timestamps may change its bytes. The accepted PDF is included.

## Publication kit

The canonical repository preprint/zenodo-deposit.json has metadata identical to metadata.json. Its only upload files are output/pdf/note.pdf as finite-energy-percolation-note.pdf and verification.zip as finite-energy-percolation-verification.zip. The repository's Zenodo tool checks, stages, inspects and publishes those exact files and metadata only after final independent package acceptance. The package itself does not create deposits or update the tracker. Final reviews, external acceptance and publication receipts remain in the repository.

CC BY 4.0 applies to the authored note and supporting authored package. Cited publications retain their own terms and are not redistributed.
