# Exact candidate countermodel for the literal continuous-unit-binormal question

Candidate reported to root before promotion. This is a verification discovery during an adversarial audit; it is not yet a novelty or publication claim. Original research used one substantive attempt. Root has now explicitly classified the decisive counterexample route as new substantive research and will record cumulative 2/5 (original1 + reopened route1); reproduction and adversarial checks add no further attempts. No QUEUE or source-snapshot file has been edited.

## Literal claim and model

Fresh Ghomi2019 Problem1.4, printed p6, asks whether a smooth closed immersed curve with a continuous injective binormal field must have nonzero linking with its small binormal push-off. It does not require the binormal map to be an immersion. The construction below even has a smooth embedded center curve, everywhere nonzero curvature, a smooth unit binormal, and an embedded disjoint push-off.

For t in R/(2pi Z), put c=cos(t), s=sin(t),

    gamma(t) = (c, s, (c²−s²)/4),
    C(t) = gamma′(t) cross gamma″(t) = (−c³, +s³, 1),
    R(t) = |C(t)| = sqrt(1+c⁶+s⁶),
    B(t) = C(t)/R(t).

The sign in C_y is POSITIVE. An initial informal parent message had the opposite sign; the correction was sent immediately before any proof or candidate was frozen. No erroneous sign is used below or in actual tests.

The xy projection is the unit circle, so gamma is a smooth embedding and gamma′ never vanishes. Since C_z=1, gamma′ and gamma″ are linearly independent and curvature is strictly positive. Its osculating plane is the smooth plane spanned by these derivatives. The smooth unit field B is orthogonal to that plane and nowhere zero.

B is injective: B_z>0 and

    −B_x/B_z = c³,    B_y/B_z = s³.

The real cube is injective, so equality B(t)=B(u) forces both cos(t)=cos(u) and sin(t)=sin(u), hence t=u modulo 2pi. This proves full continuous spherical injectivity, rather than numerical distinctness at a mesh.

However, B is not regular. Differentiating C gives

    C′ = (3c²s, 3s²c, 0).

Because C_z is constant and positive, B′=0 if and only if C′=0, which holds at exactly t=0, pi/2, pi, 3pi/2. The spherical image has four cusp points. Smooth injectivity therefore does not justify the regular-binormal hypothesis of the original partial Gauss–Bonnet/Fenchel argument. The ordinary torsion is

    tau(t) = det(gamma′, gamma″, gamma‴)/|C|²
           = 3cs/(1+c⁶+s⁶),

so it changes sign and vanishes exactly at those four points. This is outside the negative-curvature asymptotic setting of Ghomi–Raffaelli2025, where |n′|=|tau_g| is everywhere positive.

## Disjoint embedded push-off and exact linking computation

Choose ANY 0<epsilon<1/3 and put P(t)=gamma(t)+epsilon B(t). The smooth ambient shear

    H(x,y,z) = (x, y, z−(x²−y²)/4)

is an orientation-preserving global diffeomorphism with inverse (x,y,w)↦(x,y,w+(x²−y²)/4), and Jacobian determinant one. It sends gamma to the unit circle in the plane z=0. Direct substitution gives

    H(P(t))_z
      = epsilon/R + epsilon(c⁴+s⁴)/(2R)
        − epsilon²(c⁶−s⁶)/(4R²).

Since R≥1, |c⁶−s⁶|≤1 and c⁴+s⁴≥0,

    H(P(t))_z ≥ (epsilon/R)(1−epsilon/4) > 0.

Thus P is disjoint from gamma. The planar unit disk bounded by H(gamma) is disjoint from the entire H(P). The linking number is its signed intersection number with that disk, hence zero. Equivalently the second component is contained in the upper half-space and contracts there disjointly from the first. Orientation-preserving H preserves linking, so Lk(gamma,P)=0.

For completeness P is also embedded, not merely a disjoint immersed cycle. On the closed unit xy disk extend B by

    F(x,y) = (−x³, y³, 1)/sqrt(1+x⁶+y⁶).

For nonzero v the derivative of normalization v↦v/|v| has operator norm 1/|v|. The unnormalized vector map here has derivative diag(−3x²,3y²) in its first two coordinates and zero third row. Its operator norm is at most 3 on the unit disk; its vector length is at least 1. Thus F and F_xy are Lipschitz with constant at most 3, by the mean-value estimate along line segments in this convex disk. For distinct p,q in that disk,

    |(p+epsilon F_xy(p))−(q+epsilon F_xy(q))|
      ≥ (1−3epsilon)|p−q| > 0.

The same differential estimate gives a nonzero derivative on the unit circle. The xy projection of P is therefore a smooth embedding, proving that P itself is a smooth embedding. The entire explicit range 0<epsilon<1/3 consists of disjoint embedded push-offs, so this is the small-ribbon linking invariant intended in the question.

## What this changes and what it does not prove

If the literal continuous injective unit-field hypotheses are accepted exactly as printed, this construction is a negative answer. It uses neither a nonunit loophole nor a self-intersecting centerline nor ill-defined linking. It does not answer the narrower 2025 embedded negatively curved surface question, whose normal is regular. No claim that it is new is made here: a priority audit and an independent fresh whole-proof adversarial review are necessary before promotion.

The original PR's signed frame identities and conditional regular-binormal inflection obstruction remain mathematically correct. Its original historical statement that its single attempted route found no counterexample remains a dated account of that attempt. A CURRENT assertion that the literal continuous-unit-field question still lacks a candidate counterexample would need updating before acceptance/publication. A proof relying on regularity of B cannot reject this example merely because B′ vanishes.
