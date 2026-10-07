# Four-site small-time negative association for step ASEP

Problem 9600004 / AMR-095-0004, rank 933. Status: unsolved, 3/5 approaches used.

The accepted local theorem concerns the actual infinite integer-lattice step ASEP, initially occupied exactly on x <= 0. For p > 0 and 0 <= q <= p, its {-1,0,1,2} marginal is negatively associated for 0 <= p*t <= 1/10837981440. Nonconstant increasing functions on disjoint supports have strictly negative covariance at positive times in that interval.

The proof covers all 174 support-labelled increasing-event tests (78 distinct lifted event pairs), exact polynomial generator derivatives through order six, and an analytic uniform remainder passed to infinite volume. An independent implementation uses infinite step-deviation configurations and antichain event enumeration. This is stronger than pairwise occupation-covariance testing.

This does not resolve Liggett's all-coordinate, all-time question. The manuscript makes no novelty claim. Acceptance is independent AI-assisted review, not human peer review or formal verification. No mathematical repair was required. The original and accepted files are preserved byte for byte, including historical status wording.

## Contents

- author_original/: exact frozen author archive members.
- independent_audit/: exact independently accepted audit archive members and its preserved original.
- archives/: both frozen ZIPs, their external manifests, and the audit receipt.
- PUBLICATION_METADATA.json: exact scope and two-cell queue change.
- verify_publication.py: integrity, publication-scope, replay, and optional external-input checks.

See independent_audit/audit/REPORT.md and ACCEPTANCE.json for the exact acceptance boundary, and author_original/asymmetric_exclusion_9600004/PROOF.md for the analytic argument. Source PDFs, extracted source text, dataset records, private material, and bytecode are excluded.

## Reproduction

Authenticate verify_publication.py and PUBLICATION_MANIFEST.json with independently supplied SHA-256 values before execution. The wrapper itself checks the supplied manifest pin before executing packet programs:

    python -I -S verify_publication.py . --manifest-sha256 SHA256 --replay
    python -I -S -O verify_publication.py . --manifest-sha256 SHA256 --replay

Optional --base-queue BASE --queue QUEUE verifies the exact two-cell change. Optional --corpus-dir CORPUS --pdf-dir PDF rehashes all three full corpus files and five PDF sources, reconstructs the canonical problem/report pair, and compares the saved input replay. These external inputs are intentionally not redistributed. Without them, external verification is explicitly NOT_RUN. Source-free replay cannot establish that external source files were checked.

The full wrapper replay runs the author and independent suites from a fresh, relocated archive extraction under normal, optimized, isolated/no-site, and combined isolated/optimized Python, including 34 non-vacuous mathematical negative executions per suite pair. Separate wrapper controls test tampering and overclaims. Exact-code checks do not formally verify the analytic infinite-volume proof.
