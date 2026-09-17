# Binary benchmark repair

2026-09-15T03:45:35Z — GeneralBinary compiles fully against repaired original dependencies. Binary benchmark workstream approximately 50% repaired; physical binary witness and model endpoint layers remain. This is not a whole-paper estimate.

Preserved all original theorem statements and definitions. The repaired module proves the two-square Bell operator identity, upper bound, scalar saturation implying on-state residuals, the resulting on-state anticommutation identities, vanishing operator-valued Eve Fourier moments, and the actual conditional-state privacy conclusion for arbitrary finite purifying Eve.

Repairs include an exact polynomial certificate multiplier missing sqrt(3), matrix-specific multiplication identities for rectangular purification coefficients, explicit reduced-state normalization, correct association of products before commuting factors, and exact matrix-star map coercions. No global anticommutation assumption was added; the privacy proof derives the required on-state relations.

Evidence: binary_build.log. The scratch BinaryPrefix.lean and BinaryAlgebra.lean were temporary independent checks while dependencies were unavailable; they are not package entrypoints or substitutes for the now-successful full module build.

2026-09-15T03:51:30Z — Assigned GeneralBinary/GeneralBinaryWitness/GeneralPartySwap scope 100% repaired and compiled; model/certification layers handed to the foundation agent. The actual binary matrices attain 3 sqrt(3) on the normalized entangled state and all spectral effects satisfy PVM validity. PartySwap required renaming the reserved Lean token `λ` used as a binder to `label`; statements are alpha-equivalent. BinaryWitness uses its actual required GeneralBinary import rather than the unrelated aggregate GeneralConsequences import; no theorem was removed from the package.

Temporary partial-compilation scratch sources were removed after the real modules compiled; their diagnostic logs remain. BinaryAxiomCheck.lean checks privacy, explicit attainment, PVMs and the Bob-one-input perfect-guessing construction.
