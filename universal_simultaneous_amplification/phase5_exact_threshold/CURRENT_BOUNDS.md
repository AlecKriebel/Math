# Current rigorous bounds

Last updated: 2026-08-13.

\[
\boxed{1.5028569127905696267\ldots=R_{\rm hyb}
       \le R_{\rm sim}\le\infty.}
\]

## Lower bound

`R_hyb` is the unique root in `(3/2,151/100)` of

\[
R^6-8R^5+22R^4-30R^3+21R^2-6R+1.
\]

It is achieved below the endpoint by one explicit fitness-independent
dilute pair--leaf hybrid family.  Strict amplification is proved for every
fixed `1<r<R_hyb`, with the required quantifier order.

## Upper bound

No finite universal upper bound is proved.  A proof that the complete graph
maximizes dB fixation at `r=2` would give

\[
R_{\rm sim}\le2.
\]

It would not by itself prove equality; a single family working for every
fixed `1<r<2` would still be required.

The current proof-first upper candidate is `R_sim=R_hyb`, but no universal
upper theorem has yet been proved.  The proposed route has been reduced to
two precise statements:

- the bounded dual-moment inequality (BDM) at `R_hyb`, proved for all
  complete modules and all weighted three-paths, but open for arbitrary
  positive triangles and general modules; and
- a response-scale compactness theorem that synchronizes the Bd and dB
  first-exit traces.  Rule-by-rule positive trace decompositions do not
  suffice; an exact leaf/closed-`K_2` marginal-cone obstruction proves that
  the two rules must share a paired trace measure or obey an equivalent
  signed mismatch-charge bound.

The higher-rank part of BDM has an exact renewal/Schur formulation (RTER), so
the remaining gap is a cross-rule stationary-flow inequality rather than an
uncontrolled catalogue of graph cases.  These reductions sharpen the upper
frontier but do not change the boxed rigorous interval.

The exact constant

\[
R_{\rm pair}=1.6986624639825652\ldots
\]

is an upper endpoint only for the separated monomorphic-`K_2` hierarchy
class.  It is not a bound on `R_sim` and therefore does not alter the boxed
global interval above.

## Endpoint convention

`R_sim` is a supremum over open fitness intervals.  Whether an extremal
family amplifies, ties, or suppresses at the endpoint does not by itself
change the value.
