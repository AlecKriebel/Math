# Full adversarial priority audit: PR1037 / problem30003822

Audit date: 13 October 2026 (UTC). Original submitted head: e87236a97c4b87818d2768cd5789043c7c3f4e39. This audit writes only inside reviews/priority_01. It accepts the pinned root mathematical disposition as its mathematical input and independently investigates sources. It is an AI source/proof comparison, not human peer review or formal verification.

The full all-n mathematical claim is eligible as an accurately credited theorem/proof exposition. A first-solution or new-method claim is not certified. A public exact-target proof is now located: Ferudun, Theorem1.2. Crucially, GitHub records PR1037 on9Oct2026, while that preprint's DOI was registered11Oct2026. The latter must not be described without qualification as preceding the submitted proof. The source overlap must nevertheless be disclosed in any future paper. No current-open claim is defensible, and source updates are required before promoting a paper.

## 1. Frozen input and independent order

INPUT_PIN.json immediately hashes all ten original submitted files, SUBMITTED_PINS.json, ROOT_MATH_ACCEPTANCE.json, ROOT_INITIAL_DERIVATION.md, the source fetch and PR capture. The original submitted proof is25,072bytes, SHA256546d9df387da3266b1b20d31b1cd6017a65fe9f497f1b37d2a99319e6194755c.

INDEPENDENT_COMPARISON_BEFORE_HISTORY.md was written before this reviewer read submitted ATTRIBUTION.md, SOURCE_CATALOGUE.json, PROVENANCE.md or their historical conclusions. It records fresh primary comparison. Its initial use of “prior proof” means prior to this13Oct review; it did not establish precedence over the9Oct PR. CHRONOLOGY_CORRECTION.md records the later recovered dates and supersedes any stronger chronological interpretation. This distinction is substantive, not an editorial detail.

The root disposition accepts the integral all-n divisor after two distinct fresh mathematical families and its own full reading. This reviewer does not promote extra multiplicity/factorization claims or certify omitted historical computations.

## 2. Exact target and convention crosswalk

Let A=(a_ij) be the generic n by n matrix over Z[a_ij], n>=1. Let T have one row and column for every set partition, hence size B_n. Fix one unweighted internal tree on each input block. An interlayer edge subset contributes its monomial once exactly when adding it yields a forest, every component meets the output layer, and the induced output partition is the designated column. The target is

    (det A)^C_n | det T in Z[a_ij],  C_n=binom(2n,n)/(n+1).

The exact original definition and question occur on printed1457-1458/PDF77-78 of [Teufl-Wagner, OWR23/2018](https://ems.press/content/serial-article-files/46745). The neighboring pure-braid problem is unrelated. Observations through n=6 do not establish all n, and a smaller noncrossing matrix would prove a different assertion.

The following comparison guards against false exclusions:

| Convention | Required comparison |
|---|---|
| Rows as input versus column vectors | Transposing T changes no determinant. The correspondence must still count the same edge subsets. |
| Paired variable order | Source f_ij uses barred then unbarred variables. The submitted q uses the opposite order with matched top-coefficient convention. A species sign change and reordering identify these conventions without changing positive forest coefficients. |
| Fixed trees versus all tree counts | Summing over every internal tree introduces block factors. The original and exact-match preprint both fix arbitrary trees and count only interlayer subsets once. |
| Contraction | Contracting each fixed input tree preserves admissibility. Distinct original endpoints remain separate edge choices; their weights sum to b_B(j)=sum_(i in B)a_ij. Losing those parallel choices changes T. |
| Rooted forests | A rooted Laplacian minor counts a prescribed-root object. It is not automatically the full partition-to-partition transfer. |
| Laplacian symmetry | Generic nonsymmetric A still gives a symmetric2n-vertex bipartite Laplacian. Symmetry of an electrical Laplacian alone cannot exclude an implication for arbitrary A. |
| Positivity and denominators | A polynomial identity established on an open positive region can extend after clearing denominators. Positivity alone is not an exclusion argument. Singular/zero-row-sum specializations must ultimately follow from a polynomial identity. |
| Planar basis | A noncrossing basis of the quotient of the full Bell space is compatible with a nonplanar transfer. Restricting the original state space itself is a different theorem. |
| Exactness | A divisor permits higher powers. No assertion about exact multiplicity or an irreducible cofactor is part of this audit. |

## 3. Located exact-target proof and chronology

[Alper Ferudun's public preprint](https://eulersolve.org/papers/owr-16164-020/), version1.0, states the same full-Bell generic theorem in Theorem1.2(a)-(c), PDF3. Its definition in§1.1 agrees entry by entry with the original normalization. Core§§2-5, PDF5-12, supplies forest intertwining, a constant Catalan image, an inverse Gaussian operator identity, and an integral block factorization. The independent second proof in§6, PDF12-15, uses the tree pairing and a bordered matrix-tree determinant. I found no gap affecting the divisor in those core arguments. The additional computer-assisted exactness claims are outside this validation.

The downloaded21-page PDF is238,635bytes with SHA256bfa3aec9938a2a28aebac8e905abff2e132080e753f845e746485f66d16be677. Its advertised metadata hash agrees. This is an exact mathematical match, not an abstract-only resemblance, finite computation or planar specialization.

[DataCite's DOI record](https://api.datacite.org/dois/10.5281/zenodo.23298482) independently records created/registered/updated at2026-10-11T13:01:38Z, issued11October, version1.0, statefindable. Direct Zenodo retrieval failed; the author-hosted PDF was actually read. [GitHub PR1037](https://github.com/AlecKriebel/Math/pull/1037) was created2026-10-09T22:16:52Z and lists the original head committed22:16:22Z. The repository is public when checked13October. Historical visibility at9October was not independently archived, and commit author dates alone are not immutable discovery timestamps.

Consequently, no argument here assigns the later preprint intellectual priority, establishes independent discovery, proves copying, or awards worldwide first priority to either work. The earliest repository timestamp located belongs to PR1037; the exact source match is currently public and must be compared/cited. Its presence falsifies a current no-match assertion, not the historical9October bounded search.

## 4. Established ingredients and the remaining application

The following are prior mathematical structure, irrespective of the contemporary exact match:

- [CSS arXiv0706.1509v2](https://arxiv.org/pdf/0706.1509v2), posted16October2007: equation4.3c; Corollaries4.3-4.5, pp15-17; Lemma5.1/Corollary5.2, pp18-19. These prove normalized forest multiplication, cycle vanishing, exponential subset expansion and partial elimination. Page17 announces a noncrossing basis/Catalan dimension and defers the proof to reference39, listed in preparation on49. That announcement cannot be called a completed proof in the2007 paper. Its introduction/equation1.8 already describes the lambda0 Gaussian determinant setting.
- [Sportiello's thesis](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf), Chapter10: printed195/PDF203 explicitly addresses nonplanar transfer; formulas10.3-10.5 normalize f before lambda0; Theorem10.3 printed207/PDF215 and Lemmas10.4-10.7 printed208-213/PDF216-221 prove the basis. The selected monomials have lambda-independent unit coefficients. The stated ordering direction and proof direction require reversal, which preserves the triangular unit minor. The [official SNS item](https://ricerca.sns.it/handle/11384/85875), now freshly retrieved with system curl, gives citation_date2010; cover academic years2000-2003 are not a publication date.
- [Kenyon-Wilson arXivmath/0608422v4](https://arxiv.org/pdf/math/0608422v4), revised19January2009, journal2011:§1.2, Theorem1.2;§§2.1-2.3, Theorem2.6, PDF13-18. These give the partition projection, tree pairing and integral planar reduction also for arbitrary partitions/graphs. Identifying this pairing radical with the forest-state kernel recovers the same quotient structure. The cited meander nonsingularity is a prior result of DiFrancesco-Golinelli-Guitter, not a new invariant subspace here.
- The [official ICTP seminar13January2009](https://indico.ictp.it/event/a092/) corroborates announcement of noncrossing Grassmann/Clifford bases. It is not proof. The2010slides remain a corroborating historical record; fresh direct fetch403 and detailed web navigation failed, so this audit does not manufacture a fresh full-body reading of them.

The quotient and paired forest mechanism are therefore established work. The elementary deduction from them still needs a transfer determinant calculation; Catalan dimension alone is insufficient. In a constant forest-state image W, the positive coefficient-extraction normalization gives the exact transfer. An identity of the form

    G(-A^T)G(A)=(-1)^n(det A)^2 I

would imply, for p(A)=det(G(A)|W), that p(-A^T)p(A)=(-1)^(n dimW)(det A)^(2dimW). Factoriality, irreducibility of det A and unipotent normalization at I then force p(A)=(det A)^dimW. The constant invariant kernel lifts the factor to full T, and primitivity descends it to Z[a_ij]. This is a checkable bridge, and the contemporary exact-match source supplies it explicitly.

The submitted ordered Gaussian-completion argument is another explicit way to calculate that determinant, using degree-triangular raising/lowering factors and the determinant character of substitution. It should be presented as an application/calculation within the established forest algebra. I did not locate this full interlayer determinant bridge explicitly in the older inspected sources. That bounded finding does not certify historical novelty: standard Gaussian algebra can make the application short and specialists may already know the corollary. Calling a basis argument self-contained does not make the basis new; calling the final assembly different does not create a new method.

## 5. Closing old unread leads and related bodies

| Primary source | Body inspection and exact gap |
|---|---|
| [Teufl-Wagner, Determinant identities for Laplace matrices](https://math.sun.ac.za/swagner/determinant.pdf), preprint15Apr2009; LAA432(2010)441-457 | Author PDF23pages fetched. Theorems1/2, pp4-10, and Theorem10 with proof, pp14-15, fully checked. Main theorem expresses Laplacian minors using two-deletion minors; replacement theorem changes scalar spanning-tree counts by a local electrical-equivalence ratio. Full applications surveyed. No full-Bell transfer determinant result located. This closes the former unread-body lead for this preprint, not every possible later journal modification. |
| [Teufl-Wagner FPSAC2009 paper](https://dmtcs.episciences.org/2699/pdf) | Full12-page body fetched/read at its critical proof sections and applications. Printed847-858. Conjecture3 is a rooted-minor identity;§2 proves its three-boundary case, and§4 uses replacement in self-similar examples. The later Laplace preprint proves the more general minor identity. It is not the2018 full-Bell determinant problem. |
| [On the number of spanning trees on various lattices](https://math.sun.ac.za/swagner/lattices.pdf),2010 | Full9-page text inspected. Theorems1-4 concern replacement, bounds and scalar tree-entropy relations. Their state/normalization does not supply the required endomorphism determinant. “Catalan constant” occurrences concern a different quantity. |
| [The number of spanning trees in self-similar graphs](https://math.sun.ac.za/swagner/spanning.pdf), journal2011 | Partition conventions, quotient recurrences and Theorems21/26/29 contexts inspected. It aggregates under partition-homogeneity/symmetry and studies nonlinear scalar recurrences. No exact target found in inspected portions; no claim that the complete author corpus was exhausted. |
| [Resistance scaling and the number of spanning trees in self-similar lattices](https://math.sun.ac.za/swagner/ssl.pdf),2011 | Replacement Theorem1 and asymptotic Theorem2 with proof context inspected. A positive conductance renormalization sequence is different input from the generic Bell transfer. Partial-body scope, not global exclusion. |
| [Li-Yan DOI10.1002/jgt.23220](https://onlinelibrary.wiley.com/doi/10.1002/jgt.23220), first6Jan2025 | Publisher abstract/bibliography read; full/pdf/epdf403. It advertises an electrical-equivalence ratio involving spanning trees containing a prescribed forest and contraction. FULL-BODY SCOPE UNKNOWN. No exclusion of an implicit target corollary or stronger result is justified from this abstract. |
| [Kogan arXiv2610.07539v1](https://arxiv.org/pdf/2610.07539v1),6Oct2026 | Entire17-page body read. Theorem1.1/4.7 and Corollary4.8 concern normalized Pfaffian tensors, double groves and a Sp(4) basis. Lemma2.6 and Remark1 admit nonplanar coloring tensors, so dismissing this solely for planarity would be wrong. No full-Bell interlayer transfer determinant is in the body. Its displayed normalization Z_unc^-n and symplectic tensor expansion do not supply the missing operator determinant. |
| [CSS2017 paper's31Jul2016 preprint](https://discovery.ucl.ac.uk/10025167/1/forests_ON_v3gA.pdf) | Primary full62-page file obtained,599,288bytes. Introduction, main one-link/general reduction statements and proof portions, forest/series-parallel sections and references inspected. Scope is analytic continuation of OSP sigma models. No exact target found in these passages; complete absence in all versions is not certified. |
| [Rapoport2025 forward-citation lead](https://pmc.ncbi.nlm.nih.gov/articles/PMC12535553/) | Introductory primary text initially rendered, then detailed navigation/direct retrieval returned CAPTCHA. Its full critical body is UNKNOWN and not used to exclude overlap. |

The author's primary publication list was read and supplied the linked lattice/self-similar works. CSS exact-title/reference39 searches, the2017 update, KW and a2025forward-citation lead were followed. This is a bounded citation-chain pass, not a complete forward-citation census.

## 6. Corrections to the frozen historical records

The9October ATTRIBUTION.md properly credits the forest algebra and thesis and already declines novelty/current-open certification. Its historical no-match statement is not now a valid description of all currently available evidence. Keep that document's date and byte identity if preserving the edition; attach a dated source/priority addendum to every current review or paper derived from it.

The new addendum must record the exact-target Ferudun source, the qualified9/11October chronology, the newly read Laplace/FPSAC bodies, the freshly accessible SNS item, the stronger Kogan full-body comparison, and the remaining Li-Yan gap. Do not silently update a historical “checked9October” claim as though the11October source had then been reviewed.

The source catalogue's former unread Laplace-body label can be closed for the downloaded preprint in the addendum. The Li-Yan abstract-only label remains a real scope gap. The statement that CSS39 was in preparation in2007 is historical; this audit still does not certify its current standalone publication status.

## 7. Mandatory paper/title/metadata credit requirements

These apply globally, beyond one related-work paragraph:

1. Use a neutral title such as “A Grassmann proof of the Catalan divisor in the Teufl-Wagner forest transfer determinant.” Avoid first, novel, new method, definitive resolution of a currently open problem, or a title promising exact multiplicity/factorization.
2. State the precise all-n integral divisor and full-Bell normalization in the abstract. Say the proof applies established forest algebra and computes its quotient determinant. Explicitly mention the exact-target contemporary proof and the qualified chronology; do not frame it as a mere nearby grove paper.
3. At theorem introduction, cite Teufl-Wagner2018 for the question and Ferudun Theorem1.2 for the presently public same conclusion. The root's9October timestamp may be stated factually with its evidence limitations. “Independent” requires separately supported discovery history; no inference is supplied here.
4. Credit Caracciolo-Jacobsen-Saleur-Sokal-Sportiello for the forest Grassmann representation; CSS2007 for the forest/exponential/integration identities; Sportiello Chapter10 for the Catalan basis proof; and Kenyon-Wilson for the equivalent quotient/projection structure. Where meander nonsingularity is invoked, cite its original authors. Self-contained rederivation does not erase these credits.
5. Explain the exact Gaussian determinant bridge and distinguish it from inherited structure. The present accepted result establishes a divisor only. Describe the comparison as an alternative calculation/proof exposition unless a materially different mathematical contribution is separately formulated and checked.
6. Propagate these qualifications into introduction, conclusion, README, PR description if updated, bibliography, DOI metadata, result-status labels, keywords and any release announcement. Do not carry an “open mathematics” or “new solution” marketing label as current status. Preserve historical labels only as explicitly dated corpus provenance.
7. Use Alec Kriebel's provided ORCID https://orcid.org/0009-0001-9320-500X accurately for an authored paper. Do not imply coauthorship by prior source authors or human peer review.

No paper was drafted, PR changed, merge/release performed, message sent to an individual, or external outreach prepared in this audit.

## 8. Eligibility, strongest result and remaining gap

| Decision | Result |
|---|---|
| Original mathematical divisor scope | PASS, based on pinned root acceptance; priority comparison matches the original definition. |
| Accurate credited proof/exposition | ELIGIBLE after the dated source addendum and global credit/framing repairs. |
| First or newly discovered full-target theorem | NOT CERTIFIED. Earlier structural results and the exact contemporary match preclude an unqualified assertion. |
| Novel method/quotient/basis | NOT ELIGIBLE on this evidence. These mechanisms are established. |
| Worldwide or intellectual priority | UNKNOWN; do not infer it from missing keywords or printed manuscript dates. |
| Current open status | NOT ELIGIBLE: two presently available complete proof claims address the target. |
| Exactness/irreducibility/complete cofactor | OUT OF SCOPE. |
| Manuscript-ready promotion | CONDITIONAL, not an approval to publish. The concrete remaining repairs are source attribution, exact-match comparison and global metadata wording. |

The strongest verified priority finding is the explicit exact-scope match, with checkable core proofs and qualified timestamps. No older inspected body was found explicitly proving the full divisor before the dated PR. The exact gap is not a remaining mathematical gap in the accepted submitted proof; it is incomplete worldwide historical coverage, particularly Li-Yan's unread body, partial citation chains/version comparisons and independently evidenced discovery/publicity chronology. Resolving those could sharpen precedence or identify an older implicit/explicit corollary. It is unnecessary to resolve them to write an honest credited exposition, but they must remain disclosed.

QUERY_LEDGER.json records26actual search queries and failures. sources/SOURCE_RECEIPTS_MASTER.json records retrieved primary bytes/hashes and failures. sources/INSPECTION_SCOPE.json distinguishes full, critical and partial reads and9visual inspections. Raw PDFs/text/HTML/PNGs and private critical-page caches are confined to ignored sources/rawprivate; public review artifacts contain citations, short analysis and provenance metadata only.

Completion estimate for this assigned bounded priority audit:100%. No estimate of solving worldwide priority is implied.
