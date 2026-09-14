# Independent audit of the six banded block actions

Timestamp: 2026-09-14 14:54 UTC. This review independently compares
`BlockActions.lean` with Appendix A (A.13)–(A.14), rather than relying on
the formulas' author or on the existing computational verifier.

Write the physical good rank as `k=i+1` and the physical bad rank as
`k=i+2`. The checked formulas translate as follows:

| Lean theorem | Independently reconstructed nonzero action |
|---|---|
| `phaseS_mulVec` | `k/(2N) v_k + (N-k)/(2N) v_(k-1)` |
| `phaseC_mulVec` | `k/[2(k+1)N] v_(k+1) + (N-k)/(2kN) v_k` |
| `phaseD_mulVec` | `v_(k-1)/N` |
| `phaseQ_mulVec` | `[N(k-2)+k]/(2kN) v_k + k(k-1)/[2(k+1)N] v_(k+1) + (N-k-1)/(2N) v_(k-1)` |
| `phaseQ_transpose_mulVec` | same diagonal, plus `(k-1)(k-2)/(2kN) v_(k-1) + (N-k-2)/(2N) v_(k+1)` |
| `phaseD_transpose_mulVec` | `v_(k+1)/N`, with the last good rank yielding zero |

All six agree with the matrix entries printed in the manuscript, including
the direction of the transpose. The `D` sign is positive because the actual
signed block of `H` is `-D`; the implementation negates that coefficient
once, as required. No sign of the negative bad channel is silently changed.

The helper `zeroExtend` uses a signed integer index, checks both lower and
upper bounds, and returns zero outside the finite vector. This correctly
handles both ends without natural-number predecessor truncation. At the
single bad-state order `N=3`, both bad neighbors are absent at once; the
formula still keeps only the actual diagonal entry. The theorem statements
are algebraic identities, not positivity statements. In particular, the
formal coefficient `(N-i-4)/(2N)` in the transpose formula can be negative
at a boundary where its multiplying zero extension vanishes. A downstream
proof must retain this zero extension or establish the relevant index domain
before asserting coefficient nonnegativity.

The proofs expand the actual matrices, reduce selector sums over the actual
finite indices, and check each diagonal/adjacency case. They do not assume
the desired action as a hypothesis. No indexing discrepancy or mathematical
gap was found. The independent finite arithmetic reviewer also inspected
these statements before consuming them in any barrier proof.

Completion estimate for this bounded statement audit: 100%. This does not
certify the downstream barrier comparisons or the full physical identity.
