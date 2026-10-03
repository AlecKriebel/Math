# Author turn 4: pairwise-union compatibility at the next rank

## 1. Result

**Theorem.** For every integer k>=2, if x,y>1/(k+1), an admissible ordinary finite graph with |A|<=5k has a C-vertex reaching at least |A|/k vertices.

The result also permits arbitrary positive probability weights on B and C, while A still consists of equally weighted vertices. Thus a counterexample to the source's one-third diagonal half-reach assertion must have **at least eleven** first-part vertices. The asymmetric integer-k wedge and arbitrarily large first parts remain unresolved.

Turn 3 handles |A|<=4k. Its necessary inequality also handles 4k+2<=|A|<=5k: here r=4 and

    x<=3/(|A|-k+1)<=1/(k+1).

The sole new first-part size to settle is n=4k+1. The proof uses the second degree condition to force pairwise compatibility of the remaining middle types, then gives explicit dual charges. No numerical linear-program output is used as a proof certificate.

## 2. Exactly k-1 maximal types and a small residual C-space

Suppose every C-reach set has size at most four. A middle neighborhood has size at most four. Let T_1,...,T_t be the distinct four-element middle types and U their union. Turn 3 gives t<=k-1 and x<=3/(n-t). If t<=k-2, then n-t>=3k+3 and x<=1/(k+1), impossible. Hence

    t=k-1, and |U|<=4(k-1).                                     (1)

As before, C_(T_i), the class whose reached set is exactly T_i, has gamma-weight at least y, and these classes are disjoint. Call a middle type residual if it is contained in none of the T_i. Its C-neighborhood avoids every C_(T_i). The available residual C-weight is at most

    1-(k-1)y < 2y.                                               (2)

Every residual middle vertex still has C-neighbor weight at least y. Consequently any two residual middle vertices have a common C-neighbor, and their A-neighborhoods have union of size at most four:

    |S union S'|<=4 for all residual types S,S'.                   (3)

Every residual type has size at most three. Types contained in a T_i can be handled separately by charging each vertex in U at most 1/4.

## 3. Classification of the residual triples

Let F be the family of three-element residual types. Any two intersect in at least two vertices by (3). Then either all members of F contain a fixed pair P, or every member is contained in a fixed four-set D. Empty and singleton families are included in the first alternative or treated separately.

Here is the elementary classification. If F has two distinct members, write them as {a,b,c} and {a,b,d}. If every member contains {a,b}, the first alternative holds. Otherwise a third member must be {a,c,d} or {b,c,d}, since it intersects both first triples in at least two elements. A further triple containing {a,b} and an element outside {a,b,c,d} would intersect that third member in only one element. A further triple not containing {a,b} must again lie in {a,b,c,d}. Thus all members lie in D={a,b,c,d}.

If the second alternative occurs and the first does not, |D|=4 and F contains at least three of its four triples. The common intersection I of F has size one when there are three triples, and size zero when there are four.

## 4. Charges in the pair-star case

If F is empty, put charge 1/4 on U and 1/2 outside U. Every maximal type has charge one; every contained type has charge at most one; every residual type has size at most two and also has charge at most one. Total charge is at least

    n/2-|U|/4 >= k+3/2.

If F has a common pair P, put charge 1/4 on U union P and 1/2 elsewhere. Every residual triple has charge at most 1/4+1/4+1/2=1, and all pairs have charge at most one. The contained and maximal types remain bounded by one. Since |U union P|<=4(k-1)+2, total charge is at least

    n/2-(4k-2)/4 = k+1.                                         (4)

Summing the A-degree inequalities against either charge gives x(k+1)<=1, contrary to x>1/(k+1).

## 5. Charges in the four-set case

Assume F has no common pair and is contained in D of size four. Begin with charge

- 1/4 on U;
- 1/3 on D minus U;
- 1/2 elsewhere.

All maximal/contained types, all residual triples and all pairs have charge at most one. Its total charge is

    Z=n/2-|U|/4-|D minus U|/6.                                  (5)

If |U|<=4k-5, then

    Z >= (4k+1)/2-(4k-5)/4-4/6 = k+13/12 > k+1.

If |U|=4k-4 and D meets U, then

    Z >= (4k+1)/2-(4k-4)/4-3/6 = k+1.

Both cases contradict the degree inequalities. The only case still requiring a different charge is

    |U|=4k-4, D disjoint from U,
    A=U disjoint-union D disjoint-union {w}.                     (6)

In particular w lies in no maximal type. It lies in no residual triple, because all such triples belong to F and lie in D. If a residual pair {w,v} occurs, (3) applied to every triple F in the family forces v to belong to every F; otherwise their union has size five. Thus v must lie in the common intersection I.

If I is a singleton, charge U by 1/4, w by 1, I by 0, and the other three vertices of D by 1/2. Every triple of F contains I, so has charge one. Pairs containing w can only pair it with I and have charge one; every other pair also has charge at most one. Maximal and contained types have charge at most one. Total charge is

    (k-1)+1+3/2 = k+3/2.

If I is empty, charge U by 1/4, D by 1/3, and w by 1. No pair containing w can occur. Every used type again has charge at most one, while total charge is

    (k-1)+4/3+1 = k+4/3.

Both totals exceed k+1 and give the final contradiction. This completes the new n=4k+1 case and the theorem.

## 6. What this mechanism does and does not provide

The proof works because the maximal-type count is forced to be exactly k-1 at this particular first-part size. Removing their C-classes leaves total weight less than twice the minimum residual degree, which forces every pair of residual middle types to be compatible. Rank-three pairwise compatibility has the explicit pair-star/four-set classification above.

At the next rank, the first-incidence count does not necessarily force k-1 maximal types. The residual C-space can be larger than twice the required degree, so pairwise compatibility need not hold. Applying the classification without proving (2) would silently add a hypothesis. No such extension is claimed.

The original remains unresolved after four substantive author turns. One author turn remains for a genuinely different higher-rank mechanism or a precise final obstruction. The exact finite verifier checks the charge construction on all 54 canonical two-or-more-triple configurations at the nine-vertex first case, and on additional deterministic higher-k configurations; these controls do not replace the universal proof.
