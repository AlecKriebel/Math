# Author research turn 1: exposed faces and axisymmetric cones

Date: 2026-10-01. Status: partial theorem; full target active. Completion estimate: 20% of the full source target (subjective). No novelty claim. This turn develops a proof route; source retrieval and packaging do not count separately.

## 1. General convex tangent-cone reduction

Let u be a finite convex function on a neighborhood of p, and set K_p = ∂u(p). Then K_p is a nonempty compact convex set and

    τ_p(x) = lim_{r↓0} [u(p+rx)-u(p)]/r = max_{y∈K_p} y·x.

The limit is locally uniform in x. Indeed, one-dimensional convexity gives the directional limit. The directional derivative is the support function of the subdifferential. Local Lipschitz bounds on u give equicontinuity of the rescaled functions on each fixed compact set, upgrading pointwise convergence to uniform convergence. For an Alexandrov atom of size a_p,

    |K_p| = a_p.

Also, the rescaled Monge–Ampère measure is

    M_{u_{p,r}}(E) = M_u(p+rE).

For bounded E and sufficiently small r, it consists of r^n times Lebesgue measure plus the atom a_p delta_0. Thus M_{τ_p} = a_p delta_0. This condition alone constrains the volume of K_p, not its shape. It does not determine the cone.

If v = u* is the Legendre transform, Fenchel equality gives

    K_p = { y : v(y) = p·y-u(p) }.

For the polyhedral examples this is the relevant convex component of the dual contact set. If u is affine on [p,q], then

    K_p ∩ K_q = { y∈K_p : y·(q-p) = u(q)-u(p) }.

This is an exposed face of K_p, with outward direction q-p. To verify equality, the subgradient inequality at q gives ≤. Equality makes the supporting affine function at p also support at q, proving membership in K_q. The reverse inclusion follows by evaluating the two supporting inequalities at p and q. In particular, a shared face of positive dimension forces nondifferentiability of τ_p along the ray toward q.

These statements are standard convex duality, recorded to prevent confusing a reformulation with a classification.

## 2. Localization lemma for a body on one side of a plane

Let H = {y_n=0}, H+ = {y_n>0}. Suppose K is a compact convex body contained in {y_n≥0}, with nonempty interior in H+. Assume that near K∩H+, K is the zero set of a nonnegative convex solution

    det D²f = 1_{f>0}

in H+. Suppose additionally that K∩H is a Euclidean closed (n−1)-ball D of radius R>0. Then every non-singleton exposed face of K equals D.

Proof. Let F be a non-singleton exposed face, obtained by intersecting K with a supporting hyperplane S. Any extreme point z of F in H+ is also an extreme point of the contact set on S inside a sufficiently large bounded convex subdomain of H+. Since F has another point, segments toward that point show the contact set on S is not a singleton in that subdomain. Caffarelli–Savin localization, in the form of Mooney Proposition 2.7, says such a contact set has no extreme point in the PDE domain. Contradiction. All extreme points of F therefore belong to H. Since F is compact convex in finite dimension, it is the convex hull of its extreme points; hence F⊂H.

If S≠H, its restriction to H is a genuine supporting hyperplane of the ball D. It meets D at one point, contradicting that F is non-singleton. Therefore S=H and F=K∩H=D. ∎

The use of a bounded subdomain is legitimate: choose a half-ball containing K away from its spherical boundary. Extreme points in H+ remain interior PDE points; points in H are excluded. No extension of the PDE across H is assumed.

## 3. Application to the source's axisymmetric two-mass construction

Normalize the two mass locations to ±e_n, and let the dual obstacle be |y_n|. Choose the rotation-invariant construction from Mooney Proposition 3.6. Its contact set is the union of convex bodies K+ and K− in the two closed half-spaces. The construction is invariant under O(n−1) rotations around the mass axis and reflection in H. Uniqueness of each bounded obstacle problem, followed by its invariant exhaustion, preserves these symmetries.

The shared contact set D = K+∩H = K−∩H is a compact O(n−1)-invariant convex set with nonempty relative interior, and thus a disk of radius R>0. The nonempty relative interior follows from Proposition 3.6 for n≥3. In H+, f=v-y_n is nonnegative, has zero set K+, and solves the one-plane obstacle equation. The lemma applies.

For the mass p=+e_n, K_p=K+. Therefore its graph tangent cone τ_p is C¹ on R^n minus the inward ray {−t e_n:t≥0}, and is nondifferentiable at every nonzero point of that ray. Its subdifferential there is precisely D. For p=−e_n the statement is reflected.

Why C¹, rather than only differentiability? A support function is differentiable at a nonzero direction exactly when its exposed face is a singleton. If x_j→x through directions with unique maximizers y_j, compactness gives subsequential limits, each maximizing y·x. Uniqueness at x forces y_j→y. Hence the gradient is continuous.

There is also an exact transverse first-order cusp. In this normalization, for s>0 and η=(η',η_n),

    lim_{t↓0} [τ_p(−s e_n+tη)-τ_p(−s e_n)]/t = R|η'|.

This is the support function of the exposed disk D. The statement describes the directional tangent at a point on the exceptional ray, not the higher-order behavior of u near the mass.

The construction also works with the appropriate translated separating plane and affine terms, but the symmetric normalization is sufficient for this partial result.

## 4. Sharp obstruction to completing the route by convex geometry alone

The hemisphere body

    K = { y : |y|≤R, y_n≥0 }

has all the compactness, rotational symmetry, and exposed-face conclusions above. Its support function is

    h_K(x) = R|x| if x_n≥0,
             R|x'| if x_n≤0.

This is C¹ away from the negative axis, yet fails to be C² across {x_n=0, x'≠0}: the second normal derivative is R/|x'| from above and zero from below. Therefore the exposed-face conclusion cannot itself prove the smoothness sought by Mooney–Rakshit. This hemisphere has not been proved to occur as a source PDE contact body; it is a counterexample only to the proposed purely convex-geometric implication.

For the actual PDE, possible additional loss of higher regularity is concentrated at support directions whose unique maximizer lies at the rim ∂D. Interior-chamber free-boundary regularity does not cover those rim points. The new work required is a crease/rim regularity theorem or a different mechanism controlling this transition.

## 5. Exact residual target and next route

The full polyhedral/Y-shaped classification remains unresolved in this attempt. Even for two masses, the C∞ regularity away from the inward ray and the Hessian transition at the rim are not proved here. This is not a final unsolved verdict; four substantive author turns remain.

Next route: derive the axisymmetric reduced PDE and the asymptotic compatibility equation, and test whether a partial Legendre transform exposes a boundary regularity mechanism beyond the convex localization lemma. Independent verification must follow any complete candidate. This partial lemma has not yet received independent review.
