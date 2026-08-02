# dB maximization and cross-rule sum investigation

## Closed result: the dB maximizer conjecture fails through `r=9/5`

Let `G` be the seven-vertex weighted windmill with center `0`, blades
`(1,2),(3,4),(5,6)`, equal center attachments on each blade of weights

    (100, 10, 1),

and internal blade weights

    (600, 1200, 1800).

Then the exact dB chain gives

\[
 \rho_{\rm dB}(G,3/2)=0.3175490238143979\ldots
 >\frac{1458}{4655}
 =\rho_{\rm dB}(K_7,3/2).
\]

`verify_r_three_halves_counterexample.py` independently constructs the full
126-transient-state chain and the 52-transient-state lumped chain, proves
their transitions agree orbit by orbit, solves both over the rationals, and
checks the exact positive excess.

A second exact example raises the fitness to `7/4`.  It is the nine-vertex
four-blade windmill with

    outer    = (1, 40, 2400, 200000),
    internal = (9000000, 3800000, 2000000, 920000).

It satisfies

\[
 \rho_{\rm dB}(G,7/4)=0.387510078397605232\ldots
 >\frac{6588344}{17097795}
 =\rho_{\rm dB}(K_9,7/4).
\]

`verify_r_seven_fourths_counterexample.py` checks every one of the 512
labelled transition rows against the 162-state orbit chain and solves its 160
transient equations exactly.

A five-blade example reaches `r=9/5`.  On eleven vertices, take

    outer    = (1, 6, 120, 3500, 60000),
    internal = (9000000, 2500000, 880000, 410000, 190000).

Then

\[
 \rho_{\rm dB}(G,9/5)=0.410344367875481897\ldots
 >\frac{1937102445}{4780900817}
 =\rho_{\rm dB}(K_{11},9/5).
\]

`verify_r_nine_fifths_counterexample.py` uses exact FLINT rationals to check
all 2048 labelled transition rows and solve the 484 transient orbit
equations.

## Exact cross-rule diagnostic

At `r=3/2`, the complete graph maximizes
`rho_Bd+rho_dB` among all positive weighted triangles, strictly except at
equal weights.  The comparison numerator has the exact manifestly
nonnegative form

\[
 2\sum_{(i,j,k)}q_{ijk}
 \sum_{(x,y,z)\in\operatorname{Perm}(a,b,c)}
 x^iy^jz^k(x-y)^2,
 \qquad q_{ijk}>0,
\]

with 24 displayed rational coefficients in
`verify_triangle_sum_r_three_halves.py`.  That verifier derives both
six-state chains and checks the decomposition symbolically.

## Status of the universal questions

- **PROVED:** `K_n` is not a universal dB maximizer for thresholds
  `r>=3/2`, `r>=7/4`, or `r>=9/5`.
- **OPEN:** whether `K_n` is a universal dB maximizer for every `r>=2`.
- **OPEN:** whether `K_n` universally maximizes `rho_Bd+rho_dB` at
  `r>=3/2`, or even just at `r=3/2` for arbitrary `n`.
- **NUMERICALLY OBSERVED:** no sum counterexample in the finite and lumped
  searches recorded in `RESEARCH_LOG.md`.
- **PROVED FAILED ROUTE:** averaging a graph with a vertex-permuted copy can
  decrease the sum, so direct symmetrization monotonicity is false.

All numerical optimization here is discovery only.  Exact claims are backed
by absorbing-chain or polynomial certificates.

## Programs

- `search_db.py`: cancellation-safe full-subset Bd, dB, and sum search.
- `random_sum_search.py`: broad random sum reconnaissance.
- `search_gadget_sum.py`: separated star-of-gadgets limit search.
- `search_two_class_sum.py`: exact two-count lumping for dense equitable
  two-class graphs.
- `search_windmill_db.py`: exact blade-count dB/Bd evaluation and numerical
  optimization for heterogeneous windmills.
- `verify_r_three_halves_counterexample.py`: exact dB counterexample.
- `verify_r_seven_fourths_counterexample.py`: stronger exact dB
  counterexample.
- `verify_r_nine_fifths_counterexample.py`: exact dB counterexample at the
  largest certified fitness in this folder.
- `verify_triangle_sum_r_three_halves.py`: exact triangle sum certificate.
