# Structural and deterministic review of the graded staircase example

Shared PASS3, 14 October 2026. Reviewed `pass3_kernel_bounds/GRADED_CELL_OBSTRUCTION.md`, 6694 bytes, SHA-256 `e7f64b750aa2671a0bc64b5269e86572f7cd7333339aefbae7e8e82203aa2d81`.

## Verdict

**Accepted as a deterministic witness to the stated logical limitation.** The increasing-state chain is realized by the actual canonical greedy kernel. Its largest cell has limiting fraction 1/3, every fixed initial or final cell segment has vanishing mass, and no noninitial cell falls in a strictly negative one-neighbor entropy cone. Its permutons do not approach the anti-diagonal.

This is not a counterexample under the uniform avoidance law. No lower bound on its uniform probability, or claim that it evades all isolated-block estimates, is accepted or asserted.

## Canonical construction

For upper I_a with a >= 2 and lower I_b, put the first upper point first, then all lower points, then the remaining upper points. The lower maximum is bracketed by an increasing upper pair. A forbidden 1324 would require two lower points separated by an upper point, which this shuffle does not have. The internal increasing states avoid the designated three-point patterns. Thus every proposed edge is a genuine K edge, not an arbitrary gridding.

The exact transfer theorem reconstructs one canonical avoider from the specified path and its edge choices. S fixes increasing states, so every actual cell is increasing even when its original parity is even.

Summing the sizes `2,4,...,2^k,2^(k-1),...,4,2` gives `n_k=3*2^k-4`, while the maximum is 2^k. Fixed initial and final segments contain a bounded number of points depending only on the segment length, so their normalized mass vanishes. Every existing predecessor/current ratio is 1/2 or 2.

## Entropy-cone check

For a noninitial cell of size a and predecessor b, one has b >= a/2. If a >= epsilon*n and b <= delta*n, then delta >= epsilon/2. With 0 < delta < 1/2, monotonicity and concavity of binary entropy yield `h(delta) >= h(epsilon/2) >= epsilon*log 2`. The first-cell rate constant satisfies gamma <= log 2, so the displayed one-neighbor rate cannot be strictly negative on any such cell.

The qualification “noninitial” is essential and is explicit in the accepted derivative. The first cell has size two, and for each fixed epsilon > 0 it eventually fails the macroscopic-size condition. Thus it causes no asymptotic exception.

For the relative-size cone, f is increasing and `f(1/2)>log 2>=gamma`. A parameter c satisfying f(c)<gamma is below 1/2, whereas every existing predecessor has b/a >= 1/2. This verifies the claimed compatibility with that already stated rate bound; it is not a separate proof of the probability estimate.

## Failure of anti-diagonal convergence

The central cell alone contributes binom(2^k,2) increasing pairs, so the usual finite-permutation increasing-pair density has liminf at least 1/9. Under the square-spread convention, the difference from the permuton two-point density is at most 1/n: the only exceptional sampling event is choosing the same small square twice.

Two-point pattern density is continuous for weak permuton convergence because the event boundary consists of coordinate ties, which have zero product measure under uniform marginals. Since the anti-diagonal has increasing-pair density zero, these permutons cannot converge to it.

All assertions are all-size deterministic consequences of the accepted kernel. They do not establish anything about the probability of this family among all size-n avoiders.
