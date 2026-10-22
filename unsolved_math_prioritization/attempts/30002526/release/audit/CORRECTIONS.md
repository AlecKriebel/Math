# Corrections and qualifications

Frozen originals are unchanged. `proposed_corrections.patch` contains the exact recommended text changes for a later revision.

## C1 Properness in the birational obstruction

Severity: required scope clarification; nonfatal to the partial-result verdict.

Locations: PROOF.md Section 2 and SOURCES.md Bierstone–Milman item.

Problem: the prose mentions a birational morphism preserving the NC locus without explicitly saying proper. In the intended resolution setting this is understood, but unrestricted birational morphisms make the statement false: the open immersion X minus {0} into a pinch-point surface X is birational, is an isomorphism over all NC points, and has NC source. Its image omits the pinch point, and the map is not proper.

Correction: state **proper birational modification** and cite Question 1.2 together with Example 1.7. The surrounding source explicitly poses proper birational resolution; properness also holds automatically for the blowups actually under discussion. Keep the NC-locus preservation hypothesis. Do not extend this obstruction to all birational modifications or to unrelated global projective realizations.

## C2 Coverings do not necessarily change the abstract group

Severity: minor wording precision; no effect on the argument.

Location: PROOF.md Section 1, first sentence under the torsion-removal gap.

Problem: saying a covering changes the group is too categorical. Nontrivial finite covers can preserve the abstract fundamental group, as with S^1 mapping to itself by degree two.

Correction: say that a covering need not preserve the fundamental group and no preservation is automatic. The local stabilizer example and the torsion-free obstruction remain valid.

## Items checked and not corrected

- The quotient invariant-ring identity is correct. Visual inspection of the published Kapovich formula also shows the transverse squared factor applies to the full parenthesized expression. There is no verified published missing-factor error.
- The conductor is (u) in the normalization and (u,v) in the original ring. The author's normalization-side ideal is correct.
- Connected smooth projective normalization is irreducible over C. No correction from connected to irreducible is needed under the stated smoothness hypothesis.
- The square-root base change is reduced but nontransverse at the origin; both assertions are consistent.
- The nodal-cubic product realizes Z and its smoothing realizes Z^2. These are control examples, not an arbitrary-group theorem or a counterexample to the target.
- The bounded literature caveat is mandatory. No already-solved status or categorical current openness is justified by the checked evidence.

No correction raises the full-target completion estimate, changes the five-approach count, or turns this investigation into a proof or disproof of the realization question.
