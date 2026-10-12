# Arithmetic modular obstruction and exact carry accounting

Date: 12 October 2026 UTC. Target: row 1741 / problem 2350 / Erdos 864.

This note proves a finite arithmetic obstruction to one natural construction strategy. It does not prove the interval conjecture, improve its unrestricted leading upper constant, or supply an asymptotic counterexample. No novelty claim is made.

## 1. Scope and result

The unresolved symmetric problem asks whether every Sidon set B in (0,L] on the integer or half-integer lattice satisfying

    B intersect (B+B+B) = empty

has |B| <= (sqrt(2/3)+o(1)) sqrt(L). Repetitions are allowed throughout, including in the Sidon condition.

A tempting construction strategy is to take a dense modular Sidon set, translate it, and certify triple-sum avoidance by a congruence. The following exact obstruction limits that strategy.

**Theorem 1.** Let G be a finite abelian group of order q, and let B be a nonempty Sidon subset of G of size k, in the strong sense that a+b=c+d implies equality of the unordered pairs, including pairs with equal entries. If B intersect (B+B+B) is empty in G, then

    (3k^2-k)/2 <= q-1.                                      (1)

Consequently k <= (1+sqrt(24q-23))/6, in particular k <= sqrt(2q/3)+O(1).

The modulus q is crucial: (1) is not an interval theorem with q silently replaced by L. Integer triple-sum avoidance does not imply avoidance modulo q.

Theorem 2 below is quantitative even when modular avoidance is not assumed. It shows that for a modular Sidon set of near-maximal size k=(1-o(1))sqrt(q), *every* translate has at least (1-o(1))q ordered congruent triple-to-single coincidences. Thus a valid integer lift has to eliminate all of them by nonzero carries; a modular certificate cannot simply make the coincidences disappear.

## 2. Proof of the finite-group bound

Write

    D = {a-b : a,b in B, a != b},
    S = {a+b : a,b in B}.

All k(k-1) ordered nonzero differences are distinct. Indeed, a-b=c-d implies a+d=c+b. The Sidon property says {a,d}={c,b}. Either a=c and d=b, identifying the ordered pairs, or a=b and d=c, contrary to the differences being nonzero. This argument also excludes a nonzero difference of order two, because its reverse representation would be different. Therefore

    |D| = k(k-1),       |S| = k(k+1)/2.

A point of S intersect D would give a+b=c-d, hence c=a+b+d in B intersect 3B. Therefore S intersect D is empty.

Also 0 is not in S. Otherwise a+b=0 for some a,b in B, and any c in B would satisfy c=a+b+c, again contradicting the triple-sum condition. Since D omits zero by definition, D and S are disjoint subsets of G without its identity. Their cardinalities sum to (3k^2-k)/2, proving (1). Solving the quadratic gives the displayed exact root.

Conversely, for any nonempty B (without even needing the Sidon hypothesis), the two conditions S intersect D = empty and 0 notin S imply B intersect 3B = empty: a+b+c=d gives a+b=d-c, which is either zero or a member of D. Thus this finite-group disjointness criterion loses no modular triple-sum information.

## 3. Exact supersaturation under every translation

For t in G let B_t=B+t and define the ordered sum multiplicity

    r_t(u) = #{(a,b) in B_t^2 : a+b=u}.

Strong Sidonicity gives r_t(u) in {0,1,2}: a repeated-entry pair contributes one, and a distinct-entry pair contributes two.

The nonzero difference set D is unchanged by translation. Put

    H = (G without {0}) without D,
    h = |H| = q-1-k(k-1).

Let

    R(t) = #{(a,b,c,d) in B_t^4 : a+b+c=d}.

All entries are ordered; repetitions are allowed.

**Theorem 2 (exact identity).** For every t,

    R(t) = k^2 - sum_{u in H} r_t(u) + (k-1)r_t(0).           (2)

In particular

    R(t) >= k^2-2h = 3k^2-2k-2q+2.                          (3)

The lower bound may be negative, in which case R(t)>=0 is stronger. Equation (2), not merely (3), holds for all finite abelian groups admitting such a strong Sidon set.

**Proof.** Let r_D(u)=#{(d,c) in B_t^2:d-c=u}. The difference uniqueness proved above gives r_D(0)=k, r_D(u)=1 for u in D, and r_D(u)=0 for u in H. Matching a+b with d-c yields

    R(t)=sum_u r_t(u)r_D(u)
        =sum_{u in D}r_t(u)+k r_t(0).

Since sum_u r_t(u)=k^2, this is (2). The estimate r_t(u)<=2 gives (3).

If k/sqrt(q) tends to 1 along a sequence of modular Sidon sets, then h=o(q), so (2) implies R(t)>=(1-o(1))q uniformly over *every* translation t. This conclusion needs no equidistribution theorem and no averaging over translations.

If B is a perfect difference set, meaning h=0, then

    R(t)=k^2+(k-1)r_t(0),

so R(t) is one of k^2, k^2+k-1, k^2+2k-2. In particular, translating a perfect difference set never removes its modular triple-to-single coincidences.

The count bound (3) has a slightly weaker finite k correction than Theorem 1. This is expected: (3) bounds ordered representations using capacity two, whereas Theorem 1 uses the exact number of unordered sums.

## 4. Exact integer-carry version

Let q be a positive integer, and let b₁,…,bₖ be integers with pairwise distinct residues modulo q whose residue set B is a strong Sidon set of cardinality k. Define

    C_j = #{(a,b,c,d) in {b_1,...,b_k}^4 : a+b+c-d=jq},

again with ordered entries and repetitions allowed. Then finite summation gives the exact identity

    sum_{j in Z} C_j = R(0).                                 (4)

The integer triple-sum-free condition is precisely C_0=0. Consequently every triple-sum-free integer lift satisfies

    sum_{j != 0} C_j >= k^2-2h.                              (5)

If all lifted integers belong to [1,L], possible j additionally satisfy

    (3-L)/q <= j <= (3L-1)/q.                                (6)

For L<=q, no negative j is possible, and only j=0,1,2 can occur. Thus such a triple-sum-free lift obeys the particularly concrete necessary condition

    C_1+C_2 >= k^2-2h.                                       (7)

For a near-perfect modular seed the right side is (1-o(1))q. This is a real integer-arithmetic constraint on a candidate, but it is not a contradiction: nonzero carries are allowed, and no argument here excludes their bearing that many coincidences.

As a small diagnostic example, {2,3} in the integers is Sidon and triple-sum-free. Modulo 3 its unordered sums are 1,2,0 and hence it is a strong Sidon set, with h=0. The five ordered quadruples counted by R(0)=5 have nonzero carries: one has a+b+c-d=3 and four have a+b+c-d=6. Thus integer avoidance definitely does not imply modular avoidance, even for a perfect difference set. This example is only a logical check, not asymptotic evidence against the target.

For half-integer B, scale all elements by 2 before applying the congruence and carry tests. This preserves all exact sum equalities and triple-sum avoidance. It doubles the numerical interval parameter, so it must not be used to claim an unchanged sharp interval constant. Alternatively, if B lies in the half-integer coset Z + 1/2 and q is odd, map b to (2b)·2⁻¹ in Z/q. When these images are pairwise distinct and strong Sidon, the quantity a+b+c−d is integer-valued and its multiples of q give the direct carry decomposition.

## 5. Consequence for modular construction searches

Suppose a proposed construction provides a triple-sum-free modular Sidon set in Z/q and takes integer representatives lying in (0,L], with q <= (1+o(1))L. Theorem 1 proves

    k <= (sqrt(2/3)+o(1))sqrt(L).

This strategy therefore cannot furnish an asymptotic counterexample to the symmetric target under that relation between modulus and interval. If q is substantially larger than L, this conclusion does not follow; if only integer triple avoidance is proved, Theorem 1 does not apply. These are genuine remaining possibilities, not exclusions.

More generally, a search starting with k=(1-o(1))sqrt(q) modular Sidon points must confront the uniformly positive count in Theorem 2: modular translations alone cannot certify triple avoidance, and any valid lift must explicitly verify the carries in (4). This removes a possible false shortcut from the construction program without claiming the entire modular-lift program has failed.

## 6. Why a known Fourier-uniformity theorem was not used as a solution

A public source check found Miquel Ortega and Sean Prendiville, “Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity,” Journal de Theorie des Nombres de Bordeaux 35 (2023), 115-134, DOI 10.5802/jtnb.1239. The journal PDF is https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf . Theorem 1.2 concerns Fourier uniformity; Theorem 1.15 has an explicit at-least-five-variables hypothesis. Its direct conclusion cannot be invoked for a+b+c=d, which has four variables. This is an applicability check only, not a proof that all Fourier methods fail. No result from that paper is a premise of Theorems 1 or 2.

The earlier continuum barrier also remains relevant: it shows that the fixed macroscopic difference/half-sum relaxation admits uniform mass one. The results here instead retain exact residue occupancies and exact nonzero carries. They do not assume that the continuum obstruction is an integer construction.

## 7. Verification and residual

The authored finite diagnostic, not distributed in this prose edition, exhaustively enumerates every subset of Z/q for 1<=q<=17. For each strong Sidon subset it verifies difference uniqueness, Theorem 1 whenever its hypotheses hold, the identity (2), the bound (3), and equivalence of modular triple avoidance with the disjointness criterion. As every translate is another enumerated subset, this covers every translation in these moduli. It independently counts ordered quadruples by iterating triples and testing the fourth entry. It also checks the carry identity for representatives in [1,q] and the explicit {2,3} example.

These finite checks are implementation diagnostics. The general proofs are given above. The interval bottleneck remains unresolved. In particular, the check does not produce an asymptotic counterexample and the modular theorem must not be advertised as the desired interval theorem.
