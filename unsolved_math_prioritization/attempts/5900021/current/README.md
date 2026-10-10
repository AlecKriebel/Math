# Scoped equal-pressure foam-cell analysis

Target: Sullivan–Morgan (1996), Problem 21; catalogue identifier 5900021.

Status: **partial results with the full target unresolved**. Five bounded approaches were completed after primary-source recovery. This packet contains authored analysis and public-source verification metadata only.

Read `RESULTS.md` for the exact hypotheses, complete elementary proofs, five approach gaps and source distinctions. The strongest direct cellwise conclusion is a necessary total-edge-curvature budget for a sufficiently regular simple cell. Tetrahedral and dodecahedral occurrence, and finiteness of all cell types, are not settled.

## Reproduce checks

Run `python verify.py`, `python -O verify.py`, and `python -OO verify.py` from this directory. The checker uses only the Python standard library and prints a JSON report. It makes no network requests, writes no files and requires no source PDFs or private records. All 56 checks and 7 negative controls remain active under optimization. Decimal values are display only; the interval decisions use exact rational arithmetic.

`VALIDATION.json` records the observed three-mode agreement. `SOURCE_MANIFEST.json` identifies inspected sources, hashes where byte retrieval succeeded, and failed/wrong-file retrieval distinctions. No copied source document is included in this authored packet.

No publication, remote mutation or repository queue change is performed by these files.

## Independent audit derivative

The original authored inputs are preserved outside this derivative. The clarification patch is in `../audit/CORRECTION.patch`. The added `CLAIMS.json` records the exact statements tested independently; `STATUS.json` retains the full unresolved target and five exhausted approaches.

Run `python -B ../audit/check_independent.py --require-readonly` from this directory after extracting the full source-free bundle and preserving its read-only permissions. Repeat with `-O` and `-OO`. If an extractor removes those permissions, either restore directories to mode 0555 and files to 0444 or omit the read-only preflight while retaining the integrity and arithmetic checks. The independent checker prints to stdout by default; `--output /external/new-report.json` uses exclusive creation outside both protected payloads.

The original `VALIDATION.json` describes the unchanged original `verify.py`; the independent acceptance receipt is a separate file. The accepted bundle contains no copied source PDFs, source text, datasets, or coordination records.
