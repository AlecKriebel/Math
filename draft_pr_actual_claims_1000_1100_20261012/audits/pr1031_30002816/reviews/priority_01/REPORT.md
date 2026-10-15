# Independent adversarial priority audit: PR1031 / 30002816

Submitted head: f6570e093267a7f910faf9cdd60dfbc1c12f5681. Audit started 2026-10-13T05:43:37Z. Written 13 October 2026 UTC. Reviewer: independent AI source/priority adversary.

## Verdict and exact scope

**Bounded no-match, with mandatory credit and framing fixes.** In 84 exact and mechanism-based web queries, 25 successfully retrieved primary PDFs (including versions of the same work), and the relevant complete theorem pages of the closest sources, I did not locate a prior statement or proof of the full negative theorem for the real oriented mass ball \(C_{4,12}\), the exact Kähler-face/normalized-complex-\(\operatorname{Sep}(3,3)\) section used here, or the resulting general negative answer to Harvey-Lawson Question 6.5. This describes this search, **not** a worldwide-first certification or a current worldwide-open assertion. Novelty and priority remain unestablished beyond the bounded comparison.

The scoped mathematical claim supplied to this audit is: the convex hull of both orientations of decomposable unit real four-vectors in \(\Lambda^4\mathbb R^{12}\) admits **no finite projected SDP lift**, because two affine hyperplane equations select a set real-linearly isomorphic to normalized complex \(\operatorname{Sep}(3,3)\). It follows that some supporting affine function lacks a degree-at-most-one SOS representation modulo the full unit Grassmann vanishing ideal. A constant closed comass-one four-form then lacks the pointwise, and hence local, norm completion asked for in Question 6.5.

The rational claim is only existential rational coefficients for the **unnormalized** linear functional. The proof supplies no explicit coefficient list, exact comass, rational normalized calibration, least dimension, or lower-dimensional classification. Root mathematical acceptance is an input; this review does not reprove the whole mathematics or Fawzi's external theorem.

## Independence and reproducibility

Before searching, I read only the submitted current/PROOF.md, ROOT_MATH_AUDIT.md, and the permitted URL/version metadata in submitted/historical/SOURCE_METADATA.json. I did not read historical PRIORITY_REPORT, PRIORITY_SOURCE_LEDGER, SOURCE_REVIEW, or acceptance priority conclusions. No other shard worker was consulted. Messages to the root reported independently obtained findings.

QUERY_LEDGER.json preserves all 84 exact queries and batch discovery URLs. sources/SOURCE_PINS.json records primary URLs, hashes, byte counts, source versions, complete-page locators, interpretation, and exclusions. sources/FORWARD_CITATION_DISCOVERY.json records three OpenAlex discovery requests and their returned titles. Citation metadata found candidates; it was not theorem evidence.

Raw third-party PDFs, extracted text, source page images, and citation API responses remain solely under ignored sources/raw/. Authored metadata remains outside raw. An author-hosted Blekherman-Smith-Velasco URL returned HTML rather than PDF; it is explicitly excluded as a downloaded PDF, with the arXiv primary alternative pinned. Publication dates came from primary headers/records, not search-engine crawl labels.

## Closest original statements

### Sanyal, Rostalski, and the target conjecture

The original [Sanyal OWR2015 contribution](https://ems.press/content/serial-article-files/46561), printed pp.707-709 / PDF47-49, defines the oriented mass ball and optimizes \(\ell\) by replacing nonnegativity of \(\delta-\ell\) with SOS modulo the Plücker-plus-sphere ideal. Its universal conjecture is the degree \(D=1\) assertion for all Grassmann orbitopes; its reported \(n\le7\) findings are computational. It expressly places the computations in joint work with Philipp Rostalski and identifies equivalence to Harvey-Lawson Question 6.5.

That lineage predates 2015. [Rostalski's BIRS slides](https://www.birs.ca/workshops/2010/10w5007/files/rostalski.pdf), dated 15 February 2010, already use theta bodies, size-\(n+1\) moment matrices, affine squares, and the Harvey-Lawson connection (slides14-21). [Gouveia and Thomas's 2013 chapter](https://www.mit.edu/~parrilo/sdocag/MO13-Blekherman-Parrilo-Thomas.pdf), printed p.323 / PDF336, states the oriented Grassmann first-theta-body question and credits unpublished Sanyal-Rostalski work. Its actual chapter title, Spectrahedral Approximations of Convex Hulls of Algebraic Sets, and authors appear at printed p.293 / PDF306. These dated statements do not establish current worldwide-open status in October 2026.

### Harvey-Lawson and the classical Kähler ingredient

The [1982 article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6313-11511_2006_Article_BF02392726.pdf), printed p.68 / PDF22, asks locally for differential \(p\)-forms \(\psi_j\) satisfying
\[
\varphi(\xi)^2+\sum_j\psi_j(\xi)^2=\|\xi\|^2
\]
on every simple \(p\)-vector. It is a question, not an all-calibrations theorem. The paper gives affirmative answers for selected geometries. Printed p.70 / PDF24, Theorem6.11, supplies a classical complex/Wirtinger identity. Thus the Kähler calibration and its equality locus are established ingredients. The failing calibration here is existential; it is **not** identified with the Kähler form exposing the intermediary face.

[Barvinok-Blekherman2005](https://library.slmath.org/books/Book52/files/03barv.pdf), printed pp.54-55 / PDF4-5, already describes oriented unit mass/comass balls and classical complex faces. Its metric/ellipsoid conclusions do not imply the present no-lift conclusion.

### The decisive no-lift theorem belongs to Fawzi

[Fawzi's published paper](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download) defines normalized complex separable states at p.1319, arbitrary projected Hermitian spectrahedral lifts at p.1320, and states Theorem1 at p.1321. It explicitly includes \(3\times3\) and distinguishes its theorem from failure of a particular hierarchy or finite positive-map tests. The obstruction was public in [arXiv1905.02575v1](https://arxiv.org/pdf/1905.02575v1), 4 May 2019; publication was 31 July 2021.

This project applies that established theorem. It is not a new proof that separable states lack finite lifts, a new disproof of Helton-Nie, or a new quantum separability criterion. The complex/Hermitian formulation and trace-one normalization must be cited correctly.

## An exact prior component found by the adversarial search

### Vrana-Levay2009 proves the pure tensor-to-wedge lemma in greater generality

[Vrana-Levay](https://arxiv.org/pdf/0902.2269), §3.1 pp.8-9 in the pinned v2, defines the embedding
\[
\bigotimes_i\Lambda^{k_i}H_i^{(0)}
\longrightarrow \Lambda^{\sum_i k_i}\!\left(\bigoplus_iH_i^{(0)}\right)
\]
by wedging factors (equation25). Its lemma and general theorem prove that the image is decomposable exactly when the original vector is a tensor product of decomposable factors. The submitted \(T(x\otimes y)=x\wedge y\), and the fact that a decomposable element of \(U\wedge Z\) is a rank-one tensor, are the \(N=2,\ k_1=k_2=1\) specialization.

This is an exact prior component, not merely an analogy. The paper must cite it while retaining the elementary proof for checkability. The reviewed source does not supply the real Kähler mass-ball realization or Fawzi's later obstruction. I did not infer that every possible mixed-state convex section had already been stated there.

### Fermionic projector convex hulls are established

[Schliemann et al.2001](https://epub.uni-regensburg.de/28249/1/PhysRevA.64.022303.pdf), article pp.1-2, supplies the two-fermion Slater framework and pure density projectors. [Grabowski-Kuś-Marmo2012](https://arxiv.org/pdf/1111.4812), Definition4.2 / PDF8 and Theorem5.1 / PDF10, expressly describes mixed fermionic nonentangled states as convex combinations of decomposable pure projectors using generalized Segre maps. The submitted \(K=\operatorname{conv}\{zz^*:z\text{ decomposable unit}\}\) is consequently a standard fermionic separability body.

[Iemini et al.2012](https://arxiv.org/pdf/1206.0024v1), PDF4, equation17, gives the same mixture description. Equation20 retains infinitely many constraints; the following paragraph uses finite sampling as a probabilistic relaxation. Its SDP wording is not an exact finite representation of this body.

## Strong nearby no-shadow results and the embedding distinction

### Curvature/quadratic Grassmann cones

[Bettiol-Kummer-Mendes](https://arxiv.org/pdf/1908.03713v2), Corollary4.2 and Remark4.3 / p.17, shows that the cone \(P_{\mathrm{Gr}_k(n)}\) of all nonnegative homogeneous quadratic forms on real Grassmannian points is not a spectrahedral shadow for \(n\ge5,\ 2\le k\le n-2\). This is already present in [v1](https://arxiv.org/pdf/1908.03713v1), pp.15-16, 10 August 2019. The NSF-hosted version was compared and its theorem page visually checked.

The paper identifies the orbit representation as \(\operatorname{Sym}^2(\Lambda^k\mathbb R^n)\), materially different from the oriented exterior-power mass ball. Passing from \(p\) to \(pp^T\) is quadratic, loses orientation, and is not an ambient linear map of that convex hull. Arbitrary nonnegative quadratics also exceed the special class \(\delta-\ell\), or \(\|\xi\|^2-\varphi(\xi)^2\), needed here. A further identification/reduction would be required; none was located in the inspected bodies. This comparison prevents an incorrect claim of the first Grassmann-related no-shadow theorem.

The same authors' [2025 symmetry paper](https://arxiv.org/pdf/2408.03231), TheoremsA/B, pp.1-2, and Example3.4, p.7, treats equivariant descriptions and polar representations and revisits the curvature example. It supplies no inspected extension to this mass ball.

### Minimal degree and generic polynomial-image obstructions

[Blekherman-Smith-Velasco](https://arxiv.org/pdf/1308.0751), Theorem1.1, characterizes when all nonnegative homogeneous quadratics on a real irreducible nondegenerate projective variety with Zariski-dense real points are linear SOS. Non-minimal degree gives non-SOS quadratics, not automatically a failing supporting affine function on the oriented unit variety.

[Scheiderer](https://arxiv.org/pdf/1612.07048), Theorem4.23 and Corollaries4.24/4.25, pp.15-16 of v3, gives polynomial images/Veronese cones with no finite lifts. A polynomial embedding with this behavior need not be the particular Plücker unit embedding. The [Lifting for Simplicity survey](https://arxiv.org/pdf/2002.09788), p.40, Theorem5.16, presents generic monomial obstructions and the established finite-dimensional SOS framework. No reviewed exact Grassmann reduction was located there.

## Weaker results and false matches rejected

[Sanyal-Sottile-Sturmfels2011](https://franksottile.github.io/research/pdf/Orbitope.pdf), Theorem7.6 / p.34, excludes an unprojected spectrahedron using nonexposed faces for \(G_{3,6}\) and its polar. The following p.35 explicitly leaves projected spectrahedra unresolved at writing. Examples elsewhere in the paper have nonexposed faces while admitting projected lifts. This is neither the full no-finite-lift theorem nor an affine-SOS counterexample.

[Kobert-Scheiderer](https://arxiv.org/pdf/2010.02045), p.7, Theorems4.2/4.4, proves positive representations under a polar-representation hypothesis. Its cited \(G_{3,6}\) negative still concerns being a spectrahedron. Removing the polar hypothesis would invalidate the application.

[Katz-Shnider](https://arxiv.org/pdf/0801.0283), §7, Proposition7.1 / pp.16-18, names a counterexample: its all-positive-coefficient self-dual form has comass2. This refutes a sign/comass guess, not norm completion or projected lifts.

Forward-citation candidates [De Las Cuevas-Netzer2021](https://arxiv.org/pdf/2102.04240), p.9, Theorem1, restate Fawzi and derive different map-cone applications. [Gribling-Laurent-Steenkamp](https://arxiv.org/pdf/2109.14494), p.1 and relevant keyword screen, concerns separable rank and moment hierarchies. No reviewed target bridge was located in either.

## Credit allocation and mandatory whole-paper fixes

The unmatched assembly in this audit is specifically the real ambient-linear identification of the classical Kähler face, its PSD support section selecting \(U\wedge Z\), and Fawzi's complex separability obstruction to obtain the oriented \(C_{4,12}\) theorem, followed by the supporting-SOS/constant-calibration consequence. Calling the entire chain new overcredits the project. Even this assembly has only a bounded no-match finding.

Apply these fixes globally before promoting a paper/package: title, abstract, introduction, theorem labels, conclusion, README, PR summary, and status metadata.

1. Lead with a reduction/application of Fawzi's theorem; cite the published result and its 2019 preprint.
2. Credit Harvey-Lawson/Wirtinger and the existing complex-face/projector interpretation. Cite Vrana-Levay2009 for tensor-to-wedge decomposability and Grabowski-Kuś-Marmo2012 for the mixed-projector hull.
3. Credit theta-body/moment lineage: [Gouveia-Parrilo-Thomas2010](https://arxiv.org/pdf/0809.3480), Definitions1.1/1.4 and Theorem2.14, with Lasserre/Laurent as appropriate; [Gouveia-Parrilo-Thomas2013](https://arxiv.org/pdf/1111.3164), Theorem2.4, supplies general lift/factorization background. The compact trace-bound argument may be presented as a self-contained specialization.
4. Credit Sanyal-Rostalski's Harvey-Lawson/SOS connection with OWR2015, the 2010 slides, and Gouveia-Thomas2013. Do not describe the equivalence as newly discovered.
5. Discuss Blekherman-Smith-Velasco and Bettiol-Kummer-Mendes, separating quadratic/symmetric-square cones from the oriented mass ball.
6. Separate no unprojected LMI, no finite exact level of a named hierarchy, and no arbitrary finite projected SDP lift. The present conclusion is the last.
7. Preserve the existential boundary: rational unnormalized coefficients exist; no explicit form, exact comass, rational normalized calibration, minimal dimension, \(G_{3,6}\) obstruction, or \(n\le7\) classification.
8. Call the original 1982 item Question6.5. Say the theorem gives a negative answer in general; do not silently rename it a universal theorem or imply failure of the classical positive Kähler examples.
9. Remove first-proof, first-counterexample, worldwide-novelty, current-worldwide-open, independently-reproved-Fawzi, journal-acceptance, human-peer-review, or formal-verification claims. A newly generated paper/package needs fresh complete claim/citation/consistency review after these fixes.

## Search limits and exact remaining gap

The 84 queries cover exact names, degree-one/affine SOS, mass/comass balls, Grassmann shadows/lifts, Fawzi, calibrations, theta bodies, Slater/fermionic states, Kähler faces, Segre/wedge embeddings, minimal degree, and older/later literature. OpenAlex returned 18 Fawzi-DOI citing records, 52 Scheiderer-DOI citing records, and 6 curvature-DOI citing records. These are incomplete citation graphs and may include duplicated works or omit preprint citers. Closest discovered candidates received body inspection; every citing article was not read.

There was no exhaustive MathSciNet/zbMATH/Google Scholar census, complete non-English/thesis/unindexed coverage, or examination of every equivalent formulation of calibration/comass inequalities. Batches blend search results: no target hit is not a query-specific zero-result proof. Rebuilt arXiv PDFs and publisher-versus-author pagination require the pinned version locators. The main remaining priority gap is whether the same assembly or existential Harvey-Lawson negative appears in an unlocated source.

Specialist familiarity could help identify unindexed earlier work. Under the independent-research policy this is recorded only as a limitation: no individual was contacted and no outreach prepared. This audit is complete as a bounded comparison; global priority remains unestablished.

