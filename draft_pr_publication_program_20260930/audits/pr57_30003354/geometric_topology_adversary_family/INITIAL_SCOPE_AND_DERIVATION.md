# Source-first geometric/topology adversary: PR57

Prior-role disclosure: this agent previously audited PR56. This is a fresh
mathematical audit of PR57, independent of PR57's historical review and other fresh
families. Before writing this initial derivation I read only the original literal
source_record.json and CANDIDATE.md, then the official OWR passage and primary
Banakh–Belegradek/Belegradek–Hu topology passages. No historical reviewer/checker
body or another fresh family's finding was read.

Pinned head supplied by the parent: `4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29`.
Target 30003354 / OWR-15208-008 is inverse continuity of the specified conformal
parametrization at finite integer endpoints, not the existence of another
homeomorphism between the underlying spaces.

## Initial primary scope

[Official OWR 3/2017](https://ems.press/doi/pdf/10.4171/OWR/2017/3), printed p.149,
defines normalized orientation-preserving diffeomorphisms fixing 0 and 1 on the
plane, and 0, 1 and infinity on the sphere. It asks about the parametrization's
homeomorphism property and expects integer-endpoint failure. Its date is 2017;
the curated source record's parenthetical 2018 is bibliographic noise, not a new
regularity restriction.

[Banakh–Belegradek](https://arxiv.org/pdf/1510.07269), introduction and §§2,8,9,
uses smooth objects with compact-open derivative topologies, with one additional
derivative on the diffeomorphism factor. The [2016 erratum](https://link.springer.com/content/pdf/10.1007/s00208-015-1354-1.pdf),
printed p.711, corrects the earlier integer-topology homeomorphism claim to a
noninteger Hölder statement. The integer endpoint is not already covered by that
positive theorem. I have not claimed a comprehensive current-priority audit.

## Independent geometric reconstruction

1. **Gauge and uniqueness.** Suppose two normalized decompositions of a metric
   exist. In their conformal coordinates the transition F has differential whose
   pullback of a scalar Euclidean/round metric is scalar Euclidean/round. With
   positive orientation this makes F a global conformal automorphism. On the
   plane it is affine, and fixing 0 and 1 forces the identity. On the sphere it
   is Möbius, and fixing 0,1,infinity forces the identity. Thus a constructed
   normalized f is the actual unique inverse component; it cannot be discarded
   as gauge. Compactly supported examples also lie in the identity component:
   interpolate the twist angle, or interpolate z+t w with Lipschitz norm <1.

2. **Complete strict backgrounds.** Put b=½log(1+|z|²) on the plane and
   b=log(1+|z|²)−log2 on the sphere. Direct differentiation gives respectively
   Δb=2/(1+|z|²)² and 4/(1+|z|²)², hence Gaussian curvature 2/(1+|z|²)>0 and
   1. Every escaping plane curve has length at least the divergent radial
   integral ∫(1+s²)^−½ ds. A smooth positive sphere metric is complete by
   compactness. Every fixed support disk has a strict positive curvature margin.

3. **r=0 twist.** A smooth angle θₙ(s)=θ₀η(log(R/s)/n) is constant near the
   origin and zero outside R. The map e^{iθₙ(|z|)}z is smooth at 0 because it is
   exactly a rotation there; its inverse subtracts the angle at the same radius.
   In radial/azimuthal frames its differential has shear q=sθ′ with |q|≤C/n.
   The radial background is rotation-invariant, so the pulled-back relative
   metric is [[1+q²,q],[q,1]]. This gives C⁰ convergence, completeness and strict
   curvature by isometry. Dφₙ(0)=Rot(θ₀) is fixed and different from identity.
   All marked points are fixed. The failure is in C¹, exactly the source's
   diffeomorphism topology. Imposing Dφ(0)=I would be an extra, different gauge.

4. **r≥1 diffeomorphisms.** Let ρ=e^−n, ε=1/n, s=(|z|²+ρ²)^½,
   w=εχz^{r+1}log s and f=z+w. Bounds |Dʲlog s|≤Cⱼs^−j imply
   ||Dw||∞≤Cε, because s^r(1+|log s|) is uniformly bounded for r≥1.
   Thus id+t w has positive Jacobian and is globally invertible for all
   t∈[0,1], by the contraction inverse equation, for sufficiently large n.
   Since f is the identity outside R, injectivity implies it maps the disk onto
   itself; f⁻¹ also equals the identity there. Hence it is a normalized plane
   diffeomorphism and extends smoothly to the sphere fixing infinity.

5. **Metric realization is exact.** On the inner disk f_{bar z}=εz^{r+2}/(2s²).
   Differentiating through order r gives O(εs^{r−k}); cutoff terms are O(ε).
   The reciprocal of f_z is uniformly bounded in C^r (its denominator is bounded
   away from zero, and derivatives through order r are uniformly bounded).
   Thus μ=f_{bar z}/f_z→0 in C^r. With h=log|f_z| and correction a, the metric
   g=e^{−2b−2a}|dz+μdbar z|² is identically
   f*(e^{−2U}|dw|²), U=(b+a+h)∘f⁻¹. On the sphere u=U−b is zero outside the
   disk, so it is globally smooth at infinity. This identity constructs a
   domain point; no Beltrami existence theorem is being inferred from estimates.

6. **Completeness is retained.** |μ|<1 ensures positive definiteness with
   eigenvalues (1±|μ|)² relative to the scalar background. The compact correction
   a is bounded. Thus g is uniformly comparable to the complete background on
   the plane, and the global conformal metric in the preceding identity is
   complete by the onto isometry f. On the sphere completeness is automatic.
   Outside R, U=b, which also respects the plane's source growth restriction.

7. **Endpoint separation.** At 0 the (r+1)-st x derivative of w is
   ε(r+1)!logρ=−(r+1)! exactly. Every term differentiating log s leaves a
   polynomial of positive degree and vanishes at 0. Hence f does not converge
   to identity in C^{r+1}, even though μ→0 in C^r. Each r uses its own sequence.

8. **r≥2 curvature.** With a=0, the metric converges in C² on the fixed support.
   Gaussian curvature is a continuous function of a positive metric's two-jet.
   Strict positive background curvature on the compact support and equality
   outside it prove strict curvature everywhere for all sufficiently large n.

9. **r=1 exact correction.** The principal matrix of the pulled-back Laplacian
   is A=J⁻¹J⁻ᵀ, J=Df. Its first-order vector is the componentwise Laplacian of
   f⁻¹ evaluated at f(z), hence |B|≤C|D²f|. With ℓ=1+|log s|,
   A≥½I, |A−I|≤Cε, |B|≤Cεℓ, |Dh|≤Cεℓ and
   |D²h|≤C(ε/s+ε²ℓ²)≤C′ε/s. The final inequality uses bounded sℓ².
   Consequently L(b+h)≥Δb−C₀ε/s. Since D²s≥0 and Δs≥1/s,
   Ls≥1/(2s)−Cεℓ≥1/(4s), uniformly for large n. Set a=Kεχs with K>4C₀.
   On the inner disk L(b+h+a)>(K/4−C₀)ε/s>0. On the fixed annulus all
   perturbation derivatives through the needed orders are O_K(ε), so the
   operator converges to Δ and the expression to Δb>0 uniformly. Smooth cutoff
   gluing gives positivity everywhere. Since a→0 in C¹, g→g* in C¹.
   The resulting curvature is the exact expression e^{2U}ΔU, not a linearized
   surrogate. Small C¹ alone would not imply this conclusion.

Initial finding: these geometric arguments close for all finite integer r≥0 on
both surfaces. No source mismatch, hidden gauge or patching obstruction has been
found. This is a universal derivation independent of any finite diagnostic test.
The remaining audit work is detailed source locators, adversarial controls and a
lean owned-capture/ROOT handoff; no novelty or publication authority is inferred.
