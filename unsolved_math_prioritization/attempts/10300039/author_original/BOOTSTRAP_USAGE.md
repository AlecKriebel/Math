# Replaying the frozen author checkpoint

The bundle is source-free and includes authored mathematics, public identity metadata, finite diagnostics, and an external manifest. No source PDFs, excerpts, imported dataset records, or private coordination are included. The original question remains unsolved, 5/5. Independent review is pending.

Authenticate bootstrap.py against its SHA-256 supplied separately by the trusted sender before running it. PINS.json describes these values but is not its own external trust anchor. Then:

    python3 -I -S -B bootstrap.py
    python3 -I -S -B -O bootstrap.py
    python3 -I -S -B -OO bootstrap.py

The bootstrap authenticates the complete exact bundle inventory, manifest pin, archive pin, each ZIP member, and each expanded copy before executing authenticated inner code in a fresh temporary directory. Verification can run with the original distribution read-only. It assumes a trusted Python 3 standard library, interpreter, operating system, supplied external trust anchor, and quiescent filesystem. It does not claim resistance to concurrent filesystem races or a compromised runtime.

Optional complete external source binding:

    python3 -I -S -B bootstrap.py --problems /path/to/problems.json --reports /path/to/research_results.json --sources /path/to/private/pdf/directory

Both complete corpora must match pinned byte counts and hashes before target records are compared. Source PDF checks authenticate bytes, not their truth. The source directory's five PDF filenames are public in SOURCE_METADATA.json. Sources remain external and are never uploaded by this command.

For adverse controls, first set the distribution files read-only and its directories nonwritable, then:

    python3 -I -S -B controls.py

Run this as an ordinary non-root user. The harness makes only disposable mutation copies writable; it checks normal, -O, -OO, read-only relocated replay, missing/extra/changed files, links, malformed metadata, unknown options, malformed external input, and a malicious-code sentinel. Frozen source bytes are checked again afterward. These tests are finite integrity controls, not mathematical proof.

No remote writes, commits, PR publication, merge, or release were performed in this checkpoint. Later review should preserve the freeze and attach any correction as a separately identified version.
