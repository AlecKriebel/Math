# K3 Problem 3.47: corrected partial results

Record 2845, rank 1046. **Unsolved, 5/5 mathematical approaches.**

Read [ACCEPTANCE.md](ACCEPTANCE.md), the accepted
[corrected report](corrected/REPORT.md), and the
[independent audit](audit/INDEPENDENT_AUDIT.md). The original author slice is
preserved in `author/`; the corrected slice is separate. Both universal
elliptic-orbit questions remain unresolved. The source-attribution correction
points to K3 section 3.5, page 160, which itself states inclusive ellipticity.
No mathematical conclusion or checking code was changed.

The packet contains no source documents or datasets. PDF hashes, byte counts,
retrieval/inspection history, and manuscript status are accepted historical
metadata. Fresh source/PDF checks are **NOT_RUN** in source-free replays.

## Authenticate before execution

Obtain `BOOTSTRAP.py` and its SHA-256 through an independently trusted channel,
such as a separately authenticated repository commit and verification receipt.
Check that hash externally before running any packet code. Do not rely on a
hash fetched only from the same unauthenticated packet. The authenticated
bootstrap pins `verify_publication.py` and `PUBLICATION_MANIFEST.json`; the
manifest binds all other payload files. The verifier additionally pins every
original, corrected, and audit file, and rejects extra members, directories,
links, special files, malformed JSON, and silently changed receipt types.

Requirements: Python 3 standard library, Linux, working bubblewrap (`bwrap`),
and real/effective UID 1000. Linux read-only mount operations must be permitted.
This is not a claim of cross-platform portability. No network access or source
corpus is needed; no network-namespace isolation is claimed.

After authenticating the bootstrap externally:

    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

The trusted bootstrap copy must be byte-identical to the packet's bootstrap.
The wrapper runs from any directory, authenticates first, reconstructs the
correction in memory, then runs the native audit in a temporary snapshot. That
audit mounts the visible filesystem read-only for its arithmetic executions,
checks actual EROFS write denials, and runs normal, -O, and -OO subprocesses.
The wrapper compares the full audit output byte-for-byte with its pinned
receipt and rechecks all input bytes afterward. Results are printed to stdout;
keep redirected output outside the exact-inventory packet.

## Publication boundary controls

After authenticating the bootstrap and verifying the manifest-bound test
harness, run:

    python3 -I -S -B /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 EXTERNALLY_AUTHENTICATED_SHA256

Repeat with -O and -OO. The harness tests exact inventories, symlinks and special
files, linked roots and ancestors, content corruption, coordinated manifest
repinning, correction and patch corruption, strict JSON/types, relocated
read-only copies, and hostile Python import environments. It creates disposable
mutation copies outside the accepted packet. Read-only permission probes in
those disposable copies are distinct from the native audit's EROFS mount
probes. The publication receipt records separate whole-driver read-only mount
runs in all three modes; no chmod-only test is presented as a mount test.

Passing these checks authenticates and replays this finite authored packet.
It does not solve the problem, realize its abstract index model, establish
novelty, or machine-certify the imported theorems.
