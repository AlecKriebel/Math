# Independent complete-package adversarial review: PR 280 / 30000156

Review date: 21 October 2026 UTC. Source alias: OWR-768-006. This is an internal AI adversarial review, not formal independent human peer review or publication authorization.

**Verdict: one small package repair is required. No mathematical or original-source-scope defect was found.** The frozen verifier silently accepts JSON `true` and `1.0` as schema version `1`. The complete written theorem, including every further positive-upper-density selection and weak convergence, survives independent reconstruction and deliberate falsification. The bounded historical description is appropriately qualified; historical firstness remains uncertified, and the specific unrecovered 2011 manuscript must remain disclosed.

## Binding and independence

I copied and hashed all six publication-directory files before reading earlier review conclusions. The five release payloads are bound below; the release manifest itself is SHA256 `6209dc8ea3170a14d7fd813d541f11f7346b952d2acf171f8637c962be98ddd0` (1,245 bytes).

| File | Bytes | SHA256 |
| --- | ---: | --- |
| fixed-birational-cycle-nonlimit.pdf | 95,372 | b50733aec7165fc6d1848070222b94da41350bc32ccc6fc977ff3b95187cb540 |
| fixed-birational-cycle-nonlimit.tex | 19,866 | 3ee2a99514d1724f68bc00dcff43bd5115499c0b9f3d7678c49961c44a4af983 |
| fixed-birational-cycle-nonlimit-verification.zip | 124,172 | bed96c7fe5443ec70c278aeeb23f3b264d13f6eada312e5165df0b1e5ca96f8c |
| zenodo-deposit.json | 5,371 | 04b95ca27881af6238090f920e156d05c183defc66494496d458ce947023c75e |
| README.md | 1,844 | 65d7f45869d0ca7910deaa38790cee5cb8db4fe41943fd1d6c8b8352468e6754 |

I first read the complete actual two-page [original contribution](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf), then the full final TeX. The independent reconstruction and attempted objections were written in `INDEPENDENT_RECONSTRUCTION.md` before opening earlier review conclusions. Both original pages and all six final manuscript pages were visually inspected. Actual primary mathematical bodies were retrieved afresh. Only after the independent checkpoint did I compare the historical reviews, preparation receipts and root assessments. Agreement with those opinions is not a premise of this verdict.

All work was confined to the assigned review directory and ignored `private/pr0280_package1` custody. I did not edit the canonical paper, source snapshot, other review families, Git index/branches/refs, PR, provider state, ledger or publication state. I communicated only with the parent agent. No individuals or unrelated chats were contacted, and no outreach was prepared.

## Finding P280-PKG-01: schema type is not checked

Severity: low; mandatory repair for the advertised strict schema guard. Location: archived `verify.py`, lines 22–24, also the identical preparation wrapper.

The guard checks `manifest["schema"] == 1`. Python considers both `True == 1` and `1.0 == 1` true. In disposable copies of the actual extracted ZIP, changing only the un-hashed top-level manifest's schema value to JSON `true` or `1.0` still produced `status: PASS`, verified all 64 payloads and executed all 147,619 finite checks. Both malformed versions pass in normal and optimized mode. `NEGATIVE_CONTROLS.json` records all four unexpected acceptances and exact outputs.

Require the schema value to have exact integer type as well as value 1, for example `type(manifest["schema"]) is int`, before accepting it. Preserve the current frozen evidence; repair the canonical preparation wrapper, rebuild and rebind the ZIP, repeat the meaningful negative controls, and obtain a new independent complete-package review of the revised binding.

This defect does not change the mathematics or falsify a current payload hash. The frozen package has a valid integer schema. The separately bound ZIP hash still identifies its exact bytes, and the manifest is expressly an integrity record rather than a signature. I am not claiming resistance to an attacker who coherently replaces the external binding and all manifests.

The other 34 of 38 negative-control attempts rejected as expected: changed proof, changed checker, changed expected results, missing/extra files, file/directory/manifest symlinks, duplicate members, parent/absolute/backslash paths, extra schema keys, an unknown numeric schema, boolean/float byte counts and command-line overrides. Explicit runtime guards remain active under `-O`.

## Mathematical reconstruction and falsification

The exact claim is one fixed map over Q, `L(u,v)=(u,(u²+1)v)`, reduced at primes `p=3 mod 4`, with all affine points given equal mass and periods divided by p. For fixed `1/2≤x<1`, it proves the quantitative bridge to `1−φ(p−1)/(p−1)`, two incompatible subsequences, and nonconvergence on every further subset of positive upper relative prime density. The weak-limit claim is about the actual point-period probability measures.

I tried the following materially different failure mechanisms.

| Approach family | Falsification attempted | Outcome and exact limit |
| --- | --- | --- |
| Algebra and finite dynamics | Non-birationality, contraction lines, missing inverse points, incorrect invariant/genus/order | Rational inverse and genus-zero invariant are valid; both directions are total on the selected finite affine planes. Complex contraction lines explain why this is not a polynomial automorphism. |
| Counting and scaling | Equal-cycle weighting, discarded fixed points, wrong p scale, premature or moving cutoff | Each primitive fiber contributes p−1 points. The exact identity requires the stated eventual fixed-x cutoff. The p=3 and moving-endpoint controls expose the invalid stronger assertions. |
| Character arithmetic | Incorrect primitive indicator, character multiplicities, principal zero count, quadratic exceptional case | The indicator factors correctly. The principal term is exactly pθ. The exceptional quadratic character has Jacobi magnitude 1; the other relevant sums have magnitude √p. |
| Analytic limits | Unproved Artin input, invalid growing-modulus uniformity, divergent coefficient series, wrong residue-class inference | The stated Siegel–Walfisz truncation and absolute convergence justify the classical mean. The mod-4 split is essential and correctly supplied. |
| Density and weak convergence | Inferring arbitrary-subset failure from two sparse sequences; treating a CDF jump as a weak-convergence obstruction | Neither invalid inference is used. The credited atomless law rules out scalar convergence on positive-upper-density subsets; a single bounded continuous moment rules out weak convergence. |
| Historical priority | Mistaking old ingredients, a parameter-ensemble theorem or a citation context for an exact earlier application | The ingredients are old and properly credited. No exact earlier application was authenticated in the passages independently checked. The unseen 2011 body remains an unresolved bibliographic limit. |
| Package parser | Silent malformed metadata acceptance | Concrete schema-type acceptance found, as reported above. |

The full derivation is in `INDEPENDENT_RECONSTRUCTION.md`. Key checks are these:

* `u²+1` is never zero on the selected fields. Nonzero v has period the multiplicative order of its multiplier; v=0 has period 1. All periods divide N=p−1, and the fixed-point count is 2p−1.
* Every proper divisor of N is below p/2. Once `p>1/(1−x)`, exactly the primitive fibers are excluded, so `D_p(x)=1−(p−1)P_p/p²`. At the moving threshold `(p−1)/p`, all points are included. The written theorem does not interchange these quantifiers.
* The elementary character proof handles both χ=η and the principal character, giving the printed primitive-value bound. The six-small-prime argument gives `2^ω(N)≤64N^(1/4)`, hence the displayed vanishing error.
* Möbius inversion, the tail `O(X/(log X)^6)`, and the small-modulus weighted error `O(X log log X/(log X)^4)` justify the prime mean using the named standard theorem. The product bound `A≥7/24>13/48` is correct. CRT/Dirichlet forces θ→0 on one admissible sequence; the mean plus the two mod-4 class densities forces infinitely many admissible θ≥1/24.
* The stronger selection result requires the old continuous scalar law. If θ converged on a positive-upper-density subset, shrinking closed intervals about its limit would force an atom. Positive upper density inside the density-1/2 class suffices; a conditional law on that class is unnecessary.
* The bounded continuous function `h(t)=max(0,min(1,2t−1))` has exact expectation `(1−2/p)(p−1)P_p/p²=θ_p+o(1)`. Proper-divisor periods contribute zero. This excludes weak convergence without assuming that a candidate limiting CDF is continuous at a selected threshold.

No mathematical gap remains in the stated theorem, conditional only on the expressly named classical inputs. Finite computations do not supply the infinite-prime mean, subsequences or atomlessness.

## Original problem and scope

The [institutional report](https://publications.mfo.de/bitstream/handle/mfo/2873/OWR_2004_54.pdf?isAllowed=y&sequence=1) independently confirms printed pp.2944–2945 (PDF 32–33). The source fixes the extension degree, then uses q=p; its statistic weights affine points by p⁻² and uses threshold px. Its first existence assertion is universal over birational maps. Genus one enters a subsequent heuristic, and the single-reversor condition belongs to a separate refinement. The polynomial forward formula puts this example within the displayed affine setup; no projective singularity convention is needed.

The manuscript correctly states that its inverse is not polynomial over C. It makes no claim for elliptic-fiber families, polynomial automorphisms, all extension degrees, arbitrary zero-density selections or the later prime-averaged conjecture at p² scale. The strengthened positive-upper-density argument also closes an otherwise real loophole about a further suitable-prime selection. The paper negates the broad existence assertion with its actual quantifiers; it does not classify every narrower model.

## Actual primary inputs and bounded priority challenge

`PRIMARY_SOURCE_RECEIPTS.json` records fresh downloads of all seven cited primary PDFs. Every byte count and SHA256 matches the package's `SOURCE_REFERENCES.json`. My actual reading scopes are separately stated in `PRIMARY_READING_SCOPES.json`.

* [Ostafe–Shparlinski v3](https://arxiv.org/pdf/0902.3884v3), §2.1 equations (1)–(4): after exchanging coordinates, m=1, a=1, b=0, g₀=X₁²+1 and h₀=0 satisfy the older family's leading-monomial and degree conditions. The family is not new here.
* [Booker–Cohen–Sutherland–Trudgian v2](https://arxiv.org/pdf/1803.01435v2), equations (5)–(6), definitions and Lemma 1: e₁=1 and e₂=p−1 are allowed. The quadratic has nonzero leading coefficient and discriminant at odd p. Since Q(0)=1 is not primitive, their count equals P_p, with their principal term p−1 because their first principal character removes zero. Their slightly weaker error still gives the same bridge. The manuscript's self-contained Jacobi proof does not claim a new arithmetic estimate.
* [Menici–Pehlivan](https://www.impan.pl/shop/en/publication/transaction/download/product/91625), Lemma 2 and its full proof on printed pp.262–263: r=m=1 is exactly the unconditional shifted-prime mean. The actual proof invokes Siegel–Walfisz; GRH from other contexts is not a hidden hypothesis.
* [Aivazidis–Sofos v2](https://arxiv.org/pdf/1308.5701v2), Theorems 1.1(i), 1.3(i), n=1, introduction attribution and §6 on printed pp.16–17: the scalar limit is continuous. The proof directly treats primes, verifies the additive-function convergence and divergence conditions, and then compares prime powers. Proper powers are negligible here. The manuscript uses continuity, not absolute continuity.
* [Deshouillers–Hassani](https://doi.org/10.1017/S1446788712000250), introduction and Proposition 2.1 with m=2, including its explicit totient application on printed pp.77–79: the law over odd primes is continuous and hence atomless. Excluding the single prime 2 does not change the all-prime law. The year/online-date distinction in the bibliography is accurate.
* [Roberts 2011](https://www.dma.uvigo.es/~eliz/pdf/Roberts.pdf), printed pp.217–221 and reference 9: the citation to the four-author preprint is real. Its surrounding text concerns reversible gamma distributions and denominator singularities, but cannot certify the unseen body's complete content.

I independently pursued exact-map/nonconvergence searches, the exact 2011 titles and author combinations, and the current author/publication pages. No authenticated exact earlier application was found in those bounded checks. Fresh nearby-body checks are bound in `BOUNDED_PRIORITY_SOURCE_RECEIPTS.json`: Roberts–Vivaldi 2009 introduction/Theorems A–B and ensemble definition; Jogia–Roberts–Vivaldi 2006 full finite-field discussion on author pp.13–16; the Casati–Prosen 2012 paper's abstract/introductory passages, complete conclusion and reference 5; Neumärker's 2012 summary/outlook and reference 63; and Siu's 2019 printed pp.67–69 including Theorem 6.3.9. The last result explicitly fixes p and varies a cat-map parameter. It is not the present fixed triangular map across primes. None of these scoped readings authenticates the same fixed-map negative result.

Whole-body keyword screens are labeled as screens in `PRIORITY_KEYWORD_SCREEN.json`, not represented as whole-thesis reading or exclusion of differently worded equivalents. The current official Siu download has a generated repository cover and a different hash from earlier custody; I bind the actual file read and claim no byte identity or new mathematical version. I did not repeat the private account/ledger query. I inspected the redacted preparation receipt and checked that its bounded, time-specific character is accurately described; it is not an atomic future publication lock.

The map family, scalar oscillation and scalar continuous law are old, and the target application is a modest corollary of old ingredients. That assessment is not authentication of a prior publication of this exact application. Conversely, failed searches do not certify originality. The full body/version relationship of Neumärker–Roberts–Viallet–Vivaldi 2011 remains unresolved. The paper, archive README and metadata retain that exact uncertainty and do not claim worldwide absence, firstness or present open status. Under that limited description, this is not an additional repair finding.

## Archive, reproduction and preservation

The actual bound ZIP has 65 safe, unique regular-file members: one top manifest plus 64 payloads. Extraction was checked before writing files; all members were read successfully. The top manifest verifies the exact file set, lengths and hashes. The original frozen manifest (9 entries), original review manifest (6), historical arithmetic output manifest (25) and historical source artifact manifest (9) also match. All 17 original files independently match both their SHA256/Git-blob pins and `git show` at commit `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`. No Git state was changed. `MANIFEST_IDENTITY_CHECKS.json` records these checks.

The ZIP TeX is byte-identical to the release TeX. All 36 entries of the preparation seal verify, and the preparation manifest has the supplied SHA256 `5caa9469cf4149de9f38775c204855e837133c84112a59f28b2a84a4ca210ce0`.

I ran the actual extracted `verify.py` with Python 3.9.6, 3.12.14 and 3.14.6, each normally and with `-O`. Every run passes 147,619 exact finite checks over 87 admissible primes through 1000, eight raw graphs/6,088 points and six bad-prime controls, with all 64 payloads verified. The tree's file set and hashes are unchanged after replay. The `/usr/bin/python3` launcher requested an Xcode license; the directly installed Python 3.9.6 binary works. No system setting or license was changed. `INDEPENDENT_REPLAY.json` preserves this distinction.

I also wrote an independent checker using direct repeated multiplication for orders, direct whole-plane orbit traversal and gcd-count totients, without importing submitted checker code. It passes 38,150 exact checks for 34 admissible primes through 311, with 11 full graphs/19,099 points, moving-boundary controls, p=2 and six 1-mod-4 collision controls, and the totient lower bound through 1500. See `INDEPENDENT_FINITE.json` and its reproducible script.

The historical 8,347,742 finite and 230,780 analytic counts are correctly presented as separate earlier receipts; I did not relabel them as new runs. Literal replay of the two original SymPy scripts, in disposable copies, fails at the absent import as disclosed (`LEGACY_REPLAY.json`). Default and bundled runtimes lack SymPy. The new finite replay is genuinely standard-library-only. No infinite assertion is presented as a numerical extrapolation.

## Presentation, metadata and privacy

All six final PDF pages were rendered from the bound PDF and individually viewed:

1. Title, author, ORCID, version/date, abstract, map and probability definitions are consistent and legible.
2. The complete theorem, source qualification, exact point dynamics and fixed/moving endpoints are visible and correctly typeset.
3. The indicator, character/Jacobi/Gauss formulas, exceptional case and primitive-value credit match the TeX.
4. The prime and odd-prime subscripts are correct. The mean, constant separation, subsequences and scalar-law display are clean.
5. Atomlessness, the subset proof, exact continuous moment and unrecovered-source disclosure are fully legible.
6. Finite/historical computation boundaries, extensive AI disclosure, unrefereed status and complete bibliography are clear.

No clipping, overlaps, undefined references, damaged symbols or unreadable material were found. `PDF_STRUCTURE.json` independently verifies six pages, the exact title/author and UTC creation date, correct external citation/ORCID link targets, no encryption, no form and no embedded files. A compiler rebuild was not needed for this read-only review; the full rendered text and bound source were compared, and the earlier build/visual receipt was checked only after my own inspection.

The outer README, archive README, CITATION.cff, license and local deposit metadata agree on title, author/ORCID, version, date, CC-BY-4.0, preprint status and intended PDF/ZIP uploads. No own DOI is allocated in these files, and none claims a live publication. Established reference DOIs are distinguished from an identifier for this note. Review/publication outcomes are explicitly recorded separately. Extensive AI involvement includes research, proof/model development, computation, literature, writing and auditing; formal independent human peer review is expressly absent.

All archive members are UTF-8 text and were screened across the complete set, supplemented by manual inspection of the narrative/code/receipt roles. No credential patterns, private account identifiers, email addresses, raw account/ledger bodies or third-party complete source bodies were found. A few historical receipts retain the author's local research-custody paths; these disclose no unrelated account data. Third-party PDFs, full extracts and original-source page images exist only in the assigned private directory, and every one is independently confirmed Git-ignored (`PRIVATE_CUSTODY_MANIFEST.json`). They are excluded from the ZIP and this review's public evidence tree.

## Exact remaining work and limits

The repair is strict integer typing of the manifest schema, followed by rebuilt bindings, reproduction/negative controls and a new independent full-package review. The specific 2011 bibliographic uncertainty remains a disclosed limit, not an inferred proof of duplication or an impossible worldwide-absence requirement. No mathematical correction is currently identified. This review does not authorize integration, publication, DOI allocation, provider writes or a claim of worldwide novelty.

Assigned complete-package review completion: **100%**. The mathematical statement's strongest verified content is the theorem as actually printed, including the positive-upper-density and weak-convergence conclusions. The package is **not cleared unchanged** because of P280-PKG-01.
