# Research log: endpoint global action

## 2026-08-13 -- global minimum theorem

- Revisited the natural endpoint actions after the exact Fenchel/Bregman
  obstruction.  Their lack of convexity does not prevent a global variational
  theorem.
- Proved the sharp scalar inequality

  ```text
  D_Phi(x,y) >= (x-y)^2 / (2(1-y)).
  ```

  Its proof uses the physical constraint `(1-y)Z<=1`; this is the factor
  missed by a naive uniform-curvature estimate.
- Combined the scalar remainder with the Bd ground `b` and the dB ground
  `as`.  Each complete action remainder is exactly a nonnegative scalar
  remainder plus a Picone edge square.
- Concluded that the active Bd and dB endpoints are the unique global
  minimizers of their respective nonconvex actions on the physical cube.
- The theorem certifies both cross-action remainders globally.  It does not
  yet compare them to the leaf-annihilating support, whose sign remains open.

