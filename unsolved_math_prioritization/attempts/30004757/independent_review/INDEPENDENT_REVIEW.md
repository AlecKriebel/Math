# Independent adversarial review: 30004757

Date: 2026-10-01. Verdict: **PASS for the frozen partial results, with the original target unresolved after five substantive author turns.** No mathematical correction is required to the reviewed files. This is not a full-solution, novelty, priority, or exhaustive-literature verdict.

## Frozen scope and independence

The reviewed author checkpoint is `3694c255238eba2d41e69d659e58db5c75df6149`. Its `FROZEN_MANIFEST.json` has SHA-256 `2edc87290b9c617c39e6c0288414f6bc1eea4cbc37618ce4d17129f049fc222c`. All 19 listed files matched their hashes. In particular:

- `RESULT.md`: `ad073ab2c309a331a8f40afe5ee4aaeb4baa5d927315fed4038b6bb3d9ed80ae`
- `turns/TURN_5.md`: `248694a3cc0b50d5a60279d2f0afb8972b7e514ea74bbac2909bf48d1634aebf`

I read the primary results and the five saved mathematical turns, attacked the hypotheses and limiting operations, reconstructed the essential comparison and duality steps, and wrote a separate exact checker. I did not supply an additional author search turn or replace the frozen argument with a different proof. The explanations below elaborate the reviewed proof and its cited inputs.

The original [OWR contribution](https://ems.press/content/serial-article-files/46911), printed pages 1884–1886, concerns real Alexandrov Monge–Ampère potentials with point masses and graph singularities. The printed Problem 4 and its two-mass starting case were visually checked. Nonpolyhedral obstacles belong to the separate Problem 5. Tangent-cone existence alone does not answer the requested precise description or the preceding Hessian-asymptotics question.

## 1. Convex duality and the C¹ partial result

For a finite convex potential near a vertex, the directional derivative is the support function of its compact subdifferential body. Local Lipschitz bounds upgrade convergence to uniform convergence on compact direction sets. Under the height scaling used in Turn 1 the gradient set is unchanged, so the MA scaling is correctly `M_rescaled(E)=M_u(p+rE)`, not a density-preserving quadratic scaling. The limiting atom records the body's volume only.

The shared-face equality follows in both directions from the two subgradient inequalities. An affine edge consequently gives a compulsory nonsingleton exposed face in the inward edge direction.

The localization argument uses [Mooney Proposition 2.7](https://arxiv.org/abs/2004.06696) only inside an affine chamber. If a nonsingleton exposed face had an extreme point in the open half-space, take a bounded convex subdomain there containing that point and a short segment of the face. Intersecting with the subdomain preserves extremality of that point; localization contradicts it. Thus all extreme points lie in the separating plane, and compact finite-dimensional convexity puts the entire face there. A supporting hyperplane other than that plane intersects a round disk in at most one point. The only nonsingleton exposed face is therefore the shared disk.

This proves the stated C¹ property off the inward ray. Unique support maximizers converge by compactness, giving continuity of the gradient rather than merely directional differentiability. On the inward ray the exposed set is the full disk, and its support function gives the stated transverse directional derivative. The half-ball example correctly shows that this geometry alone does not give C² regularity.

## 2. Partial Legendre equation and restricted local models

I checked the signs and powers in the partial transform. With `F=pρ−u`, one has `F_pp=1/u_ρρ` and `F_zz=−det(D²_(ρ,z)u)/u_ρρ`. Including the `n−2` transverse eigenvalues gives exactly Turn 2's equation and divergence form. The Euler equation has the same sign. Degeneracy at `F_p=0` is real.

The separated ODE has a genuine local branch, not just a formal leading balance. Linearizing the regular-singular system gives the stated stable eigenvalues `−1,−6` for n=3 and `−1,−4` for n=4. The integral kernel bound and the weighted `sup |y|/x` norm give a contraction on a sufficiently short interval: the forcing contributes a bounded norm, while the Lipschitz factor gains a factor of the interval length. The differentiated asymptotics follow from the system.

For the recovered local potential, `F_pp>0` and `F_zz<0` imply a positive definite two-dimensional Hessian after transformation; the transverse eigenvalues are positive too. The domain `|x′|<a(z)b′(R+ε)` is convex because a is positive and concave. At an interior axis point the axial subgradient component is zero and the transverse components fill exactly the radius-R disk. Its n-dimensional measure vanishes, so no line-supported MA mass has been omitted.

The endpoint-sector limit is computed from the exact inverse relation on its stated restricted sector. It does not interchange a fixed-z expansion with an endpoint limit. The warnings about the absence of a finite full endpoint neighborhood and of global matching are necessary and correctly retained.

## 3. Homogeneous rim model

The anisotropic coordinate Jacobian and height factor cancel exactly in the determinant. I independently checked the full n-dimensional Hessian after the parabolic substitution, including all transverse variables, rather than only replaying the reduced two-dimensional determinant.

The profile is convex and matches the obstacle with matching first derivatives at the two joining curves. Its singular second derivative is integrable. At the remaining crease the possible subgradients lie on the one-dimensional obstacle-gradient segment, so this set adds no n-dimensional MA measure. Thus the asserted global Alexandrov identity for the limiting model is valid.

The first integral and endpoint-slope normalization determine the profile in the explicitly restricted homogeneous, symmetric, single-interval model class. They do not prove uniqueness of actual source blow-ups. The frozen text appropriately requires growth bounds, nondegeneracy, convergence and a uniqueness mechanism before inferring source matching. The claimed relationship to the classical Pogorelov mechanism is an attribution, not a novelty claim.

## 4. General faces and conditional angular expansion

The localization of [Jin–Tu–Xiong Theorem 1.1](https://arxiv.org/abs/2506.08387) is valid. Choose a bounded convex domain compactly contained in a strict affine chamber, meeting the relevant face and the positive region. Subtracting that chamber's plane gives the required nonnegative, nontrivial zero-obstacle solution. A relative two-dimensional patch in a higher-dimensional face consists of non-exposed free-boundary points. The strict dimension bound at q=0 excludes it in n=3,4.

For a remaining nonsingleton segment, an endpoint inside the chamber would violate the same localization theorem used in Turn 1. Both endpoints are therefore on interfaces. They cannot share an interface hyperplane: a segment joining two points of that plane lies in it and cannot enter the strict chamber. The result does not control faces entirely within interfaces, and does not exclude bridging segments.

For the polytope incidence statement, a simultaneous contact for nonadjacent vertices would expose a polytope face of dimension at least two. All gradients of that face are then subgradients of the obstacle and of v at the contact point, contradicting Mooney's global dimension bound in n=3,4. The separate Y construction has the stated star contacts. This argument is not being extended to arbitrary dimensions.

The polar Hessian expansion in Turn 4 has the correct radial, mixed and tangential blocks. After factoring the radial and tangential powers, the determinant tends to `n(n+1)b det Q_h`. The remainder hypothesis through weighted second derivatives is essential; it is explicitly assumed. Hence the coefficient formula is a conditional compatibility identity and gives no equation selecting h. The radial and unimodular ellipsoid calibrations agree. Changing the asymptotic quadratic form does not demonstrate nonuniqueness with a fixed normalization.

The 2025 exposed-point regularity input is also correctly limited: it can be used inside a strict chamber, while the equation after subtracting one plane fails on the other contact body across a crease. Neither that theorem nor the cited higher-dimensional existence/stability work resolves the saved rim problem.

## 5. Global collision theorem: detailed analytic audit

### Same-normalization barriers and exhaustion

The exterior radial solution has derivative `(r^n−R^n)_+^(1/n)`. Its difference from r is integrable at infinity precisely for n>2, producing the stated negative constant. Increasing R decreases the derivative. Adding the difference of the asymptotic constants therefore makes `B_δ−W_R` nonnegative, decreasing and asymptotic to zero. Its maximum is the constant difference, of order δ. The separate small-radius and large-radius estimates indeed make B_δ dominate the two-plane obstacle globally.

The zero-obstacle solution on each ball is W_R. Obstacle ordering gives the lower bound, and Mooney's enlarged Perron class gives the upper bound despite unequal boundary values of the barrier. Restrictions of larger-ball solutions have at least the smaller prescribed boundary values, so the exhaustion is monotone increasing and locally bounded. Convex compactness and weak continuity of MA measures give the global solution and equality of density on compact sets with a positive obstacle gap. The two barriers have the same asymptotic additive constant; no normalization drift is concealed here.

### Contact convergence and a genuine common facet

The contact inequality supplies the outer-radius bound uniformly as δ tends to zero. For an interior upper-half-ball point, the zero-obstacle function is uniformly O(δ) on a fixed ball. A positive quadratic centered at that point, chosen with determinant strictly below one, dominates the boundary values for small δ. Local obstacle comparison forces contact at the center. One may justify this even when the boundary values meet the obstacle either by the zero-obstacle comparison principle with nonnegative boundary values, or by the convex-envelope/Perron comparison used in Mooney's proof. Strictly positive boundary data on this small auxiliary ball are not an additional needed hypothesis.

The crease barrier has the same required comparison direction. Independently differentiating its unnormalized piece gives

`det D²[(ρ^γ+z²ρ^(−γ))/2] = (γ/2)^(n−1)(γ−1)(1−z²ρ^(−2γ))^(n−1)`,

where `γ=2(n−1)/(n−2)` on `|z|<ρ^γ`. The value and first derivatives match the linear outer pieces. After the stated normalization and a fixed small multiplier it has MA measure below one, positive sphere minimum, a positive lower bound proportional to |z|, and zero center value. Quadratic scaling to the small comparison ball preserves the determinant bound. For small δ it dominates both the obstacle and boundary values, forcing contact on compact interior subdisks.

Upper and lower contacts have nonempty interior. Their convex hulls with a common interior disk supply upper and lower neighborhoods at the disk's interior points. Thus the total contact set really has the interior required by the later duality argument. Inner contact on all fixed compact half-ball subsets plus the outer-radius bound proves Hausdorff convergence, and convex-body volume continuity gives the claimed masses.

### Subgradients and the atomic equation

The use of Mooney Lemma 4.2 is justified by its proof, not just its statement for a particular exhaustion. At a separating-plane contact point, the obstacle already contributes the axial gradient segment. The global bound on subgradient dimension in n=3,4 excludes any off-axis subgradient. An axial slope beyond an obstacle endpoint would rule out all contact in the corresponding open half-space, contradicting the full-dimensional chamber contacts. Thus the subgradient equals the obstacle segment there.

At a contact-boundary point inside a chamber, an extreme point has the single obstacle gradient. Otherwise localization extends a boundary segment to the separating plane, whose subgradient has just been controlled. Subgradient inclusion along the segment excludes an extra slope in the chamber. Interior contact points are immediate. These are exactly the mechanisms needed for `∂v_δ=∂obstacle` on the entire contact set.

Mooney's Proposition 4.1 argument then applies: smooth measure-preserving duality holds off the joining segment, the segment interior has no n-dimensional MA mass, and its endpoints have masses equal to the two contact-body volumes. The common disk also verifies actual singularity along the segment. This does not rely on weak measure convergence alone to infer regularity.

### Limits and regularity obstruction

Legendre conjugacy reverses the global O(δ) bounds, proving uniform convergence of the original unrescaled potentials on all of space. The radial upper/lower asymptotes similarly preserve the common quadratic and additive normalization. Hausdorff convergence of the individual bodies yields locally uniform support-function convergence to half-ball support functions. The merged radial potential has the full-ball body. The unequal values in the inward direction verify the claimed noncommutation of limits.

The half-ball limit is C¹ across a horizontal direction but has second normal derivatives 0 and R from opposite sides. Therefore C² relative compactness on a patch containing that direction is impossible. Uniform C^{2,β} bounds for positive β would imply such compactness on a smaller patch and are excluded. Uniform bounded second derivatives alone, individual finite-separation smoothness, and the unknown Hessian transition are not contradicted. The optional isotropic mass rescaling preserves density one and the fixed asymptotic constant exactly, and its scale tends to one. Local uniform convergence is the correct conclusion for that rescaled family.

## 6. Checks and disposition

- All frozen author inputs verified; see `FROZEN_INPUT_VERIFICATION.json`.
- The three author scripts replayed byte-for-byte: 20 + 12 + 8 checks.
- `independent_algebra.py` passes 26 additional exact symbolic checks, including the full parabolic Hessian, crease barrier and matching derivatives, ODE exponents, radial density, a non-unit-principal-axis ellipsoid calibration, and normalization rescaling.
- The analytic claims depend on the mathematical arguments above and the cited primary results, not on finite algebra checks or a numerical PDE experiment.

**Recommended disposition:** retain `unsolved`, with five substantive author turns consumed. The partial results can be preserved in a clearly scoped research report. Do not mark the original cone/Hessian classification `claimed_solved`, assert discovery/priority, or describe the local or collision-limit profiles as the finite-separation source cones. There are no mandatory mathematical revisions to the frozen package under that disposition.
