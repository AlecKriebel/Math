# Research log

## 2026-07-24 15:10 PDT

- Started from the independently replayed exact `h=0` profile whose two
  twelve-letter words repeat after six classes.
- Identified its stabilizing class half-turn with multiplication by 64
  modulo 333.  Preserving that action on complete words would enter the
  recently excluded fixed order-six multiplier family, so only
  symmetry-breaking placements can be viable.
- Split the rank-18 first placement system into half-turn eigenspaces.  The
  36-dimensional translation space decomposes as `21 + 15`.
- Derived the exact equivariant second-digit normal form: twelve active
  even quadrics and six odd bilinear equations.  All six `21 x 15`
  bilinear blocks have rank 15.
- Exhausted the 364 projective combinations of the bilinear pencil.  The
  rank histogram is `{15:361, 14:1, 12:1, 11:1}`.  The exceptional kernels
  contain 109 distinct odd directions including zero, yielding the exact
  six-equation zero count `205,901,492,005,503`.
- Tested all 36 global quotient-position permutation pairings between
  opposite classes.  Seventeen fail the first placement digit.  Eighteen
  leave affine dimension nine; exhausting all 354,294 points across those
  families gives no complete second-digit survivor.  Identity/identity is
  the sole dimension-21 family and is the fixed multiplier-64 control.
- Conclusion: the obvious fixed or globally twisted half-turn does not
  provide a construction.  Any useful symmetry breaking must vary between
  class pairs, residues, or channels rather than use one global fiber
  permutation.
