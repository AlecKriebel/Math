# K3 Problem 1.30: accepted incomplete research

Catalogue 2689, rank 1041. **Unsolved, 5/5 mathematical approaches.**
Start with [ACCEPTANCE.md](ACCEPTANCE.md), the complete
[REPORT.md](author/REPORT.md), and independent [AUDIT.md](audit/AUDIT.md).
No mathematical correction was needed. All sixteen frozen evidence files are
preserved. Historical source matches remain historical; fresh source/PDF
verification is **NOT_RUN**.

## Authenticate before execution

Obtain BOOTSTRAP.py and its SHA-256 through an independently trusted channel
(such as a verified repository commit and separately recorded receipt). Check
the bootstrap bytes externally before executing any packet code. An in-packet
hash cannot authenticate the same untrusted packet. The trusted bootstrap pins
the wrapper and manifest; the manifest binds the remaining exact inventory.
The wrapper additionally pins every frozen author/audit file and both original
manifests. Extra files/directories, links, special files, malformed JSON, changed
numeric types and self-consistent repinning of frozen evidence are rejected.

Use real/effective UID 1000 and a trusted Python 3 environment with SymPy 1.14.0
and mpmath 1.3.0 installed in that interpreter's configured purelib directory.
No package installation, network access, source corpus or knot table is done
by this packet. Dependency contents are trusted prerequisites, not authenticated
by the packet. This is explicitly not a standard-library-only computation.

After externally authenticating the bootstrap:

    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

The trusted bootstrap must match the packet's bootstrap bytes. All arithmetic
subprocesses use isolated/no-site mode, add only configured purelib for the
required dependencies, and bypass environment import paths, .pth files, user
site and sitecustomize. The independent algebra checker receives its
independent_cube module from the already authenticated bytes in memory.

Each run prints a JSON receipt with complete exact outputs and all eight
mathematical mutation failures. Redirect receipts outside the exact-inventory
packet. Missing dependencies or wrong versions cause failure, never a pass.
Read-only inputs and working directories are enforced with failed writes and
verified unchanged after execution.

## Publication controls

Authenticate and run the bootstrap first, thereby authenticating
mutation_tests.py. Then supply the independently verified bootstrap hash:

    python3 -I -S -B /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH
    python3 -I -S -B -O /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH
    python3 -I -S -B -OO /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH

The suite tests exact inventory, missing/extra files and directories, symlinks,
FIFO replacement, tampering and repinning, duplicate JSON keys, malformed
schemas, boolean/float integer substitutes, nonfinite numbers, bad pins, and
hostile imports during a read-only relocated replay. Only disposable negative
copies are made writable. Full mathematical outputs from the underlying replay
are checked against the frozen originals before a control suite can pass.

These tests establish finite algebraic reproducibility and packet integrity;
they do not prove the universal conjecture or knot realization of abstract
models, certify imported theorems, or establish novelty.
