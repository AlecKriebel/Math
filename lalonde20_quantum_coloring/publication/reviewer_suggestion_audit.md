# Presentation-suggestion audit

Audit date: 2026-08-01 (America/Los_Angeles).

This note records the disposition of seven presentation suggestions received
after an external AI audit. The mathematical proof was rechecked before the
edits, and no suggested change was treated as evidence of correctness by
itself.

1. **Named author and affiliation — applied in part.** The manuscript now
   names Alec Kriebel and gives `Independent Researcher` as the affiliation.
   No email address was added because none was supplied or approved for public
   release; inventing or inferring contact data would be inappropriate.
2. **Less ambiguous title — applied.** The title is now *The quantum
   chromatic number of the G19 join family*. In addition, the joined family is
   denoted `J_n` in the note, removing the collision between the fixed base
   graph `G_19` and the old family notation `G_n` at `n=19`.
3. **Bridge to the standard quantum chromatic number — applied.** The
   projector definition now cites Lalonde's Theorem 2.19 and the foundational
   Cameron–Montanaro–Newman–Severini–Winter paper.
4. **Expand two proof transitions — applied.** The tail lemma now states the
   equal-dimension argument that turns orthogonality inclusions into complement
   equalities. The final proof now displays the cross-color inner-product
   calculation term by term.
5. **Immutable provenance — applied without self-reference.** The manuscript
   identifies audited commit
   `b1944a23707eb69d2f9f25eda0bb73c32cd5500a` and both exact certificate
   SHA-256 digests, supplies a retrievable immutable repository URL and
   project-relative paths, and distinguishes the coverage of the two
   independent obstruction verifiers. The final manuscript commit and
   rendered-PDF hashes are recorded only after the PDF is frozen, in the
   public page and checksum manifest.
6. **GitHub Action — declined.** No workflow was added. This follows the
   author's explicit instruction. The same three verifier commands are run
   locally before publication and their exact scope remains documented.
7. **Expanded bibliography — applied.** The bibliography now includes the
   foundational quantum-coloring paper and Mančinska–Roberson's `G_13` paper,
   and the body explains their relevance.

The manuscript also now includes an explicit AI-assistance and non-peer-review
disclosure. No researcher or other individual was contacted, and no outreach
draft was prepared or sent.
