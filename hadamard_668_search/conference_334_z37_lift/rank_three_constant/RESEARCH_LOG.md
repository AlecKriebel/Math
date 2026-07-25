# Research log: constant rank-three \(z\)-adic conjugators

## 2026-07-25 PDT

- Classified the complete projective rational similarity over-list for
  rank-three matrices over \(\mathbf F_{37}\): 1,452 types.
- Replaced the loose all-entry-product code by a symmetry-reduced temporal
  code derived from
  `diag(A^r M A^s)=diag(A^s M A^r)` for symmetric `A,M`.
- Verified that every minimal polynomial has degree at most four and that
  the resulting binary intersection has at most 256 words.
- Exhausted all types against the frozen 625 quotient profiles.  The
  diagonal weight gate removed 492 types and left 960.
- Restored the fixed rank-one `J` term.  For each residual type, exhausted
  both trace orientations and every relaxed local power tuple, at most
  `37^3=50,653` tuples.
- Obtained zero surviving words for every one of the 960 residual types.
  Therefore every constant symmetric rank-three generator is impossible
  in the trace-corrected formal family.
- Independently checked all eight observed word-count shapes against the
  older brute information-set enumerator.  Also replayed a generic
  degree-four cubic type using full 37-coordinate remainder vectors rather
  than the compressed syndrome calculation.
- Resource measurements:

  ```text
  complete word census       9.91 s, 29.0 MB RSS
  complete fixed-J closure 323.06 s, 61.1 MB RSS
  direct-vector red team     11.14 s, 64.2 MB RSS
  ```

- No external communication occurred.  Work remains local and unpushed.
