# Independent priority audit: equivalent analytic and convex-algebraic results

Audit date: 30 September 2026 (America/Los_Angeles), 1 October 2026 UTC.
Audited object: frozen candidate for PR 9 / problem 30005473.
Auditor family: general analytic/Nash irreducibility, radical support maps, and convex algebraic boundary theory.
Status: completed bounded public-literature audit; historical priority remains unconfirmed.

## Decision

No inspected primary source states the complete all-rank-at-least-two discotope theorem, and no inspected source supplies an exact previous resolution of both target varieties. This audit therefore does **not** establish that problem 30005473 was already solved in the literature.

There is, however, decisive positive prior-art evidence for the central lemma. Kucharz and Kurdyka explicitly record irreducibility of the Zariski closure of an analytic image of a connected real analytic manifold in 2017, printed p.95, in the proof of Proposition 4.3. Candidate Lemma 3 is an elementary complex-field version of that standard observation, not a new irreducibility principle. [Primary article and metadata](https://dspace.uni.lodz.pl/xmlui/handle/11089/23776), [inspected primary PDF](https://ruj.uj.edu.pl/server/api/core/bitstreams/52a654f7-4489-46d9-8157-6c7715c24f3e/content).

The candidate's main theorem is a short application of that standard analytic fact to the support geometry of discotopes. The exact all-rank-at-least-two application and the generic E=S bridge are the potential contributions. Their priority is conditional on the absence of an earlier such application. An assertion that the analytic mechanism itself was newly discovered, or that all Minkowski-sum normal formulas are new, would be contradicted by verified sources. A modestly framed preprint presenting a short proof of the conjecture is consistent with the evidence currently available.

A finite public-literature search cannot certify first priority. It also cannot turn the presence of a standard lemma into documentary evidence that somebody previously stated or recognized its particular discotope corollary. These are different judgments. The correct audit classification is **exact prior resolution not located; standard mechanism confirmed; application priority unresolved**.

## Scope, claims, and success criteria

I independently read the frozen manuscript at:

/Users/alec/Documents/Math/pr9_adversarial_review_20260929/source_snapshot/candidate.md

No manuscript, source snapshot, queue record, branch, commit, or remote was changed. No outside individual was contacted and no outreach was prepared. I did not consult the other priority family's report. A child audit independently checked current citing literature; its artifacts are in citation_subaudit.

The claims evaluated here are those of the supplied candidate:

1. For D equal to a finite Minkowski sum of generalized discs D_i with dim D_i at least two, the complex Zariski closure E(D) of exposed points is irreducible, without genericity or full-dimensionality.
2. Under full-dimensionality and subsetwise general position (GP) of the spans, the purely nonlinear variety S(D) equals E(D).
3. The analytic-image lemma and the normal formula are ingredients rather than separately asserted original contributions.

An exact prior-art match would need the same or weaker assumptions, the same complex Zariski closure, and a conclusion that covers the remaining discotope cases. A genuinely equivalent general theorem would count as strong priority evidence if its already-published hypotheses can be checked without transferring the main problem to another unsupported irreducibility claim.

Search hits, citation counts, abstracts, and phrases such as “irreducible” were used to discover sources. Every central positive or negative match below was checked against an actual primary document. The structured evidence records 49 queries across thirteen batches, including final bibliographic verification. Relative search-engine publication labels were not used as publication dates.

## Primary-source match table

| Source | Verified location and date | What matches | Exact gap or consequence |
|---|---|---|---|
| Kucharz–Kurdyka, Rationality of semialgebraic functions | 2017, pp.85–96; p.95, proof of Prop.4.3 | Connected real analytic source and analytic image have irreducible real Zariski closure | Exact standard mechanism. Complex coefficients require the same identity theorem; discotopes are not discussed. |
| Fernando, On Nash images of Euclidean spaces | arXiv first posted 19 March 2015; inspected v8, 6 April 2018; journal publication 2018 | Lemma7.3 proves irreducible Zariski closure for well-welded semialgebraic sets | Confirms a broader established analytic/Nash framework; no discotope-specific conclusion located. |
| Carbone–Fernando, Surjective Nash maps between semialgebraic sets | Advances in Mathematics 438 (2024), 109288; online 2 January 2024 | Section1.2 and Example5.1(ii), pp.46–47, use irreducibility of Nash images and their Zariski closures | Direct reuse of essentially the same general mechanism, with semialgebraic/Nash hypotheses. |
| Chirikjian–Shiffman, Closed-Form Parametric Equation for the Minkowski Sum of m Ellipsoids in R^N and Associated Volume Bounds | arXiv:2012.15163; 30 December 2020, v2 28 March 2021 | Theorem1.1 gives the same radical normal formula for positive-definite ellipsoids | All matrices are invertible; no lower-dimensional summands and no complex irreducibility conclusion. |
| Ruan–Chirikjian, Closed-Form Minkowski Sums of Convex Bodies with Smooth Positively Curved Boundaries | arXiv:2012.15461; 31 December 2020, v2 12 October 2021; CAD143 (2022), 103133 | Theorem4.1 gives normal addition; Eq.25 gives the two-ellipsoid radical formula | Smooth positive curvature and bijective normal parametrization exclude the general discotope setting. |
| Gesmundo–Meroni, The Geometry of Discotopes | Le Matematiche77(1) (2022), 143–171; publisher date 27 June 2022 | Definition3.3, Remark3.4, Theorems4.3/6.1, and Conjecture8.2 checked | Substantial special cases already published; conjecture concerns S. See exact scope below. |
| Meroni, Two convex conjectures for different flavours | OWR15/2023, pp.829–832; p.830 | The conjecture is explicitly reformulated for exposed-point closure E | Confirms E is the stated 2023 target; it does not prove the missing cases. |
| Sinn, Algebraic Boundaries of Convex Semi-algebraic Sets | Research in the Mathematical Sciences2 (2015), article3; 20 March 2015 | Componentwise duality of extreme-point varieties and algebraic boundaries | Does not assert that the entire exposed/extreme-point variety is one component. |
| Plaumann–Sinn–Wesner, Families of faces and the normal cycle of a convex semi-algebraic set | Online 6 August 2022; Beiträge64 (2023), 851–875 | Definition3.4 and Theorem3.16 describe patches over irreducible boundary components | Component choice is part of the hypotheses; connected normal-cycle patches alone cannot establish global irreducibility. |
| Nie–Parrilo–Sturmfels, Semidefinite Representation of the k-Ellipse | arXiv:math/0702005, 31 January 2007; book chapter2008 | Lemma2.1 and Theorem4.3 use radical/Galois irreducibility | Focal distance quadratics and parameters differ from arbitrary centered positive-semidefinite discotope support forms. |
| Nie–Sturmfels, Matrix Cubes Parametrized by Eigenvalues | arXiv:0804.4462, 28 April 2008; SIAMJ.MAA31(2) (2009), 755–766 | Theorem4.2 gives generic matrix-data irreducibility | Discotope arrow matrices lie in a special non-generic family. Theorem4.3 explicitly permits reducibility. |

## The analytic lemma: exact equivalence and attribution

Exact bibliography:

Wojciech Kucharz and Krzysztof Kurdyka, “Rationality of semialgebraic functions,” in *Analytic and Algebraic Geometry 2*, Łódź University Press, Łódź, 2017, pp.85–96, DOI [10.18778/8088-922-4.14](https://doi.org/10.18778/8088-922-4.14).

The opening observation in the proof of Proposition4.3 says:

> “the Zariski closure Z of φ(M) is an irreducible algebraic subset of X”

This is an 18-word excerpt, verified visually on printed p.95. The actual proposition subsequently concerns composition with a hereditarily rational function. That additional function and its rationality hypotheses are needed for the proposition's meromorphic conclusion; they do not restrict the opening irreducibility observation.

Hypothesis check against the candidate is complete:

- Its nonempty connected open U is a connected real analytic manifold.
- Its F is real analytic on U.
- The codomain can be the algebraic set X=R^m.
- Neither a semialgebraic domain, injectivity, nor nonvanishing derivative is required by that observation.
- The observation concerns real Zariski closure. The candidate uses complex closure and explicitly proves the necessary complex statement.

The field distinction is real but does not create a new mechanism. Here is my independent check, rather than an attribution of extra text to the source. For P,Q in C[X], if (PQ)∘F is zero and P∘F is not zero, continuity gives a nonempty open region on which Q∘F vanishes. Its real and imaginary parts are real analytic; the identity theorem on connected U makes Q∘F identically zero. Hence the vanishing ideal over C is prime. This is precisely the candidate's proof.

A real polynomial that is irreducible as a formal polynomial need not remain irreducible over C. That pitfall is avoided here because the argument is about the vanishing ideal of an analytic image, not merely an arbitrary real irreducible polynomial. No “complex strengthening” novelty should be inferred from this field change.

There is an alternative standard Nash reading. For this particular candidate, U is semialgebraic and F is analytic and semialgebraic, so F is Nash. Its graph is a connected Nash submanifold. Projection from the graph to the value coordinates is algebraic; its Zariski image closure is irreducible. Fernando's 2018 Lemma7.3 and Carbone–Fernando's 2024 reuse confirm that analytic connectivity and Nash images have long-established irreducibility theories. [Fernando primary PDF](https://arxiv.org/pdf/1503.05706), [Carbone–Fernando primary article](https://josefer-ucm.github.io/articulos/aim4.pdf).

This does not require proving that the complex radical cover with all sign choices is irreducible. It follows the single positive real branch through a connected domain. Accordingly, a priority search confined to complex determinantal loci or algebraic independence of radicals would miss the actual proof mechanism.

## Prior normal formulas and the residual application

The candidate's formula, in its notation, is

F(u)=sum_i Q_i u / sqrt(u^T Q_i u).

For invertible ellipsoids, Chirikjian–Shiffman Theorem1.1 uses symmetric positive-definite A_i and gives sum_i A_i^2 n / ||A_i n|| on the unit sphere. Taking Q_i=A_i^2 identifies the formulas. Its Theorem2.4 already supplies addition of normal parametrizations for strictly convex bodies. Ruan–Chirikjian independently uses the same normal-addition mechanism and reproduces the two-ellipsoid formula. Neither inspected document contains “Zariski,” “irreducible,” or a theorem for general rank-deficient summands. [Chirikjian–Shiffman](https://arxiv.org/abs/2012.15163), [Ruan–Chirikjian](https://arxiv.org/abs/2012.15461).

The residual step in the candidate is the exact treatment of singular Q_i: singleton support faces occur precisely off their kernels. Each kernel has codimension at least two, so the common regular domain remains connected; the positive radical branch is analytic there. This reduction is short and elementary. It is the location where the standard analytic theorem applies to the conjecture's rank-deficient geometry.

I did not locate a prior source combining these observations into the full discotope theorem. I also did not find a source presenting the candidate's generic S=E perturbation argument. Their absence from this search is a search outcome, not a proof of first publication.

## Original-source scope: E versus S

The 2022 paper works with S, defined from sums of summand boundary points intersected with the topological boundary. It expressly leaves open whether that variety always coincides with exposed-point closure. Its published irreducibility cases are: the low-boundary-dimension generic range in Theorem4.3; all full-dimensional summands in Remark3.4; and generic sums of two-dimensional discs in Theorem6.1. Conjecture8.2 is generic and excludes segments. [Publisher paper](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734).

In the 2023 report, p.830 defines E using exposed points, retains genericity and dimensions at least two in Conjecture1, and describes generic spans as maximally transversal. It cites the 2022 conjecture as antecedent, while changing the variety's definition. [Official OWR report](https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4).

Consequences independently checked against the supplied candidate:

- Its main theorem directly answers the 2023 E formulation.
- Answering the 2022 S formulation requires its separate GP argument.
- Genericity may be dropped for E by the connected analytic domain, but cannot automatically be dropped for S.
- The candidate's explicit repeated-disc counterexample is an appropriate boundary distinction; it prevents falsely expanding a prior or new E result to all S.
- Exposed and extreme closures coincide for a compact convex set by the usual density of exposed points among extreme points; neither should be silently identified with S in non-generic configurations.
- The full algebraic boundary can have flat-face components. An irreducible E is therefore not a claim that the entire algebraic boundary is irreducible.

Two useful test instances for the claimed residual scope are a generic rank-two disc plus a rank-three disc in R^3, and two generic rank-three discs in R^4. In both, the sum of (dim D_i−1) exceeds d−1, not all summands are two-dimensional, and not all are full-dimensional in the ambient space. These fail the three listed special-case templates, while satisfying the candidate's hypotheses. This is my hypothesis comparison, not a claim that those instances are historically unprecedented.

## General convex-algebraic routes tested

Sinn's 2015 Corollary3.4 maps each irreducible component of an extreme-point closure to a dual algebraic-boundary component. It is powerful componentwise information. It does not count the components, and applying it here would still require the very connected-analytic or radical argument under audit. The route is therefore **blocked as an independent already-solved certificate** at the missing global one-component claim. [Primary article](https://link.springer.com/article/10.1186/s40687-015-0022-0).

Plaumann–Sinn–Wesner's patches are defined over an already chosen irreducible component of the algebraic boundary. Theorem3.16 then establishes dimensions, openness, and constant face dimensions for one patch. Passing through exceptional normals or across patch closures can introduce larger faces. Treating the whole regular-normal image as a single patch requires extra work; connectedness alone does not justify it. This route is **blocked as a standalone resolution** at the unproved identification of all relevant points with one component. [Primary article](https://link.springer.com/article/10.1007/s13366-022-00657-9).

General smoothness is also insufficient for the candidate's proof. The operative property is real analyticity on a connected parameter domain, not mere topological connectedness or C-infinity smoothness. Thus a source saying that an ellipsoid sum has a smooth boundary is not automatically a theorem for singular discs or a complex exposed-point closure.

Zonoid status cannot replace these checks: zonotopes themselves are zonoids, yet their exposed-point varieties are finite unions of points. The rank threshold is central. A segment adds a codimension-one exceptional kernel; the candidate's stadium example makes the resulting disconnected branches and reducible E explicit.

## Radical and spectrahedral routes tested

Nie–Parrilo–Sturmfels construct k-ellipse equations by taking a product over radical sign choices and analyze irreducibility by Galois action; their weighted and higher-dimensional extensions are checked. This is important precedent for radical elimination and algebraic-boundary irreducibility, but the input quadratics are translated focal distances. Arbitrary centered anisotropic positive-semidefinite forms and repeated summands are not the same hypotheses. [Primary paper](https://arxiv.org/pdf/math/0702005).

Nie–Sturmfels Theorem4.2 proves irreducibility with independent generic symmetric-matrix data. The source itself warns that structured matrices require additional analysis, and Theorem4.3 allows a reducible hypersurface. Discotope norm expressions can be encoded by arrow-type matrices, but those lie in a special coefficient family with built-in spectral degeneracy. A generic theorem cannot simply be specialized there. [Primary paper](https://arxiv.org/pdf/0804.4462).

A possible new deduction through polar bodies would require proving irreducibility of the appropriate polar boundary and checking that its projective dual recovers exactly E, without exceptional extra components. Doing that would be another proof, not evidence that the existing matrix-cube theorem already covers the target. The route is **blocked as a priority match** at the non-generic specialization and exact duality identification. The candidate wisely avoids reliance on radical independence or this unsupported transfer.

## Current citing literature and unobservable priority

The completed independent citation subaudit checked primary publications and theses, including Fiber Convex Bodies, Line Multiview Varieties, the Meroni and Mathis theses, and the 2026 Operatopes preprint. Its exact results and retrieval gaps are retained in [citation_subaudit/REPORT.md](citation_subaudit/REPORT.md). Its evidence includes [audit_checks.json](citation_subaudit/evidence/audit_checks.json), [source_manifest.json](citation_subaudit/evidence/source_manifest.json), `search_responses.json` (local-only raw capture), and the retained OpenAlex index responses. No exact prior resolution or material publication blocker was found in that branch.

The IMProofBench lead arose from a primary author publication page. The subauditor independently read/searched the public v2 PDF and HTML, dated 9 July 2026: no discotope, Gesmundo, or irreducibility terminology was found, and no public target/result match was located. The primary paper and homepage describe a private benchmark collection whose contents were inaccessible. Absence of a public match cannot rule out a privately held earlier proof. This limitation should not be converted into either an “already solved” verdict or a claim of certified novelty. [Primary version history](https://arxiv.org/abs/2509.26076), [public v2 HTML](https://arxiv.org/html/2509.26076v2), [benchmark homepage](https://improofbench.math.ethz.ch/).

Citation indexes were used as discovery aids only. They returned incomplete or unavailable information in the child audit. In particular, a zero citation count attached to an arXiv record cannot override directly verified citing references in primary documents.

## Reproducibility and remaining gaps

Public checkable artifacts include:

- evidence.json: complete query list, source identifiers, dates, hypothesis matches, inference labels, and verdict.
- local_sources_manifest.json: SHA-256 hashes of downloaded primary PDFs, with text extraction metadata.
- citation_subaudit: separately preserved primary citing-literature check.
- RESEARCH_LOG.md: timestamped checkpoints and completion estimates.

Raw web_results_archive.json, web_results_archive_addendum.json, citation-subaudit search_responses.json, downloaded PDFs, full extracted texts, and kk2017_ocr-11.png with its OCR derivative are local-only audit aids, excluded from the public archive. The concise report and structured query/source evidence are the publication artifacts. Their hashes and URLs permit re-fetching without republishing the sources themselves.

Remaining priority gaps are exact and material:

1. No exhaustive search of every language, unindexed thesis, proceedings volume, or private manuscript was possible.
2. Public citation graphs are incomplete; not every citing document is discoverable or accessible.
3. Author correspondence is excluded by project policy; no unpublished resolution can be checked by outreach.
4. No exact published all-rank-at-least-two E theorem or generic S=E bridge was located.
5. The standard analytic theorem already entails the E conclusion once the elementary regular-normal reduction is checked. Whether an overlooked application is sufficiently novel for a particular journal is an editorial judgment, not determined by this audit.
6. A bounded negative literature finding should be stated as “we have not located a prior resolution,” not “this is the first proof” or “priority verified.”

The audit is complete for its stated bounded scope. It supports correcting attribution and retaining explicit priority uncertainty. It does not provide a historical-priority certificate.
