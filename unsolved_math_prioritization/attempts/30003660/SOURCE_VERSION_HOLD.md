# Source-version hold: strong-induction admissibility

**30003660 / OWR-15958-007. Source gate only: 0/5 substantive author turns. Not exhausted; all five turns remain available after legitimate recovery of the exact target calculus.** No proof or counterexample to the target is claimed.

## Exact source rule and unresolved version

The complete Afshari–Leigh contribution *Cut elimination for modal mu-calculus* in OWR 53/2017, report pp.24–26, was read. The induction, strong-induction and quantifier-contraction displays on report p.25 were visually inspected. Primary archive: https://publications.mfo.de/bitstream/handle/mfo/3617/OWR_2017_53.pdf ; DOI https://doi.org/10.4171/OWR/2017/53 . The copied local PDF is the same hash-pinned primary input used in the related reviewed attempt. A current TIB primary indexed copy was also found at https://oa.tib.eu/renate/server/api/core/bitstreams/f754efe0-f461-4dc6-8e01-be4de222b790/content .

Writing barGamma for the negation of the disjunction of Gamma, the displayed rule is

    Gamma, nu x A(barGamma or x)
    ---------------------------
          Gamma, nu x A(x).

The report also prints contraction of like binders, from Gamma,sigma y sigma x A(y or x) to Gamma,sigma x A(x), for sigma in {mu,nu}. The inference shape is clear. The unresolved issue is the full rule set in which its cut-free admissibility is requested.

The report cites the 2017 conference article *Cut-free completeness for modal mu-calculus*, DOI 10.1109/LICS.2017.8005088, as reference [1], and the 2016 preprint as reference [2]. The 2016 text is available in full: Afshari–Leigh, *Finitary proof systems for Kozen's mu*, OWP 2016-26, https://oa.tib.eu/renate/bitstreams/50824d0c-d5f5-4a10-8518-36ade258b3e3/download . Its Section 3.1, Figures 1–3 on printed pp.8–9 explicitly defines Koz-minus by adding ordinary induction, generalized fixed-point identity **and deep disjunction** to the fixed-point core. It expressly notes that the extra deep-disjunction inference is not obviously admissible without cut.

Thus a proof in that augmented 2016 version cannot automatically be treated as a proof in the bare natural Kozen sequent calculus with cut removed. Nor may a negative result in a weaker core settle the fuller system. The full 2017 conference rule table has not been recovered and compared. No unsupported identification of versions is made.

## Corrected logical relationship to completeness

The OWR reduction from cut-free completeness to this admissibility bottleneck relied on the claimed completeness of a strengthened system. Kloibhofer's primary 2023 paper, *A note on the incompleteness of Afshari & Leigh's system Clo*, https://arxiv.org/abs/2307.06846 , introduction p.1, refutes the intervening cyclic system and expressly leaves completeness of the strengthened well-founded candidate open by that route.

Completeness of a fixed sound target calculus would still imply admissibility of the semantically valid strong-induction inference. The converse is not established by the invalidated completeness chain; this is a missing justification, not a proof that no such equivalence can hold.

The final 2025 *Demystifying mu*, DOI 10.46298/fi.12773, https://fi.episciences.org/16412/pdf , was rechecked at Section 3.2 and Proposition 3.6 on printed pp.14–15. Its strong-induction derivability result is for K_mu, whose definition includes cut. Its later corrected with-cut and illfounded completeness results do not supply the missing finite cut-free admissibility theorem for the intended 2017 version.

## Prior-attempt overlap without double counting

The related completeness target 30003659 / OWR-15958-006 already has a reviewed five-turn packet in https://github.com/AlecKriebel/Math/pull/310 . Its current PR head was verified as a08b65ce24b58941b757511be999f1ee6754d3e2. Its rule-comparison file, source gate, all five turn scopes and independent review were inspected. It already documents this version distinction and the Clo correction. Its finite certificates, restricted lower bounds and bounded search do not prove or refute the strong rule's admissibility.

Those five completeness turns are not reset, rerun or attributed to this gate. Conversely, no distinct strong-rule author turn has yet occurred. The catalog itself warns to count an equivalent completeness target only once. Any resumed rule-admissibility work must therefore have a genuinely pinned rule set and a direct proof-transformation or valid derivability/separation mechanism, rather than reopening the exhausted completeness search.

The adjacent path-choice target 30003661 / OWR-15958-008 is https://github.com/AlecKriebel/Math/pull/308 and concerns strong Weihrauch equivalence in computable analysis; it does not overlap this proof-theoretic rule problem.

## Concrete retrieval record and stopping reason

- The requested https://www.unsolvedmath.com/problems/30003660 was inaccessible through the web tool. The full pinned imported record was read at dataset revision 37e53eabe540fb458758e198be61634bd02ee008; there is no exact prior research-results entry.
- The OWR and 2016 preprint are fully available as the pinned primary PDFs, with the relevant rule images. The inability concerns the 2017 version comparison, not all mathematical source access.
- The official conference archive https://lics.siglog.org/2017/AfshariLeigh-Cutfreecompleteness.html confirms the article and its twelve-page extent, but provides no full rule text.
- The author-linked University of Gothenburg record https://gup.ub.gu.se/publication/256053 was inspected. The recovered institutional metadata identifies the DOI and twelve-page extent and lists no attached files.
- The DOI redirects to https://ieeexplore.ieee.org/document/8005088/ . The read-only DOI fetch returned an empty body; the web fetch displayed a JavaScript/robot-verification page. No CAPTCHA was solved or access control bypassed.
- DBLP's title search indicated an unpaywalled link, but its record/XML retrieval returned an anti-bot challenge instead of bibliographic XML. No challenge was solved. No unknown link from that failed record was treated as recovered primary text.
- Exact-title, author-site, institutional-domain and rule-term searches recovered the 2016 preprint, primary corrections and metadata, but no full accessible 2017 rule table. This is a bounded retrieval result, not a claim of global unavailability.

Live exact-ID PR, branch and target-path commit checks found no separate prior attempt; default-branch code search matched only assignment metadata. Available all-ref log searches found no distinct strong-induction/contraction target artifact. The current catalog is queued 0/5, eligible, with review hash c6d88f5d9b11cbbef541481516bb5a830094ad4f059d7f37edc05807d5858006. Its overlap warning is preserved above.

**Hold condition:** recover the exact 2017 rule set and verify its relationship to the explicit 2016 system, or otherwise obtain primary-source clarification selecting the intended version. Until then, retain the original target as unresolved at source scope, with zero author turns consumed. The available 2016 calculus is a definite related system, but it is not silently substituted as a resolution target. No QUEUE or PR disposition is asserted by this packet.
