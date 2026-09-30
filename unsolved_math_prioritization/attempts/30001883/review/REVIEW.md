# Independent review: circle-free parallel bodies

**Verdict: PASS_SCOPED_CLEARANCE_AND_PATH_OBSTRUCTIONS.** All partial assertions in the frozen artifact are valid within their stated hypotheses. No mandatory mathematical correction is required. The original Minkowski-closure question remains **unsolved, 2/5**. No counterexample to that question, global escape theorem, or novelty claim has been established.

Reviewed artifact: OBSTRUCTION.md, SHA-256 e92216da57fd1ab81fd34260a952f36099993b9985c8c5fc01c2e05f5739a282. The 241 submitted exact assertions reproduce the receipt byte-for-byte. An independently written program passes 711 exact controls. These computations supplement the proofs below and are not configuration-space holding certificates.

## 1. Primary-source scope

I read the complete Maehara contribution in [OWR 44/2011, printed pp.2498–2499](https://ems.press/content/serial-article-files/46358) and visually checked its definition and question on p.2498. The target asks:

> Is it true that for every circle-free convex body K, the set K+B is also circle-free?

Here B is a ball. The object that holds a body is a circular ring undergoing rigid motion. Its disk initially meets the body's interior, its circumference avoids that interior, and it cannot be moved away while keeping that avoidance. Boundary contact is permitted. The statement concerns global continuous escape, not local mobility or the occurrence of circles on the body's boundary.

The later [Maehara–Martini article, pp.273 and 278](https://ems.press/content/serial-article-files/44350), defines a convex body to be compact, convex, and full-dimensional. I checked the full retrieved article's operative definitions and visually inspected p.278. Its attachment convention allows the disk to meet the closed body, and its escape endpoint requires the disk to be disjoint from the body.

The artifact correctly reconciles these conventions. If a disk D misses the open convex set int K, convex separation gives a nonzero normal u and a number a with u·D≤a≤u·K. Translating D in direction −u makes the separation strict for every positive translation time and frees the ring. Thus boundary-only disk contact adds no held configurations. Once the compact convex sets D and K are disjoint, strict separation permits translation arbitrarily far away. Conversely, a sufficiently far ring has its whole bounded disk disjoint from K. These are the required global endpoint equivalences.

The later paper was published in 2018 in the volume dated 2017. It and the original OWR contribution both credit the planar-convex-set-plus-ball result to Maehara. I did not independently reconstruct the original pyramid paper's proof, which the author did not retrieve. Its stated special case can be cited with that access qualification.

## 2. Signed clearance and the correct level set

For a full-dimensional compact convex K, its halfspace description gives
\[
s_K(y)=\max_{\lVert u\rVert=1}(u\cdot y-h_K(u)).
\]
The sphere of directions is compact and the maximand is continuous, so the maximum exists. Taking a maximum of functions that are 1-Lipschitz in y proves the same Lipschitz bound for s_K.

If y is outside K, its Euclidean projection x satisfies (y−x)·(z−x)≤0 for all z in K. The unit vector in direction y−x therefore attains the value dist(y,K), and Cauchy–Schwarz bounds every other direction by that value. If y is inside K, a ball centered at y lies in K exactly when its radius is at most every supporting-plane slack h_K(u)−u·y. This identifies the negative maximum with distance to the boundary. The boundary case follows directly or by continuity.

Support functions add under Minkowski addition, and the centered radius-r ball has constant support r. Consequently
\[
s_{K+B_r}=s_K-r
\]
holds everywhere, including points inside either body. It is not merely an exterior-distance formula. Minimizing over a continuously moved compact circumference gives the continuous configuration clearance \(\phi_{K,R}\), and avoidance of the parallel body's interior is exactly \(\phi_{K,R}\ge r\).

Level-zero escape paths do not, on this argument alone, give level-r escape paths. The artifact correctly keeps this as the central gap. It does not substitute connectedness for path connectedness or a supremal bottleneck value for an attained motion.

The stated far-center bound is sufficient: if K lies in B_L(0) and |c|>L+r+R+1, then projection in direction c/|c| separates the whole radius-R disk from K+B_r, with positive margin. Continuing translation in that direction is valid.

## 3. Necessary geometry of a held parallel body

Suppose r>0 and a ring in plane P holds K+B_r. If P missed int K, convexity would put K entirely in one closed halfspace bounded by P. Translating the ring normally away from this halfspace changes each point-to-point squared distance by
\[
2td+t^2\ge0,\qquad d\ge0.
\]
All original point distances from K are at least r, so the entire translation remains allowed for K+B_r. Its disk eventually separates. This contradiction proves that P meets int K.

Let D be the ring's disk. An interior point of K+B_r in D lies in the relative interior of D because the boundary ring avoids the body's interior. If a second point of (K+B_r)∩P lay outside D, its segment to that interior point would cross the boundary circle at an interior point of K+B_r. This proves the section inclusion in D; boundary points of the convex body do not invalidate the argument.

For each x in K∩P, the planar radius-r disk about x belongs to (K+B_r)∩P. Its containment in D is exactly
\[
|x-c|+r\le R.
\]
Because P meets int K, the section has nonempty planar interior. Hence R>r. The concentric radius-(R−r) disk contains the section, meets int K, and its boundary avoids int K: an interior-body point on that boundary would supply a small planar neighborhood violating the inclusion. All four conclusions of the proposition follow. No general escape motion for the larger ring follows from them.

## 4. The ball diagnostic is a failed proof route

For K=B_1, r=1/5, and outer radius R=1, the initial height squared is 11/25. The outer circumference is tangent to the radius-6/5 ball. The smaller radius-4/5 ring begins at squared norm 27/25 and can move down to height 3/5, where its squared norm is exactly one, then move up to height two. Every intermediate height is at least 3/5, so the smaller ring avoids int K throughout.

At the turnaround, the expanded ring's squared norm is 34/25, strictly below the expanded body's 36/25. Thus this particular radius-enlarged path collides. Translating the initial outer ring directly upward instead is an admissible escape. The example therefore refutes only the asserted universal validity of the proposed path lift.

Independently, every ball is circle-free by an elementary argument: translate any admissible ring along its plane normal away from the ball's center. Every ring point's squared distance from that center is nondecreasing, including when the initial plane contains the center, and eventually the disk is separated. This confirms that the diagnostic cannot conceal a genuine holding example.

## 5. Positive-clearance robustness and the credited class

The image of the compact set [0,1]×Γ_R under a continuous specified motion is compact. If every ring avoids the closed K, that image and K have positive distance δ_0. The terminal disk has positive distance d_1 from K as well. Choosing δ=min(δ_0,d_1/2) therefore preserves circumference avoidance of int(K+B_r) for r≤δ and strict terminal disk separation. Equality at the ring-clearance threshold is allowed because the original definition permits boundary contact. The proof is valid for continuous motions and needs no differentiability.

This certificate depends on the supplied path. An allowed path with contact can have zero clearance, and bounds for individual paths do not supply the uniform information required by the full question.

The credited theorem for K=X+B_s, with planar compact convex nonempty X and s>0, indeed remains applicable after another ball is added, because B_s+B_r=B_{s+r}. It supplies the stated positive subclass. It does not classify all circle-free convex bodies.

## 6. Reproduction and recommendation

The independent controls use exact rational support witnesses for boxes, arbitrary rational halfspace normals, a family of ball-detour identities, and a positive-clearance polynomial check. There are 711 assertions, distinct from the author's 241 sphere and plane controls.

Run:

    python author_replay/verify.py
    python independent_checks.py

Retain the source-access and prior-work qualifications, the failed-lift-only interpretation, and **unsolved, 2/5**. A proof still needs an actual escape path at every positive clearance level for every relevant initial configuration, or a verified circle-free core whose parallel body is globally held. Neither is furnished here. This is independent adversarial AI review, not human peer review.
