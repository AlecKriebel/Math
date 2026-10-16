# Substantive approach log

## Approach 1: determinant and anticanonical degree

The slope inequality gives epsilon(-K_X;x)>=n epsilon(T_X;x)>0. For a rational normalization through x, every splitting degree is positive and one is at least two, yielding -K_X.C>=n+1. Both deductions are retained in the proof and controls.

This route alone was insufficient: positivity need not exceed the anticanonical Seshadri threshold n, and an estimate for rational curves through an arbitrary point does not automatically satisfy a general-point characterization. Dropping multiplicities is also invalid. No resolution was claimed at this stage.

## Approach 2: minimal pointed family and Picard reduction

The new direction minimizes a fixed very ample degree among all rational images through x, rather than minimizing anticanonical degree or assuming a general point. The stable-map boundary has a component through x; its degree already exhausts the total minimum. Stability then removes contracted trees with the sole marking. This yields a proper pointed family. Very freeness supplies smooth evaluation at a chosen map in any characteristic. Properness upgrades dominance to surjectivity. The contracted marking section trivializes the descent of each fiberwise degree-zero divisor pullback, forcing every divisor to be proportional to the chosen very ample class. The anticanonical class is thus ample, reducing to the proven Fano case.

The full proposed argument and all dependencies are in candidate_proof.md. The author stopped after this candidate completion, without inventing three additional approaches to fill the five-approach budget. Two independent geometry audits of the original candidate subsequently passed; this expanded v2 remains subject to a final delta audit, especially of the explicit moduli, section, and positive-characteristic justifications. Numerical tests cannot substitute for that review.
