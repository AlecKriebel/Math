# PR18 / 30001075: primary-source, dependency, and scope audit

Verdict: **PASS for this mathematical/source-scope gate; priority remains unconfirmed.** No theorem-level correction is required by this family. The exact target, actual-contact tangency definition, and arbitrary convex-set extension survive the independent checks. This verdict is not a substitute for the separate cap-cover and rank-family audits.

Frozen input: head `99e403e85d38d92b021198c4a57bbad3cd8775ba`. The candidate bytes inspected have SHA256 `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`. The independent first seal preceded all literature/history comparison and is identified in `first_seal.json`. No pre-existing review artifact or historical test code was read or adopted. The supplied research history was read only after sealing; its recorded historical verdicts did not alter this audit.

## Exact original question and primary context

[EMS Report 44/2008](https://ems.press/content/serial-article-files/46191), §13, printed p.2552 / PDF page 76, gives Conjecture 4 for the entire union of lines that intersect all three pairwise disjoint convex sets and lie in a supporting plane for each. Conjecture 3 is its separate 2-manifold-cover question. The report explicitly distinguishes its known topological conclusion from the measure target. The broad conjecture has no printed smoothness, genericity, boundedness, or closedness assumption. The candidate matches this scope and does not claim Conjecture 3.

The [EMS metadata](https://ems.press/journals/owr/articles/2090) distinguishes the September 2008 workshop/submission from publication on 30 September 2009. The dataset's 2008 proposed year is compatible with its 2009 bibliographic label.

The fresh [HAL thesis v1](https://theses.hal.science/tel-00342717v1/file/these.pdf) identifies a defense on 24 November 2008 and deposit on 28 November 2008. Its terminology and relevant theorem/lemma locators match the candidate. The older argument's closed-object context must not be silently expanded to the candidate's nonclosed setting.

## Newly obtained underlying manuscript

A [full author-uploaded public manuscript PDF](https://www.researchgate.net/profile/Julien-Demouth/publication/228861895_Topological_changes_in_the_apparent_contour_of_convex_sets/links/552fb7f30cf27acb0de6451d/Topological-changes-in-the-apparent-contour-of-convex-sets.pdf) was inspected through the web reader, including its appendices. The [hosting record](https://www.researchgate.net/publication/228861895_Topological_changes_in_the_apparent_contour_of_convex_sets) attributes the upload to Demouth on 16 April 2015. Precise theorem/scope/page facts appear in `source_ledger.json` and the first seal. It supports a positive historical lead on the exact question, not a later solution. It is an undated manuscript version that cites the November 2008 thesis; no identity to the September 2008 cited version is claimed. Direct local PDF requests returned HTTP 403, so no acquired-byte hash exists for this item.

The frozen literature file honestly said that its author had not independently obtained the manuscript. That historical claim should be retained as dated history. A new literature entry can now distinguish this newly inspected author-uploaded version, without rewriting the older history as if it had been read then.

## Universal mathematical checks

The checkable mathematical artifact is `DEPENDENCY_AND_SCOPE_CHECKS.md`. It contains deductions for all of the following, with hypotheses and boundary cases explicit:

| Dependency or scope point | Independent result | Exact limit |
|---|---|---|
| Fixed-normal support increment | Sign and min/max bounds proved for arbitrary compact convex sets and arbitrary increments | No derivative of support or normal field used |
| Projection/support-gap characterization | Exact meeting-plus-support-plane tangency when projection has R² interior | Planar nontransverse lines are removed first; dimensions 0/1 handled separately |
| Arbitrary-to-compact reduction | Contact-preserving containment in a countable union of disjoint compact-cap problems | Does not claim reverse containment or disjoint original closures |
| Local cap support normals / affine dimension | Segment argument preserves both at interior-of-ball contacts | Compact-cap hypotheses, not arbitrary open projections |
| Monotone implicit roots / contraction | Lipschitz constants and invariant-square choice reconstructed | Central cover proof still separately scrutinized; no smooth implicit theorem imported |
| Countable cover | Fixed-cap-pair, second-countable subcover argument checked | A cover by changing caps alone would be insufficient; candidate avoids it |
| Parameter measurability | Compact tangency is closed in line space; exclusions give Borel E | Original nonclosed-locus closedness is never needed |
| Density sampling | Density one supplies arbitrary prescribed first-order directions by a missing-ball contradiction | E need not contain any curve or open set |
| Rank / three contacts | Interior-ball, relative-disk, segment, and point mechanisms checked; contact heights are distinct | No unique contact/normal or genericity assumed |
| Swept Jacobian / area formula | Sweep is Lipschitz on bounded patches; multiplicity bounds image measure; bad parameters have null products | No injectivity, smooth Sard, or C¹ parameter set required |
| Remaining dimensional covers | Point directions and segment endpoint pairs supply Lipschitz 2-parameter covers | Constant or noninjective parameterizations are allowed |

For the imported analysis, a fresh primary author text was inspected: [Leon Simon, *Introduction to Geometric Measure Theory*, 2018 NTU notes](https://math.stanford.edu/~lms/ntu-gmt-text.pdf), Chapter 1 Corollary 3.10 (density), Chapter 2 Theorem 1.4 (Rademacher), and Chapter 2 Theorem 3.3 (area formula), at printed pp.18,45,57–58. The area formula explicitly permits a locally Lipschitz map on an open subset and each Lebesgue-measurable selected subset. Its equal-dimensional use here needs no global extension or injectivity. Scalar Rademacher applies componentwise, with open-domain localization or scalar Lipschitz extension.

The exact cited Federer §3.2.3 text and the Evans–Gariepy revised-edition theorem bodies were not accessed from their publishers. [Springer's rectifiability chapter](https://link.springer.com/chapter/10.1007/978-3-642-62010-2_4) provides subscription metadata/preview only; the CRC/Routledge page was inaccessible to the web reader. Their exact historical/theorem-number attribution is therefore not presented as newly source-verified. The needed full hypotheses have independently been checked in Simon's first-party text and in the derivations above. Adding this accessible primary reference would improve reproducibility.

## Own falsification artifact and source correction

Take Kᵢ={(i,y,0):0<y<1}, i=0,1,2. The horizontal lines y=1/n,z=0 are common tangents, so pₙ=(0,1/n,0) lies in their union, but p=(0,0,0) does not: a line through p meeting K₀ must be the line x=0,z=0 and misses K₁. This establishes that the common-tangent union need not be closed for arbitrary nonclosed convex sets. The full proof is in the mathematical artifact. Every line in this example lies in z=0, so it is a falsification of the broad background extrapolation, not of the candidate's nullness conclusion.

Required theorem repairs: **none found** in this family.

Source-documentation corrections before promoting the result: explicitly qualify the older closedness/nowhere-density background by its inspected compact/closed context; record the freshly retrieved thesis as a distinct byte artifact; identify the newly inspected manuscript by upload and exact URL without assigning an unverified manuscript year. These are mandatory if making any claim that the broad historical background or exact manuscript/version was independently verified. The candidate's existing literal statement that the report records that background is correct as a statement about what is printed, but a context clarification prevents a false mathematical reading.

Optional improvements: add the accessible Simon locators and an explicit one-line image-measure inequality from the multiplicity area formula; delete the stray `ν:=u` notation in (3) if desired. None changes the mathematical mechanism.

## Post-seal source/hash comparison

The fresh EMS PDF is 731001 bytes, SHA256 `3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35`, exactly the frozen author checksum. The fresh thesis PDF is 2842412 bytes, SHA256 `85fb6e472777d2a6efc8fe6892472a5a377132ee1f4429d2ec1ff585e2dab021`; the frozen thesis record is 2842420 bytes, SHA256 `4b0fd4835fa278c3b1f1597fb0d2ead0a4bd24d2b88bf1ff7af444a5dbfa82da`. Fresh reading verifies the current v1 content, not byte identity with the author's earlier copy. The difference is not explained or declared harmless merely because it is eight bytes. Both identities should remain recorded.

## Bounded current positive-prior leads

The source ledger records author/institution publication pages, the first-party HAL title and author-pair searches, the 2009 shadow paper, and a recent related transversal publication. The [Gamble Demouth page](https://gamble.loria.fr/publications/publications_Julien_Demouth.html) reports modification on 19 August 2026; Goaoc's complete PDF list labels itself January 2025 even though it includes a 2025 conference entry. Neither should be treated as an exhaustive current corpus. The 2009 paper's complete first-party HAL version was read and is about polyhedral shadow-boundary computation, citing the topological manuscript as a 2009 manuscript. It gives no arbitrary-convex nullness theorem. The exact-title HAL manuscript search returned zero records in that query; the Demouth–Goaoc pair query returned four records including the shadow paper. These finite queries do not prove nonexistence.

HAL record `hal-04293155v1` identifies *Some New Results on Geometric Transversals*, DOI `10.1007/s00454-023-00573-2`. Its metadata/abstract and associated [arXiv v3](https://arxiv.org/abs/2202.02719v3), revised 5 September 2024, provide positive related leads on line-transversal topology and weak epsilon nets. This family did not inspect the combined 30-page final theorem body and therefore does not certify it as an excluded antecedent. It is a handoff lead for the broader priority families after the mathematical gates. Smooth-generic, polyhedral, sphere, or semialgebraic special cases cannot alone resolve the arbitrary-convex statement.

Strongest verified result: the frozen candidate addresses the precise original measure-zero target, with the original support-tangency convention, without an uncovered imported analytical hypothesis or dimensional extension found here. The source's topological theorem is not being substituted for that target.

Remaining gap: separate central-lemma proof consensus and broader historical/current priority checking. The ledger provides evidence of a question in one accessible historical manuscript version; it is not an absence certificate and does not establish current openness or novelty. No external individual was contacted. No Git, branch, canonical/shared research state, or publication action was performed by this family.
