# Certificate and replay coverage

This inventory states what the executable replay establishes and, just as
importantly, what it does not establish. It applies to version 1.2.6 of the
package.

## Meanings used here

- **Recomputed or semantically bound** means that a verifier derives the value
  from the stated graph, formulas, or exact arithmetic and compares it with the
  certificate, or checks an exact descriptor needed to give a computation its
  advertised mathematical meaning.
- **Consistency only** means that two supplied copies are compared bytewise or
  structurally. Agreement is useful for transport and regression, but neither
  copy is an independent oracle for the other.
- **Informational** means descriptive prose or redundant display metadata that
  is not itself a machine-checked premise. No manuscript conclusion relies on
  such a field without a separately recomputed mathematical check or a proof in
  the manuscript.

Passing the replay is evidence about the executed source and certificate. An
unsigned manifest carried inside the same archive establishes internal path
and byte consistency; it does not authenticate the archive's author or supply
an external cryptographic trust anchor.

Before any mathematical field is used, `strict_json.py` gives each raw
certificate a unique interpretation: duplicate object keys at any depth and
nonstandard `NaN`/infinite constants are rejected. It then compares a
hard-coded SHA-256 fingerprint of the parsed key/container structure, array
lengths, and primitive JSON types. Thus added, removed, or structurally altered
fields fail closed, including informational fields; the fingerprint deliberately
does not substitute for the semantic and mathematical checks catalogued below.

## Coverage by certificate

| File | Recomputed or semantically bound | Informational or redundant display fields |
|---|---|---|
| `certificate_k2p_simple.json` | The number field and positive embedding; rooted/suppressed theta topology used by the graph replay; exact edge eigenvalues and every stored transition row, including the composed `K_odot_K` row; inheritance weights; comparison-tree parameters; all displayed core terms and the factorization; all 64 Fourier coordinates and all 64 ordinary-state probabilities; normalization, positivity, the minimum probability, and the zero invariant; selected rank-9 and rank-6 minors; the K2P orbit-derived ambient dimension, tree dimension, 20-dimensional parameter count, 17-dimensional collision locus, 11-dimensional fixed-output fiber, and the two-equation six-dimensional symmetric family. | `schema_version` and `title`; `semi_directed.root_suppression`; the stored semi-directed reticulation names (their count is used); `factorized_matrix` and `invariant_Q` are redundant stored displays whose mathematical equalities are recomputed elsewhere; the rank `rows`/`columns` and human-readable factored determinant string are descriptive copies of hard-coded executable selections; `symmetric_collision_family.edge_meaning`; the two equation strings are checked for count while their mathematical formulas are implemented explicitly; and redundant topology prose not used by a focused entry point. The compact-certificate generator is a reproducibility aid, not an independent oracle for literal metadata that it emits. |
| `certificate_k2p_continuous_time.json` | The degree-six field construction and isolating intervals; rooted topology, edge placement, mixing weights, network/tree vectors, and core factors; strict stochastic and edgewise continuous-time inequalities; all exact collision coordinates and ordinary-state probabilities; the induction-order sign audit; and the independent all-six-order negative point. | `title` and explanatory labels. The mathematical content of the remaining top-level sections is consumed by `src/verify_k2p_extended.py`. |
| `certificate_k3p.json` | A closed top-level key set and schema version; Klein-group order, indices, addition convention, and character table; quartic field labels, basis/encoding, relation, and isolating interval; the canonical ordered vertex/type/leaf-label schema; the complete ten-arc ID-to-endpoint-to-vector map; exact ordered reticulation choices resolved relationally against their referenced arcs; source-to-suppressed-edge bindings; theta topology; parameter vectors and transition rows; comparison tree and all root-splitting claims; ansatz residuals; all four graph-derived switching terms and 16 factorization identities; all 64 Fourier coordinates and all 64 pattern probabilities; direct ordinary-state pruning of every retained graph and the comparison tree; parameter- and output-level K2P symmetry statements; the exact ordered 15-column Jacobian descriptor map, matrix, determinant, rank, tree rank, and dimension arithmetic; the exact free and pivot tangent descriptors, fixed-output identity, strict-rate margins, and automatically differentiated formerly saturated margin derivatives. | `title`; explanatory strings in `construction_ansatz.form`, `construction_ansatz.interpretation`, `core_factorization.identity`, `root_suppression.composition_rule`, `field.generator_value`, and `field.representation`; Jacobian display prose such as `number_field`, `output_space`, `ambient_space`, `determinant_formula`, and `zariski_closure`; and continuous-time display prose such as `method`, `certificate_scope`, `number_field`, `eigenvalue_formulas`, `closed_form_witness_boundary_equalities`, and `U_margin_derivative_formula`. The associated determinant, dominance, dimension, and margin claims are recomputed or proved separately. |
| `jacobian_certificate_k3p.json` and `continuous_time_certificate_k3p.json` | No additional independent mathematics. Their mathematically operative fields are checked through the embedded sections of `certificate_k3p.json`, subject to the informational-field qualifications above and below. | These are human-sized transport mirrors. The verifier requires exact structural equality with the corresponding embedded sections. |

Within the now closed structural schema, the K3P informational column is
intentionally inclusive: any currently allowed descriptive or redundant field
not explicitly named in the recomputed column is informational. In particular,
this includes
`root_suppression.new_edge`; the descriptive portions of `theta_core`,
`literal_two_sub_blob_audit`, and `degree_two_suppressible_audit` (their
mathematical counts and incidence conclusions are recomputed); ansatz
`forced_relations`; Jacobian `determinant_denominator` and `sign`; the tree-rank
`block_determinant_formula` and `positive_parameter_recovery` prose; and the
stored `linearized_fixed_output_identity` display. The verifier independently
reconstructs the determinant sign, tree rank, and every row of the tangent
identity used by the manuscript; the positive tree-recovery formulas are
proved in the manuscript.

The K3P verifier additionally rejects coordinated label/column/pivot
permutations, free-direction relabellings, reticulation-order changes,
source-edge reassignments, actual endpoint relabellings, root-arc ID swaps,
duplicate vertex identifiers, descriptor/arc contradictions, and unknown
top-level fields. The compact K2P test separately rejects corruption of the
stored `K_odot_K` transition row. `src/test_json_schema_mutations.py` adds raw
duplicate-key, nonstandard-constant, unknown-field, nested-record, and
coordinated sidecar/schema regressions for all five JSON inputs. These tests,
together with `src/test_k3p_semantic_mutations.py` and
`src/test_k2p_semantic_mutations.py`, run as part of `verify.py` in both normal
and optimized replay modes.

## Other replay artifacts

- `verification_report_*.txt` files are deterministic regression transcripts.
  They are compared with fresh output by the release builder, but transcript
  agreement is not a second calculation.
- The canonical package's `manifest.sha256` covers its intended release files.
  A generated release archive additionally carries `FILE_SHA256SUMS`, while
  checksum sidecars accompany the ZIP and tarball outside those archives. A
  referee handoff instead carries `PACKET_SHA256SUMS` and a ZIP checksum
  sidecar. Each detects path or byte changes relative to its listed values;
  when distributed with the covered files and without an external signature,
  it establishes self-consistency rather than external authentication.
- `src/verify_source_conventions.py` independently evaluates the five stated
  coordinates and favorable-order factorization at exact rational test values.
  It is a focused convention check, not a complete symbolic transcription of
  the cited source paper.
- `src/verify_k2p_four_leaf_graft.py` is an exact 256-pattern regression for one
  four-leaf graft. The theorem for all labelled binary trees and all
  `n >= 3` is proved by the common-kernel lemma, not inferred from this finite
  test.
- The local-section, implicit-function, constant-rank, Zariski-density, and
  arbitrary-taxon conclusions combine the certified finite algebra with the
  explicit analytic proofs in the manuscript. They are not claims that a
  finite transcript alone proves those general theorems.

The authoritative way to reproduce the finite checks is to inspect the source
and run `python3 verify.py`; the reports and sidecars are conveniences for
audit and transport.
