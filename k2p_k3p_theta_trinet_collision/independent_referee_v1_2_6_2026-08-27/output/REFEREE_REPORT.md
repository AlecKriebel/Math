# Independent referee report

## Review environment

- **Reviewer:** OpenAI Codex, GPT-5-based independent reviewer; the exact
  runtime build identifier is not exposed. Separate paper-first mathematical,
  code/certificate, literature/layout, and hostile-synthesis lanes were used.
- **Date:** 27 August 2026, America/Los_Angeles.
- **Submission:** `k2p-k3p-theta-ai-referee-v1.2.6.zip`; main article
  `materials/combined-paper-clarified.pdf` (20 pages), followed only after the
  paper-first pass by two support PDFs (2 pages each).
- **Archive:** SHA-256
  `f35d5b8ef06870444b20c6572c9676155aacc9d2df214889706f48c9bb07c150`.
  The ZIP has 48 entries (44 regular files and four directories), no symbolic
  links, and no absolute or parent-traversing paths.
- **Integrity and provenance:** all 43 manifest-covered paths passed before
  and after the clean replay. All 38 packet files under `materials/` are
  byte-identical to the stated canonical repository subtree at commit
  `672d96a08be174cd6b67762a6907dfbdcd926b9b`. The local and remote annotated
  tag `k2p-k3p-theta-v1.2.6` both peel to that commit. The tag is unsigned, as
  the packet accurately disclaims.
- **System:** macOS 26.5.2, build 25F84; Darwin 25.5.0 arm64; Python 3.14.6;
  Tectonic 0.16.9; Poppler `pdftotext`/`pdftoppm` 26.08.0; SymPy 1.14.0 in an
  audit-local environment.
- **Primary literature checked:**
  [Brits et al. Version 2](https://arxiv.org/html/2607.12919v2),
  [Brits et al. Version 3](https://arxiv.org/html/2607.12919v3),
  [Ardiyansyah (2021)](https://arxiv.org/html/2104.12479v1),
  [Gross--Long (2018)](https://doi.org/10.1137/17M1134238),
  [Gross et al. (2021)](https://doi.org/10.1007/s00285-021-01653-8),
  [Gross--Krone--Martin (2024)](https://doi.org/10.1007/s11538-024-01314-z),
  [Cox--Gross--Martin (2025)](https://doi.org/10.1007/s11538-025-01506-1),
  and [Englander et al.](https://doi.org/10.1101/2025.04.18.649493).

## Executive assessment

The manuscript constructs exact three-taxon distributions shared by a
comparison tree and a binary semi-directed strict level-two theta network
under K2P and K3P. Beyond the compact `Q(sqrt(71))` collision, it gives an
edgewise strictly continuous-time K2P witness, an exact quartic K3P network
parameter outside every globally character-relabelled K2P parameter stratum,
full ambient-rank certificates, local collision loci and fibers, an analytic
continuous-time K3P branch, Zariski-density consequences, and a one-blob
grafting theorem for every labelled binary-tree topology.

I found no false theorem, incorrect witness, arithmetic error, hidden topology
change, missing analytic implication, verifier false positive affecting an
operative value, literature misstatement, or presentation defect requiring a
revision. A fresh clean-room program that imports no packet source and reads no
packet certificate reconstructed the central exact calculations directly from
the manuscript. It reproduced the compact and continuous-time K2P collisions,
the quartic K3P collision, literal pruning, positivity, rank minors, local
dimension inputs, and the K3P tangent. The complete packet replay passed in
normal and optimized modes, regenerated the compact certificate byte for byte,
and rebuilt all three PDFs with identical extracted text.

The v1.2.6 repairs are effective. Every certificate is now parsed with
duplicate-key rejection and a packet-specific closed structural schema. An
independent hostile harness rejected 81 operative or integrity mutations,
including deep duplicate keys in every certificate type, nonstandard numeric
constants, `1e999`, every compact-K2P transition row, all ten K3P arc
endpoints, every reticulation parent/choice relation, all K3P transition rows,
and coordinated embedded/sidecar Jacobian and tangent changes. Three
same-shape mutations of fields declared informational were accepted, which is
the intended and accurately documented boundary.

The previously missing Ardiyansyah citation is now present and correctly
distinguishes that paper's restricted nice-network variety results from the
present non-nice three-leaf pointwise collision. The Version 2-to-3 wording now
literally identifies the removed formal K2P lemma and K2P portion of the global
corollary. I therefore recommend acceptance.

## Findings ordered by severity

### No actionable finding

No fatal, major, minor, mathematical, computational, citation, topology, or
layout correction is required before submission.

The following are optional hardening or production observations only:

1. All three PDFs are visually clean but untagged and not linearized. Semantic
   tagging may be useful if the target journal requires accessible PDFs.
2. The supplied compact-K2P mutation regression corrupts `K_odot_K`; the
   verifier itself consumes all nine stored network/tree transition rows, and
   the independent harness confirmed this by corrupting each row. Expanding
   the maintained regression to all nine rows would document that coverage
   more visibly but is not needed for correctness.
3. If a future certificate schema admits JSON floating-point primitives, the
   strict loader could add a finite `parse_float` policy. Every present numeric
   JSON primitive is an integer; consequently the valid JSON token `1e999`
   changes primitive type and is rejected by the present schema.
4. A signed tag or externally anchored checksum could authenticate authorship.
   The current unsigned manifest and tag establish internal identity, and the
   packet expressly avoids claiming more.

## Audit of the advertised v1.2.6 repairs

| Advertised repair | Verdict | Evidence |
|---|---|---|
| Strict parsing for all five JSON inputs | **repaired** | Every operative load uses `load_canonical_certificate`; duplicate keys at every depth and `NaN`/`Infinity` constants fail. Unregistered basenames fail before parsing. |
| Closed structural schemas | **repaired** | All five independently recomputed shape fingerprints match. Added, removed, renamed, type-changed, or heterogeneous-row-shifted fields fail closed. |
| Coordinated K3P shadow routes | **repaired** | Sidecars are independently schema-checked and must equal embedded sections. Coordinated embedded/sidecar determinant, matrix, descriptor, pivot, and tangent mutations still fail semantic reconstruction. |
| Compact-K2P row coverage | **verified** | Separate mutations of all six network/effective rows and all three tree rows fail, including `K_odot_K`. |
| Coverage inventory | **verified** | It correctly separates recomputation/semantic binding, structural closure, informational values, transport mirrors, and unsigned integrity. |
| Literature and history wording | **repaired** | The Ardiyansyah scope and Version 2/3 formal-result history agree with the primary sources. |
| Twenty-four submitted pages | **verified** | All pages were rendered and inspected; all are clean and readable. |

## Mathematical claim audit

| Claim or result | Status | Independent basis | Limitations or issue |
|---|---|---|---|
| Displayed-tree parameterization | **verified** | Derived from the ten rooted arcs and four retained-parent choices; literal ordinary-state pruning agrees with Fourier inversion. | Uses the stated uniform stationary root and group-based kernels. |
| Exact strict-interior K2P collision | **verified** | Recomputed all 16 core identities, all 64 Fourier coordinates and patterns, transition rows, normalization, positivity, and exact minimum `1188799/79626240`. | None affecting the theorem. |
| K3P non-disjointness by inclusion | **verified** | K2P is the K3P specialization `a_C=a_T`; likelihood, stochasticity, and the edgewise continuous-time inequalities are preserved. | Inclusion does not itself give parameter-level symmetry breaking, which is treated separately. |
| Exact K3P parameter-level symmetry breaking | **verified** | Recomputed the quartic factorization, all coordinates and patterns, direct pruning, and the three distinct nonidentity eigenvalues on `U`. | The exact shared output is openly identified as globally relabelled K2P. |
| Edgewise continuous-time K2P result | **verified** | Independently isolated the intended cubic root, reduced every factor identity, checked all stochastic/`g>s^2` inequalities, probability bounds, and rank minor. | Edge-specific generators and rate ratios; no common generator or clock. |
| K2P rank, local locus, and 11-dimensional fibers | **verified** | Exact differentiation gives the printed nonzero rank-9 minor; tree rank is six; dimensions are `20-9+6=17` and `20-9=11`. | A local result, not a classification of the global singular locus. |
| K3P rank, local locus, and 14-dimensional fibers | **verified** | Exact differentiation in the printed order gives the stated rank-15 determinant; tree rank is nine; dimensions are 23 and 14. | Same global-singular-locus limitation. |
| Nearby observably genuine K3P collisions | **verified conditional on stated assumptions** | The collision projection is a submersion; a local section exists; the finite union of transposition-fixed K2P tree strata is closed and nowhere dense; rank and `U`-edge distinctness persist. | “Genuine” has the manuscript's explicit global-character-relabeling meaning. |
| Edgewise continuous-time K3P branch | **verified conditional on stated assumptions** | The printed tangent solves all 15 fixed-output equations; the two saturated rate margins have positive derivatives and all remaining inequalities persist by openness. | Analytic/existential; no explicit radius or closed-form nearby point is claimed. |
| Dominance and Zariski-density corollary | **verified** | A full ambient Jacobian minor makes each complexified polynomial theta map dominant; full-rank physical points give real open image sets and hence Zariski density. | Only in the stated normalized effective affine spaces; model symmetries and inequalities remain. |
| One-blob arbitrary-taxon grafting theorem | **verified** | The same tensor product of three conditional Markov kernels preserves the interface equality. Root splitting, binary/level-two topology, continuous time, and equivariant injectivity all check. | Exactly one theta insertion; no multi-blob or genuine four-terminal theorem. |
| Scope and relationship to prior literature | **verified conditional on a bounded search** | Primary records confirm the level-one/generic distinctions, the restricted level-two classes, and the current Version 3 questions. | A bounded referee search cannot establish worldwide or unpublished priority. |
| Ardiyansyah/version-history contextualization | **verified** | Ardiyansyah Lemma 5.1 excludes two- and three-leaf simple strict level-two networks from the nice class; Versions 2/3 match the manuscript's formal-result wording. | Version 3 retains one stale roadmap sentence, but the manuscript no longer overstates its removal. |
| Strict JSON and closed-schema enforcement | **verified for the five packet schemas** | Independent fingerprint recomputation plus raw/schema/semantic mutations confirm the claimed behavior and documented informational boundary. | Structural hashes intentionally do not authenticate values; mathematical verifiers and the packet manifest supply separate checks. |

## Supporting derivations

For a consistent Fourier label `x+y+z=A`, the four choices of retained parents
at `r2,r3` give the descendant sets

    ({2,3}, empty), ({2}, {3}), ({3}, {2}), (empty, {2,3})

below `u->p` and `u->q`. They yield the four core terms

    A2_y A3_z U_(y+z)
    A2_y B3_z U_y V_z
    B2_y A3_z V_y U_z
    B2_y B3_z V_(y+z)

with the four product inheritance weights. Root suppression contributes the
effective leaf-1 edge; at the symmetric witness its vector is `K odot K`.
The compact factorization `M_(y,z)=P_(y+z)R_yR_z` therefore turns every
consistent network coordinate into the comparison-star coordinate, while the
other 48 Fourier coordinates vanish structurally. Exact inversion and an
independent retained-DAG pruning calculation agree in all 64 patterns.

For a K3P edge with nonidentity eigenvalues `a_C,a_G,a_T`, positive symmetric
edgewise rates are equivalent to positivity of the eigenvalues and

    a_C > a_G a_T,  a_G > a_C a_T,  a_T > a_C a_G.

K2P reduces to `g>s^2`. These are edgewise conditions only. At the quartic
K3P point, the two equalities that lie on the rate-cone boundary move inward
with derivatives `(21-20h^2)/19>0` and `1`; the exact tangent simultaneously
keeps all 15 output coordinates fixed.

For a submersion `F:P^d -> A^m` and an embedded tree germ of dimension `t`,
`F^{-1}(T)` has local dimension `d-m+t`, while each fixed-output fiber has
dimension `d-m`. This gives `(17,11)` for K2P and `(23,14)` for K3P. The same
surjectivity gives local sections over the tree model. Finally, applying the
same tensor product conditional kernel to equal three-interface laws preserves
equality, which proves the one-theta arbitrary-taxon theorem without
extrapolating from the finite four-leaf regression.

## Code and certificate audit

### Claim-to-code map

| File or entry point | Mathematical claim tested | Method | Independence or blind spot |
|---|---|---|---|
| `materials/verify_k2p_simple.py` | Compact K2P field, rows, admissibility, factorization, patterns, minimum | Exact `Q(sqrt(71))` arithmetic and inverse Fourier transform | Consumes every stored row; certificate is an input. |
| `materials/verify_k2p_displayed_trees.py` | Literal K2P graph, four monomials, coordinates, patterns | Descendant sets plus ordinary-state Markov pruning | Hard-codes the canonical graph independently of the compact formula. |
| `materials/src/verify_k2p_extended.py` | Algebraic edgewise-CT K2P collision and source-order audit | Exact algebraic field, Sturm isolation, sign intervals, Fourier and pruning | Later K2P code reuses some arithmetic infrastructure. |
| `materials/src/verify_k2p_rank_family.py` | Rank-9/rank-6 minors, dimensions, exact family | Exact dual-number differentiation and elimination | Selected minors certify rank; they do not classify every rank-drop locus. |
| `materials/src/verify_k2p_four_leaf_graft.py` | One four-leaf graft | Literal topology and all 256 Fourier/state probabilities | Regression only; the all-`n` theorem is proof-level. |
| `materials/src/verify_k3p.py` | Quartic field/topology, collision, pruning, rank, tangent, CT margins | Exact quartic arithmetic, canonical graph semantics, retained-DAG pruning, Bareiss elimination | Shares primitive edge values/group convention across calculation paths. |
| `materials/src/test_k3p_semantic_mutations.py` | Ten K3P semantic false-positive regressions | Disposable coordinated certificate mutations | Finite regressions, not an exhaustive mutation proof. |
| `materials/src/test_k2p_semantic_mutations.py` | `K_odot_K` stored-row coverage | Disposable certificate mutation | Maintained suite is focused; independent harness tested all nine rows. |
| `materials/src/test_json_schema_mutations.py` | Raw JSON and closed-schema behavior | Disposable duplicate/unknown/type/sidecar mutations | Covers representative cases; independent harness broadened them. |
| `materials/strict_json.py` | Unique parse and packet-specific structure | Duplicate-key hook, constant rejection, structural fingerprints | Values are deliberately outside the structural hash. |
| `materials/src/verify_source_conventions.py` | Five cited coordinates and favorable-order factorization | Exact rational evaluation | Focused convention check, not a full independent source implementation. |
| `materials/src/generate_k2p_simple_certificate.py` | Compact JSON reproducibility | Regenerates the complete compact certificate | Consistency aid, not independent mathematics. |
| `materials/verify.py` | Complete mathematical suite | Checked subprocess orchestration with optimized-mode propagation | Orchestration, not an independent derivation. |
| `RUN_REFEREE_REPLAY.sh` | Paths/hashes, transcripts, generator, PDFs | Fail-closed manifest set, normal/optimized replays, disposable builds | Internal consistency, not external cryptographic authorship. |

### Exactness and coverage

No theorem-critical equality or sign decision depends on floating-point
arithmetic. The compact K2P verifier works in `Q(sqrt(71))`. The continuous-
time K2P verifier proves the relevant polynomial properties, isolates the
intended real root by Sturm arithmetic, adjoins `sqrt(1423)`, and certifies the
needed signs. The K3P verifier works in the exact quartic field defined by
`5h^4=1` and isolates its positive real embedding. Floating conversion is used
only in displayed diagnostics.

The suite covers all 64 Fourier and ordinary-state coordinates for both
compact constructions and all 256 patterns in the four-leaf regression. Both
network rank minors and tree-rank witnesses are rebuilt from exact derivatives.
The K3P tangent is checked row by row. Direct pruning constructs four-state
transition kernels, evaluates each literal retained graph, mixes by the
inheritance weights, and separately prunes the comparison star; it does not
call the Fourier monomial routine.

The closed-schema layer is structural rather than mathematical by design.
Object keys, nesting, primitive types, array lengths, and heterogeneous-array
shape multiplicities are fingerprinted. Duplicate keys are rejected before
dictionary collapse. The semantic layer then binds ordered vertices, all ten
arc IDs/endpoints/vectors, reticulation relations, transition rows, coordinates,
probabilities, Jacobian descriptors/matrix/determinant, and tangent data.
Sidecar equality is correctly described as transport consistency, not an
independent theorem check. Informational strings may vary within the same
shape, and the coverage inventory says so.

## Execution record

All mathematical and certificate mutations were made in disposable copies.
The manifest-covered packet was restored to and left in its submitted state.

| Command or check actually used | Exit status | Compared artifact | Result or divergence |
|---|---:|---|---|
| `bash ./RUN_REFEREE_REPLAY.sh --with-pdf` (clean run) | 0 | Complete/focused transcripts, regenerated certificate, three rebuilt PDFs, opening/closing manifests | All checks passed. |
| Initial concurrent replay | 1 | Closing manifest path set | Correctly rejected one audit-generated `.pyc` that appeared after the opening check; the cache was moved out and the clean run above passed. |
| `.../sympy_env/bin/python notes/independent_math_checks.py` | 0 | Manuscript formulas only | Both K2P witnesses, quartic K3P, literal pruning, minima, ranks, tangent, topology, and dimensions passed independently of packet code/JSON. |
| `python3 notes/code_mutation_harness.py` | 0 | Disposable certificate/source/packet copies | 81 operative/integrity mutations rejected; three declared-informational changes accepted as expected. |
| Independent five-file schema-fingerprint recomputation | 0 | Hard-coded schema hashes | All five exact matches. |
| Unregistered-basename strict-loader probe | 0 | Loader registration boundary | Rejected with `no closed JSON schema registered`. |
| Python compilation and shell syntax checks | 0 | All Python/shell entry points | Passed; no hidden optimized-mode `assert` dependency in packet verifiers. |
| Local/remote tag peel and 38-file Git blob comparison | 0 | Claimed canonical commit/subtree | Exact identity passed; tag is unsigned. |

## Negative controls

| Mutation family | Count | Expected/observed behavior | Interpretation |
|---|---:|---|---|
| Duplicate keys, unknown fields, `NaN`/infinities, and `1e999` across all certificate types | 19 | All rejected at strict parse or closed schema | The revised raw-JSON boundary is live. |
| Every compact-K2P stored transition row, endpoint/weight, and independent-pruning group law | 12 | All rejected at the corresponding semantic layer | Complete compact-row and direct-pruning coverage is real. |
| Ten K3P endpoints; eight reticulation relations; vertex uniqueness; all parameter/tree/suppressed rows; Jacobian/tangent/coordinate/pattern data; pruning law | 45 | All rejected, including coordinated embedded/sidecar changes | K3P structure and mathematical values are not protected merely by self-consistency. |
| Changed/added/missing file, symlink, extra directory | 5 | All rejected before mathematics | The driver fails closed on bytes, path set, type, and directory set. |
| Three declared-informational same-shape value changes | 3 expected passes | All accepted | Matches the inventory; underlying mathematics is separately recomputed. |

The source-level pruning mutations are particularly useful: replacing Klein
XOR by cyclic addition leaves the Fourier route unchanged but causes the
ordinary-state route to disagree. This demonstrates genuine independence at
the group-law implementation layer.

## PDF and presentation audit

All 20 article pages and all four support-document pages were read and visually
inspected at rendered original detail. No clipping, overlap, missing glyph,
broken equation/reference, unresolved citation, unreadable table, or figure
ambiguity was found. Figure 1 agrees with the literal ten-arc DAG and the
nine-edge suppressed semi-directed network. The page-14 tangent table is
compact but crisp. Fonts are embedded/subsetted and text extraction succeeds.

The disposable build reproduced the extracted text of all three supplied PDFs.
The support documents agree with the article's graph, factors, dimensions, and
scope. The lack of semantic PDF tags and linearization is advisory only.

## Required corrections

None.

## Unreviewed items, limitations, and confidence

- The novelty search was bounded to the cited and directly adjacent primary
  literature; it cannot rule out unpublished or poorly indexed work.
- The unsigned tag and co-distributed manifest do not authenticate authorship.
- Selected nonzero minors establish the ranks needed here but do not classify
  global singular or rank-drop loci.
- The K3P continuous-time point is established locally by the analytic
  implicit-function theorem; no numerical radius is supplied or needed.
- The arbitrary-`n` theorem is proof-level and inserts one theta blob. The
  finite four-leaf computation is only a regression.

Confidence is **high** in the exact mathematical and computational assessment,
and **moderate to high** in the bounded literature/priority assessment.

## Final recommendation

**ACCEPT**

The proof and finite implementation were independently audited; every central
claim was established, the revised assurance boundary survived broad hostile
testing, and no correction affecting correctness, reproducibility, scope, or
clear interpretation remains.
