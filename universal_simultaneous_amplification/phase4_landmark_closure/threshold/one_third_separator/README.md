# One-third endpoint separator

This folder studies the sharp remaining affine candidate

```text
(1/3) rho_Bd(G)/rho_Bd(K_n) + (2/3) rho_dB(G)/rho_dB(K_n) <= 1
```

at fitness `r=3/2`.

What is proved:

- the exact Green--Poisson identity for `e_B+2e_D`;
- a proved sharpness theorem, using the independently hostile-audited
  mesoscopic-core lemma, which forces every universal affine Bd coefficient
  to be at most `1/3`;
- an exact necessary coefficient window
  `0.088542283991... <= theta <= 1/3` for any universal convex affine
  separator (no coefficient in the window is yet proved universal);
- an exact `L--C--D` dual split and Poisson--Dirichlet identity, together
  with a rational weighted six-cycle proving that its separate `1:2`
  orientation sign is false even though batching preserves the full target;
- the candidate is strict for every nonconstant positively weighted triangle;
- a seven-atom exact barrier to arbitrary pointwise common corrections;
- exact survival of all saved Pareto witnesses and the finite
  clique--pendant product counterexample;
- exact refutation of two severe near-disconnected floating artifacts,
  including a false order-six score above `1.06`.

What remains open:

- the universal sign for arbitrary finite connected undirected weighted
  graphs;
- no simultaneous endpoint amplification, and therefore the exact value of
  `R_sim`.

Replay the proof components from the repository root:

```bash
./universal_simultaneous_amplification/phase4_landmark_closure/threshold/one_third_separator/replay.sh
```

`search_oriented_windmill_affine.py` is discovery code and is deliberately
not part of the exact replay.
