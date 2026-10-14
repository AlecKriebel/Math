# A graded actual staircase defeats the one-neighbor inference

Shared PASS3, row1778 /30005770, 14 October 2026.

This deterministic construction concerns the actual canonical 1324 kernel. It shows that fixed-prefix concentration plus the proved one-neighbor entropy cones cannot by themselves force largest-cell sublinearity or the anti-diagonal weak limit. It is not a uniform-probability counterexample, and it makes no claim about stronger isolated-block estimates with a fixed number of predecessor cells.

## 1. A completely specified valid kernel path

Use the normalized nonempty Av(213) states and the directed greedy kernel K from the accepted exact transfer. Let I_a be the increasing permutation of size a. The involution S fixes I_a. For every a>=2 and b>=1, choose the following specific shuffle counted by K(I_a,I_b):

    first upper point, all b lower points, remaining a-1 upper points.       (1)

The lower maximum lies between the first two upper points, so the greedy witness holds. A 1324 in this two-cell union would have to use two increasing points of each color in the position order lower,upper,lower,upper. This is impossible because every lower point lies in one consecutive block, with no upper point between two of them. The individual increasing cells avoid both 213 and 132. Thus (1) is a genuine edge and not only an unrestricted domino shuffle.

For each k>=1, take the chain of 2k-1 increasing states whose sizes are

    2,4,...,2^k,2^(k-1),...,4,2.                             (2)

For k=1 this means the single state I_2. Use edge (1) at every adjacent pair. The accepted exact canonical transfer reconstructs a unique 1324-avoiding permutation pi_k with exactly this normalized canonical cell chain and these shuffles. Consequently this construction is not relying on an arbitrary noncanonical gridding. Every actual cell is increasing, because S fixes increasing patterns.

The exact total size and maximum cell size are

    n_k=3*2^k-4,       M_k=2^k,       M_k/n_k -> 1/3.         (3)

For any fixed positive integer J, the first J and last J cell sizes are eventually 2,4,...,2^J and its reversal, respectively. Their total masses tend to zero. Every adjacent predecessor/current ratio is either 1/2 or 2.

## 2. The one-neighbor negative-rate cones never detect this family

The local rerooting estimate concerns the event that some noninitial cell has size at least epsilon*n and its predecessor has size at most delta*n. Its proved logarithmic upper bound is

    h(delta)-epsilon*gamma,
    h(x)=-x log x-(1-x)log(1-x),
    gamma=log C(1/lambda),       0<gamma<=log 2,              (4)

where 0<delta<1/2. The last bound follows from lambda>=4 and C(1/4)=2.

Suppose a noninitial cell in (2) of size a has predecessor b and satisfies a>=epsilon*n_k and b<=delta*n_k. Since b>=a/2,

    delta>=epsilon/2.

The function h is increasing on [0,1/2]. Its concavity and the chord from (0,0) to (1/2,log 2) give

    h(delta)>=h(epsilon/2)>=epsilon*log 2>=epsilon*gamma.    (5)

Therefore no noninitial cell of this family lies in any event region where the one-neighbor bound (4) is strictly negative. This holds simultaneously for all the fixed parameter pairs epsilon,delta in that range, not merely for one selected threshold.

The first-cell event itself is harmless: its size is 2=o(n_k). Thus adjoining the fixed-prefix and fixed-suffix conclusions does not eliminate this family.

There is also a relative-size version of the same local calculation, if that refinement is used. The cut-shuffle entropy for b<=c*a is at most a*f(c), where

    f(c)=(1+c)log(1+c)-c log c.

A negative-rate relative cone requires f(c)<gamma. Since f is increasing and f(1/2)>log 2>=gamma, such c is strictly less than 1/2. Again b/a>=1/2 excludes the event. This paragraph is a compatibility check, not an independent proof of that refined probability bound.

## 3. The family does not approach the anti-diagonal

Let Inc(pi) count unordered index pairs i<j with pi(i)<pi(j), and define the usual two-point pattern density

    t(12,pi)=Inc(pi)/binom(n,2).

The central increasing cell alone gives

    Inc(pi_k)>=binom(2^k,2),
    liminf_k t(12,pi_k)>=1/9.                               (6)

The anti-diagonal permuton has t(12)=0. To see directly why weak convergence to it would contradict (6), the two-point increasing event has a boundary only where the two x-coordinates or the two y-coordinates coincide. Independent samples from any permuton have zero probability of these ties because both marginals are uniform. Thus two-point pattern densities are continuous under weak permuton convergence. The finite-permutation square-spread convention changes the density by at most the probability that both points lie in the same square, namely 1/n. Hence (6) rules out an anti-diagonal limit.

This only supplies a deterministic witness to a logical gap. Its probability under the exact uniform law is not bounded below. Even the whole family could be exponentially negligible, which would be fully consistent with the conjecture.

## 4. What remains unresolved

Iterating the one-neighbor conclusion at successively smaller thresholds can lead to a geometric mass profile with finite total mass. There is no resulting contradiction with total mass one. The explicit family above realizes such a profile inside actual 1324-avoiders and the canonical exact kernel.

This note does not claim that the family evades an independently stronger estimate for isolated blocks of several cells; those estimates have to be tested on their own hypotheses. Nor does it show that a macroscopic cell is necessary for failure of every proposed geometric argument.

An unresolved sufficient analytic target remains a fixed u>1 for which

    sum_A u^|A| z^|A| ell_A(z) h_A(z)<infinity

for every 0<z<1/lambda. Here h and ell are the exact outgoing and incoming path sums. The companion note proves this with ell omitted, and shows that a diagonal Hilbert--Schmidt extension cannot supply the missing two-sided estimate beyond the counting radius.

## Source and finite-computation scope

The exact canonical transfer used here is `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`, SHA-256 dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03. Its staircase geometry is credited to Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Proposition 1 and proof:
https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf

The proof is all-size. Any finite test of the bridge or a small mountain is an indexing regression only. No queue, ledger, remote publication, or earlier accepted artifact is changed.
