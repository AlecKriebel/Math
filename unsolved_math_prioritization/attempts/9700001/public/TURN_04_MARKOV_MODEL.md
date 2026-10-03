# Attempt 4: fully observed finite-state Markov models

Suppose S_0,...,S_n is a time-inhomogeneous Markov chain with finite state sets K_t, known rational transition matrices P_t, and known rational initial distribution pi_0. The full information is F_t=sigma(S_0,...,S_t). Let X_t=g_t(S_t), with rational rewards. This model allows exponentially many histories but only polynomially many state-time pairs. It is an additional hypothesis, not a consequence of adjacent conditional-mean tests.

Write pi_t for the forward distributions and

r_t(s)=sum_u P_t(s,u)g_{t+1}(u)-g_t(s),
q_t(s)=pi_t(s)r_t(s).

## Theorem 4A: polynomial exact certificates with full-history validity

X is an F-martingale iff q_t(s)=0 for every state-time pair. Equivalently it satisfies the deterministic tests and one-step tests T=t+1 on {S_t=s}, T=t otherwise, as in Attempt 1. At most n-1+sum_{t<n}|K_t| tests suffice, even though the sigma-fields F_t may have exponentially many atoms.

Proof. The Markov hypothesis gives E[X_{t+1}-X_t|F_t]=r_t(S_t). This is zero almost surely iff r_t(s)=0 for every reachable state s, equivalently q_t(s)=0. Relation (1) from Attempt 1 proves the equivalence with the listed tests without requiring sigma(S_t) to be nested. QED.

Furthermore every full-history stopping time T satisfies

|E X_T-E X_0| <= sum_{t,s}|q_t(s)|.             (5)

Indeed E[1_{T>t} Delta_t]=E[1_{T>t}r_t(S_t)], whose absolute value is at most E|r_t(S_t)|. Unlike Attempt 2's counterexample, the Markov conditional-law identity holds after conditioning on the entire past. Null/unreachable states need no drift restriction.

## Theorem 4B: exact optimal deviation and a constructed stopping rule

Define the two backward recursions

U_n(s)=L_n(s)=g_n(s),
U_t(s)=max(g_t(s),sum_u P_t(s,u)U_{t+1}(u)),
L_t(s)=min(g_t(s),sum_u P_t(s,u)L_{t+1}(u)).

Then

sup_T E X_T=sum_s pi_0(s)U_0(s),
inf_T E X_T=sum_s pi_0(s)L_0(s),
A(X):=sup_T |E X_T-E X_0|
 =max(sum pi_0 U_0-E X_0, E X_0-sum pi_0 L_0).  (6)

Both extrema are attained by first entrance into the respective stop regions, with stopping forced at n. The suprema allow all full-history stopping times.

Proof. Backward induction on a fixed observed history gives the upper bound U_t(S_t) for conditional expected reward of any policy that has not stopped. Stopping now gives g_t(S_t). Continuing gives at most the expectation of U_{t+1}, by the induction hypothesis and Markov conditioning. The maximum of these is U_t. The policy that stops when the first option attains the maximum, continuing otherwise, attains equality at every induction step. Integrating over pi_0 proves the maximum claim. Reverse inequalities and choose the minimum to prove the second. Every policy's expectation lies in this interval, and stopping at 0 supplies E X_0, so its maximal absolute deviation is (6). External randomization adds only mixtures of deterministic policies and cannot improve either endpoint. QED.

Thus a precise model-relative definition is A(X)<=epsilon: no permitted stopping rule has absolute expected deviation exceeding the chosen tolerance. Membership and an offending rule when A(X)>epsilon are computable by the recursions. A finite rational table has polynomial input bit length; the recursions use polynomially many operations and retain polynomial bit length. One way to see the latter is to take the product of all input denominators: denominators of path probabilities divide this product since each time-indexed transition occurs at most once on a path; sums introduce no worse than that common denominator, and numerators need only polynomially many extra bits. Reward denominators and the initial distribution are handled by the same argument. Magnitudes are bounded by the largest input reward magnitude.

The usual Snell-envelope/backward-induction method retains its classical credit. This finite proof is included in full; no new optimal-stopping theorem or historical novelty is claimed.

## Outcome and limits

The model provides the requested constructive implication with full-history guarantees and polynomial complexity in its explicit state-transition description. It does not show that arbitrary processes admit a small Markov representation, that such a representation can be learned efficiently, or that the state is actually observed. If only prices are observed and hidden states matter, the full-state policy need not be implementable. If states are price-observable, the policy is a price-history stopping rule. These restrictions prevent treating this familiar special-case answer as a general resolution.
