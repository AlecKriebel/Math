# PR66 independent mechanism and bound priority audit

Completed bounded audit: 2026-10-04. Candidate head: `78f4a7fadac0fd24e147a617956cb409eb6a579e`. The candidate's literal `claimed_solved` remains `1/5`; no ledger or candidate artifact was changed.

**Priority verdict: the universal inequality is an immediate consequence of an earlier explicit knot estimate. PR66 cannot presently be credited as the first proof of that inequality. The particular directed chord graph and fair tournament completion proof may be a distinct presentation, but its originality and earliest priority have not been established.** The older implication includes the precise normalization and all classical diagrams. The candidate's even refinement also follows from earlier formula and realizability ingredients, although this audit did not locate that refinement explicitly printed as an earlier universal inequality.

## Exact comparison and decisive pins

Write `u` for the target invariant: additive, mirror odd, `u(right trefoil)=1`, and

    u = -(J'''(1)+3J''(1))/36,
    [h^3]J(e^h) = -6u.

The target is `|u(K)| <= floor(c(c^2-1)/24)` for every classical diagram of `K` with `c` crossings. Positivity, alternation, primeness, minimality and torus hypotheses would not constitute a full match.

Fiedler and Stoimenow's [author PDF, current version February 1, 2002](https://stoimenov.net/stoimeno/homepage/papers/inv.pdf) has these decisive pins: printed p.6 Remark 3.1 identifies `v_t3=4u=-J''(1)/3-J'''(1)/9`; printed p.7, opening display in §3.2, states `|v_t3| <= binom(c,2)+binom(c,3)`. The surrounding section introduces an arbitrary diagram; its preceding positive-diagram Theorem 3.1 is separate. Printed pp.4-7, including the formula and counting convention, were visually inspected. The display is not a numerical experiment or a special-class theorem.

The independently checked algebraic implication is

    binom(c,2)+binom(c,3) = c(c^2-1)/6,
    |u| <= c(c^2-1)/24.

Integer-valued `u` supplies the floor. This inference uses the first, sharper part of the displayed estimate; discarding it in favor of its following `c^3/6` term would miss the full match. Boundary values `c=0,1,2` give zero after taking the floor, and `c=3` gives one. There is no degree-two correction in the normalization conversion.

The same manuscript's printed p.8 final paragraph before §4 contains an unnumbered extremality assertion about two-strand torus knots for odd crossing counts and the following even count. Its claimed even consequence is stronger than the candidate's even bound. This audit does **not** certify that stronger assertion: the paper supplies no detailed extremal derivation there. The decisive priority comparison above does not depend on it.

## Versions and dates

| Body / source | What was authenticated | Remaining limit |
|---|---|---|
| [Fiedler-Stoimenow 2002 author PDF](https://stoimenov.net/stoimeno/homepage/papers/inv.pdf) | Downloaded 268871 bytes; SHA256 `193dfd4c993f2337ba17b48f524d8c71333f8717d520ba299f7b76a8cbd324b7`; printed pp.4-8 inspected as pixels. Exact normalization and universal estimate. | This is the author's updated body, not a publisher scan of the 2000 printing. |
| [Author-uploaded older manuscript](https://www.researchgate.net/publication/2598153_New_Knot_and_Link_Invariants) | Primary manuscript text says current version February 1, 1999, first version December 9, 1996; Remark 3.1 printed p.6 has the same conversion; §3.3 printed p.8 has the same binomial estimate. ResearchGate records author Thomas Fiedler's upload on August 13, 2014. | PDF download failed. Manuscript-date evidence does not authenticate its exact date of public circulation. Platform “February 1970” is erroneous metadata. The 1996 first-version date does not establish the estimate was in the 1996 body. |
| [Author publication list](https://stoimenov.net/stoimeno/homepage/papers.html) | Identifies *Knots in Hellas '98*, Series on Knots and Everything 24, World Scientific, 2000, and minor updates/corrections in hosted bodies. Bibliographic citation is pp.59-79, DOI `10.1142/9789812792679_0006`. | Bibliographic publication date is not direct confirmation of every formula in the printed 2000 body. |
| [Publisher PDF endpoint](https://www.worldscientific.com/doi/pdf/10.1142/9789812792679_0006) | Attempted ordinary public retrieval; returned HTTP 403. | Exact printed-2000 body remains unavailable in this audit. No access-control bypass attempted. |
| [CiteSeer older manuscript endpoint](https://citeseerx.ist.psu.edu/document?doi=012c27ee014fc232d822cdccf7fbffe75ee2f532&repid=rep1&type=pdf) | Search index corroborates the 1999 title-page date; direct retrieval timed out. | Search metadata alone is not decisive mathematical evidence. |

The securely inspectable pre-2026 bodies defeat a present first-result claim even with the publisher-version gap. They do not establish an earliest date or author beyond the evidence above. The coexistence of this display and Ohtsuki's 2002 printed conjecture is a real historical discrepancy, not grounds for suppressing either primary source.

## Even refinement: older ingredients, explicit inference

Fiedler-Stoimenow Eq.(1), printed p.5, contains two disjoint triple families of weight at most one per unordered triple, plus a linked-pair term of absolute weight at most one per unordered pair. Its counting convention takes one matching permutation even when a pattern has automorphisms. If `m` is the number of linked pairs, the same counting gives

    4|u| <= binom(c,3)+m.

[Stoimenow, *Positive Knots, Closed Braids and the Jones Polynomial*, Ann. Scuola Norm. Sup. Pisa (2003)](https://numdam.org/item/ASNSP_2003_5_2_2_237_0.pdf), printed p.245 Lemma 3.2, states the even valence condition for any classical Gauss diagram. That lemma has no positivity or reducedness hypothesis; the following Lemma 3.3 does. The complete relevant printed page was rendered and inspected.

For even `c>=2`, each vertex has even degree at most `c-2`, so `m <= c(c-2)/2`. Thus

    4|u| <= binom(c,3)+c(c-2)/2 = c(c^2-4)/6.

This is the candidate's even refinement. `c=0` is handled separately. **This paragraph is an independently verified implication of earlier ingredients, not a claim that the exact even formula was explicitly published there.** The old formula already exposes the linked-pair count, so the refinement does not require the candidate's tournament mechanism.

## Ingredient credit and graph mechanism comparison

| Ingredient / nearby work | Precise body pin | Comparison |
|---|---|---|
| [Polyak-Viro, 1994](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf) | Theorem 2, Eq.(5), printed p.448. Two homogeneous three-arrow patterns, coefficients `1/2` and `1`, with trefoil-one normalization. | Imported exact formula; neither its availability nor rediscovery is new. The target tournament application was not located in this body. |
| [Grzesik-Kráľ-Lovász-Volec, *Cycles of a given length in tournaments*, arXiv 2008.06577v3](https://arxiv.org/pdf/2008.06577v3) | Introduction, manuscript p.2. Exact odd/even maximum cyclic-triangle counts, controlled by degree sequence. References 14 and 23: Kendall-Babington Smith (1940), Szele (1943). | Classical graph extremum. Historical attribution is reported from this primary research paper; the original 1940/1943 bodies were not inspected. An old tournament identity alone is not prior knot resolution. |
| [Acan, *A uniform random chord diagram*, arXiv 1501.01489](https://arxiv.org/pdf/1501.01489) | §5 defines directed intersection graphs by chord over/under crossings; Lemma 5.3, manuscript p.16, invokes random tournaments for strong connectivity of a balanced intersecting clique. | Existing intersection edges are independently randomly directed. This differs from deterministic Gauss-arrow directions and completion of missing edges; its conclusion is probabilistic connectivity, not a universal `u` estimate. |
| [Chrisman, *On the combinatorics of smoothing*, arXiv 1303.7383](https://arxiv.org/pdf/1303.7383) | §2.1, manuscript pp.3-4; oriented intersection graph follows the order of first chord endpoints from a basepoint. | The order makes this directed graph acyclic; it discards original Gauss-arrow directions. Its refined loop-counting and skew-matrix mechanism differs from cyclic triangles and fair completion. |
| [Mellor, *Intersection graphs for string links*, arXiv math/0312347](https://arxiv.org/pdf/math/0312347) | Definition 4, manuscript pp.4-5, endpoints on ordered string components; directed edges counted modulo two, reciprocal directions represented as undirected edges. | For a single knot component this becomes the usual undirected intersection graph. It is not the candidate's one-direction-per-intersection graph. Weight-system/bialgebra results do not imply this extremal bound. |
| [Even-Zohar, *The writhe of permutations and random framed knots*, arXiv 1511.09469](https://arxiv.org/pdf/1511.09469) | Introduction manuscript p.2: clockwise tournament on positions expresses a graphical inversion statistic; §2 relates it to framing. | A real knot-related tournament use, but vertices are permutation positions and the statistic is writhe/framing, not the candidate's crossing vertices and `u` cyclic-triangle bound. |
| [Even-Zohar-Hass-Linial-Nowik, *Invariants of random knots and links*, arXiv 1411.3308](https://arxiv.org/pdf/1411.3308) | §3, manuscript pp.25-26, target normalization and Gauss formulas; Theorem 3 concerns moments of `u` in a random petal model. | Random-knot moments are not worst-case bounds for all diagrams. No tournament occurrence located by text search. |

Candidate-specific steps that still need a historical originality search are the tail-to-head arc orientation of chord intersections, its identification of the two PV patterns with a directed path and cycle, and the expected cyclic-triangle count after independently filling only missing edges. No earlier knot application of this entire chain was located. This is a bounded negative search result, not evidence of absence.

## Other exact-target and near-target sources

| Source | Body / theorem pin | Scope and priority relevance |
|---|---|---|
| [Ohtsuki, *Problems on invariants of knots and 3-manifolds* (2002)](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf) | Printed p.403 normalization; printed p.405 Conjecture 2.11 (S. Willerton). | Exact target. Its status label is not a comprehensive later literature audit. |
| [Willerton, *On the first two Vassiliev invariants*, arXiv math/0104061](https://arxiv.org/pdf/math/0104061) | §1 normalization and `|u| <= c(c-1)(c-2)/4`; torus formulas and observed maxima. | Coarser universal bound; tables and torus extremizers are not a universal proof. The derivative and torus formulas match `u`. |
| [Chmutov-Duzhin-Mostovoy, *Introduction to Vassiliev Knot Invariants*, author manuscript](https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf) | §13.4.2, manuscript p.391, order-three formulas; §14.3, pp.417-418, larger cubic estimate for Jones coefficient `j3`. | Printed `|j3| <= (3/2)c(c-1)(c-2)` converts to the same coarse Willerton bound. General `O(c^3)` is insufficient. Graph bialgebras in §14.4 are a different application. |
| [Abe, thesis primary text](https://sucra.repo.nii.ac.jp/record/10402/files/GD0000751.pdf) | Proposition 3.4 exact derivative normalization; Theorem 3.10 exact target for torus knots. Corresponding published paper: *Tokyo J. Math.* 38 (2015), 331-337, DOI `10.3836/tjm/1452806043`. | Torus hypothesis is explicit, so it is not a full match. The earlier FIRST_CONCLUSION's “Abe2016” was an imprecise repository/thesis label; the 2015 paper date is the proper publication comparison. This correction does not revise the sealed independent priority finding. |
| [Zhang, arXiv 2306.01591v1](https://arxiv.org/pdf/2306.01591v1) | Remark 4.1, manuscript pp.19-20; cyclic-diagram multiplicities and PV formula comparison. | Supports formula conventions, not a universal extremal bound. A word search for bound returns a local isolated-arrow proposition, not the target. |
| Östlund (2004), cited in original SOURCES | Proposition 4 / printed p.302 described in that audit; ordinary journal endpoints failed here. | Only original-audit comparative evidence, not independently authenticated source-body evidence in this child. No priority inference rests on it. |

The separately supplied original audit flags Ohtsuki's printed p.403 Eq.(11) as incompatible with the stated normalization at the trefoil and five-crossing torus knot. No corrected coefficient, hidden range or stronger theorem was assumed from that display. That issue does not affect Conjecture 2.11 or the independently matched FS estimate.

## Independence, exposure and later comparison

The first phase read only the authorized `CANDIDATE.md` and `source_record.json`, and primary sources found independently. The source record contains unsupported upstream “partial results” boilerplate; that unavoidable exposure was disclosed before drawing a conclusion and was not treated as evidence. No sibling/ROOT priority opinions or original SOURCES had been read when `FIRST_CONCLUSION.md` was sealed at `2026-10-04T16:54:33.500435+00:00`, SHA256 `50c36c1b2b6b77aa158a1df544ab1d0eca417eb17423e8f36f1074dd1d80d5f3`.

After sealing and sending the hash, ROOT disclosed its independent inspection of the same source and independent binomial collapse. The authorized original `SOURCES.md` was then read. That audit covers PV, Ohtsuki, Willerton, CDM, Zhang, Abe and Östlund, properly withholds a novelty certificate, but omits FS's decisive estimate. This report's older-manuscript dating, even-refinement inference and expanded graph comparison belong to the **later comparative phase**; the first conclusion remains byte-for-byte untouched.

## Search / access coverage and limits

Search families included exact Ohtsuki/Willerton conjecture phrasing; `v3`, `v_3`, `V3`, `v_t3`, Jones derivatives and `j3` normalizations; crossing-number upper/maximal/extremal estimates; Fiedler/Stoimenow/Ito/Taniyama; Gauss/arrow/chord diagrams and directed intersection graphs; tournaments, cyclic triangles/triples, random completions and knot applications. Repeated sports/combinatorics false positives were filtered using source bodies rather than titles. Relevant primary sources and author repositories were preferred; general search metadata and secondary pages were used only to find primary bodies. Ito/Taniyama searches did not yield a new decisive body in this bounded audit.

Successful body access: Ohtsuki, PV, Willerton, FS updated author PDF and older author-upload text, Stoimenow 2003 publisher repository, CDM author book manuscript, Zhang, Acan, Chrisman, Mellor, Even-Zohar and random-knot collaborators. Limited access: publisher FS 2000 printing, downloadable older FS pixels, original 1940/1943 tournament papers, and Östlund journal body. Abe's thesis body was accessible through indexed primary text; a full PDF open failed. No access restrictions were circumvented.

No earliest-certificate, exhaustive search certificate, or originality certificate is issued. A suitable factual classification is **earlier-result implication verified; distinct-mechanism novelty unresolved**. The audit does not recommend changing mathematical validity or inventing a new theorem. All candidate/Git/ledger state was left untouched. No human contact, messages, outreach preparation, uploads or publication were performed.

Command provenance is in `commands/*/record.json` with actual child argv, PID, cwd, UTC start/end and exit status, plus exact `stdout.bin` / `stderr.bin`. Copyright PDFs, extracted source text and pixels are private in `/tmp/pr66_mechanism_priority_20261004_private`, outside the repository. `MANIFEST.json` bounds the authored report, log, seal and provenance inventory; it deliberately does not copy copyrighted material into this folder.
