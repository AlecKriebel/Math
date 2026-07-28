# Checkpoint 4A — Paper Proof Adversarial Review

**Date:** 2026-07-28  
**Reviewer role:** independent proof auditor  
**Final verdict:** PASS

## Initial NO-GO findings

The compressed manuscript introduced three defects not present in the formal
checkpoint:

1. Table 1 called every right-column value exact-target validation, although
   the stochastic value was half the closed-form route-to-route MMD and no
   stochastic reset law was defined.
2. The operational protocol said only to record a directional failure; it
   omitted the claim-matched action for deterministic and stochastic failure.
3. Several Boolean-cube expressions wrote \(S\cup i\) although \(i\) is an
   element rather than a set.

## Repairs and final verification

- Retitled the table column “Post-audit validation,” separated deterministic
  exact-target validation from the stochastic population route radius, and
  stated explicitly that the latter defines no reset law.
- Restored deterministic failure rejection and stochastic failure-symbol or
  failure-probability semantics.
- Replaced every affected union by \(S\cup\{i\}\) or \(S\cup\{j\}\).

The reviewer then rechecked all theorem quantifiers and constants, the MMD
concentration rule, affine reconstruction, ridge defect and commutation
criterion, objective constants \(1/8\) and \(\lambda/8\), SMW formula, and
every numerical value. The rebuilt PDF received **PASS**.
