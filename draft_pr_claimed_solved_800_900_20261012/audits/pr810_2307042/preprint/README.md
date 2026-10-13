# Annular Martin-kernel research note

This folder is the preprint package for PR810, problem2307042 / AMR-022-7042,
Hayman–Lingham Problem7.42. The exact theorem and all assumptions are stated in
the four-page research note. The current stage is preparation; publication and
acceptance receipts are recorded separately when actually completed.

## Build and inspect

Build with a current TeX installation (the preparation used Tectonic):

    tectonic --outdir output/pdf note.tex

The source uses standard article, geometry, amsmath, amssymb, amsthm, fontenc,
lmodern and hyperref packages. A successful build proves only that the document
compiles. Mathematical acceptance rests on the analytic proof and independent
reviews, not document compilation, checksums or numerical sampling.

The supporting archive is assembled by build_package.py from an explicit list
of authored materials. Its MANIFEST.json gives file hashes and sizes and does
not hash itself. No third-party PDFs, raw source extracts, private credentials
or project coordination records belong in the public package.

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
