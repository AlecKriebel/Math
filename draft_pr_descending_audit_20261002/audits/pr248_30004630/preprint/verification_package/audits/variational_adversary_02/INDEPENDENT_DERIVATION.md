# Independent variational derivation

Audit: PR248 / 30004630 / OWR-4990378-001. Fresh derivation checkpointed before consulting the submitted independent_review directory. Scope: nonsmooth first-order geometry, exact scalar reduction, global minimum, concentration, and terminal-target stability. The PDE input is the source linear energy/Strichartz estimate; no computed PDE constant is asserted.

## 1. Exact hypotheses and success criteria

Let H=L²(B₁(0)⊂R³), T=1, Dirichlet zero data, and y solve y_tt−Δy+y⁵=u. Set γ=β₁=1, β₂=0, ν≥0 fixed, and U={u: ∥u(t)∥_H≤ρ a.e.}. The normalized first radial eigenfunction is e(x)=sin(π|x|)/(√(2π)|x|), continued smoothly at zero, with eigenvalue π². Set y_d=πe. Let A=∥u∥_{L¹H}, r=∥u∥_{L²H}; then 0≤A≤ρ, A≤r, r²≤ρA.

The claim under test is that the source's ordinary critical-cone strict positivity, with β₂ removed, forces positive L²-squared growth in an L∞ neighborhood. Counterevidence must use actual feasible nonlinear states and a genuine optimizer. A separate stability claim concerns global optimizer selections and target perturbations y_d^ε=(π+ε)e; it does not concern every possible notion of stability.

## 2. Uniform nonlinear input sufficient for the scalar arguments

Give Y the norm sup_t∥(y,y_t)∥_{H₀¹×H}+∥y∥_{L⁴L¹²}. The fixed linear zero-data forcing operator L satisfies ∥Lf∥_Y≤M∥f∥_{L¹H} for a finite M by source Lemma 2.9. Sobolev and Hölder give ∥y⁵∥_{L¹H}≤D∥y∥_Y⁵. The polynomial identity and Hölder on L⁵L¹⁰ give ∥y⁵−v⁵∥_{L¹H}≤D₁(∥y∥_Y+∥v∥_Y)⁴∥y−v∥_Y.

On the closed Y ball R=2MA, y↦L(u−y⁵) maps into itself whenever MD(2MA)⁴≤1/2, and is a contraction if MD₁(4MA)⁴<1. Choose a₀>0 satisfying both conditions, with the second at most 1/2. For 0<A≤a₀ the fixed point is a source mild solution, unique in the source class, and ∥y∥_Y≤2MA. At A=0 the unique solution is zero. With z=Lu and R_u=y−z,

∥R_u∥_Y≤MD(2MA)⁵=:C_R A⁵.

All constants are fixed before choosing ρ, so they are uniform for U when ρ≤a₀. Poincaré and H→H⁻¹ embeddings give terminal constants C_y,C_R' with ∥y(1)∥_H≤C_yA, ∥R_u(1)∥_H+∥(R_u)_t(1)∥_{H⁻¹}≤C_R'A⁵. This is an analytic consequence of an explicit contraction, not a formal Taylor assumption.

## 3. Scalar kernel, exact bathtub, and global uniqueness

Pairing the linear wave equation with e yields

q(u):=⟨e,z(1)⟩=(1/π)∫₀¹ sin(πt)⟨e,u(t)⟩dt.

Expanding the terminal square exactly gives

J(u)−J(0)=A−πq(u)−π⟨e,R_u(1)⟩+(1/2)∥y(1)∥²+(ν/2)∥y_t(1)∥_{H⁻¹}²+(1/4)∥y∥_{L⁴L¹²}⁴.

Every term after the signed error except that error is nonnegative. For f(t)=∥u(t)∥ and s=t−1/2, Cauchy–Schwarz and 1−cos(πs)≥2s² on |s|≤1/2 give

J(u)−J(0)≥2∫_{−1/2}^{1/2}s²f(s+1/2)ds−C₀A⁵, C₀=πC_R'.

For A>0 put b=A/(2ρ)∈(0,1/2]. The functions f and ρ1_{|s|<b} have equal mass. Pointwise, (s²−b²)(f−ρ1_{|s|<b})≥0: both factors have the same sign inside and outside. Integrating cancels the b² mass term, proving

∫s²f≥ρ∫_{−b}^bs²ds=A³/(12ρ²).

The equality density is centered saturated mass, including the endpoint A=ρ (b=1/2, f=ρ a.e.). A=0 is immediate. No radial alignment assumption on u enters this bound. Thus choose 0<ρ≤a₀ with C₀ρ⁴≤1/12, possible because C₀ is fixed and finite. Since A≤ρ,

J(u)−J(0)≥A³/(6ρ²)−C₀A⁵≥A³/(12ρ²).

This verifies the unique global minimizer ū=0 on the entire admissible set. The choice need not be numerically certified: the theorem asserts existence of sufficiently small positive ρ, and a positive rational ρ can be chosen existentially below the bound.

## 4. Subgradient, tangent, normal, and zero critical cone

For j(u)=∫∥u(t)∥_Hdt, j'(0;v)=∥v∥_{L¹H}. On L¹H, ∂j(0) consists of bounded H-valued functions λ with ∥λ(t)∥≤1 a.e.; the same representable subgradients suffice on L²H. Set λ(t)=sin(πt)e and p(t)=−sin(πt)e. Then λ∈∂j(0), F'(0)v=∫⟨p,v⟩, and p+λ=0. The state quartic and velocity costs have zero derivative at zero.

Important topology distinction: U has empty norm interior in L¹H and L²H despite pointwise slack. This does not obstruct the tangent result. For any v∈L^pH, 1≤p<∞, let v_N(t)=v(t)min(1,N/∥v(t)∥). Then v_N→v in L^pH; (ρ/N)v_N∈U, so each v_N is a radial feasible direction. The closed tangent cone is therefore all L^pH. On L∞H, zero is an interior point of U and all bounded v are radial directions directly. Any continuous normal at zero is zero because it is nonpositive on the whole tangent space and its negative. In the source pointwise multiplier language, the inactive set is all times and μ=0 by complementarity.

For any nonzero v in these spaces,

F'(0)v+j'(0;v)=∫(∥v(t)∥−sin(πt)⟨e,v(t)⟩)dt
≥∫(1−sin(πt))∥v(t)∥dt>0.

The strict inequality follows because 1−sin(πt)>0 except at t=1/2, a null set; a nonzero equivalence class cannot be supported there. Hence the ordinary critical cone is exactly {0} in L¹, L² and L∞. Dirac impulses are not elements of these spaces. Source §4.2.2 defines the substitute j''(0;v²)=0 and warns that this is not a conventional derivative. Smooth F''(0)v²=∥z_v(1)∥²+ν∥(z_v)_t(1)∥_{H⁻¹}²; no quartic or quintic second derivative contributes. The condition on nonzero critical directions is vacuous, with no hidden nonvacuity hypothesis in the inspected source.

## 5. Growth violation, with exact leading coefficient

For u_h=h e1_{|s|<h}, 0<h<min(ρ,1/2),

A_h=2h², ∥u_h∥∞=h, r_h²=2h³,
q_h=2h sin(πh)/π², (z_h)_t(1)=0.

The linear sparse/tracking cancellation is d_h=A_h−πq_h=2h²−2h sin(πh)/π. Expansions with exact coefficients yield d_h=(π²/3)h⁴+O(h⁶), q_h²/2=(2/π²)h⁴+O(h⁶). For the actual nonlinear state, the signed tracking error is O(A_h⁵)=O(h¹⁰), mixed square error O(A_h⁶)=O(h¹²), quartic cost O(A_h⁴)=O(h⁸), and velocity cost O(A_h¹⁰)=O(h²⁰). Therefore

J(u_h)−J(0)=[π²/3+2/π²]h⁴+O(h⁶),
[J(u_h)−J(0)]/r_h²=[π²/6+1/π²]h+O(h³)→0.

Both neighborhood norms converge to zero, so positive L²-squared growth fails under either L² or L∞ localization. Genuine global optimality already provides the nonnegative lower bound.

An independent continuous pulse strengthens the check: w_h(t)=h(1−|s|/h)_+e. Then A_h=h², r_h²=2h³/3, ∥w_h∥∞=h, q_h=2(1−cos(πh))/π³ and linear velocity is zero. Its actual nonlinear gap is [π²/12+1/(2π²)]h⁴+O(h⁶), so the corresponding ratio also tends to zero. More generally, any nonnegative fixed smooth compactly supported φ gives u_h=hφ(s/h)e, A=O(h²), r²=Θ(h³), first-order cancellation O(h⁴), and the same failure. Temporal jump discontinuities are inessential.

The normalized rectangular pulse v_h=u_h/r_h has L² norm one, converges weakly to zero (Cauchy–Schwarz on its shrinking support), and has first directional derivative O(h^{5/2}) and F''(0)v_h²=O(h). This directly displays the missing coercivity step in the source proof.

## 6. Perturbed optimizer existence and quantified local meaning

For each small ε>0, global optimizers exist. The source Theorem 4.1 directly applies at ν=0 because γ>0 and constant ω is integrable. For ν≥0, a direct method works here: U is closed convex bounded in L²H, hence weakly compact; all states have uniform Y bounds. Energy bounds and compact H₀¹→H give y_n precompact in C([0,1];H), using equicontinuity from y_t bounded in L∞H. The equation gives y_tt bounded in L∞H⁻¹ because y⁵ is bounded in L∞L^{6/5}⊂L∞H⁻¹ and u is bounded in L∞H. Compact H→H⁻¹ and this equicontinuity give y_{n,t} precompact in C([0,1];H⁻¹).

A subsequence has a.e. state convergence. The quintics are bounded in reflexive L^{6/5} of spacetime, and a.e. convergence identifies their weak limit as y⁵. The weak L⁴L¹² and weak-* energy limits match the strong H limit, retain zero initial data, and solve the weak equation for the weak control limit. Source Shatah–Struwe/mild uniqueness identifies this limit as its state. Endpoint displacement and H⁻¹ velocity costs are continuous along the chosen subsequence; the state and L¹ control norms are weakly lower semicontinuous (the latter is a continuous convex functional on L²). An optimizer follows. This proof uses constant bounded radius for the L∞ forcing bound, as actually specified.

Fix a=ρ/2 and h=πε/(2a), so ε<a/π ensures h<1/2. The comparison v_ε=a e1_{|s|<h} satisfies A=πε and q=2a sin(π²ε/(2a))/π²=ε−π⁴ε³/(24a²)+O(ε⁵); its linear terminal velocity is zero. Since A−πq=π(ε−q),

A−πq+q²/2−εq=−ε²/2+π(ε−q)+(q−ε)²/2
=−ε²/2+π⁵ε³/(24a²)+O(ε⁵).

The actual state quartic contributes O(ε⁴), nonlinear signed tracking error O(ε⁵), velocity cost O(ε¹⁰). Constants may depend on fixed ρ,a,ν but not ε. Thus J_ε(v_ε)−J_ε(0)≤−ε²/4 for all sufficiently small ε.

For arbitrary feasible u,

J_ε(u)−J_ε(0)≥−∥g_ε∥₂r−C₂A⁵,
g_ε=[(1+ε/π)sin(πt)−1]_+.

For δ=ε/π and s=t−1/2, g≤(δ−2s²)_+. Squaring and exactly integrating the parabola gives the stronger bound

∥g_ε∥₂²≤16δ^{5/2}/(15√2),

which implies the submitted rectangular support bound ∥g_ε∥₂≤2^{1/4}π^{−5/4}ε^{5/4}. The exponent 5/4 is correct; the exact sine integral has leading squared coefficient (16√2/(15π))δ^{5/2}.

If r≤Kε for fixed K, then A≤r and the lower bound is −O_K(ε^{9/4})−O_K(ε⁵)=o(ε²), incompatible with the comparison and global optimality. The quantifier is uniform: for every K>0 there exists ε_K>0 such that every global optimizer has r>Kε when 0<ε<ε_K. It therefore rules out a Lipschitz L² selection through the unique optimizer at ε=0.

A missing locality detail can be supplied independently. For any global optimizer u_ε,

0≥J_ε(u_ε)−J_ε(0)=J(u_ε)−J(0)−ε⟨e,y_{u_ε}(1)⟩
≥A³/(12ρ²)−C_yεA.

The comparison ensures A>0, so A≤(12C_yρ²ε)^{1/2}. Since r²≤ρA, every optimizer satisfies r=O(ε^{1/4})→0, uniformly. Returning to the g bound now makes C₂A⁵=O(ε^{5/2}) negligible compared with the comparison gain. Consequently there is c>0 such that every optimizer satisfies r≥cε^{3/4} for sufficiently small ε. In particular r/ε≥cε^{−1/4}→∞.

An additional verified weaker-norm result sharpens the scope. Put x=⟨e,y(1)⟩. Since x≤A/π+C_R'A⁵=:b, choose an A threshold with b<π. The exact terminal-plus-sparse gap is at least A−πx+x²/2. This function decreases for x≤b<π, so it is at least A−πb+b²/2≥A²/(2π²)−πC_R'A⁵≥A²/(4π²) for all sufficiently small A. Thus the example has local L¹-squared quadratic growth. After the previous cube estimate ensures A→0 for optimizers, optimality and ∥y(1)∥≤C_yA improve the upper bound to A=O(ε), hence r=O(√ε). Combining g_ε's height bound ε/π with the negative comparison gives A≥c₁ε as well; therefore A=Θ(ε) uniformly over global optimizers. The valid uniform L² sandwich is c₂ε^{3/4}≤r≤C₂√ε. In particular every global optimizer on this one-sided target ray satisfies the L¹ bound relative to the fixed zero base optimizer, ∥u_ε−0∥_{L¹H}≤Cε, while the corresponding L² bound fails. This does not prove a pairwise Lipschitz selection map between arbitrary perturbed targets. The claimed obstruction must retain its specified norm.

Here are explicit locality thresholds for that strengthening. Inflate D=C_R'>0 if necessary, and put

A_* = min(a₀,ρ,π²/4,(π/(4D))^{1/5},(1/(4π³D))^{1/3})>0.

For 0≤A≤A_* we have b=A/π+DA⁵≤π/2 and πDA³≤1/(4π²), so the scalar monotonicity and absorption used above are uniform. No additional restriction is imposed on the frozen ρ beyond its existing global-uniqueness choice; this is a local statement in A. For perturbed optimizers choose ε≤A_*²/(12C_yρ²), and the global cube bound places all of them inside this neighborhood. The resulting explicit upper bound is A≤4π²C_yε and r≤(4π²C_yρ ε)^{1/2}. If ε is reduced until C₂(4π²C_y)^5ε⁵≤ε²/8, the height estimate for g_ε yields A≥πε/8, and its L² estimate gives r≥ε^{3/4}/(8G) when ∥g_ε∥₂≤Gε^{5/4}. These are fixed-basepoint estimates along y_d^ε=(π+ε)e, uniform over all global minimizers, with constants fixed by source bounds, ρ, and ν. They are independent audit strengthening, not mandatory corrections to the frozen L² claim.

This establishes failure in an actual L²-local optimizer correspondence. It does not prove L∞ convergence of perturbed global optimizers or exclude a statement conditional on perturbed optimizers staying in an L∞ neighborhood. The growth counterexample itself does converge in L∞ and needs no such extra condition.

## 7. Literal source interpretation

The OWR report at printed 439–440 has the ν terminal velocity term and displays an L² neighborhood. The inspected full preprints have ν=0 and Theorem 4.17 uses an L∞ neighborhood; the example covers both. The source condition tests all nonzero elements of the ordinary critical cone, with no nonvacuity clause. Source §4.2.3 identifies β₂=0 as open immediately after explaining β₂>0 coercivity.

Therefore the verified construction gives a negative answer to extending the same ordinary-cone strict positivity implication and same L²-squared growth conclusion by dropping β₂>0. It does not contradict the theorem with β₂>0. The source's broader phrase about the β₂=0 case does not specify that all possible structural conditions, norms, growth exponents, or adapted stability estimates must fail; those broader problems remain outside the result. No independent novelty/priority conclusion is part of this audit.
