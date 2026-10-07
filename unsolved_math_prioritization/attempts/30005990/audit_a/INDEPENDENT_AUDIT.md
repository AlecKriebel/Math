# Independent mathematical audit of the boundary frequency lift

Problem 30005990, OWR-14298587-002. Audit date: 2026-10-07 UTC.

## Verdict and scope

The dimension-lift argument establishes a sharp theorem for the homogeneous half-space minimizer class B_gamma: for d >= 3 there is no degree in (2,5/2); degree 5/2 is realized when N >= 3; and every degree-5/2 member is a positive common multiple of t times the planar three-sector Y profile in tangential variables. It also establishes the universal spectral lower bound whenever the imported boundary blow-up theorem applies.

This is not a proof of realization by a global minimizer of the unrestricted sum of first Dirichlet eigenvalues on a bounded smooth domain. A local homogeneous energy minimizer need not, merely by its definition, occur as a tangent of such a spectral optimizer. The original spectral attainment assertion therefore remains unresolved by this argument. Likewise, the audit does not certify boundary blow-up uniqueness or regularity near actual frequency-5/2 spectral points.

The reviewed PROOF.md is the frozen 17,776-byte file with SHA-256 d78e4612f31f16b3be6a735ca2a0c1417483bdbe18f548d0d9ae52cb16909c34. Source records are identified in AUDIT_MANIFEST.json. This report is limited to the lift theorem and its stated consequences. The separate REALIZATION_AUDIT.md checks the four additional realization routes on their own frozen bytes.

## Review of the analytic argument

### The source class and the quantifiers

The definition of B_gamma in PROOF.md has the necessary nonnegativity, segregation, local H^1 integrability up to the flat boundary, zero flat trace, homogeneity, and minimization against full-trace competitors on half-balls. These are the requirements in Ognibene-Velichkov's boundary paper, Definition 4.3. Interior compactly supported variations give both distributional inequalities, rather than only harmonicity inside positivity sets.

Attainment requires N >= 3. The exclusion is valid for every finite N, but the statement that 5/2 is the first higher degree must either allow N to vary or fix N >= 3. In particular, a two-component system does not attain this three-component equality case. This precision was requested during review and is present in the frozen statement.

### Finite energy of the lift

Use x in R^(d-1), y in R^3, t=|y|, and V(x,y)=U(x,t)/t. A cutoff of U supported in a larger half-ball has zero flat trace. The one-dimensional Hardy inequality applied on vertical lines proves that U/t is square-integrable on each smaller half-ball. There is no requirement that U already have a classical normal derivative.

Polar integration gives

    integral |V|^2 = 4 pi integral |U|^2,
    integral |grad V|^2
      = 4 pi integral (|grad_x U|^2 + |partial_t U-U/t|^2).

The integrals on the right are with respect to dx dt on the original half-ball. Thus the proposed lift genuinely has finite unweighted H^1 energy in dimension d+2. Both the three radial variables and the division by t are essential.

The argument then verifies weak differentiation across A={y=0}, rather than assigning an arbitrary classical value there and assuming removability. A cutoff at radial scale epsilon has gradient squared integral O(epsilon) on every fixed compact cylinder. Cauchy-Schwarz applied to V times the cutoff gradient shows that the weak integration-by-parts error vanishes. The proposed off-axis derivatives therefore are the global weak derivatives. Nonnegativity and segregation persist almost everywhere.

### Distributional signs and the Jacobian

For a scalar component or signed component combination h, average an off-axis test phi over the radial sphere, obtaining a(x,t). The averaging preserves nonnegativity and compact support away from t=0. The lifted pairing is

    integral grad(h/t)(x,|y|) dot grad phi(x,y)
      = 4 pi integral t^2 grad(h/t) dot grad a.

The right comparison test for the original inequality is t a. The identity

    grad h dot grad(t a) - t^2 grad(h/t) dot grad a
      = partial_t(h a)

has the stated sign and no missing radial Jacobian. Its total derivative integrates to zero because the test is off the flat boundary. This proves the exact original sign for each of the two families of inequalities. The argument does not replace a signed combination by an unsigned component or assume that its Laplacian is positive.

For an arbitrary nonnegative test, multiply by the same axis cutoff. The residual pairing is bounded by the local L^2 norm of grad V times O(sqrt(epsilon)), and tends to zero. This applies separately to all signed combinations. Thus V belongs to the full interior S class on all of R^(d+2); an axis-supported defect distribution is not left unexamined. A codimension-one reflection or a merely formal off-axis Laplacian calculation would not establish this step.

### Origin and frequency

The lift is nonzero and has homogeneity beta=gamma-1. Interior regularity gives a locally Lipschitz representative. For gamma>2, beta>1, so continuity and homogeneity force V(0)=0.

The free-boundary condition can also be checked directly: choose a point where one component is positive; homogeneity supplies positive points in that component arbitrarily near the origin, whereas its value at the origin is zero. Thus the origin is on the boundary of a positivity set. The interior frequency theorem is being applied at a legitimate free-interface point. It is not being applied at a point with positive value, where the frequency would instead be zero.

The homogeneous energy identity for the S class yields N(V,0,r)=beta. It follows either from its usual radial identity or by testing the component equations with cutoffs of the components, which vanish on the support of the component Laplacian measures. The zero trace and harmonicity-on-positive-sets structure are what permit this identity; homogeneity alone for a general H^1 map would not suffice.

The imported interior alternative beta=1 or beta>=3/2 now excludes 1<beta<3/2. This is exactly gamma>=5/2 under gamma>2. No gap estimate depending on the number of components is required.

### Equality and tangential orientation

The imported equality classification applies to the exact class already proved, and identifies the lift as a planar Y configuration. The proof then uses an additional fact specific to this construction: the vector-valued lift itself is invariant under every rotation of the y variables. This is stronger than invariance up to relabeling and follows directly from its definition.

The singular spine of a planar Y configuration is exactly the orthogonal complement of its active two-plane. It is intrinsically characterized by the triple singularity, so the rotations preserve it and the active plane. For the orthogonal projector Q onto that plane, commutation with diag(I,R), R in SO(3), forces zero mixed blocks. Its three-by-three radial block must be a scalar multiple of the identity. Since Q is a projection of rank two, this scalar is zero. Consequently the active plane is wholly tangential.

This rules out an unnoticed tilted or partially radial equality model. It also shows why the equality construction needs at least two tangential dimensions, hence d>=3. Equal amplitudes of the three nonzero components are inherited from the interior classification; arbitrary separate amplitudes are not admitted.

### Attainment and competitors touching the flat boundary

The shifted-sine definition of Y in the candidate is nonnegative on all three sectors. The normal derivative magnitudes agree on each common ray. Hence the individual zero extensions have positive Laplacian measures, while the prescribed signed combinations have nonpositive Laplacians. The origin contributes no atom because the flux on a circle of radius rho is O(rho^(3/2)). Multiplication by t preserves these signs inside the half-space. This verifies U=tY in S(H_d,N).

Wang-Zhang supplies interior energy minimality. The candidate correctly does additional work to pass from that statement to full-trace half-ball minimality. Let W have the same full trace as U. Then W-U is in H^1_0 of the half-ball; its zero extension satisfies Hardy, so |W-U|^2/t^2 is integrable.

The interpolation must take place along the intrinsic star-tree geodesic. Ordinary vector averaging of two different phases would violate segregation. For clarity, that geodesic has the explicit component formula

    G_s(a,b)_i = [(1-s)a_i - s sum_(j!=i)b_j]_+
                 + [s b_i - (1-s)sum_(j!=i)a_j]_+.

For star-valued a,b this formula stays on the same star. It is Lipschitz in its endpoint data for fixed s. Its parameter speed is the intrinsic distance, which is at most sqrt(2)|a-b|. These facts justify the candidate's Sobolev chain-rule estimate for a height-dependent parameter.

The interpolation equals U below epsilon and W above 2epsilon. Its transition error is controlled by the integral of |W-U|^2/t^2 on the shrinking strip, which tends to zero. The two ordinary gradient terms also tend to zero there. It therefore converges strongly to W in H^1. On the truncated half-ball with t>epsilon/2 it has exactly U's trace on the whole boundary, and this truncated domain is relatively compact in the open half-space. Applying interior minimality and taking the strong limit proves the exact boundary comparison required by B_gamma.

This is sufficient attainment in B_(5/2). It does not supply the missing global spectral realization.

## Source verification

The following primary statements were checked in the source PDFs or their full text:

- Ognibene-Velichkov, arXiv:2404.05698v1, Definition 4.3 and Proposition 6.13: the half-space comparison class and normalized homogeneous boundary limits. Assumption 2.1 covers C^(1,alpha), alpha>0. Its stated regularity assumptions must be retained.
- Ognibene-Velichkov, arXiv:2412.00781v5, Section 2, Theorems 2.1 and 2.4, Proposition 3.5: the S class, interior regularity and gap, and the degree-3/2 equality classification. Theorem 2.4 was also inspected as a rendered PDF page. Its gap is used only at the origin's verified zero/free-interface point.
- Wang-Zhang, 2010, Theorem 1.6 and Section 6: solutions of the segregated distributional system minimize energy. The original PDF was independently retrieved and its printed page 741 visually inspected, including the defining inequalities. This corroborates the S=M statement in the 2026 paper.
- The original Oberwolfach report, printed page 2122: the notation mixes the additive expression 2+delta_d with a proposed endpoint 5/2. The sound numerical statement is first higher degree 5/2, additive separation 1/2.

Primary links and source hashes are recorded in AUDIT_MANIFEST.json. Third-party PDF contents and rendered pages are not included in the source-free audit deliverables. This audit relies on the cited analytic theorems; it does not reprove the entire source literature or certify originality or priority.

## Independent controls and limitations

Run `python3 -I -B audit_math.py`. The exact finite checks cover 49 monomial lift identities, 168 nonzero wrong-radial-dimension controls, 3125 weak-test identities, 100 intrinsic/Euclidean metric comparisons, 2500 geodesic speed checks, and 50000 endpoint-convexity checks. An ordinary Euclidean interpolation is explicitly rejected for mixing two phases. The recorded run passes.

These controls test algebra and the proposed interpolation model only. They do not prove Hardy's inequality, removability, Sobolev approximation, the imported frequency theorem, or global spectral realization. The mathematical acceptance rests on the analytic review above.

## Acceptance decision

Accept the stated sharp B_gamma theorem and the conditional-on-source-hypotheses universal spectral lower bound in the frozen bytes, which include the N>=3 precision. No corrective mathematical patch is otherwise required. Retain an unresolved disposition for the original target if it requires actual attainment by a bounded-domain global spectral optimizer. Do not infer this missing assertion from the word "blow-up class" alone.
