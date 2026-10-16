# Finite-species local theory, nonneutral localization, and bounded-momentum continuation

Prepared 2026-10-07 UTC. This is a proof artifact for an established continuation result, not a proof of global bounded momentum. It uses the Bouchut–Golse–Pallard division lemma and its derivative computation; the precise imported identities are identified below. Adaptation of the finite-horizon localization from family 362 is attributed to its continuation.tex; all signs and hypotheses were rechecked here.

## Statement and conventions

Let N<∞, m_a>0, e_a∈R, κ_a=e_a/m_a, q(p)=sqrt(1+|p|²), and u=p/q. Consider

    ∂tF_a+u·∇xF_a+κ_a(E+u×B)·∇pF_a=0,
    ∂tE−curl B=−j, ∂tB+curl E=0,
    ρ=Σ_a e_a∫F_a dp, j=Σ_a e_a∫uF_a dp.

The data are 0≤F_a0∈C_c∞(R⁶), and E0,B0∈C_b∞(R³)∩L²(R³), with divE0=ρ0 and divB0=0. Here C_b∞ means all spatial derivatives bounded. No neutrality condition is imposed. A classical solution is C¹ pointwise, with fields continuous into L² and with all particle phase supports contained in one compact set on every compact time subinterval.

Then there is a unique maximal classical solution. It is smooth on every compact subinterval. If T_max<∞ and the normalized momentum supports of every species are uniformly bounded for 0≤t<T_max, it extends as a classical, then smooth, solution beyond T_max. All species, including neutral ones, are included in the maximum. Constants can depend on N and the fixed m_a,e_a, hence on κ_a; uniformity as m_a→0 is not asserted.

## 1. Characteristics, compact support, and constraints

For C¹ fields on a closed finite slab [0,S], the ODE X'_a=u(P_a), P'_a=κ_a(E+u(P_a)×B)(t,X_a) has a unique solution through each phase point for the whole slab. The bound |X'_a|≤1 confines X_a to a compact spatial ball. Fields are bounded on that compact spacetime cylinder, so |P'_a| is bounded, excluding escape of momentum. This argument also runs backward to time 0. The transported data therefore have spatial support |x|≤R0+t, where R0 encloses all initial spatial supports, and compact momentum support on that slab. Compactness of the initial label sets and continuity of the flow make the bounds common to all labels and all finitely many species. This does not bound support at an excluded maximal endpoint.

Since u is a momentum gradient, div_p(u×B)=0. The phase divergence is zero; the flow preserves particle number, positivity and L∞ norms. Integrating transport gives ∂tρ+divj=0, including each charge sign. Consequently divE−ρ and divB are time constant and vanish if they do so initially.

## 2. Maxwell group and local finite propagation

For C_ξ w=ξ×w, the Fourier generator on (E,B) is

    A(ξ)=[[0,iC_ξ],[-iC_ξ,0]], A(ξ)*=−A(ξ).

Thus U(t), multiplier exp(tA(ξ)), is a strongly continuous unitary group on L² and every H^k, without imposing divergence constraints. For current in C_tH^k,

    F(t)=U(t)F0+∫_0^t U(t−s)(−j(s),0)ds,
    ||F(t)||H^k≤||F0||H^k+∫_0^t ||j(s)||H^k ds.

A C¹ Maxwell field W=(W_E,W_B) has local energy w=(|W_E|²+|W_B|²)/2 satisfying

    ∂tw+div(W_E×W_B)=−W_E·j_W,
    |W_E×W_B|≤w.

Integrate in the shrinking balls B(x,r+t−s), 0≤s≤t. If initial data and current vanish in the backward cone, the derivative of this local energy is the negative boundary integral of w+(W_E×W_B)·ν, which is nonpositive. Initial energy zero forces W(t)=0 in B(x,r). This proves finite propagation for C¹ fields locally and uses neither global L² nor divergence constraints.

## 3. Coulomb field and the positive curl-potential identity

Since ρ0 is a signed smooth compactly supported function, put

    E_C=−∇(−Δ)^−1ρ0.

Its Fourier transform is −iξ|ξ|^−2 ρhat0(ξ), so divE_C=ρ0 and curlE_C=0. Near ξ=0, its magnitude is O(|ξ|^−1); its square is integrable in dimension 3. At infinity ρhat0 decays faster than any polynomial. Thus E_C∈H^k for every integer k≥0, with bounded smooth derivatives by embedding. This is true for nonzero ∫ρ0. The tail of E_C need not be compactly supported.

For any smooth divergence-free G define

    V_G(x)=∫_0^1 tG(tx)dt,
    A_G(x)=V_G(x)×x.

This is the positive-sign formula. We have divV_G=0, and the curl identity is

    curl(V_G×x)=2V_G+(x·∇)V_G
               =∫_0^1 d/dt[t²G(tx)]dt=G(x).

In particular it is V_G×x, not x×V_G. The latter has curl −G. The formula is smooth at x=0, and no decay of A_G is needed because it will be cut off.

## 4. Vacuum evolution for bounded smooth finite-energy data

If D_E,D_B∈C_b∞∩L² are divergence free, let M_tg(x)=(4π)^−1∫_(S²)g(x+tω)dω and define

    E^v(t)=∂t[tM_tD_E]+tM_t(curl D_B),
    B^v(t)=∂t[tM_tD_B]−tM_t(curl D_E).

Kirchhoff's formula makes both smooth free-wave solutions; each derivative is bounded on finite slabs because the required initial derivatives are bounded. Their Maxwell residuals R_E=E^v_t−curlB^v and R_B=B^v_t+curlE^v are free-wave solutions. Both their initial values are zero. Their initial time derivatives are ∇divD_E and ∇divD_B, respectively, hence zero. Local uniqueness for the wave equation implies R_E=R_B=0. The divergences vanish for the same reason. If D_E,D_B vanish in B(0,L), the displayed formulas give E^v=B^v=0 for |x|+t<L.

To justify C_tL² without any L² derivative hypothesis, mollify the initial data with compactly supported nonnegative approximate identities. They remain divergence free, belong to every H^k, and converge in L². Each fixed spatial derivative also converges uniformly, since the next bounded derivative gives uniform continuity. The corresponding Kirchhoff solutions converge locally with every fixed derivative to the displayed solution. They also equal U(t) of the mollified data, which converge uniformly in t in L² by unitarity. The limits agree, proving F^v(t)=U(t)(D_E,D_B), C_tL² continuity and preservation of its L² norm.

## 5. A broad-data homogeneous comparison and uniqueness

For the original initial fields define

    F^h(t)=(E_C,0)+U(t)(E0−E_C,B0).

The second pair is divergence free and is the vacuum solution of Section 4. The first pair is a static solution of the homogeneous first-order Maxwell equations because curlE_C=0. Therefore F^h solves Maxwell with zero current, agrees with F0 initially, is C_tL², and has bounded spatial derivatives of every order on finite slabs. Its electric divergence is ρ0. One must not claim it is componentwise a free wave with nonzero divergence.

For any C¹ solution on [0,S], characteristics confine current to |x|≤R0+t. W=F−F^h has zero initial data. The local propagation argument gives W(t,x)=0 for |x|>R0+t: a sufficiently small ball around such x has a backward cone avoiding the current support. Thus W has fixed compact spatial support on this slab. Its C¹ regularity on the compact cylinder implies W∈C_tL² and uniform global first-derivative bounds. Hence every such solution automatically has F∈C_tL² and globally bounded first field derivatives on the closed slab.

For two classical solutions with the same data, let g_a=F_a1−F_a2, δF=(δE,δB), and choose R enclosing their momentum supports on the closed common slab. Transport by the first force gives

    (∂t+u·∇x+κ_aK1·∇p)g_a
      =−κ_a(δE+u×δB)·∇pF_a2.

The transport has zero divergence. Since ∇pF_a2 is bounded and vanishes outside |p|≤R,

    d/dt Σ_a||g_a||²L² ≤ C[Σ_a||g_a||²L²+||δF||²L²],
    ||δj||L²x ≤ |B_R|^(1/2)Σ_a |e_a| ||g_a||L²xp.

Maxwell energy gives the same bound for ||δF||². Cutoffs χ(x/L) justify its integration, with boundary error at most C/L ∫_0^S||δF(s)||²ds, tending to zero. Gronwall gives identical solutions. There is no positivity assumption on δρ or δj. The shared field is compared once, while the distribution differences are summed over all species.

## 6. Local smooth Sobolev construction and tame persistence

First assume F0∈⋂H^k. On supports |p|≤R and for k≥6 put

    Yk=||F||H^k(R³)+Σ_a||F_a||H^k(R⁶).

The integer Gagliardo–Nirenberg inequality gives the tame product bound for integer total order s,

    ||D^αg D^βh||2≤C[||g||∞||h||H^s+||h||∞||g||H^s], |α|+|β|≤s.

For each species set a_aR=κ_a ζ_R(p)(E+u×B), with ζ_R=1 near the support. It is used only in commutators. Then

    ||a_aR||H^k(R⁶)≤C_(k,R)|κ_a|||F||H^k(R³),
    ||∇a_aR||∞≤C_R|κ_a|||F||W^(1,∞).

The leading divergence-free transport disappears in the H^k energy. Each nonleading product is a derivative of ∇a_aR times a derivative of ∇F_a, of total order at most k−1. The tame product estimate bounds it by C[||F||W^(1,∞)||F_a||H^k+||F||H^k||∇F_a||∞]. Derivatives of u are bounded and cost only the particle H^k norm. Also

    ||j||H^k_x≤|B_R|^(1/2)Σ_a |e_a| ||F_a||H^k_xp.

Consequently

    Yk(t)≤Yk(0)+C∫_0^t [1+||F(s)||W^(1,∞)+Σ_a||∇F_a(s)||∞]Yk(s)ds.   (T)

These estimates can be obtained for unsquared norms by regularizing a vanishing norm before dividing, then removing regularization.

Iterate linear transport for F_a^(n+1) with F^n, and linear first-order Maxwell for F^(n+1) with j(F_a^n), all starting from the same data. Initial iterates are time independent. H^6(R⁶) controls first particle derivatives, while H^6(R³) controls first field derivatives. The same commutator calculation gives

    Y6^(n+1)(t)≤Y6(0)+C_R∫_0^t [(1+Y6^n)Y6^(n+1)+Y6^n]ds.

Choose M>2(Y6(0)+1), and choose τ sufficiently small in terms of M,R_initial,N,e,κ. Induction gives Y6^n≤M; shrinking τ makes the momentum increase at most 1 because |P'_a|≤C|κ_a|M. This closes the fixed support radius R=R_initial+1. The L² difference energy obeys D_(n+1)(t)≤C_(R,M)∫_0^tD_n(s)ds, where D_n is the field difference plus the sum of all particle differences. Taking Cτ<1/2 gives convergence in C_tL². Higher estimates of the form Yk^(n+1)≤Yk(0)+C∫(Yk^(n+1)+Yk^n) give common bounds Yk(0)exp(2Ct). Interpolation gives convergence in every C_tH^k. The smooth limit solves the equations, transports positivity, has compact phase support, and propagates the constraints by Section 1. Intermediate Maxwell iterates need not satisfy the charge constraint; the limit does. The lifespan τ depends on Y6(0) and the support radius, not on higher norms.

On a closed classical interval with Sobolev initial fields, Section 5 gives global W^(1,∞) field bounds, and compact phase support plus C¹ gives bounds on ∇F_a. Thus the coefficient in (T) is bounded. Before any proposed first loss of smoothness, (T) uniformly bounds Y6 and the support radius. Restarting the local construction at times tending to that loss gives one common positive lifespan. Classical uniqueness identifies the restarted solution with the given solution, contradicting the first loss. Higher estimates preserve all H^k and the equations give all time derivatives. This argument does not assume an H^6 endpoint limit in advance.

## 7. Finite-horizon nonneutral localization

Fix H>0 and L=R0+2H+1. Choose χ∈C_c∞ equal to 1 on B(0,L). The fields G_E=E0−E_C and G_B=B0 are divergence free. Set

    Ebar0=E_C+curl(χ A_(G_E)),
    Bbar0=curl(χ A_(G_B)).

They belong to every H^k: the curl terms are smooth and compactly supported, and E_C∈⋂H^k. They satisfy divEbar0=ρ0 and divBbar0=0. They agree with the original fields on B(0,L), including their derivatives there. Their differences D0=(E0−Ebar0,B0−Bbar0) are divergence free, in C_b∞∩L², and vanish on B(0,L). Let D(t) be their vacuum evolution. For 0≤t≤H and |x|≤R0+t,

    |x|+t≤R0+2H<L, hence D(t,x)=0.                         (V)

For every classical solution with either data, all species have spatial supports in that particle region. Subtracting or adding D therefore preserves the transport equation for each κ_a: the force difference is zero wherever ∇pF_a can be nonzero, and outside this spatial region ∇pF_a=0. Maxwell equations, source sums, and both constraints are preserved because D is a divergence-free vacuum solution. The operation preserves C_tL², smoothness, and particle supports. Thus

    (F_a,F) ↔ (F_a,F−D)

is a bijection of solutions with original and modified data on every existence interval contained in [0,H]. This is a fixed-horizon exact equivalence, not an approximation.

The local Sobolev construction for modified data, followed by adding D, proves local smooth existence for the original class. Uniqueness patches these into a unique maximal classical solution. For any closed classical interval, choosing H larger than its end, subtracting D, and using the Sobolev persistence proof proves smoothness for the original class as well.

## 8. Momentum-only continuation: exact imported mechanism and finite-species adaptation

The primary continuation theorem is Glassey–Strauss in the H^5 formulation of Luk–Strain arXiv:1406.0165, Theorem 1.1 and Footnote 1; Luk–Strain Remark 1.2 explicitly states that their methods extend to multispecies, with details omitted. The finite-species adaptation below concerns only a fixed bounded support radius, not the difficult a priori bound.

For completeness, the mechanism is the wave-kernel division lemma of Bouchut–Golse–Pallard, arXiv:math/0301175, Lemma 3.1. Let Y be the forward 3D wave kernel and T=∂t+u(p)·∇x. The lemma decomposes each first derivative of Y as T(a_i^0Y)+a_i^1Y, and each second derivative as T²(b_ij^0Y)+T(b_ij^1Y)+b_ij^2Y. Coefficients are smooth in p; their spacetime homogeneous degrees are respectively 0,−1 and 0,−1,−2. The last kernel has zero angular residue on the light cone (Lemma 3.1, equation (3.6)). On |p|≤R all coefficients and needed momentum derivatives are bounded after the appropriate homogeneous factors, because |u|≤R/sqrt(1+R²)<1. This lemma is the imported analytic identity; it is unchanged by e_a or κ_a.

For each species let U_a solve □U_a=F_a with zero wave data. The source moments are linear: scalar potential Σ_a e_a∫U_a, vector potential Σ_a e_a∫uU_a. A free-wave vector potential −Y(t,·)*_xE0 and the vacuum field with data (0,B0) provide the initial terms; their derivatives are bounded on finite slabs. The representation is valid for nonzero charge: the Lorenz residual has wave source ∂tρ+divj=0, zero value initially, and zero time derivative initially because divE0=ρ0. It therefore vanishes. The actual field equals this representation by local Maxwell uniqueness.

The transport substitution in the first division identity is

    T(1_(t≥0)F_a)=δ_(t=0)F_a0−1_(t≥0)div_p[κ_a K F_a].

Thus integrations by parts acquire precisely κ_a; field moments acquire precisely e_a. Negative signs are harmless in the following absolute estimates. Define I_a as the sum of all L∞ norms of first spacetime derivatives of ∫mU_a, m∈{1,u1,u2,u3}, and J_a similarly for second derivatives. Let Z=Σ_a I_a and J=Σ_a J_a. The first-derivative estimates in Bouchut–Golse–Pallard (4.7)–(4.10), applied separately to each source and then summed, give

    Z(t)≤C[1+∫_0^t Z(s)ds],
    ||K(t)||∞≤C[1+Z(t)].

This step uses |κ_a|, |e_a| and preserved ||F_a0||∞, never positivity of a signed sum. Hence K and its momentum derivatives are bounded for fixed T,R.

For second derivatives, apply the same division identity and the computation (5.1)–(5.8) separately to F_a. Each occurrence of the force in those computations is replaced by κ_a K; each Maxwell moment in its derivatives is replaced by the sum with factors e_b. Differentiating κ_a introduces no term because it is constant. Terms with two forces receive κ_a²; terms with a derivative of force receive κ_a e_b and are bounded by C(1+J). No derivative of F_a survives except in the last zero-residue kernel. Split that kernel at θ=min(t,[1+N(t)]^−1), where N(t)=sup_(s≤t)Σ_a||∇_(x,p)F_a(s)||∞. The small part is ≤CθN(t), by subtracting F_a(t−s,x,p) from F_a(t−s,x−sω,p); the remaining part is ≤C log(t/θ)||F_a0||∞. These are the exact two estimates giving (5.8), and the zero-residue identity supplies the subtraction. Consequently for every 0≤t'≤t<T,

    J(t')≤C[1+∫_0^(t') J(s)ds+log(2+N(t))].               (D)

Here C depends on T,R, fixed species parameters and initial norms, but not on t or N(t). Formula (D) is the finite sum of (5.9). Its coefficients include all fixed |e_b|, |κ_a| and |κ_a|²; finiteness of N is needed only to apply it on compact prefixes, not to set C. Applying Gronwall for fixed t gives ||F(t)||W^(1,∞)≤C[1+log(2+N(t))]. Differentiating the transport equation for every species and summing now gives

    N(t)≤N(0)+C∫_0^t [1+log(2+N(s))]N(s)ds.

The integral ∫∞ dy/[y(1+log(2+y))] diverges, so the scalar comparison solution stays finite for finite T. Thus N and the field W^(1,∞) norm are uniformly bounded on [0,T). The tame estimate (T) uniformly bounds Y6 (and every Yk) there. Restarting at times approaching T with the common H^6 lifespan proves unique smooth continuation of the Sobolev solution without imposing momentum bounds on its approximation iterates. Neutral species have κ_a=e_a=0: their field contribution is zero and their own derivative equation is free transport. Including them in N is harmless.

This continuation proof relies on the cited wave-division computation (5.1)–(5.9), rather than on the literal compact-field data clause of the Bouchut–Golse–Pallard theorem. That literal clause would force zero total one-species charge; it is not the data hypothesis used here. The machinery is a prior result, with explicit finite-species factors accounted for. No species-pair signed impulse, angular occupation, or selected-range global estimate is assumed in this argument.

Finally, if an original-data solution has uniformly bounded normalized momentum before finite T, perform Section 7 with H=T+1. Its modified solution has all-Sobolev data and the same radius. The preceding continuation extends it to [0,T+ε); shrink ε<1. Adding D gives an original-data extension because (V) holds throughout its extended particle region. Section 7 and Sobolev persistence make it smooth. This proves the claimed bounded-momentum criterion for C_b∞∩L² fields without neutrality.

## Sources actually read and limits of verification

- Glassey, The Cauchy Problem in Kinetic Theory (1996), Chapter 5 §5.2 printed p.140 and finite-species completion p.159; Chapter 6 §6.1 pp.163–164. The book's Theorem 5.2.1 includes neutrality among preceding constraints. This was visually verified from the PDF, not removed by inference.
- Bouchut–Golse–Pallard, arXiv:math/0301175v1, Lemma 3.1, Sections 4 and 5, especially equations (4.7)–(4.10), (5.1)–(5.12). The proof estimates, including the residue subtraction, were inspected.
- Luk–Strain, arXiv:1406.0165v1, Theorem 1.1, Footnote 1, Remark 1.2. The actual H^5 theorem and multispecies remark were read.
- Pinned family 362 build/sections/continuation.tex, finite-horizon field modification and local Sobolev persistence. The source remains read-only.

No proof of the global a priori momentum bound has been established by this supplement. The separation of local theory/continuation from that bound is essential.
