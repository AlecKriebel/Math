# Hostile review: order-12 parameter-four minimum signature

Status: **ACCEPT EXACT LOGICAL REDUCTION**

This review covers
`math/lemmas/order12_k4_minimum_signature.md` at SHA-256
`d87e2d3feffb5d93aa0a132289adb166bee27ef6f92526701a28cc988aaf215a`.
It does not certify the parent UNSAT, exclude the order-12 parameter-four
slice, or resolve the universal conjecture.

## Independent checks

- The frozen edge variables encode \(H=\overline G\). Thus a positive
  \(e_{uv}\) is an \(H\)-edge and a \(G\)-nonedge; the note uses this
  complement direction consistently.
- The exact anchored clauses make \(0,1,2,3\) a clique in \(H\). The first
  exact connected-\(G\) cut clause is the singleton cut at vertex \(0\):
  it requires at least one incident \(H\)-edge variable to be false.
  Since the three anchor incidences are true, some outer \(e_{0v}\) is false.
- The final 105 clauses of the frozen parent split into seven adjacent
  15-clause signature comparators. An independent truth-table evaluation of
  all \(7\cdot16^2=1,792\) signature pairs found that each comparator accepts
  exactly `left <= right` in lexicographic order with \(0<1\).
- An independent enumeration covered all
  \(\binom{16+8-1}{8}=490,314\) nondecreasing sequences of eight four-bit
  signatures. Exactly 483,879 satisfy the necessary singleton-cut condition,
  and every one has a minimum signature whose first bit is zero. The remaining
  6,435 sequences have first bit one at every outer vertex and violate that
  cut.
- Enumerating the four cube bits independently gives exactly the eight
  survivors stated in the note:
  `0000`, `0001`, `0010`, `0011`, `0100`, `0101`, `0110`, `0111`.

The executable probe and canonical result are
`reviews/order12_k4_minimum_signature_hostile_probe.py` and
`reviews/order12_k4_minimum_signature_hostile_probe.json`.

## Production boundary

The note leaves the immutable 16-cube production partition unchanged. Its
statement that case `1111` is the sole retained `UNSAT_LRAT_VERIFIED` leaf
and that 15 leaves remain pending agrees with the retained v3 checkpoint and
the independently reviewed one-leaf certificate. The reduced eight-cube
identity is therefore a proved hand reduction that may support a future
mixed proof; it is not a present aggregate result.
