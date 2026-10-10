# Five substantive approaches

Problem 30006363 / OWR-14299512-001. Investigation date: 2026-10-04 UTC.
The source/status gate was completed before treating the catalogue wording as
an open mathematical target. No full resolution was found at the gate, and
the existing theorem does not cover fields with zeroes.

## Attempt 1 — weak differential-form pullback

**Plan.** Extend the familiar smooth pullback proof across a nonsmooth
conjugacy rather than eliminate the zero set.

**Work.** Derive the generator identity at almost every differentiability
point, combine it with the area formula, and justify the weak pullback chain
rule by locally mollifying the coordinate map. Use weak Stokes with a smooth
primitive as test form. The full proof is Proposition 2.1 in PROOF.md.

**Established.** Equality of helicities for bi-Lipschitz volume- and
orientation-preserving time-conjugacies, allowing arbitrary zero sets.

**Gap.** Arbitrary homeomorphisms have no guaranteed transverse weak
derivative or one-form pullback with the needed chain rule. Differentiability
in the flow direction does not fill this gap. No general solution.

## Attempt 2 — approximate conjugacy and continuity

**Plan.** Approximate the topological conjugacy by smooth volume-preserving
maps and pass smooth invariance to the limit.

**Work.** Prove the $L^2$ helicity-continuity estimate via the Hodge right
inverse, formulate a sufficient strong-generator approximation condition,
and test the missing implication using explicit high-frequency torus shears.

**Established.** The sufficient condition is rigorous. The explicit smooth
maps and their inverses converge uniformly to identity, their conjugated
flows converge uniformly on bounded time intervals, but the generators stay
exactly distance π apart in $L^2$. Their exact primitives and zero helicity
are calculated, not assumed. See Section 3.

**Gap.** A specially controlled sequence for a general given conjugacy is
not constructed. The shear example rules out an automatic implication,
not every possible approximation strategy. No general solution.

## Attempt 3 — eliminate singularities

**Plan.** Approximate by nowhere-zero exact fields so that the 2025 theorem
applies, or cut out increasingly small singular neighborhoods.

**Work.** Construct an exact divergence-free cyclic sine field on the torus.
Its isolated zero of index $+1$ persists under all uniform perturbations of
size less than $1/2$. Compute all eight indices to check global consistency.
For isolated zeroes, use a radial primitive and exact cutoffs to obtain the
separate quantitative estimate $O(\varepsilon^{5/2})$ in $L^2$.

**Established.** The claimed uniform density of nonsingular fields is false.
The exact-cutoff estimate and resulting helicity convergence are valid.
See Section 4.

**Gap.** The cutoffs create open sets of zeroes, and independently applying
them does not preserve conjugacy. The indexed zero obstructs the naive
nonsingular replacement. No general solution.

## Attempt 4 — measure the puncture defect

**Plan.** On the regular complement of a finite zero set, compare primitives
and determine exactly what the missing boundary contribution is.

**Work.** Choose global primitives vanishing to second order at all zeroes,
derive the Stokes identity on punctured manifolds, verify integrability by
the measure-preserving change of variables, and estimate the boundary term.

**Established.** Proposition 5.1 proves equality when the conjugacy is smooth
off the finite zero set and

$$
 r^4\sup_{S_r(p)}\|Dh_x\|d(h(x),h(p))^2\to0.
$$

It also gives the exact defect formula without this growth condition. A
Hölder/derivative-power sufficient condition is explicitly derived.

**Gap.** Neither the smoothness on the punctured manifold nor vanishing of
this boundary remainder follows from arbitrary topological conjugacy. For
arbitrary zero sets this argument does not even produce the stated finite
boundary decomposition. No general solution.

## Attempt 5 — transport asymptotic linking

**Plan.** Transport closed long orbit segments by the homeomorphism and use
invariance of their linking numbers.

**Work.** Isolate a precise sufficient $o(T^2)$ averaged closing-path error
on $S^3$, prove the conditional reduction, and examine the regularity
assumption hidden in transporting short closing paths. Construct an explicit
volume-preserving rough torus shear commuting with a smooth exact field;
prove that it takes a straight short arc to one of infinite length, using a
divergent finite-partition variation lower bound.

**Established.** The conditional reduction is correct, and the regularity
obstruction is explicit. See Section 6.

**Gap.** The averaged linking-error estimate is not proved. Nonrectifiability
of some transported paths does not disprove the estimate or yield a helicity
counterexample. No general solution.

## Final outcome

Five approaches completed; the full arbitrary-homeomorphism problem with
singular fields remains unresolved in this work. The affirmative nonsingular
theorem belongs to Edtmair–Seyfaddini. The packet claims no new solution,
counterexample, or priority. The small exact-check script verifies explicit
example identities only; the analytical arguments require mathematical
review in addition to those checks.
