# Corrections and clarifications

## Required corrections

None. The sealed proof and result are acceptable as written as a historical partial result.

## Optional algorithmic clarification

If this work is later described as an algorithm, use the following bounded wording:

> Given a maximal-order basis, complete ideal-class representatives, generators for the necessary unit images, the conductor, and the field automorphisms, each multiplier-order orbit reduces to a finite subgroup enumeration and finite orbit computation. The present note proves this structural reduction and finiteness; it does not implement general class-group/unit computation or determine the resulting sail-face and torus geometry.

This is an authored clarification, not copied source language. It guards against turning a correct finiteness argument into a stronger software or complexity claim. No change to the mathematical theorems is needed.

## Scope guardrails to preserve

- Use the complete eight-sail union and the source's integer-linear equivalence.
- Keep all full lattices and multiplier orders; do not replace them by invertible ideals of one selected order.
- Use the recovered-order discriminant, not an arbitrary operator-polynomial discriminant.
- Quotient by actual field automorphisms, not arbitrary embedding permutations.
- The determinant-sign argument uses central symmetry and odd ambient dimension; do not silently apply it to a single sail or another dimension.
- Keep PARTIAL status and the absence of novelty/current-global-openness claims.

These guardrails already hold in the candidate and do not require a patch.
