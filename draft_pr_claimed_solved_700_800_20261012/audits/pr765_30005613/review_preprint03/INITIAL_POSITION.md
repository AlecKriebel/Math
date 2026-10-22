# Independent initial position

Timestamp: 2026-10-16T05:59:29.737189+00:00

This file was written after reading the current paper in full and checking all six frozen input hashes, before reading inherited review verdicts, mathematical reports, or root repair dispositions. The task message describes prior issues; I have not accepted any prior conclusion as a premise.

## Exact claim tested

For every integer d >= 2 there exists some connected open quasi-conical union of expanding cubes with common-face positive shrinking zero-thickness windows. Both future widths and apertures are chosen. The form Dirichlet Laplacian has a complete orthonormal eigenbasis, no zero eigenvector, no absolutely continuous or singular continuous subspace, and spectrum = essential spectrum = closure of point spectrum = [0,infinity). This does not prescribe arbitrary cube widths, smooth boundaries, Neumann conditions, finite-length passages, or computable aperture bounds.

## Independent derivation from the paper

1. For a finite tower in a fixed enclosing box, all window forms embed into H_0^1(B). The nested intersection at aperture zero is the separated form space because a point has zero H^1 capacity in d >= 2. For bounded u, multiplication by a cutoff vanishing near the touching point removes the only new interface; the product belongs to the disconnected form domain even with arbitrary earlier irregular windows. The cutoff error is bounded by sup|u| times its gradient energy plus dominated-convergence terms. Complex real/imaginary truncation treats arbitrary u. In d=2 the displayed logarithmic derivative integrates to 2*pi*integral|theta'|^2/log(1/r); it tends to zero. d=1 has positive point capacity and fails.
2. Rellich in the enclosing box turns varying-input bounded resolvents into a compactness argument. A weak input limit and strong output limit solve the zero-window variational equation against every fixed old-domain test. Compactness of the old resolvent gives norm convergence, not merely pointwise strong convergence. Positivity and discreteness follow from the same box.
3. A finite old protected eigenvalue set forbids finitely many new widths in a bounded interval: m_1^2+...+m_d^2 = 4*a^2*lambda/pi^2 gives a uniform bound on the integers. Width is chosen first, isolating full clusters second, positive aperture last. Norm-resolvent continuity transports all finitely many nested spectral sums with summable errors and stable ranks. The new birth cutoff is chosen only after that geometry is fixed. Degeneracies stay whole; a split cluster is retained in full.
4. In the final direct-sum L2 of cubes, finite-stage form spaces increase densely by compact-support exhaustion. Their variational solutions are genuine form-orthogonal projections of the final resolvent solution. Thus zero-extended R_n converge strongly to R; no infinite-stage norm-resolvent convergence or genuine whole-space finite-stage resolvent is assumed.
5. Each fixed protected trajectory converges in operator norm to a same-rank finite projection. Strong R_n convergence plus norm P_n convergence passes commutation to R. Finite-dimensional reducing spaces diagonalize R. R is injective and positive, so no protected vector can land at resolvent eigenvalue zero/infinite energy; positive resolvent eigenvalues give actual A-domain eigenvectors.
6. The repeated probes are essential: the trajectory born at each large n approximates each fixed f_(j,l) with error < 2^(-n)+2^(-n-1). Therefore the closed eigenvector span contains the entire cube ON basis. This proves no singular continuous part; dense eigenvalues alone would not suffice.
7. Compactly supported scaled plane waves on disjoint cube balls give Weyl sequences at every nonnegative lambda, including zero. Gradient errors are O(r^(-2)+sqrt(lambda)/r). This proves the half-line essential spectrum. The connected infinite-volume domain has no nonzero L2 constant; zero energy therefore is not an eigenvalue. Completeness makes the half-line the closure of positive eigenvalues.

## Initial falsification attempts

- Tried the d=2 endpoint with the ordinary annular cutoff: its energy would not vanish; the paper actually uses a logarithmic cutoff and its displayed exact integral is correct.
- Tried forcing old irregular windows into a boundary-regularity assumption: the enclosing-box/truncation/multiplication argument uses none. Smooth approximants are taken in the open domain and remain valid after the new connector is cut off.
- Tried resonant multiplicities and split eigenspaces: complete old eigenvalues and disjoint full new clusters preserve nested sums and ranks. No simple spectrum is needed.
- Tried parameter circularity: S_n belongs to already fixed O_n; only the new width is excluded, then aperture, then the new cutoff. No protected future eigenvalue is prescribed in advance.
- Tried escape to unbounded energy: finite projection norm convergence does not alone prevent it, but strong final-resolvent commutation and injectivity do.
- Tried a one-time dense-probe argument: the construction instead revisits each probe at every large birth stage, so residual error tends to zero.
- Tried the false stronger conclusion that every real spectral point is an eigenvalue: the paper states closure and explicitly excludes zero as eigenvalue.

Initial assessment: no mathematical counterexample or logical gap found in the current six-page argument. This is a human-readable mathematical review, not formal proof certification. Primary-source scope, original question matching, historical-credit limits, the exact package, and the PDF remain to be independently tested. Review completion estimate: 15%.
