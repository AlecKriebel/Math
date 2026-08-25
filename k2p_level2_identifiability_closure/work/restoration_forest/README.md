# K2P restoration-forest workspace

> **Historical depth-one workspace -- not current theorem authority.**  The
> 646 rooted tree--sunlet classifications and the no-second-layer conclusion
> described below were revoked.  The current restoration result is the
> 36,824-edge, 36,792-leaf depth-two forest in
> `work/restoration_sign_reclassification/corrected_restoration_forest.json`,
> with its independent replay and mutations bound by
> `work/final_theorem_release/RELEASE_LOCK.json`.

This directory is an isolated, read-only derivative of the frozen v4
four-port release.  Nothing here mutates or replaces the locked referee
package.

The immediate purpose is to expand every `restoration_parent` presentation
into its physical labelled children while preserving the source-to-target
direction, omitted-role transport, target attachment, and source insertion
edge.  Children are tested proof-first by displayed-quartet mismatch,
tree-versus-sunlet separation, already certified direct four-port
restrictions, and finally exact labelled mixed-graph isomorphism or the
ordinary-triangle quotient.

The current frozen result is:

- 997 canonical parents reconstruct as 2,540 physical member/root cases;
- their 5,224 role requests and seven source insertion positions generate
  exactly 36,568 raw labelled five-port children;
- corrected exact mixed-incidence canonicalization gives 2,240 directed
  relation classes;
- 35,758 children have a displayed-quartet mismatch;
- 646 have a strict tree-versus-sunlet sign obstruction;
- 148 have an exact multihomogeneous K2P quadratic obstruction; and
- the remaining 16 have an exact selected-quartet transport of the previously
  certified `F_(2,112)` quartic.

Thus every first child is separated.  No six- or seven-port state is reached,
so the forest has no unresolved leaf, cycle, or missing generated child.

Run the complete deterministic replay with:

```text
.venv/bin/python work/restoration_forest/verify_restoration_forest.py
```

Run the five adversarial mutations with:

```text
.venv/bin/python work/restoration_forest/verify_mutations.py
```

Scope remains deliberately narrower than a final K2P theorem.  The finite
certificate supplies the child-separation premise needed by restoration; it
does not independently prove the marginal-restoration implication or close
the topology/rank, bridge, gluing, or genericity gates.
