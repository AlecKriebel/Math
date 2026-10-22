# Source scope and qualification

## Original target

Rank 990, problem 30002760 / OWR-13487-001. The primary source is Dahlke, Kutyniok, Stevenson and Süli, *New Discretization Methods for the Numerical Approximation of PDEs*, Oberwolfach Reports 12 (2015), 87-185, DOI [10.4171/OWR/2015/2](https://doi.org/10.4171/OWR/2015/2). The organizers' introduction on printed page 88 asks about adaptive finite-element rates compared with best partitions in a refinement class such as newest-vertex bisection, for elliptic or parabolic transport-dominated diffusion. The adjoining discussion distinguishes that benchmark from better anisotropic approximation as the Péclet number increases.

The introduction does not fix the PDE coefficients, boundary data, norm, time discretization, marking algorithm, degree, oscillation convention, or uniformity of constants. It is a research question, not a uniquely quantified universal theorem. A parameter-uniform preasymptotic claim is a stronger interpretation, not a condition explicitly supplied by the extracted wording. This packet retains that distinction and does not declare a negative answer from a poorly chosen algorithm.

Publisher [PDF](https://ems.press/content/serial-article-files/46549): the relevant page was extracted, rendered and visually inspected. The dated corpus's blanket open classification is not a current literature theorem. Its other cited TIB page is a repository record for the same 2015 report, not an independent 2026 progress survey.

## Positive stationary result already in the literature

Christoph Erath and Dirk Praetorius, *Optimal adaptivity for the SUPG finite element method*, Computer Methods in Applied Mechanics and Engineering 353 (2019), 308-327, [DOI](https://doi.org/10.1016/j.cma.2019.05.028), [public manuscript](https://arxiv.org/pdf/1806.11000).

For their stationary scalar convection-diffusion model, Theorems 4.4-4.5 prove eventual linear estimator convergence and optimal algebraic rates over the specified NVB family. Remark 4.6 compares its class with best energy error plus data oscillation. Assumptions include a polygonal Lipschitz domain, positive diffusion, bounded regular coefficients satisfying coercivity conditions, compatible mixed boundary conditions, conforming fixed-degree elements and admissible stabilization. Algorithm 4.1 uses near-minimal Dörfler marking plus a largest-element refinement. Section 4.2 explicitly says the convergence proof is not robust with respect to the local Péclet number. Its unknown onset and constants must remain in the claim. This is a substantial affirmative answer for a specified stationary interpretation, not a full parabolic or uniform-preasymptotic result.

The retrieved PDF displays July 28, 2021 internally; the arXiv landing page lists a 2018 submission and the 2019 journal citation. Its actual bytes are hashed; no unverified identity with the publisher's typeset version is claimed. Pages 2-5 and 12-16 were inspected as text; page 14 was rendered and visually inspected.

## Relevant parabolic developments

- Rob Stevenson and Jan Westerdiep, *Minimal residual space-time discretizations of parabolic equations: Asymmetric spatial operators*, [arXiv:2106.01090v2](https://arxiv.org/abs/2106.01090). The inspected introduction distinguishes ordinary discrete inf-sup stability from a stronger condition producing spatial-operator-independent energy estimates. It proves same-trial-space quasi-optimality under conditions, not by that fact alone a best-mesh adaptive rate. The present packet imports no uninspected theorem from its body. PDF introduction, pages 1-2, inspected.
- Michael Feischl, Fernando Henríquez and David Niederkofler, *Optimal Time-Adaptivity for Parabolic Problems*, [arXiv:2512.05676v2](https://arxiv.org/abs/2512.05676), revised May 29, 2026. Section 2 assumes a finite-dimensional Gelfand triple and an elliptic self-adjoint spatial operator. Its rate-optimality concerns the number of time steps. It must not be described as a theorem for arbitrary spatial convection operators or joint NVB space-time complexity. Inspected pages 1-4; preprint status, no journal acceptance verified.
- Gregor Gantner, Robin Smeets and Rob Stevenson, *A Double-Adaptivity Solver for Parabolic PDEs*, [arXiv:2609.01748v1](https://arxiv.org/abs/2609.01748), September 2026. The introduction explains why general nonslab partitions need additional stability care. It reports a certified residual-lift estimator whose auxiliary refinement has no cardinality bound by a fixed multiple of the original mesh, and an unguaranteed simpler surrogate. These are material qualifications to any claimed general rate/linear-cost resolution. Inspected pages 1-5; preprint status, no journal acceptance verified.

These targeted checks do not establish an exhaustive world-literature open-status theorem. The disposition is that this attempt has not resolved the full broad target.

## Established methods credited

The self-contained proofs use classical coercivity/Céa, Hilbert-space Riesz representation and orthogonal projection, Fortin stability, mesh overlays, Dörfler marking, energy estimates, Hölder's inequality and backward Euler. No historical novelty is claimed.

The methodological precedents include Albert Cohen, Wolfgang Dahmen and Gerrit Welper, *Adaptivity and variational stabilization for convection-diffusion equations*, ESAIM M2AN 46 (2012), 1247-1273, [DOI and primary publication page](https://www.numdam.org/articles/10.1051/m2an/2012003/); and Carsten Carstensen, Michael Feischl, Marcus Page and Dirk Praetorius, *Axioms of adaptivity*, Computers & Mathematics with Applications 67 (2014), 1195-1253, [public manuscript](https://arxiv.org/abs/1312.1171). Publication metadata/abstracts were checked for attribution; their full proofs are not imported as unverified lemmas. Approach 4 supplies its own complete proof under explicit hypotheses.
