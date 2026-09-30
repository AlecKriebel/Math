# Research log

Date: 30 September 2026. Model: GPT-6 Astra, xhigh reasoning. The repository ranking assumed a different reasoning budget; this record states the actual one.

Ceiling: two hours from 09:37:37 UTC, five substantive approaches. **Three approaches used.** Source triage and finite checks are not extra approaches. Estimates below are judgmental completion estimates, not correctness probabilities.

## 09:37–09:46 UTC: source and prior-attempt gate

Read repository policy, current queue, complete pinned statement and the original two-page OWR contribution. No previous Alec/campaign attempt or duplicate was found. The complete Carawan follow-up reveals a material distinction between maximal-groupoid realization, categorical S-constructions and arbitrary weak-equivalence realization. The broad target is source-qualified. Completion estimate for broad characterization: 10%.

## Approach 1: elementary non-injective cofibrations

Considered pointed finite sets with every map a cofibration, where quotient data can forget how an extra point maps into the collapsed subset. This provides an elementary diagnostic mechanism but uses a less compelling cofibration structure for the source's request for natural examples. It was not developed as a publication theorem. Completion estimate for the example part: 30%; broad target: 15%.

## Approach 2: free-factor cofibrations

Used the natural free-product structure of finite-rank free groups. Pushouts along free-factor inclusions remain free groups. The automorphism b↦b[c,a] fixes a and becomes the identity after killing a, but fails to preserve the intermediate subgroup <a,b>. This gives an explicit missing automorphism of the right quadrilateral comparison. The distinction between the fixed target data and globally isomorphic unmarked flags is essential. Complete proof saved. Example-part completion estimate: 100% subject to separate review; broad target: 30%.

## Approach 3: quotient-factorization criterion

Expressed the right quadrilateral comparison fiberwise over the groupoid of cofibrations. Its fibers are the functors Fact(i)→Sub_cof(X/A). A flip argument propagates the degree-three condition from the known left fans to all polygon triangulations. This yields an iff criterion for the isomorphism-groupoid variant, including a concrete unique-subobject-lifting specialization for monomorphic cofibrations. The argument does not control realization of arbitrary weak-equivalence categories. Scoped mathematical package completion estimate: 100% subject to separate review; broad target: 45%.

## 09:51–09:54 UTC: verification and freeze

The standard-library verifier passed 8,876 exact assertions: noncommutative word substitutions and inverse maps, quotient certificates, positive pointed-set interval controls, and all triangulations of polygons with three through eight vertices. These checks do not replace the categorical proof or establish novelty.

Stopped with a complete scoped artifact rather than extending the groupoid argument into an unsupported claim for arbitrary weak equivalences. The broad target remains unresolved. Separate adversarial review is required before a draft PR. No shared queue or generated status files were changed.
