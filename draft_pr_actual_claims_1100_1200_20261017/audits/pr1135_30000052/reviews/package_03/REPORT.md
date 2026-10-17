# Independent adversarial whole-package review 03

**Verdict: NOT A CLEAN PASS — two actionable P3 supporting-checker issues. Mathematics, operative manuscript/PDF, source matching, disclosed chronology, package custody and reproducibility otherwise pass the checks below.** The two issues do not change any proved value or the full negative answer. They should be corrected with consistent result/pin refresh before another frozen candidate is promoted.

This review was independently conducted on 17 October 2026 UTC, solely inside reviews/package_03. No earlier whole-package REPORT was read or treated as evidence. The supplied editorial-history receipt was read as a history record, not as acceptance. Existing mathematical and priority reports were read after reconstructing the main analytic mechanism; their conclusions were not premises. No candidate file, Git state, PR, comment, deposit, publication record or tracker was changed. No individual or other shard was contacted; only the parent was messaged internally. All retrievals were read-only.

## 1. All actionable findings

### P3-01: a binomial moment is still labeled a second factorial moment

Location: [the parent moment checker](../../root_reproduction/check_root_moments.py), lines 35–39, particularly line 39; the corresponding current result label is also in [ROOT_MOMENT_REPLAY.json](../../root_reproduction/ROOT_MOMENT_REPLAY.json), line 11. Generated archive copies retain these exact bytes.

The code evaluates sum over k of binom(k,2) P(N=k) and correctly obtains 3x². Its label is “second factorial moment.” Under the conventional falling-factorial definition the second factorial moment is E[N(N−1)]=6x², whereas the implemented quantity is E binom(N,2)=3x². The current main paper and ROOT_MATHEMATICAL_CHECK correctly write the latter quantity explicitly; the missed check/output label leaves terminology inconsistent.

Change the current checker comment and labels to identify E N and E binom(N,2) explicitly, then refresh every affected replay expectation, control pin and archive receipt. The numerical calculation needs no correction. Historical original-input editions should stay unchanged and remain identified as historical. A global scan of the extracted packet found no further current prose that confuses these quantities; other factorial occurrences are legitimate beta-integral factorials or a correct historical falling-factorial derivation.

### P3-02: the named iid fourth-energy adverse control tests 9 instead of 15

Location: [the broad priority checker](../priority_01/check_priority_bridge.py), line 102, and the corresponding named entries in its current normal/optimized JSON results. The entry named “replace-energy-with-iid-triple” tests energy(3) != 3².

For n independent uniform unit complex phases, expanding the fourth power shows that the surviving ordered tuples have equal positive and negative index multisets. Their count is 2n²−n, hence 15 at n=3, not 9. The coherent lattice Dirichlet energy is 19. Therefore the program's numerical predicate is true but does not exercise the iid phase-energy substitution claimed by its label.

Use energy(3) != 2*3²−3, or describe the existing predicate narrowly as dropping all off-diagonal contributions. The focused rotation and parent Fourier checkers already use the correct iid value. Refresh the broad checker fingerprint/results/manifest and affected package pins after correction. This is a diagnostic-description defect, not a gap in the valid Fourier proof or its positive controls. My independent control directly enumerates the iid surviving tuples for n=1,…,7 and verifies 2n²−n.

### Scope of the adverse-control review

I read every adverse branch in all seven supplied programs, including normalization, omitted modular bands/cells, missing generator cuts, odd exponents, triangle restrictions, fixed-generator substitutes, iid-triple substitutions, endpoint reflection, norm-versus-moment inference, Fourier phase cancellation and discrete-versus-continuous slope controls. Apart from P3-02, I found no other actionable diagnostic mismatch. Some controls intentionally test a specified coarse rational lower bound rather than characterize the sharp true moment; they are not evidence of an optimal threshold. The focused rotation proof separately certifies the 234 threshold for its Fourier bound using upper and lower rational bounds for π.

## 2. Exact target and independently read primary evidence

I freshly downloaded the official [OWR 13/2004 PDF](https://ems.press/content/serial-article-files/45858), read Novak's complete contribution on printed pp. 696–699, and visually inspected the actual definition and question on printed pp. 697–698. The body is 445532 bytes, SHA256 2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e.

The discrepancy is normalized anchored Lp discrepancy. The question compares expectations of its p-th power, discusses even p, counts j=0,…,n−1, and averages both real generator and shift over the entire product cube. Thus Z and Delta are independent continuous uniforms. There is no prime-n, rational-generator, selected-generator, fixed-generator, distinct-point conditioning or jitter restriction. A reversed case with n=3,d=1,p=4 answers this universal comparison negatively. It does not answer the separate final existence/upper-bound question for selected lattices, nor infer an ordering of expected norms.

A fresh read of the [2010 author book draft](https://web.maths.unsw.edu.au/~josefdick/preprints/Novak_Wozniakowski_book_2.pdf), surrounding printed pp. 68–70 with p.69 rendered, confirms Open Problem 41 has the same generator/shift law and root-of-moment comparison. Raising that nonnegative comparison to p gives the same target. Its historical open label supplies formulation context, not current novelty. This draft is 4724291 bytes, SHA256 941c51b4aa6271abca9ff8ed800b1b341452aaace2ad36c64b8d608324c2b84a; it is not conflated with a final-book edition.

Fresh retrieval receipts are [SOURCE_FETCH.json](SOURCE_FETCH.json), [BOOK_FETCH.json](BOOK_FETCH.json) and [CHRONOLOGY_AND_SOURCE_CHECK.json](CHRONOLOGY_AND_SOURCE_CHECK.json). Full third-party bodies, extracted text, raw APIs and renders remain ignored.

## 3. Independent reconstruction of every operative analytic claim

Write T_j={jZ+Delta}. Conditional on Z, T_j is a translate of uniform Delta, with a distribution independent of Z. Therefore T_j and Z are independent. For k≠j, multiplication of a uniform circle variable by the nonzero integer k−j preserves Haar measure; hence T_k={T_j+(k−j)Z} is uniform conditional on T_j. This proves pairwise independence, coordinatewise in every dimension, without asserting triple independence.

For n=3 let U=T_0 and V=T_1. They are iid uniforms and T_2={2V−U}. If 0≤x≤1/2 and U,V<x, the raw third coordinate lies between −x and 2x. The negative portion wraps outside [0,x), and the nonnegative portion does not wrap past 1, apart from null boundaries. The third inclusion is exactly U/2≤V<(U+x)/2. At every U∈[0,x] this interval has length x/2 and lies inside [0,x], so q(x)=P(all three<x)=x²/2 on the lower half.

For N=N_x, the exact identities E N=3x, E binom(N,2)=3x² and P(N=3)=q, together with total probability, give

(P0,P1,P2,P3)=(1−3x+3x²−q, 3x−6x²+3q, 3x²−3q, q).

Expanding sum Pk(k/3−x)^4 independently gives

F(x)=x⁴−(2/3)x³+(2/27)x²+x/27+(4/9)(1−2x)q.

On the lower half this is x⁴−(10/9)x³+(8/27)x²+x/27. The simultaneous reflection (Z,Delta)↦(−Z,−Delta) modulo 1 preserves the product law and complements the count at 1−x outside fixed-endpoint null events. Thus F(x)=F(1−x). Tonelli applies to a bounded nonnegative measurable integrand, giving

E disc4⁴ = 2∫[0,1/2]F(x) dx
=2(1/160−5/288+1/81+1/216)=19/1620.

For iid Bernoulli(x) indicators, a=x(1−x), E Y²=a and E Y⁴=a−3a². Only single-index and two-pair patterns survive the centered fourth expansion. Consequently the integrated iid expression is

[n/6+3n(n−2)/30]/n⁴=(3n−1)/(30n³).

At n=3 it is 4/405=16/1620. Independently, changing q=x²/2 to q_iid=x³ makes the lower-half pointwise difference (2/9)x²(1−2x)². Its doubled integral is 1/540, strictly positive, and the ratio is 19/16. Thus neither the sign nor the normalization depends on floating-point subtraction.

For the second proof let n≥3. On 0<Z<1/(n−1), 0<Delta<1−(n−1)Z, all n indexed points lie without wrapping between Delta and Delta+(n−1)Z. Below and above them, empirical masses are exactly 0 and 1. The two outer intervals contribute

[Delta⁵+(1−Delta−(n−1)Z)⁵]/5.

Its unconditional product-density integral on this triangle is 1/[105(n−1)]. Reflection produces the descending triangle 1−1/(n−1)<Z<1, (n−1)(1−Z)<Delta<1, with equal contribution. Generator interiors are disjoint for n≥3, including the touching-closure n=3 case; boundaries have zero area. No division by the triangle area is warranted. Nonnegativity elsewhere yields the claimed bound 2/[105(n−1)].

At n=4, the bound exceeds iid by 5/8064. For all integers n≥4, clearing positive denominators reduces comparison to 4n³−21n²+28n−7>0. Substitution n=4+t gives 25+52t+27t²+4t³>0 for t≥0. At n=3 the bound 1/105 is below iid, so the exact three-point proof remains essential. This bound is not an assertion of an exact full-moment asymptotic.

For any anchored d-dimensional box with volume v, pairwise independence gives normalized count variance v(1−v)/n. Integrating v and v² gives (2^(−d)−3^(−d))/n for every positive n,d, identical to iid. At n=1 the whole law is one uniform point; at n=2 the inverse map is Delta=U, Z={V−U}, so the entire ordered pair is iid uniform coordinatewise. This establishes equality of all defined measurable ensemble functionals for n≤2, and thus minimum counterexample point count three.

Collisions are retained with index weight 1/n. For fixed finite n,d they form a null generator set. Point/box endpoints are null for each fixed tested endpoint, and for a fixed configuration only finitely many integration endpoints are affected. No positive-measure parameter event is deleted. Closed versus half-open cubes therefore do not alter the expectations.

## 4. New exact control, supplementary n=4 value and actual failure tests

[independent_control.py](independent_control.py) was newly written in this review and imports no supplied checker or external author's program. It uses exact standard-library Fraction arithmetic. The distinct implementation uses telescoped order-statistic antiderivatives, then integrates affine endpoint powers by a binomial formula, without polygon clipping, fitted degrees or interpolation.

For arbitrary fixed positive n, partition Z at every rational m/k with 1≤k<n. Between consecutive cuts, every floor floor(jZ) is fixed. The wrap thresholds Delta=floor(jZ)+1−jZ are affine, and cannot cross each other or 0/1 in an interval without an indexed difference times Z becoming integral, which would be a listed cut. Their ordered strips exhaust the shift interval. On each strip the indexed floors and point ordering are fixed, since a point tie likewise requires an indexed difference times Z integral. These strips partition the square outside finitely many line segments.

For sorted points s1≤…≤sn and even p, endpoint integration telescopes to

disc_p^p = (p+1)^−1 sum over r=1,…,n of
[(sr−(r−1)/n)^(p+1)−(sr−r/n)^(p+1)].

Each sr=jZ+Delta−floor_j. Integrating Delta between affine boundaries gives differences of affine powers of degree p+2, divided by (p+1)(p+2). Direct binomial integration in Z is exact. Closed-cell vertex checks validate the affine floor/order inequalities, and total cell area is checked to be one; the preceding structural proof, not those finite checks, establishes completeness.

The control recomputes 21 full lattice/iid moment pairs for n=1,…,7 and p∈{2,4,6}, including 19/1620 and the complete n=4 value 139/17280. Its n3/n4 cell tables are public in both result files. The independently reconstructed iid comparator uses the full binomial law and integer beta integrals. All 21 pairs agree with the supplied exact audit as data; no supplied program is imported.

It also verifies the tail integral by simplex monomials, the positive all-n polynomial coefficient certificate, iid phase fourth energy by actual surviving-tuple enumeration, the Dirichlet energy by difference multiplicities, the rational Fourier threshold certificate, two-point torus inverses and deterministic reflection. Adverse controls distinguish iid triples, invalid global q, weak n3 tails, fixed-zero-generator uniform-shift averages, incorrect collision normalization, missing positive-area cells, odd p without absolute-value splitting, finite even-grid multiplication, endpoint complement exceptions, and unsupported mean ordering from fourth moments.

Normal and optimized executions each pass 7223 explicit requirements and produce byte-identical complete JSON. Both genuine forced-failure executions compare the false identity 19/1620=4/405 and exit 1 through an explicit exception. An actual deleted cell also triggers the area-completeness exception in successful runs. No assertion statement is used. [CONTROL_RUNS.json](CONTROL_RUNS.json) pins the exact program, Python version, outputs and forced exceptions. [CONTROL.normal.json](CONTROL.normal.json) and [CONTROL.optimized.json](CONTROL.optimized.json) are the complete retained outputs.

These finite arithmetic controls supplement the universal proofs above. They are not formal proof certification, a substitute for source-model checking, or proof of every software behavior.

## 5. Priority, overlap, chronology and classical formulas

I freshly retrieved the actual [Ferudun reading-copy PDF](https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856), 182528 bytes, SHA256 edb268431856eef5d6eb00e730d1a27a7e91a15d76186b506168f259dbbb174c. I read its model/equality statements, gap lemma, iid expansion, three-point computation, Theorem 1.2 proof and progression-event/large-n proofs, including the displayed analytic page 8 visually. These provide an independently valid overlapping answer, with the same exact n3 fractions and empty-progression mechanism. Its results extend to additional dimensions and exponents. I do not certify its entire computer-assisted classification or verification suite.

The fresh [Zenodo record](https://zenodo.org/api/records/23372668) has created time 2026-10-14T14:58:42.560423+00:00, publication date 2026-10-14 and version 1.0. Its declared PDF size and MD5 match the freshly retrieved site PDF. The source paper is explicitly unrefereed; DOI assignment is not peer review.

Fresh [GitHub PR](https://api.github.com/repos/AlecKriebel/Math/pulls/1135), immutable commit and repository API reads confirm PR creation/last update 2026-10-10T11:34:20Z, one commit at e809a9c40f4ccdaced6f45f10b1dc8b7725a2119, author/committer dates 2026-10-10T11:33:05Z and current public repository status. I freshly retrieved all ten files at that exact immutable head; every byte matches the supplied inputs. The PR body still matches the stored snapshot and pins all ten distributed inputs. These are dated records, not proof of historical public visibility, first discovery, first publication, awareness or dependence.

The current note's abstract, related-work paragraph, bibliography, README, both metadata forms and generated provenance prominently credit Ferudun's same values and broader scope, distinguish the 10/14/17 October dates, and disclaim first priority. The historical input files retain their dated review claims under explicit edition/supersession caveats. There is no uncaveated present assertion that no overlapping answer exists.

For the supplemental Fourier route I freshly read [Su's author reprint](https://math.hmc.edu/su/wp-content/uploads/sites/10/2019/06/A-LeVeque-type.pdf), including the centered cumulative discrepancy definition and printed 450–451 Fourier identity, and [Anderson et al.'s AIF paper](https://aif.centre-mersenne.org/item/10.5802/aif.2298.pdf), including the exact kernel convention and complete printed 1383–1385 Lemma 2.1 proof. Their hashes match the cited versions. I visually inspected the actual formula/lemma pages. The centering constant affects only Fourier mode zero; Su's supremum bounds are not substituted for an L4 bound.

For the actual anchored F(x)=n^−1 sum 1[Tj<x]−x, direct indicator integration gives

∫ F(x) exp(−2πix) dx = (2πin)^−1 sum exp(−2πiTj).

This identity also handles endpoint representatives directly. Hölder bounds its modulus by ||F||4. For Tj={jZ+Delta}, the shift is a common unit phase, so its modulus cancels and the remaining kernel is exactly Dn(Z)=sum exp(2πijZ). Orthogonality counts a+b=c+d; multiplicities 1,2,…,n,…,2,1 give (2n³+n)/3. Therefore

E disc4⁴ ≥ (2n²+1)/(48π⁴n³).

The comparison to iid reduces to 60n²+30−48π⁴(3n−1)>0. With π<22/7, the coefficients after n=234+t are 5975502/2401, 33687216/2401 and 60, all positive. The elementary positive-integral identity for 22/7−π in the root note is correct. Thus n≥234 is a sufficient certificate, without transferring the central difficulty to an unsupported claim.

These earlier papers supply generic Fourier and kernel facts; the selected anchored coefficient, exact sampling-law application and iid comparison are supplied in this audit program. They do not by themselves document an earlier recorded resolution. The root Fourier note, current checker headers and current classification prose accurately distinguish the new application from an older target theorem; explicitly historical revision receipts legitimately retain superseded wording/hashes.

The three full priority reports and their source/version/access limitations were read. Their recorded counts agree with the ledgers: broad 52 queries/48 fetch rows/16 actual PDF rows, rotation 51 queries, classification 7 queries. These are overlapping and bounded activities, not distinct worldwide coverage. My four fresh targeted discovery queries returned Ferudun plus substantial irrelevant material; no new older target answer was identified, and no exhaustive conclusion follows. [QUERY_LEDGER.json](QUERY_LEDGER.json) records this narrow fresh search.

Actual unavailable/final-edition gaps remain as disclosed: among them Hinrichs/Weyhausen 2012, original Sugita/Takanobu and Sugita bodies, Janson, Cesaratto/Vallée, and several final-publication comparisons. I have not read those inaccessible bodies and do not certify their exclusion. No assertion of exhaustive novelty or eligibility beyond this bounded evidence is made.

## 6. Whole-package integrity, reproducibility, edition/privacy and PDF review

The complete reading scope includes main.tex, all ten original source-PR files, proof and verification narrative, root mathematical/Fourier/priority notes, all three mathematical and all three priority reports, all seven checker programs, runner, builder, README, license, generated provenance, both metadata forms and all six authored-review manifests. All authored manifest entries were read as structured inventory and independently hashed.

[START_PINS.json](START_PINS.json) pins 126 supplied files, including the six operative release files, PACKAGE_RECEIPT, all ten inputs, root notes/checkers and the six review sets. The main frozen release pins were:

| File under publication/ | Bytes | SHA256 |
|---|---:|---|
| main.tex | 11218 | 4e481ec84b1be42a9885df393e0fce065f489eea6f0f2e98ed0f84298f9e3d85 |
| output/pdf/random-lattice-counterexample.pdf | 63159 | a731f3d7db3ffb3644bf6ab3898159e00508a922ce2ec8dd4e6283cf994e6810 |
| output/random-lattice-counterexample-source-and-verification.zip | 278227 | d27bab6f38211df4b67084fc13dca85d770eb3b3f314c262646288fe74c81117 |
| output/zenodo-upload-kit.zip | 328995 | 1b43f1c812767d1cc9d2d7f242c4d120ba2ab9985e1da03855c1208dd6202c5a |
| zenodo-metadata.json | 4160 | 2c89b91b761f6b2ca0f2f1e7c653ab69bd141e08c10e76be61801fd8e0226957 |
| zenodo-deposit.json | 4491 | e815f916b925e670adb1233620a33df18a4caf64d046af69d8566268fb578d2a |

The source ZIP has 125 unique safe members, with 124 exact SOURCE_MANIFEST entries. Every member matches that manifest and PACKAGE_RECEIPT. The six review manifests authenticate 72 authored files in counts 11/22/7/14/9/9. Every review's input pins match its actual supplied edition, including the six classification pins. PR body and ten-file source manifest pins also match.

The kit has exactly five members; its PDF/source ZIP match the operative files, metadata is identical, and its flat deposit manifest correctly points to the flat files. The repository-relative deposit manifest correctly points to publication output paths. Author, ORCID, title, version/date, license and reference identifiers are consistent.

I safely extracted the ZIP only to ignored tmp/mirror and ran its standalone builder there. It completed all seven unchanged supplied programs in ordinary and optimized modes, exercising their implemented negative guards and comparing all mathematical result fields to expectations. The two parent historical wrapper results alone are unwrapped as documented. Source/input bytes are checked, and AST scanning forbids assertion statements. I reviewed the runner's argument handling and the builder's explicit member lists, pinned review manifests, safe paths, metadata equality and frozen PDF/source QA pins.

All six regenerated release files plus PACKAGE_RECEIPT, CONTROL_PLAN and REPLAY_RECEIPT are byte-for-byte identical to the frozen live inputs. No build or recompilation ran in live publication/. [BUILD_REPLAY.json](BUILD_REPLAY.json) and [INVENTORY_CHECK.json](INVENTORY_CHECK.json) record comparisons. Reproduction here used Python 3.14.6; code inspection supports the stated Python 3.10+ features, but I did not claim to execute every advertised interpreter/compression runtime.

All source JSON documents in the built mirror parse with unique keys and finite values. All Markdown local links in the extracted package resolve. The package contains only its own operative PDF and no third-party article PDF, raw HTML, images, source ZIP or private/tmp cache member. Retrieved bodies/APIs are not redistributed. Original authored CC BY 4.0 licensing and retained third-party rights are distinguished. Historical original/distributed proof hashes are expressly different editions; I authenticated the ten current immutable-head files, not the unavailable earlier private 7673-byte original. No hidden computational dependency is needed by the written proof. [CONSISTENCY_CHECK.json](CONSISTENCY_CHECK.json) contains the inventory, input, link, privacy and query-count checks.

Following the PDF skill, I rendered and visually read all four operative pages. The formulas, text, references, footer/page numbering and page transitions are legible; there is no clipped text, overlap, missing glyph or defective link rectangle. All ten PDF annotations were inspected; every internal named destination resolves. External targets are the correct OWR DOI, Ferudun DOI, source PR and specified ORCID. Fresh DOI-record/PR evidence supports their claimed identity; ORCID spelling/check digit match author metadata, without a claim to certify account ownership. The PDF metadata author/title agree. The frozen PDF was not recompiled. [PDF_QA.json](PDF_QA.json) retains page-render fingerprints and every link/destination.

Finally, [END_PINS.json](END_PINS.json) rehashes the same 126 observed files. All 17 required frozen files (six release assets, PACKAGE_RECEIPT and ten inputs), every shipped source/review pin, and 125 of the broader 126 observed paths remain unchanged. The sole change is the non-shipped ancillary root_reproduction/PORTABLE_PACKAGE_CHECK.json. Parent confirmed its separate private replay finished just after this review started and refreshed that receipt at 2026-10-17T21:27:47.165218+00:00. Both observed hashes are retained; this mutable receipt is outside the fixed archive allowlist and is not a candidate builder input. It is not a candidate finding. No operative candidate file was altered. [ARTIFACT_RECEIPT.json](ARTIFACT_RECEIPT.json) fingerprints this review's authored deliverables, excluding itself and ignored private/tmp files.

## 7. Disposition and limits

The strongest verified result is the exact minimal three-point negative answer, supported by a standalone inclusion proof, an independent all-n≥4 analytic tail proof, a newly authored exact full-integral computation including n4, and a valid supplemental Fourier proof. The independent original-model, boundary, normalization and chronology checks found no mathematical or substantive attribution repair.

P3-01 and P3-02 remain actionable in this frozen candidate; this review therefore must not count as a clean successive whole-package pass. Correct them globally in current authored support material, preserve clearly historical editions/receipts, regenerate consistent pins and packages, and review a newly frozen candidate.

This review is complete at 100% for its assigned scope. It is an AI-assisted adversarial review, not external human peer review, journal acceptance, proof-assistant certification, a new global priority clearance, or permission for a publication/deposit action.
