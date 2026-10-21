# Frozen audit instructions

Authenticate these values against the separately delivered handoff before executing code. A hash written beside a file is not an independent trust anchor.

- Public manifest SHA-256: `31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c`
- Bootstrap SHA-256: `054dbe643ad4f78f13ea0595e4cab5379d438a33ab2fd2f6aed9f5125d9dcb57`
- Test harness SHA-256: `5c6d1056179a95c647db5cc11028059c64c5abcdcabd69790cef892948c9ca27`

The manifest authenticates every file in the public directory, including the report, metadata, fixture and checker. The bootstrap checks the externally supplied manifest digest, rejects extra files, path traversal, duplicate names, symlinks and malformed manifest fields, then executes the verified checker and fixture byte snapshots.

From the bundle root, with an authenticated bootstrap:

    python3 -I -B external/bootstrap.py public external/MANIFEST.json 31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c normal
    python3 -I -B -O external/bootstrap.py public external/MANIFEST.json 31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c O
    python3 -I -B -OO external/bootstrap.py public external/MANIFEST.json 31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c OO

To rerun the software audit as a genuine nonroot user:

    python3 -I -B external/test_harness.py public external 31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c

The harness refuses UID/EUID zero, confirms that both append and create operations fail on a read-only temporary copy, tests all three Python optimization modes, rejects 18 malformed fixture variants, ignores hostile import modules under isolated Python, and rejects 10 file/manifest tampering variants. It restores temporary permissions only for cleanup. All original hashes must remain unchanged.

These controls verify finite identities and software behavior. They neither mechanize the infinite proof nor construct a free ultrafilter. The ZFC proof and source-scope comparison require mathematical review. No source files are required to run the public finite checks.
