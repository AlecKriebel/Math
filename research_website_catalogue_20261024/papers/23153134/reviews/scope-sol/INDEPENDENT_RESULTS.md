# Source-first independent reconstruction — 23153134

Completed before native scientific code/results/README/SOURCE_AUDIT, archived/current peer/root opinions or new foreign mathematical bodies. The manuscript proof itself was read. The smooth Nash existence/dimension theorem and exact printed target are external inputs still awaiting actual-source checks; no universal conclusion is inferred from finite diagnostics.

## 1. A genuine smooth hyperbolic genus-two base

Use the curvature−1 Poincaré disk metric 4(dx²+dy²)/(1−|z|²)². Put r=2^(−1/4), θ=π/8 and choose vertices r exp(ikπ/4). There is an exact elementary angle control, independent of simply assuming the octagon's interior angle.

The geodesic circle through adjacent vertices r and r exp(2iθ) is orthogonal to the unit circle; its Euclidean center is d exp(iθ), where d=(1+r²)/(2r cosθ). The adjacent opposite-side center at the same vertex is its conjugate. The half interior angle has tangent

(d cosθ−r)/(d sinθ) = ((1−r²)/(1+r²))cotθ.

Here r²=1/√2, (1−r²)/(1+r²)=3−2√2=tan²θ, so that tangent is tanθ. All quantities are positive; therefore the actual interior angle is2θ=π/4. The disk metric is conformal, so this Euclidean angle is also the hyperbolic angle. Radial distance R satisfies coshR=(1+r²)/(1−r²)=3+2√2=cot²θ. Thus both the printed radius and angle are consistent, without a decimal approximation.

Regularity makes opposite geodesic edges equal. Their orientation-preserving hyperbolic side-pairing maps reverse the induced boundary directions. The quotient is connected and oriented. The corner identifications follow i→i+5 modulo8 when going around the link; since gcd(5,8)=1, the link is the one full cycle 0,5,2,7,4,1,6,3,0. There is one quotient vertex, four paired edges and one face; χ=1−4+1=−2 and orientable genus2.

Along an edge two paired half disks form a smooth hyperbolic disk because the transition is an isometry. At the sole vertex eight π/4 sectors develop to a full2π neighborhood. Their final transition fixes the vertex and its tangent frame; an orientation-preserving hyperbolic isometry with those data is the identity. Hence there is no residual cone or orbifold holonomy. The quotient is a CLOSED smooth Riemannian surface, not merely a polygon with the correct Euler count. This is a direct local metric gluing argument; no global discreteness theorem is being substituted for the vertex check.

## 2. An independent connected double-cover construction

The abstract genus-two group has relation [a₁,b₁][a₂,b₂]=1. The proposed Z2 map sends a₁ to1 and other generators to0. Each commutator maps to0, so the relation holds; a₁ reaches1, hence the map is surjective. Its monodromy on sheets{0,1} swaps the two labels for a₁ and fixes them for the other generators. The relation acts trivially and the action has one orbit. This confirms index2 and connectedness, rather than assuming any degree-two cover is connected.

A separate geometric realization is available without classifying-space machinery. Cut the genus-two surface along a nonseparating simple curve dual to a₁. The cut surface is connected of genus1 with two boundary circles. Take TWO copies and glue each positive cut bank to the negative bank of the other copy, by the original local identity. Each seam has a collar mapped diffeomorphically to the original annulus. The resulting map π is an unramified smooth local diffeomorphism. Crosswise gluing joins the copies, so M is connected. Away from the cut each base point has one lift in each copy; on the cut the four bank points form exactly two identified pairs, again two distinct lifts. The curve has no endpoints, so no branch point is introduced. This realizes the stated sheet monodromy up to the conventional choice of dual generator.

The cover is compact: the pieces are compact before gluing, or use finitely many compact evenly covered base sets and two compact lifts of each. Its pulled-back orientation is consistent. A lifted cell decomposition doubles each cell, so χ(M)=2χ(S)=−4. Equivalently the two cut genus1/two-boundary pieces have total χ−4 and gluing circles changes no Euler characteristic. Thus M is a closed orientable genus-three surface.

The usual subgroup classification invoked in the manuscript remains a genuine external interface to inspect, but the independent cross-glue construction establishes the needed existence/topological properties as well. The standard commutator generators are not identified with the literal opposite-side octagon letters.

## 3. Output map and exact Gramian

Let e:(S,g)→R17 be the claimed smooth globally injective Nash isometric embedding, conditional at this stage on its actual theorem. Then e*δ=g. Put h=e∘π and f=0 on M. This is a smooth autonomous system. Its vector field is complete with φ_t=id for EVERY real t. In one fixed chart around each constant trajectory, Df=0, Φ(t)=I and H(t)=Dh(x). Coordinate changes transform the following bilinear form covariantly:

P_T,x(v,w)=∫₀ᵀ⟨de_π(x)dπ_xv,de_π(x)dπ_xw⟩dt
           =Tg_π(x)(dπ_xv,dπ_xw)=Tg̃_x(v,w), where g̃=π*g.

Both dπ and de have rank2; their composition has rank2. Thus P_T is a positive-definite smooth tensor for T>0. The negatively curved tensor is the ACTUAL differential observation metric, not an unrelated auxiliary metric. The rank calculation is local and alone proves no global separation.

Because the trajectory and its output are constant, equality of O_T histories for any T>0 is exactly equality of h, which by global injectivity of e is exactly equality of π. The half-open interval contains0; even any nonempty constant-history interval would give the same equivalence. Every π fiber has precisely two distinct points; hence every attained history has precisely two preimages, all others none. The pair remains indistinguishable for all real times.

On a single sheet of an evenly covered neighborhood, π is injective and e is globally injective, so h and O_T are locally injective. Alternatively rank2 gives an invertible two-output-coordinate minor locally. A smooth isometric IMMERSION lacking injectivity could create additional state coincidences, and a C1 theorem would not prove the required C∞ system. This is why the exact Nash embedding interface and its17-dimensional bound matter.

The normal index-two subgroup also gives a fixed-point-free deck involution τ. It satisfies πτ=π, τ*g̃=g̃, hτ=h and φ_tτ=τφ_t. Its two-point orbits are exactly the indistinguishability classes. This symmetry directly exposes the global ambiguity left invisible to the positive local differential metric.

## 4. Negative curvature is nonvacuous and exactly−1/T

Since π is a local isometry, K(g̃)=−1. For a positive constant scaling Tg̃, the Levi–Civita connection is unchanged: Christoffel symbols have inverse-metric factor1/T and derivative-metric factorT. The curvature operator is unchanged, its (0,4) tensor gainsT, and the sectional denominator gainsT². Thus K(P_T)=−1/T.

There is an independent direct local calculation. In centered hyperbolic coordinates z=u+iv, set s=u²+v² and λ=4T/(1−s)². For λ(du²+dv²), K=−(Δlogλ)/(2λ). Now ∂_u logλ=4u/(1−s), ∂_v logλ=4v/(1−s), and

Δlogλ=8/(1−s)+8s/(1−s)²=8/(1−s)².

Therefore K=−1/T at every point. This agrees with scaling and gives actual negative sectional curvature in dimension TWO, where the tangent two-plane exists. There is no one-dimensional empty-quantifier argument.

For each fixed T>0, the constant−1/T is uniformly bounded above by a strictly negative number across M. It is not uniform away from0 over every T→∞. At T=1,2,1/2 the curvature is respectively−1,−1/2,−2. Negative or zero T is outside the claim; at0 the tensor is0, not a Riemannian metric.

## 5. Geodesic completeness and metric comparison

Every constant-speed P_T-geodesic has its state/velocity in the fixed-speed tangent sphere bundle. The base is compact and the smooth metric is positive, so this bundle is compact (a finite coordinate cover bounds its velocities). The geodesic spray is a smooth vector field on TM. A solution staying in a compact subset cannot have a finite maximal endpoint by the local ODE extension theorem. This applies in both time directions; zero-speed geodesics are constant. Thus P_T is geodesically complete. This does not rely on global Euclidean coordinates or on simple connectivity.

For any FIXED smooth Riemannian metric q, its unit tangent sphere bundle U_qM is compact. The function v↦g̃(v,v) is continuous and strictly positive there. It attains minimum c>0 and maximum C<∞. Homogeneity gives cq≤g̃≤Cq on all tangent vectors, hence Tcq≤P_T≤TCq for every T>0 with c,C independent of T. These constants may depend on q; a common pair for arbitrarily rescaled backgrounds is not asserted.

Geodesic distance on M remains positive between the two deck-related states, while their observation histories have zero separation. There is no contradiction: a pullback positive metric records local path lengths, and a noninjective immersion/cover may map two distinct endpoints to the same output. Completeness and negative curvature do not turn it into a globally injective map. Applying a simply connected global-exponential theorem to this genus-three M would add an absent hypothesis.

## 6. One fixed finite normalized atlas and exact controls

At each point choose a sufficiently small hyperbolic disk chart taking that point to0, and shrink its coordinate radius to at most1/2. No requirement of a globally injective radius1/2 disk is used. Compactness gives a finite subcover. The charts are chosen using g̃ alone, so the atlas is the SAME for every T. At every point of every selected chart,0≤s≤1/4 and

[P_T]=4T(1−s)^(−2)I₂.

The factorized lower and upper differences at T=1 are

4/(1−s)²−4 =4s(2−s)/(1−s)²≥0,
64/9−4/(1−s)² =4(1−4s)(7−4s)/(9(1−s)²)≥0.

Both signs hold on the ENTIRE interval because every displayed denominator is positive and each numerator factor is nonnegative there. No grid sampling is needed. Exact hand values are4 at s=0,256/49 at s=1/8 and64/9 at s=1/4. At s=1/8 the lower difference is60/49 and the upper difference832/441; their sum28/9 equals64/9−4. Multiplying by any T>0 proves the two full-point matrix inequalities. The endpoint1/4 may not be in every open chart, but the weak bound remains valid.

Under a new local coordinate w=a z, the metric matrix at the same point is a^(−2) times its z-coordinate matrix. A→∞ destroys any putative common positive lower bound over EVERY coordinate rescaling; a→0 destroys a common finite upper bound. This is an exact countercontrol to an incoherent all-charts interpretation, not an assertion that the actual printed problem explicitly chose a normalization. The target wording must still be read after the freeze.

The fixed-time and all-time quantifiers are separate. P_T tends to0 as T↓0 and grows linearly as T↑∞; its curvature tends to0 as T↑∞. Nonetheless each fixed positive T satisfies the stated positive definiteness, completeness, uniform-in-state bounds and strict negative curvature, with exactly two-state histories. At T=0 the empty history is common to all M; there is no two-state statement then.

## 7. Success criteria and unfinished primary interfaces

The central geometric construction has an actual universal reconstruction conditional only on the classical smooth Nash embedding interface. Its topological cover has also been realized directly, and all explicit octagon, atlas, curvature, metric and history calculations have hand controls. No scientific program, native verifier or archived PASS result was used.

Before a final full-original disposition, actual primary checks must confirm: (i) Nash's theorem gives a C∞ compact embedding, global injectivity and dimension n(3n+11)/2=17 for n=2; (ii) the actual printed2009 problem uses the manifold/exact differential Gramian/history definition and has no extra hypothesis excluding this construction; (iii) the manuscript's cited covering classification and decisive contextual comparisons match their real statements. Interpretation of unspecified matrix normalization must remain explicit rather than silently claiming a strengthened Euclidean result.

The manuscript's specific older local/global examples and scope comparisons are still author assertions at this checkpoint, not independently verified literature findings. No historical absence inference, current-openness claim or new general method follows. If any material original step fails, report the exact gap and defer the original claim; do not launch a repair or narrower replacement. No current peer/root findings or foreign bodies have been opened.
