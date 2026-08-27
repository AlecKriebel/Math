# Independent referee report

## Review environment

- **Reviewer:** OpenAI Codex, GPT-5-based independent reviewer; the exact runtime build identifier is not exposed. Separate paper-first mathematical, code/certificate, literature/layout, and final hostile-synthesis passes were used.
- **Date:** 27 August 2026, America/Los_Angeles.
- **Submission:** `k2p-k3p-theta-ai-referee-v1.2.4.zip`; main article `materials/combined-paper-clarified.pdf` (20 pages), followed after the paper-first pass by the two supplied support PDFs (2 pages each).
- **Archive:** SHA-256 `031a1fbb115995ab7edb382d0e52f7791fd512b0e53887fc4a1c8fe5bfb93f6b`. The ZIP contains 40 regular files, no symbolic links, and no absolute or parent-traversing paths.
- **Integrity and provenance:** all 39 manifest-listed files passed before and after replay. All 34 files under `materials/` are byte-identical to the stated canonical subtree at commit `87d86cf348e888b29df94681426611ac601afe62`. The local and remote annotated tag `k2p-k3p-theta-v1.2.4` both peel to that commit. The tag is unsigned, as the revised packet accurately acknowledges.
- **System:** macOS 26.5.2, build 25F84; Darwin 25.5.0 arm64; Python 3.14.6; Tectonic 0.16.9; Poppler `pdftotext`/`pdftoppm` 26.08.0; SymPy 1.14.0 in an audit-local disposable environment.
- **Primary literature checked:** [Brits et al. Version 2](https://arxiv.org/pdf/2607.12919v2), [Brits et al. Version 3](https://arxiv.org/pdf/2607.12919v3), [Gross--Long (2018)](https://doi.org/10.1137/17M1134238), [Gross et al. (2021)](https://doi.org/10.1007/s00285-021-01653-8), [Gross--Krone--Martin (2024)](https://doi.org/10.1007/s11538-024-01314-z), [Cox--Gross--Martin (2025)](https://doi.org/10.1007/s11538-025-01506-1), and [Englander et al. Version 4](https://doi.org/10.1101/2025.04.18.649493).

## Executive assessment

The manuscript constructs exact three-taxon distributions shared by a comparison tree and a binary semi-directed strict level-two theta network under K2P and K3P. Beyond the compact `Q(sqrt(71))` witness, it gives an edgewise strictly continuous-time K2P witness, an exact quartic K3P network parameter outside every globally character-relabeled K2P parameter stratum, full ambient-rank certificates, local collision geometry, an analytic continuation into the strict K3P rate cone, and a one-blob grafting theorem for every labeled binary-tree topology.

I found no false theorem, incorrect witness, arithmetic error, missing analytic implication, or PDF regression. A clean-room program that imports no packet module and reads no packet certificate independently reproduced both factorizations, all 64 Fourier and all 64 ordinary-state probabilities for each compact witness, the exact K2P probability minimum, the selected rank-9 and rank-15 determinants, and all 15 K3P fixed-output tangent residuals. The algebraic continuous-time K2P identities and margins were separately reconstructed from the printed formulas.

The new K3P ordinary-state calculation is genuine and live. It prunes each of the four literal retained graphs for every pattern and compares the mixture with a separately pruned comparison star and both Fourier inversions. A source-only corruption of this path is rejected at the first pattern while all preceding Fourier checks pass.

Four of the six advertised repair families are complete; the semantic-binding and coverage-inventory repairs are substantial but not yet fully closed. The earlier Jacobian/free-direction permutation defect is repaired at the descriptor-to-edge-ID layer, and all five supplied coordinated mutations are rejected in normal and optimized modes. One localized assurance gap remains: edge IDs and reticulation-parent descriptors are not bound relationally to the actual rooted arc endpoints, and duplicate vertex rows are collapsed before the purported uniqueness check. A coordinated internal `p ↔ q` endpoint relabeling therefore leaves operative parent descriptors false while the verifier prints `ALL K3P CHECKS PASSED`. The shipped certificate itself is canonical and the mutation is a graph automorphism, so this does not invalidate the mathematics. It does mean that the claim that semantic binding is closed is not yet fully established.

The new coverage inventory is candid and substantially correct, but it has one additional field-level overstatement: the stored compact-K2P `K_odot_K` transition row is not consumed by `python3 verify.py`, even though the table classifies exact transition probabilities as recomputed. Both remaining issues admit small verifier/test or documentation changes.

## Findings ordered by severity

### 1. K3P topology descriptors are not fully bound to canonical arc semantics

**Severity:** minor correction required; no error in the shipped witness or theorems.

**Locations:** `materials/src/verify_k3p.py:319-337,387-437,478-501,821-824`; `materials/CERTIFICATE_FIELD_COVERAGE.md:28-33`; `materials/src/test_k3p_semantic_mutations.py:66-130`; manuscript `combined-paper-clarified.tex:79-100,600-611`.

The revised verifier now hard-codes the complete 15 Jacobian descriptors and the two free-direction descriptors, closes the K3P top-level schema, fixes reticulation list order, and binds singleton suppression sources. Those changes correctly reject the exact coordinated mutations identified in the prior review.

The graph layer is still split into two independently accepted descriptions:

1. `edge_endpoints` is constructed from the certificate's rooted arc rows.
2. `rooted_network.reticulations` is compared with a hard-coded descriptor list.

The verifier checks the incoming edge-ID set for each reticulation but never asserts that a descriptor's `parent` is the parent of its referenced arc, or that the referenced arc ends at the descriptor's reticulation vertex. It also does not fix the complete map `edge_id -> (parent, child, vector_name)`.

In a disposable certificate I exchanged `p` and `q` only in the actual rooted and root-suppressed endpoints/directions of `e_u_p/e_u_q` and the four `p/q -> r_j` arcs. I left the reticulation descriptors unchanged, including the assertion that `e_p_r2` has parent and choice `p`. Both normal and optimized verifier runs exited 0, even though the mutated arc's actual parent is `q`. This is an internal graph automorphism, so all probabilities and ranks remain true; the experiment isolates a semantic false positive rather than a mathematical one.

Two supporting probes delimit the same issue:

- Swapping only the ID strings `e_rho_1` and `e_rho_u` passes, so the column named `e_rho_1.a_C` can resolve to the `rho -> u` arc.
- Inserting a conflicting `rho/tree` vertex row immediately before the valid `rho/root` row passes. The list is converted to a dictionary first, so `len(self.nodes) == len(set(self.nodes))` is tautological and the later row shadows the contradiction.

Non-automorphic endpoint and parallel-ID swaps were rejected by exact collision or incoming-edge checks. The defect is therefore bounded to canonical meaning and raw-schema assurance.

**Required correction:** validate the complete ten-arc ID-to-endpoint map and preferably vector-name placement; resolve every reticulation descriptor against that map and check parent, child, and choice; reject duplicate vertex IDs before dictionary construction; and add the `p/q`, root-ID, and shadowed-duplicate mutations to the regression suite. No certificate number or proof needs to change.

### 2. The field-coverage inventory has two small overstatements

**Severity:** minor reproducibility/documentation correction required.

**Locations:** `materials/CERTIFICATE_FIELD_COVERAGE.md:28-33,54-62`; `materials/verify_k2p_simple.py:77-103`; `materials/verify_k2p_displayed_trees.py:253-257,529-554`.

First, the K3P entry classifies “exact ordered reticulation choices,” “rooted arcs,” and the ordered Jacobian descriptor map as recomputed or semantically bound without disclosing that descriptors terminate at mutable edge IDs and are not related back to canonical endpoints. Finding 1 supplies a passing counterexample.

Second, changing only `certificate_k2p_simple.json.network_transition_probabilities.K_odot_K[0]` from `7/16` to `999` still lets `python3 verify.py` exit 0. `verify_k2p_simple.py` correctly recomputes the transition row from the effective eigenvector but does not compare it with this stored row, while the displayed-tree verifier deliberately filters `K_odot_K` out of its stored-row loop. The full packet driver would detect an ordinary edit through the manifest and compact-certificate regeneration, but those are consistency checks, not field-level semantic consumption. The inventory's broad phrase “exact edge eigenvalues and transition probabilities” is therefore one field too broad.

The inventory's discussion of `manifest.sha256`, `FILE_SHA256SUMS`, and archive checksum sidecars also describes artifacts from the canonical release context that are not present in this minimal packet; the actual packet object is `PACKET_SHA256SUMS`. This last point is contextual polish, not a correctness issue.

**Required correction:** either compare the stored `K_odot_K` row with the recomputed row or list that stored row as redundant/informational. Qualify the K3P topology relationship until Finding 1 is fixed. Naming only integrity artifacts actually shipped in this packet would make the inventory self-contained.

### 3. No further required mathematical, scholarly, or presentation change

All other previously reported issues are repaired. Optional production polish would be to add semantic PDF tags, slightly enlarge the dense tangent table on page 13, deduplicate two printed arXiv identifiers, and tighten the sparse last bibliography page. None affects meaning or the recommendation.

## Audit of the advertised v1.2.4 repairs

| Advertised repair | Verdict | Evidence |
|---|---|---|
| K3P semantic binding and coordinated mutations | **substantially repaired, but incomplete** | The old Jacobian/free-direction mutation is now rejected; all five supplied tests pass. Finding 1 gives a new relational endpoint/parent false positive. |
| Level-one literature attribution | **repaired** | The 2018 JC large-cycle and 2021 triangle-free level-one results are now called generic, while the full level-one theorem is attributed to Brits et al. |
| Certificate coverage and narrowed integrity claims | **substantially repaired, with two small corrections** | The manifest, sidecar, transcript, finite-regression, and proof/computation distinctions are candid. Finding 2 records the remaining overstatements. |
| Independent ordinary-state K3P pruning | **repaired** | Literal four-state pruning runs on four retained choices times 64 patterns and survives a source-independence negative control. |
| Literal Version 3 history and ten-arc topology | **repaired** | The exact formal lemma/corollary removal is stated; all ten arcs are printed individually in the paper and summary. |
| Figure-label spacing | **repaired** | The `S/T` labels are separated and legible; no layout regression was found. |

## Mathematical claim audit

| Claim or result | Status | Independent basis | Limitations or issue |
|---|---|---|---|
| Fourier conventions, topology, and parameter counts | **verified** | The declared Klein-group transform leaves 16 consistent coordinates. Root suppression produces the three `p-to-q` paths through `u,r2,r3`, nine effective edges, and dimensions 20/29. | The external source's literal 2-sub-blob clauses have a suppression ambiguity, which the paper accurately quarantines. |
| Displayed-tree parameterization | **verified** | Derived from the ten rooted arcs and all four retained-parent choices; descendant characters give exactly the four terms of equation (3). | Uses the stated uniform stationary root and symmetric group-based kernels. |
| Exact strict-interior K2P collision | **verified** | Recomputed all 16 factor identities, 64 Fourier coordinates, 64 inverse probabilities, direct retained-graph/star pruning, normalization, and exact minimum `1188799/79626240`. | None affecting the theorem. |
| K3P non-disjointness by K2P inclusion | **verified** | K2P is exactly the K3P submodel `a_C=a_T`; likelihood and mixture semantics are unchanged. | Inclusion alone does not produce a parameter-level genuinely K3P witness, which the paper states. |
| Exact K3P parameter-level symmetry breaking | **verified** | Quartic reduction modulo `5h^4-1`, direct pruning, and all 64 coordinates were independently reproduced. The `U` edge has three distinct nonidentity eigenvalues. | The exact shared output is deliberately in the global `C=G` relabeled-K2P tree submodel; it is not JC. |
| Edgewise continuous-time K2P result | **verified** | Independently checked the degree-six field, all 16 identities, stochastic rows, and strict `g>s^2` margins. | Edge-specific generators/rate ratios only; no clock or common generator. |
| K2P rank, local locus, and fibers | **verified** | Exact differentiation gives the stated nonzero rank-9 minor; tree rank is 6; dimensions are `20-9+6=17` and `20-9=11`. | None affecting the claim. |
| K3P rank, local locus, and fibers | **verified** | Exact differentiation in the printed semantic order gives `h(10h^2+1)/(2^61 3^4 5^14)`; tree rank is 9; dimensions are 23 and 14. | Finding 1 concerns mutation resistance of edge IDs, not the correctness of the shipped semantic order. |
| Nearby observably genuine K3P collisions | **verified conditional on stated assumptions** | The restricted collision map is a submersion; a local section exists; the three relabeled-K2P tree loci are a closed nowhere-dense union; distinct `U` entries and rank persist in a small neighborhood. | “Genuine” has the paper's explicit global-character-relabelling meaning. |
| Edgewise continuous-time K3P branch | **verified conditional on stated assumptions** | The exact tangent solves all 15 fixed-output equations; the two formerly saturated margins have derivatives `(21-20h^2)/19>0` and `1`; other inequalities persist by openness. | Analytic/existential, with no explicit radius or closed-form nearby point; still only edgewise CT. |
| Dominance and Zariski-density corollary | **verified** | A nonzero full ambient minor makes each complexified polynomial map dominant; full-rank real points in open stochastic/CT chambers give Zariski-dense images. | Only in the normalized effective affine spaces; forced zeros, K2P symmetry, and inequalities remain. |
| One-blob arbitrary-taxon grafting theorem | **verified conditional on stated assumptions** | Applying the same product of three conditional Markov kernels to the common interface law preserves equality. Root splitting, blob topology, strict CT, and equivariant injectivity all check. | Exactly one theta insertion; not a multi-blob composability or genuine four-attachment theorem. |
| Scope and relationship to prior literature | **verified conditional on a bounded search** | Primary sources confirm the v2 K2P lemma/corollary, their formal removal in v3, the v3 open high-level K2P/K3P question, and the revised generic/full level-one distinctions. | A bounded search cannot prove worldwide or unpublished novelty priority. |

## Supporting derivations

### Four switchings and exact equality

For a consistent label `x+y+z=A`, the descendants below `u->p` and `u->q` in the four choices `(p,p),(p,q),(q,p),(q,q)` are respectively `({2,3},empty)`, `({2},{3})`, `({3},{2})`, and `(empty,{2,3})`. This yields the four core factors

    A2_y A3_z U_(y+z)
    A2_y B3_z U_y V_z
    B2_y A3_z V_y U_z
    B2_y B3_z V_(y+z)

with the four product inheritance weights. At the symmetric witnesses, the four pendant/root factors contribute `K_x K_(y+z) K_y K_z = K_x^2 K_y K_z`. A dangling branch has identity character and factor one; suppressing a degree-two vertex multiplies Fourier eigenvalues. Thus there is no omitted switching factor.

At the compact K2P point, all sixteen identities `M_(y,z)=P_(y+z) R_y R_z` hold, including `M_(A,C)=151/1440` and `M_(C,C)=71/1600`. Hence

    q_network(x,y,z)
      = K_x^2 K_y K_z M_(y,z)
      = (K_x^2 P_x)(K_y R_y)(K_z R_z)
      = q_tree(x,y,z).

The other 48 coordinates vanish structurally. The inverse transform and an independent state-space calculation agree in every pattern.

### Continuous-time criteria and local geometry

For a K3P edge, the rate/eigenvalue relation is

    4 lambda_C t = log(a_C / (a_G a_T)),
    4 lambda_G t = log(a_G / (a_C a_T)),
    4 lambda_T t = log(a_T / (a_C a_G)).

The three strict cyclic inequalities are therefore necessary and sufficient for positive edgewise rate classes. K2P reduces to `g>s^2` once `0<s,g<1`. Coordinatewise edge composition preserves these inequalities.

For a submersion `F:P^d -> A^m` and an embedded tree germ of dimension `t`, `F^(-1)(T)` has dimension `d-m+t`, while a fixed-output fiber has dimension `d-m`. Substitution gives `(17,11)` under K2P and `(23,14)` under K3P. At the quartic point the K3P tangent satisfies `J_* p'(0) + F_(U_C) + F_(V_G) = 0`, and the only saturated margins move into the strict cone with positive derivatives. The analytic implicit-function conclusion follows.

### Dominance and arbitrary-taxon grafting

A full ambient Jacobian minor is a characteristic-zero dominance certificate for the complexified polynomial map. The paper correctly restricts the conclusion to effective coordinates and does not infer generic tree equivalence.

If `p=p'` is the shared three-interface law, applying

    K(p)(omega_1,omega_2,omega_3)
      = sum_(x_1,x_2,x_3) p(x_1,x_2,x_3)
        product_i K_i(omega_i | x_i)

to both sides preserves equality. Each attached JC component map is injective because marginalizing to one descendant leaf gives an invertible path kernel. Equivariance then preserves absence of every global nonidentity-character transposition. This proves the one-blob all-taxon statement without extrapolating from the finite four-leaf regression.

## Code and certificate audit

### Claim-to-code map

| File or entry point | Mathematical claim tested | Method | Independence or remaining limitation |
|---|---|---|---|
| `materials/verify_k2p_simple.py` | Compact K2P field, admissibility, factorization, patterns, minimum | Exact `Q(sqrt(71))` arithmetic and inverse Fourier transform | Stored `K_odot_K` transition row is not consumed. |
| `materials/verify_k2p_displayed_trees.py` | Literal K2P graph, four monomials, coordinates, patterns | Exact descendant sets plus separate Markov pruning | Hard-codes canonical topology/vector placement; appropriately shares primitive vectors. |
| `materials/src/verify_k2p_extended.py` | Algebraic edgewise-CT K2P collision and source-order audit | Exact degree-six field, Sturm isolation, interval signs, Fourier and direct pruning | Strong, but later K2P scripts import its infrastructure. |
| `materials/src/verify_k2p_rank_family.py` | Rank-9/rank-6 minors, dimensions, symmetric family | Dual-number differentiation, exact elimination, direct orbit count | v1.2.4 now derives the formerly printed dimension arithmetic. |
| `materials/src/verify_k2p_four_leaf_graft.py` | One four-leaf graft | Literal topology and all 256 Fourier/state probabilities | Regression only; all-`n` result comes from the proof. |
| `materials/src/verify_k3p.py` | Quartic field/topology, collision, direct pruning, rank, tangent, CT margins | Exact quartic arithmetic, graph Fourier, ordinary pruning, Bareiss elimination | Canonical endpoint/reticulation relation and pre-dictionary vertex uniqueness remain open. |
| `materials/src/test_k3p_semantic_mutations.py` | Five coordinated false-positive regressions | Disposable certificates plus required failure diagnostics | Does not yet include the surviving endpoint/duplicate mutations. |
| `materials/src/verify_source_conventions.py` | Five source coordinates and favorable-order factorization | Exact rational evaluation | Focused convention test, not a complete source transcription. |
| `materials/src/generate_k2p_simple_certificate.py` | Compact JSON reproducibility | Regenerates the complete compact certificate | A consistency/regeneration oracle, not an independent derivation of literal metadata. |
| `materials/verify.py` | Complete mathematical suite | Subprocess orchestration with optimized-mode propagation | Orchestration, not independent mathematics. |
| `RUN_REFEREE_REPLAY.sh` | Manifest, transcript, regeneration, and PDF build checks | Fail-closed paths/hashes, normal/optimized replays, disposable builds | Internal consistency rather than external authentication. |

### Exactness and computational coverage

No theorem-critical equality or sign decision uses floating-point arithmetic. The simple K2P checker works in `Q(sqrt(71))` with a rational isolating interval. The CT K2P checker proves cubic irreducibility modulo 37, isolates the intended real root by a Sturm calculation, and obtains a six-dimensional field after adjoining `sqrt(1423)`. The K3P checker works in the irreducible quartic field `5h^4-1=0`, isolates its unique positive root, and performs exact sign tests.

All 64 Fourier and ordinary-state coordinates are checked for both compact three-leaf constructions. The four-leaf regression covers all 256 patterns. Both selected network determinants and both tree-rank witnesses are rebuilt from exact derivatives rather than accepted from nonzero stored scalars. The K3P tangent residual is rebuilt row by row, and the formerly saturated margin derivatives are now generated from keyed edge directions.

The direct K3P route at `verify_k3p.py:920-997` constructs transition kernels, topologically prunes the literal retained DAGs, mixes them with the inheritance weights, and separately sums the comparison star. It does not call the Fourier monomial routine or read stored pattern probabilities. It shares the primitive graph, eigenvectors, group convention, and exact field class, which is appropriate common-input reuse rather than circularity.

The strongest remaining common-mode risks are the mutable graph identifier layer in Finding 1, hard-coded source-convention expectations, and certificate/transcript/generator artifacts shipped from one release. The clean-room reconstruction mitigates these risks for the mathematical conclusions.

## Execution record

All substantive mutations were made in ignored disposable copies. The manifest-verified `packet_copy/` was not changed.

| Command actually used | Exit status | Result |
|---|---:|---|
| `bash ./RUN_REFEREE_REPLAY.sh --with-pdf` | 0 | Normal and optimized complete transcripts matched; focused transcripts, individual entry points, compact regeneration, all three PDF rebuild/text comparisons, and both integrity checks passed. |
| `tmp/sympy_env/bin/python notes/clean_room_symbolic_checks.py` | 0 | Both factorizations, literal direct pruning, all coordinates, K2P minimum, rank minors, and K3P tangent passed independently of packet code/JSON. |
| `python3 materials/src/test_k3p_semantic_mutations.py` | 0 | Harness confirmed all five supplied mutations failed for the intended diagnostics. |
| `python3 -OO materials/src/test_k3p_semantic_mutations.py` | 0 | Same semantic rejections under optimized execution. |
| strict JSON duplicate-key load; Python compile; `bash -n` | 0 | All five shipped JSON files and all executable sources passed. |

## Negative controls

| Mutation | Expected behavior | Observed result | Interpretation |
|---|---|---|---|
| Compact K2P `U:(1,4/5,19/30,4/5) -> (1,79/100,46/75,79/100)` | Break factorization after admissibility | exit 1, `factor (0, 1)` | Collision values are substantively recomputed. |
| Literal graph assignment `p->r2:S->T` in source only | Break graph-derived monomial | exit 1, switching `('p','p')` | Graph reconstruction is live. |
| Stored rank-9 determinant numerator changed by one | Exact determinant mismatch | exit 1, `simple determinant` | Rank scalar is recomputed. |
| K3P pivot `e_u_p.a_G`, constant `-6/19 -> -5/19` in embedded/sidecar data | Break tangent after collision/rank | exit 1, residual row 1 `=h^3/2432` | Fixed-output tangent is recomputed, not sidecar-only. |
| Direct K3P transition index XOR -> cyclic addition mod 4 in source only | Fourier passes, direct path fails | exit 1 at direct `AAA` network/tree comparison | New ordinary-state path is independent and live. |
| Five supplied coordinated K3P mutations | Each underlying verifier must fail for named semantic reason | all rejected in normal and optimized modes | Original v1.2.3 semantic defect is substantially repaired. |
| Global actual `p ↔ q` endpoint swap, reticulation descriptors stale | Should reject descriptor/arc contradiction | exit 0 in normal and optimized modes | Principal remaining semantic-binding gap. |
| Root-adjacent arc-ID swap | Should reject ID/endpoint mismatch | exit 0 | Missing canonical edge-ID map; numerically invisible because both vectors are `K`. |
| Shadowed conflicting duplicate `rho` vertex | Should reject contradictory vertex table | exit 0 | Duplicate check occurs after dictionary collapse. |
| Stored compact-K2P `K_odot_K` transition entry `7/16 -> 999` | Either reject or classify field as informational | `python3 verify.py` exits 0 | One coverage-table overstatement. |

These outcomes are substantive verifier results, not checksum failures. The packet orchestrator and manifest were deliberately bypassed for mutation testing.

## Literature, topology, and scope review

[Brits et al. Version 2](https://arxiv.org/pdf/2607.12919v2) states the K2P trinet sign/disjointness result in Lemma 5.6 and the JC/K2P global result in Corollary 5.8. [Version 3](https://arxiv.org/pdf/2607.12919v3) has no corresponding formal K2P lemma, makes Corollary 5.7 JC-only, explains the permutation obstruction, and lists high-level K2P/K3P trinet extension as open. The manuscript's revised history is therefore literal even though Version 3 retains one stale introductory sentence about later K2P generalization.

The revised Introduction also correctly separates the full level-one theorem from earlier generic results. Gross--Long proves generic identifiability for JC large-cycle networks, while Gross et al. proves generic identifiability for triangle-free level-one networks with a fixed reticulation count under JC/K2P/K3P. The cited dimension, 3-sunlet, and strongly tree-child level-two JC scopes also agree with their primary records.

Under the literal three-clause source definition of a 2-sub-blob, six single-edge subsets of the theta core qualify but contract to degree-four vertices. This is an external terminology tension. The paper records it, requires no no-2-sub-blob hypothesis, and relies only on the unambiguous maximal theta 3-blob. It does not affect the formal v2 K2P counterexample.

Targeted primary-source searches found no earlier exact tree--theta Kimura collision of the claimed form. This supports the novelty framing but is not proof of global or unpublished priority.

## PDF and presentation audit

Tectonic rebuilt all three PDFs in a disposable directory. Layout-preserving Poppler text extraction matched each supplied PDF exactly. Separately, all 24 supplied pages were rendered and inspected at high detail.

- Main manuscript: 20/20 pages passed. Figure 1's crossing-edge `S/T` labels are now separated. No clipping, missing glyph, unresolved reference, overflow, or broken figure/table was found.
- Technical summary: 2/2 pages passed. The ten rooted arcs are now listed individually and agree with the main paper.
- Displayed-tree clarification: 2/2 pages passed. Both tables and the factorization are complete and legible.

The PDFs are untagged. The page-13 tangent table is small but readable, and page 20 has substantial harmless white space. These are optional production issues only.

## Required corrections

Before submission:

1. Bind every K3P rooted arc ID to the literal ten-arc endpoint map and, where the ID carries paper semantics, to the intended vector name.
2. Resolve every reticulation descriptor against the arc map and require exact parent, child/reticulation, and choice agreement.
3. Reject duplicate K3P vertex IDs before dictionary construction and require the canonical ID/type schema. Either bind the leaf-label keys or explicitly classify them as informational.
4. Add negative regressions for the global `p/q` endpoint swap, the root-arc ID swap, and a shadowed conflicting duplicate vertex.
5. Compare the stored compact-K2P `K_odot_K` transition row with the independently recomputed row, or reclassify that one stored field as redundant/informational. Update the inventory's topology qualification and packet-context manifest names accordingly.
6. Rerun the complete normal/optimized replay and the new mutation suite.

No theorem statement, witness value, determinant, tangent, proof, literature sentence, or PDF layout requires correction on the evidence found.

## Limitations and confidence

- Novelty was checked against the cited and readily searchable primary record, not every unpublished result.
- The exact K3P strict-continuous-time point is existential via the analytic implicit-function theorem; the paper does not provide a numerical radius, and none is needed for the stated result.
- The all-taxon theorem is proof-level. The supplied `n=4` run is a regression, not exhaustive finite evidence for arbitrary `n`.
- The local tag and remote ref corroborate repository provenance but provide no external signed attestation. The packet describes this limitation correctly.
- Informational certificate prose was inventoried rather than treated as an independent mathematical premise.

Confidence is **high** in the mathematical assessment and **high** in the identification and bounded severity of the remaining computational-assurance issues.

## Final recommendation

MINOR REVISION

The central mathematics is valid and independently reproduced, and the new K3P pruning and original semantic mutation repairs are substantive. Submission should wait only for the small canonical graph-binding, vertex-uniqueness, and field-coverage fixes above; after those pass the expanded negative suite, I would recommend acceptance.

