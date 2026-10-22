# Replication and custody

The packet is portable within an audit directory. Place priority_audit next to private_sources/selected_record.json and original/unsolved_math_prioritization/attempts/30001054. Input checks resolve those paths relative to the packet's parent, never to the recorded original absolute path. They compare full bytes and SHA256, never mtimes.

From the packet directory, run the following with the manifest hash supplied in the final handoff:

    python3 -B verify_custody.py --manifest-sha256 REPORTED_MANIFEST_SHA256 --inputs
    python3 -B -O verify_custody.py --manifest-sha256 REPORTED_MANIFEST_SHA256 --inputs

For a standalone packet lacking sibling inputs, omit --inputs; that checks authored closure only and must not be reported as a successful current-input check. Both commands are read-only and create no bytecode files. The guard checks the exact recursive regular-file inventory, hidden files, content pins, early immutable checkpoint files, the initial timing caveat, and the finite word under the caller's optimization mode. It rejects symlinks, special files, empty directories, extra/missing files, wrong bytes, and an incorrect externally supplied seal. MANIFEST.json excludes only itself. Its external hash is required because a packet cannot self-authenticate a replaced manifest.

The finite word alone can be checked with:

    python3 -B check_word.py
    python3 -B -O check_word.py

For primary-source replication, use SOURCE_RECEIPTS.json. Each successful byte pin identifies the exact source URL, full downloaded-byte length and SHA256, and the actual pages read. Retrieval was in memory and PDF text extraction used pdftotext with stdin/stdout. The packet contains neither third-party bodies nor renders. Re-fetching a source can return revised bytes, subscription HTML, or an access error; require its expected PDF type and hash before treating it as the same inspected source. In particular, HTTP200 from either final GP PDF URL did not mean final-body access.

The normal and optimized custody checks do not independently validate the literature interpretation, historical independence, completeness of web coverage, or priority. The history file records observed tool-history statements and hashes; it is not a time attestation by an external authority. The initial physical save followed ENOSPC and permitted input reads, as recorded in INITIAL_POSITION.json.
