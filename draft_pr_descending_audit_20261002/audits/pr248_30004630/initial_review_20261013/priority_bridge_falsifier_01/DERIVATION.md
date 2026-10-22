# Independent derivation and falsification of the PR248 routine bridge

This is a current audit derivation, not a claim that the example was printed in earlier literature. Inputs are the frozen original counterexample, the exact source theorem, and the new B1–B8 bridge. No claim that the nonlinear state stays in a single mode is made.

## 1. Precise mathematical target

Let H=L²(B), with B the unit ball in R³, T=1 and zero initial energy data. The state solves the defocusing Dirichlet equation y_tt−Δy+y⁵=u. Take β₁=γ=1, β₂=0, target πe, and pointwise Hilbert cap ||u(t)||H≤ρ for any fixed finite ρ>0. The normalized radial mode e=sin(π|x|)/(√(2π)|x|) has eigenvalue π². The objective includes terminal position tracking, ||u||L¹H, the quartic L⁴L¹² state norm and, optionally, ν/2 times terminal velocity squared in H⁻¹ for any fixed finite ν≥0.

The core implication is strict positivity of the source's substitute second variation on every nonzero ordinary critical direction ⇒ positive L²-distance-squared growth in the displayed local neighborhood. A genuine local optimizer is enough to refute this implication. Global uniqueness, existence of perturbed global optimizers and target instability are stronger auxiliary conclusions and are not required for a covering counterexample.

## 2. The source statement is adequate; its printed IFT codomain step needs repair

Kunisch–Meinlschmidt arXiv:1907.02744v1, Theorem 4.3, printed19–21, states Fréchet C² differentiability S:L¹(0,1;H)→Y₊, where Y₊ has continuous energy state and L⁴L¹² position. Its first derivative at zero is the zero-data linear forcing map L. Its second derivative has forcing −20 ȳ³ z₁z₂ and hence S″(0)=0.

The theorem's printed proof takes a residual e:Y₊×L¹H→C([0,1];H₀¹×H) and claims D_y e is onto the entire stated codomain. At zero, D_y e(z)=−ξ_z. For a nonzero g∈H, the continuous-energy pair F(t)=(0,tg) has F(0)=0 but cannot equal −(z,z_t): its first component forces z≡0 and its second forces z_t=−tg. Thus the printed surjectivity statement, with that codomain, fails even at the point used here. The proof also cannot assume an arbitrary continuous energy pair has L⁴L¹² regularity. I do not certify this step unchanged.

The needed local statement has a routine complete repair using the source's own Lemma2.9. Let E₀ be the compatible zero-data state space: z∈C(H₀¹), z_t∈C(H), z∈L⁴L¹², with z_t the distribution derivative and both initial traces zero. With the sum norm this is Banach: all components converge in their Banach spaces, derivative compatibility passes in distributions, and the initial traces are closed conditions. Lemma2.9 gives a bounded map L:L¹H→E₀. Sobolev/interpolation gives E₀→L⁵L¹⁰. The five-linear product map is bounded from E₀⁵ to L¹H by Hölder, so P(z)=z⁵ is a continuous homogeneous polynomial and is Fréchet smooth.

Use the residual

    Φ(z,u)=z+L(P(z))−L(u) : E₀×L¹H → E₀.

It is smooth, Φ(0,0)=0 and D_zΦ(0,0)=Id. The Banach implicit-function theorem gives a unique smooth local solution map. It agrees with the unique mild state of the source. Differentiating at zero gives S′(0)=L and S″(0)=0 because P′(0)=P″(0)=0. This proves the source's local C² conclusion directly from its established linear estimate; no new global optimality or bathtub result is assumed. In particular,

    S(u)=L(u)+R(u),  ||R(u)||E₀=o(A²),  A=||u||L¹H→0,
    ||S(u)||E₀=O(A).

The little-o is uniform over directions because it is a Fréchet remainder. One may set d(A) equal to a trace constant times sup_{0<||u||₁≤A} ||R(u)||E₀/||u||₁²; it tends to zero. Both terminal position in H and velocity in H⁻¹ are continuous traces. This repairs the statement needed for B1 rather than importing the candidate's stronger O(A⁵) argument.

## 3. A strict local optimum for arbitrary positive cap

Project only the linear solution on e. Its endpoint obeys

    <e,L(u)(1)>=(1/π)∫₀¹ sin(πt)<e,u(t)>dt ≤A/π.

Let x=<e,S(u)(1)> and b(A)=A/π+d(A)A². Then x≤b(A), even when x is negative. Projection of the full terminal square, together with nonnegative state and velocity terms, gives

    J(u)−J(0)≥q_A(x),   q_A(x)=A−πx+x²/2.

For small A, b(A)<π and q_A decreases throughout (−∞,b(A)], since q_A′(x)=x−π. Hence

    J(u)−J(0)≥q_A(b(A))
      =A²/(2π²)−πd(A)A²+d(A)A³/π+d(A)²A⁴/2
      ≥A²/(4π²)

once πd(A)≤1/(4π²). Both positive terms may be discarded. This is a uniform lower bound for all sufficiently small nonzero controls; it is not a separate lower bound obtained by incorrectly substituting an upper bound into x².

This establishes a genuine strict L¹-local minimum, hence a strict L²- and L∞-local minimum because T=1 implies ||u||₁≤||u||₂≤||u||∞. The positive cap can be arbitrary. A small cap is needed for the original stronger *global* theorem, but is irrelevant to this local bridge. A=0 means u=0 as an equivalence class. The conclusion is uniform in the nonnegative velocity coefficient for local optimality, because that cost was discarded.

## 4. Full tangent, first order conditions and zero ordinary critical cone

At zero the source first directional derivative is

    D J(0;v)=∫(||v(t)||H−sin(πt)<e,v(t)>)dt
      ≥∫(1−sin(πt))||v(t)||H dt.

The coefficient is strictly positive except at the single null time t=1/2. Thus the last integral is positive for every nonzero L¹ or L² equivalence class. No pointwise value at t=1/2 defines a nonzero element of either control space.

For r=1 or2 and v∈LʳH, take bounded truncations v_m=v min(1,m/||v||H). Then v_m→v in Lʳ, and a positive scale α_m≤ρ/m makes α_m v_m admissible. Consequently the closed tangent cone at zero is all LʳH. In L∞H, zero is an interior point and the tangent is also full. Pointwise slack alone does not establish interiority in L¹ or L², and the truncation argument is essential.

The adjoint is p(t)=−sin(πt)e; λ(t)=sin(πt)e is a valid L¹H subgradient at zero because ||λ(t)||H≤1. Take constraint multiplier μ=0. Thus stationarity and all complementarity requirements hold. The source ordinary critical cone is exactly {0} in either its β₂=0 L¹ convention or L². The sparse j″ substitute is explicitly zero at u=0 in the source. The strict second-order condition on nonzero cone directions is therefore satisfied vacuously. This is not a classical twice differentiability claim about the sparse norm.

## 5. Pulses and all nonlinear/velocity remainders

Let u_h=h e 1_{|t−1/2|<h}, with 0<h<min(ρ,1/2). Then

    A_h=2h²,   r_h²=||u_h||₂²=2h³,   ||u_h||∞=h,
    L(u_h)(1)=[2h sin(πh)/π²]e,
    ∂_t L(u_h)(1)=0.

Linear tracking plus sparsity equals

    2h²−2h sin(πh)/π+2h² sin²(πh)/π⁴
      =(π²/3+2/π²)h⁴+O(h⁶).

The Fréchet state remainder is o(A_h²)=o(h⁴), so its terminal *linear* tracking contribution is o(h⁴). The terminal squared-state cross term is O(A_h)o(A_h²)=o(h⁶), and its own square is smaller. The quartic state penalty is O(A_h⁴)=O(h⁸). Because the linear endpoint velocity is exactly zero, the optional velocity penalty is ν o(A_h⁴)=o(h⁸) for each fixed finite ν. Thus

    J(u_h)−J(0)=(π²/3+2/π²)h⁴+o(h⁴),
    [J(u_h)−J(0)]/r_h²→0.

The lower bound in §3 is consistent: it has order A_h²=4h⁴, not order r_h²=2h³. The pulses are admissible and converge in L∞, so this direct calculation defeats either source localization. It does not require numerical PDE constants, a numerical PDE solution, or a global optimizer assertion. The little-o statement is not claimed uniform over unbounded ν.

## 6. Exact BW2024 assumptions and the localization repair

I independently downloaded the final publisher PDF of Borchard–Wachsmuth, JNSAO5(2024),12604, DOI10.46298/jnsao-2024-12604, and read Assumption2.1, the growth condition2.4, NDC and the complete proof of Theorem2.18. Formula pages3,12,13 were visually checked.

Set X=L²(0,1;H), Y=X with canonical Hilbert duality. Both are separable and the weak-star topology on X is its weak topology. Put G(u)=||u||L¹H+I_Uad(u), with F the smooth tracking/state/velocity part. G is proper and convex; ||·||L¹H is continuous in L² and Uad is closed convex in L², so G is lower semicontinuous. These facts suffice, and Theorem2.18 does not require strong epi-differentiability or the Legendre property.

F′(0) has the representing L² vector −sin(πt)e. The bounded bilinear second derivative is

    F″(0)[v,w]=<L(v)(1),L(w)(1)>H
       +ν<∂_tL(v)(1),∂_tL(w)(1)>H⁻¹.

The quartic state term has zero second derivative at zero, and S″(0)=0. Fréchet Taylor in L¹ gives a second-order Taylor expansion in L²: A≤r, so an error bounded by ω(A)A² is at most sup_{a≤r}ω(a) r²=o(r²). Hence BW's sequential expansion2.1 holds for every weakly convergent bounded direction sequence and positive scale tending to zero. All standing assumptions are checked.

Let v_h=u_h/r_h. It has norm1. For every test w∈L²H,

    |<v_h,w>|≤||w 1_{|t−1/2|<h}||₂→0.

So v_h is weakly null. Choose h_k decreasing geometrically to ensure BW's scale t_k=r_{h_k} is decreasing. The exact NDC expression is

    [G(u_h)−G(0)+F′(0)u_h]/r_h²+F″(0)[v_h,v_h]/2
      =1/h−sin(πh)/(πh²)+sin²(πh)/(π⁴h)
      =(π²/6+1/π²)h+O(h³)→0.

Thus NDC fails, and BW2.18 excludes positive L²-norm-squared growth in an L² ball.

One must **not** apply the printed theorem's L²-ball contraposition directly to a claim only made in an L∞ ball. To complete that case, suppose source growth held for all admissible controls with ||u||∞<ε. Pick 0<η<min(ρ,ε) and replace G by

    G_η(u)=||u||L¹H+I_{||u(t)||H≤η a.e.}(u).

This cap set is closed convex in L² (an L² convergent subsequence converges pointwise a.e.) and preserves every standing assumption. Every control in its domain lies strictly inside the hypothesized L∞ neighborhood. Hypothesized source growth therefore implies BW's L²-ball growth2.4 for F+G_η. For h<η, the same pulses are in its domain and violate NDC by the same identity, contradiction. This is the precise routine localization repair. Independently, §5 already refutes L∞ growth without invoking BW.

## 7. Historical and novelty boundary

KM's source theorem and linear-wave estimate predate the PR; the final BW paper was published18December2024, also before the PR's2026 creation. The publisher record and independent arXiv history confirm this chronology; no regenerated PDF title-page date is used. The final BW result is applicable to the actual quintic-wave reduced objective, even though its application section focuses on parabolic problems.

These older inputs plus §§3–6 yield a complete, elementary *current* local counterexample bridge, after explicitly repairing the source proof's residual codomain and BW's localization. There is no remaining unsupported mathematical construction/optimality gap for the core implication. Neither global optimality nor target instability is needed to close it.

However, the cited older primary texts have not thereby been shown to contain the exact nonlinear-wave counterexample or to state its negative resolution. Producing correct algebra today from older ingredients is not evidence that the algebra or its source-specific application was published earlier. A historical claim of already-published resolution would still need an earlier complete statement/proof or an explicit prior application/corollary.

BW2.18 supplies a conditional NDC criterion; it does not supply the target, local-minimum construction, zero critical cone or pulse witness. Sections3–5 give the entire current negative construction before that criterion is invoked in §6. KM4.3 supplies state differentiability but does not itself construct a counterexample. My independent opinion that the current construction steps are elementary/routine must not be confused with an earlier covering result. The parent's criterion accepts routine specialization of a prior covering result, not arbitrary new proofs from old ingredients. This subaudit supplies mathematical validity of the current bridge, and leaves the historical covering-result gap open for the root's adjudication.

The source-specific original global uniqueness and target-instability assertions remain stronger possible contributions, with their own priority questions. They cannot be required to recognize prior coverage of the narrow local core, nor used to redefine the original core question after this audit.
