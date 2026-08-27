# Independent referee report

## Review environment

- **Reviewer:** OpenAI Codex, GPT-5-based independent reviewer; the exact
  runtime build identifier is not exposed. Separate paper-first mathematical,
  code/certificate, literature/layout, and hostile-synthesis tracks were used.
- **Date:** 27 August 2026, America/Los_Angeles.
- **Submission:** `k2p-k3p-theta-ai-referee-v1.2.5.zip`; main article
  `materials/combined-paper-clarified.pdf` (20 pages), followed only after the
  paper-first pass by two support PDFs (2 pages each).
- **Archive:** SHA-256
  `e8302556f356ac04add887a59ab370d4a496f011d59ccfd8a3e87cc19876551e`.
  The ZIP has 45 entries (41 regular files and four directories), no symbolic
  links, and no absolute or parent-traversing paths.
- **Integrity and provenance:** all 40 manifest-covered paths passed before and
  after replay. All 35 packet files under `materials/` are byte-identical to
  the stated canonical repository subtree at commit
  `9f8d2682ead74e23b7badd9d7f46869477b4e84f`. The local and remote annotated
  tag `k2p-k3p-theta-v1.2.5` both peel to that commit. The tag is unsigned, as
  the packet accurately disclaims.
- **System:** macOS 26.5.2, build 25F84; Darwin 25.5.0 arm64; Python 3.14.6;
  Tectonic 0.16.9; Poppler `pdftotext`/`pdftoppm` 26.08.0; SymPy 1.14.0 in an
  audit-local disposable environment.
- **Primary literature checked:**
  [Brits et al. Version 2](https://arxiv.org/pdf/2607.12919v2),
  [Brits et al. Version 3](https://arxiv.org/pdf/2607.12919v3),
  [Ardiyansyah (2021)](https://arxiv.org/abs/2104.12479),
  [Gross--Long (2018)](https://doi.org/10.1137/17M1134238),
  [Gross et al. (2021)](https://doi.org/10.1007/s00285-021-01653-8),
  [Gross--Krone--Martin (2024)](https://doi.org/10.1007/s11538-024-01314-z),
  [Cox--Gross--Martin (2025)](https://doi.org/10.1007/s11538-025-01506-1),
  and [Englander et al. Version 4](https://doi.org/10.1101/2025.04.18.649493).

## Executive assessment

The manuscript constructs exact three-taxon distributions shared by a
comparison tree and a binary semi-directed strict level-two theta network
under K2P and K3P. Beyond the compact `Q(sqrt(71))` collision, it gives an
edgewise strictly continuous-time K2P witness, an exact quartic K3P network
parameter outside every globally character-relabelled K2P parameter stratum,
full ambient-rank certificates, local collision geometry, an analytic
continuation into the strict K3P rate cone, and a one-blob grafting theorem for
every labelled binary-tree topology.

I found no false theorem, incorrect witness, arithmetic error, missing analytic
implication, PDF regression, or verifier false positive affecting an operative
parsed value, a supplied unique-key certificate, or a mathematical claim. Two
independently written reconstruction programs, neither of which imports packet
verifier code or reads packet certificates, reproduce the compact and
continuous-time K2P calculations and the quartic K3P calculation. Between them
they check the printed factorizations, all 64 Fourier and ordinary-state
coordinates for each compact witness, literal pruning on all four retained
graphs, positivity and the exact K2P probability minimum, the fixed-order sign
counterexample, the rank-9 and rank-15 determinants, the two-parameter K2P
family, the continuous-time field identities and margins, and the full K3P
fixed-output tangent.

The v1.2.5 assurance repairs are effective. All complete normal and optimized
replays pass. Independent hostile tests reject every earlier K3P semantic
escape, additional graph/schema/descriptor contradictions, a source mutation
that breaks ordinary-state pruning while leaving the Fourier path intact, and
separate corruptions of every stored compact-K2P transition row, including
`K_odot_K`. The revised coverage inventory now distinguishes semantic
verification from transport integrity accurately.

One narrow scholarly correction remains before submission: the literature
discussion should cite Ardiyansyah's directly relevant 2021 algebraic study of
simple and semisimple level-two JC/K2P/K3P network models. It would also be
worth qualifying the abstract and acknowledgment's Version 2-to-3 wording as
the removal/correction of the **formal K2P lemma and corresponding global
corollary**, because Version 3 retains one stale roadmap sentence announcing
an arbitrary-level K2P result. The citation is required; the history qualifier
is advisory. Neither affects the theorem, witness, proof, title, or conclusion.

## Findings ordered by severity

### 1. Cite the closest earlier level-two algebraic study

**Severity:** minor literature-completeness correction required before
submission; no priority conflict identified.

**Location:** the level-two literature paragraph at
`materials/combined-paper-clarified.tex:29` and the bibliography.

Muhammad Ardiyansyah's 2021 preprint, *Distinguishing Level-2 Phylogenetic
Networks Using Phylogenetic Invariants* (arXiv:2104.12479), directly studies
algebraic distinguishability of simple and semisimple level-two network models
using Fourier methods under JC, K2P, and K3P. It catalogs the small simple
strict level-two topologies and proves partial variety noncontainment results
for restricted four- and higher-leaf “nice” classes. Its Lemma 5.1 also states
that no simple strict level-two network on two or three leaves belongs to that
nice class.

That work neither constructs nor rules out the present three-leaf pointwise
stochastic-interior tree--theta collision. It does not diminish the claimed
novelty. It is nevertheless close enough in model, level, topology family, and
algebraic method that omitting it leaves the literature map incomplete.

**Smallest adequate correction:** add one sentence distinguishing the 2021
restricted generic/variety results from the present full pointwise trinet
intersection, and add the corresponding reference.

### 2. Advisory: qualify the Version 2-to-3 history at its two broadest occurrences

**Severity:** editorial precision; not submission-blocking and no effect on
the new results.

**Locations:** `materials/combined-paper-clarified.tex:19` (abstract) and
`:614` (acknowledgment). The introduction at `:27`, the source-comparison
remark at `:234`, and the technical summary at `:14` are already precise.

Version 2 formally states the arbitrary-level K2P trinet result as Lemma 5.6
and the corresponding JC/K2P global result as Corollary 5.8. Version 3 removes
that K2P lemma, makes the global corollary JC-only, explains the leaf-order
obstruction, and asks whether the high-level result extends to K2P and K3P.
However, Version 3 PDF page 11 retains an internally stale Section 4.1 roadmap
sentence saying that the JC and K2P inequalities are generalized to arbitrary
level in Section 5.

The abstract's “K2P claims withdrawn” naturally refers to the two formal
claims, and the acknowledgment fairly describes their correction. The current
wording is therefore materially accurate despite the surviving stale source
sentence. Adding “formal” would remove a possible hyperliteral ambiguity.

**Recommended refinement:** change the abstract to “the formal K2P lemma and
corresponding global-corollary claim removed between Versions 2 and 3,” and
analogously qualify the acknowledgment. A footnote about the stale source
roadmap sentence is optional and probably unnecessary.

### 3. Advisory: make raw-certificate parsing unambiguously fail closed

**Severity:** optional reproducibility hardening; the supplied certificates
and their verified mathematical meanings are unaffected.

All five shipped JSON certificates contain unique object names under a strict
duplicate-detecting parser. The operative v1.2.5 K3P graph schema also rejects
duplicate vertex IDs before list-to-map conversion, which closes the earlier
reported defect. Separately, however, the loaders use ordinary Python
`json.loads`. In raw hostile JSON, an earlier bogus object property followed by
the canonical property is silently shadowed by the later value. The two K2P
top-level schemas and a few K3P nested objects also accept newly added unknown
fields as inert metadata.

These cases do not create a false pass for any value in the shipped unique-key
certificates: the parsed operative value is canonical, the extra fields are
unused, and changing the packet bytes is independently rejected by the
manifested replay. The coverage inventory also accurately says that unlisted
descriptive fields are informational. Nonetheless, a reusable verifier is
clearer if every raw certificate has one interpretation.

**Recommended hardening:** use one `object_pairs_hook` loader that rejects
duplicate names at every nesting level, close operative schemas, and reserve
an explicit metadata namespace for extensions. This is not a condition of the
mathematical recommendation.

### 4. No further actionable mathematical, computational, or presentation finding

The exact constructions, topology, direct-pruning implementations, ranks,
local arguments, and grafting theorem survived independent reconstruction and
adversarial mutation. Optional production polish would be to add semantic PDF
tags and alternative text. This is an accessibility advisory, not a scientific
or ordinary preprint-layout blocker.

## Audit of the advertised v1.2.5 repairs

| Advertised repair | Verdict | Evidence |
|---|---|---|
| Canonical K3P vertex/arc/reticulation binding | **repaired** | Exact ten-arc IDs, endpoints, vectors, vertex schema, and relational reticulation descriptors are enforced before use. All earlier and fresh coordinated mutations fail. |
| Nine hostile K3P mutation regressions | **repaired** | The supplied suite passes in normal and optimized modes; an independent 17-certificate-mutation suite also fails closed. |
| Every compact-K2P transition row consumed | **repaired** | Separate corruptions of all six network rows and all three tree rows are rejected, including `K_odot_K`. |
| Coverage inventory corrected | **repaired** | The inventory accurately separates operative semantic checks, recomputed values, informational fields, finite regressions, and transport-integrity artifacts. |
| Twenty-four pages remain clean | **verified** | All pages were rendered and inspected; disposable rebuild text matches the supplied PDFs. |

## Mathematical claim audit

| Claim or result | Status | Independent basis | Limitations or issue |
|---|---|---|---|
| Displayed-tree parameterization | **verified** | Derived from the ten rooted arcs and all four retained-parent choices; descendant characters give the four terms of the printed theta map. | Uses the stated uniform stationary root and group-based kernels. |
| Exact strict-interior K2P collision | **verified** | Recomputed all 16 core identities, all 64 Fourier coordinates, all 64 inverse probabilities, literal retained-graph/star pruning, normalization, and exact minimum `1188799/79626240`. | None affecting the theorem. |
| K3P non-disjointness by inclusion | **verified** | K2P is exactly the K3P submodel `a_C=a_T`; substitution and mixture semantics are unchanged. | Inclusion alone does not give parameter-level K3P symmetry breaking, which the paper separately treats. |
| Exact K3P parameter-level symmetry breaking | **verified** | Recomputed the quartic reduction, all 16 factor identities, literal pruning, all 64 coordinates, and distinct nonidentity eigenvalues on `U`. | Its exact shared output is openly identified as globally relabelled K2P. |
| Edgewise continuous-time K2P result | **verified** | Independently checked the degree-six field, root isolation, every factor identity, stochasticity, `g>s^2` margins, probability enclosure, and rank minor. | Edge-specific generators/rate ratios only; no common generator or clock. |
| K2P rank, local locus, and 11-dimensional fibers | **verified** | Exact differentiation gives the printed nonzero rank-9 minor; the tree rank is six; dimensions are `20-9+6=17` and `20-9=11`. | None affecting the claim. |
| K3P rank, local locus, and 14-dimensional fibers | **verified** | Exact differentiation in the printed semantic order gives the stated rank-15 minor; the tree rank is nine; dimensions are 23 and 14. | None affecting the claim. |
| Nearby observably genuine K3P collisions | **verified conditional on stated assumptions** | The collision projection is a submersion; a local section exists; the finite union of relabelled-K2P tree strata is closed and nowhere dense; rank and parameter distinctness persist locally. | “Genuine” has the paper's explicit global-character-relabeling meaning. |
| Edgewise continuous-time K3P branch | **verified conditional on stated assumptions** | The exact tangent solves all 15 fixed-output equations; the only saturated rate margins have positive derivatives, while the remaining strict inequalities persist by openness. | Analytic/existential; no explicit radius or closed-form nearby point is claimed. |
| Dominance and Zariski-density corollary | **verified** | A nonzero full ambient Jacobian minor makes each complexified polynomial theta map dominant; full-rank real points in open chambers give Zariski-dense images. | Only in the stated normalized effective affine spaces; structural zeros, K2P symmetry, and inequalities remain. |
| One-blob arbitrary-taxon grafting theorem | **verified conditional on stated assumptions** | The same tensor product of three conditional Markov kernels preserves the common interface law. Root splitting, blob topology, strict CT, and equivariant injectivity check. | Exactly one theta insertion; not a multi-blob or four-terminal theorem. |
| Scope and relationship to prior literature | **verified conditional on the required citation above and a bounded search** | Primary sources confirm the formal v2 K2P results, their formal removal in v3, the open v3 questions, and all stated generic/full distinctions. | See Findings 1--2; a bounded search cannot prove worldwide or unpublished priority. |

## Supporting derivations

For a consistent Fourier label `x+y+z=A`, the four choices of retained parents
at `r2,r3` give the descendant sets

    ({2,3}, empty), ({2}, {3}), ({3}, {2}), (empty, {2,3})

below `u->p` and `u->q`. They yield the four core terms

    A2_y A3_z U_(y+z)
    A2_y B3_z U_y V_z
    B2_y A3_z V_y U_z
    B2_y B3_z V_(y+z)

with the four product inheritance weights. The root-suppressed leaf-1 edge
contributes `K_x^2`, while the remaining pendant factors contribute `K_y K_z`.
At the compact K2P point, every identity

    M_(y,z) = P_(y+z) R_y R_z

holds exactly, so the network coordinate factors into the comparison-star
coordinate. The other 48 Fourier coordinates vanish structurally. Exact
Fourier inversion and separately implemented state-space pruning agree in all
64 patterns.

For a K3P edge with nonidentity eigenvalues `a_C,a_G,a_T`, positive edgewise
rates are equivalent to

    a_C > a_G a_T,  a_G > a_C a_T,  a_T > a_C a_G,

together with positive eigenvalues. K2P reduces to `g>s^2`. The continuous-time
claims use this edge-by-edge criterion and do not infer a common generator or
clock.

For a submersion `F:P^d -> A^m` and an embedded tree germ of dimension `t`,
`F^{-1}(T)` has local dimension `d-m+t`, and a fixed-output fiber has dimension
`d-m`. This gives `(17,11)` for K2P and `(23,14)` for K3P. The printed K3P
tangent solves `J p'(0) + F_(U_C) + F_(V_G)=0`; its two saturated cone margins
move inward with positive derivatives. The analytic implicit-function
conclusion follows.

Finally, if `p=p'` is the common three-interface law, applying the same tensor
product conditional kernel to both sides preserves equality. Each attached JC
component map is injective because marginalizing to any one descendant leaf
gives an invertible path kernel. Equivariance then preserves the absence of all
global nonidentity-character transposition symmetries. This proves the
one-theta all-taxon statement without extrapolating from the finite four-leaf
regression.

## Code and certificate audit

### Claim-to-code map

| File or entry point | Mathematical claim tested | Method | Independence or blind spot |
|---|---|---|---|
| `materials/verify_k2p_simple.py` | Compact K2P field, rows, admissibility, factorization, patterns, minimum | Exact `Q(sqrt(71))` arithmetic and inverse Fourier transform | Consumes every stored row; shares the certificate as input. |
| `materials/verify_k2p_displayed_trees.py` | Literal K2P graph, four monomials, coordinates, patterns | Exact descendant sets plus separate ordinary-state Markov pruning | Hard-codes the canonical graph independently of the compact formula. |
| `materials/src/verify_k2p_extended.py` | Algebraic edgewise-CT K2P collision and source-order audit | Exact degree-six field, Sturm isolation, interval signs, Fourier and direct pruning | Later K2P modules reuse its arithmetic infrastructure. |
| `materials/src/verify_k2p_rank_family.py` | Rank-9/rank-6 minors, dimensions, exact family | Dual-number differentiation, exact elimination, direct orbit count | Selected minors certify rank; they do not symbolically classify every rank-drop locus. |
| `materials/src/verify_k2p_four_leaf_graft.py` | One four-leaf graft | Literal topology and all 256 Fourier/state probabilities | Regression only; the all-`n` theorem is proof-level. |
| `materials/src/verify_k3p.py` | Quartic field/topology, collision, direct pruning, rank, tangent, CT margins | Exact quartic arithmetic, canonical graph semantics, ordinary pruning, Bareiss elimination | Shares primitive edge values and group convention across the two calculation paths. |
| `materials/src/test_k3p_semantic_mutations.py` | Nine coordinated false-positive regressions | Disposable mutated certificates with required diagnostic failures | A regression suite, not a proof that no imaginable mutation can evade checking. |
| `materials/src/test_k2p_semantic_mutations.py` | Compact transition-row coverage | Disposable per-row certificate mutations | Focused on stored semantic rows. |
| `materials/src/verify_source_conventions.py` | Source coordinates and favorable-order factorization | Exact rational evaluation | Focused convention transcription, not a complete independent source implementation. |
| `materials/src/generate_k2p_simple_certificate.py` | Compact JSON reproducibility | Regenerates the complete compact certificate | A consistency oracle, not independent mathematics. |
| `materials/verify.py` | Complete mathematical suite | Subprocess orchestration with optimized-mode propagation | Orchestration rather than an independent derivation. |
| `RUN_REFEREE_REPLAY.sh` | Manifests, transcripts, regeneration, and PDF build checks | Fail-closed paths/hashes, normal/optimized replays, disposable builds | Internal consistency rather than external cryptographic authorship. |

### Exactness and coverage

No theorem-critical equality or sign decision relies on floating-point
arithmetic. The compact K2P checker works in `Q(sqrt(71))` with rational sign
bounds. The continuous-time K2P checker proves polynomial irreducibility,
isolates the intended real root by Sturm arithmetic, adjoins the required
square root, and certifies all relevant signs. The K3P checker works exactly in
the irreducible quartic field `5h^4-1=0`, isolates its positive real embedding,
and performs exact sign tests.

The verifier covers all 64 Fourier and ordinary-state coordinates for both
compact constructions and all 256 patterns in the four-leaf regression. Both
network rank minors and both tree-rank witnesses are rebuilt from exact
derivatives rather than trusted as stored nonzero scalars. The K3P tangent is
checked row by row. The direct K3P route constructs four-state transition
kernels, prunes each literal retained DAG, mixes them using the inheritance
weights, and separately prunes the star. It does not call the Fourier monomial
routine or consume stored pattern probabilities.

The canonical K3P schema is now enforced before dictionaries can erase
duplicates: exact ordered vertex rows, unique IDs and leaf labels, exact ten
arc IDs/endpoints/vector names, and each reticulation's referenced incoming
arc, parent, child, choice, and suppressed-vector semantics. Independent tests
confirmed that coordinated endpoint and ID swaps, duplicate vertex IDs,
descriptor contradictions, and mathematical-value corruptions all fail.

The remaining common-mode risks are ordinary ones: the packet supplies
certificate, verifier, and expected transcript from one release; source
convention checks target selected formulas; and selected full-rank minors do
not classify full degeneracy varieties. The clean-room reconstructions
materially reduce these risks for the actual claims.

## Execution record

All hostile mutations were made in disposable copies. The manifest-verified
`packet_copy/` was not changed.

| Command actually used | Exit status | Compared artifact | Result or divergence |
|---|---:|---|---|
| `bash ./RUN_REFEREE_REPLAY.sh --with-pdf` | 0 | Complete and focused transcripts, regenerated certificate, three rebuilt PDFs, manifests | Normal and optimized checks, regressions, mutation suites, rebuilds, and pre/post integrity all passed. |
| `tmp/sympy_env/bin/python notes/clean_room_symbolic_checks.py` | 0 | Manuscript formulas only | Compact K2P and quartic K3P factorizations, literal pruning, coordinates, minima, ranks, and tangent passed independently of packet code/JSON. |
| `python3 notes/independent_checks.py` | 0 | Manuscript formulas only | Rebuilt the compact and CT K2P claims, six-order sign point, family determinant, ranks, quartic K3P collision, and IFT tangent. |
| `python3 notes/adversarial_mutation_probe.py` | 0 | Disposable source/certificate copies | All 18 K3P and nine K2P semantic probes produced their expected substantive failures. |
| `python3 notes/integrity_failure_probes.py` | 0 | Disposable packet copies | Changed, added, missing, and symbolic-link paths were all rejected. |
| strict JSON duplicate-key load; Python compilation; shell syntax scan | 0 | Five JSON certificates and executable sources | All passed; no hidden duplicate object keys or syntax failure. |

## Negative controls

| Mutation | Expected failure | Observed failure | Interpretation |
|---|---|---|---|
| Global actual K3P `p/q` endpoint swap with descriptors left stale | Canonical arc mismatch | Rejected at exact arc schema | The principal v1.2.4 escape is closed. |
| Root-adjacent K3P arc-ID swap | Canonical ID/endpoint mismatch | Rejected at exact arc schema | Numerically invisible ID changes are semantically bound. |
| Duplicate/conflicting K3P `rho` vertex row | Duplicate vertex failure before map construction | Rejected as duplicate vertex ID | List uniqueness is checked before dictionary collapse. |
| Reticulation parent, choice, or referenced-arc contradiction | Relational descriptor mismatch | All rejected | Descriptor semantics resolve against canonical arcs. |
| K3P edge vector name, eigenvalue, Fourier coordinate, pattern, Jacobian, or tangent corruption | Operative mathematical mismatch | All rejected at the named layer | Stored values are consumed or independently recomputed. |
| Direct-pruning group operation XOR changed to cyclic addition | Fourier route passes but direct route fails | Rejected at first direct K3P pattern | Ordinary-state pruning is live and independent of Fourier inversion. |
| Each of six compact-K2P network rows mutated separately | Stored/recomputed row mismatch | All six rejected, including `K_odot_K` | Complete transition-row coverage is real. |
| Each of three compact-K2P tree rows mutated separately | Stored/recomputed row mismatch | All three rejected | Comparison-tree rows are also consumed. |
| Packet byte changed, file added, file removed, or symlink inserted | Integrity boundary failure | All four rejected | Driver fails closed on both contents and member set/type. |

These are substantive verifier or packet-boundary results, not instances where
a mathematical mutation was detected only through the original manifest.

## Literature, topology, and scope review

Version 2 contains the K2P trinet sign/disjointness Lemma 5.6 and the JC/K2P
global Corollary 5.8. Version 3 deletes the K2P lemma, makes the global result
JC-only, explains the leaf-order obstruction, and asks whether the high-level
trinet inequality extends to K2P/K3P. Finding 2 concerns only the surviving
stale Version 3 roadmap sentence and the manuscript's two broadest historical
phrases.

The level-one/generic-identifiability attributions agree with the primary
records. Gross--Long gives generic JC identifiability for large-cycle
networks; Gross et al. gives generic identifiability for triangle-free
level-one networks with fixed reticulation count under JC/K2P/K3P; the cited
dimension, 3-sunlet, and strongly tree-child level-two JC results have the
scopes stated. Finding 1 adds the closest omitted earlier level-two algebraic
study. A targeted primary-source search found no prior exact
stochastic-interior three-leaf tree--theta Kimura collision, continuous-time
strengthening, or local collision geometry of the claimed form.

The rooted network has exactly the ten arcs printed in equation (2). Root
suppression produces the three internally disjoint `p--q` paths through
`u,r2,r3` and the stated pendant attachments. The core is a strict level-two
nontrivial 3-blob. The no-tree-child-rooting proof is correct: the fixed
reticulation edges exhaust both outgoing slots at `p` and `q`, forcing the
remaining core directions and leaving each with only reticulation children.

The paper consistently excludes a JC collision, generic theta/tree
equivalence, genuine four-terminal blobs, multi-blob composability, common-Q
or clock conclusions, and an unrestricted nonreversible semi-directed result.
Those limitations agree with the proofs.

## PDF and presentation audit

The replay rebuilt all three PDFs in disposable directories and obtained
layout-preserving extracted text identical to the supplied files. All 24
supplied pages were also rendered and inspected individually.

- Main manuscript: 20/20 pages passed. Figure 1 labels are separated and
  unambiguous. Equations, the small page-13 tangent table, citations, and
  references remain readable; there is no clipping, overflow, unresolved
  reference, missing glyph, or broken page flow.
- Technical summary: 2/2 pages passed. The literal ten-arc topology, witness,
  determinant, and proof-diagnosis material are legible.
- Displayed-tree clarification: 2/2 pages passed. Both retained-tree tables and
  the factorization are complete and legible.

All three PDFs are untagged. If the journal or repository requires accessible
PDFs, semantic tagging and alternative descriptions for the topology figure
and dense tables should be added. This is optional for the scientific
submission reviewed here.

## Required corrections

Before submission:

1. Cite Ardiyansyah (2021), describe its restricted simple/semisimple
   level-two JC/K2P/K3P variety results, and distinguish them from the present
   pointwise three-leaf collision.
2. Rebuild the paper and update the versioned packet hashes after that text
   change. The mathematical certificates and verifiers need no change.

Optional only: qualify the abstract and acknowledgment with “formal K2P lemma
and corresponding global corollary”; add strict duplicate-key/schema handling;
add source-coupling assertions for the printed continuous-time determinant and
six-order invariant values; add PDF tags/alternative text; and, if desired,
identify the stale roadmap sentence in a footnote.

## Unreviewed items, limitations, and confidence

- Novelty was checked against the cited and readily searchable primary record,
  not every unpublished manuscript or private result.
- The exact K3P strict-continuous-time point is existential through the
  analytic implicit-function theorem; no explicit radius is provided or
  needed for the stated claim.
- The all-taxon theorem is proof-level. The supplied four-leaf calculation is
  a regression, not exhaustive finite evidence for arbitrary `n`.
- A local and remote tag corroborate repository provenance but do not provide
  a signed external attestation. The packet states this limitation correctly.
- Informational certificate prose was inventoried rather than treated as an
  independent premise.

Confidence is **high** in the mathematical assessment, **very high** in the
bounded computational/reproducibility assessment, and **high** that the sole
required change is a minor literature-completeness correction rather than a
substantive defect.

## Final recommendation

The central theorem, witnesses, proofs, computations, and revised assurance
claims are sound. Submission should wait only for the Ardiyansyah citation and
context sentence; after that change I would recommend acceptance.

MINOR REVISION
