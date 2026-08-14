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
upper theorem has yet been proved.  Recent reductions have split the missing
upper theorem into three precise obligations rather than a graph-search
problem.

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

   The quantifier over all portal loads has now been eliminated exactly.  On
   the active branch, let `psi_B,i` and `psi_D,i` be the signed excess rewards
   accumulated in one Bd and dB return cycle to singleton root `i`, measured
   per unit initial holding time.  The universal product is equivalent to

   \[
   (x\mathbin\cdot\psi_B^{-1})
   (x\mathbin\cdot(e\psi_D^{-1}))
   \ge r^3(x\mathbin\cdot\mathbf1)(x\mathbin\cdot e)
   \quad(x\ge0).
   \]

   This inequality holds for every portal if and only if it holds on every
   one- and two-root portal.  Thus the remaining local theorem is a finite
   family of exact Kac-cycle diagonal and two-by-two copositivity inequalities,
   not a high-dimensional portal optimization.  No fixed rank prefix can
   prove even the diagonal part.  Ordinary scalar Hellinger reversal is also
   rigorously insufficient: the two macro-cycle laws have singular support,
   target-locked burst expansion leaves a non-coboundary repeated-source
   factor, and scalar pairing discards an indispensable root-orientation
   square.  A proof must retain the full signed cycle reward, source
   multiplicities, and both root assignments.

2. **Diffuse endpoint support.**  A root-to-branching coupling proves that,
   whenever finite-population, collision, and false-establishment errors are
   little-oh of the response scale, a hypothetical amplifier forces a
   positive diffuse score

   \[
   (\bar s-p)+(r-1)(\bar b-p)>0.
   \]

   The opposite inequality would therefore close this diffuse branch.  One
   half of its sharp orbit sandwich is now proved uniformly on
   `3/2<=r<=151/100`:

   \[
   E_p\mathcal F_r((r-1)q)\le (r-1)E_pq,
   \qquad \mathcal F_r(y)={rRy\over1+rRy}.
   \]

   The remaining half is the exact endpoint comparison
   `E_p s<=E_p F_r((r-1)q)`.  It has been reduced both to ten linked
   five-ground Picone orders and to one full-state reversible-spine
   cross-Dirichlet term.  Raw orbit means cannot prove it: an imbalanced
   deterministic two-cycle makes the scaled mean increase after the first
   step even though the endpoint comparison is positive.  The stronger
   scalar ground-energy sign is exactly false, so its compensating square is
   essential.

3. **Nonseparated trace and response-scale error exhaustion.**  Conditional
   on BDM, every separated physical Schur packet has the correct common Bd/dB
   coefficient.  If these packets do not exhaust a hypothetical amplifier,
   an exact retained trace
   carries at least `(R_hyb-1)/R_hyb` times the full response scale.  Formal
   Schur iteration cannot remove it: even on the unweighted four-path,
   elimination creates rule-dependent Hamming-two jumps outside the Moran
   module class.  The remaining global obligation is therefore a structural
   bulk/fragmentation inequality for this macroscopic nonseparated trace.
   Equivalently, in the root-to-branching reduction one must charge the
   response-scale aggregate consisting of the `1/n` layer, Green-amplified
   collisions, and branching paths which reach a cutoff but later die.

The exact two-root criterion also admits a Lorentz form.  Its diagonal
slacks, root-assignment likelihood, and endpoint degree mismatch form three
explicit rapidities.  A proved hyperbolic comparison reduces a sufficient
pair theorem to one Euclidean cone inequality among those rapidities.  The
obvious unmarked geometric-mean chain cannot establish it: that chain is
trapped in the singleton sector and sees zero higher-rank reward.  This
pinpoints the required missing structure without licensing another search
over graphs or low-rank potentials.  These reductions sharpen the upper
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
