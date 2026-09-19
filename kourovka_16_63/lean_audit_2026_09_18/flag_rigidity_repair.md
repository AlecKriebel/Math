# Flag rigidity repair and semantic audit

## Current status

**The actual `Kourovka/Flag/Rigidity.lean` module compiles successfully**, exit status zero with no warnings or errors, against the accepted Concrete/Generation dependencies. Command: `lake env lean -j1 -s65536 -o .lake/build/lib/lean/Kourovka/Flag/Rigidity.olean Kourovka/Flag/Rigidity.lean`. Final output log: `flag_rigidity_build.log` (empty).

## Repairs

- Explicitly unfold the existing `Preserves`/`IsDerivation` predicate aliases at their proof hypotheses so rewriting and simplification see the quantified bracket equations.
- In the full linear-equivalence theorem, express the same preservation hypothesis with the direct `Q` coercion before rewriting the generator-image equalities. This resolves the linear-map versus linear-equivalence function coercion mismatch.
- Change a declaration documentation comment before a `section` into an ordinary comment, fixing a parser error.

Every explicit theorem statement matches the supplied ZIP exactly. No hypothesis was added, no conclusion weakened, and no admissions, custom axioms or native proof computations were introduced. Original-to-repaired proof diff: `flag_rigidity_repairs.diff`.

## Statement review

The main finite theorem quantifies over the entire `E ≃ₗ[k] E` type, assuming preservation of the actual bracket and both specified subspaces. It concludes equality to the identity linear equivalence. The infinitesimal theorem quantifies over every linear endomorphism satisfying the actual Leibniz rule and flag-preservation conditions, concluding it is zero. Neither theorem silently restricts to inner derivations or a chosen automorphism subgroup. The final wrapper uses the ordinary mathlib LieEquiv type.

The first step extracts coefficients in the flag's coordinate spans, uses a nonzero characteristic-six scalar, and invokes injectivity only when showing the third image coefficient is nonzero. The residual sign is excluded by comparing two actual bracket reconstructions of coordinate22. Generation is used only after both generators are fixed (or killed for derivations). No component-group classification is assumed.

These results remain conditional on flag preservation. They do not establish the missing bridge from every finite quotient automorphism to representatives satisfying those conditions.

Checkpoint: 2026-09-19T04:23:38.162010+00:00. Assigned Rigidity source repair and compilation: 100% complete. This is a conditional flag-rigidity result, not a complete formalization of the group-existence theorem.

Final source SHA256: `2cf97f53a7af3cb20ad8a5f9ab16395886caaf430d70427772fe2926d25c8bd9`.
