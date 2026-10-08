# K3 Problem 1.22: accepted incomplete research

Record 2681, rank 1040. **Unsolved, 5/5 mathematical attempts.**

Start with [ACCEPTANCE.md](ACCEPTANCE.md), the complete
[REPORT.md](author/REPORT.md), and the independent [AUDIT.md](audit/AUDIT.md).
No mathematical correction was required. The eight author files and seven audit
files are frozen. Their source metadata and saved execution outputs are
historical evidence, not fresh source checks. Sources and datasets are omitted;
fresh source/PDF verification is **NOT_RUN**. All mathematical and literature
scope limits in the accepted reports remain in force.

## Authenticate before executing

Obtain BOOTSTRAP.py and its SHA-256 through an independently trusted channel
(for example the repository commit and its separately recorded verification
receipt). Verify those bytes externally before running any packet code.
A hash read solely from the same untrusted packet cannot authenticate it.
The authenticated bootstrap pins the verifier and publication manifest; the
manifest pins every other payload member. The verifier independently pins all
15 frozen evidence files and rejects extra files, directories, links, special
files, malformed JSON, or silently changed receipt types.

After external bootstrap authentication, run from any directory using real and
effective UID 1000 (standard-library Python 3, no network or source corpus):

    python3 -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

The trusted bootstrap copy must be byte-identical to the packet's BOOTSTRAP.py.
-I, -S, and -B disable untrusted environment/import paths and bytecode writes.
The wrapper first authenticates the complete packet, then runs original and
independent checkers and the original audit mutation harness in temporary
read-only copies. It checks input preservation after execution and prints
PASS only after all verification completes. Runtime receipts go to stdout;
redirect them outside the exact-inventory packet.

## Publication mutation suite

First authenticate and run the bootstrap above. This authenticates
mutation_tests.py before it is executed. Supply the externally verified
bootstrap hash, never an untrusted in-packet assertion of that hash:

    python3 -I -S -B /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH
    python3 -I -S -B -O /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH
    python3 -I -S -B -OO /path/to/packet/mutation_tests.py --root /path/to/packet --bootstrap-sha256 VERIFIED_HASH

Each mode replays the complete verifier and repeats it under hostile import
settings from a read-only relocated packet and read-only working directory.
Negative cases cover inventory changes, symlinks, FIFO substitution, tampering,
self-consistent repinning of frozen evidence, malformed schemas and numeric
types, duplicate JSON keys, nonfinite/overflowed numbers, and invalid pins.
Only disposable negative-control copies are made writable. The accepted inputs
remain unchanged.

This tooling checks exact arithmetic, receipt consistency, and publication
integrity. It does not establish the general conjecture, certify imported
Floer/foliation theorems, independently recompute published knot signatures,
or show that abstract rank models are realized by knots.
