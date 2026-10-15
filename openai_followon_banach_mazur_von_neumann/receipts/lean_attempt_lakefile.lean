import Lake
open Lake DSL
package family295_kernel_audit where
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"
@[default_target] lean_lib OAI where
  roots := #[`OAI.Analysis.BoundedHochschild.MainResult]
