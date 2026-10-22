# Multiplicity-free quantization: source correction and explicit examples

ID 30001707 / OWR-4799-003. Status: partial; original one-way conjecture not resolved.

Read RESULT.md for the theorem scopes, complete elementary calculations, prior credit, and remaining gaps. APPROACHES.md records the bounded research approaches. SOURCES.json contains only public bibliographic/retrieval metadata. PROVENANCE.json contains only input hashes and bounded prior-search match results, not dataset contents.

Run exact checks:

    python -I -S -B certificate.py
    python -I -S -O -B certificate.py

A separately supplied strict external manifest pins every member, including the verifier. Before executing any Python entry point, verify the separately trusted external manifest hash and the entry-point file hash. Do not accept a replacement manifest as proof of authenticity. Start a trusted Python interpreter with -I -S, as below, so package-local imports, PYTHONPATH, and site customizations cannot run before validation. The entry points also reject missing isolation flags; that guard cannot undo code already run during an unsafe interpreter startup. Then run from any working directory:

    python -I -S -B /path/to/package/verify.py /path/to/external-manifest.json
    python -I -S -O -B /path/to/package/verify.py /path/to/external-manifest.json

To replay the four positive and 38 negative controls after the same bootstrap:

    python -I -S -B /path/to/package/controls.py /path/to/external-manifest.json
    python -I -S -O -B /path/to/package/controls.py /path/to/external-manifest.json

No network, dependencies, dataset, or third-party source file is needed. The verifier rejects every unexpected node, directory, symlink, missing member, size/hash mismatch, or changed expected result. The external author receipt records normal, optimized, relocation, and adversarial controls. Hash integrity is not a mathematical proof or independent acceptance.

The archive contains only authored mathematics, authored verification code, and public metadata. It excludes source PDFs, extracts, images, dataset records, and private coordination material. This author freeze is not publication approval or independent acceptance.

Independent hardening correction: all verifier and certificate subprocesses use isolated, no-site Python startup. This prevents the independently reproduced extra-module import-shadowing execution defect in the author freeze. No mathematical result, finite check, or expected check output was changed. This is a corrected derivative, not the immutable original author freeze.
