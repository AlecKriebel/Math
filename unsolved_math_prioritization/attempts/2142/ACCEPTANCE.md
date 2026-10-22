# Acceptance report: prior EP-488 finite refutation

Date: 10 October 2026. Target: 2142 / EP-488.

**Verdict: accepted prior mathematical refutation of the finite multiples formulation.** No mathematical correction to the audited proof is required.

## Accepted claim and attribution

Declan Gessel, with disclosed GPT-6 Astra assistance in Codex, September 2026, supplies the construction, proof and Lean formalization. This publication audits that prior result and makes no claim of new discovery or priority.

There is a nonempty finite set A of integers greater than 1 and positive integer endpoints m>n>=max(A) such that 2 m M_A(n)<n M_A(m), where M_A counts the positive multiples of A up to its inclusive endpoint. The construction supplies an existential integer 0<=k<4096; this is not an enumerated numerical witness.

## Complete proof obligations accepted

1. The fixed sets of primes, Q and phi satisfy Q>128, 3Q<16phi and the exact growth-endpoint comparison.
2. Unique factorization bounds the smooth count by (8j+1)^53. The finite-growth contradiction produces one fixed k, with all quantifiers explicit.
3. The entire smooth band is finite and nonempty; all generators exceed 1, its maximum is n, and m>n.
4. The near-count identity and odd-part/exponent-residue injection yield M_A(n)<=12H(k), with both band endpoints treated correctly.
5. The dyadic-crossing construction and coprime far-count injection yield M_A(m)>=H(k)phi, including arbitrary prime powers.
6. The exact strict numerical ratio gives the strict reverse density inequality. One eligible finite set and endpoint pair refute the full universal claim.
7. The retained exact-statement adapter preserves positivity, exclusion of 1, the finite maximum condition, counting endpoints and rational division. Its proposition matches the retained catalogue right side after comment/whitespace removal.

The complete general derivations are retained in `AUDIT.md`, rather than being replaced by this summary. Only raw numerical certificate details are omitted from the publication edition.

## Primary authority and evidence limits

The original 1966 multiples formulation controls. The literal 1961 nonmultiples wording is separately recorded and is not silently corrected or claimed resolved by complementing the accepted result.

The historical audit inspected the full prior prose proof, all 496 server-source lines and the full adapter in the 561-line gist source. It also inspected the relevant primary page images and independently checked exact integer arithmetic. The publication preserves verification metadata, public citations and source hashes/counts without copying those source bodies.

The external GitHub success concerns the pinned server commit. There was no local Lean replay, imported-dependency audit or independently reproduced formal axiom list, and the external run does not certify an independently replayed later adapter. These formal-reproducibility limits do not introduce a missing hypothesis in the accepted elementary proof.

No completed human peer review, mathematical-community acceptance, current external-catalogue status or exhaustive novelty determination is claimed. The author publicly states that specialist review and historical/priority checking are being sought. This is an unrefereed AI-assisted audit.

Publication preparation is limited to exact editorial, identity and addition-only validation. It does not execute third-party code, perform new mathematical proof attempts or modify the original sealed audit, QUEUE.md or unrelated repository material.
