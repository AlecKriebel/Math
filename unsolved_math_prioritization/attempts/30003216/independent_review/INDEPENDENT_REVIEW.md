# Independent analytic review: adaptive hybrid finite elements, 30003216

## Verdict

**PASS_SCOPED_PARTIALS_ORIGINAL_UNSOLVED_5_OF_5. No mandatory correction.**

The five-turn collection proves the stated reconstructed planar algorithm and estimator results under its explicit hypotheses. It does not identify the original unprinted augmented estimator or adaptive policy. The original target therefore remains unsolved, with five author turns consumed. This verdict does not certify novelty, optimality, computational advantage, or the current historical status of every interpretation of the source question.

The reviewed author manifest is SHA-256 `87aa4fb3c4442ec708164eaed57b7a0004a4cfb6a0b7c74cb4175282c0efc351`; PROOF_COLLECTION.md is `0cd5a14b9e34ab012b4de4bba828dc8150b5f0ae259ef021393b6245cc9b5833`. All24 author files and seven source PDFs match. All five author checkers replay byte-for-byte. I did not contribute to the author route and did not change its frozen files. This is independent adversarial assistant review, not human peer review.

## 1. Exact target and retained hypotheses

The original Ku contribution asks about convergence driven by an announced augmented flux estimator. It does not print a local estimator formula or a full marking, coupling and parameter algorithm. The source-supported divergence correction is verified against the full KLS2017 equation. The reconstructed variants preserve that two-stage equation but introduce explicit policies. Leaving the source target unresolved is therefore appropriate.

Turn1 allows bounded symmetric uniformly positive definite A and a bounded Lipschitz domain. The residual and adaptive results restrict to A=I and planar triangular RT0 fluxes with free boundary normal trace. Turn3 requires a polygon star-shaped with respect to a ball. Turn4 needs only a simply connected polygon and its stated compatible refinement/overlay properties. Turn5 adds convexity for dual H2 regularity. Homogeneous Dirichlet data, exact variational solves/integration, nested flux meshes and uniform shape regularity are retained throughout the relevant results. No proof covers arbitrary adaptive policies or general higher-order/three-dimensional settings.

## 2. Turn1: reaction equivalence, projection convergence and calibration

The recovered scalar is exactly P_h u_H + delta^(-1)(P_h f-div sigma_h). Substituting it proves both mixed equations with the correct sign. For continuous input q, the coercive flux equation is equivalent to a homogeneous-Dirichlet reaction equation for w; L2 forcing implies its flux lies in H(div). Equality of that flux with the Poisson flux forces w=u and then q=u by density. Thus the fixed inaccurate coarse input causes a genuine bias.

The stability estimate in B_delta has constant delta and gives the stated sqrt(delta) bound on the weighted L2 flux norm. It is not a parameter-uniform H(div) equivalence. Nested orthogonal projections are strongly Cauchy without any global mesh-density hypothesis. Comparing the changing-input flux against the fixed limiting-input projection proves its Cauchy property. The packet correctly withholds consistency until an additional argument is supplied.

On the square, the homogeneous P1 space with only boundary vertices is zero. The eigenmode reaction solve has the stated factor lambda/(lambda+delta). Uniform RT0 refinement converges to that biased flux. Its element curl vanishes, while smooth interpolation plus inverse trace inequalities makes the all-edge tangential contribution vanish; the h-weighted bounded divergence residual also vanishes. The smooth limit has zero tangential boundary trace because its scalar potential vanishes there. This validates the calibration against an explicitly unaugmented estimator. It is not a counterexample to the source's expressly augmented estimator.

## 3. Turn2: weighted adjoints, exact correction and residual estimates

D and G must be adjoints in the flux mass and scalar L2 inner products. With that convention, S=DG is positive self-adjoint, and G S^(-1) is the minimum-mass-norm divergence right inverse. The correction identity, Schur energy and dual supremum formulas follow exactly; the maximizing scalar is S^(-1)d. Merely defining Q=div V gives finite-dimensional positivity, not a uniform inf-sup bound, a distinction the proof preserves.

The two multiplier bounds follow from delta*sqrt(lambda)/(lambda+delta), with its sharp maximum sqrt(delta)/2. The corresponding defect multiplier is at most delta. They justify the small-parameter transfer only under uniform stability and bounded coarse data.

For the planar estimator, solve -Delta z=f-div sigma_h and split e=-grad z+w. The H0^1 gradient is orthogonal to every distributionally divergence-free L2 field; simple connectedness gives w=curl psi with an H1 stream function, modulo constants. The continuous P1 interpolant is not boundary constrained here, and its curl is a conforming divergence-free RT0 field. The discrete equation supplies its orthogonality to sigma_h. Integrating the remaining RT0 field elementwise leaves exactly the tangential jumps, including boundary edges. The trace approximation estimate then bounds the solenoidal error by eta. Elementwise mean subtraction bounds the divergence error in H^-1 by oscillation plus the negative norm of the conservation defect.

For efficiency, a scalar polynomial edge-bubble extension of the tangential jump can be chosen with continuous patch trace, zero on the other patch edges, and gradient norm bounded by C h_E^(-1/2)||j_E||_E. Its curl pairs trivially with the exact Dirichlet gradient, even on boundary patches. Polynomial norm equivalence yields eta <= C||e||. The defect inequality follows from d=(f-Pf)-div e. No smooth tangential trace of the exact flux is required. The whole L2-defect replacement is only reliable, as stated.

The marking-transfer formula follows from two reverse-triangle inequalities. It needs L*kappa<sqrt(theta)<1, which also gives the later absorption. Turn2 explicitly retains the zero-indicator termination gap and the conditional conservative convergence input; it does not claim an unconditional algorithm theorem prematurely.

## 4. Turn3: a complete variable-delta variant

The domain condition supplies a bounded H0^1 divergence lift for mean-zero data. Adding the mean times x/2 gives an H1 lift for arbitrary cellwise data with no imposed normal boundary condition. The canonical RT interpolant commutes with divergence, and its H1-to-L2 stability is uniform on the assumed shape-regular meshes. This verifies the right-inverse constant rather than inferring it from finite-dimensional surjectivity.

On each fixed mesh the defect tends to zero as delta is halved, so the positive absolute tolerance guarantees finite termination even if the tangential estimator vanishes. The hybrid-to-conservative difference is bounded by C_R*tau_l^2 independently of how the coarse inputs change. Each data step terminates because uniform refinement makes h_max||f|| arbitrarily small; extra refinement cannot increase the cell-mean oscillation. These are finite-level statements, without a uniform work bound.

The conservative mixed Cauchy lemma is valid. Its bounded weak cluster points lie in the closed limiting H(div) space and have the same limiting projected divergence. To see uniqueness, approximate any limiting zero-divergence field by discrete fields and correct their small divergences with the uniform right inverse. This proves density of discrete kernels. Every cluster point is orthogonal to the limiting kernel, so there is at most one. To upgrade to strong convergence, correct approximations of that point to have the exact discrete projected forcing and use minimum-norm optimality. The limsup norm inequality plus weak lower semicontinuity closes the argument. This reasoning does not assume that the adaptive union is dense in the full ambient space.

For an old RT0 field on a refined mesh, new interior edges inside a cell have zero jump, and splitting a marked edge at its midpoint reduces its length-weighted contribution by at least one half. The same statement holds on the boundary. Together with uniform inverse-trace stability, this gives the actual reduction used in the proof.

The small/large-indicator dichotomy covers every level. Infinitely many small indicators give a subsequence converging to the exact flux by reliability, and the established full-sequence Cauchy property fixes its unique limit. Otherwise the absolute defect is eventually small relative to the indicator, transfers a positive fraction of bulk marking, and yields b_(l+1)^2 <= q b_l^2 + o(1), q<1. This recursion implies decay without requiring the perturbations to be summable. Projected forcing already has an L2 limit; its H^-1 convergence to f from oscillation identifies that limit as f. Thus the asserted H(div) conclusion is justified.

## 5. Turn4: fixed delta and moving primary data

The primary residual proof uses a boundary-preserving H1 quasi-interpolant, the zero element Laplacian of P1 functions, and standard local trace estimates. No H2 regularity is needed. The half-edge allocation is important: splitting an edge adjacent to either marked cell reduces its full contribution sufficiently to lose at least half the allocation to all marked adjacent cells. Marked-cell diameter halving reduces its volume term by at least three quarters. Additional refinement cannot increase the old-function estimator. Inverse traces plus nested Galerkin increments then give the stated residual recursion and hence primary convergence.

The flux Cauchy step compares with the B_delta projection of the exact flux. Its moving-input error tends to zero because u_l tends to u; no unsupported summation of successive data perturbations occurs. This gives a strong H(div) limit, but the proof correctly does not stop there.

Tangential estimator reduction applies to the actual hybrid sequence since its increments tend to zero. Helmholtz decomposition then shows the limit belongs to -grad H0^1. This only eliminates the solenoidal part, and the proof does not confuse it with conservation.

The fine-over-coarse overlay supplies the remaining data information: ||h_l(f-P_l f)|| <= ||H_l f|| <= rho_l. Nested P_l f has an L2 limit; its negative-norm limit is f, so the two agree. Taking limits in the recovered first mixed equation yields q_infinity=P_infinity w. Combining the recovered scalar identity with the limiting divergence gives

    -Delta(w-u)+delta P_infinity(w-u)=0.

Testing with w-u yields the sum of its gradient norm squared and delta times the squared norm of its orthogonal projection. Both are nonnegative, so w=u. This identifies the flux limit even if the limiting scalar space is proper. This is the essential consistency proof, and it passes without an implicit global density assumption or a small-delta absorption.

The existence of uniformly shape-regular compatible refinement/overlay operations is explicitly assumed. The result does not assert that arbitrary unrelated mesh generators automatically have this property, and it gives no refinement-complexity estimate.

## 6. Turn5: higher-order augmentation

The decomposition sigma_h=-grad w+xi and the first mixed relation imply (q_h-P_h w,div tau_h)=(xi,tau_h). Testing with a uniformly bounded divergence lift gives ||q_h-P_h w|| <= C_R||xi||. Convexity implies the star-shaped hypothesis needed for this lift, and the boundary normal component remains unconstrained.

The projected-reaction error equation has the correct signs. Its energy is ||grad e||^2+delta||P_h e||^2. The coarse and recovered-scalar terms pair with P_h e, giving sqrt(delta) factors directly by Cauchy–Schwarz. Nothing is absorbed through a smallness assumption on delta. The resulting flux bound controls the gradient error plus the already estimated solenoidal part.

For the primary L2 bound, homogeneous-Dirichlet H2 dual regularity is invoked only on convex polygons. In two dimensions the dual solution has well-defined nodal values, and its boundary values vanish. The cell L2 interpolation order H^2 and edge L2 trace order H^(3/2) yield precisely the displayed H^4 and H^3 squared-residual weights. No missing data oscillation or unknown primal-error term remains. The higher-order estimator is bounded by H_max times the usual primary estimator, hence tends to zero under the specified fixed-delta algorithm. Only the tangential term is claimed efficient relative to flux error alone; the full coarse augmentation is not assigned an unjustified efficiency bound.

## 7. Checks, provenance and publication scope

All five receipts reproduce byte-for-byte, with82,268,245,467,296 exact assertions. The fresh independent program uses nonorthogonal mass matrices in both flux and scalar spaces, checks weighted adjoints and Schur energies, proper-subspace positive-projection identities in every direction through exact principal minors, and actual length-weighted edge integrals. It also checks refinement allocations and strict recursion constants. All794 fresh exact controls pass; INDEPENDENT_CHECKS.json records their scope. These diagnostics supplement the preceding analytic audit; no infinite-dimensional theorem is inferred from samples.

The source review confirms the original and published equations, classical lifting/interpolation/regularity hypotheses, 2024 prior credit and the access-limited2026 preview. The full later adaptive theorem was not obtained, so neither equivalence nor non-equivalence to the original procedure is asserted. Source PDFs, extracted texts, rendered pages and imported raw records are excluded from this portable review.

The unchanged collection may be published as independently reviewed scoped partial mathematics with **original target unsolved5/5**. The parent retains the publication gate. No sixth proof-search turn, new discovery claim or general adaptive theorem is supplied by this review.
