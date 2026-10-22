# Independent review of the exact greedy-staircase kernel

Same PASS2 continuation,14 October2026. Reviewed final artifact: `pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md`,14208 bytes, SHA-256 `dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03`.

## Verdict and scope

**Accepted as an exact combinatorial reduction and completion-bias obstruction.** The adjacent-pair kernel, canonical reconstruction, marked-cell factorization and stated analytic domain are justified. The explicit increasing-to-decreasing kernel formula and resulting exponentially large incoming weight are also correct. The last section's exponential-fugacity implication is valid as a conditional statement; its hypothesis is not established.

No largest-cell concentration, spectral compactness, convergence at the radius, or1324 permuton limit is accepted by this report. The author's separate prospective squared-kernel target is not a proved estimate and is outside this acceptance.

## 1. Pair-local avoidance

The first and last points of a1324 occurrence are its coordinatewise minimum and maximum. Thus they form an increasing pair and cannot lie in nonadjacent staircase cells, since all such pairs are inverted. If they lie in one cell, their coordinate rectangle remains in it. For vertical adjacent cells the rectangle stays in their common column; for horizontal adjacent cells it stays in their common row. Every other staircase cell is outside that rectangle. All intermediate occurrence points must therefore lie in the same cell or adjacent pair.

This proves that pairwise1324-freeness is sufficient globally. The individual cell classes avoid1324 because each of132 and213 is a subpattern of1324.

## 2. Local witnesses imply canonical maximality

For a vertical pair, the lower maximum b must be between the endpoints a,c of an upper ascent. If a lower point d were left of all upper points, it could not equal b, and its value would be below b. Then d,a,b,c would be1324. Consequently the column begins in the upper cell.

Anti-diagonal reflection gives the dual fact: a horizontal forward witness forces the row maximum into the left cell. These endpoint consequences are essential. They ensure that, at each odd step, the next cell contains the actual largest remaining value, and at each even step it contains the actual leftmost remaining point. The local witness then excludes precisely the first point beyond the maximal current frontier. This proves global canonical greediness by induction, including the terminal-cell case.

Conversely, maximal greedy frontiers produce exactly these witnesses. No extra condition on distant cells is being discarded. I raised the next-cell endpoint issue during review; the written proof addresses it explicitly and correctly.

## 3. Reconstruction and parity normalization

Vertical-pair position shuffles fix the order within each column; horizontal-pair value shuffles fix the order within each row. Each cell's fixed permutation matches its local position and value orders. The incident edges at a cell act on different coordinates, so their choices do not conflict. Together with the fixed column/row order, the data reconstruct one gridded permutation.

Pair-local avoidance and maximality make this its canonical gridding. Distinct data cannot give the same ungridded permutation because that gridding is unique. Thus the product of edge counts is an exact multiplicity, not an assumed independent-cell probability law.

The involution S=reverse-complement-inverse swaps213 and132, fixes1324, and turns an even horizontal pair into the same oriented vertical kernel. No transpose or reversal of the kernel arguments is missing. In particular K(1,12)=0 while K(12,1)=1; reversibility cannot be assumed. Decreasing states have no outgoing witness and are terminal.

## 4. Marked-cell weights and domain

For each normalized state A, the prefix and suffix path sums retain every incident edge factor. Gluing them at A counts permutations with a distinguished canonical A cell exactly, so the weight is `z^|A| ell_A h_A`. Summing over large A gives the expected number of large cells after coefficient extraction and division by the exact full-class count. The largest-cell probability is bounded by that expectation.

Formal coefficient finiteness follows from positive cell sizes and finite state sets at every bounded size. For0<z<rho, the full counting series and its derivative converge. The first-state and last-state interpretations bound the individual path sums, and the once-marked sum is bounded by zF'(z) because there are at most n cells in size n. Therefore all rearrangements of these nonnegative sums are legitimate in the claimed domain.

Nothing here proves a bounded or self-adjoint operator on an unspecified function space, a Hilbert–Schmidt norm, or a boundary value at rho. The draft correctly makes none of those inferences.

## 5. Exact incoming bias

When the upper cell is I_k and the lower one is J_m, every interleaving is1324-free. Splitting a possible occurrence by its number of lower points shows that it would require an increasing pair in J_m, a213 in I_k, or a132 in J_m, all impossible.

The lower maximum is its first lower point. The witness requires it after r upper points with1<=r<=k-1. The remaining interleavings are counted by `binom(k-r+m-1,k-r)`. Summing gives exactly

`K(I_k,J_m)=binom(k+m-1,k-1)-1`,

including k=1. Summing just these one-predecessor prefixes yields

`ell_(J_m)(z)>=1+z[(1-z)^(-m-1)-(1-z)^(-1)]`.

For each fixed0<z<rho, this grows exponentially in m. Hence an all-state subexponential incoming-weight bound is genuinely false in the exact1324 encoding. It remains a counting-weight obstruction, not a positive uniform probability of a macroscopic cell: the factors z^m, h_(J_m)=1 and the full coefficient normalization remain indispensable.

## 6. Conditional exponential-fugacity criterion

Assume the unproved hypothesis that one fixed eta>0 makes the once-marked series H(z,exp(eta)) finite for every0<z<rho. For a fixed epsilon>0, choosing z=rho*exp(-eta*epsilon/2) and using positive coefficients gives the displayed probability upper bound. Since log a_n=n log lambda+o(n), its logarithmic rate is at most -eta*epsilon/2. Thus the implication is valid.

The trivial comparison H(z,u)<=uzF'(uz) is used for u=exp(eta)>1: the marked cell size is at most the total size, so u^cell_size<=u^total_size. That comparison only reaches uz<rho and cannot supply the stronger hypothesis. The draft correctly leaves it unproved. The cleaned statement about the crude shuffle/Catalan bound only certifies the open domain z<1/16 and does not assert divergence exactly at that boundary.

## Independent exact regressions

`check_pair_local_kernel.py` was written separately from the author's code. It counts admissible vertical interleavings directly, normalizes the even cell by S, and sums all state chains through n=8. The results1,2,6,23,103,513,2762,15793 match independent brute-force1324 avoidance. It evaluates2806 state pairs. Its output is `PAIR_LOCAL_KERNEL_FINITE_CHECKS.json`.

A further45 exact checks for positive k,m with k+m<=10 verify the increasing-to-decreasing formula; they are recorded in `INCOMING_KERNEL_FINITE_CHECKS.json`. These finite checks diagnose orientation and indexing; the acceptance above rests on the written all-size proofs.

All earlier accepted files and receipts remain unchanged.
