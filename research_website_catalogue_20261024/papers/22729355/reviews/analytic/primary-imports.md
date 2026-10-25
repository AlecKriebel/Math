# Primary import audit — 22729355 analytic review

This audit checks the functional-analytic imports actually needed by the proof. It does not use citation counts, publication venue, or earlier reviewer approval as correctness evidence. Broader historical comparisons in the introduction are not a novelty certification.

## Crandall–Rabinowitz, 1971

Primary article: *Bifurcation from Simple Eigenvalues*, Journal of Functional Analysis 8, 321–340. Actual article PDF acquired from the William & Mary faculty-hosted copy:
https://jxshix.people.wm.edu/2013-taiwan/crandall-rabinowitz-1971-JFA.pdf

SHA256: `c0a9c1d6de3e47fa14263a1be88833991d9a30ee4c62cf56529479b85a1cd532`.

Read Theorem1.7, printed p325, and its surrounding setup/proof. It assumes a trivial solution branch, continuous required derivatives, one-dimensional kernel and quotient by the range, and the mixed derivative of the kernel vector outside the range.

Application audit: F(mu,u)=f(1+u)+(1-mu)D u'' maps the fixed-mass H_N^2 space to fixed-mass L^2 and is smooth. Its zero branch is present. Fourier inverse estimates give the closed Fredholm range and one-dimensional null/cokernel. Pairing F_mu,u with the nullvector gives (pi/2)ell^TDr !=0. Hence the theorem applies. Analyticity/smoothness sufficient for the displayed finite Taylor order follows from the polynomial stationary map and the local implicit-function construction; the existence claim is not based solely on finite-dimensional matrix tests.

## Henry, 1981

Primary book: *Geometric Theory of Semilinear Parabolic Equations*, Lecture Notes in Mathematics840. Publisher Chapter5 DOI10.1007/BFb0089653 and Chapter6 DOI10.1007/BFb0089654. The publisher publicly supplies two-page previews, downloaded and read:

- https://page-one.springer.com/pdf/preview/10.1007/BFb0089653 — printed pp98–99, complete Theorem5.1.1 statement and its stability estimate; SHA256 `5e0b6f2a49bd3fc15c7e60986854a13c048cc7c48af68cc4dfa77762470aa6f6`.
- https://page-one.springer.com/pdf/preview/10.1007/BFb0089654 — printed pp143–144, Definition6.1.1 and complete Theorem6.1.2 invariant-graph statement; SHA256 `66cbf987a58aa5d735ce7e9c6274df6fee45c1b8fcdb6b125273a135e5353e3b`.

Theorem5.1.1 uses a sectorial operator on a Banach space and a nonlinearity on a fractional domain with exponent below one. The linearized operator must have spectrum uniformly in its stable half-plane, with a remainder small relative to that fractional norm. It yields a quantitative exponential estimate. Theorem6.1.2 constructs an invariant graph over a complementary slow space under a spectral gap and sufficiently small Lipschitz coupling.

Application audit: choose fixed-mass L^2 as base and H^1 as exponent1/2 phase space. A scalar shift makes the Neumann diffusion sectorial operator positive if necessary. The reaction derivative is bounded multiplication; the quadratic remainder is O(||u||_H1^2) in L^2 by the one-dimensional Sobolev embedding. At a patterned equilibrium, all spectrum on this restricted space has strictly negative real part. Thus the sign conventions match by writing evolution as u_t+A u=f(u). The theorem yields the claimed local exponential H^1 stability. The critical/stable splitting at onset has a one-dimensional zero mode and positive complementary gap. A small smooth cutoff makes the nonlinear coupling as small as required; reflection-invariant cutoffs and uniqueness of the graph construction preserve reflection. For a parameter-dependent reduction, rescale time by 1-mu to fix the leading diffusion operator and adjoin mu'=0. Finite differentiability can be checked in that construction: choose a small center weight epsilon so 5 epsilon is below the stable spectral gap, and cut off in a reflection-invariant H^1 ball. Derivatives through order five of the graph integral have kernels bounded by a constant times t^(-1/2) exp[-(gap-j epsilon)t], j<=5, which are integrable. The polynomial nonlinearity and smooth cutoff have bounded derivatives on that ball. Differentiating the contraction equation therefore supplies the finite smoothness required for the stated Taylor remainder. The unique cutoff graph is reflection-equivariant. This is an application check, not a claim to have read the later smoothness theorem in the unavailable book.

Access limitation: repeated attempts to retrieve the complete book from https://repositorio.usp.br/directbitstream/c1620e41-3714-424c-aef9-82a428dfa27a/3153193.pdf timed out. Later Chapter6 smoothness statements were not inspected directly in that book. The complete stability theorem and invariant-graph existence theorem *were* inspected in primary publisher text. I do not characterize this as a complete book audit. The application's smoothness and spectral hypotheses were checked independently, rather than assumed from the citation.

## Kato

Primary book text: *Perturbation Theory for Linear Operators*, reprint of the 1980 edition, obtained from the University of Edinburgh faculty-hosted scan:
https://webhomes.maths.ed.ac.uk/~v1ranick/papers/kato1.pdf

SHA256: `ec4a79bbbcd6e94097c04a5cd2e324c00ca776349c3b9559e779e79cfbc8bdf3`.

Read ChapterIV Theorem3.16, printed pp212–213, the following finite-eigenvalue continuity discussion, ChapterVII Theorem1.7, printed pp368–369, and type-(A) definitions/argument at pp375–376. These cover continuity of separated spectral subspaces under small closed-operator perturbations and holomorphic dependence for analytic fixed-domain families.

Application audit: all operators have the same H_N^2 domain inside fixed-mass L^2. Positive diagonal diffusion coefficients retain a lower bound and the reaction derivative changes by bounded multiplication. Resolvent continuity follows from small perturbations in the graph norm, and spectral projections on fixed compact contours have unchanged rank. The local branch can be parameterized analytically by amplitude through the stationary implicit-function construction. For high frequencies, coercivity and bounded reactions exclude spectrum entering a fixed right half-plane from infinity. Consequently the finitely many relevant spectral clusters remain separated. This is not an application of a finite-matrix continuity theorem to an uncontrolled infinite spectrum.

Edition precision: the paper cites a 1995 second-edition reprint. The retrieved scan explicitly says reprint of the 1980 edition. The checked chapter/theorem content matches the cited standard framework; no claim is made that the scan's bytes are the cited printing.

## Additional independent control: Crandall–Rabinowitz, 1973

Primary article: *Bifurcation, Perturbation of Simple Eigenvalues, and Linearized Stability*, actual article at:
https://jxshix.people.wm.edu/2013-taiwan/crandall-rabinowitz-1973-arch.pdf

SHA256: `d3871c46123c768a7cb677f2b91813e9d7413f5000b7aa086e87d6ff2fb58f68`.

Read Definition1.2, Lemma1.3, Corollary1.13 context, and Theorem1.16, pp162–167. For the inclusion of the domain in the base space, its simple-eigenvalue relation agrees with the sign of the branch eigenvalue obtained from -A mu'(A) eta. Since mu(A)=-(c/eta)A^2+O(A^4), this is 2cA^2+O(A^4), equivalently -2eta mu+O(mu^2). This source explicitly addresses linearized stability; it is not being used in place of Henry for nonlinear exponential stability.

## Imports not substituted for proof

The matrix localization, omission-minor formula, diffusion-ray criterion, explicit profiles, 35/77/84/22-term polynomials, all-m cubic identities, and contrast optimization are reconstructed inside the manuscript and its immutable support. They are not imported from the comparison papers. Kielhöfer is presented as complementary background and was not required as an additional load-bearing theorem. Classical Routh–Hurwitz algebra, finite-dimensional Schur complements, exact polynomial arithmetic, and elementary Fourier/Sobolev facts were checked in their stated roles. The numerical simulations are illustrative and do not replace any theorem import.
