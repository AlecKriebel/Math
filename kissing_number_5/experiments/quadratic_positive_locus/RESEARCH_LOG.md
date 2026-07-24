# Research log

## 2026-07-23

- Reformulated failure of nonnegative weighted centering plus isotropy as
  strict positivity of a mean-zero degree-at-most-two polynomial on every
  code point.
- Removed the spherical constant term by using a traceless quadratic matrix.
- Established the canonical normalization
  \(\lambda_{\max}(A)=1\), ordered eigenvalues in \([-4,1]\), and
  coordinate signs \(b_i\geq0\).
- First imported the exact enlarged-cap theorem at height \(-1/300\), giving
  a preliminary cutoff \(\|b\|<300\).
- Classified both axisymmetric spectral endpoints exactly.  For
  \(1-5t^2+\beta t\), the preliminary theorem eliminated
  \(\beta\geq17999/60\).  For \(5t^2-1+\beta t\), it eliminates every
  \(\beta\geq4\).
- Ran reproducible four-start direct 41-point construction attacks in the
  pure belt, pure two-cap, and shifted-cap loci.  The best maximum inner
  products were respectively 0.5375770409, 0.5562907281, and 0.5574466962,
  all with positive recorded quadratic margins.  These runs are numerical
  evidence only.
- Scanned sampled axisymmetric positive-kernel SDPs.  The pure belt gave
  audited floating objectives about 44.13 (degree 6) and 43.04 (degree 8).
  A coarse enlarged-cap scan at height \(-1/50\) produced a rescaled random
  audit near 40.52, but the underlying sampled kernel violated unsampled
  off-diagonal inequalities.
- Reoptimized degree eight with explicit negative-face and symmetry-ridge
  samples.  After PSD projection and rational Gram-factor extraction, an
  exact Bernstein audit succeeded on the entire cap \(u\geq-1/50\):
  \(F_{\rm off}\leq-9/10\), \(F_{\rm diag}\leq35\), so
  \(|C|\leq359/9<40\), hence \(|C|\leq39\).  The tree has 1,344 leaves,
  maximum depth 21, and digest
  `1bf44242737474073736f8ce772e6433bab6fe4ea5d869fb10a660f413069ef1`.
  This improves the canonical residual cutoff to \(\|b\|<50\) and the
  \(q_-\) endpoint to \(\beta<499/10\).
- Specified a parameter-dependent positive-kernel/SOS certificate over the
  full compact residual family.  The next computational priorities are:
  (i) stabilize and exactly audit the \(-1/50\) cap candidate; (ii) solve
  parameter-uniform axisymmetric belt/two-cap SDPs; (iii) only then lift to
  the full eight-parameter matrix-SOS problem.
- Hardened both exact proof verifiers against optimized Python: all
  proof-critical checks now raise always-on exceptions, factor shapes are
  prevalidated before calling shared arithmetic helpers, and `python -O`
  tests reject tampered enlarged-cap and reduction certificates.
