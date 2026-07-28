# Research log: QQ1 inner global attack

- **2026-07-28 PDT — checkpoint 1.** Reconstructed accepted C-158,
  C-161--C-163 and candidate commit `b8ef2d4d`.  The `ud`-edge boundary
  control has 34 dominating pairs and, crucially, the original pair
  `{u,x}` dominates.  Thus it does not realize the simultaneous global
  obligations `W_{u,d}` and `W_{u,x}` forced by `gamma(G)=3`.  Added a
  discovery-only SAT probe separating those two obligations from the
  full all-pairs condition.  Estimated completion of this focused QQ1
  inner-gate investigation: **20%**.

- **2026-07-28 PDT — checkpoint 2.** Found an exact 16-vertex control
  `OslallyN]z~r|^{~|^|~^` realizing both primary witness layers,
  the retained inner bridge, and the saturated outer bow tie.  It has
  exact vector `(2,3,3,3,3)` and fails equality at the dominating pair
  `{p,w}`.  Blocking that pair produced
  `OslallyN]fv|y~v^}n}{n`, again with exact vector `(2,3,3,3,3)`;
  vertex 15 repairs `{p,w}`, but 21 other dominating pairs remain.
  This refutes the proposed two-obvious-witness shortcut.  Estimated
  completion of the focused QQ1 inner-gate investigation: **65%**.

- **2026-07-28 PDT — checkpoint 3.** Proved the cross-layer bridge:
  for every hot witness `w` of `{u,d}` and every witness `z` of
  `{u,x}`, the state `{u,w,z}` is retained.  If it were omitted, closure
  would force `{u,d,z}`, whose attack at `r` has only the omitted state
  `{u,d,r}` or the non-dominating state `{r,d,z}` missing `x`.
  Built a standalone exact verifier recomputing both control graphs'
  parameters, greatest kernels, ranks, witness sets, retained states,
  outer bow ties, clique partitions, and full dominating-pair lists.
  Stopped the exploratory CEGAR lane: its n=16 and n=17 cores are
  order-specific observations, not a proved infinite pattern.
  Estimated completion of this bounded QQ1 inner-gate checkpoint:
  **90%**.
