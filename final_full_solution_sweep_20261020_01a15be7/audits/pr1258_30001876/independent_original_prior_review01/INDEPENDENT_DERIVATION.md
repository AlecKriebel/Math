# Direct Jacquet normalization and spectral reconstruction

This is an independently authored derivation for the literal printed Jacquet convention. It does not import the disputed constant from Takhtadzhyan–Vinogradov, Goldfeld or Stade. Standard Gamma/Laplace, Gaussian Fourier, K-Bessel, beta, Barnes and spectral identities are identified below. No assertion of an official journal correction, novelty or a new automorphic theorem is made.

## 1. Raw integral, including the power function

Use a,b>0 and Y=diag(ab,a,1). Li–Young(2.1)–(2.3) use

Iν(Y)=a^(ν1+2ν2)b^(2ν1+ν2),

u=[[1,y,z],[0,1,x],[0,0,1]], w=[[0,0,1],[0,−1,0],[1,0,0]],

and the character exp(−2πi(x+y)). Put p=3ν1/2, q=3ν2/2, k=p+q−1/2. Start with Re p,Re q>1/2. In this region all manipulations of the original real Jacquet integral below are absolutely integrable; afterward use its standard analytic continuation.

For a positive-determinant matrix g, let R be the squared norm of its bottom row and S the squared norm of the wedge of its bottom two rows. Its lower Iwasawa ratio is sqrt(S)/R and its upper ratio is det(g)sqrt(R)/S. Consequently

Iν(g)=det(g)^(2ν1+ν2) R^(−3ν2/2) S^(−3ν1/2).

For g=wuY, direct row multiplication gives

R=a²b²+a²y²+z²,

S=a²Q, where Q=a²b²+b²x²+(z−xy)²,

det(g)=a²b.

Thus the actual Jacquet integral is

Wν(a,b)=a^(ν1+2ν2)b^(2ν1+ν2) ∫R³ R^(−q)Q^(−p) exp(−2πi(x+y)) dx dy dz.

This step fixes which spectral signs are attached to which diagonal ratio. No reliance on the later Langlands labels is involved.

## 2. Gaussian reduction to two Fourier integrals

Apply t^(p−1) and s^(q−1) Gamma-Laplace representations to Q^(−p) and R^(−q). Integrating z gives

∫ exp(−t(z−xy)²−sz²) dz=sqrt(π/(t+s)) exp(−ts x²y²/(t+s)).

Set t=h(1−v),s=hv with h>0,0<v<1; the Jacobian is h. The remaining quadratic expression factors exactly:

a²b²+(1−v)b²x²+v a²y²+v(1−v)x²y²
=(a²+(1−v)x²)(b²+vy²).

The h integral is Γ(k) times the reciprocal kth power of this product. Writing A0=a^(ν1+2ν2)b^(2ν1+ν2), we obtain

Wν=A0 sqrt(π)Γ(k)/(Γ(p)Γ(q)) ∫₀¹ (1−v)^(p−1)v^(q−1)
   [∫R(a²+(1−v)x²)^(−k)e(−x)dx]
   [∫R(b²+vy²)^(−k)e(−y)dy] dv.

Absolute convergence is checkable before oscillation is used. Integrating the corresponding absolute x,y bounds gives a constant times (1−v)^(Re p−3/2)v^(Re q−3/2), integrable under the stated assumptions; Re k>1/2. This justifies Fubini, the Gamma-Laplace substitutions and the Gaussian step on the starting domain.

The elementary Fourier-Laplace evaluation is, for c,h>0,

∫R(c²+h x²)^(−k)e(−x)dx
=2π^k Γ(k)^(−1)c^(1/2−k)h^(−k/2−1/4) K_(k−1/2)(2πc/sqrt(h)).

It follows by inserting the Gamma-Laplace representation, integrating the Gaussian Fourier transform, then using ∫₀∞ t^(r−1)e^(−A t−B/t)dt=2(B/A)^(r/2)K_r(2sqrt(AB)). These are elementary integral definitions/identities for Gamma and K, rather than an imported GL3 Whittaker normalization.

## 3. Completion and the factor8

Define the completion exactly as printed in(3.13):

D=π^(1/2−3ν1−3ν2)Γ(p)Γ(q)Γ(k), W*=D Wν.

The preceding two Fourier integrals give a prefactor4π^(2k+1/2)/(Γ(p)Γ(q)Γ(k)). Since 1/2−3ν1−3ν2=−2k−1/2, completion cancels all Gamma and π factors and leaves4. The exponents of a,b become 1+(ν2−ν1)/2 and1+(ν1−ν2)/2.

The remaining v exponents are (q−p)/2−1 and(p−q)/2−1. Substitute v=u²/(1+u²). Its weighted Jacobian is

v^((q−p)/2−1)(1−v)^((p−q)/2−1)dv=2u^(q−p)du/u.

Therefore, with δ=ν2−ν1 and μ=3(ν1+ν2)/2−1,

W*(a,b)=8ab(a/b)^(δ/2) ∫₀∞ K_μ(2πa sqrt(1+u²))
          K_μ(2πb sqrt(1+u^(−2)))u^(3δ/2)du/u.                 (A)

This proves the exact Bessel identity needed by the earlier challenge directly from its raw Jacquet definition, including its factor8. No unread original Stade proof is counted as verified. The identity initially holds in the above common domain and extends through the standard meromorphic Jacquet continuation. At exceptional removable values use limits; no new automorphic continuation theorem is claimed.

## 4. Mellin and Barnes calculation, independently matched

Set η1=ν2−1/3,η2=ν1−1/3 and

λ1=2η1+η2, λ2=−η1+η2, λ3=−η1−2η2.

Then Σλ=0, δ=−λ2, μ=(λ1−λ3)/2. Equation(A) has the completed Bump/Blomer form with these explicitly interchanged parameters. Using the standard Bessel Mellin identity

∫₀∞ K_μ(2πc t)t^(z−1)dt=(1/4)(πc)^(−z)Γ((z+μ)/2)Γ((z−μ)/2),

the double transform is

Mλ(X,Y)=∫W*(a,b)a^(X−1)b^(Y−1)da/a db/b
=π^(−X−Y)/4 × ∏j Γ((X+λj)/2)Γ((Y−λj)/2) /Γ((X+Y)/2).      (B)

The remaining u beta integral supplies1/2. Thus the factor is8×1/4×1/4×1/2=1/4. Begin far enough to the right for absolute convergence; the beta parameters are (Y−λ2)/2 and(X+λ2)/2, with positive real parts there. This also checks the orientation of both diagonal variables.

Let

Iλ(s,τ)=∫W*(a,b)K_(iτ)(2πb)(a²b)^s da db/(a²b²).

Mellin inversion of the last K, followed by(B) with X=2s,Y=s−z, gives

Iλ=π^(−3s)/16 ∏jΓ(s+λj/2)
  ×(1/(2πi))∫ Γ((z+iτ)/2)Γ((z−iτ)/2)
          ∏jΓ((s−z−λj)/2)/Γ((3s−z)/2) dz.

Set z=2w, retaining its Jacobian2. Use Barnes' second lemma in its full form

(1/(2πi))∫Γ(w+a)Γ(w+b)∏jΓ(cj−w)/Γ(a+b+c1+c2+c3−w)dw
=∏jΓ(a+cj)Γ(b+cj)/∏j<lΓ(a+b+cj+cl).

Take a=iτ/2,b=−iτ/2,cj=(s−λj)/2. The three denominator factors are Γ(s+λj/2) and cancel the outside factors. This yields

Iλ(s,τ)=π^(−3s)/8 ∏j∏ε=±1 Γ((s+εiτ−λj)/2).              (C)

For purely imaginary λ and realτ, Re s>0 with0<Re w<Re s/2 separates the Barnes poles. General parameters can start farther right. Gamma exponential decay justifies the contour transform; continuation is meromorphic. Barnes' second lemma is an explicitly identified standard special-function import. The original proofs of all foundational Gamma/Barnes identities are not recursively reproduced here; the central disputed GL3 normalization has instead been derived in Sections1–3.

## 5. Exact repair in the two conventions

Write A=1−ν1−2ν2,B=−ν1+ν2,C=2ν1+ν2−1, so A+B+C=0. Define

P±(s,τ)=π^(−3s)∏Q∈{A,B,C}∏ε=±1 Γ((s+εiτ±Q)/2).

For the literal printed power function, λ=(−A,−B,−C). Since W*=D Wν, equation(C) gives

8J=P+/D, where J=∫Wν(a,b)K_(iτ)(2πb)(a²b)^s da db/(a²b²). (D)

If the power exponents are explicitly changed to a^(2ν1+ν2)b^(ν1+2ν2), the same derivation with ν1 andν2 interchanged gives λ=(C,B,A) and8J_Bump=P−/D. These are distinct for generic parameters. Neither a contragredient substitution nor an identification of Fourier coefficients across the two conventions has been made.

A coherent literal convention uses H=8J=P+/D for the period factor. If G_int retains the printed integral definition G_int=4J, its corrected gamma expression is P+/(2D), and the period includes2G_int. This distinguishes the two symbols rather than declaring all of(3.13),(3.18),(3.19),(3.20) simultaneously correct. The completed integral is P+/8, not the displayed P−/(4D). In the explicitly changed Bump convention replaceP+ byP−. The final printed gamma expression can thus agree with H in that convention even though intermediate displayed equalities cannot all hold.

## 6. Period, ineffective stabilizer and fixed scale

Use X=SL2(Z)\H, dμ=dx dv/v², g_z=[[sqrt(v),x/sqrt(v)],[0,1/sqrt(v)]], f_r(z)=F(diag(rg_z,1)). The center removed in H3 is harmless. Upper block-diagonal GL2 with positive scale, modulo its right orthogonal factor, is three-dimensional inside five-dimensional H3. Fixed r is a two-dimensional slice of that codimension-two restriction.

Let c_j(r)=<f_r,u_j>, c_τ(r)=<f_r,E(·,1/2+iτ)> and Λ(s)=∫₀∞c(r)r^(2s−1)dr/r. Keep the source's raw Fourier expansion(2.8), its U2 with diagonal1, and its Fourier coefficients A_F. The phase of the GL2 vector is conjugated in the inner product. Put a=r/sqrt(v),b=v after unfolding. Then r=a sqrt(b),dr/r=da/a, and all scale weights give precisely J above. Rescaling a→a/m,b→b/n gives m^(−2s)n^(−s), using the GL2 coefficient relation ρ_j(n)=ρ_j(1)λ_j(n)n^(−1/2).

The two U2 cosets above each ±U2 coset have equal Whittaker seeds on this restriction: multiplying the upper2×2 block by−I is a right multiplication by diag(−1,−1,1), which is orthogonal. The strip unfolds twice for the ordinary hyperbolic fundamental domain. The factor1/2 in the source's Eisenstein definition(2.18) independently confirms this ineffective-center convention. Thus the even period is

Λ_j(s)=8 conjugate(ρ_j(1)) L_j(s)J_tj(s)
      =conjugate(ρ_j(1)) L_j(s)H_tj(s),

L_j(s)=Σm,n≥1 A_F(m,n)λ_j(n)/(m²n)^s.

Its three factors2 are the U2 stabilizer, the GL2 Fourier K normalization and the signed-index pairing. The same unfolding applies to E_τ, whose constant Fourier terms disappear against the nonzero Whittaker character. The source omits that proof; this argument supplies it. At first use a common half-plane of absolute convergence; continue the product through its integral-defined period. No gamma division at a zero is required to define that continuation.

The symmetry diag(−1,1,−1)∈SL3(Z) and right orthogonal invariance make f_r(−x+iv)=f_r(x+iv); all odd cusp coefficients vanish at every scale. Unfolding against the global constant vector kills each nonzero x Fourier character, so that component also vanishes. This does not make the restriction a GL2 cusp form: Eisenstein components can remain.

## 7. Convergence, inversion and norm

The determinant-one representative r^(−2/3)diag(rg_z,1) has row-lattice vectors of lengths r^(1/3)/sqrt(v) and r^(−2/3). Their minimum bounds the shortest row vector. For r≥1 it is at most r^(−1/6)v^(−1/4); for r≤1 use r^(1/3)v^(−1/2). On a modular fundamental domain v has a positive lower bound. Quantitative reduction and the standard rapid-decrease theorem for cusp forms and their right derivatives therefore give arbitrary power decay in r at both ends and sufficient decay in v. These are named foundational automorphic imports. They apply to the smooth cuspidal restriction; they do not follow for an arbitrary noncuspidal automorphic form.

This gives f_r∈L2(X), finiteness of ∫||f_r||²dr/r, and Schwartz behavior in log r for each fixed coefficient paired with a cusp vector or a fixed Eisenstein series of polynomial growth. The constant-vector unfolding is absolutely justified in this same setting. Mellin inversion, with Fourier frequency2t rather than t, gives

c_j(r)=(1/π)∫R Λ_j(1/2+it)r^(−2it)dt,

and similarly for c_τ. This is absolutely convergent for each fixed smooth coefficient under those imports; with only L2 information it is an L2 identity, or use Fejér regularization for continuous-point evaluation. Do not interchange the entire j,t,τ family without an additional estimate.

GL2 spectral theory with the source's Eisenstein normalization gives

f_r=Σj≥1,even c_j(r)u_j +(1/(4π))∫R c_τ(r)E_τ dτ

in L2, and locally uniformly under the usual smooth spectral/Sobolev hypotheses verified by rapid decrease. This supplies the fixed-scale decomposition rather than only its scale-averaged version. Parseval, Mellin Plancherel and Tonelli on nonnegative terms give

N(F)=(1/π)Σj≥1∫R|Λ_j(1/2+it)|²dt
       +(1/(4π²))∫R∫R|Λ_τ(1/2+it)|²dt dτ.

None of these reconstruction statements requires the sharp eigenvalue-aspect restriction bound from Sections5–10. The Fourier–Whittaker expansion, GL2 spectral theorem, reduction/derivative decay, analytic continuation of Jacquet integrals and Barnes' identity remain explicitly imported standard theory. They are not circular imports of the sought fixed-scale reconstruction or of the disputed GL3 normalization.
