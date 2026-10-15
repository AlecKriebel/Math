# PR883 / PID9900008: independent disposition adversary

Audit UTC: 2026-10-15. Frozen candidate head: `af25d26e21945a1a132aace5e600485152777070`. This report evaluates a proposal. It performs no status, PR, Git, publication, or tracker action.

## Decision

**ISSUES: the mathematics of the complete prior-input implication is CLEAR, but the proposed categorical `already_solved` disposition is not established by that implication alone under the user's supplied definition.** The exact strongest finding is that the negative diffuse conclusion is an elementary, completely checkable corollary of Last–Thorisson's old atomic counterexample and Lebesgue-product mass-stationarity proposition, after the allocation-transfer argument below. Existing literature also recognizes the relevant atomic-quotient allocation obstruction. This is a substantial priority/credit finding. It does not establish a date or person of an earlier resolution of the target question, or establish that the target had already ceased to be open in the historical sense.

The current proposal acknowledges the historical gap but then makes that gap immaterial to a status defined by “the open problem was not actually open.” That is an additional interpretation of the user's category, not a mathematical consequence of the checked formulas. The user did not require a novel mechanism, firstness, or a new general theorem. On the present evidence I recommend retaining the existing exact `claimed_solved` category and, if proceeding, using a fully credited explanatory research note that decisively answers the historically stated question without claiming present openness, a new resolution, or priority. A useful new explicit corollary/realization can be scientifically legitimate even when its ingredients and mechanism are established. This audit does not certify novelty of that corollary or of the periodic realization.

If the parent instead obtains a prior explicit target resolution, or adopts an express project convention that `already_solved` includes newly recognized elementary consequences regardless of historical recognition, then the proposed immediate-skip behavior is correct. No such express convention was supplied in the verbatim user instructions examined here. Do not manufacture a historical first-resolution assertion to remove this issue.

## Independent mathematical reconstruction

I read the full proposal and frozen `source/author/PROOF.md`, then independently checked the central primary definitions and proofs before reading the two priority-family reports. Earlier accepting mathematical audit verdicts were not used as authority. Inspection was local: no new literature search or external communication was performed. Source hashes are recorded in `INPUTS.json`.

### 1. Exact target and the original periodic proof

LT2009 Example3.4 defines a measurable allocation by pointwise covariance, equivalently `tau_y(s)=s+pi(theta_s y)`. Neither injectivity nor a free action is required. Definition6.1/Remark6.2 requires the full joint mass-stationarity identity, including the uniform window point. Problem7.5 asks whether a diffuse measure's law invariant under every preserving allocation is mass-stationary. The inspected Thorisson Section4 defines the same original-pair displacement class and asks the same question without an added stationary independent background.

For the candidate, let `nu=sum_n delta_n+2 sum_n delta_(n+1/2)` and `mu=lambda_1 tensor nu`. The phase space is a circle; its entire observable state is invariant under horizontal translations. Covariance therefore forces each complete horizontal source line to translate to a complete line, with one displacement for the weight1 family and one for the weight2 family. Restricting the resulting vertical periodic measures to a period gives

    delta_[b0] + 2 delta_[1/2+b1] = delta_0 + 2 delta_[1/2].

A collision has mass3, swapping gives incorrect masses, and there is only one source family of each weight per period. Thus both vertical displacements are integers. The root shifts in the full stabilizer, so its rooted law is fixed by every such preserving allocation. This handles noninjective possibilities rather than assuming them absent. It also covers preservation only almost surely because only the supported phase0 is used.

For `C=[0,1)^2`, the mass in `C-U` is3 almost surely: one weight1 line and one weight2 line, each across a horizontal segment of length1. The mass-chosen root lies on a weight2 line with probability2/3, while the original root is on a weight1 line with probability1. The measurable statistic `H(eta)=eta([0,1) times {0})` consequently has different laws. A failure of this marginal defeats the full joint identity. Local finiteness, diffuseness, Borel phase action, injectivity of the phase-to-measure map, nonzero mass and root support all check directly. Constant X is valid. This is a counterexample on R²; it does not cover one-dimensional, free/no-invariant-direction, positive-density, added-background, or general Markov-kernel variants.

No mathematical repair of this frozen proof is required.

### 2. The LT2009 counterexample survives passage to the measure alone

Work on R. Under the source law, `N1` is a Palm rate-one Poisson process, `N2` is an independent stationary rate-one Poisson process, and `zeta=N1+c N2` for positive irrational c. The source proves invariance of the full two-process state under every preserving covariant allocation: on disjoint simple configurations, an incoming target mass is `k+c l`, with nonnegative integer k,l. Equality to1 or c forces conservation of each point type. The preserving rule is therefore N1-preserving; the Palm invariance theorem applies. This argument permits collisions whenever compatible with mass conservation; irrationality prevents the unwanted ones.

Any measurable rule determined by zeta alone pulls back measurably to the two-process state. If it preserves zeta, it is in that already-covered class. Full-state invariance implies zeta-marginal invariance. No converse factor theorem or recovery of hidden marks is needed. On the full-probability disjoint-simple set, the weights1 and c do in fact distinguish the types; that observation is consistent but unnecessary for this direction.

Non-mass-stationarity also survives forgetting the types. Under the original law `zeta({0})=1` almost surely. For a suitable bounded window, the defining mass choice hits an N2 atom with positive probability, giving `zeta({0})=c` after the shift. This is an observable measure event, not merely an event of the marked state. Thus constant X suffices and the source supplies the required base counterexample on the canonical measure space.

### 3. Every lifted allocation, including noninjective ones, projects correctly

Use canonical locally finite measure spaces and the evaluation sigma-fields, or keep an original observable pair `y=(X,zeta)` throughout. Set `J(y)=(X,zeta tensor lambda_1)` and let the extra R coordinate act trivially on the entire original state. An arbitrary lifted displacement has measurable coordinates `(a(y),b(y))`; covariance gives

    That_y(s,u) = (s+a(theta_s y), u+b(theta_s y)).

Put `rho_y(s)=s+a(theta_s y)`. It is a measurable pointwise-covariant base allocation. For bounded Borel A in R^d and a bounded Borel interval B with finite positive length, Tonelli gives

    (That_y)_*(zeta_y tensor lambda_1)(A times B)
      = integral 1_A(rho_y(s)) [integral 1_B(u+b(theta_s y)) du] zeta_y(ds)
      = lambda_1(B) (rho_y)_* zeta_y(A).

No inverse of That or rho is used; b can be arbitrary measurable and source fibers can collide. Lifted preservation implies base preservation by dividing by the finite positive length. Conversely base preservation gives equality on bounded rectangles. The pushforward then has finite mass on a countable rectangle cover because its rectangle masses equal those of the locally finite target. Both measures are consequently sigma-finite, and equality extends to the entire product Borel sigma-field. This avoids both cancellation of infinite quantities and any unjustified quotient pushforward of an infinite periodic measure.

At the root, `theta_(a(y),b(y)) J(y)=J(theta_a(y) y)`. Thus base allocation invariance implies full lifted rooted-law invariance for every lifted preserving allocation. It is not enough to test only a selected lifted subclass; the displayed formula treats an arbitrary lifted rule. Conversely a base preserving allocation lifts with b=0, giving equivalence when desired.

### 4. Measurable inverse and global all-state extension

The product map on canonical measure spaces is measurable. For a locally finite eta on R^(d+1), define `D eta(A)=eta(A times [0,1))`. This is a locally finite measure because a compact A times [0,1) lies in a compact cylinder. Its evaluations are measurable, and `D J zeta=zeta`.

The image E of J is exactly the set where `eta=(D eta) tensor lambda_1`. It is Borel: equality can be tested on a countable family of bounded rational half-open rectangles, which determines locally finite Borel measures. E is invariant under the full product translation action. The same assertion holds for pairs with X carried unchanged.

If a convention demands an allocation defined and preserving at every point of a larger canonical state space, define a desired lifted displacement on E by reading D eta and set it to0 off E. The image is Borel, so this is measurable; invariance of E makes the resulting allocation covariant and identity everywhere off E. It preserves every state. Thus no almost-sure-only extension assumption is hidden. For the forward implication needed for the counterexample, a globally preserving lifted rule simply pulls back to a globally preserving base rule via J.

If preserving is only required almost surely, the preservation event is measurable using a countable determining family and is invariant by covariance. Replacing the rule by identity off that event gives a globally preserving covariant rule agreeing almost surely. The same conclusion holds.

### 5. Full mass-stationarity transfers, with an independent witness

LT2014v1 Section8 Proposition1 and LT2015v2 Section8 Proposition1 state preservation and reflection of the full joint mass-stationarity property under `zeta -> zeta tensor lambda_1`, with the original state action extended trivially in the extra coordinate. The proposition matches the construction above. The v1 displayed proof has a window-size typo; the v2 consistent n-window and the elementary product experiment confirm the statement. The typo does not defeat the implication.

Independently, for a product window, its mass-normalized product restriction chooses the original-coordinate displacement by zeta-mass and the added displacement uniformly in the added interval. The original-coordinate root event above therefore still changes with positive probability. The statistic `eta({0} times [0,1))` records the base atom weight from the lifted diffuse measure. This directly defeats even the shifted-measure marginal, hence the full identity, with no reliance on hidden marked information.

The lift is nonzero, locally finite and diffuse because a bounded rectangle has finite base mass times finite length, and each singleton has zero Lebesgue factor. The extra coordinate supplies a stabilizer, not random background information.

**Accepted mathematical consequence:** the unrestricted diffuse negative answer follows completely from the old base counterexample, the checked allocation-transfer bridge and the published product proposition. There is no outstanding mathematical gap in this consequence.

## What the priority sources do and do not establish

The final KM2025 Remark3.2 explicitly treats a Lebesgue product with atomic quotient and reduces its balancing-allocation existence problem to the quotient problem; it expressly allows atomic maps that need not be injective or surjective. Its statement is not the allocation-invariance-versus-mass-stationarity conclusion. LT2015 Section9 is compatible with the displayed transfer, but the inspected statements do not announce the target negative answer.

Accordingly it is justified to say that the candidate's broad mechanism and an entire route to its general existential conclusion are already in prior theory. It is not justified to say that KM2025 directly resolved Problem7.5, or that LT2014 explicitly announced its negative answer. No prior explicit target resolution was located in the bounded material supplied. Historical first recognition, exact periodic realization priority, and exhaustive absence of another example remain unknown.

The derivation above is mathematically short. Its shortness supports an editorial assessment that the note is explanatory rather than a substantial new general theorem. Shortness alone is not documentary evidence that the open question was previously resolved: an unrecorded corollary can be recognized for the first time later. The corollary may be new or known; this audit establishes neither. A category whose definition depends on earlier resolution should not silently be redefined as a test of the depth or length of the new bridge.

The candidate already carries a no-novelty/no-priority disclaimer. That disclaimer is compatible with the checked result. It does not itself declare the problem previously solved.

## Required correction to the proposed disposition

1. Replace the categorical inference “complete prior-result implication, therefore `already_solved`” with the narrower finding “complete elementary known-input corollary; historical prior explicit resolution unverified.” The mathematical route and all predecessor credits should remain recorded.
2. On the evidence supplied, do not change the QUEUE status solely to invoke the skip rule. Retain the exact existing `claimed_solved` status, 1/5 effort, blank DOI and frozen sources. The user has not imposed novelty/firstness as a prerequisite to a qualified note. A note may say it gives an explicit periodic counterexample to the historical question and displays its old-input implication; it must not claim that the problem is currently open or that this is a new resolution. Full publication-stage review would still be required; this report does not authorize or replace that gate.
3. If the parent decides `already_solved` is nonetheless the intended operational convention, state expressly that this is a project classification of an immediate corollary, not an authenticated historical priority result. That is a judgment beyond the present documentary proof; this audit does not issue CLEAR for it. Stronger prior-resolution evidence or a directly applicable explicit convention would resolve the issue.

## Skip rule, close rule, and metadata gate

Conditional on a justified `already_solved` classification, the proposed mechanics are faithful: a still-eligible PR can be corrected on its own target row; once the status is no longer exactly `claimed_solved`, stop processing it, leave it open/draft/unmerged, add no comment, and prepare no paper/deposit/tracker row. The repeated specific skip prohibition controls over the generic close-failed-result instruction. The mathematics has not failed, and no closure is warranted on this audit's findings.

That conditional mechanics approval does not establish the category itself. Reclassifying merely because the authorized publication framing is uncomfortable would use a status mutation to evade work that remains in scope. The narrower qualified framing above provides a reasonable repair without falsifying the theorem or inventing novelty.

No live metadata was fetched in this adversary task. Before any eventual mutation, the parent must recheck that PR883 is still open/draft, its exact QUEUE status is `claimed_solved`, and its head is the frozen hash. A changed head or status invalidates this report as approval for a mutation until re-gated. Preserve all26 frozen source files, original1/5 effort, blank DOI, unrelated rows and unrelated repository bytes. This is a normal precondition for the proposed action, not a finding that an action has already violated it.

## Safety and exact completion

All audit outputs are original prose or metadata. The public allowlist contains no source PDFs, extracted third-party text, raw tool responses, dataset bodies, or publication artifacts. No other PR was substantively reviewed or acted on. An initial broad local search for task definitions incidentally displayed unrelated program records; this was stopped and not used to assess them. No external people were contacted, no new central proof search was undertaken, no PDF or paper was authored, and no Git/PR/Zenodo/Sheets action was taken.

Audit completion:100%. Mathematical prior-input consequence:100% checked within the source conventions. Historical prior explicit resolution:unverified. Final disposition is unresolved pending the parent's response to the category issue; it is not made complete by this audit.
