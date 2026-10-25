# Independent analytic reconstruction: Brownian first-visit cells

Record 23224103, DOI 10.5281/zenodo.23224103, version 1.0 dated 7 October 2026, six-page actual manuscript. Model/effort as assigned: GPT-6.1 Sol / Ultra. No children. This reconstruction was written before reading any deposited checker, output, favorable audit, review body or sibling opinion. All six manuscript pages were read as text and rendered and visually inspected. The fresh original PDF matches the initially supplied checksum-matched local copy.

Source custody: PDF 88322 bytes, SHA-256 `acf262d707c9faa466f30a86a8347ae7cbff0ad5a48fbb38893e460c0e3ec2e5`; ZIP 141902 bytes, SHA-256 `8835f8ea3be4e25eb25b7663a2da0d56ee4afbc3dbe60843b02436a66dc237ab`. Fresh record raw SHA-256 `165d091363737552e4edd1713b504e615bcb9e27470b34972f97104a14c3cd7d`, retrieval 2026-10-25T05:30:02.713413+00:00. The support ZIP is bound but not yet scientifically inspected at the early seal.

## Literal hypotheses, quantifiers and success criteria

The state space is T=R/Z with total Lebesgue length1. For every finite integer k>=1 and every deterministic labeled vector p=(p1,...,pk) of pairwise distinct seeds, W_i are independent Brownian motions with generator (1/2)d^2/dx^2 and initial points p_i. They continue through meetings, seeds, already painted points, and one another's territory. For each x, T_i(x)=inf{t>=0:W_i(t)=x}; the owner I(x) is the smallest label attaining min_i T_i(x). L_i is the Lebesgue integral of 1{I(x)=i}.

The theorem asserts a.s. well-defined nonnegative lengths summing to1, and for *every* real vector theta with theta_i>=0 the exact joint Laplace transform

    E_p exp(-sum_i theta_i L_i)=sum_{m>=0}(-1)^m M_m(theta;p)/m!.

For each m>=1, the coefficients are specified by the actual equations(2)-(9): explicit interval exit-time/place series, products over one particle's query discovery order, the full cumulative physical clocks, finite sums over all k query permutations and all label assignments, and ordinary nonnegative integrals. M_0=1. With theta_*=max_i theta_i, the claims are 0<=M_m<=theta_*^m, absolute convergence, and absolute degree-N truncation error <=theta_*^(N+1)/(N+1)! for every integer N>=0. The full family of coefficient polynomials (not just their values at a single theta) uniquely determines the joint Borel probability measure.

Equally spaced p_i=(i-1)/k are a fixed-vector instance; independent uniform labeled seeds require integrating the fixed-seed formula against dp on T^k, with exactly the same bound. Deterministic coincident seeds and coincident/seed query configurations are excluded where stated; the latter and the random-seed diagonals are null sets. No assertion about limits at those exceptional configurations, a compact density, a named law, large-k behavior, coefficient-quadrature accuracy, efficient evaluation or absolute priority is substituted for the actual claim.

Success requires a universal analytic derivation of these formulas, correctly correlated query hitting times for each walker, legitimate measurability/interchanges, correct BM normalization, and full coverage of k=1,m=0,theta=0, singleton remaining targets, impossible orders, wraparound, and null ties. A finite chain or a numerical check cannot prove the Brownian theorem.

## 1. Deriving the next-target kernel with the factor1/2 retained

For interval(0,l), start alpha in(0,l), and kill standard BM at its exit tau. The orthonormal sine basis sqrt(2/l)sin(n*pi*x/l) has generator eigenvalue -n^2*pi^2/(2l^2). Thus the killed density is

    H(t;alpha,beta)=(2/l)sum_{n>=1}sin(n*pi*alpha/l)sin(n*pi*beta/l)
                                      exp(-n^2*pi^2*t/(2l^2)).

For each fixed positive t the series, all finitely many beta derivatives and one time derivative converge absolutely and uniformly on beta in[0,l], locally uniformly for t>0: polynomial powers of n are dominated by exp(-c*n^2). The generator and flux factors are therefore unambiguous.

For bounded tau wedge t, optional stopping of B^2-t gives E(tau wedge t)=E B_(tau wedge t)^2-alpha^2<=l^2-alpha^2. Monotone convergence implies tau<infinity a.s. Optional stopping of the bounded stopped coordinate and dominated convergence give P(exit right)=alpha/l, P(exit left)=1-alpha/l. The small-time boundary hitting atom is zero because a continuous path starting strictly inside has a strictly positive exit time pathwise.

Write w0(beta)=1-beta/l. Markov conditioning at time t gives

    P_alpha(tau>t, B_tau=0)=integral_0^l H(t;alpha,beta)w0(beta)dbeta.

Differentiate for t>0, use H_t=H_betabeta/2, and integrate twice by parts. Since H=0 at both endpoints and w0''=0, the negative derivative is +(1/2)H_beta(t;alpha,0). Similarly the right exit density is -(1/2)H_beta(t;alpha,l). Substitution yields precisely

    f0=(pi/l^2)sum_n n sin(n*pi*alpha/l)exp(-n^2*pi^2*t/(2l^2)),
    f1=(pi/l^2)sum_n (-1)^(n+1)n sin(n*pi*alpha/l)exp(-n^2*pi^2*t/(2l^2)).

These functions are nonnegative because they are derivatives of exit-distribution tails, not because their individual summands have a fixed sign. Their total masses are the two exit probabilities above. Taking the full function first and then its improper integral avoids an unjustified integration of the signed Fourier series at zero.

The independent ODE check is v''/2=s v with endpoint values(1,0) or(0,1). The solutions are sinh((l-alpha)sqrt(2s))/sinh(l sqrt(2s)) and sinh(alpha sqrt(2s))/sinh(l sqrt(2s)). The total mean exit time from the derivative at s=0 is alpha(l-alpha), consistent with the generator1/2. The pre-support control program independently obtains eight exact Taylor orders from the differential recurrence and compares them with the hyperbolic ratios; a factor-of-two clock error is deliberately rejected. This is an algebraic normalization control, not an appeal to numerical quadrature.

For any nonempty finite remaining target set A and z not in A, a continuous circle path must first leave the lifted component(a,b) of T\A through one of its endpoints. Its length l is positive and at most1; alpha=z_lift-a lies strictly inside. Integer lift shifts leave both l and alpha unchanged. The only nonzero K_A(t;z,q) are endpoint fluxes. If A is a singleton, both endpoints represent the same q, and K_A=f0+f1 with l=1. The two endpoint masses still sum to1; they are not two separate unit densities. Every target is reached in finite time with total kernel mass1.

## 2. Ordered discovery preserves within-walker correlations

Fix m pairwise distinct query points none equal to a seed. Define successive stopping times sigma_0=0 and sigma_r=the first time after sigma_(r-1) that the same walker reaches an as-yet-unvisited query. Record the discovered query permutation pi and U_r=sigma_r-sigma_(r-1). Each sigma_r is finite by the kernel lemma and induction. Each U_r>0 since the current position is not one of the remaining targets, and distinct query points cannot be hit simultaneously by a continuous path.

Conditional on the stopping history through sigma_(r-1), the future is a BM at the known current query (or seed for r=1), independent of that history by strong Markov. Therefore the joint density of the event that the ordered query list is pi and of its increments u is exactly

    D_i^pi(u)=product_{r=1}^m K_{A_r^pi}(u_r;z_(i,r-1),x_pi(r)).

The density is *not* normalized conditional on pi; it carries the order probability itself. Removing only the reached query is correct: previously visited queries cease to be stopping targets but the walker still traverses them normally. Stopping/reflecting the walker at a meeting or painted point would define a different model. A query not adjacent in the current remaining-set complement gives a zero kernel, correctly encoding impossible permutations.

The sum over all permutations of their increment integrals is1. This can be proved by induction on the number of remaining queries: sum over the first endpoint choice and integrate its density to total mass1, then apply the identical assertion to the smaller remaining set. Thus there is no unsupported independence among a single walker's first-hitting times.

The physical first-hitting time of query j is sigma_(pi^-1(j))=sum_{r<=pi^-1(j)}u_r, exactly the manuscript's h_ij. Across distinct particles, the entire stopped trajectories are independent, so their ordered densities multiply. Given their k permutations and all increments, the owner event for each query is exactly h_(a_j,j)<h_(i,j) for every i!=a_j. Those are integer-coefficient strict linear inequalities in the positive increments. Hence integrating the density product over that polyhedral region and summing the finitely many permutation vectors yields exactly Q_a.

A fixed nonseed query has an atomless hitting-time law for each walker: it is the singleton kernel of mass1 on t>0. Independence across walkers makes equal hitting times a null event for that fixed query; a finite union over queried j remains null. Alternatively the equality sets of the independent increment density are proper hyperplanes: the two clocks involve different particles' coordinate blocks with nonzero coefficients. Thus strict owner inequalities neither omit probability mass nor require a tie correction. Summing Q_a over all assignments gives1.

Exact clock falsification control: with pi1=(1,2), increments(2,100), and pi2=(2,1), increments(3,1), physical hitting vectors are (2,102) and (4,3), giving owners(1,2). Comparing the increments attached to each query instead would incorrectly yield(2,2). Equation(6) uses the correct cumulative clocks. No physical-time Jacobian is missing because the integration variables remain the original u coordinates.

## 3. Measurability and all-location partition statements

On canonical continuous-path space, for fixed t let

    d_t(omega,x)=min_{0<=r<=t}d_T(omega(r),x).

This functional is jointly continuous in x and the path's uniform-on-[0,t] topology (and can also be expressed by rational times plus t). Compactness ensures the minimum is attained. Thus {T_i(x)<=t}={d_t=0} is measurable, so the extended-valued hitting-time map is jointly measurable. A finite minimum with the specified smallest-label tie rule is measurable; hence the ownership indicators and the integrals L_i are random variables.

For every fixed nonseed x, each T_i(x) is finite and any tie is null by the singleton argument. Apply Tonelli to the jointly measurable indicator of the bad location set: its expected Lebesgue measure is0. Therefore a.s. that set has measure0. The finitely many seed points have measure0 as well. No uncountable union of probability-zero events is being used to claim simultaneous absence of ties at every x. At all locations the minimum-label convention still specifies an owner; the a.e. statement is enough for lengths and shows sum_i L_i=1 a.s. The resulting lengths are supported on the compact simplex.

Dependence on deterministic seed p is measurable as well: realize W_i=p_i+B_i modulo1 on a common canonical space. This depends continuously on p and paths, and the preceding minimum-distance construction is joint in p,x. Alternatively the explicit interval formulas are Borel on each ordering chamber of distinct seeds/queries. Thus the subsequent uniform-seed integral is legitimate, not merely a formal average over an unproved parameter dependence.

## 4. Coefficients, absolute convergence, remainder and uniqueness

For theta_i>=0 define Z=sum_i theta_i L_i=integral_T theta_(I(x))dx. Since the total measure is1 and ownership is a.e. a partition, 0<=Z<=theta_*. For m>=1, multiply this integral m times and use Tonelli to obtain

    E_p Z^m = integral_(T^m) sum_a (product_j theta_(a_j))
                                  P_p(I(x_j)=a_j for all j) dx
             =M_m(theta;p).

At fixed m every coefficient is therefore finite and bounded by theta_*^m. The excluded query diagonals and seed coincidences have m-dimensional Lebesgue measure0; arbitrary bounded values there do not change this Lebesgue integral. The proof does not require a continuous limiting kernel when queries merge. All deterministic kernels in D are nonnegative as complete functions; the finite sum and improper time integrals have finite mass, and no signed termwise Fourier integration occurs.

Absolute summability follows from sum_m E Z^m/m!<=exp(theta_*). It permits expectation of the exponential series and gives equation(10). The sharper truncation estimate comes from the pointwise Taylor remainder of exp(-z) on z>=0: its derivative of every order has absolute value at most1 on[0,z], so |exp(-z)-sum_(m<=N)(-z)^m/m!|<=z^(N+1)/(N+1)!. Taking expectations gives equation(11), with no extra exp(theta_*) factor. It is uniform over all distinct p because the bound uses only theta_*.

Expand (sum_i theta_i L_i)^m. The coefficient of theta^n, |n|=m, is (m!/product_i n_i!)E product_i L_i^n_i. Thus the entire family M_m(theta;p) determines every mixed moment. Knowledge of its values on the nonnegative orthant suffices to identify those polynomial coefficients because its positive interior is an open set. On the compact simplex the polynomial algebra contains constants and separates points, so Stone-Weierstrass gives density in continuous functions; equality of all moments then implies equality of all finite Borel measures. This proves a full measure characterization, not merely marginal laws or finitely many moments. Bounded support also justifies derivatives of the Laplace transform at zero.

## 5. Starting laws, symmetries and boundary cases

- m=0 is supplied separately as1. k=1 gives Q_a=1 for the only label vector, M_m=theta1^m, and transform exp(-theta1).
- All theta_i=0 gives M_m=0 for m>=1 and transform1; if all theta_i=t>=0, Z=t a.s., M_m=t^m and transform exp(-t). The remainder bound also holds at theta_*=0.
- Fixed seeds may be arbitrarily close but remain distinct. Every formula still uses strictly positive component length and interior alpha at each query step. The outer bound does not deteriorate as those distances shrink. No uniform inner-series truncation or quadrature error follows from this fact, nor is one claimed.
- The theorem excludes deterministic coincident seeds. Independent uniform seeds coincide with probability0; any chosen bounded extension on those diagonals leaves the averaged coefficients unchanged. Integrating the explicit coefficients against dp is valid by measurable dependence and the same uniform bound, giving equation(12). Independent uniform *labels* are retained. Sorting the seeds first changes the labeled law and must use the ordered seed distribution, as the paper says.
- Equally spaced seeds are deterministic distinct for every k>=1. Rotation/reflection of the circle plus the induced cyclic/dihedral label maps preserve the length law. Their action is transitive on labels, yielding E L_i=1/k. IID uniform labeled seeds have full permutation exchangeability and the same mean. No full permutation symmetry is asserted for fixed equally spaced labels.
- Changing circumference to c scales spatial measure by c. Brownian scaling introduces only the common clock factor c^2, which cancels from all first-arrival comparisons. Therefore the transform of actual lengths cL is obtained by theta->c theta. A common positive diffusivity similarly changes all clocks by one common factor; unequal diffusivities are not covered by that invariance statement.
- No critical-frontier-state classification or interface ODE is an unproved dependency of this construction. It uses finite-query stopping trees and a scalar interval generator. There is no collision-time approximation, independence assumption for one walker's query times, or discrete-to-Brownian limiting step.

## Independent checks and initial disposition

The separately written pre-support `independent_controls.py` passes 182 exact rational checks: interval ODE coefficients and hyperbolic-ratio coefficients through order 8, endpoint normalization and mean exit time, deliberately wrong diffusivity, circle wraparound/singleton/retired-target/impossible-order cases, cumulative-time versus increment-only ownership, and bounded-support product-moment algebra. These are finite controls accompanying the universal derivation, not a Brownian proof by samples.

At this early independent stage, the literal main theorem is supported by the analytic derivation above; no substantive defect found. The exact remaining mathematical gap at that literal scope is none found. Full deposited-support inspection, actual central primary-dependency body verification and final integrity sealing remain. No conclusion of exhaustive priority or independent discovery is made. Follow-up recommendation is null under the assigned high bar. Publication clearance is false, and the parent must read the actual paper and all full reports before any promotion.
