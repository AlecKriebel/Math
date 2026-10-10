# Internally accepted result: inverse-polynomial Boolean-polynomial compatibility

Theorem accepted by an independent internal mathematical audit: for nonzero real multilinear f,g of degree at most d on {-1,1}^n, the uniform coordinate bound RelInf_i(f), RelInf_i(g) <= 1/(4096d^8) guarantees a common nonzero point.

The proof combines the source-credited depth-O(d^4) disjoint-support separator of Li–Li–Li–Liu (arXiv:2608.03824v1, Lemma 3.5) with a fully proved covariance inequality for adaptive decision trees. The latter converts a depth-T separator into the necessary bound max relative influence >= 1/(4T^2). The separator is reconstructed with the explicit depth bound 16d^4; the classical Markov step is included with credit to its Bernoulli-symmetrization presentation in Kothari–Kovacs-Deak–Wang–Yang (arXiv:2601.08727v3).

PROOF.md contains the complete mathematical argument, exact normalization, arbitrary-common-zero handling, and citations. The result concerns the exact two-polynomial OWR2025 question. The AI-assisted proof and audit are unrefereed; no external human peer review is claimed. No novelty or priority claim is made. No finite check is presented as a universal proof.
