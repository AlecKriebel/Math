# Certified current-target episode interface

## Exact setup

The augmented embedded state is `(x,t)`, where `t` is the target of the
actual labelled channel that produced `x`; hence `x>=t`.  The potential is

\[
V(x,t)=\sum_i\log((x_i-t_i)!).
\]

If the next physical channel is `s->u`, then exactly

\[
V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
\]

No future channel is conditioned upon.

## Episode policy

For every target complex declared available in a fixed chart, choose one
simple path in its own linkage,

\[
t=y_0\to y_1\to\cdots\to y_m=c.
\]

At an episode start, continue only while the exact designated channels fire;
stop at the first deviation or structural chart exit; after reaching `c`,
take one final ordinary jump.  A shielded target uses one ordinary jump, or a
separately certified finite zero trace.

The endpoint target of one episode is the actual target of its final physical
jump and is the start mark of the next episode.  Thus, pathwise:

1. every physical jump belongs to exactly one episode;
2. episodes do not overlap;
3. no jump is omitted;
4. policies are selected from the current marked state;
5. an available episode has at most `|C|` jumps.

For a divergent sequence on which the linkage's terminal source probability
tends uniformly to zero, the inherited scalar envelope gives a bound
`-A_R`, where `A_R -> infinity`, uniformly over the finite target set and the
compact tied-rate cell.

This statement does **not** say that conditioning on the reaction which
creates an available target gives a negative block.  The counterexamples in
`failed_approaches/` show that it need not.
