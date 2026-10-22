# Verification commands and limitations

Run from this directory:

    python check_turn1.py
    python check_turn2.py
    python check_turn3.py

Compare their JSON output byte-for-byte with turn1_receipt.json,
turn2_receipt.json and turn3_receipt.json. Turn 1 uses installed SymPy;
turns 2 and 3 use only the Python standard library. No downloaded source
code is executed. All tests use exact rational arithmetic, not simulation.

The receipts contain 486, 50,324 and 17,148 assertions respectively.
These totals test finite identities and the algebra used in the argument;
they are not independent proofs of limiting estimates. The main proof is
PROOF.md, with all analytic dependencies proved in TURN_1.md and TURN_2.md.

Verify FROZEN_MANIFEST.json and the two historical turn manifests using
SHA256. The primary PDFs are separately pinned in source_manifest.json and
SOURCE_ADDENDUM_TURN3.md. The former source_manifest and historical status
files are unchanged snapshots; CURRENT_STATUS_TURN3.md and BUDGET_TURN3.json
record the current full-candidate status. No result should be promoted
before a separate full adversarial review.
