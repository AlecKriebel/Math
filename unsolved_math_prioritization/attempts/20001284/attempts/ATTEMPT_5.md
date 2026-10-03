# Author attempt 5: an exact antipodal-switching construction and the symmetry barrier

2026-10-03 UTC. Goal: produce all-plane perimeter collisions, then determine whether origin symmetry can be preserved. Outcome: a complete nonsymmetric construction, credited as an instance of the known Ryabogin–Yaskin phenomenon; the switching mechanism collapses under the required origin symmetry. No counterexample to the source problem.

## Explicit smooth profiles
Take c=99/100 and, for a unit vector v, define
ψ_v(u)=exp(1/(1−c)−1/(u·v−c)) if u·v>c, and ψ_v(u)=0 otherwise.
This is C∞, is analytic inside its cap, vanishes to infinite order at its cap boundary, is positive inside, and has its unique maximum 1 at v. Moreover ψ_{−v}(u)=ψ_v(−u).

Put v=(1,2,3)/√14. The eight caps centered at ±e₁,±e₂,±e₃,±v are pairwise disjoint. Indeed intersection of two caps would force the center dot product to exceed 2c²−1>0.96, whereas for distinct nonopposite chosen centers that dot product is at most 3/√14<0.81.

For R>0 and sufficiently small δ>0, set
ρ_K=R+δ(ψ_e₁+2ψ_e₂+3ψ_e₃+4ψ_v),
ρ_L=R+δ(ψ_e₁+2ψ_e₂+3ψ_e₃+4ψ_{−v}).
They define distinct C∞ star bodies. Choosing δ small enough in C² makes both strictly convex by the quadratic-form criterion proved in attempt 4. Their radial functions are not even.

## Exact equality of every central-section perimeter
On a great circle the disjoint caps never overlap. The perimeter integrand therefore splits into the constant R plus four separate bump increments. Each bump increment for center z and height a is
sqrt((R+aψ_z)²+a²(∂sψ_z)²)−R.
Replacing z=v by −v merely shifts this increment by the antipodal map u↦−u on that circle. Its integral is unchanged. The other three terms are identical, so P(ρ_K)(θ)=P(ρ_L)(θ) for EVERY θ.

This is exact, not asymptotic or a finite-normal test.

## Noncongruence, including translations
First any Euclidean isometry between K and L must fix the center 0 of the underlying spherical patches of radius R. Here is a detailed reason that no extra such patch can hide inside a bump. If an open patch inside a cap belonged to a sphere of radius R centered at a, the analytic identity
|ρ_L(u)u−a|²=R²
would extend throughout that connected cap. At its boundary, ρ_L=R and all derivatives of its bump vanish. Taking a tangential derivative along the sphere at any boundary point gives a·w=0 for every tangent vector w there. Hence a is parallel to every boundary point; since the boundary contains nonparallel points, a=0. The identity would then force ρ_L=R throughout the cap, contradicting positivity of the bump. The same argument applies to K.

An isometry sends an open radius-R spherical patch of K to one of L. A nonempty subpatch must either lie outside the finitely many cap boundaries or inside a cap. The preceding argument excludes an interior cap patch with a different center; an exterior patch has center 0. Thus the isometry's translation vector is zero.

The remaining orthogonal map preserves radial values and radial local maxima. The four distinct positive local-maximum heights above R are δ,2δ,3δ,4δ. In both bodies the first three occur uniquely at e₁,e₂,e₃. Therefore the orthogonal map fixes all three basis vectors, so is the identity. It cannot send the fourth maximum v to −v. Thus K,L are noncongruent.

## Attempt to enforce the required symmetry
The radial evenizations are exactly equal:
(ρ_K(u)+ρ_K(−u))/2=(ρ_L(u)+ρ_L(−u))/2.
This equality follows directly from ψ_{−v}(u)=ψ_v(−u). More generally, independent antipodal switching only permutes the two local profiles in each antipodal pair. For an already even radial function the two profiles are identical, so such switching makes no change at all.

This proves a precise obstruction to this construction family, not to all possible counterexample constructions. Symmetrization is not asserted to preserve the original perimeter data; it simply identifies these two bodies. The source requires origin symmetry, so the construction does not answer it negatively.

## Literature credit and terminal disposition
Ryabogin and Yaskin, “On counterexamples in questions of unique determination of convex bodies,” Proc. Amer. Math. Soc. 141 (2013), 2869–2874, Theorem 2.4, already establish noncongruent smooth convex examples sharing all relevant central-section intrinsic volumes when origin symmetry is dropped. The present switched-cap construction is a self-contained check of the relevant failure mechanism, not a novelty claim or rediscovery presented as a solution.

After five substantive author attempts, the original all-plane, origin-symmetric global star-body uniqueness question remains UNSOLVED. The strongest positive result here is the cutoff-independent C² local theorem of attempt 1, still requiring final fresh audit before publication. No claim is made about arbitrary C¹ bodies, nonsmooth/infinite perimeter interpretations, or historical priority.
