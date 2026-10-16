# Global statistical embedding: problem 6000001

Queue rank 983, AMR-059-0001. Status: **claimed_solved**, four substantive mathematical turns out of five. The complete authored proof has passed two independent full mathematical audits without any required proof change. This is an AI-assisted, unrefereed manuscript; internal independent reviews are not journal or community acceptance. Historical novelty is not asserted.

For a smooth Hausdorff second-countable positive-definite statistical n-manifold without boundary, with both specified dual connections torsion-free, the theorem gives a proper global statistical embedding into an open positive Hessian domain in R^N, N=binomial(2n+4,3) for n>=1. The zero-dimensional case is treated separately. The metric and both correctly ordered connections are induced.

The ambient domain may be nonconvex and incomplete, and dual gradient coordinates are local. No finite probability-simplex realization, optimal dimension, global dual chart, indefinite or nonsmooth generalization, or boundary case is claimed. The compactness correction in Lê's later version is respected.

## Reading order

1. `public/PROOF.md`: complete unchanged proof.
2. `independent_global_audit/public/GLOBAL_AUDIT.md` and its `ACCEPTANCE.json`: full audit A.
3. `independent_audit_b/public/FULL_REPORT.md` and its `ACCEPTANCE.json`: full audit B.
4. `ACCEPTANCE.md`: consolidated scope and provenance.
5. `independent_audit_b/public/CITATION_SCOPE_NOTE.md`: optional citation clarification, retained separately.

Historical status phrases inside the three frozen packets describe their respective freeze times. This top-level publication record records the completed two-audit status. All 27 original files, including both reports and acceptances, remain byte-for-byte unchanged.

## Portable verification

Authenticate `verify_publication.py` and `mutation_tests.py` using the independent SHA-256 pins in the draft PR description before executing them. Obtain the PUBLIC_MANIFEST.json SHA-256 from that same external record; deriving a trust anchor from an untrusted download does not authenticate it.

Python 3, SymPy, and NumPy are needed for finite mathematical replay. Recorded versions are Python 3.12.14, SymPy 1.14.0, NumPy 2.3.5. The integrity-only path uses only the standard library. No network, original workspace, PDFs, source extracts, or datasets are required.

From any working directory, with absolute paths or suitable relative paths:

    python -I -S -B verify_publication.py EXTERNAL_MANIFEST_SHA256 PACKET_DIRECTORY
    python -I -S -B -O verify_publication.py EXTERNAL_MANIFEST_SHA256 PACKET_DIRECTORY
    python -I -S -B -OO verify_publication.py EXTERNAL_MANIFEST_SHA256 PACKET_DIRECTORY
    python -I -S -B mutation_tests.py EXTERNAL_MANIFEST_SHA256 PACKET_DIRECTORY

The outer wrapper checks exact closed inventory, regular files and directories, original freeze pins, all byte counts and hashes, acceptance bindings, and fresh replay. It materializes authenticated bytes into an isolated temporary tree, and runs all original verifiers and three independent finite-check programs there. It checks the source packet again afterward. Results are compared with recorded output after removing version-only fields; changed numerical results fail closed.

The original programs use Python assertions. Every replay child is explicitly launched at optimization level 0, even when the outer wrapper uses -O, -OO, or PYTHONOPTIMIZE. An explicit bootstrap guard rejects optimized children before running a frozen program. `--child-optimize 1` and `--child-optimize 2` exercise those real child rejection paths. Optimized outer validation is supported; optimized execution of the original mathematical assertions is not claimed. The child flag records distinguish these cases.

Use `--integrity-only` to omit mathematical execution. Mutation tests reject corruption, missing/extra files, symlinks, unsafe or duplicate manifest entries, forged re-anchored records, and optimized children. These checks validate packaging and finite identities; they are not formal verification of the global mathematical proof.

Only authored mathematics, source-free checks, and public bibliographic/hash/inspection metadata are included. The queue update changes only this problem's Status, Turns, and Findings cells.
