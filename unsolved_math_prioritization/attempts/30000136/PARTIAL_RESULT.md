# Nonclosed one-forms: constructive sufficient conditions and the remaining global gap

Problem30000136 / OWR-761-003. **Unsolved for the intended connected-manifold conjecture.** This package gives a sufficient criterion, explicit torus constructions, and two source/quantifier cautions. It does not claim to settle the connected case by exploiting an omitted connectedness convention.

## Exact source and conventions

[Oberwolfach Report47/2004, printed p.2500](https://ems.press/content/serial-article-files/45966) states the question for a closed manifold M with χ(M)=0 and a one-form α satisfying dα≠0: find a function f with α+df nowhere zero. There is no bound on the norm of df and no approximation topology is specified. The requested operation is addition of an exact form, of arbitrary size.

[Tabachnikov, Existence and nonexistence of skew branes, Conjecture3.2](https://pure.mpg.de/rest/items/item_3123074_1/component/file_3123075/content) explicitly says “non-closed,” so the condition means dα is not identically zero. It does not mean dα is pointwise nonzero. The subsequent dimension-one remark uses a nonzero period on a circle, which instead concerns a closed but nonexact form; all one-forms in dimension one are closed. We preserve this mismatch rather than silently redefining the target. The skew-brane application uses connected odd-dimensional real projective space.

There is also a connectedness issue. If disconnected manifolds are allowed and nonclosedness is only required somewhere, take M=T²⊔T² and α=sin(x)dy on the first component and α=0 on the second. Then χ(M)=0 and dα is not identically zero, but any α+df has a zero at an extremum of f on the second component. Thus the unqualified disconnected version is false. This elementary convention counterexample does not answer the intended connected conjecture and is not a novelty claim. Requiring nonclosedness separately on every component removes this particular objection.

## 1. A flow-compatible sufficient condition

Fix a Riemannian metric on a compact smooth manifold M. Let F be a smooth real function and V a smooth vector field such that dF(V)=0 everywhere. Suppose α(V) is nonzero at every point of Crit(F).

**Proposition1.** For every sufficiently large positive λ, α+λdF has no zeros. In particular f=λF solves the desired equation for any α,F,V with these properties.

Proof. Crit(F) is compact. Choose an open neighborhood N of it on which |α(V)| is bounded below by a positive constant. On N,

(α+λdF)(V)=α(V)≠0,

so the one-form does not vanish, for any λ. The compact complement M\N is disjoint from Crit(F); if it is nonempty, δ=min_{M\N}|dF| is positive. Put A=max_M|α|. If λ>A/δ, then outside N

|α+λdF|≥λ|dF|−|α|≥λδ−A>0.

The two regions cover M. If the complement is empty, the evaluation argument already suffices. ∎

This criterion is elementary and constructive after F,V are supplied. The unproved global step would be to produce such auxiliary data from only χ(M)=0 and dα not identically zero. Euler characteristic zero supplies a nowhere-zero vector field, but does not supply a first integral F or the required sign/nonvanishing of α(V) at its critical set.

## 2. Every nonzero shear form on a two-torus admits an exact correction

Write T²=(R/2πZ)² with coordinates x,y. Let α=a(x)dy for a smooth periodic function a not identically zero. It may vanish on large sets; no simple-zero assumption is needed. If a is nonconstant, α is a nonclosed form within the original target.

Choose a nonnegative smooth periodic bump b supported in an open interval I where a is nowhere zero, with B=∫₀^{2π}b(x)dx>0. Define

g(x)=1−(2π/B)b(x).

Its integral over the circle is zero, so g=F' for a smooth periodic function F. The form

α+dF=g(x)dx+a(x)dy

has no zeros: outside I, g=1; inside I, a≠0. This construction includes forms with many or nonisolated zeros. It is a special family, not a reduction of arbitrary one-forms to shear form by a coordinate change.

More generally, on a product S¹×N, Proposition1 applies with F depending only on the circle coordinate if a smooth vertical vector field V has α(V) nowhere zero over all critical fibers of F. The criterion does not assume every χ=0 manifold fibers over S¹, nor that α admits such a vertical field.

## 3. An exact example separates arbitrary correction from small perturbation

On the same two-torus let

α=sin(x)dx+[sin(y)+1−cos(x)]dy.

Then dα=sin(x)dx∧dy, so α is nonclosed. Define

f=cos(x)+cos(y)+sin(x).

Direct differentiation gives

α+df=cos(x)dx+[1−cos(x)]dy.

In the flat metric its squared norm is

cos²(x)+(1−cos(x))²=2(cos(x)−1/2)²+1/2≥1/2.

Thus this is an explicit connected example with a rigorous positive lower bound and an exact correction.

At (0,0), the coefficient map of the original α has Jacobian the identity, so its isolated zero has index+1. Choose a sufficiently small coordinate disk D containing no other zero and with α nonzero on ∂D. Let m=min_{∂D}|α|>0. Any continuous perturbation η with sup_{∂D}|η|<m leaves the boundary coefficient map homotopic to that of α through nonzero maps. Its degree is still1, so α+η must vanish somewhere in D. This holds in particular for sufficiently C⁰-small exact perturbations η=df.

Accordingly, demanding arbitrarily small correction would produce a genuinely different and false assertion. The original question has no such requirement; the explicit f above is allowed.

## Exact unresolved step

The general connected case still needs a global method for eliminating all zeros while keeping the exterior derivative fixed and changing α only by an exact form, or a connected counterexample. Proposition1 transfers this task to extra dynamical/critical-set data that has not been constructed in general. The torus calculation is not a normal form for arbitrary α. Ordinary vector-field zero cancellation alone does not preserve the exact-form constraint.

Three approach families were examined: global flow-compatible correction, direct torus construction, and local degree/smallness obstruction. The last excludes only an unrequested strengthening. Proposed status: unsolved,3/5, with the disconnected literal caveat retained. Source/special-case completion100%; full intended connected target completion0%. No novelty or human peer review claim. Runtime inherited; exact model identifier not exposed; no model/reasoning switch made.
