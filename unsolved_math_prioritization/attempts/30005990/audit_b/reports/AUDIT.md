# Second independent audit: boundary frequency and realization routes

Date: 2026-10-07 (UTC).

## Verdict

**Accept as a mathematically sound strong partial result. The full bounded-domain spectral attainment problem remains unsolved.** I found no theorem-level gap requiring a correction in either frozen manuscript. The radial lift proves the claimed sharp homogeneity threshold and rigidity in the precise half-space minimizing class. Each of the four supplementary routes proves only the more limited result explicitly stated in that route. None supplies the missing globally sum-minimizing spectral partition on a bounded domain with the required boundary regularity.

This verdict is independent: I did not read the other audit, the original audit directory, or the packet's checking scripts. I read both requested manuscripts in full, independently inspected the relevant primary PDFs, and wrote separate controls. No original manuscript was edited. No external publication or repository change was made.

The only proposed textual changes are optional clarifications: an explicit component formula for the tree interpolation and an explicit almost-everywhere/piecewise interpretation of the gradient remainder in the Bessel construction. Neither changes the accepted result. They are supplied separately, not silently applied.

### Frozen inputs

- PROOF.md: 17,776 bytes; SHA-256 d78e4612f31f16b3be6a735ca2a0c1417483bdbe18f548d0d9ae52cb16909c34.
- REALIZATION_APPROACHES.md: 18,644 bytes; SHA-256 eb2502b48d0781a2ab70e6ed023696875f889a33ce95ac08cf7fffff75409b0b.

Independent controls: 16 passed. These controls check algebra, examples, and deliberate failure cases; they are not substitutes for the analytic arguments below and are not a novelty certificate.

## 1. Exact source imports and scope

### Interior class and classification

The inspected primary source is Ognibene–Velichkov, *Structure of the free interfaces near triple junction singularities in harmonic maps and optimal partition problems*, arXiv:2412.00781v5. Its PDF cover identifies v5, dated 7 September 2026. The current arXiv listing independently confirms that version/date and the journal reference, *Archive for Rational Mechanics and Analysis* 250, 77 (2026).

- PDF p.5 defines S using the same nonnegative, segregated H1-local class and the same two distributional inequalities as PROOF.md. It explicitly identifies S with the local energy-minimizer class M and attributes the converse to Wang–Zhang Theorem 1.6.
- PDF p.6, Theorem 2.1, supplies local Lipschitz continuity. Section 2.2 supplies the frequency framework.
- PDF p.7, Theorem 2.4, supplies the gap between 1 and 3/2 at nodal points. The manuscript uses it only at a zero of a nontrivial map, avoiding any ambiguity in the source's displayed quantifier.
- PDF pp.10–11, Proposition 3.5, supplies the full classification of global 3/2-homogeneous members of S, including exactly three nonzero components and a common multiplier.
- PDF p.11, Corollary 3.6, is the three-cell maximum-eigenvalue theorem on the sphere, not a sum-eigenvalue theorem. PDF pp.4–5 explicitly distinguish the p=1 conjecture from the proved p=infinity case.

I independently extracted these pages from the actual PDF and visually inspected p.11; the audit does not rely on the packet's SOURCE_AUDIT.md.

### S=M and its use near the fixed boundary

Wang–Zhang, *Some new results in competing systems with many species*, Annales IHP AN 27 (2010), has the required system (1.3), Theorem 1.6, and the accompanying energy-minimality discussion on printed p.741 (PDF p.3). Section 6 begins on printed p.753 (PDF p.15) and uses geodesic interpolation. The source's local formulation is the one needed here. The packet does not infer fixed-boundary minimality merely by invoking this theorem: it supplies a separate approximation argument to allow competitors reaching the flat boundary. That distinction is essential and correctly handled.

### Boundary blow-up import

Ognibene–Velichkov, *Boundary regularity of the free interface in spectral optimal partition problems*, arXiv:2404.05698v1, supplies:

- Assumption 2.1 on PDF p.4: the quantitative boundary hypotheses, explicitly including C1,alpha domains for alpha>0.
- Definition 4.3 on PDF p.14: homogeneous, segregated half-space maps with zero flat boundary values and energy minimality on half-balls for the full trace.
- Proposition 6.13 on PDF pp.36–37: normalized nonzero homogeneous limits in that class.

PROOF.md uses the same half-ball competitor class, expressed in Sobolev-trace language. It retains the quantitative boundary hypotheses and does not assert the blow-up theorem on every merely C1 domain. Its conclusion concerning spectral optimizers is therefore a valid consequence of the stated source theorem.

### Original problem and notation

I visually inspected the original Oberwolfach PDF's printed p.2122. It really places an additive parameter inside [2+delta_d,infinity) and then prints a conjectural value 5/2 for that same parameter. The manuscript correctly separates the threshold 5/2 from its additive distance 1/2 above 2. This is an actual notation inconsistency in the source, not a transcription issue introduced by the manuscript.

A sharp threshold in the half-space cone class does not prove that the set of actual bounded-domain spectral frequencies has that same least value. The manuscript preserves this distinction. Under the strict spectral reading specified for this audit, global attainment remains a required open obligation.

### Public references and verification limits

- https://arxiv.org/abs/2412.00781v5
- https://arxiv.org/abs/2412.00781
- https://arxiv.org/abs/2404.05698v1
- https://doi.org/10.1016/j.anihpc.2009.11.004
- https://doi.org/10.4171/OWR/2024/37
- https://dlmf.nist.gov/10.2
- https://dlmf.nist.gov/10.21

The exact v5 arXiv URL and DOI resolver calls did not all fetch through the web tool; the unversioned current arXiv listing did fetch and identifies v5. The detailed theorem inspection used the local primary PDFs, with independently verified file hashes and PDF extraction. I do not claim to have independently redownloaded every PDF or certified historical novelty. DLMF's differential equation, series, and positive-zero statements were checked online.

## 2. Radial lifting: H1 and axis removability

Write n=d+2 and t=|y| with y in R3. The choice of three radial coordinates is forced by the differential identity, rather than arbitrary. With k radial coordinates one obtains

    Delta_(x,y)(U/t) - Delta_(x,t)U/t
        = (k-3)(U_t/t^2 - U/t^3).

Thus k=3 is exactly the value removing the additional lower-order terms.

The potentially dangerous point is the axis y=0. PROOF.md does not skip it:

1. Localize U by a smooth cutoff with compact support in a larger half-ball. Its zero flat trace allows zero extension across the plane.
2. The one-dimensional Hardy inequality on vertical lines gives local integrability of U/t squared in the unweighted half-space measure.
3. Polar integration yields precisely the two displayed identities (2.3), including the 4*pi factor. In particular, the lifted gradient is controlled by grad_x U and U_t-U/t, not by an unjustified pointwise quotient estimate.
4. The radial cutoff chi_epsilon has squared gradient integral O(epsilon) on bounded cylinders. The weak-derivative error term is controlled by the product of this vanishing norm and the local L2 norm of V. The off-axis derivative therefore extends across the axis without an additional distribution.

All integrations are local; the support cutoff avoids any issue at spatial infinity or at the curved boundary of the larger half-ball. The initial almost-everywhere definition at y=0 is harmless because that set is null. The claimed H1-local regularity is established before a PDE is asserted across the axis.

Independent negative control: removing the zero-trace hypothesis permits U=1. The lifted function is 1/|y|, harmonic away from the axis, but its normal flux is -4*pi and its gradient energy diverges at the axis. This produces exactly the kind of hidden axis distribution that a merely formal computation would miss. The hypotheses and Hardy step in the submitted proof exclude it.

## 3. Distributional inequalities and frequency transfer

The weak transfer identity has the correct sign and weight. For a nonnegative smooth test away from the axis, its spherical average a is nonnegative. The half-space test is t*a, also nonnegative. Direct expansion gives

    grad h dot grad(t a) - t^2 grad(h/t) dot grad a = partial_t(h a).

The integral of the right-hand side vanishes because the test is supported away from both t=0 and infinity. This applies to each component and to each signed combination h=U_i-sum_(j!=i) U_j. Therefore both required inequalities, not merely positivity-set harmonicity, transfer off the axis.

For arbitrary tests the chi_epsilon cutoff again has vanishing H1 seminorm. Cauchy–Schwarz with the established L2 gradient of each lifted combination makes the error vanish. Lipschitz nonnegative tests can be approximated within the off-axis open set. Hence V belongs to exactly S(R^(d+2),N).

The degree drops by one: beta=gamma-1. The imported local Lipschitz representative is compatible with the almost-everywhere homogeneity, which then holds everywhere by continuity. For gamma>2, beta>1 and V(0)=0. The homogeneous energy identity gives the frequency beta, and the imported interior gap yields beta>=3/2. Thus gamma>=5/2.

No S=M inference is needed for the exclusion or equality classification; the class-S theorems suffice. This is correctly stated in the manuscript. Applying the boundary blow-up theorem then transfers the exclusion to the specified global spectral optimizers, without assuming realization of the equality case.

## 4. Equality, SO(3), and sharp half-ball minimality

### Equality orientation

At beta=3/2 the imported classification gives a Y profile on a two-dimensional plane E. Its triple-junction spine is exactly E-perpendicular. The actual lifted map is invariant under all rotations of its R3 radial coordinates. Its singular spine is therefore invariant, and so is E.

The projection Q onto E commutes with diag(I,R) for every R in SO(3). In block form, its off-diagonal block is zero because SO(3) has no fixed nonzero vector; its radial block is a scalar identity because a symmetric matrix commuting with every rotation has a constant quadratic form on the sphere. Idempotence makes that scalar either zero or one. The second case would have rank at least three, contradicting rank Q=2. Thus E is entirely tangential.

This proves precisely U=t*cY(Px), not just a rotated profile in the enlarged space. It also explains the restrictions d>=3 and N>=3 for equality. A different multiplier for each component is not permissible: the signed distributional inequalities on the common rays force adjacent flux magnitudes to match.

### Membership in S for the explicit Y profile

The shifted-sine convention in Section 6 is positive on all three chosen sectors. The positive pieces are harmonic. Their zero extensions have positive Laplacian interface measures, and the signed combinations have either cancellation or a negative sum of those measures. The small-circle flux is O(rho^(3/2)), so no origin atom is hidden. Multiplication by the independent positive coordinate t preserves these signs inside the half-space. Zero additional components also satisfy the required signed inequality.

### The competitor approximation is valid

For an arbitrary full-trace competitor W, W-U is in H1_0 of the half-ball. Its zero extension and Hardy inequality give the weighted estimate needed in the boundary strip. The tree interpolation stays in the segregated target and preserves equality of traces.

An explicit formula makes the chain-rule step entirely transparent. Set hat(a)_i=a_i-sum_(j!=i)a_j. For a,b in Sigma_N,

    G_s(a,b)_i = [(1-s)hat(a)_i+s hat(b)_i]_+.

If a and b lie on the same branch this is ordinary linear interpolation. If they lie on different branches it moves through the vertex with the correct constant speed. Positive-part composition and the bounded linear hat-transform give

    |grad G_eta(U,W)|
      <= C_N (|grad U|+|grad W|+|W-U| |grad eta|).

Consequently the strip energy tends to zero, including the cutoff derivative term, by the weighted Hardy integrability and absolute continuity of the integral. Strong H1 convergence to W follows.

The truncated domain B_R intersect {t>epsilon/2} is a relatively compact Lipschitz subdomain of the half-space. W_epsilon and U have equal traces on its lower face and curved face. Interior minimality applies there, and the two maps coincide below it. Passing to the strong-H1 limit proves the full half-ball comparison inequality. This closes the fixed-boundary issue and establishes membership in the exact B_(5/2) class, rather than only interior stationarity.

## 5. Cartesian and spherical routes

### Cartesian route

The separated energy and eigenvalue formulas are correct. The transverse one-dimensional ground state contributes pi^2/L^2 to each cell. This proves the stated restricted infimum, with no assumption of global tensorization.

Because segregated normalized components are orthonormal, Ky Fan gives E_N(Omega)>=sum_(k=1)^N lambda_k(Omega). Connectedness of Omega implies a simple first eigenvalue and makes the difference from N*lambda_1 strictly positive for N>=2. The slab competitor has sum N*lambda_1+N^3*pi^2/L^2. Subtracting the restricted value gives exactly the threshold (2.4). The slice counterexample correctly diagnoses the missing per-slice normalization.

Independent three-dimensional example: take Omega=(0,1)^2, N=3, L=3. Its first three eigenvalues are 2*pi^2,5*pi^2,5*pi^2. Every Cartesian three-cell partition therefore has sum at least (37/3)*pi^2, while three transverse slabs have sum 9*pi^2. Thus the obstruction does not depend on an unknown exact planar optimal partition.

### Spherical spectral shift

The orbit measure is 4*pi*t^2 times the base hemispherical measure; the induced metric on invariant functions is the hemisphere metric. The ground-state identity for h=t gives the shift with the correct sign:

    lambda_1(omega_tilde) = lambda_1(omega)-(d-1).

The proof first works on compactly supported smooth functions and then uses density. The inverse-density argument is legitimate even for irregular open cells: compact group averaging preserves smoothness, compact support in the invariant domain, and H1 convergence; multiplication by t gives smooth compactly supported base functions. The shift plus the L2 identity controls the full norms in both directions.

The full lifted ground state need not be assumed invariant. Averaging a nonnegative first eigenfunction produces a nonzero invariant eigenfunction at the same eigenvalue, proving equality with the invariant infimum. Compactness on the sphere supplies existence. Zero capacity of the omitted axis is compatible with the H1_0 formulation and creates no additional Dirichlet barrier.

As an independent sign check, the whole hemisphere's ground state t has eigenvalue d-1 and lifts to the constant 1 on the higher sphere, with eigenvalue zero.

The min-max constant after shifting is exactly (5/2)(d+1/2), and tY supplies equality for d>=3. Replacing a disconnected open cell by a component supporting a ground state is legitimate. The source's maximum-eigenvalue theorem is therefore applicable. The manuscript correctly refuses to multiply a maximum lower bound by three to deduce a sum lower bound. The p=1 full-sphere assertion remains conditional, and even it would not certify nonconical Euclidean competitors.

## 6. Thin-cylinder Gamma convergence

The rescaling preserves each L2 norm and segregation, and subtracts N*pi^2/epsilon^2 with the correct coefficient. Every transverse excess is nonnegative. The recovery sequence f_i(x)*sqrt(2)sin(pi*s) is admissible and attains the proposed limiting energy exactly.

For the liminf, the first-mode projection is bounded in H1_0(Omega), and the orthogonal remainder satisfies the sharp transverse gap 3*pi^2. Its L2 norm is O(epsilon). Projection does not preserve segregation at finite epsilon, but the manuscript does not assume that it does. Strong L2 convergence of the original components makes their products converge strongly in L1, and positivity of the first transverse mode recovers segregation in the limit. The limiting norms are exactly one.

Weak lower semicontinuity proves the liminf. Together with recovery and compactness this gives the stated Gamma convergence in the fixed strong-L2 space, including the value limit and subsequential convergence of minimizers. The infinite values outside the normalized segregated class cause no missing case: finite liminf supplies a bounded-energy subsequence; an infinite limiting functional has a vacuous recovery upper bound.

Independent alternative compactness check: the energy bound gives a uniform tangential gradient bound and

    sum_i ||partial_s w_i||_2^2 <= N*pi^2+C*epsilon^2.

Thus the entire tuple is uniformly H1-bounded on the fixed cylinder. Rellich gives strong L2 compactness directly, while the vanishing transverse excess forces the limiting tuple into the first transverse eigenspace. This independently confirms the global, not merely mode-by-mode, compactness assertion.

A useful negative control uses two segregated functions occupying opposite half-intervals in s. Their first-mode projections are both positive multiples of the same tangential function, so projected segregation fails. Their excess energy diverges at order epsilon^-2, however, and they cannot contradict the bounded-energy theorem.

Nothing in this convergence establishes persistence of a boundary triple stratum or its precise frequency at positive thickness. Edges and boundary smoothing are additional obstacles. These limits are explicitly respected in Section 4.4.

## 7. Bessel stationary candidate

Set q=(d-2)/2 and nu=q+5/2=(d+3)/2. Substituting R(r)=r^(-q)J_nu(k*r) into the separated radial equation gives the Bessel equation with the exact angular eigenvalue gamma(gamma+d-2). The first positive Bessel zero produces the correct Dirichlet condition at r=R, and the radial factor is positive before that zero. The resulting positive eigenfunction is the cell ground state, by orthogonality to a lower nonnegative ground state if such a state existed. Rotational congruence permits one normalization constant for all cells.

The series gives

    R(r)=c*r^(5/2) (1-k^2*r^2/[4(nu+1)]+O(r^4)).

Multiplying the angular profile yields the displayed O(r^(9/2)) remainder. Its gradient has order O(r^(7/2)) within the cells and almost everywhere after zero extension. Components need not be classically differentiable across ordinary interfaces, so explicitly saying “almost everywhere, and classically within each cell” would improve the sentence. That is a clarification of the natural Sobolev interpretation, not a failure of the asymptotic claim.

The limiting uncorrected boundary frequency is 5/2. Independent high-precision evaluations in dimensions 3,4,5,8 check the radial ODE, the series coefficient, and this frequency limit. The eigenvalue-corrected and uncorrected frequency definitions have the same limit here.

The Hadamard variations in the manuscript are restricted to smooth patches away from the spine and outer boundary. On those patches the equal normalized flux magnitudes cancel the two adjacent first variations. No singular-junction shape derivative or second variation is being imported without proof. Neither this pairwise stationarity nor the exact eigenfunction construction proves global sum minimality. The rim regularity problem is also correctly disclosed.

## 8. Remaining obligation and acceptance boundaries

Accepted conclusions:

1. Exclusion of boundary cone degrees in (2,5/2), including the stronger stated class-S formulation.
2. Full rigidity at degree 5/2 and tangential tY orientation.
3. Exact half-ball energy minimality and cone-class sharpness for N>=3, d>=3.
4. The universal spectral lower bound under the imported boundary assumptions.
5. Correct restricted product formula and a genuine unrestricted tensorization obstruction.
6. Correct spherical shift and sharp three-cell hemispherical min-max value.
7. Correct normalized segregated thin-cylinder Gamma limit and minimizer compactness.
8. Correct explicit half-ball eigenfunction candidate and its pairwise first-order stationarity.

Not established:

- Existence of an admissible bounded-domain global spectral-sum optimizer with an actual boundary point of frequency 5/2.
- A sum version of the full-sphere three-partition theorem.
- Global optimality against nonconical competitors in a Euclidean half-ball.
- Persistence of the boundary triple configuration under a thin limit or rim smoothing.
- Uniqueness/decay of blow-ups or regularity near actual 5/2 boundary points.
- Historical novelty or absence of every possible later literature result.

The correct overall status is therefore **UNSOLVED, five substantive author approaches, with a verified sharp cone-class theorem and additional verified partial results**. It must not be promoted to a complete solution of the strict spectral-attainment target.

## 9. Audit artifacts

- reports/AUDIT.md: this report.
- checks/independent_controls.py: standalone independently written controls.
- checks/results.json: execution results, 16 passed.
- reports/OPTIONAL_CLARIFICATIONS.patch: optional nonessential textual additions; not applied to originals.
- reports/VERDICT.json: concise machine-readable outcome.
- reports/MANIFEST.json: input/source/output hashes and inspection metadata.

The frozen primary-source extracts and rendered source pages were used only for verification; they are not authored mathematical deliverables and should not be published as part of this audit. Any publication should include only authorized authored reports, scripts, patch, and public verification metadata.
