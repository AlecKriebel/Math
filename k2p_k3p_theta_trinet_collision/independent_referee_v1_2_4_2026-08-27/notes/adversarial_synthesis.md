# Final hostile synthesis: v1.2.4

Date: 2026-08-27 (America/Los_Angeles)

## Disposition

**MINOR REVISION before submission.** I found no counterexample to a theorem,
no wrong witness, no false determinant or tangent, and no defect in the new
ordinary-state K3P calculation. The mathematical, literature, history,
ten-arc, inventory-scoping, and layout repairs withstand review. The remaining
defect is localized but real: v1.2.4 still does not completely bind the
certificate's graph identifiers and reticulation-parent descriptors to the
actual arc endpoints, despite the manuscript's broader semantic-binding
assurance.

This is not **major revision** because the unmodified v1.2.4 certificate is
manually canonical and internally consistent, the central calculations were
independently reconstructed, and every mutation I found that changes the
non-isomorphic parameterized network was rejected. It is not yet **accept**
because passing mutations can make advertised operative graph descriptors
false while the verifier prints `ALL K3P CHECKS PASSED`.

## Exact surviving mutations

All commands below used
`python3 packet_copy/materials/src/verify_k3p.py <mutated-certificate>` from the
audit directory, with unchanged matching sidecars where applicable.

1. **Root-arc identifier swap: exit 0.** Swapping only the `id` strings
   `e_rho_1` and `e_rho_u` makes the row named `e_rho_1` describe
   `rho -> u`, not `rho -> 1`. The verifier still passes. Its canonical
   Jacobian descriptor then says `e_rho_1.a_C` while differentiating the other
   root arc. This is numerically invisible at the witness because both arcs
   carry `K`, and on zero-sum Fourier coordinates their derivative columns
   coincide. The rank remains true, but the claimed endpoint semantics are not
   certified.

2. **Global internal `p <-> q` endpoint swap with stale descriptors: exit 0.**
   Swapping the actual endpoints/directions of `e_u_p/e_u_q` and all four
   `p/q -> r_j` arcs in the rooted and suppressed graph, while leaving the
   canonical reticulation rows saying (for example) that `e_p_r2` has parent
   `p` and choice `p`, passes every check. This is an internal graph
   automorphism, so it does not falsify the distribution, determinant, or
   theorem. It does prove that the exact ordered reticulation descriptor is
   compared to a hard-coded object but never cross-checked against the arc
   endpoint it purports to describe.

3. **Conflicting duplicate vertex: exit 0.** Inserting an extra first row
   `{id: "rho", type: "leaf", label: 99}` before the valid `rho` root row
   passes. The parser first collapses vertex rows into a dictionary; the later
   `len(self.nodes) == len(set(self.nodes))` test is therefore tautological.
   A malformed, contradictory vertex table can consequently receive the
   printed `rooted binary DAG` pass. An identical duplicate also passes.

Changing leaf `1`'s stored label to `2` likewise passes because leaf positions
are hard-coded rather than read from the vertex rows. Under the inventory's
inclusive K3P informational convention this can be treated as informational
metadata, but then that status should be made explicit; binding the three
labels is simpler.

The mutations are reproducible in `notes/adversarial_mutation_probe.py`; the
code agent's preserved copies of the first two structural cases are under
`packet_mutations/code_agent/`.

## Evidence that the gap is bounded

- The supplied five semantic negative tests passed in both normal and `-O`
  mode. In particular, the former coordinated Jacobian column/descriptor/pivot
  cycle, free-direction relabelling, reticulation-list reversal,
  root-suppression source reassignment, and unknown top-level field are now
  rejected for their intended diagnostics.
- Swapping only the actual `r2` parent endpoints, swapping only the
  `u -> p/u -> q` endpoints, or swapping the `r2` edge-ID meanings all exited
  1 at an exact collision equality. These non-global mutations change the
  parameterized likelihood rather than merely rename an internal automorphism.
- Mutating only direct pruning from Klein XOR to cyclic addition mod 4 exited
  1 at `direct K3P network/tree probability at AAA`. The direct state-space
  path is live, loops over all four retained choices and all 64 patterns, and
  does not call the Fourier likelihood routine. Sharing the primitive graph,
  edge eigenvalues, and inheritance parser is appropriate rather than a
  common-mode circularity.
- The unmodified certificate has nine distinct vertex IDs, leaf labels
  `1,2,3`, the correct two root ID/endpoints, and reticulation `parent` strings
  matching the actual incoming arc endpoints. Thus the defect concerns what
  the verifier establishes under mutation, not the truth of the shipped
  witness.
- The independent mathematical audit reconstructed the K2P/K3P collisions,
  rank minors, K3P tangent, local geometry, dominance, and graft argument and
  found no mathematical error. The primary-source/layout audit found the
  literature attribution, Version 3 wording, literal ten-arc description, and
  figure spacing repaired.

## Required bounded repair

Before submission, make the graph semantics canonical in the verifier and add
negative tests for them:

1. compare the complete rooted arc `id -> (parent, child)` map with the literal
   ten-arc map (or derive every semantic name from validated endpoints);
2. for every reticulation incoming descriptor require that its `edge_id`
   resolves to exactly `(parent, reticulation vertex)`, and derive choice
   semantics from that validated relation;
3. check `len(vertex_rows) == len(vertex_type)` before dictionary collapse and
   require the canonical ID/type/leaf-label schema; and
4. add the root-ID swap, stale-parent `p/q` automorphism, and conflicting
   duplicate-vertex cases to the mutation suite.

These are small verifier/test changes. No theorem, witness, PDF, or proof
revision appears necessary. If the authors instead choose not to bind the leaf
`label` keys, list them expressly as informational. After the graph bindings
above pass, my recommendation would become **ACCEPT**.
