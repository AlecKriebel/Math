# Partial results for ordinal colored dense order preorders

Problem 30000374 / OWR-1116-002. Accepted internal-audit PARTIAL result, 10 October 2026.

## Established results

For each countable ordinal α, let Rα compare α-valued rational colorings by a strictly increasing rational map whose image is dense in its convex hull and whose target colors dominate the source colors in the usual ordinal order.

- R₀ is the empty preorder; R₁ is the singleton reflexive preorder, with strictly different Borel degrees.
- For every α ≥ 2, the relation as a set of pairs is analytic-complete and non-Borel. A fixed binary-valued source coloring already has an analytic-complete upward section, using one continuous tree coding for all such α.
- Color inclusion gives continuous preorder reductions Rα ≤ᴮ Rβ for α ≤ β; in particular R₀ <ᴮ R₁ <ᴮ R₂ ≤ᴮ Rα for α ≥ 2.
- For α > 0 the least class is the constant zero coloring. The greatest class is exactly the colorings whose every ordinal tail is dense on one common nonempty interval, giving a Σ⁰₃ upper bound. The stated constant-color and finite-support comparisons also hold.

Analytic completeness here uses the conventional continuous many-one reductions from Baire space, equivalently zero-dimensional Polish source spaces. It does not assert reduction from arbitrary connected Polish spaces, and it does not imply universality of Rα as an analytic preorder. A preorder reduction is one map preserving and reflecting every ordered pair.

The real extension of a witness preserves rational arguments but need not map Q onto Q; its real image may be a proper open interval. Continuity only on the rational subspace would be a weaker condition.

## Unresolved by this work

The exact Borel preorder degrees for α ≥ 2, reversibility or strictness of inclusion reductions among them, and analytic preorder universality remain unestablished. Mutual embeddability equivalence relations are not classified. No full solution, novelty, priority or global-openness certificate is claimed.

## Contents and attribution

- PROOF.md: complete authored mathematical proof, byte-identical to the accepted frozen original
- AUDIT.md: full substantive independent mathematical reconstruction, boundary checks and source-interface analysis
- ACCEPTANCE.json and STATUS.json: exact accepted partial claims, residual questions and review limits
- SOURCE_REVIEW.md and SOURCE_METADATA.json: authored primary-source interpretation, public citations, PDF identities and dated inspection scope
- VERIFICATION.md: supplementary diagnostic history and the distinction between integrity checks and mathematical proof
- MANIFEST.json: exact public membership and byte/hash identities

Question credit: Riccardo Camerlo, “Universal analytic preorders,” Oberwolfach Report 55/2005, printed pp. 3127–3129, Problem 5 on p. 3128. https://ems.press/content/serial-article-files/46028

The dense-witness extension is tied to Marcone–Rosendal; the tree-completeness source is Foreman–Rudolph–Weiss. The limits of possible transfers from Camerlo–Marcone–Motto Ros, Carroy–Pequignot–Vidnyánszky, and Beckmann–Goldstern–Preining are recorded with their precise hypotheses. All references appear in the proof, audit and source review.

The proof and audit are AI-assisted and unrefereed. Independent internal acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. All substantive proof and audit reasoning is included; the proof has no omitted computational dependency. Only authored prose and permitted public verification metadata are distributed. Programs, generated certificates, raw outputs, datasets, copied source documents/text/images and private coordination material are excluded.
