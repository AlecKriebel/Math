# Research log: pairwise resultant norms

## 2026-07-25

- Derived the three separate necessary equalities
  `nu_(A,r)=nu_(B,r)`, `r=0,1,2`, from the primitive ratio-torus equation.
  Recorded why the total resultant norm is only their product.
- Factored `167^3-1` exactly as `2*83*28057`; these give nine scalar
  character gates across the three star-pairs.
- Built an independent PARI model directly from `Phi_37`, the promoted
  `FACTOR_PLUS`, and the promoted pinned-alpha construction.
- Audited exact nine-trit physical slices for fifteen channel alphabets and
  ten A/B joins.  Every order-2 and order-83 marginal image is full.  Every
  order-28,057 scalar equality has positive witnesses.  Contractions track
  the random character orders closely.
- Observed zero simultaneous order-28,057 hits in each pinned slice join.
  Rejected this as a profile obstruction because the expected count in a
  slice is only about `0.0000175`.
- Estimated the complete margin-conditioned three-key join.  Nine-trit
  batching leaves about `5.092e12` channel evaluations and tens of
  terabytes of exact keys.  Concluded that batching alone is infeasible on
  the 16 GB machine.
- Stopped without expanding the raw slices, contacting anyone, modifying
  promoted files, committing, or pushing.
