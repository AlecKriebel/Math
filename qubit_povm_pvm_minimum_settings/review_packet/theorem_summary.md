# One-page theorem summary

## Problem

Fix local Hilbert-space dimension at most two in a bipartite Bell experiment.
Allow arbitrary two-qubit mixed states, arbitrary finite declared output
alphabets, shared classical randomness, zero projectors, deterministic
relabeling, and stochastic output postprocessing. Do not allow a local ancilla
or Naimark dilation that raises the local dimension.

The question is the minimum number of measurement inputs needed for qubit
POVMs to generate a Bell behavior outside the shared-randomness convex hull of
fixed-qubit PVM behaviors.

## Main classification

For every finite output architecture with two inputs per party,

\[
\overline{\mathsf Q}^{\mathrm{POVM}}_2(\mathbf A,\mathbf B)
=
\overline{\mathsf Q}^{\mathrm{PVM}}_2(\mathbf A,\mathbf B).
\]

The equality concerns convexified behavior sets. It does not assert that an
individual POVM is a PVM or that simulation preserves the original state.

There is also an explicit rational `3 x 2` Bell functional

\[
\begin{aligned}
\mathcal B={}&10(E_{00}+E_{01}+E_{10}-E_{11})\\
&+\frac35p(0,0|2,0)+\frac35p(1,1|2,0)
+\frac45p(2,0|2,1)
\end{aligned}
\]

with exact certified bounds

\[
\beta_{\rm POVM}\ge\frac{16+8\sqrt{7813}}{25}
>
20\sqrt2+\frac35+\frac{4+3\sqrt2}{250}
\ge\beta_{\rm PVM}.
\]

Therefore `3 x 2` is the minimum input architecture, up to exchanging the
parties.

## Proof mechanism

1. A Lorentz-cone circuit theorem simulates every two-input behavior when one
   party is binary on both inputs.
2. Extreme-point and common-span filtering arguments reduce any other
   separator to a pure entangled state with one binary PVM and one ternary
   rank-one POVM per party.
3. The residual strategy set is represented by a 14-dimensional Lorentz
   incidence manifold.
4. Finite POVM duality forces five strictly positive determinant multipliers
   at a hypothetical strict separator.
5. An exact quadratic form has inertia `(4,12)`. Rank at least two of the
   metric differential leaves a positive second-order direction; rank one is
   incompatible with positive multipliers; rank zero has an explicit
   deterministic local decomposition.

## Verification

Run:

```sh
./run_all.sh
```

The offline suite checks the exact `3 x 2` strategy and bound identities,
Lorentz and exceptional-fiber identities, Hessian square completion, and an
independent rational rank-zero simulation.

Repository:
<https://github.com/AlecKriebel/Math/tree/main/qubit_povm_pvm_minimum_settings>

