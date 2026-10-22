# Verified existing negative answer: component-group surjectivity

Problem 30002233 has the prior negative answer in Rabinoff's contribution to Oberwolfach Report 53/2012 and Amini–Baker–Brugallé–Rabinoff, Example 8.6 (2015). This packet gives the complete authored verification and expanded proof, with no novelty claim.

Over C((t)), a finite degree-two map has a genus-two Mumford target and a genus-three source whose minimal regular special fiber is two projective lines meeting transversely at four distinct nodes. The covariant component-group map is Z/4Z → Z/8Z, j ↦ 2j; it is injective with cokernel Z/2Z.

The two component-group orders are transposed in arXiv v3 and the published Example 8.6. Correcting those assignments repairs the local statement; the example's construction and negative conclusion remain valid. The separate primed-label slip in the 2012 report is also identified.

## Contents

- [Complete proof](PROOF.md): graph arithmetic, marked residue covers, split stable deformation over the fixed field, tame lifting, regularity and minimality, Mumford uniformization, and component-group comparison
- [Mathematical audit](AUDIT.md): claim-by-claim checks, all imported dependencies, source-correction scope, and verification limitations
- [Acceptance report](ACCEPTANCE.json): bounded accepted conclusion and artifact bindings
- [Verification outcomes](CHECK_RESULTS.json): independent exact-arithmetic checks in normal and optimized Python, original-verifier limitation, and preservation aggregates
- [Scholarly source metadata](SOURCE_MANIFEST.json): public citations, PDF hashes and byte counts, and retrieval/inspection history
- [Closed artifact manifest](MANIFEST.json): exact publication allowlist and byte bindings

The finite calculation is written out in the proof. The algebraic existence argument imports the cited published geometric theorems; it does not claim a computation re-proves them. No residue-characteristic-two example is asserted.

The original preservation statement's count of six inputs was a reporting error: seven candidate/source pins were checked and matched. The original assertion-based verifier provides meaningful checks in normal Python only. A separate implementation with explicit failures confirms the arithmetic under normal, -O, and -OO execution.
