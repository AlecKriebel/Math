# PR200 publication package: independent whole-package adversarial review 01

## Verdict

**CLEAN for the sealed publication_package_v1: no substantive mathematical, attribution, chronology, reproducibility, layout, metadata, custody or file-safety blocker found.** This verdict applies only to the exact identities below. One optional P3 reference-title normalization is recorded; the existing reference uses the actual PDF title and is not a misidentification. Any changed package needs a new seal and the separately required new independent whole-package review.

This is a separately tasked AI adversarial check, not conventional independent human peer review or formal proof-assistant certification. It does not certify worldwide novelty, first disclosure or independent discovery.

Completion estimate: 100% of this bounded whole-package review, not of the parent's publication/integration program or historical-novelty research.

## Identity and custody

- Package seal SHA256: `0bbad9ab0d715f7e720183571986fa18e27d9c5c1133726cc8b806c5f571fec5`.
- PDF: 78,822 bytes, SHA256 `9acd1ba50eeab99ca8749a56b1732d3a26ad9b7a7969e772bae06efbea07c260`.
- TeX: 16,498 bytes, SHA256 `bd41f79208694d0a01dfae80929b30600e8bc8f6b1c77405ea59cb0146499ca0`.
- ZIP: 79,863 bytes, SHA256 `72f9efa71f9bd67677ce97cea3c54a754bd3e53f759e9f9ed1319f4aab901086`.

`audit_package.py` made 92 explicit checks and was rerun after the review to confirm that the package remained unchanged. The seal covers exactly 29 files excluding itself; the ZIP has exactly 25 unique regular-file entries and 220,423 uncompressed bytes. Every member decompresses and passes CRC, every member equals its materials counterpart, every bytes/hash record agrees with the outer seal, and the self-excluding inner manifest covers every other member. ZIP Unix modes are all regular `100644`; there are no symlinks, absolute paths, traversal components, backslashes, control characters or encrypted members. No filesystem symlinks occur in the package. No dependency software, third-party full text, raw API response, credential or unintended binary was found in the payload.

All thirteen SOURCE_ORIGINS entries match both their declared bytes/hashes and the available repository source bytes. The historical original proof additionally matches the raw public file at the exact submitted commit URL, checked without a Git/index/ref operation; see ORIGINAL_SOURCE_CHECK.json. Hashes establish identity, not truth.

## Independence and chronology of this review

FREEZE.md was created at filesystem UTC 2026-10-16T05:02:13.708411 before reading the manuscript, code or favorable reports. DERIVATION.md was created at 05:03:32.781630 after reading the manuscript/contract/code/metadata and direct Stachel/Ferudun sources, but before the supplied supporting derivation, historical proof, editorial decision and priority reports. Its universal reasoning was preserved before those later reads.

The manually entered display times in those two files were rough estimates lying ahead of their actual creation; their original bytes are preserved. TIMESTAMP_RECEIPT.json records the corrected creation witnesses and hashes, and LOG.md explicitly records this correction. The ordered tool transcript, rather than an invented precise per-operation timestamp, documents the reading sequence. This reviewer makes no public-disclosure claim from local filesystem times.

## Universal mathematics: independent attempts to falsify the claim

The exact hypothesis is essential: a>b>0; a proper nested confocal *elliptical* caustic with positive axes and 0<lambda<b²; least period N>=3; ordinary positive lengths to either original common focus; consecutive *boundary* tangents; phase varying for the fixed pair/winding. Circles, hyperbolic or collapsed caustics, separatrices and N=2 remain outside the classification. Repetitions do not create a new primitive period.

The complete independent argument is in DERIVATION.md. It establishes the following, with no unresolved mathematical gap found:

1. **Published-input scope.** Direct reading of Stachel's published Theorem 4.3/(4.9) confirms modulus c/alpha, P(u)=(-a sn u,b cn u), the v half-step, boundary axes alpha dn(v)/cn(v), beta/cn(v), arbitrary initial phase and every coprime turning number. The source's earlier dn real-shift sign discrepancy is real, but is not an input used by the proof. DLMF gives the correct period. The theorem neither silently changes the modulus to mpmath's parameter nor restricts stars to winding one.
2. **Actual tangent geometry.** Substitution into both tangent equations gives Q=(-a dn(v) sn(u)/cn(v),b cn(u)/cn(v)). The original determinant has nonzero real magnitude 2 sn(v) cn(v) dn(u)/(ab[1-k²sn²u sn²v]). Its normalized ellipse equation exceeds one by sn²(v)dn²(u)/cn²(v)>0. Thus outer vertices are finite, outside E, and separated from both foci. The caustic chord equation checks the half-step independently. The polar locus has axes a²/alpha,b²/beta; its own foci are not substituted.
3. **Full factorization before imposing parity.** Directly multiplying the two algebraic squared focal distances gives H=alpha⁴/q⁴(1-k²S)(U²-k²V²S), with q=1-sn²v and S=sn²u. Double-angle identities give H=Cv dn²u[dn²delta-k²cn²delta sn²u], Cv>0. The one-focus real factors are positive; no square-root branch is hidden.
4. **Actual lattice, multiplicities and degree.** The squared functions are meromorphic on C/(2K Z+2iK' Z), though dn itself changes sign under 2iK'. At p=iK', sn² and dn² have a double pole and dn² has a double zero at p+K. When delta is not K, the other bracket has distinct zeros p+K±delta. Its degree-two pole divisor proves both zeros simple; neither can collide with p or p+K. The full divisor is therefore 2[p+K]+[p+K+delta]+[p+K-delta]-4[p]. The only degree drop in the admitted real range is delta=K, forcing primitive N=4,tau=1, where the divisor becomes 2[p+K]-2[p]. There is no omitted exceptional modulus in 0<k<1.
5. **All primitive windings and necessity.** The translation has exact order L=N/gcd(N,2). Summing the full divisor gives 4O_(p+K)-4O_p, or coefficient two at N4. The cosets coincide iff the real subgroup contains K, iff L is even, iff 4 divides N; otherwise they are disjoint. This accounts for multiplicities and collisions among factors rather than assuming disjoint individual divisors. It depends on the subgroup, not a chosen coprime generator.
6. **Odd periods and the real family.** For every N, the separate phase shift gives Rminus(u)=Rplus(u+2K), while Rplus²Rminus²=F^(N/L). Constancy of either real product forces both constant. Since the meromorphic F^(N/L) has no real poles, the identity theorem then contradicts its nonzero divisor for odd N or N=2 mod4. The proof does not put antipodal points inside an odd orbit.
7. **Sufficiency and ordinary positive lengths.** For 4|N, antipodal points do belong to the same orbit; pairing yields Rplus=Rminus and Rplus²=F. Compactness makes F constant after its poles cancel, and real positivity gives the unique ordinary square root. Repetition is a positive integer power and cannot restore constancy. The circle boundary case is separately constant for all admitted periods and confirms that noncircularity matters.

The exact primitive-six example, its caustic and both products agree with the physical reflection/tangency certificates. No numerical test is used as the universal proof.

## Independent computations and software challenge

Allowed runtime only: Python 3.14 with `-E -S -B -P`, SymPy 1.14.0 and mpmath 1.3.0 from the permitted sibling standard-software directory. No authored sibling mathematics was imported. All new output stayed in this review directory.

- `independent_checks.py`: independent integer-residue divisor bookkeeping for **10,101** primitive `(N,tau)` with 3<=N<=257; a physical-variable symbolic factorization and degree-drop check; **60** direct tangent/physical-reflection families at k=0.0001,0.81,0.9999 including high coprime windings and N up to 36; **18** actual complex divisor configurations, including N4 and simple/double zeros and order-four/order-two poles. All **38,886** explicit checks passed. Maximum relative tangent residual was about 2.05e-118; maximum reflection residual about 7.54e-119 at 120 decimal digits. Nearly circular unresolved sampled variation is explicitly permitted and labeled; it is not falsely treated as constancy or proof.
- Both portable checkers ran fully in normal and optimized `-O` modes. All four outputs matched the expected JSON **byte-for-byte**, not just the PASS flag. The exact certificate has 306 checks; the parity certificate has 1,521 rational divisor cases and 117 numerical families. The exact expected SHA256 is `a1275032fd6235e806343b3e9e91ef958f3a16558155fc76285aef12a8d9180f`; parity expected SHA256 is `347f7128c0b04f808ef6852c9b248574d2fd880d84d6abcd1f384bd7711345f8`.
- All four built-in deliberate-failure runs exited nonzero with their specified explicit exception.
- Extra in-memory mutation tests changed an actual substantive algebraic identity from equality to zero to equality to one. Both actual mathematical guards rejected it, in both normal and optimized modes, without writing a success certificate. Package source was never modified. The first parity selector was ambiguous because the expression also appeared in its diagnostic; the harness refused that selector, it was tightened, and all four final mutation tests passed. See MUTATION_CHECKS.json.

This rules out the specific assertion-elision defect in the portable code. It does not certify every possible dependency/platform version or provide interval arithmetic. Legacy assertion limitations are accurately disclosed and are not confused with these explicit guards.

## Whole payload and publication text

Every payload text was read in full after independent derivation, and every numeric expected field was reproduced exactly. All 25 ZIP entries were covered:

| Payload group | Review |
|---|---|
| README, THEOREM_CONTRACT, current TeX, metadata | Current iff statement, exact scope, positive lengths, primitive stars, circle exception and repeat rule agree. AI/unrefereed/novelty limits are consistent. |
| Both verification scripts, requirements and root replay receipt | Code and pinned dependencies agree with instructions; fresh complete replays and false-guard challenges confirm the receipt. |
| Both expected JSON files | Full normal and optimized generated outputs are byte-identical. Finite tests are expressly diagnostic. |
| PARITY_DERIVATION and ORIGINAL_POSITIVE_PROOF | Current extension agrees with the manuscript. Original proof is historically labeled and does not claim the October16 converse was in October1 submission. Original bytes authenticated directly at the submitted commit. |
| exact_history report/source/query ledger | Exact competing positive theorem is prominently and accurately recognized, with full scope and close mechanism overlap. Negative searches and chronology are qualified. |
| general_theorems report/search ledger | Theta/norm background is credited; incomplete metric dictionaries are expressly blocked instead of promoted into proofs. |
| classical report/source/query/implication ledger | Older alternating focal ratios and polarity are distinguished from full phase-product constancy; unavailable/OCR-only leads are disclosed. No global absence claim. |
| editorial decision and observed chronology | Explicitly historical preparation checkpoints. README explains why old publication_ready=false fields do not represent a current package contradiction. Unaltered local path references are identified as original-environment records. |
| SOURCE_ORIGINS and MANIFEST | Exact source and payload identities independently verified. |

Top-level TeX and materials TeX are identical; deposit metadata equals materials metadata and the seal's exact metadata. The requested upload list is exactly PDF, TeX and ZIP, in the intended order. CC BY 4.0 applies to authored content and does not claim third-party ownership. No current text claims firstness, historically established novelty, independence of discovery, human peer review, or formal machine proof.

## Primary-source and time checks

- Direct Stachel published PDF: Theorem 4.3/(4.9) checked, together with the preceding dn-shift discrepancy. This is the decisive dynamics input, not inferred from an audit verdict.
- Direct Ferudun PDF: full positive theorem and its one-focus factors/quarter-period and cyclic-divisor proof checked. It includes every coprime star winding, original foci, strict confocal setting, repetitions and an explicit constant. The manuscript's close-overlap attribution is warranted. DOI [10.5281/zenodo.23093258](https://doi.org/10.5281/zenodo.23093258).
- Both actual k115 source rows were extracted and visually checked: arXiv v11 Table2 p5 and distinct journal Table2 p345. The outer polygon definition was checked on the v11 first page. Both rows have the four-divisibility condition and dated proof question marks; neither establishes current openness. [arXiv v11 record](https://arxiv.org/abs/2004.12497v11).
- DLMF [22.4](https://dlmf.nist.gov/22.4), [22.6](https://dlmf.nist.gov/22.6), [22.8](https://dlmf.nist.gov/22.8) checked directly online for periods, shifts, elementary and addition identities.
- Fouché's printed p149 §4 and Anonymous 1853 printed p219 §2 were independently inspected in the primary scans. They support the claimed polarity background and alternating-ratio distinction. [Fouché](https://www.numdam.org/item/BSMF_1915__43__146_1/); [Anonymous](https://www.numdam.org/item/NAM_1853_1_12__218_1/).

Small anonymous direct API reads independently confirmed GitHub PR creation `2026-10-01T05:03:51Z`, Zenodo record creation `2026-10-02T01:41:04.506303+00:00`, and DataCite registration `2026-10-02T01:41:05.000Z`. Current PR head is the submitted hash; the raw historical proof at that hash matches the payload. See TIME_SOURCES.json and ORIGINAL_SOURCE_CHECK.json. Public creation records do not exclude earlier website/repository disclosure or prove when either author developed a proof. The package correctly states these limits and dates the converse to October16. Browser API retrieval failed, but direct small JSON reads succeeded; no large network download or external communication was used.

I did not repeat an exhaustive worldwide bibliography search, independently authenticate every nondeterminative old source in every historical ledger, or establish worldwide novelty. Those are not claims of this package; its remaining historical uncertainty is explicit.

## PDF and presentation

All six finished page images were inspected. The proof, formulas, equation references and attribution are legible, margins are clear, and no clipped/overlapping content, missing glyph, broken table or unresolved reference was observed. The PDF has six letter-size pages, embedded fonts, no form, no JavaScript, no encryption and no embedded files. The rendered note agrees with the current TeX in the theorem, proof, exact example and qualifications.

## Optional P3 bibliographic normalization

The current bibliography's arXiv reference title is **Eighty New Invariants in the Elliptic Billiard**, exactly the title printed on the retained v11 PDF. The registered arXiv abstract record instead uses **Eighty New Invariants of N-Periodics in the Elliptic Billiard**. This is a real version-title variation, not an incorrect paper or lost attribution. Using the registered title consistently would ease lookup; retaining the printed PDF title is defensible. Parent has elected normalization. If changed, regenerate both TeX copies, PDF, ZIP/manifest and seal, then submit the entire new package to the required new independent reviewer. No substantive theorem or priority correction is needed on the evidence found here.

## Artifact and action limits

Safe authored outputs are explicitly indexed in SAFE_MANIFEST.json. Third-party primary extracts and page images are private readings and excluded. No package file, Git/index/ref, PR, release, publication, unrelated editor or external message was changed. This review leaves the parent responsible for any separately authorized repair, new reviewer, publication and integration.
