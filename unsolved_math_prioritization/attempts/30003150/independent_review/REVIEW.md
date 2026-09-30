# Independent adversarial review: resonant-NLS reservoir diagnostic

## Verdict and exact coverage

**PASS_SCOPED_MODEL_SEPARATION_AND_DIAGNOSTICS.** No mandatory mathematical correction was identified. The original target remains **unsolved, 2/5 approaches, with a source-specification hold**. This is an independent AI review, not human peer review or a new invariant-measure theorem.

The reviewed `PARTIAL_RESULT.md` has SHA-256

`f92528750685bd135da7d7e09e57edd1f3c28c66439abdd6b43e153f5862124e`.

The verdict covers the source distinctions and the three restricted deductions in that exact artifact. It does not certify existence, nonexplosion, recurrence, a smooth stationary density, or a transfer of a theorem between different bath models.

## 1. Primary-source scope

I read Andrea Nahmod's full contribution, printed pp. 1549–1551 of [Oberwolfach Report 27/2016](https://doi.org/10.4171/OWR/2016/27), and visually inspected the concluding source page. The opening announces work constructing a unique invariant ergodic measure for a finite resonant-NLS subsystem. The final page discusses unequal endpoint temperatures, an equal-temperature Gibbs density proportional to `exp(-H/(2T))`, and the three-mode case. It describes a regional Lyapunov construction and a controllability argument. It does not display the stochastic generator, coefficients of the noise, a complete state space, or a zero-action boundary convention. The standard-Langevin footnote supplies context, but does not fix those missing formulas. Therefore the artifact correctly avoids converting this announcement into a fully specified, unqualified open conjecture.

The following contribution is Ionescu's water-wave talk. Its dynamics are not the reservoir system at issue. The artifact's warning against importing the dataset's water-wave assessment is justified by the consecutive source pages.

I also checked the displayed equation (1.8), Theorem 1 and Sections 1.3–1.4 in Hani–Li–Nahmod–Staffilani, [arXiv:2505.16018v1](https://arxiv.org/abs/2505.16018v1), including a visual inspection of the theorem page. The theorem fixes `beta0>1`, `gamma>0` and `T1>0`, takes `T3` sufficiently large, and asserts the existence of a suitable coefficient `g` and Lyapunov function. Its convergence statements concern that modified three-mode process. The text explicitly explains that the chosen forcing no longer preserves the Gibbs measure even when the temperatures agree. More natural reservoirs and longer chains are future directions. Consequently this theorem does not, without a new identification argument, resolve the original Gibbs-preserving reservoir formulation for all temperature gaps or all chain lengths.

The live arXiv record was checked on 2026-09-30 and still lists the version submitted on 2025-05-21. No later-version or journal-acceptance claim is made. This audit verifies the theorem's stated scope and its use here; it does not independently reconstruct the paper's long analytic proof.

Both cached full-PDF hashes agree with the author's manifest:

- OWR report: `c9f0622b146dae366cc33432cb6a0d75307c3ad447addc55f86126ae1c5455c4`
- Hani–Li–Nahmod–Staffilani: `300ca50afa88eec6ee0800b271f937147db0ce4ac72388e97d89481b18b6a790`

## 2. The middle-action-only obstruction

Write `r=I2` and `A=I1 sin(theta1)+I3 sin(theta3)`. The displayed source equation gives `dr=-2rA dt`. Since this coordinate has finite variation, every quadratic covariation involving it vanishes. For `V=F(r)`, the ordinary chain rule therefore yields

`dV=-2rF'(r)A dt`.

This is valid for `C1` functions along the stated paths. The notation `LV` here is the local differential or extended-generator expression, obtained after localization if needed. It should not be read as asserting that every unbounded `C1` function belongs to the domain of a globally defined strong generator on a Banach function space. That standard local reading is sufficient for all conclusions in the artifact.

At any fixed positive actions `(a,r,b)`, the two simultaneous phases `-pi/2` and `pi/2` give opposite values `2r(a+b)F'(r)` and `-2r(a+b)F'(r)`. If the derivative is zero, both values vanish; otherwise one is positive. Thus no such function has strictly negative pointwise drift at every phase over those fixed actions. This includes arbitrarily high middle action, and does not require any claim about the remaining drift or diffusion coefficients. Also, fixing `r` while letting an endpoint action diverge directly prevents compact sublevel sets for a finite-valued middle-action-only function.

There is no contradiction with phase-dependent Lyapunov functions or time-averaged drift. The later paper itself emphasizes adverse phases and constructs a phase-dependent correction. The restricted obstruction is elementary explanatory context, not a new obstruction to the published construction.

## 3. Finite-time positivity and boundary qualifications

For integrable `A` on a finite interval, the scalar linear equation has the unique absolutely continuous solution

`I2(t)=I2(0) exp(-2 integral_0^t A(s) ds)`.

One can verify this without dividing by `I2`: multiply the differential equation by the positive integrating factor and differentiate almost everywhere. This also proves the zero-initial-value assertion. A positive initial value remains positive on the specified interval because the integral is finite.

These facts establish neither global existence of the other coordinates nor a positive lower bound as time tends to infinity. The zero-action conclusion applies only if an extension to that face is actually defined with the stated integrable coefficient. The artifact explicitly retains that hypothesis and the degeneracy of action-angle variables. An invariant face alone also does not supply a stationary probability supported on it. Those restrictions are necessary and correctly maintained.

## 4. Conditional uniqueness

Let `nu` be any invariant probability for the same Markov semigroup. For every bounded measurable `f`, invariance gives `nu(f)=nu(P_t f)`, while the Markov property bounds `|P_t f|` by `||f||_infinity`. Pointwise convergence of `P_t f` to the constant `pi(f)` then gives `nu(f)=pi(f)` by bounded convergence. Applying this to indicators proves equality of measures. No Lyapunov moment of `nu` enters the argument.

The stated total-variation estimate tends to zero for each permitted starting state because `beta0>1`, and therefore supplies the premise on that theorem's state space. The implication neither adjoins excluded boundary states nor transfers to another generator. Uniqueness implies extremality in the convex set of invariant probabilities, which is precisely the ergodicity convention stated in the artifact. No smoothness conclusion follows from this argument alone.

## 5. Independent controls and reproducibility

The submitted verifier and its exact artifact were copied unchanged into `author_replay/`. Running `python verify.py` from that directory reproduces all **129** assertions and a byte-identical `verification.json`.

The separate `independent_checks.py` uses SymPy and rational arithmetic without importing the author's verifier. It passes **869** exact controls:

- 7 symbolic generator and scalar-flow identities, using an arbitrary diffusion matrix with zero middle-action row
- 540 rational phase controls, including both signs and a vanishing derivative
- 250 exact integrating-factor exponent-additivity controls
- 72 finite-state Markov-kernel controls illustrating the invariance and uniqueness identities

Run `python independent_checks.py` from any directory. The script reads the frozen snapshot and writes `independent_results.json` beside itself. These finite controls support the algebra only. The analytic justifications are the proofs above; neither checker establishes stochastic existence, recurrence, regularity, or theorem transfer.

## 6. Disposition

Preserve the unresolved status and source-specification hold. The exact next requirement is a fully specified original Gibbs-preserving reservoir process, followed by recurrence, regularity and irreducibility analysis for that same process and state space. The current package correctly stops before that missing step. No priority or novelty claim is supported or needed.
