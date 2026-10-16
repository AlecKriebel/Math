# Independent source contract and attack plan

Frozen 2026-10-16 06:05 UTC. Review completion estimate: 8%.

This document was written before reading the candidate mathematics, proof, note,
candidate README, old audit reports, family dispositions, or acceptance verdicts.
The dispatch necessarily exposed the problem label, original claimed_solved
status, expected package identities, and suggested attack topics; those are not
mathematical evidence and no acceptance conclusion is adopted.

## Authentication before extraction

All three complete original corpus bodies were hashed before any parsing:

| File role | Bytes | SHA256 |
|---|---:|---|
| catalog | 21735099 | 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566 |
| problems | 68931837 | 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf |
| research results | 80334822 | 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b |

Exactly one catalog record and one problem record have ID 30005079. Their
ordered two-element JSON serialization (indent 2, Unicode preserved, final
newline) is 5415 bytes, SHA256
6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083.
The original research-results object has no OWR-10252925-004 member.

The actual OWR report body is 1032709 bytes, SHA256
c997329409f016d06867ecc06dd38c59cea4919aa9ecf34791ed6a95f63345ec.
Printed pages 888–889 (PDF pages 28–29) were read in full as extracted text and
visually rendered pages. The visual page labels and mathematical context agree.

## Exact target reconstructed independently

The native cleaned question asks for an explicit nontrivial canonical
degeneration of a Fano variety whose entropy-minimizing valuation is
nondivisorial. The original OWR passage makes the scope precise: for a klt Fano
variety X, the canonical two-step degeneration is X -> (Z,xi_Z) -> (Y,xi_Y).
The first step uniquely minimizes the H functional on real valuations, its
associated anticanonical graded ring is finitely generated, and Z is its Proj.
The requested nontriviality is X not isomorphic to Z, not merely a nonzero vector
field, a second-step change, or a product test configuration. The valuation must
be a real function-field valuation centered on X, globally minimize H among
Val_X under the cited normalization, and fail to be a positive scalar multiple
of a prime-divisor order. Irrational coordinates alone will not establish this.

The source does not demand smooth X, an indecomposable X, a novel general
minimization theorem, a new theorem of soliton existence, or a nontrivial second
step. It does demand an actual explicit example and canonical first-step
identification. Native dated literature-status assertions are hypotheses to
verify, not evidence of current openness or priority.

## Success criteria and independent attack families

1. **Geometry:** reconstruct the family and special central fibre; check flatness,
   anticanonical grading, normality/klt/Fano hypotheses, and an isomorphism
   invariant proving X != Z. Test degenerations and local singular boundary
   cases directly rather than accept naming conventions.
2. **Exact analysis and arithmetic:** derive the moment equations and sign/root
   arguments from their integrals. Attack zero roots, canceled denominators,
   all rational ratios p/q, coincident exponential exponents, and the exact
   transcendence hypotheses. Finite numerical sampling is insufficient.
3. **Valuation and algebra:** reconstruct a valuation on the function field,
   value group, rational rank, center, associated graded algebra, finite
   generation, and the canonical discrepancy shift. Distinguish rational rank
   from ordered rank and the real filtration from a naively finitely generated
   dense-positive-cone Rees algebra.
4. **Global minimization:** read the actual cited primary theorem bodies and
   independently verify their hypotheses and normalization. Attack weak soliton
   behavior at singularities, product factorials and metric boundedness, and
   whether the criterion covers every valuation and supplies uniqueness.
5. **Publication and package:** after freezing a substantive mathematical
   assessment, inspect earlier reports and history, serious predecessors,
   metadata, author and AI disclosures, complete five-page PDF, source–PDF
   correspondence, immutable source identities, closed manifests and archive,
   and actual executable verifier controls. Authentication is not execution.

The strongest result at this freeze is an authenticated and visually verified
source contract. No candidate theorem has yet been evaluated.
