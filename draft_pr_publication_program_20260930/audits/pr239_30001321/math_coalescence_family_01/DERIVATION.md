# Independent derivation of the final-segment closure

Scope: PROOF.md §§2–6 for PR239/problem30001321. This derivation was formed before reading any historical independent review or sibling report. It also checks how the explicitly stated earlier inputs enter. It is a mathematical audit, not a priority or source-identification verdict.

## 1. Quantifiers and hypotheses

The environment law is fixed. Its coordinates p(s,x) are iid in space and time and satisfy 0<p<1 almost surely. Therefore q=E p lies in (0,1), a=q(1-q)>0 and delta=E[p(1-p)]>0. The latter strict positivity follows from positivity of the bounded random variable p(1-p), and requires no inverse moment or deterministic ellipticity constant. All constants may depend on the fixed law. The sequence M_N tends to infinity, need not be monotone, and may diverge arbitrarily slowly. Every partition/alignment is deterministic. The asserted bound is for each such partition, with constants uniform in alignment; there is no assertion about an environment-adapted choice of partition.

The earlier inputs used are (B) conditional moments of occupation sums, (F) ordinary coarse L1 convergence for every diverging scale, and (G) superpolynomial concentration above any fixed exponent >1/4. I independently read TURN_1.md and TURN_2.md in full. Their overlap calculation, ordered-index moment argument, interval-gradient bound, common-variance-event sign-test argument and boundary smoothing have the needed hypotheses. In particular, (G) is invoked only at the auxiliary H scale, not at M_N. The present audit concentrates on the genuinely additional closure rather than treating finite computations as a proof of (B), (F) or (G).

## 2. Old law is diffuse on the strip influence intervals

Let ell=floor(N^(3/4)), m=N-ell, r=N^(3/8), R=ceil(r log N), eta=kappa=1/32. Every prescribed J has O(R) integer sites. A [0,1] majorant which is one on J and tapers over r on both sides is 1/r-Lipschitz. The biased annealed binomial law gives E mu_m(f_J)<=C(R+r+1)/sqrt(m)=O(N^(-1/8)log N)=o(N^(-1/32)), including its parity restriction.

Expose old environment layers. Translation by the annealed increments preserves the Lipschitz constant, so the layer martingale increment is bounded by 2/r and its conditional variance by C I_s/r^2. On the single common event V=sum_(s<m) I_s<=N^(eta+1/2), the predictable variance is <=C N^(-7/32). At u=(1/2)N^(-1/32), the joint-event Bernstein bound has exponent c N^(5/32); the increment correction is O(N^(-13/32)), smaller than the variance term. Thus a union over O(N) prescribed intervals costs only O(N) exp(-c N^(5/32)). The failure of the common V event is charged once and is superpolynomial by the all-order occupation bound. This establishes (I) without asserting concentration for an environment-dependent interval.

The eventual strip indices can be chosen deterministically: starts lie in [-m,m] and relevant fresh sites lie in [-N,N]. A fixed finite index range containing every potentially relevant tilted strip has O(N) elements. Its influence intervals have O(R) length. Thus the preceding finite collection is legitimate.

## 3. Same-parity coalescence and conditional-mean transfer

For two same-parity starts x<y, define a quenched coupling with independent jump coins before meeting and the same coin afterward. Before meeting the difference is even and positive. A distance-two pair can meet but cannot cross in one step. Averaging a pre-meeting transition sees two independent fresh environment variables, hence the half-gap jumps by +1 and -1 with probability a each and holds with probability 1-2a. This uses fresh time layers, not quenched independence after fixing the environment.

For the homogeneous lazy walk let p_t(j) be the unrestricted mass from zero. Its killed transition kernel on positive integers is p_t(z-d)-p_t(z+d): this follows directly from the common recursion, zero boundary and initial values. Summing over z>=1 gives the exact survival probability sum_(j=1-d)^d p_t(j). The characteristic function is 1-2a+2a cos(theta); since 0<a<=1/4, it is nonnegative and bounded above by exp(-c_a theta^2) on [-pi,pi]. Fourier inversion yields max_j p_t(j)<=C_a/sqrt(t+1). Thus survival<=C_a d/sqrt(t+1), with a cap of one. The L1 coupling inequality contributes factor two. This proves (L), including t=0 by changing the constant and x=y separately. Opposite parities are never coupled.

For a fixed old law mu on the reachable parity sites, the within-cell replacement is mu'(x)=mu(J) alpha_m(x)/alpha_m(J). Every actual reachable site has positive annealed mass. A null annealed cell has zero actual mu_m mass and can be omitted. The explicit coupling within each H cell samples x from mu and y from alpha_m conditional on that cell. Every coupled pair has distance <H. Averaging future environments therefore bounds E||mu K-mu' K||_1 by C H/sqrt(ell). Independence of the old and future environments makes this valid after conditioning on the complete old environment.

Cellwise calculation gives ||mu'-alpha_m||_1=sum_J |mu(J)-alpha_m(J)| exactly. Kernel contraction bounds the corresponding output difference. For the remaining term, alpha_N=sum_x alpha_m(x) E K(x,.), so Jensen bounds its coarse L1 discrepancy by the alpha_m mixture of the length-ell discrepancies from a single start. Such a start merely translates the deterministic target partition; the alignment-uniform bound (F) applies. These three inequalities yield (P) with no quantitative assumption on M_N.

For completeness the bound rho(ell,M_N) in (F) does tend to zero jointly as ell,M_N tend to infinity. Fix R0 large first; for M<=sqrt(ell), the relevant terms are bounded by C R0 log(1+M)/M+C log(ell)/sqrt(ell); for M>sqrt(ell), they are bounded by C(R0+1)log(ell)/sqrt(ell). Then let R0 tend to infinity. No rate of divergence or diagonal exchange is hidden here. The auxiliary H=ceil(N^(5/16)) satisfies H>=m^(5/16), so (G) applies with fixed gamma=5/16. Also H/sqrt(ell)=O(N^(-1/16)).

## 4. Deterministic strips give actual product inputs

Kill a path immediately after the first step violating |X_(m+t)-x-vt|<=R. At every environment site it uses before death, |y-vt-x|<=R. Partition all such coordinates by kR<=y-vt<(k+1)R. The strip assignment is deterministic for every real v, including irrational v, and the disjoint finite input vectors are independent. One may include all reachable coordinates in the strip inputs, whether or not a particular path uses them.

If x lies outside J_k=[kR-R-1,(k+1)R+R+1], no alive path from x can use a coordinate in strip k. This remains true when the strip is resampled: the killed paths are confined by a deterministic start-dependent corridor under every environment. Hence changing the entire strip leaves K^dagger(x,.) unchanged outside J_k. Inside J_k each output is a subprobability measure, so its L1 variation is at most two. Mixing starts bounds the total variation of the output, and then the oscillation of its L1 distance from alpha_N, by 2 mu_m(J_k).

With R an integer >=1, x belongs to at most six J_k: the admissible real interval of k values has length 3+2/R<=5 and hence contains at most six integers. Consequently sum w_k<=6 and sum w_k^2<=6 max w_k. Conditional on the old environment the ordinary bounded-differences inequality gives

    P(F^dagger-E[F^dagger|F_m]>t | F_m)
       <=exp(-2t^2 / sum_k (2w_k)^2)
       <=exp(-t^2/(12 max_k w_k)).

If all relevant w_k were zero, the function would be constant and the tail would be zero; no division by zero is needed. For an actual probability law at least one relevant weight is positive. Applying the old interval bound gives exp(-c_t N^(1/32)) on the old good event. Endpoint masses and overlapping start cones need no independence.

## 5. Restoring killed paths and closing the tail

Under the annealed joint law each future increment is an independent sign of mean v, even though the current position is random. A maximal bounded-increment exponential inequality gives, uniformly in the start, probability at most d_N=C exp(-c R^2/ell)<=C exp(-c(log N)^2) of leaving the corridor. This is a whole-path maximum bound, not an endpoint estimate.

K-K^dagger is positive pointwise. Thus, for every environment, D=1-mu K^dagger(Z) is exactly ||mu K-mu K^dagger||_1 and dominates |F-F^dagger| after any coarsening. For every old environment E[D|F_m]<=d_N, so E F^dagger<=E F+d_N and P(D>t|F_m)<=d_N/t. Positivity rather than independence supplies this restoration.

For fixed epsilon, choose N large enough that C H/sqrt(ell)+rho(ell,M_N)+d_N<epsilon/8. Outside the (G) event L_(m,H)>epsilon/8, the killed conditional mean is <=epsilon/4. If F>epsilon and D<=epsilon/4, then F^dagger-E F^dagger>epsilon/2. Combining the two old bad-event probabilities with bounded differences and Markov restoration proves the claimed bound for every power K. Since exp(-c(log N)^2)=o(N^(-K)) for every fixed K, the restoration error has exactly the required strength.

## 6. Boundary and interpretation checks

- The deterministic elliptic law has quenched law equal to its annealed law and is included.
- An iid random arrow law supported on {0,1} is excluded. Its quenched law remains a point mass, and delta=0 destroys the old-law overlap input. Near-arrow fixed elliptic laws only change constants/thresholds; the proof makes no uniform assertion as delta tends to zero. Finite exact tests below include the excluded arrow law only to test the coalescing identity, which itself continues to hold there.
- Finite two-atom examples are uniformly elliptic; they do not empirically certify merely elliptic infinite-support laws. The analytic proof covers those laws because it uses only q, positive delta, independence and bounded jumps.
- Real half-open target intervals cause no obstruction. Their intersections with Z contain at most M+1 sites and their central-window cell count is at most 2R0 sqrt(n)/M+2. The same parity-telescoping variance bound gives the stated modification of (F), still tending to zero. No other closure step needs integer target M.
- All floors/ceilings alter only eventual constants. The auxiliary exponent margins are strictly positive and were also checked exactly as fractions.

No mandatory mathematical defect was found in this closure. Source-conjecture identification, literature priority, author/review history, native custody, publication metadata, complete package consistency and final case acceptance are outside this bounded verdict.
