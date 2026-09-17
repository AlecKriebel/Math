# Literal source simple spectra

Checkpoint 2026-09-15T04:15Z. Source spectral appendix proof implementation 100% compiled; focused axiom probe pending. Scope is source simple spectra, not the unrelated remaining Qqa-to-Qqc reconstruction.

`GeneralCoverageSourceSpectrum.lean` proves the exact source relative matrix has spectrum equal to the full set of shifted roots `equalityRoot a`, each with eigenspace dimension one. Its characteristic polynomial is exactly `X^d - C((-1)^(d-1))`. The proof normalizes its actual weights `chi(y-j-1)` by `star(equalityBase d)` and uses the previously verified product-one weighted-cycle eigenbasis.

For the literal source coefficient matrix `sourceBob y`, the proof constructs the unitary matrix whose columns are those normalized relative-matrix eigenvectors. The source positive-clock adjoint takes column a to column a+1. Consequently `sourceBob y` transposed is intertwined with the actual product-one weighted cycle whose weight at a is `star(polarBase(a+1))`. The full simple spectrum of that cycle transfers by unitary similarity and then by transpose invariance of rank/nullity. The final statement gives `MatrixSpectrum(sourceBob y) = Set.range chi` and dimension one for every root eigenspace.

No simple-spectrum, invertibility, factorization, or valid-measurement premise has been added to these final results. The hypotheses are only the dimension bound d≥2 and a source setting y. Existing independently compiled source unitarity and order theorems exclude any additional spectral values; our explicit similarity supplies all eigenvalues and their multiplicities.

Independent semantic review by the semantics agent checked the positive-clock/Fourier sign, the a→a+1 shift, the conjugated weights, product one, the preservation of the same eigenvalue under transposition, and the literal source-matrix endpoint signatures. It found no central flaw or circular hypothesis.

Normal build checkpoint: `lake build CyclicBell.GeneralCoverageSourceSpectrum` exited 0 and reported Build completed successfully. Evidence: `coverage_source_spectrum_build.log`.

Axiom audit checkpoint: `lake env lean repair_audit_2026-09-14/SourceSpectrumAxioms.lean` exited 0. All six endpoints depend only on `propext`, `Classical.choice`, and `Quot.sound`; see `source_spectrum_axioms.log`. Source spectral task completion: 100% compiled and audited.
