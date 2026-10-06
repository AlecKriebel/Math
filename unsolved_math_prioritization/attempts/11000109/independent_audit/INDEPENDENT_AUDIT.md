# Independent audit of the twice punctured torus extension argument

Problem 11000109 / AMR-109-0109 / rank 878 / Korkmaz Problem 2.4.

Audit date: 2026-10-06 UTC.

## Verdict

Accept the original five-file author freeze without mathematical repair. Its negative answer applies to the exact orientation-preserving, puncture-permuting mapping class group with no boundary. It constructs an automorphism of one specified invariant finite-index subgroup, of index 48, and proves that no abstract automorphism of the ambient group extends it. The appropriate disposition is **already_solved**, with **1/5 substantive author approaches used** and prior credit retained.

This is an independent mathematical and source audit, not formal verification or human peer review. The topological inputs remain cited theorems. No publication was performed in this audit.

## Input identity and completeness

The author archive was checked before its content was used:

- TWICE_PUNCTURED_TORUS_11000109_AUTHOR_SAFE_FREEZE.zip: 8,697 bytes; SHA-256 `8283ef26318dc632309b6e587bc49426ed6a74bde497a1e78f1a020e59672917`.
- TWICE_PUNCTURED_TORUS_11000109_EXTERNAL_MANIFEST.json: 1,430 bytes; SHA-256 `71fbc5234c636022a15ccb2b9ee1c3b1b1bdf0c90d777764a68adace9bbd77cb`.

The ZIP has exactly the five declared members. Every member length and SHA-256 matches the external manifest; every loose author file matches its archive member. All five were read in full. They are retained byte-for-byte under `author/` in the audit package. Their historical pending-review wording has not been overwritten; the separate ACCEPTANCE.md supplies this audit's decision.

The complete catalog, problem corpus, and research-results corpus were independently hashed and parsed. The target catalog row has rank 878 and the correct identifiers. The exact statement hash and the full problem/report-pair hash were independently recomputed, including the complete inherited report. The report is only truncated-statement triage: it does not contain a mathematical construction, lemma, proof attempt, or substantive approach to charge against the turn limit. Public byte evidence and the serialization convention are in PUBLIC_VERIFICATION.json; no dataset contents are included.

The author's historical repository searches were not repeated. They remain reported author history, not fresh independent evidence. This does not weaken the mathematical acceptance or the independently checked inherited-triage finding.

## Exact scope of the question

The original chapter defines the orientable-surface group using orientation-preserving maps and allows permutations of the marked points. Its notation omits zero boundary count. Problem 2.4 asks whether an automorphism of a given finite-index subgroup extends to an automorphism of the ambient group. Thus the target is G = Mod+(S_{1,2}), with both punctures permutable and no boundary; the target is neither the pure group nor the extended group.

The source footnote gives a weaker extended-group, inter-subgroup, non-inner statement. It cannot alone settle the question. The catalog's trailing discussion belongs to the transition toward Problem 2.5 and does not enlarge Problem 2.4. These distinctions are handled correctly in the author packet. Source: Korkmaz, printed pages 85 and 87, respectively PDF pages 92 and 94, in the [Farb volume](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf).

## Audit of Input A and the orientation restriction

Set M = Mod±(S_{0,5}), M+ = Mod+(S_{0,5}), H = Stab_{M+}(p0), and K = PMod+(S_{0,5}). The required identification is G ≅ H × C2, with the pure torus subgroup corresponding to H × {0}.

Behrstock–Margalit §4.2 identifies the extended pure torus group with the distinguished-puncture stabilizer on the sphere. Proposition 9 supplies the direct-product splitting by the central involution that exchanges the torus punctures. These exact claims were read in the pinned author PDF, including their context and the definition of the extended mapping class group. [Author PDF](https://margalit.droppages.net/papers/g1.pdf).

The later independent convention check is decisive: Bridson–Wade §6 explicitly distinguishes the pure, extended-pure, orientation-preserving, and extended groups. Proposition 6.1 states both direct-product decompositions, and Proposition 6.4 identifies the pure torus image with the distinguished-puncture stabilizer. Lemma 6.3 supplies symmetric representatives; the proof of Proposition 6.4 checks orientation and obtains the orientation-preserving image from half-twists. [arXiv v2 §6](https://arxiv.org/html/2306.13437v2#S6).

Here is the restriction check independently applied to the author's argument. Away from the branch points, the covering q is locally orientation preserving. A commuting lift u and its descended map v satisfy q u = v q there, so their orientation signs agree. The central deck involution is orientation preserving. Multiplying a representative by that involution changes whether it exchanges the two marked points but does not change its orientation sign. Therefore the unique pure representative of each central coset has the same sign as the original representative. The extended identification consequently restricts to precisely H, not to a different index-two subgroup. There is no hidden factor of two in Input A.

The argument does not require the selected sphere half-twist to have order two. Only its puncture permutation must be the transposition (0 1). The author correctly avoids a finite-order assertion about the half-twist itself.

## Audit of Input B and the centralizer

Theorem 6 of Behrstock–Margalit states that the natural conjugation homomorphism from the extended mapping class group into its abstract commensurator has trivial kernel except for the indicated closed genus-two case, after excluding the listed small surfaces. S_{0,5} satisfies its hypothesis and is not the genus-two exception. Thus the exact natural map M → Comm(M) is injective. This is stronger evidence than a bare, unspecified abstract isomorphism of the two groups, and it is exactly the property used.

The implication C_M(K) = {1} is valid. K has finite index in M. If x centralizes K, conjugation by x agrees with the identity on K, hence represents the identity commensuration of M. Injectivity then implies x = 1. This argument uses the definition of equality of commensurations correctly and does not confuse a trivial group center with a trivial finite-index centralizer.

If z belongs to Z(H), it centralizes every element of K ⊂ H. Consequently z = 1, and Z(H × C2) = {1} × C2. This center is characteristic. No torus automorphism classification or surjectivity assertion for M → Comm(M) is required.

## Same subgroup and exact index

The puncture permutation map M+ → S5 is surjective because orientation-preserving half-twists realize transpositions. Its kernel is K. The subgroup H is the inverse image of the stabilizer of 0; therefore H/K ≅ S4 and [H:K] = 24.

K is normal in M+, and also in M: conjugation preserves both orientation sign and pointwise triviality of the puncture permutation. In particular it is normal in H. Under the chosen isomorphism Θ:G → H × C2, let Γ = Θ^{-1}(K × {0}). It is a normal subgroup of G and

[G:Γ] = [H:K] · |C2| = 24 · 2 = 48.

Choose f in M+ whose permutation is (0 1). Conjugation c_f maps K onto K, with inverse c_{f^{-1}}. Transporting c_f to Γ gives the author's φ:Γ → Γ. Both the domain and image are exactly Γ. There is no passage to a smaller subgroup after defining the map and no replacement by an isomorphism between distinct finite-index subgroups. Normality in the sphere group supplies the invariance that the initial triage correctly identified as necessary.

## Audit of the hypothetical extension calculation

Assume A is any automorphism of H × C2 extending the transported φ. Since its center is exactly {1} × C2, quotienting by that characteristic subgroup yields an automorphism β of H satisfying β(k) = f k f^{-1} for every k in K.

For arbitrary h in H and k in K, the element hkh^{-1} lies in K. The homomorphism law and the prescribed restriction therefore give

β(h) f k f^{-1} β(h)^{-1} = f h k h^{-1} f^{-1}.

Set t = f^{-1} β(h) f, which lies in M. Conjugating the displayed equation by f^{-1} gives t k t^{-1} = h k h^{-1}. Multiplying by h^{-1} and h yields

(h^{-1} t) k (h^{-1} t)^{-1} = k.

Thus h^{-1} f^{-1} β(h) f belongs to C_M(K), exactly as claimed in RESULT.md §4. The centralizer is trivial, so β(h) = f h f^{-1} for every h in H. This step is elementwise, uses all k in K, and does not assume that an abstract automorphism β is inner.

Now choose h in H with puncture permutation (1 2), for example a half-twist supported away from p0. Since π(f^{-1}) = (0 1),

π(f h f^{-1}) = (0 1)(1 2)(0 1) = (0 2).

It follows that f h f^{-1} does not fix p0 and so is not in H. But β(h) is in H. This contradiction already follows from containment; surjectivity of β is not needed in the final step. The quantifier over all ambient automorphisms is fully discharged.

## Central transvections and the older automorphism remark

The warning about central transvections is substantive. Every automorphism A of H × C2 fixes the unique nonidentity central element (1,1). Writing A(h,0) = (β(h),χ(h)) shows directly that β is the quotient automorphism and χ:H → C2 is a homomorphism. Hence

A(h,z) = (β(h), z + χ(h)).

Conversely any such pair defines an automorphism, with inverse obtained from β^{-1} and the corresponding correction to the second coordinate. Therefore quotienting really removes all possible central components, rather than just a named family of examples.

For example, composing H → S4 with permutation sign gives a nonzero χ. Then (h,z) ↦ (h,z+χ(h)) is not inner, since inner automorphisms of this direct product do not alter its central coordinate. Moreover χ vanishes on K, so this particular non-inner automorphism fixes K × {0} pointwise. This demonstrates why non-innerness of a subgroup map alone would be insufficient and why an argument that silently made all ambient automorphisms inner would fail.

For any hypothetical extension of the specific φ, the prescribed restriction additionally requires χ|_K = 0. Neither this condition nor any choice of χ changes β. The contradiction in the preceding section remains. The author therefore correctly avoids relying on the overstrong natural-Aut-equals-Inn reading of the old remark. No replacement automorphism classification is needed.

## Prior credit and author turn accounting

The prior source contains the normal pure sphere subgroup construction and the distinguished-puncture obstruction. The author packet makes the orientation convention and the exclusion of all ambient automorphisms explicit using the characteristic-center quotient. This is appropriately presented as a credited prior-literature consequence, without a new-discovery or first-resolution claim.

The inherited target report was only triage. The author counted the single completed construction and quotient obstruction as one substantive approach, leaving four unused. This audit checks that same approach and does not introduce a new research approach. The proposed **already_solved, 1/5** disposition is accepted.

## Source inspection and limits

Fresh independent checks were performed as follows:

- The existing Farb-volume PDF was rehashed. Its relevant text was freshly extracted; PDF pages 92 and 94 were locally rendered and visually inspected, confirming printed pages 85 and 87, the exact notation, and the footnote. Online PDF text was also checked. No claim of whole-volume inspection is made.
- The existing authorized Behrstock–Margalit author PDF was rehashed. A fresh extraction was read for the extended conventions, Theorem 6, §4.2, and Proposition 9. Pages 5, 7, and 8 were rendered and visually inspected. The 2005 author manuscript is the byte-pinned mathematical source; the journal PDF was not compared line by line. The [arXiv abstract record](https://arxiv.org/abs/math/0504328) independently confirmed the journal citation and v2 date.
- Bridson–Wade arXiv:2306.13437v2 §6 was read online, including definitions, Proposition 6.1 and proof, Lemma 6.3 and proof, Proposition 6.4 and proof, and the concluding commensurator discussion through Theorem 6.6. No PDF bytes or PDF page images were retrieved for this source. No PDF hash or byte count is claimed. Search-visible [Oxford repository metadata](https://ora.ox.ac.uk/objects/uuid%3A47e5bae4-96ff-4229-b2ee-18ed96e3ad67) states published and peer-reviewed status; opening that record directly returned a cache-miss error. The successfully opened [Oxford Mathematical Institute record](https://www.maths.ox.ac.uk/node/67343) independently confirms the journal details.
- The prior denied arXiv math/0504328 PDF download was not retried or bypassed. This audit used the already authorized author-hosted copy for the mathematical checks and an online abstract-record read. It did not download that arXiv PDF or attempt to acquire another copy as a substitute for the denied action.
- The live UnsolvedMath page and its present status were not independently checked. The author's reported access failure remains historical, and no live-site status claim follows from this audit.

The mathematical proof is symbolic. No computational checker is required, and hashing or finite permutation arithmetic is not offered as a substitute for the topological theorems. Public source metadata and exact inspection history are recorded in SOURCE_INSPECTION.json. Source PDFs, extracted text, rendered pages, datasets, private coordination material, and private checker fingerprints are absent from the safe archive.

## Acceptance conditions and outstanding issues

There are no required proof repairs, no unresolved mathematical blockers, and no accepted derivative replacing the original proof. The accepted mathematical artifact is the original pinned five-file freeze. Its independent audit and acceptance are additional documents with their own external manifest.

Acceptance does not assert a minimal index, classify every extendable subgroup automorphism, certify a live catalog update, certify publication, or replace the cited rigidity and branched-cover theorems with a formal proof. None of those claims is needed for the negative answer.
