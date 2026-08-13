# Research log: locked-history transfer

## 2026-08-13 -- exact transfer and finite-terminal obstruction

- Derived the exact labelled dB history transfer.  Splitting a geometric
  batch into no selective sample versus at least one selective sample gives

  ```text
  T_r = diag(1,r-1)/r.
  ```

  Retaining that bit for `L` stages gives conditional ratio `(r-1)^L`.
- Proved that the labelled bit cannot factor through an ordinary finite
  union-set terminal.  For every source `u`, both history classes output the
  singleton `{u}` with positive probability.  Their exact likelihood ratio
  on this common atom is

  ```text
  (r-1)p_u/[r-(r-1)p_u].
  ```

- Derived the exact projected union-set channel.  For a row law `p`, its
  singleton mass is `sum_u p_u/[r-(r-1)p_u]`; the excess over `1/r` is an
  explicit positive collision sum.
- For uniform fan-out `m`, the projected adverse/favorable ratio is exactly

  ```text
  (r-1)(1-1/m).
  ```

  At depth `L`, the relative loss from the ideal `(r-1)^L` is at most
  `L/m`.  Thus a growing diffuse fan-out with `L/m->0` removes the finite
  collision obstruction.
- Stated the full undirected scale-separation obligations: diffuse parent
  rows, one locked target throughout a batch, ordered handoff, suppression
  of reciprocal reverse entrances, and stage/reservoir initialization mass
  below the favorable response scale.
- Distinguished relative accuracy from the much stronger absolute uniform
  accuracy on `I_k=[1+1/k,2-1/k]`, which would require total error
  `o(k^{-L_k})`.
- **PROVED:** abstract history-level exponentiation exists; exact finite
  two-terminal factorization is impossible.
- **OPEN:** realize the diffuse ordered trace by one undirected graph family
  and identify its two channels with net Bd gain and dB cost after full
  uniform-start accounting.
- Best-guess completion of the exact-threshold program: **72%**.
