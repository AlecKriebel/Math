# Publication verification

The publication wrapper is a separate, fail-closed integrity gate. A verifier must obtain its SHA-256 and the SHA-256 of `PUBLICATION_MANIFEST.json` from a trusted channel independent of an untrusted downloaded package. A self-supplied hash is not an authenticity anchor. Authenticate the wrapper before execution.

Run the authenticated wrapper with `--publication-root DIRECTORY --manifest-sha256 TRUSTED_SHA --catalog COMPLETE_CATALOG --problems COMPLETE_PROBLEMS --reports COMPLETE_REPORTS --sources-dir LOCAL_SOURCE_DIRECTORY --receipt OUTSIDE_RECEIPT`.

All arguments are mandatory except the output receipt. The source directory contains the four externally acquired PDFs under their recorded names, plus the saved canonical pair and catalog record. No source or corpus bytes are included in this publication. The full corpus byte counts and SHA-256 values, the exact 4,328-byte canonical-array binding, and the four PDF pins are recorded in the preserved source manifest.

Before executing package code, the wrapper authenticates every published file and exact inventory; all eight pinned archive/manifest inputs; every ZIP member with safe names, regular types and exact byte lengths; the original, clarified, audit and second-review trees; both exact acceptance scopes; both identical repair copies; and all required complete corpora and source inputs. It rejects duplicate JSON keys, unsafe paths, symlinks, extra files or directories, and altered byte bindings.

It then relocates only verified bytes and replays both independent reviews in isolated normal and optimized Python. The first audit replays the original and accepted author verifiers with all three full corpora and four PDFs, together with its independent arithmetic diagnostics. The second review independently replays its fixed input pins, exact fraction inequalities, 17,001 rounded-side checks and 9,973 selected-pair checks. The wrapper repeats mutation, extra-node, symlink, and repair-binding controls, then applies the preserved actual patch with zero fuzz and verifies all five resulting files against the accepted clarified archive.

The separate publication test suite runs the wrapper in normal, optimized, isolated, and isolated-optimized modes. It exercises outer-manifest and inventory rejection controls before executing any package bytes. Receipts distinguish successful integrity/finite tests from mathematical acceptance. The exact remote commit and complete remote byte readback, followed by replay of that readback, are reported after upload. A repository with zero GitHub status checks and zero workflow runs is reported as **no CI run**, never as CI passed.

Mathematical conclusion: the jointly accepted application and authored source-proof repair support a prior-literature resolution, credited to Aldous's 2021 Theorem 1.2. Original proof-search usage remains 0/5. Mechanical verification does not prove this infinite-network conclusion.
