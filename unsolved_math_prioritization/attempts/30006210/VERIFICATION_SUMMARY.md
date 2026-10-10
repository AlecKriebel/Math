# Verification scope

## Complete mathematical argument

PROOF.md retains the accepted theorem and complete four-lemma proof, with no mathematical edits:

1. Bernoulli symmetrization and the classical Markov inequality bound disjoint sign-switching blocks by 2m^2.
2. The source-credited separator argument hits maximum-degree monomials and reduces the degree sum, giving a total decision tree of depth at most 16d^4, including arbitrary common-zero vertices.
3. Transcript-conditioned adaptive resampling proves the covariance bound with the exact factor 1/2. The tree always queries its original input and never re-queries a coordinate on a branch.
4. Parseval, the probability-1/2 forced-flip relation and Cauchy–Schwarz give the full-norm square-influence estimate for all real coefficients.
5. The two separator covariances have absolute values summing to one. Disjoint supports force maximum relative influence at least 1/(1024d^8), contradicting the inclusive threshold 1/(4096d^8).

AUDIT.md retains the complete substantive mathematical review of all these steps, including n<d, constant polynomials, arbitrary coefficients, variable stopping times, common zeros, normalization and endpoint cases. The proof body from “Theorem” to the source-credit section and audit Sections 2 through 6 are byte-identical to their independently accepted originals. Status framing and original/distributed provenance are explicitly updated. The source-credit and boundary sections preserve the strict old exponential endpoint and the limits of the accepted formulation.

The classical univariate Markov inequality is the stated standard approximation-theory input. Its Bernoulli consequence and the separator, adaptive covariance bridge, square estimate and final contradiction are presented in full. There is no hidden computational dependency.

## Sources and supplementary checks

SOURCE_METADATA.json preserves all four public source identities and inspection locations. The essential separator source is Li–Li–Li–Liu, arXiv:2608.03824v1, Lemma 3.5; the Markov/Bernoulli presentation is Kothari–Kovacs-Deak–Wang–Yang, arXiv:2601.08727v3. The original OWR2025 target and earlier CRYPTO2022 formulation are also cited. Source inspections belong to the accepted audit; edition preparation does not claim fresh source retrieval or inspection. The two principal 2026 sources were inspected as arXiv manuscripts, without a separately verified journal-publication claim.

The independent audit records 8,413,368 exact finite covariance inequalities, transcript-conditioned hybrid checks on 64 input pairs, and 1,272 square-influence coordinate inequalities. These passed in normal and optimized execution. They are supplementary diagnostics, not a universal proof. No finite-check executable, raw output or certificate is distributed.

The edition has an exact ten-file allowlist and byte/SHA-256 manifest. Integrity checks cover public membership, original and distributed document identities, exact editorial replay, strict patch replay, unchanged frozen inputs and seven complete native Git tree identities. These are document-consistency checks, not mathematical proof certificates.

## Review status

The AI-assisted authored proof and independent internal mathematical audit are unrefereed. Acceptance is the internal mathematical disposition for the exact two-polynomial theorem. No external human peer review, journal acceptance of this proof, novelty, priority, formal machine proof or general distribution-formulation extension is claimed.
