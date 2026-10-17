# Stage 2 entropy argument: pseudorandom typicality does not remove all efficient-cover domination

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 2.

## Outcome and scope

The unrestricted target remains unresolved. This report proves a specific obstruction to a natural typical-A truncation. It does not claim that every possible typical-A truncation fails.

There is an explicit event Good(A), having probability tending to one in the exact uniform model, that imposes all three of the following:

- nonzero autocorrelations of order at most log p / log log p;
- Fourier coefficients of order at most sqrt(k log p);
- additive energy at most 3k^2+o(k^2), the ordinary random leading scale.

Nevertheless, there are exp(k log k+O(1)) sets A in a simple stratified family, almost all satisfying Good, and every one is covered by the same interval of 2k+O(1) translates. Consequently, the unweighted cap-sized cover count still has divergent first moment after truncation to Good:

`E[1_Good(A) N_c(A)] >= exp((98+o(1)) k log k)`.

One can also require every counted T to have both large sumset and large difference set, with doubling ratio at least `(1/500+o(1))k`; the truncated first moment still diverges at rate at least `exp((97+o(1))k log k)`.

These latter witnesses are redundant extensions of a short interval cover. The result does not defeat simultaneously requiring inclusion-minimal T and excluding A that admit simple covers. This is the precise remaining boundary, not an omitted hypothesis.

## 1. Exact model and the event Good

Let p tend to infinity through primes, `k=floor(sqrt(p))`, `c=floor(100 sqrt(p))`, and G=Z/pZ. Let P denote the uniform law on k-subsets A of G.

For nonzero d define `r_A(d)=|A intersect (A+d)|`. Let

`S_A(xi)=sum_{a in A} exp(2 pi i xi a/p)`,

and let additive energy be

`E(A)=#{(a,b,c,d) in A^4 : a+b=c+d} = sum_d r_A(d)^2`.

For all sufficiently large p set

`h=ceil(3 log p / log log p)`.

Define Good(A) by the simultaneous inequalities

`max_{d!=0} r_A(d) < 3h`,                              (1.1)

`max_{xi!=0} |S_A(xi)| <= 1+4 sqrt(k log p)`,            (1.2)

`E(A) <= 3k^2+k^(7/4)`.                               (1.3)

All logarithms are natural. The conclusions below concern these exact thresholds; the small-prime numerical tests are not substituted for their asymptotics.

## 2. A second sampling law with the same typicality

Write `p=kL+r`, where `L=floor(p/k)` and `0<=r<k`. Partition the representatives 0,...,p-1 into k consecutive cells: r have length L+1 and the others length L. Let H be the family of A containing exactly one point in each cell. Let Q be the law obtained by selecting one point independently and uniformly in each cell.

Q is uniform on H, and

`|H|=L^(k-r)(L+1)^r`.

Since every cell has length at least k, under Q any prescribed set of v distinct vertices has inclusion probability at most k^(-v). If two prescribed vertices lie in one cell, its probability is zero. Under P the corresponding probability is

`(k)_v/(p)_v <= (k/p)^v <= k^(-v)`.                    (2.1)

We prove that both `P(Good)` and `Q(Good)` tend to one.

### 2.1 Autocorrelations

For a fixed nonzero d, the unordered edges `{x,x+d}` form a simple graph of maximum degree two. If r_A(d) is at least 3h, the selected edges contain a matching of size h: choosing one edge and deleting it and its incident edges removes at most three edges at each step.

There are at most binom(p,h) choices of h edges. Requiring their 2h distinct endpoints has probability at most k^(-2h), under either law by (2.1). Thus

`Pr[r_A(d)>=3h] <= binom(p,h) k^(-2h)`.

Union over d gives

`Pr[(1.1) fails] <= p [ep/(h k^2)]^h = p^(-2+o(1))`.  (2.2)

This proof never assumes the overlapping edge indicators are independent.

### 2.2 Fourier coefficients

Under Q, a Fourier sum is a sum of k independent complex variables of modulus one. Its expectation has modulus at most one. Indeed, subtracting 1/L times the full nontrivial character sum, which is zero, leaves only the longer cells. Their contribution has absolute value at most

`r(L+1)/(L(L+1)) = r/L <= 1`.

Applying Hoeffding separately to real and imaginary parts, each with summand range length at most two, gives

`Q[|S_A(xi)-E_Q S_A(xi)|>=u] <= 4 exp(-u^2/(4k))`.

With `u=4 sqrt(k log p)`, union over xi yields failure probability at most `4p^(-3)` for (1.2).

For P, start instead with k independent uniform points of G. Their Fourier sum has expectation zero and satisfies the same tail bound. The probability that all points are distinct is at least

`1-binom(k,2)/p > 1/2`,

by the union bound on collisions. Conditioning on distinctness gives the uniform k-subset law, so the failure probability for (1.2) is at most `8p^(-3)`.

### 2.3 Additive energy: expectation and variance counts

Let X_3 and X_4 count ordered solutions a+b=c+d having exactly three and four distinct vertices, respectively. Since p is odd, the solutions with at most two distinct vertices contribute exactly `2k^2-k`. Hence

`E(A)=2k^2-k+X_3+X_4`.                               (2.3)

There are exactly `2p(p-1)` ordered three-distinct solutions in G: either a=b and c,d are the other two vertices, or c=d and a,b are the other two. There are at most p^3 four-distinct solutions. Equation (2.1) therefore gives, under either P or Q,

`E X_3 <= 2p(p-1)/k^3 = O(k)`,

`E X_4 <= p^3/k^4 = k^2+O(k)`.                       (2.4)

We next prove

`Var X_4 = O(k^3)`                                   (2.5)

under both laws, with absolute implied constants.

For two four-distinct tuples with disjoint vertex sets, their inclusion indicators have nonpositive covariance. Under P this follows from

`(k)_8/(p)_8 <= [(k)_4/(p)_4]^2`.

Under Q, either the block supports are disjoint, giving independence, or there is a shared block containing different required vertices, giving joint probability zero. Tuples individually incompatible with the block partition already have zero probability.

It remains to bound pairs of tuples sharing j actual vertices, 1<=j<=4. There are only an absolute finite number of overlap identification patterns.

For j<4, there are v=8-j distinct variables. The two additive equations have rank two over F_p: their supports differ and each coefficient vector has four nonzero coefficients, so they cannot be proportional. Thus each identification pattern admits at most p^(v-2) assignments. Every actual assignment with v distinct vertices has inclusion probability at most k^(-v). Its contribution is therefore at most

`O(p^(v-2) k^(-v)) = O(k^(4-j))`.

When j=4, choose the first additive tuple in at most p^3 ways and permute its four vertices for the second tuple in only constantly many ways. The contribution is `O(p^3 k^(-4))=O(k^2)`.

Dropping the nonpositive disjoint covariances and using covariance at most joint probability on overlapping pairs proves (2.5). Accidental extra coincidences in the rank-two assignment count only enlarge the counting upper bound; actual v-distinct configurations are the ones to which (2.1) is applied.

Chebyshev now gives

`Pr[X_4 > k^2+(1/2)k^(7/4)] = O(k^(-1/2))`,

since the O(k) difference between the mean upper bound and k^2 is negligible relative to k^(7/4). Markov gives

`Pr[X_3 > (1/2)k^(7/4)] = O(k^(-3/4))`.

Together with (2.3), these prove (1.3) with probability tending to one under both P and Q. Equations (2.2)-(2.5) establish

`P(Good)=1-o(1)` and `Q(Good)=1-o(1)`.                 (2.6)

For context, the exact uniform model actually has E(A)/k^2 tending to 3 in probability: the number of four-distinct ambient solutions is p^3+O(p^2), and the corresponding exact inclusion probability gives E X_4=(1+o(1))k^2. This observation is not needed for the obstruction.

## 3. Every stratified A has a short fixed cover

Let

`m=2 ceil(p/k)-1`, `T0={0,...,m-1}`.

The cyclic gap between consecutive points of an A in H is at most m. Indeed, the points occupy consecutive cells of length at most ceil(p/k), and the largest gap from one chosen point to the next is at most the sum of two cell lengths minus one. The same argument applies across the wrap-around boundary.

An interval of m consecutive residues, translated by those points of A, therefore covers every residue. Thus

`A+T0=G for every A in H`, and `m=2k+O(1)<c`.          (3.1)

The exact uniform probability of H is

`P(H)=|H|/binom(p,k)`.

As in the Stage 1 interval calculation,

`P(H) >= floor(p/k)^k/binom(p,k) >= exp(-k-2)`.        (3.2)

Since Q is precisely P conditioned on H, (2.6) gives

`P(Good and A+T0=G) >= P(Good and H)`

`                         >= (1-o(1)) exp(-k-2)`.    (3.3)

Thus even after the joint low-correlation, Fourier, and energy truncation, a uniform fixed-T bound of the form exp(-omega(k)) is false.

The family here is much richer than the single interval A used in Stage 1. It has

`log|H|=k log k+O(1)`.

Equivalently, its conditional distribution Q has relative entropy

`D(Q||P)=-log P(H)=k+O(log k)`.

These are exact counting observations. They do not imply that Good captures every relevant kind of typicality.

## 4. The truncated cap-sized cover first moment still diverges

Let `N_c(A)=#{T subset G: |T|=c, A+T=G}`. Every c-element superset of T0 covers every A in H. Consequently

`N_c(A)>=binom(p-m,c-m)` for A in H.

Multiplying by the probability of Good intersect H gives

`E_P[1_Good N_c] >= (1-o(1)) exp(-k-2) binom(p-m,c-m)`.

Since `p=k^2+O(k)`, `m=2k+O(1)` and `c=100k+O(1)`,

`log binom(p-m,c-m)=(98+o(1))k log k`.

Therefore

`E_P[1_Good N_c] >= exp((98+o(1))k log k) -> infinity`. (4.1)

This is a lower bound on the exact truncated first moment. Improving estimates for that same sum cannot make it tend to zero.

It is not a lower bound on the probability of the target event. The efficiently coverable subfamily has exponentially small uniform probability, and is being counted many times by its many witnesses.

## 5. Requiring large sumsets and difference sets of T does not repair this count

There exists a fixed k-set R in G with additive energy at most 4k^2 for all sufficiently large p. This follows directly from the uniform expectation estimate (2.3)-(2.4), which is at most 3k^2+O(k).

Cauchy-Schwarz applied to sum and difference representation counts gives

`|R+R|>=k^4/E(R)>=k^2/4`,

`|R-R|>=k^4/E(R)>=k^2/4`.

For sufficiently large p these lower bounds are at least p/5. Fix one such R, and let S=T0 union R. Then `|S|<=3k+O(1)`. Extend S, if necessary, to a fixed set S' of size `3k+3`; the bound m<=2k+3 makes this possible for large p.

Every c-element T containing S' covers every A in H, and every such T satisfies

`|T+T|>=p/5`, `|T-T|>=p/5`,

hence

`|T+T|/|T| >= p/(5c) = (1/500+o(1))k`.               (5.1)

There are `binom(p-(3k+3),c-(3k+3))` such T. Thus the expected number of these large-doubling covers, still restricted to Good(A), is at least

`exp((97+o(1))k log k)`.                             (5.2)

This demonstrates why classifying arbitrary witnesses solely by the size of their sumsets or difference sets does not automatically remove domination: a redundant high-doubling witness can contain a simple covering core.

## 6. What this proves and what it leaves open

The following proposed estimate is false for the explicit whp event Good in Section 1:

`sum_{|T|=c} P(Good(A) and A+T=G)=o(1)`.

It remains false after restricting the sum to T satisfying (5.1). The weaker proposed claim that every fixed T has covering probability exp(-omega(k)) after this Good truncation is also false by (3.3).

This result does not rule out a stronger, independently proved typical event. For example, Stage 1's fixed-menu theorem shows that with high probability A has no cap-sized arithmetic-progression cover at all. Intersecting Good with that event removes every A in H, since T0 is an interval. Likewise, this report does not prove divergence after restricting to inclusion-minimal covers while simultaneously excluding A with simple covering cores.

A remaining negative route would therefore need a joint statement such as:

- establish a noncircular whp event H* excluding the efficient exceptional structures relevant to all witness types;
- prove an exhaustive structural/compression theorem for inclusion-minimal covers of A in H*; and
- bound the resulting probability/count, with all adaptive dependence retained.

No such exhaustive theorem or bound is established here. The Stage 2 contribution is a concrete, jointly pseudorandom counterexample family showing that the standard autocorrelation/Fourier/energy information alone cannot be that missing theorem.

