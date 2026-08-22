# Main referee software pass — preliminary static inspection

Timestamp: 2026-08-21 22:48 PDT. Read before executing any verifier/test and
before opening any committed JSON report, validation summary, or golden output.

## Scope read completely

- All nine modules in `code/src/bimolecular_pr/` (1,846 lines).
- All seven files in `code/tests/` (868 lines; 57 test methods).
- `pyproject.toml`, `build_backend.py`, `code/reproduce.sh`,
  `RUN_ALL_CHECKS.sh`, `manuscript/build.sh`, and the manifest/archive tools and
  their four safety tests.
- The code and packet README files, citation metadata, and
  `REPRODUCIBILITY.env`, only after the implementation and tests had been read.

No code or test was run in this pass.

## What the verifier actually establishes

| Check | Exact scope | Evidentiary value and limit |
|---|---|---|
| Falling-factorial increment | 3,318 cases: all enabled binary sources and carried targets in states `{0,...,4}^2`, with every binary outcome | Exact integer comparison of a direct residual-factorial quotient and the target/source quotient. Strong finite falsification of Lemma 3.2, not a proof for arbitrary dimension/state/molecularity. |
| Entropy rewrite | 172 reachable target/state combinations in two fixed two-species networks, with exact rational prime-log signatures | Exact algebraic comparison, including `0` and a parallel source. It does not establish the entropy bound's universal quantifiers, although that bound is elementary analytically. |
| Scalar envelope | Four `q` values (including two values above the manuscript's actual `q<=1` range), six `M` values per `q`, and three monotonicity points | Checks threshold classification and exact pointwise monotonicity. It does not independently optimize the logarithmic objective or prove finite backward propagation. |
| Lifted cycles/reachability | Two fixed weakly reversible examples, small states, one finite parity shell, and one absorbing singleton | Concrete exact witnesses for zero, boundary, multiple-linkage, parallel, same-displacement, parity and absorption behavior. It does not exhaust weakly reversible graphs. |
| ACK worked example | Two rate vectors and `n=2,...,12`, comparing a generic exact signature with a specialized closed form; sign of asymptotic coefficient | A meaningful independent-interface check of the displayed episode, still finite. |
| Top-complex atlas | All 1,013 subsets with at least two elements of the ten three-species binary complexes; 55 rational weights from denominator totals 1–6; all 97 weight/divergent-support pairs; 98,261 certificates | Exhaustive over the explicitly finite atlas. The validator recomputes the top set and verifies height/availability or invariant certificates without calling the classifier. It is not exhaustive over all real weights, species dimensions, networks, or divergent sequences. |
| Random top stress | 5,000 fixed-seed four-species cases | Deterministic stress evidence only, correctly labelled as not proof. |
| Calibrations | 17 Boolean checks plus focused unit tests | Checks selected boundary facts, rate-limit formulas, one stopped-Foster toy transition, two finite stationary cycles, and absorbing point mass. These are examples, not implementations of the general recurrence argument. |
| Packaging | deterministic wheel, source hashes, canonical JSON, two regenerations, golden-byte comparison | Genuinely regenerates output in temporary files; it does not copy the golden report. |
| Release integrity | packet checksum inventory, durable-tree manifest, identical report copies, four PDF rebuilds, ZIP rebuild | Designed to fail on missing, changed, unexpected, unsafe, nondeterministic, or non-byte-identical artifacts, subject to the manifests themselves being supplied rather than externally authenticated. |

## Hard-coded values and circularity assessment

- The three-species atlas counts/digest, random counts/digest, fixed RNG seed,
  wheel digest, and numerous small expected fractions are hard-coded.
- The atlas and random data are nevertheless recomputed from cases, and every
  top certificate is validated before the hard-coded aggregate comparison.
  Hard-coding supplies regression/determinism checks, not the underlying
  result.
- Several unit tests duplicate a specialized production formula almost
  verbatim (notably the finite rate-degeneration recursion), so those detect
  accidental change better than conceptual error. The ACK check is stronger:
  it compares the specialized form with a generic source-by-source factorial
  calculation.
- The canonical report is generated twice in fresh temporary paths and then
  compared to the committed report without overwriting it. This is genuine
  regeneration.

## Fail-closed and determinism analysis

- `SOURCE_FILES` is closed over the fixed metadata/build files and every `.py`
  file discovered under `src/` and `tests/`; an unexpected Python module/test
  raises. A missing fixed file still fails when it is hashed. Non-Python files
  outside the explicit list are intentionally not verifier sources.
- Exact `Fraction` arithmetic, sorted collections, canonical JSON, a local
  `random.Random(20260806)`, and `PYTHONHASHSEED=0` remove relevant numerical and
  ordering nondeterminism.
- `reproduce.sh` enforces Python >=3.11 but does not reject future versions;
  its README accurately limits empirical byte-reproduction claims to CPython
  3.11–3.14. The current `python3` 3.14.6 lies in that range.
- The PDF builder requires exactly Tectonic 0.16.9 and pins the TeX bundle URL
  and content digest. The release archive fixes timestamps, ordering,
  compression, permissions, and members.
- The durable manifest rejects missing, changed, unexpected, and symbolic-link
  entries except explicitly documented scratch/cache patterns. The packet
  checksum layer covers every packet file except its checksum file itself.
- These hashes prove consistency with the supplied manifests, not authenticity
  of the copied packet or Git provenance.

## Manuscript claims not implemented

There is no general executable check of marked-chain irreducibility or exact
projection, potential properness, arbitrary episode recursion, normalized-log
subsequence extraction, the analytic real-weight trichotomy, finiteness or
nonemptiness of `K`, stopped-process integrability, finite-trace conversion,
CTMC nonexplosion/physical return, or the regenerative theorem. The software
uses a few finite calibrations for these interfaces. The manuscript and README
explicitly say computation is not the universal proof, so this limitation is
represented accurately.

## Static findings

1. No substantive implementation error was found in the inspected finite
   checks.
2. The standalone verifier intentionally remains software version 1.2.0 while
   the outer packet is manuscript/release 1.2.4; the submission README states
   this explicitly, so it is not an internal version discrepancy.
3. The manuscript claims availability in a tagged Version 1.2.4 repository,
   but the copied packet has no `.git`, and local matching tags stop at v1.2.3.
   This is a provenance/availability issue to verify against the remote after
   the blind phase, not a software-theorem defect.

## Planned post-replay challenges

- Independent factorial/episode oracles using no package imports.
- Independent finite top-certificate oracle and small-network search.
- Disposable-copy mutations of a mathematical helper, fixed expected digest,
  committed report, source allowlist, manifest member, PDF, and archive, each
  expected to make the relevant layer fail.
- Byte-level rebuild and report-copy comparisons, plus an inventory check that
  no skipped step is treated as passing.

Preliminary static result: pass for the claims the code actually makes, with
finite scope clearly separated from the analytic theorem.

