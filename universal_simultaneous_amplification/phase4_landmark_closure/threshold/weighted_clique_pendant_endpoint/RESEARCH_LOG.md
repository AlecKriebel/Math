# Research log

## 2026-08-08

- Derived the exact common-weight Bd and dB lumped rows directly from the
  update definitions and checked their `w=1` specialization against the
  existing unweighted chain.
- Optimized the normalized endpoint minimum `M` over a common pendant weight
  for finite graphs.  No `M>1` case appeared; one-pendant cases approach one
  from below as the clique grows.
- Optimized the surviving affine candidate `S=(x+2y)/3`.  No `S>1` case
  appeared through the recorded run (`n<=24`); the best case there was
  `c=22,m=1,w approximately 11.1756188`, with
  `Bd approximately 1.01383206`, `dB approximately 0.97666728`, and
  `S approximately 0.98905554`.
- A larger one-pendant check confirmed the limiting near-equality regime:
  at `c=1600`, the optimized minimum occurred near `w=2325.88` and was
  `M approximately 0.99972738`, with Bd ratio approximately `0.99985053`.
  Thus the sampled supremum is one from below, not a plausible witness.
- Added a two-weight symmetric leaf search.  Through `n<=10`, both the `M`
  and `S` optimizers collapsed numerically to equal weights and remained
  below one.
- Replaced the sampled obstruction by a proof uniform over arbitrary
  individual pendant weights.  The key estimates are an `O(1/c)` rescue
  bound for a core singleton and the exact aggregate leaf bound
  `sum u_L <= r`.  This proves eventual dB suppression whenever `m->infinity`.
