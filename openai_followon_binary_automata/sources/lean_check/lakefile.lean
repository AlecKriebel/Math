import Lake
open Lake DSL
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"
@[default_target] lean_lib OAI where
  roots := #[`OAI.Combinatorics.Automata.Main,
    `OAI.Combinatorics.TwoWayAutomata.Main,
    `OAI.Combinatorics.TwoWayAutomata.ExplicitFamily]
lean_lib ComparatorChallenges where
  roots := #[`ComparatorChallenges.OneWayLiveness,
    `ComparatorChallenges.TwoWayComplementation,
    `ComparatorChallenges.TwoWayDeterminization]
