# Verification instructions

Read REPORT.md for the mathematical scope before interpreting a passing check.

Use Python 3 and the standard library. A frozen publication unit consists of this packet, an external FREEZE_MANIFEST.json, an external bootstrap.py, and externally retained BOOTSTRAP_PINS.json. First compare the bootstrap and manifest hashes to independently trusted pins. Then invoke bootstrap.py with the packet directory. The bootstrap is specific to this freeze and resolves its manifest alongside itself.

A direct check is: python3 -B verify.py --packet PACKET --manifest MANIFEST --manifest-sha256 TRUSTED_DIGEST. Repeat under -O and -OO. Digests obtained only from the files being checked are not independent trust anchors. Replacing both data and pins is outside what integrity checking can detect.

proof_checks.py can also run independently. It uses exact integer and finite-field operations. It has no network access or nonstandard dependencies, writes no files, and proves no claims about geometric realization. A passing result is not a resolution of the main problem.

No sources, extracts, dataset records, credentials, or private coordination material belong in this packet. The accompanying acceptance receipt concerns these exact frozen bytes and a genuine non-root account with write attempts denied by filesystem permissions.
