# Author validation and independent-review requirements

The single substantive route produced a complete counterexample before exhausting the five-turn budget. This file records author checks only; it is not an independent audit.

## Reproduction

From the package directory, run:

`python3 controls/check.py`

The deterministic output must equal `controls/expected.json` byte for byte. No network, source downloads, third-party packages, GAP, SnapPy or Sage are required.

Results: the chosen free word reduces to 16 letters; all 30,625 ordered pairs from 175 elements of the declared Z²⋊Z box satisfy the metabelian witness identity. Of those pairs, 29,464 do not commute. A positive noncommuting test prevents accidentally replacing the group by its abelianization. Exact orbifold Euler characteristics are −1/42, −1/20 and −1/12. Euclidean and spherical comparison triples give 0 and +1/30. The finite exceptional-slope partition is disjoint and complete relative to the cited classification.

## Limits

The finite model test does not prove the universal group law; §§2–3 of PROOF.md do. The script does not compute any knot filling, certify a hyperbolic triangulation, verify an orbifold presentation from a surgery diagram, or establish novelty. Those topological inputs are read as credited classical results at the cited locations. A fresh reviewer must check the source interpretation and imported hypotheses, rather than treating passing code as a theorem.

## Essential adversarial checks

1. The original quantifier is all eligible knots, and the surgery-kernel expression uses a union over all rational slopes.
2. Slope zero is included, whereas only the meridional slope infinity is excluded.
3. Figure-eight is hyperbolic and every rational filling has infinite fundamental group; verify each exceptional-slope class and the complement separately.
4. Zero surgery is a torus bundle. Verify this against [S4] as well as [S2], whose electronic text has the disclosed D-shaped glyph.
5. Torus-bundle groups are metabelian. This is stronger than merely infinite or torsion-free and imposes the displayed nontrivial free-group law.
6. The length-16 witness is nontrivial for any freely chosen basis of any F₂ subgroup. The witness may depend on the basis; the slope zero is fixed.
7. The 2026 question is disclosed. The argument does not settle whether at least one hyperbolic knot admits a persistent F₂, or an all-but-finitely-many-fillings variant.
8. Source typography and the unread 2024 full text are disclosed. No historical-priority conclusion is drawn from the bounded literature search.

The intended final status is `claimed_solved`, `1/5` only after an independent gate accepts the exact literal claim. No remote write, merge, release or external communication is authorized by this validation record.
