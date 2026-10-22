# Source-free corrected partials: problem 10300037

Start with [corrected acceptance](ACCEPTANCE.md), [the corrected proof](corrected/packet/PROOF.md), [the independent audit](audit_original/AUDIT.md), and [the actual correction patch](audit_original/CORRECTIONS.patch).

Status: **unsolved by this packet, 5/5**. The public universal Delman–Roberts announcement is credited. This packet makes no worldwide-openness, manuscript-nonexistence, novelty, or conventional-peer-review claim.

## Replay

Python 3 standard library and GNU-compatible `patch` are required. Verify the external BOOTSTRAP.py hash against the separately published PR anchors before executing:

    python -I -S -B BOOTSTRAP.py
    python -I -S -B -O BOOTSTRAP.py
    python -I -S -B -OO BOOTSTRAP.py
    python -I -S -B TEST_MUTATIONS.py

The bootstrap authenticates the verifier and manifest before any payload is executed. The verifier rejects extra/missing paths, symlinks, nonregular files, changed sizes/digests and malformed manifest objects; it preserves originals, replays the actual patch into a temporary tree with zero fuzz, and compares every corrected byte before replaying diagnostics. It runs the corrected mutation suite and the independent exact/malformed controls. Input directories may be genuinely read-only. Only isolated temporary copies are writable.

Default replay is source-free. Optional source/PDF/extraction and corpus rehash is **NOT_RUN** unless both separately held directories are explicitly supplied:

    python -I -S -B BOOTSTRAP.py --sources-dir SOURCE_DIRECTORY --corpora-dir CORPUS_DIRECTORY

Historical source-inspection receipts are not a fresh rehash or new HTTP retrieval. Hashes bind bytes relative to supplied external anchors; they are not signatures or mathematical proof. Replacing a launcher and its external trust anchor together is outside this trust model. Passing tests is not passing GitHub CI; inspect the exact-head checks separately.
