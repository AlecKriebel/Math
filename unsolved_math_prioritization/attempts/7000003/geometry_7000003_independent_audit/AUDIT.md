# Independent adversarial audit: problem 7000003

Assessment date: 2026-10-05 UTC. Target: Ghomi Problem 1.3, rank 748 / AMR-069-0003.

## Verdict

**SCOPED PASS. No resolution of the original problem. No mandatory corrections.**

The five retained approaches are valid restricted results or obstruction controls at the scope stated in the author freeze. They neither prove full rigidity nor supply a qualifying counterexample. The mathematical disposition remains **no_resolution, 5/5 approaches completed**. This is not a solved or already-solved certificate.

The seven author files and the 15,539-byte archive were preserved. The archive SHA-256 is `fd97db7181994876f78dbc2afc20d497bdd2fd34becdf2f20c10c8ea66cb4b48`. Its contents agree byte-for-byte with the seven author files. The author verifier reproduces 24 assertions and 8 rejected corrupted controls. An independently written verifier, using Cartesian Laurent differentiation and SymPy rather than the author's sparse-polynomial engine, passes 45 assertions and rejects 9 mutations.

All four public PDFs were independently retrieved into process memory and hashed. Every byte count and SHA-256 agrees with SOURCES.json. No source PDF or extract was saved in this audit deliverable. Public-source locations and inspection scope are in SOURCE_CHECKS.json.

## 1. Exact target and meaning of rigidity

The original 2019 source was checked directly at printed pages 4–6, especially Problem 1.3. The target is extrinsic isometric rigidity for negative-curvature annuli with two specified convex planar boundary curves in Euclidean three-space. Its actual sentence does not impose tangent boundary planes, parallel planes, rotational symmetry, the nonvanishing meridian-height condition, or nondegenerate closed characteristics. The author correctly declines to append those restrictions.

The source distinguishes isometric congruence from the stronger phenomenon of a continuous isometric flex. Thus ruling out one deformation family, or proving infinitesimal rigidity at one immersion, is not a proof of the stated global uniqueness question. The fixed-boundary infinitesimal theorem uses pointwise-fixed parametrizations; fixing the two boundary sets does not literally impose that condition. Smoothness and embedded-versus-immersed conventions cannot be resolved solely from the short problem sentence. These limitations are correctly acknowledged in the freeze.

Source: [Ghomi, Open Problems in Geometry of Curves and Surfaces](https://people.math.gatech.edu/~ghomi/Papers/op.pdf).

## 2. Primary-source scope check

The 2025 Ghomi–Raffaelli paper was checked in the author's September 19 revision and publisher HTML. Its Nirenberg setup has negative curvature in the interior and convex boundaries lying in tangent planes. It poses the combined injective-interior-Gauss-map / zero-normal-linking obstruction as a question. Its examples satisfy different parts of that condition, rather than resolving the conjunction. The paper distinguishes embeddedness in the zero-linking reduction. The publisher confirms volume 35, article 381, publication October 9, 2025. The arXiv record displays v2 dated September 10, 2025. The author packet accurately describes the scope and does not misidentify a later theorem as a solution.

Sources: [author manuscript](https://ghomi.math.gatech.edu/Papers/asymptotic.pdf), [publisher](https://link.springer.com/article/10.1007/s12220-025-02200-3), [arXiv record](https://arxiv.org/abs/2412.19266).

Han–Khuri's 2011 Theorems 1–2 are conditional rigidity results for closed tight surfaces. Their boundary-degeneracy and closed-asymptotic-curve integral assumptions are not automatically available here. Equation (2.3) supports the packet's comparison with the integrated transverse coefficient. The packet does not overextend it. [Primary PDF](https://www.math.stonybrook.edu/~khuri/Khuri_Han_JDGA.pdf).

The 2026 paper's Theorem 1.1 concerns the equality case in the total-absolute-curvature lower bound; §6.3.2 concerns total positive curvature and flat convex hulls. Neither is the required annular uniqueness theorem. The nearby 2019 total-positive-curvature value differs from the 4π convention in these sources, but the author's arguments do not use it. [Primary HTML](https://arxiv.org/html/2604.25024v1).

Two additional bounded public searches located no later complete resolution. This is a retrieval result, not a proof that no such result exists. Historical repository-queue and all-state-PR-search statements in the author README were not independently replayed, and are outside this mathematical/source/integrity verdict.

## 3. Claim-by-claim mathematical audit

### 3.1 Boundary rotation-field lemma: PASS

At a point with orthonormal tangent vectors e1,e2, an infinitesimal strain-free derivative has the form dV(e1)=(0,p,q), dV(e2)=(-p,0,h). The unique rotation vector is y=(h,-q,p). This directly verifies existence and uniqueness; it does not presume that the full three-dimensional derivative of V exists.

Mixed-derivative compatibility forces the normal components of both coordinate derivatives of y to vanish. With F and V of class C², y is C¹, so the differentiation used in the proof is legitimate. If V vanishes pointwise on a regular boundary, y is parallel to its tangent. Taking the surface-normal component of the boundary derivative gives λκ_n=0. Hence nonzero boundary normal curvature forces y=0 there. No global unique-continuation conclusion follows from this calculation alone, and none is claimed.

For a surface tangent along its boundary to one fixed plane, the continuous surface normal is constant along that boundary. The shape operator therefore annihilates the nonzero boundary tangent, so K=0 there. The distinction between interior K<0 and boundary degeneracy is essential and correct. A plane containing the boundary is not automatically a tangent plane.

### 3.2 Rotational all-mode infinitesimal theorem: PASS

Independent elimination of the three strain equations gives exactly the two Fourier ODEs printed in PROOFS.md. The zero mode is included: B'_0=(r'/r)B_0, C'_0=0. For every integer mode, r>0 and nowhere-zero z' on the compact interval give continuous ODE coefficients, including endpoints. A C¹ field allows differentiation of its Fourier coefficients. Zero data at one parallel forces every coefficient to vanish; uniqueness of Fourier coefficients for continuous periodic functions then kills the full field.

The theorem really is infinitesimal and rotational-base-specific. It does not require negative curvature, and does not apply when z' vanishes at a tangent-boundary endpoint. There is no uniform-limit argument in the packet pretending to remove that obstruction.

The nonlinear comparison is also correct within its explicitly fixed axis / fixed rotational-coordinate class. Equal metrics force equal positive radii and height derivatives of opposite or equal sign. Since z' never vanishes, its sign cannot switch. Two fixed boundary heights exclude the reflected alternative. Nothing shows an arbitrary comparison immersion remains rotational.

### 3.3 Catenoid–helicoid associate family: PASS

Direct Cartesian differentiation confirms the derivative relations, conformal metric, and exact vertical period 2π sin α. Unless sin α=0, this parametrization does not descend through the annular deck transformation. At the remaining parameters it is congruent to the catenoid. Its derivative with respect to the associate parameter is also nonperiodic at the catenoid. This is a precise rejection of that construction, not a classification of all isometric annuli or all possible deformation families.

### 3.4 Negative-curvature graph obstruction: PASS

For a C² graph and a regular C¹ projected closed curve, asymptoticity gives Qγ' perpendicular to γ', where Q is the Hessian. Invertibility of Q ensures the multiplier relating Qγ' to Jγ' is continuous and nonzero. If one point avoids every projected tangent line, the second scalar factor in the derivative of the support-like function also has one nonzero sign. The derivative of a periodic C¹ function cannot have that sign everywhere. All differentiations and sign arguments work at the stated regularity.

This proves the claimed tangent-line-covering conclusion. It supplies neither a global graph representation of an arbitrary annulus nor the required missed point for every projected loop. In particular, the explicit ribbon's core has a simple radial planar projection, but the ribbon is not a graph over a neighborhood of that entire projection. There is no contradiction.

### 3.5 Characteristic return multiplier: PASS

On the stated smooth two-sided coordinate neighborhood, negative curvature and L=0 imply M≠0. Implicit differentiation of L+2Ma+Na²=0 yields a_t=-L_t/(2M). The linear variational equation gives the exponential return multiplier printed in the packet. Nonzero exponent makes the local fixed point hyperbolic and isolated; zero exponent alone proves neither nonisolation nor a bending. In particular, this return map is the holonomy of one asymptotic foliation, not an isometric-deformation map or the normal connection's holonomy.

The existence of smooth periodic coordinates is part of this local statement. In the actual embedded annulus it applies to its simple, two-sided core. No one-sided or self-intersecting neighborhood is needed.

## 4. Adversarial audit of the explicit ribbon

### Smoothness, embeddedness, torsion, and framing: PASS

Independent Cartesian differentiation starts from γ(q)=((4+cos 2q)cos q,(4+cos 2q)sin q,sin 2q). The radius is at least 3 and recovers q modulo 2π, proving injectivity of the circle map. The exact squared speed is (4+cos 2q)²+4≥13. Thus this is a smooth embedded regular closed curve, rather than a periodic parametrization with hidden repeated image points.

The independently derived triple product is -6(c³-24c²+32), c=cos 2q. The supplied decomposition proves its value is at most -42 throughout the full interval [-1,1], not merely at sampled angles. Consequently γ'×γ'' is never zero, curvature is positive, and torsion is strictly negative. The Frenet vectors are smooth and periodic because they are globally defined algebraically from the periodic nonvanishing jets. Nonzero torsion does not obstruct this periodic framing. A rotating normal frame and parallel-transport holonomy are different notions.

For X(s,t)=γ(s)+tN(s), the independently calculated first form is diagonal with E=(1-tκ)²+t²τ² and G=1. Since τ≠0, E never vanishes for real t. The surface is immersed for every t, but only a sufficiently narrow strip is certified embedded: the compact-curve tubular neighborhood theorem provides that width. The packet correctly does not assert global embeddedness for large t.

### Curvature and neutral core: PASS

The full numerator of the second-form coefficient L, using the unnormalized normal (1-tκ)B-tτT, is

    t τ' + t²(κ'τ-κτ').

The mixed coefficient has numerator τ, and the coefficient in the ruling direction is zero. Therefore K=-τ²/E²<0. At the core, L=0 and L_t=τ'. Since τ is a periodic nowhere-zero function, the integral of τ'/τ is zero. This confirms P'(0)=1 for the actual embedded strip. No Gauss–Codazzi realization gap exists: the metric and second form were derived from the explicit immersion itself. The strip is a control against inference from negative curvature alone, not a nontrivial isometric bending.

### Both offset boundaries fail planarity: PASS

The independent calculation recovers the Frenet normals at q=0,π,π/2,π/4 directly from Cartesian velocity and acceleration, including the tangential-acceleration subtraction. The determinant of the four offset points is exactly

    -2(5-t)(3+t)(1-5t/√70).

Every factor is nonzero for |t|<1. Thus the entire offset curve is nonplanar for each such t, including both t=ε and t=-ε for a sufficiently small ribbon. The calculation uses four points on each whole boundary; it is not a visual inference or a test of only one boundary. No planar-boundary or convex-planar-boundary counterexample has been produced.

### Additional independent exclusion: repeated surface normal

The exact Cartesian x-component of γ'×γ'' is

    2 sin q (3 cos²(2q) - 2 cos(2q) - 4).

Under q↦-q, this component changes sign while the other two components remain unchanged. Choose q in (0,π/2) with cos(2q)=(1-√13)/3. The x-component vanishes and the other components, hence also the norm, agree at q and -q. Since the cross product never vanishes, B(q)=B(-q) at two distinct core points.

At t=0 the ribbon's surface normal is B, not its director N. Thus its interior Gauss map is noninjective. In light of the injectivity condition for the 2025 tangent-boundary class, no extension containing this exact ribbon can belong to that class: extending the boundary cannot undo an already repeated interior normal. This strengthens the control but is **not** an obstruction to every annulus with merely planar convex boundaries. The broader Problem 1.3 still has the same unresolved boundary/global gap.

## 5. Verifier quality and limitations

The author's 24 checks are exact identities and elementary algebraic controls. The eight deliberate corruptions exercise selected signs, factors, and false descent/planarity claims. Some checks validate formulas already encoded by hand; none is a proof assistant for ODE uniqueness, Fourier completeness, tubular embedding, literature completeness, or global rigidity. The author states these limitations accurately.

The independent replay is deliberately different: it differentiates the original Cartesian curve via Laurent polynomials, reconstructs all four normal-offset points, solves the Fourier strain equations, differentiates the implicit characteristic equation, and computes the full ribbon second form. Its 45 assertions include integrity checks as well as mathematical identities; its 9 rejected mutations are not an exhaustive fault model. It does not import the author's polynomial class. It executes the author's verifier separately only to confirm reproducibility. It requires Python 3 and SymPy; the inspected environment had SymPy 1.14.0.

The audit manifest binds the audit artifacts and excludes itself from self-hashing. AUTHOR_SNAPSHOT.json independently hashes all seven author files, including their manifest. That audit snapshot complements rather than alters the author's own manifest.

## 6. Mandatory corrections and optional improvements

Mandatory corrections: **none** for this scoped no-resolution packet.

Optional clarifications, without changing the verdict:

- State explicitly in any short summary that global rigidity means uniqueness up to congruence, whereas infinitesimal rigidity and absence of a particular flex are weaker conclusions.
- Distinguish the Frenet ribbon director N from the surface normal B when discussing normal linking or Gauss-map injectivity.
- The repeated-binormal computation above can replace an inconclusive extension attempt in the narrower tangent-boundary class. It does not replace the original broad boundary problem.
- Keep the author's integrity and algebraic replay counts separate from analytic proof review and from claims of complete literature coverage.

No source text, raw dataset, private coordination file, or source PDF is included. No remote write was performed. The author freeze remains unchanged.
