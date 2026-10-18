# Whole-package adversarial review, round 2

**PASS for the exact, attributed historical-counterexample note. No mathematical, attribution, provenance, reproducibility, metadata or presentation defect requiring a correction was found in the reviewed bytes.** This is a fresh candidate-aware internal AI review; it establishes neither discovery independence nor historical priority. The bounded assignment is complete (100%).

All writes and executable corruptions were confined to this review directory. No candidate, original frozen record, Git object/ref/index, PR, release, Zenodo record, tracker, or outside individual was changed or contacted. The publication scripts were read, not run. Disk pressure caused two transient write/render failures; retrying a small owned extraction succeeded. Temporary page images and the restored corruption copy were removed after use. The actual publication PDF was fully rendered and visually inspected before those images were removed.

## Exact binding and scope

| Object | Bytes | SHA-256 |
| --- | ---: | --- |
| Tree_Five_List_Note_v1.0.pdf | 52194 | `2b98b7f4129114bf98434ae285a67736976cb4aa3d49b56298c2ee7fec5c6f6f` |
| Tree_Five_List_Verification_v1.0.zip | 132313 | `65cf534be55648b0d501a3af2834b8397f8f18e8680804ba96f7d405876c3cbb` |
| manuscript/main.tex | 9402 | `4202d9c50e4be6677fded9db501658df62491ee9ef5b0e79d0cccaa751d0a11c` |

`CANDIDATE_BINDINGS.json` also pins the build receipt, deposit metadata and two future-action scripts. The root archive manifest hash is `3d4efc6ee77dc0eacdfe937c55b60905598dbbf3d13a0c790b819b282bc3b6b4`. These bindings were checked again after all review work.

The accepted claim uses positive-integer labels, edge difference at least two, and unequal labels at graph distance exactly two. The ordinary parameter uses the common initial segment [k], rather than any spaced k-element set. The explicit eleven-vertex tree has ordinary palette minimum 5, zero-based span 4, and arbitrary-list parameter 6. Independently chosen finite nonnegative lengths at all six original leaves, with one outward disjoint path per leaf, preserve both exact values. Its incompatibility with the equality printed by Kohl in 2006 is accepted. Firstness, present openness, minimal order, new mechanism, exhaustive literature coverage, external peer review and formal certification are outside acceptance and expressly unclaimed.

## Mathematical falsification review

The graph has the spine a-b-c-d-e, two leaves at each end, and one at b and d. It is connected and acyclic, with 11 vertices, 10 edges, maximum degree 3, radius 3 and diameter 6. The only bad-list exception is B={1,3,4,5,6} at a1,a2,e1,e2; all others receive A=[5].

At b and d, all three neighbors have A and must receive distinct labels. Center values 2,3,4 leave only two available A values, so b,d are in {1,5}. Their distance-two relation forces different endpoints. The spine reflection preserves the graph AND the assigned lists, so assuming b=1,d=5 is legitimate; no invalid label-complement symmetry is used. Adjacency forces c=3. Then a belongs to {4,5}. For a=4, each outer B leaf can use only 6 after excluding b=1; for a=5, each can use only 3. The sibling leaves cannot be distinct, proving infeasibility.

The ordinary witness is valid on every edge and pair of neighbors. With [4], a degree-three center has at most two possible neighbor values, contradicting their required distinctness. Therefore the ordinary value is exactly 5. A bad five-list assignment implies list value at least 6: any universal smaller-list guarantee would extend to five-lists by choosing sublists.

The self-contained universal upper bound is valid. In breadth-first order, the only earlier neighbor of a nonroot vertex is its parent, excluding at most three integers. Earlier distance-two vertices are the grandparent, when present, and earlier siblings, altogether at most deg(parent)-1 <= Delta-1. Overlap among forbidden values can only help. Thus at most Delta+2 list entries are excluded; Delta+3 suffice. The root and singleton have no earlier constraints. Delta=1, root-parent cases and first/last siblings do not create a negative-count exception. The subcubic instance consequently has list value at most 6. This proof establishes every six-list assignment, without a sampling inference.

For each appended path, even its first new vertex has only its parent and grandparent already labeled within distance two. They exclude at most four values of [5], so extension always proceeds. New vertices on distinct appended paths are separated by at least four edges. The old induced subtree retains all old distances and its degree-three vertices; no vertex degree exceeds three. Restriction gives the ordinary lower bound and inherited bad-five-list lower bound, while the universal tree bound gives six. All-zero lengths are included. Making a single path longer gives unbounded diameter. The analytic proof covers every length vector; the numerical checks below are corroboration.

The supplementary recurrence is also correct after its explicit guard. A state (v,p,q) first requires q in L(v), and at a nonroot p in the actual parent's list and |p-q|>=2. Invalid states are false even at a leaf. For a valid state, each child root must have a feasible child state, avoid p, and differ from the other child roots. Child roots are the only vertices in different child subtrees within distance two, so an SDR is necessary and sufficient by induction. The main obstruction uses no recurrence. My separate Cartesian crosscheck covered 4,578 local states on 45 seeded small trees, including 2,842 locally invalid leaf states; all agree.

Rank compression has the correct one-way implication. For sorted distinct integer union labels x_i, x_j-x_i >= j-i. Every compressed solution therefore lifts; hence a bad original compresses to a bad instance on at most nk positive labels. Original feasibility need not survive compression, as edge lists {1},{3} becoming {1},{2} show. I checked lifting in all 1,728 combinations of a labeled three-vertex simple graph and two-element lists drawn from {1,3,4,7}. No exhaustive nk-universe claim is made for this specimen or other trees.

## Executable reproduction and corruption controls

The ZIP was freshly extracted here. Root `replay.py` authenticated 60 members and exactly matched its freshly generated output against expected results. Direct primary `verify.py` passed under both -O and -OO; root replay invokes the ordinary primary mode. The primary's mathematical checks use explicit exceptions, and its current output is 4,498 bytes with SHA-256 `206e0c6e60d010f3dc1e863baf218a2391f21283d37d8f5af9b7ebf882ac2234`.

The optional frozen construction-input replay passed in ordinary Python. Its assertions are preserved, and the root README explicitly excludes optimized -O/-OO support for this optional historical family. It is not silently treated as optimized certification. All original six-member freeze bytes were preserved. The information-boundary receipt accurately limits the claim to supplied-construction reconstruction, including topic cues, without expected numerical answers or candidate-proof access. Hashes authenticate that receipt's bytes; they do not independently prove every historical information-flow assertion.

My new `independent_review.py` imports no candidate solver. It enumerates spine labels and eliminates the attached leaf stars exactly, reproducing counts 0,0,0,0,8,6336 for common palettes 1 through 6 and zero for the bad lists. It checks all 729 independent length vectors in {0,1,2}^6 using direct all-pair distance validation, in addition to the recurrence and rank tests. This is a new implementation of a factorization also described in historical support, not a new method or discovery claim.

Six actual corruption cases were executed in a disposable extraction. Changed tree endpoints, a changed five-list, an edge-colliding ordinary witness and altered count metadata were rejected by the real primary under -O. A same-size change to verifier bytes reached the digest rejection. More strongly, the expected ordinary-five solution count was changed to 9 AND its member size/hash were updated in the root manifest; root replay still rejected the freshly computed mismatch. This exercises its mathematical result comparison beyond mere status flags or stale expected output. Restoring all bytes made replay pass again. `INDEPENDENT_CHECKS.json` records exact rejection reasons and the restored success.

## Archive and provenance bindings

The archive contains exactly 61 unique paths: root manifest plus its exact 60-member inventory, with no extra or missing archived payload. Every byte count and digest matches. The embedded and external TeX sources agree. `PACKAGE_BINDINGS.json` records all nested checks:

- Every one of the eight current corrected files equals both the live repair edition and CURRENT_EDITION_BINDINGS.json.
- The corrected manifest's seven nonself records and complete eight-name inventory are consistent. Its own hash is `5cbe8ab44417569fb85d9124f393493f997b7795ae2ebab106c4cc052d8e8a9a`.
- All three current-document bindings inside ACCEPTANCE.json match.
- The construction-input freeze has six matching artifacts and a matching external manifest pin.
- The independent priority freeze has 15 matching files; the adversarial priority freeze has eight.
- All three PRIORITY_ADJUDICATION.json evidence bindings match.
- Packaged construction-input and priority histories equal their frozen original files, including logs and results.

Historical scripts/certificates/source inspections are explicitly identified as historical in the corrected support. The current archive offers a separately runnable finite verification package. Missing raw historical Hall/state tables and third-party scholarly bodies are disclosed rather than falsely promised. Research-local filenames in old receipts need not exist inside the portable archive. No retrieved scholarly body or source-author implementation is distributed or executed by this review.

## Primary sources and attribution

I independently streamed the three public primary PDFs and matched their hashes to the retained input PDFs without saving duplicate bodies. `SOURCE_CHECKS.json` records URLs, byte sizes, fresh hashes and equality:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| OWR7/2006 | 776202 | `720ad8b58092744bb37446dd53a02d9e31dc1caf8eee3b27ad0ad52ff96bbd15` |
| Kohl dissertation | 1275437 | `ae2d73fcf89ba4d36925d18ff492958149c1ce9d82e1a2b2a5513a1f67433828` |
| Fiala–Škrekovski2001 | 246202 | `3a6820ddad634ee58f4fc6810518f824148abf39abc7217ece5370787fee421f` |

The [OWR primary](https://ems.press/content/serial-article-files/46037?nt=1), printed414–417, agrees with the arbitrary-list definition, common initial-segment convention, and Conjecture4 on416. The same page expressly attributes the general tree bound to Voigt through reference8 on417. The note credits this bound and includes its own elementary proof; it does not promote that proof to novelty.

The [dissertation](https://webdoc.sub.gwdg.de/ebook/dissts/Freiberg/Kohl2006.pdf), printed124, defines chi=lambda+1 and states the same tree equality as Conjecture4.4. Its nearby broader path/cycle Conjecture4.3 is a different assertion. I read the relevant source text, visually inspected124, and separately extracted the complete129–130 boundary pages. The proved comet and caterpillar cases exclude this radius3/Delta3 tree; the caterpillar alternatives require Delta4,5,or>=6 and stated separations. No contrary earlier theorem is assumed false to obtain this example. The [official institutional record](https://tubaf.qucosa.de/id/qucosa%3A22568) independently confirms the2006 defense and16December2009 Qucosa publication date. The note distinguishes those dates.

I visually inspected the full [Fiala–Škrekovski preprint](https://kam.mff.cuni.cz/kamserie/clanky/2001/s530.pdf), printed14/Fig4, and wrote a separate fixed-order search using BFS distances on my own transcription. The ten-vertex/twelve-edge figure has cycles, an ordinary five-palette witness and bad five-lists. My `fiala_check.py` confirms those statements and all66 connected spanning trees have feasible inherited displayed lists, with explicit witnesses in `FIALA_CHECKS.json`. This rules out only direct deletion transfer of those lists. It does not rule out other old lists, gadgets, countertrees or stronger results. The [institutional KAM index](https://www.mff.cuni.cz/cs/kam/vyzkum/kam-dimatia-series) identifies the2001 preprint. The inspected primary is not silently identified with the differently titled2005 journal body.

Both frozen priority reports, their source-access gaps, and the cross-challenge remain bounded. The final Fiala2005 body, full TCS2005 paper, Chen/Kuo/Jonas/Waters material, later tightness constructions, and other unlocated literature are not cleared by this round. No exhaustive fresh priority search was attempted. Those gaps block firstness or current-openness certification, not the explicit elementary theorem. The manuscript and deposit description preserve that distinction and credit the earlier cyclic obstruction.

## PDF and deposit consistency

The actual three-page PDF was rendered at1100-pixel scale and all pages were visually inspected. Equations, the witness table, proof continuations, citations, references, margins and page numbering are legible; there is no clipping, overlap or missing glyph. The proof's page break and the verification paragraph continuation are normal. Extracted PDF text agrees substantively with the pinned TeX source. No recompilation is necessary to review the delivered bytes; the pinned successful compile receipt also binds their source and PDF hashes.

The title, author, ORCID, date, version1.0, preprint type, filenames and mathematical statements agree across manuscript, deposit metadata and package README. Authored content's CC BY4.0 statement retains source attribution and historical metadata. Extensive AI assistance, internal AI checks, unrefereed status, absence of outside human peer review and absence of formal proof-assistant certification are clear. The internal mathematical acceptance is not mislabeled journal acceptance. The Zenodo files are still a candidate; this review makes no publication-status claim.

## Global scope of the future PR/tracker plan

`publication/update_pr_publication.py` and `publication/append_tracker.py` were inspected statically; neither was imported or run. Their exact hashes are in `CANDIDATE_BINDINGS.json`.

The PR updater requires main to remain checked out; it builds a commit with Git objects against the pinned original PR head and uses the pinned problem path. It checks open/head/body bindings, the review gate, published artifact hashes/sizes, tracker readback, and exact equality of the eight repaired files with the reviewed archive. Its intended diff has exactly13 problem-local paths: eight corrected files and five publication files. The future body states palette5/span4/list6, the outward path family, known bound and cyclic predecessor, and all priority/AI/unrefereed qualifications. It does not introduce a broader solved-status, firstness or current-open claim. The normal push is a fast-forward from the original; an intervening branch update is not force-overwritten. No branch checkout, shared-index change, merge, or unrelated path edit is planned.

The tracker appender requires a confirmed published DOI, resolves the given sheet by gid, checks the exact four headers and writes one bounded historical-result row. It searches by DOI/problem identifiers first and refuses conflicting rows. An exact existing row is recovered; an uncertain prior append with no exact row stops for reconciliation. It records intent before its one append and demands exact readback. Its note preserves known-bound/predecessor credit, unresolved priority/current openness and AI/unrefereed status. These scripts' safeguards are consistent with the reviewed claim; this static review is neither execution evidence nor independent authorization for their external mutations.

## Round1 challenge and final boundary

I withheld the round1 report/verdict until my own proof, archive, source, metadata, independent-count and real-corruption checks were complete. Afterward I read its report and receipts. I found no substantive disagreement. Its broader30 input-corruption cases are additional evidence, not substituted for my own six controls; its factorization agrees with my separately written implementation. My additional local-state, rank and full small length-vector checks support the same bounded verdict.

**Required corrections: none for these exact bytes.** The strongest accepted result is the independently checkable explicit tree theorem and the entire specified outward-path family, together with contradiction of the printed historical equality. Historical novelty, present openness, minimality, new mechanism and formal/external certification remain unestablished. A future earlier tree source could require attribution changes without falsifying the explicit theorem. Any material candidate change requires new binding and review.
