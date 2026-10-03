# Independent audit of Delone cluster group reductions

Problem 20001782, AIM-GEOMETRY-0120, queue rank 458. Audit date: 3 October 2026.

## Verdict

**PASS as an accurately scoped five-attempt partial-results package.** No mandatory mathematical repair was found. All five arguments below were independently checked; the examples meet the full stated Delone and centered-regularity hypotheses. The original dimension-only group-order problem remains unresolved. **HOLD any promotion to a solved problem, a counterexample to the original problem, or a novelty/comprehensive-literature claim.** None of those stronger claims is made in the frozen package.

This audit verifies the five existing arguments and examples. It is not a sixth proof-search attempt. The reviewed mathematical files remain unchanged.

## Material and integrity

The ten-file mathematical package was integrity-checked: byte counts, SHA-256 digests, and Git blob SHA-1 values all match the reviewed version, commit `a3a0c79d408ae120614dabedd7a8f8e60565949d`, tree `984eb407160a7d7a0203735df3cbd9b496750a49`.

Running the frozen `verify_examples.py` under Python reproduces `checks.json` byte for byte, including its 6,960-byte length. The reported parameter-case total is exactly 30 + 12 + 11 + 100 + 480 = 633. These are supplementary controls, with scope detailed below.

The upstream machine-generated partial report was considered only as historical context, not independent proof or evidence of novelty. The mathematical audit checked the identified package; it did not independently repeat the historical repository-search checks.

## Source and convention audit

The publisher version of Dolbilin, Garber, Schulte and Senechal, *Bounds for the Regularity Radius of Delone Sets*, was successfully read directly. It confirms the exact-radius convention in Section 1, centered groups and equivalence in Section 2, and the target in Problem 5.1. In particular, r is the largest admissible packing radius, while R is the smallest admissible covering radius; clusters are closed. The source distinguishes centered equivalence from congruence of unmarked finite sets. Its Conjecture 5.2 is restricted to sufficiently large dimension. The package preserves these distinctions. [Publisher version](https://link.springer.com/article/10.1007/s00454-024-00666-6)

The official AIM workshop report, page 3, independently confirms the dimension-only group-order question and the sharp dimension-two and dimension-three values 12 and 48. [AIM report](https://aimath.org/pastworkshops/softpackrep.pdf)

The 2025 CMS abstract discusses conjectures verified for special families, not a general solution. The March 2026 Müller preprint states the optional Jordan index bound 25^(q^2); the present reductions can instead use an abstract classical Jordan constant. [CMS abstract](https://www2.cms.math.ca/Events/winter25/abs/pdf/rpi-es.pdf), [Müller preprint](https://arxiv.org/abs/2603.15813)

The exact catalogue URL and original AIM item URL could not be retrieved with the audit's web tool. Consequently, the original item's precise numbering and the historical browser 403 are not independently re-certified here. The accessible primary sources are sufficient to verify the mathematical target. Targeted current searches found no later general resolution, but this remains a bounded retrieval result, not proof of exhaustive literature coverage. No substantive scope correction is required.

## Preliminary finite-group justification

The use of finite subgroups of O(d) at radius exactly 2R is valid. Here is a complete independent boundary-safe proof.

Translate x to 0. Uniform discreteness makes every bounded cluster finite. If C_0(2R) were contained in a proper hyperplane V, local finiteness would give an epsilon > 0 for which C_0(2R+epsilon) = C_0(2R). For a unit normal n to V, cover z = (R+epsilon)n by an R-ball centered at y in X. Then |y| <= 2R+epsilon, so y lies in V, whereas its distance to z is at least R+epsilon > R. This is a contradiction. Thus the cluster spans the ambient space. Its centered orthogonal group acts faithfully on its finite point set, hence is finite.

Closed balls matter at equality, and the epsilon argument handles that boundary correctly. No 2R-regularity is needed for this preliminary lemma.

## Attempt 1 passes

For X_L = Z^k x (LZ)^(d-k), with 1 <= k < d and L > 1, the shortest nonzero displacement has length 1, so the exact packing radius is 1/2. Nearest-point distances separate by coordinate. Rounding each coordinate into its nearest lattice position gives covering radius at most one half of sqrt(k+(d-k)L^2); the box center attains that distance. The displayed R is therefore minimal.

Translations by X_L act transitively and preserve X_L. They give marked-center cluster equivalences for every radius, including the cluster at exactly 2R.

If a >= 2 and L > a/2, every point of C_0(ar) has zero long coordinates, and the k unit basis vectors belong to that cluster. Its rank is exactly k. Also ar = a/2 < L <= 2R, so the radius relevant to the later short-span argument is genuinely within the 2R-cluster. For a < 2 the cluster is the center alone.

The exact group computation is valid, including for nonintegral L. The global shortest shell of C_0(2R) is {+/-e_i: i <= k}; its span V is invariant and the restriction to V is a signed permutation. Orthogonality preserves V-perp. Because L <= 2R, C_0(2R) intersect V-perp contains the cross-polytope shell {+/-L e_i: i > k}; it is the shortest shell within that intersection and forces another signed permutation. Conversely, every such block signed permutation preserves X_L and the centered ball. Therefore

S_0(2R) is B_k x B_(d-k), and |S_0(2R)| = 2^d k! (d-k)!,

where B_j denotes the signed permutation group in j coordinates. Potential coincidences between radii of other shells do not create extra mixing: preservation of V was already forced by the unique shortest shell.

This is a correct obstruction to dimension-only short-radius rank assertions, not to the original group-order problem.

## Attempt 2 passes

For P = C_x(ar)-x, with ar <= 2R, every g in G = S_x(2R) preserves P by preservation of distance from the marked center. Thus V = span(P) and V-perp are invariant. Taking H to be the image of restriction to V gives the stated exact sequence. An element of the kernel K is determined by its action on V-perp, so the embedding K into O(d-k) is faithful.

A basis chosen from the nonzero points of P determines every member of H by its ordered image tuple. Those images are distinct nonzero points of P. Consequently |H| <= (N-1)_k, with no assumption that every candidate tuple is realizable.

The intrinsic k-dimensional radius-r open balls centered at P are pairwise disjoint because their center separation is at least 2r. They lie in the radius-(a+1)r ball in V. Hence N <= (a+1)^k and

|G| <= (N-1)_k |K| <= (a+1)^(k^2)|K|.

For k=d, the kernel is trivial. For k=d-1, its faithful O(1) representation gives |K| <= 2, yielding exactly 2(a+1)^((d-1)^2). Centered 2R-equivalence transfers the rank hypothesis to every center. It is unnecessary for the pointwise bound itself.

The perpendicular polygon example correctly shows that an abstract finite orthogonal kernel can have unbounded order when codimension is at least two. It is explicitly only a finite configuration, with a nondegenerate m-gon understood to mean m >= 3. It supplies no Delone counterexample. Neither an intersection nor a projection has been shown to realize the residual kernel as a lower-dimensional 2R-cluster group, so the refusal to apply the low-dimensional Delone theorem is correct.

## Attempt 3 passes

For a finite abelian A <= O(q), commuting normal operators decompose the real representation into t one-dimensional real characters and s conjugate-pair real planes, with t+2s=q. The exponent e of a finite abelian group is realized by an element: for each prime choose an element of maximal prime-power order and multiply those commuting elements. Hence e <= m if all element orders are at most m.

Each real line has image of size at most 2. Each nonreal character plane has a cyclic rotation image of order dividing e. Faithfulness of the whole representation gives |A| <= 2^t m^s. Since successive terms of 2^(q-2s)m^s have ratio m/4, its maximum is 2^q for 1 <= m <= 4 and is 2^(q mod 2)m^floor(q/2) for m >= 4. The formulas agree at 4. This is a convenient upper bound, not a claimed sharp value for every small m.

Jordan's theorem then gives |G| <= J_C(q)F_q(m(G)). Applying it to K rather than all of G yields the displayed kernel reduction. The family of block rotations (C_m)^floor(q/2) has maximum element order m and group order m^floor(q/2), establishing the asserted exponent obstruction for abstract orthogonal groups. It is not a Delone family.

For the independent metric proof, let g != h and u=g^(-1)h. A nontrivial eigenvalue of u has finite order n with 2 <= n <= ord(u) <= m. If it is exp(2 pi i j/n), then |1-exp(2 pi i j/n)| >= 2 sin(pi/n) >= 2 sin(pi/m). Orthogonal invariance of the Frobenius norm therefore gives ||g-h||_F >= 2 sin(pi/m). Open balls of half this radius in R^(q^2) centered at the group matrices are disjoint. Their centers have norm sqrt(q), so volume comparison gives precisely

|G| <= (1 + sqrt(q)/sin(pi/m))^(q^2).

The separate m=1 case is trivial. All steps are valid. Neither proof supplies the missing uniform element-order bound for Delone groups or their kernels.

## Attempt 4 passes

The propagation lemma uses the correct radius budget. Since 2t <= 2R, centered 2R-equivalence makes both ranks center-independent. Equal nested spans at t and 2t are equal as subspaces at a fixed center. If |x-y| <= t, then C_y(t) is contained in C_x(2t), and both y-x and z-x lie in V_x for z in C_y(t). Thus z-y lies in V_x, giving V_y subset V_x; their equal dimension gives equality. Iteration along a finite graph path proves the component claim and nothing about relative density.

For X = Z x (LZ+{0,1}) x (LZ)^(d-2), L > 3, the exact minimum spacing is 1. The coordinate gap maxima are 1, L-1, and L respectively. Since squared distance to a Cartesian product is the sum of the squared coordinate distances, all upper bounds are simultaneously attained at gap midpoints. Thus r=1/2 and 2R=sqrt(1+(L-1)^2+(d-2)L^2), exactly as stated.

Translations in the displayed coordinate periods, together with y -> 1-y in the second coordinate, act transitively on the whole set. That reflection maps Ln to -Ln+1 and Ln+1 to -Ln. This proves global regularity and therefore centered equivalence of the actual 2R-clusters.

At a residue-zero center the radius-one cluster is exactly {0,+/-e_1,e_2}. At residue one the last sign is reversed. The inequalities L-1 > 2 and L > 2 prohibit any other layer or transverse direction at radius 2. The ranks at 1 and 2 are therefore exactly 2. The condition t=1 <= R also holds, already because 1+(L-1)^2 > 5.

The component of the origin is exactly Z x {0,1} x {0}^(d-2): the only edges are unit first-coordinate steps and the short vertical rung. Its affine span is the e_1,e_2-plane, while its distance from (0,M,0,...,0) tends to infinity with M. Thus the missing covering implication fails in the fully regular setting.

**Additional exact-group verification at radius 2R.** The shortest shell {+/-e_1,e_2} contains a unique antipodal pair. Its symmetry fixes e_2 and sends e_1 to +/-e_1. The perpendicular complement W of their span is invariant. When d >= 3, L <= 2R and the shortest nonzero shell of C_0(2R) intersect W is {+/-L e_i: i >= 3}; it forces B_(d-2). Conversely, the first-coordinate reflection and all these transverse signed permutations preserve X. Hence

S_0(2R) = C_2 x B_(d-2), and |S_0(2R)| = 2^(d-1)(d-2)!.

For d=2 use B_0={1}; the order is 2. At all other centers the groups are conjugate. The example therefore has bounded, explicitly determined 2R-cluster symmetry and refutes only the claimed inheritance step.

## Attempt 5 passes

If the natural representation preserves a full-rank discrete lattice, a lattice basis realizes G as a finite subgroup of GL_d(Z). In the principal congruence kernel modulo 3, any nontrivial torsion element has a power H of prime order p. Write H=I+3^a B with a >= 1 maximal and B nonzero modulo 3.

For p != 3, expanding H^p=I, dividing by 3^a, and reducing modulo 3 leaves pB=0, a contradiction. For p=3 the exact expansion divided by 3^(a+1) is B+3^a B^2+3^(2a-1)B^3=0; both remaining coefficients are divisible by 3 because a >= 1. This again contradicts B nonzero modulo 3. Reduction is therefore injective on every finite subgroup, and counting independent columns gives the stated product for |GL_d(F_3)|.

A rational form suffices: for finite G <= GL_d(Q), the sum of the finitely many lattices gZ^d contains Z^d, is contained in (1/D)Z^d for a common denominator D, and is G-invariant. It is therefore a full-rank discrete lattice.

For X=(Z+{0,alpha}) x Z^(d-1), 0 < alpha < 1/2 irrational, the alternating first-coordinate gaps are alpha and 1-alpha. Therefore r=alpha/2, while coordinatewise gap midpoints give exactly 2R=sqrt((1-alpha)^2+d-1). Translations by Z^d and the reflection x_1 -> alpha-x_1 act transitively, so this is again globally regular. Irrational alpha does not destroy periodicity of this two-coset point set.

For d >= 2, 2R > 1, so the exact cluster contains e_1,...,e_d and alpha e_1. Every cluster point lies in Z^d+Z alpha e_1, so the generated additive module is exactly that module. If sum_i n_i e_i+n alpha e_1=0, the last d-1 coordinates give n_i=0 for i>=2, and irrationality gives n_1=n=0. Thus its abstract integer rank is d+1. The pigeonhole argument applied to N+1 fractional parts produces nonzero elements of magnitude at most 1/N, so the module is nondiscrete.

**Additional exact-group verification at radius 2R.** The nearest nonzero point at the origin is uniquely alpha e_1. A centered cluster symmetry must fix it, hence fix e_1. On e_1-perp the shortest cluster shell is {+/-e_i: i>=2}, forcing the signed permutation group B_(d-1). Conversely all those maps preserve the point set. Thus

S_0(2R) = {1} x B_(d-1), and |S_0(2R)| = 2^(d-1)(d-1)!.

In particular this very group preserves Z^d. The example disproves only that the canonical cluster-generated module must already be a rank-d ambient lattice. It does not disprove the existence of another invariant lattice, a rational form, or some different dimension-only bound on module rank. The frozen text states exactly this limitation.

## What the 633 controls establish

- The 30 rectangular cases check short-cluster rank, count block-preserving coordinate permutations, and test L <= 2R. The program does not search all orthogonal cluster symmetries; the shortest-shell proof establishes that completeness.
- The 12 paired-layer cases check the radius-one and radius-two clusters, their ranks, residue-reflection equivalence at those radii, and forbidden-edge margins. The program does not enumerate all 2R-clusters or prove global regularity; the explicit global isometries do that.
- The 11 quadratic-field cases check the inequalities needed to place the standard basis and alpha e_1 in the cluster for alpha=sqrt(2)-1. Their stored module ranks are the proved formula, not ranks computed by an independent algebraic routine. Irrationality and nondiscreteness are analytic proofs.
- The 100 mod-3 cases check injectivity on selected shear-conjugated cyclic groups in dimension two. They do not prove the general torsion-free congruence-kernel theorem; the binomial argument does that.
- The 480 real-character cases check the closed form of a finite maximum for selected integer q,m. They do not prove the representation decomposition or Jordan theorem.

These limitations are compatible with the README's explicit regression-only disclaimer. The total is a count of parameter cases, not a count of independent theorems or an exhaustive general verification.

## Repairs and disposition

Mandatory mathematical repairs: **none**.

Optional clarity improvements, if a later permitted revision is made:

1. Add the short full-span-at-2R proof above to make the finite-group premise self-contained.
2. Add the exact local groups for Attempts 4 and 5. They make especially transparent why the examples do not contradict the target.
3. State explicitly that H is the image of the restriction homomorphism in Attempt 2; this is already the natural reading of its exact sequence.
4. Expand the eigenvalue step in Attempt 3 to include the elementary inequality for a general nontrivial nth root, as done above.
5. Describe the 633 checks as parameter cases and retain the distinctions in the preceding section.

No such improvement is a prerequisite for accepting the current mathematical claims. Retain the existing labels: five attempts exhausted; partial conditional reductions and route obstructions; original problem unresolved; no novelty assertion; no claim to settle the sufficiently-large-d 2^d d! conjecture.
