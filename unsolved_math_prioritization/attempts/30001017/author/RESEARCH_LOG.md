# Research log

Date: 2026-10-04 UTC. One target, five substantive approaches, no helpers and no remote writes. Completion estimates concern the all-genus conjecture and are subjective bookkeeping, not probabilities or measured fractions of a proof.

## Source gate, 17:41-17:47

Started with the requested UnsolvedMath URL. The web reader failed and the direct request returned HTTP 403. Used the authorized cached record and verified the exact conjecture against the official report, pp. 2186-2188, and EGH Conjecture 1.2. Live queue placed ID30001017 at rank662, queued 0/5. Exact-ID/title PR, branch and code searches returned no previous attempt. The corresponding attempt directory was absent; state and related-group records had no ID30001017 entry. All remote operations were read-only.

The retrieved arXiv file is v1, not a new 2021 revision. EGH works on stacks. OWR reproduces a coarse genus-four table; this explains its factor-two difference. No later complete resolution was located in the bounded primary-literature search. A 2026 low-degree-cohomology preprint was inspected at the abstract level; its stated result does not directly supply the desired top intersection numbers.

Completion estimate: 1%.

## Approach 1: Satake support and localization, 17:44-17:45

Proved the support cutoff L^n|beta_r=0 for n>dim A_(g-r)^Sat by Hodge hyperplane sections. Recovered the first boundary vanishing gap and the exact permissible localization range. Tried to induct only on Satake stratum dimensions; blocked because positive-codimension cycles inside a larger stratum can survive. At genus5,n2 the beta3 image has dimension3, so support alone is insufficient.

Outcome: rigorous elementary partial, already reflected in the literature. Completion estimate: 3%.

## Approach 2: abelian multiplication multigrading, 17:45-17:48

Proved normalized theta pushforward vanishing with finite-flat multiplication and extended it factorwise to abelian powers. Derived the determinant generating polynomial, checked its r=2 specialization against the primary theorem, and tested r=3 coefficient weights. Recovered the second vanishing gap. Tested extension to degeneration: base twists and changing multiplication degree prevent the naive compactified argument. The recent theta-relations paper explicitly distinguishes open abelian identities from difficult deeper boundary formulas.

Outcome: complete limited lemmas, no global compactified conclusion. Completion estimate: 5%.

## Approach 3: corank-two finite sums and GRR coefficients, 17:48-17:53

Implemented the finite formulas in exact rational arithmetic with standard-library Bernoulli recurrence. The initial direct transcription of a simplified preprint formula failed even at genus2. Kept the failure and traced it against the preceding double sum, inspecting the rendered pages. The double sum reproduces all contributions for genera2-5. Further checks flag preprint-specific genus6/7 table discrepancies and an intermediate sign typo. Rechecked Todd coefficients by independent convolution and theta integrals by direct polynomial expansion. These findings are source-version-specific; the journal PDF returned403 and was not inspected.

Outcome: exact reproduction of known low-genus numbers and reproducibility warnings. No higher-corank vanishing proved. Completion estimate: 5%.

## Approach 4: toroidal modification comparison, 17:53-17:55

Proved a general intersection-invariance lemma for divisor discrepancies supported over a Satake locus of dimension below the Hodge exponent. Verified the genus-four example against the primary first/second-Voronoi paper. Applied the support criterion to modifications over A1 in genus5. Retained rational-Cartier and common-refinement hypotheses explicitly; did not assume an undefined boundary intersection on an arbitrary singular model. This localizes the issue but leaves the torus-rank-three correction untouched.

Outcome: rigorous conditional comparison, blocked as a solution. Completion estimate: 5%.

## Approach 5: genus-five coefficient elimination, 17:55-17:56

Counted all required zeros outside EGH's range: (g-3)(g-4)/2 for g>=3. Isolated the first one as L²D¹³ in genus5. Removed the known terms of the degree polynomial and derived a four-point rational stencil eliminating the other unknown coefficients. Tested81 exact formal examples. An arbitrary nonzero residual coefficient still satisfies every already-known constraint, showing that the reduction needs genuinely new geometric input.

Outcome: exact reduction and insufficiency test; no value of the actual unknown intersection. Completion estimate: 5%.

## Validation and freeze, 17:56 onward

Validation only, not a sixth proof-search approach. Re-ran exact checks after independently expanding the Todd and theta formulas, inspected the report and preprint pages underlying every formula warning, checked source fingerprints and the safe-file allowlist, and froze the author packet. Fresh independent adversarial audit remains required. The exact conjecture remains unresolved; proposed queue disposition after acceptance of the record is exhausted, five approaches used.
