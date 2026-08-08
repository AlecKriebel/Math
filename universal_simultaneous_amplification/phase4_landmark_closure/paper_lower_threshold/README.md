# Simultaneous amplification below fitness three halves

This folder contains the fallback lower-bound paper and its exact replay
package.

## Proved result

The explicit rational center--triangle family satisfies

\[
\rho_{\mathrm{Bd}}(G_N,r),\rho_{\mathrm{dB}}(G_N,r)\longrightarrow 1/3
\]

for every fixed `r>1`. It therefore simultaneously amplifies every fixed
`1<r<3/2` for all sufficiently large `N`, proving `R_sim >= 3/2`. The same
family suppresses both rules at `r=3/2`, with exact order-`N^-2` deficits, and
for every fixed `r>3/2`.

The universal upper bound and exact value of `R_sim` remain **OPEN**.

The package also contains an exact finite endpoint counterexample to two
stronger candidate separators.  The unweighted graph obtained from `K_32` by
attaching four leaves to one hub has normalized Bd/dB values `x,y` with
`xy>1` and `(x+y)/2>1`, while `y<1`.  Thus the product and balanced mean are
false universally, but the disjunctive endpoint obstruction remains open.

A growing clique--pendant family has normalized endpoint limits `32/27` and
`8/9`, so the product tends to `256/243>1`.  Varying its leaf proportion
proves that every universal convex affine separator must assign Bd weight at
most `1/3`.  The sharp one-third candidate is proved for every positive
weighted triangle but remains open for arbitrary graphs.  A separate class
theorem shows that arbitrary positive pendant weights cannot rescue any
clique--pendant family with an unbounded number of leaves.

## One-command use

From this folder:

```sh
./replay.sh
./build.sh
```

`replay.sh` runs the exact construction and structural certificates and
writes individual logs under `output/verification/`. `build.sh` compiles
`main.tex` with Tectonic and writes the final paper to
`output/pdf/simultaneous_amplification_below_three_halves.pdf`.

For a complete local refresh, use:

```sh
./all.sh
```

The graph image in `assets/` is a PNG rendering of the audited source asset
`../construction/center_triangle_diagram.svg`.

## Status discipline

- **PROVED:** the lower bound `R_sim >= 3/2` and the exact interval of the
  displayed family.
- **EXACTLY COMPUTED:** the isolated triangle formulas and endpoint
  coefficients; the 36-vertex product and balanced-mean counterexample.
- **PROVED:** a growing nonvanishing product violation, sharpness of the Bd
  affine coefficient `1/3`, the one-third inequality for weighted triangles,
  and the arbitrary-weight growing clique--pendant obstruction.
- **FALSIFIED:** the universal normalized-product and balanced-arithmetic
  endpoint separators.
- **OPEN:** a universal upper bound, endpoint impossibility for arbitrary
  graphs, and the exact value of `R_sim`.

No release, DOI, submission, or external contact is performed by these
scripts.
