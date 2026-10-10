# A bounded-deficit interval obstruction for 3-AP-free omega permutations

## Status and exact scope

This is a partial obstruction, not a solution of the two-set problem. No claim of novelty is made. The finite ordering lemma below is Kasel's C3 lemma [K, Theorem 22]; it is proved here in a self-contained four-case form after checking the relevant manuscript argument. The contribution of this note is its explicit transplantation to arbitrary bounded-deficit doubling intervals, together with a quantitative finite-prefix consequence. No computational result is a dependency of the infinite theorem.

Write N = {1,2,...}. A set S is **3-permutable** if it has a bijective enumeration p:N -> S such that there are no positions i<j<k with p(i)+p(k)=2p(j). Terms are distinct, so this excludes both increasing and decreasing three-term arithmetic progressions at arbitrary subsequence positions. The enumeration must have order type omega. A finite set is called admissibly orderable with the analogous finite definition.

## Main result

**Theorem 1 (bounded-deficit interval obstruction).** If S is 3-permutable, then for every fixed integer C >= 0 there are only finitely many positive integers n such that

    [n, 2n-C] intersect Z is a subset of S.

Equivalently: for every C, all sufficiently large n have at least one missing point of S in that interval. In particular, if [a_j,b_j] are full integer intervals contained in S with a_j tending to infinity, then 2a_j-b_j tends to +infinity.

The final statement is about full consecutive intervals. It makes no assertion about sets of large density inside those intervals.

**Corollary 2 (two colors).** In any putative two-set solution N=A disjoint-union B, for every fixed C and all sufficiently large n, the interval [n,2n-C] meets both A and B.

Consequently no partition into alternating consecutive runs with endpoints e_j tending to infinity and e_{j+1} >= 2e_j-K for a fixed K can solve the problem. This includes arbitrary uniformly bounded additive perturbations of dyadic switch locations. More generally, even infinitely many monochromatic runs [n_j,m_j] with bounded-above deficits 2n_j-m_j already rule out a solution.

Proof of the endpoint example: the run [e_j+1,e_{j+1}] contains [n,2n-(K+2)], where n=e_j+1. If necessary replace K+2 by a larger nonnegative integer. At least one color contains infinitely many such runs. Apply Theorem 1. The broader assertion follows by the same finite-color pigeonhole argument.

## Finite order tools

An admissible order, denoted by <_p, has the **midpoint-extremal property**: whenever x<y<z numerically and x+z=2y, y is either before both endpoints or after both endpoints in <_p. This is equivalent to excluding both monotone orientations, not just the increasing orientation.

On a finite arithmetic progression w_0,...,w_t, comparisons of consecutive terms therefore zigzag. Exactly one parity of indices leads its existing neighbors, and the other parity trails its neighbors (when t>=1). Indeed, the orientation of the first edge determines the second because w_1 must be extremal on (w_0,w_1,w_2), and induction determines all consecutive comparisons.

**Lemma 3 (mirror propagation; cf. [K, Lemmas 23-26]).** Let I be an integer interval with an admissible order. Let g be a positive even integer, and let C_r be one residue class r modulo g in I. Suppose c is in I and c is congruent to r+g/2 modulo g. Consider all pairs c-e,c+e in C_r intersect I, where e>0 is congruent to g/2 modulo g. If such pairs exist, then either all their members precede c or all their members follow c.

Proof. The C_r ladder has one of its two zigzag phases. For every mirror pair, its two members differ by 2e, which is g modulo 2g, so one is a ladder leader and the other a trailer. The midpoint-extremal property puts both on the same side of c in position order.

Take two successive admissible distances e and e+g. On either numerical side of c, the corresponding ladder terms are neighbors, so their leader/trailer roles switch.

- If c precedes both members at distance e, choose the leader at distance e. It precedes its outward neighbor at e+g. Transitivity and then reflection about c put the whole outer pair after c. Conversely, choose the trailer at e: its outward neighbor is a leader. If the outer pair is after c, this leader followed by the inner trailer puts the whole inner pair after c.
- If both members at distance e precede c, choose a leader in the outer pair. It precedes its inner neighbor, hence precedes c; reflection puts the whole outer pair before c. Conversely, an inner leader precedes its outward neighbor, so an outer pair before c puts the whole inner pair before c.

The admissible distances form an uninterrupted finite progression of step g. Propagation from any one pair reaches every pair. The proof works in either ladder phase. This proves the lemma. QED.

We use g=2 and g=4 only. All applications below include explicit mirror-membership checks.

**Lemma 4 (Kasel's finite C3 obstruction).** Let M>=16 be divisible by 8, let I={M+1,...,2M}, and set b_i=M+i and t_i=2M-i. There is no admissible order of I satisfying

    t_5 <_p b_5,     t_3 <_p b_6,     t_10 <_p b_3.                 (C3)

Proof. Put c=3M/2. Because 8 divides M, c is 0 modulo 4. The odd-number ladder has one of two phases: its leaders are 1 modulo 4 or 3 modulo 4. By Lemma 3 at center c with g=2 and the odd class, either all odd values in I precede c or all follow c: every odd value has its reflection in I. These give four exhaustive cases.

Throughout, use Lemma 3 at c-1 or c+1 with the even class to compare that center uniformly with all available mirror-paired even values. Its seed is the already-known comparison with c, at distance 1. For g=4, use the odd residue class opposite the center modulo 4. The seed at distance 2 is supplied by the phase of the odd ladder; both c-1 and c+1 and their distance-2 odd neighbors lie in I.

1. Leaders are 3 modulo 4; all odds precede c. At center c+1, the class-3 odd neighbors precede the center. The g=4 propagation therefore gives b_3 <_p c+1. Even propagation gives c+1 <_p t_10. The last relation in (C3) closes a cycle:

       b_3 <_p c+1 <_p t_10 <_p b_3.

   The necessary reflections are 2(c+1)-b_3=t_1 and 2(c+1)-t_10=b_12.

2. Leaders are 3 modulo 4; c precedes all odds. The center c-1 is itself an odd leader. Its g=4 propagation gives c-1 <_p t_3, while even propagation gives b_6 <_p c-1. The middle relation in (C3) closes

       c-1 <_p t_3 <_p b_6 <_p c-1.

   The reflections are 2(c-1)-t_3=b_1 and 2(c-1)-b_6=t_8.

3. Leaders are 1 modulo 4; all odds precede c. Even propagation gives c-1 <_p t_10. By (C3), c-1 <_p b_3. The AP (b_3,c-1,t_5) therefore gives c-1 <_p t_5, and (C3) gives c-1 <_p b_5. But the class-1 odd neighbors of c-1 lead that center, so g=4 propagation gives b_5 <_p c-1, a contradiction.

   The reflections needed for these steps are 2(c-1)-t_10=b_8, 2(c-1)-b_3=t_5, and 2(c-1)-b_5=t_7.

4. Leaders are 1 modulo 4; c precedes all odds. Even propagation gives b_6 <_p c+1. By (C3), t_3 <_p c+1. The AP (b_5,c+1,t_3) gives b_5 <_p c+1, and (C3) then gives t_5 <_p c+1. But c+1 is an odd leader, and its g=4 propagation gives c+1 <_p t_5, a contradiction.

   The reflections are 2(c+1)-b_6=t_4, 2(c+1)-t_3=b_5, and 2(c+1)-t_5=b_7.

Every listed b_i or t_i lies in I for M>=16. In cases 3 and 4 the relevant g=4 distance is M/2-6, which is positive and 2 modulo 4; in cases 1 and 2 it is M/2-2, also positive and 2 modulo 4. All explicit APs are nondegenerate for M>=16. The four cases are impossible, proving the lemma. QED.

This proof is an attributed reformulation of the finite lemma, not a novelty claim about it. Unlike an empirical SAT sweep, it covers every multiple of 8 without a cutoff.

## Transplantation and prefix pressure

**Proposition 5 (three compulsory early values).** Let s be an integer, M>=16 a multiple of 8, and suppose S contains the two anchors s+15,s+16 and the complete interval

    I_{s,M}={s+M+1,...,s+2M}.

In any admissible omega enumeration of S, at least one of

    s+M+3, s+M+5, s+M+6                                 (the bottom triple)

occurs before the later-placed anchor. The same statement holds for any admissible finite ordering containing these values.

Proof. Write P=max(pos(s+15),pos(s+16)). Suppose all three bottom values occur after P. Since

    2(s+M+5)-(s+15)=s+2M-5,
    2(s+M+6)-(s+15)=s+2M-3,
    2(s+M+3)-(s+16)=s+2M-10,

each completion must precede its corresponding bottom value; otherwise the anchor, bottom, completion are an increasing 3-AP in position order. Restrict the order to I_{s,M} and translate by -s. The resulting admissible order satisfies (C3), contrary to Lemma 4. The bottom values differ from both anchors, so their positions cannot equal P. QED.

**Corollary 6 (quantitative finite-prefix bound).** If a finite set contains the two anchors and k such intervals for distinct multiples M_1,...,M_k of 8, all at least 16, then every admissible ordering has

    max(pos(s+15),pos(s+16)) >= k+2.

Proof. Different M_i differ by at least 8, while each bottom triple uses only offsets 3,5,6. The k compulsory early bottom values are therefore distinct and differ from both anchors. The first P positions contain these k values and the two anchors. QED.

## Proof of Theorem 1

Suppose, to the contrary, that [n,2n-C] is contained in S for unbounded n. The intervals have unbounded length and location, so S contains a fixed adjacent pair a,a+1 with a>=C+31. Set s=a-15, so s>=C+16 and these two values are s+15,s+16.

For each sufficiently large eligible n define

    M=8 ceil((n-s)/8).

Then M is divisible by 8, eventually M>=16, and

    n-s <= M <= n-s+7.

Consequently every integer in I_{s,M} is at least n, and

    s+2M <= 2n-s+14 <= 2n-C-2 < 2n-C.

Thus I_{s,M} is a subset of [n,2n-C], hence of S. As n tends to infinity these multiples M are unbounded, so there are arbitrarily many distinct ones. Proposition 5 supplies distinct elements before a fixed anchor position, or equivalently Corollary 6 forces that finite position to be arbitrarily large. This is impossible in an omega enumeration. QED.

For the equivalent interval-deficit formulation: if 2a_j-b_j did not tend to +infinity, some fixed nonnegative integer C would bound it above on an infinite subsequence, so [a_j,2a_j-C] would be contained in S there. Conversely, any infinite family of intervals in Theorem 1 violates the deficit formulation.

## Affine extension and limits

For fixed integers d>=1 and r, put T={t in N : r+dt belongs to S}. If T is infinite, retain from an admissible omega enumeration of S just the values in r+dN, and apply the inverse affine map x -> (x-r)/d. The resulting enumeration of T has order type omega and preserves every 3-AP equation. If T is finite, the eventual interval conclusion is immediate. Hence, for every fixed C>=0 and all sufficiently large positive integers n, the set {r+dt : n<=t<=2n-C} is not a subset of S. Taking positive coordinates handles arbitrary r; any finitely many nonpositive values of r+dt can be discarded without changing this eventual conclusion. No infinite intersection with an arbitrary residue class is assumed.

The theorem does not rule out unbounded trimming. The blocks in Geneson's construction [G, equations (3.3)-(3.5)] are [L_k 4^j+M_{k-1},2L_k4^j]. Their deficits 2a-b are 2M_{k-1}, which tend to infinity with the stage; there are only finitely many blocks per stage. They therefore do not violate the theorem. No assertion about the exact maximal consecutive runs is needed here.

Corollary 2 alone does not solve the partition problem: ordinary parity coloring already makes every sufficiently long consecutive interval meet both colors, while each parity class is nonpermutable because it contains a whole infinite arithmetic progression. The affine extension detects that example, but we do not prove that every two-coloring violates one of these necessary conditions.

No upper-density bound has been established here. In particular, [G] gives alpha_N(3)>=2/3, so the older conjecture alpha_N(3)=1/2 must not be used. Arbitrary finite admissible orders and arbitrary infinite linear orders are insufficient: the contradiction above specifically uses a finite position for each anchor in an omega enumeration.

## Sharpness with respect to a prescribed divergence rate

The bounded-deficit conclusion cannot be replaced by a universal prescribed rate of divergence. The following is an adaptation of the block construction in [G, Section 3], not a claim to have discovered that construction.

**Proposition 7 (arbitrarily slow allowed deficit).** Given any nondecreasing unbounded function f:N -> N, there is a 3-permutable S with upper natural density at least 2/3 and infinitely many complete intervals [a_j,b_j] contained in S, with a_j tending to infinity, such that

    0 < 2a_j-b_j <= f(a_j).

Moreover the deficits in this construction tend to infinity, as Theorem 1 requires.

Proof. Start with m_0=1 and S_0 empty. For k>=1, having defined m_{k-1}=m, choose an integer L_k>=4m so large that f(L_k+m)>=2m. This is possible because f is unbounded and nondecreasing. Define the finite block

    B_k = union over j=0,...,k of [L_k 4^j+m, 2L_k 4^j] intersect Z,
    m_k = 2L_k 4^k,
    S_k = S_{k-1} union B_k,
    S = union over k>=1 of B_k.

Every finite integer set has an admissible order: choose enough binary digits to distinguish all its elements and sort by the digits from least significant to most significant. For an AP of difference d, the lowest nonzero binary digit of d makes the middle term differ from both endpoints at the first relevant comparison bit. It is therefore before both endpoints or after both. Apply this finite ordering to each B_k and concatenate the resulting finite orders.

There is no set-theoretic AP meeting both S_{k-1} and B_k. Indeed S_{k-1} is contained in [1,m], and B_k lies above L_k+m>3m. An AP with two old terms has its prospective last term at most 2m-1. For one old term x and two new terms y<z, if y lies in the jth displayed interval, then

    z=2y-x lies in [2L_k 4^j+m, 4L_k 4^j-1].

This is strictly above that interval and strictly below the next one, or above the final interval. Thus z is not in B_k. Taking the latest stage of any purported cross-stage AP proves there are none. The concatenation is an omega enumeration, since the blocks are finite, nonempty, disjoint, and arranged in stages. Inside a stage the chosen order avoids both AP orientations. Hence S is 3-permutable.

The intervals in B_k are pairwise disjoint, and

    |B_k| = L_k(4^(k+1)-1)/3 - (k+1)(m-1).

At the endpoint m_k=2L_k4^k this gives

    |S intersect [1,m_k]|/m_k
      >= 2/3 - 1/(6*4^k) - (k+1)(m-1)/(2L_k4^k)
      >= 2/3 - 1/(6*4^k) - (k+1)/(8*4^k).

The right side tends to 2/3, proving the upper-density assertion. Choose the first interval at each stage: a_k=L_k+m_{k-1}, b_k=2L_k. Its deficit is 2m_{k-1}, at most f(a_k) by construction and tending to infinity because m_k>=8m_{k-1}4^k. QED.

Thus bounded trimming is impossible, but trimming that diverges as slowly as any preassigned unbounded nondecreasing allowance can be compatible with a dense single 3-permutable set. This still constructs only one set; it says nothing about admissibly ordering its complement.

## Formulation correction: zero versus positive integers

Existence of a two-set solution on {0,1,2,...} is equivalent to existence on {1,2,3,...}. Translate every value in both parts and both enumerations by +1 in one direction and by -1 in the other. Translation preserves disjointness, exhaustive coverage, bijectivity, order type omega, and x+z=2y.

This corrects the claimed one-way-only comparison in [K, Remark 3]. No preservation theorem for adjoining 0 to an individual set is needed. The correction does not invalidate the separate finite lemma used above, and it does not settle the two-set problem.

## Public sources

[K] William Kasel, *Structural rigidity in the Erdős–Graham two-set permutation problem*, author manuscript, August 2026, Theorem 22 and Lemmas 23-26 (PDF pages 10-14); Remark 3 (PDF pages 4-5). https://raw.githubusercontent.com/Wkasel/erdos197/main/paper/main.pdf

[G] Jesse Geneson, *Density bounds for permutations avoiding monotone arithmetic progressions*, arXiv:2608.12604v1, August 2026, Theorem 1.1 and Section 3 (PDF pages 2,4-5). https://arxiv.org/pdf/2608.12604

[LV] Timothy D. LeSaulnier and Sujith Vijay, *On Permutations Avoiding Arithmetic Progressions*, arXiv:1004.1740v1, 2010; published in Discrete Mathematics 311 (2011), 205-207. The definitions and two-set question appear on PDF pages 3-4. https://arxiv.org/pdf/1004.1740
