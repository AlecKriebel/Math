# Acceptance of the complete negative answer

Target: 30000921 / OWR-1787-006, Polynomial Stability of Hypercyclic Entire Functions.

Verdict: ACCEPT_COMPLETE_NEGATIVE_ANSWER. The independent audit found no mathematical correction necessary. The complete proof and independent reconstruction are retained in PROOF.md and AUDIT.md, with only review-status and distribution-reference edits.

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

## Exact target and conclusions

The question asks whether pf belongs to HC(D) for every differentiation-hypercyclic entire f and every nonconstant complex polynomial p, where multiplication is pointwise and H(C) has the compact-open topology. The p(z)=z counterexample negates that full universal assertion.

The stronger accepted theorem fixes a nonconstant p first. For every starting f in HC(D) and every neighborhood W of f, it constructs F in W intersect HC(D) with pF not hypercyclic. Since HC(D) is dense, this set of fixed-p counterexamples is dense in H(C).

For the particular F from the z construction at parameter eta=1, all monomials z^m with m>=1 fail simultaneously. No all-polynomials simultaneous claim is made. Universal polynomial multipliers are exactly nonzero constants; the zero multiplier and every nonconstant polynomial fail.

## Written proof obligations

The Baire construction establishes existence and density of starting hypercyclic entire functions from polynomial antiderivatives tending to zero. Dense orbit tails supply increasing approximation subsequences. Entire perturbations whose derivative orbits vanish preserve hypercyclicity. The normalized Taylor-coefficient estimate gives both entireness and locally uniform decay.

For p=z, coefficients are clipped away from zero by the threshold 1/(k+1), with correction at most 2/(k+1). All positive-order evaluations of zF have modulus at least one, while the zeroth is zero. The whole orbit misses the explicitly displayed open evaluation disk. Low derivatives are included in the exclusion.

For fixed p, a root alpha of multiplicity m gives a triangular recursion with nonzero pivot q_m(k+m)!/k!. Each correction uses only earlier corrections and is bounded by 2 eta k!/(|q_m|(k+m)!). Future choices preserve every earlier derivative barrier. The resulting null perturbation yields an entire hypercyclic F whose pF orbit misses one open disk at alpha. Uniform control in eta proves density without requiring continuity of the coefficient choices.

The only proof inputs are elementary entire-function theory, Baire's theorem, and the fundamental theorem of algebra for the fixed-p extension. Existence is not inferred from finite tests.

## Source and quantifier boundary

Costakis's 2008 Question 5 and adjacent residual-positive Theorem 6 have different quantifiers. Dense negative sets can coexist with a residual positive set. The 2018 paper's composition/convolution and selected multiplicative statements, and the 2010 residual common-hypercyclicity theorem, do not imply preservation for every f in HC(D).

Bounded searches did not establish priority, exhaustive literature coverage, or certified openness in 2026. Source proofs were not fully audited. The acceptance concerns this written mathematical argument, with all historical qualifications retained.

## Supporting evidence and distribution

The author recorded 1,200 threshold checks, 1,200 linear barriers, and 2,500 recursive steps across 100 fixed-polynomial cases per interpreter mode. The independent auditor separately checked 4,961 replacements, 246 monomial indices, 450 recursive coefficients, 30 low derivatives, 6,525 preservation checks, and 10,168 factorial-tail inequalities per mode. Both used exact Gaussian-rational arithmetic. Four deliberate algebra mutations were rejected in each of normal/-O/-OO modes, twelve rejections in total. These finite diagnostics support coefficient algebra only.

Historical normal/-O/-OO outputs were authenticated, not rerun during edition preparation. Their hashes and the original manifest identities appear in VERIFICATION.json. Integrity authenticates bytes; it does not prove mathematics.

The full authored mathematical proof and independent audit are retained, including every written argument, formula, and counterexample. This is not a computational reproduction package: executable code, raw computational datasets, copied source PDFs/text/images, search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution. The original proof and audit remain unchanged.
