# Independent source-first reconstruction and hand controls — 23357329

All deductions here precede new foreign mathematical bodies, current root/peer findings and archived scientific audit/result/program bodies. The actual manuscript proof was necessarily read. Classical inputs not yet authenticated are clearly conditional; this note does not replace them with finite tests.

## 1. Ordinary GV convention, normalization and relative collars

Let α be a nowhere-zero smooth 1-form defining an integrable cooriented plane field on an oriented closed 3-manifold, with dα=α∧η. Applying d gives α∧dη=0. For fixed α any second admissible η differs by fα. Direct expansion gives

(η+fα)∧d(η+fα)−η∧dη = df∧dα = d(f dα).

For a positive change α′=e^uα, choose η′=η−du. Then dα′=α′∧η′ and

η′∧dη′−η∧dη = −d(u dη).

Thus the closed integral is unchanged. The sign convention opposite to dα=η∧α replaces η by −η but leaves η∧dη unchanged. A normalized characteristic class with a fixed nonzero scalar factor would change the numerical a, not the existence of a>0 or linear unboundedness; that scalar cannot be silently confused when reading primary formulas.

For a transverse vector V with α(V)=1, Frobenius gives

0=i_V(α∧dα)=dα−α∧i_Vdα.

Hence η=i_Vdα works globally. In an OPEN product collar α=ds, dα=0, so η=0 and all jets agree with the product. If forms/gauges are fixed there, the same exact-difference calculations give relative integral invariance, since the boundary terms vanish. Closing the interval with an extra product arc contributes no GV integrand.

## 2. What the classical input must actually supply

The required input is a surface representation ρ:π₁Σ→Diff_c^∞(R) whose compactified actual circle-bundle suspension has NONZERO ordinary GV number. The manuscript claims this from a compatible surjective homology construction, not from an explicit representation. Merely having a universal class with a surjective map H₃(BΓ̄₁)→R is insufficient without a specified comparison from H₂(Diff_c^∞(R)^δ) to the actual compactified suspension class. That exact compatibility is the critical primary-source gate.

Assuming that input, the reduction to ONE positive connected genus≥2 block is valid. An integral 2-cycle in a space can be represented by a map from a finite union of closed oriented surfaces: one may glue triangles in a singular cycle and resolve vertex links without changing its homology class. For BG of a discrete group, the map is encoded by its induced representation because BG is a K(G,1). If a finite sum of connected representatives has positive evaluated suspension class, at least one component does. Reversing the surface orientation changes the sign if needed.

Attaching trivially mapped handles amounts to a degree-one collapse from a higher-genus surface to the selected representative. It preserves the pushed-forward fundamental class and associated value. Thus genus can be made at least two while keeping one positive a. This chooses a SINGLE surface and representation once. There is no need to realize all real values on a uniformly bounded genus, and no later N-dependent surface is introduced.

Each compactly supported diffeomorphism of R is orientation preserving: an orientation-reversing diffeomorphism cannot equal the identity outside a compact set. Choose a finite generating set and one compact interval K containing all generator supports. Inverses fix the same complement; every finite word fixes R\K. Since an increasing diffeomorphism fixes the endpoints of a containing interval, it preserves that interval too. Therefore there is a uniform open fixed neighborhood at both ends after any smooth identification R≅(0,1). Each generator extends by the identity to I=[0,1], smoothly with all endpoint jets, and the whole representation fixes common OPEN collars.

The quotient E=(Σ̃×I)/π₁Σ, with diagonal deck/holonomy action, is a smooth interval bundle carrying the horizontal suspension foliation. Properness/free action comes from the base covering, independent of whether holonomy orbits are dense. The fixed collars are canonically product bundles.

## 3. Relative bundle trivialization does not erase foliation

Choose local increasing fiber coordinates s_i which agree with the common collar coordinate. For a smooth partition of unity λ_i on the compact base, set S=Σ λ_i s_i. At a fixed basepoint the weights are constant along its fiber, so the vertical derivative of S is Σ λ_i times positive derivatives, hence strictly positive. Endpoint values are 0 and 1, and S equals the common collar coordinate there. Each fiber map is a bijection onto I and has smooth inverse; in local coordinates the inverse function theorem, including the collar endpoints, yields a smooth total-space diffeomorphism E→Σ×I preserving base, orientation and collars.

This is a fiber coordinate, NOT a horizontal first integral. The horizontal plane field generally acquires nonzero dx-components in this trivialization. Pulling the foliation to the product therefore does not make it a product foliation, and does not force its GV to vanish.

The foliation is transversely oriented by the positive interval direction. Its annihilator has a unique global normalization α(∂s)=1, with α=ds on common collars. Section 1 then gives η=i_∂s dα and η=0 there.

Close I with a product arc. For the finitely generated image, compactifying R by a point versus inserting a fixed arc gives conjugate circle actions: choose a smooth increasing circle diffeomorphism agreeing on a compact interval containing all supports and adjust only the region on which every holonomy element is the identity. The associated suspension foliations correspond. Thus the additional product arc has zero integrand and the integral over Σ×I is the nonzero classical closed suspension value a. This last identification remains dependent on what the actual primary compatibility theorem says; it is not established by the fiber-coordinate averaging alone.

For u∈I, the intrinsic suspension leaf is Σ̃/Stab(u), immersed in E. Projection to Σ is a covering, hence surjective. It follows that every such leaf meets the fiber over any specified p∈Σ, including endpoint/collar leaves. Dense holonomy images or a nonembedded leaf do not invalidate this covering argument.

## 4. Fixed topology, smooth representative and common circle

For the selected closed oriented genus≥2 surface, the construction needs an orientation-preserving pseudo-Anosov mapping CLASS with a smooth representative φ fixing a disk. The standard filling-multicurve twist mechanism described in the manuscript supplies a candidate: thin annuli around finitely many filling curves leave a complementary open disk, and the smooth twists are the identity there. The external theorem must establish the pseudo-Anosov class, not claim that a map equal to the identity on an open disk is a pseudo-Anosov normal form.

Once φ is fixed, define M=(Σ×[0,1])/((x,1)~(φ(x),0)). It is closed, connected, smooth and oriented. Hyperbolicity is a separate classical theorem requiring the pseudo-Anosov/atoroidal mapping-torus hypotheses; it is not a local form identity. Isotopic representatives have diffeomorphic mapping tori, so using a disk-fixed smooth representative does not change the pertinent mapping class. Fixing a hyperbolic metric thereafter fixes M's positive finite volume independently of N.

For p inside the fixed disk, t↦[p,t] closes smoothly and is embedded. The disk-fixed condition gives a literal product neighborhood through the seam, avoiding derivative ambiguity. V=∂t also descends globally, since the gluing derivative sends the vertical direction to the vertical direction. The oriented γ is the same curve for all insertions.

## 5. Exact finite stacking, all jets and coorientation

For any N≥1 an explicit legal choice is

a_j=(2j−1)/(2N+1), b_j=2j/(2N+1), j=1,…,N.

Each slab has positive length ℓ=1/(2N+1); the first/last and intervening gaps have the same positive length. All slabs lie strictly inside (0,1). For N=1 the slab is [1/3,2/3]; for N=2 they are [1/5,2/5] and [3/5,4/5]. There is no infinite accumulation within any given construction.

On a slab let h(x,t)=(x,(t−a_j)/ℓ_j). Put α_j=ℓ_j h*α and η_j=h*η. Since ℓ_j is a constant,

dα_j=ℓ_j h*(dα)=α_j∧η_j,  α_j(V)=ℓ_j·(1/ℓ_j)=1.

Near each slab endpoint h*α=dt/ℓ_j, so α_j=dt and η_j=0 on an OPEN collar. This is equality on a neighborhood, hence equality of every derivative. Extend the pair by dt,0 on the complement, including the seam. The seam acts on x by φ and fixes dt, so no condition ρ∘φ_*≈ρ is required. Product endpoint data make the two independently chosen structures compatible there.

The resulting global α_N is smooth, never zero because α_N(V)=1, and Frobenius integrable by the displayed local identity. Its kernel is a smooth cooriented codimension-one foliation. The same γ is positively transverse everywhere, with the same normalized value 1.

To see it meets EVERY global leaf, take any point q. If q is in an inserted block, its block suspension leaf has a path to the fiber over p by section 3, so the global leaf through q intersects γ. If q is in a product gap/collar/seam region, the horizontal surface fiber through q contains its point on γ. Product-collar leaves cannot be crossed by another leaf; in particular no exceptional glued leaf invalidates these arguments. This proves the specified strong single-circle tautness, not just existence of some transversal through each point separately.

No metric choice, seam diffeomorphism, surface, representation, a or γ was varied with N. Only the normalized plane field inside finitely many slabs changes.

## 6. Additivity and a fixed-volume obstruction

The diffeomorphism h is orientation preserving for the product orientation on Σ×I because ℓ_j>0. By pullback compatibility with exterior differentiation,

η_j∧dη_j=h*(η∧dη),

and its integral over that slab is exactly a, not ℓ_j a or a/ℓ_j. η_N is zero away from blocks and interfaces, so there are no additional seam or boundary terms. Therefore gv(F_N)=Σ_j a=Na.

For any finite proposed bound B(V₀) at the fixed metric volume V₀, choose an integer N>B(V₀)/a (if the bound is negative, any positive value already contradicts it). Then gv(F_N)>B(V₀). The same gives unbounded absolute values because all these values are positive. It is not necessary to construct negative GV or every real value, and varying the metric or hyperbolic covers would prove a different, weaker assertion.

The exact Calegari target formulation, tautness definition and distinction from its minimal-foliation question must still be read from that actual cited version; they cannot be certified solely by the native paper's quotation.

## 7. Local hand controls and diagnostic limitations

In oriented coordinates (x,y,s), write α=ds+A(x,y,s)dx+B(x,y,s)dy. Its normalized η is A_s dx+B_s dy. Comparing coefficients in dα=α∧η gives the actual Frobenius condition

B_x−A_y=A B_s−B A_s.

The GV density is

η∧dη=−(A_s B_ss−B_s A_ss) dx∧dy∧ds.

Under compression, α_j=dt+ℓ A(x,y,s)dx+ℓ B(x,y,s)dy, η_j=A_s dx+B_s dy, s=(t−a)/ℓ. The t-derivative contributes 1/ℓ to the GV density; dt=ℓ ds cancels it exactly. This is a direct local control of section 6, while pullback proves it universally.

Negative control: α=ds+s dx+s²dy is nowhere zero but has B_x−A_y=0 and A B_s−B A_s=s². It fails Frobenius except at s=0. Although contraction gives η=dx+2sdy and a nonzero expression η∧dη=−2 dx∧dy∧ds, this is NOT a foliation GV witness. In fact α∧dα=−s² dx∧dy∧ds and dα−α∧η=−s² dx∧dy. A finite checker that only sees a nonzero 3-form would accept a false positive.

Positive LOCAL control: let h(x,y,s)=s+x s²+y s³ near x=y=0, so H=h_s=1+2xs+3ys²>0 in a sufficiently small neighborhood. Set α=dh/H; it is automatically integrable and normalized. At x=y=0, A=s² and B=s³, giving η=2s dx+3s²dy and density −6s² dx∧dy∧ds. This confirms that a legitimate local normalized density may be nonzero even for a local first-integral foliation.

It does NOT prove the required global nonzero block. If a single global h with h_s>0 defined this foliation on Σ×I, agreed with s near both endpoints, and extended to the closed product, the defining form dh has η=0. The closed/relative choice-invariance in section 1 would force total GV zero; local nonzero densities cancel by exact terms. Thus the nontrivial classical suspension input cannot be replaced by a globally product-coordinate example or by local symbolic algebra.

For derivative control, ∂_t^r(ℓ A(x,y,(t−a)/ℓ))=ℓ^(1−r)∂_s^r A. For η coefficients the factor is ℓ^(−r). Each finite ℓ>0 gives a C∞ form, while higher derivatives need not remain bounded as N→∞. This is compatible with the exact theorem and shows why it says nothing about an infinite smooth limit or compactness of the sequence of plane fields.

## Source-first outcome and exact unfinished interfaces

All local/global deductions above are completed actual analytic/hand results. No internal contradiction or failure of finite insertion, single-circle tautness or ordinary-GV additivity was found. The precise nonzero actual-suspension compatibility, closed mapping-torus hyperbolization, disk-fixed pseudo-Anosov class construction and the literal 2002 target-question/definition are the bounded external interfaces still to authenticate after INITIAL. No verdict on full original claim, priority or current openness is inferred from the manuscript's assertions or from finite controls. No scientific/native program has run.
