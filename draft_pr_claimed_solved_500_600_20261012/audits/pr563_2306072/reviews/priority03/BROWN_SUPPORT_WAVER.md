# Actual-support tangent waver with both target angles monotone

Audit-only scope certificate. This is a deduction from Brown's classical explicitly maximizing point-evaluation family, not a novelty claim, not a proposed new solution, and not a scope exclusion of unread Zemyan2003. The primary source is J.E.Brown, *Geometric properties of a class of support points of univalent functions*, Trans.AMS256 (1979),371–382, DOI10.1090/S0002-9947-1979-0546923-8. Full text read here; pp374,376,380–381 visually inspected, with source receipt below. Its Theorems1–2 say the polar argument and radial angle are monotone for these actual support points.

The purpose is to test a possible stronger inference: perhaps any tangent waver in an actual S-support slit necessarily settles the radius questions. The following actual-support example disproves that inference. It strengthens the parent's purely geometric certificate, whose fractional radial power need not encode the stronger analytic behavior at infinity of support slits.

## 1. Choose a genuine globally maximizing Brown support point

Let δ=10⁻¹², R=1/2, r=tanh(1/4), θ₀=π/2+δ, χ=θ₀+R sin θ₀, and z₀=r exp(iχ). Then 0<r<1 and 0<χ<π, since δ+1/2<3/2<π/2. Let f maximize Re g(z₀) over normalized S, with B=f(z₀).

Brown pp374–375, equations(9)–(11), show its argument is the unique θ₀∈(0,π) solving θ₀+R sin θ₀=arg z₀, and

    |B| = r/(1−r²) exp(R cos θ₀)
        = (1/2)sinh(1/2) exp(−(1/2)sin δ).

These are statements about the actual global point-evaluation maximizer. The chosen functional is continuous and nonconstant on S. The estimates sinh(1/2)≥1/2+(1/2)³/6, sin δ≤δ and exp(−δ/2)≥1−δ/2 yield

    |B| ≥ (25/96)(1−δ/2) > 1/4.

No maximizer selection or numerical optimization is used.

## 2. The explicit natural trajectory is on the actual omitted slit

Set E=exp(−iθ₀/2), u=sE, and

    W(s)=−B csch²(sE),  0<s≤10⁻⁵.

Brown p376 equations(12)–(16) give precisely this near-infinity trajectory: write his spiral coordinate as exp(−2sE), and use k(exp(−2u))=1/[4sinh²u]. Alternatively, directly verify for Q(w)=B²/[w²(B−w)] that

    Q(W) W′² = B²/(B−W)·(W′/W)² = 4B E² = 4|B| >0.

Here W′/W=−2E coth u and B−W=B coth²u. As s→0, W(s)∼−B/(s²E²), tending to the unique ending trajectory at the simple pole at infinity. For 0<|u|≤1/2, the power series give

    |sinh u/u−1| ≤ Σₙ≥1(1/4)ⁿ =1/3,
    |cosh u−1| ≤1/3.

Thus there are no nonzero sinh or cosh zeros on this disk, and this trajectory is regular and has Q≠0 throughout the stated segment.

The finite omitted tip has modulus≤1: if a disk of radius d about f(0)=0 is contained in f(D), its inverse, composed with scaling by d, is a disk self-map fixing0 whose derivative is d/f′(0)=d. Schwarz gives d≤1. Letting d tend to the boundary distance and using the monotone modulus of the support slit gives tip radius≤1.

Meanwhile |sinh(sE)|≤s exp(s)≤s/(1−s), so

    |W(s)| > (1−10⁻⁵)²/[4(10⁻⁵)²] = 9999800001/4 >1.

Unique-trajectory continuation from infinity therefore cannot stop at the actual tip before either selected sign point. Both sign points belong to the actual globally maximizing omitted slit. This check avoids silently using a formal continuation past the tip.

## 3. Exact tangent reversal

For a continuous tangent argument φ(s)=arg W′(s), the log derivative gives

    φ′(s)=Im{E[−3coth(sE)+tanh(sE)]}.

The outward tangent is −W′; its argument differs by a constantπ, so has the same derivative. Define h(u)=3−3u cothu+u tanhu. Division of the ordinary sinh/cosh series gives

    h(u)=−(4/15)u⁴+(8/63)u⁶+Σₙ≥8cₙuⁿ.

The function h is even and analytic on |u|≤1/2. The preceding sinh/cosh bounds imply |u cothu|≤2 and |u tanhu|≤1/2 there, whence |h|≤19/2<10. Cauchy's coefficient estimates give |cₙ|≤10·2ⁿ. Accordingly,

    |Σₙ≥8cₙuⁿ/u| ≤2560s⁷/(1−2s).

The singular term −3E/u=−3/s is real. Since sin(2θ₀)=−sin2δ and sin(3θ₀)=−cos3δ, this proves the fully bounded identity

    φ′(s)/s³ = −(4/15)sin2δ+(8/63)cos3δ·s²+e(s),
    |e(s)| ≤2560s⁴/(1−2s).

At s₁=10⁻⁷, use sin2δ≥2δ−(2δ)³/6 and cos3δ≤1. The resulting exact rational upper bound is negative. At s₂=10⁻⁵, use sin2δ≤2δ and cos3δ≥1−(3δ)²/2. The resulting exact rational lower bound is positive. The bounds are recorded in ANGLE_BRIDGE_CHECKS.json; check_angle_bridge.py independently divides the finite series and verifies the margins with Fraction arithmetic. Thus φ is not monotone on this genuine omitted support arc.

Brown Theorems1–2 still guarantee monotone polar argument θ and monotone nonnegative radial angle A. His A=arg(w/w′)>0 in outward orientation, so the signed radial angle β=arg(w′/w)=−A is monotone as well. Consequently this actual support point has a tangent waver but satisfies both monotonicity properties in the target.

## 4. What this proves about priority, and what it does not

Even actual-support tangent nonmonotonicity does not logically imply nonmonotone θ, β or |β|. A positive tangent-waver abstract therefore cannot by itself be treated as the target's negative solution. It also cannot be treated as an exclusion: Zemyan2003 might use a different family or include additional conclusions. His full six-page formula, support realization and angle signs must be compared directly before certifying exact overlap or non-overlap. Nothing here asserts that Zemyan's example is this Brown example.

A supplementary geometry-only certificate with full integer-power behavior at infinity uses β(r)=3/(5r)+3/(20r²), θ(r)=−∫ᵣ^∞tanβ(s)/s ds, w=r exp(iθ(r)), r≥1. Then θ↑, β↓, |β|↓, and φ′=[tanβ−3/(5r)−3/(10r²)]/r is positive at1 and negative at2 by the two exact trigonometric checks in the script. It has convergent Laurent behavior near∞ and asymptote r−3i/5+O(r⁻¹). It is not asserted support-realizable; the actual Brown construction above supplies the stronger required scope check.
