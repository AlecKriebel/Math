# Schema-3 n=3 graph/path review

## Scoped verdict

**VERIFIED — graph/path layer only.**

Against merged summary SHA-256
`791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65`,
the independent clean-room replay checked:

- 5,344 fixed root cases;
- 68,584 canonical states and raw path bindings;
- 14,482 exact rooted graph records;
- 8,349 refinement states;
- exact state identity including fixed root case plus source and target rooted
  graph IDs;
- independently regenerated complete child-state sets for every raw path;
- split-complement-normalized displayed-switching descriptors.

It found zero failures, zero stronger-identity collisions, and zero
merged-provenance child-set disagreements.  The frozen path-audit commitment
is
`d9dfc6d5e6e300bff00bd940adbf55395f609031aba8adeae0f38494dacadee6`.

## Explicit withdrawal and boundary

**WITHDRAWN:** the attempted n=3 terminal routine.  An independent adversarial
reviewer found it incompatible with required two-active-label cases.  Its
outputs are preserved under
`history/withdrawn_n3_terminal_two_active_labels/` and are not evidence.

Accordingly:

- **UNRESOLVED:** all n=3 terminal polynomial/sign classifications;
- **UNRESOLVED:** the 24 claimed ordinary-T terminal classifications as part
  of this clean-room gate;
- **UNRESOLVED:** the complete n=3 hard-cover verdict;
- **UNRESOLVED:** the global JC identifiability/containment theorem.

The previously frozen n=4 theta-2 base verdict remains distinct and
unaffected.
