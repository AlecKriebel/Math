# Critical polyharmonic endpoint: a known negative answer to unrestricted uniqueness

**Prior published multiplicity theorem applied to the exact parameter; independent review pending.** Record 30000252 / OWR-1050-001. This is a credited source correction, not a new multiplicity discovery.

## 1. Exact target and source qualifications

The original [Oberwolfach report 29/2005](https://oa.tib.eu/renate/server/api/core/bitstreams/91dd0822-361f-44ee-a77f-fa862bb21ab6/content), pp.1616–1617, asks whether Theorem 5 extends to the critical exponent. Its two conclusions are distinct: positive-solution uniqueness on positivity-preserving domains (including balls), and unrestricted uniqueness with p≥2; the latter also requires strictly negative divergence when m=1. The domain is bounded and conformally contractible, with a conformal field of nonpositive divergence. Boundary data are the full Dirichlet jet through order m−1, not Navier data. The report credits Schaaf for m=1. Its workshop date is 2005 despite the imported citation's “2006” label.

The pinned record uses the standard operator (−Δ)^m. The report actually prints −Δ^m in equations (3) and (4), while its subsequent positivity remark uses (−Δ)^m. We retain this notation discrepancy explicitly. The odd-order example below works under either reading and so does not require silently repairing the displayed equation.

The unrestricted endpoint conclusion is false. A published theorem already implies at least two classical solutions for every sufficiently small positive λ, even on a ball. This artifact does not classify the separate positive-only higher-order variant: two unrestricted solutions are not automatically two positive solutions.

## 2. Published input

Mónica Clapp and Marco Squassina, [*Nonhomogeneous polyharmonic elliptic problems at critical growth with symmetric data*](https://www.dmf.unicatt.it/~squassin/papers/lavori/clapsqua.pdf), Communications on Pure and Applied Analysis 2(2), 171–186 (2003), [DOI 10.3934/cpaa.2003.2.171](https://doi.org/10.3934/cpaa.2003.2.171).

Corollary 1.1 (p.172) gives at least two solutions of
\[
(-\Delta)^m v=|v|^{q-2}v+f,\qquad v\in H_0^m(\Omega),\qquad q=\frac{2n}{n-2m},
\]
for every nonzero sufficiently small f in H^{-m}(Ω), on a smooth bounded domain with n>2m. No nontrivial symmetry or topology hypothesis is needed for this corollary: the trivial group suffices. The same page states C^{2m,α} regularity up to the boundary for a C^{2m,α} boundary and C^{0,α} forcing. The authors credit Tarantello for m=1 and Deng–Wang for m=2.

We use that published theorem and its regularity statement as inputs; its concentration-compactness and variational proof are not independently reconstructed here. This source-based application is enough to refute unrestricted uniqueness.

## 3. Exact scaling, with quantified smallness

Set
\[
p=q-1=\frac{n+2m}{n-2m}>1,\qquad a=\frac1{p-1},\qquad v=\lambda^a u.
\]
For every λ>0, this is an invertible positive scalar change of variables. By homogeneity,
\[
(-\Delta)^m v
=\lambda^{a+1}+\lambda^{a+1-ap}|v|^{p-1}v
=\lambda^{p/(p-1)}+|v|^{p-1}v.
\]
Here a+1−ap=0 and a+1=p/(p−1). The same computation backwards proves equivalence, including all homogeneous boundary data.

Let C=||1||_{H^{-m}(Ω)}. It is finite by the continuous L² embedding and Cauchy–Schwarz, and strictly positive by testing against a nonnegative nonzero compactly supported smooth function. If κ>0 is the smallness constant in Corollary 1.1, then
\[
0<\lambda<\lambda_0:=\left(\frac{\kappa}{C}\right)^{(p-1)/p}
\quad\Longrightarrow\quad
0<\|\lambda^{p/(p-1)}\|_{H^{-m}}<\kappa.
\]
Thus the corollary provides distinct v₁,v₂; uᵢ=λ^{-a}vᵢ remain distinct. Constant forcing and a smooth domain give the stated classical regularity.

For smooth functions on a smooth boundary, the source's zero normal derivatives through order m−1 agree with the zero full boundary jet: use boundary-normal coordinates and differentiate the identically zero boundary traces tangentially, inductively in the normal order. Equivalently these are the classical traces of H₀^m. No Navier condition Δ^j u=0 has been substituted.

## 4. A higher-order counterexample immune to the printed sign ambiguity

Take m=3, n=7, and Ω=B₁(0) in R⁷. Then p=13≥2. The conformal field ξ(x)=−x has Dξ+Dξᵀ=−2I, divergence −7, and forward flow x↦e^{-t}x preserving the ball. All the geometric and exponent restrictions of the unrestricted part of Theorem 5, apart from replacing strict supercriticality by the proposed endpoint, are met.

For every sufficiently small λ>0, the preceding application gives at least two C^{6,α} solutions of
\[
(-\Delta)^3u=\lambda(1+u^{13}),\qquad
D^j u|_{\partial B_1}=0\ (j=0,1,2).
\]
The boundary requirement is u=∇u=D²u=0. Since (−Δ)^3=−Δ³, the counterexample also matches the report's literal odd-order operator. The scaling here is v=λ^{1/12}u and f=λ^{13/12}. Both solutions are nonzero because λ>0.

Consequently there cannot be a positive interval on which the proposed unrestricted critical endpoint has a unique solution. At λ=0 the homogeneous linear Dirichlet problem has only the zero solution; that isolated endpoint does not restore uniqueness for any interval [0,λ̄]. We make no sign assertion about the two higher-order solutions.

## 5. Outcome and limits

The answer to extending Theorem 5 as stated in its unrestricted form is negative, by an application of an earlier published theorem. The short dataset statement's unqualified uniqueness question is likewise answered negatively. This is not a full classification of positive solutions or a new analysis of the published multiplicity theorem. No novelty or human peer-review claim is made.

One substantive source-application route was used. The exact controls check scaling exponents, the odd-order sign, admissible dimensions, and the example's p≥2 condition. They do not numerically construct PDE solutions or certify the analytic theorem. Actual model metadata: inherited runtime; exact model identifier not exposed; no model or reasoning switch made.
