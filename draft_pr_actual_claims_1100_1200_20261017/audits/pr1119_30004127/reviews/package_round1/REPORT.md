# Fresh adversarial whole-package review, round 1

Review completed 17 October 2026 UTC. Scope: PR1119 / problem 30004127, frozen publication package. **Verdict: PASS. Required repairs: none.**

This is a fresh whole-package mathematical, evidence, reproducibility, publication-metadata, and visual review. I reconstructed the operative note and the original direct proof before reading the prior root/reviewer conclusions. Those conclusions were subsequently checked as supporting artifacts, rather than used as mathematical premises. No external individual was contacted; no other worker was coordinated with; no PR, Git, tracker, publication, or global acceptance state was changed. All retained review outputs are in this folder. Downloaded third-party bodies and page images are confined to ignored `tmp/`.

The strongest verified outcome is the complete stated separation for the fixed property, under the original total sample-plus-adjacency convention. The literature conclusion remains bounded: no earlier publication giving the full comparison answer or the needed fixed-property weighted bridge was identified in the inspected set. Priority and novelty remain uncertified. The official GS2021 journal body was unavailable, and forward-citation coverage remains incomplete.

## 1. Exact frozen evidence

The six supplied release identities were independently recomputed before review:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `main.tex` | 15,976 | `4ab7d27fc11bba6d21ada7782834ef72442e1c3d8fac2a7253547eaa4c6ec9e4` |
| Five-page PDF | 80,465 | `a9d81e3b765adc8ee9bee044d23008515e31bbeb57a916358f32e8d3c021a1f0` |
| Source and verification ZIP | 301,162 | `4367fad39640b11fb1809c2302a91947a9343dd8179590a51ef87e5756caa5cb` |
| Upload-kit ZIP | 374,039 | `c749466c7322d3cb1b6b97d31961170d76596ea901bb0d915a700ade18a0d55c` |
| Zenodo metadata | 3,575 | `1c890f0b57cd23cad96555bd73baf422d33b54a36ae267ee5bf5445f35e0e60d` |
| Live deposit manifest | 3,866 | `9ec7a0d847180c0417e789efc999f44707318e211e542152053ca36149eab559` |

The original proof is 25,005 bytes, SHA-256 `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`, including inside the archive. Its supplied PR head is `786fff9ba06951209e8c1e3bc6114efbfa2c9d16`. I verified local byte identity and internal provenance consistency; I did not independently authenticate remote Git history, which was outside this read-only assignment.

`FROZEN_INPUT_RECEIPT.json` covers every live publication file, including rendered assets. The final integrity check found all of those files unchanged. `ARCHIVE_INTEGRITY.json`, `VERIFIER_AND_REBUILD_QA.json`, `PDF_QA.json`, `VERIFICATION_RUN.json`, and `FINAL_INTEGRITY_CHECK.json` contain the separate check receipts.

## 2. Claim, hypotheses, and what would falsify it

Let C3 mean 3-colorability, A3 deletion of at most one vertex followed by 3-colorability, and P = K4-free intersect A3. The exact claim is a polynomial, one-sided classical canonical tester on every nonempty finite input size without knowing n, versus exp(Ω(log²(1/ε))) worst-case **total** VDF oracle cost along a positive rational sequence, against adaptive two-sided algorithms. The lower bound survives supplied vertex names, n, the entire rational distribution, and the heavy vertex. Distances count changed unordered pairs with weight D(u)D(v), permit both additions and deletions, and use n² in the uniform case.

A successful counterexample would exploit an arbitrary repair cheaper than the claimed apex identity, a coloring/list or repeated-label error, an unsupported large-n restriction, an adaptive named-query shortcut, a failure of the older two-sided theorem to cover the source model, or prior publication of the full answer. I tried these routes. No such defect was found. No polynomial running-time claim and no sample-only lower bound with unlimited free arbitrary-name queries is being certified.

The [original workshop report](https://ems.press/content/serial-article-files/46798) was freshly downloaded and text-inspected; physical pages 26–27 were independently rendered and viewed. Printed page 1138 explicitly counts samples plus edge queries and withholds n. Printed page 1139 has the relevant Problem 5, with heredity and extendability. [GS arXiv v5](https://arxiv.org/abs/1905.09903v5), §5.3, retains Problem 5.6. This verifies that the operative note addresses the actual original target.

## 3. Independent classical-side reconstruction

P is hereditary: restriction retains the possible exceptional vertex, or becomes 3-colorable when that vertex is absent; K4-freeness is hereditary. Isolated extension and edge deletion preserve both requirements. C3 is contained in P.

For a proper partial coloring on S, the lists exclude colors of neighbors in S. Let U be empty-list vertices. For the other outside vertices, δ(v) minimizes the number of neighbors whose lists contain v's chosen color. Coloring by minimizing colors and deleting monochromatic edges changes at most n|U| + Σδ(v) pairs. There are no monochromatic pairs within S or from S to nonempty-list vertices. Counting a remaining pair more than once only enlarges this upper bound. Thus ε-farness from C3 forces |U∪W| ≥ εn/2 for W defined by δ(v) ≥ εn/2.

The list potential starts at 3n. **Every** feasible color on a W-vertex removes that color from at least εn/2 other lists; a U-selection ends the branch. With h = floor(6/ε)+1, a feasible branch cannot last h levels. Each fixed tree address at depth j is determined by previous blocks; the next block misses its danger set with conditional probability at most exp(-εℓ/2). Summation over fewer than 3^h addresses gives failure probability below 1/12. Shared blocks among nodes require no independence of node failures. A proper coloring of the distinct sampled labels would follow a surviving branch. Selected vertices lie outside the path's colored set, so repetitions are harmless.

Farness from P implies farness from C3, in the correct inclusion direction. For n≥N=12r², two r-blocks give two non-C3 witnesses and disjoint label sets with failure probability at most 1/12+1/12+r²/n≤1/4. Deleting one vertex leaves one witness intact. For 1<n<N, M=ceil(N log(3N)) gives coverage failure at most n exp(-M/n)≤N exp(-M/N)≤1/3. The n=1 case is immediate. The same tester handles both cases without n. It collapses repeated labels before deciding membership; it does not turn occurrences into twins.

The resulting M is O(ε^-6 log(1/ε)), and pair queries are at most M(M-1)/2. This proves the stated exponent-12 adjacency upper bound. Larger ε uses 1/8. The empty graph can be accepted when separately supplied; no probability distribution exists on its empty vertex set. Exact threshold equality causes no gap, and alternative strict conventions can be handled by a fixed rescaling. The computationally expensive finite membership decision is allowed by the oracle-count claim.

The [Alon–Krivelevich author manuscript](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/AlonKrivelevich.pdf), Theorem 3 and §4, was freshly inspected for the credited branching-list antecedent. The operative proof supplies its own conservative all-size bound and does not import that source's negligible-collision/large-input qualification.

## 4. Independent repair and reduction reconstruction

Write τ(X) for minimum triangle-hitting deletions. Intersecting any triangle-free target with the input removes its additions, preserves triangle-freeness, and cannot increase edit cost. Hence τ(X) also equals minimum unrestricted triangle repair cost.

For a 3-colorable tail H on n≥1 vertices, a universal apex of mass 1/2 and tail masses 1/(2n) give the exact identity

    dist_D(J(H),P) = τ(H)/(4n²).

The upper bound deletes τ(H) tail edges. The tail stays 3-colorable and becomes triangle-free, so its apex join lies in P. For an **arbitrary** target F∈P, let S be tail vertices losing their apex adjacency and t its changed tail pairs, including additions. F outside S must be triangle-free, since the apex still neighbors all of that set. Using that restriction and isolating S changes at most t+n|S| pairs of H. The original weighted cost is (t+n|S|)/(4n²). This proves the reverse inequality. Changing the exceptional vertex, adding tail pairs, or partially erasing the apex gives no escape. The proof only uses K4-freeness for the reverse inequality; the original tail's colorability is used in the forward direction.

For the cover L(H), the first coordinate is a proper 3-coloring. A triangle projects to three distinct original vertices because loops are absent. Each original edge has six distinct lifted edges. Project a minimum cover deletion repair by deleting an original edge whenever **any** of its lifts was deleted. At most t original edges are deleted for t lifted deletions, and a surviving original triangle would have a surviving lifted triangle. Consequently τ(L(H))≥τ(H). Dividing by (3n)² supplies 1/9; composing with the apex identity supplies 1/36. No promise on the colorability or triangle overlap of H is needed. n=0 is excluded from the formula and accepted separately by a source tester.

The exact oracle simulation returns zero for self-pairs, same-part pairs, and different copies of one original vertex. Apex–tail pairs are one. Every remaining pair takes one source adjacency query. Samples are generated locally from known n and the explicit distribution. Names can explicitly expose the cover representation; that gives no hidden information about H's unknown edges. Randomized, adaptive decisions and early stopping preserve the exact transcript law. Full D is independent of unknown source edges.

An execution with s samples and e adjacency calls mentions at most s+2e original labels. A single worst-case total budget Q therefore inspects at most 2Q source vertices, even when the split varies with history. This is the bridge to the imported inspected-vertex lower bound; I have not silently equated vertex count and adjacency-query count.

## 5. Fresh check of the essential imported theorem

Both primary author files were freshly retrieved: [subdir.pdf](https://www.math.tau.ac.il/~asafico/subdir.pdf), 284,288 bytes, SHA-256 `4a3281bbbd041392d814f07c2745d4c600ee9f20aa97fd781db0d8f94ac98641`; and [testdig5.pdf](https://www.cs.tau.ac.il/~nogaa/PDFS/testdig5.pdf), 333,821 bytes, SHA-256 `4062298c6ef20e0ee1dfe469057052a2d713765c6e2e9768352081507293b5ff`. These are author versions, not falsely labeled journal VoR bodies.

In the first version I read definitions on physical p.2, the cost convention on p.4, Theorem 4(ii) on p.5, and the two-sided proof in §7, pp.24–27. The theorem and concluding lower-bound page were also rendered and viewed. It gives n, permits desired-pair queries, counts inspected vertices with their induced graph available, states the exponent (1/δ)^{c log(1/δ)}, and explicitly states its undirected non-bipartite consequence. The proof uses two local deletion worlds and random relabeling; it is a two-sided indistinguishability result, not merely failure to find a triangle.

The above 2Q accounting allows an arbitrary-pair VDF execution to be simulated within that stronger inspected-vertex model. At δ=36ε, the source theorem forces the claimed exp(Ω(log²(1/ε))) total-cost lower bound. Ordered versus unordered pairs, strict farness, and fixed rescalings only change constants. A rational subsequence suffices; the constructed weights are already exact positive rationals. The source's sufficiently-large-size qualification is harmless for a worst case over all finite sizes. Thus the critical imported dependency is checked rather than left as an unsupported name or abstract.

## 6. Original direct proof and adversarial boundary checks

I also reconstructed the unchanged original proof as an independent route to the same lower-bound scale. Its sphere pigeonhole count yields at least 2^(d²-2d)/d vectors; taking the floor gives a positive K for d≥4. Canceling the encoding shift before comparing base-2B digits avoids carries. Midpoint equality and equal squared norms force equal vectors. Each edge type identifies its designated (x,a); an extra triangle would give a+b=2c in the progression-free set. Thus the tripartite host has exactly T=mK edge-disjoint designated triangles and no others.

Even/odd retained-edge patterns agree on every proper coordinate subset. All GOOD tails are triangle-free. In BAD, Z~Bin(T,1/4) counts full triangles, and minimum unrestricted triangle repair is exactly Z deletions. The apex distance is Z/(4n²). The exponential-moment calculation at log 2 gives P[Z<T/8]≤exp(-T/32); it does not condition BAD on farness and thereby introduce unwanted correlations.

For arbitrary adaptive named queries, condition on exact exposed host identities and observations. The unused part of the secret bijection remains uniform. Observations may reveal geometry of old vertices, but cannot bias the image of a particular unused name. Samples are coupled by names and do not expose an extra image when repeated. Full induced-graph observations agree until a designated triangle is fully exposed. Continue a marginal experiment after coupling failure and pad after stopping with fresh unused images; the **unconditional** padded sequence is uniform. No uniformity conditional merely on nonfailure is needed. The triangle union bound is T(k)_3/(n)_3, coarsened to 2Tk³/n³, with k≥n handled by the trivial bound.

GOOD rejects with probability at most 1/3; unconditional BAD rejects with probability at least (2/3)(1-p), so the gap is at least 1/6 for p≤1/4. The constants give s+2e≥(n³/(12T))^(1/3) and Q≥(n³/(96T))^(1/3)≥m^(1/3). With ε_d=K/(1152m), log(1/ε_d)=Θ(d), whereas log m=Θ(d²). Floors and positive small-d bounds are correct. This rules out fixed polynomial comparisons after any fixed positive classical proximity rescaling.

The doubled-wheel argument correctly allows arbitrary internal class edges: any one gives K4; with none, deletion of one vertex leaves a wheel transversal. P is therefore not blowup-avoidable. This is a direct obstruction, not a converse falsely inferred from GS's positive proposition. A sample-only bound with free arbitrary-name queries would be false because the whole finite graph could be read with zero samples; neither operative theorem nor metadata asserts it.

## 7. Programs, conversion, and portable package

I read all six public programs and the runner/converter, then ran all controls in ordinary and optimized Python on extracted copies. `VERIFICATION_RUN.json` records **12 successful executions** with complete expected mathematical JSON equality. The final reproduction used an own-folder TMPDIR. All programs use the standard library.

The finite scopes match the README: 33,867 classical graphs through order six, all-size parameter/coupon controls, 1,032 exact arbitrary-repair apex identities, arithmetic/parity/wheel controls, exact adaptive policies and posterior checks on a six-vertex host, all 76 cover inputs through order four including empty input, and 75 nonempty bridge inputs with all target repairs on at most five vertices. These are finite falsification evidence; no run is being substituted for a universal proof or a priority certificate.

The weighted edit-cube transform optimizes over every target mask. The triangle solver branches on the three edges of a surviving triangle and validates its returned repair. Coloring search and the separate monochromatic-edge minimization provide different finite checks. The oracle Bellman recursion optimizes adaptive query policies; its strict adaptive/nonadaptive difference prevents a misleading nonadaptive-only control. Its known-map negative control tests the precise information gift that would destroy the direct proof.

For each original/public verifier pair, hashes, count of converted assertions, and byte equality with a fresh conversion all agree. No public checker retains an ast.Assert. The converter preserves conditional evaluation of each guard and evaluates the original message only after failure. An independent false-guard condition/message side-effect check succeeds in ordinary and optimized modes. The only ignored cover-result fields are elapsed time and the historical self-hash; the actual public code hash is verified separately, and case data, optima, and witnesses remain compared.

The source ZIP has 98 unique safe members. SOURCE_MANIFEST covers the other 97 exactly, and equals the source-members table in PACKAGE_RECEIPT. The kit has exactly five members; its PDF, source ZIP, metadata, and README match the frozen assets, and its deposit manifest names the two adjacent upload files. The live manifest paths resolve relative to publication and its metadata equals standalone metadata. Author, ORCID checksum, date, version, title, license and claims are consistent. The package contains no third-party article bodies, extracted source text, or source images; its only PDF member is the authored note.

I ran `build_package.py` from the extracted archive. It verified the retained review fingerprints, reconstructed the public guard copies and expected results, ran all twelve checks, and rebuilt **both ZIPs byte for byte**. Thus the portable reproduction claim is independently supported. Historical receipt paths remain historical, as the README explains. The original proof is preserved unchanged; its embedded references to its historical audit context are not being advertised as an additional external certification.

## 8. Independent PDF compilation and visual QA

I copied the existing Tectonic cache into ignored own-folder storage and compiled extracted main.tex with `-C --untrusted --keep-logs` and that isolated cache. Compilation succeeded with no warnings, overfull boxes, or missing references. It produced five letter-size pages.

All five compiled pages were rendered at 110 dpi and viewed individually. No clipped text, overlap, broken glyph, unreadable equation, or bibliography defect was found. The theorem list remains readable, and section/page transitions are sound. All five rendered PNGs are **byte-identical** to corresponding renders of the frozen PDF. Extracted text is identical as well. The PDF's ten URI annotations point to the intended ORCID and primary bibliography destinations, including line-wrapped URLs whose annotations preserve the complete URL. `PDF_QA.json` records page fingerprints and link targets. A compiler timestamp can change PDF bytes; the frozen release hash remains the authoritative file identity.

## 9. Current priority evidence and its limits

After reconstructing the mathematics, I read the broad and focused priority reports, their query/version/fetch/citation ledgers, root priority decision, mathematical reports, and reproduction records. The broad audit's 41 retrieval receipts and 19 search batches are present; its 72-query count is not combined with separate overlapping searches as a global distinct total.

This review issued 19 fresh search strings in five batches, recorded in `QUERY_LEDGER.json`. It also made 32 direct source/history retrieval attempts, all recorded with timestamps, final URLs, hashes, content types, and access failures in `SOURCE_FETCH_RECEIPTS.json`. Search results are bounded and include irrelevant hits; absence from them is not an exhaustive absence proof.

Fresh version checks retain GS arXiv v5 (28 September 2021), ECCC revision 2 (same date), Goldreich R3 (4 October 2021), Fei v2 (12 August 2026), and the listed single arXiv versions of CFP2024, the 2025 polynomial-testing survey, and CSY2026. Relevant current manuscript bodies were fetched. GS's current author copy has different bytes/pagination and was not identified as the journal body. Both publisher landing/PDF requests again returned subscription/cookie HTML. I did not inspect the GS2021 VoR theorem body or assume manuscript identity with it.

The most serious prior-implication routes were checked against primary bodies:

- [GS §5.3](https://arxiv.org/abs/1905.09903v5) supplies a positive transfer under blowup-avoidability. Its full proposition/proof does not give a universal quantitative comparison; the wheel is a checkable failure of the required hypothesis. Non-avoidability by itself gives no lower bound.
- [Goldreich R3](https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf), Theorem 2.3/Corollary 2.4 and Proposition 2.11, supplies one-sided conversion and earlier heavy-center separations. The two-star property is not hereditary (an induced single star fails it), and the conversion does not turn an already easy classical one-sided property into the desired hard side. Its bounded-degree/minor-free positives do not apply to P.
- [Fei v2](https://arxiv.org/abs/2603.22702v2), Definitions 1.2–1.3, Remark 1, §7.1, and §8, concerns arbitrary pair distributions and defaults to samples. Three named queries to the known host triangle in its fixed-host parity family expose the parity, so that specific sample lower bound is not the unrestricted query lower bound here. Product weights also obey four-vertex multiplicative identities that arbitrary pair measures violate. I checked these obstructions directly; they do not rule out every future reduction.
- [AKKR](https://www.math.tau.ac.il/~krivelev/testtria.pdf), Theorem 3 and §6.1, already uses a two-fold parallel/cross parity lift and adaptive simulation. AS04 already supplies the dense two-sided triangle hardness. These older mechanisms are credited, rather than presented as new.
- [GGR, §§10.1.3–10.1.4](https://www.diochnos.com/teaching/CS5970/2020F/project-papers/PropertyTesting.pdf), distinguishes product measures from arbitrary pair measures. Its latter separation does not identify the required vertex-product metric. [Shapira's ICM chapter](https://ems.press/content/book-chapter-files/33311?nt=1), §4.4/Theorem 4.10, gives qualitative weighted-removal existence, not the proposed polynomial comparison.
- [CSY2026](https://arxiv.org/abs/2608.01523), Theorems 5.1 and 6.1, concerns uniform partition/large-induced-substructure testing. A part of size at most one is not extendable, and a fixed fractional-size statement does not encode the one-vertex exception without additional work. CFP's decision-list results and the standard-model partition/removal/separation papers inspected do not supply the weighted bridge. The [graphon definitions](https://arxiv.org/abs/0803.1248v2), §§2.4/3.1–3.2, retain distinct sampled positions; repeated heavy atoms cannot simply be identified while preserving P-completeness, as the doubled wheel demonstrates.

The possible contribution after these credits is the specific fixed property, its easy-classical sandwich, and its quantitative weighted hardness bridge. I found no prior publication packaging the full comparison. This remains a bounded finding. The source package correctly preserves incomplete forward-citation retrieval, unavailable journal bodies, unrecovered original Behrend/RS articles, and unrefereed AI-assisted status. I did not recover those original historical articles in this round or independently audit every unrelated regularity/upper-bound proof in the contextual sources. None is an unacknowledged proof dependency of the operative note.

## 10. Disposition

**PASS; no REQUIRED_REPAIR finding.** The frozen note's universal mathematical claims follow from its own classical and reduction proofs plus the freshly checked established two-sided theorem. The unchanged direct proof provides a separately reconstructed route to its sequence bound. Public controls, manifests, metadata, portable rebuild, and all five PDF pages pass.

Completion: **100% of this assigned whole-package review scope**, not 100% certainty of correctness, historical priority, or eventual peer acceptance. Publication itself was neither performed nor authorized by this review. Subsequent independent review/fix loops remain the parent's responsibility. The pinned assets were unchanged at final check.
