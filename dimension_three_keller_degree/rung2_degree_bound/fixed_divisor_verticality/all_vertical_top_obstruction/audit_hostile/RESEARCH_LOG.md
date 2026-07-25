# Hostile-audit research log

All times are UTC.

## 2026-07-25T07:30Z — local valuations reconstructed

- Re-derived the scaling descent from the parent relative-algebraic-closure
  lemma.
- Checked finite, zero, and infinity orders directly in local pencil
  coordinates.
- Confirmed the exact impossible equations \(4N=6\) and \(4N=3\).
- Confirmed that the final split specialization is excluded precisely by
  minimality, not by coprimality alone.

## 2026-07-25T07:42Z — parity and normal forms audited

- Wrote the divisor pullback as
  \(\sum n_aD_a\) and checked that base points contribute no prime divisor.
- Confirmed that absence of a double line makes every conic fibre reduced.
- Reconstructed both source/pencil normalizations and isolated the
  nonminimal rank-one binary exception.
- Recomputed both cubic kernels from their derivations.

## 2026-07-25T07:55Z — small-characteristic hazard rejected

- An initial exhaustive reduction modulo \(5\) produced a spurious cubic
  kernel caused by inseparability.
- Modulo \(11\), another accidental modular rank drop appeared.
- Neither affects the characteristic-zero argument.  Both backends were
  discarded rather than reported as independent verification.
- Replaced them with exact PARI/\(\mathbb Q\) ranks and a dependency-free
  modulo-\(101\) reconstruction whose samples are explicitly non-probative.

## 2026-07-25T08:05Z — audit complete

- Exact PARI reconstruction passed.
- Dependency-free modulo-\(101\) reconstruction passed.
- Fail-closed guard tests passed.
- Verdict: PASS with no correction to theorem scope.
