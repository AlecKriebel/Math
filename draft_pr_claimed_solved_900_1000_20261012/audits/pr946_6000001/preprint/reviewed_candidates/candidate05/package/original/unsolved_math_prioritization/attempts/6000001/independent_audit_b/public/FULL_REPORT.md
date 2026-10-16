# Independent mathematical audit B: finite-dimensional statistical embedding

Problem 6000001 / AMR-059-0001. Audit date: 2026-10-07 UTC.

## Verdict and exact object reviewed

**PASS. No mathematical correction is required for the theorem as stated in the frozen proof.** The result establishes a global proper statistical embedding of every smooth positive-definite statistical manifold without boundary into a finite-dimensional positive Hessian domain. Both ordered dual connections are induced by metric-orthogonal projection. The proposed bound is N = binomial(2n+4,3) for n >= 1.

This verdict binds the original, unmodified author packet:

- Author MANIFEST.json: 1,433 bytes, SHA-256 `7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f`.
- Author PROOF.md: 17,635 bytes, SHA-256 `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`.
- All eight author files match the authenticated manifest. The author packet verifier passed with the independently supplied manifest hash.

The review covers the entire proof, including its global existence arguments, not only its computational identities. No other independent audit report was consulted. Source papers were inspected separately; no paper, copied source passage, dataset, or private coordination material is included in this audit packet.

This is mathematical acceptance of the specified authored proof candidate, not a journal-referee decision, a historical novelty certification, or acceptance of stronger finite-probability, complete, globally convex, or globally dual-coordinate claims.

## 1. Precise scope and the original question

The 1998 problem, item 1(a), asks about an induced dual structure inside a higher-dimensional dually flat manifold. The adjacent footnote concerns an affine-space realization and is not itself a positive-Hessian realization theorem. The source contains no additional completeness, convex-domain, fixed-codimension, or globally injective dual-coordinate requirement. [Furuhata–Matsuzoe–Urakawa, pp.125 and 127](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en).

The intended flatness convention matters. Amari's primary account explicitly requires both torsion and curvature to vanish for dual flatness and works with local affine coordinate systems. Its embedding question also distinguishes the statistical motivation from the abstract geometric question. This supports the proof's torsion-free statistical interpretation. [Amari, *Information Geometry*, pp.81, 84 and 87](https://bsi-ni.brain.riken.jp/database/file/166/169.pdf).

For a general mutually dual pair that is not initially assumed torsion-free, the proof supplies a precise necessary-and-sufficient condition for realization in a torsion-free dually flat target: both original connections must be torsion-free. It does not establish this necessity for a different convention allowing curvature-flat ambient connections with torsion. That distinction is substantive; an explicit negative control below demonstrates it.

The manifold assumptions are sufficient for the topology used: smooth, finite-dimensional, Hausdorff, second-countable, and without boundary. Connectedness is unnecessary. The n = 0 remark is valid separately: a countable discrete manifold embeds properly as a discrete subset of R, and carries no nonzero tangent data.

## 2. Duality, cubic tensor, and the required scalar jet

Let L be the Levi-Civita connection and A = nabla - L. Torsion-freeness of nabla makes A symmetric in its two vector arguments. Duality identifies nabla-star - L with minus the g-adjoint of A. Torsion-freeness of nabla-star then gives the remaining symmetry of g(A_X Y,Z). Consequently C = nabla g is totally symmetric and equals -2 g(A_X Y,Z). This verifies both signs in the proof's equation (2.1).

With lowered coefficients Gamma_ijk, the required third derivative is

    Q_ijk = partial_k g_ij + Gamma_ijk
          = (partial_i g_jk + partial_j g_ik + partial_k g_ij - C_ijk)/2.

Total symmetry follows. Symmetry alone would not make these third-order data a global scalar jet; Q is not a tensor. The proof correctly addresses this stronger compatibility requirement.

At each p, use the germ of the Levi-Civita exponential map and the scalar polynomial

    v -> g_p(v,v)/2 - C_p(v,v,v)/12.

Its value and first derivative vanish, its second derivative is g_p, and its third derivative in normal coordinates is -C_p/2. For a scalar with zero differential, conversion of the third covariant derivative to ordinary derivatives adds all three terms L_ij^a g_ak, L_ik^a g_aj, and L_jk^a g_ai. Their sum is half the symmetrized first derivatives of g, giving exactly Q. Thus the construction defines a smooth section of the scalar 3-jet bundle.

Only the exponential germ at the zero section is required. Local smooth dependence on (p,v) proves smoothness of the jet section; neither geodesic completeness nor a uniform injectivity radius is used. This is a valid intrinsic construction rather than an implicit attempt to patch ordinary third derivatives as tensors.

## 3. One finite global feature space and a smooth right inverse

Start with a proper smooth embedding e into R^(2n+1). Form f from all monomials of degree at most three, including the constant. The dimension count is exactly binomial(2n+4,3). The retained linear coordinates recover e, so f is injective, immersive, a topological embedding, and proper. In particular, f(M) is closed in its Euclidean ambient space.

At a point p, choose n ambient linear functionals whose restrictions have independent differentials. They give local coordinates. Every scalar 3-jet in those coordinates is represented by a cubic polynomial in the chosen linear functionals, hence by the same finite global polynomial feature space. This establishes surjectivity of the full jet evaluation map E at every p, not just a spanning claim for tangent or second-order data.

The jet bundle is an ordinary finite-rank smooth vector bundle. Smooth bundle metrics exist because the manifold is paracompact. In such metrics,

    R = E^dagger (E E^dagger)^(-1)

is a smooth global right inverse. Fiberwise surjectivity makes E E^dagger invertible; smooth inversion is local and does not require a uniform lower bound over noncompact M. Kernel dimensions are constant by the proved surjectivity. No finite coordinate cover, global tangent frame, or analytic convergence assertion is concealed here.

The proper embedding and tubular-neighborhood theorems are genuine declared external inputs. Whitney's original embedding argument and its footnote removing finite ambient limit points support the proper version; the smooth normal-neighborhood theorem applies to the closed image. The proof does not claim its tests establish these topology theorems. [Whitney, *Differentiable Manifolds*, pp.646–647, 654–655 and 665, especially Lemma 19 and footnote 32](https://www.math.ucdavis.edu/~saito/data/high-dimensions/whitney-diffmanifolds.pdf).

## 4. Exact metric and connection pair

Apply R to the prescribed jet section, obtaining smooth coefficients a. Holding a(p) fixed while taking derivatives of the feature functions gives four separate constraints:

    a dot f = 0,
    a dot f_i = 0,
    a dot f_ij = g_ij,
    a dot f_ijk = partial_k g_ij + Gamma_ijk.

Differentiating the second constraint, now allowing a to vary, and setting phi = -a gives f_i dot phi_j = g_ij. Differentiating the third gives f_ij dot phi_k = Gamma_ijk. The cancellation of partial_k g_ij is exact. The sign phi = -a is essential.

Also phi dot df = 0 identically. This removes a genuine global obstruction: a merely closed potential-compatibility form could have nonzero periods, whereas the constructed form has zero periods on every loop. There is no appeal to global exactness from local exactness or from simple connectedness. The extra value constraint a dot f = 0 is harmless and is satisfiable because the full jet map is surjective.

Positive definiteness implies dphi is injective on tangent spaces, but phi need not be globally injective. The proof only requires f to be a global embedding and phi to be a smooth covector field. Its phrase “Lauritzen-type pair” is therefore appropriately qualified; it does not claim a global embedding of each factor from infinitesimal rank alone.

## 5. Global tubular extension and positivity

Identify M with the closed embedded submanifold S. A Euclidean tubular neighborhood may be chosen as the image of an open neighborhood of the zero section in the normal bundle; its radius may depend on the base point. Its inverse gives smooth maps r and nu with z = r(z) + nu(z).

The field phi annihilates TS. Therefore

    Psi_0(z) = phi_(r(z))(nu(z))

has zero restriction to S and differential phi along S. One can check the gradient equality by decomposing any ambient vector into its tangent and normal parts. Differentiating that equality along S gives Hess(Psi_0)(f_i, -) = partial_i phi. In particular, its tangent block is g. Along a fixed normal fiber Psi_0 is linear, so the normal-normal Hessian block at the zero section vanishes. The mixed block is unrestricted but smooth.

Use Euclidean metrics on the tangent and normal bundles and write the Hessian blocks as [A B; B^t 0], with A positive definite. Both tr(A^(-1)) and the squared Hilbert–Schmidt norm of B are globally defined smooth scalars, even for nontrivial normal bundles. Set

    t = tr(A^(-1)) ||B||_HS^2,       lambda = 1 + t.

Adding lambda(r(z)) |nu(z)|^2 preserves the prescribed value and gradient along S. At the zero section the added Hessian is zero on tangent and mixed slots and equals 2 lambda I on normal slots; derivatives of lambda do not survive because the normal coordinate vanishes there.

The quadratic-form estimate

    B^t A^(-1) B <= t I

is valid because the operator norm of a positive A^(-1) is at most its trace and the operator norm of B is at most its Hilbert–Schmidt norm. Thus the completed Schur complement is at least (2+t) I, proving full ambient positivity at every point of S. This is positive-definite Euclidean-signature completion, not a split-signature pairing.

Define U to be the positivity locus of the completed Hessian inside the tubular neighborhood. It is open and contains all of S. Nothing requires one common tube radius, bounded lambda, a uniform eigenvalue bound, compactness of M, or a global frame. Restriction to U retains the properness of f: compact subsets of U are compact in R^N under the continuous inclusion.

The construction may leave U nonconvex and the metric incomplete. It is exactly a global embedding into one open Hessian domain, even though no assertion is made that a single global dual coordinate chart covers U.

## 6. Ambient dual flatness and both induced connections

On U let G = Hess(Psi) and let D be the ordinary coordinate connection. It is flat and torsion-free. Its metric dual satisfies

    (Gamma-star)^C_AB = G^(CD) partial_A G_BD.

The symmetry of third derivatives of Psi makes this connection torsion-free. The functions eta_A = partial_A Psi have invertible Jacobian G. Locally they are coordinates, and their D-star covariant Hessians vanish. This proves D-star is flat throughout U; flatness is local and tensorial, so injectivity of the full gradient map is unnecessary.

Along the embedded image, differentiating the prescribed gradient gives G_AB f_k^B = partial_k phi_A. Therefore

    f^*G = g,
    G(f_ij, f_k) = f_ij dot phi_k = Gamma_ijk.

Nondegeneracy of g identifies the G-orthogonal projection of D with the specified nabla. Restricting ambient duality then identifies the projection of D-star with nabla-star, since the dual of a fixed connection relative to a fixed nondegenerate metric is unique. This checks the ordering of the two connections, not only the metric or an unordered pair.

For necessity, the tangential projection of a torsion-free connection along an immersion has zero torsion: project the ambient torsion equation, noting that the bracket of tangent fields stays tangent. Apply this separately to D and D-star. No curvature condition on the original submanifold connections is needed or claimed.

## 7. Independent checks and adversarial controls

The independently authored script `independent_checks.py` was run with assertions enabled. Its regenerated output matches `INDEPENDENT_CHECKS.json` byte-for-byte. It reports 72 exactly zero symbolic residuals and PASS. These are finite consistency checks; Sections 2–6 above supply the mathematical global review.

Coverage includes:

1. A full scalar 0-through-3 jet system in two variables, with 10 features and determinant 576. The positive test metric has determinant x^2 y^2 + 2x^2 + 2. The identities for the metric, conormal exactness, specified connection, and specified dual connection are checked separately.
2. A genuinely nonlinear coordinate substitution, with eight exact third-jet comparisons. A deliberately tensor-only transformation of Q fails, as it should.
3. All 56 cubic features of a nonlinear proper graph into R^5. The sampled full jet matrices have rank 10 at three distinct points. A quadratic-only feature control has rank 6 and cannot prescribe arbitrary cubic jets.
4. A periodic circle model with nonconstant positive metric and nonzero connection. The exact global right-inverse construction yields a periodic covector field and an identically zero compatibility form, testing the nontrivial-loop issue.
5. A direct circle tube potential with ambient Hessian diag(2,1) at (1,0), separately confirming tangent and normal Hessian contributions.
6. Exact Schur-complement samples with tangent eigenvalues tending toward zero and unbounded mixed blocks. Every sampled completion is positive. Removing the normal correction gives an indefinite matrix; keeping a bounded correction in a separate noncompact example eventually fails.
7. A one-dimensional full jet pair with unbounded cubic data. Omitting the connection from Q loses the prescribed connection; reversing the sign of phi reverses the metric.
8. A nonlinear positive Hessian ambient potential with 16 exactly vanishing dual-curvature components and eight dual-affine-coordinate residuals.
9. A constant Euclidean metric with metric-compatible connection matrices A_x = [[0,-1],[1,0]], A_y = 0. This connection is its own dual and curvature-flat but has T(partial_x,partial_y) = (-1,0). It demonstrates why the stated torsion-free ambient convention cannot be replaced by curvature-only flatness.

The author's separate verification script also passed, reporting 26 exact residuals and four positive Hessian-completion samples. Those checks corroborate the audit but are not counted among the 72 independently generated residuals.

## 8. Literature dependencies and limits

Marugame defines the induced connection using metric-orthogonal projection, treats positive Hessian structures locally, and gives a local equivalence with Lauritzen pairs. The candidate's induced-connection convention matches this source. Its global exact pair and variable tubular extension are proved in the candidate and are not attributed to Marugame's local theorem. [Marugame, *The Bonnet theorem for statistical manifolds*, Introduction and Sections 2.1–2.4](https://arxiv.org/abs/2103.10102).

Lê's corrected v6 states compactness in Theorems 5.1 and 5.6, and the arXiv revision record explicitly identifies its addition. The finite-model result therefore is not used to justify an unrestricted noncompact realization. The target in the audited theorem is a custom Hessian domain, which is a different allowed target. [Lê, *Monotone invariants and embeddings of statistical manifolds*, v6](https://arxiv.org/abs/math/0506163v6).

The historical MPI preprint was inspected as a historical claim, not substituted for the unavailable final Journal of Geometry full text. No conclusion of this audit depends on that journal abstract or on an unrestricted historical finite-sample assertion. [Lê, MPI preprint 77/2003](https://files-www.mis.mpg.de/mpi-typo3/preprints/2003/preprint2003_77.pdf).

Five independently retrieved source PDFs have retained retrieval records and hashes matching the author packet's source metadata. Their local bytes were rehashed during this audit. An additional Amari primary PDF was inspected and its public URL independently opened. The exact retrieval and inspection distinctions, including unavailable final journal text, are recorded in `SOURCE_METADATA.json`.

## 9. Acceptance conditions and optional editorial improvement

Required mathematical patches: **none**.

The acceptance covers precisely the theorem and hypotheses in the authenticated PROOF.md. It does not certify optimal ambient dimension, indefinite or nonsmooth generalizations, boundary cases, probability-model realizations, complete targets, globally convex targets, or a globally injective gradient coordinate map. It does not turn finite tests into a computer-verified proof.

An optional source clarification is included separately in `CITATION_SCOPE_NOTE.md`: cite Amari's primary torsion-and-curvature-free definition when explaining the original question's scope. It strengthens documentation but changes no mathematical step and is not a condition of this PASS. The original proof and author manifest were not edited.

The source-free audit files, exact author bindings, source hashes, and test artifacts are frozen by this packet's `MANIFEST.json`. Its SHA-256 must be supplied independently to `verify_audit.py`; the manifest cannot authenticate itself.
