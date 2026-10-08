# Independent audit: KP-5.16 / 3023

Date: 2026-10-08. Authored mathematical and computational audit; unrefereed. No novelty claim.

## 1. Verdict and exact object audited

**Accept the mathematical partial results, with their stated conventions and external dependencies. Do not accept them as a solution of the full graded-commutative decision problem.** No mathematical correction to the frozen proofs was required by this audit. A separate provenance addendum is required because this audit located a public prior same-target AI response, including substantial overlap with the Koszul complete-intersection route.

Controlling packet: `public_frozen_v2`, manifest SHA-256

`e745356796d71aa13e1ca182c86f2eabcb6cec895ad05f98f5ffae71a4461257`.

The report is 30,836 bytes, SHA-256 `54bd5c5cc2b3c7f26a391f0cd82cd6e3b90a3544ee1b9c283fa22a08b04e3b98`. Its exact checker is 14,656 bytes, SHA-256 `74b21a37d2c09d299ddf796b49ea973b2d9d7a5eed228dd41d81f29ccb5e2893`.

All seven packet-manifest entries and all seventeen original validation-manifest entries were independently rehashed and matched. The original validation receipt SHA-256 is `d7c2013f05aa1c23c72e54d59a8304162a2155e9ad6e789df9cf099076397f00`; the validation manifest SHA-256 is `ca4877798bdb1d15d4a83cb529eb2cdd9e7dbd519f892f50493a89f1cb4548a2`. The full original inventory remains in the historical freeze. See `PUBLIC_SLICE.json` for the exact retained public inventory; the original inventory is not distributed here.

The accepted contents are:

1. Polynomial-exterior unit-boundary/acyclicity criterion, including mixed integer gradings, and the separate sign-only characteristic-two criterion.
2. Integer-augmentation undecidability, without an inference to equivalence undecidability.
3. Quasi-isomorphism classification of regular Koszul models by quotient-ring isomorphism, with the regularity hypothesis retained.
4. Positive-degree strict-isomorphism decidability over finite fields and positive semidecidability of literal stable tame equivalence.
5. Homology, quasi-isomorphism/rational stable-tame classification, and nonformality of the mixed-degree family A_n.

The tensor-algebra reconstruction is accepted conditional on the imported unit-ideal undecidability theorem stated by Manolescu–Rozenblyum. This audit independently checks the DGA reduction; it does not reconstruct Bokut's entire foundational computability theorem. General graded-commutative stable-tame, quasi-isomorphism, and arbitrary-triangulated derived-category equivalence remain unresolved by the packet.

## 2. Source, definition, and attribution audit

### 2.1 Exact target

The inspected Problem 5.16 allows finitely many homogeneous generators with arbitrary integer degrees, over Z or a field, in separate tensor and free graded-commutative classes. Its three relations are stable tame equivalence, quasi-isomorphism, and equivalence of module-derived categories as triangulated categories. It describes quasi-isomorphism of objects using a common source. The packet supplies actual common-source constructions where that formulation matters. [K3, printed pp. 313–315](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

The source's stabilization language is insufficient to erase the distinction between strictly graded-commutative and sign-only free algebras in integral or characteristic-two settings. The report correctly states its convention rather than presenting a convention-dependent claim as an unconditional answer to the source.

### 2.2 Main preprint

The primary preprint states the three noncommutative negative results and explicitly leaves the analogous graded-commutative problems open. The live arXiv record displays v1 submitted 2026-04-28 at 15:51:10 UTC, even though its identifier begins 2605. This is an observed source timestamp, not a date inferred from the identifier. No journal reference was displayed. [Record](https://arxiv.org/abs/2605.08122), [version-pinned text](https://arxiv.org/html/2605.08122v1).

Both local public PDFs match their pinned byte counts and SHA-256 values. Fresh `pdftotext -layout` extraction from each PDF agrees after deleting the exact arXiv identifier/date stamp and removing whitespace. They are not byte-identical PDFs; text-extraction equality does not establish visual identity. The operation and result are recorded in `SOURCE_COMPARISON.json`.

The zero-derived-category reduction avoids reliance on Hochschild invariance under an arbitrary non-enhanced triangulated equivalence. The preprint's separate group route is not needed for this audit's acceptance.

### 2.3 Imported foundational result

The Russian Bokut PDF was accessible through the web reader in this audit, including its broad coefficient-ring setup, effective-construction lemma, and Markov-property discussion. However, the foundational translation from that presentation to the full coefficient-uniform unital unit-ideal theorem is not independently rebuilt here. Its original algebra/unit conventions and computability hypotheses must not be silently replaced by a superficial title match. Acceptance is explicitly of the DGA reduction using the theorem as stated in Manolescu–Rozenblyum. [Bokut primary PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=rus&paperid=1237&what=fullt).

The frozen local Bokut source entry has no PDF bytes and no invented digest. Its local verification remains NOT_RUN. A successful web view does not repair that missing local-byte check, and aggregate source coverage remains NOT_RUN.

### 2.4 Other supporting sources

Rizell's Proposition 1.3 separately treats characteristic different from two with a parity grading and characteristic two with arbitrary grading. Its characteristic-two argument uses squaring. The report supplies its own explicit finite-odd-ideal and homogeneous-extraction proof and does not discard those source hypotheses. [Primary preprint](https://arxiv.org/pdf/1512.03570).

Stacks Tag 062F gives the regular-sequence-to-Koszul-regular implication, not a theorem about arbitrary presentations. The report's induction reproduces exactly the needed implication. [Tag 062F](https://stacks.math.columbia.edu/tag/062F).

Poonen's Section 13.1 states an unknown undecidability status for the general commutative-ring isomorphism problem in that dated survey. It is not a current proof of openness, and it does not establish undecidability for complete intersections. The report observes this limit. [Author's survey](https://math.mit.edu/~poonen/papers/sampler.pdf).

The audit's bounded current searches did not locate a later resolving primary theorem. They did locate raw prior AI claims, addressed in Section 8. A bounded search cannot certify absence of all later literature.

## 3. Tensor reduction and stabilization audit

### 3.1 Tensor unit-ideal reduction

For the degree-zero x_i and degree-one r_j presentation, every degree-one monomial has exactly one r_j. Thus the degree-zero boundaries are precisely the two-sided ideal generated by f_j, and H_0 is the advertised quotient. This is true over any unital coefficient ring without a domain hypothesis.

If d h = 1 with |h| = 1, then d(hz) + h d(z) = z. The same underlying-complex contraction works on every DG module. Therefore all modules are acyclic and their derived category is zero. Conversely, if the derived category is zero, the regular module A is zero in it, hence its homology vanishes. This converse needs no linear enhancement or Hochschild comparison.

The proposed tame normal form is valid as a sequence of coordinate changes:

- Adjoin a degree-one a and degree-two b with d b = a.
- Set a' = a + h. This is elementary because h has no a or b, and d a' = 1.
- Replace each r_j by r'_j = r_j - a' f_j(x). Each correction avoids that r_j and all r variables, so each step is elementary and all r'_j are cycles.
- Re-express the old a as D in the current coordinates. It is independent of b, homogeneous of degree one, and closed because the old a was closed.
- Set b' = b - a' D. This is elementary and d b' = D - D + a' dD = 0.

No illicit commutation of a' past an x is used. The identical construction on the comparison acyclic algebra gives the same free normal form, since the degree counts agree. The native checker verifies a genuinely noncommutative sample automorphism in both inverse directions. The general assertion follows from the written coordinate argument, not that sample.

Tensor stabilization preserves homology over an arbitrary coefficient ring. One explicit justification is to split its word module according to the number k of stabilization letters. The k = 0 summand is A. For k > 0, the summand is a tensor complex of old-word blocks and copies of the two-term contractible free module spanned by the new letters. Contract its first new-letter factor, with the Koszul sign determined by the preceding block. The differential preserves k, so the direct sum of these contractions contracts the augmentation kernel. This requires neither division nor a bounded grading.

For two acyclic unital DGAs, A × B is an acyclic common source with quasi-isomorphic projections. Its diagonal coefficient map preserves units. The problem does not require that common source to be finite free. Consequently the full constructed-pair equivalence chain is valid, subject only to the imported undecidability input.

### 3.2 Commutative stabilization warning

For S_Z = Z[u] tensor Lambda(v), |u| = 2, |v| = 1, d u = v, the only map from degree 2m to degree 2m-1 is multiplication by m on the displayed monomial bases. There is no hidden extra basis element or incoming boundary. Hence H_(2m-1) = Z/m and H_(2m) = 0 for m > 0; H_0 = Z. Over F_p the coefficient p vanishes, leaving the stated adjacent Frobenius classes. Over Q integration contracts the augmentation ideal.

The native characteristic-zero calculations use exact rational coefficients to verify the integer coefficients m; the universal integral torsion conclusion comes from the explicit one-by-one integer matrices, not a rational homology computation masquerading as Smith normal form.

If literal stabilization permits this pair, the base algebra and its stabilization are stable tame equivalent but need not be quasi-isomorphic over Z or positive characteristic. The opposite-parity pair, with an exterior upper generator, contracts without division. Rational literal stabilizations of either parity are harmless in arbitrary integer degrees. These facts justify exactly the restricted implication chains used in the report. They do not redefine the source's intended convention.

## 4. Acyclicity and arithmetic audit

### 4.1 Polynomial-exterior criterion

Let P be the even polynomial subalgebra and J the ideal of finitely many odd exterior generators. The parity of d x_i is odd, so d x_i lies in J. If a degree-one element has differential 1, the only terms contributing modulo J are those with one odd generator, giving an ordinary ideal certificate for the q_j. This step does not assume J is a differential ideal: generally it is not.

Conversely the finite identity sum a_j q_j = 1 can be projected to homogeneous total degree zero even when P has infinite-dimensional graded pieces. Each individual polynomial still has finite support. The component of a_j of degree 1-|theta_j| supplies the required certificate; no bounded-degree search is inferred.

For w = sum a_j theta_j, the element c = 1-dw is degree zero, closed, and in J. Its nilpotence follows from the exterior relations and the finite number of odd generators, not from d preserving J. Thus d[w(1+c+...+c^o)] = 1. This establishes the equivalence for arbitrary commutative coefficient rings in the strict polynomial-exterior convention. The algorithmic corollary additionally uses effective polynomial ideal membership over the specified fields or Z; no statement about arbitrary non-effective exact coefficients is justified.

Independent tests strengthen the single supplied nilpotent example: a mixed-degree example has c² nonzero and c³ = 0, rejects the too-short correction, and accepts the quadratic correction. A separate inhomogeneous ideal certificate in variables of degrees 2 and -2 is projected to the correct homogeneous coefficient degrees and yields a degree-one primitive.

The conclusion decides acyclicity, hence zero-derived-category recognition. It does not decide general pairwise equivalence. In particular, it blocks a direct transfer of the tensor zero-object undecidability mechanism to this strict commutative class.

### 4.2 Sign-only characteristic two

In this convention all variables are ordinary polynomial variables, including those of odd degree. Necessity of unit membership in the ideal of generator differentials follows by expanding the derivation. If 1 = sum a_j d b_j, then in characteristic two squaring gives 1 = sum a_j² (d b_j)². Since d(a_j²) = 0 and d²b_j = 0, the displayed sum is the differential of sum a_j² b_j d b_j. Its homogeneous degree-one part is a unit primitive.

The independent check includes a nonlinear certificate with non-cycle coefficients for which the naive sum a_j b_j is not a primitive but the squared construction is. It also checks that an odd square really survives, preventing accidental use of the strict exterior convention. No conclusion for sign-only Z is obtained from either criterion.

### 4.3 Integer augmentation encoding

For K_f, a coefficient-preserving graded map to Z sends every degree-one generator to zero and each degree-zero variable to an arbitrary integer. The chain equation is exactly f(a) = 0. Thus DPRM supplies an undecidability reduction for augmentation existence. The passage from the standard nonnegative-integer formulation to integer solutions can also be made by representing each nonnegative variable as a sum of four squares. The construction is finite and does not require any unproved statement about rational points over Q.

Augmentations extend over literal canceling pairs by sending both new variables to zero, and restrict in the opposite direction. That is an invariant of stable tame classes, not a reduction to equivalence recognition. The examples f = x²-1 and f = x²+1 correctly separate root existence, base-ring quasi-isomorphism, and acyclicity. The missing pairwise-equivalence gadget is a real gap.

## 5. Koszul route and effective enumeration audit

### 5.1 Regular Koszul models

Adjoining the final exterior generator is the mapping cone of multiplication by the final regular-sequence element. The long exact sequence gives vanishing positive homology and the quotient in degree zero. Applying H_0 proves the necessary direction of the ring-isomorphism criterion; the quotient augmentations give the converse.

The report also meets the common-source definition exactly. After identifying the two quotient rings, the degreewise fiber product has projections whose kernels are the acyclic kernels of the opposite surjective augmentation. Surjectivity holds in each degree, including positive degrees where the target quotient is zero. The resulting short exact sequences make both projections quasi-isomorphisms. The fiber product need not be finite free.

For (x²,xy), the cycle y e_1-x e_2 is nonzero and d(e_1e_2) = -x(y e_1-x e_2). If it were a boundary, comparison of the e_2 coefficients in the domain Q[x,y] forces 1 = -p x, impossible. This genuinely obstructs replacing regular sequences by arbitrary presentations. The redundant-zero-relation example independently makes the same point. The one-variable x^n subfamily is classified by quotient dimension.

None of this proves undecidability of commutative algebra isomorphism, or its restriction to complete intersections. The valid equivalence theorem substantially overlaps a prior public raw AI attempt; the packet properly stops before the unsupported premises used there. See Section 8.

### 5.2 Positive-degree strict isomorphism

With strictly positive generator degrees, each needed homogeneous component has finitely many monomials. Over a fixed finite field it is a finite set. The finite list of images in each direction, generatorwise chain equations, and two inverse identities therefore gives a terminating YES/NO procedure. Exterior relations must still be respected; the report includes that check.

For the example with degrees 1,1,3, a map has exactly a 2×2 matrix on the degree-one generators and a scalar lambda on the degree-three generator. There is no missing cubic monomial in the two exterior degree-one variables. The chain relation is k lambda = det(M); invertibility requires det(M) and lambda nonzero. It gives 48 isomorphisms for each nonzero k over F_3 and zero for k = 0. An independent determinant-only enumeration confirms this and the analogous counts over F_2, F_5, and F_7.

This procedure decides strict DGA isomorphism. It does not decide quasi-isomorphism merely because the generators are positive. Positive degrees alone also do not make solving the coefficient equations over Q decidable. Zero or mixed even degrees remove the finite-dimensional-component bound.

### 5.3 Stable tame positive semidecision

Finite stabilization lists, elementary words, polynomial coefficients, and degree-preserving identifications admit effective enumeration in the stated computable classes. Unit scalars can be enumerated together with inverses. Every accepted finite word is checkable; every actual stable tame equivalence has some such word by definition. There is no terminating negative branch in the proof.

For sign-only Z, finite algebra equality still has an effective normal form: ordered monomials with unrestricted integral coefficients if no odd variable is repeated, and coefficients reduced modulo two once an odd variable occurs with exponent at least two. This explains why that convention does not break certificate checking. The supplied native checker implements strict exterior algebras and sign-only characteristic two, not this integral normal form; its absence does not refute the enumeration proof, but it limits implementation coverage.

## 6. Mixed-degree family and full Massey audit

For A_n the only nonzero chain groups occur in degrees 0 and -1. The differential from Q[x,z] is x^n times partial differentiation in z, followed by y. Characteristic zero is essential: the kernel is exactly Q[x], and z-integration makes the image exactly x^n Q[x,z]y. Consequently H_0 = Q[x] and H_-1 = (Q[x,z]/(x^n))y, with all other homology zero.

The annihilator of the entire H_0-module H_-1 is (x^n), because testing on the class of y detects every coefficient outside that ideal. The intrinsic quotient H_0/Ann(H_-1) has rational dimension n. It is preserved by any coefficient-preserving graded homology-algebra isomorphism, without requiring that x itself be preserved. Hence distinct n cannot be quasi-isomorphic. Equal n are identical. Rational stabilization preserves homology, so the same elementary classification holds for rational literal stable tame equivalence. Nothing here classifies arbitrary triangulated derived categories.

For the triple represented by (y,x^n,y), both products have primitive z. The homological sign formula is

`a v + (-1)^(|a|+1) u c`,

and |a| = -1 gives the plus sign. Thus the representative is 2zy, not zero. Differentiating the formula gives cancellation of the two abc terms, as required.

The full indeterminacy is

`[y] H_0 + H_0 [y] = (Q[x]/(x^n))y`

inside H_-1. The report's notation `Q[x]y` means precisely this image submodule, not a freely injected copy of Q[x]y. Arbitrary choices of primitives differ from z by cycles in Q[x]; their Massey representatives differ by exactly that submodule. The z coefficient in 2zy survives modulo both boundaries x^n Q[x,z]y and this full indeterminacy. No additional degree-zero classes involving z are available, since the kernel of the differential in degree zero was computed exactly.

In the zero-differential homology DGA the adjacent products vanish literally, and zero primitives give zero in every defined triple product. Quasi-isomorphisms preserve the resulting triple coset and the membership of zero: images of defining systems give one inclusion, and homology isomorphisms lift primitive differences modulo boundaries for the reverse inclusion. This proves nonformality even if a proposed homology-algebra identification moves the named classes. The audit independently checks 810 finite choices of defining-system primitives across n = 1,...,10; the universal indeterminacy proof, not this finite set, establishes nonformality.

The general polynomial-derivation construction is also algebraically sound: y² = 0 makes d² vanish. Kernel and cokernel computations can be difficult or infinite, so merely writing this construction is not a complete classification or an undecidability reduction.

## 7. Independent execution and implementation coverage

All runs used actual UID 1000 with Python 3.12.14. The frozen packet directories were 0555 and files 0444; the public-source input directory and relevant files had the same read-only profile. Native normal, -O, and -OO runs all returned zero, passed every mathematical check, and denied both append-open probes and both directory-create probes. Their complete mathematical outputs are retained in `AUDIT_RUNS.public.json`, with the source-input directory label replaced by a generic role. Normalized mathematical/source/probe outputs agree across all three optimization modes.

The native checker contains zero Python assert statements. All mathematical conditions are explicit runtime guards. Its source-verification behavior was independently exercised:

- Eight present public-source objects matched pinned byte counts and SHA-256 values.
- The absent Bokut PDF remained NOT_RUN, so full-source coverage was NOT_RUN.
- Absent sources with `--require-sources` returned exit 2.
- A deliberately invalid short byte marker under the expected public PDF filename returned exit 1 and source FAIL. No primary-source body was copied for that negative control.

Eleven semantic mutations were run in normal, -O, and -OO modes, for 33 mutation runs. All returned exit 1 through explicit guards. Mutations removed the Koszul multiplication sign, odd-square relation, Leibniz sign, differential-degree guard, or d² guard; changed the unit correction, tensor coordinate sign, Koszul syzygy sign, Massey sign, or derivative coefficient; or incompletely enumerated the finite field. `MUTATION_METADATA.json` records each exact one-location change, mutated-code hash, mode, and rejection guard. Every subprocess stdout, stderr, and exit code is retained in `AUDIT_RUNS.public.json`; only the source-input directory label is generalized.

The separately authored `check_independent.py` uses adjacent-swap word normalization rather than the native exponent-inversion formula. It made 6,825 exact normalization comparisons, including strict characteristic two and sign-only characteristic two as distinct cases. It also tested a higher nilpotent correction, mixed-degree homogeneous certificate extraction, a nonlinear characteristic-two certificate, 810 Massey defining-system samples, annihilator exponents 1 through 10, and determinant-only finite-field map counts. It passed normally, with -O, and with -OO; results were invariant after removal of the optimization field.

The original frozen hashes still matched after all runs. Read-only probes demonstrate ordinary-process write denial, not immunity to an owner or privileged process changing permissions. Finite testing corroborates the implementation and detects selected defects; it is not formal verification, a proof of any general decision theorem, or a guarantee that all conceivable defects would be rejected.

For this public slice use the externally pinned `BOOTSTRAP.py` and `mutation_tests.py` workflow in the publication README. The historical source-bearing runner and its full inventory are not distributed. Fresh public replay uses actual UID 1000, read-only inputs, all three optimization modes, and absent-source/corpus NOT_RUN results.

## 8. Newly located prior-attempt provenance and gate limit

This audit located a public raw Aletheia same-target response at the pinned source below. GitHub path history returned one commit, and the commit details identify the TeX file as added in that commit:

- Commit: `597525d09922962fe01e75cf0439b28aacba89cb`.
- Recorded author time: 2026-05-02T12:11:40Z.
- Recorded committer time: 2026-05-02T12:14:41Z.
- Public file blob: `ece47caa53b953b45e9be5c8bee423ad39c5a6ea`.
- [Pinned TeX source](https://github.com/google-deepmind/superhuman/blob/597525d09922962fe01e75cf0439b28aacba89cb/aletheia/Kirby/Kirby5-16.tex).
- [Commit](https://github.com/google-deepmind/superhuman/commit/597525d09922962fe01e75cf0439b28aacba89cb).

These are repository provenance dates, not verified original model-generation times or a proof of when the commit became publicly accessible. The source labels its contents raw model responses edited for formatting. It contains substantive same-target work on the three relations. Its graded-commutative route uses the valid regular-Koszul/quotient-ring equivalence, but then asserts unsupported undecidability premises for commutative ring isomorphism and its complete-intersection restriction. Those premises are not established by the response. It is not accepted here as a resolving theorem.

The valid Koszul step substantially overlaps Approach 3 of the packet; the noncommutative routes also overlap the already attributed Manolescu–Rozenblyum background. This does not invalidate the partial proofs, but it excludes any inference that these routes originated in the packet. The frozen report already makes no novelty claim and already identifies the unsupported commutative-isomorphism step as a gap. The addendum makes the concrete prior source explicit.

This is a newly encountered external prior attempt in this audit, not a verified match inside the supplied inherited corpus. The dataset metadata was checked for integrity as part of the frozen packet; this audit did not independently reproduce its full-corpus matching operation or establish that the external response is present there. An inherited-corpus search result must not now be restated as an absence of all prior substantive same-target attempts. Mathematical acceptance of the five documented approaches is separate from any accounting disposition based on prior-attempt history.

No source-response body, third-party PDF, dataset record, or private coordination material is included in this audit. All new text is authored analysis or public verification metadata. The frozen packet was preserved; `PROVENANCE_ADDENDUM.md` supplies a separate supplement rather than rewriting history.

## 9. Final acceptance boundary

Mathematical partial-result audit: **ACCEPT WITH EXPLICIT SCOPE AND IMPORTED-INPUT LIMITS**.

Independent finite execution: **PASS**, normal/-O/-OO invariant; 33 of 33 tested semantic mutations rejected.

Full local source coverage: **NOT_RUN**, because Bokut local bytes remain unavailable.

General commutative resolution: **NOT ESTABLISHED**.

Prior-attempt absence or novelty: **NOT CERTIFIED**; public earlier AI attempts are now explicitly identified.

No publication, branch, pull request, or queue edit was performed by this audit.
