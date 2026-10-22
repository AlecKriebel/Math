# KP-4.96: closed uniqueness remains unresolved

## 0. Scope and verdict

**Unsolved after five substantive attempts.** No closed four-dimensional counterexample, universal uniqueness theorem, or claim of novelty is established here. The results below are reductions, restricted uniqueness statements, and counterexamples to proposed shortcuts.

The target from K3, Problem 4.96 (printed pp. 269–270), asks for symplectic four-manifolds whose smooth identification preserves both the symplectic cohomology class and first Chern class, but which admit no symplectomorphism. Its sentence omits “closed.” Here the research target is explicitly the **closed interpretation**: compact, without boundary. A literal interpretation admitting noncompact manifolds or boundary is much weaker; §7 explains this distinction. The separate Stein-filling question in Remark 2 is not silently substituted for the closed target.

All diffeomorphisms and forms are smooth. Cohomology of forms has real coefficients; first Chern and Spin-c classes retain their integral information. For a fixed closed connected smooth oriented four-manifold M and a class a with positive square, write

    S_a = {symplectic forms on M representing a and its prescribed orientation},
    G_a = {g in Diff^+(M) : g^*a = a}.

The precise unresolved target is the existence of M,a for which S_a/G_a has at least two elements.

## 1. First reduction and the distinction between the two quotients

Pull back the second form by the comparison diffeomorphism f. This replaces the question by two forms on one manifold. If g^*f^*ω₂=ω₁, then f∘g is a symplectomorphism, so this replacement preserves the required nonexistence condition in both directions.

**Imported theorem (Taubes–Seiberg–Witten, in Salamon, Corollary A).** On a closed smooth four-manifold, cohomologous symplectic forms induce the same canonical Spin-c structure, and consequently the same integral first Chern class. Thus the Chern condition adds no restriction to the fixed-class closed problem. This is already known; it is also used in Iida, Proposition 1.4.

For clarity about torsion, Salamon's proof compares the canonical Spin-c structures as Γ₁=Γ₀+e. Taubes's nonvanishing and positivity force a·e≥0; swapping the forms forces a·e≤0. The equality case forces e=0, not merely 2e=0. In the b⁺=1 case the chambers agree because the symplectic cohomology classes agree. This argument uses the full cited Taubes input; it is not a new proof of that input.

**Proposition 1 (Moser and orbit reduction).** Two forms in S_a are in the same smooth path component if and only if a diffeomorphism isotopic to the identity pulls one back to the other. Consequently the closed target asks for two distinct G_a-orbits of path components, not just two path components.

*Proof.* Let ω_t be a smooth path with constant class. Fix a metric. Hodge theory supplies primitives η_t depending smoothly on t with dη_t=∂_tω_t: for example, apply the fixed Green operator and d* to each exact derivative. Define V_t uniquely by ι_{V_t}ω_t=−η_t. Compactness gives its flow φ_t for 0≤t≤1. Cartan's formula gives

    d/dt (φ_t^*ω_t) = φ_t^*(dη_t + dι_{V_t}ω_t) = 0.

Thus φ₁^*ω₁=ω₀. Conversely, if φ_t is an isotopy from the identity to φ, the forms φ_t^*ω₁ give a constant-class symplectic path from ω₁ to φ^*ω₁. Finally, G_a acts on the path components by pullback. If g^*ω₁ and ω₀ are in the same component, Moser supplies φ with φ^*g^*ω₁=ω₀, hence g∘φ is a symplectomorphism. The converse is immediate. ∎

The positive-square assumption also removes an orientation ambiguity. If a comparison diffeomorphism between connected closed symplectic four-manifolds pulled back the class but reversed their symplectic orientations, integration of the square would give a positive number equal to a negative number.

## 2. A complete test for the straight-line attempt

**Proposition 2 (pointwise criterion).** Let α and β induce the same orientation on a four-manifold. Relative to a positive volume form ν, put

    α∧α = Aν,   α∧β = Bν,   β∧β = Cν,

where A,C>0 pointwise. Every member of (1−t)α+tβ, 0≤t≤1, is nondegenerate if and only if

    B > −sqrt(AC)

at every point. For cohomologous closed forms on a closed manifold, this condition implies symplectomorphism.

*Proof.* Its wedge square divided by ν is

    q(t) = A(1−t)^2 + 2Bt(1−t) + Ct^2
         = ((1−t)sqrt(A)−t sqrt(C))^2
           + 2t(1−t)(B+sqrt(AC)).

The displayed strict inequality makes q positive, including both endpoints. At t=sqrt(A)/(sqrt(A)+sqrt(C)), the first summand vanishes; if the inequality fails, q is nonpositive there. A negative value forces a zero between that time and an endpoint. Thus failure of the inequality prevents a wholly nondegenerate segment. Closedness and equality of cohomology persist under linear interpolation, so Proposition 1 finishes the last assertion. ∎

An equivalent test avoiding square roots is: B≥0, or B<0 and AC>B². Equality is a genuine degenerate boundary case.

**Corollary 2.1 (common taming).** If a single almost complex structure J is tamed by both cohomologous symplectic forms on a closed manifold, the forms are symplectomorphic.

*Proof.* For every nonzero v, each convex combination has positive value on (v,Jv). It is therefore nondegenerate. Apply Moser. ∎

This criterion does not follow from cohomology or equality of Chern classes. Nor does failing it prove nonsymplectomorphism, as the next construction demonstrates.

## 3. A closed-manifold negative control for the straight-line strategy

**Proposition 3.** On every closed symplectic four-manifold (M,ω), there is a diffeomorphism F isotopic to the identity such that ω and F^*ω are cohomologous, have identical Chern classes, and are symplectomorphic, but their midpoint form vanishes on a nonempty open set.

*Proof.* Choose a Darboux ball with coordinates (x₁,y₁,x₂,y₂) and ω=dx₁∧dy₁+dx₂∧dy₂. Choose a smooth radial cutoff χ(r²), equal to one on a smaller ball and zero near the outside of the coordinate ball. Extend the vector field

    V = π χ(r²)(−y₂ ∂/∂y₁ + y₁ ∂/∂y₂)

by zero to M. Its flow exists globally and fixes r² because V(r²)=0. On the smaller ball its time-one map is

    F(x₁,y₁,x₂,y₂) = (x₁,−y₁,x₂,−y₂).

Consequently F^*ω=−ω there. This transformation preserves four-dimensional orientation, with determinant +1. Globally, F is the time-one map of a compactly supported flow, so it is isotopic to the identity. Pullback preserves closedness and nondegeneracy; the isotopy gives [F^*ω]=[ω] and F^*c₁=c₁. By definition, F is a symplectomorphism from (M,F^*ω) to (M,ω). Nevertheless (ω+F^*ω)/2=0 on the smaller ball. ∎

Here the original endpoints even have equal volume forms pointwise in the smaller ball. Their common first Chern class cannot prevent the local affine degeneracy. No J tames both endpoints at those points: ω(v,Jv)>0 and −ω(v,Jv)>0 are incompatible.

## 4. An explicitly excluded symmetric family on the four-torus

This is a deliberately restricted subproblem, not a substitute for the target. It is contained in the broader known circle-invariant uniqueness result of Hajduk–Walczak (arXiv version, Corollary 2.11).

**Proposition 4.** On T⁴=(R/Z)_t×(R/Z)³_y, any two cohomologous symplectic forms invariant under all translations in y₁,y₂,y₃ are connected by their straight-line segment, hence symplectomorphic.

*Proof.* Every such closed form has the unique shape

    ω = dt∧(a₁(t)dy₁+a₂(t)dy₂+a₃(t)dy₃)
        + b₁dy₂∧dy₃+b₂dy₃∧dy₁+b₃dy₁∧dy₂,                (4.1)

where the a_i are smooth periodic functions and the b_i are constants. Indeed, invariance allows only t-dependent coefficients, and closedness forces the coefficients of dy_i∧dy_j to be constant. Its square is

    ω² = 2(a₁(t)b₁+a₂(t)b₂+a₃(t)b₃) dt∧dy₁∧dy₂∧dy₃.     (4.2)

The six coordinate two-tori show that its class is determined by b_i and the averages ā_i=∫₀¹a_i(t)dt. Conversely, a_i−ā_i has a periodic primitive A_i, so subtracting the constant-coefficient representative changes ω by d(Σ A_i dy_i).

For a cohomologous pair, the b_i and ā_i agree. Each scalar a(t)·b is nowhere zero and has the same integral ā·b, so both have the same sign. Their convex combinations are therefore nowhere zero. Formula (4.2) proves nondegeneracy along the entire affine path. Moser proves the assertion. ∎

In particular averaging these invariant forms succeeds because the wedge-square condition has become linear in a(t). Averaging an arbitrary symplectic form over a compact group has no such general positivity guarantee. Proposition 3 already refutes the proposed general convexity premise.

## 5. Why pullback constructions and stabilization do not close the gap

**Proposition 5 (pullback-family obstruction).** If ω_i=f_i^*ω on a fixed smooth manifold, then every two members of the family are symplectomorphic, regardless of whether the f_i are isotopic or preserve cohomology.

*Proof.* For h=f_j^(-1)∘f_i,

    h^*ω_j = (f_j∘h)^*ω = f_i^*ω = ω_i.

Thus h is the required symplectomorphism. ∎

This explains exactly why the Lin–Wu construction does not answer this problem. Their Theorem 1.2 detects infinitely many fixed-class path components on irrational ruled surfaces, but its defining family in the proof is (f_γ^m)^*ω_μ. Proposition 5 disposes of the all-diffeomorphisms test without needing to reproduce the Dax-invariant calculation. The difference between the two quotients in Proposition 1 is essential in current examples, not merely hypothetical.

Ning's Theorem 1.3 constructs inequivalent cohomologous forms after taking a product with S². Its base four-manifolds are homeomorphic but not diffeomorphic. The stable six-dimensional diffeomorphism cannot simply be restricted to identify the bases. Moreover, the two forms there have different Chern classes. Neither the dimensional requirement nor the closed four-dimensional Chern constraint is met. No desuspension argument is established here.

The newer Li–Ning uniqueness results restrict the forms to Kähler-type or holomorphically tamed classes under specified hypotheses. Equality of cohomology alone does not put an arbitrary symplectic form in those subclasses.

## 6. The cap-gluing attempt and an exact obstruction to an easy version

**Proposition 6 (relative affine Moser).** Let W be compact with boundary. Suppose η is a smooth one-form vanishing on a collar of ∂W, and every form ω_t=ω₀+t dη is symplectic. Then there is a diffeomorphism φ of W, equal to the identity near its boundary and isotopic to the identity there, with φ^*ω₁=ω₀. If the forms extend identically across a common cap, the same conclusion holds on the glued closed manifold.

*Proof.* Solve ι_{V_t}ω_t=−η. The vector field vanishes on the collar, so its flow exists for the full time interval and is the identity near the boundary. The derivative calculation in Proposition 1 applies. Extend that flow by the identity on the cap. ∎

Thus a local alteration made through a nondegenerate exact segment with a compactly supported primitive cannot produce the desired closed pair.

The relative and closed questions have different cohomological constraints. For example, take W=S²×D² with ω₀=σ+τ, where σ and τ are positive area forms. Choose a nonnegative smooth function f supported inside D² with ∫fτ>0, and let ω₁=σ+(1+εf)τ for ε>0. These forms agree near ∂W and have the same absolute degree-two class because the disk contribution is exact. Nevertheless

    (1/2)∫_W(ω₁²−ω₀²) = ε(∫_S²σ)(∫_D²fτ) > 0,

so they are not symplectomorphic. The difference has no primitive vanishing near the boundary: integrating it over {p}×D² would contradict Stokes. On a closed manifold cohomologous forms have equal total volume, so the same volume argument cannot survive capping while preserving the absolute cohomology class. This W is not Stein and is not offered as a Stein-filling example.

Iida's 2026 preprint provides a substantially subtler, normalized relative construction, which it explicitly separates from the closed question. The boundary contactomorphism used to identify the fillings need not extend over the filling. Its non-equivalence arguments are therefore not a theorem that arbitrary common cappings produce cohomologous, nonsymplectomorphic forms on a single closed manifold.

To turn a relative example into a solution here one must prove, rather than assume: existence of suitable closed symplectic gluings; a global smooth identification matching their degree-two classes; and an obstruction to every global symplectomorphism, including those that move the chosen cap. None of those conclusions follows just from the inequivalence of the fillings. No construction satisfying all these requirements was obtained.

## 7. Literal nonclosed wording is not the research conclusion

If noncompact manifolds are allowed, there is an elementary affirmative example. Let Ω be the standard form on R⁴ and let

    h(x)=x/sqrt(1+|x|²),

a diffeomorphism from R⁴ to the open unit ball. Both Ω and h^*Ω are symplectic; their degree-two and first Chern classes vanish because R⁴ is contractible. The first has infinite volume while the second has volume π²/2. A symplectomorphism preserves the positive measure determined by ω²/2, so none exists. This example is not closed. It does not settle the intended closed version.

Likewise, rescaling a compact Stein ball changes volume while preserving its contact plane field and c₁. It is not a counterexample to Weinstein equivalence, because positive scaling gives a Weinstein homotopy. The normalized filling question removes this elementary scale ambiguity; Iida discusses precisely that distinction.

## 8. Exact remaining gap

The following have not been proved or constructed:

- A closed M, a fixed a, and ω₀,ω₁∈S_a outside one another's G_a-orbits.
- A theorem saying G_a acts transitively for every closed symplectic four-manifold.
- A symplectic invariant distinguishing such a closed fixed-class pair.
- A capping procedure that supplies all the missing data listed in §6.

The checked finite algebra is evidence for the displayed identities and boundary cases only. It cannot establish a statement about all smooth four-manifolds. The principal outcome is an honest unresolved gap together with reusable tests that reject several false-positive routes.

## References

- R. İ. Baykur, R. C. Kirby and D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, Problem 4.96, pp. 269–270. [Author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- D. Salamon, *Uniqueness of Symplectic Structures*, §§2.1–2.7 and Corollary A. [arXiv:1211.2940v5](https://arxiv.org/abs/1211.2940v5).
- B. Hajduk and R. Walczak, *Symplectic forms invariant under free circle actions on 4-manifolds*, Corollary 2.11 in the arXiv version. [arXiv:math/0312465](https://arxiv.org/abs/math/0312465).
- J. Lin and W. Wu, *Infinite connected components of the space of symplectic forms on ruled surfaces*, Theorem 1.2 and its proof. [arXiv:2507.14636v2](https://arxiv.org/abs/2507.14636v2).
- S. Ning, *Cohomologous symplectic forms with different Gromov widths*, Theorem 1.3 and §4. [arXiv:2505.09550v1](https://arxiv.org/abs/2505.09550v1).
- T.-J. Li and S. Ning, *The spaces of Kähler and holomorphically tamed symplectic forms on closed 4-manifolds*, §§1.2–1.4. [arXiv:2607.18778v1](https://arxiv.org/abs/2607.18778v1).
- N. Iida, *Stein structures not determined by the contact boundary*, Proposition 1.4, Theorem 1.8, Theorems 7.7 and 9.1, Remark 10.2. [arXiv:2608.09361v2](https://arxiv.org/abs/2608.09361v2).
