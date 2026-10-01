# Turn 2: uniform convergence under local moments of any order above one

**Scoped partial, substantive author turn2/5. The exact X log X endpoint remains unresolved.** This turn attacks the functional topology directly. It proves a stronger mode of convergence under an explicitly stronger-than-X-log-X moment condition, with no increment regularity assumption. The extra moment is stated rather than hidden. No novelty is asserted.

## 1. Functional theorem

Retain the source's exact generation-indexed iid coupling, with X nonnegative, integer-valued, nondecreasing and càdlàg on I⊂(1,infinity), E X(lambda)=lambda. Assume

    for every compact[a,b]⊂I, there is p>1 with E X(b)^p<infinity.      (P)

The exponent may depend on the compact interval. Replacing it by min(p,2) permits 1<p≤2 throughout the proof.

**Theorem.** Under(P), W_n(lambda)=Z_n(lambda)/lambda^n converges almost surely locally uniformly to a càdlàg process W. On each compact[a,b]⊂I it also converges in expected supremum norm:

    E sup_(lambda in[a,b]) |W_n(lambda)−W(lambda)| -> 0.                (1.1)

In particular it converges almost surely in the local Skorokhod J1 topology, and hence in probability as requested by the original theorem. No fourth moments, variance assumption, Hölder increment bound, or independence of offspring increments is required.

Theorem1 is not the desired endpoint theorem under only X log X. There are integrable offspring laws with finite X log X and no moment of any order above one. The process-law uniqueness partial from Turn1 applies under(P), but simple descriptions of the binary/geometric/Poisson limiting processes remain a separate gap.

## 2. A maximal inequality for independent monotone processes

Let Y_1,...,Y_m be independent nonnegative nondecreasing càdlàg processes on[a,b], with E Y_i(b)^p<infinity, 1<p≤2. They need not be identically distributed and need not have independent increments. Then

    E sup_t |sum_i (Y_i(t)−E Y_i(t))|^p
       <= C_p sum_i E Y_i(b)^p,
    C_p=(2p/(p−1))^p.                                     (2.1)

Here m can be any finite deterministic integer, including zero.

### Deterministic monotone curves and random thresholds

First fix a finite increasing grid t_1<...<t_r=b and deterministic nonnegative monotone functions f_i on it. Put w_i=f_i(b). Ignore w_i=0. Choose independent threshold indices J_i such that

    P(J_i<=j)=f_i(t_j)/w_i.

This is a probability distribution because the displayed values are nondecreasing and end at1. For independent Rademacher signs epsilon_i,

    sum_i epsilon_i f_i(t_j)
      =E_J[sum_i epsilon_i w_i 1_(J_i<=j)].               (2.2)

Conditional Jensen applied to the maximum absolute value to the power p bounds the left maximum's p-th moment by the corresponding threshold sum's moment. Conditional on the thresholds, sort the indices by J_i, breaking ties arbitrarily independently of the signs. The threshold sum at any grid point is one of the partial sums of the independent signed weights in this order. Thus its maximum is bounded by the maximum of the finite martingale of all partial sums.

Doob's Lp inequality and the elementary Rademacher moment bound give

    E_epsilon max_j |sum_i epsilon_i w_i 1_(J_i<=j)|^p
       <= (p/(p−1))^p E_epsilon |sum_i epsilon_i w_i|^p
       <= (p/(p−1))^p (sum_i w_i²)^(p/2)
       <= (p/(p−1))^p sum_i w_i^p.                       (2.3)

The middle inequality is Jensen applied to the square, since p≤2. The last uses concavity of x^(p/2). This proves the same bound for the left side of(2.2), after averaging thresholds.

For clarity, the finite martingale inequality used here is classical and does not assume a process-index filtration for the original Y_i. Its short proof uses the first crossing time of a level t to obtain

    t P(M*>t) <= E[|M_m| 1_(M*>t)],

where M* is the maximum of absolute partial sums. Integration and Hölder yield ||M*||_p≤p/(p−1)||M_m||_p. The filtration is the finite sequence of independent signs after conditioning on the thresholds.

### Symmetrization

Let Y_i' be independent copies of the processes, independent of all Y_i. Jensen with respect to the copies bounds the centered process maximum by that of sum_i(Y_i−Y_i'). The differences have the same joint law after independent sign changes. The inequality |x+y|^p≤2^(p−1)(|x|^p+|y|^p) therefore bounds its expected maximum by

    2^p E_(Y,epsilon) max_j |sum_i epsilon_i Y_i(t_j)|^p.

Apply(2.3) conditional on the sampled curves Y_i. This proves(2.1) on every finite grid. Exhaust a countable dense grid including b. Càdlàg paths determine the supremum on that grid, and the mean functions are càdlàg by domination by the integrable endpoint values. Monotone convergence proves(2.1) on[a,b]. This also avoids a nonseparable supremum measurability assumption.

The key point is that random thresholds represent deterministic monotone curves after conditioning. They do not posit independent increments or a martingale in the parameter t for the original offspring processes.

## 3. Apply the inequality to one generation

Let F_n contain all offspring-process copies used before generation n. Conditional on F_n, the entire function Z_n(lambda) is known and nondecreasing, and the new copies X_(n,i) are independent of it. Put M=Z_n(b), which is finite almost surely. For i=1,...,M define

    Y_i(lambda)=1_(i<=Z_n(lambda)) X_(n,i)(lambda).

These are conditionally independent nonnegative nondecreasing càdlàg processes, although their activation thresholds can differ. Their conditional means are lambda 1_(i<=Z_n(lambda)), so

    sum_(i=1)^M (Y_i(lambda)−E[Y_i(lambda)|F_n])
       =Z_(n+1)(lambda)−lambda Z_n(lambda).              (3.1)

Their endpoint p-th moments are all E X(b)^p. Applying(2.1) conditional on F_n and then averaging, with E Z_n(b)=b^n, gives

    E sup_lambda |Z_(n+1)(lambda)−lambda Z_n(lambda)|^p
       <= C_p b^n E X(b)^p.                             (3.2)

No p-th moment of Z_n(b) is used; only its first moment appears. This is where the monotone-process inequality avoids the variance and increment conditions in the source's tightness proof.

Consequently,

    E ||W_(n+1)−W_n||_infinity,[a,b]^p
       <= C_p a^(-p) E X(b)^p (b/a^p)^n.                (3.3)

## 4. Uniform convergence on small intervals and then on all compacts

First suppose b<a^p. Taking p-th roots in(3.3) yields

    sum_(n>=0) E ||W_(n+1)−W_n||_infinity,[a,b]
       <= (2p/(p−1)) a^(-1) (E X(b)^p)^(1/p)
                      /[1−(b/a^p)^(1/p)] < infinity.   (4.1)

Tonelli implies that the sum of these nonnegative supremum norms is finite almost surely. Hence the martingales converge uniformly on[a,b], almost surely. The tail of the expected sum also proves convergence in expected supremum norm. The uniform limit of càdlàg functions is càdlàg. It agrees at each fixed parameter almost surely with the scalar martingale limit, is nonnegative, and has mean1 there by the L1 convergence.

For a general compact[a,b], choose one p∈(1,2] with E X(b)^p<infinity and a finite partition a=t_0<...<t_r=b so fine that t_(j+1)<t_j^p. Such a partition exists because x^p−x is continuous and strictly positive on[a,b]. On each subinterval the same endpoint moment bounds X(t_(j+1)) by X(b), and(4.1) applies. Taking a finite union gives uniform convergence on the full compact, almost surely and in expected supremum norm. A countable compact exhaustion of I supplies one locally càdlàg version and locally uniform convergence on a probability-one event.

Uniform convergence implies J1 convergence using the identity time change. No separate alignment of random jumps is assumed; the maximal bound controls the actual whole functions on the given coupling.

## 5. A bounded source process outside the original increment hypothesis

The theorem genuinely removes a restriction on how jumps cluster. Let T be uniform on[0,2). Independently let R≥4 have tail P(R>=r)=4/r for r≥4, and set D=2^(-R). Put V=(T+D) modulo2. For lambda∈I=(2,4), define

    X(lambda)=2+1_(T<=lambda−2)+1_(V<=lambda−2).          (5.1)

This is a nondecreasing càdlàg integer-valued process, bounded by4. Both T and V are uniform on[0,2), since conditional on D the second is a rotation of T. Hence E X(lambda)=lambda. Every moment in(P) is finite, so the uniform convergence theorem applies.

Nevertheless the first inequality in the source's(H) fails for every kappa>1/2. Set delta_n=2^(-n), n≥5, and use lambda_1=3−delta_n, lambda_2=3, lambda_3=3+delta_n. On

    T in[1−delta_n/2,1),     D in[delta_n/2,delta_n],

there is one jump in each adjacent interval and no wrap around2. Thus both increments equal1. Since

    P(delta_n/2<=D<=delta_n)=4/n−4/(n+1)=4/[n(n+1)],

we have

    E[(X(lambda_2)−X(lambda_1))²
      (X(lambda_3)−X(lambda_2))²]
       >= delta_n/[n(n+1)].                             (5.2)

Dividing by (2delta_n)^(2kappa) gives a quantity tending to infinity for every kappa>1/2. No finite local constant C can give the source bound. The other increment bound is harmless here: X³≤64 and E[X(lambda_3)−X(lambda_2)]=lambda_3−lambda_2.

This is a bounded admissible process with strongly clustered dependent jump times. It is an example outside(H) for which the proved stronger convergence holds, not a counterexample to the original weak-moment conjecture.

## 6. Exact remaining endpoint gap

(P) is stronger than(L). For a concrete frontier model, let Y>=2 have tail P(Y>=m)=2(log2)^3/[m(log m)^3] for integers m>=2 (and P(Y>=1)=1). These decreasing tails define a finite-valued integer law, with finite mean mu>2 and finite E[Y log Y], but E Y^(1+epsilon)=infinity for every epsilon>0, by the tail-sum test. Let P_t be an independent rate-one Poisson process and define X(lambda)=Y+P_(lambda−mu) on I=(mu,infinity). It is a source-admissible nondecreasing càdlàg integer process with mean lambda, finite X log X at every parameter, and no moment of any order above one. Thus the remaining endpoint includes genuine models, not only a formal limit of the estimates.

The constant p/(p−1) in the maximal inequality diverges at p=1. The interval condition b<a^p also collapses as p decreases to1. Neither passing p down to1 nor the L1-function result from Turn1 proves the required X log X endpoint. A genuinely endpoint maximal estimate or a valid model counterexample is still needed.

The law is abstractly determined in the finite-dimensional integrable class by Turn1, and this turn now supplies a càdlàg version under(P). It does not provide the requested simple descriptions of the binary, geometric or Poisson full processes. The original bundle therefore remains unresolved at2/5 substantive turns.

## 7. Credit and controls

The method combines classical symmetrization, random-threshold representations of monotone functions, Doob's finite martingale maximal inequality and elementary Galton–Watson first moments. The proof above supplies every reduction needed for the source coupling. Mailler–Marckert's original theorem, scalar Kesten–Stigum and the source's functional-topology distinction retain credit. No claim is made that this partial theorem or its method is historically new.

The finite checker verifies deterministic monotone-grid controls, common offspring-copy conditional centering, partition arithmetic and the bounded clustered-jump example. These checks are diagnostics; they do not replace the arbitrary-process maximal inequality or its infinite-generation application.
