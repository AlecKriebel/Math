# Perron/robust-depth hybrid

This isolated experiment combines the exact enlarged-cap consequence
\[
\#\{i:\langle e,x_i\rangle<-1/300\}\geq7,\qquad
\#\{i:\langle e,x_i\rangle>1/300\}\geq7
\]
with the Lorentzian/Perron representation of a hypothetical 41-code.

The outcome is a rigorous **barrier**, not a kissing-number resolution:

* exact Perron-axis and covariance identities are derived;
* the depth theorem supplies a strict variance inequality;
* an exact one-parameter scalar/frame family shows that these consequences
  permit \(\rho\to42\) and frame potential tending to the Welch minimum;
* exact 41-vector modifications of \(D_5\) show that global robust depth,
  the common rank-five Gram structure, and both the noncentered and centered
  Perron endpoints coexist when the kissing sign is relaxed.

The precise failed hypothesis is recorded in each construction.  In the
noncentered construction only the duplicated unordered pair has inner
product greater than \(1/2\).  The centered construction has explicit
inner product \(\sqrt3/2>1/2\).

Run the independent standard-library verifier from the repository root:

```sh
python3 experiments/perron_robust_depth_hybrid/verify.py
python3 -m unittest \
  experiments.perron_robust_depth_hybrid.test_verify -v
```

No floating-point arithmetic, solver output, or finite grid is trusted.
