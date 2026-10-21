# Operator/physics/topology follow-on triage

2026-10-06, completed targeted triage. Scope IDs 260–321. Best-guess screening completion: 95%; no proof claim, full priority audit outstanding.

## Recommended: all von Neumann algebras and their preduals are Banach–Mazur stable

**Input:** #295, `preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/build/sections/01-introduction.tex`, main theorem lines 44–53: ordinary bounded Hochschild H^k(M,M)=0 for all complex von Neumann M and k>=2; no completely bounded restriction.

**Precise target:** For every complex von Neumann algebra M there exists epsilon_M>0 such that for every von Neumann algebra N, d_BM(M,N)<1+epsilon_M implies M,N Jordan *-isomorphic. The same conclusion from d_BM(M_*,N_*)<1+epsilon_M. Include the equivalent linear-isometry statements. Threshold initially depends on M; do not claim a universal threshold without further work. Ordinary Banach-space distance, not completely bounded distance. Jordan isomorphism is the proper target; ordinary *-isomorphism can fail because opposite algebras are isometric.

**Mechanism:** Apply Jean Roydor's conditional theorem (2022, Journal of Topology and Analysis 14(3), 767–792), whose hypotheses H^2(M,M)=H^3(M,M)=0 are supplied by #295. Author's slides explicitly state theorem 2 with both algebra/predual versions: https://www.cirm-math.fr/RepOrga/2169/Slides/Roydor_Slides.pdf . Published primary paper DOI https://doi.org/10.1142/S1793525321500151 . Web search extracted theorem verbatim from indexed author slides; direct web open errored, so obtain full PDF for final verification.

**Bundle:** Local rigidity under arbitrary small bounded associative multiplication perturbations, via Johnson and Raeburn–Taylor. For each M and standard product m, sufficiently close bounded associative product m' is intertwined with m by a bounded linear isomorphism near identity. Primary original theorem https://www.sciencedirect.com/science/article/pii/0022123677900726 (Raeburn–Taylor 1977, doi 10.1016/0022-1236(77)90072-6); author abstract explicitly H2=H3=0 suffices. Could add formal bounded deformation triviality by standard cohomology recursion, but analytic convergent claims need precise theorem.

**Novelty/duplicates:** Full corpus rg for `Banach.Mazur` returned no matches. Corpus #289 references the 2014 *completely bounded* multiplication-perturbation theorem, which is distinct. The cb Banach–Mazur stability theorem was already unconditional (Ricard–Roydor https://arxiv.org/abs/1108.1970), and must not be advertised as new. #295 intro mentions connections to multiplication stability without proving or stating the general Banach–Mazur conclusion. This is a direct but substantial application paper, with independent novelty mainly in removing final hypotheses and unified precise scope. Full literature priority audit still needed.

**Exact gap:** Check published Roydor theorem's hypothesis and predual/general nonseparable scope; compose. No new core estimate apparent. Any universal epsilon or quantitative global modulus requires extra argument.

**Estimated impact:** 8.0 (major broad operator-algebra geometry result), tractability very high. A short research note is most honest unless quantitative refinements established.

## Backup: failure of circle cancellation and nontrivial topological s-cobordisms for hyperbolic aspherical 4-manifolds

Input #320 gives closed homotopy-equivalent nonhomeomorphic aspherical M,N of dimension 4, common torsion-free word-hyperbolic group. Khan's four-dimensional rigidity up to s-cobordism, https://arxiv.org/abs/0907.0308 , yields nontrivial topological 5-dimensional s-cobordism. By Farrell–Jones permanence for G x Z and high-dimensional Borel rigidity, M x S1 and N x S1 are homeomorphic. Thus circle cancellation fails within closed aspherical 4-manifolds with hyperbolic pi1. A standard open-cylinder/s-cobordism argument also suggests M x R ~ N x R.

**Downgrade:** Upstream #320 introduction lines 50–58 explicitly observes applicability of Khan and why good-group restrictions matter. Thus nontrivial s-cobordism consequence is already clearly implicit and arguably stated; standalone priority and independent novelty weak. Circle cancellation is not found explicitly in source but is a short combination. Impact 6.8 for derived statement, not independent 9+ breakthrough. Only include if other pool is thin; verify orientation scope and product FJ carefully.

## Excluded directions

- #287 free entropy dimensions not invariant under generators: explicitly proved in `sections/entropy-dimensions.tex` for four dimensions, not new.
- #314 Balmer spectrum topology/thick tensor ideals for all finite groups: already in introduction and general-groups corollary.
- #293 proper strongly closed transitive operator algebra: already companion abstract.
- #315 Hopf/Euler characteristic, signature bounds, finite-cover Betti growth: all in `consequences.tex`.
- #278 functional nondifferentiability/subgradient consequences of Kohn–Sham failure: already `sections/07-functional-consequence.tex`.
- #294 tensor stable finiteness and non-W* AW*-factor: already included.
- #280 arbitrary finite-group orbifold rationality: net-side rationality does not by itself provide algebraic C2-cofiniteness; transfers central difficulty, blocked absent new mechanism.
- #272 classical bipartite bound information: zero quantum-Eve distillable key does NOT imply zero key against a fixed measured classical Eve; incorrect transfer, blocked.
- #269 Laughlin sphere gap→torus Hall conductance: torus/twisted-boundary spectral gap not supplied; central difficulty remains.
- #302 classification of zero-mean-dimension minimal Z crossed products: old implications substantially already known, not novel input-dependent result.

## Independent adversarial audit: #082 triangular Hilbert variation -> commuting ergodic Hilbert theorem

Checkpoint completion: 100% route-level audit; proof writeup and priority audit not complete.

Reviewed `Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/build/sections/introduction.tex` lines 3–34: exactly B_(a,b)(F,G)(u,v)=integral F(u+t,v)G(u,v+t)dt/t, full pointwise rational annular r-variation, every r>2, L3xL3->L3/2. This is the right input.

### Continuous transference is sound

For a jointly measurable measure-preserving R² action and f,g in L3, fix finite rational truncation/variation menu with maximal radius R. Pull back f,g along the action and cut off to a box [-L-R,L+R]^2. On the inner box [-L,L]^2, the Euclidean integral equals the orbit integral. Apply upstream estimate for each basepoint x, raise to 3/2 and integrate x. Cauchy–Schwarz in x controls the product of the two orbit L3 integrals. Action invariance leaves an outer/inner area ratio tending to one as L grows. Take countably increasing menus by monotone convergence. Local integrability along the action follows by Fubini away from t=0. Finite r-variation gives Cauchy limits as scale tends to zero or infinity; maximal domination gives L3/2 convergence. No dense-subclass convergence theorem needed.

### Discrete restriction mechanism removes the apparent gap

Use a fixed small cell width, not a width tending to zero. Extend finitely supported lattice F_ij,G_ij to functions on R² constant on central subboxes (say side 1/2) of each integer cell, zero elsewhere. Evaluate output in smaller central subboxes (say side 1/8). At such output (i+a,j+b), nonzero integrand near t=n has exactly the lattice factor F_(i+n,j)G_(i,j+n), times the kernel integral over the overlap of the two shifted one-dimensional cell windows. The overlap length ell(a,b) is uniformly bounded above and below by positive constants. For nonzero integer n,

K_n(a,b) = integral_(n+I(a,b)) dt/t = ell(a,b)/n + O(1/n²),

uniformly in the restricted output fractions. Choose hard radial annular endpoints at half-integers; entire small windows about integers are included or omitted together. Thus Euclidean annular variation controls ell times the desired lattice variation up to the variation of a summable-kernel error. The latter is pointwise bounded by C sum_(n!=0) |F_(i+n,j)G_(i,j+n)|/n². Its ell^(3/2)(Z²) norm is <=C||F||_3||G||_3 by Minkowski, Holder and sum n^-2<infinity. Integrating over output fractions obtains the discrete inequality. Then apply finite-window Z² Calderón transference to arbitrary commuting invertible transformations.

**Audit verdict:** no hidden central gap found. The fixed-width restriction proof should be written carefully; naive suspension evaluated on diagonal phases would be invalid since that has measure zero. The central-box argument avoids this.

**Boundary:** Controls symmetric odd Hilbert sums, not ordinary one-sided Cesàro averages. Does not cover noncommuting actions. L3 input scope maintained. Countable partitions settle measurability. No unsupported uniform-in-frequency modulation claim.

**Priority:** March 2026 Becker–Durcik https://arxiv.org/abs/2603.20173 abstract gives shifted bilinear Hilbert transform and bilinear ergodic averages; inspect exact action scope before publication (expected powers of one transformation). 

Priority cross-check completed for Becker–Durcik 2026 full primary text https://arxiv.org/html/2603.20173v1 : Section 1.2 treats powers T^i and T^-i of ONE invertible transformation (Theorem1.2, Theorem1.3, Cor1.4). Its discussion around equation1.8 explicitly states general commuting S,T pointwise averages remain open. It does not already supply the proposed arbitrary-commuting bilinear Hilbert variation result. This is also a useful contemporary boundary citation.

## Final focused Banach–Mazur source check

Rechecked author Roydor's 2020 CIRM slides through the indexed primary PDF text. Theorem 2 states: M is a von Neumann algebra with predual L1(M); assume H2(M,M)=H3(M,M)=0. Then there exists epsilon_M>0 such that, for every von Neumann algebra N, the following are equivalent: M,N Jordan *-isomorphic; M,N linearly isometric; L1(M),L1(N) linearly isometric; d(L1(M),L1(N))<1+epsilon_M; d(M,N)<1+epsilon_M. No separability, factoriality, injectivity, finite-type, or faithful-state restriction is stated in that theorem. The predual here is intrinsic, including nonsemifinite M. Thus the broad target is supported by the exact author's theorem statement, and #295 supplies exactly its ordinary bounded cohomology assumptions.

Limitations retained: epsilon depends on M; the conclusion is Jordan *-isomorphism, not necessarily multiplicative *-isomorphism; distances and maps are ordinary complex Banach-space ones. Comparison object N must itself be a von Neumann algebra (or predual of one); this is not stability among all Banach spaces. Direct full-PDF retrieval from CIRM returned HTTP403 and DOI article full text was not accessible, so the journal-proof audit remains a publication-stage task. The exact theorem statement was obtained from primary-author slides via web search, not guessed from the abstract. Searches for a separability qualifier did not reveal one, but absence of such a qualifier in the slide statement is the precise evidence for the nonseparable scope.
