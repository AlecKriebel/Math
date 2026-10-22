# Fixed points of the standard Minkowski question-mark function

## Scope and outcome

These are authored proofs of partial results and explicit descriptions of failed routes. They do not prove the exact number of fixed points. They concern the standard function Q:[0,1] -> [0,1], normalized by Q(0)=0 and Q(1)=1. Its continued-fraction formula, with x=[0;a1,a2,...] and S_k=a1+...+a_k, is

    Q(x) = sum_{k>=1} (-1)^(k+1) 2^(1-S_k).

For rational x the sum terminates. Use the canonical finite continued fraction with last partial quotient at least 2, except at x=1. The two finite expansions give the same value: splitting a final a into a-1,1 replaces a signed term t by 2t-t. The separately defined value at zero is 0.

We use the equivalent Stern-Brocot construction: Q sends the mediant of the endpoints of a Stern-Brocot interval to the arithmetic mean of their Q values. At the initial endpoints those values are 0 and 1. The construction produces a continuous strictly increasing bijection. For completeness, the level-n image intervals have length 2^-n and the domain intervals have maximum length tending to zero. An interval with endpoints a/b<c/d has determinant bc-ad=1 and length 1/(bd); each refinement increases b+d by at least 1, and bd>=b+d-1. Thus the maximum length after n refinements is at most 1/(n+1). These meshes and the ordered endpoint assignments give a continuous bijective extension in both directions. The finite continued-fraction formula follows from the same mediant recursion, or from the two branch equations below by the Euclidean algorithm. Agreement on the dense set of rational numbers gives agreement everywhere.

The identities used below are

    Q(1-x)=1-Q(x),
    Q(x/(1+x))=Q(x)/2.

The reflection identity follows by reflecting every Stern-Brocot interval and its image. The second identity follows because the map L(x)=x/(1+x) sends the entire Stern-Brocot tree to its left subtree, whose image is the half interval [0,1/2]. Each equality first holds on rational vertices by induction and then everywhere by continuity.

Write F(x)=Q(x)-x and K={x in (0,1/2):F(x)=0}. All counts below count distinct points, not an analytic multiplicity: Q is singular and an analytic multiplicity has not been defined here.

## Approach 1: arithmetic and algebraic classification

### Proposition 1.1: the rational fixed points are exactly 0, 1/2, 1

Let x=p/q be a nonzero rational in lowest terms, with canonical continued-fraction sum S. Bringing the defining sum to denominator 2^(S-1), its last term contributes +1 or -1 and every earlier term an even integer. Hence Q(x) in lowest terms has denominator exactly 2^(S-1).

The vertex x is first created at Stern-Brocot depth S-1, where the root 1/2 has depth 1. One way to check the depth identity is the subtractive Euclidean algorithm: reducing a rational by the inverse left or reflected-left branch subtracts one from its continued-fraction sum and one from its tree depth, until reaching an endpoint. Let f_1=f_2=1 be the usual Fibonacci numbers. At depth k, the sorted denominators of any interval are bounded respectively by f_(k+1), f_(k+2). This holds for (1,1) at depth zero. Refinement retains one denominator and replaces the other by their sum, proving the bounds inductively. A new vertex of depth n therefore has denominator at most f_(n+2). Consequently q<=f_(S+1).

For S>=3, f_(S+1)<2^(S-1): start with f_4=3<4 and use f_(m+1)<2f_m for m>=3. If x were fixed, equality of reduced denominators would require q=2^(S-1), a contradiction. S=1 gives x=1; S=2 gives x=1/2. Directly Q(0)=0, Q(1/2)=1/2 and Q(1)=1. This proves the claim.

### Proposition 1.2: no quadratic irrational is fixed

A quadratic irrational has an eventually periodic continued fraction, by Lagrange's classical theorem. Suppose the periodic block has length l and digit sum A. Terms in successive complete blocks of the series for Q are multiplied by the same rational ratio (-1)^l 2^-A. The finite initial part is rational, and the periodic tail is a convergent geometric series with rational initial block and rational ratio of absolute value less than 1. Thus Q(x) is rational. It cannot equal the irrational input x.

This argument uses Lagrange's theorem as a standard classical theorem; it is not a new proof of that theorem.

### What this route establishes, and its gap

Every nontrivial fixed point is irrational and is not quadratic. This allows algebraic numbers of degree at least 3 as well as transcendental numbers. It neither proves transcendence nor bounds the number of such fixed points. These elementary facts are consistent with, and credited to, the existing question-mark literature; no novelty is claimed.

## Approach 2: self-similarity and a global sign decomposition

### Proposition 2.1: F(x)<0 on (0,2/5] and F(x)>0 on [3/7,1/2)

For an integer n>=3 and x in [1/(n+1),1/n], monotonicity gives

    Q(x)<=Q(1/n)=2^(1-n)<=1/(n+1)<=x.

The middle inequality follows from 2^(n-1)>=n+1, by induction starting at n=3. Equality throughout could occur only for n=3 and x=1/4, where direct evaluation gives Q(1/4)=1/8<x. Thus the inequality is strict. These intervals cover (0,1/3].

On [1/3,3/8], Q(x)<=Q(3/8)=5/16<1/3<=x. On [3/8,2/5], Q(x)<=Q(2/5)=3/8<=x; the only possible endpoint equality x=3/8 is again excluded by its directly computed Q value. This proves the negative half of the assertion.

On [3/7,7/16], Q(x)>=Q(3/7)=7/16>=x, with equality at x=7/16 excluded by Q(7/16)=29/64. On [7/16,4/9], Q(x)>=29/64>4/9>=x.

For n>=4 put r_n=n/(2n+1)=[0;2,n]. On [r_n,r_(n+1)],

    Q(x)>=Q(r_n)=1/2-2^(-n-1)>1/2-1/(4n+6)=r_(n+1)>=x.

The strict inequality is equivalent to 2^(n+1)>4n+6, true at n=4 and preserved under incrementing n. These intervals cover [4/9,1/2). The positive half follows.

### Corollary 2.2: existence, symmetry and the precise remaining count

Since F(2/5)=-1/40 and F(3/7)=1/112, continuity gives a fixed point in (2/5,3/7). Hence K is nonempty and contained in that interval. The full fixed set on [0,1] is the disjoint union

    {0,1/2,1} union K union (1-K).

In particular there are at least five fixed points. If K has m finite elements, the total is 3+2m. Otherwise the fixed set is infinite. K is compact: it equals the closed zero set in [2/5,3/7], and neither endpoint is a zero. In particular it has a minimum and maximum, but compactness does not make them equal.

### Why simple self-similar propagation stops

A direct calculation from the branch equation gives

    F(L(t)) = F(t)/2 + t(t-1)/(2(1+t)).

The correction term is negative for 0<t<1. Thus F(t)<=0 implies F(L(t))<0. But the diagonal is not preserved: a nontrivial fixed t cannot also have L(t) fixed. Using the two contractions of the graph as contractions of the fixed-point equation would therefore be invalid. The global sign decomposition leaves the whole interval (2/5,3/7) unresolved; self-similarity alone has supplied no one-crossing invariant there.

## Approach 3: exact Stern-Brocot cylinders and effective isolation

### Proposition 3.1: rigorous interval pruning

For a rational interval I=[a,b], monotonicity places the graph in the rectangle

    [a,b] x [Q(a),Q(b)].

If Q(b)<a, then Q(x)<x for every x in I. If Q(a)>b, then Q(x)>x for every x in I. Such an interval contains no fixed point. Strict inequalities are required; endpoint signs alone would not imply either conclusion.

Start with [2/5,3/7], a Stern-Brocot interval of determinant 1. Its mediant has Q value the average of the endpoint values, exactly. Repeatedly subdivide intervals not eliminated by either strict test. At any fixed depth this produces a finite partition; the union of retained intervals contains every element of K. All quantities are rational, so comparisons are exact and require no floating-point root finder.

The supplied run uses maximum depth 128 relative to this starting interval. It visits 275 intervals and produces 138 terminal intervals, of which one is retained. All others have a strict certificate of exclusion. The single retained interval is

    [196891866281783104237450/468374932927154430517551,
     73080867820262788865501/173847946133977969489589].

Its width is exactly

    1/81426020110025487843678548887211712316576276539.

Its left endpoint has F<0 and right endpoint F>0. Thus it both contains all elements of K and contains at least one element. The complete finite partition, Q endpoint values and exclusion reasons are retained in EXACT_RESULTS.json and reconstructed by verify.py. The hull width is about 1.23e-47. Every point of K has the first 44 digits after the decimal point

    42037233942322307564099300664622187394918986.

This last decimal assertion is obtained by exact integer floor comparisons, not rounded floating-point output.

### Proposition 3.2: one nontrivial fixed point is computable

Begin with the sign bracket [2/5,3/7] and bisect arithmetically. Each midpoint is a rational strictly between 0 and 1/2, so Proposition 1.1 proves that its F value is nonzero. The continued-fraction formula computes that value exactly. Keep the half interval having a negative left endpoint and a positive right endpoint. The nested intervals after n steps have width 1/(35*2^n). Their unique common point alpha is computable, because the midpoint gives an explicitly bounded approximation. Continuity and the bracketing signs give F(alpha)=0. Propositions 1.1 and 1.2 make alpha irrational and nonquadratic. A 160-step exact instance is retained.

This is a computable selection of one fixed point, not a proof that the selected point is the least, greatest or sole nontrivial fixed point. Computability alone implies neither algebraicity nor transcendence.

### Exact gap of the cylinder route

A single retained interval may contain several or infinitely many roots. The finite depth does not establish that future retained intervals stay on one branch, or that the diameter of their full union tends to zero. Those unproved assertions would be sufficient to force uniqueness. None is inferred from the 128-level run or from published computations with longer common continued-fraction prefixes.

## Approach 4: dynamical basins and a derivative criterion

### Proposition 4.1: multiple lower-half fixed points force a nonexpanding approach

Suppose a<b are in K. Choose a rational r in (a,b). By Proposition 1.1 it is not fixed. Since Q is strictly increasing and fixes a,b, its iterates z_n=Q^n(r) stay in (a,b). If Q(r)<r, monotonicity makes z_n strictly decreasing. It has a limit c in [a,b), and continuity gives Q(c)=c. No fixed point lies in (c,r]: if y>c were fixed there, monotonicity would force z_n>=y for every n, contradicting the limit. Therefore F is negative throughout (c,r], by continuity and its negative sign at r.

For every t in (c,r], strict monotonicity now gives

    c<Q(t)<t,
    0<(Q(t)-Q(c))/(t-c)<1.

If Q(r)>r, the iterates instead increase to a fixed c in (a,b], and the identical argument gives t<Q(t)<c on [r,c). The same secant quotient lies strictly between 0 and 1. In either case at least one fixed point has a one-sided approach along which the Q secant slopes are bounded above by 1. It cannot have derivative +infinity.

### Corollary 4.2: a fixed-point-specific derivative condition suffices

If Q'(x)=+infinity at every x in K, K has exactly one element. Existence is Corollary 2.2 and two elements contradict Proposition 4.1. The hypothesis is not proved here.

### Proposition 4.3: uniform expansion or monotonicity of F on an interval is impossible

For any rational r=p/q in (0,1), choose its left Stern-Brocot parent u/v. Repeated mediants approaching r give

    r_n=(np+u)/(nq+v),
    r-r_n=1/[q(nq+v)],
    Q(r)-Q(r_n)=2^-n [Q(r)-Q(u)].

The determinant identity proves the middle formula and repeated averaging proves the last. Write d_n=r-r_n and C=Q(r)-Q(u)>0. For h>0 with d_(n+1)<=h<=d_n, monotonicity bounds

    0 <= [Q(r)-Q(r-h)]/h <= C 2^-n q((n+1)q+v),

which tends to zero. The right parent proves the same right derivative. Thus Q'(r)=0 and F'(r)=-1 at every interior rational. Every nonempty open interval contains such a rational, so F cannot be nondecreasing on any interval; Q cannot have secant slope uniformly greater than 1 there.

An explicit decrease inside (2/5,3/7) is checked at 5/12 < 53/127. This rejects a tempting shortcut of proving Q(x)-x globally increasing near the suspected root. It does not disprove the fixed-point-specific derivative hypothesis: rational points are not in K.

## Approach 5: Diophantine separation at rational arguments

### Proposition 5.1: an elementary sufficient arithmetic criterion

Assume there is q0 such that every reduced rational p/q in (2/5,3/7) with q>=q0 satisfies

    |Q(p/q)-p/q| >= 1/q^2.                    (H)

Then K has exactly one element.

To prove this, assume there are two and use Proposition 4.1. In the decreasing-orbit case c is irrational and F(t)<0 for c<t<=r. Infinitely many continued-fraction convergents p_n/q_n of c approach it from above, with denominators tending to infinity and

    0<p_n/q_n-c<1/q_n^2.

For sufficiently large such n they lie in (c,r), inside (2/5,3/7). Strict monotonicity and Q(c)=c imply

    0<p_n/q_n-Q(p_n/q_n)<p_n/q_n-c<1/q_n^2,

contradicting (H). The increasing-orbit case uses lower convergents and gives

    0<Q(p_n/q_n)-p_n/q_n<c-p_n/q_n<1/q_n^2.

Again there is a contradiction. This proves the conditional theorem, using only the standard convergent error bound and alternation about an irrational limit. The condition (H) is not established.

### Proposition 5.2: the unconditional denominator-separation bound is weaker

For reduced x=p/q not equal to a trivial fixed point, put D=2^(S-1), so Q(x)=N/D in lowest terms. Then

    |Q(x)-x| = |Nq-pD|/(qD) >= gcd(q,D)/(qD).       (B)

The numerator is a nonzero integer divisible by gcd(q,D), proving the inequality. This would imply (H) if D<=q*gcd(q,D). But D can be vastly larger: for x=1/q, S=q and D=2^(q-1), whereas gcd(q,D)<=q. Thus (B) alone gives no bound of order 1/q^2 uniformly. This failure of the elementary estimate is not a counterexample to (H), since the actual numerator can be large.

### Exact tests, stronger published criterion, and remaining gap

A standard-library rational scan checks every reduced p/q with 0<p/q<1/2 and q<=1500, totaling 342090 inputs. The only cases with q^2*|Q(p/q)-p/q|<=1/2 are 3/7 and 8/19, with exact values 7/16 and 19/64. The cases strictly below 1 are 1/3, 2/5, 3/7, 8/19 and 66/157. This is a finite test; it proves no eventual bound. The scan deliberately includes the wider half interval, not only the candidate root interval.

Gayfulin and Shulga's Theorem 4 gives a stronger sufficient criterion with displacement strictly greater than 1/(2q^2), eventually at reduced nontrivial rational arguments. Their Appendix needs additional continued-fraction/derivative arguments to reach the smaller constant. We do not claim to have reproved that stronger theorem here. Rational arguments must be reduced and trivial fixed points excluded; allowing unreduced representations of 1/2 would make any all-large-q statement false. The source's displayed shorthand is interpreted in this necessary context, not as a literal assertion about every unreduced pair of positive integers.

Neither the stronger literature condition nor (H) has been proved for unbounded denominators in this investigation. The finite counterexamples to the naive all-q form are retained as exact negative controls. No arithmetic contradiction to multiple irrational roots has been obtained.

## Domain and conclusion

On [0,1], the proved count is at least five; exact equality remains unresolved here after the five approaches. If instead one explicitly extends Q to R by Q(x+n)=Q(x)+n for integers n, every integer is fixed, so the literal real-line equation has infinitely many solutions. The unit-interval count, or equivalently a count modulo integer translation, must not be confused with the count over all of R. Under that extension the half-open interval [0,1) would have 2+2m fixed points if K had m finite elements.

The primary OWR question does not itself spell out a real-line extension. Accordingly this investigation retains the standard unit-interval question, records the domain issue, and does not claim the trivial real-line observation resolves the intended problem.
