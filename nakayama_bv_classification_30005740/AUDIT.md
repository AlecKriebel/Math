# Independent adversarial audit: canonical BV generators for A_h

Audit date: 2026-10-21 UTC. Verdict: the classification is mathematically supported for every field k of characteristic zero and every nonzero h in k[x]. The existing ordinary Hochschild Gerstenhaber algebra admits a BV generator exactly when h is squarefree. In the repeated-factor case, there is no degree-minus-one generator at all, even without imposing square-zero. This is an independently checked proof, not a claim that a published classification was located.

## Source dependencies verified

Inspected the local full-text primary journal source, Lopes–Solotar, *Lie structure on the Hochschild cohomology of a family of subalgebras of the Weyl algebra*, J. Noncommut. Geom. 15 (2021), 1373–1407, DOI 10.4171/JNCG/439; public PDF https://ems.press/content/serial-article-files/30909 . Section 3 supplies the free bimodule resolution and Corollary 3.11 identifies HH² with A/dA, d=monic gcd(h,h′). Section 6.1 states that D_f(x)=0, D_f(Y)=f is inner precisely for f in h k[x]. Theorem 6.2(b) identifies the Lie center with classes D_f for d|f and deg f<deg h. Theorem 6.2(c) implies that HH¹ is abelian when d=1. These are the only substantive source-dependent structure claims needed.

The source assumes nonzero h and characteristic zero for these Lie calculations, not algebraic closure. Its monic normalization is harmless: rescaling Y identifies a nonmonic presentation with the monic one. Neither finite-dimensionality nor a Frobenius condition is assumed.

## Resolution and cup comparison independently checked

Write A=k<x,Y>/(Yx−xY−h). The relation generator r has differential

 ∂r = 1⊗Y⊗x + Y⊗x⊗1 − 1⊗x⊗Y − x⊗Y⊗1
       − Σ_s h_s Σ_{i=0}^{s−1} x^i⊗x⊗x^{s−1−i}.

Its image under the degree-two comparison into the normalized bar resolution is

 F₂(r)=[Y|x]−[x|Y]−Σ_{s≥2}h_s Σ_{i=1}^{s−1}[x^i|x]x^{s−1−i}.

The boundary of the inner sum is Σ_{i=0}^{s−1}x^i[x]x^{s−1−i}−[x^s]. The −[Yx]+[xY] term from the first two bar elements is −[h], which cancels the +[h] from these correction terms; the linear h term also matches directly and the constant term vanishes in normalized bar notation. Thus this is a genuine degree-two comparison, including linear and constant coefficients, rather than a commutative-antisymmetrization guess.

For any two derivations D,E this gives the cup representative

 D(Y)E(x)−D(x)E(Y)−Σ_s h_s Σ_{i=1}^{s−1}D(x^i)E(x)x^{s−1−i}.

In particular, D_f cup E is represented by f E(x). The calculation holds for all E, regardless of its x-component, its normalizer expression, or its y-degree. Therefore c=[D_d] annihilates every HH¹ cup product because d E(x) lies in dA. No assertion that all positive-degree products vanish is needed or made.

## Linear obstruction checked with the stated BV signs

For nonconstant h, deg d<deg h, so c is nonzero and central by Theorem 6.2(b). If d≠1, deg h≥2, and the independent classes D_1,D_x establish dim HH¹≥2 without any infinite-dimensionality claim.

For a hypothetical degree-minus-one generator, set λ=Δ|HH¹:HH¹→HH⁰=k. In the OWR convention the degree-one identity reads

 [c,z]=−Δ(c cup z)+λ(c)z−λ(z)c.

Its left-hand side and cup term vanish, hence λ(c)z=λ(z)c for every z. Choosing z independent of c forces λ(c)=λ(z)=0, and the same equation then forces λ to vanish everywhere. Consequently any cup-zero pair of degree-one classes would have zero bracket. This argument is independent of Δ² and of its values on HH².

## Cup-zero/noncommuting pair checked over arbitrary characteristic-zero fields

Choose any irreducible u|d. Put π=h/d, g=d/u, and

 a=D_g; b(x)=π; b(Y)=L Y; L=πd′/d.

The polynomial π contains every distinct irreducible factor of h once, up to a nonzero scalar. Thus L is polynomial: writing d as a product of powers, its logarithmic derivative has only simple irreducible denominators, all canceled by π. No root in k is required.

Applying b to Yx−xY−h gives Lh+hπ′−h′π=0, so b is an actual derivation. The cup representative is gπ=d(π/u), zero modulo d. Direct commutation gives

 [a,b](x)=0, [a,b](Y)=Lg−πg′=h u′/u²=:q.

Since u²|h, q is polynomial. Characteristic zero gives u′≠0. Its degree is deg h−2deg u+deg u′<deg h, so h does not divide the nonzero polynomial q. Therefore D_q is not inner, providing the required nonzero canonical Gerstenhaber bracket. This contradicts the generator identity and completes the negative direction.

This proof deliberately defines b on the presentation rather than writing it as ad(πy). The two conventions Y=hy and Y=yh generate the same subalgebra but differ by h′. Under the second convention, the naive ad(πy) formula may have an additional polynomial term. This convention issue does not affect the explicit derivation proof.

## Positive direction and boundaries

If d=1, HH²=0, higher HH vanishes, and HH¹ is abelian by Theorem 6.2. HH⁰=k has zero bracket with everything. Hence the entire canonical bracket is zero; Δ=0 is a legitimate square-zero BV generator. This includes all nonconstant squarefree h and all nonzero constants. For a nonzero constant, A is the first Weyl algebra and HH*=k.

The standard Nakayama automorphism sends x↦x and Y↦Y+h′. For every nonconstant h in characteristic zero, the invariant two-dimensional space spanned by Y and h′ has a nontrivial size-two unipotent Jordan block, so this automorphism is not semisimple. For constant h it is identity. Thus nonsemisimplicity alone neither prevents BV nor guarantees it: nonconstant squarefree h admits Δ=0, while repeated-factor h admits no generator.

The h=0 case must not be folded into this statement. It is excluded by the cited nonzero-h hypothesis. Extending the actual Weyl-subalgebra definition to h=0 gives k[x], whereas specializing the abstract two-generator presentation gives k[x,Y]. These are different algebras. Both have familiar divergence BV generators, but neither changes the classification for nonzero h. Characteristic p is not covered: separability, the center, cohomology, and scalar-valued λ change substantially.

## Reproducible exact checks and limitations

checks.py verifies the normalized-bar telescoping identity in degrees 2 through 20 and exact derivation/cup/bracket identities for seven examples, including powers of x²+1, mixed multiplicities, and a nonmonic h. CHECK_RESULTS.json records the output. These finite symbolic checks supplement the all-degree proof above; they are not offered as its substitute.

No mathematical counterexample was found in this audit. No claim is made about BV operators generating an unrelated bracket, twisted Hochschild variants, or positive characteristic.
