# Source-free independent acceptance packet

Read AUDIT.md for the verdict, complete mathematical review, and precise source-dependency limits. ACCEPTANCE.json provides the machine-readable disposition. INDEPENDENT_CHECKS.json and AUTHOR_SUITE_RERUN.json record separately counted test results. SOURCE_REHASH.json and CORPUS_REHASH.json contain verification metadata only.

Reproduce the independent source-free controls with a trusted Python interpreter:

    python3 -I -S -B independent_checks.py /path/to/original/freeze /path/to/AUTHOR_FREEZE.zip

Authenticate this audit packet against its separately delivered AUDIT_MANIFEST.json and archive hash. The tests also hard-code the original author bootstrap, manifest, and ZIP pins supplied through the independent handoff. They reject a mismatching bootstrap before executing it. No copied scholarly PDFs, source text extractions, images, datasets, credentials, or private coordination files are included.

This audit accepts a credited published negative result. It does not claim a new counterexample, human peer review, formal verification, or a first-principles reconstruction of the published mapping-class construction.
