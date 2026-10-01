# PR20 exact original target and primary-source adversarial audit

**Mathematical verdict: PASS, already solved negatively in the literature, for every j >= 0.** The historical attribution to Goresky and Pardon (1989) survives independent examination of the original question, definitions, theorem and relevant proof. **Publication-record verdict: repair the book-version wording and add the scope/evidence clarifications below.** No new substantive mathematical attempt was added.

Audit target: problem 30001947 / OWR-11454-005; frozen PR head `7914dfa8c2ddf0efb784a29accc8a05b5a24a690`. The original-scope seal was written at 2026-10-01 18:12:47 UTC, and the mathematical/source-evidence seal at 18:18:52 UTC. The original dated review was read only after both seals. No sibling or root substantive conclusion was used. The initial snapshot manifest contained its queue assertion; it was treated as metadata and excluded from the evidence.

## Exact original question and curation

The full official [OWR report](https://ems.press/content/serial-article-files/46371), printed pp. 3279-3280 / PDF pages 63-64, defines the sought objects as compact integrally oriented PL stratified F2-Witt pseudomanifolds. It asks whether their middle intersection-homology pairing in dimension 4j+2 realizes the nonzero class of W(F2). It explicitly distinguishes merely F2-oriented examples: even-dimensional real projective spaces supply the nonzero class there. The question is about symmetric bilinear Witt classes, not a quadratic refinement or Arf invariant. Its isolated-singularity discussion is a restricted obstruction, not the whole question.

The frozen `source_record.json` original/clean statements preserve this scope literally through typography and ordering changes. “F2-Witt space” inherits the PL pseudomanifold definition. No boundary and no codimension-one strata are the conventional absolute-duality category, confirmed by the contemporary sources' definitions; they are not new restrictions imposed by this audit. The printed question does not specify j's range, but nonnegative dimension gives j >= 0. Dimension two must be included. The report's “open” assessment is historical evidence, not current-status evidence. EMS identifies volume 8 (2011), no. 4, pp. 3217-3286, published 25 July 2012, DOI 10.4171/OWR/2011/56.

The earlier author-hosted OWR source uses local pp. 63-64 and has a different byte hash from the official journal PDF. Both contain the same Q2. All four frozen downloaded-source hashes were independently reproduced; this difference is a version distinction, not a failed checksum.

## Direct prior theorem and scope bridge

The original [Goresky-Pardon journal facsimile](https://www.math.ias.edu/~goresky/pdf/Wu.jour.pdf) is *Topology*28(3) (1989),325-367, DOI 10.1016/0040-9383(89)90012-8. Its §2.1 uses PL pseudomanifolds and regular-stratum orientability. Section 8.3 implies local orientability. Section 10.1 has the matching lower-middle mod-two link condition. The odd operation in §10.2 is an intersection-homology operation; §4.3 identifies its middle value with self-intersection. Section 10.5 Theorem A and §10.7 Part A give the requested 4j+2 vanishing. The lemma's integral-chain calculation on printed 339-340 proves the needed first Wu relation; this is not an appeal to conjectured general Wu relations or to an ordinary-cohomology formula. Relevant pages were rendered and visually checked.

There is a hidden working assumption worth recording: §2.4 first assumes normal connected pseudomanifolds. It calls this nonessential via normalization. The following independent scope bridge avoids treating that sentence as unexplained permission to change the source target.

Let pi: Xtilde -> X be normalization. Friedman's preliminary book, Proposition 5.1.11, pp. 192-193, proves that pi induces an intersection-homology isomorphism for perversities p(S) <= codim(S)-2. Lower middle perversity satisfies that inequality. Normalized links have the same lower-middle groups, so the F2-Witt condition persists; integral orientation pulls back because pi is a homeomorphism on regular strata. Compactness persists under proper normalization. Treat each normal connected component separately; their middle groups form a direct sum. Thus each component has an alternating nonsingular middle form and even middle dimension, and X has even middle dimension. The actual W(F2) invariant is dimension modulo two, as explicitly explained in the characteristic-two paper's footnote 8. This already proves Witt-zero for the entire original category.

The stronger alternating-form statement also survives normalization. For r=n/2 and a singular stratum of codimension c, two allowable middle cycles in stratified general position have intersection dimension at most

`2(r-c+m(c))-(n-c) = 2m(c)-c <= -2`.

Their intersection points therefore lie in the regular stratum, where normalization is a homeomorphism. The pairing agrees with the normalized pairing. A nonsingular alternating bilinear form is Witt-zero: choose nonzero e, choose f with b(e,f)=1, split off their nonsingular hyperbolic plane, and repeat on its orthogonal complement. This check includes the zero group. For j=0, Friedman's seven-page correction also independently treats surfaces with point identifications and proves the vanishing.

GP's displayed Theorem A does not separately distinguish degree zero in its divisible-by-four clause; the modern signed-oriented degree-zero group is Z. Do not blindly transplant its entire displayed table. Q2 has dimension at least two, and the direct square proof and modern table agree in every requested degree.

## Positive attribution and version chronology

The [2012 corrigendum](https://faculty.tcu.edu/gfriedman/papers/2-Witt2.pdf) and [2012/2013 detailed paper](https://faculty.tcu.edu/gfriedman/papers/2-Witt3.pdf) do leave the oriented 4k+2 alternative unresolved. Their respective journal DOIs are10.1002/cpa.21421 and10.1007/s00013-013-0503-6. They are older accounts of an overlooked result, not present-day contradiction certificates.

The acknowledgement is already present in [arXiv 1311.2633v1](https://arxiv.org/pdf/1311.2633v1), dated 11 November 2013, §5.2.1, footnote 11 on p27, with GP cited as [18]. The [author PDF dated 11 May 2015](https://faculty.tcu.edu/gfriedman/papers/stratwitt.pdf) and [v4 uploaded 4 August 2015](https://arxiv.org/pdf/1311.2633v4) contain footnote 14 on p28, GP [19]. The complete footnotes and surrounding definitions were inspected. The author explicitly identifies his unresolved oriented case with the prior GP result. The 2015 journal metadata is *Topology and Its Applications*194,51-92, DOI 10.1016/j.topol.2015.07.014. The precise claim is prior resolution by 1989 with acknowledgement present by November 2013; this audit does not certify global priority.

The linked [book PDF](https://faculty.tcu.edu/gfriedman/ihbook.pdf) is dated 24 July 2019. Its own printed page 676 is PDF page 696 and gives Z in degree 0, Z/2 in positive multiples of 4, and zero otherwise, attributed to GP §10.5. The canonical uppercase URL serves the identical bytes. The author's homepage expressly labels it preliminary manuscript format. Cambridge confirms the separate 2020 publication and Chapter 9 on pp. 613-702, DOI 10.1017/9781316584446.010; its gated chapter does not verify the theorem at final-edition printed 676. Reference numbering and pagination differ between manuscript and publisher metadata. No final-edition page locator is inferred.

## Repairs and limits

1. **Required evidence precision:** replace “the 2020 book p676” in the research log/queue or other propagated claims with “the 24 July 2019 preliminary manuscript, printed p676 / PDF p696.” A 2020 final-edition locator requires independent access and checking. The negative answer does not depend on that extra access.
2. **Required scope completeness in a promoted direct-theorem account:** explicitly mention GP's normal connected working assumption and its harmless normalization/direct-sum extension. The old review mentions normalization, but the candidate's direct hypothesis audit should carry the actual bridge or cite this checkable audit.
3. **Required provenance precision for promotion:** retain the version/page/hash ledger, including the book manuscript hash omitted from the old four-source checksum list. Any revised note requires a fresh note hash and a review for its actual bytes; the old review certifies the frozen old bytes only. The 2013/v1 locator is a useful chronology clarification, not a new theorem.

The frozen note digest agrees with readiness and both review records. The frozen review digest agrees with the review summary. The separate readiness `review_hash` field has no documented meaning within the ten-file snapshot and differs from those artifact digests; it must not be represented as the source-review artifact hash without identifying its preimage. The explicit `reviewed_sha256` and `review_sha256` links do verify.

The original budget records one substantive investigation out of five, with final recorded packaging at 04:35 UTC before its 06:13 UTC cap. This audit adds zero attempts. Those are internally consistent frozen records; signed reviewer execution transcripts and independent budget telemetry were not supplied, so this is not a certification of unseen execution.

The bounded current literature/correction search found no primary counterexample or correction to this exact claim. The 2019 primary maps paper repeats the GP relation but has a different open conjecture on bordism of maps. This search is not a global absence certificate. The strongest verified result is the exact negative answer and its prior attribution; the remaining gap is evidence-record precision, not an open mathematical case. All foreign full texts stay in ignored `tmp/primary_sources`; no Git, PR mutation, publishing, or external communication was performed.

See `SCOPE_SEAL.md`, `SOURCE_LEDGER.json`, `PROVENANCE_CHECKS.json`, `BOUNDED_SEARCH.json`, and `MANIFEST.json` for checkable receipts.
