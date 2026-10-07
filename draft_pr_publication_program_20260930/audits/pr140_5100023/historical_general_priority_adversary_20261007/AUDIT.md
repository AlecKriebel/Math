# PR140 historical/general priority audit — independently frozen verdict

The inspected historical primary sources do **not establish an earlier full proof of the focal antipedal centroid invariant k405 or its explicit coefficient**. They do establish nearly all surrounding machinery, including the exact skew-hodograph transformation and the ordinary boundary-tangent pedal centroid theorem. A target-specific opposite-edge antipedal identity is still needed to bridge those results to k405. The bridge in DEDUCTION_AUDIT.md is a new reviewer deduction using the accepted candidate identity; it is not evidence that this full deduction had been published earlier.

**Verdict:** historical literal full subsumption not established; historical formula subsumption not established; novelty undetermined. There is no absolute priority clearance and no recommendation to close as already_solved from these historical sources alone. No new mathematical defect was alleged or mathematical gate repeated.

## 1. Target, independence and success criteria

This family concerns PR140 / problem5100023 / k405, original head 9e908ae58b5ceee6a0825bbebd8acf565db55340. Its input is repaired_candidate_v1/PROOF.md, whose exact pin is in RESULT.json. The mathematical gate passed before this priority assignment. The target is the unweighted centroid of the unprimed antipedal intersection polygon of a primitive even periodic billiard orbit in a noncircular ellipse, with a strictly nested nondegenerate confocal elliptical caustic. The poles are O and either focus. Simple and star orbits are admitted. Hyperbolic/degenerate caustics, area centroids, outer-polygon antipedals and arbitrary even-length listings of repeated odd-period orbits are outside the repaired claim.

A historical positive subsumption finding would require either an actual prior statement/proof for this centroid, or a complete prior theorem whose hypotheses and construction provably identify this centroid without inserting the candidate's central lemma. An elementary consequence can be old even without the k405 label; conversely, assembling old dynamical tools around a new target-specific identity does not prove historical resolution.

The initial checkpoint was frozen before exchanges about the finished verdict. No contemporary priority-family report was read. An incidental exact contemporary search hit was referred to ROOT without opening its manuscript; its chronology is outside this family's conclusion. ROOT later supplied chronology steering, which is not represented here as independently checked evidence.

## 2. What the source actually left open

Reznik–Garcia–Koiller arXiv:2004.12497v11 (29 October 2020), Section 3.5/Table 5, printed p.7, records k405 as the vertex centroid C0* for even N and poles O/f1/f2, with question marks in the value/proof positions. Table 4 credits Bialy–Tabachnikov for the distinct pedal cases k302/k306. These adjacent entries are material evidence that the authors distinguished the already-proved pedal theorem from the unresolved antipedal entry. They are not an absolute certification that nobody else had a proof.

The antipedal definition is intersection of consecutive lines through the original vertices perpendicular to the pole-to-vertex rays. The published companion's Table 5, p.348, retains k405 in that sense. Section 3.7 of v11, printed p.8, states that “opposite vertices of an even N-periodic are reflections about the origin.” This supports the repaired primitive-period convention, though the source does not formally define least period. The mathematical audit already addressed repeated-odd ambiguity; this family does not broaden the claim.

Primary bodies actually read: v11 HTML definitions/tables/Section 3.7; published companion/table already held by ROOT and examined in the earlier geometric audit. The new v11 body is privately pinned here. [Source v11](https://arxiv.org/html/2004.12497v11), [published companion](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).

## 3. Strongest old results and exact hypothesis mapping

### Bialy–Tabachnikov: the old tensor and pedal invariants

Theorem 4.1 fixes the centroid of perpendicular feet from an arbitrary fixed pole to **outer-ellipse tangents at the billiard vertices**. It explicitly identifies k302/k306. Corollary 3.2 gives the boundary-normal second-harmonic sums; Theorem 2.2 supplies first-variation/support identities. These are directly applicable to a genuine billiard orbit, including the transformed orbit below.

They do not identify intersections of lines through original vertices perpendicular to focal rays. Their Theorem 4.3 proof uses even-period central symmetry, so the center-pole part of k405 rests on a classical elementary mechanism. The focal antipedal claim is not stated there. Both the May 2020 v2 and the actual published PDF were read; relevant published pp.1346,1348,1349 were visually checked. Published online 11 September 2020; journal volume 2022. [Preprint](https://arxiv.org/pdf/2001.08469v2), [published full text](https://par.nsf.gov/servlets/purl/10408490), [DOI](https://doi.org/10.1007/s40879-020-00428-7).

### Gutkin–Tabachnikov and Akopyan–Schwartz–Tabachnikov: the transformation is prior

Gutkin–Tabachnikov (2002), Section 7, pp.296–299, Theorem 7.1, Proposition 7.3 and Corollaries 7.6–7.7 give the orbit correspondence and length-preserving periodic duality. The elliptic specialization maps (P_i,w_i) to (D w_i,-D^(-1)P_(i+1)); Example 7.8 attributes it to Veselov (1988/1991). The PDF was legitimately downloaded from the author's own linked public file. The relevant theorem pages were read and rendered.

Akopyan–Schwartz–Tabachnikov Lemma 3.1/Remark 3.2 explicitly revisit this same construction in 2020; the published pp.1318–1319 were visually checked. These sources justify the transformed billiard and family correspondence, rather than silently applying a Euclidean billiard theorem after arbitrary affine scaling. They contain no focal antipedal centroid bridge in the inspected sections. [Gutkin–Tabachnikov author-linked PDF](https://drive.google.com/file/d/1UdPIWG09B7XHjUTxUCe8W-0MZMxdWk5u/view), [DOI](https://doi.org/10.1016/S0393-0440(01)00039-0), [AST preprint](https://arxiv.org/pdf/2001.02934v2), [AST published full text](https://par.nsf.gov/servlets/purl/10408491).

### Weill 1878: genuinely old focal invariants, different centroid objects

The original NUMDAM scan was read, with printed pp.270–271 and303 rendered for literal verification. Part I Theorem V fixes the centroid of the contact-point polygon of a bicentric polygon. Its alternate formulation on p.271 concerns a circle-inscribed polygon circumscribed about a conic with a focus at the circle center. Neither is the raw antipedal of a confocal ellipse billiard.

Part II Theorem XXXI, p.303, is broader: for Poncelet polygons between conics with a common focus it gives constant focal directional-cosine sums, inverse focal-radius sums and step-separated focal angular cosine sums. This is actual old coverage of related focal invariants, not merely a modern author's historical attribution. Theorems XVIII–XX concern particular derived contact-polygon constructions. None of these located statements supplies the needed focal antipedal pair identity or its centroid coefficient. [Original Weill scan](https://www.numdam.org/item/JMPA_1878_3_4__265_0.pdf).

### Schwartz–Tabachnikov 2016: ordinary Poncelet centroid and contact polarity

Theorem 1, preprint p.7, makes the ordinary Poncelet vertex/lamina centroids trace homothetic ellipses or points. Section 3's compact-curve/pole-cancellation proof requires the actual centroid expression and its singularity cancellations. It does not state a theorem for every rationally derived polygon.

Remark 3.1(i), p.10, extends to a tangency-point Poncelet polygon through ordinary conic polarity. Theorem 2 on p.10 is the contact-centroid constancy for homothetic nested ellipses attributed to Weill. A noncircular confocal pair with lambda>0 is not homothetic; the antipedal also differs from ordinary polarity unless an inversion is inserted. The complete relevant HTML body and web-parsed PDF sections were read; a full private PDF was not retained because its 5.10 MB exceeded the bounded retrieval limits. [Primary full text](https://arxiv.org/html/1607.04766v1), [DOI](https://doi.org/10.1007/s00283-016-9622-9).

### Tsukerman 2012: negative pedals with restrictive sampling hypotheses

Definition 1.1 and Theorem 3 use equal consecutive focal angular steps. Section 4, pp.12–16, studies negative pedals of equally spaced circle points; Theorems 10–11 identify the resulting conic/discrete-conic polygons. Those hypotheses are not given for raw elliptic billiard vertices. Unequal axial scaling of an ellipse to a circle does not preserve the perpendicular-line construction. The relevant full PDF sections and listed theorems were examined. This is a useful classical construction, not a verified general-even k405 result. [Primary PDF](https://arxiv.org/pdf/1212.0200v1).

### Poncelet grids, projective integrals and circummass results

Levi–Tabachnikov's 2005 preprint/2007 article, Sections 1–3, constructs intersections of original side lines and confocal Poncelet-grid objects. The initial grid theorem is stated with odd n. It neither identifies the candidate antipedal nor proves its Euclidean centroid fixed. [Primary PDF](https://arxiv.org/pdf/math/0511009), [DOI](https://doi.org/10.1080/00029890.2007.11920482).

Schwartz's author PDF dated 3 February 2014, Theorem 1.2 p.4 and surrounding Sections 1–2, proves constancy of pentagram monodromy invariants in Poncelet families. The project's target is a Euclidean focal centroid; no identity identifying it with a projective monodromy invariant was located. A known algebraic integrability method alone is not target subsumption. [Author PDF](https://www.math.brown.edu/~res/Papers/poncelet_monodromy.pdf), [DOI](https://doi.org/10.1016/j.geomphys.2014.07.024).

Chávez-Caliz 2020, Theorems 2–3 and Proposition 2, concerns circummass loci, even-period original/outer area products, and a lamina-centroid degeneration. These are different quantities/constructions. Its relevant primary HTML theorem statements were read; it does not establish the unweighted antipedal mean. [Primary full text](https://arxiv.org/html/2004.05404v1).

## 4. The bridge and what it proves about priority

DEDUCTION_AUDIT.md contains the complete checkable transformation mapping. On the skew-hodograph orbit, the tangent normal at the vertex associated with midpoint angle t is (-sin(t),cos(t)). Opposite perpendicular-foot means from a fixed point (d,0) are (d cos^2(t),d sin(t)cos(t)).

The candidate's accepted focal opposite-edge identity is an affine image of that pair mean, with a fixed lambda-dependent diagonal matrix and translation -h e_x. Once this **additional focal lemma** is supplied, the old Bialy–Tabachnikov pedal theorem proves focal centroid constancy, and its harmonic formulas recover exactly the candidate's coefficient.

The target-specific missing work is not the circle action, conserved perimeter, normal-harmonic sums or skew-hodograph isomorphism. It is the relation of the antipedal intersections to those quantities: solving the two focal line systems, pairing opposite edges, and exploiting the focus/confocal denominator cancellation. This is exactly candidate Eq.(8) in another form. No located prior primary source in this audit states that complete relation.

Therefore:

| Question | Bounded answer |
|---|---|
| Are the surrounding dynamical tools old? | Yes, explicitly published; the skew map is documented at least by 2002 and attributed there to earlier Veselov work. |
| Is the origin-pole cancellation a new mechanism? | No, it follows from classical even-period central symmetry. |
| Does an old theorem prove the focal mean after adding the candidate identity? | Yes. The deduction is written out. |
| Does that demonstrate a prior full k405 proof? | No. The target-specific identity was inserted from the accepted candidate. |
| Is that identity absent from all historical literature? | Not established; the audit is bounded and sources/indexing are incomplete. |
| Is the explicit focal coefficient novel? | Undetermined. It follows from old harmonic formulas plus the additional bridge. |
| Does this justify already_solved historical disposition? | Not from these findings alone. |

This distinction matters even for constancy alone. Producing a new formula would not rescue a priority claim if the full original constancy result were already proved. Here, however, full prior constancy has not been established by the inspected old sources.

## 5. Reproduction, evidence custody and gaps

The final bridge_controls.py makes 18 exact algebraic checks in both normal and optimized mode. Explicit failures remain active under optimization. It does not run the author verifier, simulate orbit dynamics, search for a new central proof, or prove historical publication from mathematics. Eq.(8) is visibly an accepted premise. Final receipts bind exact code, UTC, PID, interpreter and SymPy versions. The initial unsealed controls and receipts remain private precursors.

PRIMARY_SOURCE_MANIFEST.json records actual bodies, hashes, dates, read extent and page mappings. Copyright PDFs, extracted text and rendered images remain in ignored private_primary_sources; portable audit evidence contains only metadata, original reviewer derivations and short quotations. Public source receipts record a bounded failed PDF retrieval honestly rather than claiming inaccessible mathematics.

Remaining limitations:

- Original Veselov 1988/1991 bodies and the M'Clelland 1891 treatise were not read. The precise old skew statement is independently supplied by the actual 2002 body, so this does not prevent the bounded transformation conclusion.
- No exhaustive search of all books, languages, unpublished correspondence, theses or unindexed papers was performed.
- The 2016 primary HTML is fully available; private PDF non-retention was a resource choice, not a paywall blocking the relevant theorem check.
- Search silence is not novelty evidence. SEARCH_LOG.json retains queries and attempted-access limitations.
- The September/October 2026 exact-result chronology and contemporary source family are ROOT's separate task; the incidental later hit is not treated as prior resolution here.

The current proof already makes no novelty claim. Any future paper should credit the classical origin cancellation and conserved quantities. If it uses this alternative proof, it should cite the prior skew-hodograph and pedal theorems and explicitly state/prove the extra antipedal identity. It should not assert a new conserved tensor, first historical proof, exhaustive novelty, or already_solved status on the basis of this bounded review.

## 6. Frozen checkpoint

Actual final UTC/PID, exact candidate pin and the closed portable file set are in RESULT.json and FINAL_MANIFEST.json. Best-guess family completion is 100% of this bounded historical/general assignment. Overall priority, authorship chronology, publication suitability and case disposition remain ROOT's responsibility and are not marked complete by this report. No Git, shared-native record, PR, paper, DOI, tracker or external outreach mutation was performed.

