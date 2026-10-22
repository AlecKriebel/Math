# Independent priority adversary: Kohl tree equality

Frozen findings, 2026-10-17. This is a bounded independent priority-falsification audit, not a certificate of firstness or present openness.

## Decision

I did **not** find an inspected earlier theorem or construction that establishes a strict arbitrary-list L(2,1) gap on a finite tree. I did find a substantial older overlap: Fiala and Škrekovski already exhibited a five-list L(2,1) gap on a ten-vertex graph in their 2001 preprint. Its actual drawing is cyclic. A direct transfer by edge or vertex deletion with the inherited lists fails: all 66 connected spanning trees have feasible inherited list assignments, with witnesses preserved here.

The submitted manuscript's explicit statement that it makes no historical novelty, priority, exhaustive-survey, or current-openness claim is defensible. This audit supplies **no clearance to remove that qualification**. The most material outstanding sources are the full 2005 Kohl–Schreyer–Tuza–Voigt paper, Chen's 2004 thesis/manuscript and related 2005 Kuo talk, Jonas's 1993 thesis, the journal version of the Fiala–Škrekovski paper, and exact later planar sharpness constructions.

No candidate files were changed. No outside individual was contacted, no outreach was prepared, no Git write or publication was performed, and no other priority-family findings were read. Only the candidate statement/proof and original mathematical sources were used. Downloaded input PDFs, extracted text and rendered images are local research inputs and **are not distributed**. Authored reports, code, metadata and the witness artifact are distinct from those inputs.

## Claim and disqualifying alternatives

The target is equality, for every finite tree T, of (a) the minimum k allowing labels in the common initial segment {1,...,k}, and (b) the minimum k guaranteeing a labeling from every assignment of k-element positive-integer lists. Adjacent labels differ by at least two; labels at distance two differ. The specimen is the eleven-vertex caterpillar in submitted/PROOF.md, with ordinary palette size 5 (span 4), list parameter 6, and bad lists A={1,2,3,4,5}, B={1,3,4,5,6}. Its original leaf-path extensions retain these values.

Allowing zero instead of insisting on positive labels does not change these universal parameters: a common integer translation of all lists and chosen labels preserves every constraint. Restricting lists to consecutive intervals would change the problem; the specimen uses a noninterval list.

An earlier different countertree would defeat a universal-resolution novelty claim just as effectively as an isomorphic specimen. By contrast, a gap for L(d,0), L(p,1) with p>=4, circular coloring, a cyclic graph, unequal lists/precoloring, reconfiguration of two existing solutions, or an ordinary upper-bound algorithm does not do so without an additional exact implication. An upper bound of Delta+3 is not by itself a gap; one must also establish an ordinary palette of Delta+2 for the same tree.

## Original source and family boundaries

I inspected Kohl's OWR contribution in full, printed pp.414–417, using the authenticated local original PDF (SHA256 720ad8b58092744bb37446dd53a02d9e31dc1caf8eee3b27ad0ad52ff96bbd15). Its definitions and p.416 give exactly the arbitrary-list/common-initial-segment comparison. The p.417 reference continuation matters bibliographically. The source is [OWR 7/2006](https://ems.press/content/serial-article-files/46037?nt=1), [DOI](https://doi.org/10.4171/OWR/2006/07).

I inspected the thesis's section 4.4, printed pp.124–130, and the relevant pp.96–98 and142–143 references, from the original PDF (SHA256 ae2d73fcf89ba4d36925d18ff492958149c1ce9d82e1a2b2a5513a1f67433828). The thesis explicitly distinguishes previously overoptimistic equality for other separation vectors from the L(2,1) tree conjecture. The proved radius-two/double-star/two-star families and the specified Delta>=4 caterpillar families do not contain the radius-three, Delta=3 specimen. This is a scope check, not evidence of later openness. [Kohl thesis](https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf).

## Positive older overlap: actual Fiala–Škrekovski example

The primary [KAM 2001-530 preprint](https://kam.mff.cuni.cz/kamserie/clanky/2001/s530.pdf), *List distance labelings of graphs*, has the target list convention on pp.3–4, path/cycle equality on pp.7–13, and an explicit strict gap in Figure 4 and the text of p.14. I inspected these portions and rendered/viewed the complete p.14. The graph has ten vertices and twelve edges: two triangles joined along two parallel three-edge paths, with a central eight-cycle. The displayed lists are {1,2,4,5,6} at the leftmost vertex and {1,2,3,4,5} elsewhere. The displayed ordinary labeling uses palette 5.

This is real priority overlap for **general-graph** five-list obstructions, not the specimen: vertex/edge counts, cycles and the list pattern differ. In particular it defeats any claim to the first L(2,1) list/ordinary separation in general. The supplementary check `check_fiala_figure4.py` transcribes the picture, verifies the displayed ordinary witness, finds its bad assignment infeasible, enumerates the 66 connected spanning trees, and saves a feasible labeling for every one in `check_fiala_figure4.json`. Every forest subgraph extends to a spanning tree, so deleting vertices/edges with inherited lists cannot turn this example into a bad tree assignment. This is a checked finite statement, not a claim about other possible gadgets or lists.

There is a bibliographic version trap. OWR/thesis cite *List distance-labelings of graphs*, DAM148(1)13–25 (2005), but the [publisher DOI metadata](https://doi.org/10.1016/j.dam.2004.11.005) and [Fiala's own publication list, p.3 item27](https://kam.mff.cuni.cz/~fiala/papers/publications.pdf) give *Generalized list T-colorings of cycles* at those coordinates. The full journal body was inaccessible here. I do not assume that every preprint example or conclusion survived unchanged, or that the journal lacks extra examples.

## Exact transformation challenges

### Total/incidence labeling

I inspected [Yu, Wang and Liu, arXiv:1105.1906v1](https://arxiv.org/pdf/1105.1906), pp.1–6, especially Observation1 and Section2. This is a genuine exact equivalence between list (p,1)-total labeling of G and list L(p,1) labeling of its incidence/subdivision graph S_I(G). The explicit strict gap following Lemma2.7 uses paths and **p>=4**. Its p=2 paths and stars yield equality, so that paragraph is not a prior resolution of the target. Theorem2.6 merely recovers the earlier tree upper bound.

Independent boundary deductions: S_I(G) is a tree only if G is a tree; a cycle remains a cycle after subdivision. Moreover each edge of S_I(G) has a degree-two subdivision endpoint. The specimen has edges a-b and d-e joining two degree-three vertices, so neither it nor its leaf-path extensions is an incidence graph. This does not exclude a different prior countertree through total labeling.

The saturated height-two sharpness family quoted in Lemma2.7 is also insufficient at p=2: a degree-Delta vertex whose neighbors all have degree Delta forces ordinary palette at least Delta+3. With palette {1,...,Delta+2}, a degree-Delta vertex can use only an endpoint, forcing all of that center's neighbors to the same opposite endpoint, contrary to their distance-two constraints. Thus this familiar sharpness mechanism does not supply the missing ordinary Delta+2 side of a gap.

### Generalized list T-coloring

I inspected [Fiala, Král' and Škrekovski, KAM2003-647](https://kam.mff.cuni.cz/kamserie/clanky/2003/s647.pdf), pp.1–5 and25–29, including Theorem5 and its examples, against the [publisher abstract](https://epubs.siam.org/doi/10.1137/S0895480103437870). The characterization is for balanced/overbalanced instances, with list sizes controlled by the sum of forbidden-difference-set sizes on incident edges. Translating the target to T squared uses t={0,1} on original edges and {0} on distance-two edges. At specimen vertex b this sum is 2*3+3=9, while the bad list size is5. Therefore the balanced theorem does not directly classify this instance. The illustrated generalized obstructions also have cycles and/or different forbidden sets; no exact tree gap was extracted.

### Backbone formulations

The primary author manuscript [Bu, Finbow, Liu and Zhu, *List backbone colouring of graphs*](https://www.calstatela.edu/sites/default/files/listbackbonefinal.pdf), pp.1–12, was inspected, including its sharpness example on p.8 and all result statements. The L(2,1) equivalence requires the pair (G,H)=(T squared,T); simply having a spanning tree backbone does not make the model L(2,1) on that tree. Its sharpness example uses an odd-cycle G and a common three-list obstruction, so ordinary and list requirements already coincide there.

I also inspected [Pimpasalee and Nakprasit, AJC66(3)378–392 (2016)](https://ajc.maths.uq.edu.au/pdf/66/ajc_v66_p378.pdf), printed pp.378–382, especially the complete main theorem. Here the outer G is a path or cycle, not the square of a nontrivial branching tree. The path L(2,0) gap does not imply the target: adding distance-two requirements also changes the ordinary parameter. The [2018 conference abstract](https://www.math.fau.edu/combinatorics/pimpasaleewannapol.pdf) states further Halin/backbone results; it is one page and provides no target tree gap.

## Unresolved primary-source checks

These are explicit limitations, not claimed resolutions or cleared sources:

| Source | Evidence obtained | Exact gap |
| --- | --- | --- |
| Kohl–Schreyer–Tuza–Voigt, TCS349(2005)92–98, [DOI](https://doi.org/10.1016/j.tcs.2005.09.032) | Publisher abstract/references and publisher API metadata; upper bound is also in Kohl's original thesis and Yu et al. | Direct publisher/PDF requests failed; API supplied core metadata only. Full original sharpness proof/examples not independently inspected. |
| Chen, *The list-L(2,1)-labeling problem of graphs* | Kohl thesis p.142 calls Y.Chen's item a manuscript. Zhou–Shiu–Lam's primary paper references identify Y-J.Chen, M.Phil.,2004, National Dong Hwa University. | Full thesis and whether these are exactly the same version not established. Do not infer absence of tree examples. |
| Kuo, 2005 TMS/AMS talk with the same title | [Kuo's institutional page](https://am.ndhu.edu.tw/p/404-1038-5251.php?Lang=zh-tw), conference-publication entry, inspected | No actual abstract/slides obtained. Relation to Chen version remains a plausible lead, not a verified identity. |
| Jonas, 1993, *Graph coloring analogues...list lambda-labelings* | [University doctoral record](https://phd.cosw.sc.edu/study/colleges_schools/artsandsciences/mathematics/alumni/graduate_alumni/index.php) and advisor's primary record; ProQuest identifier9400228 | ProQuest inaccessible; no thesis body inspected. Title alone does not establish its list convention or tree claims. |
| Fiala–Škrekovski 2005 journal version | Publisher metadata and author bibliography | Full body unavailable; see version trap above. |
| Ito–Kawamura–Ono–Zhou, reconfiguration, TCS544(2014)84–97, [DOI](https://doi.org/10.1016/j.tcs.2014.04.011) | Publisher abstract and [author institutional list](https://www.ecei.tohoku.ac.jp/alg/papers/papers_2014.html) | No full paper obtained. Its abstract assumes two existing labelings, which by itself provides no choosability gap; hidden tree examples remain unchecked. |
| Zhu et al., planar list L(2,1), DM341(2018)2211–2219, [DOI](https://doi.org/10.1016/j.disc.2018.04.025) | Publisher abstract asserts Delta+3 upper bound and examples attaining it | Full sharpness construction not obtained; whether its ordinary parameter is already Delta+3 not independently established. |
| Kohl, 11th C5 workshop, Question8.1 | Search index exposes actual question/special-family statements; CiteSeer retrieval failed | No actual body obtained, so not counted as source-body inspection or an independently dated prior version. |
| Raspaud–Zhu, JGT55(2007)249–265, [DOI](https://doi.org/10.1002/jgt.20234) | Publisher abstract defines list circular coloring: one edge-separation parameter in a cyclic palette | Author PDF failed certificate/retrieval checks; abstract already differs from target, but no full-paper clearance claimed. |

The title/citation trail of Chen was cross-checked in the actual primary [Zhou–Shiu–Lam paper, pp.219–223 and231](https://shiu1958.github.io/PDF/P1310pub.pdf), where the tree case is a spider and the proved list value is p+2 (Theorem2.2). This covers one branching vertex, not the four degree-three vertices of the specimen. Cartesian products with a nontrivial path contain cycles. Thus the inspected result is another positive special family, not a gap.

No project's own AI-generated posts, preprints, repository copies or search hits were accepted as an independent earlier discovery. Search-engine crawl/relative publication dates were not used as historical discovery dates. The editorial date near 2026-10-11 does not establish the first discovery date of this construction. A claim of priority would need independently authenticated earlier-artifact dating as well as the remaining source investigation.

## Defensible framing

Retain the exact theorem and explicit counterexample, its source attribution to Kohl's conjecture, and the disclaimer about historical novelty. If historical context is expanded, acknowledge that general-graph L(2,1) five-list separations already occur in Fiala–Škrekovski's early preprint. A defensible report of this audit is: “An independent theorem/example-based audit found no prior tree resolution among the source portions inspected; priority remains unresolved, with identified primary sources still to inspect.”

The audit's strongest verified adverse result is the early cyclic five-list gap, plus the exact failed deletion transfer. The strongest remaining priority gap is not a mathematical gap in the submitted theorem; it is the uninspected historical source bodies and unindexed literature. Negative searches cannot close it.
