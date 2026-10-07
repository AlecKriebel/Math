# Research log: 30005600

## 2026-10-07 17:02 UTC: readiness gate

The full corpus record and absent exact-code research report were checked. Corpus sizes and SHA-256 hashes match the pinned 37e53eabe540fb458758e198be61634bd02ee008 revision. The actual OWR 36/2023 PDF, printed pp. 2033--2036, was read and p. 2036 visually checked. The published Karpukhin--Métras--Polterovich article and author-hosted preprint were checked. A current 2026 Martynyuk preprint extends higher-eigenvalue existence/sphere results and does not establish this torus threshold. No complete resolution was found in the bounded current search.

Exact target: with trivial spin structure on R²/(Z(1,0)+Z(a,b)), b>0, |a|≤1/2, a²+b²≥1, determine the infimum of the first strictly positive Dirac eigenvalue times square-root area over all smooth positive conformal factors. Zeros are omitted. Both conjectured expressions agree at b=π. No Laplacian, nontrivial spin, or first nonnegative eigenvalue substitution is allowed.

The current repository queue still says queued, 0/5. Exact ID/code, topic PR, root directory, attempts directory, related-record and related-group checks revealed no inherited substantive matching attempt. The exact directory read, semantic PR titles and error limitations are preserved separately. Failed code search/recursive tree transport was not represented as successful coverage. No publication or queue modification is part of this work.

Completion toward full conjecture: approximately 5%, a planning estimate only. The credited b>2π theorem leaves most of the asserted sharp threshold unsettled.

## Substantive approach plan

1. Sharpen the harmonic-map energy argument, including the equality endpoint and the precise spin-sensitive missing gap.
2. Derive the weighted chiral Rayleigh principle with the kernel constraint retained, and attempt a sharp conformal inequality.
3. Solve a one-dimensional conformal-factor family exactly, with explicit control of all other Fourier sectors.
4. Test spin-trivializing covering constructions from low-energy nontrivial-spin harmonic maps.
5. Search genuine two-variable smooth conformal factors by a kernel-corrected Rayleigh--Ritz method, recording only numerical evidence and certified algebraic checks as such.

Each of these is mathematical proof or counterexample work. Readiness, source retrieval and package verification are not counted as approaches.

## 2026-10-07 17:05 UTC: approaches 1--3

1. Harmonic energy/spin parity: reconstructed the exact even-dual-lattice restriction on equatorial maps; the published 4π energy gap yields the credited lower bound min(2π/√b,√(2π)), including the value at b=2π. The missing assertion is a spin-sensitive energy bound in the interval [4π,8π), not a positivity or existence theorem. Full-goal completion estimate: 10%.
2. Weighted chiral inequality: derived the complete Rayleigh principle with weighted kernel constraint, its exact constant-mode elimination, a general L∞-dependent lower bound, and the sharp still-unproved weighted inequality needed to finish. Concentrating factors defeat the elementary Poincaré estimate. Full-goal completion estimate: 10%.
3. One-variable factors: proved the exact full-spectrum result μ₁=2π/∫f under max f≤∫f by controlling nonzero Fourier sectors with quasiperiodic boundaries. This excludes nonconstant counterexamples in an infinite, explicitly defined family; it does not cover arbitrary factors. Full-goal completion estimate: 12%.

## 2026-10-07 17:07 UTC: approaches 4--5 and disposition

4. Spin-trivializing covers: proved that non-equatorial harmonic maps pulled back through a cover killing a nontrivial spin character have total energy at least 8π. Their associated eigenpairs cannot supply a sub-spherical energy witness. Lower eigenmodes of the pullback metric remain uncontrolled, so this does not exclude a metric counterexample obtained from a literal cover. Intrinsic trivial-spin maps and cover deformations also remain unclassified.
5. Two-variable Rayleigh--Ritz search: 287 initial factor evaluations and 14 bounded optimizations across seven classes found no strict numerical improvement below the conjectured target. The square/equilateral metrics do improve below their flat values, but remain above the target in the tested basis. Six flat controls and three exact one-variable controls passed. Best factors were tested at larger Fourier cutoffs. Floating-point quadrature is explicitly not certified. The inability to find the known sub-flat bubbling behavior at b=2 is recorded as a search limitation, not evidence for a false flat minimization theorem.

Full-goal completion estimate: 12%, heuristic and not a probability or measurement. Final disposition: unresolved after 5/5 mathematical approaches, with credited known regime and scoped partials. No sixth search route, queue edit, publication, release, or outreach is part of this packet. Self-checks and integrity checks may still be completed; independent review remains pending.

## 2026-10-07 17:11 UTC: author self-check

The portable exact checker passed in normal and optimized Python with identical output: 5,600 finite dual-lattice controls, 729 weighted-variance cases, 34 admissible cosine parameters, all three nontrivial spin-cover characters, and three deliberately rejected shortcuts. The actual numerical run used 1,666 optimizer objective calls, additional to the 287 initial factors, controls and refinements. These tests do not certify infinite-dimensional analysis. The nearest Dirac-topic draft PR was checked and concerns a distinct massive Dirac potential/Schur-form problem, not torus conformal minimization.

No full-goal completion change: 12% heuristic. Final author freeze is being prepared for independent review, with copied source material excluded.
