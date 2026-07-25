# Post-gate decision for the order-668 program

## Verdict

The construction gate has failed.  No Hadamard matrix of order 668,
conference matrix of order 334, Legendre pair of length 333, or physical
two-consecutive-higher-digit lift has been found.

The work did produce exact, reproducible mathematics worth preserving:

1. the five two-high LP333 profiles now have a complete physical-margin
   filtration and retraction census;
2. representatives of both semiregular `C37` parity types have explicit
   exact-margin adjacency supports modulo two;
3. constant formal conjugators in the trace-corrected exponential family
   are excluded through rank three, and two first-nonconstant rank-two
   families are excluded; and
4. the smallest exact support-switch families provably cannot repair either
   frozen modulo-two witness.

These results strengthen two scoped paper projects.  They do not indicate
convergence to `H(668)`.

## Strict gate scorecard

| Gate | Outcome |
|---|---|
| Test several structured families on the five shell orbits | Completed in `H668_72H_GATE.md`; none produced a physical consecutive lift |
| Reach at least two consecutive higher digits | Failed in both the five-profile LP333 lane and the semiregular `C37` support lane |
| Estimate the complete remaining search | Completed below at the certified relaxation scale; every flat completion is astronomically beyond the host |
| Audit arXiv `2607.20765` | Completed; local order-18, order-9, and order-6 multiplier exclusions are subsumed, while the five-orbit work lies in open paper ID3 |
| Preserve publishable structure if the gate fails | Completed in `shell_two_exact/`, `shell_two_physical_margin_lift/`, and `conference_334_z37_lift/` |

## Complete remaining-search scale

The exact counts rule out interpreting the next solver layer as the
remaining problem.

| Scope | Certified size/state unless labeled estimate |
|---|---|
| All-quotient semiregular characteristic-two relaxation, modulo natural equivalences | between `2^720` and `2^721` |
| Exact trace-law plus first-moment union over all 625 integral quotients | base-two logarithm `1223.75748046440094` |
| One fixed-quotient modulo-four CP-SAT encoding | 1,494 support bits, 418,293 reused products, 1,503 independent equations |
| Best retained exact-margin type-1 support | 672 of 1,503 next-digit carry coefficients wrong |
| Smallest semiregular transvection family | 49,284 members per witness; zero exact-margin members |
| Constant rank-three formal family | 1,452 projective rational types; zero survivors after fixed-`J` closure |
| Generic common three-plane nonconstant pair before support constraints | structural estimate: orbit-scale parameter space on the order of `37^6` |

The `2^720`--`2^721` count is already symmetry-reduced and is the most
honest complete scale for the surviving modulo-two semiregular lane.  The
1,494-bit CP-SAT model addresses one quotient and one higher digit, not the
complete integral search.  Its bounded `UNKNOWN` outcomes therefore do not
constitute a meaningful fraction of the remaining problem.

For the five two-high LP333 profiles, exact raw target multiplicities and a
neutral independence model predict approximately 10,251.6 physical
digit-two points but only `2.6461e-5` physical digit-three points across the
entire five-profile program.  This decimal estimate is planning evidence,
not a theorem.  The exact theorem is less favorable structurally: the
physical margin cut removes every five-form retraction and leaves maximum
retraction dimensions `4,3,3,3,4`.

## What is genuinely new-looking

Subject to broader literature review, the strongest publication packages
are:

- **LP333 fixed-compression paper:** the five exact two-high orbits,
  rank-six physical margin digit on all 405 targets, following six
  quadrics with zero common polar radical, no five-form retraction, and the
  complete 11,011 four-subspace census.  This is a result inside the July
  paper's open subgroup ID3 and an additional fixed-compression slice, not
  a classification of ID3.
- **Semiregular conference paper:** the 625 integral quotient classes,
  universal `6/3` trace law, exact finite-field censuses, explicit
  modulo-two supports for both parity types, constant-rank-three
  obstruction, and first-nonconstant named-family obstructions.  This is a
  plausible computational-combinatorics note, not a graph construction or
  nonexistence theorem.

Neither package is currently Wikipedia-level.  An explicit `H(668)` would
be.

## Resource and restart decision

More RAM alone does not change the verdict.  Exact replays use at most about
101 MB; the bounded modulo-four CP-SAT diagnostic peaked near 2.7 GB.  The
bottleneck is mathematical contraction, not the 16 GB host.

Pause headline `H(668)` spending on these lanes.  Resume only if at least
one of the following appears:

1. a theorem that couples nonmonomial transvections while restoring all
   block margins globally;
2. an algebraic rank-at-least-four or low-generated-algebra
   parameterization with a finite, costed denominator;
3. a direct integral conference/SDS construction principle; or
4. a new physical point satisfying exact row margins and two consecutive
   higher digits.

Another isolated lower-layer witness, bounded `UNKNOWN` run, or
uncosted structured family is not a restart trigger.

No external communication occurred.
