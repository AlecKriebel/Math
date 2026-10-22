# Gradient-constrained Ginzburg–Landau minimizers

Problem 30005994 / OWR-14298587-009, queue rank 959.

**Disposition: UNSOLVED for the original general-potential question, after five substantive approaches.** A very recent, credited preprint resolves the standard quartic-potential case in every dimension. This packet does not claim a new solution, a counterexample to the original problem, or priority for any partial result. It is an AI-assisted mathematical report, awaiting independent review.

## 1. Scope and the change in the literature

Let B be the unit ball in R^N. The original report fixes

G_{ε,W}(u) = ∫_B [ |∇u|²/2 + W(1−|u|²)/(2ε²) ] dx,

where W:(−∞,1]→[0,∞) is C¹ and convex, W(0)=0, and W(t)>0 for t≠0. Its Question 2 uses this same functional, not only the customary example W(t)=t²/2. The admissible set is

V = { ∇φ : φ∈H²(B), Tr(∇φ)=Id }.

The question asks whether U(x)=f(|x|)x/|x| is the unique minimizer for every ε>0, in dimensions 2≤N≤6. Here f is the regular radial profile, with f(0)=0, f(1)=1, 0<f<1 and

−f''−(N−1)f'/r+(N−1)f/r² = ε⁻² W'(1−f²)f.

The exact setup and question were checked on printed pages 2133–2136 of [the official OWR report](https://ems.press/content/serial-article-files/50045), including visual inspection of pages 2133 and 2136. Omitting W from the catalogue's cleaned sentence must not remove these hypotheses.

[Ignat–Nahon–Nguyen, Theorem 1](https://arxiv.org/html/2310.11384v1) establishes the gradient-field result for N≥4 under C² convex-potential hypotheses; the journal version appeared in 2025, [DOI 10.1007/s00205-025-02082-3](https://doi.org/10.1007/s00205-025-02082-3). The OWR theorem is stated in its C¹ setup; the explicit C² hypothesis in the full paper is recorded rather than silently erased. This report does not independently settle that regularity distinction.

A material update is [Ignat–Nguyen, arXiv:2609.35398v1, Theorem 1.1](https://arxiv.org/html/2609.35398v1), submitted 28 September 2026. It establishes uniqueness in the entire H¹ class with trace Id, for every N≥2 and ε>0, **for W(t)=t²/2**. The two-dimensional precursor is [Chen–Liu–Wei–Yang, arXiv:2608.15957v1, Theorem 1.1](https://arxiv.org/html/2608.15957v1), submitted 16 August 2026. These are preprints in the records inspected on 7 October 2026; no journal acceptance or independent verification of their complete proofs is claimed here.

The inclusion V⊂{u∈H¹(B;R^N):Tr(u)=Id} and the identity

Φ(r)=∫_0^r f(s)ds,  ∇Φ=U

transfer the newer theorem immediately to the standard gradient-field question. Regularity at the origin follows from f(r)=O(r); the known regular vortex has Φ∈H²(B). Equality among gradient fields is equality of vector fields; potentials differ only by an additive constant. This is a corollary of other authors' theorem, not an original resolution.

The general W question in N=2,3 is not answered by that quartic theorem. The five approaches below concern this remaining general-potential scope. They are mathematical arguments, not five source searches or packaging steps.

## 2. Common comparison identity

Write a(r)=ε⁻²W'(1−f(r)²), v=u−U∈H¹_0(B;R^N). Consider finite-energy competitors; infinite energy is harmless. Convexity and the weak equation for U give

G_{ε,W}(U+v)−G_{ε,W}(U) ≥ F(v)/2,

F(v)=∫_B (|∇v|²−a(r)|v|²) dx.                                      (2.1)

Indeed, put q=2U·v+|v|² and t=1−|U|². Convexity gives W(t−q)−W(t)≥−W'(t)q. The terms linear in v cancel against ∫∇U:∇v=∫aU·v. Only C¹ convexity is needed. This familiar comparison method is credited to the work cited above; the restricted estimates below are proved explicitly.

## 3. Approach 1: global semiconvexity and an explicit parameter range

**Aim.** Prove the general assertion by controlling the negative part of (2.1) uniformly.

Set M=W'(1). Convexity, W'(0)=0, and strict positivity away from zero imply M>0. Since 0≤1−f²≤1, we have 0≤a≤M/ε². Let λ_D>0 be the first scalar Dirichlet eigenvalue of −Δ on B. Applying its Rayleigh inequality componentwise gives

F(v) ≥ (λ_D−M/ε²)∫_B|v|².

Consequently, for **ε²>M/λ_D**, U is the unique minimizer even in the full vector H¹ boundary class. There is no gradient-specific assumption in this conclusion. An elementary sufficient bound is ε>2√M/π: extension by zero to (−1,1)^N and the one-dimensional Dirichlet inequality in one coordinate give λ_D≥π²/4.

This proves a complete large-parameter subcase for every source-admissible W. The endpoint ε²=M/λ_D is not claimed by this estimate.

**Why this does not close the target.** The bound deteriorates as ε↓0. It gives no lower bound for F in the unresolved parameter range, and it cannot distinguish a genuinely lower-energy competitor from a negative direction of the auxiliary F. The latter is not the full second variation.

## 4. Approach 2: remove all angular means by a ground-state transform

**Aim.** Exploit the gradient constraint spectrally instead of discarding the radial structure of a.

**Proposition.** In every N≥2 and for every source-admissible W and ε>0, U is the unique minimizer among admissible vector fields u such that the spherical average of u(rθ) is zero for almost every r. In particular this covers all gradient competitors whose scalar potential has no degree-one spherical harmonic.

**Proof.** Initially take v smooth, compactly supported away from 0, and with zero spherical average. Put z=v/f. The radial ODE yields

−Δf−af=−(N−1)f/r².

Integration by parts gives the exact identity

F(v)=∫_B f²{ |∂_r z|² + r⁻²[|∇_S z|²−(N−1)|z|²] } dx.              (4.1)

For each r, z has zero mean. The spherical Poincaré inequality, applied to each component, bounds its angular Dirichlet energy below by (N−1) times its L² norm. Thus

F(v)≥∫_B f²|∂_r(v/f)|² dx≥0.                                      (4.2)

For arbitrary H¹_0 zero-mean v, first approximate in H¹ by compactly supported smooth fields, then subtract their spherical averages. This angular projection is bounded in H¹. Radial cutoffs removing the origin preserve the zero-mean condition; a point has zero H¹ capacity for N≥2, using logarithmic cutoffs in N=2. The resulting approximants converge in H¹. Since a is bounded, F is continuous in H¹. On every annulus f is positive and smooth enough, and lower semicontinuity passes (4.2) to the limit.

If G(U+v)=G(U), (2.1) and (4.2) imply ∂_r(v/f)=0 on every annulus. Hence v(rθ)=f(r)c(θ). Its zero boundary trace and f(1)=1 give c=0. This proves uniqueness.

For the last assertion define A(r)=average_{S^{N−1}} φ(rθ)θ. Spherical integration by parts gives

average_{S^{N−1}} ∇φ(rθ)=A'(r)+(N−1)A(r)/r.                         (4.3)

Thus A=0 implies the required zero mean. This includes radial potentials and all even potentials φ(−x)=φ(x), and is a direct classical harmonic/ground-state argument, with no novelty claim. ∎

**Actual remaining mode.** The boundary data do not force A=0. For example,

ψ(x)=x₁(1−|x|²)²

has ψ=0 and ∇ψ=0 on ∂B, but its degree-one component is nonzero. Its spherical gradient mean is

m(r)=[(N−(N+4)r²)(1−r²)/N] e₁,

which is not identically zero. Therefore adding ψ to Φ is admissible and escapes this proposition. A proof must control these degree-one scalar modes and their nonlinear interactions; merely citing the gradient constraint is insufficient.

## 5. Approach 3: parity pairing and the failure of local-to-global inference

**Aim.** Treat the missing odd scalar potentials, whose gradients are even, by pairing antipodal points. This avoids the cubic obstruction for a quadratic W, but not for a general convex W.

Suppose v(−x)=v(x). Since U is odd, at x and −x set

a=1−|U|², b=|v|², c=2U·v.

The paired potential change is

[W(a−b−c)+W(a−b+c)]/2−W(a).                                      (5.1)

For W(t)=t²/2 it is exactly −ab+b²/2+c²/2. Equivalently, with

Q(v)=F(v)+2ε⁻²∫(U·v)²,

G(U+tv)−G(U)=t²Q(v)/2+t⁴(4ε²)⁻¹∫|v|⁴.

The known local-stability theorem for this standard model supplies Q≥0; see [Ignat–Nguyen, DOI 10.4171/AIHPC/84](https://ems.press/journals/aihpc/articles/9817540). This proves strict increase at every nonzero amplitude for an even vector perturbation. It is now subsumed by the newer full quartic theorem, but the calculation identifies precisely what must be generalized.

For a C² potential, the tempting replacement is the pointwise inequality

(5.1) ≥ −W'(a)b + W''(a)c²/2.                                    (5.2)

If true, it would promote the second-variation comparison to a finite-amplitude comparison on this parity class. **It is false even for a smooth, source-admissible potential.** Choose W(t)=t⁴, a=1/2, b=1/10 and c²=1/10. The left side minus the right side of (5.2) is exactly

−309/10000.

These are geometrically feasible pointwise data: |U|²=1/2, and c²≤4|U|²b=1/5. For instance in R² take U=(1/√2,0), v=(1/√20,1/√20). All W arguments are ≤1. The calculation is rational after eliminating c².

This disproves only the attempted pointwise lower bound. It is not a lower-energy field with the prescribed boundary, and not a counterexample to the minimizer question. Convexity does give (5.1)≥W(a−b)−W(a), but that only recovers the inadequate auxiliary F after linearization. A new integrated bound using the PDE and the gradient constraint is still required.

## 6. Approach 4: comparison with a supporting quadratic potential

**Aim.** Transfer the September 2026 theorem to a genuinely larger class of W by domination, rather than assume its quartic proof applies unchanged.

**Proposition (credited-theorem corollary).** Let c>0. Suppose W satisfies the source hypotheses and

W(t)=ct²/2 for 0≤t≤1,    W(t)≥ct²/2 for t<0.                       (6.1)

Then in every N≥2 and for every ε>0 the regular radial vortex is the unique minimizer of G_{ε,W} in the full H¹ boundary class, hence in V.

**Proof.** Put δ=ε/√c. For every competitor u,

G_{ε,W}(u)≥G_{δ,t²/2}(u).

Let U_δ be the standard radial vortex. Since |U_δ|≤1, (6.1) gives equality of these two energies at U_δ. Moreover W'(1−|U_δ|²)=c(1−|U_δ|²), so U_δ is the radial profile for W and ε. Theorem 1.1 of [Ignat–Nguyen](https://arxiv.org/html/2609.35398v1) now yields

G_{ε,W}(u)≥G_{δ,t²/2}(u)≥G_{δ,t²/2}(U_δ)=G_{ε,W}(U_δ).

Equality forces u=U_δ by the uniqueness in that theorem. ∎

For example W(t)=ct²/2+(-t)_+⁴ meets (6.1) and is C² convex. The result covers competitors whose modulus exceeds one and does not rely on truncating a gradient field, an operation which need not preserve that constraint.

**Obstruction to universality.** Every positive c fails (6.1) for W(t)=t⁴ near t=0, and no c has equality on all [0,1]. A lower comparison potential alone is insufficient: equality at the proposed minimizer is needed. Since the radial profile runs through the whole interval of squared moduli, matching at only one value or at the boundary does not supply that equality. This approach resolves the class (6.1), not arbitrary convex W.

## 7. Approach 5: generalize the entire-vortex calibration directly

**Aim.** Preserve the finite-ball/whole-space comparison mechanism behind the new theorem while allowing a nonquadratic W.

For a convex C¹ W define its translated Bregman remainder

B_W(a;q)=W(a−q)−W(a)+W'(a)q≥0.                                   (7.1)

For a compactly supported smooth perturbation w of fθ, let q=2fθ·w+|w|². Cancellation of the linear terms gives the exact formula

G(fθ+w)−G(fθ)=F_f(w)/2+(2ε²)⁻¹∫ B_W(1−f²;q).                    (7.2)

Suppose additionally that an entire radial profile F for the same W is available, with 0<F<f on the ball, and let ρ=F/f. The analogous exact expression around Fθ, with perturbation ρw, has remainder B_W(1−F²;ρ²q). Subtracting yields a quadratic difference plus

(2ε²)⁻¹∫[B_W(1−f²;q)−B_W(1−F²;ρ²q)].                           (7.3)

For W(t)=t²/2 the integrand in brackets is (1−ρ⁴)q²/2≥0. The new paper controls the remaining weighted quadratic form using its ODE estimates. No claim is made that those estimates hold for a different W.

For arbitrary convex W, even the sign of the bracket in (7.3) does not follow from 0<F<f<1. An exact test is

W(t)=t⁴,  f²=9/10,  F²=1/2,  ρ²=5/9,  q=1/100.

The two remainders are respectively

561/100000000 and 48241/1049760000,

and their difference equals −1654369/41006250000<0. The value q can be realized at a point by w orthogonal to θ with |w|²=q in N≥2. Thus positivity of each individual Bregman remainder does not imply positivity of their difference.

This is an obstruction to a purely convexity-based transfer. It is not asserted that the selected f and F occur at the same radius for genuine t⁴ vortex profiles, or that the complete energy difference is negative. A successful extension needs additional ODE information controlling (7.3), a different comparison multiplier, or another global mechanism. Establishing that missing information remains beyond this packet.

## 8. What is and is not established

- The full original general-potential statement is not proved or refuted here. In particular arbitrary convex W in N=2,3 remains unresolved in this work. No exhaustive claim about all current literature is made.
- The standard quartic question has a recent all-dimensional preprint resolution by Ignat–Nguyen, following the planar preprint of Chen–Liu–Wei–Yang. This is credited explicitly and not counted as our solution.
- Approach 1 proves a large-ε range for all source potentials. Approach 2 proves the no-dipole competitor class for all ε. Approach 4 transfers the recent theorem to the domination class (6.1).
- Approaches 3 and 5 identify exact algebraic failures of proposed extensions. These failures neither refute the target nor certify any minimizer's instability.
- The five approaches are global spectral domination; angular ground-state comparison; nonlinear parity pairing; supporting-potential comparison; and entire-vortex Bregman calibration. Source checking and exact-test implementation are not counted as mathematical approaches.
- Earlier results and elementary methods are credited; no novelty or priority claim attaches to these partial statements.

## 9. Reproduction and review limits

Run `python -I -B verify_exact.py` with Python 3 and SymPy. The checks reproduce polynomial identities, exact negative witnesses, the gradient boundary/moment calculation, the radial ground-state identity modulo the profile ODE, and the parameter normalization. They test real algebra used in the arguments. They are not numerical evidence for the whole conjecture, a formal proof assistant verification, or a substitute for checking analytic density and trace arguments.

`SOURCE_METADATA.json` distinguishes cached-PDF verification from web-only inspections. Only the official OWR PDF has a locally verified byte count and SHA-256 in this packet's provenance. No local hash is claimed for the newer preprints. Source documents, extracted text, images, corpus contents and private repository evidence are excluded from the public packet. Independent review must assess this exact frozen version before any publication.
