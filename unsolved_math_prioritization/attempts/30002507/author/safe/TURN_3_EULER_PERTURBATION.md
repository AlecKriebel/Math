# Approach 3: changing a sparse set of prime coefficients

This explores a multiplicative construction route. The standard Euler-product mechanism is reconstructed independently; the withdrawn Hilberdink–Saias main theorem is not an input.

For a set P of ordinary rational primes define lambda_P(1)=1 and extend completely multiplicatively from lambda_P(p)=-1 if p is in P and lambda_P(p)=0 otherwise. Let F_P(s)=sum lambda_P(n)n^{-s}. It converges absolutely in H_1, and there

F_P(s)=product_{p in P}(1+p^{-s})^{-1}.

## Theorem 3.1: sparse changes preserve the obstruction above their absolute threshold

Let P,Q be two sets of ordinary primes. Suppose delta>0 and sum_{p in P symmetric-difference Q} p^{-delta}<infinity. There is an ordinary Dirichlet series U, absolutely convergent together with 1/U throughout H_delta, such that

F_P=U F_Q,

initially on H_max(1,delta). The function U is holomorphic and has no zeros in H_delta. Moreover

sigma_c(F_P)<=max(sigma_c(F_Q),delta),
sigma_c(F_Q)<=max(sigma_c(F_P),delta).

In particular, if sigma_c(F_Q)>delta, then sigma_c(F_P)=sigma_c(F_Q). Corresponding meromorphic continuations of F_P and F_Q have exactly the same zeros and poles, with multiplicities, in H_delta.

### Proof

Set

U(s)=product_{p in Q\P}(1+p^{-s}) product_{p in P\Q}(1+p^{-s})^{-1}.

Each factor is nonzero when Re(s)>0. On H_delta use the holomorphic power-series branch log(1+p^{-s})=sum_{k>=1}(-1)^{k+1}p^{-ks}/k. On every closed half-plane Re(s)>=delta+epsilon, the absolute values of these logarithms sum to at most a fixed constant times sum_{p in P triangle Q}p^{-delta-epsilon}. Hence their signed sum L is holomorphic, U=exp L is holomorphic and nowhere zero, and its reciprocal is exp(-L).

Expansion of the local factors produces ordinary Dirichlet series: numerators contribute the two terms 1+p^{-s}, and denominator factors the geometric series sum_{k>=0}(-1)^k p^{-ks}. At a real sigma>delta the sum of absolute coefficients is bounded by

product_{p in P triangle Q}(1-p^{-sigma})^{-1}<infinity.

The same bound applies to 1/U. This proves absolute convergence without requiring an unjustified conditional Euler product. In the common absolute half-plane, cancellation of factors gives F_P=U F_Q, including equality of each formal Dirichlet coefficient.

For completeness, multiplication by U also transfers ordinary convergence. Fix s with Re(s)>max(sigma_c(F_Q),delta), and write U=sum u_d d^{-s}. Let S_Q(y)=sum_{n<=y}lambda_Q(n)n^{-s}; these partial sums are bounded and tend to F_Q(s). The coefficient identity yields

sum_{m<=X}lambda_P(m)m^{-s}=sum_{d<=X}u_d d^{-s} S_Q(X/d).

Dominated convergence for the absolutely summable series in d gives the limit U(s)F_Q(s). This proves the first inequality for sigma_c. Apply the same reasoning to 1/U for the second. If sigma_c(F_Q)>delta, the second inequality forces sigma_c(F_P)>=sigma_c(F_Q), and the first gives the reverse inequality.

Finally, the identity extends by uniqueness wherever both sides have meromorphic continuation in the connected half-plane H_delta. Multiplication by a nowhere-zero holomorphic function preserves the order at every zero or pole. QED.

## Consequence for finite alterations

For a finite symmetric difference the hypothesis holds for every delta>0. Thus changing finitely many prime values cannot improve a positive convergence abscissa of this family. More generally, changing a sufficiently sparse infinite set cannot move an abscissa that is already to the right of its perturbation threshold.

This is more precise than the observation that finite Euler factors create no new zero in H_0: it also checks convergence of the actual ordinary series. For example, deleting a prime p from P multiplies F_P by 1+p^{-s}; the inverse geometric series is absolutely convergent on H_0.

## The unresolved construction step

The withdrawn 2018 proposal attempted a much more extensive conversion of generalized-prime models into subsets of ordinary primes. Its 2024 withdrawal does not identify a specific erroneous lemma, and this packet does not claim to locate that error. The theorem above does not repair it. A successful nonsparse construction still needs both a power-saving estimate for ordinary coefficient partial sums and global control of the divisor in the same convergence half-plane. Neither is established here. Estimated full-resolution progress: 0%; the sparse-perturbation theorem is complete.
