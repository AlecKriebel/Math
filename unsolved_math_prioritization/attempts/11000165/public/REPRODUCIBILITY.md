# Reproducibility, adaptations, and integrity

## Run locally

Use Python 3.10+ with the standard library. No network, package installation, external datasets, scholarly PDFs, repository checkout, or private files are required. Start in the extracted public directory:

    python3 -I -B verify_package.py
    python3 -I -B run_checks.py
    python3 -I -B check_tamper_controls.py

For an externally pinned check, take the manifest SHA-256 from the separately supplied archive receipt or independently trusted publication record:

    python3 -I -B verify_package.py --manifest-sha256 THE_VERIFIED_MANIFEST_SHA256

The root manifest excludes itself to avoid circular hashing. The separate archive receipt pins its exact bytes. Archive construction uses sorted regular files under public/, fixed permissions 0444, owner/group 0, empty owner/group names, and mtime zero; gzip timestamp and filename are fixed. Two fresh builds must be byte-identical. Extraction is checked before scripts are run.

## Replay behavior

The replay first checks the full public file set and all hashes. It runs each of the seven mathematical scripts in normal, -O and -OO modes in disposable copies, comparing deterministic mathematical output to the recorded baseline. It also tests an intentional false runtime guard in all modes and exercises formula-mutant rejection. The input public tree is snapshotted and must remain byte-for-byte unchanged.

The principal independent checker completes 62,840 checks per execution. Its mathematical result agrees with the historical independent normal/optimized receipts and the root rerun; only public proof/checker identity fields change in the publication edition. The independent historical normal, optimized and root results are identical after the same coordination-hash omission.

The universal genus-two polynomial identities are algebraic identities over Z[p,q], not numerical sampling. Finite rank/genus/power tests in the other parts supplement uniform written proofs. A passing checker does not reprove the classical topology, identify a curve in an unseen source figure, certify novelty, or mechanically verify the entire proof text.

## Disclosed public adaptations

[ORIGINAL_IDENTITIES.json](ORIGINAL_IDENTITIES.json) records both original and delivered hashes and byte counts for every selected input. [AUDIT_BINDINGS.json](AUDIT_BINDINGS.json) connects the inspected originals to the final acceptance records and their public copies.

- Mathematical manuscripts retain their proofs, qualifications and citations. Limited administrative language and local source-fixture references are removed.
- Historical manifests retain only public mathematical inputs and metadata. Their listed original hashes are not silently replaced by public-edition hashes.
- Source metadata retains public URLs, available PDF hashes/sizes, and inspection history; local filesystem locations are omitted.
- The principal exact checker only drops unrelated input hashes. Its exact checking logic remains unchanged.
- Supplementary assert predicates are mechanically converted to explicit RuntimeError guards, so Python optimization cannot disable them.
- The former SymPy-backed genus-two checker is replaced by standard-library exact arithmetic using the independent universal polynomial calculation and the same 121 integer homology/orientation samples. The historical result is reproduced.
- One supplementary checker's stdout filename is made independent of the extraction directory.

The original final combined audit had SHA-256 515f62b1113721b44bbf9a10214ad27fe70f92dc7ec221c2afa6a2526d6e7539. Its original manifest had SHA-256 94ec2598c7056dc95690f8d5863195e57abafc12b9dca346160f133f9001c3c5. Both identities are checked in the public acceptance binding. Adapted public copies have their own explicitly recorded hashes.

## Trust boundaries

An unpinned package can establish internal consistency but cannot prove authenticity against an adversary who replaces the entire package and verifier. Use an independent external manifest/archive pin for that threat. Original-to-public identity records are provenance declarations verified against originals at build time; excluded material is deliberately not needed at replay time. The independently pinned final-audit input identities anchor the accepted mathematical manuscripts.

Tamper controls check byte changes, file-set changes, symlinks, nonregular objects, malformed or duplicate manifest data, path traversal, byte/hash mismatches, incorrect external pins, and malicious rebasing of acceptance identities. Formula-negative controls deliberately corrupt key signs and must fail even under -O/-OO. These tests demonstrate particular fail-closed behavior; they are not a general security certification.
