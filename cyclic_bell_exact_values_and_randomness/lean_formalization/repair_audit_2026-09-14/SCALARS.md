# Exact scalar and four-dimensional repair log

2026-09-15T03:30:35Z — ScalarData builds on the pinned Lean 4.19.0/mathlib revision. Assigned scalar/target module scope approximately 35% complete; downstream D4 and Phases still under compilation. This percentage is not an estimate of whole-paper completion.

Repairs retain every original definition and theorem statement:

- Proved the sine-square constant through the double-angle cosine identity; the submitted `norm_num` had rewritten away the sine term needed to use its proposed half-angle lemma.
- Unfolded the `k = sqrt 2` bridge in the sine/cosine product proof.
- Replaced a failing tactic-branch layout in the 16-entry root-of-unity table with explicit checked power decompositions.
- Preserved the real trigonometric arguments and their casts when reducing the source coefficient formula; identified integer powers with natural powers using `zpow_ofNat` after finite index reduction.
- Replaced unsuitable nonlinear arithmetic normalization in `k_alpha`/`k_beta` with exact polynomial combinations.

The source coefficients still use their original exponential embedding, real sine denominators, and integer exponent convention. No axiom, placeholder proof, statement weakening, or numerical approximation was added.

Build evidence: `scalars_build.log` (updated by subsequent builds in this work stream).
