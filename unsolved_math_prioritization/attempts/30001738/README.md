# Unitary multiplicities: credited resolution and catalogue correction

Problem 30001738 / OWR-4804-006; rank 979; **already_solved, 0/5** for the precise p-adic irreducible source target.

Read [ACCEPTANCE.md](ACCEPTANCE.md), [the complete report](author/REPORT.md), and [the independent audit](audit/AUDIT_REPORT.md). Beuzart-Plessis's published 2022 theorem, extending Feigon–Lapid–Offen, gives total multiplicity 2^k when every inducing factor is individually Galois invariant, with repetitions counted. The weaker whole-product-invariance catalogue assertion is false: the explicit paired-character example has multiplicity 1 rather than 4. No novelty is claimed.

The immutable author/ and audit/ directories, original ZIPs and freeze receipts are retained in full. Their historical statements that review or publication had not occurred describe their freeze time. The outer acceptance is the current disposition. No mathematical correction patch was needed.

## Portable replay

Requires a trusted Python 3 interpreter, standard library and operating system. No packages, network, papers or datasets are needed. Obtain the SHA-256 pins of PUBLIC_MANIFEST.json and verify_publication.py independently from the draft PR description (or another independently trusted receipt). Check the verifier hash before executing it. A checksum stored only beside its payload is not an external trust anchor.

From any directory, invoke the independently pinned verifier with:

    python -I -S -B /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -O /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -OO /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet

The verifier rejects unlisted entries, linked or special files, invalid paths, wrong pins and byte mismatches, verifies both frozen archives and nested manifests, then runs the captured verified scripts in a private temporary snapshot. It checks full computed receipts, not just exit codes. It replays the author's finite checks and the independent audit's 38 corruption/semantic rejections. It is an integrity/reproducibility checker, not a hostile-code sandbox, race-resistant filesystem security boundary, or mathematical proof certificate.

After the outer package is verified, its publication-specific mutation suite can be run with:

    python -I -S -B /path/to/packet/mutation_tests.py EXPECTED_MANIFEST_SHA256 /path/to/packet

This tests normal, optimized, doubly optimized, and relocated execution and rejection of changed payloads/archives/manifests, extra or missing files/directories, links, bad pins, malformed inventories and manifest-laundered changes to frozen evidence. It never changes the original packet. Mutation-suite code must also be independently pinned or captured from a verified package before execution.

## Contents and limits

PUBLIC_MANIFEST.json is the closed allowlist, with byte counts and SHA-256 pins for every other file. Public source/corpus verification metadata are included; copied papers, extracts, screenshots, dataset contents, private sources and coordination files are excluded. Replay does not repeat fresh literature inspection or public corpus retrieval. The source metadata and audit state the historical inspection evidence and its limits.

The affirmative conclusion requires characteristic-zero p-adic fields, complex coefficients, irreducible normalized induction and individual factor invariance. No extension to arbitrary reducible induction, Archimedean or positive-characteristic fields, modular coefficients or nongeneric quotients is asserted.
