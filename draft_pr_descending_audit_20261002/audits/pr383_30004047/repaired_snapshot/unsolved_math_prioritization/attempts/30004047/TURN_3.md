# Author turn 3: maximal-neighborhood counting and finite first-part bounds

## 1. A cardinality-sensitive necessary condition

Fix an integer k>=2, and let A have n vertices of equal weight 1/n. Middle and last parts may have arbitrary positive probability weights beta and gamma; ordinary graphs are a special case. Assume every a sees beta-weight at least x>0 and every b sees gamma-weight at least y>1/(k+1). Suppose, towards a counterexample, that every c reaches strictly fewer than n/k first vertices. Put

    r=floor((n-1)/k).

Then every reached set has size at most r, and every nonempty middle neighborhood S_b=N_A(b) has size at most r. The latter follows by choosing any C-neighbor of b, which exists because y>0.

**Theorem.** If r<=1, such a counterexample is impossible. If r>=2, let t be the number of distinct occurring middle neighborhoods of size exactly r, and U their union. Then

    t<=k-1,
    x <= r(r-1)/(rn-|U|) <= (r-1)/(n-t) <= (r-1)/(n-k+1).       (1)

This is a necessary condition for a particular finite first-part size. It does not identify the unrestricted function phi or assert an upper bound on counterexample size.

## 2. Why there are fewer than k maximal types

For a set T of size r, let C_T be the C-vertices whose reached A-set is exactly T. If T occurs as S_b for a middle vertex, every C-neighbor of that vertex lies in C_T, since reached sets have size at most r. Hence gamma(C_T)>=y. The sets C_T for distinct T are disjoint.

Suppose there are k distinct occurring maximal types T_1,...,T_k. A middle neighborhood S that is contained in none of them has no neighbor in any C_(T_i). Its total possible C-neighbor weight is at most

    1 - sum_i gamma(C_(T_i)) <= 1-ky < y,

contradicting its degree requirement. Thus every middle neighborhood is contained in at least one T_i. Every A-vertex has a middle neighbor, so A is contained in their union. This gives n<=kr, contrary to kr<=n-1. Therefore t<=k-1.

When r=0, no nonempty middle neighborhood can occur, already a contradiction. When r=1, all nonempty middle types are maximal. The same argument forces at most k-1 singleton types covering A, whereas r=1 implies n>=k+1. This proves the first assertion.

## 3. A dual charge using the union of maximal types

For r>=2, assign charge 1/r to every A-vertex in U and charge 1/(r-1) to every vertex outside U. Each maximal middle neighborhood has total charge one. Every other middle neighborhood has at most r-1 vertices, so its charge is at most one as well. Summing the A-degree inequalities with these charges gives

    x ( |U|/r + (n-|U|)/(r-1) )
       <= sum_b beta(b) charge(S_b) <=1.

The total charge is (rn-|U|)/(r(r-1)). Since |U|<=tr and t<=k-1, this proves all three inequalities in (1). No bounded-rank fractional matching theorem is assumed here; the displayed charge is the full certificate.

A counterexample must in particular have enough distinct maximal types to satisfy

    t >= n-(r-1)/x,

as well as the upper bound t<=k-1. Overlap of the maximal types makes the stronger first bound in (1) more restrictive.

## 4. Consequence for every integer k in a bounded-size range

**Corollary.** If x,y>1/(k+1) and |A|<=4k, some c reaches at least |A|/k vertices.

If n<=k, any nonempty reached set is enough. Otherwise r>=1; the case r=1 was disposed of above. Since n<=4k, the remaining possibilities are r=2 or r=3. For r=2, n>=2k+1 and (1) gives

    x<=1/(n-k+1)<=1/(k+2)<1/(k+1),

a contradiction. For r=3, n>=3k+1 and (1) gives

    x<=2/(n-k+1)<=1/(k+1),

again a contradiction. This proves the corollary, with strictness exactly as stated.

In particular, an ordinary counterexample to phi(x,x)>=1/2 at x>1/3 would require **at least nine A-vertices**, improving the six-vertex range from turn 2. More generally the symmetric-threshold special case at level 1/k has no ordinary counterexample with at most 4k first vertices. The source's more general asymmetric wedge is not silently replaced by this subcase; only the explicit condition (1) is available here for asymmetric parameters.

## 5. Why the charge by itself stops at the next rank

At k=2,n=9,r=4, (1) permits x as large as 3/8. Here is a concrete first-incidence support attaining that bound, so the charge cannot simply be strengthened without using additional information.

Let A be the disjoint union of T={1,2,3,4} and D={5,6,7,8,9}. Use one middle type T with beta-weight 3/8. Use all ten three-element subsets of D as middle types, each with beta-weight 1/16. The weights sum to one. Each vertex of T has degree weight 3/8; each vertex of D lies in six triples and also has degree weight 6/16=3/8. There is exactly one maximal four-element type. The charge from Section 3 is 1/4 on T and 1/3 on D, of total 8/3, and every used type has charge exactly one.

This is **not** a tripartite counterexample. In fact, it cannot be completed with every reached set of size at most four and y>1/3. To see this, the C_T class has weight at least y. A C-vertex outside C_T can contain at most four of the ten triple types in its reached set: among at most four D-vertices there are at most binomial(4,3)=4 triples. No C_T vertex contains any such triple. Summing their ten degree requirements gives

    10y <= 4(1-gamma(C_T)) <=4(1-y),

hence y<=2/7. This is below 1/3. Thus the first-incidence charge is sharp as an isolated relaxation, while the second-incidence conditions defeat this explicit attempted realization.

The useful new obligation at higher rank is therefore to combine maximal-type structure with simultaneous C-neighborhood compatibility; a first-incidence cover calculation alone loses essential constraints.

## 6. Status

Three substantive author turns are complete. The full original remains unresolved. This turn supplies a uniform-in-k finite-size theorem, precise asymmetric necessary inequalities and a sharp but nonrealizable relaxation example. No claim of a universal support reduction, complete source resolution or historical novelty is made.
