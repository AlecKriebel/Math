# Research log: injectivity of the special free-group sum

## Scope

Let `F = <h_1,...,h_99>` be the free group and `S = 1+h_1+...+h_99`.
Determine whether left and right convolution by `S` are injective on
`ell^2(F)`. The proposed route identifies an associated bipartite graph with
the infinite 100-regular tree and proves that its adjacency operator has no
square-summable eigenfunction at zero.

No claims about cost, Betti-number comparison, or general zero-divisor
conjectures are assumed or evaluated here. All work stays in this folder;
no Git operations or external communication are authorized for this subtask.

## Checkpoints

- **2026-10-07 04:34:12 UTC — 15% complete.** Established the precise target,
  opened a dedicated folder, and delegated an independent search for an
  elementary proof or counterexample to the tree-adjacency assertion.
- **2026-10-07 04:36:03 UTC — 80% complete.** Found a direct
  Cauchy–Schwarz proof: if `Af=0` on a rooted `(q+1)`-regular tree and `E_n`
  is the squared mass on the `n`th sphere, then `E_(n+1) >= E_(n-1)` for
  `n>=2`. Since `sum E_n<infinity`, every positive-radius sphere has zero
  mass; the equation one level out then forces the root value to vanish.
  Graph acyclicity and operator conventions have direct proofs. An
  independent subagent separately found and verified the tree estimate,
  including the root bound `E_2 >= d/(d-1) E_0`. Remaining check:
  adversarial verification of graph identification and conventions.
- **2026-10-07 04:36:58 UTC — 100% complete for this local
  operator claim.** The independent reviewer checked the graph's
  acyclicity, both block entries, inversion conjugacy, and the ambient
  coset decompositions. It found no mathematical flaw. Clarified that
  adjoint injectivity follows from the separate proofs for both `T` and
  `T^*`, not from a general assertion that injectivity passes to adjoints.
  Strongest result: both left and right convolution by this exact `S`
  and their adjoints are injective on `ell^2(Gamma)` whenever the stated
  free group is a subgroup of `Gamma`. No central gap remains for this
  claim; cost/Betti implications are outside the subtask.

## Approach-family tracking

| Family | Mechanism | Evidence | Status | Exact gap |
|---|---|---|---|---|
| Elementary rooted-tree estimate | Cauchy–Schwarz plus cancellation of the number of children and parent repetitions | Explicit nondecreasing mass on each parity of spheres; separately reproduced by an independent subagent; graph, operator, and coset conventions adversarially checked | Verified | None for the exact operator claim |
| Spectral measure of the regular tree | Zero is in continuous spectrum but has no spectral atom | Not needed; no citation sought | Unused | None for the elementary result |

## Strongest verified intermediate statement

For every integer `d>=2`, adjacency of the infinite `d`-regular tree has
trivial kernel on square-summable functions. The proof uses only local
equations, finite sphere sums, and Cauchy–Schwarz. Consequently,
`1+h_1+...+h_99` and its adjoints are injective under both convolution
conventions on the free group and on every ambient group containing that
free subgroup. No spectral citation, general zero-divisor conjecture,
bounded-inverse claim, or cost conclusion is involved.
