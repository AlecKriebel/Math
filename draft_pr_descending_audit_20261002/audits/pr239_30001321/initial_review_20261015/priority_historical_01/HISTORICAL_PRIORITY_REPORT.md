# Historical and direct-lineage priority audit: 30001321 / OWR-4081-005

Audit date: 2026-10-15 UTC. Scope: primary historical sources and the direct exposure/bootstrap/local-limit lineage. This report does not certify the frozen proof or declare novelty.

## Finding and disposition

**No authenticated primary theorem inspected in this lane has been shown to imply the full frozen claim for every fixed iid law 0<p<1 in the transverse ±1 model. This is an unresolved priority assessment, not novelty clearance.**

There is substantial stronger prior context than the submitted source addendum records. Most significantly, a 2024 preprint by Bethuelsen, Birkner, Depperschmidt and Schlüter already proves the same arbitrary-diverging-width, superpolynomial-tail shape in a different directed one-dimensional dynamical environment. Its fixed-width lemma rigorously implies that conclusion; dismissing it as merely a weak CLT would be incorrect. Berger–Cohen–Rosenthal had an even earlier strong coarse estimate in a static model, and Peretz later extended that static lineage to low dimensions. These sources should be discussed before any publication that describes a new all-scale closure or the historical significance of disproving Berger's conjecture.

The direct theorem-inclusion gap is concrete: the static results require all coordinate directions to have positive uniformly bounded probabilities; the percolation result fixes a different transition mechanism that depends on an infinite future cluster. Neither hypothesis class includes arbitrary iid p_{t,x} transition vectors. Adapting a proof to a missing model is mathematical work, and is not an already established corollary merely because the mechanisms look similar.

## Exact object being compared

For each fixed probability law nu supported in (0,1), sample iid p_{t,x}~nu and run the ±1 walk. For every deterministic positive interval scale M_N→infinity, of any rate, and deterministic alignment, let L_{N,M_N} be the sum of absolute differences of quenched and annealed interval masses. The assertion is

    for every epsilon,K>0: P_env(L_{N,M_N}>epsilon)=O(N^{-K}).

The eventual N may depend on the chosen slow scale; constants may depend on the fixed law. No uniformity over laws approaching deterministic arrows is asserted. Both integer-site and real geometric interval conventions are covered by the frozen statement. This audit does not weaken the target to convergence of expectations, convergence in probability, a weak CLT, or M_N≥N^gamma.

The frozen PROOF.md, SOURCE_ADDENDUM_TURN3.md and TARGET.json were read before new priority opinions. The original SOURCE_AUDIT.md was read later for provenance context; no inherited independent-review verdict was used. A separate initial view and input hashes preserve that ordering.

## Primary source chain and authenticated locations

### Berger's original announcement

[Full official OWR report](https://ems.press/content/serial-article-files/46239), printed pp.2151–2152, PDF pp.37–38 of 64, contains Theorem 1 and Conjecture 1. The theorem covers iid, nearest-neighbor, elliptic space-time RWRE in transverse d≥2, every diverging cube scale, and superpolynomial environment tails of the coarse L1 discrepancy. The conjecture negates its extension to d=1. The next page attributes the argument to neighborhood exposure, a bootstrap, and martingale concentration; its sole reference is Bolthausen–Sznitman2002. The text does not supply a full proof.

[EMS article metadata](https://ems.press/journals/owr/articles/4081) distinguishes the workshop/report year from publication: submitted 16 August 2009, workshop 16–22 August 2009, published 30 June 2010, journal volume6(2009), pp.2115–2178, DOI10.4171/OWR/2009/38. Search-engine crawl dates in 2025/2026 are not publication dates. The PDF says elliptic, without an explicit uniform bound. No authenticated direct later statement resolving that exact d=1 conjecture was located in the scoped searches.

### The directed L2 antecedent

Bolthausen–Sznitman2002, *On the static and dynamic points of view for certain random walks in random environment*, Methods Appl. Anal.9(3),345–376, has a directed Theorem3.1, printed p363/PDF19 of32, and Remark3.2 p365. The directed assumptions admit the parity/NE encoding of the frozen model; its quantitative conclusion is a bounded second moment for a reverse mass density and an absolutely continuous invariant measure. This is genuine same-model structural coverage. It is not the coarse-L1 superpolynomial assertion. Its high-dimensional CLT discussion in Remark4.3 p371/PDF27 does not state the needed d=1 bound. The independent adversary's report documents the exact assumptions, identities, source hash and reading locators.

### Berger's static semi-local theorem

[Berger2012 full published paper](https://ems.press/content/serial-article-files/31809), *Slowdown estimates for ballistic random walk in random environment*, Proposition4.5, printed p143, assumes the static iid uniformly elliptic d≥4 ballistic setup of p136. It compares exit distributions on polynomial-size boundary cubes outside a superpolynomial exceptional event. It is an antecedent to the later fixed-time bootstrap, rather than the target theorem. Section1.8 p131 explicitly notes a low-dimensional obstruction to one of its estimates. [arXiv0811.1710](https://arxiv.org/abs/0811.1710) was first submitted 11 November 2008; the published paper records received1 March2009, revised24 February2010, JEMS14(2012),127–174, DOI10.4171/JEMS/298.

### Berger–Cohen–Rosenthal: a real all-scale precursor

[BCR final electronic reprint](https://arxiv.org/pdf/1405.6819v2), Theorem5.1, reprint p28, gives coarse L1 at most C M^{-c}+C N^{-c}, outside an N^{-xi(1)} environment event, uniformly over starting points in a box and equal-cube partitions. The model is static, iid, uniformly elliptic, d≥4, with their condition(P), equivalent there to the specified ballisticity conditions. Lemma2.14 and Lemma2.16 provide the annealed spread bounds. Their Section5 shrinks box scales by a bootstrap. Main Theorem1.11 is a prefactor L1 local limit statement, and should not be confused with the more directly relevant Theorem5.1. [arXiv metadata](https://arxiv.org/abs/1405.6819) authenticates v1 27May2014 and v2 2September2016; journal Ann.Probab.44(4)(2016),2889–2979, DOI10.1214/15-AOP1038. Both versions were retrieved.

### Peretz: a later resolution of a different low-dimensional conjecture

[Peretz2025 full preprint](https://arxiv.org/pdf/2204.12238), Theorem1.5 p4 and Proposition4.1 p11, extends the static invariant-measure/prefactor lineage to d≥2 under iid uniform ellipticity and condition(T). The latter supplies superpolynomial environment estimates for polynomial-size exit cubes; the proof of Theorem1.5 invokes the remaining BCR machinery. This disproves BCR's static dimension-two invariant-measure conjecture, not Berger's OWR transverse-one conjecture. [arXiv metadata](https://arxiv.org/abs/2204.12238) gives v1 26April2022, v2 3August2025; the PDF is dated5August2025, and EJP30(2025),1–36, DOI10.1214/25-EJP1377 is authenticated bibliographically. The publisher PDF URL returned an HTML challenge, which is retained as a failed retrieval, not misidentified as a PDF. No precise journal day is inferred from inconsistent indexing.

### Directed percolation: the closest strong predecessor found

[BBDS2023 full preprint](https://arxiv.org/pdf/2105.09030) proves a prefactor L1 local limit theorem for a directed walk on the supercritical oriented-percolation backbone in d≥3, with a strong coarse comparison Lemma2.1. [Its metadata](https://arxiv.org/abs/2105.09030) authenticates first submission19May2021; journal EJP28(2023),paper37, DOI10.1214/23-EJP924. The transition rule is uniform among neighboring future-backbone sites, and uses a simple walk off the backbone.

[BBDS2024 v1](https://arxiv.org/pdf/2410.14302v1), Lemma4.1 pp19–20, already extends that coarse estimate to d≥1: for fixed M the L1 bound is C M^{-c}+C N^{-c}, with exceptional probability at most Ctilde N^{-ctilde log N}. [v2](https://arxiv.org/pdf/2410.14302v2) has the lemma on p21 and additionally repairs/clarifies a contact-process input in AppendixB. The model is unchanged. [Metadata](https://arxiv.org/abs/2410.14302) authenticates v1 18October2024 and v2 5January2026; v2's title-page date is6January2026. Theorem2.2 is its a.s. prefactor LLT; the sharper coarse lemma is the relevant source here. Its discussion expressly leaves extension to a broader class of dynamic models as prospective.

The original deduction in IMPLICATION_AUDIT.md A proves that the fixed-M estimates in BCR and BBDS yield the full slow-scale superpolynomial statement **within their respective models**, with no uniform-M asymptotic assumption. BBDS therefore establishes that one transverse dimension does not itself obstruct that type of coarse concentration in every dynamic model. It does not establish the frozen all-iid-p conclusion.

### Recent general-flow fluctuation work screened for hidden coverage

[Drillick–Parekh arXiv2510.22155v1](https://arxiv.org/pdf/2510.22155), first25October2025, Theorem1.13 p11 under Assumption1.2, treats rescaled fluctuation fields in a negative-regularity distribution space for general iid-in-time stochastic kernels; Example1.4 concerns nearest-neighbor media. The conclusion is a fluctuation limit for fields tested at diffusive scales, not an environment-tail theorem for the unsmoothed coarse norm at arbitrary M_N. Its high-moment and replica estimates are relevant tools, but substituting shrinking indicator tests would require quantitative control absent from the stated theorem. This source was screened independently here; detailed general-local-limit coverage belongs to the parallel local-limit lane, whose report was not read.

The directed BS theorem locator was visually checked against the published page image: printed363/PDF19 is controlling. Its full publisher file ends at376, whereas Berger’s short reference lists345–375. The independent adversary preserved its locator corrections in the reading record. All cited literature statements are treated as the authors’ results; this lane verifies source hypotheses, conclusions and the displayed corollaries, without claiming a new line-by-line proof audit of every cited paper. BBDSv2 clarifies a contact-process input, so any broad supercritical-parameter assertion should cite the current version as well as recording the2024 first version.

## Exact implication and non-implication results

The separate `IMPLICATION_AUDIT.md` gives proofs, not search impressions. After preserving independent initial views and reports, the historical adversary checked its sectionA and found no hidden alignment or fixed-m uniformity gap. The adversary’s full report is in `adversary/report.md`; its BS/BMP source and retrieval records are independent of the BCR/BBDS reading above.

The checkable deductions are:

1. For arbitrary fine and target partitions, L_target≤L_fine+2 alpha(B), where B comprises fine cells split by target boundaries. Fix a large fine width first, then let the requested target width diverge. Annealed Gaussian spread makes alpha(B)→0 uniformly in alignment. This proves the genuine all-scale corollaries noted above.
2. Almost-sure prefactor approximation and spatial ergodicity do not quantify finite-time exceptional probabilities. Even exp(−c(log M)^2) spatial tails can be far larger than N^{-K} at M_N=log log N.
3. Weak CLTs and every positive polynomial coarse scale can coexist with order-one discrepancy on an arbitrarily slowly diverging scale, as demonstrated by explicit alternating-block measures. They are logical test examples, not RWRE counterexamples.
4. Copying a 1D environment into extra dimensions violates iid; making the copies independent changes the projected quenched law. The NE encoding is exact for directed results but sets two backward probabilities to zero and hence violates static uniform ellipticity. A limiting ellipticity parameter cannot be discarded without uniform estimates.

The exact rational controls in `implication_checks.py` pass **38,814 assertions**. They are reproducible finite checks of the deduction's bookkeeping and shortcut obstructions. They do not replace the analytic proofs, authenticate asymptotic source claims, or certify the submitted theorem.

## Strongest verified coverage and remaining gaps

| Approach family | Mechanism/evidence | Strongest verified coverage | Exact remaining gap to frozen claim | Status |
|---|---|---|---|---|
| Berger OWR announcement | Exposure + bootstrap + concentration, exact printed quantifiers | Target-shaped theorem for d≥2 | Transverse dimension one; announcement has no full proof | Historical anchor authenticated |
| Directed reverse-density theory | BS2002 second-moment/invariant-density argument | Same-law structural theorem after exact NE encoding | No arbitrary-M coarse L1 superpolynomial tails | Relevant prior tools; no implication |
| Static ballistic bootstrap | Berger2008/2012 → BCR2014/2016 → Peretz2022/2025 | Strong coarse comparison and all-scale consequences in covered static models | Encoded target is not all-directions elliptic; no permitted zero-backward-probability limit | Transfer route blocked as a direct corollary |
| Percolation dynamic bootstrap | BBDS2021/2023 → BBDS2024/2026, fixed-M coarse lemma | Exact slow-scale/superpolynomial shape already in a directed d=1 dynamic model | Fixed backbone rule is not arbitrary iid transition vectors | Strong near-prior; model transfer unproved |
| Early dynamic CLTs/local modulation | BMP series, independently read by adversary | Same/broader iid dynamic models for weak/smooth-test conclusions; moment estimates with restrictions | Tail order, all-law hypotheses, and slow-cell norm simultaneously | See adversary report; source gaps explicit |
| General flow fluctuations | DP2025 distribution-valued limits and replica estimates | Diffusive/moderate fluctuation fields | Shrinking unsmoothed tests and time-superpolynomial coarse norm | No exact theorem implication established |

A route is blocked here when its proposed shortcut silently replaces the missing theorem by a model-extension or quantitative estimate not contained in the source. It can be reopened by a materially new proved inclusion, an explicit adaptation, or a previously uninspected exact theorem; similarity of proof vocabulary is insufficient.

## Search limits and publication implications

The query log records exact searches, source chains and failed access attempts. Exact-title and exact-conjecture wording searches predominantly returned the original report; broader searches uncovered the strong BCR/Peretz/BBDS chain. These are observations about a bounded search, not evidence of absence. The original Berger contribution has only one cited source, so tracking its entire later mathematical influence is not the same as checking direct bibliographic citations to its workshop title.

A full 1999 BMP primary local-limit paper was not obtained by the independent adversary; repository records and a later author survey provide a lead but do not substitute for the missing full theorem. Other unindexed manuscripts, theses, non-English sources, or unpublished prior proofs remain possible. No person was contacted, and no outreach draft was prepared. Outside archival expertise could help with inaccessible early primary sources; only the human may pursue external communication.

For a concrete reviewable update, the source/credit discussion should identify BCR Theorem5.1, Peretz's low-dimensional extension, and especially BBDS Lemma4.1 in its 2024 first version, distinguish their models, and state the exact unresolved priority gap. The assertion that this is the first arbitrary-scale closure in one dynamic transverse dimension is not supported. Nor does this audit justify claiming that Berger's exact conjecture was previously resolved. A paper-level or novelty declaration remains outside this lane's clearance.
