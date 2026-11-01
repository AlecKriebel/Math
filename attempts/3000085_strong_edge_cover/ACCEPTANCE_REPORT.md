# Acceptance report: prior counterexample, ID 3000085

Date: 2026-10-21.

**Accepted conclusion:** The assertion that every hypergraph without isolated vertices whose edges are individually finite admits a strongly minimal edge cover is false.

**Credit:** Dominic van der Zypen, *Counterexample to a conjecture of Aharoni and Korman*, arXiv:2205.02296v1, Lemma 2.1 (2022), https://arxiv.org/abs/2205.02296v1. This is acceptance of an existing result, not a new solution or novelty claim.

**Recommended disposition:** already_solved; one audited disposition turn. No queue mutation or publication was performed by this audit.

## Acceptance basis

1. The definition has the direction |C\D|≤|D\C| for every competing edge cover D. A reversed inequality does not encode the target.
2. The hypergraph on N with every finite subset as an edge meets all target hypotheses and covers each vertex by a singleton.
3. Every nonminimal cover has a one-edge deletion witness, with edge-family difference counts 1 and 0.
4. Every minimal cover has two distinct edges; their union is finite, distinct from both, and absent from the cover. Replacing them gives another cover with difference counts 2 and 1.
5. Hence every cover fails the required condition. No infinite-cardinality subtraction, compactness assertion, or existence of minimal subcovers is used.
6. An independent adversarial reviewer checked the logic and edge cases. See `INDEPENDENT_REVIEW.md` for that review.
7. Exhaustive finite regressions checked 65,812 families and 64,824 covers on one through four vertices. They verified the local exchanges and retained the unique singleton-cover exception at each size. They support bookkeeping, not the infinite conclusion.

## Limits

- No formal proof-assistant verification is claimed.
- No independent audit of the later 3-uniform gadget theorem is claimed. Its published statement is stronger but unnecessary here.
- Neither the original 1992 paper nor the historical wiki page was inspected; attribution and exact-target identification rely on the accessible primary counterexample and stated formulation.
- No copied source text, source PDF, private dataset, or private coordination material is included in these authored deliverables.
