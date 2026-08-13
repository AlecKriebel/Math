# Exact-byte audit: common-catalyst operational macro

**Audit date:** 2026-08-12 PDT  
**Target:** [common-catalyst theorem](proof_first_h111_common_catalyst_operational_macro_theorem.md)  
**Target SHA-256:** concatenate
`3662b346d9efe30cff1075fdab000c6f` and
`c0a749ce0bbbdc1b7c2b2719e2625dd5`  
**Target size:** 469 lines, 17,970 bytes  
**Verdict:** **STRICT PASS FOR THE LITERAL SUPPORT SCOPE.**

The target bytes were treated as immutable.  I independently replayed the
particle coupling, conditional clean-block probability, geometric prelude,
expected ledger closure, fluid service window, time and endpoint
integrability, nonexplosion, and handoff to the workload-only Foster theorem.
No counterexample or missing implication was found within the theorem's
literal support

\[
                 T=\{X+Y,Y+Z,2Y\},\qquad R=\{0,Y,Z\}.
\]

This audit does **not** extend the target to lower supports containing
\(X\), nor to three-unary lower supports.  Those residual incidences require
the separate generalized label coupling described in Section 8.

## 1. Exact factorization and particle representation

For \(Y\ge1\), remove one persistent catalyst and write

\[
 z_{\mathsf X}=X,\qquad z_{\mathsf Z}=Z,\qquad
 z_{\mathsf Y}=Y-1.
\]

The three falling-factorial source propensities are exactly

\[
 Yz_{\mathsf X},\qquad Yz_{\mathsf Z},\qquad
 Yz_{\mathsf Y}.
\]

After aggregating labelled top rates, the remaining \(H-1\) labels are
independent particles with irreducible three-state generator \(Q\) in
operational time \(A(t)=\int_0^tY(s)\,ds\).  Thus
\({\cal L}_T=Y{\cal L}_Q\) is an exact time change, not an averaging
assumption.  Top reactions never remove the final catalyst.

For each initial particle state, the finite graphical event used in Section
2 has a fixed positive probability: the chosen top path reaches
\(\mathsf Y\), competing path arrows are absent, and every top arrow out of
\(\mathsf Y\) is absent for the rest of the operational block.  These events
are independent over the initial labels, so their sum has the stated uniform
Chernoff lower tail for every initial particle profile.

There is a minor wording point, but no mathematical defect, in the sentence
that an external lower \(Z\to Y\) transfer “can only help \(E_i\).”  Read
\(E_i\) as the scheduled **base top-arrow** event.  If the transfer moves a
label to \(Y\) before a later scheduled \(Z\)-arrow, that scheduled arrow is
simply inactive; the label has already achieved the required terminal hit.
The event forbids all later top arrows out of \(Y\), so it stays there.  A
\(Z\to0\) event deletes one label.  Therefore, on the base graphical event,
the number of terminal successful labels is at least the graphical success
count minus the number of \(Z\)-deaths, exactly as used in (3.4).

## 2. Conditional unspoiled probability

Before the first lower reaction sourced at \(Y\), top reactions and
\(Z\)-sourced lower reactions preserve at least one catalyst.  Hence
\(Y\ge1\), and accumulating operational length \(a_0\) takes at most
physical time \(a_0\).  Conditional on the complete top and \(Z\)-sourced
history, the integrated lower \(Y\)-source hazard is

\[
 K_Y^R\int Y(t)\,dt\le K_Y^Ra_0,
\]

and the integrated constant birth hazard is at most \(\beta a_0\).
Independent exponential-clock compensation therefore gives the conditional
bound

\[
 q_0=\exp\{-(K_Y^R+\beta)a_0\}>0.
\]

Because this lower bound is conditional on the graphical history, it
combines in the correct order with the Chernoff event.  No independence
between the population-dependent \(Z\)-history and the top success count is
silently asserted.

On a clean block, either at least \(\alpha H_{\rm start}\) labels die by
\(Z\to0\), or deleting fewer labels from the Chernoff success set leaves at
least \(\rho H_{\rm start}\) particles at \(Y\).  No births occurred, so
\(H_{\rm end}\le H_{\rm start}\), and this is a genuine catalyst shell.
This proves one uniform conditional success probability at every large
block start.

## 3. Dead-face seeding and geometric debt

On \(Y=0\), the top linkage is dead.  In the literal two-unary lower graph,
a simple lower path from zero to \(Y\) has length one or two.  A selected
constant birth followed, if necessary, by the selected unary transition of
that labelled molecule succeeds with a fixed probability per trial and
finite mean trial duration.  Other unary molecules do not delay the selected
constant clock or the labelled molecule's unary lifetime.  Direct deaths
remain favorable.  The seed time and its birth count therefore have uniform
finite first moments.

Until the fractional return \(H\le H_0/2\), each operational block begins
at workload at least \(H_0/2\).  After enlarging the finite threshold, every
complete attempt has the same lower success probability.  The number of
attempts is geometrically dominated.  Each failed active block stops at its
first birth or \(Y\)-source event and hence charges at most one active-block
birth; every visit to \(Y=0\) invokes the uniformly integrable seed.  This
proves the uniform expected duration and total expected birth debt in (5.2).
No pathwise claim that the final block's deaths repay earlier births is used.

## 4. Endpoint trichotomy

The three prelude endpoint events are disjoint and exhaustive:

1. fractional return, with the exact pathwise ledger
   \(D-B=H_0-H\ge H_0/2\);
2. a death-rich block with
   \(M_Z\ge\alpha H_{\rm start}\ge\alpha H_0/2\); or
3. a catalyst shell \(Y\ge\rho H\), still above \(H_0/2\).

If no \(Z\to0\) label exists, the second branch is empty and the argument
only becomes simpler.  Failed-attempt deaths are retained in the physical
ledger and may be discarded only as favorable terms in the final lower
bound.

## 5. Deterministic and stochastic service

On the unit simplex, the top ODE is exactly

\[
               \frac{dq}{ds}=q_{\mathsf Y}qQ,
 \qquad q(\theta)=q(0)e^{Q\theta},
 \qquad \frac{d\theta}{ds}=q_{\mathsf Y}.
\]

On the compact shell \(q_{\mathsf Y}(0)\ge\rho\), bounded operational
intervals have the uniform lower bound
\(q_{\mathsf Y}(\theta)\ge\rho e^{-K\theta}\).  Hence every fixed
operational time is reached in uniformly finite physical time.  Irreducible
finite-state convergence then places both \(q_{\mathsf Y}\) and
\(q_{\mathsf Z}\) above fixed positive constants after a uniform finite
physical time.  Since strong connectivity of \(R\) gives
\(\delta_Y+\delta_Z>0\), the direct-death occupation integral can exceed
any prescribed \(2D_0\) on one uniform finite fluid horizon.

On physical time \(T/n\), quadratic top clocks produce the stated
density-dependent ODE.  The density martingale has quadratic variation
\(O(n^{-1})\); lower unary clocks produce only \(O(1)\) reactions, and the
constant clock produces \(o(1)\), uniformly over the compact shell.
Localization and Gronwall give uniform \(L^1\) convergence.  Applying the
direct-death compensator yields the uniform expected service count
\(D_0\).  Births in this window have exact expectation \(\beta T/n\).

The appended final ordinary jump is legitimate: total hazard is at least
the positive constant birth hazard, so its mean holding time is at most
\(1/\beta\), and it adds at most one adverse birth.  It guarantees a genuine
jump on the service and death-rich branches.

## 6. Expected ledger closure

Let \(F,D,I\) denote the fractional-return, death-rich, and catalyst-shell
events.  Choose
\(D_0=C_{\rm pre}^B+3\), then enlarge the population cutoff so that both
pathwise favorable branches pay at least \(D_0\), the conditional shell
service has mean at least \(D_0\), and service-window births have mean at
most one.  The expected births restricted to \(D\cup I\), including the
final jump, are at most \(C_{\rm pre}^B+2\).  Therefore

\[
 \begin{aligned}
 \mathbb E(D_\tau-B_\tau)
 &\ge D_0\mathbb P(F)+D_0\mathbb P(D)+D_0\mathbb P(I)
       -(C_{\rm pre}^B+2)\\
 &\ge1.
 \end{aligned}
\]

This expectation-level partition correctly handles arbitrarily many births
in earlier failed attempts.  The geometric prelude, fixed service window,
and final holding time give a uniform finite mean duration.  Since
\(H(X_\tau)\le H(x)+B_\tau\), endpoint integrability follows from the same
birth estimate.  Choosing \(\eta\) below the net-ledger margin divided by
the duration bound gives the required physical-time workload inequality.

## 7. Foster handoff

Population-increasing channels have at most linear rate, while quadratic top
channels preserve \(H\); the nonexplosion argument is valid.  The stopping
rule is state-selected, all-clock, strong-Markov at every failure, and has an
actual endpoint.  It supplies the exact occupation macro required by
the workload-only physical-time Foster lemma.  Its SHA-256 begins
`8cf2a8d4` and ends `851b2a`; the dependency's independent audit begins
`9d8fc8b5` and ends `babcc67`.  The full pins are recorded in the target.
Thus the target proves positive recurrence for every fixed class in its
literal support family.

## 8. Exact scope boundary

The strict pass above is deliberately scoped.  The residual homogeneous
family also contains the same top support paired with lower unary sets
\(\{X,Y\}\), \(\{X,Z\}\), and \(\{X,Y,Z\}\).  The target theorem fixes
\(R=\{0,Y,Z\}\), so it does not prove those cases.

A valid generalization must suppress, independently for every initial free
label, its \(X\)- or \(Z\)-sourced lower clock until that label first reaches
\(Y\), while retaining all clocks globally.  Since one operational block
takes at most \(a_0\) physical time, this per-label graphical event still has
a fixed positive probability.  The global clean event then separately
suppresses births and all \(Y\)-sourced lower events; its integrated hazard
remains \(\beta a_0+K_Y^Ra_0\).  A Chernoff argument over labels yields the
same catalyst-shell alternative for every lower support containing \(Y\).
If \(Y\) is absent from the lower support, the face \(Y=0\) is invariant and
reduces classwise to an open unary network.  This extension is not silently
attributed to the frozen target.

## 9. Final verdict

The frozen target is mathematically complete for exactly
\(T=\{X+Y,Y+Z,2Y\}\) and \(R=\{0,Y,Z\}\), for arbitrary strong labelled
orientations and positive rates.  **STRICT PASS FOR THE LITERAL SUPPORT
SCOPE.**
