# Odd two-torsion theta partial results: target 30001576

**Unresolved, five of five proof routes used.** This source-free draft packet
publishes independently accepted bounded partial results, with explicit
interface clarifications. It gives neither an all-genus solution nor a
counterexample, novelty certification, or journal-acceptance claim.

## Reading order and exact scope

1. `current/PARTIAL_RESULTS.md` is the current full proof, obtained by applying
   the preserved contextual `current/PROOF_INTERFACE_PATCH.diff` with zero
   fuzz and no offset. The full superseded proof is omitted.
2. `current/AUDIT.md` is the complete independent audit. The full
   `current/PROOF_INTERFACE_ADDENDUM.md` supplies the all-genus coefficient
   derivation and precise imported theorem interfaces. Both are unchanged.
3. `ACCEPTANCE.json`, `ACCEPTANCE.md`, and `STATUS.json` state the current
   bounded disposition. `historical/` holds only selected public metadata,
   the prior acceptance, and the authored source/scope audit. A historical
   statement that no publication occurred describes that earlier audit stage.

The target concerns the reduced support of the interior locus in complex
ppav moduli, including decomposables. Empty genera one and two are vacuous.
The accepted local diagonal statement applies to the specified three-odd
characteristic where every residual coefficient is nonzero. Its convergent
proof works in each genus; finite jet tests are not all-genus evidence.
The rank-one argument is conditional on actual access to that open boundary
stratum and the lower-genus codimension hypothesis. Jacobian rank three at
the specified diagonal point does not give scheme smoothness when g>3.
The 2023 finite-jet criterion critique does not refute the theta theorem.
No argument here specializes an arbitrary global component to the required
diagonal locus or rank-one boundary.

## Finite checker contract

Both `current/check_formal_jets.py` and `current/independent_checks.py` are
preserved byte-for-byte. The original has explicit guards, writes only
stdout, and is optimization-safe. Its original comparisons do not detect
removing repeated-edge factorials. The independent ordered-word checker
compares the full third jet, including 1/6 and 1/2 coefficients, and rejects
that mutation. Six independent mathematical controls alter factorials,
heat scaling, cross multiplicity, elimination sign, residual coefficient,
or Fourier lead. Two positive runs and those six exact-reason rejections
are required per mode; delivery-integrity controls add no mathematical scope.

`current/CHECK_RESULTS.json` and `current/INDEPENDENT_CHECK_RESULTS.json` are
the original positive raw outputs. `FINITE_CONTRACT.json` fixes all eight
case identities and complete stdout/stderr/exit expectations. The three
`run_finite_checks.mode*.reference.*` pairs are fresh complete suite outputs,
with mode identity retained. Recursive exact types distinguish integers
from booleans and floats. No output normalization or PASS-only acceptance
is used. `CHECK_RUNS.json` records pre-seal capture, not the final gate.

## Trusted execution and noncircular authentication

Trust the CPython runtime and its standard library, installed SymPy 1.14.0
and mpmath 1.3.0, and an externally obtained bootstrap SHA-256. The runtime
and installed packages are explicit dependencies, not vendored or fully
cryptographically attested by this packet. `run_checker.py` requires
`-I -S -B`, actual UID/EUID 1000, and those exact package versions. It appends
only the installation's explicit package directory under the runtime prefix;
it does not run site processing or .pth files. It checks both package origins
before importing, never imports from the packet or current working directory,
and fails on unsupported versions. It neither installs dependencies nor
silently falls back to another import route. Direct unisolated execution of
the preserved original scripts is outside the supported trust path.

Obtain `BOOTSTRAP.py` and its SHA-256 from an independently trusted receipt
or reviewed PR body. Verify that hash externally, keep that exact copy outside
the packet, and run it against the packet root. Do not trust a bootstrap hash
learned only from an untrusted packet. For example, after external hash checking:

    python -I -S -B /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet
    python -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet

Use `--controls` before the packet argument for the full hostile/control
suite. Run as UID/EUID 1000 after making every file mode 0444 and every packet
directory mode 0555. A fresh Git checkout needs these modes set before replay.
The gate performs real create, append-open and unlink denial probes. Both
baseline and full controls hash the whole packet before and after replay.

The external bootstrap fixes the whole manifest, verifier, and control
harness before execution. The manifest lists every payload file, including
all reference outputs and executable code; it excludes itself and the
bootstrap to avoid a hash cycle. The external bootstrap also requires its
packet copy to be identical. Exact inventory, single-link ordinary files,
no symbolic ancestors, strict JSON schemas, complete output equality, and
hostile cwd/Python-environment checks are enforced. Final gate receipts and
external trust anchors stay outside the packet because including receipts
that hash themselves would be circular.

## Explicit exclusions

Historical filenames mentioned by the unchanged audit describe its original
snapshot. Only the files in this packet's manifest are final-replay inputs.
No copied source PDFs or text, datasets, private sources, or private
coordination material are included. No identifying metadata of excluded
private files is published. There is no queue change or unrelated work.
The original audit harness, original snapshot harness, pre-seal capture
harness, historical receipt replay, superseded full proof replay, source-body
replay, new source search, dataset replay, formal proof-assistant verification,
global all-genus verification, arbitrary-period-matrix evaluation, and
independent reproof of imported dimension theorems are all **NOT_RUN** in the
final public replay. Existing public-source inspection metadata is historical,
not a claim of fresh publication-stage retrieval.
