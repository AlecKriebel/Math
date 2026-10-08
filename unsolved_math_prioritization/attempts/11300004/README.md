# Wild-knot quadrisecants: corrected partial results

Problem 11300004 / AMR-112-0004, rank 1014. Disposition: **unsolved, 5/5**.

The independently audited report establishes seven auxiliary lemmas and a rectifiable tame unknot with infinite total curvature and no trisecants as a countercontrol. It does not prove the universal assertion that every wild knot has infinitely many distinct quadrisecant supporting lines. Marked quadrisecant configurations are different objects from supporting lines; the 1994 published knot formulation and the 2002 arXiv arc formulation are also distinguished. No wild counterexample, novelty, formal certification, or human peer-review claim is made.

Read `audit/public/corrected/packet/REPORT.md`, `audit/public/AUDIT.md`, and `audit/public/ACCEPTANCE.json`. All accepted public audit files and corrected proof/code files are preserved byte-for-byte. The pure-code ledger type correction is in `audit/public/LEDGER_TYPE_HARDENING.patch`. Historical receipts remain historical, including their original remote-write flags. No original source-quotation archive, literal source-quotation-removal patch, private file, copied source document, dataset contents, or source extract is included.

## Reproduce

Requires Python 3.9+ standard library on POSIX, a genuine non-root account, and trusted Python/OS. Before executing anything, independently authenticate the SHA-256 of `BOOTSTRAP.py` against a separately trusted publication receipt or PR description. A package cannot authenticate its own trust anchor. The bootstrap pins the verifier and manifest before executing them; the verifier enforces the exact inventory, byte counts, digests, accepted archive equality, and unresolved scope.

From this directory:

    python3 -I -S -B BOOTSTRAP.py
    python3 -I -S -B -O BOOTSTRAP.py
    python3 -I -S -B -OO BOOTSTRAP.py
    python3 -I -S -B TEST_MUTATIONS.py
    python3 -I -S -B -O TEST_MUTATIONS.py
    python3 -I -S -B -OO TEST_MUTATIONS.py

The full replay relocates all files into a genuinely read-only tree and checks failed writes, UID/EUID, unchanged files, the 93-run distributed author suite, 129 independent runs, 12 corrected exact-integer ledger regression rejections, and independent finite mathematical controls. The corrected archive's internal replay covers all three optimization modes. The outer publication controls test missing/altered files, strict inventory, malformed manifests, symlinks, hardlinks, FIFOs, hostile code and import isolation, plus explicitly repinned malformed-schema diagnostics and malformed archive controls. Diagnostic repinning is confined to the test harness and never changes the production trust anchor. An integrity-only invocation is also available with `--integrity-only`; it does not execute the mathematical controls.

Private source/corpus inputs are deliberately absent, so current source rehash, corpus rehash, record join, fresh retrieval and fresh source inspection are `NOT_RUN`. Historical inspection metadata is not presented as a fresh source check. GitHub CI is separate and is not established by a local replay; zero checks means `NOT_RUN`.

Threat model: immutable candidate files, trusted external launcher pin, trusted isolated Python and standard library. This is neither a sandbox for arbitrary concurrent adversaries nor a formal proof assistant. Finite checks do not establish the general topological assertion.
