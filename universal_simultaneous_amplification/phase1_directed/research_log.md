# Directed phase-one research log

## 2026-08-01 (America/Los_Angeles)

* Fixed the convention `w_uv = source u -> dead target v`; dB normalization
  is therefore columnwise.
* Derived the complete-support extinction system at `x=1/r` and proved its
  analyticity at `x=0` from transience of the limiting finite chain.
* Differentiated the first-step equations.  Verified that derivatives vanish
  for states of size at least three, computed the directed doubleton loss
  term, and averaged singleton derivatives.
* Obtained
  `A_dir=sum_{v,u!=v}(d_v^- - w_uv)/w_uv` and proved exactly that
  `A_dir-n(n-1)(n-2)=E_dir`, the proposed incoming-column square defect.
* Classified equality as independent constant incoming columns.  Proved this
  class is exactly dB-equivalent to `K_n` under column scaling for every
  fitness.
* Ran exact `QQ(r)` subset-chain checks on two asymmetric triangles and one
  asymmetric four-vertex matrix.  All coefficients matched.  A
  column-uniform, row-nonuniform matrix tied `K_4` exactly while its wrong-row
  defect was `1131/77`, falsifying the source-target-swapped alternative.
