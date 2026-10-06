# Partial analysis of weighted Yamabe heat-trace monotonicity

Problem 30001169 / OWR-3389-022, rank 822. Status: **unresolved after five approaches**. These are partial deductions and reproducible tests, not a proof or counterexample to the full conjecture. No novelty or publication-priority claim is made.

## 1. Exact scope and conventions

The primary source is Carlo Morpurgo's item (16), section 9, printed pp. 421–422 of *Low Eigenvalues of Laplace and Schrödinger Operators*, Oberwolfach Report 06/2009, DOI [10.4171/owr/2009/06](https://doi.org/10.4171/owr/2009/06). The [official EMS PDF](https://ems.press/content/serial-article-files/46205) was inspected visually on PDF pages 67–68. This target is Conjecture 2, not the adjacent Conjecture 1 comparison problem.

Let g be the unit round metric on S^n, n≥4, and use the nonnegative Laplacian. Put c_n=(n−2)/(4(n−1)) and Y=Δ_g+c_n R_g=Δ_g+n(n−2)/4. Let W be smooth, everywhere positive, and satisfy ∫W^(n/2)dv_g=Vol(S^n,g). The operator is Y_W=W^(−1/2) Y W^(−1/2) on L²(dv_g). The question is whether f_W(t)=t^(n/2)Tr(exp(−tY_W)) decreases for every t>0.

For h=Wg, dv_h=W^(n/2)dv_g and L_h=Δ_h+c_nR_h=W^(−(n+2)/4)Y W^((n−2)/4). Multiplication Uu=W^(n/4)u is unitary L²(dv_h)→L²(dv_g), and U L_h U^−1=Y_W. Thus the geometric conformal Laplacian heat expansion applies with exactly this measure. In particular this is not a drift Laplacian on an independently weighted measure space.

Constant rescaling must also rescale time: for a>0, Y_(aW)=a^−1Y_W and f_(aW)(t)=a^(n/2)f_W(t/a). Consequently the sign of f′ is invariant under constant normalization, but numerical time coordinates are not.

## 2. Approach one: local heat invariants

For each fixed smooth h, with a differentiated asymptotic expansion,

f_W(t)=(4π)^(-n/2)[Vol(h)+t(1/6−c_n)∫R_h dv_h+t² B_4(h)+…].

Here 1/6−c_n=(4−n)/(12(n−1)). Writing h=u^(4/(n−2))g gives ∫R_hdv_h=∫[4(n−1)/(n−2)|∇u|²+n(n−1)u²]dv_g>0. Thus f′_W(t)<0 for all sufficiently small positive t when n≥5. This agrees with the 2009 report.

The apparently exceptional dimension four is settled locally by the next coefficient. The integrated coefficient for Δ_h+R_h/6 is

B_4(h)=(1/180)∫(|Rm_h|²−|Ric_h|²)dv_h.

Total divergence terms integrate to zero. Since h is conformally flat in dimension four, |Rm|²=2|Ric|²−R²/3. With E=Ric−Rg/4, Gauss–Bonnet gives ∫(−|E|²/2+R²/24)dv=8π²χ(S⁴)=16π². Hence ∫(|Rm|²−|Ric|²)dv=−32π² and (4π)^−2 B_4=−1/90. Volume normalization gives Vol(S⁴)/(4π)²=1/6. Therefore

f_W(t)=1/6−t²/90+O_W(t³),     f′_W(t)=−t/45+O_W(t²).

Every fixed admissible W in dimension four has a strictly decreasing scaled trace on some interval (0,ε(W)). No uniform ε over all weights is asserted. The heat expansion is used only at t→0; its remainder cannot be discarded at intermediate times.

This coefficient identity is standard: [Andreas Juhl, *Heat kernel expansions, ambient metrics and conformal invariants*](https://arxiv.org/abs/1411.7851), §14.2, p. 74, formulas (14.4)–(14.5), explicitly gives the normalized integrated four-dimensional coefficient −χ/180 plus a Weyl-curvature term. Juhl's P₂ is the negative of our positive L, and his Tr(exp(tP₂)) is our heat trace. Thus this is an application of known heat-invariant formulas, not a claimed new invariant or a full resolution.

## 3. Approach two: spectral lower bounds and a quantitative near-round range

Set p=n/2. Differentiating the absolutely convergent heat trace gives

f′_W(t)=t^(p−1)Σ_j(p−tλ_j(W))exp(−tλ_j(W)).

The normalized sharp Sobolev inequality and Hölder's inequality imply λ_0(W)≥n(n−2)/4. Specifically ∫Wv²≤Vol(S^n)^(2/n)||v||²_(2n/(n−2)), while ∫vYv≥[n(n−2)/4]Vol(S^n)^(2/n)||v||²_(2n/(n−2)). Hence every term is nonpositive when t≥2/(n−2); higher eigenvalues make the sum strictly negative even at equality. This recovers the source's large-time statement.

A finite exact computation extends the guaranteed interval for a restricted, but infinite-dimensional, class of weights:

**Partial theorem.** If n=4, W has the prescribed normalization, and 999/1000≤W≤1001/1000 pointwise, then f′_W(t)<0 for every t≥1/4.

Proof of the finite portion: denote m=999/1000 and M=1001/1000. The generalized Rayleigh quotient is ∫vYv/∫Wv². Min–max gives λ_j(1)/M≤λ_j(W)≤λ_j(1)/m, counting eigenvalues with multiplicity. The round degree-ℓ eigenvalue is μ_ℓ=(ℓ+1)(ℓ+2), with multiplicity d_ℓ=(2ℓ+3)(ℓ+1)(ℓ+2)/6. Eigenvalue groups may overlap; the ordered min–max bounds, and therefore their sums, remain valid.

Write q(x)=(2−x)e^−x. Since q′(x)=(x−3)e^−x, q has a unique minimum, so its maximum on every compact interval is attained at an endpoint. Partition [1/4,1] into 750 consecutive intervals [a_i,b_i], each of length 1/1000. On the i-th interval the contribution of the first nine round degree blocks is at most

U_i=Σ_(ℓ=0)^8 d_ℓ max{q(a_i μ_ℓ/M),q(b_i μ_ℓ/m)}.

All omitted modes have tλ≥(1/4)·110/M>2 and hence negative contributions. Omitting them is an upper bound, with no approximation of their size. The attached certificate encloses every exponential by exact rational arithmetic and verifies U_i<−3/500 for every i. Thus f′_W(t)=tΣq(tλ_j)<0 on [1/4,1]. For t≥1 use λ_0(W)≥2 as above. This proves the stated partial theorem.

The certificate uses odd/even Taylor sums of exp(−z) through degrees 33 and 32 for 0≤z≤1. Alternating-series bounds enclose the exponential. Repeated squaring, with explicit integer floor/ceiling at scale 10^40, encloses exp(−x) for the original argument. Every comparison is rational; neither floating-point signs nor Python assertions are used. The code does not prove min–max, heat asymptotics, or the Sobolev inequality.

**Remaining gap:** for such near-round weights there may still be an interval between ε(W) and 1/4. In particular pointwise closeness alone has not been converted into uniform bounds on heat-expansion remainders.

## 4. Approach three: the infinite product-cylinder model

This checks an independently derived degeneration model, not a compact-sphere counterexample. On ℝ×S^(n−1) with product metric the scalar curvature is (n−1)(n−2), and the positive conformal Laplacian is −∂²_s+Δ_(S^(n−1))+(n−2)²/4. The scaled trace density per unit cylinder length is

(4π)^−1/2 t^((n−1)/2)Tr(exp[−t(Δ_(S^(n−1))+(n−2)²/4)]).

For n≥5 it is (4π)^−1/2 e^(−t/4) times the round scaled Yamabe heat trace in dimension n−1, so the round monotonicity recorded in the primary source makes it strictly decreasing.

For n=4 it is a positive constant times G(t)=t^(3/2)Σ_(j≥1) j²e^(−tj²). If t≥3/2, termwise differentiation is strictly negative. Poisson summation gives

G(t)=√π/4 [1+2Σ_(k≥1)(1−2π²k²/t)e^(−π²k²/t)].

The derivative of the k-th bracket term has sign 3−2π²k²/t. All these derivatives are strictly negative for 0<t<2π²/3. Since 3/2<2π²/3, the two ranges cover every positive t, including the endpoints using the other representation. Absolute convergence on compact positive time intervals justifies differentiation. Thus this product-cylinder density decreases in every dimension n≥4.

**Remaining gap:** no sign for the derivative of a *finite capped* cylinder follows from a decreasing infinite-cylinder density. End effects and their differentiated remainders would need separate bounds. No finite-cylinder conclusion is claimed, and the separate dimension-three comparison investigation is not used here.

## 5. Approach four: radial spectral exploration

For a weight depending on x=cosθ, decompose into degree-q harmonics on S³, multiplicity (q+1)². An orthogonal radial basis is (1−x²)^(q/2)P_j^(q+1,q+1)(x), with round eigenvalues (j+q+1)(j+q+2). Gauss–Jacobi quadrature forms the weighted Gram matrix B, and a finite generalized eigensolver solves Ac=λBc. The weights tested were the exactly defined smooth positive functions W(x)=c exp(a T_k(x)), with c chosen from the volume normalization; the computation approximates c by quadrature. T_k is the Chebyshev polynomial, represented in code by cos(k arccos x).

The attached floating-point script samples k∈{0,1,2,3,4,6,8,12}, a∈{0.1,0.5,1,2,4} (with only a=0 for k=0), and 120 times in [0.015,1]. Coarse orders are J=55,Q=35. Six sensitive cases are rerun at J=160,Q=100. All outputs are explicitly marked exploratory.

Several positive coarse values vanish under refinement. For example k=1,a=4,t=0.015 changes from about +0.00436 at (55,35) to about −0.00063129 at high orders. The omitted spectrum can contribute negatively to f′, so truncated positive sums are not lower bounds. A separate preliminary ball-support/Bessel-zero model in even dimensions 4,6,8 also did not suggest a positive derivative at the sampled scales; that discontinuous limiting model is not an admissible smooth weight and is not used as evidence for the theorem.

**Remaining gap:** there are no rigorous eigenvalue, quadrature, or omitted-tail error enclosures in these scans. A negative scan does not prove monotonicity; a positive truncated scan does not disprove it. The exact partial theorem in §3 is independent of all these computations.

## 6. Approach five: why endpoint data cannot finish the problem

A simple abstract spectral construction proves that the known endpoint data alone are insufficient. Begin with the round S⁴ spectrum. Replace only its five eigenvalues equal to 6 by five eigenvalues equal to 100; keep the eigenvalue 2 and all degree-ℓ≥2 eigenvalues unchanged. This is a positive abstract discrete spectrum, **not asserted to be the spectrum of any Y_W**.

Its scaled trace is f_*(t)=f_1(t)+5t²(e^(−100t)−e^(−6t)). It has the same terms through t² as the round trace and the same lowest eigenvalue 2. Its heat trace is even below the round trace at every positive t. Nonetheless f_*′(1/2)>0.

Here is a rational bound for that last assertion. Write S=f_*′(1/2)/(1/2). The ground-state contribution is e^−1>1/3 because e<3. For ℓ≥2, bound the magnitude of the negative term by P_ℓ exp(−μ_ℓ/2), where P_ℓ=(2ℓ+3)(ℓ+1)²(ℓ+2)²/12 and P_2=84. Each of the three factors in P_(ℓ+1)/P_ℓ decreases with ℓ, so the ratio is at most P_3/P_2=25/7<4. Also μ_(ℓ+1)/2−μ_ℓ/2=ℓ+2≥4. Using e>8/3 bounds the ratio of consecutive tail terms by r=4(3/8)^4<1 and the first term by 84(3/8)^6. The five replacement eigenvalues contribute magnitude 240e^−50<240/2^50. Therefore

S > 1/3 − 84(3/8)^6/[1−4(3/8)^4] − 240/2^50 > 1/20.

The last inequality is checked exactly in the certificate; e>8/3 follows already from the first five terms of its power series, and e<3 from the factorial/geometric-series comparison. This model has eventual strict decrease and a negative small-time derivative but an intermediate increase.

**Remaining gap:** the geometry and multiplication-operator structure of W are essential. Realizability of the abstract spectrum has not been shown and is not expected from these data alone. This construction is an obstruction to a proof strategy, not a counterexample to the question.

## 7. Status, literature, and acceptance boundary

The full question remains unresolved in this attempt. The proved outputs are: (i) every admissible fixed W decreases for sufficiently small t, including dimension four by a standard coefficient identity; (ii) the known explicit large-time range; (iii) the exact quantitative near-round n=4 range t≥1/4; (iv) monotonicity of the infinite product-cylinder density; and (v) a nongeometric spectral model showing why the endpoint criteria cannot suffice.

Public searches checked the exact title, Yamabe/conformal-Laplacian heat-trace monotonicity, Morpurgo/CLR terms, the official source, Juhl's heat-invariant article, and Rupert L. Frank's [*Cwikel's theorem and the CLR inequality*](https://doi.org/10.4171/JST/59). No current publication resolving this precise arbitrary-weight monotonicity statement was identified. That is a bounded search result, not proof of global literature completeness. The similarly named Laugesen–Morpurgo Neumann heat-kernel monotonicity problem is different. The live catalog page could not be read (403 / retrieval errors); the supplied complete record and official report are distinguished in PUBLIC_METADATA.json.

No matching actual prior target attempt was found in the checked default-branch code, all-state PR title/body search, or exact-ID commit search. No remote state was changed.
