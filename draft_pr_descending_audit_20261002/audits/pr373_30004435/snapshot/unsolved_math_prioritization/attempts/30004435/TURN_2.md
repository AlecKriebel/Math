# Turn 2: observable tail quotients for finite hidden Markov processes

This turn extends the first-turn probability-only classification to every deterministic observation of a finite stationary Markov chain, with a finite linear-algebra test for the surviving tail information. Stochastic finite-alphabet emissions reduce to this case by enlarging the Markov state. The unrestricted stationary-process method request remains unresolved. No novelty claim is made for the standard Markov/observable-space ingredients.

## 1. Statement and the finite hidden phase variable

Let Y be a stationary Markov chain with s supported states, transition P and stationary distribution pi. Let X_k=f(Y_k) take values in a finite alphabet A. Let Z denote the recurrent-class/cyclic-phase variable from Turn 1, and let D be the least common multiple of the class periods. All Z values considered have positive probability. Conditional on Z=z, the chain and its observation are invariant under shift by D, with exponential mixing of finite cylinders along this skeleton.

For a word w in A^l let

    p_z(w)=P(X_[0,l−1]=w | Z=z).

Put z~z' if p_z(w)=p_z'(w) for every finite word. Denote this finite quotient by Q(Z).

**Theorem.** Each of the past, future and bilateral tail fields of X equals sigma(Q(Z)), modulo null sets. Moreover the equivalence relation is determined by words of length at most s−1 (including the empty word when s=1).

Distinct hidden phases need not remain distinguishable after observation. The quotient, rather than the original hidden phase, is essential.

## 2. Recovering the conditional law in either remote direction

Fix z and a finite word w. For integer k set

    I_k=1{X_[kD,kD+l−1]=w}.

Under P(.|Z=z), the I_k are stationary. Their covariances are bounded in absolute value by C rho^|k−j| once the windows do not overlap, for constants C<infinity and rho<1 depending on z and the word. Indeed condition on the hidden state at the end of the earlier block; the finite cyclic mixing estimate from Turn 1 makes the distribution at the start of the later block uniformly close to its conditional stationary phase distribution. The finitely many overlapping separations can be absorbed in C. The same bound applies when both indices are negative, by stationarity and symmetry of covariance; no reversibility is required.

Consequently the variance of the average of N consecutive I_k is at most C'/N. Chebyshev along N=j² and Borel–Cantelli give almost-sure convergence along the squares to p_z(w). Since 0<=I_k<=1 and (j+1)²/j²→1, the averages between successive squares have the same limit. This proves a probability-only strong law in both directions.

The limiting future average is unchanged by deleting any finite number of initial terms. For every m it can be computed using only windows with kD>=m. The past average similarly uses only windows ending at kD+l−1<=−m. Thus the random vector (p_Z(w):w finite) is measurable in both completed one-sided tails. There are only finitely many z and countably many words, so the statements hold simultaneously outside one null set. In particular sigma(Q(Z)) is contained in both tails.

## 3. The upper bound and equality of conditional laws

Any X-tail event is a Y-bilateral-tail event because each observed coordinate is a function of the corresponding hidden coordinate. Turn 1 therefore makes it an event h(Z), with h taking values0 or1. We must show h is constant on equivalence classes of ~.

First, equality of all forward word probabilities implies equality of the entire two-sided conditional X laws. Given a cylinder whose coordinates include negative times, translate the cylinder by a sufficiently large multiple of D so that all its coordinates are nonnegative. Conditional D-stationarity preserves its probability. Fill any gaps and sum contiguous word probabilities. This proves equality on a generating cylinder algebra and hence on all measurable X events.

If z~z', an X-measurable event A=h(Z) has conditional probability h(z) under z and h(z') under z'. Equal conditional observation laws force these two numbers to agree. Therefore h factors through Q. Every bilateral X-tail event lies in sigma(Q(Z)); Section2 supplies the converse inclusion already in each one-sided tail. This proves all three equalities. No exchange of an intersection with a join or conditional sigma field is used.

## 4. A finite word-length certificate

Write alpha_z for the conditional row distribution of Y_0 given Z=z. For a in A define

    M_a=diag(1{f(i)=a}) P.

For w=a_1...a_l put M_w=M_(a_1)...M_(a_l), and M_empty=Id. Since P1=1,

    p_z(w)=alpha_z M_w 1.

In the real vector space of columns of length s define

    V_k=span{M_w 1: |w|<=k}.

Then V_0=span{1}, and V_(k+1) is the span of V_k and all M_a V_k. If two consecutive spaces agree, the space is invariant under every M_a and contains every later word column. Otherwise its dimension increases by at least1. Since the ambient dimension is s, stabilization occurs by V_(s−1).

Therefore (alpha_z−alpha_z') vanishes on every word column if and only if it vanishes on the words of length at most s−1. This is an exact linear-algebra certificate, not a finite experimental guess. Rational P permits exact arithmetic. The same argument is the usual finite-dimensional observable-space construction; the contribution here is an explicit certificate for the scoped tail quotient, without a novelty assertion.

For finite stochastic emissions e_i(a), the joint process (Y_k,X_k) has transition P(i,j)e_j(b) and stationary law pi(i)e_i(a). Remove zero-mass joint states and apply the theorem to the deterministic projection onto X. The stated word bound then uses the number of supported joint states. No claim of a sharper hidden-state bound is needed here.

## 5. Examples, controls and the remaining obstruction

A deterministic six-cycle observed as001001 has three surviving observable phases, although its hidden phase variable has six values. A constant observation collapses every hidden phase and recurrent class. Conversely two closed aperiodic classes with iid binary observations of different biases retain their class label in both tails through empirical frequencies.

verify_turn2.py checks exact word probabilities, the invariant observable-space construction, stabilization by s−1, and agreement of short-word and longer-word quotients on finite deterministic observations of cyclic chains and mixtures. It separately enumerates hidden paths to check matrix-word probabilities. These are algebraic controls; the all-length theorem is proved above.

This argument cannot classify arbitrary finite-alphabet stationary processes: there need not be a finite hidden phase variable or a finite-dimensional invariant word space. Replacing the original process by increasingly large hidden-Markov approximations would require a justified tail-limit passage, which Turn 1's examples show cannot be taken for granted. The source's no-entropy condition is still unmet in full generality.
