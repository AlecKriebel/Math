# Status and scope

**UNSOLVED; partial interim mathematical checkpoint.** This package makes no claim that the original question is resolved.

## Exact target

For every integer N≥1, let

    F(N)=max{|A|: A⊆{1,…,N}, {n,2n,3n}⊄A for every positive integer n}.

Only n≤floor(N/3) impose constraints. Selecting two members of a triple is allowed. No pair-ratio avoidance requirement is substituted for the complete-triple condition.

The target is the arithmetic nature of alpha=lim F(N)/N. A proof that alpha is irrational would establish the stated anticipated answer; a proof that it is rational would refute it. The known existence proof, exact convergent series, additional finite values, and decimal approximations do not decide this question. A density problem for one fixed infinite set is not silently substituted for this finite-extremum limit.

## Three different minima

At cutoff X, the vertices are 2^a3^b≤X. A hitting set meets every complete triple. Let tau(X) be its unrestricted minimum size. For its excess D=sum_E(|H∩E|−1), let q0 impose D=0 and q1 impose D≤1. Thus

    tau(X)≤q1(X)≤q0(X).

The exact-one formula is all-scale. The [separate single-defect theorem](proofs/04_SINGLE_DEFECT_THEOREM.md) identifies q1 with the explicit corrected-color formula. Neither of these facts identifies tau with q1. Agreement at 200 smooth cutoffs is a finite statement only.

The scale-eight output E(X)=tau(8X)−tau(X)−floor(log_3(8X)) is the actual output. The corresponding explicit color-candidate output is a different object. Binary output for the candidate is proved; binary output for actual E at every X is unproved.

## Cutoffs and endpoints

- d_k is the k-th increasing 3-smooth number, beginning with d_1=1.
- Numeric cutoff X=192 is prefix index 25, not index 192.
- d_24=162 and tau(d_24)=7; in contrast tau(24)=3.
- d_45=1536 and d_77=19683. All complete triples at a cutoff use an inclusive vertex endpoint.
- Exceptional-patch intervals are [24·2^m,27·2^m), for integer m≥0. The upper endpoint is excluded.
- Integral endpoint values have measure zero. The jump at 192 is not part of the integral up to 192.

## Reconstruction and verification limits

This package contains newly authored reconstructed mathematics and synthetic finite certificates. Its file identities concern these included editions only; no historical byte-identity claim is made.

Public source identities are newly inspected source-file metadata, or explicitly labeled identity checks on an existing public-dataset snapshot. They are not identities of earlier authored proof editions. A manifest establishes byte identity and inventory; it does not itself establish a theorem. Finite checkers test the exact statements documented for them. Written arguments supply the all-scale reductions and analytic proofs.

No global equality tau=q1, no global binary theorem for actual E, no finite-state model for the unrestricted optimizer, and no rationality or irrationality conclusion is claimed. No exhaustive novelty search or external peer review is claimed.
