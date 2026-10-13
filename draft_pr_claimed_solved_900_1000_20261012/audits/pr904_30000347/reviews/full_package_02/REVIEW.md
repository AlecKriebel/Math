# Fresh adversarial full-package review 02 — PR #904 / problem 30000347

Completed: 2026-10-13T03:56:27.903927+00:00. Independent initial reconstruction recorded: 2026-10-13T03:46:45.711781+00:00.
Completion estimate: **100% of this assigned review**. This is not a claim of completed publication or proven novelty.

## Verdict

**Mathematics: PASS. Publication package: one minor required repair (R1).** No mathematical error, omitted deletion strategy, source-model substitution or required proof repair was found. The released PDF is readable and matches the standalone LaTeX. The documented normal and optimized outer reproduction commands pass. Metadata and the two intended release payloads align.

The frozen ZIP is not ready for an unqualified no-issue package verdict because its priority report and query log promise two public citation-list artifacts which are absent. This is a precise documentation/reproducibility defect, with no effect on the NP-completeness theorem. Fix R1 and bind a new freeze before publication. This review does not authorize or perform merge/publication.

## Independence and review scope

I first read note.tex and original_packet/frozen_packet/PROOF.md, and wrote a contemporaneous independent deduction under ignored tmp/INITIAL_INDEPENDENT_DEDUCTION.md. Only afterward did I read the supporting proof, computational, source-model and priority-family material. I did not read any full_package_01, full_package_02 or full_package_03 report written by another reviewer. No other agent or individual was contacted; no external communication, shared-file modification, branch operation, staging, push, release or DOI action occurred. All review writes are within the assigned full_package_02 directory. Third-party full sources and rendered source scans are confined to ignored private_sources/.

The exact hypothesis is NP-completeness of the budget language for finite simple undirected graphs, distinct initially connected terminals r,s,t, unit traversal lengths, unrestricted edge deletion, and a nonnegative binary integer budget; each of the three distances must rise by at least one, with disconnection allowed. Hardness is claimed even when every original distance is3 and every deletion cost is1. The rational extension changes deletion costs only. Success requires a total polynomial reduction, all geodesics characterized, arbitrary edge deletions covered in reverse, and a polynomial certificate check. The finite/exact variants additionally require terminal connectivity or exact distances4.

## Independently reconstructed proof

**Subdivision upper bound.** Replace each ordered source edge uv by u-b-c-v with fresh b,c. A Q-cover S extends by c when only u belongs to S, by b when only v belongs, and by either when both belong. Each gadget is covered with exactly one new vertex. Original vertices form A; all b form B; all c form C. No original Q-edge remains, so all three parts are independent. Thus tau(H)<=m+tau(Q), and each nonempty source gadget creates all three cross-part types.

**Subdivision reverse bound.** For an arbitrary H-cover X, S=X intersect V(Q) need not itself cover Q. Every gadget needs one internal vertex for b-c; each Q-edge uncovered by S needs both b,c. If q such edges remain, |X|>=|S|+m+q. Adding one endpoint of each uncovered source edge gives a Q-cover S' with |S'|<=|S|+q<=|X|-m. Repeated endpoint choices only reduce size. This proves the exact identity for nonoptimal covers too, including isolates, disconnected source graphs and m=0. Endpoint orientation is immaterial.

**Complete geodesics.** New terminals are nonadjacent and have disjoint neighborhoods, excluding lengths1 and2. Each cross-part edge creates length3 for its terminal pair. Conversely a three-edge terminal path must use its first terminal's spoke, an H-edge between the two interior vertices, and the second terminal's spoke. No third terminal or third-part detour fits into three edges. Consequently all original geodesics across the three demands are exactly indexed by H-edges. This is a complete family, not a selected subset.

**Spoke upper and reverse bounds.** Deleting spokes corresponding to an H-cover hits every original geodesic. For any blocker F, put each deleted spoke's H-endpoint into X and choose one endpoint of each deleted H-edge. Every deleted edge contributes at most one vertex. Each H-edge uv has geodesic e_u,uv,e_v, which F must hit. Whichever edge is hit contributes u or v to X. Thus X covers every H-edge and |X|<=|F|, even for all-middle deletions or arbitrary spoke/middle mixtures. Equality opt(G_H)=tau(H) follows. Deletion cannot create a shorter path, so hitting all original geodesics is exactly the stated distance-increase criterion.

**Total reduction, counts and binary encoding.** Composition gives opt(G_H)=m+tau(Q), so budget B=m+k preserves both yes and no answers. The reverse construction yields a source cover of size at most |F|-m<=k. For m>=1, the image has n+2m+3 vertices and n+5m edges; the latter is3m+(n+2m). Graph representation is polynomial in the usual explicit vertex/edge input. Binary k is never expanded into vertices or edges, and adding m requires polynomial bit time. For m=0 and k>=0, map to the H-triangle plus three spokes with B=2; this is a valid fixed yes-instance, including empty or single-vertex sources. k=0,m>0 yields a no-instance as expected. Isolated source vertices create harmless spokes and cannot affect cover optima. All image graphs are initially connected and simple.

**NP and rational costs.** An edge-list certificate has polynomial size even for enormous budgets. Breadth-first searches before and after deletion verify every required distance, with unavailable distance represented by infinity. For binary positive rational deletion costs, a common denominator product has bit length bounded by the sum of input denominator bit lengths; the cost sum and exact comparison therefore have polynomial bit complexity. Unit costs are permitted rationals, giving hardness. The reverse extraction is not claimed to preserve arbitrary weighted cover cost, and need not do so.

**Finite and exact3-to4 variants.** Each backup is a fresh four-edge chain with degree2 internal vertices, internally disjoint from the other chains and old graph. A simple terminal path entering a new internal vertex must traverse the whole chain; even concatenating through another terminal cannot create a path of length<=3. The original geodesic family is unchanged. A blocker may delete arbitrary backup edges, but ignoring those deletions still extracts an H-cover no larger than F. Conversely cover-spoke deletions leave every backup intact and force all terminal distances simultaneously to4. Hence the unrestricted, finite and exact variants have the same optimum on the augmented images. The fixed edgeless-source target can be augmented the same way. BFS verifies the extra predicates. Residual connectivity of every vertex is neither proved nor claimed.

No circularity, protected-edge hypothesis, large-cost gadget, hidden directedness or unsupported hardness import was identified. Only classical Vertex Cover NP-completeness is needed externally.

## Primary source and attribution checks

I retrieved the full primary sources afresh. Their URLs, byte counts and hashes are recorded in ignored private_sources/retrieval.json and REVIEW_RESULT.json. The independently retrieved Krause, Poljak, Khachiyan and Karp source hashes match the corresponding recorded retrievals where supplied.

The workshop contribution defines distance by edge count, distinguishes deletion costs, and explicitly asks the three-vertex undirected question. It discusses directed hardness separately. The workshop was6-12 November2005; the publisher records publication30 September2006. [Full report](https://ems.press/content/serial-article-files/46024?nt=1), [publisher record](https://ems.press/journals/owr/articles/1111).

The thesis title/date, graph vocabulary, infinity convention, BSP definition, full Section4.3 and Theorem9.3 were checked. It assumes positive costs and initially connected nonadjacent demands after removing trivialities, allows multicut solutions, and leaves the undirected triangle unclassified while treating directed triangles separately. This matches the theorem's model. [Institutional thesis](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf).

Karp's original image-only printed p94 was rendered and read visually: its Main Theorem includes Node Cover, the same vertex-cover decision condition used here. Publisher metadata confirms1972 and pp85-103. [Original scan](https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf), [publisher metadata](https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9).

Poljak's printed p308 was rendered and read visually: replacing every edge by three edges gives alpha(F)=alpha(G)+m and |V(F)|=|V(G)|+2m. Taking vertex-cover complements gives exactly tau(F)=tau(G)+m. The title, volume15(2), year1974, and pp307-309 are correct. [Primary paper](https://dml.cz/bitstream/handle/10338.dmlcz/105554/CommentatMathUnivCarol_015-1974-2_9.pdf).

Khachiyan et al.'s entire Section6, Theorem11/Claim5, pp226-227, was inspected. It attaches the three parts to u1,u2,u3 on one terminal path, uses zero/one traversal lengths, protected interior vertices and vertex removal. The note accurately credits this antecedent and distinguishes its changed edge-deletion/unit-length/three-demand mechanism. All seven authors, journal volume43, pp204-233, online2007 and issue2008 match the publisher record. [Full primary paper](https://d-nb.info/1239024797/34), [publisher record](https://link.springer.com/article/10.1007/s00224-007-9025-6).

The supporting bounded priority report does not certify first priority. It identifies access gaps for Bienstock-Diaz full text, final Dvorak-Knop text, later shielding material, and sparse citation indexes. The exact question is historically recorded as open; neither the note nor metadata asserts that it stayed open through2026 or that this is the first proof. General length-bounded cut, directed multicut, full multiway disconnection and vertex interdiction are correctly distinguished. I did not treat unsuccessful searches or self-consistent hashes as a novelty theorem.

## Reproduction and adversarial evidence

Safe ZIP inspection found48 unique regular files, no absolute/traversal/symlink members, and47 manifest payloads plus PACKAGE_MANIFEST.json. Extraction occurred into this review's ignored tmp/extracted directory with no network or original workspace dependencies needed by the verifier. Both commands exited0:

```
python3 verify_package.py --pdf /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr904_30000347/publication/output/pdf/note.pdf
python3 -O verify_package.py --pdf /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr904_30000347/publication/output/pdf/note.pdf
```

The ordinary/optimized stdout is byte-identical PASS JSON: problem30000347,47 payload files, separately verified PDF,5 replayed suites, distributed files unchanged. Evidence: ignored tmp/replay_normal.json and replay_optimized.json. Child execution uses -I and omits -O, so PYTHONOPTIMIZE cannot erase its mathematical assertions. Outer and original packet guard functions use explicit exceptions rather than optimizable assertions.

The replayed originals verify their own deterministic counts and frozen manifests. Their recorded exhaustive evidence includes165,952 arbitrary deletion sets over145 small tripartite graphs,89,975 cover extractions,3,375 tripartite(2,2,2) exact optima,1,094 nonempty source graphs through order5, and6,484 budget comparisons. Fresh supporting proof-family checks include2,808 source orientation instances,21,630 budget comparisons,1,718 finite-cover cases and262,144 arbitrary augmented deletion sets. Computational-family checks additionally examine all endpoint choices in small cases and4,096-bit budgets. I inspected the relevant checker implementations: geodesics are obtained from actual adjacency/BFS data, optima from generic exact hitting recurrences or exhaustive vertex covers, and arbitrary deletion feasibility from fresh BFS. These are meaningful consistency tests, not proofs of the universal complexity conclusion.

Fresh outer-package controls written during this review reject18 attacks across ordinary and optimized modes: changed/missing manuscript, unexpected file, byte-identical proof symlink, unsafe manifest entry, malformed manifest, jointly changed original proof/manifest, wrong identity and changed separate PDF. All rejection outputs and executable controls remain under ignored tmp/outer_adversarial_controls.py and outer_adversarial_results.json. The original packet's100 mutation controls and seven optimization/integrity controls also replayed successfully.

A coordinated change to note.tex and its PACKAGE_MANIFEST entry is accepted in both modes, as expected for an unanchored manifest serving as a trust anchor. The original proof additionally has a literal verifier anchor. The README explicitly limits integrity to trusted manifests/verifiers and distinguishes finite checks from mathematical proof. Thus no integrity/authenticity guarantee beyond that boundary is assumed. Raw historical assertion-based checkers can silently lose checks under direct -O; the supported isolated-child wrapper avoids that mode and discloses the limitation.

## PDF, source consistency and publication metadata

Rendered and visually inspected all4 released manuscript pages at140dpi. The title/author/ORCID, mathematics, infinity symbols, equations, theorem/corollary flow, bibliography links and page numbers are readable; no clipping, overlap, missing glyph or black-box defect was seen. Tectonic compilation from the archive's standalone source in a clean temporary directory succeeded. The rebuilt PDF has4 pages and byte-identical extracted text to the released PDF. Its SHA256 differs, as the README correctly allows for generation metadata. Evidence: ignored tmp/pdf_rebuild_results.json and page images.

The outer README, LaTeX/PDF title, package manifest and Zenodo title are `NP-completeness of three-terminal shortest-path blocking`; version1.0 and12 October2026 align. The creator is Alec Kriebel / Kriebel, Alec, independent researcher, ORCID0009-0001-9320-500X. The README licenses authored manuscript/proofs/code/audits under CC BY4.0; metadata uses cc-by-4.0 and excludes third-party reference terms. Extensive AI construction, checking, adversarial review and writing are disclosed. Unrefereed status, absence of independent human/journal review, no first-priority assertion, and no formal proof-assistant certification are clearly stated.

Zenodo lists exactly the frozen PDF under release name three-terminal-shortest-path-blocking-v1.0.pdf and the frozen source ZIP; the manifest's separate PDF size/hash/name agree. The freeze binds note, PDF, ZIP, deposit JSON, README, verifier and bundle manifest. Every bound size/hash matched at start and final recheck. Frozen hashes are copied in REVIEW_RESULT.json.

Archive hygiene inspection found no third-party PDFs, images, HTML/raw source files, raw problem-catalogue report, credential signatures or private account data. The nested authored AUTHOR_FREEZE archive contains the same authored frozen packet, checked by the original verifier; it does not hide source PDFs. Absolute local paths in historical computational receipts are provenance rather than secret credentials. Original pre-audit/status language remains preserved and is expressly superseded by the published note/record.

## R1: required package repair

**Location:** publication/build_package.py line20; distributed reviews/priority_family/PRIORITY_AUDIT.md line61; QUERY_LOG.md line85.

The priority report says title/DOI lists and query endpoints are saved in CITING_KRAUSE.json and CITING_BIENSTOCK.json. The query log says the lists are preserved in public CITING files. Neither file appears among the48 ZIP members or in PACKAGE_MANIFEST.json. The priority-family builder allowlist has only PRIORITY_AUDIT.md, SOURCE_MANIFEST.json and QUERY_LOG.md. This is independently reproduced in ignored tmp/archive_hygiene_results.json.

Both omitted files exist under reviews/priority_family outside the archive. I inspected them: they contain short sanitized query receipts and bibliographic title/DOI/year metadata, with sparse-index limitations. They do not contain full source text, credentials or raw API responses. **Preferred concrete repair:** add both to that allowlist, rebuild the archive and manifests, update its freeze, and audit the resulting new frozen bytes. Alternatively, amend both packaged sentences to explain the lists were local-only and deliberately omitted. Keep original_packet unchanged. No manuscript/proof/metadata change is required for R1.

## Exact residual limitations

There is no identified mathematical proof gap within the stated model. R1 remains the sole required package repair. First bibliographic priority and continued open status remain unverified and are not asserted. AI-only review and finite computation are explicitly disclosed limitations. No claim for planar, bounded-degree, weighted traversal length or globally connected residual graphs follows from this proof. Completion of this review is not publication approval, and its verdict applies only to the frozen hashes recorded here.
