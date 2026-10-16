# Replication

Use Python3 standard library only. Run from this directory, supplying the exact MANIFEST.json SHA256 pinned outside this packet:

    python3 -B verify_custody.py --manifest-sha256 EXTERNALLY_PINNED_MANIFEST_SHA256
    python3 -B -O verify_custody.py --manifest-sha256 EXTERNALLY_PINNED_MANIFEST_SHA256
    python3 -B check_event_mapping.py
    python3 -B -O check_event_mapping.py
    python3 -B test_custody.py
    python3 -B -O test_custody.py

The custody verifier is read-only and does not authenticate a freely rewritten manifest without the external pin. It checks all actual recursive files including hidden files, excluding only MANIFEST.json itself. No symlinks, special files or empty directories are permitted. The inventory has no absolute-filesystem or preserved-mtime requirement. The seal timestamp is recorded after all authored edits and scratch cleanup, rather than requiring imported source mtimes at replication.

The event check is a small independent convention/multiplicity check. It does not replay or prove the full geometry gate, and it does not validate scholarly priority. The custody adversarial tests create only their own tiny fixture in ownignoredscratch/ inside this directory and remove it before exit. Their recorded normal/-O results are in CUSTODY_TEST_RESULTS.json. They are deliberately run before sealing; invoking them later leaves no persistent new files on success. Use -B to avoid bytecode files, which exact custody would correctly reject as extra files.

If the original input snapshot and private selected record are available as siblings under the audit directory, optionally run:

    python3 -B check_current_inputs.py
    python3 -B -O check_current_inputs.py

This optional check is separate from authored-packet custody. CURRENT_INPUT_IDENTITIES.json uses relative paths under sibling original/ and private_sources/; --audit-root may select a relocated audit tree. It does not query Git or require original absolute paths or mtimes. A portable source-only copy lacking those sibling inputs can still verify this authored packet.

SOURCE_COMPARISON.md gives public source URLs, versions, pages actually read and received-body SHA256 values. Source PDFs, full text, private record contents and unrelated work are not redistributed. Body hashes alone do not certify publication dates or completeness of a search.
