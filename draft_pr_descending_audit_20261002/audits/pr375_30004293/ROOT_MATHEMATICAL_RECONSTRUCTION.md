# Root reconstruction of PR375's five scoped results

Root checkpoint: 2026-10-03, after source-first baseline, direct reading of every author proof and executable source, and complete original-head replay; before reading the probability/moment family reports. Audit completion60%, original sharp-prefix resolution0%. The diagonal family's candidate-free stronger derivation has separately been read; it is not used as a premise below. Exact-head final integration and independent-family corroboration remain pending.

Let the independent indicators satisfy P(n in A)=1/n, including deterministic1, and let A_D=A intersect[1,D]. Define M(D) as the largest number of distinct subsets of A_D with a common sum, where the maximum is over every attainable sum. This finite-prefix quantity is not the infinite-model maximum in Green's literal OWR display. Its proposed leading exponent log M(D)/log log D is a quantitative interpretation, not an OWR-specified normalization. All statements below retain their stated almost-sure, in-probability, expectation or fixed-parameter quantifiers.

## Sources and boundaries

Root independently obtained the actual five primary PDFs and read Green's whole contribution, the FGK published definitions/introductory results and full Lemma2.1 proof/remark, the beta2 calculation in the archived version, and the relevant recent abstracts/introduction/theorem statements. The published annular beta_k definition is an in-probability definition. With that definition, success probability for each fixed k and every c<beta_k tends to1 as its scale tends to infinity. No rate is assumed. The unpublished recent Mao–Song full proof is not independently reconstructed or used as a premise of the five prefix arguments. Its alpha_k/beta_k and fixed-k equalities do not themselves supply a growing-fiber prefix theorem. Tenenbaum's divisor-power results concern another model; there is no established transfer here. Sources are credited and historical eligibility is bounded; neither current worldwide priority nor present-day open status is certified.

## Turn1: annular lower bounds and tail structure

For fixed k, c<beta_k, use disjoint logarithmic annuli whose upper log-scales descend geometrically by factor c. Equal-sum fibers of at least k in each successful annulus combine independently by taking unions of their chosen subsets. The resulting subsets are distinct because annular supports are disjoint, and their sums agree. Thus successful annuli multiply the fiber sizes. The smallest scale can be sent to infinity before counting the annuli so that their success probabilities are uniformly close to1. No quantitative convergence rate is required.

Independent bounded annular success indicators obey a rate-free strong law: their variance through n terms is at most n; Chebyshev along n=m^2 is summable, and monotonicity bridges consecutive squares. This gives almost-sure liminf log M(D)/log log D at least log k/log(1/c), after finite initial annuli are discarded and endpoints are interpolated. Countably many rational c approaching beta_k and integer k may be intersected. Taking the supremum gives the stated zeta lower bound, including the credited eta=.35332277… lower bound.

For fixed r, combining r successive annuli proves beta_(k^r)>=beta_k^r. Consequently the supremum in k agrees with the corresponding limsup exponent; this does not require a uniform theorem in growing r or k. The elementary beta guard comes from equal-sum subsets and their maximal participating coordinate: a common sum forces a second coordinate of comparable size, giving the fixed beta_k<=2/3 bound used to keep denominators positive.

Changing at most q indicators changes M(D) by at most a multiplicative factor2^q in either direction. Therefore the extended-valued liminf and limsup of log M(D)/log log D are invariant under every finite indicator change. Each is a tail random variable and is almost surely constant by the independent tail zero-one law. This proves neither finiteness nor equality of those constants. If L(X) counts the largest fiber with sum at most X, then M(floor sqrt X)<=L(X)<=M(floor X) for large X: every prefix subset sum is at most D(D+1)/2. The factor2 change inside log log is negligible. This transfers a finite in-probability exponent only if such convergence has first been proved; it does not prove convergence.

## Turn2: signed relations and growing lengths

A nontrivial collision supplies a signed relation with all coefficients in {-1,1} after common terms cancel. Expose its largest entry m and a second-largest n. If the relation has length ell, n>=m/(ell-1). Once m, the smaller entries and their signs are fixed, the signed equation determines n. Independence then bounds its occurrence by (ell-1)/m^2 times the product of reciprocal smaller entries. The signs contribute at most2^(ell-1), and ordering distinct smaller entries gives the factorial divisor(ell-2)!. Summing yields the fixed-ell tail bound C_ell(1+log X)^(ell-2)/X. The factorial and the two-largest-entry exposure are essential; a naive single-root count would not be summable.

For ell allowed to grow, apply the same factorial estimate in logarithmic dyadic bands. With ell<=c log m, the exponent is bounded by -1+c log(2e/c), which is strictly negative at c=1/4. This supplies a summable exclusion of sufficiently large short relations. Fixed-size collisions are therefore eventually confined to a finite random core. If every compared subset has at most h elements, its symmetric-difference relation has length<=2h. Outside that core all subsets in a fiber have a common membership pattern, so the fiber cardinality is bounded by the finite number of possible core patterns and eventually stabilizes. The random stabilization bound depends on h and on A; no uniform growing-h conclusion is asserted.

Also N(D)/log D tends to1 almost surely. Expectation is harmonic and variance<=expectation. Chebyshev on D_j=exp(j^2), followed by monotonicity and log(D_(j+1))/log(D_j)->1, proves the assertion without an unjustified rate.

## Turn3: fixed-size flags and subpower growth

For k distinct equal-sum subsets, collect their membership columns in {0,1}^k and quotient by the diagonal vector. Greedily choose independent columns in descending coordinate order. Distinct row signatures force at least ceil(log2 k) pivot dimensions; otherwise at most2^t distinct signatures exist. Between successive descending pivots every membership column lies in the span of the earlier pivots and the diagonal. This support condition survives rounding pivot log-scales up into integer bands, even if pivots share a band.

For a fixed k, the flag/count discretization costs a polynomial in log D with a constant depending on k. After quotienting the diagonal, a dimension j band has at most2^(j+1) residual cube classes. Its entropy cost is bounded by(j+1)log2. Equal-sum equations in the quotient determine the distinct pivot integers uniquely once residual assignments are chosen; impossible, repeated or wrongly ordered roots are discarded. The ratio between Bernoulli probabilities for a configuration containing a pivot n and the configuration with that pivot deleted is exactly1/(n-1), not1/n. The all-residual configurations have total probability<=1, and this counting step uses their original product probabilities, without pretending that deletion preserves the Bernoulli law.

On the regular count event, the negative exponent is controlled by log2-c(t+log2). Fix r, then k=2^r and a sufficiently small positive c. All constants are now fixed before D tends to infinity. The failure probabilities are summable on dyadic D. Taking countably many fixed r yields log M(D)/log D->0 almost surely. A hidden uniform growing-k bound is not invoked at this turn.

## Turn4: explicit all-flag upper bound

The explicit cube count for a j-dimensional quotient is Q_j=2^(j+1)-1. This follows by counting at most2^(j+1) cube points in a(j+1)-dimensional ambient subspace and merging the zero and all-one vectors into the same diagonal class. Keeping this explicit bound removes the uncontrolled constants from Turn3. Abel summation charges the regular-count error u+2 just once per change of the band entropy coefficient; it is not multiplied by the number of occupied coordinates.

For L=log D, use k=floor(L/(log L)^3), count tolerance u=sqrt L log L, and t0=ceil(log2 k). The flag/band/root count is bounded by [2^k(L+3)]^t. The exact root odds add at most(2e)^t D^(-S), with S the sum of scaled pivot logs. Set a=log3-1>0. The first entropy coefficient minus pivot cost is a; later increments are negative because log(Q_j/Q_(j-1))<1 for j>=2. Telescoping therefore gives at most a-c(t+a) in the power of D. The geometric remainder has denominator controlled by cL-R>=1, where R=k log2+log(L+3)+log(2e)+(u+2)log2. These explicit expressions give t0 R=o(L).

Choosing c=(a+epsilon)/t0 leaves an exponentially small flag failure, bounded by exp(-epsilon L/2) for large L. The occupancy failure is bounded by L exp(-(log L)^2/3). Both are summable on dyadic scales. The low prefix contributes at most2^(N(D^c)); the independent count law supplies its logarithm. Thus the frozen proof supports the almost-sure limsup bound

  (log M(D))(log log D)/(log D) <= (log3-1)(log2)^2

in limsup. The normalization is much larger than log log D and does not determine the sharp exponent. The known fixed beta2=1-1/log3 is credited; it is not promoted to a prefix equivalence.

## Turn5: exact tilt, annealed growth, rare tails and moments

Under the normalized tilt lambda^N/Z, independence gives inclusion probability lambda/(i+lambda-1) and Z=product_(i<=D)(1+(lambda-1)/i), with the deterministic i1 factor included. The count has mean lambda log D+O_lambda(1), variance at most its mean, and for lambda>=1 the selected sum has expectation<=lambda D. Pigeonhole gives M>=2^N/(S+1). Taking lambda=2^q cancels its numerator exactly when changing measure, so convexity of x^(-q) gives

  E M(D)^q >= Z_(2^q)/(2^q D+1)^q.

For q>1 this has polynomial exponent2^q-1-q>0. At q2 the exact product Z_4=(D+1)(D+2)(D+3)/6 yields the stated asymptotic coefficient1/96. Annealed polynomial growth is compatible with almost-sure subpower growth: it describes rare configurations, not typical fibers.

For a fixed gamma, choose lambda>(1+gamma)/log2. Under the tilted law, count concentration and the selected-sum Markov bound have an intersection of probability at least1/2 after fixed tolerances are chosen. Restricting N from above gives a lower bound on lambda^(-N), so changing measure back gives a polynomial rare-event lower bound with the stated rate I(lambda_gamma). Parameters and tolerances are fixed before limits; strict gamma-prime margins cover integer/floor endpoint effects. A variable parameter substitution into an asymptotic estimate is not made.

Finally set X_D=log M(D) log log D/log D. On the explicit annular regular event, the Turn4 estimate bounds X_D by C_star+o(1). Off that event, the deterministic log M<=N log2 bound applies. Factorial moments of the Bernoulli count bound every fixed moment of N/log D uniformly. Cauchy–Schwarz then kills the exceptional contribution because its probability decays faster than every power of log log D. This proves the frozen fixed-moment limsup bound E X_D^p<=C_star^p. It neither gives a sharp moment asymptotic nor convergence of log M/log log D.

## Reproduction and strongest verified conclusion

Root's original-head replay binds all54 changed Git objects/53 target files,42 immutable author WIP files, all220 nested manifest occurrences, every five-turn checkpoint and state count. All150925 author assertions and8390 historical assertions reproduce as complete streams. The original42-file, five-source author replay agrees byte-for-byte with the recorded author replay; the current53-file public wrapper verifies52 public entries and its optional PDF count is0. These finite computations corroborate the universal arguments; assertion counts are not proofs.

The original conclusion remains **unsolved,5/5**. Verified lower bounds and the explicit subpower upper bound leave the sharp prefix exponent and its convergence unresolved. A separate diagonal-rank route may strengthen only the larger normalization; it will be published as an audit deduction only after independent adversarial confirmation and root control reproduction. No sixth author turn, new solution or novelty is claimed.
