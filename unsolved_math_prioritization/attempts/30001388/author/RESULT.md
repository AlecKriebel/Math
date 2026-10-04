# Escaping boundary points of Baker domains: five-route investigation

**Target:** 30001388 / OWR-4137-004. **Status: unsolved.**

No proof or counterexample to the general question is obtained. The results below are elementary reductions, checks on known examples, and precise obstructions to five attempted methods. No novelty or first-resolution claim is made. In particular, the rational model used below is not a counterexample to the problem.

## 1. Source-correct target and literature boundary

Let f be a **transcendental entire** function, let

I(f) = {z in C : f^n(z) tends to infinity as n tends to infinity},

and let U be a periodic Fatou component contained in I(f). Must the **finite-plane boundary** satisfy

∂U ∩ I(f) ≠ ∅?

The entire/transcendental hypotheses come from the context of Rippon's contribution to the original Oberwolfach report, printed p. 2954 [OWR]. The catalogue's one-line statement omits that context. Infinity itself is not an admissible answer. Nor is merely proving an unbounded orbit, or an escaping point somewhere in the Julia set.

The 2025 Bergweiler–Rempe survey explicitly records this target as Question 6.40 [BR, pp. 59–61]. Positive results cover univalent domains, and finite-degree hyperbolic or simply parabolic domains. In the finite-degree doubly parabolic case the escaping boundary set has harmonic measure zero, which says nothing by itself about emptiness. The 2026 Jové–Pawelec work [JP] studies finer recurrence and additional expanding-domain hypotheses; it does not assert a universal answer to this question. This is a bounded source review as of 4 October 2026, not a proof that no other resolution exists.

### Period reduction

For every entire f and integer p ≥ 1, I(f^p) = I(f). One inclusion is immediate. For the other, suppose f^{pn}(z) tends to infinity but the whole orbit does not. Some residue j with 1 ≤ j < p then has a bounded subsequence w_k = f^{pn_k+j}(z). Pass to a convergent subsequence. Continuity of the entire function f^{p-j} makes f^{p-j}(w_k) bounded, contradicting f^{p(n_k+1)}(z) → infinity. Thus it suffices to consider an invariant Baker domain for F = f^p. This argument uses continuity at finite points, not the false assertion that an entire function is continuous at infinity.

For such F, F(∂U) ⊆ ∂U: approximate a boundary point by points of U, use F(U) ⊆ U, and use the forward invariance of the Julia set to exclude the interior of U.

## 2. Attempt 1: harmonic measure and orbit-growth estimates

**Mechanism.** Push Lebesgue measure on the unit circle to harmonic measure using a Riemann map; try to show a positive-measure collection of radial boundary orbits escapes.

The known positive tools are genuinely useful but do not cover the target. Rippon–Stallard [RS, Theorem 1.1] handle all univalent Baker domains. Barański–Fagella–Jarque–Karpińska [BFJK, Theorem A] handle hyperbolic/simply parabolic domains whose associated inner function has a nonsingular Denjoy–Wolff point, including finite degree. Their Remark 1.1 also gives a sufficient interior-growth condition

Σ_n |F^n(z)|^{-1/2} < infinity.

An explicit obstruction to applying that growth test universally is the known doubly parabolic example f(z) = z + exp(-z). Start at x_0 = 0 on the real axis, and put x_{n+1} = x_n + exp(-x_n), y_n = exp(x_n). Then y_0 = 1 and

y_{n+1} = y_n exp(1/y_n).

For 0 ≤ t ≤ 1, 1+t ≤ exp(t) ≤ 1+(e-1)t. Induction gives

1+n ≤ y_n ≤ 1+(e-1)n,

hence

log(n+1) ≤ x_n ≤ log(1+(e-1)n).

Consequently the sufficient reciprocal-square-root series diverges (discard its initial zero denominator). Every fixed iterate f^p still has logarithmic growth along this orbit, so passing to a period does not repair the test. This does not claim that the sufficient condition is necessary.

More fundamentally, [BFJK, Theorem B] says the escaping boundary set has measure zero in the finite-degree doubly parabolic case, while [FJ] supplies such a domain with escaping boundary points. Therefore no extension that tries to prove positive harmonic measure for **every** Baker domain can work.

**Outcome:** exact growth obstruction and an identified invalid strengthening. **Gap:** construct at least one point in a measure-zero exceptional boundary set, or handle singular Denjoy–Wolff points by a different argument. Zero measure cannot be converted into emptiness.

## 3. Attempt 2: prime ends and the associated inner function

**Mechanism.** Conjugate F on U to g = φ^{-1}Fφ on the disk and pull boundary orbits through φ. The desk-review suggestion of escaping crosscuts is a version of this route.

Here is a sharp control showing why the internal map is not enough. Define

T(w) = w - 1/w,
C(w) = (w-i)/(w+i),
C^{-1}(ζ) = i(1+ζ)/(1-ζ).

A direct rational-function calculation gives

C(T(C^{-1}(ζ))) = (3ζ²+1)/(ζ²+3) =: g(ζ).

The same g is the associated inner function for the Baker domain U of the **entire** map f(z) = z + exp(-z), with the normalization in [FJ, §6]. Nevertheless, their finite boundary-escape behavior differs.

### 3.1 The rational model has no escaping finite real orbit

T maps the upper half-plane H into itself, since

Im T(w) = Im(w)(1 + 1/|w|²) > 0.

For w = iy with y > 0, T(iy) = i(y+1/y). In particular, the orbit from i tends to infinity: its squared heights increase by at least 2 at each step. Schwarz–Pick then implies that every orbit in H tends to infinity, since its hyperbolic distance to that orbit stays bounded; in H a bounded hyperbolic distance bounds the ratio of imaginary parts above and below by positive constants.

But no real orbit defined at every time escapes. If |x_n| tended to infinity, then eventually |x_n| > 1, and thereafter

|x_{n+1}| = |x_n| - 1/|x_n| < |x_n|,

contradicting divergence to infinity. Orbits that reach the pole 0 are excluded by the requirement that all iterates be defined. This also shows that a boundary orbit of g cannot converge to 1 without eventually hitting 1: otherwise Cayley conjugacy would give a real T-orbit tending to infinity.

T is rational and has a finite pole. Its domain is **not** a transcendental-entire Baker domain. The calculation is a control against a proof using only disk dynamics and interior escape.

### 3.2 The entire realization has escaping boundary points

For the above entire f, [FJ, Theorems A and C] proves the existence of escaping boundary hairs and proves that escaping boundary points are inaccessible from U. Thus the same inner map accompanies genuine finite boundary escape once the conformal embedding changes. Looking only at radial boundary points converging to the Denjoy–Wolff point discards the points needed in this example.

The inference φ(g^n(ζ)) → infinity from g^n(ζ) → 1 would itself require boundary control on φ; radial convergence at 1 alone does not supply convergence along an arbitrary boundary sequence. Conversely, a physical orbit escaping to infinity need not approach the dynamical prime end.

**Outcome:** an exact same-inner-map control, not merely an abstract continuity objection. **Gap:** a theorem about the conformal embedding and its prime-end impressions, including inaccessible points, rather than another theorem about g alone.

## 4. Attempt 3: connectedness, fast escape and boundary crossing

**Mechanism.** Use global escaping continua and their accumulation on J(f) to force a crossing of ∂U.

There is a useful exact topological reformulation. Let X = I(f), and let C_U be the connected component of X containing U. Then

∂U ∩ X ≠ ∅  if and only if  C_U ≠ U.

Indeed, if x ∈ ∂U ∩ X, then U ∪ {x} is connected and belongs to X. Conversely, if ∂U ∩ X is empty, U is both open and closed in the subspace X: its relative closure is cl(U) ∩ X = U. Every connected subset of X meeting U is therefore contained in U. Since U is connected, C_U = U.

Thus connectedness of I(f) is sufficient, because I(f) also contains Julia points and so is strictly larger than U. A connected escaping subset meeting U and a point outside U would likewise suffice. However, simply knowing that all components are unbounded would not help: U is already unbounded. Connectedness after adding infinity is also insufficient; the desired crossing has to be finite.

### A purely topological negative control

In the plane, let

U_0 = {z : 0 < Re z < 1},
X_0 = U_0 ∪ ⋃_{m≥1}{Re z = -1/m} ∪ ⋃_{m≥1}{Re z = 1+1/m},
J_0 = ∂X_0.

Then J_0 consists of the displayed vertical lines and the two limiting lines Re z = 0,1. Every component of X_0 is unbounded; X_0 ∩ J_0 is dense in J_0; and X_0 ∪ {infinity} is connected on the sphere, since each constituent together with infinity is connected and they share infinity. Yet ∂U_0 ∩ X_0 is empty and U_0 is a component of X_0. To identify the components, apply the continuous projection Re: a connected subset of X_0 has connected image inside (0,1) ∪ {-1/m,1+1/m}; it cannot span a gap in that real set.

This is not an entire-function construction and makes no claim to satisfy the analytic restrictions on Baker boundaries. It disproves the claimed implication from precisely the listed topological inputs. Known fast-escaping-set results supply global components, not the missing finite intersection with the specified U.

**Outcome:** exact equivalence plus a control against two tempting global shortcuts. **Gap:** prove that a particular Baker domain cannot itself be a component of I(f); asserting that is equivalent to the question, not progress beyond it.

## 5. Attempt 4: inverse branches and compact orbit selection

**Mechanism.** Pull back large boundary sets and pass from finite orbit segments to an infinite escaping orbit.

The following standard compactness criterion makes the needed certificate explicit.

**Lemma.** Let B be a closed subset of C, let F be continuous, and let K_n ⊆ B be nonempty compact sets for n ≥ 0. Suppose

F(K_n) ⊇ K_{n+1},
and min{|z| : z ∈ K_n} tends to infinity.

Then some x ∈ K_0 has F^n(x) ∈ K_n for every n and hence escapes.

**Proof.** For N ≥ 0 define

E_N = {x ∈ K_0 : F^j(x) ∈ K_j for 0 ≤ j ≤ N}.

Each E_N is closed in the fixed compact K_0. It is nonempty: choose a point of K_N and successively lift it through K_{N-1}, …, K_0 using the covering assumptions. The E_N are nested; compactness gives a point in their intersection. The radial condition gives escape. □

For the target, B = ∂U would give a complete affirmative proof **if those boundary sets and coverings could be produced for arbitrary U**. Merely using open neighborhoods of Julia points does not do so: a Julia blowing-up argument can find preimages in the neighborhood without placing them on this particular Fatou boundary. Likewise, inverse-branch contraction near typical orbits is not the required forward covering chain on boundary sets tending to infinity. [JP] has additional expansion and boundary-preservation hypotheses; none is proved here for arbitrary Baker domains.

### Finite-time controls

The rational T from §3 has arbitrarily long real orbit segments outside any prescribed [-R,R], despite having no escaping real orbit. For R ≥ 1 and integer N ≥ 1, start at x_0 = R+N+2. While x_j > 1, the drop 1/x_j is less than 1, so induction gives x_j > R+N+2-j > R for 0 ≤ j ≤ N. The initial point depends on N and leaves every fixed compact set as N grows.

The nested closed sets [N,infinity) furnish the corresponding elementary compactness warning: they are all nonempty but have empty intersection in R. In the sphere the remaining point is infinity, which is not an answer to the target.

**Outcome:** a rigorous sufficient certificate and a dynamical negative control for finite orbit tests. **Gap:** nonempty pullbacks anchored in one finite compact boundary set, with verified escape at every future time, not only at selected times or for varying initial points.

## 6. Attempt 5: explicit tracts and a counterexample transplantation

**Mechanism A: generalize a tract construction.** For f(z) = z + exp(-z), the lines Im z = ±π are invariant, and on each line

x_{n+1} = x_n - exp(-x_n).

This strictly decreases. It cannot have a finite limit L, since continuity would give L = L-exp(-L). Hence x_n → -infinity. Starting at x_0 = 0, the sharper bound x_n ≤ -n follows by induction, because exp(-x_n) ≥ 1. The boundary membership of these lines is supplied by [FJ, immediately before Proposition 4.4], not by the recurrence alone. This is a check of a known affirmative example, not a new result.

For a deformation f_a(z) = z+a+exp(-z), a > 0, the same invariant lines have real recurrence x ↦ x+a-exp(-x). Points below the fixed threshold x_* = -log a decrease forever and tend to -infinity: if a finite limit existed it would have to equal x_*, larger than the initial value. This certifies escape only; it does **not** establish that those points lie on the boundary of any particular Baker domain. That missing boundary identification is exactly what a naive parameter continuation would need to prove.

**Mechanism B: transplant the nonescaping Boole boundary.** The rational control has the desired interior-versus-boundary behavior, so one might try to approximate T by an entire function while preserving it. A basic residue obstruction defeats uniform approximation around its pole. If h is entire and r > 0, then

∮_{|z|=r}(h(z)-T(z)) dz = 2πi,

so

max_{|z|=r}|h(z)-T(z)| ≥ 1/r.

In particular no sequence of entire functions converges uniformly to T on any circle surrounding zero. Approximation on a one-sided absorbing region might avoid this obstruction, but it gives no control of all finite boundary points or their forward orbits. No entire transplantation, surgery, or new counterexample has been constructed.

**Outcome:** exact escaping tracts in the known model, precise limitation of the deformation, and a residue barrier to a direct rational-to-entire transplantation. **Gap:** simultaneously preserve a transcendental-entire Baker domain and exclude escape at every finite point of its actual boundary, including inaccessible points.

## 7. Final assessment and reproducibility

All five substantive approach families were completed without a general resolution. The strongest deliverable is a source-checked delineation of the boundary-embedding gap, together with the same-inner-function control, the component reformulation, the compact-covering criterion, and exact algebraic/finite-prefix controls. These deductions do not establish a new theorem about all Baker domains.

The accompanying standard-library script checks rational-function identities, exact finite Boole prefixes, the imaginary-orbit squared-height bounds, the scalar inequalities used in the tract argument, and residue coefficients. It deliberately does not claim to numerically certify Julia-set membership, harmonic measure, a Fatou component, or any infinite escaping orbit. Those statements are either proved above or explicitly credited to the sources.

Queue recommendation: **unsolved, 5/5**, with no claim of full resolution. New work should require a materially new boundary-preserving mechanism; merely rephrasing the component equivalence or producing longer finite simulations does not reopen a successful route.

## References

[OWR] Mini-Workshop: The Escaping Set in Transcendental Dynamics, Oberwolfach Reports 54/2009, pp. 2927–2964, especially p. 2954. https://doi.org/10.4171/owr/2009/54

[RS] P. J. Rippon and G. M. Stallard, Boundaries of univalent Baker domains, Journal d'Analyse Mathématique 134 (2018), 801–810. Author preprint: https://arxiv.org/abs/1411.6999

[BFJK] K. Barański, N. Fagella, X. Jarque and B. Karpińska, Escaping points in the boundaries of Baker domains, Journal d'Analyse Mathématique 137 (2019), 679–706. Author manuscript: https://diposit.ub.edu/server/api/core/bitstreams/b9cb8958-7aa2-46f8-ab85-ec930c7869da/content

[FJ] N. Fagella and A. Jové, A model for boundary dynamics of Baker domains, Mathematische Zeitschrift 303 (2023), article 95. https://doi.org/10.1007/s00209-023-03245-2 ; https://arxiv.org/abs/2202.04969

[J] A. Jové, Boundaries of hyperbolic and simply parabolic Baker domains (2024 preprint). https://arxiv.org/abs/2410.19726

[BR] W. Bergweiler and L. Rempe, The escaping set in transcendental dynamics (2025), §6.6, especially Questions 6.38–6.43. https://doi.org/10.1365/s13291-025-00300-1 ; https://arxiv.org/abs/2507.11370

[JP] A. Jové and Ł. Pawelec, Boundaries of Baker domains of entire functions. A finer approach (2026 preprint), Theorems A–D and §5. https://arxiv.org/abs/2605.05184
