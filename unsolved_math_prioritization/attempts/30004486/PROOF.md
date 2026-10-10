# A bounded energy–momentum envelope theorem for spherical skyrmions

Problem 30004486 / OWR-1703869-006.

**Status: partial. The requested non-staticity theorem is not proved.** This note proves local semiconcavity and exact one-sided slope/multiplier formulas in the credited existence interval. It gives no sign or nonvanishing estimate for those slopes. No novelty claim is made.

## 1. Exact model, conventions, and credited inputs

The domain and target are the unit round sphere with outward orientation. Write x for the domain point and normal. For κ>0 and m∈H¹(S²;S²), put

Eκ(m)=D(m)+Aκ(m),
D(m)=½∫S²|∇m|² dσ,
Aκ(m)=κ/2∫S²[1−(m·x)²] dσ,
Q(m)=(4π)⁻¹∫S² m*ωS²,
S(m)=∫S²m dσ,
L(m)=∫S²x m*ωS²,
J(m)=S(m)+L(m).

The density ρm is defined by m*ωS²=ρm dσ. The pointwise inequality |ρm|≤|∇m|²/2 gives D(m)≥4π|Q(m)|. Degree is integral for H¹ sphere-valued maps and is continuous under strong H¹ convergence. In particular it is preserved by the pointwise target rotations used below. These are the usual Sobolev degree conventions of the primary paper.

Joint rotations act by mR(x)=Rm(R⁻¹x). They preserve Eκ,Q and satisfy J(mR)=RJ(m). We use the physical sign convention

∂t m=m×[ΔS²m+κ(m·x)x].                              (1.1)

For a unit vector a, Ra(t) rotates by positive angle t about a, and Xa(x)=a×x. Thus the joint-rotation generator is

Ka(m)=a×m−dm(Xa).

The signed frequency ω below is defined by m(t)=(m)Ra(ωt). Reversing the Landau–Lifshitz time convention reverses ω; nonvanishing is unaffected.

Melcher–Sakellaris [MS], Theorem on PDF p.2 and Corollary 2 on p.9, prove that, for each κ>0, some εκ>0 has the following property: for

Iκ=(4π,4π+εκ),

the degree-zero problem at J=ja has a minimizer, including a smooth one, with energy below 8π. We only use this interval, and fix κ throughout. We import their strict trial-energy bound and their existence of a smooth minimizing representative. We do not re-prove their construction or their harmonic-map regularity theorem. The envelope results below do not require every minimizer to be smooth.

The other non-elementary compactness input is the quantization theorem of Brezis–Coron–Lieb [BCL], Theorem E.1 and its sphere version, **Corollary E.5**, printed pp.699–702 (the different Theorem E.5 later on p.702 is not the result used). Its N=2 statement is:

If mn:S²→S² is bounded in H¹ and mn→m almost everywhere, then, after subselection, the signed measures ρmn dσ converge weakly to

ρm dσ+4π Σi qi δxi,

where the finite list has distinct xi and nonzero integers qi. The empty list is allowed. We read the statement, its proof, and its sphere reduction. The ensuing energy estimate is derived below rather than added as an unstated hypothesis of [BCL].

Define

e(j)=inf{Eκ(m):m∈H¹(S²;S²), Q(m)=0, J(m)=ja},
M(j)={m:Q(m)=0,J(m)=ja,Eκ(m)=e(j)}.

By joint rotations, e is independent of the chosen unit a and also equals the infimum with |J|=j.

## 2. Statement of the bounded result

For every compact interval K⊂Iκ:

1. e is continuous and locally semiconcave; in particular it is locally Lipschitz. The union of M(j), j∈K, is compact in strong H¹.
2. Every m∈M(j) has a unique vector multiplier α(m) for smooth pointwise target-rotation variations. It is parallel to a: α(m)=ω(m)a. The function ω is continuous on these compact minimizing families and is bounded there.
3. There are C<∞ and η>0, depending on K and κ, such that, for every j∈K, m∈M(j), and |h|<η with j+h∈Iκ,

   e(j+h)≤e(j)+ω(m)h+(C/2)h².                    (2.1)

   The constants are not evaluated numerically or bounded explicitly in κ or distance to 4π.
4. Both one-sided derivatives exist and are finite at each j∈Iκ. They satisfy

   e′+(j)=minm∈M(j) ω(m),
   e′−(j)=maxm∈M(j) ω(m).                        (2.2)

   Consequently e is differentiable except at at most countably many j. At every differentiability point, every minimizing field has the same multiplier ω=e′(j).
5. For a smooth minimizing field, the Landau–Lifshitz solution furnished by its multiplier is non-static if and only if ω(m)≠0. Thus, at a differentiability point, all the credited smooth minimizing profiles are non-static if and only if e′(j)≠0.

These assertions do not say that e′ is nonzero, that e is monotone, that e is globally concave, or that the constrained minimizer is unique. They do not determine behavior at the endpoint 4π.

## 3. Momentum variations and the only rank-deficient level

For a smooth test field v:S²→R³, vary m by mt(x)=exp(t[v(x)]×)m(x), where [v]×w=v×w. These variations make sense in H¹ and stay sphere-valued. For b∈R³, let Xb(x)=b×x. Direct differentiation, first for smooth maps and then by approximation or the weak product identities, gives

dJb(m)[v×m]
 =∫S²{b·(v×m)+v·dm(Xb)}dσ
 =∫S²m·[b×v−dv(Xb)]dσ.                         (3.1)

Here Jb=b·J. The second identity uses div Xb=0. The first identity is also the coordinate-free version of [MS, Lemma 2]. For completeness, the orbital part follows from the homotopy formula for pullbacks of the closed area form: in oriented coordinates its variation is the exterior derivative of the one-form m·((v×m)×dm). Integrating against b·x and integrating by parts gives ∫v·dm(Xb). Thus no derivative of m beyond H¹ is used. The integration-by-parts version on the right is particularly useful: the variation is continuous even under strong L² convergence of sphere-valued maps.

Suppose b≠0 annihilates the momentum derivative for all v. Equation (3.1) says

dm(Xb)=b×m                                                   (3.2)

in distributions, hence in L². Integrating this linear transport equation along the rotation flow shows that m is jointly equivariant about b. This remains valid for H¹ maps: domain rotations are differentiable as L²-valued curves, and differentiation of R−tm(Rtx) gives zero.

Here is the degree and momentum calculation without assuming smoothness or choosing a target phase at its poles. Rotate and normalize b to e3. In spherical domain coordinates (θ,χ), equivariance means

m(θ,χ)=R3(χ)h(θ),  z(θ)=h(θ)·e3.

On every compact subinterval of (0,π), h is H¹. With t=log tan(θ/2), finite energy gives

D(m)=π∫R[|ht|²+1−z²]dt<∞.

Since ht⊥h, |zt|≤√(1−z²)|ht|, so zt∈L¹(R). Thus z has limits z−,z+ at t=−∞,+∞. Integrability of 1−z² forces each limit to lie in {−1,1}. Computing the pullback density gives

m·(mθ×mχ)=−zθ,
Q(m)=(z−−z+)/2.

The transverse components of S,L vanish by integration in χ. Integration by parts, justified first on [δ,π−δ] and then by the endpoint limits, gives

L3=−2π∫0πcosθ zθ dθ
   =2π(z−+z+)−2π∫0πsinθ z dθ,
S3=2π∫0πsinθ z dθ.

Therefore J3=2π(z−+z+). If Q=0, then z−=z+=±1, so |J|=4π.

It follows that, on every degree-zero field with |J|>4π, the linear map

v↦dJ(m)[v×m],  C∞(S²;R³)→R³,                 (3.3)

is onto. Otherwise its finite-dimensional range would have a nonzero annihilator b, contradicting the calculation above. Notice that this proves rank for weak H¹ fields as well as smooth ones.

## 4. Exact local momentum corrections

Fix a degree-zero field m with |J(m)|>4π. By (3.3), choose three smooth fields v1,v2,v3 for which the matrix B with columns dJ(m)[vi×m] is invertible. Set

Tt n(x)=exp([Σi ti vi(x)]×)n(x),  t∈R³.

The finite-dimensional map t↦J(Tt n) is smooth. For n sphere-valued and close to m in strong H¹, its derivatives through any fixed finite order are continuous in n and uniformly bounded for small t. One can see this directly by differentiating (3.1) along Tt: the instantaneous angular velocity fields depend smoothly on x,t, and integration by parts removes dm from momentum derivatives. For energy the explicit formulas for ∇(Tt n) and the bounded anisotropy term give the same assertion through order two; strong H¹ convergence suffices. Bounds depend on the smooth vi and a bound for ∥n∥H¹.

The parameter-dependent finite-dimensional inverse function theorem therefore produces, uniformly for n in a sufficiently small strong-H¹ neighborhood of m, a correction t=t(n,q) satisfying

J(Tt(n,q) n)=q,  t(n,J(n))=0,

for |q−J(n)| small. The first two derivatives in q are uniformly bounded. An explicit justification of uniformity is to shrink the t-ball until its Jacobian differs from B by less than 1/(2∥B⁻¹∥), uniformly in n; the contraction proof of the inverse theorem then gives a common image ball and first-derivative bound. Differentiating the inverse equation gives the second-derivative bound.

The maps Tt n have the same Q as n: s↦Tst n is a strong-H¹ continuous homotopy and degree is integer and strongly continuous. Consequently these are admissible exact corrections, not approximate constraints. The function

q↦Eκ(Tt(n,q) n)                                      (4.1)

has uniformly bounded Hessian in q in such a neighborhood.

## 5. Multipliers, axial alignment, and physical frequency

Let m minimize at q=ja. Write ℓE(v)=dEκ(m)[v×m] and ℓJ(v)=dJ(m)[v×m]. If ℓJ(v)=0, start the variation exp(s[v]×)m and use Section 4 to correct its momentum back to q. The correction is O(s²), because its first momentum derivative vanishes. Minimality for positive and negative s therefore gives ℓE(v)=0. Since ℓJ is onto R³, elementary linear algebra gives a unique α∈R³ with

ℓE(v)=α·ℓJ(v) for every smooth v.                  (5.1)

No Banach-manifold claim about H¹(S²;S²) is needed.

The local corrected competitor (4.1) now gives the upper support

F(q′)≤F(q)+α·(q′−q)+O(|q′−q|²),                    (5.2)

where F(q)=inf{Eκ:Q=0,J=q}. Rotational invariance gives F(Rq)=F(q). Substitute q′=Rb(s)q into (5.2), use both signs of s, and conclude α·(b×q)=0 for every b. Hence α=ωa. This argument avoids differentiating a rough H¹ field twice along a domain rotation.

The multiplier depends continuously on m within the minimizing set in strong H¹. Indeed, in one of the fixed charts from Section 4 it is obtained by solving the nonsingular 3×3 system with entries ℓJ(vi) and right-hand side ℓE(vi). Both are continuous in m. For example,

ℓE(v)=∫∇m:((∇v)×m)dσ−κ∫(m·x)((v×m)·x)dσ,

which is strongly-H¹ continuous.

If m is smooth, all smooth tangent fields φ can be written v×m, with v=m×φ. Let

gE=Pm[−Δm−κ(m·x)x],
Ga=Pm a−m×dm(Xa),   Pm=Id−m⊗m.

Equation (5.1) becomes gE=ωGa. The vector identity −m×Ga=Ka then gives

m×[Δm+κ(m·x)x]=ωKa.

By rotational invariance this implies that m(t)=mRa(ωt) solves (1.1). Section 3 shows Ka is not identically zero when Q=0 and j>4π. Thus this solution is static exactly when ω=0. This also checks the sign of the multiplier-frequency identification against [MS, equations (4), (18), (19)].

## 6. Subthreshold compactness and continuity of the value

Let mn be bounded in H¹, Q(mn)=0, and limsup Eκ(mn)<8π. After subselection mn⇀m in H¹, mn→m strongly in L² and almost everywhere. Apply [BCL] to the Jacobians. Let μ be a weak limit of the energy measures ½|∇mn|²dσ. Local weak lower semicontinuity gives μ≥½|∇m|²dσ. Since |ρmn|dσ≤½|∇mn|²dσ, each Jacobian atom 4πqiδxi forces μ({xi})≥4π|qi|. Adding the diffuse lower bound and these finitely many atom bounds, and using continuity of Aκ under L² convergence, yields

Eκ(m)+4πΣi|qi|≤liminf Eκ(mn),
Q(m)+Σi qi=0.                                      (6.1)

If any qi is nonzero, the right side is at least

4π(|Σi qi|+Σi|qi|)≥8π.

The last inequality holds for every nonempty finite list of nonzero integers: either the sum is nonzero, or at least one positive and one negative integer occur. This contradicts the strict subthreshold bound. Therefore there are no Jacobian atoms. In particular Q(m)=0 and J(mn)→J(m). This is only weak compactness with constraint continuity at this stage; it does not yet assert strong H¹ convergence of arbitrary subthreshold sequences.

Fix j0∈Iκ. Applying a local correction at one minimizer in M(j0) gives limsupj→j0e(j)≤e(j0)<8π. If jn→j0 and mn∈M(jn), the preceding paragraph applies after discarding finitely many terms. Its weak limit m satisfies Q(m)=0 and J(m)=j0a, so

e(j0)≤Eκ(m)≤liminf e(jn)≤limsup e(jn)≤e(j0).

All quantities are equal. Hence e is continuous, m∈M(j0), and Eκ(mn)→Eκ(m). Since Aκ(mn)→Aκ(m), the Dirichlet norms converge; weak H¹ convergence then upgrades to strong H¹ convergence.

On compact K⊂Iκ, continuity gives a uniform bound maxKe<8π. The same argument for any sequence jn∈K proves strong-H¹ sequential compactness of the union of all M(j), j∈K. It is closed by continuity of the constraints and energy, so it is compact. Section 5 therefore also gives boundedness and attainment of the maximum and minimum of ω on each M(j).

## 7. Uniform upper supports and semiconcavity

Choose a slightly larger compact interval K′⊂Iκ containing K in its interior. Cover the compact minimizing family over K′ by finitely many neighborhoods from Section 4. Taking the smallest correction radius and largest Hessian bound produces common constants η,C. Restrict (4.1) to q′=(j+h)a. At h=0 its derivative is α·a=ω(m), by (5.1), and its second derivative is bounded above by C. Taylor's theorem proves (2.1), uniformly in m and j∈K′ after reducing η.

In particular, use the same minimizing field for h and −h and add the two inequalities:

e(j+h)+e(j−h)−2e(j)≤Ch².                            (7.1)

For f(j)=e(j)−Cj²/2 this is local midpoint concavity. Continuity, iteration on dyadic subdivisions, and a covering by small intervals show that f is concave locally. Thus e is locally semiconcave. Finite concave functions are locally Lipschitz and have finite one-sided derivatives at interior points, with f′+≤f′−. The intervals (f′+(j),f′−(j)) for different nondifferentiability points are disjoint; assigning a rational number to each nonempty interval shows that there are at most countably many such points. These statements transfer to e.

The same uniform support inequality bounds the multipliers by observable finite-difference slopes whenever 0<h<η:

[e(j+h)−e(j)]/h−Ch/2 ≤ ω(m)
≤ [e(j)−e(j−h)]/h+Ch/2.                            (7.2)

This is a rigorous estimate with a nonexplicit local remainder constant. It is not an effective numerical frequency estimate without additional information about e and C.

## 8. Exact one-sided slope formulas

From (2.1), division by h>0 and passage to the limit gives e′+(j)≤ω(m) for all m∈M(j). Similarly, division by h<0 reverses the inequality and gives e′−(j)≥ω(m). This proves one inequality in each formula (2.2).

For the reverse right inequality, take h↓0 and mh∈M(j+h). Apply the uniform support based at mh with increment −h:

e(j)≤e(j+h)−ω(mh)h+(C/2)h².

Therefore [e(j+h)−e(j)]/h≥ω(mh)−Ch/2. Any sequence h→0 has a subsequence along which mh converges strongly in H¹ to m0∈M(j); multiplier continuity gives ω(mh)→ω(m0). Since the right derivative exists, e′+(j)≥ω(m0)≥minM(j)ω. This proves the first equality.

For h<0 the same inequality, divided by h, gives [e(j+h)−e(j)]/h≤ω(mh)−Ch/2. Subsequential compactness and multiplier continuity give e′−(j)≤maxM(j)ω. This proves the second equality.

At differentiability points the minimum and maximum coincide, so every minimizing multiplier equals e′(j). Combined with Section 5, this proves the non-staticity criterion in Section 2.

## 9. Elementary bounds and exact unresolved obstruction

For every admissible field,

|J|≤|S|+|L|≤4π+D≤4π+Eκ.

For a minimizer with j>4π, equality e(j)=j−4π would force |S|=4π, hence m is a constant unit vector almost everywhere. Such a field has |J|=4π, a contradiction. Thus

j−4π<e(j)<8π,  j∈Iκ.                              (9.1)

Neither (9.1) nor semiconcavity rules out a constant segment of e or an isolated zero derivative. The trial fields in [MS] give upper bounds; an upper bound alone does not determine the derivative of the true minimum. Symmetry of unconstrained minimizers would concern global free minima, whereas a constrained minimizer with ω=0 could be another stationary field. No such symmetry or stationary classification has been proved here.

The gap is now precise: to prove all the obtained smooth solutions non-static throughout Iκ, one must exclude 0 from the multiplier set of every smooth minimizer there. At differentiability points this is exactly e′(j)≠0. At a corner, knowing only e′+(j)≤0≤e′−(j) neither proves nor refutes existence of a zero-frequency minimizer: zero may lie between two nonzero multipliers.

An abstract countermodel guards against a logical shortcut, but is **not** a counterexample in the spherical model. On the symplectic cylinder S¹×I with coordinates (θ,p), let the circle rotate θ, momentum be p, and Hamiltonian H≡c with 0<c<8π. The action is free, the momentum derivative is nonzero, every point minimizes at fixed p, and the Hamiltonian frequency is zero. Thus a nonzero symmetry generator and regular momentum constraint alone cannot establish motion. Similarly, the elementary envelope min(2h+h²,−h+2h²) has left slope 2 and right slope −1 at zero, while its two active branch slopes are both nonzero. These examples justify the logical cautions only.

**Full-target conclusion:** unresolved. The proved bounded result is the compactness/semiconcavity/envelope theorem above and its exact conditional non-staticity test. No full energy law, sign theorem, nonzero lower frequency bound, explicit endpoint asymptotic, or counterexample to the spherical target is claimed.

## References and credit

[MS] C. Melcher and Z. N. Sakellaris, *Curvature stabilized skyrmions with angular momentum*, arXiv:1902.04881v2 (1 May 2019), published in Letters in Mathematical Physics 109 (2019), 2291–2304. https://arxiv.org/abs/1902.04881 ; https://doi.org/10.1007/s11005-019-01188-6 . Model and existence: PDF pp.1–3. Momentum calculus: pp.4–6. Strict competitors and attainment: pp.7–9. The energy-dependence/non-staticity question is explicitly posed on p.3.

[OWR] C. Melcher, joint work with Z. N. Sakellaris, *Emergent spin-orbit coupling in a spherical magnet*, in Oberwolfach Report 22/2020, *Calculus of Variations*, DOI 10.4171/OWR/2020/22, printed pp.1168–1171. https://ems.press/content/serial-article-files/46860 . The exact model and theorem are on pp.1169–1170 and the question on p.1171. The workshop occurred in August 2020; the imported record's parenthetical 2021 should not replace the report number.

[BCL] H. Brezis, J.-M. Coron, and E. H. Lieb, *Harmonic Maps with Defects*, Communications in Mathematical Physics 107 (1986), 649–705. DOI 10.1007/BF01205490. https://sites.math.rutgers.edu/~brezis/PUBlications/112-Journal.pdf . Appendix E, Theorem E.1, proof, and Corollary E.5 on printed pp.699–702, PDF pp.51–54, supply the quantization input.

The derivation is a bounded application of established compactness, symmetry, and variational-envelope methods; no priority claim is attached to it. Bounded current-source checking did not find an exact later replacement theorem, which is not an exhaustive open-status certificate.
