# Independent original-question priority audit

Started 2026-10-12 06:34 UTC. Target: PR 466, problem 30000999 / OWR-2042-008, exact head `77a27c5da92b8f42f79b2f27e40f5c9a6403ddb9`.

Before reading any earlier independent audits or peer reports, I read only the frozen author `release/PROOF.md`, `release/SOURCE_GATE.md`, and `SOURCE_RECEIPT.json`. No prior independent audit content has been read. The source gate is a claim to verify, not evidence substituting for primary literature.

## Claim to be tested

The original question is reported as asking whether a finite constant C, uniform over all probability measures on a sphere with intrinsic geodesic Wasserstein distance, satisfies `W_p(mu,nu) <= C W_p(R mu,R nu)`, where R is the dual of normalized equator averaging, `1 <= p < infinity`.

Provisional hypothesis H1: if the source really uses unrestricted probabilities, the negative answer is a routine consequence of the classical antipodal/odd kernel of the Funk transform, and cannot be promoted as a novel 2026 resolution merely because I fail to locate a paper spelling out this particular Wasserstein inequality.

Competing hypothesis H2: the primary source may impose an overlooked evenness, projective quotient, or support condition. Under such a restriction the antipodal counterexample would not settle the exact original question, and the stronger even-density result needs its own priority assessment.

Competing hypothesis H3: a primary publication already gives an explicit exact Wasserstein negative answer (or an equivalent theorem), which should be distinguished from H1's routine deduction from earlier noninjectivity.

## Success criteria and falsifiable checks

- Independently inspect printed p. 1763 and neighboring context of Stephens's 2008 Oberwolfach contribution; identify transform, measure domain, distance, quantifiers, p and n restrictions.
- Locate pre-2026 primary sources documenting the odd nullspace/noninjectivity for the same classical transform, checking normalization and density-to-measure implications.
- Test the implication directly: equal transformed distinct probability measures force the proposed inverse inequality to fail, using that W_p is a metric; show an explicit admissible pair and dimension edge cases.
- Search historical formulation traces and later citations/answers without treating absent search results as a certificate of novelty or openness.
- Keep the stronger even, positive, smooth-density theorem separate from the original all-probability claim.

## Boundaries

No conclusion about a first published explicit Wasserstein answer follows from bounded search. No claim is made about an even-measure or projective-sphere repair, other than that the original theorem's priority must be assessed independently. I will not change statuses, Git state, PRs, papers, cloud artifacts, or contact any person.

Progress estimate: 10% toward this audit's evidence-based priority recommendation. This is a work estimate, not a probability that a hypothesis is true.
