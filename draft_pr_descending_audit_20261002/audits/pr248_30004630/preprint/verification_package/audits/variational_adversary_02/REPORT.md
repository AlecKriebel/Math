# Fresh independent variational, growth and stability audit

**Mathematical verdict: PASS for the frozen, explicitly scoped counterexample to the unmodified β₂=0 implication. No mandatory mathematical repair identified.**

**Source-resolution verdict: the same ordinary-cone positivity criterion cannot imply the same L²-squared growth after deleting β₂>0. This does not resolve the broader search for adapted sufficient conditions or weaker-norm β₂=0 growth/stability theories.**

This audit concerns PR248 / 30004630 / OWR-4990378-001 at parent intake head e9c5d10978764db2cf25fa7d49cf4bd14a82d604. COUNTEREXAMPLE.md is bound to SHA-256 a4ffb1e682a235e0221a83edf4b2db2c7fc7b17a02f778884489a1c3dd321cc3. All 19 authenticated submitted files match parent intake. No frozen input was edited. The route was reconstructed before consulting the earlier independent_review; comparison with that review occurred after the independent derivation checkpoint. This is independent assistant adversarial verification, not human peer review or novelty certification.

## Strongest verified result

Under the submitted smooth unit-ball, zero-data, defocusing quintic wave model, γ=β₁=1, β₂=0, fixed ν≥0, target πe and sufficiently small constant radius ρ:

1. Zero is the unique global optimizer over all feasible spatial/time controls. The uniform small-L¹-input contraction yields ∥y∥_Y≤CA and ∥y−z∥_Y≤CA⁵; all constants are fixed before ρ. The sign-correct bathtub inequality holds for every density 0≤f≤ρ and every A∈[0,ρ], including zero and saturated full mass. It absorbs the quintic error with the submitted C₀ρ⁴≤1/12 condition.
2. First-order conditions hold and the ordinary critical cone is exactly {0}. Pointwise inactivity does not create L¹/L² norm interior; truncation instead proves the full tangent cone and zero normal. The source's j'' convention at zero is used faithfully. Vacuous strict positivity is allowed by the literal source condition and is explicitly disclosed.
3. The actual nonlinear objective along the submitted pulses has leading gap (π²/3+2/π²)h⁴, while the L² norm squared is 2h³ and the L∞ norm is h. The signed tracking error, quartic state cost and optional terminal velocity term are higher order. Positive L²-squared growth therefore fails even in the stronger L∞ neighborhood. An independently derived continuous triangular pulse has the same failure, so temporal discontinuities are inessential.
4. Global optimizers exist for the target perturbation (π+ε)e, also with the optional H⁻¹ velocity cost. The fixed-amplitude comparison has gain −ε²/2+O(ε³), and the exact threshold geometry gives ∥g_ε∥₂=O(ε^{5/4}). For every K, all sufficiently small ε and every global optimizer satisfy ∥u_ε∥₂>Kε. This is a uniform statement over all optimizer selections, rather than one inconvenient selection.

## Independent strengthening and precise stability scope

The same example has **local L¹-squared quadratic growth**. For A=∥u∥_{L¹H} and x=⟨e,y(1)⟩, the kernel and nonlinear estimate give x≤A/π+DA⁵. For small A, this upper bound is below π; the exact terminal-plus-sparse expression A−πx+x²/2 decreases in x there. Consequently

J(u)−J(0)≥A²/(2π²)−πDA⁵≥A²/(4π²).

The full proof in INDEPENDENT_DERIVATION.md gives an explicit positive A_* in terms of a₀,ρ,D and explicit ε locality thresholds; it requires no additional change to the frozen radius. The global cube bound first places every perturbed optimizer in this neighborhood. It then follows that every optimizer on the one-sided target ray has

∥u_ε−0∥_{L¹H}=Θ(ε),   cε^{3/4}≤∥u_ε−0∥_{L²H}≤C√ε.

Thus all perturbed global optimizers converge to the unique base optimizer in L², but their L² distance is not O(ε). The L¹ upper estimate is a bound relative to the fixed zero base optimizer, uniform over this perturbed optimizer correspondence. It does not by itself prove a pairwise Lipschitz selection map between arbitrary targets. No L∞ convergence of perturbed global optimizers was established. A stability theorem conditioned on remaining in an L∞ neighborhood requires a separate analysis. The growth countersequence itself converges in L∞ and has no such dependency.

This strengthening is optional independent evidence, not a mandatory repair: the frozen theorem and conclusions already specify L² and do not assert failure of all growth/stability theories.

## Adversarial checks and exact remaining gaps

The attempted failure points were: replacing true feasible states with a formal Taylor expansion; restricting optimality to the e mode; incorrect constraint interior/tangent reasoning; mass endpoints in the bathtub argument; hidden nonzero-cone hypotheses; wrong sign or power in endpoint/velocity costs; ε-dependent pulse amplitude constants; optimizer existence and weak-to-mild passage; and swapping existence of one bad optimizer for a universal selection statement. None invalidates the scoped theorem. The nonlinear state need not remain in the e mode; the uniform Y remainder controls all other modes.

The optional-velocity existence proof has the required bounded y_tt in L∞H⁻¹ because f≤ρ, the energy bound gives y⁵ in L∞L^{6/5}⊂L∞H⁻¹, and compact H→H⁻¹ gives velocity convergence including the terminal trace. Almost-everywhere state convergence identifies the weak quintic limit; the retained energy/L⁴L¹² bound and source uniqueness identify the limit mild solution. Lower semicontinuity completes the direct method.

No numerical PDE constant is available or needed for this existence construction. The source linear estimate and mild/Shatah–Struwe uniqueness are credited analytic inputs, not finite-check results. Historical novelty, final publisher typesetting, and a complete β₂=0 theory were not audited. These are precise limitations, not defects in the counterexample.

## Source fidelity and classification

The official OWR report printed439–440 and full preprint Theorem4.17/§4.2.2 were read directly, with the model/theorem pages visually inspected. Fresh downloads of all three primary PDFs match submitted SHA-256 and byte pins. The OWR has an extra ν term and an L²-neighborhood display; the full preprints omit ν and use L∞ localization. The construction covers these differences. The inspected source has no condition that the critical cone contain a nonzero vector.

The source places the β₂=0 open case beside its coercivity-dependent sufficient condition. The verified obstruction answers the unmodified implication negatively; it does not disprove the published β₂>0 theorem. A precisely worded claimed_solved status for that negative implication is mathematically defensible. Promotion as a solution of every possible β₂=0 sufficient-condition/stability program would exceed the verified result. Parent owns queue/PR disposition and any optional integration; this audit made no PR, queue, branch, index, commit, push, release, deposit or spreadsheet changes.

## Reproduction evidence

- Independent checker: 210 exact symbolic/rational assertions and five noncertified 80-digit diagnostics, all passing. New families include continuous triangular pulses, exact sine positive-part norm/asymptotic constant, exact parabolic norm, sharp sine bathtub/zero-full mass boundaries, asymmetric/boundary densities, and the scalar L¹ growth/basepoint perturbation algebra.
- Author checker: actual replay passes 3,937 assertions and exactly matches submitted JSON.
- Earlier independent checker: actual replay after independence checkpoint passes 1,385 assertions and exactly matches submitted JSON.
- Both independent-checker development errors were local checker issues (a wrong positivity assumption on an integration variable, and structural equality of equivalent symbolic expressions), corrected and documented. Neither was a submitted proof defect.

INDEPENDENT_DERIVATION.md contains the full checkable analytic derivation. SOURCE_PINS.json and SOURCE_NOTES.md bind source access. INPUT_BINDINGS.json binds the submitted files. Replay JSONs retain actual command, runtime, exit status, stdout/stderr and script hashes. Private PDF/text/page reading copies are excluded from the authored artifact manifest.
