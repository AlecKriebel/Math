# AI-assisted literature audit of Schubert classes in the gamma filtration

Problem 30003042 / OWR-14213-008. Audit date: 11 October 2026 UTC.

This is an AI-assisted mathematical analysis and editorial reconstruction of published work. It has not received external human review, journal acceptance, or formal certification. The underlying Spin index result is published. Its Maple computation was not rerun. “Accepted” below means acceptance of the stated literature-derived inference within this analysis, not peer review or certification.

## Verdict

**ACCEPTED AS A LITERATURE-DERIVED NEGATIVE RESOLUTION.** The universal assertion is false already at **n = 8**, with the original maximal-even-Clifford-index and Severi–Brauer function-field hypotheses retained. The conclusion is that the specified special class **e₈ belongs to γ⁵K(X over F(S))** in an instance of the original setup, whereas the conjecture excludes that membership.

This is an inference from published results, including a published computer-assisted index computation. It is not a newly proved Spin index theorem, an independent replay of Maple, an explicit newly computed Schubert-polynomial certificate, or a novelty claim. The parameter-specific conclusion is justified by the actual proof of Karpenko's implication, not merely by taking the contrapositive of two universal statements.

The bridge between the two meanings of “generic” uses the maximality/divisibility property of generic-torsor indices. It does not require asserting that every 2016 Clifford-splitting model is itself the particular generic torsor used in the later paper.

## 1. Sources and version control

The labels below refer to primary sources. Numerical page references to preprints are their printed pages, which coincide with PDF page numbers. Source byte counts, SHA-256 hashes, URLs, and inspection scopes are recorded in `SOURCE_VERIFICATION.json`.

**[O] Original question.** Nikita Karpenko, “Grothendieck ring of maximal orthogonal Grassmannian,” in *Algebraic Cobordism and Projective Homogeneous Varieties*, Oberwolfach Report 5/2016, contribution at pp. 226–227, PDF pp. 12–13. The target is Conjecture 3 on p. 227. DOI: https://doi.org/10.4171/OWR/2016/5. PDF: https://ems.press/content/serial-article-files/46609.

**[A] Expanded statement and implication.** Nikita A. Karpenko, *Around 16-dimensional quadratic forms in I_q^3*, final author preprint dated 29 November 2015, revised 4 June 2016, 13 pages. Published in *Mathematische Zeitschrift* 285 (2017), 433–444. Final preprint: https://sites.ualberta.ca/~karpenko/publ/a16i5.pdf. Important pins: pp. 3–5, §1 and the definition following Corollary 1.6; p. 5, Remark 2.2; p. 8, Conjecture 3.3 and the start of §4; pp. 9–10, Proposition 4.2 and Theorem 4.3; p. 11, Remark 4.5, the paragraph on extension of fields, and Conjecture 4.7; p. 12, the complete proof of the implication and Remark 4.8. The older a16i3.pdf is not the version used here.

**[K-pre] Original exact-index computation, final preprint.** Nikita A. Karpenko, *On generic flag varieties for odd spin groups*, dated 5 May 2021, revised 23 November 2021, 11 pages: https://sites.ualberta.ca/~karpenko/publ/spindI15.pdf. Important pins: §1 for arbitrary characteristic and generic torsors; §3 for the Chow-ring description; p. 7, Theorem 4.1 and §5; p. 8, §6; pp. 9–10, Appendix A.

**[K-journal] Published exact-index computation.** The same article in *Publicacions Matemàtiques* 67(2) (2023), 743–756, DOI https://doi.org/10.5565/PUBLMAT6722310. Publisher record: https://mat.uab.cat/pubmat/articles/view_doi/10.5565/PUBLMAT6722310. The journal PDF was independently retrieved through that record's Article link. The relevant §5 is on p. 751; §6 begins on p. 751 and its final index list is on p. 752, PDF pp. 9–10. These pages were both textually and visually inspected and agree with [K-pre] on the relevant computation, deduction, and values. The theorem number 4.1 is unchanged.

**[KM] Independent later summary and version warning.** Nikita A. Karpenko and Alexander S. Merkurjev, *Indexes of generic Grassmannians for spin groups*, final author preprint dated 13 November 2021, revised 7 May 2022, 15 pages: https://sites.ualberta.ca/~karpenko/publ/spindh19.pdf. Published in *Proceedings of the London Mathematical Society* 125(4) (2022), 825–840, DOI https://doi.org/10.1112/plms.12471. Pins: §§1–2 for definitions and characteristic scope; p. 4, Lemma 2.3; p. 5, prose following Theorem 3.6 identifying the deviation interval for dimensions 17 and 18; p. 14, Appendix B; p. 15, reference [4] to the 23 November 2021 final preprint.

**[DKM] Precise genericity bridge.** Rostislav A. Devyatov, Nikita A. Karpenko and Alexander S. Merkurjev, *Maximal indexes of flag varieties for spin groups*, *Forum of Mathematics, Sigma* 9 (2021), e34, 1–12, DOI https://doi.org/10.1017/fms.2021.30. Journal PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/D86A1DAABD2D66EF47122854AAD4BAE6/S205050942100030Xa.pdf/div-class-title-maximal-indexes-of-flag-varieties-for-spin-groups-div.pdf. Pins: pp. 1–2, odd forms, similarity and torsors; p. 3, Proposition 2.1 and its preceding explanation; pp. 8–9, the even-dimensional introduction. Proposition 2.1 was also visually inspected.

**[P] Author's publication page**, inspected and saved on the audit date: https://sites.ualberta.ca/~karpenko/publ/. It identifies the above final preprint versions and publications. It warns that the journal Appendix B of [KM] was corrupted and directs readers to the final preprint. It also says the first 3 in each of the dimension-17 and dimension-18 preprint rows should be underlined. Neither the corrupted journal table nor the underlining is used to obtain the index value here. The value is explicit in [K-pre] §6, [K-journal] pp. 751–752, and the prose on [KM] p. 5.

The three author-hosted final preprints [A], [K-pre], and [KM] were independently downloaded again during this audit. Every new copy was byte-identical to the corresponding previously inspected copy. This confirms which bytes were read; it is not a verification of the papers' proofs.

## 2. Exact original setup

The following information is present in [O] p. 226 and carried into [A] §4:

1. F is a field of arbitrary characteristic, and φ is a nondegenerate quadratic form of odd dimension 2n+1. In characteristic 2, nondegeneracy is the quadratic-form convention used by these sources, not the impossible requirement that an odd-dimensional alternating polar form be nonsingular.
2. X is the orthogonal Grassmannian of n-dimensional totally isotropic subspaces of φ.
3. A = C₀(φ) has maximal index 2ⁿ. Since its degree is 2ⁿ, A is a division algebra.
4. S is the ordinary Severi–Brauer variety SB(A), and the field in the target is K = F(S). This kills the Clifford invariant by a function-field extension; it does not assert that φ itself is split over K.
5. The class e_n is the K-theoretic special Schubert class corresponding to a point on the split quadric. Over K it is understood through the splitting-field identification of K-theory. An actual rational Schubert subvariety or a rational point on the original anisotropic quadric is not being assumed.
6. The target excludes e_n from γ^(n+1−floor((n+1)/2))K(X_K) for all n ≥ 8.

At n = 8 these conditions say dim φ = 17, ind C₀(φ) = 256, S = SB(C₀(φ)), and e₈ is supposed not to lie in γ⁵K(X_K). The full original statement [O], Conjecture 3, and [A], Conjecture 4.7, have the same class, field, threshold, and range of n.

The scalar 18 used in the index theorem is the dimension of an auxiliary even form. It is not the dimension of the original odd form. Also, the later papers use m for an isotropic-subspace dimension, whereas Conjecture 3.3 of [A] uses m for the dimension of the whole quadratic form. The following argument uses d for the latter and r for the former to avoid this collision.

## 3. The two generic constructions and the needed bridge

### 3.1 The model required by the 2016 proof

Take an even nondegenerate form ψ over F with dimension d = 2n+2, trivial discriminant, and division half-Clifford algebra C⁺(ψ) of degree 2ⁿ. Set A = C⁺(ψ), S = SB(A), and K = F(S).

Then q = ψ_K has trivial discriminant and Clifford invariant, hence belongs to I_q^3(K). The text following [A], Corollary 1.6, calls forms constructed this way “generic” for its purposes and states that such models exist over an extension of any chosen base field. This is a deliberately broader convention than fixing a generic fiber of GL(N) → GL(N)/Spin_d.

For any nondegenerate codimension-one subform φ of ψ, [A] pp. 3–4 records

- dim φ = 2n+1;
- C₀(φ) ≅ C⁺(ψ) = A;
- a component X of the maximal Grassmannian of ψ is isomorphic to the maximal Grassmannian of φ.

Thus this construction gives exactly the original φ, X, A, S and K, with maximal Clifford index over F. Its suitability does not disappear merely because the Clifford algebra becomes split over K: that is the intended construction.

### 3.2 What the later exact-index result says

For a generic Spin₁₈-torsor, [K-pre] §6 and [K-journal] pp. 751–752 determine the indices of the Grassmannians of totally isotropic r-planes:

- 2ʳ for r = 1, 2, 3;
- 8 for r = 4, 5;
- 16 for r = 6, 7, 8, 9.

In particular, the fourth index is 8. The Grassmannians use vector-space dimensions: the first is the projective quadric, and the fourth parametrizes isotropic 4-planes, equivalently projective 3-spaces on that quadric. There is no projective-versus-affine off-by-one error.

### 3.3 Why the later result applies to the earlier model

It is unnecessary to prove that q = ψ_K is literally the same generic torsor as in [K-pre]. The appropriate consequence of [DKM], Proposition 2.1, is sufficient.

Let G be a split reductive group, P a parabolic subgroup, E_gen a generic G-torsor, and E any G-torsor. The proposition places the image of CH(E_gen/P) in the split Chow ring inside the image of CH(E/P). In top codimension, these images are respectively

ind(E_gen/P) Z ⊆ ind(E/P) Z.

Therefore ind(E/P) divides ind(E_gen/P). The direction matters: the generic index is a universal upper bound under divisibility. The proposition is valid for a split reductive group generally, not only for odd spin groups; [DKM] pp. 8–9 explicitly relates the even forms of trivial discriminant and Clifford invariant to Spin torsors.

Apply it to G = Spin₁₈, P defining the fourth Grassmannian, and q = ψ_K. Then

ind OG₄(q) divides 8.

This already contradicts the value 2^floor(18/4) = 16 demanded for this very model by [A], Conjecture 3.3. The exact value for an arbitrary member of the broader 2016 class is not required; the upper bound is enough. No assertion that every arbitrary nongeneric 18-dimensional form has index exactly 8 is made.

An alternative bridge follows the route of [K-pre] §6: a 17-dimensional subform has trivial even Clifford algebra, up to the harmless similarity normalization for its discriminant; its fourth Grassmannian has index dividing the generic Spin₁₇ value 8. Its inclusion in the 18-dimensional form implies the same bound for OG₄(q). [DKM] p. 2 verifies that similarity does not change these Grassmannians. The argument above using Spin₁₈ directly is simpler.

## 4. Reconstructing the parameter-specific implication

The following expands the actual paragraph on [A] p. 12 at d = 18. It also explains why a failure at d = 18 produces a failure at n = 8 rather than only an unspecified failure of the universal statement.

Let ψ, F, A, S, K and q = ψ_K be as in §3, with d = 18 and n = 8. Set r = floor(d/4) = 4. The published upper bound gives ind OG₄(q) | 8.

### 4.1 Transferring a linear-space class on the quadric

Let Y be the projective quadric of ψ, so dim Y = 16. Every closed point of OG₄(q), with residue field L, provides a totally isotropic 4-plane over L. Consequently Y_L contains a projective 3-space. Its structure-sheaf class l₃ belongs to T¹³K(Y_L), where T denotes the topological filtration, since 16−3 = 13.

The finite pushforward K(Y_L) → K(Y_K) preserves topological codimension. Under the split K-theory identification used in [A] p. 12, its value on l₃ is [L:K] l₃. The requisite rational K-classes and compatibility are part of the standard quadric/twisted-flag K-theory facts used in that published proof; their existence is not an assertion that these linear spaces are geometrically defined over K.

Because the index divides 8, integral combinations of such degrees give 8. Summing the corresponding transfers therefore yields

8l₃ ∈ T¹³K(Y_K).

This formulation avoids an unnecessary inference that there must be a field extension of degree exactly 8. The index is a gcd; a zero-cycle of degree 8, or a finite integral combination of degrees, suffices. Equivalently one can use the degree not divisible by 16 singled out in [A] and the usual power-of-two splitting degrees.

### 4.2 Extracting the point class without division by 8

The K-theoretic relation invoked on [A] p. 12 specializes to

8l₃ = l₀ + h¹⁵ + 2h¹⁴ + 4h¹³,

where h is the class of a hyperplane section. This is consistent with iterating 2l_j = l_(j−1) + h^(16−j), for j = 1, 2, 3. It is an integral identity, not a rational-coefficient cancellation.

Each hyperplane term on the right belongs to T¹³: its exponent is at least 13. Subtracting those terms gives

l₀ ∈ T¹³K(Y_K).

### 4.3 The incidence correspondence and the important dimension shift

Use the even form ψ, not the odd φ, for this step. Let X be a component of its maximal Grassmannian, so its tautological isotropic subspaces have dimension 9. Let Z = P(T) be the incidence variety of an isotropic line inside such a 9-plane. Its projections are

Y ← Z → X,

written g and f, respectively. The fibers of f are P⁸, so dim Z−dim X = 8. Pullback by the smooth incidence projection g preserves the topological-filtration index, and proper pushforward by f lowers it by at most 8. The K-theoretic version of [A], equation (1.2), discussed on p. 11, identifies f_*g^*(l₀) with e₈. Thus

e₈ ∈ T^(13−8)K(X_K) = T⁵K(X_K).

Using the rank-8 tautological bundle of the odd-dimensional Grassmannian at this point would give the wrong relative dimension. The published argument first uses the rank-9 bundle for ψ and only then identifies its component with the Grassmannian of φ. This accounts for the exact parameter shift.

### 4.4 Turning topological membership into gamma membership

Since C₀(φ) = A has maximal index 256 over F and K = F(SB(A)), [A], Theorem 4.3, applies to the original odd-dimensional model. It identifies the topological and gamma filtrations on K(X_K). Equivalently, its even-component version is stated in Remark 4.5. Therefore

e₈ ∈ γ⁵K(X_K).

Finally,

n + 1 − floor((n+1)/2) = 8+1−4 = 5.

This is exactly the prohibited term. The arithmetic generalizes in the proof as

d = 2n+2,  r = floor(d/4) = floor((n+1)/2),

d−r−1−n = n+1−floor((n+1)/2).

Thus the published implication is pointwise in the dimension parameter. A purely formal contrapositive of “all Conjecture 4.7 instances imply all Conjecture 3.3 instances” would not by itself identify n = 8; the inspected proof does.

## 5. Computational and mathematical dependency scope

The negative resolution depends on the published index bound 8. Its provenance is transparent:

1. [K-pre], Theorem 3.6, describes the generic odd-spin Chow ring modulo torsion using its tautological Chern subring and one additional class.
2. Theorem 4.1 turns a divisibility calculation in a free integral Chow ring into the Grassmannian index. With n = 8 and r = 5, its auxiliary parameter is l = 3.
3. In §5, the author reports a Maple 2021 computation using the Chow ring package version 4.0. It shows that the cube of the relevant integral class is not divisible by 2²³. In the theorem's notation, this gives a deficiency at least 24−22 = 2, hence an upper bound 2^(5−2) = 8 for the fifth Spin₁₇ Grassmannian.
4. Appendix A specifies the weight substitutions, the type-C₈ parabolic with the package's reversed root numbering, the integral class, its Schubert expansion, and a nonzero parity result after normalization. The 128 normalization contributes 2²¹ to the cube; the printed normalized cube divided by 2 has a nonzero reduction modulo 2, consistent with exact valuation 22 for the original cube. These are descriptions and arithmetic interpretation of the paper's outputs, not outputs reproduced in this audit.
5. Monotonicity gives the fourth Spin₁₇ index at most 8. The paper uses known highest-index information and elementary splitting arguments for the matching lower bound. Section 6 passes to Spin₁₈ and obtains the displayed exact fourth/fifth values 8.
6. [KM] p. 5 explicitly summarizes the dimension-17 and dimension-18 deviations and expressly says their determination involved computer computations. It cites [K-pre] rather than supplying a new independent computation.

For the disproof itself, the upper bound 8 is enough. The exact-index lower bound, the rest of the Spin₁₈ list, the Spin₁₉ computations, and the general asymptotic bounds in [KM] are not necessary to the contradiction.

The independently checked portions here are the source identities and versions; exact target match; parameter and field matching; generic-index divisibility direction; application to the maximal-Clifford-index model; the integer arithmetic and codimension shifts in the existing implication; and the published final-preprint/journal agreement on the input value. The background K-theory, Chow-theory, and quadratic-form results cited inside these papers remain literature dependencies. No claim is made to have reproved Panin's theorem, the Chow-ring presentation, Totaro's theorem, or the underlying characteristic-free quadratic-form theory.

No Maple, Chow ring package, or other source-author program was downloaded or executed. No independent finite Schubert-ring computation or proof-assistant verification was performed. The software used locally only downloaded, hashed, extracted, and rendered sources and assembled this audit.

## 6. Characteristic, scope, and tempting but invalid shortcuts

- [O] and [A] expressly allow arbitrary characteristic. [K-pre] §1 and [K-journal] p. 743 do so as well. [KM] starts from an arbitrary initial field, and [DKM] Proposition 2.1 concerns split reductive groups over a field without a characteristic-zero restriction. The argument has no newly introduced characteristic mismatch. A characteristic-zero instance would already refute the universal claim; the cited machinery is broader.
- “Generic” in the 2016 paper and “generic torsor” in the later work should not be silently equated. Section 3 supplies the needed divisibility bridge. No exact index is claimed for every arbitrary nongeneric form.
- Trivial Clifford invariant alone is not used to replace the maximal-index hypothesis over F. Maximality is built into the pre-splitting model and is needed when applying Theorem 4.3 over F(S).
- A K-theory isomorphism after a field extension preserves the lambda-ring structure and gamma filtration. It need not preserve the topological filtration as an equality. [A] p. 11 explicitly warns about this difference. We apply T = γ over the special field K, not by assuming equality over an algebraic closure.
- The inference supplies an existential counterexample satisfying the full original setup and the precise n = 8 failure. It does not classify the gamma filtration for every n, determine the optimal replacement threshold, or assert failures at all n ≥ 8.
- A statement about Chow groups versus associated gradeds of gamma filtrations, including the different Yagita Spin₁₇ counterexample, is not substituted for this argument. No Yagita result is needed in the dependency chain.
- The older discussion that the exponent 5 should be optimal at n = 8 ([O], Remark 5; [A], Remark 4.8) is the conjectural expectation being overturned. Its already-proved membership in the fourth term does not imply nonmembership in the fifth.

## 7. Inspection record and limits

Text inspection covered [O]'s full two-page contribution; [A]'s relevant definitions, §§1, 3 and 4 and the complete implication; [K-pre] §§1–6 and Appendix A; [KM] definitions, Lemma 2.3, p. 5 and Appendix B; [DKM] pp. 1–3 and 8–9; and the journal [K-journal] introduction and the relevant §§5–6. Some adjacent text was read to locate references; that is not a claim of auditing every proof in every paper.

Fresh visual inspection covered [O] PDF pp. 12–13, [A] pp. 10–12, [K-pre] pp. 7–8, [KM] p. 5, [DKM] p. 3, and [K-journal] PDF pp. 9–10. This specifically checked the target exponent, the norm identity, the incidence shift, the boxed Spin index values, and the direction of the Chow-image inclusion. Appendix A was text-inspected, not executed.

The direct DOI web-open calls for the three later journal articles returned access errors in that web tool. These were not access denials. The official publisher record and article link for [K-journal] and the official Cambridge journal PDF for [DKM] were successfully retrieved through ordinary public download. No [KM] journal PDF is used; its author-directed final preprint and prose suffice.

The public edition contains authored analysis and public source-verification metadata. Source PDFs, extracted source text, source images, datasets, programs, and computational certificates are not reproduced. EDITORIAL_MAP.json records the exact transformation of the authored audit, including hashes of unchanged mathematical regions. Preparation rechecked artifact identities and the recorded refetch matches; it did not constitute another source inspection or an independent rerun of the mathematical computation.

## 8. Accepted statement suitable for a concise status correction

The gamma-filtration nonmembership conjecture in Karpenko's 2016 Oberwolfach contribution is false already at n = 8. Karpenko's published Spin₁₈ index calculation gives index 8 for the fourth orthogonal Grassmannian, rather than the conjectured 16. Generic-index maximality makes this bound applicable to the maximal-Clifford-index/Severi–Brauer model. The explicit implication proved in *Around 16-dimensional quadratic forms in I_q^3*, final preprint p. 12, then gives e₈ ∈ γ⁵K(X over F(S)), the exact prohibited membership. This is a literature-derived resolution; the published Maple-dependent index computation has not been independently replayed here.
