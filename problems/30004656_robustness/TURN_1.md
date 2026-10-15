# Turn 1: exact optimal Lipschitz interpolation on the random circle

First substantive turn. Original unrestricted two-layer conjecture remains unresolved. This turn treats the unambiguous spherical model in ambient dimension d=2, for every width and every activation, by proving an exact law for the optimal Lipschitz constant among ALL interpolating functions. It is a geometric partial result, not an arbitrary-dimensional neural-network theorem. Uniform spacings, Dirichlet simplex volumes, Chernoff bounds and the McShane extension formula are classical tools; no historical novelty is certified.

## 1. The deterministic optimum

Let n≥2 distinct points x_i lie on the unit circle S¹ and have labels y_i∈{-1,+1}. Define L_* to be the smallest Lipschitz constant, for Euclidean chord distance on S¹, of any real-valued function interpolating these labels. If all labels agree, L_*=0. Otherwise

    L_*=2/min{||x_i-x_j|| : y_i≠y_j}.                     (1)

Every interpolant satisfies this lower bound by the Lipschitz inequality. It is attained: on the finite data set the labels have exactly that Lipschitz constant, and

    F(x)=min_i [y_i+L_*||x-x_i||]

extends the labels to all of R² with the same constant. Each summand is L_*-Lipschitz, and taking a finite minimum preserves that property; the finite-data inequalities show F(x_i)=y_i. Clipping to[-1,1] also preserves interpolation and the constant. No claim that this particular extension has a prescribed two-layer architecture is made.

Write the cyclic spacings as s_1,...,s_n, normalized so they sum to1. Mark the edges whose endpoint labels differ, and let J be their number. If both signs occur then J is positive and even. Set T=min{s_i:edge i is marked}. Then

    0<T≤1/J≤1/2,       L_*=1/sin(πT).                    (2)

Indeed the shorter circular arc between any opposite-label pair crosses at least one marked edge, so its normalized length is at least T. A marked edge attaining T supplies an opposite-label pair at that distance, and T≤1/2 ensures it is the shorter arc. Chord length is2sin(π times shorter normalized arc length), proving(2).

## 2. Exact random-spacing law

Now let x_i be independent uniform on S¹ and y_i independent uniform random signs, independent of all x_i. Distinctness holds almost surely. Root the cyclic order at x_1, rather than at the deterministic angle zero. After rotation by the angle of x_1, the other n-1 angles remain independent uniform. Their ordered spacings, including the wraparound spacing, are uniformly distributed on the simplex

    s_i>0, sum_i s_i=1,

that is, Dirichlet(1,...,1). This rooted choice avoids the size-biased gap containing a fixed deterministic origin. The cyclic labels remain independent random signs and are independent of the spacings.

Choosing the set of flip edges and a starting sign determines all cyclic labels if and only if the number of flips is even. Therefore

    P(J=j)=2^{1-n} binom(n,j) for even j,                 (3)

and it is zero for odd j. In particular P(J=0)=2^{1-n}.

Conditional on J=j>0, the marked set is independent of the spacings. By their exchangeability we may fix any j coordinates. For t≥0, translating each of those j coordinates down by t leaves a simplex of total mass1-jt; its dimension is n-1. Thus

    P(T>t | J=j)=(1-jt)_+^{n-1}.                         (4)

This is an exact identity, including zero probability once jt≥1. No independence of the spacings is claimed.

Combining(2)–(4), for every u≥1 the exact distribution of the optimal Lipschitz constant is

    P(L_*≤u)=2^{1-n}
       +2^{1-n} sum_{2≤j≤n, j even}
          binom(n,j) [1-(j/π)arcsin(1/u)]_+^{n-1}.        (5)

For0≤u<1 the CDF is just2^{1-n}; foru<0 it is zero. At u=1 the same formula applies and has no additional atom. All equal labels give the atom at0. In particular there is no fixed-width or activation assumption hidden in the distribution.

## 3. A high-probability lower bound, uniform over every network

The law(3) is Binomial(n,1/2) conditioned on even parity; that parity has probability1/2. The standard Chernoff bound gives

    P(J<n/4)≤2 exp(-n/16).                                (6)

For J≥n/4, formula(4) implies

    P(T>t | J)≤exp[-(n-1)nt/4],

with the inequality still true if Jt≥1 because the left side is zero. Fix any A>0 and put

    t=8(A+1)log n/n².

For all sufficiently large n this is at most1/2. Since (n-1)/n≥1/2, the last exponential is at most n^{-(A+1)}. On the complementary good event, sin(πT)≤πT≤πt, so

    L_*≥ n²/[8π(A+1)log n]                               (7)

with probability at least

    1-2exp(-n/16)-n^{-(A+1)}.                             (8)

On this single event every interpolating function on S¹, hence every interpolating two-layer network of any width and any fixed or data-dependent activation, obeys(7). This is stronger than c sqrt(n/k) for all k≥1 when n is sufficiently large, with A fixed. Thus the source lower-bound statement holds in this fixed d=2 spherical regime without an architectural restriction.

This does not imply that few neurons suffice to attain L_*, and says nothing about the Gaussian/global-norm regime or growing d. The source's O(1)-Lipschitz overparameterized construction is stated for high-dimensional separated data, such as n polynomial in growing d; the large-n fixed-circle result does not contradict it. Here even unconstrained interpolation is intrinsically nonrobust because opposite labels become very close.

## 4. Scope and next gap

The exact law isolates the geometric obstruction in a low-dimensional source case. It does not establish the conjectured width-dependent lower bound in the difficult high-dimensional overcomplete regime. The recent piecewise-linear arbitrary-weight preprint's restriction d≥3 concerns its kink-rigidity method, not a failure of elementary geometric lower bounds on the circle. No unaudited claim from that preprint is needed here.

The checker enumerates finite cyclic label patterns and rational angular configurations, and verifies the exact transition law and simplex-tail expressions. Infinite probability assertions follow from the written spacing argument. Original unresolved1/5.
