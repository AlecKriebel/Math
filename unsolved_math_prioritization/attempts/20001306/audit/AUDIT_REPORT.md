# Independent adversarial audit: polar-zonoid intersection bodies

Problem 20001306 / AIM-CONVEX_GEOMETRY-0038, queue rank 511. Audit date: 3 October 2026.

## Verdict and permitted scope

**PASS — partial results only. The full genericity problem remains unsolved, with five substantive attempts completed (canonical queue status: `unsolved`, turns: `5/5`).**

No mathematical blocking defect was found in the frozen proof. In particular, the four-dimensional theorem is valid in the explicitly specified fixed-axis revolution-body space. It does not establish unrestricted four-dimensional density or the conjecture for all dimensions. The finite rational-certificate result is an existence and verification result, not an effective universal density construction.

The author's descriptions of the bounded attempt as “exhausted” are not an instruction to create a noncanonical queue status. Publication metadata and the queue must use `unsolved` and `5/5`. No full-solution or first-discovery claim is warranted.

The author manifest's six listed files were checked before and after the audit. They remain byte-for-byte unchanged. Audit files are separate from the frozen author files. No remote writes were performed.

## 1. Source and problem identity

The locally available official AIM workshop PDF identifies the relevant item as Problem 10 on printed page 3. It asks for Baire-generic non-polar-zonoidality of the intersection body of an origin-symmetric convex input. The missing digit in the imported item number is not a different problem.

Schneider's 2001 paper, printed pages 264–266, supplies the intended setting in dimensions at least three, the Banach–Mazur compactum, and the equivalence between the Busemann-area formulation and the zonoidality of a positive scalar multiple of the polar intersection body. Its distinction between known openness and unknown density agrees with the frozen note. Its nearby exceptional bodies rule out substituting “only ellipsoids are exceptional” for the target.

Alfonseca's 2013 paper, Proposition 1 and Corollary 2, requires convexity, origin symmetry, revolution symmetry, and radial smoothness only near the axis. It supplies exactly the four-dimensional flat-top criterion used here. Its discussion also expressly distinguishes intersection bodies in the radial-closure class from intersection bodies of convex inputs. Neither the low-dimensional characterization of the larger class nor examples in that class settle the present problem.

The dimension-two counterexample to an unrestricted reading is correct: the intersection-body operation is a rotation and dilation, and every centered planar convex body is a zonoid. There is no analogous exemption of dimension three; the three-dimensional cube witness uses an actual convex input.

Source links:

- AIM, *Fourier analytic methods in convex geometry*, Problem 10: https://aimath.org/WWN/fourierconvex/fourierconvex.pdf
- Schneider, *On the Busemann Area in Minkowski Spaces*: https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.42/no.1/b42h1rsc.pdf
- Alfonseca, *Intersection bodies that are not polar zonoids: a flat top condition in dimensions four and six*: https://arxiv.org/abs/1303.3813
- Schneider, *Crofton measures in projective Finsler spaces*, Section 5: https://home.mathematik.uni-freiburg.de/rschnei/Wuhan.pdf

This audit independently checked the local primary sources needed for the mathematics. It did not repeat the author's live repository-duplication search or the separate 2026-preprint search. Those are bounded author-stage provenance claims, not independently recertified worldwide literature coverage, and the cited recent preprint is not an input to any proof accepted below.

## 2. Topology, continuity, and affine quotient

All bodies in the ambient space are full-dimensional and origin-symmetric; therefore the origin is interior and all reciprocal radial expressions are defined. The Hausdorff space allowing lower-dimensional centered convex sets is complete, and its full-dimensional subspace is open. This proves the required Baire property.

For an inner radius r and Hausdorff error delta < r, the support-function inequalities indeed give

    (1 - delta/r) K subset L subset (1 + delta/r) K.

Section-volume monotonicity then gives equation (2), including its reciprocal-error bound and its lower section-volume bound. This is a uniform estimate around a full-dimensional body; it does not assert continuity at a degenerate limit.

The positive cosine-transform cone is closed: integrating a convergent sequence of its functions bounds the positive generating masses, and weak-* compactness recovers a positive even limit. Thus the exceptional set is closed and its complement is open. In this Baire space, residuality of that open complement is equivalent to density. Closedness by itself gives neither density nor residuality.

The affine covariance formulas in (3) are correct. The Banach–Mazur comparison can be made using representatives sandwiched between K and arbitrarily small dilations of K. Together with the inner-radius estimate, this proves equivalence of the density questions in the Hausdorff space and the affine quotient. It does not rely on an unjustified open-mapping assertion.

## 3. Finite rational certificates

The signed-measure separation statement has the correct signs and follows from closed-cone separation and cosine-kernel symmetry. Symmetrizing the separating measure preserves both its evaluation and the cone inequality.

The rational refinement is valid even though a nonzero rational vector need not have rational unit normalization. The homogeneous extension absorbs its length. Approximate the positive and negative measures separately, approximate atom positions by nonzero rational vectors in a compact annulus, and approximate the finitely many weights rationally. Both the homogeneous evaluation and the entire cosine polynomial converge uniformly in the required senses.

Adding a rational multiple d of the coordinate absolute-value sum repairs a possible error of size epsilon < d because the l1 norm is at least one on the Euclidean unit sphere. The chosen evaluation margin bounds the additional functional by less than eta/4. It therefore preserves strict negativity and gives strict positivity of the polynomial away from the origin.

The finite exact polyhedral test is sound: every sign cone intersected with the rational cube is a bounded rational polytope, and the relevant expression is linear on each piece. Testing its vertices establishes nonnegativity on the piece; homogeneity covers all vectors. Degenerate sign pieces do not invalidate this argument.

The neighborhood bound (5) uses the correct coefficient norm sum |a_i| |q_i|. It remains essential to obtain certified values of the relevant section volumes for a general input. The proof correctly does not treat a numerical plot, a finite directional mesh, or unbounded coefficient search as such a certificate.

## 4. Cube obstruction

The sign-vector inequality follows from convexity, coordinate sign symmetry, and permutation averaging on the simplex. The constant gamma_n agrees with its binomial expression. The diagonal section-volume formula includes the necessary coarea factor sqrt(n); this factor cancels against the homogeneous evaluation at a sign vector. Thus (7) has the correct normalization.

The exact three-dimensional value is -1/3. Dimension four gives precisely zero for this particular certificate and permits no non-zonoid conclusion. Strict values in dimensions 5 through 64 are finite verified instances. No infinite-dimensional extrapolation is made. These are instances of Schneider's published obstruction, as the attribution states.

## 5. Harmonic operator normalization and perturbations

For the stipulated unnormalized operators, the distributional identity is

    (Delta + n - 1) C = 2 R.

The factor 2 is the derivative jump of the absolute-value kernel across its equator. Constant densities provide an independent normalization check: R1 = |S^(n-2)| and C1 = 2 |S^(n-2)|/(n-1). These identities exclude an unnoticed probability-area normalization or an imported incompatible source constant.

On even spherical harmonics, the Radon multipliers are nonzero and their inverses grow only polynomially. The same is true for the cosine transform. The asserted smooth/distributional inverses and their commutation with the spherical Laplacian are therefore justified.

Differentiating m/(A+sRq), with m=n-1 and A=|S^(n-2)|, gives the generating-density constant and first variation in (10), and the harmonic specialization in (11). The convexity test in (12) is the tangent Hessian of the homogeneous gauge, with the stated sign and factor. For fixed smooth q, sufficiently small perturbations are convex and have positive smooth generating density. Increasing frequency requires estimates not supplied by fixed-q differentiation. The frozen note identifies this gap rather than hiding it.

The general-base variation includes a variable reciprocal-square factor inside C inverse; cancellation with R cannot simply remove it. Thus this route does not prove a perturbation theorem near every exceptional body.

## 6. Restricted four-dimensional theorem and distributional endpoint audit

Let Y_4 be the fixed-axis invariant full-dimensional subspace used in the proof. It is relatively closed in the ambient space and Baire. Rotational averaging proves that the maximum axial coordinate equals the radial height h. Thus

    (b/h) K subset K intersect {|x_4| <= b} subset K

is a valid sandwich. The truncated bodies are convex, full-dimensional, origin-symmetric, and invariant about the same axis. For 0 < b < h, continuity of the original radial function gives a genuine neighborhood of each pole on which the new radial function is b/t (using t > 0 at the upper pole). Hence the published criterion applies without global smoothness or strict convexity. Taking b upward to h proves density in Y_4, and ambient openness proves relative openness.

The inverse-transform verification is also correct independently of that criterion. With H(t)=integral_0^t rho(u)^3 du, the four-dimensional zonal Radon formula gives the constants in (13). A possible endpoint/atom loophole can be closed explicitly:

1. Extend H oddly. Set J(t)=t^2/H(t) with J(0)=0, and G=J'. For continuous positive rho, G is globally continuous, even, and has limit 1/rho(0)^3 at zero.
2. The fundamental theorem of calculus gives integral_0^x G(t) dt = x^2/H(x). Substitution into the zonal Radon formula proves that (3/(16 pi^2))G is the inverse Radon transform of f_L globally, including endpoints by limits. No missing integration constant or pole-supported atom is available.
3. Near a truncated pole, H and G have smooth extensions in the t coordinate. Their compositions on the spherical cap are smooth. Applying the distributional Laplacian there therefore gives the ordinary displayed smooth density, without an extra endpoint delta term.
4. At the pole, direct differentiation yields G'(1)-G(1)=2b^6/H(1)^3. The term (1-t^2)G'' vanishes there and gives exactly

       mu_L(1) = -9 b^6 / (16 pi^2 H(1)^3).

5. This density is negative on a nonempty open cap, not just at a measure-zero pole. Possible singular terms elsewhere cannot cancel a negative pairing with a nonnegative smooth test function supported inside that cap. Uniqueness of the even inverse cosine distribution rules out a different positive representing measure.

For the last certificate statement, choose the test function even by using both caps. Its inverse cosine transform is smooth and defines a finite signed measure nu, with Cnu equal to the nonnegative test function. Self-adjointness then gives the required strictly negative evaluation. This makes the link to Proposition 1 rigorous.

Y_4 is a proper symmetry-restricted class. No step transfers its density to the full ambient space. The strongest accepted result is precisely the relative theorem, attributed as a corollary of Alfonseca.

## 7. Six-dimensional obstruction to the same argument

The cylinder's radial formula and moment definitions agree with the source criterion. Direct antiderivatives give lower and upper h contributions 1 and 1/4, and lower and upper k contributions 1/3 and 1/2. Therefore

    h = 5/4, k = 5/6, r(1) = 1, h r(1) - 2 k^2 = -5/36.

The source's displayed h evaluation does not equal its own displayed integrals. The frozen note's correction is mathematically justified and does not reverse the source's conclusion that this sufficient pole test fails. Continuity of the moments means sufficiently small axial truncations of this cylinder still fail that test. Failure of a sufficient condition does not establish zonoidality, and the note correctly says that the source proves this cylinder non-polar-zonoidal by a separate inverse-transform calculation.

## 8. Verification scope and publication controls

The frozen exact verifier was run from a separate copy so that its output-writing behavior could not change the frozen package. Its output matches the frozen result byte-for-byte. Independent controls recompute the central claims rather than treating the author's successful assertions as a proof of themselves. The accompanying `calculation-controls/independent_results.json` records the exact checks and limitations.

The independent script requires Python and SymPy (tested with SymPy 1.14.0). From the package root, run:

    python3 audit/calculation-controls/independent_calculations.py

If author files are stored elsewhere, supply `--author-dir` with their directory. The script writes only its own `independent_results.json`; it does not overwrite author files. The author's original verifier requires only the Python standard library.

Positive and boundary controls include the Euclidean ball normalization and the zero four-dimensional cube certificate. The negative cap and strict cube signs are obstruction controls. Symbolic or universal identities are distinguished from the author's sixteen finite endpoint-jet specializations. Neither the computational suite nor this audit claims to decide the full genericity conjecture or to certify a worldwide novelty search.

Public delivery should include only the authored proof, explanatory notes, exact code/results, manifests, and the sanitized audit/control artifacts. It should exclude downloaded PDFs, complete source transcriptions, catalog or prior-report extracts, and other local context. The audit does not authorize remote publication; that remains a separate gate.

## Remaining mathematical task

For every fixed n >= 3 and every exceptional convex K, construct arbitrarily Hausdorff-close convex L whose actual intersection body is not a polar zonoid, or refute that density statement. This universal perturbation step remains open in the package. The accepted partial results do not remove it.
