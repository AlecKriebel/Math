# Physical carrier reactivation theorem

Fix a terminal chart and a complete source-rate flag. Scale its rational
workload so that `H(y)=h.y` is integer-valued on complexes.

A positive reaction `y->u` has `H(u)>H(y)`. Its actual physical target `u` is
present after the reaction and is therefore an enabled source. In the
creator linkage choose a path from `u` back to `y`; stop at the first target
`v` with `H(v)<=H(y)`. Every earlier source is strictly faster than `y`, and

\[
H(u-y)+H(v-u)=H(v-y)\le0.
\]

The path is lifted through actual targets and is sequentially enabled.

## Finite phase

The finite phase records exact bounded coordinates, capped availability,
actual current target, source support, linkage, lattice data, and the
position in one of finitely many return prefixes. Active population
coordinates are not stored.

Include every processed physical channel. A positive edge has the preceding
return certificate. In a closed finite phase component with no negative
workload edge, a positive edge is impossible: closedness retains its return
prefix, and a prefix cancelling a positive integer increment contains a
negative edge. Thus every closed component is either:

- **strict**, containing a negative physical transition; or
- **zero**, all of whose physical transitions preserve workload; or
- nonclosed, producing a declared chart/support/source-flag exit.

## Uniform physical race

In a strict component, finite graph reachability and the compact positive
tied-rate cell give a common service minorization `p>0`. Reactions that leave
the selected service source enabled do not delay its exponential clock.
Actual destruction of that source is a finite phase transition. If
unprocessed slower hazard divided by carrier hazard is at most
`epsilon_R`, then

\[
P(\text{slower interruption before service})\le K\epsilon_R,
\qquad \epsilon_R\to0.
\]

The number of carrier transfers has geometric moments.

## Reactivation

After a service, if aggregate debt remains positive, restart from the new
physical state and actual target. In a strict recurrent component the same
chart constants apply. Loss of source support is an exit. Entry into a zero
component transfers the unchanged debt to the next slower physical
reaction-count trace.

Hence reactivation depends only on the current physical state and finite
phase, never on the identity or history of the reactions that created the
debt.
