# Final independent scoped review: SIRSN traffic, 9700031

2026-10-02. **PASS_FULL_FIVE_TURN_SCOPED_PACKET**, no mandatory mathematical revision. **Original remains unsolved5/5.** The ordinary-assumption interval3<beta<4 is not settled, and no valid SIRSN counterexample is constructed. The final result and scope limitations are accurate.

## Binding and evidence

Final author manifest SHA256 47bf7a3e79e2e4234240707f458ca489efeaec9d31a47c8b2fcfdf4ed2589bac binds36 files, all verified. Every author checker replayed byte-exact, totaling99,203 assertions. Historical proof files remain unchanged.

Previously issued independent reviews are preserved byte-for-byte in prior_turn1/ and prior_turns23/. They bind the original proof versions and explain the full source/JM qualification and critical-band argument. The final review rechecked their applicability to the current bundle; their verdicts do not substitute for the new turn4/5 audit below. Fresh independent final controls supplement the earlier133,334 and8,224 controls. Counts are finite algebra/bookkeeping evidence, not a formal continuum proof.

The exact later proof hashes are:
- TURN_4.md: bf15adecef685b3683b90e177fa4120bb8386a7a17d12f9ce24c8b70afd9731a
- TURN_5.md: 7c6eb00142154982edf1a64cc53357b3ba80a96b75f99e7f2f9613f21d5c54a0

## Source and earlier three turns

Aldous2012 Problem31 is renumbered Problem5 in the published2014 §8.3. The expected object weights prescribed routes by the endpoint density|x−y|^(−beta); the major-road cutoff is endpoint distance, not road speed. Source pages and definitions were checked in the earlier bound reviews, including the primary2014 paper https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf .

Turn1's moment criterion and turn2's additional confinement-modulus criterion pass under explicit JM. Turn3's critical beta3 theorem passes under JM and ordinary first moments: all fixed road-size bands have finite equal means, while only finitely many sufficiently large bands occur in each bounded window almost surely. Thus cutoff traffic is finite almost surely despite infinite expectation, and its positive subunit moments are finite. The planted-route covariance argument, random-size cutoff, fractional tails and positive intrinsic-mark expectation identity were checked. No positive intrinsic-mark moment follows automatically from these arguments.

## Turn4: sampled completion

**Technical assumption is explicit.** CS supplies a standard measurable countable sampled-network realization, consistent measurable kernels for finitely many extra endpoints and Euclidean covariance. It does not assert a jointly measurable deterministic route for all continuum endpoint pairs. The source discusses such sampling and intrinsic major-road extensions, but the candidate does not silently claim a fully formal version theorem from arbitrary bare FDDs.

**Exchangeable conditional averages.** On the canonical marked-array/background probability space, finite permutations preserve the law and leave the background fixed. Averaging mu12 over permutations of the firstn labels is exactly its conditional expectation on the invariant sigma-field. These sigma-fields decrease withn. The reverse martingale theorem applies to the integrable mass of any bounded test set, giving almost-sure and L¹ limits. This avoids incorrectly treating dependent pair observations as independent samples.

**Random measures and restrictions.** Conditional expectation of a locally finite random measure with finite expected bounded-window mass can be constructed on a countable determining ring and patched across bounded windows, or by normalizing with a strictly positive spatial weight of finite expected total mass. Its conditional mean is a genuine locally finite Borel measure. Vague convergence follows from a countable dense family of compactly supported tests plus local mass bounds. An invariant-background measurable road set can be inserted in the conditional integral; restriction therefore commutes. This proves coherence on overlaps of band families, rather than only separate convergence of unrelated band totals.

**Integrability without a continuum map.** Importance weights cancel the endpoint sampling density in the expectation. The fixed-pair kernels and sampled roads suffice for the earlier planted-route mass transport and scaling computation, so beta3 band mean is2*pi*|A|*d*log2. No pathwise continuum integral is presumed. All bands can use the same endpoint array and invariant sigma-field. The sampled-road point-set cutoff makes the number of active bands finite in a bounded window for every sample size, so the finite-sum passage to whole-cutoff traffic is justified. Under the extra positive-mark moment the direct whole-cutoff argument at beta>3 is also valid.

**Independence of sampling density.** The mixture/thinning coupling is correct. Conditional on locations and the route array, endpoint labels are independent with the indicated probabilities, because labels do not enter the route kernel. The factor4 produces the correct conditional mean. After truncating the q-weighted pair contributions and excluding label probabilities smaller thanepsilon, the terms are bounded. Only pair-pairs sharing a label contribute conditional covariance, and their number isO(n³), against normalizationO(n⁴). Thus the difference vanishes inL² for each truncation. Removing the truncations is justified by the finite band expectation: the expected discarded weighted contribution equals the corresponding integrable endpoint integral and tends to zero. The random retained-sample normalization tends to its deterministic half-density limit. The two already almost-sure limits must consequently agree. This proves density independence jointly with the background, without bounded original importance ratios.

**Covariance and JM agreement.** Transformed endpoint densities remain positive, so the density-independence result transfers spatial covariance. The endpoint/length/kernel factors give exactlyc^(5−beta) before converting to the push-forward lawc^(beta−5). For a JM realization, the conditional iid U-statistic strong law identifies each band limit with the intended integral; unconditional finite band expectation ensures conditional integrability almost surely. The finite-band assembly then yields whole-cutoff agreement at beta3. None of this constructs a deterministic route map in the CS-only setting.

## Turn5: mandatory cuts and scalar obstruction

**Critical separation lemma.** A nonconstant indicator on connectedR² has a nonzero distributional derivative against some compactly supported smooth test function; otherwise mollification would make it constant almost everywhere. The translation Taylor expansion is valid with a uniformO(t²) remainder, bounded by a compactly supported Hessian integral. Directional integration of the absolute linear term is4|v|t. It lower-bounds the integrated translation symmetric difference byct. Polar integration against|z|^(−3) then contains the divergent integral dt/t. The conclusion is valid for arbitrary measurable nontrivial partitions, without assuming a smooth boundary or finite perimeter, and already diverges at arbitrarily small separations.

**Mandatory-cut hypothesis is strong and precisely stated.** The joint measurability and integrated inequality(4) make the road/endpoint exceptional sets compatible with Tonelli. Applying the separation lemma for length-almost every cut point would force infinite critical traffic whenever the indicated cut-road set had positive length inside a cutoff window. The critical local-finiteness theorem excludes this, and countable road/window exhaustion gives the stated zero-length conclusion. This is not an impossibility theorem for every tree-like network or every abstract bottleneck; the two positive-area populations and measurable integrated usage domination are essential.

**Heavy scalar mark profile.** The proposed probabilities are positive with a legitimate residual atom. Their firstD moment is less than2. SettingS=D² yields divergent E[D*S^alpha] for everyalpha>0, with the stated geometric-subsequence proof. Its dyadic partition identity holds pointwise in the mark and then under Tonelli. The two claimed scalar inequalities follow in the separate casesK<=sqrt(u) andK>sqrt(u), as written. The profile therefore obstructs deductions based only on those scalar estimates.

The profile is not an embedded, consistent, Euclidean invariant route family with verified SIRSN road intensity. The author explicitly states this. It is not a counterexample to the original question, and divergence of the annealed mark moment is not a proof of almost-sure traffic divergence.

## Final assessment

All retained scoped theorems pass. The final author summary accurately separates:
- extra-moment and extra-confinement full-interval results;
- the ordinary-moment beta3 theorem under JM;
- the CS sampled traffic completion and its agreement when JM exists;
- the mandatory positive-area-cut restriction;
- the scalar limitation of the available estimates;
- the unresolved ordinary-assumption beta>3 interval and stronger deterministic-route version issue.

The five substantive author turns are exhausted; the review is not a sixth search. Proposed final repository disposition remains **unsolved5/5**, with the critical theorem highlighted only in its proven scope. No novelty, human peer review, formal certification, universal finite-expectation assertion or valid full-target counterexample is claimed. Earlier review artifacts and author files are preserved unchanged.
