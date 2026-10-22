# Read-only replication

From any directory:

    PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr767_30005902/priority_adversary01/verify_closure.py
    PYTHONDONTWRITEBYTECODE=1 python3 -O /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr767_30005902/priority_adversary01/verify_closure.py

These verify exact recursive authored inventory, including hidden files and excluding only the top MANIFEST.json; reject symlinks, special files and empty directories; require the manifest to postdate all listed files; and verify the unchanged initial-position pin. They do not access network, Git or modify files.

For a separate current-input identity check:

    PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr767_30005902/priority_adversary01/verify_closure.py --check-current-input

The latter additionally reads the adjacent selected record and original author proof and compares their recorded statement/review/proof identity. Later unrelated input changes do not alter the historical closure.

For the independently cross-read first packet and its two key computations, run the two verify_history.py commands in ../priority_audit/REPLICATION.md. PEER_REPLAY.json records this audit's actual normal/optimized reproductions; CHECKABLE_PRIORITY_IMPLICATION.md gives my distinct GL2 calculation and exact operation proof. Arithmetic outputs are supplemental to the written/source check, not bibliographic completeness certificates.

