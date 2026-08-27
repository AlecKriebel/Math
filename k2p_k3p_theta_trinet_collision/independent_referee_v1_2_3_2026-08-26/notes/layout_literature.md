# Independent presentation and literature audit (v1.2.3)

Date: 2026-08-26 (America/Los_Angeles)

Scope: read-only audit of `packet_copy`. I read the 19-page main manuscript in full before opening either support PDF, then read both support PDFs. I rendered and visually inspected all 23 supplied PDF pages (19 + 2 + 2) page by page. I did not rebuild any PDF and did not run the referee orchestrator.

## Bottom line

No visual or bibliographic defect blocks review: every page renders, all fonts are embedded, equations/tables/references remain inside the page, and no unresolved cross-reference marker was found. I found one substantive literature-attribution correction, one source-version wording caveat, and one minor cross-document presentation ambiguity. The central novelty/scope framing is credible relative to the cited primary literature and targeted searches, but—as usual—absence from a targeted search is not proof of worldwide priority.

## Findings requiring or meriting an edit

### L1 — The cited 2018/2021 papers support generic, not full, identifiability (moderate)

The introduction says that algebraic work "has established generic and, under additional hypotheses, full identifiability results for level-one models" and cites only Gross--Long (2018) and Gross et al. (2021) (`combined-paper-clarified.pdf`, p. 2; `combined-paper-clarified.tex:29`). Both cited primary sources state generic-identifiability results:

- Gross--Long studies a single undirected cycle of length at least four and establishes generic identifiability for the JC large-cycle class: <https://doi.org/10.1137/17M1134238>.
- Gross et al. proves generic identifiability for triangle-free level-one semi-directed networks with fixed reticulation count under JC/K2P/K3P (abstract and Theorem 2): <https://doi.org/10.1007/s00285-021-01653-8>.

Neither source is the full pointwise level-one theorem described by the sentence. The latter theorem is instead in Brits et al. v3, Theorem 4.9, which the preceding paragraph already cites: <https://arxiv.org/pdf/2607.12919v3>, pp. 17–18 (printed numbering; theorem begins on p. 17).

Recommended repair: change the sentence to "has established generic identifiability results for level-one models"; or split it into generic results cited to [8,7] and the later full result cited to [2].

### L2 — "Version 3 removes those K2P statements" is substantively right but textually over-broad (minor)

The packet repeatedly says v3 removed the arbitrary-level K2P statements (`combined-paper-clarified.pdf`, pp. 1, 7; `combined-paper-clarified.tex:27,234,244`; `technical-summary-clarified.pdf`, p. 1; `technical-summary-clarified.tex:14`; `SOURCE_CONVENTION_CROSSCHECK.md:5`). The versioned comparison is correct at the level of formal results:

- v2 Lemma 5.6 says the K2P polynomial is zero on one model and strictly positive on the other, hence disjoint; v2 Corollary 5.8 gives the JC/K2P global blob conclusion: <https://arxiv.org/pdf/2607.12919v2>, pp. 23–24.
- v3 replaces that K2P lemma with an explicit warning that the JC induction cannot readily be adapted because the K2P polynomial is not invariant under all leaf permutations, and v3 Corollary 5.7 is JC-only: <https://arxiv.org/pdf/2607.12919v3>, pp. 23–24.
- v3 expressly lists extension of the high-level trinet inequality to K2P/K3P as open: <https://arxiv.org/pdf/2607.12919v3>, p. 25.

However, v3 retains a stale sentence in Section 4.1 saying that the JC and K2P inequalities are further generalized to arbitrary-level trinets in Section 5: <https://arxiv.org/pdf/2607.12919v3>, p. 11. Thus "removes those K2P statements" can be read as claiming that every textual assertion was removed, which is not literally true. This is an inconsistency in the cited preprint, not a mathematical error in the submitted packet.

Recommended repair: say "Version 3 removes the formal arbitrary-level K2P lemma and the K2P part of the global corollary" and, if useful, add that the residual p. 11 sentence appears stale. The more precise language already used in Remark 6 (`combined-paper-clarified.tex:234`) is a good model.

### P1 — The technical summary repeats the compressed arc notation that the clarification note was meant to remove (minor)

The technical summary writes

`u -> p,q,  p,q -> r_2,  p,q -> r_3`

(`technical-summary-clarified.pdf`, p. 1; `technical-summary-clarified.tex:16-20`). The surrounding prose makes the intended ten arcs recoverable, but the notation itself can be parsed in more than one way. The support note explicitly says it "removes a compressed wording ambiguity" and gives every arc separately (`k2p_displayed_tree_clarification.pdf`, p. 1; `k2p_displayed_tree_clarification.tex:17-21`), followed by an unambiguous edge-placement table (`:23-38`).

Recommended repair: expand the summary line to the same explicit ten-arc list, or write "u to p and q; p and q each to both r2 and r3." This is a presentation inconsistency only; all edge labels, vectors, and conclusions agree across the documents.

### P2 — Figure 1 is legible but two labels are unnecessarily crowded (cosmetic)

In the rooted panel, the labels `T` and `S` on the crossed inner arrows nearly touch; in the suppressed panel, the pendant-leaf `2`, its `K` label, and `r_2` are tightly stacked (`combined-paper-clarified.pdf`, p. 5, Figure 1; `materials/figures/theta_network.tikz:33-36,51-57,67`). No label is clipped or actually unreadable, and the prose immediately below gives the complete edge placement. Slightly increasing separation would reduce the chance of a reader seeing `TS` as one label.

### P3 — Accessibility advisory: PDFs are untagged (advisory only)

All three PDFs report `Tagged: no`. This does not affect visual rendering, and their text extracts successfully, but semantic navigation and screen-reader reading order may be weaker than in a tagged PDF. This is not a mathematical or print-layout defect.

## Complete visual inspection record

All three files are US Letter, unencrypted PDFs with embedded fonts.

- `combined-paper-clarified.pdf` (19/19 pages inspected): PASS. No missing page, clipped margin content, missing glyph, black box, broken equation, overflowed table, unreadable reference, or unresolved `??` marker. Figure 1 on p. 5 is dense but complete (see P2). The pivot table on p. 13 is small but readable. The repository URL on p. 18 wraps across lines but stays within the text block. The bibliography on p. 19 is intact.
- `technical-summary-clarified.pdf` (2/2 pages inspected): PASS. The pages are information-dense and use relatively small type, but every displayed vector, determinant, inequality, and link is legible. No clipping or collision was found. P1 is a wording/notation issue, not a rendering failure.
- `k2p_displayed_tree_clarification.pdf` (2/2 pages inspected): PASS. Both tables, the four-switching formula, the 4-by-4 matrix, radical expressions, boxed equality, and replay line render fully and remain within margins.

Section/equation/theorem references in the manuscript resolve to numbers in the compiled PDF; a text search found no unresolved cross-reference placeholder. Page numbers and running section transitions are present throughout.

## Literature and scope verification

### Versioned source claims

- Brits et al. v2 metadata and the withdrawn K2P formal claims match the packet bibliography and Remark 6: <https://arxiv.org/abs/2607.12919v2> and <https://arxiv.org/pdf/2607.12919v2>, especially printed pp. 23–24.
- Brits et al. v3 metadata (25 August 2026), full pointwise level-one theorem under JC/K2P/K3P, JC-only arbitrary-level result, leaf-order obstruction, and open K2P/K3P high-level question match the packet's substantive scope: <https://arxiv.org/abs/2607.12919v3> and <https://arxiv.org/pdf/2607.12919v3>, especially printed pp. 17, 23–25. The stale p. 11 sentence is the caveat recorded in L2.

### Other scope assertions

- Gross--Long (2018) supports the historical statement about generic identifiability for JC large-cycle networks, but not the packet's current wording about full identifiability: DOI <https://doi.org/10.1137/17M1134238>.
- Gross et al. (2021) supports generic identifiability for triangle-free level-one networks under JC/K2P/K3P with fixed reticulation count: DOI <https://doi.org/10.1007/s00285-021-01653-8>.
- Gross--Krone--Martin (2024) gives dimension formulae for triangle-free level-one group-based network varieties, supporting "dimensions for broad classes" with the understood triangle-free qualification: DOI <https://doi.org/10.1007/s11538-024-01314-z>.
- Cox--Gross--Martin (2025) studies the 3-sunlet/minimal triangle network and dimension questions for group-based models, supporting the packet's 3-sunlet literature sentence: DOI <https://doi.org/10.1007/s11538-025-01506-1>.
- Englander et al. v4 (revised 4 July 2026) states generic identifiability for binary semi-directed level-two networks under JC provided they are triangle-free and strongly tree-child. This matches `combined-paper-clarified.tex:29,582` and supports the packet's distinction from its non-tree-child theta: DOI <https://doi.org/10.1101/2025.04.18.649493>; authoritative version feed <https://api.biorxiv.org/details/biorxiv/10.1101/2025.04.18.649493/na/json>.
- Evans--Speed is an appropriate foundational source for the group/Fourier formulation used here: DOI <https://doi.org/10.1214/aos/1176349030>.
- Sturmfels--Sullivant is an appropriate source for Fourier-coordinate/toric phylogenetic invariant conventions: DOI <https://doi.org/10.1089/cmb.2005.12.457>.

### Novelty assessment

Targeted searches using combinations of `K2P`, `K3P`, `theta trinet`, `tree-theta collision`, `strict level-two`, and `phylogenetic network identifiability` located no earlier exact tree/theta K2P or K3P collision of the form claimed here. More importantly, the immediately preceding primary source, Brits et al. v3 (25 August 2026), explicitly leaves the high-level K2P/K3P trinet question open on printed p. 25. The packet is dated August 2026 and answers that precise question with an explicit witness. Accordingly, the novelty framing is credible against the cited and readily searchable record. This is necessarily a bounded literature conclusion, not a proof that no unpublished or differently worded predecessor exists.

The manuscript is also appropriately narrow about what it does **not** establish (`combined-paper-clarified.pdf`, pp. 2, 17–18; `combined-paper-clarified.tex:39,581-588`): no JC collision, no contradiction of the level-one K2P 3-sunlet calculation, no generic theta/tree equivalence, no unrestricted multi-blob composition, and no genuine four-attachment K3P conclusion. Those delimitations are consistent with the primary sources above.

## Bibliography and source-convention consistency

- The manual bibliography (`combined-paper-clarified.tex:625-634` / PDF p. 19) and `references.bib:1-94` contain the same nine works. Author lists, titles, venues, years, volumes/article numbers/pages, version dates, and the seven journal/preprint DOIs checked against the DOI/arXiv/bioRxiv records above are consistent.
- The `.bib` entry for Brits et al. v3 additionally records the generic arXiv DOI `10.48550/arXiv.2607.12919`, whereas the printed bibliography uses the more useful version-specific arXiv URL. This is harmless and not an inconsistency in the cited object.
- `SOURCE_CONVENTION_CROSSCHECK.md:5,9-11` correctly identifies that v2 Lemma 4.1 is retained in v3 and fixes the source's `(A,C,G,T)` order, Klein addition, and K2P equality `a_C=a_T`.
- Its source parameterization and five displayed coordinates (`SOURCE_CONVENTION_CROSSCHECK.md:13-29`) agree term-for-term with the appendix proof of v3 Lemma 4.1: <https://arxiv.org/pdf/2607.12919v3>, printed p. 28. Its positive factorization (`SOURCE_CONVENTION_CROSSCHECK.md:31-35`) also matches the final source factorization on that page.
- The main manuscript's invariant and favorable-order factorization (`combined-paper-clarified.pdf`, p. 7; `combined-paper-clarified.tex:237-244`) use those same conventions. I found no C/G/T ordering drift among the manuscript, the source-convention document, and the clarification note.

## Referee-facing disposition

Presentation/literature recommendation: **minor revision**, chiefly to correct L1. L2 and P1 should also be cleaned up because both are easy changes and head off predictable reader confusion. No PDF needs emergency regeneration for clipping, corruption, or unreadability.
