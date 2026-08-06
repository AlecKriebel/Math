# Critical dissipation-variance theorem

## Theorem

In every nonconservative recurrent phase class produced by the safe
single-linkage hierarchy, the hierarchy can be normalized at its first
nonzero reward layer so that

\[
\bar d_0<0.
\]

At any preceding layer with \(\bar d_0=0\), the complete-credit reward is an
exact coboundary and its Poisson-corrected variance is zero.  Consequently a
nonconservative finite-phase class with a genuine Lamperti coefficient
\(\Xi=2a+v\ge0\) does not arise.

At the first nonzero layer the corrected square has strict negative drift.
If the layer is reached after a slowdown of order \(R^a\), choose an integer
power \(P>a+1\).  The regenerative increment has bounded moments at that
normalization and

\[
\mathbb E[(Y+\Delta Y)^P-Y^P]
   \le -cY^{P-1},
\qquad
\mathbb E\sigma\le CY^a.
\]

Thus the episode drift scale dominates its physical duration.

## Proof mechanism

The hierarchy is built by repeated finite-state fast elimination.  At each
stage:

1. every molecularity/top-mass birth creates a carried target and a finite
   service credit;
2. the stage is not ended until all credits belonging to faster layers have
   been serviced, transferred to a slower layer, or have caused an exit;
3. after that complete relaxation, the stage reward is pathwise nonpositive;
4. a strict unpaired service gives a negative edge;
5. if every recurrent edge has zero reward, the finite reward is a
   coboundary and the associated token count extends to an exact linear
   conservation law.

The Schur complement of a finite fast generator is subtraction-free: by the
matrix-tree theorem every absorption probability is a ratio of polynomials
with positive coefficients.  It therefore creates no hidden sign
cancellation and no new positive reward.  Repeating the construction through
the finite source-rate flag preserves the nonpositive-edge invariant.

Now fix a recurrent class at one layer.  Let \(r_{ij}\le0\) be its complete
credit reward, \(P=(p_{ij})\) its limiting kernel and \(\pi\) its positive
stationary distribution.  Then

\[
\bar d_0=\sum_{i,j}\pi_i p_{ij}r_{ij}\le0.
\]

If the inequality is strict, solve the Poisson equation and obtain strict
corrected-square drift as in the bounded-defect theorem.  If equality holds,
then every term with \(\pi_i p_{ij}>0\) has \(r_{ij}=0\).  After Poisson
correction every increment is zero, not merely mean zero; hence the
asymptotic variance is exactly zero.  Contract that zero class and inspect
the next rate layer.  The number of rate layers and recurrent SCC
contractions is finite.  The process terminates at a strict negative layer
or at a class in which all complete-credit rewards are zero.  The latter is
the service-token conservation alternative.

This is a rate-preserving proof.  No edge is replaced, and no two unrelated
products of independent reaction constants are ordered.
