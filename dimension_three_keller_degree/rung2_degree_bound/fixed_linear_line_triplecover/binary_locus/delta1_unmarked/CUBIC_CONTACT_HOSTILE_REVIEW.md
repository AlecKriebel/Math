# Hostile review: cubic unmarked contact component

Audit `CUBIC_CONTACT_GCD_NOTE.md` from the unspecialized contact equations.

- Reproduce the generic-chart contact eliminant with saturation by every
  normalization denominator.  Confirm that \(C(a)\) is a genuine
  component and that its coordinate formulas in (1) lose no endpoint.
- Substitute (1) into all six contact coefficients, not merely the final
  eliminant.  Check the Jacobian and curvature sign conventions.
- Verify identities (4)--(6) by polynomial reduction modulo \(C(a)\) in
  a second exact system.
- Do not infer divisibility from pairwise resultants: check the literal
  common quadratic \(G\).
- Check that the conclusion requires only \(\deg(qG)=3\), including if
  \(G\) becomes reducible or non-squarefree at a root of \(C\).
- Mutate one coefficient of \(G\) and one coefficient of \(R\); require
  both independent reconstructions to fail.
- Restrict the conclusion to this cubic contact component.  This note
  does not close the \(a_3=1/2\) lower branch, other rational eliminant
  factors, or any boundary chart.
