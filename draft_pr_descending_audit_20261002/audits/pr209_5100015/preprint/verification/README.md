# Portable verification and evidence

This is the dated verification tree for the outer center-pedal invariant k303,b. The universal argument is in the research note and current PROOF.md; finite controls do not prove all periods or phases. Areas are signed in trajectory order; feet lie on the outer polygon's boundary tangent side lines. Strictly nested nondegenerate confocal elliptical caustics and periods not divisible by four are covered, including admitted stars/reversal/fixed repetitions. Hyperbolic/focal/collapsed caustics and filled-lobe areas are outside scope.

Use an existing Python installation with SymPy1.14.0 and mpmath1.3.0. Scientific replays used Python3.14.6; other versions are not certified. No installation or environment creation is performed. From this directory:

```
python -B integrity.py
python -B run_checks.py --output /absolute/path/to/new-k303b-replay --jobs 2
```

To exercise the actual harness orchestration with synthetic child failures, separately run:

```
python -B harness_failure_controls.py --output /absolute/path/to/new-k303b-failure-controls
```

These controls simulate successful/nonzero, timeout with binary partial output, launch failure and after-input integrity failure outcomes. They verify aggregate finalization and output/optimization guards. No scientific program is executed by this synthetic fixture test; actual eight-suite reproduction is the first command above. Fixture results are explicitly labelled.

The output must be a new separate directory outside the entire source archive. Optimized Python is rejected. Eight inspected, byte-bound original scientific programs run unchanged in isolated folders with -B and no network calls. The author and inherited checkers, exact Cartesian physical checks, source controls, meromorphic controls, exact contemporary comparison and classical-identity bridge are compared to frozen expected scientific outputs. Only explicitly recorded creation timestamps are ignored. With writable output storage, copied programs, raw stdout/stderr (including binary partial timeout output), outputs, per-suite timeout/launch/nonzero failure receipts and aggregate results remain in that output directory. Other completed suites and the after-input integrity check are retained on timeout or launch failure. Output storage failures can prevent receipt writing and must be resolved before claiming a completed run. Do not run scientific scripts directly in the frozen archive: several write adjacent receipts. The harness verifies all manifest files before and after without editing inputs. The verification manifest excludes itself; the outer source manifest binds it. Hashes do not certify mathematics.

The author checker has5660 exact assertions and4512 numerical diagnostics; the inherited checker has6195 exact assertions and6615 numerical diagnostics. Root exact geometry has340 assertions on six closed physical billiards: actual same-caustic reflection/tangency, center feet and tangent intersections, two triangle phases, a six-period equality and excluded four-period products32/50. The six-period inputs are inherited through PR209 from PR148, not new independent parameter discoveries. Additional scoped families have distinct physical, analytic and source mechanisms. Reports, derivations, complete failure/correction records and seals are under audits/. Historical pending-review or priority assessments retain their dated meaning.

The72,751-byte bad initial physical-control output is retained losslessly in FAILED_PROBE_01_COMPLETE.json.gz with hashes and deterministic recovery evidence. Temporary compaction and exact recovery are disclosed in FAILED_PROBES.md. Early physical-family diagnostics omitted -B; final/root replays used -B, and absence of all historical cache writes is not certified. A negative-control threshold correction and nondiscriminating wrong-construction samples are disclosed in actual reports. Failed probes are not passing theorem evidence.

Classical KLS2002 cyclic identities, KS2003/2004 Landen formulas, AST/BT2020 foot/velocity and hodograph mechanisms, Stachel canonical coordinates and conic/Jacobi/meromorphic methods are credited. Ferudun v1.1 Theorem2/Section6, DOI10.5281/zenodo.23088516, is the exact full contemporary theorem; v1.0 only covers the primitive even centered subset via its arbitrary-point theorem. Bounded priority leaves historical ordering, independent non-derivation and novelty undetermined. Server chronology and missing archive captures do not certify firstness. The additive author-update timestamp supplement preserves the original15payloads and seal; classical manual timestamp corrections are explicit.

original_submission/ preserves all23 native original files. audits/ preserves five scoped families; root_reproductions/ and audit_receipts/ retain actual checks and acceptance scope. Some historical receipts contain original absolute paths or hashes of private primary files. Those are provenance statements, not portable execution dependencies. Historical retrieval/inventory/manifest helpers document what ran; they are not offline harness inputs and should not be executed for reproduction. No downloaded third-party code runs. No third-party primary papers, extracted full texts, private transport bodies, secrets, caches or software environments are included.

Extensive AI tools supported solving, checking and writing, including separately prompted automated adversaries. This is unrefereed; no independent human peer review or formal verification is claimed. Required new sequential whole-package reviews and actual release receipts are separate case records outside the dated source ZIP, avoiding self-reference. This archive does not self-authorize publication.
