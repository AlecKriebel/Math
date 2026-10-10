# EP-839 / problem 2334: a separated-block obstruction and an endpoint repair

## Status and exact scope

This publication edition records accepted mathematical results and their independent audit. It does not resolve either original question or assert novelty.

Let A = {a_1 < a_2 < ...} be positive integers, with no a_i equal to a consecutive block a_j + ... + a_k for 1 <= j < k < i. The targets are:

1. limsup a_n/n = infinity, equivalently lower natural density zero;
2. H_A(x)/log x -> 0, where H_A(x) = sum_{a in A, a < x} 1/a.

Upper natural density zero and convergence of H_A(x) are different statements. Neither is claimed here. All finite checks below are evidence about the displayed finite constructions, not substitutes for the infinite proofs.

The attempt investigates whether the separated-block construction behind Freud's upper-density example can defeat either target. It cannot: a general bound forces H_A(x) = O(log log x) for this construction architecture. A printed endpoint issue was also found in the stated extension rule. A one-integer endpoint correction is proved sufficient, and the corrected example still has upper density 19/36. Its reciprocal mass is calculated explicitly. The endpoint observation and repair were accepted by the independent audit after a minor T=4 boundary-wording correction to this note. The finite construction and the 19/36 existence result remain intact.

## Sources actually read

- Paul Erdős, *Some forgotten problems*, 1992, printed pp. 42–43 (PDF pp. 9–10), https://hrj.episciences.org/125/pdf. Both pages were text-read and visually inspected. The displayed original questions and the distinct upper-density conjecture were checked against the page images.
- Robert Freud, *Adding Numbers*, James Cook Mathematical Notes, 1993, printed pp. 6199–6202, in https://webhomes.maths.ed.ac.uk/cook/iss_no60.PDF. The complete four-page article was read from PDF spreads 10 right, 11 both, and 12 left, with auxiliary OCR. The extension's endpoint is read from the image, not inferred from OCR.

No current or historical novelty claim is made. SOURCES.json records the historical retrieval and inspection scope. The later Coppersmith–Phillips paper was not needed or represented as inspected. Edition preparation did not add scholarly-source inspection.

## 1. General obstruction for prefix-sum-separated bounded-width blocks

**Theorem 1.** Fix C > 1. Suppose A is a union of nonempty finite blocks B_r, with m_r = min B_r, such that

- B_r is contained in the integer interval [m_r, C m_r];
- m_{r+1} > T_r, where T_r = sum_{a in B_1 union ... union B_r} a.

Then, as x -> infinity,

H_A(x) <= (log C / log 2) log log x + O_C(1).

In particular H_A(x)/log x -> 0. No consecutive-sum avoidance assumption is needed for this theorem.

**Proof.** All blocks are automatically in increasing order. Set h_r = |B_r|. Since m_{r+1} >= T_r+1 and T_r >= T_{r-1}+m_r, induction gives T_r >= 2^r-1 and m_r >= 2^{r-1}. Also

sum_{a in B_r} 1/a <= sum_{n=m_r}^{floor(Cm_r)} 1/n <= log C + 1/m_r.

The sum of the 1/m_r error terms is finite. Discard the finitely many blocks with log m_r < 16; their total contribution is bounded in terms of C only. Write u_r = log m_r for the remaining blocks.

Call a block small if h_r <= m_r/u_r^2. Its reciprocal contribution is at most 1/u_r^2. Because u_r >= (r-1) log 2, all small-block contributions have a bounded total.

For every other block, T_r >= h_r m_r > m_r^2/u_r^2. If u_i and u_{i+1} are the logarithms of the minima of two successive non-small blocks, intervening blocks can only increase the minimum, so

u_{i+1} >= 2u_i - 2 log u_i >= (3/2)u_i,

where the last inequality holds for u_i >= 16. Moreover, using log(1-t) >= -2t for 0 <= t <= 1/2,

log u_{i+1} >= log u_i + log 2 - 2(log u_i)/u_i.

The error sum is bounded uniformly: u_i >= 16(3/2)^{i-1}, and log u/u is decreasing for u > e, so it is dominated by a convergent geometric series times a linear factor. Consequently, the number d of these blocks whose minima are below x satisfies

d <= (log log x)/log 2 + O(1).

Each contributes at most log C plus the already summable 1/m_r error, including a partially present last block. Adding the bounded small-block and initial contributions proves the theorem. ∎

**Lower-density corollary.** Prefix-sum separation alone already forces lower natural density zero, without a width bound: if N_r is the cumulative count, then T_r >= N_r(N_r+1)/2 and the count below m_{r+1} is N_r. Thus N_r/(m_{r+1}-1) <= 2/(N_r+1) -> 0.

This theorem is conditional on a construction's block structure. The avoidance property has **not** been shown to force such a partition. Establishing that implication would be an unjustified leap toward the original question.

## 2. The log-log bound is attained by an admissible construction

This explicit reconstruction illustrates sharpness at C = 2. It is consistent with the log-log lower bound already stated by Erdős; no priority is claimed.

Start with the empty sequence. Given an admissible finite prefix P = (b_1,...,b_N), let T = sum P and m = T+1. Let s_j = b_j+...+b_N be its N positive suffix sums. Append

B(P) = {m,m+1,...,2m-1} minus {m+s_j: 1 <= j <= N}.

For the empty prefix, the suffix set is empty and the first block is {1}.

**Proposition 2.** This procedure gives an infinite admissible sequence. Its lower natural density is zero, its upper natural density is 1/2, and

H_A(x) = log log x + O(1).

**Proof of admissibility.** The suffix sums are distinct and lie in [1,T] = [1,m-1], so exactly N elements of the full block are removed and its first element m survives. Since T >= N, the new block is nonempty. All old-only block sums are at most T < m. Two distinct new terms have sum at least 2m+1, beyond the new block. A consecutive block crossing the old/new boundary and containing exactly one new term must consist of a suffix of P followed by m; its sum m+s_j was removed. These are all possibilities for a forbidden equality in the extended prefix. Induction proves the infinite claim.

Let m_r be the start of the r-th block and N_r,T_r the count and sum after it. The exact count identity is

N_r = N_{r-1} + m_r - N_{r-1} = m_r.

Because any N distinct positive integers sum to at least N(N+1)/2, N_{r-1} = O(sqrt(m_r)). The full block's sum is m_r(3m_r-1)/2, and at most N_{r-1} removed terms each have size less than 2m_r. Thus

m_{r+1} = T_r+1 = (3/2)m_r^2 + O(m_r^{3/2}).

The block's reciprocal mass is

log 2 + O(1/m_r) - sum_j 1/(m_r+s_j)
= log 2 + O(m_r^{-1/2}).

Prefix separation gives m_r >= 2^{r-1}, so these errors are summable. Therefore the reciprocal mass through r complete blocks is r log 2 + O(1). The recurrence for u_r = log m_r has the form u_{r+1} = 2u_r + log(3/2) + o(1). Its inhomogeneous terms are bounded. Also m_{r+1} >= m_r^2 eventually. It follows, by dividing by 2^r and summing the resulting absolutely convergent series, that u_r = kappa 2^r + O(1) for some kappa > 0. Hence log log m_r = r log 2 + O(1). Between m_r and m_{r+1}, both the possible change in H_A and the change in log log x are bounded. This proves the asserted H_A(x) asymptotic for all x, not only at block endpoints.

At x just below m_{r+1}, the count is m_r while m_{r+1} is asymptotic to (3/2)m_r^2, so lower density is zero. For r sufficiently large, the largest new term is 2m_r-3: the two larger candidates are removed by suffix sums T and T-1, whereas T-2 is not a suffix sum because the prefix sums start 0,1,3. Thus the density at these endpoints tends to 1/2. During a block, the count up to a point t is at most N_{r-1} + t-m_r+1; its ratio to t is at most 1/2+o(1) since t <= 2m_r and N_{r-1}=o(m_r). In the gaps the ratio decreases. The upper density is exactly 1/2. ∎

This proves that a log-log upper bound for the specified block architecture cannot be improved to a bounded reciprocal sum.

## 3. Freud's finite construction, restated and checked

For an integer y >= 1 set L = 32y-4 and U = 144y-12 = 4L+16y+4. Freud's choice x = 17y-2 gives the following four ordered blocks:

- A: every integer in [32y-4,36y-4];
- B: integers not divisible by 3 in [48y-5,54y-7];
- C: even integers in [64y-6,72y-10];
- D: every integer in [72y-6,144y-12].

Delete from D the following sets:

- I: 96y-9, 96y-6, ..., 108y-15 (step 3);
- III: 128y-10, 128y-6, ..., 144y-22 (step 4);
- V: {84y-9, 120y-14, 132y-13, 118y-13, 144y-16}.

Call the resulting finite set F_y. The labels I and III follow the two principal deletion categories in the source; V comprises its five boundary sums.

Here is a direct finite verification by cases. Five or more consecutive terms exceed U. Three terms starting in B or a later block already exceed U, since the first three B terms sum to 144y-11. Four terms crossing A/B also exceed U. Pairs within A are odd, lie above B, and below D, so miss C. Triple sums within A coincide with the consecutive pair sums within B and form I. Four-term sums within A coincide with consecutive pair sums within C and form III. The three boundary pairs A/B, B/C, C/D and two A/B boundary triples are exactly V. Pairs within D exceed U. These exhaust all block sums that could be terms. All deleted elements lie strictly inside D, its first element survives, and deleting inside D cannot create a new block sum at most U. Therefore F_y is admissible.

The deletion sets are disjoint, with sizes 4y-1, 4y-2, and 5. Direct summation gives

|F_y| = 76y-7,
sum_{a in F_y} a = 7436y^2 - 1406y + 70.

In particular F_1 is a valid 69-term starting block of total sum 6100. The finite 19/36 asymptotic is unaffected by the issue discussed next.

## 4. A printed endpoint issue in the infinite extension

The printed rule starts with a finite admissible prefix of sum T, sets y = T^2 and x = 17y-2, and deletes four further intervals from its next F_y block. In terms of L = 32y-4, those printed intervals are

J1 = [L+1, L+T],
J2 = [2L+T, 2L+2T+1],
J3 = [3L+2T+3, 3L+3T+3],
J4_printed = [4L+3T+1, 4L+4T+6].

The left endpoint of J4_printed was checked visually on printed p. 6202, PDF spread 12 left. Source pages and images are not reproduced in this edition.

**Proposition 3 (endpoint witness).** For every T >= 4 divisible by 4, this printed rule leaves a forbidden equality inside the new block:

(2L+T-2) + (2L+2T+2) = 4L+3T.

**Proof.** J2 removes the even C terms from 2L+T through 2L+2T. Its immediate surviving C neighbors are exactly the two terms on the left. They are consecutive in the extended sequence; no other block occupies that C interval. Both belong to C, and the right term is below its last element, because y=T^2 and T>=4; when T=4 the left term is C's first element. Their sum z=4L+3T lies in D. It lies above I. It is 0 modulo 4, whereas every III deletion is 2 modulo 4. It is different from the five V values: in particular it lies strictly between 120y-14 and 132y-13, with the other V values outside that interval. It lies above J3 and just one unit below J4_printed. Thus z also survives. ∎

The objection applies to the source's own starting construction: the proved sum polynomial gives sum F_1 = 7436 - 1406 + 70 = 6100, which is at least 4 and divisible by 4. Substitution of T=6100 into the complete symbolic witness above proves applicability without materializing the next block. No seed-size or congruence condition excluding this starting block appears in the complete source article.

The proof above establishes the general mechanism without a finite witness list. The seed boundary T=1 has an additional degeneracy and is not within the correction theorem below.

## 5. A sufficient bounded correction

**Theorem 4.** Given any finite admissible prefix of total sum T >= 3, use y=T^2 and the same F_y, J1, J2, J3, but replace the last interval by

J4_corrected = [4L+3T, 4L+4T+6].

Appending the surviving terms produces an admissible extension. Only one integer has been added to the printed deletion interval.

**Proof.** For T>=3, J1 lies inside A and removes only the T elements after its first element L. J2 lies strictly after C's first element and strictly before its last. J3 and J4_corrected lie inside D and do not touch its first element. The inequalities follow directly from y=T^2 and the displayed endpoints.

The first four new terms are L, L+T+1, L+T+2, L+T+3. A sum involving at least five new terms exceeds U. Within the new block, the only new short consecutive sums introduced by deletions in A are the sums starting at L and using two, three, or four new terms:

2L+T+1, 3L+2T+3, 4L+3T+6.

They lie respectively in J2, J3, J4_corrected. All other short A blocks and the A/B boundary blocks remain unchanged. The C deletion creates exactly one new adjacent pair. Its sum is 4L+3T for even T and 4L+3T+1 for odd T; both belong to J4_corrected. Three C terms already exceed U. The B/C and C/D boundaries are unchanged. Deleting terms in D creates no new short sum at most U because two D terms exceed U and its first term has not changed. Thus all entirely new-block possibilities have been checked.

For a block crossing the old/new boundary, write s in [1,T] for its old suffix sum. With one, two, three, or four new terms, its sum lies respectively in

[L+1,L+T],
[2L+T+2,2L+2T+1],
[3L+2T+4,3L+3T+3],
[4L+3T+7,4L+4T+6].

These are contained in J1, J2, J3, J4_corrected. With five or more new terms the sum exceeds U. Old-only sums are at most T<L and the old prefix was already admissible. This exhausts every case. ∎

Beginning with F_1 satisfies T>=3. Repeating the corrected extension therefore proves the infinite existence claim without relying on the defective endpoint. The correction costs at most one extra integer per stage; it does not alter the density constant.

## 6. Reciprocal mass of the corrected Freud sequence

**Theorem 5.** Starting with F_1 and repeatedly using Theorem 4 with y=T^2 gives an admissible infinite sequence with lower natural density zero, upper natural density 19/36, and

H_A(x) = gamma log log x + O(1),

gamma = [log 2 + (19/12) log(9/8)] / log 4
      = approximately 0.6345239594751639.

In particular this sequence satisfies both original proposed conclusions; it is not a counterexample to either.

**Proof.** For a fixed residue progression of density rho in [alpha y+O(1), beta y+O(1)], summation or integral comparison gives reciprocal mass rho log(beta/alpha)+O(1/y). Applying this to the six principal ranges A, B, C, D, I, III gives

h_F = log(9/8) + (2/3)log(9/8) + (1/2)log(9/8)
      + log 2 - (1/3)log(9/8) - (1/4)log(9/8)
    = log 2 + (19/12)log(9/8).

The five isolated V deletions affect this by O(1/y). The four corrected extra intervals contain at most 4T+10 integers altogether. Each lies at scale y, so their reciprocal cost is O(T/y)=O(y^{-1/2}); their contribution to the ordinary sum is O(Ty)=O(y^{3/2}). Consequently a new block has reciprocal mass h_F+O(y^{-1/2}), and the total prefix sum after adding it is

T_next = 7436 y^2 + O(y^{3/2}).

Thus y_next = T_next^2 = 7436^2 y^4 (1+O(y^{-1/2})), and

log y_next = 4 log y + 2 log 7436 + O(y^{-1/2}).

As in Proposition 2, this implies log log y_r = r log 4 + O(1), and the reciprocal errors are summable. Through r complete new blocks, reciprocal mass is r h_F+O(1). Within each block or the following gap both H_A and gamma log log x vary by bounded amounts. This proves the stated asymptotic for all x.

At the start of a new block, all previous terms have total sum T, hence count at most T, while the new minimum is L=32T^2-4. Lower density is therefore zero. The new block has 76y+O(sqrt y) terms, and all earlier terms contribute only O(sqrt y); its unchanged endpoint is U=144y-12. Endpoint densities tend to 19/36. For completeness, the limiting finite count function at scaled endpoints

32,36,48,54,64,72,96,108,128,144

has respective values

0,4,4,8,8,12,36,44,64,76.

Between those points it is linear, up to a uniformly bounded integer-count error. Its ratio to the argument is maximized at 144, where it is 19/36. Prior terms and additional deletions are o(y); gaps only decrease the density. This proves the exact upper density. ∎

## 7. What was checked, and what remains
The original mathematical checks are historical supplementary evidence, summarized with byte identities and match results in VERIFICATION.json. The independent audit is presented in AUDIT.md. No mathematical program was rerun during preparation of this edition. The infinite and universal claims rest on the written proofs above, not on finite tests or numerical extrapolation.

The exact remaining obstacle is that a general admissible sequence need not have the prefix-sum-separated bounded-width form. This attempt neither proves that arbitrary admissible sequences have lower density zero nor rules out positive logarithmic density by a different construction. It records a sharp obstruction to the tested route and a bounded correction to a prior extension recipe. Both original questions remain unresolved here. No novelty or priority is asserted.

This is AI-assisted, unrefereed work. Acceptance refers to an independent internal AI mathematical audit, not external human peer review, journal acceptance, or proof-assistant certification. The minor T=4 boundary-wording correction to this note is already incorporated; it is distinct from the substantive one-endpoint repair of Freud's printed extension rule.
