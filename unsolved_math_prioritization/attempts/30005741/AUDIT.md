# Independent logical audit: truncated symmetric Poisson lengths

Target: **30005741 / OWR-14298013-005**.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The complete written mathematical proofs, analytical constructions, source-theorem dependencies, and finite-field reduction appendix are retained. This is not a computational reproduction package: executable code, raw finite dimension-vector datasets and certificates, copied source documents and images, and private coordination material are omitted. Historical finite computations are supporting evidence only; they do not prove either unrestricted equality. The historical computations cannot be reproduced from this edition alone.

Both full questions remain unresolved by this work. No novelty, priority, comprehensive literature-survey, or current global-openness claim is made.

This edition retains the complete independent mathematical reasoning and source-hypothesis analysis. Computational and source-inspection statements below describe the original audit, not new editorial executions or source inspections. The two optional wording clarifications have been applied to PROOF.md. Raw dimension vectors and private process details have been omitted without changing the accepted mathematical statements.

Verdict: **ACCEPT the candidate's Theorems A–D as proved partial results. No mathematical correction is required.** Two optional editorial clarifications are listed in Section 12. Neither original question is resolved by this work, and no novelty or comprehensive literature-status claim is accepted or made.

The original audit authenticated the candidate manifest SHA-256 e6f265dabf2932e211571fd72a7a362226108cde5e942a8f3c8a814139ce2b43, all 16 listed members, and exact package membership. No candidate or source-author program was imported or executed during that independent audit, and no original candidate or source member was changed. The candidate and independent audit have again been authenticated during editorial preparation without executing their mathematical programs.

## 1. What was accepted, and what was not

For a Lie algebra L over any field F of characteristic p > 0, write R = s(L) = S(L)/(v^p : v in L). The bracket on L is alternating, including at p = 2. No restricted structure is assumed.

The accepted statements are:

1. If L is nilpotent and dim L' ≤ 2, ordinary and strong nilpotency classes of R agree, with values 1, p, 2p − 1, or 3p − 2 in the candidate's four cases.
2. If L is class two, dim L' = m < infinity, and [x,L] = L' for some x, both classes are 1 + (p−1)m. The stated finite direct-sum closure and arbitrary central abelian direct-summand additions are valid.
3. If dim L' ≤ 1 and p > 2, ordinary and strong derived lengths agree: 1 in the abelian case, ceil(log₂(p+1)) in the nonzero central case, and 1 + ceil(log₂ p) in the noncentral case. The noncentral calculation, including equality of entire derived series, also holds at p = 2.
4. Any counterexample to either specified question can be localized to finite dimension and specialized to a genuinely finite field of the same characteristic while preserving its exact unequal pair of finite invariants.

These results do not cover every nilpotent or solvable L. No finite computational sample is promoted to a universal proof. In particular, no equality of ordinary and strong derived lengths is asserted in general in characteristic 2.

The proofs of the partial statements were checked directly. The necessity directions of the published structural theorems used in statement 4 remain cited mathematical inputs; this audit does not certify that entire article from first principles.

## 2. Source identities and exact hypothesis matching

### 2.1 Primary structural article

I. Z. Monteiro Alves and V. Petrogradsky, *Lie structure of truncated symmetric Poisson algebras*, Journal of Algebra 488 (2017), 244–281; [arXiv:1612.08051v1](https://arxiv.org/abs/1612.08051v1), [journal DOI](https://doi.org/10.1016/j.jalgebra.2017.05.035).

Authenticated PDF: 312,691 bytes, SHA256 `d8aa1997211d67e7097f1dde787a571769cdede211fb43cfed7c68ab43aab7d0`. Authenticated extracted text: 106,287 bytes, SHA256 `4987623fa7a0bb38dbefe5f68bc6cb88f4b77c9837bcff3292cecf89125764d9`.

Theorem 4.1, PDF page 7, concerns an arbitrary Lie algebra over a field of positive characteristic. It equates Lie nilpotence of s(L), strong Lie nilpotence of s(L), and nilpotence of L together with finite-dimensional L'. There is no finite-dimensional-L, algebraically-closed-field, or restricted-Lie hypothesis. Therefore the nilpotency reduction's finite-dimensional-L' input and finite strong invariant are justified in characteristics 2 and 3.

Theorem 4.3, PDF page 8, gives the corresponding solvability equivalence for p ≥ 3. At p = 2, its ordinary-solvability implication is explicitly absent. The candidate retains p > 2 throughout the solvability reduction, so it invokes precisely the available theorem. It does not use equality of derived lengths as a structural input.

Theorem 4.2 separates the strong-class formula, which still holds at p = 2 and 3, from ordinary-class equality, which is stated for p > 3. The candidate does not silently extend that equality to small characteristic. Its upper bounds can also be obtained directly from its elementary weight arguments.

I visually inspected PDF pages 7 and 8 to confirm the statements and the strong-nilpotency definition's typographical error. I also visually inspected pages 13 and 14: Lemma 8.3 provides a factor of 3, while Lemma 8.6 explicitly divides by 2. The candidate's description of the obstruction in the older proof is accurate. It is an obstruction to that proof, not evidence that the desired equality fails.

### 2.2 Exact question source

Salvatore Siciliano, *Solvability of symmetric Poisson algebras*, contribution to *Mini-Workshop: Poisson and Poisson-type algebras*, Oberwolfach Report 46/2023, printed pages 2703–2704, PDF pages 23–24; [workshop DOI](https://doi.org/10.4171/owr/2023/46), [publisher PDF](https://ems.press/content/serial-article-files/48175?nt=1).

Authenticated PDF: 348,993 bytes, SHA256 `e33479028da10623035810f64b50e920d9191dee800d20da30e36afa96372626`. Authenticated extracted text: 96,510 bytes, SHA256 `b2ec6510177bb4399d751c0ead390dea5c5f820d3bec5ad24cac83f847392b1b`.

The contribution gives separate ordinary/strong nilpotency-class and derived-length questions. The former targets p = 2,3 under Lie nilpotence; the latter targets p > 2 under solvability. The page-24 rendered source explicitly notes a characteristic-2 derived-length discrepancy. I checked the contribution text on pages 23–24 and visually inspected page 24. No current global openness certificate is inferred from this dated source.

## 3. Indexing, PBW basis, and infinite-dimensional scope

The accepted conventions are gamma₁(R) = R, gammaₙ₊₁(R) = {gammaₙ(R),R}; upper Lie powers U₀ = R, Uₙ₊₁ = {Uₙ,R}R; ordinary derived spaces delta₀ = R, deltaₙ₊₁ = {deltaₙ,deltaₙ}; and strong derived spaces D₀ = R, Dₙ₊₁ = {Dₙ,Dₙ}R.

Class c means gamma꜀₊₁ = 0 but gamma꜀ ≠ 0, or U꜀ = 0 but U꜀₋₁ ≠ 0, respectively. Derived length n means the first zero at index n. Since R is unital and nonzero even when L = 0, the abelian case has value 1 for all four invariants. A nonzero word with c entries belongs to gamma꜀, not gamma꜀₊₁. The candidate counts its words correctly.

The PDF page-7 prose incorrectly writes zero for both consecutive upper powers. Reading the earlier power as nonzero is justified by the surrounding definitions, the class-one assertion, and the later strong-class proof. The candidate discloses rather than propagates that typo.

For any basis of L, the ideal (v^p : v in L) equals the ideal generated by the basis-vector pth powers. One inclusion holds because each basis vector is an allowed v; the other follows from Frobenius applied to each finite linear combination. No perfect-field hypothesis is needed. Truncated finite-support monomials are therefore a basis, even when L has infinite dimension.

Extend a basis of a Lie subalgebra H to one of L. Its truncated monomials form a subset of this basis, proving s(H) → s(L) injective. This is the injection used for every local lower-bound witness and the finite-dimensional reduction.

For a central abelian direct summand C, s(L ⊕ C) is the algebraic tensor product s(L) ⊗ s(C). The bracket is {a⊗u,b⊗v} = {a,b}⊗uv. Each of the four series equals the corresponding series of s(L), tensored with s(C). The reverse inclusion at every stage uses the unit in s(C), so arbitrary coefficients in the central tensor factor can be supplied. Tensoring over a field with nonzero s(C) preserves nonvanishing. Infinite cardinality causes no issue because elements have finite support and no completion is being used.

This is an invariance claim for central direct-summand additions, not for arbitrary nonsplit central extensions. The broader infinite-dimensional cases in Theorems A and C are handled by upper bounds valid in all of L and lower bounds in embedded finite subalgebras; they are not silently decomposed as a small algebra plus its center.

## 4. Class-two proof and the breadth lemma

When L' is central with basis z₁,…,zₘ, let I = L'R. Every bracket belongs to I. Because each zᵢ is Poisson central, {Iᵃ,Iᵇ} is contained in Iᵃ⁺ᵇ⁺¹. Thus Uₙ ⊆ Iⁿ. The maximum possible total z-degree in a nonzero truncated monomial is m(p−1), so Uₘ₍ₚ₋₁₎₊₁ = 0. The ordinary class is bounded by the strong class, yielding the same upper bound for both.

If [x,L] = L', choose yᵢ with [x,yᵢ] = zᵢ. For every polynomial P in the central zᵢ, direct Leibniz expansion gives {xP,xyᵢ} = xPzᵢ. Starting with x and appending xyᵢ exactly p−1 times for each i produces x times the product of zᵢ^(p−1). The number of entries is 1 + m(p−1). Since x is outside L' and the zᵢ are independent, this is a nonzero truncated basis monomial. No claim that the yᵢ commute is needed for this calculation. No division or characteristic-dependent factorial occurs.

The breadth lemma is valid over every field, including F₂. If every image B(x,V) has dimension at most one, choose B(a,b) = z ≠ 0. The images of a and b are contained in Fz. Any u with image not contained in Fz must satisfy B(u,a) = B(u,b) = 0: otherwise one nonzero value would force its one-dimensional image to equal Fz. Choose v with B(u,v) outside Fz. Then B(a+u,b) = z while B(a+u,v) lies outside Fz. The image of a+u has dimension at least two, a contradiction. The argument uses alternation and bilinearity, not a supply of many field elements or division by 2.

For dim L' = 2 in class two, the image span of the bracket is exactly L', so the lemma supplies the full-image x needed above. For dim L' = 1 and nilpotent L, a nonzero gamma₃(L) would equal L', forcing the lower central series to stabilize rather than terminate. Hence L' is central, and the same word with m = 1 proves class p. The abelian case gives class 1.

Verdict on these cases and the single-summand part of Theorem B: accepted.

## 5. Two-dimensional noncentral L': extraction and maximal word

Assume L is nilpotent, dim L' = 2, and gamma₃(L) ≠ 0. Every nonzero lower-central stage must strictly decrease until zero; otherwise equality at two consecutive stages persists forever. Therefore dim gamma₃ = 1 and gamma₄ = 0. The inclusion [gamma₂,gamma₂] ⊆ gamma₄ shows that L' is abelian. These lower-central facts use only Jacobi and hold for alternating Lie algebras in characteristic 2.

Choose z modulo gamma₃ and nonzero w spanning gamma₃. Write [t,z] = alpha(t)w with alpha nonzero. There is a bracket z' = [u,v] outside gamma₃ because brackets span L'. It is noncentral: its z coefficient is nonzero. If both u and v centralized L', then Jacobi would imply [a,[u,v]] = 0 for every a, contradicting this. Thus one may arrange [u,z'] ≠ 0 and alpha(u) ≠ 0.

Set x = u and y = v − alpha(v)alpha(u)⁻¹u. Then [x,y] = z', [y,z'] = 0, and [x,z'] = w' ≠ 0. The division is by a specifically nonzero field element, not by 2 or 3. The elements x,y are independent modulo L': a linear dependence there would place [x,y] in [L,L'] = gamma₃, contrary to its choice. The two remaining elements z',w' are independent because they lie in different lower-central layers. Their span is therefore the four-dimensional subalgebra with [x,y] = z and [x,z] = w and no further nonzero defining brackets.

On the commutative truncated algebra in y,z,w, define D(y) = z, D(z) = w, D(w) = 0. This derivation is well defined because derivatives of the pth-power relations vanish in characteristic p. Leibniz gives

- {xf,xy} = x(zf − yD(f));
- {xf,x} = −xD(f).

In particular the consecutive entries (xy,x) take xwᵇ to −xwᵇ⁺¹. Repeating the pair p−1 times gives (−1)^(p−1)xw^(p−1). Then appending xy increases the z exponent by one: the otherwise troublesome derivative term contains w^p and vanishes. After p−1 further entries the value is (−1)^(p−1)xz^(p−1)w^(p−1), a nonzero basis monomial. There are 1 + 2(p−1) + (p−1) = 3p−2 entries. This remains valid at p = 2, where minus equals plus, and at p = 3.

For the global upper bound, give z weight 1, w weight 2, and all complementary basis vectors weight zero. A nonzero bracket of basis vectors has output weight at least the sum of the input weights plus one. The only nontrivial checks are brackets of two weight-zero vectors, which lie in L', and brackets with z, which lie in Fw. Brackets with w and brackets within L' vanish. The monomial Leibniz expansion therefore raises total weight by at least one, while multiplication never lowers it. Thus Uₙ is supported in weight at least n. The maximum available weight is 3(p−1), so U₃ₚ₋₂ = 0. Complementary basis vectors may be arbitrarily numerous without changing this bound.

The embedded word supplies the matching ordinary lower bound. Verdict on the remaining case of Theorem A: accepted.

## 6. Direct-sum closure

Let unital Poisson algebras A and B have finite ordinary classes c and d. Since the last nonzero lower-central spaces are spans of left-normed words, choose actual nonzero words u and v with c and d entries. Starting with a₀⊗b₀, first appending the remaining A entries tensored with 1 and then the remaining B entries preceded by 1 gives u⊗v. It is nonzero over the field, and the number of entries is c+d−1. This proves the required tensor-product lower bound, including when one class equals 1.

For the particular algebras under consideration, the already established weight upper bounds add. If their respective maximum weights are c−1 and d−1, the strong class in the tensor product is at most c+d−1. The lower and upper bounds coincide. Induction handles finitely many nonabelian summands. Any sum of abelian central summands can be collected in C and handled as in Section 3.

The argument is not an unsupported general theorem about tensor products of derived lengths or about arbitrary Poisson algebras. Verdict: accepted with exactly the candidate's stated scope.

## 7. Central one-dimensional derived subalgebra

Let L' = Fz be nonzero and central, and p > 2. The recurrence Dₙ ⊆ z^(2ⁿ−1)R follows from centrality: bracketing two elements having z exponent at least a introduces at least 2a+1 powers of z. It forces Dₙ = 0 when 2ⁿ−1 ≥ p.

Choose [x,y] = z. The three elements x,y,z are independent: if z were in the span of x and y, bracketing that dependence with x and y would force its coefficients to vanish. Thus their Heisenberg subalgebra embeds.

For the constant symplectic bracket on x,y, the six distinct truncated monomials 1,x,y,x²,xy,y² span a closed Lie subspace V when p > 2. Each is a bracket of two elements of V, up to an invertible coefficient 1, 2, or 4. The six displayed identities in the candidate are correct. At p = 3, 2 and 4 remain invertible, x² and y² remain nonzero, and {x²,y²} = 4xy = xy. Consequently {V,V}₀ = V even in that critical characteristic. This is a perfect Lie subspace containing a central element; there is no contradiction in that assertion.

The actual bracket is z times the constant symplectic bracket on these polynomials. Centrality gives {zᵃV,zᵇV} = zᵃ⁺ᵇ⁺¹V. Starting from V ⊆ delta₀ yields z^(2ⁿ−1)V ⊆ deltaₙ. This subspace contains the nonzero monomial z^(2ⁿ−1) whenever 2ⁿ−1 < p. The ordinary lower bound therefore matches the strong upper bound, giving ceil(log₂(p+1)).

At p = 2, the proposed six monomials are no longer distinct and nonzero: x² = y² = 0. In fact the remaining four-dimensional constant symplectic algebra has a three-dimensional first commutator space, so this perfect-subspace proof would fail. The candidate correctly excludes that characteristic from this central-case theorem. No conclusion about characteristic-2 equality in general follows from the occasional valid finite Heisenberg test.

The proof uses no finite-rank assumption on the alternating bracket form of L/Fz. It does not assert that an infinite-rank class-two L splits into a single Heisenberg algebra and a central complement. Verdict: accepted in the exact stated range.

## 8. Noncentral one-dimensional derived subalgebra

Let L' = Fz and define alpha by [t,z] = alpha(t)z. Noncentrality permits x with alpha(x) = 1. Set A = ker alpha; it contains z and has codimension one. For u,v in A, write [u,v] = bz. The derivation form of Jacobi gives [x,[u,v]] = [[x,u],v] + [u,[x,v]] = 0 because u,v commute with z and both inner brackets lie in Fz. The left side is bz. Thus A is abelian.

Define beta on A by [x,a] = beta(a)z; beta(z) = 1. Then A = Fz ⊕ ker beta, and C = ker beta is central in L. This proves L = (Fx ⊕ Fz) ⊕ C with [x,z] = z, even in characteristic 2 and even when C has infinite dimension. There is no unproved finite-dimensional classification step.

In T = F[x,y]/(x^p,y^p) with {x,y} = y, monomial Leibniz expansion gives coefficient ad−bc and exponent x^(a+c−1)y^(b+d). Terms outside the truncation range vanish. This formula is correct also in characteristic 2.

For 1 ≤ s < p and 0 ≤ r ≤ p−2, {x^(r+1),yˢ} has nonzero coefficient (r+1)s and yields xʳyˢ. The missing r = p−1 row is supplied by {x,x^(p−1)yˢ}, whose coefficient is s. Thus {T,T} = yT; the top x-exponent row is not omitted.

For I_q = y^qT with 1 ≤ q < p, the bracket is contained in I₂q. If 2q ≥ p, both are zero. Otherwise, every target xʳyˢ with 2q ≤ s < p is produced by {y^q,x^(r+1)y^(s−q)} when r ≤ p−2, with nonzero coefficient −q(r+1). For r = p−1, use {xy^q,x^(p−1)y^(s−q)}; its coefficient is s−pq = s in the field and is nonzero. Both inputs have y exponent at least q. Hence {I_q,I_q} = I₂q exactly.

Because these spaces are already associative ideals, the strong series adds nothing. For n ≥ 1, deltaₙ(T) = Dₙ(T) = y^(2ⁿ⁻¹)T. Its first zero occurs at 1 + ceil(log₂ p). The p = 2 instance terminates at index 2 and requires no forbidden coefficient division. The central tensor factor C preserves the series. Verdict: accepted, including the claimed equality of series rather than only of their lengths.

## 9. Finite-dimensional localization

In either question's stated characteristic range, the source theorems provide dim L' < infinity and finiteness of the strong invariant. Ordinary invariants are at most strong ones, by containment of their series; hence a counterexample has a finite unequal pair a < b.

At the last nonzero stage of each relevant series, choose a nonzero defining expression evaluation. Such a choice is legitimate because the stage is the linear span of evaluations of its bracket/product polynomial. A nonzero sum cannot have every summand zero. Each expression has finitely many inputs, each input of s(L) has finite basis support, and the union S of these supports is finite.

Let H be the Lie subalgebra generated by S. The subspace span(S) + L' is finite dimensional and bracket closed: every bracket in L lies in L'. Therefore H is finite dimensional. This is the necessary extra argument; finite support alone would not ensure finite-dimensional generated subalgebras in arbitrary solvable Lie algebras.

By the injectivity of s(H) → s(L), both selected last-nonzero witnesses survive in s(H). By functoriality of every series under Poisson inclusions, each of the ambient zero-stage identities still vanishes in s(H). Thus neither invariant increases, and neither can drop below its selected nonzero witness. The exact pair a,b is preserved. This reasoning does not assume the unequal witnesses use the same support; their finite union is taken.

Verdict: accepted. The characteristic-2 solvability case is deliberately excluded, since the cited necessity theorem is not available there.

## 10. Specialization, zero identities, and finite residue fields

Fix a finite-dimensional H over F, a basis e₁,…,e_d, and its finitely many structure constants. The p^d truncated monomials form a fixed finite basis for s(H). All structure coefficients of multiplication and the Poisson bracket on that basis are polynomials over F_p in the Lie structure constants.

Each relevant fixed series stage is the span of evaluations of a multilinear bracket/product expression. The strong lower polynomial adds one bracket variable and one multiplier variable at each step. The strong derived polynomial takes two copies with disjoint variable sets, brackets them, and adds an independent multiplier. Ordinary polynomials omit multipliers. The recursive descriptions in the candidate therefore remain multilinear, even over finite fields. Multilinearity, not a claim about arbitrary polynomial functions over finite fields, is what reduces universal vanishing to finitely many monomial-basis substitutions.

Choose one nonzero output coefficient f and g from basis-input evaluations at the two preceding nonzero stages. The indexing is correct: gamma_a for ordinary class a, U_(b−1) for strong class b, and index a−1 or b−1 for derived lengths. If a stage is nonzero on arbitrary inputs, multilinear expansion guarantees a nonzero basis-input evaluation.

Let A₀ be the actual F_p-subalgebra of F generated by all structure constants, and set A = A₀[(fg)⁻¹]. Since f and g are nonzero elements of a field, this is a nonzero finitely generated F_p-algebra. Inverting fg makes both f and g units individually. It is important that A₀ is the actual coefficient subring, with all relations inherited from F, not a polynomial ring on formally independent structure constants.

The free A-module with basis e₁,…,e_d is a Lie algebra because alternation and Jacobi are polynomial relations already zero in the subring A ⊆ F. Alternation is retained explicitly in characteristic 2. The truncated symmetric algebra remains free over A on the specified p^d basis: its defining ideal is generated by the basis pth powers, and monic monomial relations introduce no coefficient torsion.

For every basis-input evaluation of each needed zero stage, every output coefficient is zero in F and hence zero in A, by injectivity of the subring inclusion. All these zero equations survive every quotient of A. It is not enough merely to preserve the two nonzero evaluations; the candidate correctly preserves every relevant zero identity as well.

Choose any maximal ideal m of A. Its quotient k = A/m is a field, finitely generated as an algebra over F_p. Zariski's lemma says it is a finite algebraic extension, so k is a finite field, not just a field of finite transcendence degree. The characteristic stays p because the homomorphism from F_p to the nonzero quotient field is injective.

The supplied proof of Zariski's lemma is sound. Select a maximal algebraically independent subset t₁,…,t_r of a finite algebra-generating set and clear denominators in monic equations for the remaining algebraic generators by one nonzero h. The resulting field is integral over B = F_p[t₁,…,t_r,1/h]. If a field is integral over B, every nonzero b in B has its inverse in B, by its integral equation, so B is a field. When r > 0, an irreducible polynomial in F_p[t₁] not dividing h stays nonunit after adjoining the other variables and localizing at h. Such an irreducible exists by Euclid's argument. This contradiction forces r = 0 and hence a finite algebraic degree. The same argument works with any ground field.

After reduction modulo m, the free module still has exactly d basis elements. All zero-stage evaluations vanish; the units f and g have nonzero images. Consequently both invariants are exactly the original a,b. This simultaneously preserves finiteness of the ordinary and strong invariants, not merely a nonzero word. Nilpotence or solvability of the specialized Lie algebra follows from its embedding in its own truncated symmetric algebra.

Nothing requires m to have prime-field residue. For example, F₃[t]/(t²+1) is a finite coefficient ring which is already the field F₉ and has no F₃-valued point. The audit explicitly checks an F₉-coefficient Heisenberg example. This illustrates why replacing “finite field” with “prime field” would not be justified by the presented descent argument; it does not purport to disprove every conceivable stronger prime-field reduction.

Verdict on Theorem D: accepted. No dimension bound, extension-degree bound, exhaustive finite search, preserved isomorphism type, or actual counterexample is furnished.

## 11. Independent exact computations and negative controls

The auditor implementation was authored independently before reading the candidate's programs. It constructs the truncated basis, computes brackets by choosing removed generator factors and applying Leibniz, and computes exact subspaces by field row reduction. Strong stages are closed under multiplication by algebra generators with a queue until no new basis row appears. This equals closure under all monomials and their linear combinations. The implementation uses explicit exceptions, not Python assertions.

No candidate or source-author program was imported or executed. The candidate's four Python files were later inspected as text only. Its expected-dimension JSON was read only as inert comparison data after the independent computations.

The final suite independently computes 31 cases, including all 25 candidate cases; all 80 candidate stored full dimension vectors agree. It adds abelian baselines, a direct sum, a central direct-summand check, a characteristic-2 derived-length boundary example, and a nonprime F₉ coefficient example. It checks entire affine derived subspaces against the stated y-power ideals, not just their dimensions.

Further exact checks include:

- Filiform maximal words, every intermediate pair and terminal step, at p = 2,3,5,7,11,13.
- Quadratic-space bracket ranks at the same primes, including the rank drop at p = 2 and rank 6 at p = 3.
- All 64 alternating maps F₂³ × F₂³ → F₂² and all 729 analogous maps over F₃: all 42 and 624 maps respectively with two-dimensional total image have a full-image adjoint element.
- A separate literal-factor implementation agrees on all 7,610 ordered basis pairs in four selected algebras.
- Ambient Jacobi and Leibniz checks on 4,716 triples: exhaustive where the truncated algebra has dimension at most 16, with deterministic selected triples in the two larger cases.
- Explicit rejection of a false condition, an alternating non-Lie table, a wrong bracket expectation, forcing t²+1 = 0 into F₃, and attempting to invert a zero witness.

The historical independent computation reproduced the candidate's characteristic-3 filiform example with [x,y]=z and [x,z]=w. Both classes are 7, even though the intermediate spaces differ, and both derived lengths are 3. The raw dimension-vector tables are omitted; this finite example supports the analytical proof rather than establishing a universal result.

A useful out-of-scope negative boundary is the six-dimensional characteristic-2 Lie algebra with basis x,y₁,…,y₅ and [x,yᵢ] = yᵢ. The saved independent finite calculation gives ordinary and strong derived lengths 3 and 4, respectively; its raw dimension-vector table is omitted. Thus a checker that silently extended Question 2's equality claim to p = 2 would be rejected. This example is finite corroborating boundary evidence; it is not a new claim of novelty.

Ordinary, -O, and -OO runs have identical mathematical results. Each arithmetic negative control and all seven separate temporary-copy seal controls are active in each optimization mode. The seal controls reject changed content with unchanged byte count, a missing member, an extra file, a changed manifest, a changed outside seal, a member symlink, and a directory symlink. Original artifacts are reauthenticated after controls.

During checker development, a guessed four-y-variable version of the characteristic-2 negative example was rejected by the actual computation: it has equal derived lengths 3,3. The final boundary fixture uses five y variables and was verified explicitly. This was a corrected test-fixture expectation, not a defect in the candidate's statements or an unreported candidate modification.

All finite checks remain corroboration only. The arbitrary-field, arbitrary-dimension, and unbounded-specialization statements stand on the preceding mathematical proofs and correctly scoped published inputs.

## 12. Editorial clarifications and final boundaries

Two optional wording improvements from the original audit have been applied in this prose edition:

1. Siciliano's contribution is listed under its actual title, *Solvability of symmetric Poisson algebras*, followed by the workshop title as its venue. The original candidate used the workshop title in that source entry. The source identity, pages, and questions were otherwise correct.
2. The original candidate's “Basic algebra and central extensions” heading is now “Basic algebra and central direct summands.” The proof already explicitly assumed a central direct summand, so this is a heading clarification, not a missing hypothesis or proof correction.

Neither clarification changes a theorem or is a condition on this mathematical acceptance. The sealed candidate has not been edited.

The unrestricted nilpotency question remains unsettled by the accepted arguments beyond the specified families. In particular, general class-two bracket maps lacking a full-image adjoint vector and higher-class algebras with larger derived subalgebra are not settled universally. The independent free-two-step rank-three computation does not close that gap.

The unrestricted derived-length question remains unsettled beyond dim L' ≤ 1 by these proofs. No implication from nilpotency-class equality to derived-length equality is assumed. The finite-field reduction is unbounded in dimension and field degree. Both full-question resolution flags remain false, and no novelty claim is made.

The original audit did not change the candidate, sources, repository branches, or remote publication state. Editorial preparation likewise left the original candidate and audit unchanged and did not rerun mathematical programs.
