# Global dependency crosswalk

This table records only claims used in the proof-level reduction.  A document
whose own heading is stale is cited through the independent review that
actually verified the claim.

| Dependency | Verified result used | Evidence | Role in Outcome P | Qualification |
|---|---|---|---|---|
| Convention | Locked simple binary LSA-rootable `sd_0` class with no omnians; open JC domain | `reviews/final_standard_convention/REVIEW.md`, `docs/DEFINITIONS_LOCK.md` | Fixes the exact theorem universe | Not the broader exhaustive-cleanup convention |
| Primitive structure | One cycle plus four theta event cores; `S_TC` has at most one triangle; no retained two-port theta | `reviews/root_probe/REVIEW.md`, `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | Ensures finite local forms, one coherent `T`, and no bivalent stabilizer | Keep levels distinct: the suppressed mixed-graph proof has two possible tails, while a rooted restatement has two ordinary vertices plus the root, still only three tails for four arcs; local algebra is not thereby classified |
| Cut theorem | Pointwise rank-at-most-four iff cut, including one-active and two-active crossings | `independent/bridge_cut/PROOF.md`, `reviews/global_bridge/REVIEW.md` | Gives both cut inclusions under `preceq_JC` | Reverse inclusion uses target equations on the shared source-open set |
| Component tree | Equal cut sets determine the same reduced labelled unmarked component tree | `reviews/global_bridge/REVIEW.md` | Matches component incidences and boundary blocks | Does not alone mark ordinary versus nontrivial nodes |
| Ordinary/blob marker | A full nontrivial three-port factor is a three-sunlet; the arm-homogeneous `F=abc-t^2` is zero on the ordinary median and has a strictly positive factored pullback on every open three-sunlet | `docs/GENERATOR_AND_SUPPORT_THEOREM.md`, `independent/counterexample_search/three_leaf_separator_certificate.json`, `independent/bridge_cut/PROOF.md`, `reviews/global_bridge/REVIEW.md` | Repairs the ordinary-component omission | The auxiliary `G=a-bc` from the crossing proof is not projectively invariant and is not used here |
| Bridge quotient | Exact positive fiber is the full incidence-scaling action; positive analytic slices exist | `independent/bridge_cut/PROOF.md`, `reviews/global_bridge/REVIEW.md` | Produces intrinsic projective local tensors and effective edge scales | Physical bridge multipliers are not identified |
| Localization | Global source-relative containment induces focal projective source-relative containment; no cross-blob compensation | `independent/bridge_cut/PROOF.md`, `reviews/global_bridge/REVIEW.md` | Converts the global problem into local directed containments | No continuous target parameter choice is made |
| Root reduction | Every root factor has an equivalent real incoming-port presentation | `reviews/root_probe/REVIEW.md`, `docs/ROOT_REDUCTION_THEOREM.md` | Lets one local theorem cover root and nonroot factors | Source and target incoming physical labels may be disjoint |
| Ordinary `T` germ | All ordinary triangle orientations share a strict-open full-dimensional regular projective JC germ | `reviews/triangle_redirection_cleanroom/REVIEW.md`, `docs/TRIANGLE_MOVE_LOCK.md` | Supplies the stochastic converse | Does not prove complete-image equality |
| Arbitrary-word logic | Product submersion and one-/two-port coherence promote a correct fixed-full bounded theorem | `reviews/arbitrary_subdivision_promotion_referee/THEOREM_AND_PROOF.md` | Optional route to prove `L_blob` | Conditional on the local fixed-full classification; no census conclusion assumed here |
| Global theorem logic | Cut + localization + root + local closure + `T` gluing imply Outcome P | `reviews/final_theorem_logic/PROMOTION_PROOF.md`, corrected by this audit | Supplies the formal implication | Its claim that ordinary nodes are fixed by the bridge tree must be replaced by the homogeneous three-sunlet `F` step |

## Exact remaining dependency cut

```text
verified convention
  + verified pointwise cuts
  + verified incidence quotient/localization
  + verified ordinary-vs-blob marker
  + verified root reduction
  + L_blob
  + verified ordinary-T germ/gluing
  -------------------------------------------------
  = Outcome P
```

The weak-but-not-strong all-taxa ambiguity theorem is an additional frozen
input only for the final **sharpness** corollary.  It is not used to prove the
positive `S_TC` classification.
