# Complete elementary proofs and negative controls

These are independent derivations for statement matching and failure detection. They do not reprove the recent prior-paper threshold theorem and carry no novelty claim.

## 1. Unit sphere, unit ball, and quantifiers

Fix ε,T,L,M, and denote by m(y₀) the infimum of norms of all controls driving y₀ to zero. Linearity gives a bijection v↦rv between controls for y₀ and ry₀ whenever r>0. The inverse is division by r. Therefore m(ry₀)=r m(y₀), and m(0)=0 since the zero control works. Every nonzero datum in the unit ball is r times a unit-sphere datum with 0<r≤1, so the supremum on the ball is at most the supremum on the sphere. The reverse inequality is set inclusion. The two costs are equal.

For a nonnegative scalar function Cε, limsup as ε→0+ is finite if and only if some finite K bounds Cε for every sufficiently small positive ε. Indeed, a finite limsup permits any larger K eventually; conversely an eventual bound bounds the limsup. Together with homogeneity this proves the quantifier formulation in the README. Using an infimum of control norms rather than an attained minimum gives the same threshold: an arbitrarily small increase of K absorbs the approximation error.

## 2. Scaling, including the control normalization

Put a=|M|, η=M/a, s=at/L, ξ=x/L, δ=ε/(aL), and

    Y(s,ξ)=√L y(Lξ,Ls/a),   V(s)=√L v(Ls/a).

Chain differentiation gives Y_s−δY_ξξ+ηY_ξ=0. The controlled and homogeneous boundaries remain ξ=0 and ξ=1, and the final time becomes S=aT/L. The substitution is invertible. Moreover,

    ∫₀¹ |Y(0,ξ)|²dξ = ∫₀ᴸ |y₀(x)|²dx,
    ∫₀ˢ |V(s)|²ds = a ∫₀ᵀ |v(t)|²dt.

Thus the bijection preserves the initial unit ball and multiplies control norms by √a. Taking first the infimum over controls and then the supremum over initial data proves

    Cε(T,L,M)=a⁻¹ᐟ² Cδ(aT/L,1,η).

As ε→0+ if and only if δ→0+, finite-limsup times correspond under multiplication by a/L. Taking infima proves

    T_unif(L,M)=(L/a)T_unif(1,η).

Consequently a universal proposed formula independent of L cannot be correct for arbitrary interval lengths.

## 3. An infimum is not necessarily an attained minimum

For T₂>T₁, extend a null control on [0,T₁] by zero on [T₁,T₂]. Its state is identically zero after T₁ by uniqueness, and its control norm is unchanged. Hence Cε(T₂)≤Cε(T₁). The set of uniform-control times is upward closed. If nonempty and with finite positive infimum τ, this implies that it is either [τ,∞) or (τ,∞): for any T>τ, the defining property of an infimum provides a member s<T, and upward closure gives T as a member. It says nothing about τ itself.

For an explicit logical negative control, set

    Aε(T)=exp((τ−T)/ε),
    Bε(T)=ε⁻¹ exp((τ−T)/ε).

Both are positive and continuous decreasing functions of T. For each T>τ both tend to zero as ε→0; for T<τ both diverge. Their uniform-time infima are τ, but Aε(τ)=1 is bounded whereas Bε(τ)=ε⁻¹ diverges. These are abstract cost countermodels, not claims that either is the PDE cost. They prove that the endpoint assertion requires additional analysis.

## 4. Exact one-eigenmode observability calculation

Normalize L=|M|=1 and write η=±1. The forward-time adjoint equation is

    z_t=εz_xx+ηz_x,   z(t,0)=z(t,1)=0.

For n≥1 define k=nπ,

    λ=1/(4ε)+εk²,   φ(x)=exp(−ηx/(2ε))sin(kx),
    z(t,x)=exp(−λt)φ(x).

Direct differentiation, using sin(k·0)=sin(k·1)=0, shows εφ″+ηφ′=−λφ. This is therefore a smooth admissible adjoint solution. Its observed boundary flux is εz_x(t,0)=εk exp(−λt), so

    D:=∫₀ᵀ |εz_x(t,0)|²dt
      =ε²k²(1−exp(−2λT))/(2λ).

To relate this to control cost, let p(t,x)=z(T−t,x). Integration by parts for a forward controlled state y gives

    d/dt ∫₀¹ y(t,x)p(t,x)dx = ε v(t)p_x(t,0).

The terms involving the drift vanish at the boundary since p is zero there. For a null control, integration in time gives

    ⟨y₀,z(T)⟩ = −∫₀ᵀ v(t) εz_x(T−t,0)dt.

The identity also holds for the transposition solution, since this smooth p is an admissible test function in its definition. Cauchy–Schwarz and the unit datum y₀=z(T)/‖z(T)‖₂ show that every null control for this datum has norm at least ‖z(T)‖₂/√D. Thus

    Cε(T,1,η)² ≥ Rη,n(ε,T)² := ‖z(T)‖₂²/D.

We now calculate this ratio exactly. The elementary antiderivative of e^(−ax)cos(bx), evaluated at 0 and 1 with a=1/ε and b=2nπ, together with sin²(kx)=(1−cos(2kx))/2, gives

    I+ :=∫₀¹ e^(−x/ε)sin²(kx)dx
        =(1−e^(−1/ε))·2k²ε³/(1+4k²ε²).

Reflection x↦1−x preserves sin²(nπx), so

    I− :=∫₀¹ e^(x/ε)sin²(kx)dx = e^(1/ε) I+.

The cancellation

    [2k²ε³/(1+4k²ε²)]·2λ/(ε²k²)=1

is exact. Consequently

    R+,n² = (1−e^(−1/ε))/(e^(2λT)−1),
    R−,n² = (e^(1/ε)−1)/(e^(2λT)−1).

For fixed ε,T, each numerator is independent of n, while λ increases with n. The largest single-eigenmode ratio over all integers n≥1 is therefore attained at n=1, even if the selected n is allowed to depend on ε.

For every fixed T>0, R+,1→0 because its numerator is at most 1 and its denominator diverges. Thus no individual eigenmode gives a positive-speed lower-threshold obstruction, even though the cited full theorem gives a nonzero threshold. This is a limitation of this family of tests, not an upper bound on the actual cost.

For negative speed, divide numerator and denominator by their leading exponentials:

    R−,1² = exp((1−T/2)/ε−2επ²T)
             ·(1−exp(−1/ε))/(1−exp(−T/(2ε)−2επ²T)).

The final fraction tends to 1. Therefore R−,1→∞ for 0<T<2, tends to 1 for T=2, and tends to zero for T>2. It proves an elementary negative-speed obstruction below 2, but cannot detect the larger threshold 2+2√2. In particular, replacing the complete observability problem by its first eigenmode would lose the needed obstruction.

## 5. Pointwise smallness does not establish an operator-norm limit

On ℓ² let P_n(x)=x_n e_n. For each fixed x∈ℓ², x_n→0 and hence ‖P_nx‖→0. Nevertheless ‖P_n‖=1 for every n, attained at e_n. Thus pointwise convergence of a family of operators does not imply convergence of their norms. This example only refutes that inference; it does not assert that P_n is a PDE control map.
