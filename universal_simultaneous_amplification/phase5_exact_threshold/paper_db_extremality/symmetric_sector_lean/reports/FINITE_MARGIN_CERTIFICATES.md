# Finite margin certificate design

The Lean definitions `t`, `lowerEll`, `c`, `epsilon`, `betaTerm`, and `beta`
translate Appendix A equations (A.20), (A.27), (A.30), and (A.32).
Ranks in `beta` are exactly `Finset.Icc 1 (N - 2)`. The recurrence has an
auxiliary value `t N 0 = 0`; its rank-one specialization is exactly
`2*N/(2*N-1)`. All displayed divisions and subtractions take place in ℚ.
The finite certificates concern these actual recursive `t` values and the
actual finite maximum; no independent positive polynomial is substituted.

For efficient checking, an untrusted Python generator supplies lists of
nonnegative integers representing lower bounds with denominator 10000.
`MarginCertificate` requires Lean to verify the initial zero, every one-step
recurrence inequality through rank N−1, strict positivity of every used
lower witness and occupation factor, and every physical-rank debt bound.
The generic theorem `gridValue_le_t` proves the lower bounds by induction
and proves the recurrence denominator positive on its exact domain.
`betaTerm_le_grid` then proves the reciprocal comparison with strictly
positive denominator. `beta_add_epsilon_le_of_certificate` passes these
bounds to the exact finite maximum.

The generated proofs use `decide +kernel`. This is Lean's kernel reduction
mode, not `native_decide`; no compiled evaluator, computed-answer axiom,
or external assertion is in the proof dependency path. The generator can
be faulty without compromising soundness: faulty witnesses will fail to
check. The generator uses only Python's standard library.

Each order has its own `GeneratedMargins/OrderNNN.lean` module. These modules
form a serial import chain, and `GeneratedMargins/All.lean` imports its final
member. This deliberately bounds clean-build memory: Lean releases transient
kernel-reduction caches between orders, and Lake cannot run all 248 checks
concurrently. The module organization changes neither the checked predicates
nor the dependency path of the final finite theorem. Regenerating the files
with `python3 tools/generate_margins.py` is deterministic.

At N=40 the grid certificate establishes a margin at least 1/200. At every
41≤N≤287 it establishes a margin at least 1/100. The separate theorem
`exact_margin_40` reduces the *actual* rational recurrence and maximum and
proves the manuscript's printed fraction
639304267467075678841 / 115369588296792467144716. This fraction is less than
1/100, so the later-order bound proves that N=40 uniquely attains the
minimum on the entire 248-order range. This argument does not rely on an
external solver identifying which rank maximizes beta.

This component proves only the finite beta/epsilon statements. The
connection to the reduced scalar, its physical active-chain definition,
and the all-order tail are distinct obligations tracked elsewhere.
