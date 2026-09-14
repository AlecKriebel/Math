# Block action checkpoint: implementation and trust disclosure

UTC: 2026-09-14T14:44:32.094812+00:00

`BlockActions.lean` implements zero extension of arbitrary rational vectors on finite rank coordinates, proves the exact finite selector sum formula, and derives six action formulas directly from `phaseS`, `phaseC`, `phaseD`, `phaseQ` and `coefficientK`. No domain or matrix-positivity hypotheses are used in these equalities. Missing coordinates have value zero by a definition with proved in-range and out-of-range lemmas.

Every good coordinate `i` represents physical rank `i+1`; every bad coordinate `i` represents physical rank `i+2`. At the first coordinate, predecessor extension is zero; at the final coordinate, successor extension is zero. The transpose-D action likewise gives zero at the top good coordinate because it lies outside the shorter bad vector. Consequently negative formal coefficients of missing upper entries cannot affect an actual finite sum.

The six action theorems each compiled with dependencies exactly `propext`, `Classical.choice`, and `Quot.sound`. The reusable kernel-checking command is:

```
lake env lean SymmetricSector/BlockActions.lean
lake env lean reports/BlockActionsAxioms.lean
```

Source SHA-256 at this localized checkpoint: `dc87f65c29958c63dabb789b868d7794b901ac5b942d6dec39803cac16018591`.

This is a localized dependency check, not a clean aggregate build or a proof of scalar positivity. The author of this report also authored `BlockActions.lean`; it is an implementation/trust disclosure and does **not** claim independent mathematical review of that file. The lead has been asked to assign the action formulas and indexing to a separate reviewer. A final `tools/audit.py --clean` run requires a coordinated source freeze and a target list covering all promoted results.

## Concrete A.27 contraction checkpoint

UTC: 2026-09-14T14:52:19.843707+00:00

At the lead's request, this author also implemented `Contraction.lean`. The principal theorem `phaseA_phaseV_le` proves the actual Schur operator satisfies `phaseA N *ᵥ phaseV N ≤ c N • phaseV N` for every `N≥3`. Its weight is the actual inverse-defined `phaseV`, identified separately with the proved recurrence in `GoodPhase.lean`. The proof uses the exact bad barrier Hhat, the concrete Q and C actions, the full inverse positivity and invertibility theorems, and the actual radial upper bound. All boundary coordinates are zero extended. The successor comparison deliberately drops a positive formal top contribution; it does not assume a nonexistent bad-channel state.

All four principal contraction statements were checked with ordinary foundational dependencies only. `reports/ContractionAxioms.lean` reproduces the statement/dependency query. SHA-256: `344647efbb75febe09f35231398fe216e15b30c29f0783c12924164d5b69a9e9`. Independent review was requested from the separate finite-arithmetic reviewer; this author does not self-certify mathematical independence.
