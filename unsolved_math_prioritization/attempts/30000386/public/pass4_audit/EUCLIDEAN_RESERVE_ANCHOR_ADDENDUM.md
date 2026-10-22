# Euclidean reserve acceptance: explicit initial anchor

The prior independent acceptance in `EUCLIDEAN_RESERVE_AUDIT.md` remains
frozen. This addendum pins the author's clarified input
`pass4_coupling/EUCLIDEAN_RESERVE_PRELIMINARY.md`, SHA256
`0e62592e1b7756817824e8f163eb6dd48c4980a0c809a0889fb7dae88dbc31a2`.

Sections 3 and 4 now explicitly require the Angel and reference to start
together at a_0=z_0=(0,0). This is the initialization inherited from the
previously accepted tracker and used in the earlier audit's excursion
argument. Without an initial error bound, a uniform tracking bound from
time zero would not follow. The clarified statements are accepted.

All rank, guard, witness-count, curvature, and excursion calculations are
unchanged. Acceptance concerns the lead-fifteen speed-1/4 radius-20 tracker,
and the separate arbitrary-H radius-(12+H/3) tracker under the global
at-most-eight-handled-sites-per-target-time restriction. Neither proves
unrestricted arbitrary-H safety.
