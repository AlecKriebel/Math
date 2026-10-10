# Independent audit of the frozen five-turn positive-character packet

Date: 2026-10-02 UTC. Target: 30000048 / OWR-722-001. This reviewer did not participate in the positive-character author search. The review was confined to the frozen claims and their dependencies; no additional author attempt to settle the original was performed.

## Verdict

PASS for the precise scoped partial theorems in TURN_1.md through TURN_5.md. I found no mathematical defect requiring a correction. The original unrestricted classification remains EXHAUSTED / UNRESOLVED after 5/5 substantive author turns. There is no full candidate for that original question. This review is not a historical novelty determination and not a proof-assistant certificate.

The strongest retained SU(3) theorem is conditional on a finite Hermitian sum of character-polynomial squares. Its proof does not establish this condition from pointwise positivity and integral Haar mean one. The mean-15 discriminant is correctly presented as an obstruction to an unjustified SOS implication, not a normalized counterexample.

## Frozen inputs and reproducibility

Input directory: the five_turn_packet delivered by the author. SHA-256 of FIVE_TURN_MANIFEST.json: ca6b6d88db566ba4ac0f542996b226471a198638d7af2e7ebd31dfb1d165d443. The packet has 40 manifest-listed files, plus the manifest itself. All 40 sizes and SHA-256 hashes matched. TURN_5.md hash: c178341d7e2e3bdbaf14ca096a6ecbadd38e4a6666a5d5a2efe1083a5cd18ab1.

All five author checkers ran successfully and reproduced their complete saved JSON receipts exactly. I also independently implemented two checks without reusing the author's decomposition routines:

- Re-enumeration of all 19,635 turn-2 coefficient triples at 41 distinct rational real traces, excluding exactly 19,631 and leaving precisely the four stated survivors
- Direct skew-tableau enumeration, rather than character multiplication, for 1,064 diagonal and stable-strip LR instances, including empty-row, endpoint, opposite-order, and near-boundary cases

These finite checks are corroboration. The all-weight and all-r results were reviewed as mathematical arguments rather than extrapolated from finite computations.

## Source and hypothesis audit

I reopened the complete two-page author-hosted Serre 2004 contribution and the final 2025 primary paper. The original question indeed concerns integral virtual complex characters on connected simply connected compact Lie groups, pointwise real nonnegativity, and normalized Haar mean one. Serre's rank-one theorem is already in the 2004 source. The 2025 Problem 4.6 retains the broader connected-group question with a connected finite covering; for simply connected G that covering does not change the group. Its Laurent extremality result in section 5 matches the credited input.

The packet correctly distinguishes this question from positivity of irreducible coefficients, finite-group questions, and the separate prime-power-zero problem. No claimed result here covers arbitrary higher-rank simple groups or mixed products. The source limitation and final status are accurate.

Primary sources checked:

- https://www.college-de-france.fr/media/jean-pierre-serre/UPL8835246706135048784_On_the_values_of_the_characters_of_compact_Lie_groups.pdf
- https://ems.press/content/serial-article-files/50890

## Claim-by-claim audit

### Turn 1: SU(2)^r

The induction is valid. Integrating one SU(2) factor extracts an integral coefficient polynomial and leaves a nonnegative mean-one marginal. The domination lemma is sound: vanishing to second order at every simple real interior root proves divisibility by the full product of squared monic character polynomials; monic division preserves the integral quotient. Parseval on its trace substitution then forces the quotient to be -1, 0 or 1. The nonzero leading Laurent coefficient is therefore exactly plus or minus the marginal square.

At equality, root-of-unity averaging and even zero multiplicity exhaust the degree of the Laurent polynomial. Evaluations at t=1 and t=-1 force the negative sign and even top frequency. This gives one irreducible factor square, including trivial factors and r=0. No assumption about ordinary-character coefficients entered the proof.

### Turn 2: finite center-neutral SU(3) span

The Schur-orthogonality coefficient bounds are necessary for every nonnegative function in the stated span and give the complete integer box. The rational real-trace points are realized by genuine SU(3) diagonal elements. Negative exact evaluations therefore exclude the candidate triples rigorously. The four survivors have the stated exact irreducible-square identities, providing global sufficiency. There is no grid-to-global inference. My independent enumeration reproduced the result.

### Turn 3: full SU(3) height-four span

The fifteen-character triangular polynomial basis, reality condition, and central projection account for the entire support range. The five noncentral conjugate monomial pairs are exhaustive. The unit-circle trace construction has determinant one and covers the entire circle. The stated Jacobians at traces zero and one are nonsingular, so the local positivity arguments really take place inside an open trace set.

For central average 1, the genuine torus constant coefficient remains one and Laurent rigidity applies. For averages x and x^2-y+x, the circle restriction gives the coefficient relations, and the linear/quadratic local tests at zero force the remaining integer parameters to vanish. For average (x-1)^2, positivity of the three central summands makes each vanish on the trace circle; the sign change of x-1 across an interior arc then forces the second factor to vanish there. The ensuing Laurent identity eliminates the remaining parameters. Each case is complete at the stated height cutoff.

### Turn 4: all-weight affine and convex-square families

For a nonzero coefficient in 1+c chi, reality forces the irreducible to be self-dual. The identity evaluation eliminates c<0. The principal-element sine formula gives a strict value below -1 for all self-dual labels a>=3, and the exact trace-3/2 calculation handles a=2. The adjoint example and c=0 are handled correctly.

The diagonal LR formula m_k(a,b)=min(a,b,k,a+b-k)+1 follows from the displayed skew shape and ballot-word convention. The allowed row-2 two-count interval max(0,k-b)<=t<=min(a,k) incorporates all row, column and ballot restrictions. Its zero extension for k>a+b follows from the unique determinant twist having negative last part.

The top diagonal coefficient in a convex combination is positive, at most one, and integral, hence all mass concentrates at one height. Integer threshold differences then concentrate min(a,b), leaving only conjugate labels, whose squares agree. This is valid for arbitrary finite real nonnegative averaging weights, not merely rational ones.

### Turn 5: non-diagonal Hermitian SOS

The leading u^N v^N coefficient is exactly the trace of the highest-height diagonal Gram block. Integrality and total Gram trace one force all other blocks to vanish; PSD forces their off-block rows and columns to vanish too. The leading monomials give integer band sums. Their unit-circle Gram polynomial is nonnegative and has constant coefficient one, so all nonzero-distance band sums vanish. The proof correctly does not infer diagonality from that fact alone.

I independently checked the stable-strip tableau bookkeeping. For a-c=3h>0, the target GL(3) partition has the stated total degree. The overlapping lower columns have length c+2h-k, positive in the strip. Column strictness forces t<=k-2h; the ballot bounds are weaker. The strip hypotheses make all remaining row counts nonnegative, and exactly max(0,k-2h+1) tableaux result. The case h>k has no containing skew shape. Negative differences follow by conjugation symmetry. The diagonal strip coefficient is k+1 except at the two boundary indices, where it is k. My direct tableau checks corroborated this formula independently of the author's character code.

Hence every off-diagonal contribution to the relevant irreducible coefficient is a constant times a vanishing band sum. The coefficient is k+1-w, where w is boundary diagonal mass. Integrality forces w in {0,1}. At w=0, PSD removes the boundary rows; at w=1, only the conjugate boundary pair remains and its lone off-diagonal entry is killed by its band sum. The final one- or two-index middle support, and N=0,1, are handled correctly. The conclusion is equality of the function with one irreducible square, not an unjustified rank-one claim about every Gram representation.

Finally, the discriminant identity, coefficient expansion, mean 15 and formal value -5 at u=v=4 all check. Since the trace image has interior, a purported character-polynomial SOS identity would extend to every formal complex trace. Its negativity at 4 therefore forbids the SOS representation. Dividing by 15 violates integrality, exactly as disclosed.

## Remaining scope and disposition

The partials may be retained with this independent scoped mathematical pass. Do not mark the original 30000048 solved. The missing general positivity-to-SOS implication is not supplied, and the packet establishes no unrestricted SU(3) classification. Historical originality remains a separate literature question. No sixth author search was performed by this review.
