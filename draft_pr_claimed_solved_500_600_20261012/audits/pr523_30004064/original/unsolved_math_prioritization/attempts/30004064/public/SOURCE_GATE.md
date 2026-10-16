# Source and scope gate

Problem: **30004064 / OWR-16766-003**, “Dual Recovery of Binary Tomography Solution Intersections.” Checked 2026-10-04.

## Catalogue identity and primary statement

The [problem URL](https://www.unsolvedmath.com/problems/30004064) was attempted with the web reader and a direct HTTP request. The latter returned HTTP 403. The record was recovered from the catalogue's public [Hugging Face dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json), revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`. The relevant record names the exact objective and exact sign-recovery rule analyzed in PROOF.md. Its generated literature assessment, open label, and verification label are not accepted as mathematical evidence.

The complete original publisher [report PDF](https://content.ems.press/assets/public/full-texts/serials/owr/16/1/16766/online/10.4171-owr-2019-4.pdf), DOI [10.4171/OWR/2019/4](https://doi.org/10.4171/OWR/2019/4), was downloaded. Kadu's entire contribution, printed pp. 256--259, was read. The crucial printed p. 258 was also visually inspected. Its Theorem 1 displays the full-row-rank objective and recovery rule, and its Conjecture 1 asserts both unique-image recovery and common-coordinate recovery in noiseless tomography.

The catalogue statement does not repeat the report's full-row-rank condition; this does not affect the counterexample, whose matrix has full row rank. Its 3-by-3 data are genuine row and column sums, and removing one redundant sum does not change the binary solution set. The arbitrary-size family also satisfies arbitrarily strong undersampling. The pseudoinverse/projected form is handled separately rather than being conflated with the unprojected objective.

## Cited paper, update, and known limitation

The cited publication is Kadu and van Leeuwen, *A Convex Formulation for Binary Tomography*, *IEEE Transactions on Computational Imaging* 6 (2020), pp. 1--11, [DOI 10.1109/TCI.2019.2898333](https://doi.org/10.1109/TCI.2019.2898333).

The [arXiv record](https://arxiv.org/abs/1807.09196) lists v3, revised 15 December 2020, as its latest version at this check. The complete [v3 PDF](https://arxiv.org/pdf/1807.09196v3) was downloaded and compared byte-for-byte with the [CWI author-manuscript copy](https://ir.cwi.nl/pub/30666/30666.pdf); they are identical. The relevant Sections II-A, II-B, II-C, III, IV and VI were inspected, together with the complete Appendix A proofs of Proposition 1 and Corollary 1. The original OWR statement, the paper's objective, the zero-sign convention, and its scalar discussion were reconciled. Page 3 was visually checked.

Important scope facts:

1. Section II expressly adopts sign(0)=0. The numerical discussion uses zero to indicate an undetermined pixel.
2. Section II-A, equations (10)--(11), already gives the scalar dual optimizer as soft-thresholding. In particular, the noiseless endpoints y=1 and y=-1 give zero. Thus the scalar exact-recovery obstruction is source-known, not a new discovery claimed here.
3. Section II-A discusses obtaining useful signs from approximate iterates. Section II-C also discusses smoothing the one-norm. These observations cannot turn the exact zero optimizer into a nonzero one.
4. Section III in v3 describes a primal-dual algorithm whose displayed output is the sign of an additional primal/subgradient variable. This is a different output from the sign of the exact multiplier. The present result does not claim to disprove that algorithm's possible usefulness.
5. Section IV describes approximate CVX solves and a numerical threshold. The theorem in this package is exact and makes no claim to reproduce the paper's floating-point experiments.
6. The relevant Appendix A proof obtains the general objective by minimizing a quadratic and using the Moore-Penrose inverse. PROOF.md independently establishes the consequence needed here. No unverified imported theorem is necessary.

The author's public [CVX example](https://github.com/ajinkyakadu/BinaryTomo/blob/db4965de499981be13ddf7a979f1cd0e9e1fd51f/test_tomo_cvx.m) was read at revision `db4965de499981be13ddf7a979f1cd0e9e1fd51f`. It removes dependent measurement rows, minimizes the stated objective, then thresholds the back-projection before applying sign. The associated [matrix constructor](https://github.com/ajinkyakadu/BinaryTomo/blob/db4965de499981be13ddf7a979f1cd0e9e1fd51f/bin/getA.m) confirms row/column tomography as the two-direction model. These files were inspected, not executed or redistributed.

## Bounded prior-work and previous-attempt checks

Targeted web searches checked the exact title, identifiers, the authors with “conjecture” or “dual,” and binary tomography with “counterexample” or “correction.” They located the primary report, paper, author manuscript, and code above. No separate primary source settling a specified iterative-limit reformulation was identified. This is not an exhaustive literature search or a certification of historical priority.

Read-only searches of all-state pull requests in `AlecKriebel/Math` used the numerical identifier, OWR identifier, “Binary Tomography,” “tomography,” and “Dual Recovery.” They returned no matching target PR. A repository-content search for the numerical identifier likewise returned no matching attempt. The queue was separately fetched and recorded rank 550 as queued, 0/5, with no findings or linked chat. Queue status alone was not used as evidence that the problem had never been attempted.

## Source integrity and public-content boundary

Downloaded primary files were used only as local reading copies. Their SHA-256 hashes are:

- OWR report PDF: `8d9d44137ed3246a1e5819e6518d4c4033c35188df351a0963fa0c3e8951ec2f`.
- arXiv v3 PDF and identical CWI manuscript PDF: `e65aa0919a97a9e1634b2a14c8dfe56d8c92d009e853321b02d6a1bc5feea4ac`.

The public candidate consists only of authored mathematical prose, source metadata, attempt history, and independent exact-check code/results. It excludes source PDFs, copied source code, extracted source text, catalogue records, account material, and coordination records. Exact public file hashes appear in FROZEN_MANIFEST.json.

## Gate verdict

**Source scope passes for the literal exact-minimizer question.** A complete negative proof is supplied. Its limits are explicit: no novelty claim; no refutation of a separately specified approximate, smoothed, or auxiliary-primal-variable algorithm. Independent mathematical review of the frozen package is required before remote publication.
