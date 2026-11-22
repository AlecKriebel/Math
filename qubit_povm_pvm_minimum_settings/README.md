# Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation

For two inputs per party, every two-qubit POVM behavior with arbitrary finite declared outputs is a finite mixture of complete qubit projective strategies. For three inputs against two, a physical POVM achieves $(16+8\sqrt{7813})/25$ on the paper's rational Bell functional, while every qubit projective strategy scores at most $289/10$. This establishes the minimum input architecture up to party exchange.

## PRA manuscript and files

[Manuscript PDF](paper/main.pdf) · [Line-numbered PDF](paper/review.pdf) · [TeX source archive](submission/arxiv_source.tar.gz) · [Submission metadata](submission/journal_metadata.md)

From this directory, run `bash paper/build.sh --submission` to rebuild the manuscript, line-numbered copy and upload archive. The paper source and bibliography are in [paper/](paper/). The [pre-submission review](../qubit_povm_pvm_pra_review_20261122/PRA_REVIEW.md) assesses the previous manuscript and derives the shorter proof of the projective-fiber proposition used in this revision.

## Verification

- The [exact artifacts](artifacts/) contain the physical strategies, rational Bell coefficients and symbolic checks. With the packages in `requirements.txt` installed, run `bash run_all.sh`. The [independent verifier](../qubit_povm_pvm_pra_review_20261122/check_artifacts.py) recomputes the scores and checks the rational certificate across input formats.
- The [Lean project](bell_lean/) contains the proofs, pinned dependencies, and theorem-to-claim map. From that directory, run `python scripts/run_lean.py --bootstrap --serial` for a source build and axiom audit. The [November verification record](../qubit_povm_pvm_pra_review_20261122/evidence/lean_summary_20261122.json) identifies the expanded physical statement and the dependency replay for the equality and finite-simulation theorems.
- The [formal coverage](bell_lean/docs/CERTIFIED_COVERAGE.md) distinguishes the kernel-checked conclusions from the auxiliary arguments in the manuscript. The machine proof and the manuscript include independent routes to the projective-fiber result and the global projective bound.

The [September version 2 package](VERSION_2.md), [earlier referee packet](review_packet/README.md), and [v1.1.0 publication deposit](https://doi.org/10.5281/zenodo.21699161) document earlier versions. The September archive's online bootstrap uses the preparatory step described in `VERSION_2.md`.

Alec Kriebel, Independent Researcher. [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). The manuscript and data use CC BY 4.0, and the verification code and Lean sources use MIT. [Licenses](LICENSE)
