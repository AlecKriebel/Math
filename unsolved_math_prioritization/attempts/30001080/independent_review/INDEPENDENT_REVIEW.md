# Independent full review: 30001080

## Verdict

**PASS_COMPLETE_SOURCE_QUALIFIED_TRANSPORT_CHARACTERIZATION.** No mandatory mathematical correction. This verdict binds the unchanged `TURN_2.md` SHA-256 `87664cd4c83fd77f0835165189a99119f936c5e1df14408cfaffb2ad8044bf21` and author `FROZEN_MANIFEST.json` SHA-256 `ff0e2b79fbd6f24ef89a2683ee26e188f64d664965d287d0859648969a01ca66`.

The final proof answers the full abstract, measure-only Markov question of Last–Thorisson (2009), Problem 7.3, under its locally compact second countable Hausdorff Abelian, locally finite, nonzero and sigma-finite assumptions. It separately proves the canonical-law characterization using actual Cox-derived singleton matchings with the original intensity measure retained as background. That is a source-qualified affirmative answer to the OWR distribution-of-the-measure question. The qualification that the matching can observe the original measure must remain explicit. No theorem for a stricter Cox-only observation rule or for a non-Abelian/non-second-countable group is certified.

Two substantive author turns are documented. A `claimed_solved 2/5` disposition is supported for this precise target. The new proof is a candidate deduction from credited classical inputs; this audit does not certify historical novelty or community acceptance. The parent retains the publication gate.

## Independence and evidence

The reviewer did not contribute to either author proof. The review reconstructed the measurable arguments, read the complete relevant original and foundational contributions, checked the precise theorem hypotheses, and independently wrote finite controls on noncyclic groups. All 13 manifest-bound author files and all five full source PDFs match their hashes and byte counts. Both supplied programs were read and replayed; their 18,814 and 75,172 exact assertions reproduce the frozen receipts byte for byte. The separate reviewer program passes **186,869 exact assertions**. Finite controls check implementations and counterexamples to shortcuts; they do not establish infinite-dimensional measure identities.

## 1. Canonical first-turn proof

The positive integrable function of the canonical measure is available because the canonical law is sigma-finite. It is legitimately measure-only. Its symmetric endpoint factors give a finite test measure, and each symmetric gate yields a row-substochastic jump part completed by a holding atom. Spatial preservation follows by Tonelli and symmetric interchange of the endpoints.

The finite holding subtraction is valid on finite-Q test sets. Finite marginal uniqueness extends the equality to bounded tests before the antisymmetric signed-measure argument is used. If `nu=m-R_*m`, then `d_f nu` is reversal-invariant. Symmetrizing an arbitrary measurable set gives `d_f nu=0`. A countable separating family is required only for the standard Borel Radon-measure space. It kills the defect outside the period graph. On the period graph, the restriction of the measure to its closed stabilizer subgroup is zero or Haar, and the weight is even. Positive deweighting and compact exhaustion give the full Mecke identity. The first turn correctly records that this argument alone does not handle an arbitrary auxiliary state.

## 2. Off-base-diagonal lemma in the final proof

I checked the endpoint identities without assuming that the auxiliary state space is standard Borel. For a canonical separating set A and a displacement set B, let F consist of `(mu,t)` with `mu in A`, `theta_t mu outside A`, and `t in B`. Then F and its reversal are disjoint. The allowed gate is their union. Testing invariance against `1_D(omega)1_A(xi(omega))`, where Q(D) is finite, yields exactly

`m((D x B) intersect rho^{-1}F_A) = R_*m((D x B) intersect rho^{-1}F_A)`.

The incoming nonnegative term is bounded by the full invariant Markov expectation; the outgoing term is bounded by Q(D). There is no subtraction of infinite quantities. Restricting to a countable finite-Q partition gives a common finite product cover for measure uniqueness. Equality for rectangles therefore extends to every measurable subset of the corresponding off-base-diagonal piece. A countable separating family on M covers the complement of the period graph. The argument never separates arbitrary points of Omega and never disintegrates over the measure marginal.

The local density with symmetric compact C is positive on C and has row mass at most one. Its reversal symmetry makes deweighting valid. The Campbell measure is sigma-finite on the displayed countable finite-Q/local-mass-bounded product cover. This checks both the localization and exhaustion steps.

## 3. Period-subgroup kernels

This is the essential additional argument for hidden auxiliary states. The graph of the period subgroup is Borel, so its restricted mass on a relatively compact Borel B is measurable and finite. The normalized restriction, with the stated zero-denominator identity branch, defines a measurable covariant Markov kernel without any measurable Haar selection.

For each fixed measure, restriction of each translated measure to the closed period subgroup is a locally finite invariant measure there. Haar uniqueness therefore applies pointwise. The coefficient can vary between cosets, which is why it is not legitimate simply to use one global coefficient. The proof handles this: on the set E of positive coefficients the normalized jump law is the same restricted Haar probability, while E is invariant under the subgroup. Translation preserves the restricted measure on E; the complement stays fixed. Thus the kernel really preserves the original measure at all starting locations.

Every allowed displacement leaves xi unchanged, so the multiplier w_B is invariant along the kernel. Applying the assumed law invariance to `w_B f` is a nonnegative identity even when its expectation is infinite. This recovers Campbell reversal on each bounded displacement set of the period graph. Inversion preserves Haar because the group is Abelian. The common finite-mass product cover then supplies the full sigma-finite uniqueness step. Together with the preceding lemma, this proves reversal for arbitrary measurable tests on `Omega x G`.

This reasoning remains valid when the image law of xi is not sigma-finite. For example, a countable collection of identical measure-valued fibers can have infinite mass over a single canonical state even though the joint law is sigma-finite. The proof does not invoke a conditional distribution on that marginal.

## 4. Exact Cox construction

Struble's full theorem has the required second-countability hypothesis and yields a compatible proper invariant metric. The union of the two closed pair-distance balls is compact and has finite intensity. Endpoint singletons and the condition that this entire union contain exactly two points imply partner uniqueness even at tied distances. Keeping or rejecting the pair with a symmetric canonical gate preserves this uniqueness. The allocation is an involution, fixes every multiple atom, and preserves the whole counting measure. Translation covariance follows from the invariant metric and the gate transformation.

Measurability can be checked by integrating the pair indicator against the locally finite counting kernel. Its value is either zero or a unit mass at the unique partner. Since G is standard Borel, this unit-mass kernel determines a measurable partner, with the identity branch elsewhere. This is consistent with, and supplies detail for, the author's measurable-sum argument.

After inserting the root and the candidate partner, the pair event holds precisely when the original Poisson measure vanishes on the union of balls. The Poisson Mecke identity consequently gives the claimed off-diagonal density

`1_{t != s} b(theta_s mu,t-s) exp(-mu(U(s,t))) mu(dt)`.

At an atom the void factor includes the masses at both endpoints. Omitting the root atom would give a different and incorrect kernel. The diagonal is excluded and belongs to the holding mass. The finite Poisson-series calculation remains valid with repeated locations; compact exhaustion is justified because partners at distance at most R require information only within the radius-2R compact ball. The allocation definition gives row mass at most one, and symmetric spatial balance proves measure preservation. No Palm property of the unknown candidate law is used in this Poisson calculation.

For canonical sufficiency, all gates needed for off-base-diagonal localization are members of this actual matching family. The density is strictly positive for every distinct pair. On the period graph, reversal fixes the canonical measure and Haar inversion handles the remaining displacement distribution. Deweighting away from zero and the automatic identity at zero yield the full canonical Mecke equation. This proof does not rely on the stronger abstract theorem to assert a smaller test class works.

## 5. Classical implications and exact source coverage

Last–Thorisson (2009), equation (2.7), states the Mecke characterization on the same abstract measurable flow with sigma-finite Q and nonzero covariant locally finite xi. The text explicitly says the proof applies beyond the canonical space. Theorem 6.3 gives Palm equivalence with mass-stationarity; Theorem 4.1 gives the required converse transport invariance. The hypotheses match, including the direction of translation and the negative displacement in reversal.

The full OWR contribution discusses `(xi,zeta+delta_0)` before introducing the Cox transport question for the distribution of xi. The candidate's intensity-background matching is a deterministic allocation of exactly this joint object, and its averaging gives the required invariant preserving transport. I accept this explicit, stated source interpretation. I do not strengthen it to an allocation forbidden from seeing xi. The complete 2011 final paper remains unread because its publisher download was inaccessible, and no theorem or definition from that unavailable text is certified.

The complete 2015 preprint and final publisher discussion distinguish their bounded weighted transports from Markov transports and still identify Problem 7.3 as open at that time. The candidate does not rebrand that older weighted theorem as its result. The OWR short announcement omits some technical framework, while the full 2009 formulation supplies second countability and sigma-finiteness; these are preserved rather than generalized silently.

## 6. Scope of independent controls

The reviewer program uses `Z/2 x Z/2` and `Z/3 x Z/2`, with nonuniform invariant metrics, multiplicities, ties and zero atom masses. It checks exact matching preservation and covariance; the two-insertion/void equivalence; Cox balance as coefficients indexed by the actual exclusion sets; every restricted-subgroup subset B and its zero branch; and full marked-orbit invariance/rank even when several hidden states share one measure. It also records the constant-measure hidden-state countercontrol, emphasizing why replacing the joint law by the canonical law would lose information. These tests supplement the full analytic audit above.

No correction to the frozen author mathematics or packaging is required. Publish only the manifest-bound author files and the portable review files; source PDFs, extracted text, rendered pages and raw imported records are reading material only.
