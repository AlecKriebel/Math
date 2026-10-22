# Boolean polynomial compatibility

Problem 30006210 / OWR-14299088-012 has a complete affirmative proof for the exact two-polynomial Boolean-cube question, accepted by an independent internal mathematical audit.

For every pair of positive integers n,d and every pair of nonzero real multilinear polynomials f,g on {-1,1}^n of degree at most d, the bounds RelInf_i(f), RelInf_i(g) <= 1/(4096 d^8) for every coordinate imply that f and g are simultaneously nonzero at some vertex. Relative influence uses the full squared L2 norm, including the constant coefficient. Thus c=1/4096 and C=8 suffice. The proof establishes the stronger necessary lower bound 1/(1024 d^8) on the maximum relative influence for disjoint supports.

The essential separator is prior work of Longcheng Li, Qian Li, Xingjian Li and Qipeng Liu, [arXiv:2608.03824v1, Lemma 3.5](https://arxiv.org/abs/2608.03824v1). PROOF.md reconstructs it with the explicit depth 16d^4, includes the classical Markov/Bernoulli argument credited to [Kothari, Kovacs-Deak, Wang and Yang, arXiv:2601.08727v3](https://arxiv.org/abs/2601.08727v3), and supplies the complete adaptive covariance and square-influence arguments.

The AI-assisted proof and independent internal audit are unrefereed. Internal acceptance does not claim external human peer review, journal acceptance, formal machine certification, novelty or priority. The result concerns the exact two-polynomial question; no general distribution-formulation, other-group or approximate-support extension is claimed.

The earlier exponential sufficient threshold requires a strict inequality. At d=1, f=1+x and g=1-x refute the non-strict endpoint printed in the 2025 report. This correction remains explicit in the proof and audit and does not affect the new threshold.

## Contents

- PROOF.md: complete theorem, four lemmas, quantitative contradiction and source credit
- AUDIT.md: full substantive independent mathematical audit and limitations
- SUMMARY.md: concise accepted theorem and proof mechanism
- ACCEPTANCE.json: original acceptance, original and distributed proof identities, and review status
- STATUS.json: exact constants, quantifiers, normalization and boundaries
- SOURCE_DEPENDENCIES.json: credited prior inputs and the authored argument
- SOURCE_METADATA.json: four public source titles, versions, URLs, PDF identities and inspection scope
- VERIFICATION_SUMMARY.md: mathematical, source-inspection and integrity scope
- MANIFEST.json: exact ten-file membership and byte/SHA-256 identities of the other nine files

Only authored mathematical prose and public acceptance, citation and verification metadata are distributed. The universal proof is standalone apart from its stated classical Markov inequality input. Finite checks are supplementary. Source PDFs, copied source text or images, datasets, code, certificates, raw receipts and private coordination are excluded.
