# Reproducibility

From this directory run:

```sh
python3 verify_exact.py
```

Requirements: Python 3.8+ standard library only. No installation, network access, source download, private corpus, or environment secret is required. The expected result is PASS with 28,156 exact assertions. CONTROL_RESULT.json records the author execution. The optional --write-result argument regenerates that JSON in the current authored directory; omit it when auditing an immutable copy.

The control families independently calculate Gamma and Gamma2 from a finite reset generator; verify rational indicator and continuous-tent BE witnesses; check the exact factorization and sufficient quadratic bound used in the universal coupling proof; verify the time parameter inequality in the literature-to-W1 transfer; and test normalization identities. They also check source metadata shape and key scope declarations. Numerical integration or floating-point Gaussian simulation is not used as evidence.

Analytic facts such as Gaussian tails, compactness, coupling validity, the universal quantifiers, and the cited primary theorems must be checked from FULL_PROOFS.md and the cited original literature. Finite exact tests do not replace those arguments. In particular, a passing script does not mean the original problem is solved.

SOURCE_VERIFICATION.json supplies public URLs, PDF hashes, byte counts and inspection coverage. Independently fetching the same URL may return different PDF bytes after a source update; a hash mismatch should trigger a version check, not be hidden. The packet deliberately contains no scholarly PDF, extracted text, source-page image, or catalog corpus.

The outer author freeze receipt and SHA256SUMS authenticate the frozen authored files. Independent review should first verify these hashes, run this script without mutation, and then review the exact original assumptions and every claimed proof. A review must distinguish a failure of a broad Markov converse from any claim about canonical heat flow.
