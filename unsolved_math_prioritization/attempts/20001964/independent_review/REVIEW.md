# Independent audit of the equivariant-integration source obstruction

**Verdict: PASS_SCOPED_GLOBAL_SMOOTHNESS_OBSTRUCTION_AND_JET_CRITERION.** No mandatory mathematical correction is required. Recommended queue disposition: **unsolved, 2/5 approaches**, with a source-specification caveat. The literal globally smooth, fixed-point-only conjunction fails; a repaired integration theory is not solved. This is an independent adversarial AI audit, not human peer review or a novelty certification.

Frozen `SOURCE_OBSTRUCTION.md` SHA-256:
`f15366c1d98912f120f43f24ca5ac6b6186c448489efe49176d0e49d29c1a66a`.

## 1. Exact source and interpretive boundary

I read and visually inspected printed p. 9 of the complete [AIM workshop report](https://aimath.org/WWN/momentmaps/momentmaps.pdf), including the continuation of Definition 6.4, Comments 6.5–6.6, Question 6.7, and the following material. The question allows a noncompact real-algebraic symplectic manifold, compact Hamiltonian torus, proper semialgebraic moment map, compact fixed set, and smooth semialgebraic parameter dependence. It does not impose compact spatial support. Its output is described as smooth on the Lie algebra.

The preceding definition explicitly takes values in the rational-function field and gives a fixed-component sum with inverse equivariant Euler classes. The adjacent comment already mentions a distributional alternative. The later hypercompact definition and pairing theorem are separate statements, not extra assumptions of Question 6.7.

The author's no-go theorem explicitly interprets the requested localization as this fixed-point-only expression on regular parameters and interprets smoothness globally. That is a defensible literal reading, but it should not be promoted into a negative answer for every intended regularized or chamberwise formulation. This interpretive boundary is correctly visible in the frozen text and supports the conservative status recommendation.

## 2. The complex-line example meets every needed hypothesis

Take M=R²=C, ω=dx∧dy and the ordinary algebraic rotation action of the real-algebraic compact group S¹. For V=−y∂x+x∂y,

    ι_Vω=−y dy−x dx=−d((x²+y²)/2).

Thus the stated moment map and sign convention are consistent. Its inverse images of compact sets are closed and bounded, hence compact; negative levels cause no problem. The fixed set consists of the origin. The action, manifold and moment map are real algebraic or polynomial as required.

The constant form α=1 is invariant, smooth, equivariantly closed, and polynomial in the parameter. It remains admissible under any ordinary semialgebraic interpretation of the form-valued parameter map. Although the source does not explicitly restate equivariant closedness, imposing it cannot exclude this example.

The equivariant Euler class of the complex normal line at zero is u after the declared normalization. Integration over this zero-dimensional fixed component evaluates the restriction to one, so the fixed-point prescription is 1/u. Changing an Euler or Lie-algebra normalization inserts a nonzero constant and cannot remove the pole.

If a globally smooth F agreed with that value for u≠0, continuity of uF(u) at zero would simultaneously give zero and one. The contradiction uses neither linearity nor an integration module axiom. It also does not confuse ordinary integration of a zero-form with localized equivariant pushforward: the latter is allowed to have negative parameter degree. This is a genuine obstruction to the stated conjunction.

## 3. Localization and compact-support compatibility

Rational localization inverts u; C∞(R) does not contain a smooth inverse of u. The obstruction is therefore already compatible with the neighboring rationalized definition, rather than refuting it. The chosen α lies in the original polynomial subalgebra, so the argument does not rely on inserting a singular input form through rationalization.

The unit form is not compactly supported in M. If a different problem restricted to compactly supported equivariantly closed polynomial forms, the example would no longer apply. The usual equivariant Thom isomorphism for an oriented representation makes the compatibility transparent: for V=Cⁿ with Euler class e(V)=c uⁿ, a compactly supported equivariant class is b(u) times its Thom class, and restriction to zero is e(V)b(u). Its fixed-point quotient is b(u), with the Euler factor canceled. This comparison uses ordinary equivariant compact-support theory; it is not an assertion that every smooth compact-support representative belongs to every semialgebraic form category.

Accordingly, the candidate neither disproves compact-support localization nor silently changes its test form into a compact-support one. Its all-form domain is the decisive distinction.

## 4. Weighted representations and the exact extension criterion

For positive integer weights w₁,…,wₙ, the moment map satisfies

    2μ(z) ≥ min(wⱼ) ||z||².

This proves properness; all weights are nonzero, so the fixed set is precisely zero. The product formula for Euler classes gives c uⁿ, where c=∏wⱼ≠0. Only the differential-degree-zero part of a form survives restriction to a point, yielding a smooth scalar a(u). The expression under review is a(u)/(c uⁿ) for u≠0.

The criterion is both necessary and sufficient:

- If it extends to F∈C∞(R), then a=c uⁿF holds on a dense set and hence everywhere. All derivatives of order less than n at zero vanish.
- If these jets vanish, Taylor's theorem with integral remainder gives

      a(u)=uⁿ/(n−1)! ∫₀¹(1−s)^(n−1) a^(n)(su) ds.

  The integral is smooth as a function of every real u, including negative u and zero. On each compact u-interval its differentiated integrands are continuous on a compact rectangle, so differentiation under the integral is justified to every order. Dividing by c provides the extension.

The extension value at zero is a^(n)(0)/(c n!), consistent with this formula. Uniqueness follows from density of the punctured line. For polynomials, the jet condition is precisely divisibility by uⁿ. There is no assumption that arbitrary smooth functions are analytic, and no unjustified replacement of flat functions by their Taylor series.

The coefficient-only forms a(u)=uⁿb(u) are valid equivariantly closed examples: the de Rham differential and contraction act trivially on their spatial degree-zero constant coefficient. Taking smooth semialgebraic b gives exactly the claimed admissible family. Semialgebraicity alone plainly does not force the jets, since a=1 is polynomial.

## 5. Boundary corrections and existing distributional theory

A contribution at infinity could cancel a pole only by changing the value prescribed by the fixed-point-only sum on nonzero parameters. A term supported only at the singular parameter cannot alter those punctured-line values, and cannot make their restriction the restriction of a globally smooth function. A chamberwise function or a distribution can retain the pole behavior; those are different output categories, not contradictions to the no-go statement.

I read the definitions and exact statements of [Libine's complete paper](https://arxiv.org/abs/math/0411638), especially Definition 9 and Theorems 10 and 13. The hypotheses include properness, polynomial equivariant forms and the additional no-zeroes-at-infinity condition. Theorem 10 describes the restriction of a distribution involving the equivariant symplectic exponential to the strongly regular open set. Theorem 13, after the scaling regularization, is explicitly a distribution on that open set with the fixed-point expression there. It does not assert a smooth extension across the excluded hyperplanes. The frozen artifact accurately credits this construction and does not claim to reprove its analytic estimates or refute its results.

For the circle representation, the relevant strongly regular set is R\{0}. Thus the singularity at issue is exactly outside the set on which the cited theorem gives the displayed function. No illicit extension across that set is available from the theorem.

## 6. Exact controls and reproducibility

The author program was replayed beside the frozen snapshot. All **24,965 author assertions** passed and the receipt reproduced byte-identically (SHA-256 `834f7d6a2428f44461c92f5b52dc14eefc342284b91e86ad401c46be158ea01a`).

The independently written checker passed **114,137 exact assertions**, including:

- direct integration of the expanded Taylor kernel for 294 monomial remainders, rather than substituting a Beta-function identity;
- 15,625 polynomial coefficient vectors with seven independent jet-order tests each;
- 340 positive weighted representations, checking the contraction sign, coercivity inequality and Euler factors;
- Thom-factor cancellation and rational smooth semialgebraic examples with both passing and failing jets.

These are finite formula diagnostics. Continuity proves the global no-go, and the written Taylor argument proves the all-smooth criterion. No numerical regularization or full analytic localization theorem is certified by these tests.

## 7. Final disposition

The source-level global-smoothness incompatibility and the weighted one-variable jet criterion both pass. Keep the original broad integration program unresolved and retain two used approaches. No repaired theory with distributions, regular-parameter functions, chosen renormalization, restricted support, or boundary corrections is constructed here. No novelty claim is supported by this audit.
