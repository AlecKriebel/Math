# Fresh adversarial package review 01: PR #1001

Reviewed pinned proposal: **Full stress stratifications determine a labelled graph**, problem 6900004; submitted PR head `f333d06cc161b1b8ae8422bf413ed1ffae31e614`.

Verdict: **the mathematical theorem, original-source literal framing, known-ingredient credit, executable verification, metadata consistency, package hashes and PDF layout pass. One low-priority public-package navigation issue should be repaired before final publication.** No mathematical blocker, unsupported universal step or incorrect source-credit claim was found. The present gate truthfully remains pending; it must close only after fixes and a new fresh review.

## Review independence and pinned inputs

`INPUT_PINS.json` pins all 32 substantive input files at review opening. The TeX proof was read first. `INDEPENDENT_DERIVATION.md` records the reviewer's own derivation before comparison with previous mathematical and priority reports or their verdicts. The current supplement already describes proof mechanisms and credit claims, so this is an independent adversarial verification rather than blind discovery. Earlier PASS verdicts were never treated as evidence of correctness. After the derivation, previous reports were read to test consistency and remaining limitations.

No package file, original PR artifact, shared branch, GitHub state, deposit or tracker was changed. All new material is confined to this review directory. No individual or unrelated shard was contacted.

## Universal theorem and attempts to falsify it

The accepted claim is exact equality of connected coordinate-sign partitions of the common labelled full base `(R^d)^n`, for simple graphs on `[n]` and n,d>=1. It includes collisions and deficient affine span. It does not compare stress fibres of distinct graphs directly.

For a present edge ij, a vector positive only at coordinate ij satisfies equilibrium exactly when its endpoints coincide. A sign-preserving homeomorphism is bijective and preserves existence of this sign pattern in both directions. Therefore collision-diagonal membership is constant on every entire equivalence class, which makes the diagonal a union of connected strata.

For a missing edge, the chosen moving scalar vertex is t, the other endpoint is 0, and every remaining scalar is a distinct fixed value >=2. Actual graph edges stay noncollapsed throughout [-1/2,1/2]. At collinear configurations the vector equilibrium equations are exactly B D_t w=0, since the direction vector is nonzero. T_t=D_t^(-1)D_0 is positive, invertible, and satisfies B D_t T_t=B D_0. Its inverse proves surjectivity; orientation reversal cancels in each ratio. Positive diagonal multiplication preserves negative, positive and zero coordinates, rather than merely support dimensions.

The full continuous configuration path is in one equivalence class. The image of an interval is connected in the class's subspace topology, and every connected subset lies in a connected component. This is the required topological step. Endpoint equivalence alone is insufficient but is not what the proof uses. At t=0 and t=1/4 the path is respectively inside and outside the missing pair's diagonal, so that diagonal cannot be a union of whole strata.

The criterion reconstructs the edge set from the actual subsets constituting the full partition. It handles empty graphs, zero fibres, isolated vertices, disconnected graphs and n=1/n=2. It requires positive d and a simple graph. Loops, parallel edges and deleted-collision domains would permit counterexamples to the extension, and none is claimed. A homeomorphism that merely preserves dimension cannot replace coordinate-sign equivalence; K3's equal-dimensional fibres with different singleton support demonstrate this boundary.

The path/star example is correct in every positive dimension. Leaf elimination proves that a forest's stress fibre is exactly the coordinate space supported on collapsed edges, including configurations with several collapsed edges. The stated linear change matches the three edge differences and has the inverse displayed in the supplement. It therefore maps equivalence classes and their connected components bijectively. The degree multisets distinguish the trees. This is a valid counterexample to treating arbitrary ambient-linear equivalence as literal partition equality, and it confirms why the scope must remain prominent.

## Primary-source fidelity and credit

Freshly retrieved original-paper bodies are recorded in `SOURCE_RETRIEVAL.json`, with SHA-256 hashes. Journal pp.20-22 of [Karpenkov 2018](https://armj.math.stonybrook.edu/pdf-Springer-final/018-0080.pdf) were rendered and inspected completely. The positive dimension, simple graphs, full labelled Cartesian base and connected sign-strata definitions agree with the manuscript. The nearby examples include collisions. Problem 4 does not separately define a cross-graph equivalence, but its combinatorial context leaves intended meaning uncertain. The paper consistently identifies its answer as literal equality and explicitly retains that semantic reservation.

[Doray-Karpenkov-Schepers v2](https://arxiv.org/pdf/0806.4976v2) confirms symmetric stresses and zero nonedge coordinates, so reducing redundant stress arrays to unordered-edge coordinates preserves the source's data. The exact singleton detector is already [Panina v4](https://arxiv.org/pdf/1902.07212v4), Section 3 Lemma 4. Her actual published body mirror confirms Lemma 3.1 and Appendix A.3 numbering; these are accurately credited. The manuscript does not substitute her noncollapsed/affine-quotient domain for its full base. The incidence-normalization statement also appears in the [Clay-Jordan-Toth author paper](https://arxiv.org/pdf/2410.07452), Section 2.

The existing priority report and 54-query log were checked for claim consistency, explicit body-access limits and overclaiming. Three additional exact-question/reconstruction/incidence queries found no exact competing theorem; this small fresh batch adds no exhaustive originality guarantee. The final KSS body, final handbook chapter, terminology/all-language coverage and author intention remain explicit limits. No unexplained claim of first priority for established ingredients or definitive novelty certification appears in the preprint or metadata.

## Execution and independent boundary checks

All three included programs and `run_checks.py` were read before execution. They use standard-library exact rational arithmetic and explicit guards. The runner confines mutants to a temporary directory and writes the requested receipt only in this review directory; its isolated interpreter flags are correctly not called a security sandbox.

Fresh execution reproduced **9 baselines**: all three included checkers in normal, -O and -OO modes. Every mathematical JSON field matched its pinned reference; UID and optimization were explicitly separated. All **18 actual altered-source runs**, six mutations in three modes, failed with the exact expected mathematical reason, exit code 1 and empty stderr. Thus syntax errors or unrelated exceptions cannot satisfy the advertised control. `FRESH_PACKAGE_REPRODUCTION.json` retains the full raw receipt.

My additional `independent_boundary_check.py` imports none of the package code. It checks every graph through n=4, every labelled forest through n=5, every vertex-collision partition, and curved rational placements in dimensions two and three. It verifies 102,604 singleton multi-collision cases and 31,484 forest full-kernel dimensions. Thirty additional noncollinear path/star inverse and edge-difference checks pass. These finite diagnostics test broader multiple-collision configurations; the written proof, not enumeration, supplies universality and connectedness.

## Archive, exact metadata and visual inspection

All 29 manifest payload entries match their byte lengths and SHA-256 hashes. The ZIP contains exactly those files plus the manifest: 30 entries, no duplicates, no unsafe paths, successful CRC test and byte-identical extracted contents. No third-party paper is redistributed. Metadata in `metadata.json` and `zenodo-deposit.json` is structurally identical, including title, author, ORCID, scope-qualified description, version, date, license and references. Upload paths point to the inspected PDF and ZIP.

All three PDF pages were freshly rendered at 115 dpi and visually inspected. Text, equations, theorem, proof, comparison example, source credit, references and author footnote are readable with no clipping, overlap, missing glyphs or overfull material. The page break between the path/star formula and its explanation is legible. The PDF explicitly discloses extensive AI use, unrefereed status and AI review rather than conventional human peer review. Its claims agree with the TeX, supplement, README and metadata.

## Actionable issue PKG01-1 (low priority / P3)

The copied historical evidence retains nonportable locations without a public relocation index. `evidence/SOURCE_SCOPE_RECONCILIATION.md:22` links machine-local extraction and `SOURCE_RETRIEVAL.json` paths; the archive's included retrieval record is `evidence/ORIGINAL_SOURCE_RETRIEVAL.json`. Its line 34 links historical submitted sources outside the ZIP. `evidence/PRIORITY_AUDIT.md:62` names `QUERY_LOG.md` and `SOURCE_AUDIT.json`, whereas the public equivalents have `PRIORITY_` prefixes. `evidence/ROOT_MATH_AUDIT.md:83` points to a nonbundled `root_reproduction/` directory. These are truthful stage-specific historical references, not a proof or provenance defect. Nevertheless, a reader of the standalone public archive cannot navigate them as presented.

**Repair:** add an authored evidence provenance/relocation index, linked from README and supplement, with package-relative links to included reports, JSON verdicts, retrieval records, checker sources and receipts. Distinguish omitted primary-source PDFs/extractions and original submitted files from included counterparts, using primary URLs and pinned GitHub-commit references for external originals. Preserve the historical reports and pin files byte-for-byte; do not silently rewrite provenance. Regenerate the manifest and ZIP after the addition.

Acceptance check: every included historical report/check/receipt can be located from the index, while omitted paths are clearly marked historical/local-only and no longer presented as bundled public files. This requires no change to the proof or the scientific metadata claim.

## Final publication disposition

The proof and scope-qualified result are sound on this review. Repair PKG01-1, incorporate final review evidence, regenerate the archive/hashes and obtain the new fresh adversarial review required by the user's loop. Only after that review is clean should the pending publication gate be closed. The mathematically accepted result remains **literal equality of full fixed-labelled connected coordinate-sign partitions, with collisions retained**, with known ingredients credited and extensive-AI/unrefereed disclosure. There is no basis here to upgrade it to an ambient/abstract classification, certify the original author's intention or assert exhaustive novelty.

Review checkpoint: **100% of this fresh package review completed**; final publication is conditional on the single low-priority repair and completion of the requested fresh-review gate.
