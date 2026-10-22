# Structural review of the arbitrary-location isolated-block count

Shared PASS3, 14 October 2026. Reviewed `pass3_kernel_feasibility/ISOLATED_BLOCK_TAIL.md`, SHA-256 `f61fde65b505d884a7bf9f9432edf5d937f5009a8168246f67052484890d7fdd`.

## Verdict

**Accepted for the exact marked-block encoding and finite inequality (1).** The proof retains both exterior path laws and both boundary shuffle costs. It is an actual full-class count, not a conditional-uniformity assumption about a remainder. The concentration reviewer is separately checking the stated exponential consequence.

This estimate concerns blocks with the specified boundary-mass restriction. It does not prove largest-cell concentration without that restriction.

## Fragment normalization

The accepted exact kernel is homogeneous in the normalized cell states: the same directed K governs every edge, irrespective of its original parity. Cutting before and after a consecutive block therefore produces three legitimate state paths. If a fragment began at an originally even cell, interpreting its first normalized state as an odd cell simply realizes the corresponding valid canonical path supplied by the exact encoding theorem. It does not change state sizes, edge multiplicities, or the number of data choices.

An empty fragment has one encoding. Nonempty prefix and suffix fragments of masses p and q have exactly a_p and a_q data choices. The marked fragment of mass m, with at most fixed K cells, has exactly b_(m,K) choices. Its terminal cell can be treated as terminal in its own fragment because that fragment's whole remainder is that cell; removing an outgoing edge causes no hidden maximality condition.

## Reconstruction and boundary costs

Concatenating the three state paths and restoring the two cut edge shuffles reconstructs the full canonical path uniquely. The number of cells in the prefix locates the marked block, so there is no separate unrecorded location choice. This remains true when one or both exterior fragments are empty.

For fixed three fragments, let l and r be the adjacent exterior cell sizes. Each boundary shuffle is a binary interleaving, with one inside endpoint of size at most m. Thus its multiplicity is bounded by binom(m+l,l) or binom(m+r,r). Missing exterior neighbors have size zero and contribute the correct factor one.

For k=l+r, the convolution

`sum_(j=0)^k binom(m+j,j) binom(m+k-j,k-j) = binom(2m+k+1,k)`

follows from the coefficient of x^k in `(1-x)^(-2m-2)`. It dominates each individual product and increases with k. Replacing k by floor(delta*m) is therefore valid for every admissible marked object. Once this uniform edge bound is taken, discarding the boundary restriction only enlarges the exterior count.

There are n-m+1 possible exterior mass splits p+q=n-m. Fixed-size skew concatenation is injective and preserves 1324 avoidance, so a_p a_q <= a_(n-m). Summing the fragment counts gives exactly the displayed finite bound, with no exponential factor hidden in the marking or normalization.

## Asymptotic interface

The finite inequality has the inputs required by the author's rate calculation: a fixed-K internal growth gap and an explicit boundary entropy. Any claimed probability conclusion must keep K fixed and retain the isolation condition. No uniformity in growing K or in arbitrary macroscopic cell clusters is supplied by the encoding. In particular, the argument does not exclude profiles with many successively smaller but still macroscopic neighboring cells.

All earlier accepted files and receipts are preserved. This report adds no new structural theorem beyond its independent verification of the author's finite count.
