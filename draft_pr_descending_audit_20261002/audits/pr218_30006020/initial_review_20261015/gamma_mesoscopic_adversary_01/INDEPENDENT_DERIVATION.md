# Independent Gamma/mesoscopic derivation, sealed before other audit reading

Author: independent subagent `/root/pr218_gamma_mesoscopic_adversary_20261015`.
UTC: 2026-10-15 06:15:34. Checkpoint completion: 65% of the assigned adversarial audit.
Frozen candidate head supplied by parent: `dc457c741c779fbf90fbfdcdc73f750b3716f561`.

Only the frozen submitted `CANDIDATE.md`, project instructions, and the PDF skill
were read before this derivation. No sibling report, old review, checker,
disposition, or parent reconstruction was consulted. The argument below is
conditional on the model and stated transfer inputs; published geometric
inputs have not yet been independently source-checked.

## Claim, assumptions, and falsification targets

Let a_j = zeta(2j)/(2j), H(z) = exp(sum a_j z^j), h_n = [z^n]H.
The random positive integer assembly has multiplicities C_j with probability
product(a_j^C_j/C_j!)/h_n conditional on sum j C_j = n. Independently mark
each size j by Y ~ Gamma(2j, rate 1), then divide all marks by their sum T.
For every positive sequence q=q_n with q -> infinity and q/n -> 0, the target is

    sum_i delta_(n Y_i/(q T)) => PPP(dx/(2x)) on (0,infinity),

including joint moment convergence of counts on finitely many compact windows.
Falsification targets: a hidden rate q >> log n, a blow-up of h_(n-j)/h_n
near j=n, a noncontinuous random dilation, failure of uniform integrability,
or a missing requirement in transfer to the geometric law.

## 1. Coefficients and the unmarked assembly

Expanding zeta and its logarithm gives

    H(z) = (1-z)^(-1/2) B(z),
    B(z) = product_(m>=2) (1-z/m^2)^(-1/2).

B is analytic and nonzero on |z|<4, B(1)=sqrt(2), and its Taylor coefficients
decay exponentially. Convolution with [z^n](1-z)^(-1/2) gives
h_n ~ sqrt(2/pi) n^(-1/2). Splitting the convolution at sqrt(n) proves this
directly: below the split the binomial ratio tends uniformly to 1, and above
it the exponentially small tail dominates the polynomial ratio. Therefore

    h_(n-r)/h_n <= C sqrt((n+1)/(n-r+1)) <= C sqrt(n+1),

for every 0<=r<=n, and the ratio tends uniformly to 1 on 0<=r<=o(n).
The same convolution argument works for fixed positive powers H^t.

Removing selected components proves the exact factorial identity

    E product_j (C_j)_(r_j)
      = h_(n-sum j r_j)/h_n product_j a_j^r_j,

with zero if the selected total exceeds n. For finitely many windows
[a_l q,b_l q], every fixed factorial order selects total O(q)=o(n), so the
ratio tends uniformly to 1. Also sum_(a q<=j<=b q) a_j -> (1/2)log(b/a).
These give independent Poisson factorial moments. The Poisson law is
moment-determinate, and joint counts are tight from bounded first moments.
For the random measures, tightness on every compact follows from the same
bound and exhaustion by compact subsets of (0,infinity). Joint convergence
on an endpoint-null interval semiring identifies the unique PPP limit.

## 2. Gamma marking with every allowed rate

Let f be globally Lipschitz, nonnegative, and supported in [a,b], 0<a<b.
Write R_(n,j)=h_(n-j)/h_n. By the first factorial identity, the expected
absolute difference of marked and unmarked integrals is at most

    sum_(j=1)^n a_j R_(n,j)
       E |f(Y_j/(2q))-f(j/q)|.                         (E)

Three estimates control this without any log(n) union bound.

1. For a q/2 <= j <= 2b q, R_(n,j)<=C eventually since q=o(n). Jensen gives
   E|Y_j/(2q)-j/q| <= sqrt(2j)/(2q). Hence this part of (E) is
   at most C/q sum_(j=ceil(aq/2))^floor(2bq) j^(-1/2) = O(q^(-1/2)).
2. For j<a q/2, the unmarked value vanishes and the Chernoff choice theta=1/2
   gives P(Y_j>=2a q)<=exp(-a q) 2^(2j)
   <=exp(-a(1-log 2)q). Here R<=C and sum a_j=O(log(q+2)); the contribution
   is O(log(q+2) exp(-a(1-log 2)q)).
3. For j>2b q, the unmarked value vanishes and theta=-1/2 gives
   P(Y_j<=2b q)<=exp(b q)(3/2)^(-2j)<=exp(-c j),
   where c=2 log(3/2)-1/2>0. Up to n/2, R<=C and the exponential sum
   vanishes as q->infinity. Above n/2, R<=C sqrt(n+1), so even the crude
   bound C sqrt(n+1) sum_(j>n/2) exp(-c j) vanishes exponentially in n.

Thus (E)->0 for every q->infinity, q=o(n). In particular there is no hidden
need for q/log n->infinity, nor a quantitative speed for q/n->0. Nonnegative
compactly supported Lipschitz tests determine the Laplace functionals of
locally finite point measures, so Z_n=sum delta_(Y_i/(2q)) has the same PPP
limit as the unmarked process. These estimates also supply local tightness.

## 3. Normalization, topology, and endpoints

Conditional on every composition, T=sum Y_i ~ Gamma(2n,1), so T/(2n)->1
in probability uniformly over the composition. Set U=T/(2n).
The normalized scaled point measure is D_(1/U) Z_n, where D_d moves x to d x.
The dilation map (mu,d)->D_d mu is continuous in the vague topology for d>0:
for f in C_c, f(d_n x) converges uniformly to f(d x) on a single compact set
containing all supports for d_n->d>0, and vaguely convergent positive measures
have uniformly bounded mass on that compact after choosing a continuous
envelope. Slutsky gives joint convergence (Z_n,1/U)->(Z,1), without requiring
independence of Z_n and T. It follows that D_(1/U)Z_n => Z.

The limit PPP almost surely has no point at any prescribed endpoint because
dx/(2x) has no atoms. Thus the compact-window count maps are almost surely
continuous, including finitely many windows simultaneously. Disjoint-window
independence is the defining Poisson random measure property. The endpoints
0 and infinity are excluded from the state space and from all tested windows.

## 4. Every fixed marked moment

For a compact window [a,b], let p_j=P(Y_j/(2q) in [a,b]) and w_j=a_j p_j.
The same three ranges, now without R, prove sum_j w_j<=C_(a,b) uniformly.
Independent marking and removal of selected components give

    E(M)_r = sum_(j_1+...+j_r<=n)
       R_(n,j_1+...+j_r) product_l w_(j_l).             (F)

Here the factorial counts ordered distinct components; equal part sizes are
allowed and are already accounted for by the assembly factorial identity.
When the selected total is <=n/2, R<=C and this contribution is <=C C_(a,b)^r.
When the selected total exceeds n/2, some j_l>n/(2r). For fixed r, q=o(n)
implies n/(2r)>2bq eventually; consequently p_(j_l)<=exp(-c j_l)
<=exp(-c n/(2r)). Using R<=C sqrt(n+1), a union bound over r positions and
sum a_j=O(log(n+1)) bounds the entire remaining contribution by

    C_r sqrt(n+1) exp(-c n/(2r)) (log(n+1))^r -> 0.

All fixed factorial and ordinary moments of M are uniformly bounded. The
threshold after which the estimate applies may depend on r,a,b; this is
permitted because the theorem only asks for each fixed order.

## 5. Normalized moments and joint moments

For U in [1/2,2], the normalized count on [a,b] is bounded by M on [a/2,2b].
For the complement, K<=n deterministically and the two elementary Chernoff
bounds are

    P(T<=n) <= exp(-(2 log 2 - 1)n),
    P(T>=4n) <= exp(-(2 - 2 log 2)n).

Thus the complementary contribution to an r-th moment is <=n^r exp(-c_0 n),
up to a factor 2. Every fixed normalized moment is uniformly bounded.
For convergence of the r-th moment one uses the bound at order r+1 (or 2r),
not merely the same-order bound. Weak count convergence then implies uniform
integrability and convergence of the r-th moment. A mixed monomial of total
degree r is bounded by the r-th power of the total count on the finite window
union; its uniform integrability follows at order r+1. This proves all joint
moments and limiting independence for the model.

## 6. Exact requirements for actual-law transfer

The argument above alone proves only the ideal model. Sufficient geometric
inputs are: (i) an actual latent good event whose probability tends to 1 at a
polynomial rate; (ii) the conditional actual law on it and the conditional
model law on K<=k_n have a uniform, multiplicative density ratio 1+o(1), valid
for every latent composition and its Dirichlet law; (iii) fixed-order actual
K-moments are O((log n)^r), with polynomial model cutoff tail as well.

A fixed t>1 bound E t^K=O(n^alpha) gives all these logarithmic K-moment
bounds by summing the Chernoff tail beyond A log n, A>alpha/log t.
For t=11/10 and k_n=floor((3/5)log(2n)), alpha=1/20, the cutoff exponent is

    eta=(3/5)log(11/10)-1/20 = approximately 0.0071861 > 1/220.

If the cited non-one-vertex conditional excess really is uniformly
O(log(g)^25 g^(-1)2^k) for all k<=k_n, then it is polynomially small, since
1-(3/5)log 2>0. The bad contribution of any r-th count power is then bounded
by (E K^(2r))^(1/2) P(bad)^(1/2)=o(1). On the good event, uniform density
comparison applies even to shrinking windows and n-dependent statistics.
The bounded model moments make the o(1) density error harmless. Total
variation by itself would not imply this unbounded-moment transfer.

At fixed genus, transfer from finite square count N to the limiting area law
also needs endpoint-nullness and a fixed-genus upper bound for K. Dirichlet
mixtures with at least two coordinates have continuous coordinate marginals;
the single-coordinate atom is at area 1, outside the stated source window
for all sufficiently large g. A deterministic K<=n bound then also transfers
each fixed-genus moment before taking g->infinity. This respects the iterated
sampling limit; it establishes no diagonal N(g) limit.

## Independent provisional finding

No counterexample or rate gap was found in the model Gamma, normalization,
topology, or moment arguments. The strongest independently derived result is
the full model mesoscopic PPP with all fixed joint count moments under only
q->infinity and q/n->0. The actual-law conclusion remains conditional here
on the precise published geometric and cylinder-count inputs. No claim about
novelty, priority, or other strata is made.
