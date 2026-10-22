# Synchronous reflected-Brownian coupling partials

Problem 9500005 / AMR-094-0005. Both original questions remain unresolved; exhausted 5/5. See [acceptance](ACCEPTANCE.md), [report](author/REPORT.md), and [independent audit](audit/AUDIT.md). No correction patch or novelty claim.

## Contents and public boundary

The author and audit subdirectories preserve all 14 accepted frozen files unchanged. They contain authored mathematics and code, full finite-check receipts, and permitted dated public-source verification metadata. They contain no copied sources, corpus bodies, private source data, or private coordination files. The outer manifest authenticates the entire packet. QUEUE_BINDING.json authenticates the exact queue postimage without duplicating it here.

## Trusted replay

Use Python 3.12, standard library only, with real/effective UID 1000. First obtain the BOOTSTRAP.py SHA-256 from the draft PR body or another trusted external record. Verify those bytes independently and keep that authenticated bootstrap outside the candidate directory. Do not derive the trust anchor from an untrusted candidate's own hash claims.

Run the trusted bootstrap with:

    python -I -S -B /trusted/BOOTSTRAP.py /candidate/packet /candidate/unsolved_math_prioritization/QUEUE.md

Repeat with -O and -OO before the bootstrap path. The wrapper authenticates the complete inventory and exact QUEUE before executing any candidate checker. A fresh temporary read-only copy is used for exact finite checks. Complete output bytes, parsed JSON types, denied physical writes, and unchanged input hashes are verified. Source/corpus/PDF checks are explicitly NOT_RUN.

The separately authenticated mutation_tests.py can be invoked with -I -S -B (and -O/-OO) plus --root PACKET --queue QUEUE --bootstrap-sha256 EXTERNAL_HASH. It tests missing/extra/symlink/FIFO files, recursive inventory, rehashed changed evidence, exact schemas, substituted wrappers, exact QUEUE substitution, and hostile read-only relocation. Authenticate this test harness against the trusted manifest before running it.

The original audit/replay_audit.py is historical evidence. The publication wrapper repeats the same six positive and 21 semantic-negative subprocesses rather than attempting to reproduce its variable timestamp or earlier snapshot. All complete recorded stdout/stderr is compared without normalization. The finite checks support the written proofs; they do not verify an infinite-horizon Brownian event or formalize the mathematical arguments.
