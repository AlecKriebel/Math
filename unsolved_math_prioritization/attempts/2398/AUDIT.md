# Audit and corrections for prior vertex critical edge resilience results

This edition combines the full correctness-relevant printed correction list, an independent focused review of the repaired conventional proof, and an appropriately scoped report of the separate finite computation. The prior existence theorem is attributed to Ema Skottová and Raphael Steiner; the finite order-sixty graph is attributed to Alex Chan. The lower proof, imported upper-bound dependency, and finite-computation boundary remain distinct. This is unrefereed AI-assisted audit work, without a claim of external human peer review, formal replay, novelty, priority, exhaustive current-literature status, or resolution of k=4,r>=2.

## Part I Local corrections to the audited proof

These repairs refer to the retained Skottová-Steiner arXiv:2508.08703v1 PDF, SHA256 6e4fa149ae6e15dc9b608aac6b1094bb8b2fac5547b8bd5a02f62e6ebd328cb6. Page numbers are printed PDF page numbers. The list concerns correctness-relevant or potentially misleading local statements, not a stylistic copyedit. The theorem statements and parameter thresholds are unchanged.

## Gluing lemma on page 4

- The order sum in the first proof paragraph has upper limit t-1; it must be t, agreeing with the lemma statement and the construction.
- In the transferred removed-edge set, G_i-v means G_i-v_i.
- The last coloring step ranges over all gadget indices i in [1,t] except j, not [1,k-1] except j.
- The displayed containment of B_i in colors [2,k] may be sharpened to [2,k-1]; the broader containment is harmless, since the coloring codomain already has k-1 elements.

## Odd local clique partition on page 10

The printed A = [1,p] intersect ({i,i+1}+2mZ), where p=n_(k,m), does not in general describe starts inside H_i. Replace it by

    A_i = {i+2ma, i+2ma+1 : 0 <= a <= (k-3)/2}.

For 1 <= j <= m use V_j = {v_(a+2(j-1)) : a in A_i}. These sets partition H_i exactly. If x=i+2ma+b with 0 <= b < 2m, its part is V_(floor(b/2)+1), not V_(ceil(b/2)). The final reference to H_1 should read H_i. PROOF.md checks the clique distances and partition directly.

## Block structure on page 12

- In the odd case of Claim 4.7, the summation sentence must keep H_(j+2m), not H_(j+2m+1).
- In the even case, the intervals C_1 and C_2 used for absolute vertex indices must both be translated by j. Equivalently the whole paragraph can use offset coordinates l-j consistently. Mixing offsets and absolute indices is incorrect as printed.
- The concluding containment for the second block is l in t'_c+F, not l in t'_c.

## Missing exceptional-case bridge on pages 13 and 14

Claim 4.8 cites Claim 4.7 in its even case, but Claim 4.7's stated scope excludes k=6,8. Appendix B proves Claim 4.6 for those cases. Add this short consequence before Claim 4.8:

Every expected-color class for even k >= 6 consists, modulo p, of exactly two disjoint blocks t+F. Indeed Claim 4.6 partitions each parity class into monochromatic runs of exactly m entries, and Claim 4.4 gives exactly 2m entries of each color per period. Therefore exactly two such runs have each color. For odd k >= 7 the analogous count is one run.

This supplies the exact assertion needed in Claim 4.8 for k=6,8, without using Claim 4.8 to prove it and without circularity. To choose full blocks inside the period window used there, note that the first two positions of that window are among the neighbors already forbidden for the missing color. Thus a color block cannot wrap across that window boundary.

On page 14 the later restatement of T_1 must retain the earlier lower endpoint i_0-2m+1, not i_0-2m+2. T_1 has 2m entries, one representative of each residue modulo 2m.

## First deviation argument on pages 14 and 15

- The sentence asserting agreement on S' must say agreement on S; agreement on S' is what remains to be proved.
- The upper endpoint of T_2 is t_0+2m-1, not t_2+2m-1 (there is no defined t_2 here).
- In the k=5 parity argument, interchange x and y first to ensure x<y. Then the two relevant positive odd differences y-x and x+4m-y sum to 4m, so one is less than 2m. This makes the short-edge inference explicit.

## Even vertex deletion coloring on pages 19 and 20

The expansion of B_0=p+1-A'_0 has wrong terminal terms, followed by the false congruence 2(k-2)m+1 = 1 mod p. The correct un-reduced expression is

    B_0 = {3,5,...,2m-1} union {p-2m+3,p-2m+5,...,p+1}.

Reducing modulo p gives

    B'_0 = {1,3,...,2m-1} union {p-2m+3,p-2m+5,...,p-1}.

The congruence used is p+1 = 1 mod p. With these terms, the inclusion in the three permitted residue intervals is correct; the resulting exclusion of D_2 and D_3 is unchanged. The direct residue proof in PROOF.md avoids relying on the misprinted expansion.

## Exceptional even cases on pages 22 and 24

- Subclaim B.3's printed congruence -2m+1 = (k-4)m+1 mod p is false. The required exclusion follows instead because -2m+1 is the negative of 2m-1, and 2m-1 belongs to D_1. Subclaim B.1 allows both signs. No new edge is required.
- At the start of page 24, the interval of non-starting positions must end at t_i-2, not t_i. The equality chain is false at the starting point itself. If t_i=t_(i-1)+2 the chain is empty, and its needed equality is the identity at t_i-2=t_(i-1). Equation (13) then follows in every case.
- The sentence t_0 not in T is correct only for the finite list T={t_1,...,t_s}; it need not exclude t_0 from T+2mZ. The argument does not require that stronger exclusion.

## Supplementary Proposition 5.1 on page 16

Before choosing a longest path in G[W], handle W empty. If v is universal and w is any other vertex, a proper three-coloring of G-w uses v's color only at v. Restoring w creates at most one edge of that color, contrary to r >= 1 resilience. Hence W is nonempty and the longest-path argument applies. The proposition's degree, connectivity, and order bounds are unchanged.

## Disposition

The false displayed formulas above are not accepted literally. Their explicitly repaired versions yield the same claimed results. All dependencies needed for k >= 5 lower bounds close under the repaired argument. The independently checked k=4 example is separate and is not used to repair the conventional proof.

## Part II Focused independent review of the repaired proof

### Independent audit of the repaired vertex critical graph proof

Date: 11 October 2026. Problem identifier: 2398 / EP944.

## Decision and exact scope

**ACCEPT.** The repaired proof in Sections 2–13 of the pre-edition proof report, reproduced in PROOF.md, establishes the Skottová–Steiner lower construction for every integer k >= 5 and r >= 1, including the progression-order statement, the all-sufficiently-large-orders statement, the square-root subsequence bound, and the cube-root all-orders bound. Every material repair listed in the pre-edition corrections report, preserved in Part I, is valid. No further mathematical correction or hold is required for those repaired statements.

This is an independent logical audit of an existing proof in Ema Skottová and Raphael Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1. It is neither a new proof of the unresolved every-r assertion at k=4 nor a claim of a new solution of all of EP944. The separate finite Chan graph, its data, searches, and Lean material are outside this focused audit. Nothing here establishes any k=4, r>=2 construction.

Section 14's upper-bound implication is accepted with precisely the stated external input: Conlon–Fox Lemma 8.1, whose proof is expressly omitted in the inspected source. That input is not used in the lower proof. Section 15's necessary conditions at k=4 are accepted with its added empty-nonneighbor-set case.

Acceptance concerns the repaired formulas and arguments, not the false formulas literally printed in the original manuscript. The paper's theorem hypotheses and numerical bounds survive unchanged.

## Audited inputs and method

The two central pre-edition authored inputs are the proof report, 29,468 bytes, SHA256 f71ac8ecc15bc5dbb2e23f9049e7fe985422aeb1eed073b955799ff3d1ecb984, and corrections report, 5,520 bytes, SHA256 4c507c28fc2c96f046ca46a3394074427f5da35b74621025a20baf1c19bb8e66. Both were read completely. The mathematical dependencies were then checked against the retained primary manuscript, including both appendices.

The Skottová–Steiner PDF has 716,221 bytes and SHA256 6e4fa149ae6e15dc9b608aac6b1094bb8b2fac5547b8bd5a02f62e6ebd328cb6. The Conlon–Fox PDF has 583,703 bytes and SHA256 6a8b97133f7b90e8463892eef6ff5bc08cae788c58b7bdf90b8481cb85ff1aff. Fresh layout-preserving text extraction from each retained PDF reproduced its retained text extract byte for byte. The main manuscript's text was inspected throughout the construction, global proof, gluing, quantitative deduction, and appendices. Original page images 10, 12, 14, 19, 20, 22, and 24 were visually inspected for the important printed formulas. Conlon–Fox pages 56 and 57 were visually inspected; its regularity definition on page 1 was checked in the PDF text.

The primary audit inventory was independently authenticated at 2026-10-11T01:02:20.149121+00:00: all 97 listed members matched both byte count and SHA256. Its manifest hash is 2f42c7e526b5b7a113c2c267a2de65e2de61a083338fdfb0d6c22e78e529a96f. Authenticating a member's bytes is not a claim of reviewing its mathematical or executable content. No inherited verifier, author program, candidate program, downloaded script, certificate replay, or Lean project was executed or imported.

The proof below is universal and written. An independently authored endpoint checker supplied finite corroboration of formulas, not a replacement for universal reasoning. The checks and provenance are recorded separately. The original sealed audit was not altered.

## Construction and puncture coloring

Write p=(k-1)m for odd k and p=2(k-1)m for even k; N=qp+1; F={0,2,...,2m-2}. The assumptions k>=5, r>=1, m>18r+2, q>=24r+12, and 4 dividing q are used as stated. In particular p is even, L=qp/4 is integral, q>=36, and every listed distance is positive and below N/2. The maximum of the shifted D2 or D3 intervals is at most qp/2-2m+1. Thus the definition gives a simple circulant graph, invariant under cyclic shifts and reversal, with its distance-one spanning cycle intact before edge removals.

The formulas for the puncture coloring really partition positions 1,...,p. For odd k they are the alternating pairs (1,2), (3,4), ..., (k-2,k-1) in successive rows of 2m positions. For even k the row pairs advance by two modulo k-1; because k-1 is odd, their k-1 rows cover every color twice, once in each of its prescribed blocks. All start-plus-F positions are within 1,...,p. Repeating the pattern q times colors exactly the vertices other than 0.

For odd k, a same-color forward difference is bp+delta, with delta in F-F. It is even, excluding D1, and its residue avoids [2m,p-2m+1], excluding D2. The reverse distance is N-(j-i), with residue 1-delta, which still avoids that D2 interval. Since the two period indices lie in 0,...,q-1, the reverse distance is at least p-2m+3>2m-1. This last inequality is needed: a statement just about residues would not exclude a short reverse D1 edge.

For even k, start differences modulo p belong to {0,(k-2)m+1,km-1}. Adding F-F gives the set A used in the repaired proof. Its nonzero central pieces are odd progressions with endpoints [(k-4)m+3,km-1] and [(k-2)m+1,(k+2)m-3]. Actual cyclic distances have residues in A union (1-A). This union is contained in

    [0,2m-1] union [(k-4)m+3,(k+2)m-2] union [p-2m+2,p-1].

These intervals avoid both D2 and D3 residue intervals. Forward differences in D1 are excluded by the parity of the short residues of A. Reverse differences are at least p+1-(km-1)-(2m-2)=(k-4)m+4>2m. Thus every puncture coloring is proper, including all wraparound edges. Cyclic symmetry supplies the coloring for every deleted vertex. No theorem of Jensen is needed.

The replacement of Appendix A's B0 formulas is exact. Reducing F-F to A0' gives two even progressions. Subtracting those from p+1 gives precisely

    {3,5,...,2m-1} union {p-2m+3,p-2m+5,...,p+1}.

Its reduction modulo p has 1 instead of p+1. The printed terminal expression 2(k-2)m+1 is not p+1 and is not congruent to 1 modulo p. The repaired proof does not rely on that false congruence.

## Unaffected windows and local balance

Assume a proper (k-1)-coloring phi after at most r edge deletions, and let S consist of positions 1,...,3p, all unaffected. Every edge with at least one endpoint in S survives; the local proofs use only such edges.

For odd k, the corrected parts of H_i are

    {i+2ma+epsilon+2(j-1): 0<=a<=(k-3)/2, epsilon in {0,1}}, 1<=j<=m.

Every position in H_i has a unique representation i+2ma+b with 0<=b<2m. Its part is floor(b/2)+1, and epsilon is b modulo 2. This proves the partition for every i, not just i=1. The distances inside a part are 1, 2m-1, or between 2m and (k-3)m+1. Each part is therefore a (k-1)-clique. Every color occurs exactly m times in H_i. The original fixed [1,p] intersection and ceiling index are genuinely wrong; the replacement fixes both.

For even k, take the first occurrence j of a color in H_i. The forbidden forward distances put all its occurrences inside the union of the five 2m-blocks starting at

    j+{0,(k-4)m,(k-2)m,km,(2k-4)m}.

Using this slightly enlarged candidate set is legitimate. If its forward translate exceeds 3p, then j>2p+1. The last occurrence ell is at least j, and the backward candidate set from ell is contained in S: its lower endpoint ell-(p-1) is positive and its upper endpoint ell is at most 3p. All earlier occurrences of this color in H_i remain within that backward set. Thus the reflection does not assume that the same chosen endpoint works in both directions.

For each l=0,...,m-1, take offsets 2l and 2l+1 from each of the five starts. These ten-point sets partition the enlarged candidate set. The five successive pair-to-pair gaps around the cycle are (k-4)m, 2m, 2m, (k-4)m, and (2k-4)m, up to direction. Their differences with -1,0,1 belong to D. At k=6 the low endpoint 2m-1 belongs to D1, so no endpoint exception occurs. Each pair is itself an edge. The resulting graph contains C5[K2]; an independent set takes at most one vertex in a pair and at most two pair positions on the five-cycle. Hence a color occurs at most twice in each ten-point set and at most 2m times in H_i. Total cardinality forces equality for all k-1 colors.

Equal color counts in H_i and H_(i+1) imply phi(i)=phi(i+p). This defines the periodic expected pattern psi. The lifting rule used later is valid: every distance in D has a representative in D intersect [1,p-1], and representatives of the two residues can be placed on opposite sides of a point in [p+1,2p], all inside S. Both signs of a forbidden difference are allowed.

## Ordinary blocks and change points

For odd k>=7, the m occurrences of a color in H_(j+2m) are restricted to j+[p-2m+2,p+2m-1]. This is an absolute-index interval of length 4m-2. Inside it, any same-color difference must be even and at most 2m-2: D1 excludes short odd differences and D2 excludes all differences from 2m through the interval's maximal difference 4m-3. Exactly m points therefore fill one t+F block. The window stays H_(j+2m); the printed H_(j+2m+1) is not interchangeable in that sentence.

For even k>=10 the relevant absolute intervals are

    j+[(k-4)m+3,(k+2)m-2],
    j+[(2k-4)m+2,2km-1].

The first has 6m-4 positions and the second 4m-2 positions. Each has fewer than 6m positions. Since (k-4)m>=6m, D1 and D2 again force same-color differences in either interval to be even and at most 2m-2. Each interval holds at most m occurrences, and the total 2m forces m in each, hence a full t+F block in each. Translating both intervals by j is indispensable; the source's unshifted intervals cannot support its statement about the absolute indices. The second conclusion must be t'_c+F, not t'_c alone.

A change point at i is a change from psi(i-2) to psi(i). The block descriptions imply that any such i is a block start, and that there is no other change point of the same parity less than 2m later. Independently, psi(x) differs from psi(x+2m) by the lifting rule, so every m-step parity interval contains a change. Together these facts force exactly one change-point residue modulo 2m on each parity. This closes Claim 4.6 for odd k>=7 and even k>=10 without using Claim 4.8.

## Appendix B and its noncircular exceptional cases

For k=6,8, work modulo p. A ring R_i has k-1 classes spaced by 2m; Q_i=R_i union R_(i+1). The following dependency chain is complete and does not use the later nearby-vertex two-option claim.

1. From a class x in the first ring, the only possible same-color companions in Q_x are at offsets (k-2)m, (k-2)m+1, km, km+1. Every other nonzero offset in Q_x is excluded by D1, D2, or D3. The four candidates are pairwise adjacent: their positive differences are 1, 2m-1, 2m, or 2m+1. If a color appears only in the second ring, use the same observation in Q_(i+1); its two same-ring possible companions differ by 2m. Thus every color appears at most twice in Q_i, and counting gives exactly twice.

2. Suppose psi(i) differs from both psi(i-2) and psi(i+2m-2). Equality of the color counts in Q_(i-2) and Q_(i-1) forces that color to occur at some x in R_(i-2). After the forbidden differences and the two assumed exclusions, i-x is 2+(k-2)m or 2+km modulo p. The other occurrence y in Q_(i-2) belongs to the four-companion list. Hence i-y belongs to {-2m+1,-2m+2,1,2,2m+1,2m+2} modulo p. Differences -2m+2 and 2 are ruled out by the assumed exclusions. Differences 1, 2m+1, and 2m+2 are forbidden. Finally -2m+1 is the negative of the forbidden distance 2m-1. This is the correct repair; the source's claimed positive congruence is false. It follows that psi(i) is always one of psi(i-2), psi(i+2m-2).

3. If one point of a ring changes and the next at distance 2m does not, the preceding two-option statement forces their colors equal, contrary to the forbidden 2m difference. A mixed ring would contain such a transition when traversed cyclically. Thus a ring is entirely changing or entirely non-changing.

4. If two classes in one ring have the same color, interchange them if needed to arrange j-i=(k-2)m modulo p. Given equal colors c at i+2l-2 and j+2l-2, the point z=j+2l-2m differs from the first by (k-4)m+2, a forbidden distance. Its color is not c. Its two options from step 2 are psi(z-2) and psi(j+2l-2)=c, so it does not change. Step 3 makes the whole ring through z non-changing; that ring includes i+2l and j+2l. Induction keeps their color c, and at l=m contradicts the forbidden difference 2m. Each ring consequently has every color exactly once.

5. On parity x in {0,1}, list the changes t_1<...<t_s in x+{2,4,...,2m}, and put t_0=x. At least one exists. Non-change propagation from t_(i-1) ends at t_i-2, not at t_i. Together with step 2 at t_i, this gives, for every integer a,

       psi(t_i+2ma)=psi(t_(i-1)+2m(a+1)).

   When successive changes are distance 2 apart, the intervening propagation is the identity, so that boundary case is included. Iterating gives psi(t_i)=psi(x+2mi). Step 4 makes these colors indexed distinctly modulo k-1. Since the color after the final change persists through x+2m, s=1 modulo k-1. If s>1 then s>=k. The color psi(x+1) appears somewhere on R_x, say at x+2mj with 1<=j<=k-1. The formula would give it at t_j, but t_j-(x+1) is an odd distance from 1 to 2m-1. This contradicts D1. Thus s=1. Together with step 3, this proves Claim 4.6 for k=6,8.

The endpoint correction in step 5 is necessary because a change-point equality with its predecessor is false by definition. The notation t_0 not in the finite list T is harmless; the proof does not require t_0 not in its periodic extension.

## The exact two-block bridge and translated window

Claim 4.6 partitions each parity into maximal runs of exactly m entries, each a t+F block. Over one period, local balance gives 2m occurrences of each color when k is even. Each complete run contributes m occurrences. Therefore each color has exactly two disjoint runs modulo p. This applies to k=6,8 using Appendix B and supplies precisely the statement absent from the original invocation of Claim 4.7 in Claim 4.8. It is not circular: local balance and Appendix B precede and do not depend on Claim 4.8.

For odd k, the unaffected clique through i_0,i_0-1 and their shifts by -2m,-4m,...,-(k-3)m contains all k-1 colors. Every member except those two is adjacent to a vertex i>3p through D2. This proves the two-option claim for all odd k>=5, including k=5 without a change-point argument.

For even k and i_0 in [p+1,2p] with i=i_0+q'p, the stated neighboring offsets come from D2 at period q' and D3 at period q'-1. The domain 3p<i<=qp/2 ensures both period indices are nonnegative and at most q/2-1. All those neighbors lie in S and their ordinary distances are the actual cyclic distances. Thus no removed edge can defeat these exclusions.

Set a=i_0-(k-4)m-2. The first two positions of the p-window [a,a+p-1] are forbidden for a color absent from the tested neighbors. A parity run crossing either boundary of the window would, directly or after a p-translation, occupy one of these two positions. Therefore each of that color's two runs is represented by a complete block inside this window. This justifies the full-block choice without silently assuming a compatible window cut.

The allowed support inside the window consists of offsets [-2m+1,2m-2] and [(k-4)m+2,(k+2)m-3]. The forbidden gap between them contains at least three consecutive positions even when k=6. A step-two block therefore cannot jump the gap. Subtracting its span 2m-2 from the allowed interval endpoints restricts its starts to

    T1=i_0+[-2m+1,0],
    T2=i_0+[(k-4)m+2,km-1].

Two same-parity starts differ by a positive multiple of 2m, with 2m itself forbidden. If their difference is odd and below 4m, the second start has absolute odd distance at most 2m+1 from the first block's last point. Every such distance is forbidden by D1 or D2. Hence any two starts differ by at least 4m. T1 has span 2m-1 and T2 span 4m-3, so one start lies in each.

T1 has exactly one representative of each residue modulo 2m. Its possible change-point starts are precisely those of the parity blocks containing i_0 and i_0-1. Thus an absent color must be psi(i_0) or psi(i_0-1), proving phi(i) belongs to {psi(i),psi(i-1)}. Replacing T1's lower endpoint by i_0-2m+2 would lose a required representative; retaining +1 is the correct repair.

## First deviation and deletion budget

In any 2m-position interval, more than 2r occurrences of one actual color force a single parity. Otherwise a majority parity supplies at least r+1 vertices and every vertex of the opposite parity is adjacent to all of them through D1. Deleting at most r edges cannot remove all these same-color adjacencies. This is about phi, not psi.

The reduction to a one-sided extension is valid. Split a target containing S into its left and right extensions, use reversal for the left, and choose a 3p core ending or starting at the appropriate end of S. The one-sided target can be enlarged to L positions. Pairs on opposite outer sides have separation greater than p, so no omitted cross-side periodicity equality is needed. Since L+p<N/2, every auxiliary position used below stays inside the domain of the two-option and parity arguments.

At the first deviation i+1, minimality gives phi(i)=psi(i), and the two-option claim gives phi(i+1)=psi(i)=c. Agreement is only assumed on S and before that first deviation, not on all of S'.

For k>=6 choose the change point t_0 of i's parity in [i-2m+1,i], and the next change point t_1 of the other parity. Because i-t_0 is even and at most 2m-2, W=[t_0,t_0+2m-1] contains both i and i+1. On i's parity all expected colors in W are c. On the other parity they are c_1 before t_1 and c_2 afterward. These two colors differ by definition of change, and both differ from c by a neighboring forbidden distance, including when t_1 is the first position of its parity in W.

The intervals [t_0+1,t_1-1] and [t_1,t_0+2m-1] have total length 2m-1, so one contains m consecutive positions with only options {c,c_j}. Since c occurs on both parities of W, it occurs at most 2r times there. The m-position interval consequently has at least m-2r occurrences of c_j. The inequalities m-2r>m/2+1 and m-2r>2r force both parities and more than 2r occurrences of c_j in W, a contradiction. Applying the parity lemma to W resolves the original proof's imprecise invocation on the smaller m-position interval. The printed undefined t_2 endpoint must be t_0.

For k=5, the p=4m-periodic expected coloring has fixed parity for every color. For opposite-parity x<y in a period, the positive odd differences y-x and x+4m-y sum to 4m, so one lies in D1. Unaffected representatives force their colors different. Balance supplies exactly two colors on each parity.

The count in the repaired k=5 argument is correct including both boundary losses. The windows SL=[i-2m+2,i+1] and SR=[i-1,i+2m-2] each have 2m positions and each has at most 2r actual c's. Their union has 4m-3 positions, hence at least m-3 expected c's. In SL, the deviating i+1 is an extra actual c, so at most 2r-1 expected c's occur there. Restoring the expected c at the overlap point i shows that SR has at least m-2r-1 expected c positions, all of i's parity.

Among these positions, at most 2r-1 retain actual c, and at most 2r-1 have actual color c_1=psi(i-1): the extra opposite-parity actual occurrence at i+1 or i-1 respectively would otherwise violate the parity lemma. Thus at least m-6r+1 have the other opposite-parity color c_2. Each has a predecessor in SR of expected color c_2.

Expected c positions and their successors give at least 2(m-2r-1)-1 positions with c as an option, losing at most the last successor. Expected c_2 positions and their successors give at least 2(m-6r+1) positions with c_2 as an option, with no loss because SR ends on the c parity. Inclusion-exclusion inside SR gives at least 2m-16r-1 positions with both options. At most 2r actually use c, so at least 2m-18r-1 use c_2. This exceeds m+1 and 2r under m>18r+2; both parities occur and the parity lemma is contradicted. No first deviation exists in either case.

## Global contradiction and progression orders

An L=qp/4 interval contains at most 2r affected vertices, leaving at most 2r+1 unaffected gaps. The largest gap has size at least

    (L-2r)/(2r+1) = q p/(8r+4) - 2r/(2r+1) > 3p-1.

The strict last inequality holds even at q=24r+12. Its integer size is at least 3p, so partial periodicity applies to every L interval. There is an unaffected vertex because N>2r. Label it 0. Its distance-one edge to N-1 survives. Each consecutive pair 0,p,2p,...,qp lies in an L interval because p+1<=L, so all these vertices have equal color. As qp=N-1, the surviving edge has equal endpoint colors. This proves the resilience assertion for every deletion set of size at most r. Together with the puncture coloring it proves chromatic number exactly k and vertex-criticality exactly as defined.

For A=8(k-1)(18r+3), n-1=Ax, and x>=6r+3, set m=18r+3 and q=8x for odd k or q=4x for even k. Then qp+1=n, 4 divides q, and q>=24r+12. This proves the stated congruence-class existence theorem. Taking x=6r+3 gives an infinite increasing sequence n_r=Theta_k(r^2), with f_k(n_r)>=r and hence the square-root subsequence bound.

## Gluing and every sufficiently large order

The gluing construction preserves simplicity because the gadgets are disjoint outside their designated terminals, and each attachment joins a scaffold vertex to a vertex in its own gadget. It has h+sum from i=1 to t of (n_i-1) vertices. All t edges, not t-1, contribute a gadget.

In any putative (k-1)-coloring of the glued graph after at most r removals, some scaffold edge has equal endpoint colors. Reinsert its gadget's deleted vertex using that common color. Every removed attachment edge corresponds to exactly one original incident edge; internal removed edges remain internal. The two neighbor classes partition the original neighborhood, so this transfer adds no duplicated obligation and needs at most the original r removals. It contradicts the gadget's resilience.

With distinct terminal colors, a gadget is colorable by first assigning its terminals colors 2 and 1, respectively, in the chosen puncture coloring and then permuting the palette. Deleting a scaffold vertex permits a coloring of the remaining scaffold and this extension across every gadget, supplying an arbitrary distinct auxiliary color at a missing terminal before discarding it. Deleting a vertex inside gadget j permits a coloring of H-e_j; its endpoints necessarily have equal colors, while all other scaffold edges have distinct endpoint colors. The puncture coloring of G_j at the deleted internal vertex can be permuted so that its original attachment vertex has their common color. Every other gadget extends via the distinct-terminal rule. The range must be all i in [1,t] except j. Thus neither edge resilience nor vertex-criticality is lost.

The auxiliary sparse-scaffold facts are also closed. An odd wheel is 4-critical. Deleting a spoke can be colored by giving the hub and that spoke's rim endpoint the third color and alternately coloring the remaining rim path with two colors; the other vertex and edge deletions are immediate path or odd-cycle cases. A Hajós join of two k-critical graphs is not (k-1)-colorable because both deleted-edge inputs would force equal terminal colors and therefore violate the new edge. Deleting an internal edge or a nonterminal vertex gives a coloring with distinct terminals on that side, matched to an equal-terminal coloring of the other deleted-edge input. Deleting an outer terminal removes the new edge. Deleting the identified terminal allows the two puncture colorings to be permuted so the new edge's endpoints differ. Deleting the new edge uses equal-terminal colorings on both sides. These cases give edge- and vertex-criticality and the upper chromatic bound.

The wheel of order n-3 joined to K4 gives a 4-critical scaffold of odd order n>=7 with 2(n-4)+5<2n edges. Even-order wheels supply the other orders. Adding a universal vertex preserves criticality: for a newly deleted incident edge, color the old puncture and give its deleted endpoint and the universal vertex one common new color. The remaining deletion cases follow from old criticality. Repeating gives, for every h>=k+3, a k-critical scaffold with at most (k-2)h edges.

For any n>=A[2(k-2)A(6r+3)+2], write h=A+(n modulo A) and x=(n-h)/A. Then A<=h<2A and h>=k+3. For a scaffold with t<=(k-2)h edges,

    x > n/A-2 >= 2(k-2)A(6r+3) > (k-2)h(6r+3) >= t(6r+3).

An integer x at least t(6r+3) can be split into t integers each at least 6r+3, for example by assigning the minimum to t-1 of them and the remainder to the last. The resulting progression-order gadgets glue to exact order h+Ax=n. For fixed k, the threshold is bounded by a constant depending on k times r^3, and choosing r of order n^(1/3) proves the all-orders lower bound. This is the needed fixed-k, unbounded-r quantifier order; the argument does not merely give large k for each fixed r.

## Separate upper bound and supplementary case

Conlon–Fox Lemma 8.1 has the exact regularity convention used in the repaired proof: one interval (alpha,alpha+epsilon) contains the density of every sufficiently large subpair. Its partition bound is 2^(epsilon^(-C)), and page 57 says its proof is omitted. With epsilon=(log n)^(-1/C), the number of parts is at most n^(log 2)<n, so a largest part X has at least two vertices. A largest color class in X minus a deleted vertex has size at least (|X|-1)/(k-1)>=epsilon|X| once epsilon<1/[2(k-1)].

For a paired set Y with density at most epsilon, averaging degrees gives expected contribution at most epsilon|Y|. For density above epsilon, regularity has alpha>0. A color-1 class of size at least epsilon|Y| would have positive density to the color-1 class in X, contrary to proper coloring. This remains true if X and Y overlap: their color-class subsets omit the punctured vertex and their common color forbids all edges, with no loops in a simple graph. Summing the contributions over the Y partition gives epsilon n, and deleting the corresponding incident edges lets the puncture color extend. The implication is correct and separate from every lower-proof dependency. No independent proof of the external regularity theorem is claimed.

For Proposition 5.1, the crossing-edge expectation gives every nontrivial cut at least 3r+3 edges. In the maximum-degree argument, the additional W empty case is essential to a fully explicit proof: if v is universal, in a 3-coloring of G-w its color appears only at v. Restoring w in that color leaves exactly one monochromatic edge, impossible for r>=1. Hence W is nonempty. For each w in W, restoring it in v's color forces at least r+1 neighbors of that color, all in W and independent. An endpoint of a longest path in G[W] has all its neighbors on the remaining path, which has at most 2r vertices and independence number at most r. This contradiction proves the maximum degree bound and, with the minimum degree, order at least 5r+6. These are necessary conditions only.

## Computational corroboration and final boundary

During the focused audit, an independently authored checker ran successfully in normal Python and Python -OO without importing any inherited program. Its 48 construction cases use k=5,...,16, m in {21,22,39,40}, and q=36, valid for r=1. It checked 254,724 same-color puncture distances, 38,160 two-option attachment edges, 72 odd clique partitions, 480 prescribed C5[K2] cross-pair edges, 24 repaired B0 expansions, and eight exceptional Appendix B residue cases. It also checked all 1,024 subsets of the abstract ten-vertex C5[K2] for independence number two and 6,000 integer boundary cases for the all-orders decomposition. Both incorrect printed congruences were detected as false in the relevant test cases. These checks support endpoint arithmetic; the preceding arguments, not those finite samples, establish the universal claims.

The acceptance boundary is therefore precise: the repaired conventional lower proof closes for all k>=5 and all r>=1; its two quantitative lower bounds follow; the upper-bound implication uses the identified Conlon–Fox theorem; the supplementary k=4 statement supplies necessary conditions. The separate Chan computation is neither repeated nor used as a dependency. No residual-family existence, full EP944 solution, novelty, or current-literature completeness is claimed.

## Primary references

- E. Skottová and R. Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1, 12 August 2025. https://arxiv.org/abs/2508.08703v1 and https://arxiv.org/pdf/2508.08703v1
- D. Conlon and J. Fox, *Bounds for graph regularity and removal lemmas*, Geometric and Functional Analysis 22 (2012), 1191–1256. Primary author-hosted manuscript: https://www.its.caltech.edu/~dconlon/RegRem.pdf, especially the page 1 convention, Lemma 8.1 on page 56, and the omission notice on page 57.

## Part III Independent audit of the order sixty graph

## Object and source identity

The target is the graph in alexgocardinal/dirac-critical-graph at the fixed commit 697307af42505b11490fdc74c04eda5c7ec76c51, not a moving default branch. The edge-list bytes have length 1020, Git blob 7602fbdee784a3b8bea0ac3f8cd85d8a4cb252f8, and SHA256 85914250312a4fe8d1a67d747fea2ee1772c9762796af90095efa61fb4c0400c. The puncture-coloring witness has length 120 and SHA256 b89a814e7bffc4a891c78cd511d719573aad437a7dbd8c203e2a57c292ebcf7e.

The source defines a right Cayley graph on a semidirect product of order 60 with six generators, closed under inversion. The historical independent verifier reconstructed the graph from that definition. This publication edition omits the coordinate encoding, multiplication data, generator list, edge list, coloring assignments, and certificate contents. The public source URLs and byte identities in SOURCES.json identify the audited object without distributing those data.

The verifier reconstructs all directed generator incidences and checks that they have no loops and are symmetric. Its resulting set of 180 undirected edges matches the frozen raw list exactly. It explicitly checks that every vertex has degree 6. This rules out a discrepancy between the report's algebraic graph and the input being colored.

## Positive witnesses and symmetry

Only the edge list and a 60-position puncture-coloring row are read as author data. They are not executable. The row records one deleted vertex and assigns three colors to all remaining vertices. Every remaining edge is checked for different endpoint colors.

For each of the 60 left multiplications, the program explicitly verifies a permutation of all vertices and equality of the entire transported edge set. It transports the puncture row through those verified permutations and checks every transported witness directly. Thus each of the 60 vertex-deleted graphs is three-colorable, independently of trusting an unchecked group-automorphism assertion. Assigning a fourth color to the deleted vertex supplies an explicitly checked proper four-coloring of the full graph.

## First exact noncolorability search

The DSATUR-style recursion starts with an empty partial coloring. At each node it chooses an uncolored vertex with the greatest number of distinct already used neighbor colors, breaking ties by residual degree and then label. It branches over each allowed already used color and, if fewer than three colors have been used, one new color. This is complete: all still-unused color names are interchangeable, and the vertex-choice rule depends on equality patterns, not on their names. Renaming an arbitrary full coloring in order of its first encountered colors gives a branch preserved by the search. A branch terminates only at a complete coloring or when all legal assignments fail. There is no timeout, heuristic rejection, floating point, external solver, memoization assumption, or untrusted search certificate.

Verified left translations partition the edges into four disjoint orbits. Deleting a representative is exhaustive for its orbit because each permutation preserves adjacency and therefore transports colorings bijectively. The four orbit sizes and exact recursive node counts are:

- Orbit 1: 60 edges, 1230 nodes
- Orbit 2: 60 edges, 1464 nodes
- Orbit 3: 30 edges, 1207 nodes
- Orbit 4: 30 edges, 1219 nodes

The representative labels are omitted with the raw graph data.

Each search terminates without a three-coloring. The orbit sizes sum to 180 and their verified union is the entire edge set.

## Second exact noncolorability search

The second recursion uses a copy-on-branch array of available color masks. It chooses a vertex with smallest domain, breaking ties by static degree and label, branches over every available color 0,1,2, and removes that color from the domains of its unassigned neighbors. A zero domain rejects the branch. This is standard complete forward checking: the only removed choices conflict with an already assigned adjacent vertex. It uses neither the first routine's color quotient nor its dynamic vertex ordering, and no graph-orbit quotient.

It directly solves all 181 instances consisting of G and G-e for each of the 180 separate edges. All return noncolorability, with 1,651,066 total recursion nodes. Full per-instance node counts were retained in the historical computation receipts; this edition publishes only aggregate verification metadata. Separate positive runs found proper three-colorings of one vertex puncture and of the graph with one particular pair of edges removed. Their raw assignments and edge labels are omitted.

Both routines were tested on every labeled graph on one through five vertices for two and three colors. Their decisions were compared with direct iteration over every color assignment, and returned positive witnesses were checked. This gives 2,198 tests per routine. All target computations and controls were repeated in normal, -O, and -OO Python. No validation is implemented with assert, so optimized execution cannot silently remove a gate.

## Mathematical consequences and exact scope

The proper four-coloring and non-three-colorability imply chi(G)=4. All vertex deletions have chromatic number at most 3. None can be two-colorable, since restoring the removed vertex with a third color would contradict chi(G)=4. Hence every vertex deletion has chromatic number exactly 3.

Every edge deletion has chromatic number at least 4 by the exact searches, and at most 4 by restricting the full graph's coloring. This proves the one-edge immunity assertion. It also implies that every proper three-coloring of any vertex puncture uses each color at least twice in that vertex's neighborhood: otherwise restoring that vertex with an absent or uniquely occurring neighbor color gives a three-coloring after deleting at most one edge. Since the neighborhood has six vertices, every such coloring has the exact 2+2+2 split. This consequence requires no separate replay of the author's balanced-puncture certificates.

One extension of the checked puncture witness has exactly two monochromatic edges. Thus its three-color defect is at most 2. The preceding immunity assertion makes it at least 2. The exact defect is 2. The source manifest mentions a different two-edge witness; different color extensions can give different pairs, so this is not a contradiction. The accepted pair is the one directly checked by the independent verifier. Neither pair nor the coloring assignments are distributed in this prose edition.

The result establishes k=4,r=1. It does not establish any (4,r)-graph for r>=2, let alone one for every r. Nor does it establish the stronger fixed-order divergence statement.

## Static inspection of the Lean semantics

In the structured route, FinGraph contains a Boolean adjacency relation with symmetry and looplessness. ProperExcept excludes precisely edges incident to the deleted vertex. ProperAfterEdge ignores both orientations of one specified edge. KVertexCritical at k=4 means a four-coloring, no three-coloring, and a three-coloring of every vertex puncture. EdgeImmuneAtFour quantifies over every actual edge and rules out a three-coloring after deleting it. These definitions match the intended finite simple graph claim; the exact chromatic numbers of punctures follow as above.

The generic theorem TwoPerColourAtPunctures implies immunity by considering the color of an endpoint of the deleted edge. Two distinct neighbors have that color, and at least one connecting edge survives. The structured checker Valid recursively requires an active unassigned branch vertex and a valid child for each compatible color. A closed leaf is False; such a leaf is allowed only behind an incompatible branch. Its generic soundness argument extends any hypothetical full coloring along its compatible branch and derives a contradiction. The inspected mathematical mechanism is sound.

The actual 21 certificate instances are certified in source using native_decide. The author-supplied final axiom report contains Lean.ofReduceBool. The compact route instead uses bv_decide for its universal negative Boolean claims, while positive witness checks and concrete edge-table checks use native_decide. Static inspection distinguishes these two routes; it does not independently reproduce either Lean compilation or a final axiom trace. Generated certificate trees were not needed or fetched, and no author replay script was executed.

The all-k UniversalDecoupling theorem in both projects is explicitly parameterized by orderFour, jensenGeFive, and lowChromaticObstruction, over an abstract graph type and abstract predicates. Its short proof supplies only the k=4 versus k>=5 logical split. This is not a proof of Jensen's theorem, nor an end-to-end formalization of the universal graph classification. In particular, the absence of sorryAx in a conditional theorem cannot establish its input hypotheses.

## Status limits

The historical audit accepts the finite graph properties at the disclosed independent exact-computation boundary. This prose-only publication does not include the executable searches, graph data, or coloring and search certificates needed to reproduce that finite verification. Its finite acceptance therefore rests on the authenticated historical searches described here, not on a self-contained conventional proof of finite noncolorability. The conventional k>=5 proof in PROOF.md does not use this computation. It does not certify the original toolchain, binaries, external-build logs, reported 35,967-node certificate replay, normalized-coloring count, full automorphism group, girth, diameter, cut-classification claims, or external peer-review status. Those ancillary claims are unnecessary to the accepted result. The source's public statement that external reproduction and peer review were pending is recorded as its stated status, not updated by assumption.

No attribution to the contents of an uninspected NBER manuscript is made. The graph and formal-source audit are anchored to the fixed GitHub commit and retained primary report.
