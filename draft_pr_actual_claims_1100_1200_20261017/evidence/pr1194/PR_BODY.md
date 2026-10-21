## Accepted prior resolution

This authored exposition records the exact finite balanced-subsequence-pattern
classification proved by Gal Beniamini, Nir Lavee and Nati Linial in
[*How Balanced Can Permutations Be?*](https://doi.org/10.1007/s00493-024-00127-x),
Combinatorica 45, article 9 (2025). For integers n>=k>=1:

- k=1: every n>=1.
- k=2: n>=2 and n=0 or 1 modulo 4.
- k=3: n>=3 and n=0,1,9,20,28,29 modulo 36.
- k>=4: no n>=k.

This is an audit of a prior published resolution, with no novelty claim.
The pattern definition uses arbitrary increasing index sets. Endpoints,
infinitude for each k<=3, and nonexistence for each k>=4 are included.

## Complete proof and finite-evidence boundary

The elementary increasing-pair square identity gives the positive discrepancy
n(n-1)(2n+5)/72 and a complete contradiction for n>=k>=4. Downward closure,
its endpoints, and elementary order-1/order-2 sufficiency remain self-contained.
Order-3 arithmetic, quarter-turn counting, the odd-centre correction, six
source-attributed analytical families, chamber cuts, and exact finite-sum
polynomial derivations are retained. Their unbounded conclusions do not rely
on interpolation from sampled values.

Full order-3 sufficiency additionally uses premise F1, the 19 separately
checked exceptional witnesses in published Appendix A Table 1, pages 28–29,
equivalently [arXiv:2306.16954v1](https://arxiv.org/pdf/2306.16954v1), Table 1,
page 21. Every list was validated as a permutation and all triples were
counted by two independently written methods. The two source versions agree.
Numerical permutation lists, individual witness outcome tables, raw
certificates and executable code are omitted. The complete low-order
classification cannot be independently reproduced from this edition alone;
this is not a complete self-contained proof of the finite-witness part.
The precise source citation locates the missing evidence. Hashes alone do
not prove it. Reproduction requires obtaining Table 1 and rechecking F1.

## Verification scope and source credit

The accepted audit independently checked the pair-square identity on all
5,913 permutations of lengths 1–7 and the rotation formulas on 306
parity-labelled inputs of lengths 1–5. It checked all six families using
exact chamber inequalities and polynomial summation, as well as finite
direct tests. Historical normal, -O and -OO runs produced byte-identical
substantive output. This edition preparation byte-authenticated that
evidence; it performed no new mathematical computation or source inspection.
Source titles, public URLs, PDF hashes and sizes, and historical retrieval
and inspection metadata are provided without copying source text.

Acceptance covers the historical exact target only, not the paper's unrelated
quantitative discrepancy, permuton or reconstruction claims. The endpoint,
odd-centre and chamber derivations are explanatory completions, not a claim
that the published theorem is false. This AI-assisted exposition is unrefereed.
Acceptance means an independent internal AI audit. No external human peer
review, formal proof-assistant certification, CI verification, novelty or
exhaustive literature-status claim is made.

Exactly eight authored proof/audit/acceptance/provenance/verification files
are added under unsolved_math_prioritization/attempts/3100034. QUEUE.md and
all unrelated paths are unchanged. Copied sources, numerical witness data,
raw certificates, executable code and private coordination material are excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,491 bytes; SHA-256 `ee820ce0322f9feae06adcb6f8bdbc2c484dfa72023ee8ae0a9517149415d79b`.
- `ACCEPTANCE.md`: 2,169 bytes; SHA-256 `b9e4a5a5d89af17ce9505198e5a74aafbdfa6039e5bceb207adf8f1eb77c1495`.
- `AUDIT.md`: 4,770 bytes; SHA-256 `ddefba2571ae1c6d0794ca64fbbe1056bc343432cdac820427f4c73fafbe30e8`.
- `MANIFEST.json`: 1,349 bytes; SHA-256 `cec90b22208fa1a09da2888a118dc5c9e594f84dd259f44983382a46e8a03761`.
- `PROOF.md`: 23,456 bytes; SHA-256 `2293175303fb27ecb91dda7852100fe1e2a1ec7d3de0e97aed45891aea5fdffb`.
- `README.md`: 2,072 bytes; SHA-256 `a5cad8282c002820891ccc4dda18f161c5ddf837a183e826ed5c052ec4b74ca4`.
- `SOURCES.json`: 2,866 bytes; SHA-256 `0723c48fc62a8050d9a59d400615a1d8b791540a58341e4458c8ec1c40fc1d72`.
- `VERIFICATION.json`: 2,223 bytes; SHA-256 `ef11f8e7e8247bd78fccef6147e39553564aec4ca03b698eb1a709c01e285674`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

