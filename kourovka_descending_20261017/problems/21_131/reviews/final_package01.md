# Final package adversarial review 01

**Verdict: QUALIFIED PASS. No substantive mathematical defect or required correction identified.**

Review completed: **2026-10-24 19:04:18 UTC**. Best-guess completion of this assigned review: **100%**. Best-guess readiness of the fixed package for publication, retaining its stated qualifications: **98%**. These percentages are workflow estimates, not probabilities that the theorem is true.

This was a fresh review of the entire seven-page preprint and its assembled reproduction package. I did not author its proof. Earlier review verdicts were not accepted as proof: I reconstructed the argument, checked its quantifiers and boundary cases, inspected the actual AAJZ author PDF and Hammoudi publisher PDF, and reran the canonical verification from a separate extraction. All work was confined to `package_review1/` and this report. No reviewed candidate files, Git state, publication records, or outside communications were changed.

## Fixed files reviewed

All four hashes were recomputed at the beginning and end of the review and remained unchanged.

| File | Bytes | SHA-256 |
|---|---:|---|
| `publication/source-and-verification.zip` | 160939 | `c3c813a59575d749acbd4c24fafc4d463fff75a645fb603aee60d5caae281886` |
| `publication/paper.pdf` | 92527 | `aa17be7d2c19a3668f88a10b265de083021c2025f68e0f28661c8b7df2dbf8d4` |
| `preprint/main.tex` | 23266 | `56dc49bab304bc6991111e98dfab60dcccf4a641159c833407b3ea57ed030312` |
| `zenodo-deposit.json` | 5189 | `474e667125730538c4959de79b1f0c5e223316356713db52b5def8b45fc71410` |

The machine-readable receipt is `package_review1/FINAL_RECEIPT.json`; the research log is `package_review1/RESEARCH_LOG.md`.

## Mathematical reconstruction and falsification attempts

### Original-definition AT target and actual infinite-tree local finiteness

I checked the original definition against the locally preserved primary OCR receipt at `independent_definition/sources/rozhkov_1986_successful_web_excerpt_receipt.md`, including the explicit infinite-support clause, the root subgroup / longitudinal subset distinction, and transitivity of the accompanying groups. The preserved receipt is properly labeled as a manually preserved relevant tool-visible primary excerpt, not original PDF bytes or a complete independently archived extraction.

For the proposed target, the vertices `0^(n-1)1` form an antichain. Thus each selected directed generator changes at most one coordinate of any tuple, fixes the all-zero ray, acts only immediately after its first departure, and has infinite level support because every label recurs infinitely often. The target does not silently replace the original generators by finitary ones. At every positive level, one selected generator supplies the full cyclic permutation; the other departing symbols may have identity action. This is sufficient for the accompanying group to be transitive for every prime, including odd primes.

The local-finiteness argument withstands the important bad-cutoff attack. For a finite selected label set `I`, a depth `N` whose label is absent from `I` removes the side rooted cycle. The only possible nontrivial depth-`N` sections of the selected generators are their tails at the all-zero vertex. These tails commute and generate a finite elementary abelian group, since their portraits remain disjoint and every selected label occurs after `N`. The section multiplication and inverse formulas preserve this one finite section group at every depth-`N` vertex. The resulting embedding in a finite wreath product proves finiteness of the whole generated subgroup on the infinite tree. No inference from apparent stabilization of finite quotients is required. The independent elementary abelian directed subgroup establishes infinitude; countability is immediate. Therefore the target is an infinite locally finite `p`-group, and consequently is infinitely generated.

### Universal locally finite envelope and augmentation algebra

The successive diagonal wreath construction works for arbitrary countable locally finite `p`-groups, including groups of unbounded exponent and the Prüfer group. Each transition preserves countability and local finite `p` behavior. For an element of order `p^b`, a later cyclic factor of order divisible by `p^b` makes the diagonal commutator formula valid at the cyclic wraparound coordinate. This condition is essential and is stated. The limit is perfect because every element becomes a commutator later, so the original group embeds in its derived subgroup. There is no assumption that an arbitrary target has exponent `p`.

For every extension field of the prime field, finitely many coefficients from the augmentation ideal are supported in a common finite `p`-subgroup. The central-element induction proves nilpotence of that finite subgroup's augmentation ideal over that extension field. Finite matrix entries lie in one such nilpotent ideal, proving absolute stable nilness. This argument uses characteristic `p`, not finiteness of the extension field. The group basis gives an injective map into the adjoint group.

### Finite canonical adjoint subgroup

I independently checked both noncommutative elementary identities and the six-factor diagonal factorization. The use of three matrix coordinates supplies a distinct intermediate index for every product word. Addition and integer powers give all prime-field coefficients. Thus the finite set of elementary matrices over algebra generators generates every elementary matrix with a coefficient in the nil ideal.

The scalar elementary group is finite. The finitely many scalar conjugates of the displayed generators generate a group normalized by the scalar group and by itself, hence normal in the whole elementary group. This establishes the claimed finite generation and the use of reduction modulo the nil ideal.

The auxiliary map `u -> diag(u,u^-1,1)` is **not** treated as a homomorphism. Its defect is `diag(1,u^-1 v^-1 u v,1)`. Those coefficients, as `u,v` vary, generate the full derived subgroup. The actual embedding is the homomorphism `h -> diag(1,h,1)`. The coefficient order is correct in a noncommutative algebra; the supplied negative controls detect the incorrect homomorphism shortcut.

The finite list of generator differences generates a nil subalgebra of the stable-nil matrix algebra. An algebraically nilpotent finitely generated algebra over the finite prime field would be finite, contradicting the infinite embedded target. Hence the algebra is nil and nonnilpotent. A single adjoint generator would have finite `p`-power order, so deleting identities and repetitions leaves at least two generators. This matches the exact definition in Notebook 9.76, rather than merely exhibiting the target in the unrestricted adjoint group.

### Absolute stable nil extension: all fields with one fixed seed

The crucial stronger lemma survives the all-extension quantifier attack. AAJZ Lemma 4.3 applies over the prime field to the countable polynomial-matrix algebra. Every finite set in that algebra is contained in a finite matrix corner over finitely many polynomial variables, so it has locally subexponential growth. The resulting one fixed finitely generated infinite-dimensional seed works for all field extensions: an arbitrary matrix over a scalar extension is a finite sum using prime-field matrix units, and polynomial-variable evaluation transfers nilpotence of its universal counterpart. The seed is not chosen afresh after choosing the extension field.

The finite auxiliary wreath algebra is an external semidirect sum with a matrix ideal and nilpotent quotient. The argument is valid after base change and after every finite matrix amplification: a power enters the nil ideal and a further power vanishes.

The infinite-dimensional scalar-extension map for finite-row matrices is only asserted to be injective, not surjective. Writing a finite tensor sum with extension scalars linearly independent over the prime field proves injectivity entry by entry. Multiplication involves finite sums because the right factor has finite row support. The two bimodule actions preserve finite row support; the semidirect sums are explicitly external, preventing an unproved intersection assertion.

After matrix amplification, flattening the blocks again gives finite-row matrices. For a fixed finite row support, restriction to its square corner is a homomorphism with square-zero kernel; stable nilness makes the corner nil. The quotient by the finite-row ideal is a matrix algebra over the fixed seed, also nil. This proves the required nilness of every matrix amplification. Tensoring the fixed finitely generated AAJZ containing subalgebra preserves its injection, so the argument establishes the stated absolute stable nil property for that same algebra.

No appeal to a general, unproved implication “stable nil implies absolutely nil” appears in the proof.

### Homogeneous classical Golod source and inverse-image epimorphism

Hammoudi's actual Theorem 3 on printed p.96 requires **absolutely nil**. The preceding construction supplies this for the difference algebra. I inspected the primary PDF proof through printed pp.96–97: its homogeneous relations lie in the original kernel and use the same finite free generating symbols. Corollary 3 on p.97 confirms the same-generator group lift. Thus the canonical Golod group maps onto the previously constructed finite canonical unit subgroup.

The homogeneous ideal makes the covering algebra positively graded with finite-dimensional homogeneous components. Over the finite prime field its degree truncations are finite nilpotent algebras and separate elements, so the associated finite `p`-group maps separate group elements. This proves residual finiteness of the classical source. It is infinite because it maps onto the earlier infinite group.

Taking the inverse image of the embedded target under that surjection gives a subgroup with an epimorphism onto the target. The argument does not infer that a Prüfer group embeds in a residually finite group. The paper correctly distinguishes universal embedding in the broad 9.76 source from the subgroup-quotient realization in the homogeneous residually finite source.

## Primary theorem and problem scope

I regenerated the text from the actual local source PDFs; the regenerated AAJZ and Hammoudi text agrees exactly with the stored derived text.

| Primary source | SHA-256 | Checked scope |
|---|---|---|
| AAJZ author manuscript, arXiv 1703.08734v2 | `d0a57570ceeed1b960ee1a146acbed8a82e95b9cc3211b7295da55831186d369` | Theorem 4.3 first clause; Lemmas 4.1, 4.3–4.5; explicit containing-algebra construction. Critical pp.17–18 also visually inspected. |
| Hammoudi publisher PDF | `f97d36b0ae4d798afa4266ce64ffe455d89829611294da097e3e1a4c97162107` | Absolute-nil definition; Theorem 3; homogeneous same-generator proof; Corollary 3. Printed pp.96–97 visually inspected. |
| Official 20 October 2026 Notebook | `f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118` | Exact 9.76 definition on p.38, distinct 13.55 on p.72, actual existential subgroup epimorphism request 21.131 on p.199. |
| AAJZ 2017 announcement | `0079e2e536569228a21569782ca7f08fb4b9e1d66a2a76cbf16a628481000451` | Theorem 6 records the prior stable-nil embedding input; it is not presented as a new theorem of this preprint. |

The original AT OCR receipt hash is `c96e6ca0dbcb43ee2ed946e9309860a22b4d9130f3dc05f9cef314e17caab5d7`. The residual original-PDF byte/raster limitation is not silently removed by this review. A fresh MathNet access attempt also timed out. The later definition is not substituted for the original infinite-support condition.

The AAJZ numbering is explicitly attributed to its author manuscript. The inaccessible final journal PDF is not represented as having been independently inspected. The use of the first stable-nil clause, rather than the second merely-nil growth clause, is correct. Hammoudi's page range is correctly 93–101.

## Fresh package reproduction and presentation

The archive was extracted only under `package_review1/unpacked/`. All archive paths were checked for absolute paths and parent traversal. `MANIFEST.json` has 23 entries and covers exactly every other package file; all byte counts and SHA-256 values match. There are 24 files including the manifest. The archived paper and TeX source are byte-for-byte equal to the standalone reviewed candidates.

Running `python3 verification/run_all.py` from that fresh extraction exited **0**, on Python 3.14.6, with:

- 11,778 common-zero section checks;
- 63 named noncommutative matrix checks;
- 348,516 fresh tree comparisons;
- 3,516 fresh algebra assertions.

The regenerated `verification/latest_results.json` is byte-for-byte equal to packaged expected results. The family finite-image/transitivity data and nonabelian wreath/augmentation results are included in that successful comparison. I also read all five evaluator modules and the runner. Their finite scope and exact arithmetic are consistent with the README. The bad tree cutoff, invalid cyclic wraparound, and non-homomorphic auxiliary diagonal map have genuine negative controls.

Running `python3 -O verification/run_all.py` exited **1** immediately with the stated refusal to run without assertions. This is the intended negative control, not a failed reproduction.

I recompiled the unpacked `main.tex` into `package_review1/rebuilt/` using Tectonic. Compilation succeeds, produces seven pages, and the complete extracted PDF text is exactly equal to the submitted PDF's text. The rebuilt PDF has hash `023bef25f14b80b4d65cc50d3c9e1538aa7275f45219909ec7f12422cc553bbe`; binary identity was not required because PDF build metadata may differ.

All seven submitted PDF pages were rendered and visually inspected. I found no clipped equations, overlaps, missing glyphs, unresolved references, or unreadable material. The ordinary proof and bibliography page breaks do not impair use.

The deposit JSON agrees with the paper and README on title, author/ORCID, date, version, file names, seven-page length, scope, license, references, and AI/peer-review disclosures. It does not claim a finitely generated AT target, a resolution of 13.55, independent human peer review, or formal proof-assistant verification.

## Priority and remaining qualifications

The paper's priority wording is appropriately bounded. It credits the established algebra embedding theorem, earlier periodic-group embeddings, Hammoudi's cover theorem, and original AT theory. It claims a complete deduction/application to the exact problem rather than origination of those inputs. I reviewed the packaged historical priority audit and its subsequent scope addendum, and conducted fresh exact/related searches. I located no contrary complete same-scope solution. This is not an independent exhaustive census of every database, inaccessible final paper, or unpublished work, and this report does not certify first discovery.

Two optional clarity/provenance improvements would be reasonable in a future revision, but neither is a substantive objection to this fixed package:

1. In the seed argument, explicitly writing that the `Y_l` may be chosen as matrices over the prime field (for example matrix units) would make the universal-element evaluation even more immediate.
2. Some historical audit links and evaluator direct-entry-point comments refer to the full research repository rather than archive-relative files. The documented canonical runner is self-contained and succeeds. The preserved original AT OCR receipt remains in the research repository rather than the archive; the current paper accurately calls it part of the local research record.

**Final disposition:** the complete proof, universal quantifiers, stronger classical-source section statement, verification package, presentation, metadata, and disclosures pass this adversarial review. The qualification is the explicitly disclosed original-1986 source-custody gap and the necessarily bounded priority assessment. No required mathematical or packaging revision was identified before consideration of the other final reviews.
