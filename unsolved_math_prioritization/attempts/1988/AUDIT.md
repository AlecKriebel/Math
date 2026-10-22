# Independent mathematical audit: EP-197 / 1988

## Review status and edition

These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” refers only to the corrected partial results in this edition. No external human peer review, journal acceptance, formal proof-assistant certification, novelty or exhaustive worldwide-status determination is claimed.

This is the complete substantive mathematical audit of the original candidate, retained with its two required corrections and historical finite-check account. The distributed PROOF.md already includes both corrections; the unmodified candidate is not accepted as written. Code, finite certificates and detailed test outputs are omitted from this prose-only edition. No new scholarly-source retrieval or inspection was performed during edition preparation.

## Decision and scope

Accept the bounded-deficit interval theorem, its finite-prefix bound, its two-color consequences, and the arbitrary-slow-allowance construction after the two precise domain qualifications in CORRECTIONS.md. The unmodified finite-count statement over all integer n is false because negative starts give empty intervals. The unmodified affine paragraph also overstates infinitude of arbitrary lattice intersections. Neither defect affects the substantive proof for large positive starts.

The requested partition of the positive integers into two 3-permutable sets is unresolved by this work. This audit establishes no novelty or priority claim and makes no claim to have checked the surrounding literature exhaustively. The finite computations below are corroboration, not the proof of any infinite theorem.

During the recorded audit, the candidate was read in full, including its proof, status, source assessment, generator, checker, and exact public inventory. Its 21 authored/check members were authenticated against the recorded inventory hash. The historical sources were freshly retrieved during that audit and their bytes matched the candidate's recorded hashes; details are in SOURCE_METADATA.json.

## 1. Definitions and the order-type distinction

For distinct numerical values x<y<z with x+z=2y, the prohibited positional arrangements are x before y before z and z before y before x. Thus admissibility is exactly the condition that y is earliest or latest among the three. There is no adjacency-of-positions assumption. Both orientations are essential.

Any restriction of an admissible order remains admissible. An infinite subsequence of an omega enumeration remains an omega enumeration: list its increasing original indices, each of which is finite. This is the restriction fact needed in the corrected affine paragraph. An arbitrary infinite linear order is insufficient for the anchor argument, because an anchor could have infinitely many predecessors. Finite admissible orders for arbitrarily large sets do not produce compatible omega enumerations. The candidate correctly avoids both invalid inferences.

## 2. Zigzag and mirror propagation

On a consecutive arithmetic-progression ladder, two adjacent comparisons meeting at an interior rung cannot point successively in the same positional direction, because that rung would then be between its numerical neighbors. Thus the ladder alternates leaders and trailers. Endpoints need only lead or trail their one existing neighbor; no nonexistent neighbor is used.

For an even g and a center c in the opposite half-residue class, a mirror pair c-e,c+e has e congruent to g/2 modulo g. Its two members are separated by 2e congruent to g modulo 2g, so they have opposite ladder phases. Midpoint extremality places both members on the same positional side of c.

Here is a complete check of the propagation, with an inner pair at distance e and an outer pair at e+g, both present:

- If the inner pair follows c, its leader precedes its outward neighbor; transitivity puts that outer member after c, and reflection puts its mate after c.
- If the outer pair follows c, choose the inner trailer. Its outward neighbor is a leader and precedes it, so the inner trailer follows c. Reflection gives its mate.
- If the inner pair precedes c, choose the outer leader. It precedes its inner neighbor and hence c. Reflection gives its mate.
- If the outer pair precedes c, the inner leader precedes its outward neighbor and hence c. Reflection gives its mate.

The admissible distances form an uninterrupted finite progression. These four implications therefore propagate either positional side both inward and outward from any seed. The argument does not depend on which ladder phase holds and works for every positive even g. In particular, the candidate's g=2 and g=4 uses are valid. The interval condition is material: the admissible ordering (1,11,6,5,7) on a punctured set puts the pair 1,11 before center 6 and the pair 5,7 after it. The missing ladder terms prevent the argument; this supplies a negative control against an unwarranted generalization.

## 3. All four C3 cases and endpoints

Write M=8q, q>=2; c=12q, b_i=8q+i, and t_i=16q-i. Every named term is in [8q+1,16q]. The odd class reflects into itself about c: its extreme pair is 8q+1,16q-1. Thus all odds lie on one positional side of c. The odd-ladder leaders are either residue 1 or residue 3 modulo 4, yielding exactly four cases.

For even-class propagation at c+1 or c-1, the seed member c has reflection c+2 or c-2. All are inside the interval. For opposite-odd-class propagation with g=4, the distance-2 seeds are c±1 and their odd neighbors, all inside the interval already when q=2. No extra phase assumption is being smuggled in: the mirror lemma is phase independent.

1. Leaders 3 modulo 4; odds before c. At c+1 the opposite odd class is earlier, giving b_3 before c+1. The even class is later, giving c+1 before t_10. The imposed t_10 before b_3 closes a strict cycle. The two reflected target values are t_1 and b_12.
2. Leaders 3 modulo 4; c before odds. The center c-1 is a leader, giving c-1 before t_3. The even class precedes that center, giving b_6 before c-1. The imposed t_3 before b_6 closes the cycle. The reflected targets are b_1 and t_8.
3. Leaders 1 modulo 4; odds before c. The even flood gives c-1 before t_10, and the imposed t_10 before b_3 gives c-1 before b_3. Reflection in the AP (b_3,c-1,t_5) gives c-1 before t_5, and t_5 before b_5 gives c-1 before b_5. Opposite odd leaders force b_5 before c-1. The reflected targets are b_8, t_5, and t_7.
4. Leaders 1 modulo 4; c before odds. The even flood gives b_6 before c+1; t_3 before b_6 gives t_3 before c+1. Reflection in (b_5,c+1,t_3) gives b_5 before c+1, and t_5 before b_5 gives t_5 before c+1. The center c+1 is an odd leader, so the opposite-class flood forces c+1 before t_5. The reflected targets are t_4, b_5, and b_7.

The g=4 target distances are 4q-2 in cases 1 and 2, and 4q-6 in cases 3 and 4. They are positive and congruent to 2 modulo 4 even at q=2. The smallest listed t_i is t_10=16q-10>=8q+1 for q>=2; the largest listed b_i is b_12=8q+12<=16q. These inequalities verify all listed endpoint memberships globally, not just at sampled scales. Distinctness follows from the positive distances and the explicit nonzero AP differences. This completes an all-M check of the candidate's four-case proof.

Kasel's Theorem 22 has exactly this C3 hypothesis. The candidate's cases 1 and 2 reformulate the two branches of Kasel's Theorem 27 at M divisible by 8, while cases 3 and 4 reformulate Theorem 28. The mirror argument is Kasel's Lemma 26 in a self-contained form. Attribution is appropriate; no source's machine verdict is needed.

## 4. Anchor transplantation and the omega contradiction

For a fixed integer s, the two anchors are s+15,s+16 and the bottom values are s+M+3,s+M+5,s+M+6. At M>=16 all bottom values lie strictly above both anchors. If all three bottom values occur after the later anchor, the three identities

    2(s+M+5)-(s+15)=s+2M-5,
    2(s+M+6)-(s+15)=s+2M-3,
    2(s+M+3)-(s+16)=s+2M-10

force the respective completions before their bottom values. Otherwise anchor, bottom, completion would appear in increasing positional order. All six completion/bottom terms lie in the shifted interval, so restriction and translation give the forbidden C3 order. The possibility of equality of positions is excluded by distinct values. This proves Proposition 5 for both finite orders and omega orders.

Different permitted M differ by at least 8, while a bottom triple has offsets only 3,5,6. Thus those triples are pairwise disjoint and avoid the anchors. For k intervals there are at least k distinct bottom values before the later anchor. Its inclusive prefix also contains both anchors, giving P>=k+2. No assumption that the full intervals are disjoint is required.

For the corrected Theorem 1, infinitely many eligible positive integers n are unbounded. The full intervals have unbounded lengths, so one of them supplies adjacent anchors a,a+1 with a>=C+31. Fix s=a-15>=C+16 once and for all. For every sufficiently large eligible n set M=8 ceil((n-s)/8). Then M>=16 and n-s<=M<=n-s+7. Its lower shifted endpoint is at least n+1, and its upper endpoint satisfies

    s+2M <= 2n-s+14 <= 2n-C-2.

The shifted interval is therefore inside the assumed full interval. The M values become unbounded; repeated n at a common M cannot cause trouble. Arbitrarily many distinct M now force arbitrarily many predecessors of one fixed anchor position, impossible for an omega enumeration. This is the entire infinite proof. Finite certificates and any SAT sweep are irrelevant to its logical validity.

If full intervals [a_j,b_j] with a_j tending to infinity had deficits bounded above along an infinite subsequence, choosing a fixed nonnegative integer C above those deficits would give forbidden full [a_j,2a_j-C] intervals. This proves the deficit formulation including negative deficits. Its converse is immediate by taking those exact intervals. The finite-versus-infinite quantifiers are in the correct order: the threshold may depend on S and C.

## 5. Partition consequences and affine restriction

The same eventual obstruction applies separately to both proposed parts; beyond the maximum of their two thresholds the interval is contained in neither part, hence meets both. For a run [e_j+1,e_{j+1}] and e_{j+1}>=2e_j-K, take n=e_j+1 and any nonnegative integer C>=K+2. Then [n,2n-C] lies in the run. Infinitely many offending runs yield infinitely many in one of the two colors. The endpoint and finite-color arguments are correct.

These conditions do not settle the partition problem. Having both colors in every long consecutive interval is far weaker than admissibly ordering both colors. The affine extension is valid with the exact qualifications in CORRECTIONS.md: use positive inverse coordinates, restrict only an infinite intersection when invoking omega permutability, and dispose of finite intersections directly. The empty-intersection example there shows why the original sentence requires replacement.

## 6. Proposition 7: every prescribed allowance

Let f:N->N be nondecreasing and unbounded. Given the fixed finite m=m_(k-1), eventually f(n)>=2m, so there is an integer L_k>=4m with f(L_k+m)>=2m. This choice is made once per stage and creates one set for the entire given f. The assertion is not a family of unrelated finite examples.

Each B_k consists of k+1 finite nonempty intervals. It lies above m, and m_k=2L_k4^k is its largest value. Thus stages are pairwise disjoint and numerically increasing; their concatenation has only finitely many predecessors for every member.

For a finite integer set choose t with 2^t greater than its numerical diameter and compare its residues modulo 2^t from the least significant bit upward. These residues distinguish the elements, including negative integers if desired. For an AP x,x+d,x+2d, put h=v_2(d)<t. All lower bits agree, and at bit h the endpoints agree while the middle differs. Therefore the middle is before both endpoints or after both. This supplies a complete proof of the finite ordering invoked by the candidate; applying it to the entire B_k, rather than separately to its component intervals, also covers all within-stage cross-interval APs.

For cross-stage APs, let B_k be the latest stage represented and let old terms lie in [1,m]. A progression with two old terms has its third term at most 2m-1, below B_k. With one old term x and two new terms y<z, necessarily x<y<z and z=2y-x. If y is in the jth interval then

    2L_k4^j+m <= z <= 4L_k4^j-1.

This is above that interval and below the next one, or above the last interval. In every case z is outside B_k. These alternatives exhaust APs involving more than one stage. Thus their exclusion is set-theoretic, independent of enumeration. Combined with the internal bit order, the concatenation is admissible of order type omega.

The component lengths are L_k4^j-m+1, so summing gives

    |B_k|=L_k(4^(k+1)-1)/3-(k+1)(m-1).

Divide by m_k=2L_k4^k and use L_k>=4m to obtain the candidate's lower bound

    2/3 - 1/(6*4^k) - (k+1)/(8*4^k).

It tends to 2/3, proving the limsup-density claim. Only a lower bound is claimed; no equality or complement construction is inferred. For the first interval a_k=L_k+m and b_k=2L_k, its deficit is 2m, positive and at most f(a_k). Since m_k>=8m_(k-1)4^k, both a_k and those deficits tend to infinity. This is compatible with Theorem 1 and verifies all quantifiers in Proposition 7.

The mechanism and density count are adapted from Geneson's Section 3. Allowing a larger stage parameter L_k preserves its proof. The candidate's attribution and its refusal to certify novelty are appropriate.

## 7. Zero-based versus positive formulation

Translate both parts of a partition and both enumerations by +1 to move from {0,1,2,...} to {1,2,...}, and by -1 for the reverse direction. Translation preserves coverage, disjointness, all AP equations, bijectivity, and omega order type. If the index domain convention also changes from zero-based to one-based, shift indices by one as well. No assertion about adjoining zero to a fixed part is needed.

Kasel's Remark 3 discusses deletion and adjoining zero and misses this translation equivalence of existence questions. The correction is valid and logically separate from the finite C3 lemma. It does not resolve either equivalent existence question.

## 8. Historically recorded finite checks and negative controls

The recorded independent checker imported no candidate code. It authenticated the original public inventory and external seal, derived allowed branch hypotheses afresh, and replayed 236,283 primitive steps across 160 branches at ten scales. Each edge, hypothesis, parent index, midpoint reflection, transitivity step, and final reverse-edge conflict is checked. Eleven malformed objects are rejected independently. The candidate's own checker was also rerun in normal, -O, and -OO modes, including its twelve malformed controls; its outputs exactly match the saved originals.

Further independent checks comprise:

- Exhaustive admissible-order enumeration for intervals of lengths 1 through 9, with counts 1,2,4,10,20,48,104,282,496. The enumerator is cross-checked against all 5,040 raw permutations at length 7.
- 12,648 mirror-property tests, including even moduli beyond the two used in the proof.
- Explicit admissible C3 witnesses at M=20 and M=28. These demonstrate that dropping the mod-8 hypothesis is invalid; they do not assert a theorem for all other residues.
- 14,322 endpoint/reflection/G4-distance checks across the 1,023 scales M=16,24,...,8192, plus 39,712 anchor/rounding checks and 511 mutually disjoint bottom triples.
- 36 bit-reversal orders, 144 block parameter cases, 1,290,328 one-old/two-new checks, and a fully enumerated two-stage admissible concatenation of 2,615 terms.
- Two exact logarithmic-allowance examples, using integer arithmetic even when the second stage is too large to enumerate.
- A punctured-interval witness showing the mirror lemma needs its interval condition, an untrimmed-block witness (1,8,15) showing the trimming is meaningful, and increasing, decreasing, and nonconsecutive positional-AP controls.

The candidate generator was run only in an isolated temporary copy. All ten gzip certificates and its generation manifest were byte-identical to the candidate. Independent and candidate replay outputs are each identical across normal, -O, and -OO runs. No proof check depends on Python assert statements.

All finite ranges have explicit cutoffs. The all-M C3 proof, the infinite anchor argument, and the infinite slow-allowance construction were assessed mathematically above and do not follow merely from these test counts.
