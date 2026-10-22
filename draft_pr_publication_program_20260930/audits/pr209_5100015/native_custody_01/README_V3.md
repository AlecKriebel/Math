# PR209 public verifier command correction

This is an additive correction to the preserved README_V2.md and V2 packet. Select PUBLIC_ALLOWLIST_V3.json and NATIVE_CUSTODY_SEAL_V3.json for the compact public package.

The selected public verifier is verify_public_custody_offline_v3.py. Its module docstring now names its own exact filename in the command:

    python3 -E -S -B -P /absolute/path/verify_public_custody_offline_v3.py

That docstring command is its only source change from verify_public_custody_offline.py. PUBLIC_VERIFIER_V3_SOURCE_EQUIVALENCE.json binds the old/new source pins, byte-identical source after the module docstring, and identical executable AST with the leading docstring excluded. The executable verifier body is unchanged. The full/private verifier remains verify_custody_offline.py and remains outside the public allowlist. Root will independently inspect and run the selected public V3 verifier and full private verifier.

All V2 files and controls remain byte-exact. The large inherited native metadata remains private. Native custody remains complete at 100%; the broader case remains 5%, with no mathematical, source, priority, integration or publication verdict added by this correction. Prior successful offline verification receipts remain historical receipts for the unchanged executable body; this documentation correction does not claim a new verifier execution.
