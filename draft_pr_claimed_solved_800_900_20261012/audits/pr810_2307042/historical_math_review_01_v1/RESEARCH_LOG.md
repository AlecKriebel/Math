# Independent adversarial review of PR810 / problem2307042

## 2026-10-13T03:12:19Z — Review initialized (5% complete)

Source under review: frozen `source/author/PROOF.md`. Existing reviewer conclusions have not been read. Work restricted to this audit folder; no git mutation or outside communication.

Exact mathematical claim: in the smooth bounded annulus 1 < |z| < e, at a = sqrt(e), the minimal normalized Martin kernel belonging to inner boundary point -1 is strictly below the upper Harnack envelope at every sufficiently close point other than a. This would forbid any initial equality curve or Green line for that kernel.

Hypotheses to check: (i) the periodized strip Poisson formula is positive harmonic; (ii) its normalization is a minimal Martin boundary kernel, for unrestricted approaches to the boundary point; (iii) its gradient at a has magnitude less than 1/10; (iv) four globally positive harmonic competitors have a uniform first-order advantage in every direction; (v) the actual source problem asks for equality along a Green line and the consequence meets that quantifier.

Approach families: independent conformal/PDE derivation of Poisson/Green functions; direct singularity/reflection proof of minimality; exact convex-geometric comparison; high-precision stress checks. Numerical evidence will supplement rather than substitute for proofs.

Success criteria: every formula and inequality independently derived, no unproved central claim or inconsistent boundary condition, checkable exact proof plus reproducible numerical script, and precise scope of source consequence. Priority/novelty audit belongs to the parent workflow and is not a conclusion of this review.

Initial gap: all substantive claims remain to be independently checked.

## 2026-10-13T03:20:21Z — Independent derivations and stress checks complete (90% complete)

Poisson/Green formulas were rederived from the upper half-plane and independently matched to separated Fourier solutions. The Martin limit was checked with a uniform s-factor expansion valid for arbitrary approach. Minimality was independently established by reflected harmonic Fourier modes, exclusion of all high-order singular modes, symmetry elimination of logarithm/tangential dipole, and zero-boundary maximum principle after cancellation. The four globally positive competitors and rational gradient bound give a uniform directional advantage.

The standard-library-only script reproduce_checks.py passed. Its 100-digit decimal computations compare image/Fourier Poisson and Green representations with analytic truncation estimates, cross-check the gradient, test normal/slanted/extremely tangential Martin approaches (normal distances down to 1e-120), and stress the uniform O(x) singularity remainder. A separate floating mesh includes 4096 uniform directions plus all four switching directions at nine radii from 0.05 to 1e-8. Every sampled gap was positive; this remains diagnostic rather than a proof of a specific radius.

Strongest verified result: the complete stated punctured-neighborhood theorem, including minimal Martin-kernel identification, with no mathematical repair required. Exact remaining review gap: final consistency check of the audit artifacts and explicit assessment of claim scope; no substantive proof gap currently identified. Priority and current openness are outside this mathematical audit.

## 2026-10-13T03:22:05Z — Final checkpoint (100% complete for this mathematical audit)

Final consistency check completed. Verdict PASS; no mathematical errors, unsupported central claims, or required repairs found. An exact switching-angle derivation independently verifies the global first-order minimum used only as a diagnostic. The reflected Fourier argument was made explicit enough to exclude essential singularities and ensure convergence of its regular part. Source proof SHA-256: `88ceb90850cd364d3ef53a17d1c60beebff3a19b650c1af14b06c07c208e41fc`.

Final artifacts: INDEPENDENT_DERIVATION.md (checkable analytic derivation and adversarial tests), reproduce_checks.py (standard-library reproducibility), CHECK_RESULTS.json (100-digit and mesh outputs), REVIEW_REPORT.json (verdict and per-family mechanism/evidence/gaps), and this log. Numerical limitations and publication-scope limitations are explicit. No proof repair is necessary. Historical priority and preprint suitability beyond the mathematical claims remain for the parent workflow.
