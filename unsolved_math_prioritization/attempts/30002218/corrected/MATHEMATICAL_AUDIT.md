# Mathematical audit

## 1. Target and source match

Let A and B be C*-subalgebras of a common B(H), and let A₁ and B₁ denote their closed norm-unit balls. Put

    d(A,B) = max{sup(a∈A₁) dist(a,B₁), sup(b∈B₁) dist(b,A₁)}.

The target asks for a universal positive δ such that

    A separable, A ≅ A⊗Z, d(A,B)<δ  ⇒  B ≅ B⊗Z.

Tensor products here are spatial. In the unital arguments below the ambient algebra is taken nonzero; the zero-algebra case is immediate. The original question occurs in Stuart White's contribution to the Oberwolfach report, p. 3143; its metric is defined on p. 3140. There is no nuclearity, simplicity, unitality, or explicit separability assumption on B. The target is two-sided closeness, not merely a near inclusion. The complete metric d_cb(A,B)=sup_n d(M_n(A),M_n(B)) is a different hypothesis. [OWR]

This same formulation appears as Problem XCIX in the May 2026 revision of [STW], §27, pp. 82–83. That is positive evidence of its publicly stated open status at that date. The bounded searches conducted on 2026-10-06 found no later matching resolution; this is not an exhaustive claim about all literature or unpublished work.

For sufficiently small δ the missing separability assumption on B is harmless. Here is a direct argument under d(A,B)<1/2. Choose γ with d(A,B)<γ<1/2, and ε>0 with q=2γ+ε<1. Let (a_j) be dense in A₁ and choose b_j∈B₁ with ||a_j-b_j||<γ. Each b∈B₁ is within q of some b_j, by first approximating b in A₁ and then using density. Let L be the closed complex linear span of the b_j. Starting with any b∈B, subtract an element of L within q||b||, and iterate on the residual. The residual norms tend to zero geometrically, so b∈L. Thus B=L is separable. This is a standard transfer fact, also covered by [CSSWW, Proposition 2.10], not a new result.

## 2. Credited positive results and their boundaries

### 2.1 Nuclear case

[CSSWW, Theorem 4.3] supplies A≅B when A is separable and nuclear and d(A,B)<1/420000. Hence the target follows in this additional-nuclearity case: for an isomorphism θ:A→B and α:A→A⊗Z, the composite

    B --θ⁻¹--> A --α--> A⊗Z --θ⊗id_Z--> B⊗Z

is an isomorphism. No separability of H is needed for this abstract isomorphism. The stronger spatial-conjugacy statement elsewhere in that paper has additional ambient hypotheses and is unnecessary here. Nuclearity of the ambient A cannot be dropped from this application merely because Z is nuclear.

### 2.2 Embedding and closedness results

[CSSWW, Corollary 4.7] transports a copy of a strongly self-absorbing algebra across a sufficiently small one-sided near inclusion. For the constant used below, an embedding of Z can be chosen within 152√γ on a prescribed finite set when 0<γ<1/12600000. This yields an ordinary embedding, without automatically giving centrality. Their Corollary 4.6 also proves closedness of the D-absorbing class among separable subalgebras sharing the ambient unit. These are existing results; neither asserts a uniform open neighborhood.

### 2.3 Cuntz-semigroup transfer

[PTWW, Corollary 4.15] prints the following conclusion

    d(A,B)<1/6422957, A≅A⊗Z
      ⇒ d_cb(A,B)<1/42
      ⇒ (Cu(A),Σ(Cu(A))) ≅ (Cu(B),Σ(Cu(B))).

The last arrow is [PTWW, Theorem 3.10]. The scale is included. The radius 1/6422957 is recorded here as a published statement, not as an independently certified quantitative bound: the source has an unresolved parameter discrepancy described in §2.4. A conservative retained-parameter bound 1/16000000 is verified below for the common-unit unital subcase. This does not provide a *-isomorphism of A and B or an absorption theorem for B. [STW, §27] explicitly distinguishes the Cuntz-semigroup result from the absorption problem. Nuclear classification theorems cannot be applied after silently adding nuclearity or Z-absorption to B.

### 2.4 Printed arithmetic, a source discrepancy, and a conservative bound

The original author check correctly evaluates the formulas printed in [PTWW, Proposition 4.13], but it does not validate the proof chain leading to those formulas. Both the arXiv v2 and published versions have the following discrepancy:

- Lemma 4.11 uses β=96kα(600k+1).
- Substitution α=11γ gives β=1056k(600kγ+γ), as printed in Lemma 4.12.
- Proposition 4.13 instead prints β=1056(600kγ+γ), without the leading k, while its proof invokes Lemma 4.12.

This is a source-level bookkeeping gap. No claim is made that Corollary 4.15 is false, that its radius is optimal, or that the discrepancy has not previously been noticed. The numerical check below distinguishes what each calculation establishes.

**Printed-parameter calculation.** Write N=6422957 and k=5/2. Using Proposition 4.13 exactly as printed gives

    β=1585056γ,
    η=3203122γ+52306848000γ²,
    d_cb(A,B) ≤ 10γ/(1-2η-5γ).

For 0<γ<1/N, the first smallness condition follows from √2<3/2 and

    24(12√2 k+4k+1)γ < 1344/N < 1/2200,
    1344·2200=2956800<N.

Also 2η+425γ=6406669γ+104613696000γ²<1, since this polynomial is increasing on γ≥0 and

    N²-6406669N-104613696000 = 3427616 > 0.

Thus these printed formulas imply the announced complete-distance estimate. This arithmetic is correct. It does not account for the factor k from Lemma 4.12. The proof's additional γ<10⁻¹¹ observation does not by itself resolve the larger-radius issue either.

**Retained-parameter calculation.** Keeping the parameter supplied by Lemma 4.12 gives

    β_*=1056k(600kγ+γ)=3962640γ,
    η_*=10γ+2β_*+13200kγ(1+β_*)
       =7958290γ+130767120000γ².

For the common-unit unital subcase, the perturbation argument in the proof of Proposition 4.13 then uses the conservative expression

    d_cb(A,B) ≤ 10γ/(1-2η_*-5γ),

provided its smallness hypotheses hold with η_*. Take M=16000000. For 0<γ<1/M, the first condition still follows from 1344·2200<M. Moreover,

    2η_*+425γ=15917005γ+261534240000γ²<1,
    M²-15917005M-261534240000=1066385760000>0.

Hence 1-2η_*-5γ>420γ>0, and the complete-distance bound is less than 1/42. Applying [PTWW, Theorem 3.10] gives scaled Cuntz-semigroup transfer at the conservative radius 1/16000000 in this common-unit unital subcase. This is an audited consequence of the existing perturbation method with the larger parameter retained, not a novelty claim or an improvement of the published statement.

The restriction on the conservative deduction is deliberate: [PTWW, Proposition 4.2] assumes nondegenerate representations, whereas Corollary 4.15 is printed for arbitrary algebras on a shared Hilbert space. Passing to the common support of the shared unit satisfies that hypothesis. This audit does not independently reconstruct a bound for arbitrary different supports or arbitrary nonunital pairs. It does not impose these restrictions on the source-stated Corollary 4.15.

The discrepancy matters: at γ=1/7000000, which is below 1/6422957, the retained expression is

    2η_*+5γ = 2791940731/1225000000 > 1.

Thus that proof's positivity hypothesis can fail inside the printed radius. This invalidates an independent verification of the full printed radius by this calculation; it does not supply a counterexample to Cuntz transfer or to Jiang–Su stability.

## 3. Direct transfer: the error that does not disappear

Suppose A and B are unital and share 1, and d(A,B)<γ<1/12600000. Let X⊂B₁ and Y⊂Z₁ be finite, including 1 in Y. Choose a_x∈A₁ with ||a_x-x||<γ for x∈X. Since A is Z-stable, for any ε>0 one can find a unital embedding φ:Z→A with

    ||[φ(y),a_x]||<ε  (x∈X, y∈Y).

For completeness, this standard approximately-central embedding property can be seen by identifying A with A⊗Z⊗Z⊗⋯, approximating the finitely many a_x in finitely many tensor factors, and using a later Z-factor. Strong self-absorption identifies the infinite tensor power with Z. [TW]

Apply the embedding-transfer result to φ(Z). Obtain an embedding ψ:Z→B satisfying

    ||ψ(y)-φ(y)||<152√γ  (y∈Y).

It is unital: ψ(1) is a projection and ||ψ(1)-1||<152√γ<1, whereas any projection distinct from 1 has distance 1 from 1. Expanding a commutator gives

    [ψ(y),x]=[ψ(y)-φ(y),x]+[φ(y),x-a_x]+[φ(y),a_x],

and therefore

    ||[ψ(y),x]|| < 304√γ+2γ+ε.                (1)

This is a rigorous finite-set transfer estimate. For a fixed positive γ, decreasing ε leaves a positive upper-error allowance. Equation (1) supplies no embeddings with arbitrarily small commutators at that fixed γ. It is an upper bound, not a lower bound and not a proof that better embeddings cannot exist.

There is an even simpler warning against coordinatewise arbitrary choices. In the Z-stable algebra M₂⊗Z let x_n=1, p=e₁₁⊗1, b=e₁₂⊗1, and y_n=1-γp for 0<γ<1. Then x_n is central, y_n is a contraction with ||y_n-x_n||=γ, and ||[y_n,b]||=γ for every n. Thus choosing uniformly close representatives does not preserve central sequences, even when the two algebras are identical. This is a counterexample to that selection shortcut only, not to the target.

## 4. A rigorous conditional central-sequence bridge

The following is an authored deduction from known theorems. It is not asserted to be novel, and its additional premise has not been obtained from the target.

**Conditional theorem.** Let A and B be separable unital C*-subalgebras of a unital C, with 1_A=1_B=1_C, and assume A≅A⊗Z. In

    Q(C)=ℓ∞(C)/c₀(C),

view Q(A) and Q(B) as their canonical injective subalgebras and set

    F_A=Q(A)∩A′,    F_B=Q(B)∩B′.

Suppose that for some 0<γ<1/12600000 every contraction in F_A is within γ of a contraction in F_B. Then B≅B⊗Z.

**Proof.** By [TW, Theorem 2.2], because A is unital, separable, and Z-stable, there is a unital *-homomorphism ρ:Z→Q(A)∩A′. It is injective because Z is simple. Choose γ₁ with γ<γ₁<1/12600000. The pointwise distance premise implies ρ(Z)⊆_γF_B, and hence ρ(Z)⊂_γ₁F_B in the strict uniform convention of [CSSWW, Definition 2.2]. Represent Q(C) faithfully on a Hilbert space; such a representation preserves all these norm distances. Apply [CSSWW, Corollary 4.7] with γ₁, choosing the prescribed finite set to contain 1. This produces an embedding σ:Z→F_B with ||σ(1)-1||<152√γ₁<1. The projection argument above makes σ unital. Apply [TW, Theorem 2.2] to B to conclude B≅B⊗Z. ∎

F_A and F_B may be nonseparable. This causes no problem: the embedding theorem is applied to the separable copy ρ(Z), and does not require its target F_B to be separable. The final absorption criterion does require B to be separable, as explicitly assumed. The natural maps Q(A)→Q(C) and Q(B)→Q(C) are injective because a bounded sequence from A or B tends to zero in C exactly when it tends to zero in its own algebra.

The missing implication is central-sequence near inclusion. Coordinatewise approximation gives proximity to Q(B); ambient commutant estimates, when applicable, give proximity to a commutant. Neither alone gives proximity to their intersection F_B. Nonunital algebras require the correct multiplier/annihilator formulation; this conditional theorem makes no claim to settle those extra issues.

### Why an intersection argument needs actual proof

Let D⊂M₂ be the diagonal algebra, let U_t be the real rotation with angle t, and put C_t=U_tDU_t*. Then

    d(C_t,D) ≤ 2||U_t-1|| → 0.

For 0<t<π/2, the rank-one generator of C_t has nonzero off-diagonal entry sin(t)cos(t). Its commutator with diag(a,b) vanishes exactly when a=b. Consequently

    D∩C_t′ = C·1,   whereas   D∩D′ = D.

The distance from diag(1,-1) to C·1 is 1: for any scalar z, max{|1-z|,|-1-z|}≥1, with equality at z=0. Thus the two relative commutants have Kadison–Kastler distance 1, despite C_t→D. This disproves a general continuity rule for such intersections. It is not a counterexample to continuity of F_A versus F_B under the original special hypotheses, nor to Jiang–Su stability.

## 5. The vanishing-distance argument and its exact scope

Suppose B is separable unital in a unital C, and A_n⊂C are separable unital Z-stable subalgebras sharing 1_C, with d(A_n,B)→0. Choose γ_n>d(A_n,B) tending to zero. For large n the embedding-transfer threshold applies. Let (b_j) be dense in B₁ and (z_j) dense in Z₁, with z₁=1. For X_n={b₁,…,b_n} and Y_n={z₁,…,z_n}, apply the construction of §3 with A_n, γ_n, and ε_n→0. We obtain unital embeddings ψ_n:Z→B satisfying

    max(j,k≤n) ||[ψ_n(z_j),b_k]||
       <304√γ_n+2γ_n+ε_n →0.

Ignore the finitely many unavailable early terms, or fill them with one later embedding. The formula Ψ(z)=[(ψ_n(z))] defines a unital *-homomorphism Z→Q(B), because each coordinate map is a unital *-homomorphism. Contractivity and density extend the displayed commutator convergence to every z∈Z and b∈B. Thus Ψ(Z)⊂Q(B)∩B′. [TW, Theorem 2.2] gives B≅B⊗Z.

This reproves the Z-instance of [CSSWW, Corollary 4.6]. It proves closedness. The original target needs one fixed positive radius valid for all pairs. The hypothesis here instead gives arbitrarily small distances to the same B. There is no license to replace the fixed d(A,B) by a sequence tending to zero. No iteration reducing that distance, and no uniform error-improvement theorem for (1), has been established in this investigation.

## 6. Disposition

All five approaches stop at the boundaries stated above. No counterexample meeting the exact source hypotheses was constructed, and no proof of the universal δ assertion was found. The meaningful outputs are the verified source/status match, credited partial results, explicit constant audit with its source discrepancy and conservative bound, and conditional bridge identifying a missing premise. The original problem remains unresolved in this work.

## References

- [OWR] J. Cuntz, G. A. Elliott, A. Toms, W. Winter, eds., *C*-Algebras, Dynamics, and Classification*, Oberwolfach Reports 9 (2012), 3129–3209, published 2013; Stuart White's contribution pp. 3140–3143. https://doi.org/10.4171/owr/2012/52 ; https://ems.press/content/serial-article-files/46423
- [CSSWW] E. Christensen, A. M. Sinclair, R. R. Smith, S. A. White, W. Winter, *Perturbations of nuclear C*-algebras*, Acta Mathematica 208 (2012), 93–150. https://arxiv.org/abs/0910.4953 ; https://doi.org/10.1007/s11511-012-0075-5
- [PTWW] F. Perera, A. Toms, S. White, W. Winter, *The Cuntz semigroup and stability of close C*-algebras*, Analysis & PDE 7 (2014), 929–952. https://arxiv.org/abs/1210.4533 ; https://doi.org/10.2140/apde.2014.7.929 ; published PDF https://eprints.gla.ac.uk/90387/1/90387.pdf
- [TW] A. S. Toms, W. Winter, *Strongly self-absorbing C*-algebras*, Transactions of the AMS 359 (2007), 3999–4029, Theorem 2.2. https://arxiv.org/abs/math/0502211
- [STW] C. Schafhauser, A. Tikuisis, S. White, *Nuclear C*-algebras: 99 problems*, arXiv:2506.10902v2, revised 8 May 2026, §27, pp. 82–83. The arXiv record states that it is to appear in a special issue of Münster Journal of Mathematics. https://arxiv.org/abs/2506.10902v2
