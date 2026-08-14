# Three proof steps most likely to fail

## 1. Arbitrary positive right scaling in the hardness reduction

A mass-action equilibrium multiplies the Jacobian factor on the right by an arbitrary positive diagonal matrix. If that scaling could stabilize a lifted NO instance, the reduction would fail. The proof must be checked at the path endpoints: `L(0)D` has exactly one positive eigenvalue for every `D>0`; a Hurwitz endpoint has the opposite signed determinant; an interior singularity transfers to the unscaled open-cube family because `D` is nonsingular and `det L(q)=(-alpha)^d det B(q)`.

## 2. Equality of the entire mass-action row image

Constructing one flux witness is insufficient. The steady-flux equations must imply that **every** positive flux has row parameters `rho>0` and `q in (-1,1)`, with no hidden cross-row coupling. This follows only because all stoichiometric columns in row `i` are `+e_i` or `-e_i`, so `Gamma v=0` separates rowwise.

## 3. Fixed-species bit complexity

Fixed ambient dimension alone does not prove polynomial time when there is one flux variable per reaction. The proof depends on circuit supports of size at most `n+1`, polynomial-bit minor generators, complete projection of their cone, fixed-dimensional relative-facet conversion including lineality/lower dimension, and a fixed-variable real-algebraic decision bound.
