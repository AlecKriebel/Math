# Reproduce the independent RBM audit

Verdict and mathematical scope are in AUDIT_REPORT.md. The author freeze was not
modified. This directory contains original audit code, analysis and metadata;
it contains no imported proof text or certificate contents.

Use Python 3.10 or later. Obtain appendix.md, certificate.json and
positive_controls.json from the source commit linked in AUDIT_REPORT.md and keep
them outside this directory. The programs check the public input identities.

    python3 -I -B audit_certificate.py /path/to/appendix.md /path/to/certificate.json
    python3 -I -B -O audit_certificate.py /path/to/appendix.md /path/to/certificate.json

The main audit checks all feature identities and all unrestricted selectors in
two different ways. Expected status: PASS. The normal and optimized receipts
should differ only in python_optimized.

For the auxiliary parity construction and earlier local chart, supply the public
auxiliary data and the separately held original paired research report:

    python3 -I -B audit_auxiliary.py /path/to/positive_controls.json /path/to/prior_report.txt
    python3 -I -B -O audit_auxiliary.py /path/to/positive_controls.json /path/to/prior_report.txt

For inventory, source hashes and complete public corpus match verification:

    python3 -I -B audit_inputs.py /path/to/author_freeze.zip /path/to/author_directory /path/to/source_directory /path/to/corpus_directory /path/to/positive_controls.json

The source directory for that final check contains the seven public source files
named in the author source_verification.json and the inspected prior-report copy
as upstream_report.txt. The corpus directory contains the two full public
corpora. Neither source nor corpus data is redistributed here.

All scripts print receipts to standard output. They do not execute producer code
or mutate their input files. The MANIFEST.json records this audit's deliverables;
its own hash is recorded separately in the final archive metadata.
