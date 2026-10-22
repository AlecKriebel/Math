# Replay and scope

Run:
    /opt/homebrew/bin/python3.11 -E -S -B -P fresh_controls.py
    /opt/homebrew/bin/python3.11 -E -S -B -P supplemental_exact.py

The scripts explicitly insert /Users/alec/Library/Python/3.11/lib/python/site-packages and require SymPy1.14.0 and mpmath1.3.0. No installation, network access, Git or provider mutation is used by the scripts. The fresh-controls run uses90 decimal digits and may take a few minutes. Its numerical diagnostics are not interval-certified. Both scripts overwrite only their own results files in this audit folder; no shared source or status files are touched.

The public manifest below is an explicit finite payload allowlist. It includes the failed initial harness only as inert text and labels that failure in a separate note. Source PDFs were not copied into the packet. The original manuscript and preserved proof remain external pinned inputs; SOURCE_SCOPE.json records their exact paths and byte hashes.

A report seal binds the manifest and the two report files. It is an integrity check, not external timestamp certification, a signature, Root acceptance or publication authorization.
