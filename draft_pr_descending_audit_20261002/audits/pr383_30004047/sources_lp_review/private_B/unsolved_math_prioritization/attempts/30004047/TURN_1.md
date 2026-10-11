# Author turn 1: exact fixed-template game and complete-uniform middle families

## 1. Fixed-template formulation

This turn retains only the two mono-constrained degree conditions. It does not use the extra degree bounds in the neighboring psi problem. For a fixed finite middle set B with positive probability weights beta, and fixed last-part neighborhoods T_c subset B, let

    F_x = {S subset B : beta(S)>=x}.

Every first-part vertex can be replaced by its B-neighborhood S in F_x, with the total weights of identical neighborhoods combined. Conversely any rational probability distribution alpha on F_x gives a finite first part by a blow-up. For rational beta,x the exact fixed-template weighted optimum is therefore

    rho = min_alpha max_c sum_(S in F_x) alpha(S) 1[S intersects T_c].       (1)

The last-part weights gamma have already been chosen to ensure

    sum_(c : b in T_c) gamma(c)>=y for every b in B.

They enforce admissibility but do not weight the maximum in (1). All feasible neighborhood sets are nonempty because x>0.

Finite linear-program duality gives the equivalent exact certificate

    rho = max_q min_(S in F_x) sum_(c : S intersects T_c) q(c),              (2)

where q ranges over probability distributions on C. For completeness, introduce a variable z and minimize z subject to alpha>=0, sum alpha=1, and for each c the corresponding row payoff at most z. Its dual has nonnegative row multipliers q with sum q=1 and a lower bound lambda on every column payoff. Maximizing lambda is exactly (2). Both feasible polytopes are nonempty and compact after bounding 0<=z<=1, so the optima exist. Rational data give rational optimal solutions, hence actual finite blow-ups, rather than only limiting weighted objects.

Thus a sufficient and, for the fixed template, necessary certificate for rho>=1/k is a probability distribution q on C such that every beta-heavy S meets a q-fraction at least 1/k of the last-part neighborhoods. The uniform distribution on k selected vertices is a special certificate: it works if the complement of the union of their T_c has beta-weight strictly below x. This special *integral covering certificate* is not necessary, as Section 4 shows.

This formulation is a finite optimization equivalence, not a resolution of the arbitrary-template problem. Its weighted/blow-up framework is standard and already appears in the primary paper and the related research packet; the new work below is the complete-uniform evaluation and the exact failed-cover test.

## 2. Evaluation for complete-uniform middle families

Fix integers 1<=r<=n. Take C=[n], and take B to be all r-element subsets of [n]. Join b in B to c in C exactly when c belongs to b. Use uniform middle and last weights. Then every b has r/n of C as neighbors. Let m=binomial(n,r), and fix x in (0,1]. Define

    h = min{j in {r,...,n}: binomial(j,r)>=ceil(x m)}.                     (3)

**Theorem.** For this fixed B--C template, the least possible largest A-reach fraction, over all nonempty finite first parts A with every A-vertex adjacent to at least x m middle vertices, is exactly h/n.

**Lower bound.** Let a have middle-neighborhood S_a, a family of r-subsets. If its union in [n] has size j, then |S_a|<=binomial(j,r). The degree bound and (3) imply j>=h. Thus each a has at least h distinct second neighbors in C. Counting reachability pairs in A times C gives a c reaching at least (h/n)|A| first-part vertices.

**Attainment.** Let A be all h-subsets H of [n], and join H to every r-subset b contained in H. Every A degree is binomial(h,r)>=ceil(x m), and its C-reach set is exactly H. Each c therefore reaches binomial(n-1,h-1) of the binomial(n,h) first vertices, a fraction h/n. This is an ordinary finite graph, with no approximation or irrational-weight issue.

In the game (2), the uniform distribution on C is consequently optimal. More generally the symmetric-group averaging of any q does not decrease the minimum column payoff because that minimum is a concave symmetric function of q; here the direct counting proof already establishes the exact value.

## 3. The entire family cannot refute the source's integer-k implication

Consider any such complete-uniform middle template, with any finite first part and any parameters x<=binomial(h,r)/binomial(n,r), y<=r/n for which the construction above would have reach h/n<1/k. We prove that the two conjectured hypotheses cannot both hold. By the preceding theorem this also excludes every first part over this template from furnishing a counterexample at any x,y.

For k=1, h<n implies

    x <= binomial(n-1,r)/binomial(n,r) = 1-r/n.

Hence x+y<=1, contradicting the required strict inequality.

Assume k>=2. If r>=2, then

    x <= product_(i=0,...,r-1) (h-i)/(n-i)
      <= (h/n)^r <= (h/n)^2 < 1/k^2,
    y <= r/n <= h/n < 1/k.

Consequently kx+y<2/k<=1, contradicting the second required inequality kx+y>=1.

If r=1, then x<=h/n and y<=1/n. The integer inequality kh<n gives n>=kh+1. Since h>=1,

    h+k <= kh+1 <= n.

It follows that x+ky<=(h+k)/n<=1, contradicting the first required inequality.

Thus the original implication holds for this entire parameterized family, including every allowed first part. This is a restricted-template theorem, not a proof that all graphs admit such a template reduction. It also does not assert that the fixed-template lower value h/n equals the unrestricted phi(x,y).

## 4. A strict-threshold graph with no two-vertex covering certificate

Take n=11, r=4, and x=y=4/11. Then m=330 and ceil(xm)=120. Since

    binomial(8,4)=70 < 120 <= binomial(9,4)=126,

we have h=9. Use the attaining graph:

- A consists of the 55 nine-element subsets H of [11];
- B consists of the 330 four-element subsets b of [11];
- C=[11];
- H--b is an edge iff b is contained in H, and b--c is an edge iff c belongs to b.

Every A degree is 126, hence at least (4/11)330=120. Every B has four C-neighbors, exactly y|C|. The source's two k=2 hypotheses are strict: x+2y=2x+y=12/11>1. Every c reaches exactly 45 A-vertices, so the largest reach fraction is 45/55=9/11, well above one half.

Yet no pair of C-vertices covers A by second neighborhoods. For any pair {c,d}, the A-vertex H=[11] minus {c,d} reaches neither c nor d. Equivalently, B minus (T_c union T_d) consists of the 126 four-subsets avoiding c,d, with middle-weight 126/330=21/55>x. Thus every pair fails the heavy-set hitting certificate from Section 1. Repetition of a selected C-vertex cannot help.

This proves that the tempting stronger assertion “the threshold hypotheses force two C-vertices whose reach sets cover A” is false, even at a strictly admissible diagonal point. It is an exact obstruction to that mechanism, not a counterexample to phi>=1/2. The optimum fractional game certificate here is much stronger than any certificate obtained solely by demanding a two-vertex cover.

## 5. Remaining task and count

The general problem remains unresolved after one substantive turn. We have an exact finite game, an evaluated infinite family, and a concrete failure of the small integral-cover route. General templates can have overlapping middle neighborhoods not represented by all r-subsets with uniform weight. No reduction to the evaluated family is proved. Subsequent work must exploit those overlaps or find a genuinely different construction, rather than assume the disproved covering certificate.
