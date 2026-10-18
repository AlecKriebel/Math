# Reverse cross-challenge of the structural priority audit

Prepared after this family's initial independent seal of 2026-10-18T04:06:17.211569Z. Challenge began at 2026-10-18 04:07:21 UTC. Initial authored files and seal have been preserved.

## Outcome

The structural audit's decisive positive finding survives independent challenge: **the exact multiplication is already recorded on the full top-semilattice domain in Castiglioni and San Martín's arXiv:1611.09589v1 (29 November 2016), Example 3.5(4), printed p. 7.** No hidden requirement of a bottom, distributivity, finiteness, or a lattice was identified. A claim that the multiplication or first universal mechanism is new is therefore falsified.

A second conclusion also survives: membership in the older class hIS4, even with logical unit, diagonal, order compatibility, separation, and meet preservation added, does **not** imply the full L-algebra or mixed semibrace identity. An independently implemented four-chain countermodel verifies this separation.

The current full classification is directly checkable using the old formula and the supplied additional argument. The checked 2016 text does not state the complete semibrace/L-algebra application as such. This review therefore gives no first-application, first-statement, independent-discovery, oldest-origin, novelty, or current-worldwide-openness clearance.

The line in my initial direct-lineage report saying no meet-valued formula had been found was an honest bounded **pre-cross-review search finding**. It is now superseded by the authenticated structural family's positive discovery and my own primary-body verification. It must not be reused as a current combined-literature conclusion. The initial report remains unchanged as a historical independent record.

## Authentication before use

The supplied sibling OUTPUT_MANIFEST.json was 1394 bytes, SHA256 c1f0d4b742146413d4c0e4322c0abb26f92f417844a39a43ffae7d290de8cca1. Its seven literal relative_path/bytes/sha256 entries were independently recomputed and matched before any member content was used. Paths were checked as relative and without parent traversal. Only those authored members and the explicitly authorized local 2016 primary PDF were inspected from the sibling family.

AUTHENTICATION.json records the seven input pins. They are receipts, not membership in this cross-review's output manifest. The sibling check script was inspected but was not executed in place, because its main function rewrites the adjacent sealed results. CROSS_CHECKS.py is independently authored here and writes only its own results here.

## Attack 1: exact operation versus a resemblance

The actual 2016 v1 PDF was authenticated at 154406 bytes, SHA256 c89c6d2a5e054879bfb8382c2c2311d467d58330ee160bf3102db7d6a9e56294. I extracted its body into this family's private folder and independently rendered and inspected printed pp. 2 and 7.

After identifying source 1 with target e, formula (4) is literally the admitted operation:
- value e when x≤y;
- value x∧y when x is not≤y.

Both comparisons use the meet order. The operation is not merely a classical implication with a similar diagonal or order relation, and it is not the fallback-y operation in the workshop's Problem 10. Formula (5) on the same source page uses equality in its branch test and must not be confused with formula (4).

The source's Example 3.5 is stated for a bounded semilattice. Printed p. 2 explicitly defines bounded here by the existence of a greatest element. The introductory “with bottom 0, when necessary” covers a list of examples; formula (4) neither names nor uses 0. The formulas which return 0 do need a bottom. The proof for formula (4) and the full target's existence construction do not.

For a concrete boundary case, all nonpositive integers with meet=min and top=0 have no least element: each n has n-1 below it. Formula (4) is still defined on this entire infinite domain. The included finite sample only checks implementation consistency; this domain argument establishes the missing-bottom boundary. A singleton causes no branch ambiguity; x≤x always selects e.

## Attack 2: version, final title, and chronological precision

The [primary arXiv version record](https://arxiv.org/abs/1611.09589v1) was reopened and states v1 submission at 2016-11-29 12:26:14 UTC. The actual downloaded body is headed arXiv:1611.09589v1 and 29 Nov 2016.

The [publisher record](https://link.springer.com/article/10.1007/s11225-017-9759-3) independently confirms the final title *l-Hemi-Implicative Semilattices*, publication online 3 October 2017, and Studia Logica 106, 675–690 (2018), with issue date August 2018. It identifies subscription preview content. I did not obtain a complete final body.

An indexed passage from the primary institutional final-article URL exposes Example 3.1(4), with the same formula and a greatest-element domain. That supports the renumbering as **limited indexed primary passage inspection**; it does not justify claiming complete final-PDF inspection or dating exact current final bytes to 2016.

The safest exact locator is therefore the body-verified version-pinned 2016 Example 3.5(4). The final title and DOI may also be cited with the evidence boundary stated. “Recorded by 29 November 2016” is supported; “introduced for the first time in 2016” is not. An earlier source could still exist.

## Attack 3: class-general leap to L-algebras

I checked the actual v1 definitions on pp. 2–3 and the H4/H5 definitions and order result on p. 6. In this source:
- hIS requires top-semilattice, diagonal x→x=1, and the implication p≤q→r ⇒ p∧q≤r;
- hIS4 adds x→(x∧y)=x→y;
- Corollary 3.4 gives the logical-order characterization in hIS5;
- p. 7 Remark 3.6 places formula (4) in hIS4.

These statements do not contain the cycloid or mixed semibrace identities. A full extracted-body term scan found no cycloid/semibrace/L-algebra terms; that scan alone is not a proof that no implicit consequence exists.

The independent countermodel uses the four-chain 0<a<b<e, meet=min, and rows/columns in that order:

| → | 0 | a | b | e |
| --- | --- | --- | --- | --- |
| 0 | e | e | e | e |
| a | 0 | e | e | e |
| b | 0 | 0 | e | e |
| e | 0 | a | b | e |

CROSS_CHECKS.py checks H3 in its original quantified conditional form over all 64 triples, independently of the sibling's equivalent equational test. It also verifies H4, diagonal, both unit/absorber laws, logical order, separation, and meet preservation. All pass.

At x=a,y=b,z=0, the left cycloid expression is e→0=0, while the right is 0→0=e. The mixed law also fails. Thus the countermodel blocks a derivation based only on that whole collection of general properties.

It does **not** block using the exact old formula (4), which is a proper specialized family. For that operation the additional laws can be proved directly. Let F_x(z)=x→z. Factor F_x as meet-with-x followed by the map on ↓x that sends x to e and fixes strict predecessors. This map preserves binary meets, including x=e and singletons, so S1 follows. If u≤x, direct branch comparison gives F_u F_x=F_u. Applying it with u=x∧y gives S3; symmetry gives cycloid. Units, diagonal, and logical order follow directly from the formula.

Consequently the old universal construction plus a direct identity verification gives the sufficient direction of the current classification. The necessity argument from the printed combined axioms is another direct argument. Neither is legitimately inferred merely from the name hIS4. This is the useful distinction between an old exact formula and an unproved class equivalence.

## Attack 4: “new full result” and current worldwide openness

Eight actual post-seal searches coupled hemiimplicative/hemi-implicative terminology with L-algebra, cycloid, semibrace, Dietzel, and the source title, and checked the follow-up title *On a variety of hemi-implicative semilattices*. The latter's accessible primary institutional abstract concerns a representation theorem for a subvariety, not an identified exact target statement; its full body was not inspected. Narrow searches were sparse/noisy and did not identify a verified prior full semibrace application. Those non-results do not establish historical absence.

The original 2023 question cannot certify worldwide openness in 2026. The already-known full-domain operation removes any basis for presenting the mechanism as new. The source mismatch between general hIS4 and full L-algebras likewise removes any basis for declaring that an arbitrary hIS4 theorem already states the full target. Both overstatements should be rejected.

A defensible description is: a direct verification/classification under the workshop's printed axioms using an operation already recorded by Castiglioni and San Martín, with the priority of this particular application unestablished. It is unnecessary to label it a new theorem or a previously open problem to state the mathematical content accurately.

## Actionable global recommendations

Root states that the current edition already credits the exact 2016 operation and qualifies all eight surfaces; those root files were not inspected or edited here.

1. At the first formula and in each contribution summary, say the operation is recorded in Castiglioni–San Martín 2016, Example 3.5(4). Avoid “introduced by” if it implies oldest origin.
2. Keep the final article metadata separate from the pinned preprint locator; do not claim full final-body inspection on the basis of an indexed formula passage.
3. State “greatest element” explicitly. Do not narrow the old source to lattices with both bounds or finite/distributive semilattices.
4. Keep the hIS4 countermodel and its interpretation: it excludes a class-wide inference, not the exact formula's directly verified laws.
5. Replace any surviving “new universal construction,” “first mechanism,” “first non-chain example,” “first application,” or “currently open worldwide” wording across title, abstract, summaries, status tags, metadata, and release/index text. No release or index mutation is authorized here.
6. Any combined audit conclusion must incorporate this positive precedence finding. The original direct family's negative search line is preserved only as a timestamped historical observation.

No defect was found in the sibling's central exact-operation match, greatest-only interpretation, or hIS4 countermodel. The final-body access limit and remaining original-source/history gaps remain real. This challenge does not certify the earliest exact full statement or exclude older implicit consequences.

## Boundaries

No outside individual was contacted and no outreach was prepared. No other-shard output was read. No Git, PR, root file, sheet, index, release, or publication mutation occurred. New authored outputs reside only in direct_lineage_cross_challenge; raw provider receipts and source extractions/renders remain private under _local. SOURCE/provenance paths are input receipts only, never output-manifest members.

Completion estimate at seal: 100% for this bounded reverse challenge; novelty confidence is not assigned.

