# PR207 exact-result priority audit

Audit scope: problem 5100044 / original arXiv k804,a. This is an independent exact-result and chronology audit, not publication approval. First assessment was sealed before new searches or other new priority reports. The audited positive claim uses genuine least collision period divisible by four, signed shoelace areas in trajectory order, strict nondegenerate confocal elliptic caustics, unit inversion of original vertices about an original focus, straight segments between inverted vertices, and every admitted coprime star winding.

## Decisive finding

**An exact deposited theorem already matches the entire positive target.** Alper Ferudun, *Focal Inversion Area Products in Elliptic Billiards*, DOI [10.5281/zenodo.23093706](https://doi.org/10.5281/zenodo.23093706), Theorem 1 (PDF page 2), is an exact scope match. Its seven-page full text was read as extracted text and rendered pixels. The manuscript and reproducibility archive were downloaded through the native Zenodo API; size and MD5 match the record and separate files metadata. This is substantive full-text evidence, not a search-snippet or abstract-only match.

A new October 2026 publication of this theorem must cite Ferudun and cannot frame the theorem, either-focus equality, inclusion of primitive stars, repetition scaling, or circle extension as an unqualified new resolution. The public record does not establish first discovery, independence, simultaneous discovery, or absolute priority for either author. This audit does not authorize changing QUEUE status or merging, closing, or publishing the PR.

## Exact expression and scope map

| Audited target | Ferudun's deposited text | Match |
| --- | --- | --- |
| Proper ellipse and strict confocal elliptic caustic | Section 1 uses a>b>0 and 0<lambda<b squared | Exact |
| Original orbit area times one focal inverse area | Definitions in Section 1 and Theorem 1 | Exact |
| Unit-radius focal inversion of original vertices | Explicit vertex formula in Section 1 | Exact |
| Signed area, stars, trajectory order | Signed cyclic determinant definition and scope statement | Exact |
| Genuine least period divisible by four | Theorem 1 uses least n=4r | Exact |
| All coprime admitted windings | Theorem 1 and coprimality in Section 2 | Exact |
| Both original foci give the same result | Theorem 1 and equation (11) | Exact |
| Repeated admitted cycles, reversal, circles | Theorem 1, following paragraph, Section 6 | Already covered |
| Unrestricted displayed length divisible by four is false | Section 6.1 plus source-archive triangle control | Already covered as a conclusion |

The focal inverse here is neither an outer tangent polygon nor inversion of whole edges into circular arcs. No mismatch of geometric objects rescues a novelty claim. The repeat-list qualification is present in the deposited text, not merely the current landing page.

Ferudun's paper proves the same conclusion by a direct Jacobi-torus cancellation of the product's possible poles. Isotropic focal tangency lowers inverse-vertex determinant orders; reversal removes the apparent even Laurent order; complementary zeros cancel the remaining original and inverse area poles. The submitted PR instead pairs antipodal inverse edge contributions, identifies a reduced cyclic dn sum by pole/residue matching, and invokes its half-shift product. These are distinguishable proof organizations within the established complex elliptic-function method. Distinguishable organization is not evidence of independent discovery or a new method. This audit has read the whole published argument but has not separately reproduced every Ferudun verification program.

The root's new repeated-triangle fixture differs from the archived Ferudun fixture: the latter uses squared outer axes 21 and 16, lambda=336/25, and a triangle with logical vertices (1,0),(-3/5,16/5),(-3/5,-16/5) under diagonal metric (21,1). It compares the triangle with its negative and fourfold repeats. Ferudun's printed Section 6.1 additionally uses two primitive hexagons in x squared/4+y squared=1 to obtain unequal doubled twelve-vertex products 250/3 and 256/3. Thus a new numerical/radical fixture or an elementary connected-family proof can be useful verification/exposition, while the boundary conclusion itself already overlaps. No priority claim for such a refinement is established here.

## Deposit chronology: native evidence, not self-declared dates alone

Primary endpoints:

- [Zenodo record JSON](https://zenodo.org/api/records/23093706)
- [Zenodo separate file metadata](https://zenodo.org/api/records/23093706/files)
- [Zenodo version listing](https://zenodo.org/api/records/23093706/versions)
- [DataCite DOI metadata](https://api.datacite.org/dois/10.5281/zenodo.23093706)

The native record was created on 2026-10-02 at 02:43:18.639796 UTC and modified at 02:43:19.872769 UTC. More strongly, the separate files API associates the *current matching PDF checksum* with file creation at 02:43:18.692673 UTC and update at 02:43:18.726988 UTC that day. It associates the matching source ZIP with creation at 02:43:18.737463 UTC and update at 02:43:18.768831 UTC. DataCite reports creation, registration and update at 2026-10-02T02:43:20.000Z. The public version listing reports one version (revision 3), and the files match it. There is no evidence of later file replacement in these public records.

These observations support dating the exact deposited content to October 2, rather than treating October 2 as only an author-supplied manuscript date. They do not prove the first moment any proof was discovered, written privately, shared, or exposed to another party. Metadata in downloaded ZIP documents and script receipts is self-reported evidence of the retained workflow, not an independent timestamp authority.

The root's preserved native GitHub evidence identifies PR207 creation at 2026-10-01T05:42:14Z and updated_at equal to that value, with current preserved head a7f8486548122c7d545430821afeedbccf48b3e7. That commit records author/committer time 2026-10-01T05:41:59Z. The root has separately pinned the current head proof and full submission-range tree. Commit timestamps are not publication receipts, and this audit does not certify a forensic PR-opening-head transaction. The conservative chronology is therefore: the public PR is dated October 1; the currently preserved submitted proof is attached to that PR and pinned; the exact Ferudun deposit content is natively dated October 2; the new root boundary and proof-reconstruction work is dated October 16. Do not backdate those later additions to the PR date.

The GitHub PR date preceding the Zenodo deposit makes “we only discovered the theorem after an already published October 2 paper” an unsupported account of the original attempt. Conversely, those dates do not establish that Kriebel's proof was first ever, that Ferudun saw or did not see it, that either effort was causally independent, or that discoveries were simultaneous. A careful publication can record the observed dated objects without asserting those stronger historical facts.

## Earlier primary source findings

The original [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), Table 9 on printed page 11, was inspected as text and pixels. It lists A times one focal inverse area as k804,a for N congruent to zero modulo four, with an unknown general proof. Its neighboring k804,b gives the N4 value 4. This is the source observation; it is not prior proof of the full theorem.

Garcia and Reznik's [2022 companion, DOI10.33039/ami.2022.02.001](https://doi.org/10.33039/ami.2022.02.001), publisher PDF pages 7 and 10, was inspected as text and pixels. Table 1 relabels this product k805,a, lists low-period derived cases 4,4i,8, and leaves the general-proof column unknown. Proposition 4.9 gives the simple N4 value 4. The dagger refers to unit focal inversion of original vertices. Therefore low-period novelty is excluded, while that table alone does not establish an arbitrary-period theorem or current openness.

The 2021 *Fifty New Invariants* k804 is an angle-cosine sum; the submitted source notes' edition distinction is consistent with the primary companion and Ferudun's full text. No inference about mathematical resolution follows merely from removal of the original product row in the shorter journal edition. This lane did not independently re-audit every page of the 2021 final edition; the root's separate source-contract lane covers that check.

The PR206 overlap, DOI10.5281/zenodo.23096994, is a different odd-period product of the two inverse areas. It does not replace the exact PR207 citation above. This distinction is an input from the assignment and root's accepted preceding case; this lane did not re-run the PR206 source audit.

## Search coverage and limitations

SEARCH_LOG.json records the bounded query families, exact primary landing and record followups, and excluded irrelevant results. Exact expressions, original and later row labels, focal-inversion terminology, date-qualified searches, arXiv and Zenodo searches, and the Ferudun site were used. Search engines produced the original observation, the 2022 low-period article, adjacent bicentric/triangle work, and the exact Ferudun record. No additional exact general theorem was fully verified by this lane. That is a bounded negative search result and does not certify absence of older, differently phrased, unpublished, non-English, or unindexed work.

A 2026 inversive-distance/Poncelet lead, DOI10.1007/s12215-026-01409-7, remains outside this lane's full-text audit and was sent to the root for the independent general-theorem lane. It is not used to support any novelty conclusion here. Likewise, abstract/snippet-only adjacent results and third-party reposts were never treated as positive exact-theorem evidence.

The new telescoping/Fourier reconstruction is not an exception to the theorem overlap: even if correct and structurally distinct, its method-level priority would require checking classical cyclic Jacobi and multiplication identities as well as the precise new rational identity. The root has a separate general-method audit for that question. This report establishes no novelty for that route.

## Strongest defensible conclusion and remaining gap

**The exact least-period theorem and the repeated-list obstruction are already represented in a full, dated, publicly deposited October 2 preprint. They require explicit attribution in any current verification note.** This suffices to reject framing an October 16 publication as a sole novel resolution. It does not erase the observed October 1 PR date or adjudicate firstness between the attempts.

The exact historical priority relation and causal independence remain unresolved. The original PR proof's mathematical review, the newly supplied elementary boundary verification, and reproducible current checkers may support a qualified verification note if the root's full process approves it. No mathematical or bibliographic content has been merged, no repository status changed, and no service write or communication with outside individuals occurred in this lane.

Completion estimate: **100% of this bounded exact-result/deposit audit**; not 100% of PR207 or the persistent program. No exhaustive novelty certificate, current-openness declaration, firstness claim, independence claim, or publication approval is issued.
