# Literal binormal question: complete counterexample and prior equivalence

## Exact target and disposition

The target is Ghomi's 2019 *Open Problems in Geometry of Curves and Surfaces*, Problem 1.4, printed page 6, joined to numeric record 7000004 / AMR-069-0004. It asks whether a smooth closed immersed curve with continuous osculating planes and a continuous injective binormal must have nonzero linking with its sufficiently small binormal push-off. The printed wording does not impose a regular spherical binormal. Our example has an embedded centerline, everywhere positive curvature, a smooth injective **unit Frenet binormal**, and embedded disjoint push-offs with linking zero. Thus the ambiguity about normalization and immersed linking is immaterial to this counterexample.

The counterexample below is a verified elementary consequence of an earlier explicit construction in Lei Ni, Wei Zhang and Yijian Zhang, *On questions of Pogorelov and Toponogov*, arXiv:2606.29231v1, submitted 2026-06-28, section 2, printed pages 2–3. The appropriate campaign outcome is **already_solved**, accepted as a credited partial research finding, without a new paper, DOI or publication-tracker row. This classification does not assert that the cited paper explicitly states the linking consequence or names Ghomi's question, nor establish the earliest historical recognition of that consequence. It does not resolve the later strictly negative curvature question.

## A compatible, globally injective binormal

Write c=cos(t), s=sin(t), with parameter t in R/(2pi Z), and set

    Gamma(t) = (c,s,(c^2-s^2)/4),
    W(t) = (-c^3,s^3,1),
    R(t) = sqrt(1+c^6+s^6),
    B(t) = W(t)/R(t).

The xy projection of Gamma is the unit circle, hence Gamma is a smooth embedded closed curve and has nonzero speed. Differentiation gives

    Gamma' = (-s,c,-sc),
    Gamma'' = (-c,-s,-(c^2-s^2)),
    Gamma''' = (s,-c,4sc),
    Gamma' cross Gamma'' = W.

Since W_z=1, curvature is strictly positive everywhere. Consequently its osculating planes vary smoothly, and B is exactly its unit Frenet binormal, orthogonal to Gamma' and Gamma''. It is smooth, closed and unit length. Because B_z>0, its direction ratios recover

    -B_x/B_z = c^3,       B_y/B_z = s^3.

Real cubing is injective, so equality of two binormals gives equality of both c and s, and hence equality of parameters modulo 2pi. This is global injectivity, including antipodal and cardinal parameters.

However, W'=(3c^2s,3s^2c,0). Differentiating W=RB and using W_z=1 shows that B'=0 implies R'=0 and W'=0, and the converse holds. Therefore B' vanishes exactly at t=0, pi/2, pi, 3pi/2. The torsion is 3cs/R^2. Smooth injectivity of a spherical binormal does not imply nonvanishing derivative, even when its centerline is embedded with strictly positive curvature. The regular-binormal Gauss–Bonnet obstruction cannot be applied at these four points.

## Embedded push-offs for every 0<epsilon<1/3

Let P_epsilon=Gamma+epsilon B. To prove embedding without relying only on a tubular-neighborhood existence claim, extend the binormal direction to the closed convex unit disk in R^2 by

    F(x,y)=(-x^3,y^3,1)/sqrt(1+x^6+y^6).

The derivative of v -> v/|v| is (I-vv^T/|v|^2)/|v|, of operator norm at most 1/|v|. Here |v|>=1, while the derivative of (-x^3,y^3,1) has operator norm at most 3 on the disk. Thus F, and its xy projection, are 3-Lipschitz. For distinct points p,q on the unit circle,

    |p+epsilon F_xy(p)-q-epsilon F_xy(q)|
       >= (1-3epsilon)|p-q| > 0.

The same derivative bound gives an invertible derivative for the planar map p -> p+epsilon F_xy(p) when epsilon<1/3. Restricting to the circle gives an injective immersion; compactness gives a smooth embedding. Therefore P_epsilon is embedded for every epsilon in the asserted interval. An independent strict-polar-angle proof is supplied in linking_family/CANDIDATE_LINKING_CERTIFICATE.md.

## Disjointness and zero linking by a spanning disk

Use the global smooth shear

    H(x,y,z)=(x,y,z-(x^2-y^2)/4).

Its polynomial inverse adds (x^2-y^2)/4 to z; its Jacobian determinant is 1, so it is an orientation-preserving diffeomorphism. H(Gamma) is the unit circle in z=0, bounding the oriented unit disk D in that plane. Direct substitution gives

    H_z(P_epsilon)=epsilon/R
       +epsilon(c^4+s^4)/(2R)
       -epsilon^2(c^6-s^6)/(4R^2).

Because R>=1 and |c^6-s^6|<=1, this is at least

    (epsilon/R)(1-epsilon/4) > 0

for 0<epsilon<1/3. Consequently the entire H(P_epsilon) misses D, not merely its boundary. Both curves are embedded, and they are disjoint. The oriented linking number equals the algebraic intersection number of the second curve with a spanning surface for the first. Here that intersection is empty, so it is zero. Linking is invariant under H, whence

    Lk(Gamma,Gamma+epsilon B)=0   for every 0<epsilon<1/3.

This universal proof supplies injectivity, compatibility, embedding, disjointness and linking; finite exact controls are supplemental evidence only. It does not depend on nonzero total torsion, numerical writhe integration, crossing-sign sampling, or an approximation preserving binormal injectivity.

## Exact specialization of the earlier printed construction

Ni–Zhang–Zhang print the graph V(x,y)=(x,y,x^4-y^4), with unit normal

    n(x,y)=(-4x^3,4y^3,1)/sqrt(1+16x^6+16y^6),

and the closed asymptotic curves, for a>0,

    gamma_a(t)=(a c,a s,a^4(c^4-s^4)).

On the unit circle c^4-s^4=c^2-s^2=cos(2t), and direct differentiation gives

    gamma_a' cross gamma_a''
       =a^2(-4a^3c^3,4a^3s^3,1).

Thus the graph normal restricted to gamma_a is its unit Frenet binormal. The normal map is globally injective by the same cubic-ratio argument; the curvature is positive. Set a=4^(-1/3). The positive ambient homothety by 1/a maps gamma_a exactly to Gamma and preserves its unit binormal. It maps gamma_a+delta B to Gamma+(delta/a)B. Accordingly every 0<delta<a/3 gives disjoint embedded push-offs and linking zero by the proved certificate. No unsupported theorem from that paper's other sections is used.

A second independent prior-consequence proof works directly on the printed a=1 graph disk. Put alpha=epsilon/|(-4x^3,4y^3,1)| on its boundary and q=(x-4alpha x^3,y+4alpha y^3,x^4-y^4+alpha). For epsilon<1/4, alpha<=epsilon and |x-4alpha x^3|<=|x|, while |y+4alpha y^3|>=|y|. Hence

    q_z-q_x^4+q_y^4
       =alpha+[x^4-(x-4alpha x^3)^4]
               +[(y+4alpha y^3)^4-y^4] >= alpha > 0.

The push-off misses the entire graph disk. Its embedding is additionally ensured for sufficiently small epsilon by the ordinary tubular-neighborhood theorem; this second proof does not claim embedding for the entire interval (0,1/4).

The older Brown/Banchoff teaching page also prints a cos(2t) wavy-circle family and asks about binormal cusps. Its server Last-Modified metadata alone is not a verified historical publication date. The dated June 2026 primary construction is sufficient for the present credited outcome; worldwide earliest priority remains unestablished.

## Retained conditional findings and exact scope boundary

For a smooth arclength-parametrized curve and a C^2 compatible unit B, set T=Gamma' and N=B cross T. There exist signed k and tau with T'=kN, N'=-kT+tau B and B'=-tau N, without division by k. Under a parameter of positive speed v, all three derivatives acquire v. The binormal twist density is T dot (B cross B')=tau. For regular B, tau has fixed nonzero sign, the spherical tangent is U=-sign(tau)N, and the outward oriented spherical geodesic curvature is **k/|tau|**, so k_g d ell=k ds. Gauss–Bonnet for a regular simple spherical B gives |integral k ds|<2pi. If k has one sign, this contradicts Fenchel's total-curvature bound >=2pi. These claims require B regular; they do not rule out our four stationary points. Nonzero twist alone never excludes cancellation with writhe.

The ruled strip Gamma+rN has Gaussian curvature -tau^2 on its centerline. Our tau vanishes at four points. More generally a strictly negative curvature surface has invertible shape operator, so the derivative of its unit normal along a regular curve cannot vanish. Therefore our counterexample does not satisfy the hypothesis of Ghomi–Raffaelli's 2025 Problem 1.1. The printed prior graph has K=-144x^2y^2/(1+16x^6+16y^6)^2 and K=0 on the axes. No assertion about the Nirenberg rigidity problem or the later negative-curvature conjecture follows.

The source-qualified original conditional observations remain useful. The original unsolved disposition is superseded by the complete counterexample and positive-prior equivalence; old diagnostic programs and old review certify only their dated local partial packet. The current whole result requires a new complete adversarial gate.

## Audit integrity and attempt accounting

Original substantive attempt 1 is preserved byte-for-byte. Developing a new wavy-circle counterexample was charged as substantive attempt 2 at the preserved ROOT_COUNTEREXAMPLE_CHECKPOINT.md; it is not relabeled as a zero-cost audit. Reproduction and independent falsification add no further substantive attempt. Total: **2/5**. Root first obtained a sine variant; the differential family independently derived the equivalent cosine candidate before receiving that root reconstruction. The linking reviewer independently froze its original-scope analysis, then verified the supplied candidate; the primary-scope reviewer independently verified the prior construction after formula exposure. These are distinct approach families, not three claimed blind rediscoveries.

The old readiness.review_hash 2e499128... correctly binds the full raw source record and separate prior report using the actual importer serialization. The old verdict.review_sha256 0d8a579e... correctly binds the separate review document. They are different roles, not a stale binding. The differential family's original alleged mismatch is expressly withdrawn by its additive qualification; all closed original bytes are retained. Actual replay setup failures and a root initial AssertionError with unrecovered precise phase are preserved separately; successful later unchanged actual replays do not reclassify those failed invocations as successes.

AI tools were used extensively for derivation, reproduction and adversarial checking. This is unrefereed AI-audited research documentation, not external human peer review or formal proof-assistant verification.
