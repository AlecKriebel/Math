# Exact semidefinite complexity of the symmetric TSP polytope

A concise consequence note by Alec Kriebel (ORCID 0009-0001-9320-500X). For all sufficiently large N, exact real PSD matrix order is between 2^(cN), for some absolute c>0, and 2(N-1)+(N-1)(N-2)2^(N-3); hence the order is 2^Theta(N). Matrix order counts one PSD cone, or the sum of block orders; affine equalities are free.

The exponential lower-bound breakthrough is OpenAI family 126, pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a. This note records its TSP consequence, using Yannakakis's established 3n-city face reduction, an explicit 2n-city contraction, exact slack calculations, all-city-count padding, and the standard subset-state flow upper bound. It claims neither a new lower-bound method nor first priority for these reductions. Prior unrestricted TSP bounds include the CCC 2016 corrected stretched-exponential bound.

The central matching proof was reconstructed by independent mathematical audits; no material gap was found. The release's actual Lean statements cover only superpolynomial growth, and their full builds were not reproduced. Neither the exponential input nor this follow-on theorem is claimed to be formally verified. Finite tests are falsification evidence, not asymptotic proof. AI tools were used extensively; no conventional human peer review has been completed.

## Contents and reproduction

The contents map below describes the project repository. In the Zenodo deposit, `main.tex` is in the separate source archive and `paper.pdf` is a separate download; neither is duplicated inside the verification archive.

- `main.tex`: standalone manuscript; `publication/paper.pdf`: actual downloadable six-page PDF.
- `proofs/`: explicit geometric and upper-bound derivations.
- `DEPENDENCY_LEDGER.md`, `THEOREM_LEDGER.md`, `APPROACH_TABLE.md`: accepted scope and exact dependency boundaries.
- `agent_notes/`: mathematical and priority audits, with finite check results.
- `checks/reproduce.py`: reproducible graph, rational-flow, shift, local-kernel and splitting checks.
- `publication/README.md`: payload and clean-build instructions.

From the extracted verification archive, run `python3 checks/reproduce.py`. It uses only the standard library. For the optional upstream tagged-Fourier/parity checks, install NumPy 2.3.5 in your chosen environment and run `python3 checks/reproduce.py --upstream`. This fetches six external proof sections from the pinned commit, verifies their recorded hashes, and retains their OpenAI attribution. A source hash cannot itself verify a theorem.

Compile standalone `main.tex` using the built-in Codex LaTeX editor, or run `tectonic main.tex` in the extracted source archive. Bibliographic references are embedded, so no additional project files are required. Source tested with Tectonic 0.16.9; finite checks with Python 3.14.6 and supplementary numerical checks with Python 3.12.14 / NumPy 2.3.5.

New prose/documentation: CC BY 4.0. New code: MIT. See LICENSES.md. Third-party papers, upstream proof trees, fonts/runtimes, credentials and caches are excluded from the Zenodo payload. Publication receipts and tracker verification are retained separately in the project repository.
