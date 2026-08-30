# R6 fresh adversarial mathematical review — 2026-08-29 package

Review date: 2026-08-29 (America/Los_Angeles)
Package root: `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/isolated/k2p_principal_d_plus_submission_referee`
Review-owned exact checks: `/Users/alec/Documents/Math/k2p_same_fresh_referee_2026-08-29_r6/independent_checks/math`

## Bottom line

I found no counterexample to K2P-SAME, no invalid hand implication, and no defect in the exact weak-tree-child sharpness witness. The mathematical argument outside the large finite classifications is coherent and, after adversarial scrutiny, passes. In particular, I independently reproduced the domain inequalities and sections, tree--sunlet identity, rank-nine ordinary-triangle blocks, core-completion counts, minimal repairs, raw-count arithmetic, and the complete weak-sharpness common tensor and Jacobian determinants without importing submission code.

This mathematical subreview deliberately did **not** run the quick/full/global harnesses. Consequently C05--C09, which assert exhaustive facts about very large frozen ledgers, remain **UNVERIFIED in this subreview** rather than being inferred from stored PASS reports. C11's hand implication is valid conditional on those finite premises. The root referee should combine this report with the independent computational replay before assigning a final scientific status.

One concrete current-package defect remains. `proof_compression_submission/probe/PROBE_WORD_THEOREM.md` identifies its “Current coverage artifact” using two obsolete digests. The actual current coverage file, the crosswalk, and the revised bundle manifest use different current digests. This is not a counterexample to C09, but it is a present-tense provenance contradiction in a load-bearing proof narrative and should block release until corrected and resealed. See Finding M1.

Suggested component statuses from this subreview:

- Hand mathematics: **PASS**, conditional only where the theorem explicitly consumes finite computer-assisted premises.
- C05--C09 exhaustive computational premises: **UNVERIFIED here**.
- Overall mathematical theorem: **UNVERIFIED here**, because C11 consumes C05--C09; no mathematical defect or counterexample was found.
- Reproducibility/release: **HOLD** because of Finding M1.
- Confidence: 0.97 that the hand proof architecture is valid if the enumerated premises are true; 0.995 in the independently rebuilt weak-sharpness witness; no independent probability is assigned to exhaustive finite coverage until the computational referee reports.

## Evidence boundary and method

I treated all stored reports, hashes, certificates, and PASS statuses as assertions. I read the complete article and supplement TeX and PDFs, the generated certificate appendix and compression tables, the bibliography, the theorem--artifact crosswalk, and the current proof narratives relevant to C01--C13. I inspected the mathematical semantics of the raw generators, slow canonicalizer audit, symbolic rank-upper mechanism, probe-word verifier, and both weak-sharpness verifiers. I did not use an earlier referee report as evidence, did not modify the isolated package, and did not contact anyone.

The large ledgers were not exhaustively replayed by this subreview. Reading a verifier establishes what a successful execution would mean; it does not establish that execution succeeded on every record. Accordingly, no finite census is marked PASS merely because a stored report says PASS.

The independent script `r6_exact_math_checks.py` imports no module from the submission. It uses only review-owned formulas and primitive graph encodings. Its JSON records `"imports_submission_code": false` and `"status": "PASS"`.

## Primary sources and bindings inspected

| Artifact | SHA-256 | Size / location |
|---|---|---|
| Article PDF | `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4` | 194,542 bytes, 26 pages, `proof_compression_submission/output/K2P_SAME_Principal_Domain_Article.pdf` |
| Supplement PDF | `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d` | 160,762 bytes, 24 pages, `proof_compression_submission/output/K2P_SAME_Reader_Supplement.pdf` |
| Article TeX | `43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d` | `proof_compression_submission/article/main.tex` |
| Supplement TeX | `d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33` | `proof_compression_submission/supplement/supplement.tex` |
| Generated certificate appendix | `1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649` | `proof_compression_submission/supplement/certificate_appendix.tex` |
| Generated compression tables | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` | `proof_compression_submission/supplement/compression_tables.tex` |
| Bibliography | `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6` | `proof_compression_submission/references.bib` |
| Theorem--artifact crosswalk | `43b8a284d1a5c2a3997d467f6d917eaaa00378f432ab434913bf7868151698c8` | `proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json` |

The PDFs were rendered page-by-page and visually inspected as part of the review; no missing mathematical display or visibly truncated proof was found.

Principal proof narratives read:

| Narrative | SHA-256 |
|---|---|
| `work/domain_rooting_closure/PROOF.md` | `f71a8e811881205b195128fde13ec717d08046f247fa43f27a4e8bfc4ba2d93d` |
| `work/quartet_separation_closure/PROOF.md` | `a0f34c91c1a986412e6ae968015eaa38c09a9e2ee813b8d68b2c4655f0842744` |
| `work/bridge_marginal_closure/PROOF.md` | `0677a72be56cdadfe410c5a89cbe3a98743ff3bbf4892646982afd9523dab3dc` |
| `proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md` | `1749e00bb1a1be5c482d596ed84a8394cf06951d0f704bb00a8502cecc64b902` |
| `work/canonicalizer_completeness/PROOF.md` | `7e0e7be28c5be309a67a9f7174858a2a3e356627acff233bbd97d0369a68ba2a` |
| `work/cycle_three_port_closure/PROOF.md` | `6822a6b88929c8ef9f7a842215e6728ae1f41ec01ab2f98b5cbd51b3baa1da51` |
| `work/theta2_five_port_closure/PROOF.md` | `2e09f17b64bd3d9fb110a21189908e9d6e21d1b35b6280888f42f2eb5248171a` |
| `work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md` | `425a041bc3e4cc7bd4f74c952455623ff26f430d9c4ceb006edcac9e8c3765d8` |
| `work/weak_sharpness_closure/PROOF.md` | `dcc36e0ae4299e3f0415d31e73522f224c91506f90062d0a13791af5746e9369` |
| `work/weak_sharpness_audit/PROOF_AUDIT.md` | `d0a4e950a17fe59bda918ed48ff582836ce4592cc4eb97676814cc5ecf1d95aa` |
| `proof_compression_submission/probe/PROBE_WORD_THEOREM.md` | `f45cd543b6cafbada2c9cd361b06f708f2bdebe112c596a774cd0ee7736a17e8` |

`work/global_theorem_closure/GLOBAL_PROOF.md` was read only as a historical/superseded artifact, in accordance with its own status and the current crosswalk; it was not used as authority.

## C01--C13 claim matrix

“PASS” below is a mathematical status. “UNVERIFIED” means that the exact claim contains an exhaustive machine premise not established by this subreview. Locations refer to the source line ranges and corresponding PDF pages.

| ID | Status | Claim and exact location | Mathematical evidence / attack | Computational evidence boundary and exact remaining gap |
|---|---|---|---|---|
| C01 | **PASS** | Principal and CT domains, subdivision, rerooting: article `main.tex` 202--414 (PDF pp. 3--6), especially Lemmas 2.2--2.3; supplement 121--151. | Fourier inversion gives `0<s,g<1` and `g>2s-1`; exact rational boundary-near checks and an explicit three-factor section were rebuilt. Root movement changes only the mixture presentation, including reticulation-adjacent edges, and power-root subdivision stays physical. Narrative `f71a8e...`. | No finite ledger premise. |
| C02 | **PASS** | Displayed quartets, decorated tree of blobs, whole-map tree--sunlet separator: article 415--533 (PDF pp. 6--7); supplement 409--425. | The article derives the K2P pullbacks rather than invoking the revoked rooted tree/sunlet oracle. Positive inheritance weights preserve the strict sign. I independently expanded the representative tree--sunlet residual to the zero polynomial. Narrative `a0f34c...`. | The external tree-of-blobs topological inference is imported with citation; exact cited-version numbering could not be independently retrieved, noted below. The K2P algebra actually used is printed and checked. |
| C03 | **PASS** | Bridge fibre, marginal submersion, localization, restoration: article 535--846 (PDF pp. 7--11); supplement 426--438. | The all-zero coordinate fixes normalization. Comparing sectors forces the common C/T scale; G has its independent scale. The only stabilizers are the two incidence gauges, with no cycle holonomy. Pair anchors yield analytic positive normalizers. The marginal section condition `r^(m-1)>max(S,G,2S-G)` is sufficient and has room near the boundary; CT gluing has the printed nonempty interval. Narrative `0677a7...`. | The 997 concrete restoration obligations are C08, not inferred here. |
| C04 | **PASS** for the mathematical grammar and count theorem | Core reduction, four theta events, repairs, grammar, canonicalizer action, and count identities: article 848--1040 (PDF pp. 11--14); supplement 153--241. | Checked reticulate-pole/same-path exclusions and no-omnian obstructions for all four event placements. Independently brute-enumerated the printed obstruction hypergraphs and recovered every listed minimal repair. Independently recomputed `C(4,1)=831`, `C(4,0)=C(5,1)=1983`, `C(5,0)=4155`, and raw totals 405,216, 2,946,240, 13,440. The slow canonicalizer proof uses the full marked-incidence relation and full licensed signed permutation action; no topology-name oracle is part of the mathematical universe. Narratives `1749e0...`, `7e0e7b...`, `6822a6...`, `2e09f1...`. | This does not certify every collision/noncollision in the realized large ledgers; those consequences are C05--C09 and require replay. |
| C05 | **UNVERIFIED** | Every raw four-port direction exactly once; symbolic rank exclusions and 75 exceptions: article 1041--1164 (PDF pp. 14--16); supplement 226--320. | Code inspection confirmed raw IDs are formed from primitive relations before canonicalization. `syzygy_upper.py` constructs exact integer polynomial vector fields satisfying `J_f V=0`; this is a global symbolic rank bound, not sampled rank evidence. The rank verifier separately handles 75 exceptional representatives and rejects optimized Python. | Did not enumerate all 405,216 records or replay all 75 exceptions. Needed evidence: successful independent raw-ID/canonicalizer/rank replay on this package. Key crosswalk artifacts: raw summary `592120...`, rank coverage `c52c57...`, rank manifest `1ec69e...`; generator `91e58a...`, rank verifier `f5a72d...`, syzygy code `e91af1...`. |
| C06 | **UNVERIFIED** | Exhaustive direct separator families: article 1041--1202 (PDF pp. 14--16); supplement 243--320 and generated appendix. | Certificate semantics are sound: exact polynomial body/pullback equality is distinct from graph-orbit equivalence; direction-safe source/target maps are explicit; ranks require a global target upper bound plus source minor; isomorphisms and triangles carry labelled maps/transport. Representative polynomial pullback schema is algebraically coherent. | Did not replay all 1,472 direct terminals or all 36 higher-degree records (22 quintics, 12 quartics, two cubics). Key artifacts: template table `b6c63c...`, printed appendix JSON `9990bb...`, direct-36 certificate `8f0760...`, direct lock `dca3e0...`, verifier `87f274...`. |
| C07 | **UNVERIFIED** | Corrected whole-map finite universe and exact composite coverage: article 1041--1164; supplement 287--350. | Arithmetic partitions independently sum to 405,216 raw4, 2,946,240 theta2, 13,440 cycle bases, and 536,364 cycle completions. The theorem's logic consumes only certified relation classes and does not infer orbit equivalence from literal polynomial equality. | Did not replay every raw4/theta2/cycle record or terminal classification. Key artifacts: corrected universe `a67862...`; raw4 `7fe220...`; theta2 `a714cf...`; cycle base `7bfb6c...`; cycle full `6e170c...`; composite verifier `0c9bf7...`. |
| C08 | **UNVERIFIED** | Restoration forest: article 827--846 and bounded theorem; supplement 321--350. | The induction measure and fixed-full restoration quantifiers are correct: it restricts an already-existing full target section and never inverts a target deletion map. Parent/transport semantics and terminal-leaf condition are coherent. Independent arithmetic gives 36,568 + 256 = 36,824 edges. | Did not stream all 997 parents / 2,540 roots / 36,824 edges or verify every child archetype. Key forest `396d19...`, transport certificate `a706eb...`, transport ledger `eda415...`, verifier `99f8a3...`, replay `d74cc0...`. |
| C09 | **UNVERIFIED**; current narrative defect M1 | Coherent one-/two-port probes and arbitrary words: article 1120--1164 and main proof 1332--1363; supplement 352--407. | The word induction is mathematically plausible and preserves ordered segment words, source/target direction, path-sink/dummy roles, parent order, and triangle transports. The relation uses graph maps and labelled supports, not literal polynomial-body equality. No 2-closure or invented triangle symmetry counterexample was established. | Did not replay 29,964 one-port rows, 544,571 two-port rows, 67,741 transports, or 4,379 restrictions. Key certificate `6edd40...`, parameter transport `a706eb...`, relation/restriction ledgers `67bd9d...`/`1aff01...`, word verifier `8dcc19...`. Additionally, `PROBE_WORD_THEOREM.md` lines 305--311 gives obsolete coverage digests; see M1. |
| C10 | **PASS** | Whole-map `T_i`, three-port signs, ordinary-triangle common germ and contextual gluing: article 474--533 and 1204--1330 (PDF pp. 6--7, 17--19); supplement 409--453. | Independently differentiated the printed tree/sunlet maps, recovering the exact 4×4 and 5×5 block determinants `-1/2` and `-1/4`, hence the rank-nine minor `1/8`. The proof uses submersions and contextual constant-rank sections, not an invalid square inverse. Simultaneous physical bridge gluing is explicit. | No large census premise beyond using the local alternatives already certified. Crosswalk triangle artifacts include sign proof `f2feaa...`, exact triangle data `25593e...`, certificate `b81a6c...`, no-assert verifier `c4a529...`. |
| C11 | **UNVERIFIED**, conditional hand proof **PASS** | Global equivalence, genericity, and reconstruction: article 1332--1538 (PDF pp. 19--21). | Both directions are logically valid given C05--C09: containment localizes to one physical target type, bounded factors become coherent graph transports, and contextual triangles provide common germs; a common germ yields both directed containments by definition. Genericity correctly proves irreducibility, equality of generic complex/maximal physical rank, finiteness via `r<=n-1` and `|V|<=4n-3`, lower-dimensional total rank-drop image, target sections, and proper competitor closures. Reconstruction assumes exact input, keeps unresolved supports through assembly, uses exact semialgebraic membership, outputs a triangle class, and terminates by finiteness. | The central implication consumes the unverified exhaustive C05--C09 premises. Key current article source/PDF `43278b...`/`e49e72...`; promotion companion `fcf5ec...`; release lock `bbb411...`; main verifier `6c2a61...`. Stored replay reports were not treated as evidence. |
| C12 | **PASS conditional on C11** | Strict CT corollary: article 1540--1588 (PDF pp. 21--22). | `D_CT={0<s<1,s^2<g<1}` is nonempty open in `D_plus`; nonzero polynomial witnesses remain nonzero on a dense CT open set. Power roots preserve CT. The printed bridge choice `0<s<min(1,A1,A2,sqrt(U/L))`, `Ls^2<g<U` makes the original and both transported pairs CT-physical. | No new finite classification; it inherits C11's finite premise. |
| C13 | **PASS** | Weak-not-strong sharpness: article 1590--1799 (PDF pp. 22--24); supplement 455--571. | From primitive arcs I recovered rooting triples `(5,2,3)` and `(7,2,5)`, verified binary/standard/level-2/weak tree-child and failure of strong tree-child, and found no labelled mixed or triangle-forgotten isomorphism. Independent four-switch tensor expansion gives exact equality at the stated rational CT parameters. Direct symbolic differentiation reproduces the two named 9×9 determinants and cherry determinant `2464/675`; the cherry inverse and induction yield dimension `4n-3`. Narratives `dcc36e...` and independent audit `d0a4e9...`. | Fully independent of the bounded atlas. Primary and audit certificates are `e66c78...` and `cfd8d3...`; primary/audit verifiers `f0cab6...` and `28ecbd...`. |

## Scrutiny of the sixteen requested mathematical topics

1. **Class, rootings, weak/strong tree-child, restrictions, triangles — PASS.** Definitions distinguish the fixed mixed graph from an admissible rooted presentation. The no-omnian criterion is the correct local reformulation of strong tree-childness for the allowed presentations. Restrictions suppress only licensed degree-two vertices and keep incoming/dummy/port data. Ordinary-triangle equivalence is an explicitly transported graph relation, not polynomial equality.

2. **Fourier inversion, domain, subdivision, root movement — PASS.** Inverting the K2P Fourier eigenvalues gives positive stochastic entries exactly when `0<s<1`, `0<g<1`, and `g>2s-1`. Coordinate power roots preserve this cone. Rerooting on a tree edge or through a reticulation-adjacent configuration is justified at the distribution/mixture level and does not complement inheritance unless the graph transport reverses the two parents.

3. **Quartets, tree--sunlet, tree of blobs — PASS with citation note.** The strict quartet sign is a positive mixture of displayed-tree signs and detects the decorated blob tree. The whole-map `T_i` calculation is printed and independently expanded. The manuscript explicitly rejects the revoked rooted tree/sunlet oracle.

4. **Two-sector bridge fibre — PASS.** All-zero normalization removes a hidden scalar. C/T comparison imposes equality of their scale; G remains independent. Rank-one factorization leaves exactly two incidence gauges. Pair anchors give analytic normalizers, the positive action is free, and strict inequalities provide local saturation. There is no holonomy because bridge gauges live at incidences and are glued through the displayed local product.

5. **Paired marginal products and transports — PASS at theorem level.** Coordinatewise products preserve `D_plus`. The explicit section has strict room and is submersive. Source/target switching signatures are retained. Tensor-invisible parameters are not declared identifiable. Inheritance complements occur only under a certified parent-order reversal.

6. **Semialgebraic localization and fixed-full restoration — PASS.** Finite target choices plus Tarski--Seidenberg and constant-rank stratification produce one target analytic section on a smaller regular germ. The proof localizes an already assumed full containment section; restoration restricts it and never lifts an abstract marginal equality or inverts a deletion map. This addresses the former quantifier hazard.

7. **Cycle/theta core reduction and minimal repairs — PASS.** Root reduction reaches an incoming real port. The cycle core and four directed theta placements cover the local possibilities. Reticulate-pole and same-path attachments are excluded where claimed. Direct examination of the no-omnian obstruction sets and a review-owned transversal enumeration reproduce all minimal repairs.

8. **Ordered words and exact counts — PASS for semantics/arithmetic.** The grammar distinguishes ordered subdivision words, path-sink roles, repair tags, and dummy roles. The four displayed completion formulas independently evaluate to 831, 1983, 1983, and 4155. Their raw products reproduce the three headline universe sizes. Exhaustive record realization is left to the computational audit.

9. **Certificate semantics — PASS as logic; exhaustive coverage UNVERIFIED.** Quartet/whole-map signs are exact pullbacks. Rank exclusion requires a symbolic global target upper bound plus an exact nonzero source minor. Direct polynomial identities are checked with source and target substitutions. Isomorphism/triangle terminals carry labelled graph maps and licensed direction/port/parent transports. Nothing in the proof licenses a semantic conclusion from hash agreement alone.

10. **PC-PARTIAL boundary — PASS.** The article and supplement state that identical polynomial bodies do not imply graph-orbit equivalence. Exceptional rank, restoration, and probe ledgers remain explicitly load-bearing. This prevents proof-compression output from silently replacing the finite classification.

11. **Rank-nine ordinary triangle — PASS.** The exact 4×4 and 5×5 blocks are correct, with determinants `-1/2` and `-1/4`. Their variables are complementary after the common normalization, so the combined rank is nine. The argument uses submersion/constant-rank sections and then simultaneous bridge gluing; it never invokes a nonexistent square inverse.

12. **Global equivalence and no proper containment — PASS conditional on finite premises.** Containment first forces the same decorated blob tree and then one local target choice. The bounded theorem and coherent probes convert those local choices to one graph transport. Conversely, graph/triangle transport gives a common physical germ; by definition that gives both containments. Hence proper one-way containment is excluded.

13. **Genericity — PASS conditional on C11.** The image closure is irreducible. A nonzero complex Jacobian minor cannot vanish on the nonempty real physical open set, equating generic complex and maximal physical ranks. Strong tree-child bounds reticulations and vertices, hence gives finitely many competitors. The total source rank-drop image has dimension at most `d_N-1`. A full-dimensional competitor intersection would yield a target section and contradict C11. Real semialgebraic and complex closure dimensions are compared correctly; each appended exceptional component is individually proper before taking the finite union.

14. **Reconstruction — PASS conditional on C11.** The theorem is explicitly exact-input, not numerical or finite-sample. It retains all unresolved local supports until global coherent assembly, uses terminating exact semialgebraic model membership, and outputs the ordinary-triangle class. The restriction count is finite because the topology list, candidate supports, and relevant minors are finite.

15. **Continuous-time transfer — PASS conditional on C11.** Every separator/rank condition is polynomial and survives on the open CT cone unless identically zero. Subdivision, marginal sections, triangle witnesses, and simultaneous bridge gluing have explicit CT-preserving constructions. No boundary is silently included.

16. **Weak-class sharpness — PASS independently.** Both graphs and their properties were reconstructed from arcs; non-equivalence survives forgetting triangle direction. Exact rational CT parameters give the same full tensor. The specified zero-based rows/columns and exact nonzero determinants were regenerated from symbolic derivatives, not copied matrices. The cherry observables have a nonzero inverse minor, and the extension preserves the graph properties and dimension increment.

## Independent exact attacks

### Review-owned program and result

- Program: `independent_checks/math/r6_exact_math_checks.py`
  SHA-256 `81b3fa05d004289ec9121946bbece00e334953f701fabfc873d6042a2ba16dc3`
- Result: `independent_checks/math/R6_EXACT_MATH_CHECKS.json`
  SHA-256 `80e3a857c18a812d0e176c64a50109f41e98a998231ae0b7f1913c4e0aaab7f3`
- Command log: `logs/r6_exact_math_checks.json`
- Exit status: 0
- Wall time: 0.760939 s
- Peak RSS: 70,090,752 bytes
- Stdout/combined-output SHA-256: `d78957da49f82b79d739420ae6f1bba3f21162204885e12bd84898bdcb9acb08`

### Results

- Four boundary-near rational points were checked exactly against every strict `D_plus` inequality; three CT points were checked exactly against `s^2<g<1`.
- An explicit three-factor marginal section near `g=2s-1` was constructed and each factor checked exactly.
- The representative tree--sunlet residual expanded to exactly zero.
- Direct differentiation of the triangle maps recovered determinants `-1/2`, `-1/4`, and combined minor `1/8`.
- Completion counts were independently obtained as `831, 1983, 1983, 4155`.
- Minimal transversals exactly matched the cycle and four theta repair tables.
- Raw arithmetic gave 405,216, 2,946,240, and 13,440; printed partition sums also matched 536,364 cycle completions, 36,824 restoration edges, 29,964 one-port rows, and 544,571 two-port rows.
- Primitive weak-sharpness arcs gave rooting counts `(5,2,3)` and `(7,2,5)` and no labelled mixed or triangle-forgotten isomorphism.
- Independent four-switch K2P expansion gave exact full-tensor equality.
- Symbolic differentiation gave the exact submitted determinants
  `10368019213741323/563981315074464023964442388464888915634290688` and
  `1435825/85002596691653613846528`, plus cherry determinant `2464/675`.

These attacks are independent of the decisive classifier and canonicalizer. They validate representative algebra, arithmetic, graph encodings, and the whole weak witness. They do not replace exhaustive generation of C05--C09.

## Numbered finding

### M1. Current probe theorem names obsolete coverage digests

- **Classification:** reproducibility-blocking / authoritative-proof-narrative inconsistency; not theorem-fatal.
- **File and lines:** `proof_compression_submission/probe/PROBE_WORD_THEOREM.md`, lines 305--311, SHA-256 `f45cd543b6cafbada2c9cd361b06f708f2bdebe112c596a774cd0ee7736a17e8`.
- **Claim made there:** the “Current coverage artifact” has file SHA-256 `3791e4bb829976aa78289281b9998bfe0605ba4a20518f1e8dd660d7d1a91bb8` and logical payload `1d4248028b38f6b731f066960d9e584240de68a17323539fe5b47f119a8086f6`.
- **Observed current artifact:** `proof_compression_submission/probe/PROBE_WORD_COVERAGE.json` has file SHA-256 `c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660` and embedded `payload_sha256` `d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49`.
- **Cross-check:** current `THEOREM_ARTIFACT_CROSSWALK.json` C09 and `REVISED_REFEREE_BUNDLE_MANIFEST.json` both bind the actual current file SHA `c2e32b37...`, proving this is an internal narrative mismatch rather than a hash-command ambiguity.
- **Minimal reproducer:** from the package root, inspect lines 305--311 of the theorem, compute SHA-256 of `PROBE_WORD_COVERAGE.json`, then parse its top-level `payload_sha256`. The two observed values disagree with both values printed in the theorem.
- **Intended semantic reason:** a current load-bearing theorem narrative must identify the exact coverage premise it claims to consume. Outer byte manifests merely authenticate the contradictory theorem bytes and do not repair that semantic edge.
- **Effect:** no mathematical counterexample follows; the actual artifact can still be independently replayed. But the claimed current proof-to-artifact binding is false as printed, so a reader following the narrative is sent to an artifact that is not present.
- **Smallest adequate remedy:** replace the two printed digests with `c2e32b37...` and `d66b2824...`; add a semantic check that parses these two declarations and compares them with the current coverage file and payload; regenerate every ledger/crosswalk/report/archive whose bytes bind the narrative. Downstream authoritative artifacts require resealing.

## Scope and literature boundary

The manuscript correctly limits the result to binary standard semi-directed strongly tree-child level-2 networks, strict inheritance, and `D_plus`, with a CT restriction. It does not claim mixed-sign, stochastic-boundary, singular-edge, higher-level, weak-class-identifiability, numerical-stability, bit-complexity, or finite-sample inference results. Nothing in this review suggests adding those claims.

I checked the official Huber et al. source supporting the two level-2 semi-directed generators. The official Englander et al. page supports the substantive quartet/tree-of-blobs result and K2P/JC scope, but the exact current-version proposition numbers cited in the supplement could not be independently fetched during this review because the current bioRxiv endpoint returned a rate-limit response. The article prints and checks the K2P identities it actually uses, so this is a narrow attribution-version verification gap, not a load-bearing proof gap. The Brits et al. source is related work rather than a premise of K2P-SAME. Novelty searching is evidence of search coverage, not an exhaustive priority guarantee.

## Required actions arising from this mathematical subreview

1. Correct the two stale hashes in `PROBE_WORD_THEOREM.md` and add the semantic binding check described in M1.
2. Rebuild/reseal all byte-dependent manifests, reports, PDFs if affected, and the referee archive; independently verify that the narrative, coverage JSON, crosswalk, and outer manifest now agree.
3. Complete the independent exhaustive computational replay of C05--C09. Do not promote C11 from conditional to verified on the basis of stored reports alone.
4. If exact citation-version auditing is required for release, record a retrievable archived copy of the cited Englander version and verify the proposition numbering. This is not needed to repair the mathematical proof because its relevant K2P formulas are self-contained.

No mathematical rewrite, mixed-sign extension, proof-compression search, or unrelated research is indicated by the evidence.
