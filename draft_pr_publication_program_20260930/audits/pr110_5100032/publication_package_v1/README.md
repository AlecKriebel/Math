# A telescoping proof of the focal antipedal sum invariant

Alec Kriebel, independent researcher; ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Version 1.0, 6 October 2026. CC BY 4.0.

The self-contained note proves the ordinary positive focal antipedal distance-sum equality observed by Reznik, Garcia and Koiller as invariant k603. The outer ellipse has a > b > 0, and its strictly nested confocal elliptical caustic has 0 < lambda < b². The proof covers every regular closed admitted billiard/Poncelet orbit, including odd primitive periods, stars, reversal and repeated traversal. It does not assert that either individual sum is constant through its family, or extend to hyperbolic or degenerate caustics.

For each edge, the two antipedal vertices are intersections of the lines through the original endpoints perpendicular to their respective focal rays. The norm difference equals Gamma times the vertical displacement after choosing a consistent caustic-on-left orientation. Reversing endpoints preserves the norm difference and reverses the displacement coefficient. Closure proves equality of the sums.

## Files and reproducibility

- `focal_antipedal_sum.tex`: standalone manuscript source, including bibliography and disclosure.
- `verify.py`: standard-library exact rational-chord verifier, with active explicit guards in both normal and optimized Python.
- `run_verification.py`: executes normal and optimized verification and eight mandatory deliberately invalid subprocess runs.
- `verification_normal.json`, `verification_optimized.json`, `execution_envelope.json`: actual executed results and compact process receipts, with real child PIDs, UTC endpoints, exit codes and stream hashes.
- `proof_binding.json`: binds verification to the exact manuscript bytes.
- `source_audit_summary.md`, `input_pins.json`: bounded provenance, attribution and exact preserved research-input references.
- `intended_zenodo_metadata.json`, `zenodo-deposit.json`: identical intended metadata; the latter plans the adjacent PDF and support ZIP file names.
- `LICENSE`, `RESEARCH_LOG.md`: licensing and preparation checkpoints.
- `seal_source_payload.py`, `source_payload_manifest.json`, `source_seal_receipt.json`: source integrity validation and the actual authored-source seal.

Use Python 3.10 or newer; no packages or network are required. Run the
following commands in an extracted or disposable scratch copy. In particular,
the runner writes new execution receipts beside itself; use a copy to preserve
the immutable sealed source package:

```sh
python3 verify.py
python3 -O verify.py
python3 run_verification.py
```

Each positive run checks 1,456 directed chord cases with 63,346 passing explicit guards. This includes 714 paired reversal cases, 80 horizontal chords, and coefficient signs negative/zero/positive in 1,040/60/356 cases. Three closed-cycle controls use a genuine four-cycle, its triple traversal and its reversed triple traversal. All four mandatory incorrect coefficient, focal height, norm sign and manuscript binding controls are rejected internally in each positive run. The runner also requires each of these four independently invoked faulty processes to exit with the expected rejection in both normal and optimized mode: eight required failures. These counts describe finite exact controls, not the scope of the written all-real/all-period theorem. No finite closed odd orbit is claimed checked by this program; the manuscript proof covers odd periods without a parity assumption.

The program solves both antipedal defining equations independently. For a rational chord it uses the unnormalized support normal `(alpha,beta)=(delta_y,-delta_x)`, with its sign chosen for positive support `w`. Writing `T=alpha²+beta²` and `K=a²alpha²+b²beta²`, tangency gives `lambda=(K-w²)/T`. The exact solver norm is compared to `T (R_sigma/H_sigma)²`, with `H_sigma=w-sigma c alpha > 0`. An exact rational square root of `K-w²` removes the common square-root scale in the coboundary check. No approximation, division by the vertical displacement, or division by Gamma is used.

The binding file must be regenerated and verification rerun after any manuscript edit. The execution files record this particular run; rerunning the runner replaces those receipts and therefore changes their source-manifest hashes. The sealing script checks exact input references in the surrounding repository audit folder and is intended for the author's original custody environment. The verifier itself is portable and needs only the adjacent manuscript and binding file.

## Attribution, status and planned deposit

The observation is credited to Reznik–Garcia–Koiller, *Eighty New Invariants of N-Periodics in the Elliptic Billiard*, arXiv:2004.12497v11, and the published *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, DOI [10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y). Classical antipedal geometry, the known focal-height product, centrally symmetric cases and generic telescoping are credited as background. The candidate addition is the ordinary-positive per-edge norm-difference reduction and full-period proof.

A bounded primary-source audit completed on 6 October 2026 found no earlier full covering result. The complete journal final *Estimating Elliptic Billiard Invariants with Spatial Integrals*, DOI [10.1007/s10883-022-09608-y](https://doi.org/10.1007/s10883-022-09608-y), and its precursor were compared in full; that selected comparison is cleared. The remaining finite-corpus and version limits are explicit in `source_audit_summary.md`. No absolute-first, exhaustive-literature or continued-open-status guarantee is made.

AI tools were used extensively in solving, deriving, drafting, literature checking, code generation, verification and adversarial checking. Independent AI-agent checks are not conventional human peer review. This manuscript is unrefereed and has not received conventional human peer review.

The deposit manifest plans adjacent files `focal_antipedal_sum.pdf` and `focal_antipedal_sum_support.zip`. They are not generated by this source-only preparation step. Compilation, visual layout review, archive assembly and fresh whole-package reviews are separate root responsibilities. Metadata preparation and this source seal are not publication, merging or deposition authorization. This directory contains no third-party PDFs, extracts, images, raw source/web/UI bodies, credentials or huge operational receipts. Historical source evidence and old pending gates remain preserved in the surrounding audit folder.
