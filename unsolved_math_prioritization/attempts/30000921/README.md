# Polynomial multiplication need not preserve differentiation hypercyclicity

Complete negative answer to target 30000921 / OWR-1787-006, with no mathematical correction required by the independent audit.

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

## Result

Let H(C) carry the compact-open topology and let D be differentiation. There exists an entire F in HC(D) such that zF is not in HC(D). Thus the universal pointwise-polynomial-multiplication assertion in Costakis's Question 5 is false.

The proof establishes more:

- For every fixed nonconstant complex polynomial p, counterexamples F in HC(D) with pF outside HC(D) are dense in H(C), and can be obtained in every neighborhood of every starting f in HC(D).
- One particular F from the p=z construction simultaneously makes every z^m F nonhypercyclic, for integers m>=1.
- The polynomial multipliers that preserve every member of HC(D) are exactly the nonzero constants.

The general polynomial p is fixed before F is constructed. No single F failing for every nonconstant polynomial is claimed. The simultaneous statement concerns monomials only.

## Proof and source context

The manuscript gives the full Baire proof of existence and density, dense-tail and null-orbit perturbation lemmas, an entire-coefficient bound, the explicit z counterexample, and a triangular recursion at a root of each fixed p. The correction is explicit relative to a starting hypercyclic function; no numerical explicit starting function is asserted.

The original Question 5 is on printed page 330, PDF page 34, in George Costakis's 2008 contribution, “Which maps preserve universal functions?” Its neighboring Theorem 6 gives a residual positive class. That theorem is compatible with the dense counterexample sets proved here. This result is about pointwise p(z)f(z), not composition P(f), polynomial differential operators P(D), or translation hypercyclicity.

No historical priority or novelty is established. The 2018 multiplicative-structure paper and the 2010 common Cesàro hypercyclicity paper have distinct operations or generic quantifiers; neither was treated as a proof of the universal assertion. Detailed historical inspection limits, including failed web-reader retrievals during the audit, are retained in SOURCES.json.

The full authored mathematical proof and independent audit are retained, including every written argument, formula, and counterexample. This is not a computational reproduction package: executable code, raw computational datasets, copied source PDFs/text/images, search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

## Reading order

- PROOF.md: the complete accepted analytic proof and public references.
- AUDIT.md: the full independent mathematical reconstruction, quantifier checks, and historical verification scope.
- ACCEPTANCE.md and ACCEPTANCE.json: exact accepted claims and document bindings.
- SOURCES.json: scholarly titles, public URLs, PDF and derived-text identities, and separate historical inspection bounds.
- VERIFICATION.json: historical finite checks and integrity metadata, with no code or raw datasets.
- MANIFEST.json: the exact eight-file inventory, hashing the other seven files.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution. The original proof and audit remain unchanged.
