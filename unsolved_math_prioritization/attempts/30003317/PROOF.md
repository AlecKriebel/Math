# Corrected edition: fixed-restriction surreal derivations

Problem 30003317 / OWR-15181-008. The original existential question is unresolved by this work. No novelty or priority is claimed.

AI-assisted, unrefereed authored mathematics with an independent internal AI audit. This is not external human peer review or formal proof-assistant certification.

Only authored mathematical prose, the exact correction, acceptance records and public verification metadata are distributed. No executable code, raw datasets, copied source documents, extracted source text, source images, raw search responses or private coordination material are included. This is not a computational reproduction package.

## Edition and correction notice

The complete authored proof follows, with the audit's exact one-line Lemma 2 scope correction applied to a separate copy. The hypothesis now says that |a| is infinite or infinitesimal, equivalently that a is not Archimedean-equivalent to 1. Every other original proof byte is preserved. Before this editorial wrapper, the corrected proof is 21,364 bytes with SHA-256 7f5390fe1b7a3092022cfdf701a42d242a32bd3bec299682272a754d87e1f6b1.

The complete independent audit is retained in AUDIT.md. It supplies detailed summability, set-valued NBG recursion and inverse-automorphism arguments supporting the compressed steps in the proof. Those explanations impose no additional assumptions or further required corrections. Acceptance is of corrected partial reductions and obstructions, relative to the explicitly cited published structural inputs. The underlying published nested-truncation theory and complete canonical-construction machinery are not independently reproved here.

The full target concerns two distinct surreal derivations on all of No agreeing on the entire exp/log/summation closure K=R⟨⟨L⟩⟩. Neither nonuniqueness nor uniqueness is proved. The historical and bounded literature observations are not a certificate of present literature-wide openness.

## Complete corrected authored proof

# Fixed-restriction surreal derivations: reductions and obstructions

## Status and exact question

This is a partial mathematical attempt on OWR-15181-008, upstream ID 30003317. It does **not** construct two distinct surreal derivations with the same prescribed restriction and does **not** prove uniqueness. No resolution of the original question is claimed. The results below are deductions from published structural facts, with full arguments for the deductions. No novelty claim is made for them.

Let No be the proper class of surreal numbers, M its group of positive monomials, J its additive group of purely infinite numbers, and L its class of log-atomic numbers. Thus M = exp(J). Let

    K = R⟨⟨L⟩⟩

be the smallest subfield of No containing R and L and closed under exp, log on positive elements, and sums of summable set-indexed families. This is not the ordinary field R(L). The question is whether there exist distinct surreal derivations D0,D1 on all of No with D0|K = D1|K.

A surreal derivation satisfies Leibniz's rule, strong additivity, exponential compatibility, kernel R, and D(x)>0 for x>R. Strong additivity includes preservation of summability, not merely equality when both sums happen to exist. Surjectivity is not part of the question.

We work with class functions in NBG with global choice, as is usual when discussing all of No. Every individual normal-form support, summable family, path tree, ordinal stage, and cut used below is a set. A collection of class functions is not itself asserted to be a class in NBG. Statements about a family of derivations below mean that a single class function of two arguments explicitly supplies the family.

For nonzero b, write a ≺ b when |a| < |b|/n for every positive integer n; write a ∼ b when a-b ≺ b. These relations use the natural valuation. A reverse well-ordered set of monomials is one in which every nonempty subset has a largest member. A family is summable when the union of supports is reverse well ordered and each monomial occurs in only finitely many supports.

## Published inputs

[BM] Berarducci–Mantova, *Surreal numbers, derivations and transseries*, arXiv:1503.00315v3, later JEMS 20 (2018), 339–390, https://arxiv.org/abs/1503.00315. Numbering and printed page references here refer to the 47-page arXiv v3.

1. Every surreal has a unique normal form Σ r_m m. Multiplication distributes over summable families. The exponential of an infinitesimal is its usual power series. See [BM, Sections 2.3–2.4 and 3].
2. The intrinsic dominant path of every non-real surreal reaches L after finitely many steps. This is [BM, Corollary 5.11 and the first paragraph of Lemma 6.23], pp.27 and 35. It is a property of the exponential/series structure, independent of the choice of derivation.
3. No satisfies the path condition T4, [BM, Theorem 8.10], pp.43–44. Eventually a path has coefficient ±1 and no terms to its right in the next logarithm.
4. [BM] constructs a surreal derivation ∂BM from monomial-valued data on L by summing the derivatives of paths which enter L, assigning zero to other paths. See Definitions 6.13, 6.21, Theorem 6.30, and Remark 6.31. Its restriction maps K into K.

The proofs of these major structural results are not reproved here. The inspection record distinguishes the published inputs from the deductions proved below.

## 1. Agreement on L is equivalent to agreement on K

**Lemma 1.** Let D0,D1 be strongly additive exponential derivations on No that vanish on R. If they agree on L, they agree on K.

**Proof.** Put E = D1-D0. The difference is strongly additive: for a summable family, the two image families are summable, and the union of their two reverse well-ordered supports is reverse well ordered, with finite multiplicities. It is an ordinary derivation, vanishes on R and L, and satisfies E(exp x)=exp(x)E(x).

The zero class Z={x:E(x)=0} is a subfield. Indeed, addition and multiplication follow from the derivation rules, and E(x^{-1})=-x^{-2}E(x). If x∈Z, then exp x∈Z. If x>0 belongs to Z, then E(log x)=E(x)/x=0. Finally, if (x_i) is a summable set-indexed family in Z, strong additivity gives E(Σ x_i)=Σ E(x_i)=0. Hence Z contains the entire defining closure K. The converse follows from L⊆K. ∎

This does not require K to be a set, nor an ordinary finite-expression generation argument.

## 2. Every extension in a fixed family has the same leading derivative

**Lemma 2 (dominance calculus).** For any surreal derivation D, let a be nonzero with |a| either infinite or infinitesimal (equivalently, a is not Archimedean-equivalent to 1). Then:

    b ≺ a  ⇒  D(b) ≺ D(a),
    b ∼ a  ⇒  D(b) ∼ D(a).

**Proof.** Signs can be absorbed into real constants. First let a>0 be infinite and |b|≺a. For every real t, a+tb is positive infinite, so D(a)+tD(b)>0. Therefore |D(b)|<D(a)/n for every positive integer n.

Next let a>0 be infinitesimal and |b|≺a. Each a+tb is positive infinitesimal. Its inverse is positive infinite, so

    D((a+tb)^{-1}) = -(D(a)+tD(b))/(a+tb)^2 > 0.

Thus D(a)+tD(b)<0 for every real t, again giving |D(b)|≺|D(a)|. The second assertion follows by applying the first to b-a. ∎

This is the argument of [BM, Proposition 6.4], included to make the reduction explicit.

For x∉R, remove its real normal-form coefficient and take its largest remaining term q0. Recursively take q_{i+1} to be the largest term of log|q_i| after removing its real part. This is the dominant path. The published termination fact gives a finite k with q_k∈L.

**Theorem 3 (leading-term rigidity).** If D0 and D1 are surreal derivations agreeing on L, then

    D1(x) ∼ D0(x)     for every x∉R.

More precisely, for the intrinsic dominant path just described, every surreal derivation D satisfies

    D(x) ∼ (q0 q1 ··· q_{k-1}) D(q_k).

**Proof.** Write x=r+u, where r is its real coefficient. Then u∼q0 and u is either infinite or infinitesimal in magnitude. Lemma 2 gives D(x)=D(u)∼D(q0).

For each i<k, write q_i=r_i m_i, with r_i∈R× and m_i∈M. Then

    D(q_i)=q_i D(log m_i).

The purely infinite number log m_i has leading term q_{i+1}. By Lemma 2,

    D(log m_i) ∼ D(q_{i+1}),

and hence D(q_i)∼q_i D(q_{i+1}). All quantities compared are nonzero. A finite product of factors of the form 1+ε, with ε infinitesimal, is again 1+an infinitesimal. Iterating yields the formula. Its right-hand side is identical for D0 and D1 because q_k∈L. ∎

**Important limit.** Theorem 3 proves equality of the leading monomial and leading real coefficient of the derivatives. It does not prove equality of their entire normal forms. The dominant path is only one path; the other paths are precisely where an extension difference could be hidden.

## 3. Exact affine description and a proper-class family consequence

Fix one surreal derivation D. Call a class function E:No→No an admissible homogeneous perturbation of D if:

- E is a strongly additive derivation and E(exp x)=exp(x)E(x);
- E vanishes on R∪L;
- E(x)≺D(x) for every x∉R.

**Theorem 4.** A class function D' is a surreal derivation agreeing with D on K if and only if D'=D+E for an admissible homogeneous perturbation E. It is distinct from D if and only if E is nonzero.

**Proof.** For necessity, take E=D'-D. The algebraic, exponential, and summation requirements follow by subtraction; Lemma 1 gives the restriction statement, and Theorem 3 gives the strict asymptotic bound.

For sufficiency, D+E is a strongly additive exponential derivation. It vanishes on R and agrees with D on K by Lemma 1. If x∉R, then (D+E)(x)∼D(x)≠0, so its kernel is exactly R. If x>R, the same equivalence gives (D+E)(x)>0. Thus every required axiom holds. ∎

**Corollary 5.** If one nonzero admissible E exists, then for every finite surreal c the map

    D_c(x)=D(x)+cE(x)

is a surreal derivation with the same restriction to K. Distinct c give distinct derivations. In particular, two distinct extensions imply a proper-class-sized explicitly parametrized family of extensions.

**Proof.** Multiplication of a derivation by any field element preserves Leibniz's rule and exponential compatibility. It also preserves strong additivity because multiplication by a fixed surreal preserves summability. If |c| is bounded by a positive integer, E(x)≺D(x) implies cE(x)≺D(x). Hence cE is admissible.

Choose a with E(a)≠0. Then D_c(a)-D_d(a)=(c-d)E(a), which is nonzero when c≠d. The map z↦z/(1+|z|) injects No into the finite interval (-1,1). Thus the single class function

    (z,x) ↦ D(x) + [z/(1+|z|)] E(x)

has pairwise distinct sections, each an extension. This formulation avoids treating a collection of proper-class functions as a set or class of NBG. ∎

The conclusion is only for finite scalar multiples. It is not asserted that arbitrary infinite scalar multiples retain positivity.

## 4. A monomial fixed-point criterion

The previous description can be reduced to data on M. Fix a surreal derivation D. Let c:M→No be a class function and put w(m)=m c(m). Consider these four conditions:

**(W)** For every reverse well-ordered set S⊆M, the family (w(m))_{m∈S} is summable.

**(F)** For every m∈M, writing log m=Σ_n r_n n in normal form, one has

    c(m) = Σ_n r_n n c(n).

The sum in (F) is defined by (W). In particular (F) at m=1 gives c(1)=0.

**(L0)** c(λ)=0 for every λ∈L.

**(B)** m c(m)≺D(m) for every m∈M\{1}.

**Theorem 6.** There is a surreal derivation D'≠D with D'|K=D|K if and only if there is a nonzero class function c satisfying (W), (F), (L0), and (B). Given c, the extension is

    D'(Σ_m r_m m) = D(Σ_m r_m m) + Σ_m r_m m c(m).

**Proof.** Suppose first D' exists. Set E=D'-D and c(m)=E(m)/m. Condition (W) follows by applying strong additivity of E to the summable family of distinct monomials in S. Exponential compatibility gives

    c(m)=E(log m)=Σ_n r_n E(n),

which is (F). Agreement on L gives (L0), and Theorem 3 gives (B). If c were zero, strong additivity would force E=0.

Conversely suppose c satisfies the four conditions. By (W), define the strongly R-linear map

    E(Σ_m r_m m)=Σ_m r_m w(m).

Here is why normal-form summability is enough for full strong additivity. If (x_i) is summable, its monomial union S is reverse well ordered and each m∈S occurs in only finitely many x_i. The image family obtained by expanding each x_i has supports contained in the summable family (w(m))_{m∈S}; each w(m) is repeated only finitely many times. At any output monomial, only finitely many input m contribute by (W), and each of those occurs only finitely often. Thus the expanded image family is summable and may be regrouped, proving E(Σ_i x_i)=Σ_i E(x_i).

Equation (F) says c(m)=E(log m). Consequently

    c(mn)=E(log m+log n)=c(m)+c(n).

Therefore E(mn)=mE(n)+nE(m) for monomials m,n. The identity extends to arbitrary normal forms by infinite distributivity. The two relevant double families are summable: one is the product of the normal-form family of x with the summable derivative family of y, and the other is its counterpart with x,y reversed. The usual Hahn multiplication lemma supplies the product summability. Thus E is a derivation.

For γ∈J, m=exp γ is a monomial and (F) gives

    E(exp γ)=exp(γ)E(γ).

For real r, E(r)=0 because c(1)=0. For infinitesimal ε, strong additivity applied to exp ε=Σ_{n≥0} ε^n/n!, together with Leibniz's rule, gives

    E(exp ε)=Σ_{n≥1} ε^{n-1}E(ε)/(n-1)!=exp(ε)E(ε).

Every x has the form γ+r+ε, so multiplication of these three exponential factors proves exponential compatibility for every x. Condition (L0), followed by Lemma 1, makes E vanish on K.

It remains to promote (B) from monomials to all non-real x. Remove the real coefficient of x and let r0 m0 be the largest remaining term. Lemma 2 gives D(x)∼r0 D(m0). For every other support monomial m<m0, Lemma 2 gives D(m)≺D(m0). Condition (B) implies that every support monomial of every r_m E(m) is strictly smaller than the leading monomial of D(m0). The image family is summable by (W), so the same is true of its sum E(x). Hence E(x)≺D(x). Theorem 4 applies. Nonzero c yields nonzero E by evaluating at a monomial. ∎

This is an exact criterion for a fixed D, not a solution of its homogeneous fixed-point system. The full existential question asks whether the criterion has a nonzero solution for at least one surreal derivation D. Establishing uniqueness only for ∂BM would not by itself settle that existential question.

## 5. Surjectivity is constant within a fixed-restriction family

We give the transfinite argument, rather than treating the proper-class field No as a set-sized maximal Hahn field. The argument is adapted from [BM, Lemma 7.5 and Proposition 7.6], pp.39–40.

**Lemma 7 (class pressing-down lemma).** If f:On\{0}→On is a class function with f(α)<α for every nonzero α, then at least one fiber f^{-1}(β) is a proper class.

**Proof.** Suppose every fiber is a set. Set g(0)=1 and define a strictly increasing continuous class function g:On→On such that g(α+1) is greater than every member of f^{-1}(β), for all β≤g(α), and greater than g(α). This is possible at each successor stage because only a set of set-sized fibers is involved. At limit stages take the supremum of the previous values. Choose α=sup_{n<ω} g^n(1). Then α is a nonzero limit ordinal and continuity gives g(α)=α. Since f(α)=β<α, choose ξ<α with β≤g(ξ); the successor construction gives α∈f^{-1}(β) and hence α<g(ξ+1)<g(α)=α, a contradiction. ∎

**Lemma 8 (asymptotic integration suffices on No).** If D is a surreal derivation and every nonzero f has an asymptotic integral, meaning D(y)∼f for some y, then D is surjective.

**Proof.** Choose a class function A assigning to each nonzero f a single nonconstant term A(f)=r m, m≠1, with D(A(f))∼f. To obtain it, choose an asymptotic integral y, subtract its real coefficient, and take its leading term; Lemma 2 preserves asymptotic differentiation. The class choice can be made by selecting a witness of least birthday and then using a fixed well-order on the set of witnesses at that birthday.

Fix f≠0. Define terms t_α recursively until the process stops:

    R_α = f - Σ_{β<α} D(t_β),
    t_α = A(R_α)  if R_α≠0.

At every stage α that is an ordinal, the earlier terms form a set. We prove inductively that t_β strictly decrease in magnitude, and that D(t_β) also strictly decrease in magnitude. Suppose the earlier stages are defined. For γ<α,

    R_α = [R_γ-D(t_γ)] - Σ_{γ<β<α} D(t_β).

The first term is ≺D(t_γ), by the defining asymptotic equivalence. The tail is likewise ≺D(t_γ): its image family is summable by strong additivity, and each constituent has leading monomial below that of D(t_γ). Hence R_α≺D(t_γ). Since D(t_α)∼R_α, the derivatives strictly decrease. Lemma 2 and comparability of monomials then force t_α≺t_γ. Thus the terms themselves are summable at every set-sized stage, and all displayed sums are legitimate.

Assume the recursion never stops. Let m_α be the leading monomial of R_α. The m_α strictly decrease, hence are pairwise distinct. For α>0, the monomial m_α occurs either in f or in D(t_β) for some β<α. Put S_0=supp(f)∪supp(D(t_0)) and S_β=supp(D(t_β)) for β>0. Choose the least h(α)<α with m_α∈S_{h(α)}. Lemma 7 gives a proper-class fiber of h. Since α↦m_α is injective, that would inject a proper class into one set S_β, impossible in NBG. Therefore the recursion stops at an ordinal α, and strong additivity gives

    f = Σ_{β<α} D(t_β) = D(Σ_{β<α} t_β).

There is no proper-class sum in this argument. ∎

**Theorem 9.** If D0,D1 are surreal derivations with the same restriction to L, then D0 is surjective if and only if D1 is surjective.

**Proof.** If D0 is surjective, for each f≠0 choose y with D0(y)=f. By Theorem 3, D1(y)∼f. Thus D1 has asymptotic integration and is surjective by Lemma 8. Interchange the two derivations for the converse. ∎

In particular, every hypothetical extension of the canonical ∂BM|K is surjective. This does not assume surjectivity in the target definition and does not identify the extensions.

## 6. What a nonzero defect must do on paths

**Lemma 10.** Let E be a nonzero strongly additive exponential derivation vanishing on R∪L. Then some surreal has a path P all of whose terms have nonzero E-value. Such a path never enters L and is eventually right-trailing in the sense of T4.

**Proof.** Choose x with E(x)≠0. Strong additivity yields a non-real normal-form term P(0) with E(P(0))≠0. If P(n)=r m, then E(P(n))=P(n)E(log m). The latter is nonzero. Expanding log m and using strong additivity yields a term P(n+1) of log m with E(P(n+1))≠0. Choose the first such term in its reverse well order. This recursively constructs a countable path. No P(n) belongs to L, because E vanishes there. Published T4 gives the eventual right-trailing property. ∎

The converse has not been proved: the existence of a path avoiding L does not manufacture a global E satisfying (W).

**Lemma 11 (set-sized boundary data do not force zero).** Given any set-indexed family of positive surreals (b_i), there is c>0 with c≺b_i for every i. Consequently, for any sequence a_n≠0 and positive sequence u_n, the formal system

    d_n=a_n d_{n+1},     |d_n|≺u_n   (n≥0)

has a nonzero solution in No.

**Proof.** The cut with left set {0} and right set {b_i/k:i∈I, k≥1} is a legitimate set cut, so choose c strictly between its two sides. For the second assertion, put A_0=1 and A_n=a_0···a_{n-1}, choose c≺|A_n|u_n for every n, and put d_n=c/A_n. ∎

This only addresses one formal chain of equations. It proves neither the existence of an actual surreal derivation nor compatibility of different paths, products, or all summable families. There is no analogous argument for a proper class of bounds: a positive c cannot be below every positive surreal, since c/2 is itself positive.

## 7. Two obstructions to automorphism and infinitesimal-flow shortcuts

**Lemma 12.** There is no nonzero exponential-compatible derivation E on No with E(x)≺x for every nonzero x.

**Proof.** Applying the assumed contraction to exp x gives E(x)=E(exp x)/exp x≺1 for every x. Suppose d=E(a)≠0 and set b=1/d, so b is infinite in magnitude. Let ε=E(ab), which must be infinitesimal. Leibniz gives aE(b)=-1+ε, so

    E(ab²)=b(2aE(b)+1)=b(-1+2ε),

which is infinite in magnitude. This contradicts E(ab²)≺1. ∎

Thus the smallness E(x)≺D(x) in Theorem 4 cannot be replaced by global valuation contraction E(x)≺x. In particular one cannot simply choose a globally infinitesimal derivation and exponentiate it as a universal formal flow. The related automorphism obstruction is [KKS, Proposition 5.2]: every strongly R-linear exponential-field automorphism that preserves the leading term of every surreal is the identity. The current v3 proof was inspected. [KKS] is Kaplan–Krapp–Serra, *Decomposing the automorphism group of the surreal numbers*, arXiv:2509.22374v3, https://arxiv.org/abs/2509.22374, Proposition 5.2, PDF p.10. This is a result about automorphisms, not a uniqueness theorem for surreal derivations.

**Lemma 13 (naturality blocks monomial-preserving conjugation).** Let σ be a strongly R-linear exponential-field automorphism of No that maps M onto M and fixes L pointwise. Then σ commutes with ∂BM. Consequently, conjugation by such a σ cannot produce a second extension of ∂BM|K.

**Proof.** Since σ fixes R∪L and respects the defining operations and sums, it fixes K pointwise. In particular it fixes ∂BM(λ) for every λ∈L, by [BM, Remark 6.31].

Because σ and σ^{-1} preserve monomials, coefficients, exp, and normal-form sums, P↦σ∘P is a bijection from the paths of x to the paths of σ(x). A path enters L precisely when its image does. If P first enters L at step k, its path derivative is

    P(0)···P(k-1) ∂BM(P(k)).

Applying σ gives the path derivative of σ∘P. If P never enters L, both path derivatives are zero. Strong additivity therefore commutes σ with the summable path-derivative family, giving σ(∂BM x)=∂BM(σ x). ∎

Bagayoko's later *Hyperseries subfields of surreal numbers*, arXiv:2409.16251v2, https://arxiv.org/abs/2409.16251, supplies monomial-preserving embedding constructions (Definition 3.6, Proposition 5.9, Theorem 6.3). Applying such machinery requires checking its exact hypotheses. Even if it supplies an automorphism fixing L, Lemma 13 shows why conjugating ∂BM by a monomial-preserving one does not answer the present question. No stronger claim about all exponential-field automorphisms is being made.

## Remaining mathematical gap

The unresolved requirement is a nonzero globally well-based solution c of (F), vanishing on all L, with bound (B), for at least one surreal derivation D. Known nonterminating paths supply places where homogeneous freedom might occur, but no construction here reconciles that freedom with (W) over every reverse well-ordered set. Conversely, neither dominant-path rigidity, valuation-contractive rigidity, nor uniqueness of the canonical path-sum recipe proves c=0.

Accordingly the original existential problem remains unresolved in this attempt.
