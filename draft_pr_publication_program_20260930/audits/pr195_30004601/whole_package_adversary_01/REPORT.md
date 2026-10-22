# PR195 publication package: fresh independent adversarial review 01

**Verdict: CLEANPASS. No substantive mathematical, reproducibility, attribution, disclosure, archive-integrity, or publication-package defect was found in the exact frozen package reviewed. No required repair is identified.** This is a completed AI adversarial review of the qualified research note and its accompanying package. It does not establish historical priority, conventional human peer review, publication, or completion of the parent's required successive-new-review process.

Review date: 15 October 2026 UTC. Completion estimate: 100% of this assigned whole-package review. All outputs are confined to this review folder. No reviewed input was changed, and the final input rehash matched the initial pins. No Git/index/ref/checkout/branch operation, remote write, publication, outreach, or editor-tab operation was performed.

## 1. Exact reviewed object and independence

The reviewed input is the sibling `publication_package_v1`, whose exact fourteen-file inventory and SHA-256 values are recorded in `REVIEWED_INPUT_PINS.json`. Its `SAFE_ALLOWLIST.json` matches its actual file set. The key supplied pins were independently confirmed:

| Object | Bytes | SHA-256 |
|---|---:|---|
| PACKAGE_SEAL.json | 2,649 | 466ea1c10b452fc90a8deaf026c3e211d534238d2b08ee00fe9259cfa8223eef |
| seven_plane_gin.pdf | 82,753 | 4cdc4d5810d0ffe09c23242aeea9560bd9dffcdacdc9c09f9b2133562d3d5180 |
| seven_plane_gin.tex | 18,436 | c824a6b0327044714027f80d5067488a1f5875a2007f1555b2c038d595a2e43d |
| verification-package.zip | 130,177 | 697fc4471fed5deaceb828f639f4147341472054dfa850f201d1da108a9b2c63 |

I read the manuscript, the original OWR conjecture, and the corresponding BPT/MPT primary statements before opening favorable archive audit reports or gates. `INITIAL_MECHANISM.md` fixes the resulting independent argument. Routing context supplied pins and the claimed scope; I did not use its favorable assertions as proof. Only afterward did I read all four archive reports, all six complete verifier programs, the exact certificates through reconstruction/comparison, nested manifests, gates, evidence matrix, query log, retrieval/scope records, research logs, and publication metadata. `COVERAGE.json` records coverage of all fourteen top-level files and all fifty-five ZIP entries.

## 2. Claim, falsification criteria, and mathematical result

The exact claim is over every characteristic-zero field K, for the ambient four-polar ideal J of

`Q=xy(x-y)(x-2y)zw(x+z+w)`.

With decreasing variable order and degree reverse lexicographic gin B, the pure-second-variable cutoff is 8 and B has a degree-7 minimal generator using the first three variables and divisible by the third. A largest-third-variable witness suffices for the conjecture's broader wording. No full gin, particular monomial exponent, smallest example, arbitrary-section result, or positive-characteristic extension is necessary or claimed.

I tried to invalidate each central implication, rather than merely match numerical outputs:

* **Ambient ideal and section:** the arrangement is central and essential because of the coordinate factors, and the seven factors are distinct. Euler's identity permits omitting Q in characteristic zero. All four ambient derivatives are taken before restriction. My new chain-rule control gives ternary restricted-arrangement derivative ranks 3 and 9, versus ambient-polar ranks 4 and 12. These ideals are different; the manuscript keeps them different.
* **All linear syzygies:** reduction modulo each nonzero distinct restricted factor is valid in a domain. It forces `a_i.u=lambda_i L_i`; substitution makes the trace condition both necessary and sufficient. The constant version proves independence of all four degree-6 polars. Thus the proof does not conceal extra degree-0 relations or assume minimality.
* **Trace and section ranks:** independent X,Y force the four pencil scalars equal. Independent ternary X,Z,W then force all seven scalars equal and `7a=0`, leaving no linear syzygy. In the binary case X,Z,W have rank two; the scalar parametrization has two parameters, and the trace has rank exactly one because its common-scalar coefficient is 7. Even vanishing of the other trace coefficient leaves the dimension exactly one. Nonzero X+Z+W ensures injectivity of the parametrization into actual syzygies.
* **Binary height and resolution:** after extending scalars, a projective common zero would lie on exactly one restricted factor by Euler and distinctness. Its ambient polar vector is that factor's nonzero normal times a nonzero product. This is impossible. The height-two, four-minimal-generator Hilbert--Burch hypotheses hold. The three positive syzygy coefficient degrees sum to 6. Exactly one is 1, so the only multiset is (1,2,3), giving binary quotient dimensions (3,1,0) in degrees (6,7,8).
* **Genericity over arbitrary K in scope:** the rank/distinctness conditions are open, and the explicit rational compatible flag belongs to them. Its full basis has determinant 1. The nonempty inverse image in GL4 meets the gin open. The required opens are K-defined opens in affine-space GL4, so the infinite-field rational-point assertion is valid here; it is not a claim about rational points of an arbitrary variety. Finite coordinate ranks supply corroboration, not genericity.
* **Section identity and minimality:** the classical revlex quotient identity gives the first-variable truncations of B. Strong stability makes the binary pure power standard when the binary quotient is nonzero, proving cutoff 8. The x3 multiplication kernels are 0 and 1 in the two relevant degrees. No ideal elements exist below degree 6. A killed degree-6 standard monomial therefore yields a degree-7 minimal divisor involving x3. A divisor of this first-three-variable monomial cannot involve x4, proving full-ring minimality. This closes the gap that would remain if one had shown only membership or used a third sectional row to detect arbitrary later-variable generators.

None of these attacks produced a counterexample or unsupported bridge. The excluded degenerate ternary flag and characteristic 7 each give rank 11 rather than 12, as expected. They support retaining the actual hypotheses and do not extend the claim.

## 3. Independent computations and inspection of certificates

`independent_controls.py` is newly authored for this whole-package review and imports no package verifier. It constructs ambient polars by the product rule, performs exact rational elimination, checks all 21 binary pair determinants, obtains the critical ranks, distinguishes the restricted Jacobian, and checks the excluded controls and rank-two flats. Its deterministic result is `INDEPENDENT_CONTROLS.json`. It reproduces:

| Section | Degree | Matrix shape | Rank | Quotient |
|---|---:|---:|---:|---:|
| ternary | 6 | 4 x 28 | 4 | 24 |
| ternary | 7 | 12 x 36 | 12 | 24 |
| binary | 6 | 4 x 7 | 4 | 3 |
| binary | 7 | 8 x 8 | 7 | 1 |
| binary | 8 | 12 x 9 | 9 | 0 |

I inspected the complete primary exact verifier, including its differentiation/substitution, exact row reduction, independent row/column minor selection, complete left-kernel construction, scalar syzygy system, primitive syzygy selection, and all signed Hilbert--Burch minors. The checked identities and nonzero minors supply both rank bounds. Equality with the saved certificate is exact byte equality. The orthogonal program checks the frozen primary implementation before loading it, supplies ideal-membership representations and checks all 21 binary Buchberger pairs, and limits its three/four-variable initial ideals to explicit coordinates through degree 7. Neither paper nor README promotes those checks to a full gin computation.

A newly extracted archive, entirely under `private_work/extracted`, passed the documented command using `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P verify_package.py`. `REPLAY_STDOUT.json` preserves the output. All four required programs passed: exact counterexample certificate, orthogonal certificate, three PT examples, and fourteen rigid octics. I also separately replayed the scalar/boundary and polar-algebra programs and matched their saved JSON objects exactly. Before/after file-set and hash comparisons confirmed that the replay added or changed no extracted files.

The verifiers use only the standard library. The documented Python 3.11+ requirement is correct for `-P`. The sealed older README's 3.10+ statement is expressly identified as a historical command-line error in the current README and does not make the current extraction command fail. No undeclared original-submission file, external service, installed CAS, or downloaded code is needed for the scientific replay.

## 4. Sources, attribution, and bounded predecessor comparisons

The exact second-variable target was independently read and visually confirmed in [official OWR, printed p.234, Conjecture 7](https://ems.press/content/serial-article-files/46883). [BPT Conjecture 5.7](https://arxiv.org/pdf/1801.09868) uses the exponent d0+1 and the bound d0+1, agreeing with the note's p. BPT Theorems 4.4 and 6.2 support strong stability and sections; the note safely uses the classical triangle mechanism inside B3. The [final MPT Conjecture 4.6/Theorem 4.7](https://ems.press/content/serial-article-files/52275?nt=1) uses zero-based indices and proves the three-ambient-variable arrangement case. The manuscript accurately retains and credits that result.

The [Falk--Proudfoot section 4 construction](https://arxiv.org/pdf/math/0002094v2) identifies shared coordinates, yielding the displayed parallel connection of U(2,4) and U(3,4). It also credits earlier matroid work; the note says the construction is classical and points to that presentation, rather than assigning firstness to itself. [Tohaneanu section 2.1](https://arxiv.org/pdf/1405.2122v2) does mediate the stated Orlik--Terao attribution. [Conca Lemma 1.2 and proof](https://arxiv.org/pdf/math/0210064) directly support the revlex section identity.

My independent flat computation finds exactly one codimension-two flat with multiplicity at least three: the four-factor pencil. Hence |S0|=1, s=3, d=7 in [Migliore--Nagel Theorem 8.11/Corollary 8.12](https://arxiv.org/pdf/2508.12113v1), giving precisely the note's five-generator J-top resolution. The distinction from four-generator J is real. Their section 3 also distinguishes restricting the ambient ideal from taking the restricted polynomial's Jacobian. Substantive prior family information is retained, without an unsupported inference that the J-top resolution itself establishes this counterexample.

The [PT2020](https://arxiv.org/pdf/1911.04083) and [PT2022](https://arxiv.org/pdf/2003.06294) target locations and earlier-example equations agree with the comparison programs. Their generic exclusions are justified: maximum-rank minors establish the needed open rank conditions; binary height and Hilbert--Burch supply the missing upper bounds. The eight-factor shifts are (2,2,3), cutoff 9, with no earlier third-variable kernel. The other two cutoffs are 7 and 5; all initial-degree gin elements lie in the binary truncation, excluding earlier third-variable witnesses. A WLP/SLP failure alone is correctly not treated as this conjecture's refutation.

I independently compared all fourteen defining equations in [Janasz--Pokora arXiv v4, section 5](https://arxiv.org/pdf/2502.17031v4) with the exact verifier, including all three quadratic-field equations. The source transcription is correct. Prime 1009 and the selected quadratic roots define valid residue maps. Full-column-rank nonzero minors and distinct-factor minors in the residue fields prove characteristic-zero nonvanishing. The generic binary shifts (2,2,3), cutoff 9 and zero earlier ternary kernels follow, without claiming a positive-characteristic gin. The 63 families remain expressly unexhausted.

This new review did not independently re-prove every theorem or repeat all 120 historical searches in the inherited 36-record audit. I read the complete evidence matrix, exact query log and relevant reports as dated authored audit evidence, and directly checked the above central sources and comparisons. The current paper does not claim a universal historical exclusion from that evidence. The [Ilardi institutional record](https://www.iris.unina.it/handle/11588/726226) still labels its postprint private/restricted; I obtained no full article. Its possible overlap remains unexcluded. The note's historical qualification is truthful and material, and is compatible with the expressly authorized bounded-publication scope. Access gaps are not repaired by inventing a firstness certificate.

## 5. Whole archive, source/PDF and metadata consistency

All 55 ZIP entries were inspected for names, lengths, hashes and file types. There are no duplicate names, traversal/absolute/backslash paths, symlinks, downloaded articles, private source folders, credentials, or third-party runtime dependencies. Exactly 54 payload files appear in the archive inventory; the inventory excludes itself, avoiding a hash cycle. Every inventory hash, all four nested safe allowlists/manifests, and every Root gate safe-file pin match. The six files duplicated at the top level and archive root agree byte-for-byte, including the manuscript source, current README and verifier. `ARCHIVE_INSPECTION.json` supplies every entry pin. Historical original-custody pins are identified as such and are not replay dependencies.

The six-page PDF was independently rendered and every page visually examined. Equations, table values, variable subscripts, author/ORCID, references and disclosures agree with the LaTeX source; no clipped or overlapping text, unreadable symbols or missing references were found. The standalone TeX source has no local-file includes or private source dependencies. I did not recompile it; the package contains two prior compiler-success attestations, and this review verifies the actual supplied PDF/source presentation. PDF metadata confirms six pages, no encryption, no forms and no JavaScript.

The title, author, ORCID, date, exact polynomial, cutoff, witness degree and characteristic-zero scope agree among the PDF, source, README, bibliographic file, and deposit description. The deposit identifies a preprint and the three actual output filenames. Its source identifiers agree with the cited works. The CC BY license is limited to authored materials and does not purport to license downloaded papers. No repository or deposit lifecycle code outside the package was reviewed or executed.

Extensive AI use, unrefereed status, absence of conventional human peer review, classical construction/method credit, unresolved historical priority, unestablished independence and public chronology, missing Ilardi full text, and unexhausted families/code/nine-factor gins are disclosed consistently. Old gates' false publication-ready states are dated historical records, not contradictory assertions about a later deposit. The reviewed package itself remains a frozen review snapshot and does not pretend this new review or publication has already occurred.

## 6. Findings, limits, and disposition

There are **no required repairs and no substantive findings**. Optional typographic cleanup: the current README joins a few words/numbers (`inspected36`, `and120`, `ideals,12`); these are cosmetic and do not alter a claim, a command, or reproducibility. The sealed older Python-version wording is already explicitly corrected by the current instructions. Neither item is a scientific or publication blocker within this qualified scope.

The strongest verified outcome is the explicit characteristic-zero counterexample with checkable proof and exact reproducible corroboration. The precise remaining scientific-history gap is historical precedence/independence beyond the bounded inspected corpus, particularly the inaccessible Ilardi text and unexhausted families, code and related examples. These limits must stay attached to publication. They do not invalidate the mathematical result or require universal historical certification before publishing the already qualified note.

**CLEANPASS applies only to the frozen fourteen-file package and fifty-five-entry archive identified above.** Any change creates a new reviewed object. The parent must still carry out its required subsequent fresh whole-package review and any publication steps; this report performs neither.
