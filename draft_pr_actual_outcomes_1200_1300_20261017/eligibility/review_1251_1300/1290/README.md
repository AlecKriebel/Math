# Positive coarse curvature without a nonreversible L2 gap

Problem 4000005 (AMR-039-0005), “Non-reversible spectral gap,” concerns Problem E in Yann Ollivier's open-problem list. This package gives an attributed, checked reconstruction of the known negative answer to an unrestricted nonreversible L2-gap extension. It does not settle every question or possible additional hypothesis in Problem E.

The basic Bernoulli-prepending counterexample is credited to Fu-Zhou Gong and Li-Ming Wu in Gong, Liu and Wen, *Ricci curvature of Markov chains on Polish spaces revisited*, Osaka J. Math. 50 (2013), 491–502, §3, p. 495. No novelty or priority is claimed. The full mathematical argument is in [PROOF.md](PROOF.md); its accepted text is preserved byte-for-byte.

## Mathematical conclusions

For each 0<a<1, the example has compact Polish state space, a Feller kernel, a unique full-support invariant probability, and coarse Ricci curvature exactly 1−a. On complex mean-zero L2, its spectrum is the closed unit disk, its spectral radius is one, and every positive power has norm one. Nevertheless each fixed mean-zero L2 observable tends strongly to zero under iteration. Lipschitz-norm contraction remains valid.

Variance has no finite uniform bound by the ordinary jump energy, the squared residual norm, or the one-step conditional-variance energy displayed in the proof. These are three different quantities. The infinite example is topologically irreducible, but is not irreducible for its stationary measure or any common nonzero irreducibility measure; no conclusion is asserted for an additionally imposed Harris-irreducible class.

The finite length-L truncations are irreducible and aperiodic, retain curvature at least 1−a, and have mean-zero spectral radius zero. Their exact ordinary Poincaré gap is 1−cos(π/(L+1)), so the sharp Poincaré constants diverge quadratically. The proof covers every function through Walsh-character shift blocks. The finite-rank realizations converge strongly to the infinite operator, without operator-norm convergence or a uniform exponential-decay prefactor. This isolates a failure of a naive finite-approximation inference; stronger approximation theorems remain outside the claim.

## Two source corrections and their limits

Under the published prepending convention, direct adjoint computation gives PP*=I, while P*P is a proper conditional-expectation projection. The printed reversed identity on Gong–Liu–Wen p. 495 is rejected by the nonzero first-coordinate character killed by P. This is a local algebraic correction under an explicit convention, not an official erratum and not a claim that the published spectral-radius conclusion is false.

The inspected Erbar–Fathi arXiv:1612.00514v1 assumes a finite, irreducible, reversible, continuous-time chain and uses entropic Ricci curvature. It does not substantiate an attributed extension to nonreversible coarse-curvature bounds. This source-level mismatch implies no blanket statement about all later nonreversible literature. Ollivier's reversible spectral-gap theorem and nonlocal blurred-gradient inequalities are not contradicted.

## Files and evidence

- [PROOF.md](PROOF.md): complete construction and proof, including exact curvature, spectrum, norm, three energies, irreducibility, and the exact finite gap.
- [AUDIT.md](AUDIT.md): mathematical audit and bounded record recommendation.
- [ACCEPTANCE.json](ACCEPTANCE.json): acceptance scope, exclusions, and content bindings.
- [SOURCE_PINS.json](SOURCE_PINS.json): scholarly titles, public URLs, source hashes/sizes, page locators, and retrieval/inspection limits.
- [CHECK_RESULTS.json](CHECK_RESULTS.json) and [CHECK_SUMMARY.json](CHECK_SUMMARY.json): aggregate numerical and preservation evidence.
- [MANIFEST.json](MANIFEST.json): closed public file inventory and hashes.

All 110 retained checks pass under ordinary Python, -O, and -OO. Exact finite arithmetic and rational transport checks support the exposition; floating-point eigenvalues only corroborate the independently proved exact gap. Neither the calculations nor this AI-assisted assessment constitute external human peer review or formal proof-assistant certification. Only selected source definitions, statements, hypotheses, attribution, and the relevant printed identity were inspected. The full articles were not independently audited.

The public package contains authored mathematical exposition and verification/source metadata. It contains no source PDFs, extracts, page images, datasets, scripts, or coordination records. Public source links can change; the listed hashes identify the inspected bytes.
