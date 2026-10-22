# Stage 5 entropy: exact permutation-cycle counting and the final weighted frontier

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 5.

## Result

The original covering probability is not resolved. This argument directly counts actual additive representation graphs, rather than excluding another proposed algorithm or replacing addition by an abstract incidence relation.

The new proved results are:

1. Exact Fourier and collision-partition formulas for permutation-valued solutions of all the graph's cycle equations.
2. An exponential sparsity bound for the graphs that admit any genuine additive covering realization. At the operational cap their fraction among all p-edge graphs is at most `exp[-(0.994983...+o(1))p]`.
3. An exact obstruction to a graph-by-graph independent-cycle approximation: every feasible graph needs an exponentially large nonzero Fourier contribution relative to the zero mode.
4. A sharper cover-conditioned representation-multiplicity bound, improving the previously proved `Omega(p/L)` logarithm to `Omega(p log L/L)` under the usual codegree bound L.
5. An exactly normalized count using one explicitly chosen cap-sized cover per successful A. Its weight and the graph count remain coupled; the available separate estimates still give only the trivial upper bound one.

No original probability bound bounded away from one, no required residual expectation estimate, and no affirmative exact-budget construction follows. The final unproved weighted inequality is stated in Section 8.

## 1. Exact model and graph notation

Let p tend to infinity through primes. Set

`G=F_p`, `k=floor(sqrt(p))`, `c=floor(100 sqrt(p))`.

A is uniform on the k-subsets of G, and its translating set may depend arbitrarily on A. The target event is

`E_p={there is T, |T|<=c, A+T=G}`.

All statements using c-subsets assume p is sufficiently large that `k,c<p`. This loses no prime tail. Because a cover can be padded, E_p is exactly the event of a cover with cardinality c. This observation will be used with an explicitly cap-sized canonical selector; it will not be inserted into a count of minimal covers.

For general integers `k,t>=2`, `k,t<p`, and `kt>=p`, let J be a p-edge subgraph of the labelled bipartite graph K_(k,t). Write `v=k+t`, let h count all components including isolated vertices, and set `r=v-h`. Its p-by-v plus-incidence matrix B over F_p has a 1 at each edge's left and right endpoint. Changing the signs of all right columns turns it into an oriented incidence matrix, so

`rank(B)=r`.

For a vertex tuple `z=(a_1,...,a_k,t_1,...,t_t)`, the edge label vector is `Bz`, with label `a_i+t_j` on edge (i,j). Let

`N_J=#{ell:E(J)->F_p bijective : ell belongs to im(B)}`.

This N_J does not impose distinct coordinates within the vertex parts. Membership in im(B) retains every alternating cycle equation. Each label vector in im(B) has exactly `p^h` preimages. Therefore

`Q_J^all := #{z in F_p^v : Bz is a permutation of F_p} = p^h N_J`.  (1.1)

Let `D_(k,t)` instead denote tuples with distinct coordinates within each part, and define

`Q_J = #{z in D_(k,t) : Bz is a permutation of F_p}`.

Thus `Q_J<=Q_J^all`; one must not treat them as equal. Every tuple counted by Q_J is a true covering pair. Conversely, for a distinct-coordinate pair put

`f_z(x)=#{(i,j):a_i+t_j=x}`, `R_z=product_(x in F_p) f_z(x)`.

The product is zero for a noncover. For a cover it counts exactly the representation selections, one pair for each target. Each selection gives one J with all p edge sums distinct, with no additional choice of an edge label once z is fixed.

Consequently, the exact incidence identity is

`sum_(J:|E(J)|=p) Q_J = sum_(z in D_(k,t)) R_z`.                 (1.2)

This identity is the basis of the graph-sparsity result below. It also explains why the multiplicity cannot be divided out twice.

## 2. Exact permutation Fourier formula

Fix an ordering of the p edges and put `omega=exp(2 pi i/p)`. For `xi in F_p^p`, define the normalized Fourier coefficient of the uniform permutation law by

`C_p(xi)=(1/p!) sum_(ell permutation of F_p) omega^(xi dot ell)`.

Let `V_J=ker(B^T)`, whose dimension is `q=p-r`. Orthogonality gives, for every y in F_p^p,

`1[y in im(B)] = p^(-q) sum_(xi in V_J) omega^(xi dot y)`.

Indeed, the sum is p^q when y annihilates V_J, and zero otherwise. Summing over all permutation vectors gives the exact formula

`N_J = p! p^(-q) sum_(xi in V_J) C_p(xi)`.                    (2.1)

The sign convention is plus in both Fourier exponents; replacing both by minus gives the same formula. The entire sum in (2.1) is real and nonnegative. Individual Fourier coefficients are not assumed nonnegative or small. The term xi=0 equals one. No cycle constraint has been omitted or declared independent.

### A fully finite collision-partition formula

For a set partition pi of E(J), choose a reference edge in each block. Let D_pi have rows `e_e-e_reference` for all other edges in that block. Define

`mob(pi)=product_(blocks C of pi) (-1)^(|C|-1)(|C|-1)!`.

Partition-lattice inclusion-exclusion gives

`Q_J^all = sum_(pi partitions of E(J)) mob(pi) p^(v-rank_(F_p)(D_pi B))`. (2.2)

Proof: for an arbitrary edge-label vector y, the sum of mob(pi) over partitions whose blocks have constant y equals one if all labels are distinct and zero otherwise. For a given pi, vertex tuples satisfying these equalities are the kernel of D_pi B, of the displayed size. Summing over z proves (2.2). Since there are p distinct labels in a field of p elements, distinctness means being a permutation.

All ranks are taken in characteristic p. Replacing them by characteristic-zero ranks without checking is not permitted. Formula (2.2) involves substantial alternating cancellation; bounding its summands by their absolute values discards precisely the permutation information.

For completeness, the corresponding exact Fourier coefficient itself has the collision expansion

`p! C_p(xi) = sum_pi mob(pi) p^|pi| product_(C in pi) 1[sum_(e in C) xi_e=0]`. (2.3)

This follows by applying the same inclusion-exclusion to the exponential sum and summing the common label on each block. Equations (2.1)-(2.3) are exact finite additive counts, not probability estimates for the original event.

## 3. A genuine obstruction to the independent-cycle approximation

If N_J is nonzero, then

`N_J >= p(p-1)`.                                             (3.1)

To see this, start with any consistent permutation ell. Every `s ell+b 1`, with `s!=0` and b in F_p, is again a permutation in im(B): the all-ones edge vector is in im(B), obtained by setting all left variables to 1 and all right variables to 0. These `p(p-1)` label vectors are distinct, since a permutation takes at least two distinct values. The action is free, so N_J is in fact divisible by p(p-1).

Now take `k=floor(sqrt(p))` and `t<=c`. The xi=0 contribution in (2.1) is

`Z_J=p! p^(-(p-r))`.

By Stirling and `r<=k+t=O(sqrt(p))`, uniformly over these graphs,

`log Z_J=-p+O(sqrt(p) log p)`.                               (3.2)

In particular, Z_J tends to zero exponentially. On every feasible graph, however, (2.1) and (3.1) force

`sum_(xi in V_J, xi!=0) C_p(xi)`

` >= p(p-1) p^(p-r)/p! - 1`

` = exp[p-O(sqrt(p) log p)]`.                                (3.3)

The inequality concerns the real total, not a termwise sign claim.

Thus a uniform assertion that permutation labels satisfy the q cycle constraints with probability approximately p^(-q), or that nonzero modes give only a subexponential relative correction, is impossible on any compatible graph in this regime. It would produce a positive count below one. This is an actual algebraic/integrality obstruction for the additive graph object, not an abstract model.

This does not refute an averaged graph theorem, nor a theorem proving that almost all graphs have zero count. On the contrary, the next section proves exponential sparsity of compatible graphs. A useful argument must count that exceptional graph support and its weights together. The fact that a hypothetical solution belongs to a high-probability input event H_p does not turn its compatible graph into an independently labelled generic graph.

## 4. Exponential sparsity of genuinely realizable graphs

Let

`G_real(k,t,p)={J subset K_(k,t): |E(J)|=p, Q_J>0}`,

and `lambda=kt/p>=1`. Then

`|G_real(k,t,p)| <= (p)_k (p)_t lambda^p / [p^2(p-1)]`,       (4.1)

where `(p)_s=p(p-1)...(p-s+1)`.

First, the arithmetic-geometric-mean inequality gives `R_z<=lambda^p` on a cover, because `sum_x f_z(x)=kt`; the same upper bound holds for the zero product on a noncover. Equation (1.2) therefore gives

`sum_J Q_J <= (p)_k(p)_t lambda^p`.                          (4.2)

Second, every feasible graph admits at least `p^2(p-1)` distinct-coordinate vertex tuples. From one tuple apply

`a_i -> s a_i+u`, `t_j -> s t_j+w`,

for `s!=0` and u,w in F_p. All edge sums undergo the same invertible affine map, and distinctness within each part is preserved. The action on ordered tuples is free: two distinct left coordinates force s=1 for a stabilizer, then u=w=0. Thus `Q_J>=p^2(p-1)` whenever Q_J>0. Combining this with (4.2) proves (4.1).

There are exactly `binom(kt,p)` p-edge graphs. Suppose t is of order sqrt(p) and lambda stays in a compact subinterval of `(1,infinity)`. Stirling gives

`log binom(kt,p)=lambda p H(1/lambda)+O(log p)`.

Consequently,

`|G_real| / binom(kt,p)`

` <= exp[-d_lambda p+O(sqrt(p) log p)]`,                      (4.3)

where

`d_lambda=lambda H(1/lambda)-log lambda`

`         =-(lambda-1)log(1-1/lambda)>0`.

At t=c, lambda tends to 100 and

`d_100=-99 log(99/100)=0.9949832495...`.

The fixed-lambda entropy expansion is not asserted uniformly as lambda approaches 1. The exact bound (4.1) remains valid there.

An exact slightly stronger replacement for lambda^p in (4.1) is available. Write `q0=floor(lambda)` and `s=kt-p q0`. The integer maximum of a product of p positive integers with total kt is

`q0^(p-s)(q0+1)^s`.

Pairwise balancing of any two entries differing by at least two proves this maximum. This sharpening does not alter the cap's leading order-p exponent.

### Optional separate refinement for minimal pairs

An inclusion-minimal t-centre cover has at least t distinct private targets, all with f=1. For `t<p`, removing any t such targets and applying AM-GM to the remainder yields

`R_z <= [(kt-t)/(p-t)]^(p-t)`.                              (4.4)

The same affine action preserves minimality, so (4.1) for graphs admitting a minimal pair may use this smaller product bound. For fixed lambda>1 and t=O(sqrt(p)), its logarithm is

`p log lambda - t[log lambda-1+1/lambda] + O(t^2/p)`.

This saves order t, not the remaining order-p entropy. Formula (4.4) will not be applied to the cap-sized canonical selector below, because padding need not preserve minimality.

The sparsity theorem is unconditional, but its random object is J, not the uniformly sampled A in the original problem. A graph support count by itself cannot be substituted for the desired random-A probability.

## 5. Sharper representation multiplicity from the actual additive second moment

Fix any genuine cover by distinct sets A,T, with |A|=k, |T|=t and `lambda=kt/p>1`. Let

`L=max_(d!=0) |A intersect(A+d)|`,

`mu=lambda-1`,

`V=L t(t-1)/p-lambda+1`.

The actual additive identity gives

`(1/p)sum_x f(x)^2`

` = [kt+sum_(d!=0) r_A(d)r_T(d)]/p`

` <= lambda+L t(t-1)/p`.

For uniform x put Y=f(x)-1. Coverage ensures Y>=0; `E Y=mu>0`. Write `nu=E Y^2`. Thus

`mu^2<=nu<=V`,

so V is necessarily positive for any such cover. The bound below is asserted on actual covers; parameters with `V<mu^2` cannot describe one.

Define `phi(y)=log(1+y)/y` for y>0 and phi(0)=1. Its integral representation

`phi(y)=integral_0^1 (1+s y)^(-1) ds`

shows that phi is convex on `[0,infinity)`. Under the size-biased law with density Y/mu, Jensen gives

`E log(1+Y)=mu E_size-biased phi(Y)`

` >= mu phi(nu/mu)`

` = (mu^2/nu) log(1+nu/mu)`.

For fixed mu>0, the function `g_mu(x)=(mu^2/x)log(1+x/mu)` is decreasing for x>0. This follows from `log(1+u)>u/(1+u)` for u>0. Substituting `nu<=V` therefore proves

`log R_z >= p (mu^2/V) log(1+V/mu)`.                        (5.1)

This argument is entirely cover-conditioned and uses the real convolution; it makes no Poisson, independent-witness, or unconditioned-moment assumption.

At t=c, lambda tends to 100. For definiteness take the previously established typical bound with `L_p=3 ceil(3 log p/log log p)` for sufficiently large p; the Stage 2 Good event has `L<L_p`. Use `V_p=L_p c(c-1)/p-lambda+1`. The guaranteed bound is

`log R_z >= Omega(p log L_p/L_p)`.                           (5.2)

This improves Stage 4's `Omega(p/L_p)` lower bound by a logarithmic factor. It is still o(p). Jensen is sharp for a nonnegative Y supported on 0 and one positive value; that observation only describes the moment inequality, and makes no claim that such profiles factor as actual additive convolutions.

When lambda=1, a covering profile must be identically one, R_z=1, and (5.1) is replaced by that direct statement. The cap has lambda>1 eventually.

## 6. Exactly normalized cap-canonical weighted count

Fix any one of the previously justified noncircular typical events H_p, with `P(H_p)=1-o(1)` and its explicitly predetermined parameters. No intersection over all conceivable decoder menus is taken. In particular, H_p can include the previously proved autocorrelation bound used in Section 5.

For each successful A, choose K_c(A) to be the lexicographically first c-subset T satisfying A+T=G. This is an explicitly cap-sized selector. It is a deterministic definition, not a low-description decoding theorem. It need not be affine invariant.

For each p-edge graph J in K_(k,c), define

`W_J = sum_(z in D_(k,c), B_J z a permutation)`

`       1[A in H_p] 1[T=K_c(A)] / R_z`.

Then the exact probability identity is

`P(H_p and E_p) = [sum_J W_J] / [(p)_k c!]`.                 (6.1)

Proof: fix one successful unordered A in H_p and its one unordered K_c(A). There are k!c! ordered tuples. For each tuple there are exactly R_z allowed graphs J, corresponding to the independent choice of one actual representation of each target. Each graph contributes 1/R_z, so the total is k!c!. Dividing by `(p)_k c!=binom(p,k) k!c!` counts this A with its uniform probability. Noncovers contribute zero.

There is exactly one division by the representation multiplicity. No additional division by the number of covers belongs in (6.1), because K_c has already selected one. Conversely, removing the canonical indicator would count all c-centre covers and would no longer equal the success probability. All graph labels are determined by z, so there is no extra p! factor in (6.1).

The Stage 4 minimum-cover selector and its sum over cardinalities remain valid. Equation (6.1) is a different exact normalization chosen deliberately to keep the operational cap and its multiplicity estimate in one term. No minimum-cover component bound or private-target bound is imported into this cap-canonical count.

## 7. Applying all the new unconditional bounds still gives no probability gain

Put t=c, `v=k+c`, `lambda=kc/p`, and

`gamma_p=(lambda-1)^2/V_p * log(1+V_p/(lambda-1))`.

On H_p, (5.1) gives `R_z>=exp(p gamma_p)`. Also `Q_J<=p^v`. Bounding each W_J by these quantities and then using (4.1) yields

`P(H_p and E_p)`

` <= min(1, [p^v binom(p,c)/(p^2(p-1))]`

`              * exp[p(log lambda-gamma_p)])`.                (7.1)

This is a correct consequence of the new results, but its unclipped logarithm is

`p(log 100-o(1))+O(k log p)`,

which is positive. Thus (7.1) supplies only the trivial upper bound one. The graph-sparsity theorem saves approximately p in the exponent compared with counting all graphs; the sharper representation bound subtracts an additional order `p log L_p/L_p`. The remaining positive order-p term is not removed.

Replacing the graphwise `p^v` by the forest-injective-label bound `p^h(p)_r` is legitimate, but does not change this conclusion. Here r=O(sqrt(p)), and the improvement from `(p)_r/p^r` has logarithm only O(1) at a fixed cap constant. The exact cycle completion is not a product of independent probabilities, by Section 3.

Even a much better marginal estimate for either graph support or multiplicity would need checking in their joint, canonically weighted law. The graph-sparsity proof used an upper bound on R_z to count incidences, while (7.1) used a lower bound on R_z to undo representation multiplicity. Treating those as the same typical value would be an additional theorem. Canonicality, H_p, and the inverse weight cannot be dropped from the desired estimate and later restored without justification.

## 8. Exact final unproved inequalities and acceptance boundary

The direct weighted-count target is now:

Find a fixed epsilon>0 and an unbounded prime subsequence such that

`sum_(J subset K_(k,c), |E(J)|=p) W_J`

` <= (1-epsilon) (p)_k c!`.                                 (8.1)

Together with `P(H_p^c)=o(1)`, this would give a fixed positive failure probability along that subsequence and would negate the original convergence-to-one assertion. Neither (8.1) nor a stronger o(1)-fraction bound is proved here.

An alternative sufficient weighted-entropy estimate, preserving Stage 4's definitions

`F_c(beta;A)=binom(p,c)^(-1) sum_(|T|=c) exp[-beta U(A,T)]`,

would be, for some beta_p>0 and a fixed a>0 along unbounded primes,

`E log F_c(beta_p;A) <= -log binom(p,c)-beta_p a c sqrt(k)`.   (8.2)

The deterministic soft-min inequality would then yield `E R_c>=a c sqrt(k)`. The sharper exact-model concentration theorem proved in the final constructive argument gives

`P(E_p)<=exp[-(E R_c)^2/(2 k c^2)]<=exp(-a^2/2)<1`.

The denominator 2 improves the earlier conservative denominator 8 without changing the required expectation scale. Its proof uses the m-Lipschitz cardinality change under a single swap of A, rather than a 2m symmetric-difference estimate.

No estimate of the strength of (8.2) has been obtained. The read-k Laplace inequality provides only order-k suppression against order-k-log-k minimization entropy.

The affirmative bridges also remain conditional: `E R_(33k)=o(p^(5/6))` or `E R_(49k)=o(p^(3/4))` would permit the already proved shift amplification and exact-budget repair. The present cycle count proves neither.

The unconditional full-budget residual bound retained from previous passes is

`0 <= R_c(A) <= floor[p binom(p-k,c)/binom(p,c)]`

`               =(exp(-100)+o(1))p`.

The final constructive argument improves its integer upper bound to g_c, where `g_0=p` and `g_(i+1)=g_i-ceil(k g_i/(p-i))` in the relevant range. It proves `0<=R_c<=g_c` and `p binom(p-k,c)/binom(p,c)-c<g_c<=p binom(p-k,c)/binom(p,c)`. Thus the same positive-density asymptotic remains the strongest currently established full-budget upper scale.

The lower bound remains zero. Fixed-T exponential rarity, failure of specified low-entropy menus, the legal typicality exclusions, exact normalization, graph sparsity, and large cover-conditioned representation multiplicity do not supply a nonzero lower bound of the required order for the unrestricted optimum.

