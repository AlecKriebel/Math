# Calegari Question 6.1: accepted scoped partials

Problem **10300011 / AMR-102-0011**, rank **1004**. Disposition: **unsolved, 5/5 approaches**.

The [unchanged proof](author_original/author/PROOF.md) establishes only:

1. For an essential lamination consisting of finitely many two-sided compact connected leaves, containing a genuine sublamination is equivalent to being genuine.
2. The horizontal foliation of the specified orientation-preserving circle suspension has no genuine sublamination.
3. Intrinsic unbranched-carrier topology and transverse weights alone omit the embedding information needed to decide the target.
4. A deck-invariant genuine witness descends through a finite regular cover. The finite-union extension is restricted to compact two-sided leaves and its explicitly stated hypotheses.
5. The proposed carrier-certificate approach leaves soundness, completeness for the given lamination, and negative termination unproved.

See the [full independent audit](audit/AUDIT_REPORT.md) and [acceptance](audit/ACCEPTANCE.json). Essentiality passes to sublaminations. This packet does not establish a general hereditary rule for genuineness. The compact-leaf argument must not be generalized to arbitrary laminations or arbitrary finite unions of witnesses.

The independent audit accepted the exact frozen mathematical proof and verification files without a post-freeze correction. Historical “pending review” labels inside `author_original/` and historical “no remote writes” labels remain unchanged. Current acceptance is recorded separately in the audit. The positive-genus clarification preceded the freeze. Neither the author nor this acceptance claims a general characterization, an algorithm for the fixed-lamination problem, novelty, comprehensive current openness, machine-checked topology, or human peer review.

## Exact originals and source boundary

`archives/AUTHOR_V1.zip` is the original 24,189-byte author archive, SHA-256 `84795261940f05abad6f2b6208cc0558fde23beeb77ab735c607bac9fcb846a8`.

`archives/AUDIT_V1.zip` is the original 20,123-byte independent-audit archive, SHA-256 `7950ecc8d0da23d87e310710883668711d5e8dff1a92de75a4fd5cb37694d7c3`.

All archive members are reproduced byte-for-byte in the author and audit directories. Author bootstrap, author manifest, proof and audit manifest retain their independently supplied pins. Original receipts are historical evidence, not newly performed retrievals.

Only authored mathematics, audits, verification programs, acceptance reports and public metadata are included. Source PDFs, extracted third-party text or images, raw dataset records, private source material and private coordination files are excluded. Public scholarly references, source byte counts and hashes are listed in `author_original/author/SOURCE_PINS.json`; corpus hashes and record-match metadata appear in `CORPUS_BINDINGS.json`. No new download or primary-source inspection is claimed by this publication step.

## Reproduce the source-free checks

First authenticate `BOOTSTRAP.py`, `VERIFY_PUBLICATION.py` and `PUBLICATION_MANIFEST.json` against the external SHA-256 pins published in the draft PR. A self-consistent mutable bundle does not authenticate itself. Use a trusted Python interpreter and standard library on a quiescent filesystem; this is an integrity boundary, not an operating-system sandbox.

From this directory:

```sh
python3 -I -S -B BOOTSTRAP.py
python3 -I -S -B -O BOOTSTRAP.py
python3 -I -S -B -OO BOOTSTRAP.py
python3 -I -S -B TEST_MUTATIONS.py
python3 -I -S -B -O TEST_MUTATIONS.py
python3 -I -S -B -OO TEST_MUTATIONS.py
```

The bootstrap authenticates the verifier before executing it. The verifier checks the exact recursive file/directory inventory, strict manifest schema, hashes, both ZIP/member inventories, the independent acceptance, and the exact reviewed subject before staging authenticated bytes in a disposable directory. It then runs the original author bootstrap, author malformed-input controls, author boundary controls, independent mathematical controls and independent boundary controls. The supplied source tree is never modified. `--integrity-only` stops before executable replay.

The publication mutation suite uses a separate trusted original bootstrap and covers every file's deletion and alteration, malformed/duplicate/forged manifests, executable substitutions with marker detection, symlinks, extra files/directories, and a FIFO. Both ordinary and genuinely read-only relocated copies are tested. Use an ordinary non-root Unix account whose permissions are enforced; the suite explicitly tests that a write is denied. An inability to enforce read-only permissions is a failure, not a pass.

No network, third-party packages, PDFs or datasets are required. Optional `--sources-dir DIR` and `--corpora-dir DIR` request an actual read-only rehash of caller-supplied files after the public packet is authenticated. Absent inputs are reported as `NOT_SUPPLIED_NOT_RECHECKED`; historical matches are never substituted for a current pass. Missing or wrong supplied inputs fail closed. Do not upload those inputs as part of this packet.

Finite graph and arithmetic checks support bookkeeping and rejection behavior. They do not establish unbounded topology, formal proof correctness, or GitHub CI success. GitHub CI status must be read for the exact PR head separately.
