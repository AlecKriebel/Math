# Fresh whole-candidate adversarial review: PR 464

Problem 30004807 / OWR-8415343-010. Frozen head `97b2ed225574ca61bd03cb8db021a533e04938dc`, captured with status exactly `claimed_solved`. This is a mathematical and claim-acceptance checkpoint, not review of a finished preprint or permission to publish one.

**Decision: accept the qualified candidate for preprint preparation.** Current mathematical/claim blocking issues: **0**. Unresolved mathematical gaps in the qualified theorem: **0**. Identified attribution repair: **1**, now verified in current root audit notes. Mandatory carry-through requirement for a future package: **1**. Optional presentation addition: **1**. First historical priority remains **unestablished**.

The strongest verified result is an explicit static, spherically symmetric, asymptotically flat spacetime whose natural static slices contain harmonically regular negative-mass ZAS, but whose homogeneous weak Bianchi integral has value `-8*pi` for a genuine source-convention test. The complete scalar contraction is absolutely integrable for every smooth compactly supported vector test on the retained exterior boundary structure. This refutes the geometric implication in the report under the cited BKTZ convention. It does not settle an added energy condition, a specified matter model, arbitrary tilted-slice admissibility, a collapsed-point test convention, or the wider motion/evolution program.

## Independence and actual inputs

`INITIAL_HYPOTHESIS.md` was recorded before any root, peer, or historical audit verdict. I first read only repository instructions and the frozen author's proof, reconstructed the target from independently fetched primary documents, derived the density and flux, and ran an author-free direct four-dimensional computation. `INDEPENDENT_INITIAL_CONCLUSION.md` records qualified acceptance before cross-review. Only afterward did I read the complete root ledger/reconstruction and the completed source-geometry, curvature-flux, reproduction, and priority reports. I subsequently inspected the historical audit and the other frozen claim-bearing landing files for consistency.

I independently fetched and read the complete relevant OWR contribution, BKTZ Sections 1.3–1.4 and its weak-identity definition, theorem, boundary calculation and corollaries, and the Bray–Jauregui definitions of convergence, ZAS, resolution and mass. I visually inspected OWR printed 2232–2233, BKTZ pages 6 and 9, Bray–Jauregui page 6, and DKMV pages 3–4: seven primary page scans. I also read Bray–Jauregui Section 6.6, which treats extensions beyond the time-symmetric setting separately. Foreign PDFs, extractions and rendered scans are private and excluded from the public whitelist. Receipts retain only bibliographic locations, sizes and hashes.

The final input binding records the actual SHA-256 values of every reviewed root/peer narrative and the thirteen frozen source files. All thirteen frozen files retain their captured sizes and hashes. The historical standalone author-manifest hash has no supplied manifest bytes/path and is **unattested**; I do not promote that reference into a verified manifest. The immutable snapshot binding is a separate, verified provenance claim.

## Exact target and admissibility

The [OWR report](https://ems.press/content/serial-article-files/46918), printed 2232–2233, describes a geometric class through regular negative-mass ZAS on spacelike slices and conjectures the homogeneous weak identity for that class. Its displayed test is a vector field. The printed text imposes no additional independent NEC, electromagnetic constitutive law, or lapse-curvature condition on that conjecture.

[BKTZ v3](https://arxiv.org/pdf/1901.00813v3) supplies the operative technical setting. Section 1.3 identifies constant-time spacelike slices; page 6 footnote 3 explicitly permits support on the inner boundary. Definition 2.1 distinguishes the inhomogeneous identity, whose integral equals a limiting boundary flux, from the homogeneous identity, whose integral/flux is zero. Equation 2.5 retains the radial boundary test component. The candidate's radial test has angular-independent spherical components, meeting even the supplementary convention used in that displayed formula. A section of the tangent bundle at a boundary need not be tangent to the boundary surface.

For `a>0`, `rho>=a`, and `phi=1-a/rho`, the static slice metric is `h=phi^4 delta`. The Euclidean resolution is smooth and positive at the retained sphere; `phi` vanishes precisely there, its inward normal derivative is `1/a>0`, and its Euclidean Laplacian vanishes. These directly satisfy [Bray–Jauregui](https://arxiv.org/pdf/0909.0522v2), Definitions 6–7. The ZAS area condition applies to every permitted approaching boundary graph converging in C1: its Euclidean area stays bounded, while the maximum of `phi^4` tends to zero. This is stronger than a coordinate-sphere calculation. Definition 10 gives

    m_reg = -(1/4) (4 a^(2/3))^(3/2) = -2a.

The static shift and time derivative of `h` vanish, so these slices are totally geodesic/time symmetric. The spatial area radius `r=(rho-a)^2/rho` gives `h=(1+4a/r)^(-1)dr^2+r^2dOmega^2`, confirming the negative-mass Schwarzschild spatial metric and constant cumulative mass. The spacetime lapse is independently specified; sharing this spatial metric does not make the spacetime vacuum.

The short report does not formally settle admissibility for every nonsymmetric spacetime or every arbitrary hypersurface. This review accepts its literal geometric condition in the cited static-foliation construction, not an unstated private intention. Clarification of a stronger intended definition could be useful; this fact is recorded without preparing or initiating outreach.

## Curvature reconstructed and falsified independently

For `N=A+B*N_v`, `N_v=(rho+a)/(rho-a)`, assume `A,B>=0` and `A+B>0`. In Cartesian exterior coordinates the spatial connection is

    Gamma^k_ij = 2 phi^(-1)
                 (delta^k_i phi_j + delta^k_j phi_i - delta_ij phi^k).

The additional nonzero time connections are `Gamma^0_0i=N_i/N` and `Gamma^i_00=N*phi^(-4)*N_i`. Their direct Ricci contraction gives the static warped-product formulas in the candidate. This is a smooth-interior calculation only.

For a radial function, `phi'=a/rho^2`, `phi''=-2a/rho^3`, `N_v'=-2a/(rho-a)^2`, and `N_v''=4a/(rho-a)^3`. Substituting these into the conformal spatial connection shows that the radial and tangential Hessian components of `N_v` are respectively

    4a(rho+a)/(rho(rho-a)^3),
    -2a(rho+a)/(rho(rho-a)^3).

They equal `N_v` times the corresponding covariant spatial Ricci eigenvalues. Thus `Hess_h N_v=N_v Ric_h` and `Delta_h N_v=0` hold identically, rather than merely at sampled points. Consequently

    R_g=0,
    G^t_t=0,
    G_spatial = (A/N) Ric_h.

The spatial mixed Ricci eigenvalues are `(4,-2,-2)a/(rho^3 phi^6)`. At `A=B=1/2`, `N=phi^(-1)`, giving exactly the frozen proof's Einstein tensor. Its Ricci-square invariant is `6a^2/(rho^6 phi^10)`, positive and divergent at the inner end. A vanishing scalar curvature does not imply a removable singularity.

My new standard-library checker differentiates the complete diagonal four-metric through exact second-order rational jets in Cartesian coordinates. It constructs all Christoffel symbols, their derivatives, the full Ricci tensor and Einstein tensor, and tests arbitrary vector values/first derivatives and index pairing. It imports no author or peer code. **All 2,916 checks at 72 metric points pass** in both normal and optimized Python, with byte-identical result bytes. The points include rotated radial directions, radii as close as `rho/a=1001/1000`, and main, vacuum, constant-lapse and other positive mixed-lapse cases. Explicit exceptions, not assertions, enforce every check.

Those finite checks are falsification evidence for signs, missing components, metric factors and coordinate dependence. They are not a proof of quantified identities by sampling; the analytical derivation above and below establishes the universal statements.

## Whole scalar, singular indices and boundary sign

Define the weighted mixed spatial tensor

    D^i_j = N phi^6 G^i_j
          = (Aa/rho^3) (6 n_i n_j - 2 delta_ij),  n=x/rho.

It is smooth up to `rho=a>0`, Euclidean symmetric and traceless. Its contraction with the spatial connection is

    (2/phi) [tr(D) phi_k + D^i_k phi_i - D^k_j phi_j] = 0.

All mixed Einstein entries containing time vanish, as do the relevant static spatial connections with a time lower argument. Therefore, for every source-convention test vector field,

    G^mu_nu nabla_mu psi^nu dV_g
        = D^i_j partial_i psi^j dt d^3x.

The right side is bounded on the compact support, including the retained boundary, so its absolute integral is finite. Cartesian coordinates avoid any false inference from singular spherical coordinate components at the poles. The result applies to arbitrary time and angular dependence, not just the specially chosen radial test.

Raising the differentiated index in `G_mu_nu nabla^mu psi^nu` produces the same mixed contraction pointwise on the smooth interior. No index raising or lowering of a tensor distribution at the singular boundary is assumed. Independently smooth covectors need not become smooth source-convention vectors after singular index raising. The vector and covector test classes are therefore not silently exchanged.

For the main example and `chi=1` near the boundary, the separate radial and each angular connection density have asymptotic coefficients `4/(rho-a)` and `-2/(rho-a)`. These summands would each have a logarithmically divergent integral, but their pointwise sum is zero. The scalar must be formed before integration, exactly as the proof does. No separate divergent integral, principal value, distributional product or regularization is used.

The Euclidean divergence of `D` vanishes: its radial and tangential eigenvalues are `4Aa/rho^3` and `-2Aa/rho^3`, and `D_r'+2(D_r-D_T)/rho=0`. The inner outward normal of the truncated exterior is **minus** `n`. Ordinary integration by parts and absolute convergence give

    I_N(psi) = -(4A/a^2)
               integral_{R x S_a} psi_spatial dot n dt dA_delta.

The physical-metric flux gives the same sign: its outward normal covector has radial component `-phi^2`, its induced tube density is `N phi^4 rho^2`, and their product with `G^rho_rho psi^rho` is `-4Aa psi^rho/rho`. No lapse, area or normal factor is missing.

The permitted test `psi=eta(t)chi(rho)partial_rho`, with `integral eta=1` and `chi=1` near the inner sphere, is smooth in exterior Cartesian coordinates because `a>0`. The full scalar density is `4Aa eta partial_rho(chi/rho)`, an ordinary integrable function. Its integral is `-16*pi*A`; the main case is `-8*pi`. This is the inhomogeneous identity with a nonzero boundary functional and a counterexample to the homogeneous identity.

## Edge and limiting cases

- **Vacuum `A=0,B>0`:** `G=0`, all defects vanish, and constant time rescaling gives the negative-mass Schwarzschild vacuum spacetime. Vanishing Ricci does not remove its Weyl/Kretschmann singularity.
- **Constant lapse `B=0,A>0`:** the metric remains Lorentzian and the same nonzero boundary functional persists. Its curvature has order `(rho-a)^(-6)`, whereas positive `B` gives order `(rho-a)^(-5)`. The frozen proof's inverse-linear lapse comparison is explicitly restricted to `A,B>0`.
- **Excluded `A=B=0`:** this is not a Lorentzian metric. Opposite-sign parameters that could produce lapse zeros are outside the asserted family.
- **Flat `a=0` control:** the interior becomes flat, but the retained inner sphere and chosen radial test change with `a`. The radial field `x/|x|` is not a fixed smooth origin-crossing test as `a` shrinks. For a fixed smooth Cartesian test, the constant boundary value averages against `n` to zero and the defect is `O(a)`, tending to zero. No flat-spacetime anomaly is proved.
- **Timelike singularity:** `s'=phi^3` makes the candidate's radial metric conformal to `-dt^2+ds^2`, with finite `s` and `s~(rho-a)^4/(4a^3)`. Nearby tubes have Lorentzian induced metrics. A radial null geodesic has finite remaining affine length `(rho-a-a log(rho/a))/E`. Together with invariant blow-up this gives a genuine timelike naked inner end. No nondegenerate four-dimensional metric extension to the cylinder is claimed.
- **Tilted slices:** uniformly spacelike local graph tilts `t=t0+q s(rho)`, `|q|<1`, retain a smooth positive resolution and negative regular mass. A nearly null graph with `f'=phi^3 sqrt(1-phi^2)` instead has radial coefficient `phi^6` and angular coefficient `phi^4`; any simple defining conformal factor leaves a degenerate radial resolution. The analogous tilt also defeats regular resolution for the cited vacuum prototype. Thus an all-arbitrary-tilted-slices condition would change the problem substantially. The static-foliation qualification is essential and already present.
- **Energy/matter:** static energy density is zero, while angular pressure is negative for `A>0`. An angular null direction violates NEC. Initial-data constraints with `R_h=0,K=0` do not establish spacetime NEC. No prescribed Einstein-matter constitutive system is solved here.
- **Existing sufficient results:** the main example has nonzero `x^(-5)` Einstein curvature, missing BKTZ Theorem 1.1's `x^kappa`, `kappa>0`, gain. Its lapse logarithmic derivative has constant correction `1/a`, rather than Corollary 2.2's `1/(2a)`. Corollary 2.3 additionally fixes the lapse/radial-metric relation, which this lapse lacks. The established sufficient theorems do not cover the candidate.

## Priority, attribution and cross-artifact consistency

I independently verified the positive prior metric/tensor evidence in [Dadhich–Kar–Mukherjee–Visser](https://arxiv.org/pdf/gr-qc/0109069), equations 9–15. Its dictionary is `(m,bar_r,kappa,lambda)=(-2a,rho,A,B)`. The positive square-root branch on `rho>a` gives exactly the affine lapse in the candidate. Their `tau` is radial **pressure**, not radial tension; the negative-mass substitution gives precisely the candidate's radial positive and angular negative stresses. Their subsequent wormhole classification explicitly concentrates on `m>0`. Attribution should describe this as the known family's negative-mass specialization, not assert that they printed the later regular-ZAS/BKTZ application.

The [official APS page](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.65.064004) and the original PDF spell the third author's surname **Mukherjee**. APS lists publication on 7 February 2002; the issue date is 15 March 2002. The OWR report's volume/workshop year is 2021, while the publisher lists 26 November 2022 for publication. These dates must not be conflated.

The older family and tensor cannot be claimed new. BKTZ's already published flux calculation supplies the method after convergence is established independently; their sufficient theorem cannot be invoked as a black box on this excluded borderline case. The defensible contribution is the explicit, properly convergent counterexample application to the report's geometric implication. This is mathematically modest and should be written as such.

The separate priority report documents substantial but bounded searches and no established earlier printed application resolving this exact conjecture. I read and challenged that positive-comparison argument; I did **not** independently repeat its full search corpus. Lack of a located application does not prove novelty, continued openness or first priority. Conversely, the earlier metric alone does not establish that the later conjecture had been refuted in prior work. I do not recommend `already_solved` solely from that construction match.

The frozen proof, landing files and historical audit consistently preserve the vector-test, static-slice and NEC qualifications. Current root/peer derivations agree on Einstein components, signs, mass, invariant blow-up, scalar absolute integrability and the all-field functional. The source thirteen-file hashes agree. The historical author's final `assert all_passed` is insufficient as an optimized-mode failure guard, but the fresh independent reproduction driver explicitly requires all 17 Boolean values/count, success flag and exact expected output in both modes; the historical 35-check auditor uses explicit raises. This is a verification-entry-point limitation, not mathematical evidence against the accepted theorem.

**Attribution repair verified in current audit notes (1):** I reread the corrected root ledger and mathematical review in full. They now credit DKMV before the derivation, give the negative-mass dictionary and correct Mukherjee spelling/chronology, acknowledge the old positive-mass classification boundary, credit BKTZ's flux method, and independently prove convergence. The corrected final priority report and reproduction normal-trace formula agree. No current mathematical or claim-acceptance blocker remains.

**Mandatory future-package carry-through (1):** the eventual abstract/introduction, proof, bibliography, current landing/metadata descriptions and other claim-bearing publication materials must carry those same credits and restrictions. Preserve frozen historical source bytes with clear historical labeling if bundled. No current preprint has yet been supplied, so package-wide implementation and publication readiness have not been reviewed or approved. This is the next required gate, not a newly invented defect in an absent paper.

**Optional presentation addition (1):** explain the uniformly spacelike versus nearly null tilt boundary, or cite Bray–Jauregui's time-symmetric setting/Section 6.6, alongside the existing static-foliation qualification. No all-tilted-slices theorem should be added.

## Acceptance boundary and next gate

The qualified counterexample has no unresolved mathematical gap found by this review. The root may proceed to concise preprint preparation with the verified attribution carried into every current publication artifact, retaining the exact hypothesis and exclusions. This report is not a final preprint/package audit, does not authorize ignoring the user's required new-adversary repair loop, and does not certify human peer review, proof-assistant verification, or historical first priority.

No original proof-search route was attempted; all new work verifies or stress-tests the frozen candidate. No original source, Git/index/branch, PR, status, remote service, cloud document or paper was changed, and no individual was contacted. All foreign copies remain private. Only the explicit positive public whitelist is suitable for checkpoint selection.
