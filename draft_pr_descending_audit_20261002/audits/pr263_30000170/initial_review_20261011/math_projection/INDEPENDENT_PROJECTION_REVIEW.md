# Independent projection and quantifier review of PR263 / 30000170

**Verdict: GO for the mathematics of the explicitly scoped complex-coefficient Theorems A–C. HOLD for any promotion to an unqualified resolution of the original research target.** The projection implication, full exact-degree localization, and fixed positive-definite metric extension are sound. The construction supplies no conclusion about a real-only question or function prox-regularity relative to any fixed finite subgradient. Novelty and historical priority are outside this review.

Frozen input: `c4eff3253932a504f8e558c8b5f5b1b5e155de0f`, read from `initial_review_20261011/original_submission/files/attempts/30000170`. The initial derivation below preceded consulting any original reviewer or other current mathematical review. No author or original-reviewer code was executed. Own independent rational controls passed at **2026-10-11 21:38:08 UTC**, with 9,760 exact assertions. They supplement the universal proof below; they are not a projection solver or an existence certificate for an identified nearest pair.

## 1. Exact claim and success criterion

Let `S` be the set of monic complex quadratics whose roots have real parts **at most** zero, identified with real coefficient space `(Re a, Im a, Re b, Im b)`. The verified projection conclusion is

\[
\forall\varepsilon>0\ \exists q\notin S:\quad
\|q-z^2\|<\varepsilon,\qquad |\operatorname{argmin}_{s\in S}\|q-s\||\ge2.
\]

The norm may come from any one fixed positive-definite real inner product. The analogous statement is true in all six real coefficient directions for exact-degree complex quadratics, allowing the leading coefficient to vary. The proof must establish global nearest points in this coefficient metric; a nonconvex slice or two guessed candidates would not meet the criterion.

The epigraph conclusion concerns set prox-regularity at `(z²,0)` with **all** limiting normal directions included. It does not substitute for the finite-subgradient function definition.

## 2. Independent global stability description and boundary audit

Write `a=x+iy`, `b=u+iv`, and substitute `z=w-iy/2`. This imaginary translation leaves root real parts unchanged and gives

\[
p(w-iy/2)=w^2+xw+B+iV,\qquad
B=u+y^2/4,\quad V=v-xy/2.
\]

The exact global characterization is

\[
S=\{x\ge0,\ B\ge0,\ V^2\le x^2B\}. \tag{1}
\]

Here is a root-parameter derivation independent of any square-root branch. Write the two roots as `-r+iω₁`, `-s+iω₂`, with arbitrary real `r,s,ω₁,ω₂`. Then

\[
x=r+s,\qquad B=rs+\frac{(\omega_1-\omega_2)^2}{4},\qquad
V=\frac{(r-s)(\omega_1-\omega_2)}2,
\]
\[
x^2B-V^2=rs\big((r+s)^2+(\omega_1-\omega_2)^2\big). \tag{2}
\]

If `r,s≥0`, (1) follows. Conversely, under (1), if the bracket in (2) is positive, then `rs≥0` and `r+s≥0` imply `r,s≥0`. If that bracket is zero, `r+s=0` and `ω₁=ω₂`; the condition `B=rs≥0` again forces `r=s=0`. This covers every quadratic, including repeated roots.

Consequences checked explicitly:

- At `x=0`, stability is exactly `B≥0,V=0`; both roots lie on the imaginary axis. The inequality was not derived by dividing by `x` and then extrapolating to zero.
- At `B=0`, stability requires `V=0,x≥0`.
- The monic complex stable set is globally closed, directly from (1). It is nonempty and finite dimensional, so every input has a global nearest stable point.
- For real monic coefficients, `y=v=0`, and (1) reduces to `a≥0,b≥0`. This is the convex orthant. The complex obstruction therefore cannot be represented as a real quadratic counterexample.
- The closed boundary convention is essential. An open strictly stable set would have different projection-existence behavior; no strictly stable nearest-point statement is claimed.

## 3. Actual proximal normals, without a slice inference

For `t>0`, let

\[
p_t=(z+it)(z+t^2-it)=z^2+t^2z+t^2+it^3.
\]

One root is simple on the imaginary axis and the other has real part `-t²<0`. At this point, `x=B=t²>0`, `V=t³`. In a neighborhood depending on `t`, the lower boundary inequality is strict and (1) is simply the smooth inequality

\[
h(x,y,u,v)=v-xy/2-x\sqrt{u+y^2/4}\le0.
\]

Its full four-coordinate differential is

\[
n_t=Dh(p_t)=(-t,-t^2/2,-t/2,1). \tag{3}
\]

These are **actual proximal normals**, not just normals to a coefficient slice. To check this point: Taylor's formula at fixed `t` bounds `n_t·(s-p_t)` above by `K_t||s-p_t||²` for nearby feasible `s`. For more distant `s`, Cauchy–Schwarz extends the same form of bound after increasing `K_t`. Expanding distances to `p_t+τn_t`, with `0<τ<1/(2K_t)`, shows that `p_t` is its unique global nearest point in `S`. A uniform `K_t` is neither assumed nor needed.

Thus `n_t→n₀=(0,0,0,1)` is a convergent sequence of proximal normals at points approaching `p₀=z²`. It places `n₀` in the limiting normal cone used by PRT2000.

## 4. Independent obstruction with no radical arithmetic

Use the comparison point **`p₀` itself**, constant in `t`. Equations (3) and the coefficients of `p_t` give

\[
\langle n_t,p_0-p_t\rangle=t^3/2,
\qquad \|p_0-p_t\|^2=2t^4+t^6,
\]
\[
\frac{\langle n_t,p_0-p_t\rangle}{\|p_0-p_t\|^2}
=\frac1{2t(2+t^2)}\longrightarrow+\infty. \tag{4}
\]

If `S` were prox-regular at `p₀` relative to `n₀`, Definition 1.1 of PRT2000 would, after distance expansion, require some one fixed `ρ` to satisfy

\[
\langle n_t,p_0-p_t\rangle\le\frac\rho2\|p_0-p_t\|^2
\]

for every sufficiently small `t`. This contradicts (4). The quantifiers are satisfied: the base points approach `p₀`, the normals approach the one fixed limiting normal `n₀`, and the comparison point is always in the required neighborhood. This is stronger than a finite collection of bad numerical ratios.

As another exact check, comparison with `p_{κt}` gives

\[
\langle n_t,p_{\kappa t}-p_t\rangle
=\frac{(\kappa-1)^2(2\kappa+1)}2t^3.
\]

The frozen `κ=√2` numerator `2√2-5/2` is correct, but its radical sign test is unnecessary. Any fixed positive `κ≠1`, or the constant comparison used above, suffices.

There is also a useful limiting-normal interpretation. For stable coefficient vectors of norm `δ`, (1) implies

\[
|v|\le |xy|/2+x\sqrt{u+y^2/4}
\le\delta^2/2+\delta\sqrt{\delta+\delta^2/4}=o(\delta).
\]

Hence the imaginary-constant covector `n₀` is even a regular normal at `p₀`. It is not proximal there: `n₀·p_t=t³`, while `||p_t||²=2t⁴+t⁶`. This independently illustrates the degeneracy; the proof above does not need an unproved identification of regular and proximal normals.

## 5. The operative PRT theorem and the global projection consequence

The actual primary paper was read at Definition 1.1 and Proposition 1.2, printed p. 5233, the complete Theorem 1.3 at p. 5234, and Proposition 3.5 and its proof at pp. 5242–5243. [PRT2000, primary full text](https://sites.math.washington.edu/~rtr/papers/rtr170-LocalDiffDistance.pdf).

The operative assumptions are a closed subset `C` of a Hilbert space and a point of `C`. The theorem equates set prox-regularity with several distance and projection properties. Its additional clause `(k)` equates it with projection single-valuedness on a neighborhood when `C` is weakly closed locally. Finite-dimensional real coefficient spaces meet that qualification. No global convexity, prescribed modulus of continuity, or uniqueness assumption about a selected slice is added. The paper's Proposition 3.5 proof explains the extra clause through continuity of unique projections for a weakly closed set.

Apply `(a)⇔(k)` to closed `S`. Failure of prox-regularity implies that every neighborhood of `p₀` contains an input whose projection is not single-valued. Finite-dimensional closedness already supplies nonempty projection sets, so this means **at least two distinct attained global minimizers**, rather than zero minimizers. A feasible input cannot be such a point, because its distance-zero minimizer is itself alone.

All nearest points also approach `p₀`: for any projection `s` of `q`,

\[
\|s-p_0\|\le\|s-q\|+\|q-p_0\|
\le2\|q-p_0\|.
\]

No specific input `q`, or specific pair of minimizers, is supplied by this existence proof. No such explicit identification is required for the claimed existential theorem.

## 6. Every fixed positive-definite coefficient metric

For a fixed symmetric positive-definite matrix `G`, use `⟨u,w⟩_G=uᵀGw`. The support covector (3) is represented by the genuine metric normal `G⁻¹n_t`, and

\[
\langle G^{-1}n_t,p_0-p_t\rangle_G=t^3/2.
\]

Its metric squared distance is at most `λ_max(G)(2t⁴+t⁶)`. The support quotient therefore still diverges. The metric normals remain bounded and converge, and the space with this fixed inner product is still finite dimensional and Hilbert. PRT applies directly in that metric.

This establishes the quantified claim **for each fixed** positive-definite metric. It does not infer uniqueness invariance merely from equivalence of arbitrary norms. A metric depending degenerately on `t` and root-matching distances are outside the claim.

## 7. Full exact-degree ambient space: hypotheses and localization

For `l z²+a z+b`, with `l` near 1, root differentiation at `λ=-it` yields

\[
d\lambda=-\frac{\lambda^2\,dl+\lambda\,da+db}{t^2-2it}.
\]

Taking the real part in the six independent real directions verifies the frozen full support covector

\[
N_t=(t^3/2,-t^2,-t,-t^2/2,-t/2,1). \tag{5}
\]

In particular, these leading-coefficient components were not guessed from a monic slice. The active root remains simple and dominant at fixed `t`, so (5) is an outward proximal normal of the local full stable boundary. The two leading-coordinate components of `p₀-p_t` vanish; the support and norm in (4) remain unchanged.

The full exact-degree stable set is not globally closed in the six-dimensional space because `l=0` is excluded. Consequently PRT must **not** be applied to that set globally without localization. The frozen proof's repair is valid. In the chosen coefficient metric, select a radius `R>0` so small that the closed ball `B_R(p₀)` contains no vector with `l=0`. The stable subset

\[
C=S_{\rm full}\cap B_R(p_0)
\]

is compact: normalization is continuous throughout the ball, and the monic stable set is closed. Eventually `p_t` and the comparison points are in the interior of the ball, so the local normals and the obstruction persist for `C`.

For `||q-p₀||<R/2`, every stable polynomial outside the ball has distance at least `R-||q-p₀||>||q-p₀||`, while the feasible competitor `p₀` has distance `||q-p₀||`. Thus the projection sets onto `C` and onto the **entire** full exact-degree stable set coincide. Compactness gives attainment; the strict estimate excludes any minimizer on the cutoff sphere. Contraposition of PRT for closed `C` now supplies the claimed arbitrarily nearby global nonuniqueness. This also ensures all these inputs themselves have nonzero leading coefficient.

This is a complete repair of nonclosedness and a full ambient argument; no normalization-map preservation of metric projections is assumed.

## 8. Epigraph set versus finite-subgradient function regularity

At `(p_t,0)`, the smooth epigraph inequality is `α(p)-r≤0`. The active-root derivative gives

\[
\nabla\alpha(p_t)=\frac{2}{t(t^2+4)}n_t,
\qquad
c_t=\frac{t(t^2+4)}2\longrightarrow0.
\]

Hence its support covector `(n_t,-c_t)` is a positive multiple of `(∇α(p_t),-1)` and converges to `(n₀,0)`. Comparing `(p_t,0)` with `(p₀,0)` preserves the numerator and denominator of (4). This directly disproves epigraph-set prox-regularity at that horizontal limiting covector. Replace `n_t` by (5) for the full-degree case; use a closed local coefficient/height cutoff if a globally closed ambient set is required. Monic `α` is continuous, so its whole epigraph is already closed.

The exact finite-subgradient definition and its epigraph formulation were separately read in [PR2010, primary full text](https://www.heldermann-verlag.de/jca/jca17/jca0849_b.pdf), printed pp. 203 and 205. Function prox-regularity relative to a finite subgradient uses a localization near that subgradient and near the function value, corresponding to the epigraph direction `(v,-1)`. Here the height coordinate tends to zero; normalizing it to `-1` makes the imaginary-constant component `1/c_t` diverge. The displayed sequence does not approach any finite `v`. It therefore cannot falsify that function property.

For an inner product mixing coefficient and height coordinates, the limiting **support covector** remains `(n₀,0)`; its representing metric normal vector may acquire a nonzero height component through `G⁻¹`. Describing it as horizontal should be understood in this covector sense, or in the standard/product metric. This is a precision note, not a gap in the obstruction or in the finite-subgradient distinction.

## 9. Falsification attempts, evidence limits, and exact remaining gap

The independent rational controls cover 2,401 root-parameter choices, including unstable roots, zero trace, repeated roots, equal frequencies, zero frequencies, and vanishing `B`. They verify the coefficient characterization and the identities in (2). Separate controls verify the monic and full root derivative normals, the simpler support obstruction, general rational secants, and non-diagonal positive-definite metric duality in dimensions 4, 5, 6, and 7. All checks use `fractions.Fraction`; no floating diagnostic is promoted to proof. Four finite threshold checks additionally test the direction of the support inequality for increasing `ρ`. The universal conclusion comes from (4) and PRT, not from finite sampling.

Adversarial hypotheses ruled out: a wrong outward sign; a missing imaginary linear-coefficient direction; a monic-slice inference in the full ambient metric; division by zero on the trace-zero boundary; nonattainment masquerading as nonuniqueness; a cutoff minimizer being mistaken for a global full-degree minimizer; norm equivalence being mistaken for projection invariance; and a horizontal epigraph normal being substituted for a finite subgradient.

**Strongest verified result:** arbitrarily close attained global nonunique nearest stable complex quadratics, monic and full exact degree, for each fixed positive-definite coefficient inner product; and failure of whole-epigraph set prox-regularity.

**Exact mathematical gap in these statements:** none found. An explicit nearest pair is not constructed, but it is not part of the existential claim.

**Exact gap to an unqualified original-target resolution:** independent source alignment must decide whether the source target demands real coefficients and/or finite-subgradient function prox-regularity. Neither variant is resolved by this construction. No priority, novelty, or later-resolution conclusion follows from this audit.

**Final checkpoint:** review verification 100% complete for this family's assigned scope; mathematics GO subject to the stated scope, overall source disposition HOLD pending source alignment.
