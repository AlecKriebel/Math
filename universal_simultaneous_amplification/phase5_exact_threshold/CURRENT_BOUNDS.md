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
upper theorem has yet been proved.  The proposed route is now reduced to two
precise statements.

1. **Universal minimal product.**  For every finite connected weighted
   module and every portal load, prove the portal-general stationary product

   \[
   q_Bq_D\ge r^3[\rho_{Bd}-p]_+[\rho_{dB}-p]_+,
   \qquad r=R_{hyb},\quad p=1-1/r.
   \]

   This theorem is proved for every connected weighted module of order at
   most three: weighted paths are covered by the weighted-`P_3` theorem and
   positive triangles by the exact portal-product theorem.  It remains open
   in general.  A weak-core compounding theorem now proves that this minimal
   product would automatically imply BDM for every bounded separated module,
   so BDM is no longer an independent local conjecture.
2. **Nonseparated trace exhaustion.**  Conditional on BDM, every separated
   physical Schur packet has the correct common Bd/dB coefficient.  If these
   packets do not exhaust a hypothetical amplifier, an exact retained trace
   carries at least `(R_hyb-1)/R_hyb` times the full response scale.  Formal
   Schur iteration cannot remove it: even on the unweighted four-path,
   elimination creates rule-dependent Hamming-two jumps outside the Moran
   module class.  The remaining global obligation is therefore a structural
   bulk/fragmentation inequality for this macroscopic nonseparated trace.

The local product itself has two equivalent exact endpoints.  Singleton-root
Schur compression gives a paired root-tree determinant inequality.  Honest
low/high renewal instead gives a full-excursion repayment inequality in
which a doubleton-fed base-graph Green potential must pay the product of the
two signed full-cycle rewards.  Rank-one/two marginal data alone are
provably insufficient, and a weighted star proves that no separate
per-rule polynomial-in-order reward bound can work.  Thus the surviving
local theorem must retain cross-rule Green/tree compensation rather than an
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
