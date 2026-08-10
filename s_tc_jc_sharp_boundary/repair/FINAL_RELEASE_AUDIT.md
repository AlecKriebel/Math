# Final release audit

## Verdict under review

The original positive classification of standard strongly tree-child
level-2 JC networks is **UNRESOLVED**.  It was not repaired, repackaged, or
silently weakened.  The only active submission theorem is the independently
verified all-taxa sharpness result in `W_TC \ S_TC`.

## Claims retained

1. **PROVED:** the displayed four-leaf rooted networks are binary,
   tree-child, LSA-valid, and level two.
2. **PROVED:** their narrow standard semi-directed reductions lie in
   `W_TC \ S_TC`, are leaf-labelled nonisomorphic, and are not related by
   ordinary triangle redirection.
3. **PROVED / EXACTLY COMPUTED:** the open JC models share a regular
   eight-dimensional stochastic region at an exact quadratic-algebraic
   interior point.
4. **PROVED:** identical cherry substitution preserves the overlap, has a
   positive analytic inverse, and gives dimension `2n` for every `n >= 4`.

The independent evidence is summarized in
`repair/reviews/SHARPNESS_GATE_REVIEW.md` and
`docs/THEOREM_CERTIFICATE_CROSSWALK.md`.

## Claims withdrawn or excluded

The release does not assert a complete local atlas, bridge-tree
reconstruction, one-sided containment classification, automatic triangle
bound, positive theorem for `S_TC`, K2P/K3P result, or an efficient inference
algorithm.  The forensic reasons are preserved in the definition, bridge,
and atlas gate reports under `repair/reviews/`.

## Release integrity

The active source and exact verifiers live only in `source/` and
`reproducibility/`.  Contradictory historical generations are retained under
`quarantine/withdrawn_positive_v1.1.1/` with an explicit withdrawal notice.
The public project page serves only the active sharpness PDF.  A final
manifest and clean-worktree replay are required after the independent
manuscript review is incorporated.
