# Family 047 actual Lean scope audit

Checkpoint: 2026-10-06 America/Los_Angeles. Audit completion estimate: semantic declaration/scope audit 90%; mechanical proof reproduction 10%. These are process estimates, not mathematical evidence.

The actual module is `OAI.Algebra.AffineCancellation.Main` and the actual theorem is `OAI.ComplexCancellation.main`. The comparator challenge contains a deliberate `sorry`; it is not the proof. `lean/ComparatorChallenges/ComplexCancellation.json` points to this actual solution module, allows only `propext`, `Quot.sound`, `Classical.choice`, and disables Nanoda. These permitted axioms are configuration, not a reproduced axiom report.

## Exact theorem and semantic agreement

At repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, let P = C[p,s,u,F,J], x=s^2+u^3+p^2 F, H=x^2 F-(1+2sx)J-p^2 J^2-pu, and A=P/(H). `MainStatement` asserts the conjunction:

1. `Algebra.FiniteType ℂ A`;
2. `IsDomain A`;
3. `ringKrullDim A = 4`;
4. `Nonempty (Polynomial A ≃ₐ[ℂ] MvPolynomial (Fin 5) ℂ)`;
5. `¬ Nonempty (A ≃ₐ[ℂ] MvPolynomial (Fin 4) ℂ)`.

The actual theorem has no free parameters or extra mathematical hypotheses. All its coordinate/algebra definitions and the full `MainStatement` body are textually identical to the comparator challenge. It uses genuine quotient ideals, complex coefficients, ordinary polynomials, ordinary complex algebra equivalences, and ordinary ring Krull dimension. Local nilpotence is the standard pointwise condition: for every r some nonnegative iterate of D sends r to zero (the zero bound can only apply to r=0).

## Actual proof artifacts and dependency chain

- `Model.lean` defines exactly the quotient above.
- `CylinderShift.lean` defines polynomial point shifts over arbitrary commutative rings, frame data, scalar roots and polynomial encode/decode coordinates without dividing by p.
- `CylinderMaps.lean` proves `encode_decode`, `decode_encode`, and functoriality. The second inverse uses regularity of p^3, and this is subsequently proved on the universal quotient; it is not an input to the final theorem.
- `Cylinder.lean` constructs `coefficientMap : A →ₐ[ℂ] P`, `forward : Polynomial A →ₐ[ℂ] P`, and `backward : P →ₐ[ℂ] Polynomial A`. It proves both `forward_backward` and `backward_forward`, and defines `equivalence` by `AlgEquiv.ofAlgHom`. The quotient saturation lemma proves regularity of p before using domain, avoiding circular use of domain to establish stabilization.
- `Dimension.lean` derives finite type, domain (via the coefficient embedding), and Krull dimension four from the cylinder equivalence and Noetherian dimension formulas.
- `Main.nonpolynomiality` starts by assuming an actual complex polynomial algebra equivalence and derives a positive-degree invariant for a nonzero LND on the graded degeneration (`Rees.positive_invariant_of_polynomial`).
- `EquivariantLift.exists_equivariant_lift` constructs a nonzero invariant replica lifting this derivation to the determinant pullback bundle and commuting with its fiber Euler operator. It assumes only the input derivation is nonzero and locally nilpotent, conditions supplied by the previous step.
- `GradedLND.highest` extracts a nonzero locally nilpotent top homogeneous component. `Bundle.no_positive_invariant` excludes its positive homogeneous invariant by coefficient-derivation extraction and determinant rigidity.
- `Determinant.rigidity` reduces the determinant obstruction to orbit rigidity. `Rigidity.orbit_constant` uses mathlib's polynomial Mason–Stothers theorem, including nonzero terms, coprimality from the degree-one bound, and a nonsquare condition. The required nonsquare is proved over a rational function coefficient field by parity of integer degree, rather than asserted over C. The remaining fixed-coefficient case is excluded by the explicitly proved sl2 highest-weight lemma.

The key source-level mathematical assumptions are thus discharged in the chain, rather than packaged as abstract structures containing the target theorem. There are 55 OAI modules (5573 source lines) in the actual closure, all under this family directory, plus `Mathlib` imported by `Model.lean`. The closure is preserved unmodified in `verification/lean_copy`.

## Difference between written and Lean mechanisms

The printed manuscript's Proposition `prop:homogeneous-lift` lifts the *same* homogeneous derivation D0, preserving its valuation shift, by Picard invariance and unique normalized line-bundle linearization. The actual Lean theorem `PolynomialTorsor.exists_equivariant_lift` instead constructs a lift E satisfying E(pullback r)=pullback(c D r) for a nonzero invariant c. It neither asserts c=1 nor that E preserves the original valuation shift. In actual `Main.nonpolynomiality`, one subsequently takes a highest valuation component of E. Because the particular positive homogeneous pullback invariant w is annihilated by E, this component also annihilates w; this is sufficient for the formal obstruction. The source thus follows an alternative replica-and-highest-component mechanism for the same final theorem. It does not formally certify the printed general normalized lifting proposition.

Likewise, the printed rigidity proof excludes negative-weight h via the coefficient intersection T ∩ C(a,d,u)=C[a,d,u]. The actual Lean proof uses the separately proved sl2 highest-weight argument `SL2.no_negative_highest`, together with locally nilpotent η. It does not certify that specific intersection argument, although it asserts the same final determinant rigidity proposition.

This distinction must be retained when citing scope: the final theorem agrees, but every printed intermediate proposition is not thereby formalized. The formal alternative appears to avoid the printed smoothness/Picard argument; the manuscript's smoothness and that general lift require their own mathematical audit.

## What was checked

The exact declarations, model, stabilization maps/compositions and the nonpolynomiality proof chain were read. Every closure source was copied with `git show` from the pinned commit and SHA-256 recorded. A second pass verified that every copied OAI file retained its recorded hash. A lexical closure scan found no `sorry`, `admit`, `axiom`, `unsafe`, `sorryAx`, `native_decide`, `skipKernelTC`, or `implemented_by`. This scan is useful provenance evidence; it is not kernel verification and does not eliminate errors in unexecuted tactic proofs.

The minimal verification Lake configuration retains Lean 4.34.1, `autoImplicit=false`, and the exact upstream mathlib pin `d13f23b723b8a846827a245b89c10fc7d3f11612`, while excluding many irrelevant repository dependencies. Lean's installed compiler/version and mathlib checkout revision were verified. `lake update` reached exact dependency configuration and began building the cache helper, then was interrupted before the automatic broad cache fetch to avoid filling the shared disk. Direct Lean attempts returned missing-module errors, preserved verbatim in logs. No OAI theorem compiled; no kernel axiom report or comparator result was obtained.

## Coverage exclusions and exact remaining gap

The original family source asserts a complete actual cancellation theorem, rather than merely its conditional reduction. Its source-level scope is sufficient as an upstream input *if* the actual proof is correct. That condition has not been mechanically validated in this audit. Do not report the actual theorem as independently kernel checked. The immediate remaining mechanical step is to acquire/build the compatible Mathlib umbrella dependency on a machine with sufficient storage, run the targeted OAI build, and execute `PrintAxioms.lean`; the accepted axiom set should be exactly within the comparator policy. A comparator run would additionally check theorem agreement.

The actual theorem does not explicitly formalize transcendence degree, smoothness, any retract maps, a five-component idempotent endomorphism, Costa's question or priority. Krull dimension equals transcendence degree for the finite type domain by a standard mathematical bridge, but this follow-on bridge is not in `main`. Smoothness of the specific hypersurface needs a separate verification if claimed. The Costa consequence is not formalized merely because cancellation's input has a source proof. Stable-coordinate and general line-bundle consequences are excluded by `lean/docs/047.md`.

No substantive mathematical defect was found by this limited source-level scope audit. This does not constitute a complete independent line-by-line proof certification.

## Reproduce (sufficient storage required)

From `verification/lean_copy`, run:

```sh
lake update
lake exe cache get
lake build OAI.Algebra.AffineCancellation.Main
lake env lean PrintAxioms.lean
```

No command should run in the source clone. The minimal copy changes only Lake project configuration; every upstream OAI module is byte identical to its pinned source. `source_manifest.json` identifies all source hashes; `mechanical_receipt.json` states the actual verification limitations. Generated dependencies were removed after the failed attempts to recover storage; the minimal source/configuration and logs remain.
