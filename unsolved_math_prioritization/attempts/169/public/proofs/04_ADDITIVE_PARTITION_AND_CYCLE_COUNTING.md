# Stage 4 entropy argument: additive partition functions and exact cycle-counting reduction

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 4.

## Outcome

No nontrivial bound on the original adaptive success probability is proved in this argument. The report uses the actual equations A+T=G throughout; it adds no abstract countermodel.

The strongest established counting statements are:

1. an exact additive partition-function identity in terms of all union sizes |X-A|;
2. a self-contained read-k/Hölder bound for that partition function, including exact-size conditioning;
3. an exact spanning-forest parametrization of representation selections, with every cycle-label consistency constraint retained;
4. a cover-conditioned lower bound on representation multiplicity using the actual autocorrelation identity; and
5. an exactly normalized canonical-cover count combining those ingredients without dividing any multiplicity twice.

The available partition bound suppresses the logarithm by only order k, while the minimization entropy is order k log k. The cycle count has an uncontrolled graph/label enumeration, even after known simple cores are excluded. These are precise missing estimates, not assumed conclusions.

## 1. Model, typicality and notation

Let p tend to infinity through primes, `k=floor(sqrt(p))`, and `c=floor(100 sqrt(p))`. A is uniform among the k-subsets of G=Z/pZ. For a fixed A and an integer t between 0 and p, define

`U(A,T)=p-|A+T|`,

`R_t(A)=min_{|T|=t} U(A,T)`.

Minimizing over exactly t or at most t gives the same residual, by padding. Let `B_t=binom(p,t)` and, for beta>=0, define

`F_t(beta;A)=(1/B_t) sum_{|T|=t} exp(-beta U(A,T))`,

`Z_t(beta;A)=B_t F_t(beta;A)`.

When a typical event is used below, it is the explicitly specified H_p of Stage 3: a finite intersection of the proved autocorrelation/Fourier/energy condition, the specified progression and growing-doubling exclusions, bounded affine-envelope holes, and the specified decoder-family exclusion. Its parameters and codebooks are fixed before A is sampled. It has probability 1-o(1), and it removes the known stratified and Singer simple-core examples. No intersection over every conceivable singleton menu is permitted.

## 2. Exact additive union-size identities

For a fixed A, put

`P_{A,t}(z)=sum_{|T|=t} z^(U(A,T))`.

Then the following polynomial identity holds for every real or complex z:

`P_{A,t}(z)=sum_{X subset G}(z-1)^|X| binom(p-|X-A|,t)`.       (2.1)

A binomial coefficient is zero if its upper parameter is less than t.

Proof: for the hole set H(A,T), expand

`z^|H(A,T)|=sum_{X subset H(A,T)}(z-1)^|X|`.

The condition X subset H(A,T) is exactly `T intersect (X-A)=empty`. There are `binom(p-|X-A|,t)` such T. Interchanging the finite sums proves (2.1).

Consequences include the exact cover count

`N_t(A)=sum_{X subset G}(-1)^|X| binom(p-|X-A|,t)`,             (2.2)

and, for every integer s>=0,

`E_{T uniform t} binom(U(A,T),s)`

` = (1/B_t) sum_{|X|=s} binom(p-|X-A|,t)`.                    (2.3)

Thus actual coverage depends on the full union-size hierarchy, not only pair intersections. Evaluating at z=0 or z=exp(-beta) involves alternating cancellation in the right side of (2.1). Bounding each term separately by its absolute value loses the relevant information.

Commutativity gives the legitimate annealed identity

`E_{A uniform k} F_t(beta;A) = E_{T uniform t} F_k(beta;T)`.

It does not interchange expectation and minimum, and it does not imply the analogous symmetry for E R_t or E log F_t. No such interchange is used here.

## 3. A rigorous Laplace bound and its exact entropy deficit

In this section assume 1<=t<=p-1; the endpoint cases are deterministic and are not needed for the cap. Fix A with |A|=k and let B initially be a Bernoulli centre set with inclusion probability 0<rho<1. For each x define

`I_x=1[B intersect (x-A)=empty]`.

The p windows x-A all have size k, and each centre coordinate belongs to exactly k windows. Each I_x has mean

`u=(1-rho)^k`.

We claim

`E_rho exp(-beta sum_x I_x)`

` <= [1-u+u exp(-beta k)]^(p/k)`.                             (3.1)

### 3.1 Self-contained Hölder/entropy proof

For any product law mu and any law Q on the same finite coordinate space, the regular-window entropy inequality is

`k D(Q||mu) >= sum_x D(Q_(x-A)||mu_(x-A))`.

It follows from the entropy chain rule exactly as in the Stage 1 entropy proof: local entropies sum to at least k times global entropy, while product cross-entropies sum exactly k times their global value.

For arbitrary local functions g_x, the finite variational identity

`log E_mu exp(sum_x g_x) = sup_Q [sum_x E_Q g_x-D(Q||mu)]`

follows by subtracting the relative entropy to the tilted law. Applying the preceding entropy inequality and then separately maximizing each local law gives

`log E_mu exp(sum_x g_x)`

` <= (1/k) sum_x log E_mu exp(k g_x)`.

Take g_x=-beta I_x. Each local expectation is `1-u+u exp(-beta k)`, proving (3.1). This proof does not assume independent holes.

### 3.2 Transfer to exactly t centres

Set `rho=t/p` and let

`b_t=binom(p,t) rho^t(1-rho)^(p-t)`.

Conditioning B on |B|=t gives the exact uniform t-set distribution, so

`F_t(beta;A)`

` <= min(1, b_t^(-1)[1-u+u exp(-beta k)]^(p/k))`.              (3.2)

This is uniform over every k-set A. There is no conditioning approximation.

At t=c, Stirling gives `b_c=(1+o(1))/sqrt(2 pi c)`, while

`u=(1-c/p)^k=exp(-100)(1+O(1/k))`.

For all beta>=0, the logarithmic suppression obtainable from (3.2) is at most

`(p/k)[-log(1-u)]+log b_c`

` = b_100 k+O(log k)`,                                      (3.3)

where `b_100=-log(1-exp(-100))>0`. The factor exp(-beta k) can improve the bound only up to this saturation value.

### 3.3 Why this bound does not control the unrestricted optimum

For beta>0 the exact deterministic inequalities are

`R_t(A)-log B_t/beta <= -log Z_t(beta;A)/beta <= R_t(A)`,      (3.4)

or equivalently

`[-log F_t(beta;A)-log B_t]/beta <= R_t(A)`

`                                           <= -log F_t(beta;A)/beta`.

They follow because one minimizing T contributes exp(-beta R_t), while every one of the B_t terms is at most that value.

At the cap,

`log B_c=(100+o(1))k log k`.

The order-k suppression in (3.3) is smaller than this minimization cost for all sufficiently large p, regardless of beta. Hence (3.2)-(3.4) supply only the trivial lower bound R_c>=0. Averaging does not improve that conclusion.

For the current negative bridge, a sufficient genuinely new estimate would be, along unbounded primes,

`E_A log F_c(beta_p;A)`

` <= -log B_c-beta_p a c sqrt(k)`                             (3.5)

for some fixed a>0. Then (3.4) would give `E R_c>=a c sqrt(k)`, which the audited concentration theorem turns into the required fixed positive failure probability.

A version conditioned on the noncircular H_p is equally possible, with its probability accounted for when passing back to E R_c. Neither version of (3.5) is established.

The opposite free-energy inequality could support the independently proved lower-budget amplification route. The present bound does not provide a mean residual of order p^(3/4) at budget 33k, nor the smaller-order 49k bound required there.

## 4. Counting all representations: the exact graph object

Fix ordered distinct A=(a_1,...,a_k) and T=(t_1,...,t_t), and suppose A+T=G. Put

`f(x)=#{(i,j):a_i+t_j=x}`,

`R(A,T)=product_{x in G} f(x)`.

There are exactly R(A,T) ways to choose one actual representation of each target x. Each selection produces:

- a simple bipartite graph J contained in K_(k,t), with exactly p edges;
- a bijection ell:E(J)->G assigning target label x to its selected edge;
- equations `a_i+t_j=ell(i,j)` for all edges.

The graph is simple because one pair (i,j) cannot represent two different target labels. Conversely, any distinct-coordinate solution of such a bijectively labelled graph gives a cover and one representation selection.

This is a cover-dependent object: it is unavailable for a noncover. No artificial incidence relation is introduced.

## 5. Spanning forests, ranks, and the retained cycle constraints

Let v=k+t and let h be the number of connected components of J, counting isolated vertices. The coefficient matrix of the equations has rank

`v-h`.                                                       (5.1)

Indeed, replace each right variable t_j by -t_j. The matrix becomes an oriented graph-incidence matrix. On each component a spanning tree has rank its number of vertices minus one, and every remaining edge row lies in that span.

Choose a spanning forest. There are v-h forest edges. Assign one root variable in each component and propagate the variables along the forest using its edge labels. A nonforest edge is consistent if and only if the alternating signed sum of labels around its fundamental cycle is zero.

There are exactly

`p-v+h`                                                      (5.2)

independent linear constraints on the edge-label vector. They are the cycle-space equations. They are **not automatically true** merely because the variable matrix has small rank.

For a fixed graph and a fixed edge labelling, the variable system is either inconsistent or has exactly p^h solutions before requiring distinct coordinates and H_p. Equivalently, one may select the v-h forest labels freely, derive all nonforest labels from the cycle equations, and then test whether all p derived edge labels are distinct. Because there are p labels in F_p, distinctness is equivalent to being a bijection onto G.

Thus the missing rarity can reside in the requirement that the induced edge labels form a permutation of F_p. Counting the p equations as independent is wrong; discarding the p-v+h label-consistency equations is also wrong.

### 5.1 Minimality yields a true component bound

If T is inclusion-minimal, every centre has a private target. Every representation selection must use its edge at that target, so no right vertex of J is isolated. Every component therefore contains at least one left vertex. Write its part sizes as a_i>=1 and b_i>=0, with sums k and t.

Since J has p edges,

`p <= sum_i a_i b_i`

`   = t+sum_i(a_i-1)b_i <= (k-h+1)t`.

Consequently

`h <= k+1-ceil(p/t)`.                                       (5.3)

One can choose all component roots among the A vertices. At the cap, this saves approximately k/100 root values compared with k, but leaves approximately 99k/100 roots. The graph, forest labels, and association of root values with components are additional advice; their descriptions are not free. In particular, (5.3) does not supply the sublinear-seed/sublinear-advice compression premise from Stage 3.

## 6. Cover-conditioned representation multiplicity from autocorrelation

Let `L=max_{d!=0} r_A(d)`. The actual convolution identity gives

`(1/p)sum_x f(x)^2`

` = [kt+sum_{d!=0} r_A(d)r_T(d)]/p`

` <= lambda+L t(t-1)/p`,                                    (6.1)

where `lambda=kt/p`.

For a cover, f(x)>=1 everywhere. Suppose lambda>1 and view x as uniform in G. The nonnegative variable Y=f(x)-1 has mean lambda-1 and second moment at most the right side of (6.1). Paley-Zygmund gives

`Pr_x[Y >= (lambda-1)/2]`

` >= (lambda-1)^2 / [4(lambda+L t(t-1)/p)]`.

On these points, `log f(x)>=log((lambda+1)/2)`. Therefore every such genuine cover satisfies

`log R(A,T)`

` >= p (lambda-1)^2 log((lambda+1)/2)`

`       / [4(lambda+L t(t-1)/p)]`.                            (6.2)

At t=c, lambda tends to 100. On the proved usual event `L=O(log p/log log p)`, this gives

`log R(A,T) >= Omega(p/L)`.

This is an actual cover-conditioned lower bound, not a Poisson assumption or a claim about independently chosen witnesses. It counts the many representation selections of each pair (A,T). It does not count distinct T, and it does not by itself compress A.

The general formula is retained because a minimum cover can have t much smaller than c. Padding a cover to c changes its witness multiplicity and cannot be silently inserted into a minimal-witness count.

## 7. Exact canonical-cover normalization

Fix a deterministic canonical minimum cover selector K(A), using a fixed lexicographic tie-break, whenever R_c(A)=0. This is a mathematical definition, not a claimed small-description decoder.

For each t<=c, let J run over p-edge subgraphs of K_(k,t), let ell run over bijections E(J)->G, and let Sol(J,ell) be the ordered solutions of its equations with coordinates distinct within each part. For a solution, A and T denote the corresponding unordered sets.

Then the target probability restricted to H_p is exactly

`P_p(H_p and R_c=0)`

` = [1/(binom(p,k) k!)] sum_{t<=c} [1/t!]`

`     * sum_J sum_ell sum_{(a,t) in Sol(J,ell)}`

`          1[A in H_p and T=K(A)] / R(A,T)`.                  (7.1)

Terms with kt<p have no graph and contribute zero. Every solution of a bijectively labelled graph is already a cover, so its denominator is positive.

To verify (7.1), fix one successful unordered A and its one canonical unordered T. There are k!t! orderings and exactly R(A,T) representation selections for each ordering. Each selection contributes 1/R(A,T). The prefactors therefore count A exactly once, followed by division by binom(p,k).

The representation multiplicity is divided **once**. There is no additional division by the number of covers because canonical selection has already removed that multiplicity. If one instead sums all minimal T, the separate factor 1/m_c(A) from Stage 3 is required, but it is a different multiplicity.

Equation (7.1), combined with the spanning-forest description in Section 5, is an exact additive counting route. H_p and canonicality must remain inside the solution count. Removing them to use a loose upper bound can reintroduce precisely the simple exceptional cores excluded by the task.

## 8. What the elementary cycle count actually bounds

For a fixed graph J with h components, there are at most p^(v-h) cycle-consistent edge-label vectors. Requiring a bijection can only reduce this number. Each has at most p^h variable solutions. Thus the elementary bound on labelled solutions for one graph is at most p^v.

There are at most `binom(kt,p)` graphs. This estimate retains the cycle rank but discards the rare requirement that all induced labels be distinct, and also discards H_p and canonicality. At t~100k,

`log binom(kt,p) = [100 H(1/100)+o(1)]p`,

where H is binary entropy in natural logarithms. This is order p, much larger than k log k. Even the representation lower bound (6.2) only removes order p/L from this particular bound; it does not overcome the positive order-p graph entropy when L grows.

There is also the deterministic arithmetic-geometric-mean bound `R(A,T)<=lambda^p`. Combining a loose global count with that upper bound and then dividing by (6.2) likewise gives no useful probability estimate. Representation multiplicity can be subtracted only after the weighted labelled-solution count has been controlled; it is not a free saving against input entropy.

A genuinely new sufficient estimate would upper-bound the actual H_p-restricted, canonical, bijectively labelled cycle-consistent sum in (7.1) by `(1-epsilon) binom(p,k) k!` with the t! factors retained, along unbounded primes. An o(1) fraction would be stronger. No such estimate is obtained here.

## 9. Exact frontier

The actual-additive results in this pass do not yield either E R_c>=a c sqrt(k) or a sufficiently small lower-budget mean for the positive amplification route.

What is now explicit is where a counting proof has to improve:

- the read-k Laplace inequality loses a factor of log k relative to minimization entropy;
- the exact union-size polynomial requires high-order alternating information;
- the spanning forest handles variable rank, but the permutation-valued edge labels carry consistency and distinctness information not yet estimated on H_p;
- genuine covers have many representation selections, but graph/label enumeration must be divided by that multiplicity exactly once;
- canonicality removes duplicate covers without estimating the probability of the remaining solution families.

No additional simple algorithm subclass is presented as a solution. No known exceptional A is claimed to survive H_p. The original adaptive event remains unresolved.

