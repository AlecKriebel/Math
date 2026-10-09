# Accepted clause-specific consequences for KP-1.64

Date: 9 October 2026 UTC. Problem 2723 / KP-1.64.

## Accepted mathematical conclusions

For positively transverse oriented links in the standard cooriented contact sphere, with the **canonical induced contact structure on the cyclic branched cover**:

- KP-1.64(a), the double-cover Stein-fillability implication to transverse quasipositivity, is false.
- The double-cover instance of KP-1.64(c), demanding slice-Bennequin sharpness for the given transverse representative, is false. Any blanket version allowing a double cover is therefore false as well.
- KP-1.64(b), with an existential cover degree strictly greater than two, is not resolved by this audit. Neither is a separately restricted higher-order-only version of (c). The whole three-part problem must not be marked solved on this basis.

These are verified consequences of published results and elementary deductions from them. They are not claimed as new original results, a new proof-search approach, or a novelty/priority determination.

## A single fully specified witness

Take the positive transverse closure T of

\[
 b_6=(\sigma_1\sigma_2)^6\sigma_1^5\sigma_2^{-21}\in B_3.
\]

The full twist factor has identity permutation; the remaining two odd adjacent transpositions multiply to a 3-cycle, so T is a knot. Its exponent sum is \(12+5-21=-4\), and the braid formula gives \(\operatorname{sl}(T)=-4-3=-7\).

Brejevs–Wand's published theorem gives a Stein-fillable contact structure supported by the once-punctured-torus open book with monodromy \(t_\delta t_a^5t_b^{-21}\). The disk-open-book branched-cover construction, with the contact identification supplied by Harvey–Kawamuro–Plamenevskaya, identifies this structure with the canonical induced structure on the cyclic double cover of T. Thus no unrelated fillable contact structure on the same smooth manifold has been substituted.

The accepted proof chain includes Baldwin's tightness input and the oriented Whitehead-surgery identification. Min–Nonino's **published** Theorem 1.6 applies with n = 5 and r = -21: every tight contact structure on the resulting oriented manifold is Stein fillable. Nonvanishing of a Floer contact invariant alone is not used as a Stein-fillability criterion.

For clause (a), negative exponent sum rules out quasipositivity of b6. The transverse Markov theorem and quasipositivity preservation under positive destabilization then rule out a quasipositive braid representative anywhere in T's transverse isotopy class. The full audit also verifies the published all-k family through the reduced-standard-form obstruction and the same contact/transverse bridges.

For clause (c), every smooth knot has \(g_4\ge0\), so

\[
 \operatorname{sl}(T)=-7<-1\le2g_4(K)-1.
\]

The gap is at least six. No slice-genus calculation or converse from nonquasipositivity to nonsharpness is assumed.

The entire oriented smooth knot type K is also nonquasipositive, by a separate argument. If K were quasipositive, Hayden's Theorem 1.2 would supply a quasipositive minimal-braid-index representative q of index m, where \(1\le m\le3\) and \(e(q)\ge0\). Generalized Jones would require

\[
 |-4-e(q)|\le3-m\le2,
\]

whereas the left side is at least four. This contradiction is stronger than braid-level nonquasipositivity and is not inferred from it alone. The audit establishes the corresponding smooth oriented link-type result for every k >= 5, and explicitly makes no determination by this short argument for k = 0, 1, 2, 3, 4.

## Review and preservation

The complete authored source audit was followed by separate independent AI review. That review read the entire mathematical audit and independently checked the original K3 page 62 formulation, the Brejevs–Wand theorem/proof, the induced-contact bridge, Min–Nonino's published Theorem 1.6, Hayden's Theorem 1.2, and the generalized Jones inequality. The accepted scope is exactly the clause-specific set above.

All mathematical sections 1–7 of MATHEMATICAL_AUDIT.md are preserved byte-for-byte in this edition. The remaining edits remove only private provenance/coordination references or clarify the historical review stage and references to included metadata. PROVENANCE.md documents them. The original audit and source records remain untouched. The reading log describes the original source audit, not a new reading pass during publication preparation.

This is AI mathematical/source review, not human peer review or formal proof-assistant verification. The audit reads the immediate source arguments and records the foundational results still imported. It does not purport to re-prove the whole underlying contact/Floer literature.

## Source and residual limits

- The exact K3 formulation comes from the full permission-watermarked author preliminary volume, page 62. The four-page AIM workshop summary is not used as evidence of the numbered clauses.
- Brejevs–Wand's accepted manuscript and arXiv v2 were inspected and compared. Its final publication status is verified, but its final JSG publisher-PDF identity is not claimed.
- Min–Nonino's actual published 42-page PDF is the operative fillability source. Its negative-r construction and classification exhaustion, not a title-based L-space restriction or stale preprint-only reading, support the application.
- The source catalogue retains fifteen public PDF identities, all rehashed and matched for this edition. Hash equality proves byte identity only. Source bodies and page images are excluded.
- Higher-order cover fillability does not follow merely from double-cover fillability, extending the open-book page, or the existence of an arbitrary Stein-fillable structure. The required compatible higher cyclic contact covering/filling data are missing from the inspected arguments.
- No global openness claim is made for clause (b), and no every-higher-cover version of (c) is claimed refuted.

Zero new substantive proof-search approaches were used. No further proof-search campaign is started by this edition. No executable scripts, fixtures, computational result files, source copies, private coordination material, QUEUE changes, or unrelated repository edits are part of this package.
