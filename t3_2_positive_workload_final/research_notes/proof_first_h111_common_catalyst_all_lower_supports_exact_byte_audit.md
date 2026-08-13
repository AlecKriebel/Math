# Exact-byte hostile audit: common catalyst with all residual lower supports

**Audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The target of this audit is exactly

~~~text
research_notes/proof_first_h111_common_catalyst_all_lower_supports_theorem.md
SHA-256 81a48c007e092570cd500d8f124c0546538d44f7e62599100ecf00480f401496
360 lines / 14,150 bytes
~~~

The target was held immutable throughout the final replay.

> **STRICT PASS.**  The frozen target proves its literal theorem for
> \(T=\{X+Y,Y+Z,2Y\}\) and each of
> \(U=\{X,Y\},\{X,Z\},\{Y,Z\},\{X,Y,Z\}\), with arbitrary fixed
> strongly connected labelled orientations and arbitrary fixed positive
> rates.  The per-label coupling, global-clock conditioning, fractional
> stop, seeding, service, complete expected ledger, duration, endpoints,
> nonexplosion, and classwise handoff survive hostile replay.

This verdict is for the displayed common-catalyst family only.  It does not
certify either of the other homogeneous dead-ray kernels or the final
312-incidence composition by itself.

## 2. Exact top-particle identity

With one \(Y\)-molecule designated as catalyst, the remaining \(H-1\)
labels have counts \((X,Z,Y-1)\).  Assigning one free label to each top
reaction gives, without approximation,

\[
 YX,\qquad YZ,\qquad Y(Y-1),
\]

for the three falling-factorial source propensities.  Every target in the
top support contains \(Y\), so after a top jump one product \(Y\) can remain
the designated catalyst and the free label changes among
\(\mathsf X,\mathsf Z,\mathsf Y\).  The free labels therefore have
independent generator \(Q\) in operational time
\(A(t)=\int_0^tY(s)\,ds\), exactly as asserted in (2.4).  There is no
unspoken molecular pairing approximation.

## 3. Protected labels and arbitrary lower support

For each free label, the protected event uses only that label's top
graphical clocks and an independent dominating lower clock.  The lower
rate of one molecule at either \(X\) or \(Z\) is a fixed finite constant,
so one physical-time clock of rate \(K_*\) dominates all such clocks.
Requiring no candidate mark during \([0,a_0]\) is stronger than requiring
silence only until the terminal \(Y\)-hit and has probability
\(e^{-K_*a_0}\).

The block has physical duration at most \(a_0\) before its operational
endpoint whenever the global adverse clocks have not fired, because
\(Y\ge1\).  Thus this physical-time domination covers the entire successful
block.  Candidate clocks, top clocks, and labels are independent across
free labels, so the protected indicators admit the literal binomial
Chernoff lower bound.  Actual nonprotected \(X/Z\)-sourced transfers and
deaths remain active; they cannot change a protected label.  Once a
protected label reaches \(Y\), its top \(Y\)-out clocks are suppressed by
its own protected event and its lower \(Y\)-clock by the separate global
event.

This checks the load-bearing extension beyond \(R=\{0,Y,Z\}\).  In
particular, order-\(H\) clocks sourced at \(X\) are neither contracted nor
silently discarded.

## 4. Global event and fractional-return repair

Birth clocks and all lower clocks sourced at \(Y\) are disjoint from the
per-label protected clocks.  After revealing the protected events and the
allowed top and \(X/Z\)-sourced histories, their integrated hazard before
the earlier of \(A=a_0\) and the fractional stop is at most

\[
                  (K_Y^R+\beta)a_0.
\]

The frozen target correctly calls the resulting event **unspoiled**, not
clean.  On that event either the fractional-return branch has already
succeeded or the operational endpoint is reached.  Intersecting with the
protected-label Chernoff event therefore yields exactly the union in (3.3):
fractional return or catalyst shell.  This is the necessary repair of the
earlier false statement that no adverse clock alone implied an operational
endpoint despite fractional preemption.

The additive distinguished catalyst is absorbed by the slack
\(p_*/2\) versus \(\rho=p_*/4\), and absence of a birth gives
\(H_{\rm end}\le H_{\rm start}\).  Hence (3.4) is uniform for all
sufficiently large block starts.

## 5. Catalyst seed and invariant face

When \(Y=0\) and \(Y\in U\), strong connectivity of the lower support
supplies a simple path \(0\to\cdots\to Y\) of length at most three.  The
selected immigration clock has fixed positive rate, and the tagged
molecule's successive unary holding rates and branch probabilities are
fixed.  Deviations restart at their actual endpoints.  Competing bulk
unary reactions cannot delay physical time.  Geometric trials therefore
give uniform first moments for seed duration and total immigration count.

When \(Y\notin U\), the only allowed pattern is \(U=\{X,Z\}\).  Every top
complex contains \(Y\), and the lower linkage does not change \(Y\), so
\(Y=0\) is literally invariant.  The surviving lower chain is a finite
open-unary strongly connected linkage.  Its killed unary subgenerator is
transient and its standard positive resolvent vector gives the claimed
linear Foster reduction.

## 6. Geometric prelude and endpoint partition

Until fractional return, every active block begins above \(H_0/2\), so the
same conditional success probability applies after every seed.  The number
of complete attempts is geometrically dominated.  An active failure lasts
at most \(a_0\) and stops at its first adverse birth, hence contributes at
most one birth; the seed has the uniform first moments from Section 4.
This proves the two expectations in (5.2) without a bounded reaction-count
claim.

The terminal events are disjoint.  On \(F\), the pathwise workload identity
gives \(D-B=H_0-H\ge H_0/2\).  On \(I\), the actual endpoint has a fixed
positive catalyst fraction and retains every death from every failed
attempt.  No local successful block is asked to repay the realized birth
history.

## 7. Shell service and expected ledger

The shell ODE is exactly the time-changed finite-state equation

\[
        \dot q=q_{\mathsf Y}qQ,
        \qquad q(\theta)=q(0)e^{Q\theta}.
\]

Irreducibility of \(Q\), the lower bound
\(q_{\mathsf Y}(\theta)\ge\rho e^{-K\theta}\), and compactness of the shell
give a uniform finite physical horizon with arbitrarily large integrated
exposure to \(\sum_i\delta_iq_i\).  Strong connectivity of the lower graph
ensures at least one \(\delta_i>0\).  On physical time \(T/n\), the top
density martingale has quadratic variation \(O(n^{-1})\), lower clocks
produce \(O(1)\) reactions, and their density perturbation is \(o(1)\).
The exact direct-death compensator therefore proves the uniform conditional
service estimate (6.4).

The appended all-clock jump has mean holding time at most \(1/\beta\) and
adds at most one birth.  It makes the zero-time shell start harmless.  In
the final ledger, the prelude-birth contribution restricted to \(I\) is at
most its unconditional bound \(C_B\), the service-window expected births
are at most one, and the final jump adds at most one.  Thus (7.2) is a valid
event-weighted expectation, not a pathwise or conditional-birth assertion.
The duration and endpoint integrability conclusions then follow directly.

## 8. Physical-time and classwise handoff

Population-increasing binary reactions here have constant or linear
propensity, while quadratic top reactions preserve \(H\).  Standard
localization/Yule comparison gives nonexplosion, including arbitrary
neutral top depth.  Every stopped endpoint is an actual population and
every restart is justified by the strong Markov property.

The resulting inequality is precisely the occupation macro required by

~~~text
research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma.md
SHA-256 8cf2a8d41f0fab64bf34b6608fa7cf6b0f1b385a30f4a01afeb10c7732851b2a
~~~

whose independent strict audit is

~~~text
research_notes/proof_first_levelset_h_alone_physical_time_foster_lemma_exact_byte_audit.md
SHA-256 9d8fc8b5e15178e7a8305422ba7fd08e6875e851c37951207815d5d84babcc67
~~~

Accordingly the classwise positive-recurrence conclusion is valid for the
literal common-catalyst family, with the invariant open-unary face handled
separately as stated.

## 9. Reproduction and render

The target hash, line count, byte count, visible control-byte scan, and
Pandoc conversions were independently replayed.  Tectonic produced a clean
letter-paper PDF with no overfull, underfull, undefined-reference, or
missing-glyph diagnostic.  Every rendered page was visually inspected;
the theorem statement, lists, equations, tags, and final scope render
cleanly.
