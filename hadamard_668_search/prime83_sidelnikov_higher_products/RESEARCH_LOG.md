# Research log

## 25 July 2026: higher-product prime-83 exclusion

- Extended the previously closed degree-at-most-two Sidelnikov lane to two
  strictly larger finite families.
- Proved and checked the endpoint-fold inverse-pair condition
  \(U_kU_{-k}=v_kv_{-k}\) for all \(1\leq k\leq41\).
- Exhausted the independently decimated degree-at-most-three family:
  3,910,048 canonical affine binary representatives reduce to 5,434 exact
  row-compatible `U/V` states, and none has a full integer `C/D` PAF
  decomposition.
- Exhausted the un-decimated degree-at-most-four family: 325,835 exact
  row-compatible `U/V` states yield 179,221 distinct required full PAF
  vectors, and none has a `C/D` decomposition.
- Replayed both computations against byte-frozen output, checked the separate
  Python semantic certificate, and passed AddressSanitizer and
  UndefinedBehaviorSanitizer.
- Scope boundary: independently decimated degree four, degree five and higher,
  arbitrary character products, unrestricted `BS(84,83)`, and `H(668)` remain
  open.  No Hadamard candidate was produced.
