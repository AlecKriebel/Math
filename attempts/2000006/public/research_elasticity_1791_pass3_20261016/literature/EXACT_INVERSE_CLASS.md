# E-6322 exact inverse class and finite-energy weak closure

16 October 2026. This report keeps the frozen full primal class and all permitted smooth data. Put D=G(Ω), h=G⁻¹|∂D, and let A_g be the original full finite-energy class. Maps and inverses below are equivalence classes modulo null sets. No homeomorphism is assumed.

## Results

1. The inverse-image class has an exact characterization by explicit transport and boundary Piola conditions. In particular, inverse Sobolev regularity does not have to be assumed in that characterization; it follows from those conditions and the dual energy.
2. Primal global minimization transfers exactly to this class.
3. Its energy sublevels are sequentially weakly compact in W^{1,9/5}(D). The dual energy extended by infinity outside this class is sequentially weakly lower semicontinuous, and also lower semicontinuous for strong L¹ convergence. Consequently its sequential relaxation in either topology adds no finite-cost maps.
4. These facts do not show that arbitrary finite-dual-energy maps satisfy the required transport or Piola conditions. They do not justify additive inverse variations without checking those conditions.

These are direct deductions from the previously verified primal baseline and elementary integration by parts. No claim of novelty is made.

## 1. The transformed density

For H∈R^{3×3}, C=cof H and K=det H>0, define

V(H)=a|C|⁶/K⁵+b|H|³/K²+c/K+dK³,

and set V=+∞ when K≤0. Denote J(v)=∫_D V(Dv).

As a function of independent variables (H,C,K), the first two terms are the perspectives K·a|C/K|⁶ and K·b|H/K|³. Together with c/K+dK³ they give a convex extended-valued minor representation, so V is polyconvex. This observation does not by itself prove lower semicontinuity in a space with gradient exponent below two.

Young's inequality, or minimizing the competing powers in K, gives constants depending on the fixed positive coefficients such that

V(H)≥c₀(|H|^{9/5}+|cof H|^{9/4}+K³+K⁻¹).

For example |H|^{9/5}=(|H|³/K²)^{3/5}(K³)^{2/5} and |C|^{9/4}=(|C|⁶/K⁵)^{3/8}(K³)^{5/8}. To obtain the displayed sum at once, split the coefficient d into three positive parts before applying these inequalities. Thus every finite-J map has the indicated minor integrability, in particular cof Dv∈L^{9/4}⊂L¹. A separate range bound controls its zeroth-order norm.

Pass 2 established for each y∈A_g that its a.e. inverse v belongs to W^{1,9/5}(D), has full trace h, satisfies Dv=(Dy)⁻¹∘v a.e., and J(v)=I(y). Let

B_g={v : v is the a.e. inverse of some y∈A_g}.

This definition is exact but depends on the primal class. The next characterization tests a candidate using v itself and the fixed smooth datum G.

## 2. An intrinsic characterization with explicit compatibility conditions

Let C_g consist of maps v with all of the following properties.

**C1. Energy and range.** v∈W^{1,9/5}(D;R³), v(z)∈Ω a.e., K=det Dv>0 a.e., and J(v)<∞.

**C2. Measurable inverse and exact transport.** There are full-measure measurable sets D₀⊂D and Ω₀⊂Ω on which v is a bijection with a measurable inverse y:Ω₀→D₀, and

∫_D f(v(z))K(z) dz=∫_Ω f(x) dx

for every nonnegative measurable f on Ω. Values of the inverse outside Ω₀ are immaterial. This condition is an explicit a.e. bijection and Jacobian change-of-variables hypothesis; it is not inferred from C1.

**C3. Transported Piola identities up to the entire boundary.** For every scalar ψ smooth on a neighborhood of Dbar and every vector field φ smooth on a neighborhood of Ωbar,

∫_D [ψ(z)K(z) div φ(v(z)) + φ(v(z))·(cof Dv(z))Dψ(z)] dz
=∫_{∂Ω} ψ(G(x)) φ(x)·ν_Ω(x) dS(x).                         (P)

All integrals are well-defined by the range bound, smooth test functions and the integrability from C1. The boundary term is prescribed data; no trace of Dv occurs in it. Equivalently it can be written on ∂D using the smooth cofactor of DG⁻¹ and the boundary area formula.

**Proposition. C_g=B_g.** In particular C1–C3 imply Tr v=h, although that trace was not included as a separate condition. Neither inverse continuity nor a prior weak derivative for the measurable inverse y is required.

### Necessity

Let y∈A_g and v=y⁻¹. Pass 2 gives C1. The established a.e. bijection, the primal area formula and positive Jacobian give C2. Write F=Dy and j=det F. Under z=y(x),

K(y(x))=j(x)⁻¹,  cof Dv(y(x))=j(x)⁻¹F(x)ᵀ.

The left side of (P) becomes

∫_Ω [ψ(y(x))div φ(x)+φ(x)·F(x)ᵀDψ(y(x))] dx
=∫_Ω div[ψ(y(x))φ(x)] dx.

The ordinary Sobolev chain rule is legitimate because ψ is smooth near Dbar, y takes values in Dbar and Dy∈L⁶. The divergence theorem and Tr y=G give exactly the right side of (P). This proves C3 for every original competitor, including those with exceptional collapsed fibers.

### Sufficiency and the actual weak derivative

Take v∈C_g and its measurable inverse y. Since y takes values in bounded D, y∈L∞(Ω). C2 and the a.e. inverse identities imply the change-of-variables formula also with an extra measurable factor in z. More explicitly, for any nonnegative measurable q on D, use f(x)=q(y(x))/K(y(x)) in C2 to obtain

∫_D q(z) dz=∫_Ω q(y(x))/K(y(x)) dx.

The a.e. bijection and K>0 justify this substitution; signed integrable expressions follow by their positive and negative parts. In particular the matrix field

A(x)=(Dv(y(x)))⁻¹

is well-defined a.e., and

∫_Ω |A|⁶ dx=∫_D |(Dv)⁻¹|⁶ K dz=∫_D |cof Dv|⁶/K⁵ dz<∞.

Now fix i,j and put ψ(z)=z_i and φ(x)=e_jη(x), initially with η∈C_c∞(Ω). The boundary term in (P) vanishes. The two volume terms, changed to x variables with C2, are

∫_Ω y_i(x)∂_jη(x) dx + ∫_Ω η(x) [(cof Dv)_{ji}/K](y(x)) dx=0.

The last coefficient is A_{ij}. This is precisely the distributional definition of ∂_jy_i=A_{ij}. Hence y∈W^{1,6}(Ω), with Dy=(Dv)⁻¹∘y. This is a proof of weak differentiability, not an application of an inverse theorem outside its exponent range.

### The full primal trace and energy

Repeat the preceding identity with η smooth on Ωbar, using the now established Sobolev derivative. It gives

∫_Ω [y_i∂_jη+η∂_jy_i] dx=∫_{∂Ω}G_iη(ν_Ω)_j dS.

Sobolev Gauss–Green gives the same left side with Tr y_i on the boundary. Therefore (Tr y_i−G_i)(ν_Ω)_j=0 distributionally on ∂Ω for each j. Since the smooth unit normal has nonzero components locally and their squares sum to one, Tr y_i=G_i. This works on every boundary component.

The derivative identity gives det Dy=1/(K∘y)>0, and C2 gives exactly

I(y)=∫_D [a|cof Dv|⁶/K⁵+b|Dv|³/K²+c/K+dK³] dz=J(v)<∞.

Thus y∈A_g, proving C_g⊂B_g. Pass 2's full inverse-trace theorem now yields Tr v=h. This completes the equivalence.

## 3. Exact transfer of minimization

The inverse correspondence A_g↔B_g is bijective modulo null sets and preserves the energy. It follows without a density or approximation claim that

min_{A_g} I = min_{B_g} J = min_{C_g} J,

and y_* is a global primal minimizer if and only if v_*=y_*⁻¹ minimizes J over B_g, equivalently C_g.

This is a precise inverse variational problem. It is not minimization over every W^{1,9/5} map with trace h and finite J. The extra conditions in C2–C3 must be proved for any proposed comparison. Checking det D(v+tζ)>0 alone is insufficient.

## 4. Energy-bounded weak closure without low-exponent minor continuity

**Proposition.** For every M<∞ the sublevel {v∈B_g:J(v)≤M} is sequentially weakly compact in W^{1,9/5}(D). If v_n∈B_g converges weakly in that space and liminf J(v_n)<∞, then v∈B_g and J(v)≤liminf J(v_n).

**Proof.** Work along a subsequence with bounded energies and realizing the liminf. Lift v_n to its primal inverse y_n. Energy equality and the fixed full trace bound y_n in W^{1,6}(Ω). Primal polyconvex lower semicontinuity and weak continuity of the primal minors give, after a subsequence, y_n⇀y in W^{1,6}, y∈A_g and

I(y)≤liminf I(y_n).

Compact Sobolev embedding on the smooth bounded domain also gives y_n→y uniformly on Ωbar. Meanwhile the inverse energy estimates and bounded range Ω bound v_n in W^{1,9/5}(D). Rellich compactness gives a subsequence converging a.e. to a weak Sobolev limit v, whose values lie in Ωbar.

Choose one common full-measure subset of D where all inverse identities y_n(v_n(z))=z hold and v_n(z)→v(z). Uniform convergence of y_n and continuity of y then give

y(v(z))=z.

For z∈D, v(z) cannot lie on ∂Ω because y(∂Ω)=G(∂Ω)=∂D. Thus v(z)∈Ω a.e. The already established a.e. uniqueness of the inverse of y identifies v=y⁻¹ a.e. Hence v∈B_g, and

J(v)=I(y)≤liminf I(y_n)=liminf J(v_n).

No weak continuity of cof Dv_n or det Dv_n at the low inverse gradient exponent was used. The crucial compact object is the primal map y_n.

The same proof applies if merely v_n→v strongly in L¹(D): energy boundedness yields a weak Sobolev subsequence, whose a.e. limit agrees with the L¹ limit. It likewise gives the asserted inequality.

## 5. What relaxation does and does not add

Define J_B(v)=J(v) on B_g and J_B(v)=+∞ otherwise, on W^{1,9/5}(D). Section 4 proves sequential weak lower semicontinuity of this extended functional. Its sequential weak relaxation is therefore J_B itself. The analogous functional on L¹(D), extended by infinity outside B_g, is also sequentially lower semicontinuous. No map outside B_g can be reached with a bounded liminf energy in either relaxation.

This does not assert that the unweighted weak closure of B_g contains only B_g when the approximating energies diverge. It does not prove density of diffeomorphisms or homeomorphisms in A_g, nor an energy-recovery sequence from such classes. No such approximation is needed for the exact transfer proved here.

It also does not identify finite J plus trace h with B_g. The energy controls derivatives and minors but does not, by itself, establish C2 or C3. Any unconstrained dual PDE or regularity theorem requiring arbitrary additive competitors still needs an admissibility theorem beyond the present results.
