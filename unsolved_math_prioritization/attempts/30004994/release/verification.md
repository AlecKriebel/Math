# Verification of Meyerovitch's counterexample

This is an authored reconstruction of the known construction in Meyerovitch, Theorem 1.2 and Section 4 ([arXiv:1701.01318v2](https://arxiv.org/abs/1701.01318v2)). The mathematics and priority belong to that prior work.

## 1. Exact target and conventions

For every countably infinite amenable discrete group G acting expansively by continuous automorphisms on a compact metrizable abelian group X, is positive topological entropy equivalent to the existence of distinct x,y for which d(sx,sy) tends to zero as s leaves every finite subset of G?

The source uses this whole-group, cofinite meaning of asymptotic. For G=Z it is two-sided, not just forward-time convergence. It suffices to refute the positive-entropy-to-asymptotic-pair implication for one group allowed by the question.

## 2. The group and the system

Let H_n=(F_2)^(n+1), so q_n=|H_n|=2^(n+1), for n>=1. Set

G = direct sum over n>=1 of H_n,
F_N = H_1 x ... x H_N (with all later coordinates zero).

The group G is countably infinite, abelian and discrete. Its finite subgroups F_N exhaust it. For each s in G, s+F_N=F_N for all sufficiently large N; hence (F_N) is a Følner sequence and G is amenable. It is not finitely generated, since every finite collection of elements is contained in some finite F_N.

Inside the product group F_2^G, define X by the coordinate equations

sum over h in H_n of x(g+h) = 0 in F_2, for every n>=1 and g in G.

Each equation involves finitely many coordinates and is a continuous linear constraint. Thus X is a closed subgroup of the compact metrizable abelian group F_2^G. The left shift (s*x)(g)=x(g-s) preserves every equation and is a continuous group automorphism with inverse the shift by -s. This is an algebraic action in the precise source sense.

Choose an enumeration G={g_1,g_2,...} with g_1=0 and metric

d(x,y)=sum over j>=1 of 2^(-j) times 1[x(g_j) != y(g_j)].

If x and y differ at t, shifting by -t makes their zero coordinates differ, so their distance becomes at least 1/2. Thus c=1/4 is an expansive constant. This does not require X to have finite type.

## 3. All finite patterns and their global extension

Choose a nonzero distinguished element a_n in H_n, and let

E={g in G: g_n != a_n for every n}.

For g in G, let I(g)={n:g_n=a_n}. This set is finite because g has finite support and all a_n are nonzero. For each choice of one b_n in H_n\{a_n} for every n in I(g), replace those coordinates of g by b_n; denote the resulting point of E by r_b(g). Given any function w:E->F_2, define

x_w(g)=sum over all such choices b of w(r_b(g)).

An empty set of replacements contributes the single value w(g), so x_w restricts to w on E. All sums are finite, and replacements preserve membership in G.

Fix every coordinate except n and vary coordinate n over H_n. By the definition just given, the value with coordinate a_n is the sum of the values with coordinate b in H_n\{a_n}. Summing the entire fiber therefore gives zero in F_2. This verifies every defining constraint, so x_w lies in X. In particular, every assignment on E extends globally.

Now restrict to F_N. Any permitted pattern is determined by its coordinates in E intersect F_N: use the n-th parity equation to replace an a_n coordinate by the sum of all other coordinate values, and induct on the number of distinguished coordinates. Conversely, every assignment to E intersect F_N extends to E and then to X by the formula above. Therefore the restriction space has dimension

D_N = product over n=1,...,N of (q_n-1),

and exactly 2^(D_N) patterns occur on F_N. This proves both the upper bound and the extension-dependent lower bound; treating local consistency as global extendibility without this argument would leave a gap.

## 4. Positive entropy

Let P be the clopen partition according to x(0). Its join over F_N has exactly 2^(D_N) nonempty atoms, giving entropy

h(P)=lim as N->infinity of [D_N/|F_N|] log 2
    =[product over n>=1 of (1-2^(-(n+1)))] log 2.

This is also the topological entropy. To see the upper bound directly, every finite open cover of X is refined by the cylinder partition on some finite coordinate set K. Enlarge K to contain zero. Eventually K is contained in F_N and K+F_N=F_N, so the join of this cylinder partition over F_N is exactly the partition into F_N-patterns. Thus every open-cover entropy is at most the displayed limit. The coordinate partition supplies the reverse bound.

For nonnegative u_i<=1, induction gives product(1-u_i)>=1-sum(u_i). Applying this to u_n=2^(-(n+1)) yields, for every N,

product over n<=N of (1-u_n) >= 1/2 + 2^(-(N+1)).

The decreasing product therefore has limit at least 1/2. Consequently

h(G acting on X) >= (log 2)/2 > 0.

The known exact product formula agrees with Meyerovitch's Lemma 4.2. No numerical approximation is needed to establish positivity.

## 5. Absence of distinct asymptotic pairs

For the product metric, x and y form an asymptotic pair if and only if x-y has finite coordinate support. Indeed, infinitely many differing coordinates yield infinitely many shifts with distance at least 1/2 by moving each difference to coordinate zero. Conversely, if the difference support S is finite, then for each finite coordinate window K there are only finitely many shifts s with (s+S) intersect K nonempty. Outside these shifts the distance is bounded by the summable metric tail, which can be made arbitrarily small.

Suppose z in X has finite support S. Choose a coordinate n outside the supports of every element of S; equivalently, g_n=0 for every g in S. For any g in S and nonzero h in H_n, the element g+h has nonzero n-th coordinate and is outside S. The parity equation on g+H_n reduces to

0=sum over h in H_n of z(g+h)=z(g).

Thus z vanishes at every point of S and is zero everywhere. The only finitely supported point of X is zero. Since x-y belongs to X, every asymptotic pair is diagonal.

## 6. Conclusion and boundaries

All original hypotheses hold and h>0, but no nondiagonal asymptotic pair exists. Therefore the universal equivalence is false, with a previously published counterexample.

The construction is not a counterexample for finitely generated groups. The source reports positive results under additional ring-theoretic or topological hypotheses, but none are assumed by the exact target. The finite-stage entropy ratios alone would not suffice: if all q_n were 2, the ratios would instead equal 2^(-N) and tend to zero. The growing q_n and the rigorous positive infinite-product bound are essential.

There is no remaining gap for the negative answer to the stated universal claim. No assertion is made here about a newly restricted residual question or about proving the surviving implication in greater generality.
