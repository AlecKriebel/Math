# Turn 5: non-atomic conditional-law tails and a nonmixing boundary case

This fifth substantive turn broadens the empirical-law argument beyond a finite hidden state. It then examines a source-admissible binary process with an infinite, nonmixing common tail. The full entropy-free method request remains unresolved after five turns. The packet stops author search here.

## 1. A conditional-mixing mixture theorem

Let Theta be a random parameter in a standard Borel space, and let mu_theta be a measurable probability kernel on A^Z for finite A. Suppose there is a fixed positive integer D such that every mu_theta is invariant under the shift by D, for almost every theta. Suppose also that each component has the strong-mixing property

    alpha_theta(n)=sup |mu_theta(B intersect C)−mu_theta(B)mu_theta(C)| →0,

where B ranges over sigma(X_k:k<=0) and C over sigma(X_k:k>=n). No rate uniform in theta and no countability or identifiability of the parameter are assumed. If applying this as a subclass of the source, assume the mixture itself is invariant under the unit shift.

Let M be the random two-sided law mu_Theta, regarded as a random element of the standard Borel space of probability measures on A^Z.

**Theorem.** Under the mixture,

    T^- = T^+ = sigma(M) modulo null sets.                 (1.1)

If additionally the bilateral tail is trivial under almost every mu_theta, then it too equals sigma(M). The extra bilateral hypothesis is not inferred from alpha-mixing.

## 2. Recovering M without a uniform strong law

For any forward word w of length l, put p_theta(w)=mu_theta(X_[0,l−1]=w). Under each component, average its indicators at times kD for k=1,...,N. Conditional D-stationarity gives the correct mean p_theta(w). The covariance at lag h tends to0: shift the earlier block by a fixed multiple of D until its right endpoint is at most0, then the later block is separated by a gap tending to infinity, so alpha_theta controls the covariance. The finite initial separations are harmless.

The variance of the average tends to0 by Cesàro summation of these bounded, vanishing covariances. All variances are bounded by1, so dominated convergence over theta proves convergence in joint L² to p_Theta(w). The same calculation for negative sampling times gives the identical limit, since conditional D-stationarity makes the reversed covariance sequence the same for a fixed real-valued indicator. No reversibility is assumed.

For every fixed m, omit finitely many initial future blocks so the average is measurable in sigma(X_k:k>=m); this changes the average by a quantity tending uniformly to0. Thus its L² limit p_Theta(w) lies in the completed future field for every m. Negative averages similarly put it in the past tail. Countably many words suffice.

The vector of these probabilities determines the full conditional two-sided law: translate any finite cylinder by a large multiple of D into nonnegative coordinates and sum appropriate contiguous word probabilities. Hence sigma(M) lies in both tails. Measurability can be seen directly from these countably many coordinates on the space of laws. No parameterwise choice of a convergence subsequence, and no common mixing rate, was needed.

## 3. The reverse inclusion under disintegration

First the component one-sided tails are trivial. The proof from Turn3, Section3, works with D-stationarity: translate a fixed cylinder by a suitable multiple of D until it is in the past, separate a future-tail event arbitrarily far, and use alpha_theta(n)→0. For a past-tail event translate the other way. Independence from every cylinder gives independence from itself.

Now fix one global tail event A and choose a Borel representative on A^Z. For every m it agrees almost surely under the mixture with some Borel event measurable in the corresponding remote half-line. Disintegrating these equalities for the countably many m shows that, for almost every theta, this same A is measurable in every completed component remote field. Consequently mu_theta(A) is0 or1.

In the joint space this implies

    1_A(X)=mu_Theta(A) almost surely,

because the conditional variance of the indicator is mu_Theta(A)(1−mu_Theta(A))=0. The right side is the evaluation M(A), a measurable function of the random law M. Thus A belongs to sigma(M). Notice that a redundant parameter label is not recovered: only its induced path law is. The bilateral argument is identical if component bilateral triviality is separately assumed. This proves(1.1).

As a concrete extension of Turn2, arbitrary mixtures of finite-state hidden Markov models with a common finite bound s on the hidden state count fit after adjoining each model's recurrent class and cyclic phase to the parameter, and taking D=lcm(1,...,s). The phase-conditioned hidden laws, and hence their observations, are mixing and bilaterally tail-trivial by the finite-chain proof. The model parameters themselves may range over an uncountable set. The statement is about the induced conditional observation law, not recovery of unidentifiable model labels.

## 4. Exact non-atomic example: a random iid bias

Choose P uniformly on[0,1]; given P=p, take a two-sided iid Bernoulli(p) process. The overall law is stationary but not mixing. The theorem gives all three tails equal to sigma(P), as the conditional word law determines p. An independent redundant label attached to P would not enter the observable tails.

For N observations on either side, let K and L be their success counts. Direct beta integration gives

    P(K=k)=1/(N+1),
    E[P | K]=(k+1)/(N+2),
    E[(K/N−P)²]=1/(6N).

With the two blocks conditionally independent given P,

    E[((K+1)/(N+2)−(L+1)/(N+2))²]
       =N/[3(N+2)²].                                    (4.1)

This is an exact finite-window version of the Turn1 defect for f=X_0 and disjoint observation blocks not containing0. Every gap gives the same formulas by conditional independence. The defect tends to0 while the limiting tail remains nontrivial and non-atomic. The elementary beta identities are verified below with rational arithmetic; no entropy quantity is used.

## 5. Why conditioning on ergodic components is still insufficient

Let alpha be irrational in(0,1), let U be uniform on[0,1), and set

    X_k=floor(U+(k+1)alpha)−floor(U+k alpha),  k in Z.

This is a binary stationary process: increasing time by1 replaces U by U+alpha modulo1. Every remote future determines U. Indeed, from the block starting at m, set V={U+m alpha}; the cumulative sum of its first n symbols is floor(V+n alpha). Writing q_n=floor(n alpha) and t_n={n alpha}, the difference from q_n equals

    1{V>=1−t_n}.

The thresholds1−t_n are dense in(0,1), by density of an irrational rotation. Their comparison bits determine V uniquely (as the supremum of the thresholds at which the bit is1, including0). They therefore recover U by subtracting m alpha modulo1. This is an explicit measurable reconstruction from each future half-line.

For the past ending at m−1, the sum of its last n symbols is

    −floor(V−n alpha)=q_n+1{V<t_n}.

The dense thresholds t_n again determine V and U. Hence both one-sided tails, and consequently the bilateral tail, equal the entire sigma(U) field. This example satisfies the original finite-alphabet and stationarity requirements. It verifies equality in another special case; it is not a counterexample to the source.

It also shows why conditioning on the invariant-event field does not produce the mixing hypothesis of Section1. Irrational rotation is ergodic: a shift-invariant square-integrable function has Fourier coefficient c_j satisfying c_j=e^(2 pi i j alpha)c_j, so all nonconstant coefficients vanish. Thus the invariant-event field is trivial. Every positive power is still ergodic, but none is mixing: there are integers n_j tending to infinity with {n_j D alpha} tending to0, and translates of any interval indicator then converge to itself in L¹. Its correlation tends to its mean rather than the square of its mean.

Since the binary itinerary reconstructs U, it generates this same nonmixing system. Strong mixing of the binary process would imply ordinary mixing of the whole shift system by approximation with finite cylinders, contradicting the interval calculation. No finite D and no conditioning on its ergodic-component label turn this example into the conditional-mixing subclass. Basic Fourier/density facts here are used only for this classical rotation obstruction, not as a purported general probability-only solution.

## 6. Final gap and verification boundary

verify_turn5.py checks the beta-binomial formulas and(4.1) exactly. For alpha=sqrt(2)−1 it uses exact arithmetic in Q(sqrt(2)), with integer sign comparisons, to verify forward and backward reconstruction intervals, telescoping counts and shift recoding. No floating-point test is used as a certificate. Finite shrinking-interval checks support the explicit reconstruction, whose all-length proof uses irrational density.

After five genuine turns the remaining question is still: prove the one-sided tail equality for every stationary finite-alphabet process without entropy. We have not shown that every process is a finite hidden-Markov observation, satisfies uniform summable continuity, admits a suitable finite-mean finitary isomorphism, or is a mixture of conditional-mixing laws. The original theorem is known through entropy-based arguments, but those do not fulfill the requested method. The disposition proposed for review is unsolved5/5, with the complete scoped results above retained and prior credit explicit.
