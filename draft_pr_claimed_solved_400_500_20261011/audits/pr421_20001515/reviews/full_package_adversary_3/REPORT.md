# Third independent whole-package adversarial review

**Verdict: PASS. Required edits: 0. Optional edits: 0.** This verdict concerns the exact 53-file scientific package at PR421 head `2e85a0b10c3793ed1d46726b50efac5a6306b707` and the corrected live PR description. No remaining mathematical or publication-package defect was found. It does not certify live Zenodo acceptance, publication, external human peer review, formal verification, historical firstness, absolute novelty, minimality or virtual specialness.

The exact hypothesis is that the full mapping torus

\[
G=\langle a,b,c,t\mid tat^{-1}=a,\ tbt^{-1}=ab,\ tct^{-1}=bcb\rangle
\]

admits a free proper cocompact cubical action on a CAT(0) cube complex. The final positive b is essential. The proof was assessed as a hypothesis; author lemmas, metadata verdicts and peer reports were not accepted as premises.

## Independence and eligibility

There is a disclosed procedural limitation: I read candidate ATTEMPT_1.md and the paper source before writing CRITERIA.md. I therefore do **not** claim author-blind reconstruction or criteria-before-all-source order. I then defined falsifiers, independently reconstructed incidence, reversible algebra and the global cover/action argument, wrote an independent implementation without candidate imports, and sealed those five artifacts at 2026-10-13T00:31:28.364990Z before reading any root/peer reports or gates. INDEPENDENCE_SEAL.json records the ordering deviation and frozen hashes. Those five artifacts remain unchanged. Root's subsequent acceptance of this disclosure was not used as mathematical evidence.

Native GitHub GET initially established an open draft PR at the actual head and a selected `claimed_solved` row before candidate proof bodies were read. Final native GET at 2026-10-13 00:42:49 UTC again found PR421 open and draft, branch `research/20001515-explicit-cubulation`, and that same head. The QUEUE header and the exact ID 20001515 row were fetched separately at the immutable head: Status is `claimed_solved`, Turns is `1/5`, and Findings/DOI are blank. No other case's mathematical body was read. An initial generic content/blob acquisition produced transformed or truncated text and was rejected as custody evidence; exact line fetches and SHA-verified native trees supplied the accepted evidence. Raw acquisition responses remain private.

## Independent finite geometry and algebra

The independent artifact RECONSTRUCTION.md and executable reconstruct.py retain square-corner occurrences before identifying link simplices. In Q the second square revisits A; its two A corners give distinct d+/q+ and p-/e- edges, alongside p-/q+ from the first square. Comparing all potential link edges establishes induced fullness of both attaching maps. The involution exchanges x and y and reverses b; its two square images lie in the appropriate dihedral orbits, and the actual face isometries agree on shared edges.

The genuine Q product contributes six edge cylinders and two cube cylinders. Each of eight signed interval directions cones a full domain link; no cell has two interval directions. The assembled actual vertex link has 14 vertices, 32 edges and 16 triangles. Incidence multiplicities are checked before deduplication. Its graph has exactly those 16 three-cliques and no four-clique. Thus the actual link is simplicial and flag. The quotient counts are one vertex, seven edges, eight squares and two cubes. Independent deletion of an A triangle and duplication of a corner fail the relevant checks. These checks supplement the incidence argument, including the repeated A occurrence, rather than replacing it with clique totals.

The six side-square equations reversibly eliminate three interval generators. The remaining presentation is

\[
P=\langle x,y,b,z\mid xy=yx,\ bxb^{-1}=y,\ z^{-1}(bx)z=b^{-1}y\rangle.
\]

The apparent second HNN relation is equivalent by the base relation; cube cells add no fundamental-group relations. The changes `a=xy^-1`, `t=x`, `c=(zx)^-1` have explicit inverse changes `x=t`, `y=a^-1t`, `z=c^-1t^-1`. The commuting relation becomes `at=ta`; the base relation is equivalent to `tbt^-1=ab`. Since `b^-1y=xb^-1`, the HNN relation is equivalent to `c(bt)c^-1=b^-1t`, and multiplication gives `tct^-1=bcb`, with reversible converse. This identifies the full P with the exact G, without an index restriction or a power of the stable letter.

A separate implementation of free-word/height semidirect normal forms verifies the inverse automorphism `a->a,b->Ab,c->BacBa`, all three HNN relators and all six side squares. Changing the final b or the HNN conjugation gives a nonidentity form. Normal and optimized executions of my independent implementation agree. The reversible presentation proof, not one-way relator testing, establishes the group isomorphism.

## Global cover, completeness and action

The finite quotient uses the general face-identification cubical convention, so its cubes need not be embedded. [Leary v3](https://arxiv.org/abs/1009.1540v3), Theorem C.9, explicitly applies to this convention with arbitrary vertex links. The genuine simplicial flag link therefore gives a CAT(0) universal cover with the lifted unit metric. Theorem C.4 then establishes embedded cubes and single-face intersections in that cover. Strictness is a consequence of the CAT(0) theorem, not an unsupported assertion that any quotient automatically has a strict cover.

The cover is three-dimensional; hence it has no infinite ascending chain of cubes and is complete by Leary Theorem A.6. Its finite links give local compactness. Complete geodesic CAT(0) and local compactness give properness of the metric by metric Hopf–Rinow. The full deck group acts freely and cubically. For compact C, infinitely many distinct translates meeting C would yield convergent p_i,q_i in C with h_i p_i=q_i. Fixed covering neighborhoods around the limits put the points in fixed sheets for large i; a deck transformation between fixed sheets is unique, a contradiction. The finite quotient is compact, giving cocompactness. This addresses full-group action, metric and action properness independently of the finite computations.

## Primary sources, exact subgroup and attribution

PRIMARY_APPLICABILITY.md checks the current primary theorem sources, including corrected [Minasyan–Osin v6](https://arxiv.org/abs/1310.6289v6). In H, the embedded base A0 is Z² and Bass–Serre vertices are hA0. The bx axis has consecutive edge stabilizers `<y>` and `<x>` with trivial intersection, and height supplies a bi-infinite nonbacktracking axis. The specific bx is WPD by Corollary 4.3. [Dahmani–Guirardel–Osin v5](https://arxiv.org/abs/1111.7048v5) supplies its virtually cyclic hyperbolically embedded group; [Sisto](https://arxiv.org/abs/1310.7753v1) gives the Morse property in a finite-generator word metric.

[Ben-Zvi–Kropholler–Lyman](https://arxiv.org/abs/2011.05374v1), Theorems 1.1/5.1, apply to the exact bx circle. K has one vertex and empty maximal tree, so its lifted 1-skeleton metric is the x,y,b Cayley metric. The lifted circle lies within one edge of the cyclic orbit; bounded endpoint connectors transfer Morse quasiconvexity to it. Finite completion gives a local isometry whose pointed subgroup image is exactly `<bx>`, not a power or supergroup. Composing with the involution gives the same-domain map with generator image By. The full-link gluing yields the same full G. Thus the paper's qualitative existence deduction from earlier tools has the necessary exact-subgroup and metric hypotheses; it is not merely a proposed completion strategy. It does not supply the explicit small cell counts. [Hagen–Wise v3](https://arxiv.org/abs/1605.07879v3) free cubulation and general gluing observations are used within their actual scope. Current Bongiovanni–Ghosh–Gültepe–Hagen and Wu–Ye results were also checked and do not silently replace the needed equivariant geometric-action argument.

Independent HTTP acquisition of AIM and default-TLS acquisition of the 2024 and 2026 captures returned identical selected-source bodies specifying `ab,bcb`. The workshop report's `aba,bcb` formulation is distinguished. A blank source status is not current-openness evidence. The bounded priority inspection does not establish exhaustive absence of prior work. The paper appropriately credits the earlier-tools deduction and withholds historical firstness, absolute novelty, minimality and virtual specialness. SOURCE_IDENTITY_AND_PRIORITY.md records acquisition limitations and search bounds.

After my independence seal, root identified secondary-review name/coset slips in peer2's supporting prose. They are not present in the accepted paper: it correctly uses Minasyan–Osin, Ben-Zvi–Kropholler–Lyman and hA0. No immutable peer2 report was altered, and no secondary-review claim was substituted for primary-source checking.

## All-file custody, reproduction and visual audit

The original candidate manifest SHA-256 is `0a43f04fde4e6335e7ee852357429310e013dd62d2f9a3da6b81cacb50b0cd41`. Its 53 local paths and the 53 update-manifest entries match the actual-head native objects. Thirteen selected nonrecursive Git tree objects were independently reserialized and SHA-1 checked, all untruncated. Every scientific file matches SHA-256, Git blob identity, length and mode 100644. Foreign sibling trees were retained as opaque identities. Historical ancestor comparisons independently establish preservation outside the selected case, and the original 13-file author snapshot was checked against its historical native objects. The root receipt's 53 records also match my own native custody rather than serving as a premise. All 53 files, representing 37 unique payloads, were inspected; FILE_INSPECTION_LEDGER.json records each treatment and duplicate alias.

The original mathematical proof remains SHA-256 `c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6`. An exact whole-AST comparison shows the three checker repairs are precisely the replacement of 62 Assert nodes by explicit conditional AssertionError raises. No accepted Assert remains. This preserves their ordinary verification predicates under Python optimization; it is not a theorem about arbitrary code environments.

From clean private copies, both normal and optimized bundle drivers pass. Each launches six baseline program runs, rejects 14 substantive mathematical corruptions and three integrity corruptions, and verifies six relocated normal/optimized runs with an outside working directory and spaces in the path. Saved generated outputs were deleted before reproduction. My additional seven mathematical mutations reject in both modes with substantive AssertionError, empty stdout and absent generated results; five additional integrity attacks reject in both modes. These include duplicate JSON keys, traversal, extra directories, symlinks and coordinated proof/manifest replacement. ADDITIONAL_CORRUPTIONS.json records 14 mathematical and 10 integrity rejections. No finite check is used to fill a theoretical gap.

Both ZIPs have safe relative unique members, no symlinks and valid CRCs; four source members and 24 verification members were checked. The private archive rebuild reproduces both ZIP bytes exactly. The source archive compiles with Tectonic. Its rebuilt PDF has identical extracted text and all six rendered page images identical to the canonical PDF, though PDF byte identity differs with build metadata. I visually inspected all six canonical pages: no clipping, overlap or missing-glyph defect was found, and equations, tables and references are legible.

Canonical PDF SHA-256 is `3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841`; source SHA-256 is `6c339c55aef95458e633ba2dc3136b26e4abacf55acca08e170b992783785390`. REPRODUCTION.json and PDF_VISUAL_AUDIT.json record exact results. Historical dated research notes and execution records were interpreted with their explicit publication addenda, preserving provenance rather than treating earlier pending assessments as current claims.

## Description, licenses and native metadata

The corrected live body is exactly 3,689 bytes, SHA-256 `8265fde5e337cf815cd94ea6a0a1a523087784c7a64f4b5211c54fba7531b603`, equal to PR_DESCRIPTION.md. It now names the actual 53-file package, actual scientific head, original historical head and bounded claims accurately. Peer2's original R1 concerned the stale 13-file/original-head description and missing live access; that immutable FINDINGS verdict remains historical. The one body repair and my final native readback resolve R1 without scientific byte changes. FINAL_SCOPE_READBACK.json records the current observation.

The first-party paper/source/verification licenses consistently use CC BY 4.0 and correct author ORCID. Extensive AI involvement, unrefereed status, no external human peer review and no proof-assistant certification are disclosed in paper, package, PR description and metadata. Foreign downloaded source bodies are excluded from the publication archives and this review's positive public allowlist.

The exact Zenodo metadata and three publication files pass the native local checker. Current official documentation and current official legacy serializers/deserializers explicitly support version and language; the linked old schema omits them and is stale. ZENODO_CONTRACT.md records that discrepancy, implementation identities and the contract analysis. The offline native response check passes and 23 meaningful metadata/file/state corruptions reject. No authenticated server acceptance was tested, no deposit was staged or published, and no live mutation was made. The publishing operator must inspect the real authenticated readback during publication; that future operation is not a package edit.

## Final disposition

No required or optional edits are requested. Strongest verified result: the explicit finite model and its full-group free proper cocompact CAT(0) cubical action, with checked primary-source applicability and reproducible publication artifacts. Mathematical gap found: none. Publication performed by this reviewer: none. Original proof-search turns added: zero; author budget remains 1/5.

PUBLIC_ALLOWLIST.json positively identifies only this review's original public artifacts. FINAL_SEAL.json pins that inventory and its files without a self-hash cycle. Raw native responses, foreign source bodies, private fixtures, renderings and extraction/reproduction directories remain private. The parent must inspect the complete report and evidence before any publication decision.
