# Problem 2303016: credited direct capacity proof

**Reviewed disposition: already_solved, 1/5. Full source/method/proof review: PASS.**

For compact E in R^n, n >= 3, the points of E where the integrated local-capacity Wiener expression is finite form a polar set. The source already knows this consequence of Kellogg and requests a direct proof. This packet supplies a method-compliant Newtonian energy argument, crediting the classical capacitary strategy of Hedberg–Wolff (1983), pp. 173–174. No novelty or priority claim is made.

- [Complete direct proof and precise sharpness](TURN_1.md)
- [Exact original scope and method requirement](SOURCE_NORMALIZATION.md)
- [Independent full source/method review](final_review/REVIEW.md)
- [Result and limitations](RESULT.md)

The argument proves its equilibrium first-variation and weak potential bounds, localizes to uniformly small integral tails, and obtains an energy contradiction. It does not invoke Kellogg, a Dirichlet-boundary theorem or the Wiener equivalence. Standard Borel capacitability and capacity-zero/polar equivalence remain explicit foundations. Ordinary Choquet capacitability is distinguished from the fine-topological Choquet property.

The denominator exponent is critical under every positive power weakening, and an uncountable polar set can be the entire exceptional set. No universal claim about all nonintegrable gauge weakenings is made.

All 14 frozen author files and all review files are unchanged; their historical pending-review wording is retained, while this wrapper records the completed PASS.

## Replay

Author checks use standard-library Python:

    python verify_turn1.py > /tmp/turn1.json
    cmp TURN_1_CHECKS.json /tmp/turn1.json

Independent replay is already portable when given this directory. It requires **SymPy** in addition to Python's standard library:

    python final_review/check.py . > /tmp/review.json
    cmp final_review/CHECKS.json /tmp/review.json

The author has 2,690 scalar controls; the independent review has 1,909 controls and replays the author output. The analytic all-set proof was reviewed separately; finite controls do not certify polarity. Primary PDF identities are recorded in SOURCE_MANIFEST.json, but PDFs/imported records/private material are not redistributed.
