# PR 292 / problem 30001608: independent source and stochastic recheck

**Verdict:** the claimed six-rate permanent-seed model matches the operative primary-source model. The complete TURN_4 proof survives this review, including every fixed real lambda>0. No falsifying state, hidden clock change, or surviving mathematical gap was found. This is a bounded mathematical/source assessment, not a worldwide novelty certificate.

The reviewed package is the 40-file frozen snapshot at head `1198534928f4c2bf8bf758c9ceb16edaa3a496e8`; every original-file hash was independently checked against SOURCE_SNAPSHOT. The independent source/model checkpoint was saved before reading TURN_4, its source recheck, any candidate checker, or prior substantive review. The interrupted source_model log was read only afterward. No candidate checker was read, imported, or executed; the retained controls were independently written.

## Source, clock, and scope

The state is (a,b,x,y) in N0^4, D=x+y+1, with two arrivals at lambda/2, first-download transfers A-to-X at a(x+1)/D and B-to-Y at b(y+1)/D, and completion departures X at x(y+1)/D and Y at y(x+1)/D. All +1 terms are retained. The theorem concerns irreducibility and positive recurrence in this continuous physical time, with a unique stationary probability law.

The three primary versions were read separately:

| primary body | operative evidence | version finding |
|---|---|---|
| [OWR 48/2010, printed pp.2782-2783](https://ems.press/content/serial-article-files/46306) | permanent seed, exponential contact clocks, DFC stability question and any-input-rate objective | DFC is the question on p.2782; the Enforced Friedman question on p.2783 is a different algorithm |
| [arXiv:0910.5577v1](https://arxiv.org/pdf/0910.5577v1), pp.7-9, Figure 2 | exact six intensities, seed terms and denominator | 2009 Conjecture 3.4 proposes sufficiently-high-load instability, not stability |
| [HAL hal-00781341 author proof](https://hal.science/hal-00781341/document), Section 2 p.5 and Section 3.2 pp.10-12 | positive-recurrence definition, Figure 2, invisible waiting-room explanation, Conjecture 3.6 | January 5, 2011 proof changes the conjecture to stability; HAL cover is dated January 26, 2013 |

The 2011 proof explicitly excludes the empty A/B waiting rooms from peer visibility. That resolves the apparent mismatch between generic peer-contact prose and the displayed denominator. The source's informal phrase about contacting another peer should not override Figure 2: strict exclusion of the contacting visible peer would give a different denominator. Null contacts, including self samples when interpreting the diagram through a contact protocol, do not change the six-event count generator. The rates depend only on the four counts, so no missing history or algorithm state is required for this count model.

The [actual publisher landing page](https://link.springer.com/article/10.1007/s11134-011-9209-2) confirms the 2011 bibliographic record, but exposes subscription preview rather than Section 3.2. Both the old alleged final-PDF response and the current retained publisher response are HTML; neither is an inspected final publisher PDF. Exact equality to that edition's body is therefore unverified. The controlling mathematical content was inspected in the author proof and crosschecked with the official OWR statement and 2009 figure. No journal page number for Conjecture 3.6 is inferred from metadata.

The 2011 simulation footnote uses fixed times between simulated changes. It supplies historical empirical motivation, not a stationary-law or finite-mean-return-time equivalence between clock conventions. TURN_4 uses the displayed continuous-time rates directly and does not rely on that simulation convention. The all-load quantifier is supported by the unrestricted 2011 conjecture and the surrounding any-input-rate objective. It means each fixed positive lambda; no uniform bound in lambda is required. Lambda=0 and additional chunks are outside this theorem.

The retained historical target record independently identifies problem 30001608 as the DFC stochastic stability question. It is a dated catalog crosswalk, not fresh evidence of current worldwide openness.

## Full proof assessment

I read every section of TURN_4 and checked the following implications analytically, before relying on finite computation.

1. The exact generator gives LW=2lambda-u-d, LZ=(y-x)/D, and L(Z^2)=2Z(y-x)/D+lambda+d. The rounded absolute value has the required Lipschitz derivative at both joins. The stated base-drift inequality follows with c/(2m)=1/8.
2. The finite birth/death corrector has geometric invariant weights. Its flux formula includes the terminal equation at R, its differences are negative, and extending g by zero past R preserves the stated comparison. Every fixed positive lambda permits finite R because the truncated mean tends to theta+1>theta. This is a finite auxiliary-chain calculation, not an unsupported stationary substitution in the original chain.
3. The product identity uses post-transition g values. Both ratio cutoffs decrease on both first-download events, so those potentially large-rate interface terms are nonpositive. Arrival and departure errors have the displayed bounds. The D=1 case has no departures. A departure can have a positive interface cost; the proof correctly bounds it instead of declaring it nonpositive.
4. The three regions exhaust the state space. If both visible counts exceed R, the corrections vanish on every one-step successor. In the one-small-count region, x>=3(y+1) gives both the sign of the imbalance term and qd>=y; the cutoff band is fully included. The two alternatives b/D>=eta and b/D<eta have uniform negative bounds. In the remaining region, the visible population is bounded and u grows at least linearly with a+b, yielding a finite exception set.
5. V is nonnegative and coercive. Each fixed positive lambda gives finite m,R,G,N,B. Population and actual-jump bounds establish nonexplosion. Stopping at finite population makes Dynkin's identity legitimate; nonnegativity, Fatou and monotone convergence remove localization and bound expected finite-set hitting time. Irreducibility and the finite neighborhood of that set justify the continuous-time Foster conclusion. No unproved uniform integrability of V is needed in this last passage.

Thus the proof supplies the missing uniformity over all states through a single pointwise Foster inequality. It does not transfer the main difficulty to a fluid-limit or switching assertion.

## Independent controls

`independent_controls.py` uses exact rational arithmetic and imports no candidate checker. It checks every auxiliary Poisson equation, including the top state, and 545 targeted generator states for each lambda=1/100,1,10. These include 212 states outside the claimed finite set for each load, both chunk orientations, cutoff thresholds, rounded-imbalance thresholds, zero coordinates, and arbitrarily large waiting populations. All 1,635 sampled states pass the exact identities and bounds. The selected R values are 54,89,476; the resulting N values are 6,324,144; 37,844,441; and 17,594,298,702. Large constants are permitted by the existence theorem.

Four meaningful negative controls also pass:

- Removing J gives positive base drift about 0.25 at lambda=1 and (a,b,x,y)=(0,378444410,378444410,0), whereas full LV is about -19.09.
- Replacing D by total population while retaining the original cutoff test breaks the corrector comparison at the same state: modified Lg is about -9.67 while the asserted upper bound would be about -18.39. This detects a source-model substitution, not a counterexample to the actual chain.
- Removing the seed numerator terms makes zero visible population absorbing and leaves positive LV=17/8 at the recorded large-waiting state. It also makes the waiting population grow with arrivals, so the permanent-seed assumption is essential.
- A concrete departure from y=R to R-1 has positive interface cost about 0.00342. An argument suppressing every departure-interface cost would be false; the candidate's positive error allowance handles it.

Finite checks are implementation/error-detection evidence. The all-real-load, all-state conclusion rests on the analytic inequalities just assessed, not on this finite sample.

## Distinct limiting challenge and exact remaining boundary

`LIMITING_DERIVATION.md` derives and justifies the fixed-horizon family (floor(rho R),b,n,R). X has births rho(X+1) and deaths X; B is immigration/death. Stopping, pure-birth domination and arbitrary-order moment bounds give finite-horizon convergence and first-moment convergence. This is stronger than the unproved critical-regime heuristic, but remains local in horizon and ratio.

At rho=1 the rederived means include the seed-driven term -t^2/2 in the majority population. An independent Gillespie diagnostic at lambda=10 and R=10^6 agrees with the predicted means at t=1 and t=10 within 1.5 estimated standard errors.

At rho=0,n=0, however, expected total-population increment tends to (lambda-1)t on every fixed time horizon. At lambda>1 it remains positive for every such horizon. Even rho=1/2 at lambda=10 yields positive limiting drift for every fixed horizon. Therefore an unweighted total-population Foster argument on a fixed physical-time skeleton is blocked. This is a falsified shortcut, not a counterexample to stability. The global candidate's workload and imbalance terms survive this challenge.

| approach family | status | exact gap or conclusion |
|---|---|---|
| source/version reconstruction | passed within stated edition limit | final publisher body not independently available; operative figures and author proof verified |
| critical and noncritical boundary limits | verified local result | no uniform infinite-time or state-uniform recurrence conclusion follows |
| raw total-population fixed-time skeleton | blocked by positive limiting drift | needs a materially different function or controlled state-dependent horizon |
| submitted global cutoff-Poisson Foster proof | passed full-scope review | no surviving mathematical gap identified for the exact six-rate chain |

No outside individual was contacted. External expert input could provide further independent scrutiny, but no outreach was prepared or initiated. No Git, PR, Sheet, Zenodo, or other remote state was changed. Literature priority remains a separate review obligation.

Completion estimate: **100% of this bounded source/model and stochastic review**. This does not assign a percentage to worldwide novelty or to the larger research program.
