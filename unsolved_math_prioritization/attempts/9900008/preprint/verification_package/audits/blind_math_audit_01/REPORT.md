# Independent mathematical audit of PR883 / problem 9900008

Audit UTC: 2026-10-15T11:35:25.560Z
Decision: **PASS — the submitted negative answer is mathematically valid under the original pointwise-covariant allocation convention.** No mathematical repair is required. This is an independent agent audit, not human review or formal certification. It establishes neither novelty nor priority.

## Independence, timing, and scope

The source-first memo was prepared at 2026-10-15T11:28:52.172Z and saved at 2026-10-15T11:28:59.690Z. Before that save, the only mathematical inputs read were the exact native target record, Thorisson's original Section 4, and the relevant original Last–Thorisson definitions and discussion in 0906.2062. The candidate proof was read only afterward. The analytic verdict was frozen at 2026-10-15T11:31:24.105Z before viewing any old auditor verdict, acceptance, or literature report. No such comparison was subsequently needed or performed.

The memo independently proposed parallel diffuse lines with unequal quotient weights and a biased root law. It initially used an irrational weight as a sufficient way to obstruct splitting. After reading the candidate, I checked its stronger elementary observation: with just one source family of each weight modulo the forced period, distinct positive weights 1 and 2 already suffice. Irrationality is unnecessary in this periodic construction.

This work reviewed and reproduced the submitted proof. It did not initiate a new deep literature campaign, inspect the referenced PR284 or any other problem attempt, contact people, mutate external services, or operate on Git. All writes and executions were confined to this audit's dedicated folder. Original-proof effort remains the supplied 1/5; review and reproduction do not increase it.

## Exact claim and primary-source ledger

The universal claim under test is the reverse direction of the proposed equivalence: for diffuse locally finite random measures on the permitted LCA groups, does invariance under every measurable equivariant measure-preserving allocation imply mass-stationarity without an independent stationary background? A single valid example on R² refutes that implication. The separate Markovian-kernel question is outside this audit's conclusion.

| Input | Exact material checked | Role |
|---|---|---|
| Native whole_record.json | Entire record, ID 9900008 / AMR-098-0008 | Identifies the exact background-free allocation problem and its full group scope. Metadata about historical research status is not accepted as a current literature verdict. |
| Thorisson, *Some Open Probability Problems* | Entire Section 4, printed pp. 5–6; both pages visually inspected | Original Problem 4.1 and the preceding displacement-generated allocation class. No freeness, full-support, planar-density, or injectivity hypothesis appears. |
| Last–Thorisson, 0906.2062 | Section 2 flow/measurability/Palm definitions; Section 3 invariant kernels and Example 3.4; complete relevant Section 4 transport theorem and proof; Section 6 definition, Remark 6.2, theorem and derivation; Section 7 discussion and Problems 7.5–7.7. Printed pp. 9, 18, 24 visually inspected. | Pointwise covariance, spatial preservation, rooted-law invariance, full joint mass-stationarity law. |
| Last–Thorisson, 1405.7566 | Complete relevant Section 2 and Sections 5–9 bodies, including proofs of Theorems 4–8, the background construction and lemmas, product-lift Proposition 1 and its proof, and final transport interpretation. Printed pp. 9, 12, 15 visually inspected. | Compatibility check: the density theorem and independent-background theorems do not imply the claimed background-free converse for this singular example. |
| Submitted PROOF.md | Entire proof | Audited construction, universal argument, counterevent and optional Palm check. |
| Submitted verify.py and certificate.json | Entire source and certificate, before any execution | Supplementary finite diagnostics, reproduced on private copies. |

The exact bytes and SHA-256 hashes are recorded in INPUT_PINS.json. No author-provided saved success result was used as verification. The proof's reference to a related PR supplies attribution, not a black-box dependency: the finite unequal-weight argument needed here is proved in full in the submitted text and reconstructed below.

Primary public sources: [Thorisson's original note](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), [0906.2062](https://arxiv.org/abs/0906.2062), [1405.7566](https://arxiv.org/abs/1405.7566). These links identify conventions and theorem scope; they do not establish priority of this submitted construction.

## Complete reconstruction of the decisive argument

### 1. State, action, and measure

Let

\[
\nu=\sum_{n\in\mathbb Z}\delta_n+2\sum_{n\in\mathbb Z}\delta_{n+1/2},
\qquad \mu=\lambda_1\otimes\nu.
\]

On the standard Borel circle \(\Omega=\mathbb R/\mathbb Z\), set

\[
\theta_{(a,b)}u=u+b\pmod1,\qquad
\xi(u)=\theta_{(0,u)}\mu,\qquad Q=\delta_0.
\]

Use a constant X with its trivial action. For each compact planar rectangle, only finitely many horizontal lines contribute and each intersecting segment has finite length; hence every \(\xi(u)\) is locally finite and Radon. Every singleton has zero mass because its horizontal Lebesgue factor is zero. The measure is nonzero, and the root lies in its support at the only Q-supported state.

The action is jointly Borel and obeys the group law. The random measure is flow-adapted with the source's sign convention \(\theta_t\eta(B)=\eta(B+t)\). For a compactly supported continuous test function f, the integral against \(\xi(u)\) is a finite sum locally in u of continuous line integrals. Thus the phase-to-measure map is vaguely continuous. The locations of lines of mass density 1 distinguish u modulo 1, so it is injective. A continuous injection from the compact circle to the Hausdorff vague measure space is an embedding. The evaluation sigma-field therefore recovers \(\mathcal B(\Omega)\): \(\sigma(\xi)=\mathcal F\).

Consequently, using phase states does not enlarge the observable randomness available from (X,xi). The action has horizontal stabilizers and integer vertical stabilizers. Their presence is permitted by the original problem.

### 2. All measurable preserving allocations, including noninjective ones

Take any pointwise-covariant measurable allocation. From the original definition,

\[
\tau_u(s)=s+\pi(\theta_su),\qquad \pi(u)=\tau_u(0).
\]

This representation follows directly by substituting the root in the covariance identity; it imposes no continuity, injectivity, or differentiability. Write \(\pi(0)=(a_0,b_0)\) and \(\pi(1/2)=(a_1,b_1)\). Since \(\theta_{(x,n)}0=0\) and \(\theta_{(x,n+1/2)}0=1/2\), every support point satisfies

\[
\tau_0(x,n)=(x+a_0,n+b_0),\qquad
\tau_0(x,n+1/2)=(x+a_1,n+1/2+b_1).
\]

Thus the horizontal invariance forces each full source line to be translated, rather than split. Integer vertical invariance forces consecutive source lines in one family to have consecutive target heights. A single family cannot fold two distinct members onto the same target line. Collisions between the two different families have not been excluded at this stage.

For any Borel set, translation invariance of \(\lambda_1\) yields the exact spatial pushforward

\[
(\tau_0)_*\mu
=\lambda_1\otimes
\left(\sum_n\delta_{n+b_0}+2\sum_n\delta_{n+1/2+b_1}\right).
\]

If this equals mu, comparison on rectangles \([0,1)\times A\) gives equality of the transverse measures. Restrict those measures to the finite interval \([0,1)\), then map this interval into the circle. There is exactly one representative of each source family in this interval, so

\[
\delta_{[b_0]}+2\delta_{[1/2+b_1]}
=\delta_0+2\delta_{1/2}.\tag{*}
\]

This is a finite per-period identity. Pushing the unrestricted infinite measure straight to the quotient would be invalid; that operation is not used.

Both source residues in (*) must belong to the target support, since positive off-support mass cannot cancel. If they coincide, the receiving residue has mass 3, unlike either target mass. If they are distinct and swapped, the mass at 0 is 2 instead of 1. Thus the only possibility is

\[
[b_0]=0,\qquad[1/2+b_1]=1/2,
\]

and both b's are integers. In particular \(\theta_{\tau_0(0)}0=0\). This proves rooted-law invariance under every allocation in the stated class. Noninjectivity on the mass support was allowed and eliminated only by the exact balance equation; arbitrary behavior off the support remains harmless.

Only preservation at state 0 entered this reasoning. It therefore covers both everywhere-preserving allocations and allocations preserving xi merely Q-almost surely. Restricting any allocation on a larger canonical pair space to this invariant orbit gives an allocation in the class already treated, so the orbit presentation does not miss a globally defined source allocation. Conversely, the source's xi-measurable subclass is also covered because the proof handles the entire measurable class here and \(\sigma(\xi)=\mathcal F\).

### 3. Exact failure of the full mass-stationarity law

For \(C=[0,1)^2\), let U be uniform on C, independent of the state. The source's definition requires

\[
(\theta_V\xi,U+V)\overset d=(\xi,U),\qquad
V\mid(\xi,U)\sim\xi(\cdot\mid C-U).
\]

The chosen C is relatively compact, has positive Haar measure, and its boundary has zero planar Haar measure. For every \(U_2\in[0,1)\), the half-open vertical interval \([-U_2,1-U_2)\) contains the light line at 0 and exactly one heavy line. The latter is at 1/2 for \(U_2<1/2\), and at -1/2 otherwise. The horizontal section has length 1. Hence \(\mu(C-U)=3\), including the half-open boundary cases.

Conditional on U, a light line is chosen with probability 1/3 and a heavy line with probability 2/3. Horizontal displacement does not affect the state. Thus the measurable event

\[
A=\{\eta:\eta([0,1)\times\{0\})=2\}
\]

has probability 0 for the original law and 2/3 for \(\theta_V\xi\). This already falsifies the required joint equality.

One can check the whole output law in this box as an additional safeguard. Conditional on the line type, \(U_2+V_2\) is respectively \(U_2\) or \(U_2+1/2\pmod1\), so it is uniform. The line-type probabilities do not depend on U. Also \(U_1+V_1\) is uniform on \([0,1)\), independent of the remaining variables. In phase coordinates the complete sampled output law is

\[
\left(\tfrac13\delta_0+\tfrac23\delta_{1/2}\right)
\otimes\operatorname{Unif}(C),
\]

whereas the required right side is \(\delta_0\otimes\operatorname{Unif}(C)\). There is no marginal-only definition substituted into the proof.

### 4. Optional Palm check

Under uniform phase measure P, the action is stationary. In a unit box each phase contributes one line from each family. Shifting to the light family produces phase 0 and shifting to the heavy family produces phase 1/2. The Campbell integral therefore equals \(f(0)+2f(1/2)\); the intensity is 3 and the normalized Palm law is \(\delta_0/3+2\delta_{1/2}/3\). This agrees with the direct sampling result. Non-mass-stationarity does not rely on merely exhibiting a different Palm law: the explicit mass-law event above independently proves it.

## Adversarial checks and boundary variants

| Attempted failure | Result and reason |
|---|---|
| Split a diffuse line measurably, including pathological maps | Exact horizontal covariance forces a translation on every support line; such splitting is excluded by the source's own class, not by an added regularity assumption. |
| Fold two light lines onto one heavy line | The unit vertical period forces n to map to n plus one fixed offset; members of a source family cannot collide. |
| Collide light and heavy families | The received mass would be 3, contradicting (*). |
| Send mass to an unsupported residue | Nonnegative spatial mass cannot cancel there. |
| Alter only the null singleton at the root | Not pointwise covariant. Changing pi(0) changes every point on every light source line, a set of positive mass in every suitable box. |
| Use Q-a.e. preservation to avoid the balance equation | Q is concentrated at 0, so Q-a.e. preservation is exactly preservation at the state used in the proof. |
| Detect unobserved phase information | The phase-to-measure map is a measurable embedding; no hidden auxiliary random variable is present. |
| Reject the measure for being singular or lacking full support | Diffuse means no atoms; it does not mean planar absolute continuity. Full support and freeness are absent from the original hypotheses. |
| Use zero mass in the conditional sampling box | The box mass is exactly 3, so no arbitrary zero-denominator convention enters. |
| Invoke the later positive-density theorem | Theorem 6 of 1405.7566 assumes an actual density field, positivity and specified line-integrability/infinite-half-line conditions. This line-supported measure has no planar density. |
| Invoke the later diffuse/product-lift theorems | Theorems 7 and 8 explicitly retain independent stationary backgrounds. Proposition 1 preserves mass-stationarity under a Lebesgue product; it does not remove that background from the allocation characterization. |
| Extend the result to Markovian kernels | Unsupported: fractional kernels can split mass and are outside the allocation calculation. |

There is a useful exact demonstration of the convention boundary. Let v=(0,1/2) and define

\[
\widehat\tau_u(s)=s+v\,1_{\{u=0,\ s=0\}}.
\]

This map is measurable and preserves each diffuse \(\xi(u)\), because it changes only one spatial singleton. For each fixed u,t its covariance identity fails at most at s=0 or s=t, hence holds spatially xi(u)-almost everywhere. Nevertheless its root at u=0 moves to phase 1/2. It is therefore a counterallocation under the *different* spatial-a.e.-covariance convention with an unrestricted root value. It is not a counterallocation under the pointwise convention used in the original problem, whose displacement representation enforces the line formulas above. The submitted proof correctly identifies this limitation.

Equal weights supply another boundary check. In the formal two-family quotient equation they permit both identity and swap. For the candidate half-period spacing the two measure phases then coincide, and the claimed unequal-root-density discrepancy disappears. The unequal-weight hypothesis is doing real work. Removing the horizontal Lebesgue factor would leave atoms and violate diffuseness; removing its stabilizer by adding spatial information would invalidate the line restriction. These observations do not enlarge the audited theorem.

## Reproduction and evidentiary limits

All candidate verifier source was inspected before running it. The verifier and certificate were copied into a private subfolder; those copies were executed with Python 3.14.6 in ordinary and optimized (-O) modes. Both actual exits were 0. Each run checked 9 quotient labels, 530 exact rational windows, 361 translation pairs, 18 rejected negative controls, and two accepted unequal-weight variants. Candidate manifest integrity was not claimed or run; the audited inputs were pinned independently.

The independently authored independent_exact_checks.py imports no candidate code. Its actual exit was 0. It checked 16 residue-label pairs (including separate off-support labels), 2,401 rational translation pairs with 25 balanced cases, and the full phase/recentered-coordinate product law on 4,160 exact grid inputs across 64 even denominators, including half-open boundary inputs. Its equal-weight control returned both assignments as expected.

EXECUTION_RECEIPT.json contains the safe structured receipt, actual exits/counts, full finite JSON outputs, and output hashes. Raw absolute command paths and PDF renders remain private and are excluded from the explicit public manifest. The native exec_command tool surface failed to launch, but actual local Python execution succeeded through Node's child-process interface; there was no execution blockade.

These computations are finite diagnostics. They cannot prove the uncountable all-allocation statement, the measurability assertions, or a continuous joint law by sampling. Those claims were checked by the exact derivations above. No empirical/model assumption or numerical approximation is needed for the mathematical counterexample.

## Final assessment

The strongest verified claim is exactly the submitted counterexample on R²: a nonzero diffuse locally finite measure, with constant X and no background randomness, has a rooted law invariant under every pointwise-equivariant measurable preserving allocation, yet fails the original full mass-stationarity law by an event discrepancy of 2/3. The universal proposed equivalence is therefore false in its stated group class.

There is no remaining mathematical gap identified in this construction. The result does not address a modified free-action formulation, one-dimensional diffuse measures, positive planar densities, independent-background allocation characterizations, or the separate Markovian-kernel question. Novelty, priority, redistribution, and publication decisions remain separate gates and are not certified by this PASS.
