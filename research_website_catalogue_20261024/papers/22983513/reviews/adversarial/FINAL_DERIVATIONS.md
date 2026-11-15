# Final analytic checks in the independent adversarial lane

The substantial eight-family proof reconstruction in early/INITIAL_RECONSTRUCTION.md was sealed before foreign science, supplied code/results or historical/current opinions. It already reconstructs the full arbitrary-bounded-open-set theorem, two distinct general infinite-support mechanisms, convergence, exact remainder, repeated-index quadratic inference and boundary/normalization falsifiers. This final document records the postseal closure of its source frontier and the distinct validated Fourier mechanism; it changes no hypothesis or conclusion and supplies no repair.

## The form-domain and finite-support implications are sufficient

For clarity, the crucial domain inference is conditional. For u∈Dom H with Hu=Eu, xαu∈Dom H follows from bounded-coordinate multiplication in H₀¹ and the distribution product rule. The vector ∂αu need not satisfy a Dirichlet boundary condition in general. Only if xαu has finite spectral support does (H−E)xαu enter Dom H. In that hypothetical case the differentiated interior equation and the form-domain characterization make it an E-eigenvector. Its simultaneous membership in the range of H−E contradicts self-adjoint range/kernel orthogonality and the nonzero integration-by-parts pairing. This is valid for every coordinate and for every real normalized eigenfunction, on disconnected as well as rough bounded open sets.

The alternative early polynomial proof is independently checkable: in distributions, (−Δ−E)²(xαu)=0. A finite eigenfunction expansion then forces every coefficient with E_k≠E to vanish, by L²orthogonality; hence (H−E)xαu=0, contrary to the pairing1. It uses no global H²boundary regularity or unproved boundary unique continuation. The zero-extension compactness and Poincaré arguments ensure that every finite threshold has finite-dimensional spectral subspace, and that positive bottom energy and all finite indices exist.

The absolute-convergence argument controls every fixed-row spectral rearrangement by Σ|E_k−E_j||a_jk|² and Σ(E_k−E_j)²|a_jk|². The former follows by Cauchy–Schwarz, the latter from Dom H. Only finitely many rows lie below finite z. Thus all low-block pair cancellations are legitimate. A zero positive high-block remainder at z>E₁ would give finite support for xαu₁, already excluded. The strict inequality at every finite real threshold is proved, including thresholds at repeated eigenvalues.

The quadratic proof uses full truncated sums, not a simplicity assumption. Equal-to-threshold terms are zero, so stopping the first-J list partway through an eigenspace does not change those evaluations. Its strict upper-root inclusion plus non-strict lower-root inclusion gives a strict gap bound; zero gaps are harmless. When the next eigenvalue is still E₁, direct D=4E₁²/n²>0 closes the exceptional branch. This verifies the exact original quantifiers rather than a connected/smooth/simple-spectrum replacement.

## A distinct explicit Fourier and validated-tail mechanism

On (0,π), u_j=sqrt(2/π)sin(jx), E_j=j². Product-to-sum and direct integration of x cos(mx) give diagonal a_jj=π/2 and, for j≠k,

    a_jk=0                  when j+k is even,
    π a_jk=−8jk/(j²−k²)²   when j+k is odd.

This independently exhibits infinitely many nonzero high coefficients for every j. Translating the interval adds a constant only to the diagonal, which drops out of every spectral-difference sum. The parity and symmetry checks in own_controls.py are exact rational computations of the scaled off-diagonal coefficients, not numerical quadrature or a deposited-code import.

For finite real z>E₁, let t_j=z−j² and j range over j²<z. Write S_K for the finite high-mode remainder using b_jk=πa_jk and k≤K. For k>K≥2j,

    |b_jk|≤128j/(9k³),
    t_j(k²−j²)(k²−z)b_jk²≤(16384/81)t_jj²/k².

Consequently the uncomputed positive tail is at most

    T_K=(16384/(81K)) Σ_(j²<z)t_jj²,

because Σ_(k>K)k⁻²≤1/K. The scaled exact full remainder is π²R(z), so rational bounds p₋<π<p₊ give the validated enclosure

    S_K/p₊² ≤ R(z) ≤ (S_K+T_K)/p₋².

The code constructs p₋,p₊ using alternating-series bounds for Machin's identity π=4(4atan(1/5)−atan(1/239)). Its tangent identity is checked exactly: tan(4atan(1/5))=120/119, and subtracting atan(1/239) gives tangent1 in the first quadrant. Standard angle/alternating-series reasoning fixes the branch. No floating-point interval or estimated truncation error is used.

Six real/eigenvalue thresholds, each at K256 and K1024, produce twelve validated enclosures containing the direct exact rational remainder; every lower bound is positive. Refinement reduces width by more than a factor2, and the refined width is less than a tenth of the exact remainder. These checks audit the actual infinite-series coefficients, sign and normalization with bounded error. They supplement the universal proof; enclosure inclusion alone is not mislabeled an exact numerical proof of an analytic identity on every domain.

## Exact spectra and wrong-model controls

Every tested box prefix is certified against all omitted positive multiindices. Enumerate 1≤m_i≤K; any absent mode has energy at least Σa_i+min_i a_i((K+1)²−1), for inverse-squared-side coefficients a_i>0. The final needed eigenvalue is strictly below that bound. Repeating each eigenvalue realizes a disjoint union of congruent translated boxes and exercises genuine ground and higher multiplicities. Dimension1 additionally has an all-J positive closed formula derived by direct power sums in the early proof. Finite matrix controls check only symmetric-block cancellation; they expressly cannot realize all Dirichlet commutator sum rules in finite dimension.

Eight explicit altered-model/algorithm controls demonstrate the importance of the hypotheses: z=E₁ is equality; non-strict Yang permits a synthetic saturating list; Neumann ground energy0 breaks the asserted gap bound; unsquared M₂ gives a negative scaling example; finite coordinate compression loses the full sum rule; reversing the high-tail sign is detected; self-adjoint finite toy matrices do not supply the PDE commutation hypothesis; and repeated ground states require the positive D branch. These are counterexamples to altered statements, not to the paper's literal theorem.

## Primary normalization and historical boundary

The actual printed OWR415 definitions and both unsquared gap displays were personally read and visually checked, with attribution/context on414–416. The published Harrell–Stubbe Proposition6 at1802 was personally read and visually checked. Setting its kinetic parameterσ=1 and identifying its dimensiond with the manuscript's n gives exactly D=((n+2)A/n)²−(n+4)B/n. Thus the paper's explicitly disclosed squared normalization matches the primary inequality. The literal unsquared workshop display is not a universal bound, as the early scaling counterexample proves; the paper does not claim otherwise or silently substitute a different question.

The old trace identities and non-strict estimates remain credited. The actual Ashbaugh2002printed12 caveat corroborates the manuscript's specific historical sentence, but does not establish worldwide priority today. The present adversarial lane did not body-audit every antecedent or the current problem website, and offers no firstness/continued-open guarantee. No substantive defect was found in the full stated theorem. The exact mathematical success and these provenance limits are separate conclusions.
