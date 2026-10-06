# Five bounded mathematical approaches

The source and prior-attempt audit preceded these approaches. None produced a
full candidate proof; no sixth search route is hidden in the verification work.

1. **Extract spherical bubbles and spend the energy budget.** Rescaling and an
   exact radial integral recover the quantum 16π². Disjoint selected bubble
   balls give L ≥ I. If the total energy is below 32π², integer quantization
   forces L = I = 1. At higher energy this has the wrong direction for simplicity.
   Proof: PROOF.md §2. Status: known-result consequence, complete at low energy.

2. **Convert the squared exponential into a Q-curvature equation.** For
   v = u²/2, an exact product-rule computation gives

   Δ²v = u Δ²u + (Δu)² + 4∇u·∇Δu + 2|D²u|².

   Thus the first term is λu²e^(4v), but the remaining differential terms cannot
   be erased or assigned a favorable sign. Nor does the coefficient λu² converge
   to a fixed positive coefficient in the required local topology. At a smooth
   boundary with u = Δu = 0, one has Δv = |∇u|², generally nonzero; the Navier
   condition is lost. This blocks a direct invocation of Liouville/Q-curvature
   quantization or simplicity. Status: exact reduction obstruction.

3. **Use Navier positivity and radial monotonicity.** Put w = -Δu. The system is
   -Δw = λu e^(2u²) > 0, -Δu = w, with zero boundary values for both. The maximum
   principle gives w > 0. On a ball, for radial smooth solutions,

   r³ w'(r) = -∫₀ʳ t³λu(t)e^(2u(t)²)dt,
   r³ u'(r) = -∫₀ʳ t³w(t)dt.

   Both functions decrease strictly away from the origin. This gives one spatial
   maximum; it does not prove that energy cannot reappear at a larger vanishing
   radius. A bubble tower can concern scales at the same spatial maximum. The
   original Struwe proof itself treats radial scale induction. Status: exact
   monotonicity deduction, blocked at exclusion of extra scales. No numerical
   shooting result is claimed as an existence or nonexistence theorem.

4. **Apply the fourth-order local Pohozaev identity.** PROOF.md §§3–5 proves the
   conditional moment identity n₀ = m²/(16π²) and excludes more than one positive
   bubble if exterior convergence, finite comparable height ratios, and weighted
   exhaustion hold. Its algebra is decisive under those hypotheses. Deriving
   those hypotheses uniformly from the target assumptions remains unproved.
   Status: complete conditional theorem; no full-target resolution.

5. **Try to remove the weighted assumptions by energy/Cauchy control.** Ordinary
   no-neck energy does not bound the source and primitive moments: the weights
   c/u and (c/u)² may diverge. An exact nonnegative-measure control exhibits
   vanishing energy and source mass but a nonvanishing squared weighted mass.
   Cauchy–Schwarz plus Pohozaev only recovers E ≥ 16π². The explicit defect
   formula in PROOF.md §6 quantifies exactly what a successful neck estimate must
   remove. Status: failed implication isolated; not a PDE counterexample.

## Checkpoint / completion estimate

2026-10-06 00:19 UTC: source normalization and prior-attempt checks complete;
five routes have reached the outcomes above. Best-guess completion toward a full
proof or counterexample: 0% certified. Completion of the separately scoped
conditional theorem: 100%, subject to independent mathematical audit. These
estimates do not represent a probability that the conjecture is true.
