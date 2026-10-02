# 30005936 / OWR-14298374-005: space-time-white-noise splitting

## Exact distinct source

David Cohen's complete contribution in [OWR26/2024](https://ems.press/content/serial-article-files/49484), printed1495–1498, contains two noise settings. The assigned target is the **second**, on printed1497/PDF53: the Itô stochastic heat equation on [0,1] with homogeneous Dirichlet boundary, deterministic nonnegative initial data, and multiplicative space-time white noise. The source explicitly mentions the experimental superlinear example g(v)=v^1.25, asks for positivity/convergence with g less regular than in reference[2], and separately asks for a weak convergence rate without specifying a test class.

For h=1/N and time step τ=T/M, the finite-difference system has drift N²D_N and independent standard Brownian motions W_n^N, multiplied by sqrt(N). The intended displayed vector scheme is

 U_{m+1}=exp(τN²D_N) [ U_{m,n} exp(sqrt(N) f(U_{m,n}) ΔW_{m,n}
                                      −N f(U_{m,n})² τ/2) ]_n,

where f(v)=g(v)/v for v≠0. The old-value factor is present in this vector formula. An extension at zero must be specified when a derivative at zero is absent; multiplying a zero state by its stochastic exponential makes that convention immaterial as long as it is finite. The full source page and the vector formula were visually checked.

[PR317](https://github.com/AlecKriebel/Math/pull/317), target30005935, concerns the first setting, with one common time-only Brownian driver and no spatial mesh. Its frozen source and final result explicitly exclude the second setting. Its scalar/SDE tail mechanism and weak-test distinctions are relevant prior work, but are not automatically a theorem about this independent-grid-noise scheme or the continuum white-noise equation. This new attempt will not count merely reindexing that old calculation as a substantive author turn.

## Important continuum-versus-semidiscrete discrepancy

The OWR summary displays a τ^(1/4) mean-square bound against the continuum u(t_m,x_n) under only τ<=γh². The cited detailed primary paper distinguishes two statements:

- Theorem6, equation(18), printed1325: the τ^(1/4) estimate compares the time scheme to the **spatially semidiscrete** solution u_n^N(t_m), uniformly under τ<=γh².
- Corollary7, equation(19), printed1326: the full error against the continuum solution is bounded by C h^(1/2) under that condition.

Both detailed pages were visually checked. Under balanced refinement τ comparable to h² the orders agree, but the one-sided condition alone does not turn the spatial error into a τ-only bound. The OWR display and the detailed intended estimates will be recorded separately. A discrepancy in a summary formula is not being advertised as a solution of the rough-coefficient problem.

## Detailed primary result and assumptions

Bréhier–Cohen–Ulander, *Analysis of a positivity-preserving splitting scheme for some semilinear stochastic heat equations*, ESAIM:M2AN58(2024),1317–1346, DOI10.1051/m2an/2024032. [Published PDF, official institutional copy](https://research.chalmers.se/publication/542281/file/542281_Fulltext.pdf); [earlier arXiv2302.08858v1](https://arxiv.org/abs/2302.08858). The institutional PDF is the published paper; the arXiv copy is only v1. The direct journal PDF returned403.

Sections1–4, the scheme and theorem statements were read. The assumptions are u0∈C³ with zero endpoints; u0>=0 for positivity; and g∈C¹ globally Lipschitz with g(0)=0. The paper states that the moment/error constants depend on g through its Lipschitz constant. Its f is bounded by that constant. Theorem6 also gives an error bound C sqrt(τ/h) against the semidiscrete solution under τ<=γh. The superlinear experiment lies outside its assumptions. Positivity and mean-square/weak convergence must be distinguished, as must temporal and joint spatial-temporal errors.

## Current literature comparison

Ulander's [arXiv2412.10800v3](https://arxiv.org/abs/2412.10800v3), revision28October2025, proves weak quarter-order bounds for a **different LTE scheme** using exact nonlinear-SDE simulation and exact heat integration, on a bounded invariant state interval. Its assumptions impose C² drift and C³ diffusion locally on that interval, with endpoint conditions for a Lamperti transform. Its introduction, assumptions, algorithm and Theorem9 were read. This does not verify the source's frozen-coefficient geometric-Brownian LT scheme for an unbounded superlinear state space. No claim is based on treating all “splitting” methods as identical.

A bounded current search found no primary result covering the full requested extension of this exact scheme. This is not exhaustive literature coverage or novelty certification. Weak rates require an explicit test class; strong estimates can give Lipschitz-test bounds, but do not establish a higher weak order for smooth tests or a result for arbitrary unbounded observables.

## Prior-attempt gate and budget

ID/alias/reference PR and commit searches, both target paths,378 live branches and438 mirrored refs found no exact attempt. A semantic space-time/heat PR search found only PR317; the substantive scope difference is documented above. Direct UnsolvedMath retrieval failed, so the pinned import at revision37e53eabe540fb458758e198be61634bd02ee008 was checked against the full primary contribution. Raw imports and source PDFs are separate reading inputs.

Eligible for a distinct five-turn attempt. **Author count0/5.** Full resolution must address the original exact white-noise scheme and its stated rough/superlinear scope, with correct error targets and an explicit weak-test class. A globally Lipschitz nonsmooth extension, a fixed-dimensional SDE result, or a theorem about another integrator would be scoped partial work.
