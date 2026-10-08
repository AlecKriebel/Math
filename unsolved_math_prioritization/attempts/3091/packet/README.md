# Generalised empty hexagons: public mathematical derivative

3091 / OPG-59923; rank 1058. **Exhausted, 5/5; full target unresolved.**

This public-only derivative retains the accepted mathematical report, native
geometry checker, authored fixtures and independent Caratheodory oracle unchanged.
The audit is explicitly labeled as a derivative: its proof-by-proof review is
preserved, and original full-packet inventory claims are replaced by public scope.
New manifests bind only files in this directory. No original private-packet
manifest/archive identity, excluded-file metadata or full-original replay claim
is included. Bibliographic and dataset metadata are public and source-free.

## Replay

Authenticate BOOTSTRAP.py against the external SHA-256 supplied in the PR body
and acceptance report before executing it. Integrity checks use Python 3.10+ standard library:

    python3 -I -S -B BOOTSTRAP.py /absolute/path/to/packet --integrity-only

Full exact-output replay requires Python 3.12.14, the version recorded by the
pinned expected outputs. There is no path, version or mode normalization.

For full replay, make a disposable copy with all directory modes 0555 and all
files 0444, use actual/effective UID 1000, and run from any working directory:

    python3 -I -S -B /trusted/path/BOOTSTRAP.py /absolute/path/to/readonly-packet

Repeat with -O and -OO. The bootstrap is kept external and fixed in tampering
tests. Rewritten attacker bootstraps are not trust anchors. The wrapper rejects
missing/extra files, extra directories, symlinks, FIFOs, unsafe paths, incorrect
hashes/byte counts, bad JSON field types, duplicate keys and nonfinite numbers,
including exponent overflow. Authentication precedes native-code execution.

The fresh public-only replay runs native geometry and the independent oracle in
all three modes. It retains complete stdout/stderr and parsed results, exact finite
counts, 24 precise semantic mutation rejections, and public before/after inventories.
The original whole-packet integrity checker is deliberately not run; fresh
public-only integrity is supplied by the new manifests and wrapper instead.

The semantic mutants include ignored closed-edge blockers, farthest-ear selection,
an incorrect slab constant and corrupted fixtures. Exact intended errors are
required; arbitrary crashes are not passes. Read-only native input and cwd writes
must fail with PermissionError under UID 1000. Input bytes remain unchanged.
These permission-mode tests do not constitute an OS sandbox.

Run the fixed-bootstrap and strict-schema controls with:

    python3 -I -S -B TEST_MUTATIONS.py /absolute/path/to/packet

They also cover hostile cwd/PYTHONPATH imports in all three modes. The publication
matrix runs full replay from a hostile read-only cwd with PYTHONPATH/PYTHONSTARTUP.

Optional --source-dir DIR supplies nine public source files by retrieval label.
--problems FILE and --research-results FILE must be supplied together. These
options rehash public bytes only. Without them, fresh sources/corpora say NOT_RUN.
Fresh download, source inspection, dataset join, SAT replay, Lean build and the
29-point witness check remain NOT_RUN in this wrapper. Historical inspection is
separately described in the source audit; no source body is redistributed.

Universal mathematics depends on the proof report and independent review, not
finite checks. H=30, the pentagon bound and the 29-point witness are literature
dependencies. The all-ell conjecture and ell=4 remain unresolved; no novelty claim.

EXPECTED_OUTPUTS.json pins complete native stdout/stderr/exit/results, the full
public audit and every semantic outcome. Fresh outputs must match with exact JSON
types and ordered arrays. TEST_OUTPUT_COMPARISON.py tests 22 altered-output cases
in all three modes, including plausible counts, extra fields and output bytes.
The expectations come from the initial public-only replay; mathematical acceptance
still rests on the separately reviewed proof, not on regression self-agreement.
