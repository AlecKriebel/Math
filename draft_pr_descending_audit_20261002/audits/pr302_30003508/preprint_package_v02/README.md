# Consistent spectral recovery of smooth reversible diffusion tensors at a fixed lag

Alec Kriebel, independent researcher, ORCID https://orcid.org/0009-0001-9320-500X.

The eight-page research note proves almost-sure consistency of a specified finite-rank empirical spectral-equation fit for a general smooth symmetric uniformly elliptic tensor S and unknown positive smooth invariant density mu. The known domain is bounded, connected and smooth, dimension at least2. The data are exact stationary positions at one known fixed positive lag, the reflecting condition is conormal, and fixed pointwise ellipticity/density bounds are known. Tensor and separately fitted divergence estimates converge locally uniformly; the ellipticity-clipped tensor converges globally in L2. The covariance is2S/mu and the interior drift is(div S)/mu. The fitted divergence is not obtained by differentiating the fitted tensor.

The note supplies the estimator, all-positive-mode retention, vanishing ridge, boundary-corrected empirical kernels, dependent-pair variance proof, full spectral-jet excitation and eigenvector-free measurability. This is a convergence analysis for the smooth setting of Reiss's original OWR24/2017 spectral reconstruction question. It does not assert a rate, computational efficiency, a numerical estimator implementation for general domains, or a theorem for rough/nonreversible models or added sensor noise.

Spectral residual fitting and eigenvalue-power weighting are established earlier methods. The manuscript and SOURCE_EDITIONS.md credit their predecessors and disclose the dated bounded priority audit, including the uninspected Crommelin–Vanden-Eijnden2011 publisher-final body. No unconditional worldwide firstness claim is made. The supplementary classical regularization argument is a new derivation during the audit of another possible consistency estimator; it is not evidence of an earlier publication of this diffusion application and does not prove the spectral estimator's convergence.

AI tools were used extensively in solving, checking and writing this work. The preprint is unrefereed and has not undergone human peer review. Independent AI adversaries are not human referees or a formal proof-assistant certificate.

## Contents and reproduction

- `spectral_tensor_consistency.tex` is the standalone source; the separately supplied PDF is its rendered note.
- `classical_regularization_application.md` and `independent_classical_derivation.md` give the supplementary alternative forward-kernel regularization argument and its independent mathematical reconstruction.
- `SOURCE_EDITIONS.md` records original-problem identity, decisive primary passages, inspected editions and access limits. Third-party PDFs and extracted bodies are not redistributed.
- `controls/` contains eight unchanged historical/current finite-control programs. `CONTROL_CASES.json` pins those programs and selects the scientific output fields compared with `EXPECTED_SCIENTIFIC_OUTPUTS.json`.
- `verify_package.py` checks the member manifest and replays every control in newly created writable copies. It writes only the requested new output directory and leaves package members unchanged.
- `record_metadata.json` is the exact intended Zenodo record metadata. The deposit-tool wrapper refers to the separately supplied PDF and verification ZIP, with the same metadata.
- `MANIFEST.json` records exact sizes and SHA256 hashes of the declared supplement payload. It excludes itself explicitly to avoid a circular hash. The outer ZIP checksum and separately supplied PDF checksum are recorded outside the ZIP.

Use Python3.9 or later, SymPy1.14.0, and optimization disabled. The runner refuses an optimized interpreter or a different SymPy version. From an unpacked bundle, run:

```text
python3 -E -B verify_package.py --output /absolute/path/to/new-replay-directory
```

The output directory must not already exist. The runner retains each executed source copy, actual child PID/argv/cwd/UTC timestamps, complete stdout/stderr, exit status, and scientific-output comparison. Algebraic values, labels and rational strings are compared exactly. A few illustrative floating-point diagnostics are compared with disclosed relative tolerance1e-12 and absolute tolerance1e-14; exact algebra/sign assertions within the programs still run. Process IDs, timestamps, interpreter paths, runtime-module inventories and other machine-dependent provenance are retained from the actual replay and are not expected to be byte-identical to historical receipts.

The controls check local differential jets, reflection moments, finite-rank signed kernels, repeated/negative/zero/small eigenvalues, pair covariance with shared endpoints, and excluded model/boundary cases. The original author checks retain their historical pending-status flags and author-turn counts; those fields are snapshots of their original dates, not the current preprint disposition. The rectangle/one-dimensional examples are local algebra controls outside the main smooth multidimensional class. Counts from different suites may overlap and do not constitute independent theorem proofs. The auxiliary suite supplies finite diagnostics without a single theorem-verification count.

Passing these programs does not prove the infinite-dimensional elliptic/statistical theorem, certify literature absence, implement statistical tensor estimation, or establish numerical performance. The mathematical proof is in the note and its supplementary derivation.

## License

The paper and original documentation are offered under CC BY4.0; the supplied original verification code is offered under the MIT license in LICENSE.txt. Third-party primary sources are cited under their own rights and excluded from the bundle.

The manuscript and verification materials retain their explicit unrefereed status. Internal AI verification does not constitute human peer review or a formal theorem certificate.
