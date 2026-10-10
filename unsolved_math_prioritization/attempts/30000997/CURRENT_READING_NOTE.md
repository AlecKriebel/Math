# Mandatory reading note and audit response

2026-10-03. This note corrects the reading of the frozen five-turn author packet at commit `3f5d67dba43eac1c01a48a3481d8153b319fee02`. Historical files are not rewritten. The original global implication remains unresolved, with the budget exhausted at 5/5. These are review corrections, not a sixth research attempt.

## C1. Tensor normalization

Throughout this packet, for c=d_g²/2 and q=exp_p(v) off the cut locus, define

S_packet(v;u,w) = −D_v²[A(v)(u,u)][w,w],
A(v)=Hess_p c(p,exp_p(v)),

where the Hessian is in the first argument with the second endpoint fixed before v is varied. The endpoint vector in the coordinate tensor is η=Dexp_p(v)w. Thus

S_packet = (−c_ij,k'l' + c_ij,a' c^(a'b) c_b,k'l') u^i u^j η^k' η^l'.

The mixed nullity condition is c_i,j' u^i η^j'=−g_p(u,w)=0. The tangent directions must not be identified with unscaled unit endpoint vectors.

In [Kim–McCann, *Towards the smoothness of optimal maps on Riemannian submersions and Riemannian products*, Lemma 2.5](https://www.math.toronto.edu/mccann/papers/RiemSub.pdf), the cross-curvature convention uses −2 times the fourth cost derivative. For the same cost and corresponding vectors,

cross_KM = 2 S_packet.

Consequently the finite witness has S_packet=7/10−8/π² and cross_KM=7/5−16/π². The diagonal orthonormal-null controls are S_packet=2K/3 and cross_KM=4K/3. Their signs and null-pair conditions agree. This factor-two convention distinction is separate from scaling the cost d²/2 to d². All computed values in the frozen packet use S_packet, consistent with its displayed coordinate definition; no numerical value of that tensor is being changed.

## C2. Actual smooth squared-distance domain

The opening hypothesis of TURN_5.md must be read as follows:

Fix a surface point p and v in the interior tangent injectivity domain D_p, so the geodesic from p to exp_p(v) is uniquely minimizing and nonconjugate.

Apply this hypothesis everywhere the general Jacobi Hessian is identified with derivatives of the actual smooth squared-distance cost, including the generalized formulas in TURN_1 and TURN_5. The later global criterion in TURN_5 already quantifies v in D_p and requires no algebraic correction.

A minimizing nonconjugate geodesic alone is insufficient: it can end at a cut point with another minimizer, where squared distance need not be differentiable. Along a selected nonconjugate branch outside D_p, a Jacobi expression can define an extended Hessian without representing the actual squared-distance Hessian. Nonconjugacy does not establish uniqueness or global minimization.

## Equatorial uniqueness and admissibility, stated in full

For 0<a<1/6, put f_a(x)=cos x+a cos³x sin⁴x on the latitude interval and use longitude period 2π. The resulting smooth metric satisfies g_a>=g_round as quadratic forms, including at the smooth poles by continuity. Take equatorial endpoints whose shorter longitude separation is 0<r<π.

Every joining curve γ has L_a(γ)>=L_round(γ)>=r. The shorter equatorial arc has L_a=r, so it is minimizing. If another g_a minimizing path existed, its length comparison would force L_round=r. On the round sphere the two non-antipodal endpoints have a unique minimizing arc, so that path must be the same equatorial arc. This proves uniqueness; it is not inferred merely from a nonzero Jacobi determinant.

Along that arc K=1. The transverse exponential Jacobi factor is sin r/r, which is nonzero for 0<r<π. Thus the path is also nonconjugate and its initial tangent belongs to D_p. The actual squared-distance cost is smooth on a neighborhood of the pair. In particular, r=π/2 and the endpoint vector (2/π)∂x used in the finite witness are admissible. The antipodal case r=π is excluded. This reasoning makes no assertion about cut loci at off-equator source points.

At the displayed pair, the null-direction tensor is strictly positive on the compact set of normalized orthogonal pairs. Smooth inverse-exponential coordinates and uniform continuity preserve that positivity on a sufficiently small product U×V inside the smooth-cost domain. The negative full pair is already in this product and persists locally. This proves the local product-domain separation, not global A3w for the complete sphere.

## C3. Numerical terminology

The historical program field `safe_no_conj_poles` is only a heuristic filter for solver success, a positive endpoint Jacobi value, and sampled pole avoidance. It certifies neither absence of earlier conjugate points nor minimization before the cut locus. The code and raw diagnostic JSON remain unchanged for provenance.

The rejected shooting examples should be described as **numerically suspected nonminimizing branches**. Approximate shorter competitors have not been validated by interval bounds or exact endpoint matching. One coarse negative tensor value also changed sign on refinement. These facts justify rejecting the samples as certified evidence; they prove neither global A3w nor its failure. No numerical diagnostic is needed in any retained exact theorem.

## C4. Prior credit and scope

[Figalli–Rifford–Villani, *On the Ma–Trudinger–Wang curvature on surfaces*, §§2 and 6.1](https://people.math.ethz.ch/~afigalli/papers-pdf/On-the-Ma-Trudinger-Wang-curvature-on-surfaces.pdf), already develops Jacobi-Hessian representations, two-dimensional angular MTW formulas, and symmetry-geodesic variations on surfaces of revolution. This machinery is prior art. Its quarter-period calculation agrees with the relevant mixed coefficient here after translating basis and convention; the method must not be claimed as new.

The flat-product obstruction is likewise prior art in the cited Kim–McCann paper. No novelty or priority certification has been obtained for the particular elementary warp, local separation, finite witness, or equatorial positivity interval. The audit accepts correctness within the stated partial scope, not a new solution of the global conjecture.

## C5. Administrative state provenance

The frozen remote TURN_STATE.json is 226 bytes; the historical local operational version is 266 bytes. They have different ancillary fields but agree on five author turns, exhaustion, and the unresolved global target. All 18 other entries in the frozen remote directory matched the corresponding local Git blobs, and all 17 author-manifest entries matched their SHA-256 hashes in the full audit.

Both state versions are preserved under provenance/ and bound in STATE_PROVENANCE.json. The original files are not silently harmonized. CURRENT_STATE.json is an additional current interpretation after the audit. Therefore no byte-identical whole-directory local/remote claim is made.

## Audit binding and review status

The full independent audit manifest has SHA-256 `a13ccb62178706582faaca66a12f1be65558a8b032876f90f99d0449254e9aa5` and reviews immutable author commit `3f5d67dba43eac1c01a48a3481d8153b319fee02`. Its report, corrections, input binding and controls are preserved in audit/initial/. The audit accepted the partial mathematics subject to C1/C2 and preservation of scope; the present corrected reading awaits narrow re-review. Global status remains exhausted/unresolved at 5/5.
