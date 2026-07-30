# Private response framework for likely referee objections

## 1. “The theorem is only about convex hulls.”

Correct. Shared classical randomness is explicitly part of both operational
classes. The manuscript never claims raw-strategy-set equality. Linear Bell
optimization is unchanged by this convexification, and minimum-setting
separation is therefore classified for the stated operational model.

## 2. “Shared randomness changes the physical problem.”

It changes the raw realization set and is consequently stated prominently.
It is standard free classical coordination in the comparison being studied.
The paper also flags raw-set equality without convexification as open.

## 3. “Why do arbitrary finite outputs reduce to ternary outputs?”

The reduction begins at an extreme exposed maximizing behavior, chooses
extremal POVMs, forces scalar-only span intersections, and uses
`dim Herm(2)=4`. One measurement span is binary; the other has dimension at
most three. Linear independence and the extremal support-perturbation bound
`sum rank(M_a)^2 <= 4` leave three rank-one effects. Zero effects and
postprocessed labels are retained as declared outcomes.

## 4. “Four-outcome qubit POVMs are extremal.”

They can be extremal in isolation, but cannot occur in the selected residual
maximizer after the common-span dimension restriction. The claim is
behavior-dependent and does not deny tetrahedral POVM extremality.

## 5. “Filtering may alter the full behavior.”

The common-span lemma gives the exact eventwise identity
`q_± p_±(a,b|x,y)=r^±_{a|x}p(a,b|x,y)`. Averaging signs reproduces every event,
not merely marginals.

## 6. “The binary-party decompositions might differ by input.”

The proof decomposes the equality between the two compressed ensembles into
circuits. Each circuit simultaneously realizes both inputs on one
purification, and circuit weights form one shared variable for the entire
behavior.

## 7. “The incidence variety may contain unphysical points.”

The physical-completeness theorem reconstructs future-null Alice effects,
future-null steered operators, a full-rank reduced state, Bob POVMs, and a
pure state from every nearby strict incidence point. Probability positivity
is then automatic.

## 8. “Equality constraints do not have signed multipliers.”

The nonnegative signs do not come from equality-constrained KKT conventions.
They come from positive-semidefinite POVM dual slacks and full-rank steering.
The manuscript derives the scale relation explicitly for each input.

## 9. “A tangent need not be a physical curve.”

Constraint differentials are independent, so the regular level-set theorem
integrates every incidence tangent. Physical signature, time orientation,
positive marginals, and full rank are open.

## 10. “The exceptional fibers are incomplete.”

Appendix G treats the generic inverse and all four components of its
degeneracy divisor: `x2=0`, `x3=0`, `x0=x1`, and `x2=x3`, including the two
zero-coordinate subcases omitted from early notes.

## 11. “The rank-zero capacities might fail.”

The antisymmetric-flow variable lies in three closed intervals. The Gram row
relations give pairwise intersection; for real intervals pairwise
intersection implies common intersection. This includes zero capacities.

## 12. “The `3 x 2` upper bound may optimize only the displayed state.”

It does not. The proof first optimizes the state to a Bell-operator
eigenvector, puts an arbitrary pure state in Schmidt form, exhausts all six
ternary-PVM rank patterns, and controls all Bloch directions.

## 13. “Which orientation is minimal?”

The architecture is `3 x 2` up to exchanging Alice and Bob.

## 14. “What prior result is closest?”

The Vértesi--Bene `I_CH3` construction already demonstrated a qubit POVM
advantage in the same broad input/output architecture. The present
classification claim is the universal `2 x 2` equality plus exact
minimum-input conclusion, not the broad existence of a qubit POVM advantage.

## 15. “What role did AI play?”

Generative AI assisted exploration, proof development, code, audits, and
manuscript drafting. The human author assumes responsibility. The release
does not claim independent expert human verification; exact scripts verify
encoded algebra and explicit constructions only.

