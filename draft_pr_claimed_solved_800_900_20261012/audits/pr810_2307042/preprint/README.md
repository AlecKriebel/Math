# Annular Martin-kernel research note

This folder is the preprint package for PR810, problem2307042 / AMR-022-7042,
Hayman–Lingham Problem7.42. The exact theorem and all assumptions are stated in
the concise research note. Repository acceptance and publication receipts are
maintained separately from this frozen prepublication verification package.

## Build and inspect

Build with a current TeX installation (the preparation used Tectonic):

    mkdir -p output/pdf
    tectonic --outdir output/pdf note.tex

The source uses standard article, geometry, amsmath, amssymb, amsthm, fontenc,
lmodern and hyperref packages. A successful build proves only that the document
compiles. Mathematical acceptance rests on the analytic proof and independent
reviews, not document compilation, checksums or numerical sampling.

After extracting verification.zip, work in its preprint/ directory. The
standard-library diagnostic script at ../math_review_01/reproduce_checks.py
recomputes its output file; this is diagnostic verification, not a proof. Its
explicit invariant guards remain active with normal and optimized Python. The
correction receipt records the historical script and negative-control tests.
Rebuild the PDF as above before running python3 build_package.py. PDF creation
timestamps may differ; byte-for-byte reproduction of compiled PDFs is not
claimed. The supporting archive is assembled by build_package.py from an explicit list
of authored materials. Its MANIFEST.json gives file hashes and sizes and does
not hash itself. No third-party PDFs, raw source extracts, private credentials
or private project coordination records belong in the public package. Bounded
public QUEUE-delta and research-log records are included as provenance.

## Disclosure and scope

OpenAI tools were used extensively in solving, drafting and independent
adversarial verification. This is an unrefereed preprint; no completed human
peer review or proof-assistant certification is claimed. The theorem excludes
contact in a punctured neighborhood of the base and equality throughout a
Green line issuing from it. It does not exclude isolated contact farther away.
Priority statements are limited to the accompanying dated audit.

Author: Alec Kriebel, independent researcher.
ORCID: https://orcid.org/0009-0001-9320-500X.
Paper and authored supplementary materials: CC BY4.0.

The October12 priority audit in the supporting archive expands the historical
source-status packet with Shiga, Köhn and Leutwiler and a full final-title
Bear–Smith author manuscript. Original frozen packets retain their historical
inspection limits; the new dated audit is the current source/priority record.
No first-resolution or current-worldwide-openness certification is claimed.
