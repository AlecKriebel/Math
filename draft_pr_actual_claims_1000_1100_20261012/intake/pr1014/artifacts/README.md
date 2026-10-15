# Equal-pressure foam cells: accepted scoped partial results

The full global finite-type question, tetrahedral and dodecahedral occurrence, and two-faced continuation remain unresolved after 5/5 approaches. Read `current/RESULTS.md` and the complete `audit/AUDIT.md`. The accepted current and audit directories, including their checkers and public metadata, are byte-preserved.

The norm-one edge-curvature budget is necessary under the simple ball-cell, disk-face, interval-border and finite-curvature hypotheses. The local plane/two-catenoid annuli are truncated patches, not completed minimal disks or a global foam. Compact stationarity needs compact support, finite area, no external boundary and minimal interfaces. Finite types require a uniform per-cell Q+T bound that is not proved. N=9 is only a count threshold.

## Verification

First authenticate `BOOTSTRAP.py` against an independently supplied SHA-256 (for example the reviewed PR description), and retain that authenticated copy outside the packet. The final bootstrap authenticates the entire manifest, acceptance, all receipts and executable checks. Run the external copy as follows, replacing the paths:

- `python -I -S -B /trusted/BOOTSTRAP.py /path/to/packet`
- `python -I -S -B -O /trusted/BOOTSTRAP.py /path/to/packet`
- `python -I -S -B -OO /trusted/BOOTSTRAP.py /path/to/packet`

Add `--controls` before the packet path to run integrity, schema, comparator and hostile-environment controls. Actual UID=EUID=1000 is required. Set all packet directories to 0555 and all files to 0444 before execution. The validator performs real create/append denial probes. This is an accidental-write barrier, not kernel immutability or protection against intentional chmod by the owner.

The unchanged checkers perform 56 original checks with 7 input-validation controls and 227 independent checks including read-only preflight. Sixteen semantic mutants are exercised separately: 10 geometry/algebra mutations and 6 hypothesis/status guards. Full fresh stdout/stderr must match pinned per-mode references byte-for-byte with exact recursive JSON types and no normalization. These checks do not constitute formal proofs of analytic results or global realizability.

`PREPARATION_RECEIPT.json` and `PREPARATION_CONTROLS_*` are explicitly pre-seal evidence. The final external noncircular receipt remains outside this packet and its pin is supplied in the reviewed PR description. Historical acceptance, source retrieval and inspection are labeled historical; the old audit harness, old report, historical patch application, source-body replay, dataset replay, new source search and formal proof-assistant verification are NOT_RUN here. The corrected current report and unchanged safe mathematical programs are freshly replayed.

Kusner's ResearchGate HTML preview provenance remains unverified; no inspected Kusner PDF is claimed. All copied third-party source bodies, datasets, private sources, private coordination and identifying metadata are excluded. No QUEUE changes are included.
