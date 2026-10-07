# Research log: exact TSP semidefinite complexity

## 2026-10-06 22:10 America/Los_Angeles — initial checkpoint

Persistent goal established. Source clone pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a; copied family 126 under this effort and recorded SHA-256 hashes. Shared checkout is on main with concurrent changes; preserve its index and files. No dedicated target folder existed before this initialization.

Target: prove exact real PSD lift matrix dimension 2^{Omega(N)} for all sufficiently large N, with separately checked 2^{O(N)} upper bound if stated. Publication requires proof validity, priority audit, two complete-package independent reviews, actual production Zenodo publication, and verified tracker entry. Upstream Lean scope explicitly covers only superpolynomial growth, not the needed exponential statement.

Mathematical resolution estimate: 5%. Publication package estimate: 1%. These estimates are not evidence.

## 2026-10-06T22:12:16-07:00 — independent structural progress

Read central source arguments directly: local trace contraction, invariant eigenspace multiplicity, orthogonal splitting, tagged-stack Fourier Gram potential, parity functional and matching realization. Algebraic identities presently check; independent audits continue. Derived exact subset-state flow formulation with m=2(N-1)+(N-1)(N-2)2^(N-3) scalar nonnegativities and diagonal PSD embedding. Literature audit found CCC 2016 corrected prior TSP bound, requiring precise tilde-Omega notation. Original Yannakakis reduction has 3n cities; independent 2n contraction variant under investigation. Source remote main still equals pinned adc7f1 at check.

Mathematical resolution estimate: 40%. Publication package estimate: 5%.
