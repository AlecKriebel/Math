# Primary-source literature verification and novelty-boundary search

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*  
**Referee track:** independent analytic-proof referee, post-information-barrier literature pass  
**Search cutoff:** 21 August 2026, America/Los_Angeles (the last API requests occurred after 00:00 UTC on 22 August)  
**Completed:** 21 August 2026, 22:52 PDT  
**Completion estimate:** 100% of the bounded literature-verification assignment  

No author, institution, or other person was contacted. This report uses public primary sources, publisher records, official conference/project pages, and public bibliographic APIs. Author-generated packet audits were not treated as evidence.

## Bottom line

The material prior-work statements in `manuscript/paper_content.tex:66-128` are supported by the public primary sources checked. In particular:

1. Anderson--Cappelletti--Kim (ACK) really does prove the weakly reversible, binary, one-linkage theorem only under the extra per-species pure-complex condition \(\{S_i,2S_i\}\cap\mathcal C\ne\varnothing\), and the manuscript accurately identifies how that condition enters ACK's published boundary argument.
2. Xu's May 2026 arXiv v2 proves nonexplosion for all bimolecular weakly reversible stochastic mass-action systems, defines that as part of “regularity,” and still treats bimolecular positive recurrence as open.
3. Paulevé--Craciun--Koeppl's word “recurrence” denotes reversal of reachability, not positive recurrence or finite mean return time. The manuscript uses precisely the narrower interface.
4. Public sources substantiate announcements of a positive-recurrence theorem for every weakly reversible two-species stochastic reaction network, but the five-author proof remains listed as “in preparation.” Its proof therefore could not be inspected.
5. The deterministic boundedness and permanence statements are correct for strictly positive initial conditions; they do not imply the stochastic theorem.
6. A targeted public search found no paper or preprint proving the exact overlap: arbitrary finite species, molecularity at most two, one linkage class, weak reversibility, and positive recurrence for all positive rate constants without ACK's pure-complex condition.

The last conclusion is necessarily time-bounded negative search evidence, not a proof of absolute novelty or priority. Unindexed, newly submitted, private, in-press, or otherwise nonpublic work could exist.

## Source-by-source verification

| Manuscript claim | Primary source and date | Exact interface checked | Finding |
|---|---|---|---|
| Anderson--Kim formulated the stochastic positive-recurrence conjecture and proved structural sufficient conditions (`paper_content.tex:76-78`). | [SIAM publisher record, DOI 10.1137/17M1161427](https://epubs.siam.org/doi/10.1137/17M1161427), published online 16 October 2018; [arXiv:1710.11263](https://arxiv.org/abs/1710.11263), submitted 30 October 2017. | The introduction says weak reversibility alone is believed to guarantee positive recurrence; the paper's proved results are sufficient conditions for binary networks, including weakly reversible one-linkage networks with inflows/outflows and double-full networks. | **Verified.** The manuscript does not overstate the proved 2018 scope. |
| ACK proved the binary, one-linkage case with an extra pure-complex assumption (`paper_content.tex:79-99`). | [arXiv:1904.08967](https://arxiv.org/abs/1904.08967), submitted 18 April 2019, v2 16 January 2020; [Cambridge publisher record, DOI 10.1017/jpr.2020.28](https://doi.org/10.1017/jpr.2020.28), published online 4 September 2020; [author-hosted published PDF](https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf). | ACK Theorem 4.1 assumes weak reversibility, binary complexes, one linkage class, and for every species \(S\), \(\{S,2S\}\cap\mathcal C\ne\varnothing\), then concludes positive recurrence. Theorem 6.1 is the tier criterion used in the proof. In Section 6.1 a D-top mixed complex has one absent coordinate and one divergent coordinate; the pure-complex assumption supplies \(S_v\) or \(2S_v\), D-tier maximality excludes \(2S_v\), and \(S_v\) provides the rate comparison. | **Verified exactly.** This supports both the stated prior theorem and the manuscript's claimed point of departure. |
| Product-form, strongly endotactic, one-dimensional, and path-method results are partial progress rather than the exact theorem (`paper_content.tex:101-105`). | [ACK product-form paper, DOI 10.1007/s11538-010-9517-4](https://doi.org/10.1007/s11538-010-9517-4); [strongly endotactic paper, arXiv:1808.05328](https://arxiv.org/abs/1808.05328) and [DOI 10.1016/j.spa.2020.07.012](https://doi.org/10.1016/j.spa.2020.07.012); [Wiuf--Xu arXiv:2012.07954v3](https://arxiv.org/abs/2012.07954); [2025 path-method DOI 10.1137/24M1665933](https://doi.org/10.1137/24M1665933). | The product-form theorem requires complex balance/deficiency-zero conditions. The strongly endotactic paper proves positive recurrence only for a subclass and also exhibits transient/explosive strongly endotactic networks. Wiuf--Xu assumes one-dimensional stoichiometric subspace (H2) and both reaction directions (H3); Corollary 4.10 gives positive recurrence and exponential ergodicity on each positive irreducible component. The 2025 path method gives sufficient criteria, not the exact universal one-linkage/bimolecular result. | **Verified at the scope boundary.** None subsumes the submitted theorem. |
| Xu proves nonexplosion for every bimolecular weakly reversible system and still records positive recurrence as open (`paper_content.tex:105-106,117-119`). | [arXiv:2409.05340](https://arxiv.org/abs/2409.05340), submitted 9 September 2024, v2 revised 9 May 2026; [v2 PDF](https://arxiv.org/pdf/2409.05340v2). | Xu defines a reaction system as regular when its CTMC is nonexplosive and its deterministic ODE has global solutions. Theorem 4.6(v), not (iv), states that every second-order weakly reversible mass-action system is regular. Theorem 4.13 gives an equivalence between class-wise positive recurrence and existence of a stationary distribution; it does not prove either. The concluding discussion says the bimolecular positive-recurrence conjecture remains unresolved. | **Verified.** Xu's introduction points to item “4.6(iv),” while the theorem's relevant item is actually (v); this is an internal typo in Xu, not an error propagated by the manuscript. The unusual title spelling “Regulary” is also the title on arXiv. |
| A complementary two-species theorem has been publicly announced since 2022, with a manuscript still in preparation (`paper_content.tex:106-117`). | [University of Geneva official program](https://www.unige.ch/jpe75conference/program.html), talk 10 June 2022; [Cornell public recording page](https://vod.video.cornell.edu/media/t/1_hn76x7n9/261126952), meeting metadata 22 June 2022; [SIAM AG25 official abstract book](https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf), conference 7--11 July 2025; [ConStRAINeD official results page](https://constrained.polito.it/publications/), accessed 21 August 2026. | Geneva's abstract says the weak-reversibility positive-recurrence conjecture is answered affirmatively in two dimensions. Cornell's public page identifies the 2022 conference recording and gives meeting time 22 June 2022 at 12:35:35 p.m. SIAM's 2025 abstract says weakly reversible mass-action CTMCs in two dimensions are positive recurrent. ConStRAINeD says every weakly reversible SRN with two species is positive recurrent for all rates, while item 16 lists the five-author paper as “In preparation.” | **Announcement and scope verified; proof not verified.** The public claim is broader in network structure but fixed to two species. The submitted theorem is broader in species number but restricted to one linkage class and bimolecularity. Neither public description contains the other. |
| No public manuscript for the two-species theorem was located as of 20 August 2026 (`paper_content.tex:112-113`). | Exact-title and author-combination searches on arXiv and public web indices; [ConStRAINeD publication list](https://constrained.polito.it/publications/). | Searches for the exact title *A proof of the chemical recurrence conjecture in two dimensions* and combinations of Agazzi, Anderson, Cappelletti, Laurence, and Mattingly returned talks/project pages but no paper or arXiv record. The official project page still labels it in preparation. | **Verified as a bounded negative search through 21 August 2026.** It is not proof that no nonpublic manuscript exists. |
| Deterministic weakly reversible one-linkage systems have bounded trajectories for strictly positive initial data (`paper_content.tex:66-69`). | [Anderson arXiv:1104.4992](https://arxiv.org/abs/1104.4992), submitted 26 April 2011, v2 16 June 2011; [DOI 10.1007/s10910-011-9886-4](https://doi.org/10.1007/s10910-011-9886-4). | Anderson defines boundedness for trajectories and proves in Theorem 3.12 that every trajectory starting in the strictly positive orthant is bounded for weakly reversible, single-linkage, nonautonomous mass-action systems with bounded kinetics. Constant positive mass-action rates are a special case. | **Verified.** The manuscript's formulation is slightly narrower than the source theorem and correctly retains strict positivity of initial coordinates. |
| Those deterministic systems are permanent (`paper_content.tex:68-69`). | [Boros--Hofbauer arXiv:1903.03071](https://arxiv.org/abs/1903.03071), submitted 7 March 2019, v2 13 March 2019; [DOI 10.1137/19M1248431](https://doi.org/10.1137/19M1248431). | Definition 4.1 defines permanence relative to the positive stoichiometric compatibility class. Theorem 4.2 proves that weakly reversible, single-linkage mass-action systems with bounded kinetics possess an appropriate compact forward-invariant set and are permanent. | **Verified.** This is deterministic and does not entail stochastic positive recurrence, as the manuscript explicitly warns. |
| Paulevé--Craciun--Koeppl recorded the state-return property as combinatorial “recurrence,” not Markov positive recurrence (`paper_content.tex:279-282`). | [arXiv:1302.3363](https://arxiv.org/abs/1302.3363), submitted 14 February 2013; [author-hosted published PDF](https://people.math.wisc.edu/~craciun/PAPERS_NEW/Pauleve_Craciun_Koeppl_JMB_2014_FINAL.pdf); [DOI 10.1007/s00285-013-0686-2](https://doi.org/10.1007/s00285-013-0686-2). | Definition 1.4 says a discrete reaction network is recurrent exactly when \(x\to^*x'\) implies \(x'\to^*x\). Lemma 4.5 gives a per-reaction reachability criterion, and Lemma 4.6 proves every weakly reversible network is recurrent in that sense. | **Verified exactly.** This is symmetric reachability. It contains no finite-mean-return or stationary-probability conclusion. |

## Detailed checks of the most material interfaces

### 1. ACK and the removed hypothesis

The manuscript's comparison to ACK is unusually specific, so I checked the actual proof rather than only the abstract.

- ACK Theorem 4.1 has exactly four relevant conditions: weak reversibility, binary complexes, one linkage class, and a pure unary or pure double complex for every species.
- ACK's Theorem 6.1 is a tier-sequence criterion leading to positive recurrence of the embedded chain.
- In the boundary subcase in Section 6.1, the relevant D-top complex \(S_u+S_v\) is not enabled because the \(u\)-count is zero although the \(v\)-count diverges. The special assumption guarantees \(S_v\) or \(2S_v\) occurs as a complex. If \(2S_v\) occurred it would lie strictly above the assumed D-top level, so it is excluded, leaving \(S_v\). That unary complex is then enabled and supplies the needed source-intensity comparison.

Thus `paper_content.tex:86-99` is not a generic novelty narrative; it is an accurate identification of a load-bearing use of ACK's extra condition. The new manuscript's marked-target construction is materially different at that interface. Whether that new construction is correct was addressed in the blind proof report, not inferred from this literature comparison.

### 2. Xu v2: nonexplosion is not positive recurrence

The exact separation matters. Xu's “regularity” combines:

- nonexplosion of the stochastic mass-action CTMC, and
- global existence for the deterministic reaction-rate equations.

The second-order weakly reversible result is Theorem 4.6(v) in the displayed theorem. It supplies the manuscript's external nonexplosion input. Xu's Theorem 4.13 merely states, under the bimolecular weakly reversible hypothesis, that class-wise positive recurrence is equivalent to existence of a stationary distribution on each communicating class. The later discussion explicitly presents positive recurrence as a remaining conjecture. Therefore no circularity arises from citing Xu for nonexplosion while independently proving positive recurrence.

The arXiv page gives v2 as 9 May 2026. The PDF itself carries a 12 May 2026 document date; this is not a substantive conflict. The bibliography's “revised 9 May 2026” correctly reports arXiv's version timestamp.

### 3. Paulevé--Craciun--Koeppl terminology

The 2014 paper's formal definition is graph-theoretic/dynamical reachability. The paper also discusses how nonvanishing stochastic rates preserve which transitions have positive probability, but that observation cannot promote symmetric reachability to finite expected return time. The manuscript is therefore right to state the distinction expressly. Its lifted state-return lemma proves exactly the population-state interface it needs and does not borrow a probabilistic recurrence conclusion from the citation.

### 4. Public two-dimensional claims

The 2022 Geneva program and 2025 SIAM abstract are genuine official public announcements, and the current ConStRAINeD page makes the theorem scope explicit: all weakly reversible stochastic reaction networks with two species, independent of rate constants. The Cornell URL is live; its HTML metadata names the 2022 conference and gives `Meeting Time: 2022-06-22 12:35:35pm`, corroborating the bibliography's 22 June date.

The public project description sketches a proof strategy, but it is not a proof. Item 16 still says “In preparation,” with authors Andrea Agazzi, David F. Anderson, Daniele Cappelletti, Lorenzo Laurence, and Jonathan C. Mattingly. I found no linked preprint or full paper. Accordingly:

- the fact and advertised scope of the announcement are **verified**;
- the announced proof's validity, detailed hypotheses, definitions of classes, nonexplosion handling, and exact relation to the present proof are **not verified**;
- the manuscript accurately avoids claiming that either result supersedes the other.

## Search for an overlapping arbitrary-species result

### Target signature

The searched-for overlap was a public theorem establishing, without a per-species pure-complex assumption:

- an arbitrary finite number of species;
- stochastic mass-action kinetics with arbitrary positive rate constants;
- every complex of total molecularity at most two;
- a weakly reversible complex graph with one linkage class; and
- positive recurrence (not merely nonexplosion, reachability recurrence, deterministic permanence, or existence under complex balance) on every reachable class.

### Sources and queries

I searched the arXiv API and arXiv web index, Crossref's public works API, publisher pages reached from the citation graph, exact-title searches, and public project/conference pages. Representative exact query strings were:

- `all:"positive recurrence" AND all:"reaction network"`;
- `all:"weakly reversible" AND all:"positive recurrent"`;
- `all:bimolecular AND all:"weakly reversible"`;
- `all:"single linkage class" AND all:stochastic`;
- `all:"one linkage class" AND all:stochastic`;
- `"weakly reversible" bimolecular stochastic reaction network positive recurrence single linkage`;
- exact-title and five-author variants for the announced two-dimensional paper.

Public endpoints used included [arXiv advanced search/API](https://export.arxiv.org/api/query), [Crossref REST API](https://api.crossref.org/works), the [SIAM publisher site](https://epubs.siam.org/), [Cambridge Core](https://www.cambridge.org/core/), [Springer Nature Link](https://link.springer.com/), and the official conference/project pages linked above.

### Search result

No exact overlap was located. The closest public results occupy different parts of the assumption space:

| Result | Species dimension | Network/molecularity scope | Extra condition or missing conclusion |
|---|---:|---|---|
| Anderson--Cappelletti--Kim 2020 | arbitrary | weakly reversible, binary, one linkage | Requires \(S_i\) or \(2S_i\) as a complex for every species. |
| Wiuf--Xu v3 | effectively one-dimensional stoichiometry | broader reaction orders under its hypotheses | Requires one-dimensional stoichiometric subspace and directional conditions. |
| Announced two-species theorem | two species | advertised for all weakly reversible SRNs | No public proof; fixed to two species rather than arbitrary species. |
| Xu v2 | arbitrary | every bimolecular weakly reversible system | Proves nonexplosion/global existence, not positive recurrence. |
| Complex-balanced/product-form theory | arbitrary | networks satisfying balance hypotheses | Requires complex balance/deficiency conditions absent here. |
| Strongly endotactic tier results | arbitrary | selected strongly endotactic subclasses | Do not prove all weakly reversible one-linkage binary networks; strongly endotactic alone can even be transient/explosive. |
| Anderson--Kim 2018 | arbitrary | selected binary structural classes | One-linkage result there includes inflow/outflow assumptions; double-full is a different sufficient class. |

This supports the manuscript's carefully limited novelty statement that it removes ACK's pure-complex condition while retaining the binary and one-linkage assumptions. It does **not** establish universal priority. A defensible journal-facing formulation remains “we did not locate a public result with this exact scope as of [date],” not an unqualified “first proof ever.”

## Official textbook interfaces

The manuscript cites textbooks only for standard interfaces and then gives the needed argument. I checked the official publisher metadata and accessible chapter structure.

### Norris, *Markov Chains*

- [Cambridge book page](https://www.cambridge.org/core/books/markov-chains/A3F966B10633A32C8F06F37158031739), DOI [10.1017/CBO9780511810633](https://doi.org/10.1017/CBO9780511810633), print publication 1997.
- [Official Cambridge table of contents](https://assets.cambridge.org/97805216/33963/toc/9780521633963_toc.pdf): Chapter 2 includes jump chains/holding times (§2.6) and explosion (§2.7); Chapter 3 includes class structure (§3.2), recurrence/transience (§3.4), invariant distributions (§3.5), and the ergodic theorem (§3.8).
- [Official Chapter 3 page](https://www.cambridge.org/core/books/abs/markov-chains/continuoustime-markov-chains-ii/2228CD364D132F59E73CC5718C90E1A5), pp. 108--127, chapter DOI [10.1017/CBO9780511810633.005](https://doi.org/10.1017/CBO9780511810633.005).

The official preview did not expose the exact theorem text, so I do not claim an official line-by-line verification of a theorem number. The cited interfaces—finite closed classes, jump-chain/holding-time conversion, invariant distributions, and positive recurrence—are exactly the subjects of the listed sections. More importantly, the manuscript supplies its finite trace-chain and continuous-time conversion explicitly (`paper_content.tex:942-1073`), so no hidden specialized hypothesis is delegated to Norris.

### Meyn--Tweedie, *Markov Chains and Stochastic Stability*, second edition

- [Cambridge book page](https://www.cambridge.org/core/books/markov-chains-and-stochastic-stability/E2B82BFB409CD2F7D67AFC5390C565EC), DOI [10.1017/CBO9780511626630](https://doi.org/10.1017/CBO9780511626630), print publication 2 April 2009.
- [Official Cambridge table of contents](https://assets.cambridge.org/97805217/31829/toc/9780521731829_toc.pdf) confirms the book's communication/regeneration, stability, recurrence, and drift-criterion structure.

The manuscript cites this only as background for sampled-chain Foster theory and immediately proves the stopped nonnegative-supermartingale estimate, integrability, and finite expected hitting time (`paper_content.tex:908-940`). The official preview did not provide a theorem text against which to check a particular numbered result. That exact textbook theorem is therefore **not independently verified from an official full text**, but it is also not a material unproved premise in the manuscript.

### Asmussen, *Applied Probability and Queues*, second edition

- [Springer book page](https://link.springer.com/book/10.1007/b97236), DOI [10.1007/b97236](https://doi.org/10.1007/b97236), second edition 2003.
- [Official “Regenerative Processes” chapter page](https://link.springer.com/chapter/10.1007/0-387-21525-5_6), pp. 168--185, chapter DOI [10.1007/0-387-21525-5_6](https://doi.org/10.1007/0-387-21525-5_6).

Springer's preview did not expose the theorem text. Thus the exact printed regenerative occupation theorem is **not independently checked line by line from the official source**. The manuscript nevertheless states the occupation formula, proves finiteness and normalization, identifies successive returns as regenerative by the strong Markov property, and uses only the standard stationarity conclusion (`paper_content.tex:1056-1073`). I found no mismatch in the interface.

### Anderson--Kurtz, *Stochastic Analysis of Biochemical Systems*

The citation at `paper_content.tex:52-54` is motivational rather than load-bearing. The official Springer DOI is [10.1007/978-3-319-16895-1](https://doi.org/10.1007/978-3-319-16895-1). No theorem from the book is invoked in the proof, so no theorem-interface issue arises.

## Discrepancies, limitations, and residual uncertainty

### Minor source-side quirks, not manuscript errors

1. Xu's introduction refers to Theorem 4.6(iv), but the actual “every second-order weakly reversible” statement is item (v). The manuscript avoids the erroneous item number.
2. Xu's title is spelled *On the Regulary of Reaction Systems* on arXiv; the bibliography reproduces the source rather than silently correcting it.
3. The Cornell page is not reliably machine-openable through every browser safety layer, but direct retrieval of its public HTML succeeded and exposed the title and 22 June 2022 meeting timestamp. I did not transcribe or audit the video itself.

### Not independently established

- The full five-author two-species proof, because no public manuscript was found.
- Absolute novelty or priority beyond the public record searched.
- Exact theorem wording inside paywalled portions of Norris, Meyn--Tweedie, and Asmussen. Their chapter/section interfaces were confirmed from official publisher material, and the submitted manuscript re-proves the needed steps.
- Exhaustive coverage of subscription-only indexes such as MathSciNet, zbMATH Open's complete current indexing, Web of Science, or Scopus. The negative search used arXiv, Crossref, public publisher pages, exact-title searches, citation chasing, and official project/conference records.
- Any work first made public after the cutoff or too recently to have entered the searched indexes.

## Referee implication

This literature pass found no citation mismatch that undermines the proof and no public prior result that duplicates the exact theorem. It supports the manuscript's novelty boundary as written: the paper removes ACK's per-species pure-complex condition within the binary, one-linkage setting, while neither claiming the multiple-linkage/higher-molecularity conjecture nor claiming to supersede the announced two-species theorem.

The appropriate strength of conclusion is: **public-source prior-work account verified through 21 August 2026, subject to the explicit negative-search limitations above.** This literature result does not itself validate the new proof; that conclusion rests on the independent analytic audit.
