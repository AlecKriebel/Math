# Credited reconstruction of the RBM(4,3) obstruction

Read REPORT.md for the recovered problem, exact model, full analytic argument,
credit, verification and limits. Recommended disposition: verified prior negative
resolution, subject to the separate uninvolved audit. One substantive approach
was used; no new mathematical discovery is claimed.

The source is Anonymous, v0.2.0-candidate, DOI 10.5281/zenodo.22550044,
commit fac57cd9a497a509d443f34f9b9843f6c7a7042f of
https://github.com/ipitchford/rbm43-eight-point-obstruction.
It remains an unrefereed, AI-assisted publication.

## Reproduction

Obtain certificate.json and appendix.md from that pinned public commit, put them
outside this authored packet, then run with Python 3.10 or later:

    python3 -I verify_reconstruction.py /path/to/certificate.json /path/to/appendix.md
    python3 -I -O verify_reconstruction.py /path/to/certificate.json /path/to/appendix.md
    python3 -I test_reconstruction.py /path/to/certificate.json /path/to/appendix.md
    python3 -I -O test_reconstruction.py /path/to/certificate.json /path/to/appendix.md
    python3 -I verify_prior_local_chart.py

The full reconstruction needs only the standard library and marks all 16,777,216
unrestricted selectors. It executes no producer code. The scripts print receipts
to stdout, so replay does not change saved receipts. Tests may create ordinary
Python bytecode unless PYTHONDONTWRITEBYTECODE is set. Bytecode is not part of
the authored inventory.

Expected source SHA-256 hashes and byte sizes are in source_verification.json.
They are checked as provenance; semantic verification is independent of a hash
match. The recorded PDF metadata explicitly makes no PDF retrieval/inspection
claim. The Markdown proof was retrieved and read in full.

## Packet boundary

Only authored analysis, new verification code, verification receipts and public
source/corpus hashes are included. The imported corpora, original research
report, source PDFs, source extracts, original certificate contents and
coordination material are excluded. Source attribution is retained even though
the source declares its prose and data public domain.
