# Publication and verification package

Title: Exact semidefinite complexity of the symmetric traveling-salesman polytope.
Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Date: October 6, 2026 (America/Los_Angeles).

The intended deposit has three separately downloadable files: `paper.pdf`, `tsp-source.zip`, and `tsp-verification.zip`. The outer upload-kit directory is packaging, not an additional upload. The source archive contains the standalone TeX, supplied upstream BibTeX citation, rights notices and package README. The verification archive contains authored proofs, dependency/approach ledgers, research checkpoint log, independent audits, reproducible finite-test code/results and source/version receipts. It excludes third-party manuscripts and proof-tree copies.

The mathematical headline is exact real matrix-order complexity 2^Theta(N), as a consequence of the cited OpenAI exponential matching theorem. The known reduction and standard upper formulation are credited. No approximation, hierarchy, P-versus-NP, complex-PSD or formal-exponential claim is made. AI tools were extensively used; conventional human peer review has not occurred.

## Clean reproduction

Extract `tsp-source.zip` into an empty directory. Run `tectonic main.tex` (tested 0.16.9), or open it in the built-in LaTeX editor. All references are embedded in the standalone source. A newly built PDF may have different creation-time metadata and byte hash; proof text and page content must agree.

Extract `tsp-verification.zip` into another empty directory. Run `python3 checks/reproduce.py` (standard library only; tested Python 3.14.6). The optional `python3 checks/reproduce.py --upstream` needs NumPy (tested Python 3.12.14, NumPy 2.3.5) and network access to fetch six hash-verified, pinned external proof sections. It checks finite rational local kernels, small noncommuting tagged Fourier stacks and a finite parity-moment decomposition. These computations are falsification checks; the source's asymptotic theorem is justified by the cited proof and mathematical audits.

The archived source_bridge_receipt is a static import/semantic inspection, not a successful Lean build. To repeat that optional inspection with your own pinned source clone, set TSP_UPSTREAM_DIR to its root and run `python3 checks/source_bridge_audit.py` without `--finite-only`. This copies a scoped import tree into the extracted verification directory and reads the clone without modifying it. A complete Lean build is optional and remains unverified; its theorem would still be only superpolynomial.

CC BY 4.0 covers newly authored documents and data; MIT covers newly authored code. See the included rights notices.
