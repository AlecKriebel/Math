# Second independent full package adversarial review

**Verdict: QUALIFIED PASS. No substantive mathematical defect or required package correction found.**

Review completed: **2026-10-24 19:14:39 UTC**. Best-guess completion of this assigned review: **100%**. This is a workflow estimate, not a probability of mathematical truth. The qualifications are the disclosed original-1986 source-custody limitation and bounded priority assessment described below.

I did not author the proof or any preceding review. I reconstructed the complete argument independently before consulting the previous package review for its historical scope. Earlier PASS verdicts were not used as mathematical evidence. This is an independent adversarial **AI** review; it is neither independent human peer review nor formal proof-assistant verification. No first-discovery certification is asserted.

All extraction and generated work is under `package_review2/`; this report is the only other file written. No reviewed candidate, Git state, publication record, or outside communication was changed. No other agents or children were contacted or created.

## Exact fixed artifacts

The assigned hashes were recomputed at the start and end and match. The deposit metadata was also hashed and reviewed.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `publication/source-and-verification.zip` | 170274 | `e1fc9b2568e324aa5d2d45d29ceeca79c390f5424c7d790e108d0be6a277ec19` |
| `publication/paper.pdf` | 92698 | `5788ee036f6b3c3932bb6c0c18e5ec581678bf5951a18d76d853545370fd0c9c` |
| `preprint/main.tex` | 23341 | `36d6afdfa88437c9f1d35afa17e537b98edce4cfa698564475be554b69daaa2b` |
| `zenodo-deposit.json` | 5189 | `474e667125730538c4959de79b1f0c5e223316356713db52b5def8b45fc71410` |

Machine-readable evidence is in `package_review2/FINAL_RECEIPT.json` and `package_review2/reproducibility_receipt.json`. The checkpoint log is `package_review2/RESEARCH_LOG.md`.

## Complete mathematical reconstruction

### The exact problem and the AT target

I extracted the actual local official 20 October 2026 Notebook and checked Problems 9.76, 13.55, and 21.131. Problem 21.131 requests a homomorphism **onto** an infinite AT group from a subgroup of a Golod group, explicitly referring to 9.76. The paper supplies that epimorphism. The definition in 9.76 is the canonical finitely generated adjoint subgroup of a nonnilpotent nil quotient of a finite free nonunital algebra in characteristic p; it does not impose homogeneity or residual finiteness. Problem 13.55 instead asks whether an entire Golod group is isomorphic to an AT group. The paper correctly leaves that distinct problem open.

For the target, the vertices `0^(n-1)1` form an antichain. Hence the directed generators have disjoint local supports, commute, and have order p. A finite product with a nonzero exponent at one selected label has a nontrivial portrait at a vertex carrying that label. This proves independence and an infinite elementary abelian directed subgroup. Countability follows from countably many generators.

Every directed generator fixes the all-zero ray and changes only the coordinate immediately after the first departure from that ray. For odd p, departures other than the symbol 1 may legitimately have identity action. Every label occurs infinitely often, so every designated longitudinal generator has infinite coordinate-level support. At each positive level, one designated generator supplies the full p-cycle, and the root subgroup supplies it at level zero. Thus each accompanying permutation group is transitive. The argument applies to p=2 as well as odd primes and does not replace original infinite-support generators by finitary automorphisms.

The local-finiteness proof is genuinely on the infinite tree. For a finite set of chosen labels I, a label absent from I occurs at some depth N. At depth N the side root cycle is absent, and the only remaining nontrivial generator sections are the directed tails at the zero vertex. Those tails still commute, have order p, and remain independent, giving a finite group B_N. Section multiplication and inversion keep every section of every word in the same B_N. The full action therefore embeds in the finite group `B_N^(p^N) semidirect W_N`. The empty I boundary case simply gives the finite root cyclic group. Every finite subset of the target uses finitely many labels, so the target is locally finite p. Its infinitude then implies it cannot be finitely generated.

I specifically checked the bad-cutoff obstruction: selecting a depth whose label belongs to I leaves a side rooted cycle not lying in the directed-tail group. The proof avoids that obstruction explicitly.

### Locally finite perfect envelope and augmentation input

At each diagonal wreath transition, finitely many elements have finitely many coordinates. Local finiteness of the preceding stage places all those coordinates in one finite p-subgroup, and adjoining the finite cyclic shift still gives a finite p-group. Thus every stage and the direct limit remain countable and locally finite p.

For an element of order p^b, a sufficiently late shift length is divisible by that order. The commutator with the coordinate function `f(i)=h^i` then equals the diagonal h at every coordinate, including wraparound. Every limit element becomes a commutator at a later stage, so the limit is perfect. This works for unbounded element orders, including a Prüfer target; no bounded-exponent assumption is hidden. The optional one-step construction for the particular AT target only needs its selected generators to have order p, not every target element.

Over any extension field of F_p, a finite collection of augmentation elements is supported in a common finite p-subgroup. The central-order-p induction correctly gives a nilpotent augmentation ideal there: the central ideal generated by z-1 has pth power zero, and the quotient reduces the group order. A finite matrix has finitely many entries supported in that one nilpotent ideal, so the matrix is nilpotent. This proves absolute stable nilness, with no assumption that the extension field is finite or countable. The group-basis map into the unitized algebra is injective.

The first clause of AAJZ Theorem 4.3 supplies a finitely generated **stable nil** containing algebra. The paper does not mistakenly use the second clause, which only supplies a nil algebra under a growth restriction. Unitization preserves the embedding, and an embedding carries the envelope's derived subgroup into the containing adjoint group's derived subgroup.

### Finite canonical subgroup and nonnilpotence

The elementary multiplication and commutator identities are correct over a noncommutative coefficient algebra with the stated commutator convention. Three coordinates supply the necessary distinct intermediate index. Induction constructs elementary matrices over every algebra word; addition and integer powers supply every prime-field coefficient. This last step would need revision over a general field but is correct over F_p.

The finite scalar elementary group Q has finitely many conjugates of each displayed elementary generator. Their generated group L is normalized by Q and by itself and contains the original generator set. Consequently it is normal in the full elementary group. This proves finite generation of the required relative elementary group without assuming a general finite-generation theorem over an infinite ring. All generators and their products lie in `1+M_3(B)`.

The six-factor formula for `diag(u,u^-1,1)` is correct. Reduction modulo B makes its product trivial, so this diagonal element lies in L. Its multiplicative defect is exactly `diag(1,u^-1 v^-1 u v,1)`; the order of these noncommuting coefficients is correct. These defects generate the diagonal copy of the derived unit group. The actual embedding is `h -> diag(1,h,1)`. No false homomorphism assertion for `u -> diag(u,u^-1,1)` is used.

Taking the nonunital algebra generated by the finitely many differences of L's generators produces a nil algebra inside the stable-nil matrix algebra. Geometric-polynomial inverses place L in its adjoint group with precisely the displayed canonical generators. Were the algebra nilpotent, its finitely many bounded-length generator words would span it; over F_p its adjoint group would be finite. The embedded infinite target rules this out. Each adjoint element has finite p-power order, so an infinite L cannot be cyclic. Removing identity entries and repetitions leaves at least two generators and does not change the difference algebra. This establishes the full 9.76 condition, including the finite canonical subgroup and nonnilpotence, rather than just an embedding in an unrestricted unit group.

### One fixed absolutely stable nil construction

I checked the delicate all-field-extension quantifier independently against AAJZ's actual manuscript. The polynomial-matrix seed algebra is countable dimensional over F_p and has locally subexponential growth: each finite subset lies in a finite matrix corner over finitely many commuting polynomial variables. AAJZ Lemma 4.3 therefore yields one fixed finitely generated infinite-dimensional algebra B_0 whose tensor product with that seed algebra is nil.

For every extension E/F_p and every finite matrix over B_0 tensor E, expansion into finitely many prime-field matrix units gives the paper's displayed finite tensor sum. The same expression with independent polynomial variables is nilpotent in the fixed universal seed. Evaluating those variables at the extension scalars proves nilpotence. This verifies absolute stable nilness of that same B_0 simultaneously for all E; it is not chosen after E. The updated explicit typing `Y_l in M_n(F_p)` is correct and makes this mechanism transparent.

The finite auxiliary matrix wreath algebra is an external semidirect sum with matrix ideal and nilpotent quotient. Base change and matrix amplification preserve that description. The elementary nil-ideal/nil-quotient argument is valid: for each element, a power enters the ideal and a further power vanishes. No uniform exponent is assumed.

For finite-row matrices, the base-change map is an injection, not an asserted surjection onto an infinite Hom space. In a finite tensor sum one can choose extension scalars linearly independent over F_p. Vanishing entry by entry then forces each original matrix to vanish. The common row support is finite. Matrix multiplication is defined by finite sums, and the two bimodule actions preserve finite-dimensional output support. These facts also establish compatibility with the external semidirect multiplication. No unsupported identification of tensoring with all infinite-column maps occurs.

After finite matrix amplification, flattening the blocks again gives a finite-row matrix. For a fixed finite row support T, restriction to the T-by-T corner is a homomorphism with square-zero kernel. Stable nilness of the coefficient algebra makes each corner element nilpotent, hence the original element nilpotent. The quotient by that finite-row ideal is a matrix algebra over the absolutely stable nil seed, so it is nil as well. This proves the needed nilness for every amplification and every extension.

AAJZ's explicit containment construction uses the same fixed seed and only two additional finite-row matrices. The countable-dimensional input has a generating linear map from the countably infinite seed unitization. Its resulting finitely generated containing algebra injects into the ambient semidirect algebra, and tensoring over a field preserves this injection. Thus the paper proves absolute stable nilness for the selected containing algebra. It never assumes that arbitrary stable nil algebras are absolutely nil.

### Homogeneous residually finite cover and actual epimorphism

Hammoudi Theorem 3 requires an **absolutely nil** algebra. The difference algebra has that property because after each field extension it injects into `M_3(B tensor E)`. The theorem's proof constructs homogeneous relations inside the original kernel using the same finite free generators. The source proof and its Corollary 3 therefore justify the claimed surjection from the corresponding classical canonical Golod group onto L. The relation budget is the classical Golod one; the covering algebra is nil and nonnilpotent.

The homogeneous quotient is positively graded with finite-dimensional homogeneous components. Its degree truncations over the finite prime field are finite nilpotent algebras and separate elements. Their adjoint finite p-groups consequently separate elements of the canonical subgroup, proving residual finiteness. The source group is infinite since its image L is infinite.

Finally, the inverse image of the embedded H under the surjection onto L is a subgroup, and restricting the surjection to that inverse image is onto H. This is the stated subgroup-quotient realization, not an unsupported embedding in a residually finite source. The Prüfer boundary case is therefore consistent: it may be a quotient of a subgroup of that source although it cannot itself embed in a residually finite group. The AT corollary follows from the verified infinite locally finite target.

## Primary sources and exact limitations

I inspected the actual local source PDFs, regenerated AAJZ/Hammoudi text, and checked the critical AAJZ printed pp.17–18 and Hammoudi pp.96–97 visually. Regenerated text is byte-identical to the stored derived text. Fresh web access also returned the primary AAJZ and Hammoudi PDFs. The principal source hashes are:

| Source | SHA-256 |
|---|---|
| Official 20 October 2026 Notebook | `f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118` |
| AAJZ author manuscript arXiv 1703.08734v2 | `d0a57570ceeed1b960ee1a146acbed8a82e95b9cc3211b7295da55831186d369` |
| AAJZ 2017 announcement | `0079e2e536569228a21569782ca7f08fb4b9e1d66a2a76cbf16a628481000451` |
| Hammoudi publisher PDF | `f97d36b0ae4d798afa4266ce64ffe455d89829611294da097e3e1a4c97162107` |
| Manually preserved original AT OCR receipt | `c96e6ca0dbcb43ee2ed946e9309860a22b4d9130f3dc05f9cef314e17caab5d7` |

The 2017 announcement's Theorem 6 establishes the earlier algebra embedding input; the precise countable-dimensional formulation and detailed numbering used in the paper are explicitly assigned to the arXiv manuscript. The inaccessible final 2019 journal PDF is not represented as having been inspected. Hammoudi's absolute-nil definition, exact Theorem 3, homogeneous-kernel construction, and Corollary 3 agree with the paper's use. The 93–101 page range is correct.

The original Rozhkov PDF bytes remain unavailable. A fresh request during this review was also inaccessible. I checked the preserved primary OCR receipt, including the infinite-support language, subgroup C/subset D distinction, and accompanying transitivity condition. That receipt candidly identifies itself as a manually preserved relevant excerpt, not original bytes or a complete raw extraction. The construction satisfies the stricter infinite-support requirement stated there. This review does not upgrade that custody evidence into an independently rendered 1986 source. The paper, README, and deposit metadata disclose this limitation consistently.

All 13 files listed in the main source manifest have matching sizes and hashes in the research repository. The added algebra/absolute-extension/absolute-review source manifests also match the available primary files and proof records. They are provenance records, not claims that third-party articles are contained in the archive.

## Reproduction, package integrity, and presentation

The archive contains 27 unique regular files, no absolute or parent-traversal paths, and no symlinks. Its manifest covers exactly the other 26 files. Every stated byte count and SHA-256 value matches. Archived TeX and paper agree byte-for-byte with the standalone fixed candidates. The historical first review is clearly a dated earlier checkpoint with its own earlier hashes; its presence does not claim that it reviewed the later bytes.

From the fresh extraction, `python3 verification/run_all.py` exited 0 on Python 3.14.6. It reproduced all packaged expected results, including byte-identical `latest_results.json`:

- 11,778 common-zero section checks;
- 63 named matrix checks;
- 348,516 fresh tree comparisons;
- 3,516 fresh algebra assertions;
- the construction-family finite images/transitivity and nonabelian wreath/augmentation results included in the full comparison.

Both `python3 -O verification/run_all.py` and `PYTHONOPTIMIZE=1 python3 verification/run_all.py` immediately exit 1 with the documented assertion-safety refusal. I read all five evaluator modules and the runner. Their arithmetic is exact, the documented canonical entry point is self-contained, and the negative controls genuinely reject a bad tree cutoff, an inadmissible wreath wraparound, and the false diagonal-map homomorphism. Historical direct-entry-point comments or audit links may refer to the full repository; they do not obstruct the documented runner.

As an additional independently authored falsification test, `package_review2/independent_stress.py` uses concrete 12-by-12 matrices with noncommutative unitriangular 4-by-4 coefficient blocks, imports none of the packaged evaluators, and checks the elementary commutator, diagonal factorization, defect, and actual diagonal embedding identities. All **468** named comparisons pass over fields of orders **2, 3, 4, 5, 7, 11**. The four-element field supplies a finite extension-field case in characteristic two. Each field also detects genuine coefficient noncommutativity and rejects the false auxiliary homomorphism. These finite checks remain supplemental, not proofs of universal quantifiers.

Tectonic successfully rebuilt the unpacked source into a seven-page PDF. The complete extracted text equals the submitted PDF's extracted text. The rebuilt PDF SHA-256 is `5ecfd498767794049dbf4db199b4b5d2e4463dcf68e072d97668a4bd7a1d3087`; differing build metadata does not require binary identity. I visually inspected all seven submitted pages and found no clipped equations, missing symbols, overlapping text, unresolved references, or unreadable content.

The deposit JSON, paper, README, and license agree on title, author and ORCID, date, version, files, scope, CC BY 4.0 treatment of original paper/prose/code, established references, and AI/human-review disclosures. Third-party article bodies are not redistributed. The metadata does not claim a finitely generated AT target, a solution of 13.55, a universal residual-finite embedding, formal verification, or independent human peer review.

## Priority assessment and disposition

I checked the packaged priority audit and subsequent scope addendum as dated records rather than mathematical authority. The final presentation correctly credits Phillips, AAJZ, Hammoudi, and Rozhkov. Fresh exact/related web searches located no contrary complete same-scope solution; the Phillips publisher record also confirms the cited 1979 correction. This is a bounded search and does not establish exhaustive priority, rule out unpublished work, or independently certify first discovery. The paper's wording preserves those limits.

**Final disposition:** the complete theorem, original-definition AT corollary, all-field scalar-extension argument, canonical relative elementary construction, homogeneous residually finite source, inverse-image epimorphism, exact finite supplements, seven-page presentation, metadata, licensing, and disclosures pass this second independent adversarial review. I found no required mathematical or packaging correction. The qualified PASS retains the openly stated original-1986 byte/raster custody gap and nonexhaustive priority limits. The publication decision remains with the parent workflow; this review performed no publication action.
