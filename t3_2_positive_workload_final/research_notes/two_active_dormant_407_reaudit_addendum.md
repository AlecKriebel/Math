# Re-audit addendum: actual service endpoints break the bounded corrector

Audit timestamp: 2026-08-10 PDT.

Frozen repaired snapshot:

    theorem note  8ad0ffdd264f243fc4816ce4a24ee953d13d40a5308ae3aa9c70664859953ba2
    certificate   79d0f772b4262d00ca9b29fbd2fc0a82a4c510b8dd7bef95609a07ca90679431
    focused tests 8319f9c174475e65959dc293bf99b5b1f5f7f6b8a010ae90b52a8da25f4d367a

## Verdict

**FAIL as written at descriptor-local scope; repair remains open.** The new
start-weighted Green formulation, maximal-degree cut, historical-singleton
exclusion, unweighted hard-row boundary charge, and exact 951-to-317
handoff survive this audit. However, equations (7.12)--(7.14) are false
when, as the repaired note explicitly requires, the actual spectator
coordinate of a service endpoint is retained.

This is a counterexample to the bounded entropy-coboundary assertion, not a
counterexample to recurrence or T3-2. All analytic, pair-level, and global
flags must remain false.

## Exact counterexample

Use the normalized support

    L+ = {2U,V+I},   L0 = {0,I,2I,U+I}.

It occurs in six exact generalized rows, twice at each spectator cap 0, 1,
and 2. Choose the strongly connected orientations

    2U -> V+I -> 2U

and

    0 -> I -> 2I -> U+I -> 0.

Every rate may be one. A historically consistent positive-debt base exists.
Starting with spectator `u+2`, the physical word

    2U -> V+I,  I -> 2I,  2I -> U+I,  U+I -> 0

ends at `(U,I,relative V)=(u,0,1)`. The three lower reactions occur against
the enabled fast clock but have strictly positive probability, which is all
historical consistency requires.

Now reset relative displacement at this no-fast base. Proper excursions
`2U -> V+I -> 2U` are exact physical-state self-loops and are contracted.
The next nonself zero-order transition is

    0 -> I,  V+I -> 2U.

It is strict old-`V` service and has actual endpoint

    (u,0,0) -> (u+2,0,-1).

For the spectator entropy in (7.11), therefore,

    T B_ell(u)-B_ell(u)
      = log((u+1)(u+2)) + 2 ell_U
      = 2 log u + O(1).

This is positive for every fixed `ell_U` once `u` is large. Consequently
`d_+` does not have finite support, the function `chi` in (7.13) is not
uniformly bounded, and the `O(1)` conclusion (7.14) is unavailable.

## What remains credible

- The corrected polynomial Green bound with start factor
  `(1+u)^(r+1)` is consistent with the maximal-degree geometry.
- The factorial estimate with `theta' < theta < 1/2` can retain a bounded
  actual service jump by spending the strict theta gap, even though the
  killed-to-cemetery `H_theta` drift alone does not retain that endpoint.
- Historical singleton exclusion survives: a positive-debt no-fast return
  lands on an enabled lower target, and strong connectivity supplies an
  eventual service path.
- The Section 6 unweighted third-insertion arithmetic is valid after the
  cumulative `A` boundary is treated separately from the per-raw-block
  event. Its final exponent is still `-1/8`.
- The fourth-power algebra and exact seam telescoping are correct.

Equation (7.17)'s arbitrary-interruption moment tail is plausible but still
only sketched; an arXiv-ready version should state the finite expansion and
the stopped tail estimate explicitly.

## Minimal likely repair

The counterexample grows only logarithmically in spectator entropy. A
replacement of (7.14) by

    E[B_ell(U_sigma)-B_ell(u)] <= C log(u+e)

would still be sufficient, because every one-active tier has
`log(u+e)=o(log n)`. Combined with `P(D)=1-o(1)`, this gives
`E Y_n <= -(1-o(1))log n`, and the start-weighted `j=2,3,4` bounds still
make the remaining fourth-power terms lower order. That logarithmic bound
must be proved for every arbitrary strong orientation; it is not established
by the frozen repaired snapshot.

Reproduce the counterexample with:

    PYTHONPATH=src python3 -B src/two_active_dormant_407_repair_reaudit.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_two_active_dormant_407_repair_reaudit.py -v
