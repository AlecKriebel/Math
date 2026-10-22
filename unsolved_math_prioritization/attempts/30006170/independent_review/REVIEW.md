# Independent review: bounded chaining, weak mixing and the remaining separation question

## Verdict

**PASS_CREDITED_FIRST_QUESTION_AND_RETURN_CRITERION; ORIGINAL BUNDLED TARGET UNRESOLVED.** No mandatory mathematical correction was found.

Reviewed `PARTIAL_RESULT.md` SHA-256:
`d1f360b70cf68ace0ea4e306057565cf7bc27c11af65d8b9e9f4abe0355c69cd`.

The reconstruction supplies a valid measure-class-preserving action that is metrically ergodic, hence weakly mixing, but not boundedly chaining. It correctly credits the construction and mechanism to Tserunyan--Zomback's recent preprint, while repairing a local stochastic-matrix adjective with an explicit stationary matrix. The return-set criterion is correct. Neither provides the boundedly-chaining-but-not-one-chaining example requested by the second original question.

Recommended status: **unsolved, 2/5**, retaining the exact terminology, indexing qualification, preprint status and lack of novelty claim. This is separate adversarial AI review, not human peer review or certification of the entire recent preprint.

All **1,035,791 submitted finite assertions** reproduce byte for byte. The independent controls pass **164,453 exact assertions**. Those finite checks do not replace the arbitrary-measurable-set arguments audited below.

## 1. Original quantifiers, indexing and current source

I read the complete relevant contribution and visually inspected printed p.122 of [Oberwolfach Report 2/2025](https://ems.press/content/serial-article-files/51347). Its Theorem 4 explicitly describes unqualified chaining as k-chaining for some single k. Thus the original Questions 5--6 concern the notion called **bounded chaining (BC)** in the 2026 paper. Substituting the newer weaker C property, whose bound depends on A and B, would change the target.

The old definition separately mentions gamma_0 A intersect A without declaring gamma_0 to be the identity. Under a literal freely chosen gamma_0,...,gamma_k reading, it uses one more translate than the newer convention. The submission correctly records this ambiguity rather than silently identifying the two fixed levels. Failure of every finite bound is unaffected by any such shift, so the negative answer to Question 5 is robust. The second question remains unproved under either specified reading.

I also read the relevant definitions, nonsingularization discussion, Lemmas 6.3--6.4, Theorem 5.7 and the full Proposition 6.13 argument in [Tserunyan--Zomback, arXiv:2609.18061v2](https://arxiv.org/abs/2609.18061). The Proposition 6.13 page was visually inspected. The primary version record shows v1 submitted 16 September 2026 and v2 on 17 September; the PDF prints a manuscript date of 21 September. The source record contains no withdrawal notice at this check. These dates do not establish journal publication. Question 1.4 still explicitly asks for nonsingular separations within the global bounded-chaining hierarchy.

Weak mixing is correctly defined by diagonal products with every ergodic pmp action. The submission does not replace it by double ergodicity on the action's own square, which is a different condition in the nonsingular setting.

## 2. The explicit stationary matrix and the local source correction

The stated P is row-stochastic. Direct rational multiplication gives pi P=pi for pi=(1/5,1/5,3/10,3/10). It forbids inverse-letter transitions and aa,AA, while all its advertised cross edges and the loops at b,B have positive weights. P is irreducible; indeed every entry of P squared is at least 1/9. Every pair of columns of P has a common positive predecessor, so P-transpose times P is strictly positive.

Detailed balance pi_i P_ij=pi_j P_ji holds, but P is not symmetric. The source's usual matrix-symmetry adjective is incompatible with the drawn support and row stochasticity: both rows a,A send their full total mass two to b,B. Symmetry would make the reverse cross-flow two, exhausting both b,B rows and leaving zero mass for their positive loops. The submission's correction is therefore explicit and justified. It does not misquote its replacement as the source's actual numerical matrix, or conclude that the intended construction is invalid.

The proof only needs the specified support, positive stationary distribution and common-predecessor property. All hold for the replacement. The needed recurrence can even be made quantitative: from any state, the probability of being at a prescribed state c after two steps is at least 1/9. The probability of avoiding c through 2n further steps is at most (8/9)^n. Thus every prescribed state is visited again almost surely from every starting state, without a countable-state recurrence assumption.

## 3. Nonsingularization and equivalence on the legal section

The mixture over all group translates has total mass one because the coefficients sum to one. A set is null for the mixture exactly when every inverse translate is mu-null. Left translation permutes this null-set condition, proving measure-class preservation in both directions. The positive identity coefficient also implies mu is absolutely continuous with respect to the mixture.

The union of translates of L is conull: for every mixture component g_*mu, that component is concentrated on gL. Hence L is a complete section modulo null sets.

The less immediate assertion is equivalence of the two measures **restricted to L**. I checked the finite-prefix argument carefully. Fix a reduced finite group word g. On the domain where both x and gx are legal, cancellation has one of finitely many lengths, at most |g|. Partition further by the next surviving state. On each resulting piece, the map replaces one finite legal prefix by another, with the identical remaining Markov tail. The ratio of their cylinder probabilities is a fixed positive finite number, since all initial state weights and all used transition weights are positive. Therefore that partial map preserves null sets in both directions. Countably many g and the mixture then prove the claimed equivalence on L.

This reasoning applies to arbitrary null subsets, not merely cylinders: equality of the conditional tail measures first holds on tail cylinders and hence on the generated sigma-algebra. Completion is legitimate because the identity component gives global mu absolute continuity with respect to the mixture, and the partial prefix maps preserve the relevant null ideals. This closes a potential measurability gap in the later use of arbitrary positive E,F inside L.

## 4. Arbitrary measurable-set density and one-step chaining on L

For positive E,F in L, equivalence of restricted measures gives positive mu measures. Some first-letter states s,t satisfy mu_s(E)>epsilon and mu_t(F)>epsilon for a common epsilon>0. The common-predecessor property supplies c with P(c,s),P(c,t)>0.

Cylinder martingale convergence applies to the completed Markov probability space: its finite-coordinate sigma-algebras generate the Borel sigma-algebra modulo completion. It provides a cylinder where E has density greater than 1-delta. By the recurrence established above, partition that cylinder by the first later extension ending at c. This is a countable disjoint partition modulo a null set. Its weighted-average density still exceeds 1-delta, so at least one cylinder wc has that density. This justifies the terminal-state requirement; it is not a density claim inferred from finite enumeration.

Taking delta<epsilon times the smaller of P(c,s),P(c,t), the conditional missing mass in either child cylinder wc s or wc t is less than epsilon. Removing wc by g=(wc)^{-1} converts the conditional law on each such child cylinder exactly to the law conditioned on its first state. Thus mu_s(gE)>1-epsilon and mu_t(gE)>1-epsilon. Intersecting with E and F in the corresponding conditional spaces gives both positive intersections.

The resulting statement is one-step chaining for positive subsets of the particular complete section L. It is not a global one-chaining assertion on the nonsingularized space. Every generator has a positive return to L, as witnessed by a legal cylinder beginning in its inverse followed by an allowed state. These returns generate the whole free group.

## 5. Metric ergodicity and the Hilbert-section argument

I checked both cases in the direct metric-ergodicity proof. Since the group is countable and the action nonsingular, all equivariance identities can be imposed on one common invariant conull set.

If the measurable equivariant map is constant z almost everywhere on L, every positive generator return forces that generator to fix z. Completeness of L then forces the map to be constant on the whole space modulo null sets.

Otherwise its pushforward from L is not a point mass. Separability permits two positive-measure sufficiently small balls U,V with distance between them exceeding diameter(U). Applying the proved one-step chaining to their preimages gives an isometric translate gU intersecting both U and V. Its diameter equals diameter(U), contradicting that strict separation. This works for arbitrary separable metric targets, not only Hilbert spaces.

For weak mixing, the section map x -> indicator(D_x) into L2(Y,nu) is measurable for any invariant measurable D in X times Y, where Y is a standard probability space. One can justify this by approximation with finite sums of measurable rectangles and L2 convergence; separability of L2 then gives the usual measurable version. Invariance of D and Fubini give the Koopman equivariance identities almost everywhere, simultaneously for all group elements after a countable intersection.

Metric ergodicity makes the section map a constant vector. It is an indicator almost everywhere, because almost every section is an indicator. Its Koopman invariance and ergodicity of the pmp Y-action force that indicator to be zero or one almost everywhere. Fubini then gives the same null/conull conclusion for D. No use of double ergodicity or of an unproved stationary distribution for the mixture enters this step.

## 6. Height obstruction under all finite translates

The free-reduction estimate is correct, including both extreme cancellation cases. If g has p initial positive a letters and x is legal, then

\[
\max(0,p-1)\le h(gx)\le p+1.
\]

If a non-a initial letter survives when p=0, the height is zero; if all of g cancels, the surviving legal tail has height at most one. For p>0, a surviving nonempty suffix after the initial a-run fixes the height at p. If that suffix cancels completely, at most one more a can cancel, because the legal word contains no AA. The legal continuation can contribute at most one new positive a, because it contains no aa. These alternatives cover all infinite legal tails.

Thus h has oscillation at most two on each gL. No point of any such translate is the infinite all-a word. Starting from height at most one on L, each nonempty overlap can raise the maximum possible height of the next translate by at most two. The terminal translate of a k-chain therefore has height at most 2k+1 everywhere. The cylinder [a^(2k+2)] is inaccessible, although it has positive mixture measure from the component a^(2k+2)_*mu applied to [b].

The obstruction uses only nonempty intersections, so it certainly excludes positive-measure chains. It works for every finite k and proves failure of BC after nonsingularization. There is no contradiction with a result stated for the original stationary Markov measure: the mixture is a different measure and global chaining need not survive nonsingularization.

The independent checker classifies all possible continuation heights by cancellation-stopping cases for every reduced group word through length seven. It verifies that each case is realized by a legal infinite continuation and checks the same bounds. This supports, but does not replace, the arbitrary-length proof.

## 7. Return-set criterion and the unresolved second question

For a nonsingular action, R_A is symmetric and contains the identity. Applying g^{-1} to the overlap gA intersect hA proves equivalence with g^{-1}h in R_A. Multiplying successive increments gives the forward direction of the return-set formula. Conversely, countability of the union selects one translate with positive intersection with B; factoring its group element into k members of R_A constructs the required chain. Padding by identity elements handles the exact level k.

Therefore k-C is equivalent to conullity of U_k(A) for every positive A. The missing quantifier is still a **single finite k uniform over all positive A**, together with failure at the lower prescribed level. The reconstructed action fails every finite k, so it cannot supply the second question's requested separation. Essential chaining on a fixed complete section and singular examples likewise do not supply it. The source and the submitted package both preserve this gap.

## 8. Reproducibility and final scope

The submitted checker was run in an isolated replay directory with the frozen artifact. It writes its receipt. The result is byte-identical: 1,035,791 assertions, including 344,835 reduced-word/legal-tail pairs.

The independent standard-library checker passes 164,453 exact assertions, including:

- Stationarity, reversibility, support and the explicit two-step recurrence bound
- 46,762 cancellation-stopping cases across 4,373 group words
- 2,666 exact legal-prefix replacement ratios and group identities
- Conditional-density error thresholds and generator-return cylinders
- 9,610 positive-set tests for return products versus actual translate-overlap paths in cyclic and dihedral finite actions

No finite test is described as a proof for arbitrary measurable sets. The complete measurable argument for the first question is audited above. The recent construction remains credited to Tserunyan--Zomback; neither its whole paper nor its other claimed separations are certified here. No author mathematics or public repository state was changed by this reviewer.

Retain the bundled target's **unsolved 2/5** status, the preprint and matrix-correction qualifications, and the old/new fixed-level indexing distinction. The publication files are listed in `review_summary.json`; full third-party sources and redundant replay files are excluded.
