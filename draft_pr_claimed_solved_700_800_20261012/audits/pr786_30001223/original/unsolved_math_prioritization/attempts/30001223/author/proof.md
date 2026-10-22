# Counterexamples to the simple-top Young-module bridge

## Verdict and scope

For every odd prime p, let k be an algebraically closed field of characteristic p, put r=2p−1, set q=1, and take λ=(2p−2,1). Then the classical Young kS_r-module Y^λ is simple, but I_n(λ) is not projective for any integer n≥2. In particular p=3, r=5, λ=(4,1) refutes the unrestricted positive-characteristic formulation of Miyachi's Conjecture 7 in the 2009 Oberwolfach report [M]. This is a proposed authored counterexample with a complete argument below, supplied for independent audit. No claim of novelty or prior publication is made.

This does not refute the separate De Visscher–Donkin classification conjecture for projective-injective polynomial modules. It refutes the proposed implication from simple Young-module top to the existence of a projective polynomial injective. It makes no claim to refute a variant restricted to characteristic zero with a nontrivial root-of-unity parameter.

## 1. Source statement and conventions

[M], printed pp. 945–946, uses q-Schur algebras S(n,r), costandard modules ∇_n(λ), injective hulls I_n(λ), and tiltings T_n(μ). At stable rank it defines Y^λ=F I(λ) using the Schur functor F. Conjecture 7 asks whether simplicity of the head of Y^λ characterizes the existence of a rank n≥ℓ(λ) with I_n(λ) projective. Its subsequent criterion involving a rank-dependent De Visscher–Donkin set Λⁱ_n is explicitly a stronger proposal. It is not stated there as an already established equivalent classification. The definition uses an invertible parameter q; there is no characteristic-zero or q≠1 restriction attached to Conjecture 7. The later characteristic-zero qualification on p. 946 concerns the rational-category method for simple Specht modules.

The present example uses q=1, so the Hecke algebra is kS_r and the quantum characteristic is p. A partition is p-restricted (also called column p-regular) when λ_i−λ_{i+1}<p for every i, including the last nonzero part followed by zero. This is different from p-regular (no part repeated p times), and also different from the rank-n restricted condition omitting the last inequality. Our λ is p-regular but not p-restricted, since 2p−3≥p for p≥3. We do not infer projectivity from p-regularity.

We work with rational polynomial representations of the algebraic group GL_n(k), equivalently Schur-algebra modules. These are not representations of only the finite group GL_n(F_p). The distinction matters to both the proof and the checker.

## 2. Standard structural inputs, with exact locations

The following established facts are used from [DD]; all printed page numbers below refer to the 12 January 2005 manuscript, not its repository cover sheet.

1. In degree r, I_n(λ) has a costandard filtration whose multiplicity of ∇_n(μ) is [∇_n(μ):L_n(λ)]. A section other than ∇_n(λ) has μ strictly dominating λ. See §2.2, printed p. 7.
2. A projective indecomposable polynomial injective is contravariantly self-dual and is an indecomposable tilting module. Conversely an injective tilting is projective. Contravariant duality fixes each simple L_n(μ). See §2.4, printed pp. 10–11.
3. Rank truncation from GL_N to GL_n, N≥n, is exact and sends I_N(λ) to I_n(λ), and T_N(μ) to T_n(μ), whenever the displayed labels have at most n parts. See §2.2, printed pp. 8–9.
4. For GL_2, ∇_2(a,b)=det^b⊗Sym^(a−b)(E), where E is the natural module. The symmetric-power identity and determinant convention appear in §2.2, printed p. 8; determinant twisting gives the displayed two-row formula.

None of these inputs assumes either conjecture under investigation. In particular, we do not use the conditional classification in [DD, Theorem 5.1].

## 3. The Young module is simple

Let V=k^r with its permutation action of S_r, and let A={v∈V:Σ_i v_i=0}. Since p does not divide r=2p−1, the constant line k·(1,…,1) is complementary to A. Thus V=k⊕A.

To prove A simple over k, take a nonzero S_r-submodule U⊆A and v∈U\{0}. The coordinates of v cannot all be equal: a constant vector in A is zero because r is invertible in k. Choose i,j with v_i≠v_j. Then v−(ij)v=(v_i−v_j)(e_i−e_j) lies in U and is nonzero. Conjugating by permutations gives all coordinate differences, which span A. Therefore U=A.

The Young permutation module M^(r−1,1) is V; the Specht submodule S^(r−1,1) is A, because its polytabloids are precisely coordinate differences. The defining Young summand containing this Specht module is consequently Y^(r−1,1)=A. Hence Y^λ is simple of dimension r−1=2p−2, and its top is simple.

This argument uses no finite-field enumeration or decomposition table.

## 4. Two explicit GL_2 polynomial modules

Write x,y for a basis of E and use basis v_i=x^(m−i)y^i of Sym^m(E). Over the algebraically closed field k, every torus-stable subspace is a sum of weight spaces. The monomials in a fixed symmetric power have pairwise different torus weights.

We will repeatedly use this elementary coefficient principle: if a k-subspace is invariant under the one-parameter unipotents, then the coefficients in t of g(t)v also lie in the subspace. Indeed evaluation at sufficiently many distinct elements of the infinite field k and Vandermonde inversion recover those coefficients.

### 4.1 Sym^(2p−1)(E) is simple

Any nonzero invariant subspace contains a monomial v_i by torus-weight decomposition. Under y↦y+t x, the coefficient of t^i in v_i is x^(2p−1), so the subspace contains this highest monomial. Under x↦x+t y, the coefficients of x^(2p−1) are binomial(2p−1,j)v_j. All are nonzero modulo p: Lucas's formula, with base-p digits 2p−1=(1,p−1), gives binomial(2p−1,j)≠0 for every 0≤j≤2p−1. Hence all monomials are present. This proves simplicity, with highest weight (2p−1,0).

For completeness the needed binomial fact also follows by expanding (1+t)^(2p−1)=(1+t^p)(1+t)^(p−1) modulo p, where every coefficient of (1+t)^(p−1) is ±1.

### 4.2 Sym^(2p−3)(E) is a nonsplit extension of two different simples

Let B=Sym^(2p−3)(E), and let W be the span of v_i for

    0≤i≤p−3, or p≤i≤2p−3.

This is the image of the injective multiplication map E^(F)⊗Sym^(p−3)(E)→B sending x^(F)⊗f to x^p f and y^(F)⊗f to y^p f. The two monomial ranges are disjoint, so the map is injective, and its equivariance follows from the characteristic-p binomial identity. Thus W is invariant and has dimension 2p−4.

W is simple by the same monomial argument: any monomial yields x^(2p−3), and the nonzero coefficients of (x+t y)^(2p−3) occur exactly at those two ranges. This follows from (1+t)^(2p−3)=(1+t^p)(1+t)^(p−3) modulo p. Thus W has highest weight (2p−3,0).

The quotient B/W has basis the classes of v_(p−2) and v_(p−1). Its torus weights are (p−1,p−2) and (p−2,p−1). The two opposite unipotents connect these weight lines: the coefficient lowering index p−1 to p−2 is p−1≠0, and the opposite coefficient raising p−2 to p−1 is also p−1≠0. Hence B/W is simple, of highest weight (p−1,p−2), and dimension 2.

The extension 0→W→B→B/W→0 does not split. Any invariant complement would also be torus-invariant. Distinct torus weights force the only possible complement to be span(v_(p−2),v_(p−1)). But under y↦y+t x, v_(p−2) has coefficient x^(2p−3) at t^(p−2), which is nonzero and belongs to W. This candidate complement is therefore not invariant.

Since W and B/W are simple and the extension is nonsplit, W is the entire socle, while B/W is the simple top. The two simples have different highest weights even when p=3, when their dimensions both happen to be 2.

Tensoring by det, we conclude that ∇_2(λ)=det⊗B has simple socle L_2(2p−2,1) and simple top L_2(p,p−1), which are not isomorphic.

## 5. I_2(λ) is this costandard module and is not projective

Among partitions of r with at most two parts, the only label strictly dominating λ=(r−1,1) is (r). By §4.1, ∇_2(r)=Sym^r(E) is simple with label (r), so it has no composition factor L_2(λ). The injective-filtration multiplicity formula in §2 therefore gives

    I_2(λ)=∇_2(λ)=det⊗Sym^(2p−3)(E).

Contravariant duality fixes every simple and exchanges top with socle. Since the top and socle just computed have different labels, I_2(λ) is not contravariantly self-dual. By structural input 2, it is not projective.

At p=3 the decomposition matrix, using row and column order (5),(4,1),(3,2), is

    1 0 0
    0 1 1
    0 0 1.

The costandard dimensions are 6,4,2, so the injective dimensions and, by contravariant duality, projective dimensions are 6,4,6. In particular I_2(4,1) has dimension 4 and top L_2(3,2), while that top's projective cover has dimension 6. This is an additional numerical proof of nonprojectivity at the smallest explicit example, using the same standard reciprocity input.

## 6. Every higher rank is excluded

Suppose, for a contradiction, that I_N(λ) were projective for some N≥2. By structural input 2 it would be T_N(μ) for a partition μ of r. Since L_N(λ) occurs in I_N(λ), the tilting highest weight μ dominates λ. Consequently μ_1≥r−1. There are only two possibilities: μ=(r), or μ=(r−1,1). Both have at most two parts.

Apply the exact rank truncation from N to 2. Structural input 3 gives

    I_2(λ) ≅ T_2(μ).

The left-hand side is injective and the right-hand side tilting, so structural input 2 would make I_2(λ) projective. This contradicts §5. Thus no N≥2 works.

Notice that the stable-rank Schur functor is never applied at rank 2<r. Rank 2 enters only through polynomial-module calculations and the explicitly justified rank truncation. This prevents the common error of inferring preservation of an arbitrary module's head or projectivity under an idempotent functor.

## 7. Consequences and boundaries

For every odd p the left side of the proposed equivalence holds and the existence assertion on the right fails. Taking p=3 gives the completely explicit pair (k,λ)=(overline(F_3),(4,1)). A single such pair suffices to disprove the broad conjecture.

Every member of the proposed Λⁱ_n family is known to yield a projective injective by its sufficient construction. Therefore our λ cannot belong to any such Λⁱ_n, n≥2. The stronger simple-top/index-set characterization is refuted as well. This observation does not require proving that the Λⁱ_n family classifies every projective injective.

The example also makes the endomorphism-ring obstruction concrete. At p=3 the indecomposable injective I_2(4,1) has scalar endomorphism ring k, hence a self-injective endomorphism algebra, but the module itself is not projective. Self-injectivity of that ring cannot be promoted to projectivity of the module.

The same elementary permutation-module argument works for Y^(r−1,1) whenever p∤r, but the polynomial-module computation here is restricted to r=2p−1 and odd p. We do not assert that every such augmentation module gives a counterexample.

## 8. Reproducible supporting checks

verify.py uses exact arithmetic modulo 3, extracts the formal coefficient matrices in a,b,c,d for det(g)^k Sym^m(g), and verifies:

- Sym^5(E) has coefficient span of dimension 36, the full endomorphism algebra of its 6-dimensional space.
- det⊗Sym^3(E) has the invariant cube submodule, with both its submodule and quotient absolutely simple by full 2×2 coefficient spans.
- The equations for a section of the quotient have coefficient rank 4 and augmented rank 5, certifying nonsplitting.
- The endomorphism ring of det⊗Sym^3(E) has dimension 1.
- All 80 nonzero vectors in the 4-dimensional F_3 augmentation representation generate it under S_5.

The first three computations use polynomial coefficients, not only matrices evaluated on GL_2(F_3). The final 80-vector test is merely supporting finite evidence; the proof of simplicity over the algebraically closed field and the proof for all ranks and odd primes are §§3–6. The small decomposition matrix printed by the checker is an explicitly recorded consequence of those calculations and the cited reciprocity theorem, not an independent decomposition-number computation.

## 9. Literature assessment

Primary sources [M] and [DD] were retrieved and inspected on 6 October 2026. Bounded current public searches by the report, problem title, authors, and conjecture terminology did not establish a previously published resolution of this exact bridge conjecture. This is a search limitation, not evidence that the present counterexamples are novel. The projective-injective classification established for ranks 2 and 3 in [DD] is compatible with the counterexample; it is not a theorem proving the bridge to all simple-top Young modules.

## References

[M] Hyohe Miyachi, “Dipper's hypothesis and self-injective endomorphism rings,” in *Representations of Finite Groups*, Oberwolfach Reports 6 (2009), report 17, contribution pp. 944–947; especially Theorem 5 and Conjecture 7, pp. 945–946. DOI: https://doi.org/10.4171/OWR/2009/17 . Publisher report: https://ems.press/content/serial-article-files/46217 .

[DD] Maud De Visscher and Stephen Donkin, “On projective and injective polynomial modules,” *Mathematische Zeitschrift* 251 (2005), 333–358. DOI: https://doi.org/10.1007/s00209-005-0805-x . Manuscript dated 12 January 2005: https://openaccess.city.ac.uk/id/eprint/969/1/prinjjan12.pdf ; repository record: https://openaccess.city.ac.uk/id/eprint/969/ .
