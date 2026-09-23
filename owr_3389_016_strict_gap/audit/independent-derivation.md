# Independent derivation audit: strict discriminant gap bound

Checkpoint: 2026-09-23T03:47:54Z. Completion estimate for this assigned proof audit: **95%** (complete self-contained derivation; awaiting adversarial review of this artifact). No other candidate or audit files were inspected before deriving the argument. The parent subsequently reported that the spectral-remainder/zero-extension route independently coincides with the candidate. The self-adjointness obstruction in §4 was then developed as a different proof of the equality exclusion. No external communication was made and no commit was created by this audit agent.

## Exact claim and verdict

Let Ω be any nonempty bounded open subset of Rⁿ, where n≥1. Let H be the Friedrichs Dirichlet Laplacian on L²(Ω), with eigenvalues 0<E₁≤E₂≤⋯, counted with multiplicity. For J≥1 define

\[
A=J^{-1}\sum_{j=1}^{J}E_j,\qquad
B=J^{-1}\sum_{j=1}^{J}E_j^2,
\]
\[
m=\frac{n+2}{n}A,\qquad
D=m^2-\frac{n+4}{n}B.
\]

**Verdict:** the claim

\[
D>\frac{(E_{J+1}-E_J)^2}{4}
\]

is valid for every finite J. Neither connectedness nor boundary smoothness is required. The proof below includes the zero-gap and ground-eigenvalue-multiplicity cases.

The strongest auxiliary result verified here is that the Yang polynomial is strictly negative throughout the closed spectral gap [E_J,E_{J+1}] at every point strictly greater than E₁. The only possible endpoint equality in that interval occurs when the endpoint is E₁.

## 1. Functional-analytic setup on arbitrary bounded open sets

The form domain is H₀¹(Ω). Extension by zero into a bounded box and Rellich compactness give compact resolvent, and the box Poincaré inequality gives E₁>0. Choose an orthonormal eigenbasis u_j, real or complex.

For each coordinate x_α, multiplication maps H₀¹(Ω) into itself. The Dirichlet operator-domain characterization is

\[
\operatorname{Dom}(H)=\{u\in H_0^1(\Omega):-\Delta u\in L^2(\Omega)\},
\]

where the Laplacian is distributional. Therefore

\[
x_\alpha u_j\in\operatorname{Dom}(H),\qquad
(H-E_j)(x_\alpha u_j)=-2\partial_\alpha u_j.
\tag{1}
\]

Put a^α_jk=⟨x_αu_j,u_k⟩. Self-adjointness of multiplication gives |a^α_jk|²=|a^α_kj|². The following identities hold:

\[
\sum_k(E_k-E_j)|a^\alpha_{jk}|^2=1,
\tag{2}
\]
\[
\sum_k(E_k-E_j)^2|a^\alpha_{jk}|^2
=4\|\partial_\alpha u_j\|_2^2.
\tag{3}
\]

For (2), evaluate the quadratic form of x_αu_j and use the weak eigenfunction equation with test function x_α²u_j. The terms involving x_α²|∇u_j|² and the cross term cancel, leaving ∫|u_j|²=1. Identity (3) is Parseval applied to (1). Since x_αu_j∈Dom(H), all quadratic-weight spectral sums below converge absolutely. These arguments use no boundary traces.

## 2. Exact nonnegative remainder

Write a=E_J, b=E_{J+1}, and

\[
Q(t)=t^2-2mt+\frac{n+4}{n}B=(t-m)^2-D.
\]

For any t∈[a,b], define

\[
R(t)=\sum_{\alpha=1}^n\sum_{j=1}^{J}\sum_{k>J}
(t-E_j)(E_k-E_j)(E_k-t)|a^\alpha_{jk}|^2.
\tag{4}
\]

All factors outside the squared coefficient are nonnegative, so R(t)≥0. Identities (2)–(3), together with ∑_α‖∂_αu_j‖²=E_j, give

\[
\begin{aligned}
nJQ(t)
&=\sum_{j\le J}\bigl[n(t-E_j)^2-4E_j(t-E_j)\bigr]\\
&=\sum_{\alpha,j\le J,k}(t-E_j)(E_k-E_j)(t-E_k)
|a^\alpha_{jk}|^2\\
&=-R(t).
\end{aligned}
\tag{5}
\]

In the last line, the summands with j,k≤J cancel in pairs: exchanging j,k reverses E_k−E_j while preserving the other factors and squared coefficient. This is a finite cancellation, so no rearrangement problem occurs.

Consequently Q(a)≤0 and Q(b)≤0. These alone yield the non-strict gap bound; the equality analysis is essential for strictness.

## 3. What vanishing remainder would force

Suppose t∈[a,b], t>E₁, and R(t)=0. Choose j=1. For every α and every k with E_k>t, necessarily k>J, and the coefficient

\[
(t-E_1)(E_k-E_1)(E_k-t)
\]

is strictly positive. Thus a^α_1k=0 whenever E_k>t, and

\[
x_\alpha u_1\in\operatorname{span}\{u_k:E_k\le t\}.
\tag{6}
\]

This span is finite dimensional. Equation (1) now shows that ∂_αu₁ is a finite Dirichlet eigenfunction sum as well. In particular, ∂_αu₁ belongs to Dom(H).

## 4. Independent equality obstruction by self-adjointness

Let u be any Dirichlet eigenfunction with eigenvalue E and suppose x_αu is a finite Dirichlet eigenfunction sum. Define v=∂_αu. Equation (1) makes v a finite eigenfunction sum, hence v∈Dom(H). Distributional derivatives commute with the Laplacian in Ω, so

\[
Hv=-\Delta(\partial_\alpha u)
=\partial_\alpha(-\Delta u)=Ev.
\tag{7}
\]

Both x_αu and v are in Dom(H). Self-adjointness and (1) therefore give

\[
-2\|v\|_2^2
=\langle(H-E)(x_\alpha u),v\rangle
=\langle x_\alpha u,(H-E)v\rangle=0.
\tag{8}
\]

Thus ∂_αu=0. Applying this to every coordinate in (6) gives ∇u₁=0 and contradicts

\[
\|\nabla u_1\|_2^2=E_1\|u_1\|_2^2=E_1>0.
\]

Hence

\[
R(t)>0\quad\text{and}\quad Q(t)<0
\qquad(t\in[a,b],\ t>E_1).
\tag{9}
\]

This proof requires neither zero extension nor Fourier analysis. In operator terms, a finite spectral expansion would turn x_αu into a generalized eigenvector satisfying (H−E)²(x_αu)=0; a self-adjoint operator has no nontrivial generalized eigenvectors.

### Initially derived alternative obstruction

Before receiving any information about the candidate proof, this audit independently obtained the following alternative: (6) implies ∂_αu₁∈H₀¹(Ω) for every α. Zero extension U of u₁ then lies in H²(Rⁿ), because its first derivatives are the zero extensions of ∂_αu₁ and lie in H¹(Rⁿ). The distributional equation −ΔU=E₁U holds on all of Rⁿ. Fourier transformation yields (|ξ|²−E₁)Û(ξ)=0. Since the sphere |ξ|²=E₁ has Lebesgue measure zero and Û∈L², U=0, a contradiction. The parent reported independent convergence of this route with the candidate; it should not be presented as a distinct proof family from that candidate.

## 5. Exact gap-defect identity and strict conclusion

Let c=(a+b)/2 and g=b−a. Averaging Q(a) and Q(b) gives

\[
\frac{Q(a)+Q(b)}2=(m-c)^2+\frac{g^2}4-D.
\]

Using (5),

\[
\boxed{
D-\frac{g^2}4
=(m-c)^2+\frac{R(a)+R(b)}{2nJ}.
}
\tag{10}
\]

If b>E₁, then R(b)>0 by (9), so the right-hand side is strictly positive. This includes positive gaps, zero gaps above the ground eigenvalue, and every J whose first J+1 eigenvalues are not all equal.

If b=E₁, then all E_j with j≤J+1 equal E₁. Here g=0, A=E₁, B=E₁², and

\[
D=\frac{4}{n^2}E_1^2>0.
\]

This is the sole case in which both remainders in (10) vanish; the square (m−c)² remains positive.

## 6. Boundary and falsification checks

- **J=1:** Q(E₁)=0 always. Strictness cannot correctly be justified by claiming both endpoint Yang inequalities are strict. The argument needs only R(E₂)>0 when E₂>E₁, and handles E₂=E₁ separately.
- **Multiplicity:** no assumption that E_J<E_{J+1} is made. Internal or endpoint multiplicities cause only zero summands in (4).
- **Disconnected Ω, including infinitely many components:** compact resolvent and finite spectral subspaces still hold for bounded Ω. No positivity or simplicity of a ground eigenfunction is used.
- **Rough boundary:** all boundary-sensitive steps are replaced by H₀¹ form identities, the operator-domain characterization, and distributional derivatives.
- **Normalization and units:** each a^α_jk has units of length; the cubic energy factor in R(t) times |a|² has units of energy squared, matching nJQ(t) and D.
- **Scaling:** dilation Ω↦sΩ sends E↦s⁻²E and both sides of the target inequality to s⁻⁴ times their original values.
- **n=1, one interval of length L:** with κ=π²/L², E_j=κj². This is consistent with strictness for every J. In particular J=1 gives D=4κ² versus gap²/4=9κ²/4.
- **Abstract-operator limitation:** the strictness is not a consequence of the non-strict Yang inequalities alone. Its mechanism uses the differential commutation with ∂_α and the Dirichlet realization. A generic spectral sequence satisfying non-strict bounds would not justify (7).

## Route registry and remaining gap

| Route | Mechanism | Evidence | Status | Exact remaining gap |
|---|---|---|---|---|
| Spectral remainder | Pairwise cancellation of the low-spectrum trace, leaving a nonnegative tail | Equations (2)–(5) | Verified derivation | None identified |
| Self-adjoint equality obstruction | Finite coordinate expansion creates a forbidden generalized eigenvector | Equations (6)–(8) | Verified derivation; distinct from zero extension | Independent adversarial review of domain steps |
| Zero-extension obstruction | Global L² Helmholtz solution cannot be supported on a Fourier sphere | Argument after (9) | Independently rediscovered; coincides with candidate family | None identified, but not independent family evidence after convergence |
| Purely algebraic endpoint equality | Try to exclude saturation using only non-strict Yang inequalities | First-gap saturation can be encoded in an abstract positive spectral sequence | Blocked | Needs a genuinely additional operator/domain fact; rephrasing saturation does not supply one |

No counterexample or unclosed mathematical gap was found. Novelty is not assessed by this audit. The proof does not produce a uniform positive numerical margin independent of Ω and J; it proves pointwise strictness at every finite J.

## Parent closure — 2026-09-23T04:02:39Z

Assigned derivation verification: 100%. The independent adversarial cross-check requested above passed; see proof-audit.md §6 and final-manuscript-audit.md. No remaining mathematical gap was identified. Priority was assessed separately in priority-audit-independent.md.
