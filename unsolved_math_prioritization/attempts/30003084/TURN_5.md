# Author turn 5: all cubic-supported sets and a large-line criterion

**Scoped partial results, pending independent review.** Every finite complex projective point set not on a conic but contained in some cubic has an ordinary conic. In addition, an ordinary conic exists whenever a line contains l points and the remaining r points satisfy l>=max(4,r-1). These statements retain singular/reducible conics and five-point uniqueness. They do not settle arbitrary point sets.

TURN_4 treats irreducible cubics. Here we treat every reducible cubic support, including its singular intersection points, and prove the large-line assertion used in one case. For sets of at most ten points we may already use TURN_2–TURN_3. We can therefore assume n>10 in the cubic classification below.

## 1. Large-line criterion over C

Let L contain l points of P and let r points lie outside L. If the outside points were collinear, P would lie on the union of two lines, contrary to the hypothesis. Choose three noncollinear outside points A={a,b,c}.

Choose p in P on L avoiding the at most three intersections of L with the joining lines ab, ac, bc. This is possible when l>=4. For each remaining outside point e, the five points A together with e and p have no four collinear: any offending line would contain e and two points of A and would have been excluded when choosing p. They therefore determine a unique conic R_e. It cannot contain L, because its other line component would have to contain the three noncollinear points A. Consequently R_e has at most one further intersection with L besides p.

Exclude those at most r-3 possible further intersections from P on L. If l>=r-1, then l-1>r-3, so some q distinct from p remains. The five points A,p,q have no four collinear and determine a conic Q, which also does not contain L. It contains exactly p,q among P on L. If Q contained any outside e not in A, uniqueness for A,e,p would force Q=R_e and hence q in R_e, contrary to its choice. Thus Q contains exactly those five points and is ordinary.

This is an elementary complex-algebraic argument; it uses no order or real-plane separation principle.

## 2. Two-point-deletion reflection lemma

Let A be a finite subset of an abelian group H, with |A|>=5, and fix k in H. Suppose

x maps to k-b_1-b_2-x

permutes A minus {b_1,b_2} for every distinct b_1,b_2 in A. Then every character chi:H to C* has at most three values on A.

The proof is the same subtraction argument as TURN_4, but with two rather than four deleted points and a constant factor chi(k). For B={b_1,b_2}, write z_a=chi(a), F=sum_A z_a, G=sum_A z_a^(-1), and K=chi(k). Complement invariance gives

(product_B z_b)(F-sum_B z_b)=K(G-sum_B z_b^(-1)).

Fix one deleted point c, with Q=z_c and S=z_c. For d,e outside {c} with z_d!=z_e, subtraction gives

F-S=z_d+z_e+K/(Q z_d z_e).

Four pairwise distinct values z_d,z_e,z_f,z_g outside {c} would imply Q z_d z_e z_f=K=Q z_d z_e z_g, a contradiction. If A has four character values, protect one representative of each and choose c among the remaining points. Thus no such four values exist. Fixed-point-freeness is again unnecessary for this lemma.

The same assertion is valid in multiplicative notation, with the reflection x mapping to k/(b_1 b_2 x).

## 3. A nonsingular conic and a line

Let the cubic support be an irreducible conic C together with a distinct line L. Write A=P intersect (C minus L), B=P intersect (L minus C), and retain all intersection points of C and L separately. The nonconic hypothesis implies |A|>=3 and |B|>=1: at most two points off L would lie on another line, and B empty would put all of P on C.

If |A|<=4, then n>10 gives at least seven points on L and at most four off it. Section 1 proves the result. Hence assume |A|>=5.

If |B|=1, choose four points of A and the point of B. No four are collinear, and their unique conic Q can contain neither C nor L. Its four intersections with C are exhausted by the four selected smooth points. Thus Q avoids all other points of A and every point of C intersect L; B has only its selected point. This is an ordinary conic.

Suppose |B|>=2 and fix distinct b,b' in B. Choose any three distinct a_1,a_2,a_3 in A. These five points have no four collinear and determine a unique conic Q. It cannot contain C, because of b,b', or L, because the three points of A are noncollinear. Its two intersections with L are exactly b,b', so it avoids both possible intersection points of C and L. Its fourth intersection with C is therefore a smooth point away from L, counted with multiplicity. If there is no ordinary conic, this residual point belongs to A and is distinct from the selected three.

### Secant case

Choose coordinates C:xy=z^2 and L:z=0. The smooth points away from the component intersections have parameters

C: [t:t^(-1):1], t in C*;  L: [u:1:0], u in C*.

For Q=alpha x^2+beta y^2+gamma z^2+delta xy+epsilon xz+phi yz, its restriction to C, multiplied by t^2, has leading coefficient alpha and constant coefficient beta. Its restriction to L is alpha u^2+delta u+beta. Since the two distinct finite nonzero parameters b,b' are its complete L intersection and L is not a component, alpha and beta are nonzero. Hence

product of the four C parameters = product of the two L parameters = b b'.

Fixing any two a_1,a_2 in A, the residual rule for the third variable x is x mapping to b b'/(a_1 a_2 x). It permutes A minus {a_1,a_2}. The two-deletion lemma applied to the identity character of C* contradicts |A|>=5.

### Tangent case

Choose coordinates C:yz=x^2 and L:z=0, with parameters

C: [t:t^2:1], t in C;  L: [1:u:0], u in C.

The restriction to C has leading and next coefficients beta and delta, while the restriction to L is beta u^2+delta u+alpha. Again beta is nonzero. Thus

sum of the four C parameters = sum of the two L parameters = b+b'.

The residual reflection is x mapping to b+b'-a_1-a_2-x. The additive group generated by these finitely many complex parameters is a finitely generated torsion-free abelian group. It has an injective multiplicative character, for instance by sending a free basis to independent positive primes. The two-deletion lemma gives the same contradiction. Both component-intersection cases are covered, even if those singular points belong to P.

## 4. Three distinct lines in general position

Use coordinate axes as the three components and write their smooth points as

A: [0:1:a],  B: [b:0:1],  C: [1:c:0], with a,b,c in C*.

Let A,B,C also denote the finite nonzero parameter sets, and reserve the three vertices separately. Each set is nonempty, since otherwise P lies on the other two component lines.

A conic through two points of A, two of B, and one of C is uniquely determined: no four of these points are collinear. It contains no component line. For example, containing the A line would force the two B points and the C point onto its other line, which is impossible. Its two A and two B intersections exhaust those component intersections, so it avoids all three vertices. Restriction of its equation to the three axes gives

(a a') (b b') (c c') = 1,                           (3)

where c' is the residual C intersection, with multiplicity. The same holds cyclically. Absence of an ordinary conic therefore makes c mapping to 1/(a a' b b' c) a fixed-point-free permutation of C for all distinct a,a' and b,b'.

First assume all three parameter sets have size at least three. Let H_A be the subgroup of C* generated by ratios of elements of A, and similarly H_B,H_C. Comparing two reflections whose A pairs share one point shows that every ratio a/a' preserves C multiplicatively; a third A point exists to form the two distinct pairs. Thus H_A is contained in the multiplicative stabilizer of C. The latter is finite, since its action on the nonempty finite set C is faithful, and it is contained in H_C, since h c and c both belong to C. Cyclic repetition gives

H_A=H_B=H_C=H,

and each of A,B,C is invariant under H. It follows that they are single cosets alpha H, beta H, gamma H. Here H is a finite cyclic subgroup of C*, of order at least three.

Distinct-pair products exhaust H: for any h in H choose x in H with x^2!=h and take y=h/x. Such an x exists because a square equation has at most two complex solutions and |H|>=3. Complement invariance in (3) implies (alpha beta gamma)^(-2) belongs to H. Choose distinct A and B pairs so that their product, multiplied by gamma^2, is one. Then the residual point for c=gamma is c itself. The corresponding conic has exactly the selected five points of P, contradicting the no-ordinary assumption.

If the smallest set has size one and the other two have size at least two, the conic through two points of each larger set and the sole point of the smallest set is immediately ordinary: its residual intersection is either a repeated selected point or outside P, and no vertices lie on it.

If the smallest set has size two, and the other two have sizes at least three and two, no-ordinary-conic behavior would make every residual reflection interchange those same two smallest-set parameters. Their product would fix the product of the chosen pairs on the other two lines. Holding one pair fixed and varying the other pair through a common point gives different products, a contradiction.

The remaining case with all three sizes at most two has at most nine points including the vertices and was already settled. Otherwise only the pattern (a,1,1), a>=3, remains. If the vertex opposite the large component is absent from P, the whole set lies on the large component together with the line through the two remaining smooth points, contrary to hypothesis. If that vertex is present, take it, the two single smooth points, and two smooth points on the large component. Their unique conic contains no component line. The vertex contributes intersection multiplicity at least two with the cubic, and the other four points contribute at least one each; all six intersection multiplicities are used. The conic is ordinary. This also addresses every allowed vertex of the original point set.

## 5. Three concurrent distinct lines

Choose components x=0, y=0, x=y with common point [0:0:1], and use smooth parameters

A: [0:1:-a],  B: [1:0:-b],  C: [1:1:c], with a,b,c in C.

The same two-two-one selection is uniquely determined and has no component. It avoids the common point, because the two selected smooth points on each of the first two lines already exhaust their intersections. Restriction of the quadratic equation gives the additive counterpart of (3):

a+a'+b+b'+c+c'=0.

If one parameter set has at least three points and another has at least two, comparison of two residual reflections with a common point in the first pair yields invariance of the third nonempty finite set under a nonzero additive translation. This is impossible over C: the orbit of any point under repeated translation is infinite.

For n>10, if two parameter sets do not have at least two points, the two smaller sets each have size one. Then all points lie on the large component and the line through those two small-set points; the possible common vertex is on the large component. This violates the nonconic hypothesis. The only alternative in which no set has size at least three has at most seven points including the common vertex, already settled. Hence every concurrent-line case has an ordinary conic.

## 6. Final partial theorem and exact original gap

Any cubic is either irreducible, a nonsingular conic plus a line, or supported on at most three lines. A repeated component leaves support of degree at most two and cannot contain a nonconic P. TURN_4 and Sections 3–5 therefore prove the claimed ordinary-conic theorem for every cubic-supported P. All component intersections, singular points, five-point rank conditions, and multiplicity versus additional-point distinctions are retained.

Together with TURN_2–TURN_3 and Section 1, a hypothetical counterexample to the original question must have at least eleven points, be contained in no cubic, and have at most floor((n-2)/2) points on each line. None of these necessary conditions proves that such a set does or does not exist. The rank-four Gale classification has not been extended to arbitrary rank, and the reflection laws arise from a common cubic and are not available for unrestricted configurations.

Five substantive author turns are complete. The original source question remains **unsolved, 5/5**. The proof package records these scoped theorems and the exact remaining gap for a separate adversarial review. Classical Bezout, elliptic divisor theory, finite abelian-group structure and existing ordinary-conic definitions are credited; no novelty assertion is made.
