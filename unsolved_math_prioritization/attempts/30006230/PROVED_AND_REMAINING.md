# Exact proved scope and remaining formulation choice

This summary follows the [final acceptance index](accepted/pass1_audit/ACCEPTANCE_INDEX.md) and [source-scope adjudication](scope_adjudication/SOURCE_RESOLUTION_SCOPE.md). It adds no mathematical claim.

## Fixed notation and conventions

Let x ∈ Rⁿ, t ∈ R, Q = n + 2, ρ = (|x|⁴ + 4t²)^(1/4), ψ = |x|²/ρ², ∇G = (∇x, |x|∂t), and LG = Δx + |x|²∂t². Fix 0 < R ≤ ∞. Every spatial inequality is quantified over real tests in Cc∞(B_R minus {0}), where B_R = {ρ < R}, and uses Lebesgue measure. The nonzero axis is not removed.

The target B_Q(V,W;R) means that

\[
(r^{Q-1}Vf')'+r^{Q-1}Wf=0
\]

has f > 0 on the entire fixed interval (0,R), with coefficient of W exactly one. Flux-classical means f ∈ C¹ and r^(Q−1)Vf′ ∈ C¹, with the equation pointwise. No endpoint value, boundedness, integrability or extension of f is imposed. Under regular positive leading coefficients, the solution is classical.

Write

\[
\begin{aligned}
H_G[u]&=\int V(\rho)|\nabla_Gu|^2-\int W(\rho)\psi u^2,\\
H_\rho[u]&=\int V(\rho)\psi|u_\rho|^2-\int W(\rho)\psi u^2,\\
A_V[u]&=\int V(\rho)(L_Gu)^2/\psi,\\
D_{V,W}[u]&=\int\left[W(\rho)+(Q-1)(V(\rho)/\rho^2-V'(\rho)/\rho)\right]|\nabla_Gu|^2,\\
E_{V,g}[u]&=\int V(\rho)g(\rho)^2|\nabla_G(u_\rho/g(\rho))|^2,\\
S_Q[V]&=(Q-5)V/r^2+3V'/r-V''.
\end{aligned}
\]

Here uρ is the source gauge-polar derivative, (x·∇xu + 2t∂tu)/ρ. The Hardy–Rellich energy A is the nonnegative extended integral of the off-axis quotient. Its value on the null axis is immaterial. Every right side at issue is finite for each source test, so infinite A satisfies the stated inequality.

## Accepted principal assertions

- **Regular Hardy equivalence:** Q ≥ 3, V ∈ C¹ with V > 0, real W ∈ C¹. Either all-test condition H_G ≥ 0 or Hρ ≥ 0 is equivalent to B_Q. Both are also equivalent to the one-dimensional quadratic-form condition in the proof. No side condition or endpoint hypothesis is added.
- **Current nonnegative-potential core necessity:** Q ≥ 4, V ∈ C² with V > 0, W ∈ C¹ with W ≥ 0, S_Q[V] ≥ 0. The all-test core A ≥ D implies B_Q. For the regular-weight theorem, the W-sign and side conditions are needed only near zero, while V remains positive on the whole interval.
- **Global nonnegative-leading-weight extension:** Q ≥ 4, V ∈ C² with V ≥ 0, W ∈ C¹ with W ≥ 0, and S_Q[V] ≥ 0 everywhere. The same core necessity holds. This does not combine arbitrary interior zeros of V with merely near-zero side conditions.
- **Current real-potential counterexample:** Q = 5, R = exp(12), V = 1, W = λ/r² − 1/r⁴, S₅[V] = 0, with λ defined exactly by the proof's variational thresholds. A ≥ D holds for every original test, all those tests have finite A, and B₅ fails. Rounded numerical λ values do not specify this example.
- **Historical positive-potential counterexample:** Q = 3, R = 1, V = r^(3/4), W = λr^(3/4), S₃[V] = (7/16)r^(−5/4) > 0. The positive λ is variationally defined. The all-test core holds and B₃ fails, including the stated finite/infinite-energy treatment.
- **Fixed independent function necessity:** Q ≥ 3, V ∈ C¹ with V > 0, real W ∈ C¹, and one fixed independent g ∈ C² with g > 0. If A ≥ D + E for every source test, then g is a positive supersolution and an exact positive solution exists. The exact solution may differ from g. No side condition is needed for this necessity statement.
- **Degenerate Hardy obstruction:** for any Q ≥ 3 and interior a, V = r^(1−Q)(r−a)² and W = (1/4)r^(1−Q) satisfy both all-test Hardy premises but admit no strictly positive flux-classical solution across a. This example does not satisfy the Hardy–Rellich side condition.
- **Zero-weight classification:** with V = 0, each Hardy premise, the core premise, and the independent-function premise holds exactly when W ≤ 0. B_Q holds exactly when W = 0. In the global C² side-conditioned V ≥ 0 class, V is either everywhere positive or identically zero.

The five principal proof branches and the degenerate addendum have accepted dispositions. Full source tests, historical Q = 3, coefficient one, full-interval positivity, and the compact-primitive constraint have been addressed at those scopes. They are not outstanding proof gaps in this package.

## What prevents an unqualified source-level conclusion

The original Oberwolfach paragraph does not select a noncircular Hardy–Rellich antecedent. The cited forward theorem's remainder uses an already positive solution of the desired ODE. Keeping that meaning in the antecedent presupposes the conclusion. Dropping the remainder gives the proposed core; replacing the function by one fixed independent g gives a different proposed statement. Both are now addressed at their declared scopes, but the source does not identify either as its intended formalization.

The source also does not settle the adopted degenerate solution convention or all weight-sign, classical side-condition and energy conventions. Historical/current dimensions are kept separate and their relevant accepted branches are covered. An operational “deferred” designation concerns this formulation selection; it does not revoke the accepted mathematics.

No per-dimension classification of arbitrary real W, every possible degenerate weak solution notion, altered endpoint/test domains, test-dependent g, or arbitrary-supersolution all-test sufficiency is claimed. These extensions are not requirements for an already established counterexample to a universal branch and must not be presented as missing steps in its proof.
