# Full independent review: 30001994

## Verdict

**PASS_COMPLETE_ORDINARY_POTENTIAL_SOURCE_TARGET. No mandatory correction.**

This verdict binds the unchanged author PROOF.md SHA-256 `37fb589e872a65f9176d36c7db98119c2dfd1715d92f96fc81183dc099dcc956` and FROZEN_MANIFEST.json SHA-256 `e62c82154b877464b1d83e3e8c9c75c5e15053e5025b758c70de298b39e95bb6`.

The example disproves extension of the original ordinary gradient-valued correction map to arbitrary bounded nonnegative scalar conductivity. It does so for a smooth compactly supported conductivity and smooth compactly supported divergence-free input, with no H1-local scalar correction at all. This is a complete negative answer to the source-space mapping question. A `claimed_solved 1/5` disposition is supported after one substantive author turn. The affirmative weighted-completion projection is retained and must not be described as an ordinary-potential solution. The proof does not establish nonexistence of every generalized formulation or a separate full time-dependent PDE theorem for arbitrary forcing. Historical novelty and community acceptance are not certified. Publication remains the parent's decision.

## Independence and scope of evidence

The reviewer did not contribute to the author route. Before freeze, the reviewer read the original source and foundational spaces; after freeze, the complete proof, source gate, requested attacks, checker and receipts were examined. All eleven manifest-bound author artifacts and all five source PDFs match their exact hashes and byte counts. The author's 323 exact symbolic checks replay byte-identically. A separately written checker passes 673 exact controls using a different periodic smoothing profile, Cartesian vector differentiation and explicit weighted/unweighted norm comparisons. Neither finite checker proves Sobolev density or infinite-dimensional solvability. Those arguments are audited below.

## 1. Exact target and source spaces

I read the entire OWR contribution, printed630–633, and visually inspected the actual question on631. The question is about the correction used in E=A+grad(phi_A), with div(sigma E)=0 and the reconstructed E in the stated W(curl) space. The full published Arnold–Harrach paper supplies the omitted details. Its Section2.1 defines L2_rho using a spatial decay weight that is bounded above and below on each compact set. Thus membership implies ordinary L2_loc. Lemma3.1 maps into ordinary globally L2 curl-free fields. Its restriction to divergence-free vector Beppo–Levi inputs is exactly the required correction map.

Consequently, exclusion of all H1-local scalar solutions is stronger than necessary to obstruct that map. A scalar distribution with an L2-local gradient has an H1-local representative up to constants, so allowing an ordinary distributional gradient does not escape the example. A discontinuous angle with a surface delta in its gradient falls outside the source output.

The source requires connected exterior, not simply connected conductor. The annular-cylinder topology is therefore admissible. The source's positive lower bound is exactly the assumption being removed in the open question; it cannot be reimposed to reject a degenerate example. The report's reversed ball inclusion is documented. The optional translation places a genuine small ball inside the conductor, so even literal retention of that printed inclusion does not invalidate the construction.

## 2. Smoothness, support, geometry and input

For q=x1^2+x2^2, the radial/vertical bump eta is smooth on all of R3 and flat at q=1, q=4 and z=+/-1. It is positive precisely on the stated open annular cylinder. Multiplying r-x1 by eta is globally smooth because eta vanishes on a full neighborhood of the axis, where r itself is nonsmooth. The conductivity is compactly supported, nonnegative and bounded by4. Its essential infimum on the conductor is zero. Its only interior zeros are the positive-x1 meridional cut; that set has volume zero. Near an interior point of the cut, r-x1 is quadratic in the transverse angular displacement.

The annular cylinder is a bounded Lipschitz domain. Corners at its rim do not violate the Lipschitz condition. Its exterior is connected through the central passage and either end. Translating the construction by -(3/2,0,0) puts B_(1/4)(0) inside the conductor by the elementary radial and vertical bounds given in the proof.

The cutoff chi may be chosen with all the stated support and plateau properties. Its gradient has only radial and vertical components and is orthogonal to the angular circulation. The resulting A is globally smooth, compactly supported and divergence-free. All its first derivatives are square-integrable, so it belongs to the exact source input spaces. It is the unit angular-gradient field A0 on the entire conductivity support. No hidden boundary condition on A is being discarded.

## 3. Single-valued approximate potentials and exact weighted energy

The three pieces of h_epsilon agree at both internal joins and give the same value at the identified angle endpoints. The derivatives on the two sides of the angle seam agree as well. For each fixed epsilon the function is Lipschitz on the circle, not a multivalued angular coordinate. Its derivative has mean zero, as every periodic scalar derivative must.

Since chi vanishes near the axis and outside a bounded region, chi h_epsilon is a genuine compactly supported H1 function on R3. Multiplication by chi adds no gradient contribution on the conductor because chi is constant there. Thus the residual on the conductor is exactly the indicated angular pulse. Ordinary smooth approximation in global H1 is available; bounded sigma transfers that convergence to the conductivity-weighted gradients. A diagonal sequence of smooth functions can be chosen if desired, so the use of compact H1 intermediates causes no gap in the closure assertion.

I independently checked the cylindrical factors: sigma contributes eta*r*(1-cos(theta)), |A0|^2 contributes r^(-2), and volume contributes r. The radial factors cancel, leaving precisely C_eta and the angular integral. The latter is 2(epsilon-sin(epsilon)); the bound by epsilon^3/3 follows by integrating 1-cos(theta)<=theta^2/2. Multiplication by pi^2/epsilon^2 gives the claimed squared error at most (pi^2 C_eta/3)epsilon. In particular the error tends to zero in norm, rather than merely weakly.

The unweighted norm formula on the conductor also agrees: the derivative-squared angular integral is 2pi^2/epsilon-2pi, and the radial/vertical factor is2log2. Its divergence is correctly presented only as an illustration. The proof of nonexistence does not rely on treating failure of one approximation scheme as failure of all possible potentials.

## 4. Weak testing really forces exact cancellation

Suppose phi is H1_local. The flux sigma(A+grad(phi)) is an ordinary L2 field with compact support. Therefore its distributional divergence equation, initially tested on smooth compact functions, extends continuously to compactly supported H1 tests. Taking kappa phi is valid: kappa is smooth compactly supported and identically1 near the compact conductivity support. The extra cutoff derivative is multiplied by zero wherever it could contribute. This yields the displayed orthogonality against grad(phi).

The approximate potentials are also legitimate tests. Their weighted gradients converge strongly to -sqrt(sigma)A, and the weighted residual is in L2, so passing to the limit gives orthogonality against sqrt(sigma)A. Adding the two orthogonalities gives the squared norm of the residual, which must be zero. This is a direct Hilbert-space calculation based on actual admissible tests; it does not invoke an unproved uniqueness or closed-range theorem for the degenerate operator.

Since sigma is strictly positive almost everywhere in the conductor, the zero weighted residual implies grad(phi)=-A0 there in the ordinary almost-everywhere sense. The zero meridian cannot hide a nonzero ordinary L2 gradient or a surface singularity. This is the decisive distinction from a weighted completion.

## 5. The topological contradiction is valid globally

The test field B=eta A0 is globally smooth and compactly supported because of the same flat cutoff and axis separation. It is divergence-free. Although its support reaches the boundary of the conductor, it is an admissible global compact test field; the proof does not need B to have support compactly contained in the open conductor. It vanishes outside the conductor closure, and the boundary has measure zero.

Global integration by parts pairs every H1-local gradient with B to zero. The forced identity in the conductor instead gives the strictly negative number -integral eta|A0|^2. That integral is finite and nonzero. This contradiction is unaffected by the meridional zero set, by the normalization of phi or by an arbitrary extension of phi in the insulating region. It excludes existence itself, not just continuity or linearity of a proposed selection map.

This global dual argument is stronger and cleaner than assigning a loop integral to an arbitrary H1 function. No unjustified trace on a one-dimensional loop is used.

## 6. Weighted completion and later literature

The closure V_sigma is a closed linear subspace of ordinary vector L2 after multiplication by sqrt(sigma). Orthogonal projection therefore always gives the stated weighted correction for weighted-square-integrable input. Its flux is divergence-free by testing against sqrt(sigma)grad(v), and its projected mass form is symmetric nonnegative. In the compact-support setting, the norm of sqrt(sigma)A is controlled by the source L2_rho norm, so the stated continuity is correct.

If an ordinary correction exists in that setting, a cutoff and ordinary H1 approximation put its weighted gradient into V_sigma. Orthogonality then identifies it with the projection. In this example the projection cancels the weighted circulation exactly, while Sections4–5 show that no H1-local scalar represents it. The source-space conclusion and the affirmative generalized statement are therefore consistent.

The later literature scope controls were checked directly: Francini–Franzina–Vessella condition(1.1ii) imposes uniform positive definiteness. Pauly et al. Hypothesis4.2 in the2018 report and Assumption4.3 in the publisher proof require a strictly positive operator on the conductor and additional domain/range conditions. Neither is a theorem asserting the missing ordinary correction for every smoothly degenerating scalar coefficient. No exhaustive priority claim is inferred from these checks.

## Disposition

The complete counterexample and its positive weighted-completion qualification pass without mathematical revision. Preserve the exact ordinary-potential/W(curl) scope in any QUEUE row, PR title and result summary. Include only the frozen public author artifacts and this portable review package, excluding source PDFs, extracted text, page renders and replay workspaces.
