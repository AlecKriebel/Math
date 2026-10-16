# Fresh whole-publication-package adversarial review, round 1

Review completed: 2026-10-13 UTC. Reviewer role: fresh adversarial review of PR #618 / problem 30004609. Completion estimate for this review: 100%. This is an AI-generated internal review, not human peer review.

## Verdict

**PASS in the stated mathematical scope, with no mandatory correction found.** The final manuscript proves the full characteristic-zero low-exponent supersolvability target. Its finite diagnostics are reproducible and are expressly distinguished from the universal proof. The final PDF, ZIP and deposit metadata agree. The prior matching result is acknowledged without a certified-first-priority or independent-development claim.

This conclusion comes from the deductions and checks below, not from the PASS conclusions in earlier reports or from the parent's replay. No candidate, publication artifact, upload package, PR, queue or publication state was modified. No individual was contacted. All review files are confined to this review directory; source fulltexts and render/extraction intermediates are ignored.

## Frozen objects actually reviewed

| Object | Bytes | SHA-256 |
|---|---:|---|
| Final PDF | 69778 | `5a75a8208a1d679939e2f08428d1adae0af9bf877f77473fa0a57240ed0713af` |
| Final LaTeX source | 17414 | `0b944fb495ee1f950bc5d0863a7fe4fd9535ff44b88b7ed61bf815de73a4eaa1` |
| Verification ZIP | 206225 | `d60155726071e3873e7f9101308d9632a092121a93514a0e84122024935a2188` |
| Deposit manifest, `zenodo-deposit.json` | 2217 | `9997281d31f51d84be1f363956b4c8591114e730ff0d6de5c443dd52e5a7f609` |
| ZIP's `PACKAGE_MANIFEST.json` | 11390 | `9c18afdf9f7def1a5fbc420170e490c675a9d18fc66b15cbcf90c6bed506434e` |

The ZIP contains exactly 66 files: its self-excluded manifest and 65 manifested members. Its PDF and source are byte-identical to the publication directory's final files. Initial and final hashes agree; see `REVIEW_INPUT_HASHES.json` and `FINAL_INPUT_RECHECK.json`.

## Exact claim and falsification criteria

Theorem 1, source lines 24–26, concerns a finite set of distinct central hyperplanes over a characteristic-zero field K, with a free logarithmic derivation module. The coefficient degrees of its homogeneous basis may include zero exponents; every positive degree must be 1 or 2 except for at most one 3. The conclusion is a maximal modular chain in the intersection lattice. The review sought a false dimension count, hidden assumption of graphicness or complex coefficients, unproved formality of a deletion, unsupported modularity lift, extra cyclic structure, missed reducible/nonessential case, or source/metadata wording that exceeded the proved scope.

The universal argument uses two established inputs: factorization for free arrangements and free-implies-linear-relation-formality. These are identified, rather than silently replaced by computations. The elementary deductions after them were reconstructed below. An arbitrary-characteristic or multiarrangement theorem is outside the advertised claim.

## Independent reconstruction of every mathematical step

### 1. Reduction and the single exponent 1 (source lines 37–39)

Let C be the common intersection. Every defining form annihilates C, and choosing a complement identifies the arrangement with an essential factor times an empty arrangement. The intersection lattice is unchanged; constant derivations along C supply precisely the removed zero exponents. Rank zero has a one-element lattice. In ranks one and two every atom and the bottom/top elements are modular, so a maximal modular chain exists.

For a product, defining forms belong to direct-sum normal spaces. Its logarithmic derivation module splits by the variable groups, so product freeness and exponent union hold. Its lattice is the product lattice; ranks, meets and joins add componentwise. Interleaving maximal modular chains produces a maximal modular chain. Each irreducible factor inherits the at-most-one-cubic condition. This covers Boolean arrangements, several exponent-1 factors, products involving rank-two pencils, and nonessential ambient spaces.

In an essential factor choose r independent normals as coordinate forms x_i. A degree-1 logarithmic derivation satisfies theta(x_i)=lambda_i x_i because divisibility by x_i forces that diagonal form. Any further normal is an eigenvector: in its nonzero coordinate positions all lambda_i equal. If the diagonal map is nonscalar, the eigenvalue coordinate blocks contain all normals separately and give a genuine product over K itself. Irreducibility therefore forces theta to be a scalar Euler derivation. There are no nonzero constant logarithmic derivations in an essential arrangement. In a free positively graded basis, degree 1 is consequently the K-span of the basis members of degree 1. Its dimension is exactly one. No algebraic closure, chosen spectral decomposition outside K, or theorem about arbitrary deletions is needed. The two listed irreducible exponent multisets follow.

### 2. Relations, connectivity and multiplicity (source lines 41–50)

The normal map K^E to V* is onto in the essential case, hence its kernel R has dimension n−r. A complete rank-two normal flat of m elements has local relation dimension m−2. Since normals are nonzero and pairwise nonproportional, any triple relation has three nonzero coefficients. Distinct complete rank-two flats share at most one element: sharing two independent normals would identify their planes. Linear-relation formality gives the claimed sum of supported local spaces.

If the incidence graph were disconnected, all local relation vectors would be supported inside individual components. Thus any global relation is a sum of component relations. For a sum of vectors from the different component normal spans equal to zero, expand each vector in its own normals; the resulting coefficient tuple is a global relation. Restricting it to each component makes each individual component vector zero. The component spans are a direct sum, hence the arrangement is a product. This contradicts irreducibility and also rules out isolated elements. This connectivity argument uses formality explicitly; bare incidence connectivity is not substituted for matroid connectivity.

For the multiplicity bound, choose forms x,y and rescale each remaining normal to x+c_i y, with distinct nonzero c_i in K. For a homogeneous degree-e logarithmic derivation write theta(x)=xP and theta(y)=yQ, where deg(P),deg(Q)≤e−1. Modulo x+c_i y, tangency gives c_i y(Q−P)=0; since y is coprime to x+c_i y, that linear factor divides P−Q. If m>d+1 for the maximum basis degree d, the m−2 distinct factors have total degree greater than d−1, so P=Q for every free-basis derivation. The x- and y-coefficient rows of the basis matrix would be proportional over the fraction field. A free basis cannot have zero determinant: D contains Q(A) times every coordinate derivation and has full fraction-field rank. This proves m≤d+1. It works with extra ambient variables as well; the multivariable degree bound does not change.

Distinctness is genuinely used in both this divisibility product and the local relation support argument. Repeated hyperplanes cannot be inserted without changing the proof's hypotheses.

### 3. Arithmetic and the tree alternatives (source lines 52–71)

For each complete rank-two flat with m elements, there are binomial(m,2) element pairs and its Möbius contribution to b_2 is m−1. Partitioning every pair by its unique flat yields the defect sum binomial(n,2)−b_2 = sum binomial(m−1,2). Ordinary two-element flats contribute zero.

For degrees (1,2^{r−1}), factorization gives n=2r−1 and b_2=2(r−1)^2, so the defect is r−1. The multiplicity bound permits only triples, yielding u=r−1. The connected incidence graph has 3u edges and n+u vertices, hence beta=2u−n+1=0.

For degrees (1,2^{r−2},3), n=2r and b_2=2r^2−2r−1; the defect is r+1. There are only triples and quadruples, giving u+3v=r+1. Its cycle dimension is 2u+3v−n+1=3−3v. Formality additionally gives r=dim R≤u+2v=r+1−v. Thus v≤1. For v=1, u=r−2 and beta=0; for v=0, u=r+1 and beta=3. All table entries and inequalities check exactly. No other multiplicities or graph components are omitted.

### 4. Minimal dependency forces the core (source lines 74–87)

In the v=0 case, r+1 nonzero triple relations span an r-dimensional space, so a dependent subfamily exists. Choose an inclusion-minimal one T. Every dependency coefficient is nonzero, every proper subfamily is independent, and its relation-vector rank is t−1. Each support element appears at least twice, or its coordinate could not cancel.

The support incidence graph is connected. Otherwise restricting the zero dependency to a component would give a proper dependent subfamily, since all coefficients in that component remain nonzero. There are exactly 3t incidence edges, t line vertices and s element vertices, so its cycle dimension is 2t−s+1. The cycle space of a subgraph injects into that of the whole graph, giving 2t−s+1≤3; counting support degrees gives s≤3t/2. These imply t≤4 (for t=5 the lower cycle dimension is already at least 4).

Conversely, each of a triple's three elements must occur in another selected triple, and another rich line cannot cover two of those elements. Therefore t−1≥3. Hence t=4. The two bounds force s=6 and every support element has degree exactly two. Each of the three other triples meets a chosen triple at its own distinct element. The six elements can therefore be indexed by the six pairs of four triples, giving precisely the subdivision of K4 with stars as rich triples. No graph-realization assumption has been made.

The core's cycle dimension is three. Contracting all its edges decreases edges and vertices so that the quotient cycle dimension is beta(G)−beta(core)=0. A connected multigraph of cycle dimension zero is a tree: loops, parallel pairs and additional connections between core vertices would add cycles. Thus every external component attaches at exactly one core vertex. A core triple already has all three of its incidence edges present, so attachment is only at an element vertex. This excludes hidden extra core triples and multiple attachment points.

### 5. Terminal-pencil deletion and modularity (source lines 90–106)

Write L={a,p_1,...,p_{m−1}}, and suppose every removed p_i belongs to no other rich line. All other local relation spaces lie in K^{E'}, where E' retains a. Formality gives R=R_L+S. The intersection R_L intersect K^{E'} is zero: a relation there would be supported only on the single nonzero normal a. The sum is direct, and restricting relations to E' yields exactly R'=S. The other rich lines remain unchanged because they contain none of the removed elements. Deletion formality is proved here, not assumed from freeness or from an arbitrary-localization claim.

The relation dimension drops by m−2 while the element count drops by m−1, so the normal rank drops by one. Put W=span(E') and U=span(L). The full span is W+U, with dim U=2, dim W=r−1 and total dimension r. Therefore U intersect W=Ka. Since removed elements are not proportional to a, none lies in W, and E' is exactly a represented flat and a coatom.

For any flat F select a generating set of normals. With at most one generator outside W, its nonzero quotient image forces F intersect W to equal the span of the inside generators. With at least two outside generators, the pair spans U by distinctness, and F=span(inside)+U. Its intersection with W is span(inside,a). Both cases are spanned by represented normals. The matroid join has vector-space dimension dim(W+F), while the meet is the span of common represented elements. Therefore a represented vector-space intersection is exactly the modular rank equality. This proves W is modular.

If C is modular in W, then for a full flat F the intersection W intersect F is a flat of the retained configuration. Consequently C intersect F=C intersect(W intersect F) is represented. C is globally modular. A maximal modular chain in W, followed by the full span, is a maximal modular chain in the original configuration. This verifies the lifting claim even when the base arrangement is not free.

### 6. Pruning termination and the rank-three chain (source lines 109–115)

In a finite incidence tree rooted at a rich line, a nonroot line vertex farthest from the root has its two outward element neighbors as leaves. It is a terminal triple, so the proved lemma applies. Deleting the two leaves and their now-redundant line vertex leaves the retained incidence tree. Iterate until the chosen root pencil remains. In the unique-fourfold tree choose that fourfold root; it is not prematurely removed. The terminal lemma also covers m=4, but the proof needs only triple removals before the final rank-two pencil.

In the cyclic case, the same farthest-line argument applies in the attached trees rooted toward the core. It never deletes a core element. All formality assertions are maintained by the terminal lemma. When only the core remains, its four local relation vectors have rank three by minimality, and they span all retained relations by inherited formality. Hence its normal rank is 6−3=3. Any original line outside the core had at most one core element by the quotient-tree argument, so none supplies an extra core rich line. Deleting points does not create collinearity.

Fix a star L_i. The other three rich triples meet its plane in their represented common element; their planes are distinct. Any remaining rank-two flat is an ordinary pair of disjoint indexing edges, because adjacent edges lie in a star triple. A disjoint pair covers all four indexing vertices, so exactly one member is in L_i. Its plane is distinct from span(L_i), and in the rank-three ambient span its intersection with span(L_i) is that represented one-dimensional direction. Thus L_i meets every rank-two flat in a represented point. Ranks zero, one and three give represented intersections immediately. L_i is modular; every atom is modular, giving the four-term maximal chain. Reverse each modular extension, then form products and undo essentialization. This proves the theorem in every allowed rank.

The free non-Fano example with degrees (1,3,3) lies outside the single-cubic hypothesis. The exact lattice diagnostics find no modular coatom, and its exact Saito certificate checks the claimed free degrees. It is a legitimate boundary illustration, not a counterexample to the theorem.

## Field scope and source/priority audit

The original target was checked against the actual [OWR 5/2021 PDF](https://ems.press/content/serial-article-files/46883), including visual inspection of printed pp. 283–284. The setting is a characteristic-zero field, and the next page states the low-exponent conjecture. The paper's positive-exponent formulation incorporates essentialization and products correctly.

[Yuzvinsky's primary AMS paper](https://www.ams.org/journals/tran/1993-335-01/S0002-9947-1993-1089421-5/S0002-9947-1993-1089421-5.pdf) was independently retrieved and its printed p. 236 visually checked: Corollary 2.5 supplies free-implies-formal for rank at least three, with arbitrary-field definitions. Thus the present characteristic-zero field scope is not accidentally restricted to C. Factorization is a standard identified input with the correct [Terao publication metadata](https://link.springer.com/article/10.1007/BF01389197). The original paywalled Terao fulltext was not obtained; its use is not a new or disputed assumption. Even a complex-only formulation suffices for arbitrary characteristic-zero K by descending finitely many normal/basis coefficients to a finitely generated characteristic-zero subfield, embedding it in C, and preserving ranks, Saito determinant identities and exponents. Every subsequent proof operation is explicitly K-linear.

The [v4 withdrawal notice](https://arxiv.org/abs/1707.07091v4) identifies the two caveats accurately described at source line 28: incomplete hand enumeration and the factor-size inference. Independently fetched v1 and v3 show that the all-1/2 theorem, modular terminal-triple construction and numerical counts are antecedents. The final proof uses neither affected argument. Its pruning lemma and multiplicity bound were checked directly above.

[DiPasquale v1](https://arxiv.org/pdf/1806.05295v1), Corollary 4.10 and Proposition 6.1, were checked against their actual definitions. The two tree cases have direct local relation sums. The source map remains injective on every localization's rank-two local spaces; higher relation kernels consequently vanish recursively. Freeness supplies total formality. Thus they satisfy TF2 and lie within the predecessor theorem. The cyclic case has a nonzero local-relation kernel and escapes TF2. The manuscript uses explicit arXiv numbering and does not silently assert that journal numbering was inspected.

The actual [DGT v1](https://arxiv.org/pdf/1211.4562v1) Theorems 5.6 and 5.11 require line-closedness/tree or quadratic-complete-intersection structure; the paper credits their prior tree/parallel-connection mechanism without illicitly importing those hypotheses. The actual [quadratic-classification v2](https://arxiv.org/pdf/1405.2122v2) Theorem 2.4 matches the credited rank-three precursor. The supplementary priority report's additional source boundaries were spot-checked in independently downloaded primary fulltexts: Le–Römer's complete-intersection hypothesis; Le–Mohammadi's relation-subideal theorem; Schenck–Tohăneanu's K4 relations; Möller–Mücksch–Röhrle's modular localization result; DiPasquale–Sidman–Traves' rank-three classification discussion; and Liang–Wang's regular-matroid hypothesis. None was found to be falsely represented as resolving the cyclic target without its additional mechanism. Source URLs, hashes and retrieval records are in `SOURCE_RETRIEVAL.json`.

Ferudun's [version 1.1](https://doi.org/10.5281/zenodo.23313624) was independently downloaded from Zenodo; its SHA matches the inspected source ledger. Theorem 1.1 is the same full target; Lemma 4.3 uses cancellation on dependency supports followed by a count of terminal elements outside the support, and Theorem 5.2 completes induction. The final manuscript accurately compares that leaf-count mechanism with its cycle-space forcing. This is substantial mathematical overlap, properly credited.

Fresh anonymous GitHub API reads confirm PR creation `2026-10-04T16:19:57Z`, current unchanged head `cae273cb692bde0a0a73790c3840af8c7eb1eed7`, and current public visibility. The frozen proof's Git blob has SHA `73716fdb49896b2443ada06ed707dba1e0d08f304d9e563cf251c949d8752798`, exactly the archive's copy. Fresh Zenodo API reads confirm creation `2026-10-12T00:39:41.612424+00:00` for 23307000 and `2026-10-12T09:20:42.830800+00:00` for 23313624. The paper states these bounded records and explicitly leaves historical visibility, exhaustive first priority and independent development uncertified. That is a defensible framing.

## Archive, reproducibility, metadata and visual checks

- Every ZIP entry was checked for canonical relative paths, traversal, duplicate names and symlinks before safe extraction. The exact inventory and all 65 checksums pass. The nested original `author.zip` has only its eight authored original files, with matching hashes; it contains no hidden source PDF.
- The stipulated Python at `/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python` ran the complete strict `verify_package.py` successfully. `STRICT_REPLAY.stdout.json` records original-candidate replay, fresh incidence/non-Fano comparison, byte-identical algebra replay and final original-packet integrity. Pinned SymPy 1.14.0 and mpmath 1.3.0 are documented. This was an actual replay, not inference from stored results.
- Four isolated integrity attacks—extra file, missing file, changed byte and symlink—were each rejected. Their receipts are `STRICT_INTEGRITY_ATTACKS.json`. No attack touched the reviewed input.
- Supporting scripts were inspected for what their assertions prove. Exact ranks, local relations, flats and modularity use rational/symbolic arithmetic. The algebra checker solves homogeneous tangency equations before finding Saito bases; the non-Fano and withdrawal checks validate tangency and determinant identities. The support/pool enumeration is finite and is labeled accordingly. No finite enumeration is used to bridge an all-rank gap.
- All five deposited PDF pages were visually inspected at 120 dpi. The statement, equations, count table, core argument, lemma, completion and references are complete and legible; no clipping, overlap, missing glyphs or dangling reference was found. Bibliographic line wrapping is harmless.
- The standalone LaTeX source compiled in a separate temporary output directory. Rebuilt and deposited PDF text with layout extraction are byte-identical. The rebuilt PDF differs only at the byte/hash level as anticipated by the timestamp warning. Two underfull bibliography warnings do not create a visual defect. See `SOURCE_REPRODUCTION.json`.
- Current README and priority note clearly supersede the dated frozen candidate's pending-review and novelty assertions. The original artifacts are not rewritten to make anachronistic claims. The standalone candidate verifier correctly reports that the historical sibling queue is absent; no current queue validation is falsely inferred from this.
- Deposit title, author/ORCID, date (13 October 2026), version, characteristic-zero scope, single-cubic boundary, AI/unrefereed disclosure, Ferudun acknowledgment and two upload filenames match the paper/package. CC BY 4.0 is stated for original authored work.
- The complete and nested inventories contain authored material, metadata, code, the author's PDF/source and the original authored ZIP. They contain no third-party scholarly fulltexts, local environment, private-source corpus or credential/key signatures. Public commit-author contact metadata is public chronology evidence, not an outreach draft. Fulltext downloads for this review remain only in ignored `sources.private/`; renders/extractions remain in ignored `tmp/`.

## Mandatory fixes

**None found.** No required mathematical, source-attribution, publication-disclosure, visual-layout, metadata or package-reproducibility change is assigned.

## Optional polish, explicitly nonblocking

1. `publication/PACKAGE_README.md:24` (ZIP `README.md:24`): the short source-build example uses Tectonic's default output location. A reader who recompiles directly inside the strict packet will overwrite the frozen PDF and invalidate its inventory. The same paragraph already warns about nonidentical compilation hashes, so this does not invalidate the supplied replay instructions. For clarity, use `tectonic --outdir ../low-exponent-pdf-build low_exponent_supersolvability.tex`, first creating that external directory, or recommend a separate copied source directory. Our separate-directory compilation succeeded.
2. `publication/low_exponent_supersolvability.tex:111`: the statement that the core's rich lines are exactly four is correct together with line 87. One explicit sentence that every noncore rich line contains at most one core element would make the absence of extra surviving lines easier to see. The quotient-tree argument already supplies that fact; this is explanatory polish, not a missing lemma.

## Strongest verified result and exact remaining gap

The strongest verified mathematical result is the complete Theorem 1 in its stated characteristic-zero, finite-distinct-central-free scope, including all ranks, products and nonessential arrangements. The actual publication package is reproducible and internally consistent at the hashes above. No mathematical gap was found. This is a standard proof audit with exact supporting computations, not a proof-assistant certificate or human peer review.

The remaining limitations are epistemic and procedural: historical visibility and exhaustive priority are not certified, and the requested second fresh sequential whole-package adversarial review has not been performed by this reviewer. This PASS alone does not authorize publication or substitute for that next review. Any later material change must be assessed against new frozen hashes.
