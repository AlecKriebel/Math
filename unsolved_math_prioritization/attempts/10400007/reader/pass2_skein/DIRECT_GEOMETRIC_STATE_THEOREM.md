# PASS2: direct geometric exterior states from vacua and sewing

14 October 2026 UTC. This strengthens the accepted PASS1 construction. It does not retract any PASS1 theorem and does not claim novelty. The definition below does **not** take the WRT exterior vector as an input. WRT appears afterward in the comparison proof.

## 1. Result and exact improvement

For every smooth oriented knot K in oriented S³ and every integer level k≥1, its peripheral exterior determines a class in ordinary H₀ of the Andersen–Ueno geometric local system on the boundary torus. A relative Heegaard presentation computes this class using only:

- the geometric sphere vacuum;
- the geometric sewing isomorphisms and their inverses;
- projection to specified sewing-label summands;
- propagation of vacuum labels;
- the geometric extended-surface action;
- one geometric torus normalization scalar.

The fundamental filling is a label-1 coordinate after meridian factorization. It does not require importing a higher-genus orientation-duality pairing. The normalized contraction equals V_K(exp(−2πi/(k+2))). PASS1's finite interpolation then recovers the full polynomial from 4c+1 levels for any c-crossing diagram.

This removes the exact PASS1 definitional dependency h(K):=ν Z_RT(E_K)(1). The resulting class is subsequently **proved** equal to that vector. The strengthened statement remains a geometric reconstruction of known CFT/WRT theory, rather than a new quantum invariant. Its broader explanatory status is a separate scope question; no additional prohibition on H₀ or on comparison proofs is used.

## 2. Geometric input available before WRT comparison

Use Andersen–Ueno, *Geometric construction of modular functors from Conformal Field Theory*, arXiv:math/0306235v2. For an extended marked surface Σ, let

  W_k(Σ)=H⁰(T(Σ);L_k(Σ)),
  H_k(Σ)=H₀(T(Σ);L_k(Σ)),

where L_k is the horizontal-section local system of their ghost-corrected vacua bundle. The canonical identification θ:W_k→H_k sends a horizontal section s to [x,s(x)]. The coefficient ring is C; support is ordinary singular homology; the degree is zero. The local system and its mapping-class equivariance are independently geometric, as established in PASS1.

Their geometric data needed here have the following exact source locations:

- §4.1 fixes a vacuum vector and nonzero invariant vectors |0_{λ,λ†}⟩ in V_λ⊗V_{λ†}.
- Lemma 4.1 specifies the affine-module pairing normalized to evaluate to 1 on that vector.
- Definition 11.3 takes horizontal sections; Theorem 11.4 supplies flat-bundle naturality.
- Theorem 12.1 constructs sewing on flat sections; Theorem 12.2 proves independence of complex structures and coordinate choices.
- Definitions 12.1–12.2 specify sewing also for unstable surfaces; Proposition 12.2 handles added vacuum points.
- Proposition 12.3 and Theorem 12.3 give surface naturality; Proposition 12.4 and Theorem 12.4 give disjoint-union compatibility and commuting sewings.

[Primary geometric paper](https://arxiv.org/pdf/math/0306235v2)

In particular, sewing is an independently constructed map, not a transported RT map. Locally it comes from the convergent sewing expression with graded dual bases, of the form

  Σ_{d≥0} τ^(Δ_λ+d) Σ_i Ψ(v_i(d)⊗v^i(d)⊗−),

tensored with the abelian correction and continued horizontally. The exact source is §14.4, equation (80), and Theorem 14.6 proves convergence and the horizontal equation; equation (82) and Theorem 14.7 handle the abelian factor. For sl₂, Δ_λ=λ(λ+2)/(4(k+2)). The fixed normalized pairings determine the dual bases. We use the actual geometric sewing maps, not an unevaluated formal series.

## 3. Direct vacuum, projection, and stabilization scalar

The label set is {0,1,…,k}, with 0 the vacuum and 1 the fundamental representation.

### 3.1 Handlebody vacuum

Let H be a genus-g handlebody. Give its boundary Σ_H the Lagrangian

  Λ_H=ker[H₁(∂H;Q)→H₁(H;Q)].

Choose a complete meridian disk system D. Cutting the boundary along its g curves and capping the resulting circles yields a sphere with 2g marked points. Geometric sewing gives

  G_D: ⊕_{λ₁,…,λ_g} W_k(S²;λ₁,λ₁†,…,λ_g,λ_g†) → W_k(Σ_H).

The all-zero summand is canonically identified with C by propagation of vacua. Define

  v_D=G_D(1 in the all-zero summand).

No exterior invariant or RT state appears in this definition. Disk-system independence is proved below; it is not assumed from the notation.

### 3.2 Compression projection

Let C be a compressionbody regarded as a cobordism Σ_C→T, where T is a torus. Let δ₁,…,δ_{g−1} be a complete set of nonseparating compression curves, so compressing Σ_C along them yields T. Give T the prescribed peripheral meridian Lagrangian Λ_T=Qm. Give Σ_C the transported Lagrangian

  Λ_C={x∈H₁(Σ_C;Q): i_Σ(x)∈i_T(Λ_T)⊂H₁(C;Q)}.

It contains the compression curves and has dimension g. Apply inverse geometric sewing, project to the all-zero label tuple, and remove those vacuum points by propagation. This defines

  p_C:W_k(Σ_C)→W_k(T).

This is a coordinate projection supplied by geometric factorization. It is not defined as a cobordism map.

When applying AU's integral-lattice convention, use the primitive integral lattices underlying the displayed rational Lagrangians. For a compressionbody the preimage above is saturated; the meridian is primitive. Thus this notation is compatible with their marked-surface input.

### 3.3 Torus calibration

On a standard peripheral torus, choose meridian a and longitude b. Let e₀ be the vacuum obtained by sewing a sphere with two vacuum points along a. Let ε₀ be the corresponding vacuum coordinate. Let S₀ be the geometric extended mapping class a↦b, b↦−a with weight zero, in the extended-surface convention used below. Gluing its mapping cylinder between the two standard vacuum solid tori gives the weight-zero S³: the relevant Maslov correction has a repeated meridian entry. This specifies the lift used for calibration, rather than an arbitrary projective representative. Define

  s_k=ε₀(W_k(S₀)e₀),   D_k=s_k^(−1).

Both are obtained from geometric surface operations. The comparison proof below shows that s_k is nonzero and, in the standard unitary SU(2) normalization,

  s_k=√(2/(k+2)) sin(π/(k+2)).

The formula is a verification of the geometric scalar, not its definition. The inverse factor is necessary: a raw projection alone does not satisfy relative Heegaard stabilization.

## 4. Definition of the knot-exterior class

Let E_K=S³\int(N_K), T=∂E_K, and retain the meridian m and preferred longitude ℓ. The longitude supplies the preferred zero-framing. Choose a relative Heegaard decomposition

  E_K=H_g∪_f C,

where H_g is a handlebody and C compresses the Heegaard surface to T. This exists for every knot exterior. Use Λ_H and Λ_C as in §3 and the weight-zero extended gluing diffeomorphism f₀:Σ_H→Σ_C. Define, directly,

  h_k^geom(K;H,C,f,D,δ)
   = θ_T[D_k^(g−1) p_C W_k(f₀) v_D] ∈ H_k(T).

Every operation on the right was geometrically specified in §2–3. The knot enters through the relative Heegaard gluing map and the two disk systems determined by the exterior decomposition. It does not enter through a precomputed scalar or a preassigned WRT exterior state.

The equivalent all-homology formula conjugates only the independently defined **surface** sewing/projection/transport maps through θ. These are specified linear maps on local-system homology; no claim that every sewing projection is the pushforward of an ordinary continuous map between Teichmüller spaces is needed. This is distinct from defining the entire exterior map by conjugating an existing three-dimensional RT map.

### Anomaly bookkeeping

Use the Gilmer–Masbaum extended-manifold convention

  w(M∪_ΣM′)=w(M)+w(M′)−μ_Σ(Λ_M(Σ),Λ(Σ),Λ_M′(Σ)).

Give H, the gluing mapping cylinder, and C weight zero. In the first gluing, the handlebody kernel agrees with Λ_H. In the second, the Lagrangian transported backward through C from Λ_T agrees with Λ_C. Each Maslov correction therefore has repeated entries and vanishes. The formula computes the weight-zero exterior, without suppressing a projective scalar. [Gilmer–Masbaum, §2, equation (1) and Lemma 2.1](https://arxiv.org/pdf/0912.4706v3)

## 5. Definition of the fundamental filling functional

Factor T along its meridian m:

  F_m:W_k(T)→⊕_{λ=0}^k W_k(S²;λ,λ†).

The label-1 summand is one-dimensional. Use the fixed normalized pairing of §2 to choose its nonzero geometric coordinate c₁:W_k(S²;1,1†)→C. Concretely, on the standard two-pointed sphere with its chosen local directions, trivialize the abelian correction by the preferred sphere section and evaluate the conformal block on |0_{1,1†}⟩. The normalized block u₁ has c₁(u₁)=1. Define

  ε₁^m=c₁ pr₁ F_m,
  f_k^geom=ε₁^m θ_T^(−1).

There is no use of an orientation-duality pairing on a genus-g space in this definition. Changing the one-dimensional coordinate by a nonzero scalar multiplies every numerator and the unknot denominator by the same scalar. Thus that harmless global gauge need not be canonically suppressed.

The meridian/longitude framing determines the sewing identification; a meridional Dehn twist changing the core framing is not silently regarded as the same peripheral input.

Define

  z_k^geom(K)=f_k^geom(h_k^geom(K))/f_k^geom(h_k^geom(U)).

The two contractions are scalars and need no identification between the two knots' torus spaces. The same geometric gauge and framing convention are used.

## 6. Comparison proof, including the compression normalization

Only now invoke Andersen–Ueno's established isomorphism I from the SU(2) skein/WRT modular functor to W_k. Theorem 1.1 of arXiv:1110.5027v2 respects all surface structures. Fix the vacuum-unit normalization. The resulting comparison sends the geometric vacuum sector, sewing maps, inverse sewing projections, propagation, and extended surface action to the corresponding RT modular-functor operations. [Primary comparison paper](https://arxiv.org/pdf/1110.5027v2)

The following elementary RT normalization calculation identifies the **independently defined** recipe with its intrinsic state:

1. The genus-g empty-handlebody vector is the all-zero sewing vector. In the skein picture each vacuum label is the tensor unit, so inserting the all-zero channel inserts no nontrivial colored strand.
2. Adding a nonseparating 1-handle is the vacuum inclusion i₀. Attaching the reverse 2-handle kills nonvacuum cut labels and is a scalar multiple a·p₀ on the vacuum channel.
3. A cancelling 1–2 handle pair attaches the 2-handle along a curve dual to the belt curve. In the isolated genus-one factor its raw composite is p₀ S₀ i₀=s_k. Handle cancellation forces a s_k=1. Hence a=D_k.
4. Locality of sewing makes this the same factor on each nonseparating compression. Therefore a genus-g-to-torus compressionbody contributes D_k^(g−1)p_C.

The killing of the nonvacuum sectors and the locality used here are the standard colored splitting rule. BHMV's proof of the Colored Splitting Theorem and Corollary 4.10 also show that torus core-label vectors are orthonormal and that a reverse handle contributes the inverse vacuum gluing scalar. The comparison proof may use RT duality for this check; duality was not used to define p_C or the filling. [BHMV, §4.9–4.11](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bhmv.pdf)

More explicitly, on the vacuum sector the splitting formula gives

  ⟨i₀x,i₀y⟩_sewn=D_k⟨x,y⟩_cut,

while different cut-label sectors are orthogonal. Consequently, for arbitrary y,

  ⟨i₀x,y⟩_sewn=D_k⟨x,p₀y⟩_cut.

The RT reverse-handle map is the adjoint of i₀, so it is exactly D_k p₀. This proves the coefficient on every genus and every lower-surface state, not just on one test vector. The geometric recipe itself uses neither these RT inner products nor this adjoint as input.

It follows, by this generator-by-generator calculation rather than by definition, that

  h_k^geom(K)=θ_T I_T Z_k^RT(E_K,weight 0)(1).

The geometric filling is the RT fundamental-core functional up to the single nonzero label-1 gauge factor. This follows from the orthonormal torus core-label basis, or by cutting the filling disk to the normalized two-point block. The same factor occurs for every knot and cancels in z_k^geom.

This proves that the direct recipe is invariant under changes of complete disk systems, handle slides, Heegaard isotopies, stabilizations/destabilizations, and all changes of relative Heegaard presentation: each presentation has just been shown to compute the state of the same weight-zero exterior. Equivalently, the known RT relations prove relations among the independently constructed geometric expressions. Such a comparison proof is permitted by PASS2 and is not a definition by importing the final exterior state.

The torus vacuum matrix element is nonzero; the fundamental matrix element is

  S₁₀=√(2/(k+2)) sin(2π/(k+2))=d₁/D_k,
  d₁=2cos(π/(k+2))≠0.

Thus the unknot denominator is nonzero at every k≥1. In another fixed label-1 gauge the same nonzero scalar multiplies it. The displayed SU(2) matrix formula is also recorded in [Ginsparg, *Applied Conformal Field Theory*, equation (9.50a)](https://homes.psd.uchicago.edu/~sethi/Teaching/P483-F2003/ginsparg.pdf), with spin indices j=λ/2.

## 7. Naturality and full Jones agreement

An orientation-preserving diffeomorphism of knot pairs transports the peripheral data and any chosen relative Heegaard decomposition to one for the target exterior. Geometric surface naturality transports the formula term by term. The preceding independence result then removes any need to make a canonical choice of Heegaard splitting. The output is a class naturally assigned to the peripheral exterior, with the specified filling functional, rather than merely an invariant of a selected decomposition.

The exterior/filling composition has weight zero because μ(Qℓ,Qm,Qm)=0. The normalized scalar therefore agrees with the weight-zero fundamental-colored S³ ratio. By the already audited PASS1 convention calculation,

  z_k^geom(K)=V_K(t_k),   t_k=exp(−2πi/(k+2)).

This is for knots. The auxiliary link skein calculation uses a component-parity sign and total writhe; no unexamined multi-component zero-framing theorem is claimed.

If c is the crossing count of any diagram, take B=2c and k=1,…,2B+1. Define

  P_K(t)=t^(−B) Σ_k t_k^B z_k^geom(K)
                    ∏_{j≠k}(t−t_j)/(t_k−t_j).

The PASS1 degree-bound proof gives supp(V_K)⊂[−B,B], so exact Lagrange interpolation proves P_K=V_K in Z[t,t^(−1)]. The diagram supplies only the finite bound, not the states or coefficients.

## 8. Dependency analysis: removed and remaining

**Removed:** the exterior class is no longer introduced by writing ν Z_RT(E_K). It has a complete geometric rule determined by the exterior's Heegaard data and AU vacuum/sewing/transport. The filling has a direct sector-coordinate definition. The comparison theorem verifies the recipe and its independence after the definition.

**Still present and explicit:** proof of decomposition independence here uses the existing CFT/WRT comparison and the known RT cobordism relations. The coefficient systems are geometric CFT systems on surface Teichmüller spaces; H₀ itself remains canonically equivalent to horizontal sections. This report does not claim a new local system on a knot-complement character variety or a positive-degree complement configuration group.

The exact PASS1 dependency objection has consequently been addressed. If further explanatory adequacy is withheld, it must be justified by a remaining substantive issue in this independently defined geometric account, not by repeating the now-inaccurate assertion that no rule for the exterior state was supplied except importing Z_RT(E_K). Whether this reconstruction is the explanation intended by Roberts remains a separate source-faithful adjudication, with no forced historical or novelty conclusion.
