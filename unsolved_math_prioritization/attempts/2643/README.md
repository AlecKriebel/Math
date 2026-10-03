# Kourovka 21.134: both questions were already answered negatively

**ID 2643 · already solved in the literature · 0/5 substantive proof-attempt turns.**

This is a credited source certificate for J. G. Thompson's counterexample, as recorded by Yu Li and Wujie Shi and the October 2026 Kourovka Notebook. It is not a new solution.

The pair \(H=L_3(4):2_2\), \(G=2^4:A_7\) has identical exact-element-order counts and hence identical numbers of solutions of \(x^n=1\) for every positive integer \(n\). Both groups have order 40,320. Their solvable radicals have orders 1 and 16, respectively; \(H\) is almost simple and the groups are not isomorphic. This refutes both parts of the exact target.

## Certificate and review

- [Full source certificate and structural deductions](frozen_original/SOURCE_CERTIFICATE.md)
- [Independent source and proof-scope audit: PASS](INDEPENDENT_AUDIT.md)
- [Original preparation log](frozen_original/RESEARCH_LOG.md)
- [Published-data arithmetic checker](frozen_original/verify_counts.py) and [reproducible output](frozen_original/verification.json)

The seven original author files are preserved byte-for-byte under `frozen_original/`. Their review-pending statements describe the preparation snapshot. The separate audit records the subsequent PASS with no mandatory correction.

The table of element-order counts is imported from Li–Shi's Theorem 9, which reports a MAGMA computation. Neither this package nor its audit independently enumerates the two groups. The portable checker validates those imported counts and the package's integrity; it does not replace the source theorem.

## Reproduce

Run `python3 verify_publication.py` from this folder or any working directory. It verifies all declared file digests, the frozen author manifest, the independent-audit hash and a byte-exact replay of the arithmetic output. Python 3.10+ and its standard library suffice. No network or private source files are needed.

## Primary references

1. [Kourovka Notebook, October 2026, page 197](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf#page=197), Problem 21.134 and its starred update. The editors credit Thompson and record Vasil'ev's letter of 18 May 2026.
2. Yu Li and Wujie Shi, [A Note on Thompson Problem, arXiv:2303.09460v1](https://arxiv.org/abs/2303.09460v1), attribution on page 2 and Theorem 9 on page 4; published in Ricerche di Matematica 74 (2025), 559–563, [DOI 10.1007/s11587-023-00835-4](https://doi.org/10.1007/s11587-023-00835-4).

The exact catalogue URL was not readable live (HTTP 403); no external-catalogue correction is claimed. This package concerns 21.134 and does not conflate it with 21.137. Preparation and independent audit were AI-assisted. No mathematical novelty, independent group enumeration, human peer review or formal proof-assistant certification is claimed.
