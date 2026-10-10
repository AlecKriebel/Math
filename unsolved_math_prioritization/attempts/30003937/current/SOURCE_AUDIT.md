# Source and scope audit

Inspection date: 2026-10-08. PDF hashes and byte counts in `SOURCE_MANIFEST.json` bind the exact inspected local PDF bytes. The packet distributes none of those bodies. An associated public URL identifies each document, without claiming that every DOI landing page is byte-identical to the inspected preprint.

## Primary target and imported theorems

- OWR39/2018, Mario Putti's contribution, printed pp. 2398–2400: the beta=1 elliptic/reaction system and conjectured long-time density/potential behavior. The potential topology is not specified. The source has no assertion that its whole-domain potential is unique.
- Facca–Cardin–Putti, arXiv:1610.06325v1 (20 October 2016), associated with the 2018 SIAM publication: equations (2), Conjecture 1, the normalized weak formulation (7), Proposition 1, and Theorem 1 provide the local positive-Hölder framework and finite-time positivity estimate. Theorems cited by number here refer to this inspected preprint version. A complete version-by-version proof comparison with the journal article is not claimed.
- Facca–Daneri–Cardin–Putti, arXiv:1709.06765v2 (28 August 2018), associated with the 2020 JSC publication: the modified energy, its dissipation, and transport-density minimization are prior results. The work is not a general global continuum convergence theorem.
- Bonifaci, arXiv:1611.06729v1 (21 November 2016), associated with the 2020 Algorithmica article: relative-entropy arguments for finite-dimensional Physarum/linear-programming dynamics are prior methodology. Their use does not supply continuum well-posedness.

## Proof-level qualification of the reported local theory

An independent audit inspected the final Q-estimate in section 4.1, printed p. 16 of the pinned arXiv:1610.06325v1 PDF, including the rendered page. It uses a generic Hölder modulus-composition Lipschitz step which fails for z₁(x)=x and z₂(x)=x+ε. The counterexample and the narrower valid L2 estimate are detailed in `continuation.md`. This identifies an unsupported proof step; it does not disprove the specialized fixed-forcing elliptic-map theorem or assert that the journal version has the same issue. The continuation implication is now explicitly conditional on a valid local restart result. Conditional entropy and the directly constructed interval/radial solutions do not need that unverified C^δ-Lipschitz step.

## Nearby results that do not automatically resolve the target

- Facca–Piazzon, Transport Energy, arXiv:1909.04417v2 (12 May 2020): the inspected variational characterization concerns measures; the dynamic construction uses its own measure-space metric, and a separate regularized L2 gradient flow. Those laws are not the original μ_t=μ(|∇u|−1). The later journal record is Facca–Piazzon–Putti, L¹ Transport Energy, Applied Mathematics & Optimization 86 (2022), article 21, DOI 10.1007/s00245-022-09880-1. The author/title difference between preprint and publication is retained. The published abstract and metadata were inspected; this does not claim a complete line-by-line audit of the journal full text.
- Piazzon–Facca–Putti, Computing the L1 optimal transport density: a FEM approach, arXiv:2304.14047v1 (27 April 2023): introduction and defining approximation equations describe a functional discretization and a gradient-flow minimization scheme. Convergence of those approximations is not a theorem for every trajectory of the original continuum equation. The arXiv version list inspected on 2026-10-08 lists v1.
- Facca–Cardin–Putti, Branching structures emerging from a continuous optimal transport model, arXiv:1811.12691v2 (8 May 2020): the beta-family and its recap of beta=1 must be separated from the original target. The correct branching preprint is 1811.12691; 1812.11782 is the basis-pursuit paper below.
- Facca–Cardin–Putti, Physarum Dynamics and Optimal Transport for Basis Pursuit, arXiv:1812.11782v2 (26 September 2020): finite-dimensional matrices, rather than the unrestricted continuum PDE, are the setting of the claimed dynamical results.
- Lorenz–Mahler–Meyer, Lα-Regularization of the Beckmann Problem, SPP1962-187: the inspected cover and first article page date it to January 2022. Search-index freshness is not a publication date. Its regularized static Beckmann analysis does not prove the original DMK conjecture.

## Coverage limits

This was a bounded source/literature inspection, including the documents above, primary arXiv metadata, and relevant author publication information. No verified full later resolution of the exact system was located. That negative result is not an assertion of worldwide openness, priority, or completeness. Later results about different gradient flows, finite-dimensional dynamics, branching exponents, or numerical schemes are not silently substituted.

The measure-minimizer hypothesis in the conditional entropy note is deliberately explicit: uniqueness in an L1 class alone would not justify uniqueness among all measures on the compact closure, including possible boundary measures. Gauge normalization does not imply whole-potential uniqueness. Neither missing uniqueness nor an unspecified topology is used to manufacture a resolution.

PDFs were available for local inspection on 2026-10-08. Reinspection and fresh public metadata checks were completed the same day. The manifest records byte identity and observed versions, not an independently reconstructed network-transfer history. One fresh attempt to open the transport-energy DOI through the web reader returned an internal error; the already materialized official metadata and the accessible arXiv preprint were used instead. No access restriction was bypassed.
