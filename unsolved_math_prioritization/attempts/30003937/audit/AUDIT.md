# Publication context for the preserved audit

The report below records the prior mathematical audit, including its historical checks of an original packet and a contextual patch round trip. The original report, original five mathematical notes, original archive, old manifests, and old run receipts are not delivered here. Its references to those files and supplied outputs describe that earlier audit, not this publication inventory. The current publication delivers only the 13 corrected files under `current/`, authored audit/correction material, and fresh verification evidence.

Fresh default reproduction of the complete original packet and original-to-corrected patch round trip is NOT_RUN: the required original packet is excluded from this distribution. Source-PDF and corpus rehash are also NOT_RUN in the source-free default. Historical hashes and inspection statements are provenance metadata, not claims of fresh retrieval or complete delivery. See `../ACCEPTANCE.md`, `../SCOPE.json`, and the fresh receipts for current scope.

The corrected files preserve their original reviewed bytes. References in them to a preserved original packet are provenance statements, not distribution promises.

---

# Independent audit: continuum Dynamic Monge–Kantorovich partial results

Problem 30003937; original source OWR-16414-001. Inspection date: 2026-10-08.

## Disposition

Accept the mathematical partial results with the explicit source-proof qualification supplied in `CORRECTIONS.patch` and the accompanying corrected derivative. Do not promote this packet to a solution of the general original conjecture. The disposition remains unresolved/exhausted after five approaches. This audit adds no sixth proof-search approach and makes no novelty claim.

The original source-free archive is 28,047 bytes with SHA-256 `c88c89e69795002ca9c12cc6c8212587d9853c9a1fc58431cd21fbfe37119b3f`. Its complete contents match the 13 files of the preserved frozen packet. Every original byte and pin is unchanged. The corrected derivative is separately identified and re-pinned; the contextual patch explicitly records every change.

One substantive qualification is required: the inspected local-theory preprint uses a false generic Hölder modulus-composition Lipschitz step. A valid local restart theorem therefore remains an explicit premise of the continuation implication. This is not a disproof of the specialized elliptic-map theorem, its associated journal version, or the original conjecture.

## 1. Target, hypotheses, gauge, and topology

The OWR contribution at printed pp. 2398–2400 concerns the beta=1 system with strictly positive initial conductivity and zero normal flux. Its initial broad formulation uses equal-mass L1 sources, while its discussion of local theory invokes bounded forcing and Hölder conductivity. The packet works in the smoother positive local framework; it does not prove the larger source class.

The sign convention is internally consistent: q=μ∇u and −div q=f, so weak feasibility is ∫q·∇φ=∫fφ. The paper's choice of physical-flux notation need not be copied when this convention is declared.

Mean zero fixes additive constants at every finite time on a connected domain. It does not make all limiting MK potentials unique when density vanishes. The source does not specify a convergence topology. The packet correctly avoids treating either omission as a counterexample.

All uses of positivity in regular trajectories mean positivity on the compact closure, hence a positive minimum at each finite time. This differs essentially from the degenerate example's density, which vanishes on open sets. There is no positive-initial-density counterexample in the packet.

## 2. Conditional entropy and its consequences

The derivation is valid under the stated regularity, feasibility, and finite initial entropy assumptions. On compact time intervals the positive lower bound and elliptic regularity justify the differentiations. Alternatively, the explicit energy identity and entropy-chain-rule assumptions suffice; no local existence theorem is needed for that implication.

Independently, differentiating ∫μ|∇u|² while holding f fixed yields A′=−∫μ_t|∇u|². With g=|∇u| this gives

    S′=−(1/2)∫μ(g+1)(g−1)².

The feasible comparator has A=∫q_*·∇u≤∫μ_*g. Consequently

    H′≤C−S−R,   R=(1/2)∫μ(g−1)².

Feasibility gives C≤P, scalar arithmetic gives P≤S, and relative-entropy nonnegativity gives H≥0. Integration and monotonicity establish 0≤S(t)−C≤H0/t for 0<t<T. The endpoint t=0 is excluded and T=∞ is never inferred.

If the trajectory is global, integrability of the nonincreasing gap implies t(S−C)→0. The mass estimate follows from P²≤MA and P≥C; the density/flux estimate is weighted Cauchy–Schwarz. C=0 is allowed and causes no division-by-C problem. Divisions by M are legitimate because μ remains positive on a domain of positive volume at finite times.

The Kantorovich-potential decomposition is exact and nonnegative provided that the comparator is an admissible weak test function, |∇u_*|≤1, and ∫fu_*=C. It gives a μ(t)-weighted gradient estimate. Dropping that weight would require extra coercivity that is unavailable as t→∞.

The weak-measure convergence corollary is valid as a conditional compactness argument on nonnegative finite measures on the compact closure. The derivative makes nonnegativity explicit. The separate unique-minimizer premise must cover precisely this measure space, including boundary measures, and equality with S at the positive densities. Uniqueness only in L1 is insufficient. The original text already states this limitation. No strong L1 or unweighted potential convergence follows from this corollary.

## 3. Continuation: required source-proof qualification

### Exact finding

The pinned arXiv:1610.06325v1 PDF, printed p. 16, section 4.1, was inspected both as extracted text and as a rendered page. Its final Q-Lipschitz estimate relies on a generic Hölder-norm comparison for the difference of two moduli. The pointwise reverse triangle inequality does not imply that comparison.

For z1(x)=x and z2(x)=x+ε on [−1,1], 0<ε<1, the Cδ norm of z1−z2 is ε. At x=−ε and x=0, the difference |z1|−|z2| takes values ε and −ε. Therefore

    [|z1|−|z2|]Cδ ≥ 2ε^(1−δ),
    [|z1|−|z2|]Cδ / ||z1−z2||Cδ ≥ 2ε^(−δ) → ∞.

Both inputs are gradients of smooth scalar functions and stay in a bounded smooth family. Thus no generic bounded-set Lipschitz constant repairs this composition step. At δ=1/2 and ε=1/4096, the seminorm ratio is at least 128, checked using exact rational arithmetic.

This example does not show that these two gradients are potentials generated by one fixed forcing and nearby scalar conductivities. It therefore exposes an unsupported proof step without disproving the specialized statement. No full comparison with the associated SIAM journal proof was performed. The audit does not claim that paper was retracted, corrected, or independently disproved.

### What survives without that step

Along any existing regular trajectory, μ(t)≥e^(−t)μ0 follows directly from the reaction equation. Thus finite-time collapse of the positive minimum is excluded.

If the Cδ norm is bounded up to a finite endpoint, elliptic Hölder estimates bound ∇u in Cδ, the valid single-function modulus bound controls |∇u| in Cδ, and the product estimate bounds μ_t in Cδ. Integrating in time gives a positive Cδ endpoint. This argument uses boundedness of Q, not local Cδ-Lipschitz continuity of Q or compactness of a Cδ ball. Extending that endpoint as a regular trajectory still requires a valid local restart/concatenation theorem in this class. The derivative states this premise explicitly.

A weaker valid estimate is also available. For a≤μi≤b and ||∇ui||∞≤G, testing the difference elliptic equation gives

    ||∇(u1−u2)||2 ≤ (G/a)||μ1−μ2||2,
    ||Q(μ1)−Q(μ2)||2 ≤ G(1+b/a)||μ1−μ2||2.

This proves uniqueness among already existing regular trajectories by Gronwall. It supplies neither local existence nor Cδ restart on its own. It does justify rotational symmetry in the radial special case without relying on the disputed generic composition step.

The finite-time H1-potential, L1-flux, and L1-time-variation bounds are correct. The static oscillatory conductivities have fixed bounds and energy but unbounded Hölder seminorm; they invalidate coercivity of that norm, not continuation or convergence itself.

## 4. Dissipation and the frozen variational step

The domain v≥−m is essential. The derivative and second derivative of r_m are correct, and

    r_m(v)−v²/(3m)=v²(m+v)/(6m²)≥0.

At the boundary, ∂r_m(−m)=(−∞,−1/2]. Solving the inclusion selects v=m(g−1); the other algebraic root violates the velocity domain except where it coincides. The two Fenchel terms and their sum match the Lyapunov dissipation, including g=0.

The one-step direct method is sound with bounded m bounded below, 0<τ<1, and the bounded smooth connected domain/mean-zero bounded forcing conditions made explicit in the derivative. Cubic coercivity, strict convexity, weak lower semicontinuity, and the closed affine obstacle yield a unique L3 minimizer. Pointwise Euler conditions are correctly conditional on enough extra regularity; at an active obstacle they force g=0.

The minimizer need not be bounded, so iteration of this exact bounded-m construction is not established. The packet states that gap. Weighted square-velocity control gives finite-time L1 variation but not spatial compactness. The periodic conductivity example correctly exhibits the mismatch between average reciprocals and reciprocal averages, and hence failure of a naive separate-weak-limits product passage. It is not a trajectory or a failure of the explicit one-dimensional evolution.

## 5. Fixed-flux special cases

On an interval the weak elliptic equation and zero boundary flux fix F independently of μ. The displayed density formula, finite-time strict positivity, and exponential Cδ convergence follow exactly. At F=0 the finite-time gradient is zero, so the chosen limiting gradient is sign F with sign 0=0.

For t≥log 2, |F|/μ≤2 gives dominated convergence in every finite Lp. Integrating the gradient difference and subtracting the mean gives uniform convergence of the potentials. Uniform-gradient convergence is not asserted; sign changes or degeneration may obstruct it. Primal-dual equality certifies optimality, with no assumption of global potential uniqueness.

For radial bounded forcing, Q=O(r), Q is Lipschitz, Q(R)=0, and the vector field Q(r)e_r is Lipschitz at the origin. Dividing by a positive Cδ conductivity gives the claimed finite-time gradient regularity. The radial formulas directly construct the solution. The weaker L2 uniqueness estimate above removes dependence on the questioned Cδ-Lipschitz proof for the symmetry claim. Large-time convergence in finite W1,p and uniform norm is valid. The radial 1-Lipschitz potential certifies optimality against every feasible flux, not merely radial ones.

## 6. Degenerate potential family

The density and perturbation glue C1 across their support endpoints. The forcing has compact support, zero mean, and is bounded. The gradient supports are disjoint as claimed; where density is positive, u_x=1. Elsewhere the product with density vanishes. Hence the elliptic and reaction equations and zero boundary flux hold exactly.

The base slope lies in [0,1], and the perturbation derivative is bounded by 1/128. Every potential is therefore an MK potential after subtracting the mean. Independent beta-integral calculations give

    ∫w = 1/30720,
    ||w−∫w||2² = 11/2202009600 > 0.

The two prescribed subsequences of sin(log(1+t)) give distinct mean-zero limits. They differ in every finite Lp and the uniform norm; this is not additive-gauge drift. The finite time-integral of ||u_t||2² is consistent with the absence of convergence, since it gives no L1-in-time length bound.

The initial conductivity vanishes on open sets. That explicitly violates the original strict-positive initial-data class. No approximation step in this packet transfers the example into that class.

## 7. Sources and reproducibility

All nine PDF sizes and SHA-256 hashes were independently recomputed and match the manifest. No PDF/text source body or screenshot is distributed in this audit. Associated arXiv URLs identify preprint versions; DOI links do not assert identical PDF bytes.

Fresh public arXiv metadata checks confirmed the 2016 original preprint, the two-author 2020 Transport Energy v2, and the 2023 FEM v1. The 2022 journal metadata in the available official HTML lists Facca, Piazzon, and Putti and the title L1 Transport Energy. These title/author/version distinctions are preserved. A fresh attempt to open the OWR DOI through the web reader failed; the pinned local OWR PDF remained available. This is not a claim of a new successful PDF download.

The 2020 transport-energy preprint has a separate measure-space metric flow and regularized flow. Its energy normalization is twice the packet's S. The 2023 work builds finite-dimensional functional approximations and a minimization scheme. Neither source is silently substituted for all trajectories of μ_t=μ(|∇u|−1). Other finite-dimensional, static regularization, and beta-family papers likewise retain their distinct scopes. This audit is bounded source verification, not a worldwide literature-exhaustiveness certificate.

The original checker passed normal, -O, and -OO execution at UID 1000, with actual failed directory creation and 13 failed existing-file write-opens in every mode. Full stdout/stderr files are supplied, not just success booleans. The corrected derivative is likewise tested with its own updated pins. The independent checker imports no original code and covers non-scalar triangle-network algebra, Fenchel support inequalities, explicit fixed-flux/radial identities, independently integrated perturbation moments, and nine semantic overclaim controls.

External controls verify rejection of in-packet output, existing external output, writable required-read-only packets, and a changed report with stale pins. A deliberately wrong cubic sign is also rejected after re-pinning the mutated original checker, and by the independent checker without a hash guard. These two controls distinguish mathematical regression detection from mere byte-integrity rejection.

Permission read-only is not kernel immutability: the file owner can change modes. Before/after hashes show unchanged tested inputs. Exact bounded computations support regression testing; none proves infinite-dimensional existence, compactness, or the complete conjecture.

## Public source links

- Original OWR report: https://doi.org/10.4171/owr/2018/39
- Inspected original local-theory version: https://arxiv.org/abs/1610.06325v1
- Associated SIAM publication: https://doi.org/10.1137/16M1098383
- Energy and numerical formulation: https://arxiv.org/abs/1709.06765v2
- Inspected Transport Energy preprint: https://arxiv.org/abs/1909.04417v2
- L1 Transport Energy journal record: https://doi.org/10.1007/s00245-022-09880-1
- Inspected FEM approximation: https://arxiv.org/abs/2304.14047v1
