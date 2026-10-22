# Independent audit of problem 30003533

Audit date: 8 October 2026. Problem: OWR-15576-002, queue rank 1000.

## Decision

Accept the five scoped auxiliary mathematical developments, subject to the narrow wording correction below. No theorem or displayed estimate requires repair. Do not accept this work as a solution of the source problem, a smooth counterexample, or a new high-frequency coercivity theorem. The appropriate research disposition remains **unsolved, 5/5**.

The frozen packet has two reproducibility/validation defects: its self-test cannot mutate copies of a read-only source packet, and its ledger ordinal comparison accepts a Boolean as the integer 1 after hashes are rebound. The supplied correction fixes both and adds a regression case. All corrected checks pass in ordinary Python, `-O`, and `-OO`, including genuinely read-only relocation under the unprivileged agent account.

This audit read all of PROOFS.md and the packet's claims, ledger, summaries, sources, manifest and scripts. It independently reconstructed the mathematical arguments and used a separate control program that imports none of the author's Python modules. It did not reprove the cited published PDE theorems or conduct a comprehensive present-day literature search.

## Frozen identity and scope

- Original manifest SHA-256: `2ed09ec9ba1d31bb913b84c6e63f3256394744c7635817ec2a1467cbcb124ec0`.
- Original PROOFS.md SHA-256: `331a6b124d492566d29977cd6d2ac47ef58b8dab89f8c9ce979e431188bf548a`.
- The original 13-file packet remains byte-for-byte unchanged, with its original file modes.
- The corrected manifest reproduced by CORRECTIONS.patch has SHA-256 `10e904a94ffabba520bd60ebbfb27f0dd41eb0d248f49eb7680ed0dd7e6aaf94`.
- The corrected proof differs only in the sufficient-versus-necessary wording following Proposition 3.1. All propositions, calculations, source qualifications and unresolved gaps remain intact.

The mathematical target is the modulus of the diagonal quadratic form of

A_k = (1/2)I + D'_k - i k eta S_k

on complex L2(Gamma, ds), with the normal pointing into the exterior and eta > 0 fixed before k varies. The required polynomial interpretation fixes Gamma and eta first, then asks for c > 0, alpha >= 0, and k0 with beta(k) >= c k^(-alpha) for **every real** k >= k0. Constants may depend on that fixed geometry and coupling. An inf-sup estimate, a bounded inverse, a modified equation, a discrete compression, or a subsequence lower bound does not establish this assertion.

## Source and formulation audit

The source citation is correct: Smyshlyaev's contribution is in Material Theories, OWR 33/2017. Equation (2) specifies the primed double layer and coupling k eta; equation (3) specifies modulus coercivity. The p. 2085 display has a frequency still free on the right after taking a liminf, and an introduced constant is unused. Visual inspection confirms this is in the source, rather than an extraction error. The packet's property (P) is a clearly identified repair, supported by the preceding prose, not a literal theorem statement from the report. The report's informal “strongly non-trapping” label does not provide a full geometric definition. The packet appropriately singles out a smooth strictly-star-shaped core without claiming to define the entire intended class. [Official report](https://ems.press/content/serial-article-files/46698?nt=1).

The known convex result has explicit C3, piecewise analytic and strictly positive curvature assumptions, and a sufficiently large coupling coefficient proportional to k. The packet preserves these restrictions. The published constant-normal-multiplier obstruction already exists; no novelty claim is justified for reconstructing or extending that elementary boundary calculation. [Author preprint, Theorem 1.2 and Lemma 5.1](https://people.bath.ac.uk/eas25/SpKaSm13.pdf).

The smooth nontrapping example in Section 6.3.2 gives beta(k) <= C/k along k = m pi/a, under a coupling bounded by a constant times k. Its nontrapping definition uses uniform escape of generalized billiard trajectories. This defeats a frequency-uniform positive lower bound on the wider class but is compatible with a polynomial lower bound with exponent at least one along that sequence. The text expressly leaves fixed-frequency coercivity possible. It does not refute (P). [v5 paper, Definition 1.3 and Section 6.3.2](https://arxiv.org/pdf/1708.08415v5).

The star-shaped open-book examples are Lipschitz polyhedra, and Corollary 1.6 concerns the same standard Helmholtz formulations. Their failure for all positive frequencies is not a smooth counterexample. The correction changes localization statements and proof passages, including one passage used for Theorem 1.3, but does not withdraw Corollary 1.6. This audit confirms those statements, without claiming an independent reconstruction of the polyhedral construction. [2022 article](https://centaur.reading.ac.uk/101202/8/Chandler-Wilde-Spence2021_Article_CoercivityEssentialNormsAndThe.pdf), [correction](https://www.personal.reading.ac.uk/~sms03snc/GCC.pdf).

Seven local PDF hashes and byte counts match the supplied public metadata. Five sources were substantively inspected for this audit; the older parabolic version and the 2026 survey received hash/size checks only here. SOURCE_CHECKS.json specifies the exact distinction. No source PDFs, extracted source text, dataset contents or private coordination files are included in the audit deliverables.

## Approach 1: variable-weight normal multiplier

### Proposition 1.1: accepted

For a boundary curve with unit tangent xi, differentiating Z = a n yields D_xi Z = (D_xi a)n + a D_xi n. Orthogonality xi dot n = 0 removes the weight derivative exactly. The quadratic form of DZ equals that of its symmetric part. A tangential value -a kappa with a >= a0 gives a least eigenvalue at most -a0 kappa. Continuity up to the boundary contradicts any adjacent-open-region lower bound -epsilon I with epsilon < a0 kappa. C2 boundary and C1 traces are enough for this calculation. No assumption about a normal derivative of a is needed.

This only obstructs positive scalar normal boundary multipliers with the stated pointwise derivative sign. It does not prohibit tangential components, nonlocal multipliers, or integrated compensation. A frequency-dependent weight tending to zero defeats the fixed numerical obstruction but also loses the boundary weight; the packet correctly leaves that separate estimate open.

### Proposition 1.2 and geometry control: accepted

The positive radial graph r = 1 + cos(3 theta)/4 is embedded and regular. Since r >= 3/4 and |r'| <= 3/4, its support quotient is at least 9/(4 sqrt(34)), strictly larger than 3/8. The ball of radius 3/8 lies inside the radial interior. A line segment from any point of that ball can cross the boundary only in the outward direction, because (x-z) dot n > 0. Thus a segment ending inside cannot have exited earlier; this supplies the claimed ball-star-shapedness.

Direct coefficient expansion gives r^2 + 2(r')^2 - r r'' = 17/8 + (11/4)c - c^2/2. At c = -1 this is -9/8 and the denominator is 27/64, so the outward curvature convention in the packet gives -8/3. The sign proves nonconvexity. The facing-patch inequality forces a putative star center simultaneously to have first coordinate below a1 and above a2. That local obstruction correctly prevents relabeling the cited smooth example as strictly star-shaped.

No high-frequency conclusion about this explicit curve is proved or computationally certified.

## Approach 2: geometric perturbation

### Proposition 2.1: accepted in dimension three under its stated family assumptions

The surface-area Radon-Nikodym factor J_t makes U_t unitary. Substituting U_t and its inverse into the integral operator gives one square-root Jacobian at each endpoint, not a full Jacobian at one endpoint. Uniform C2 control and metric nondegeneracy give common coordinate radii with r_t comparable to the reference separation rho. Compactness of the parameter interval and injectivity of each embedding give a positive minimum separation off the diagonal neighborhood. Close nonlocal sheets therefore do not invalidate the argument for this fixed family, although its constant may be large.

The decisive estimate for the double layer is both a_t = O(rho^2) and partial_t a_t = O(rho^2). Differentiating n_t dot DX_t = 0 cancels the possible linear term in the latter. C1 dependence in C2 supplies the required uniform second-coordinate-derivative remainders and time derivatives of the normals and Jacobians.

Writing F_k(r) = exp(i k r)(i k r - 1)/r^3 gives

F'_k(r) = exp(i k r)(-k^2/r^2 - 3 i k/r^3 + 3/r^4).

Together with partial_t r = O(rho), multiplying by a = O(rho^2) bounds this derivative contribution by C(k^2 rho + k + rho^(-1)). The a and Jacobian derivative terms obey the same bound. The single-layer derivative is bounded by C(rho^(-1) + k), so multiplication by k eta contributes C(k rho^(-1) + k^2). This proves the stated integrable envelope with frequency factor 1 + k^2.

Both Schur integrals are uniform: the same symmetric reference separation controls rows and columns, and a two-dimensional surface integrates rho^(-1) with radial area element rho d rho. Differentiation and integration are justified by this common envelope for each finite k; integration in t followed by Schur yields Ct(1+k^2). The separate half-identity is unchanged, and the weakly singular kernel does not conceal another jump distribution.

### Corollary 2.2: accepted

The diagonal-modulus infimum is 1-Lipschitz in operator norm, by the pointwise reverse triangle inequality and taking infima in both directions. The resulting neighborhood t = O(k^(-2)) is a sufficient frequency-dependent neighborhood. It proves nothing at a fixed nonzero deformation for arbitrarily high k. Uniform convexity itself is open in the C2 topology, so the packet correctly declines to infer a nonconvex example from this estimate.

## Approach 3: weighted forms and inverse bounds

### Propositions 3.1 and 3.2: accepted; one following sentence requires clarification

The identity lambda(A v,v) = (P A v,v) - ((P-lambda I)A v,v) is valid with the stated complex inner product. Cauchy-Schwarz bounds the defect by delta ||A|| ||v||^2. Taking real parts proves the displayed sufficient transfer bound. Replacing A by a phase multiple changes no norm estimate.

The matrix product P A = [[1,1],[-1,1]] has Hermitian part I on complex C2, not merely on real vectors. P has positive principal minors and eigenvalues 2 +/- sqrt(2). The vector (1,-1) gives exactly zero original quadratic form, while the supplied inverse is exact. A constant frequency family therefore has every claimed uniform bound while beta is zero.

The sentence “transfers only if this sufficient condition ... is verified” can be read as falsely asserting necessity. For A = I, P = diag(1,3), c = 1 and lambda = 2, delta = 1 and c = delta ||A||, but A has coercivity 1. The replacement says the criterion is sufficient, not necessary. This does not change Proposition 3.1 or the obstruction established by Proposition 3.2.

## Approach 4: finite escape model

### Propositions 4.1 and 4.3 and Corollary 4.2: accepted

For a contraction, I-T* T is positive and has the stated positive square root. The sum defining V telescopes exactly to ||v||^2 because T^N = 0; the last coordinate in VT = LV is zero for the same reason. Thus T is compressed from the finite backward shift on H-valued coordinates. The sine vectors diagonalize its scalar Hermitian part, including the endpoint case N = 1. Tensoring the finite change of coordinates with the identity on H is legitimate even in infinite dimension. This yields the sharp real-part gap, and subtraction of an arbitrary remainder of norm epsilon is justified.

The chord bound gives 1-cos(pi/(N+1)) >= 2/(N+1)^2. Including the factor 1/2 in A and the assumed error leaves at least 1/[2(N+1)^2], hence the claimed 1/(2 C^2) frequency bound. All step and error estimates must hold for every sufficiently large real frequency to imply (P).

For the finite shift, diagonal unitary conjugation supplies all rotations, while the top Hermitian eigenvalue supplies the radius. Convexity of numerical range then gives the full disk, including N = 1 where it degenerates to a point. T = 2L in dimension two has zero cycles algebraically but lacks the required contraction, and (1,1) yields the advertised zero form. This is an abstract countermodel, not a boundary-scattering construction.

No representation of the actual operator as the required contraction plus small remainder has been furnished. Nontrapping alone has not supplied its norm, glancing control, finite-step property or remainder size.

## Approach 5: finite blocks and compact tails

### Fixed-frequency compactness and Propositions 5.1-5.3: accepted

On a compact C2 surface in dimension three the normal numerator vanishes quadratically, leaving at worst the integrable inverse-distance kernel at fixed k. The two-dimensional logarithmic bound is also integrable. Cutting out a small diagonal strip gives bounded kernels and hence Hilbert-Schmidt operators; the Schur norm of the removed strip tends to zero with the stated rates. This proves compactness separately at each frequency, not a uniform approximation rate.

For the Hermitian rotated form, the two off-diagonal terms are conjugates. Their sum is bounded below by -2 b ||x|| ||y||. The smaller eigenvalue of the scalar 2-by-2 comparison matrix is exactly the displayed lambda, and a,d > 0 with ad > b^2 makes it positive. The proposed tail value follows by norm domination of the compact part.

Strong convergence of the complementary projections is uniform on compact sets by a finite net argument. Applying it to the images of the unit ball under K and K* proves both one-sided norm limits, hence also the cross block and tail limits. In infinite dimension the complementary spaces are nonzero at every finite stage, so unit tail vectors show gamma <= cos(theta)/2. Consequently the chosen tail lower bound is eventually at least gamma/2 and the determinant condition eventually holds. In finite dimension the eventual full projection removes the tail.

The assumption of a fixed-frequency positive rotated form is essential to that argument. For context, if beta(A) > 0, separation of the closed convex numerical range from zero gives a suitable phase at that fixed frequency. This observation supplies no lower bound in frequency and no uniform finite truncation index.

The rank-one family has eigenvalues exp(-k) and 1/2, so its diagonal-modulus minimum is exactly exp(-k) for k >= 1. Choosing an integer m > alpha and using exp(k) >= k^m/m! proves k^alpha exp(-k) -> 0. The model is invertible at every frequency but its inverse is not uniformly bounded. The packet explicitly distinguishes that fact from the separate uniformly-invertible matrix countermodel.

## Validation defects and supplied correction

1. **Read-only self-test failure.** The original source files are mode 0444 and its directory mode 0555. copytree preserves these modes in temporary mutation copies. The first write to the copied proof raises PermissionError in each Python mode. The repair makes only disposable mutation copies writable. It never alters the source's permissions. The separate read-only test is retained.
2. **Boolean ledger ordinal.** Python compares True equal to 1. The original list comparison therefore accepts a hash-rebound first attempt with turn=true in all three modes. The repair checks each attempt is a dictionary and its ordinal has exact type int before comparison, then adds this adversarial regression case. The trust-root caveat still applies: no local script is secure if both its own code and every externally trusted digest are replaced.
3. **Sufficient-versus-necessary wording.** Only the paragraph after Proposition 3.1 changes; the proof and formula do not.

CORRECTIONS.patch also updates VALIDATION.md and rebinds the changed file hashes in MANIFEST.json. It was applied independently with the patch utility to a second clean copy and reproduced every corrected byte and the expected manifest hash. The patched author's historical “independent review pending” flags remain part of its original author metadata; ACCEPTANCE.json is the separate independent review record.

## Independent control results and limitations

VALIDATION_RECEIPT.json records the observed outcomes:

- Original author verifier: 4,455 exact finite controls, passing normal, -O and -OO.
- Independent program: 4,658 exact checks, 2,144 explicitly numerical checks and 69 integrity/schema checks, passing all three modes. The exact portion uses rational coefficient identities and Gaussian-rational complex vectors. The numerical portion checks finite sine-eigenvector formulas and is not called an exact certificate.
- Independent malformed/adversarial cases: 23 cases, each rejected in three modes, totaling 69 rejections. Relevant semantic payloads and their manifests were deliberately rebound, so those rejections do not merely reflect stale file hashes.
- Unmodified original relocation: independent checks pass in all three modes on read-only files in a nonwritable directory.
- Corrected author self-test: invoked under all three modes, each invocation reports six successful original/relocated replays and 39 rejections covering 13 mutation cases. The corrected packet itself was read-only throughout these runs.
- Corrected independent checks: three further successful mode runs; read-only bytes and modes unchanged.
- Original source packet: final byte/mode snapshot matches the initial snapshot exactly.

The controls test finite algebra, kernel-geometry jets, schema and reproducibility. They do not discretize the boundary operator on the polar example, prove a PDE bound, certify all smooth deformations, or establish a frequency-uniform tail estimate. The mathematical acceptance rests on the written arguments audited above; the controls supplement it.

## Final acceptance boundary

Retain: the variable-weight obstruction and explicit star-shaped curve; the three-dimensional family perturbation estimate; the sufficient near-scalar transfer and positive-metric countermodel; the sharp nilpotent-contraction model bound and acyclicity obstruction; and the block/tail certificate with its fixed-frequency and superpolynomial-rate limitations.

Do not promote: any of these models to a solution of the original strongly-nontrapping question; the smooth O(1/k) upper bound to a polynomial-loss refutation; the nonsmooth open-book theorem to a smooth theorem; or passing finite controls to formal verification. No new substantive research turn is charged for this audit or its corrections. **Unsolved, 5/5 remains the justified disposition.**
