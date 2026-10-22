# Prior solution audit: prescribed boundary zero sets

Read author/ACCEPTANCE_REPORT.md, audit/AUDIT_REPORT.md, and ACCEPTANCE.md for the mathematical conclusion and explicit imported dependencies.

## Authentication and offline replay

Use Python 3.10+ on POSIX as a real non-root user. No packages or network are required. Obtain BOOTSTRAP.py's exact byte count and SHA-256 from the independently reviewed PR or trusted commit, and verify them before executing any downloaded code. A script cannot authenticate itself merely by printing PASS. A hash stored alongside untrusted code is not an external trust anchor.

After authenticating BOOTSTRAP.py, run from any ordinary directory:

    python3 -I -S -B BOOTSTRAP.py PACKET_DIRECTORY
    python3 -I -S -B -O BOOTSTRAP.py PACKET_DIRECTORY
    python3 -I -S -B -OO BOOTSTRAP.py PACKET_DIRECTORY

The bootstrap pins the wrapper and manifest, then executes the authenticated wrapper bytes in memory. The manifest covers every payload including the wrapper; bootstrap and manifest are separately pinned. Exact recursive inventory includes both of them. The wrapper fixes all 15 accepted author/audit identities independently, parses all JSON with duplicate-key/nonfinite/exponent-overflow rejection, uses exact types, and authenticates bytes before any child execution. Only authenticated snapshots are copied into isolated disposable replay directories. The unchanged audit harness receives a writable temporary author copy because its mutation fixtures inherit permissions; its own actual read-only probes and all mutation cases still execute unchanged.

Each source-free replay reproduces 301 historical expected outcomes, including all three Python optimization modes within the preserved harness. It explicitly reports the other 36 source cases as omitted and current source checks as NOT_RUN. The historical 337-case receipt is preserved, not relabeled as a fresh full-input result.

## Publication-boundary controls

After authentication and a successful replay:

    python3 -I -S -B mutation_tests.py PACKET_DIRECTORY

The suite tests normal, -O and -OO execution, hostile Python environment variables and import files, a genuinely read-only whole packet and cwd, missing/extra files, symlinks, FIFO, same-size modifications, hostile child replacements, and rehashed hostile manifests. It also reaches strict JSON/type helpers directly. All mutations are disposable; copytree-preserved read-only modes are made writable only in those disposable mutation copies.

All accepted bytes remain unchanged before and after replay. No source inputs are sought automatically. Optional source verification remains available separately through the unchanged audit checker, with the externally supplied public PDF identities in audit/SOURCE_AUDIT.json. Its execution is outside the default source-free publication replay.

## Limits

Trusted interpreter, standard library, stable filesystem, and cryptographic hash assumptions apply. This is not an arbitrary-code sandbox, a hostile concurrent-filesystem defense, or a universal analytic proof checker. Read-only tests prove the tested creation/append operations were denied to the actual non-root UID. Local replay is separate from GitHub CI; zero checks means NOT_RUN, never a CI pass.
