# Independent exact-byte audit of the generalized common-catalyst theorem

**Hostile proof replay, 2026-08-12 PDT.**  The immutable target is

~~~text
research_notes/proof_first_h111_common_catalyst_all_lower_supports_theorem.md
SHA-256 81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496
360 lines / 14,150 bytes
~~~

The verdict is **STRICT PASS**.  The theorem gives the all-clock
physical-time workload macro for

\[
 T=\{X+Y,Y+Z,2Y\},\qquad
 R=\{0\}\cup U,
\]

for each of the four residual relative lower supports

\[
 U\in\{\{X,Y\},\{X,Z\},\{Y,Z\},\{X,Y,Z\}\}.
\]

The target retains every top and lower clock.  In particular, it does not
turn the order-\(H\) lower activity sourced at \(X\) into a bounded phase.

## 1. Exact factorization and protected labels

After reserving one catalyst when \(Y\ge1\), the three falling-factorial
propensities are exactly

\[
 (x)_{X+Y}=Yz_{\mathsf X},\qquad
 (x)_{Y+Z}=Yz_{\mathsf Z},\qquad
 (x)_{2Y}=Yz_{\mathsf Y}.
\]

Thus the free labels have independent one-particle top clocks with an
irreducible generator \(Q\) in operational time
\(A(t)=\int_0^tY(s)\,ds\).  This is an identity of the stochastic
generator, not an averaging limit.

For each initial label, the target selects a simple \(Q\)-path to
\(\mathsf Y\), prescribes its top arrows, suppresses competing top arrows,
and suppresses its own lower \(X/Z\) marks until the terminal hit.  The
last suppression is realized by a separate rate-\(K_*\) dominating
physical-time clock for each label.  An unspoiled operational block has
physical duration at most \(a_0\), because \(Y\ge1\) before the first
\(Y\)-sourced lower event.  Hence each label has success probability at
least

\[
                         p_Qe^{-K_*a_0}>0.
\]

The graphical clocks are disjoint between labels, so the protected
indicators are genuinely independent.  All lower clocks of unprotected
labels remain live.  Chernoff therefore produces a fixed positive fraction
of terminal \(Y\)-labels uniformly over every initial free-particle
profile.

## 2. Conditioning order and the repaired success union

After revealing the top and all \(X/Z\)-sourced lower histories, the birth
clock and the per-molecule \(Y\)-sourced clocks are disjoint.  Before the
earlier of the operational endpoint and fractional return, their integrated
hazard is at most

\[
                  (K_Y^R+\beta)a_0.
\]

The unspoiled probability is consequently bounded below by the fixed
\(q_0=e^{-(K_Y^R+\beta)a_0}\).  The target correctly states the resulting
success event as the union

\[
 \{\text{fractional return}\}
 \ \cup\
 \{\text{unspoiled operational endpoint in the catalyst shell}\}.
\]

This is the load-bearing repair relative to the superseded candidate

~~~text
a8ccddd150e1ae90efa1141083d61349507fe4e2939eaaafad10d29db508b482
~~~

That candidate omitted fractional-return preemption in its displayed
intersection.  The frozen target uses the correct union in (3.3), so each
complete attempt has a state-uniform positive conditional success
probability until fractional return.  Geometric repetition is therefore
valid.

## 3. Arbitrary lower supports and seeding

When \(Y=0\) and \(Y\in U\), strong connectivity of the finite lower graph
supplies a simple path from \(0\) to \(Y\) of length at most three.  A
selected constant birth followed by tagged unary transitions has one fixed
positive success probability.  Competing tagged transitions restart a
trial at its actual endpoint; events of other particles neither delay the
selected constant clock nor the tagged unary lifetime, and an independent
creation of \(Y\) is immediate success.  Geometric trials have uniform
finite mean time and birth count, independently of the initial \(X/Z\)
population.

If \(Y\notin U\), then \(Y=0\) is exactly invariant: every top complex
contains \(Y\), and the lower linkage cannot create it.  The fixed-class
projection is an open strongly connected unary network.  Killing its
one-particle graph at zero gives a transient subgenerator and the standard
linear Foster function.  Thus the invariant exception is discharged, not
discarded.

## 4. Shell service for every possible death species

In normalized fluid variables, the top ODE is exactly the time change

\[
 {dq\over ds}=q_{\mathsf Y}qQ,\qquad
 q(\theta)=q(0)e^{Q\theta},\qquad
 {d\theta\over ds}=q_{\mathsf Y}.
\]

On the compact shell \(q_{\mathsf Y}(0)\ge\rho\), every fixed operational
horizon is reached in uniformly finite physical time.  Irreducibility of
\(Q\) gives uniform convergence to its strictly positive stationary law.
Therefore the aggregate exposure

\[
             \int_0^T\sum_{i\in\{X,Y,Z\}}\delta_iq_i(s)\,ds
\]

can be made arbitrarily large, no matter which of \(X,Y,Z\) carries the
direct lower death.

For a population \(n\), the full-chain window has physical length \(T/n\).
On the rescaled interval the top density martingale has quadratic variation
\(O(n^{-1})\); lower unary clocks make \(O(1)\) jumps and hence an
\(o(1)\) density displacement.  Localization and Gronwall give the stated
uniform density limit.  The exact direct-death compensator then transfers
the deterministic exposure to the uniform conditional mean service bound
(6.4).  Constant births contribute only \(\beta T/n\).  The appended first
ordinary jump is legitimate, has mean holding time at most \(1/\beta\),
and charges at most one further birth.

## 5. Expected complete ledger

Let \(F\) be fractional return and \(I\) the catalyst-shell endpoint.  They
partition the prelude outcomes.  On \(F\), the pathwise workload identity
already gives

\[
                        D_{\rm pre}-B_{\rm pre}\ge H_0/2.
\]

On \(I\), the strong Markov property and the uniform shell estimate give

\[
       \mathbb E[D_{\rm serv}{\bf1}_I]\ge D_0\mathbb P(I).
\]

The geometric prelude has unconditional expected birth debt \(C_B\); the
service window and appended jump add at most two more units in expectation.
Choosing \(D_0=C_B+3\) and then the large-state cutoff gives exactly

\[
 \mathbb E(D_\tau-B_\tau)
 \ge D_0\mathbb P(F)+D_0\mathbb P(I)-(C_B+2)\ge1.
\]

This is the correct event-weighted expectation.  It does not ask the final
successful block to repay every realized birth on earlier failures.
Geometric attempt duration, the fixed service window, and the final holding
time give one uniform finite mean duration \(C\).  Thus

\[
 \mathbb E[H(X_\tau)-H(x)+\eta\tau]\le0
 \qquad\text{for }\eta=1/(2C),
\]

with endpoint integrability following from
\(H(X_\tau)\le H(x)+B_\tau\).

## 6. Verdict boundary and exact bytes

The theorem proves precisely the common-catalyst occupation macro needed
by the frozen workload-only physical-time Foster lemma.  It does not claim
the two-carrier or dyadic homogeneous kernels.  Within its stated support
family there is no remaining stochastic, boundary, conditioning, moment,
or endpoint seam.

The target hash, line count, byte count, and absence of hidden control bytes
were independently recomputed.  The exact Markdown was converted to
MathJax HTML and to letter-size LaTeX/PDF.  The render was inspected for
equation loss, malformed delimiters, and overflow.

**Frozen verdict: STRICT PASS.**
