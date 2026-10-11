# First fresh adversarial preprint/package review: PR311 / problem30005303

## Decision and scope

**Review complete; package corrections required before the next full adversary. No mathematical defect found in the main theorem, source reduction, supplementary facial-support lemma, or attributed counterexamples. This review does not clear immutable publication.** The user-required second NEW full adversary must read the globally repaired package and PDF in full.

I personally adjudicated the complete released manuscript, supplement, executable code, documentation, and five-page PDF. Fresh portable reproduction passed, independent expected-output comparisons passed, and additional independent/negative/mutated controls passed in the stated finite scopes. Three actionable corrections are listed below. None changes the mathematical theorem on the evidence inspected.

The source-only gate was frozen before package access: SOURCE_ONLY_CRITERIA.md SHA256 9e11b10ce198985a65a3f0a612a66e76f9447df144e74ed51da8d12556e0a046; FIRST_INDEPENDENT_CONCLUSION.md SHA256 3d3ff048076968b5fc9ae06ffe0d6636db102156e51f8500b085283b34110f67; SOURCE_ONLY_FREEZE_MANIFEST.json SHA256 fe8d9a79dbb2396d3ca7a750568f927ac836fce1eeae0e351d5c0152d881ce27. Actual source-only seal UTC was 2026-10-04T17:41:21.042460+00:00; all three were measured 0444. The named root release receipt records 2026-10-04T17:49:21.656356+00:00. No unreleased candidate or root/sibling/inherited report was read.

Completion estimate: 100% of this FIRST full review after final sealing and verification. This is distinct from completion of publication or certification of historical priority.

## Actionable findings

### R1 — Clarify the native build receipt's hash referent (P2, provenance)

BUILD_RECEIPT.json, native_jobs entries, repeats program_sha256=85020339f2a629d3aafb62f63699c4e9c17be2997e910aaeb6630886663a5d03 for tectonic, pdfinfo, pdftotext, and pdftoppm. These are distinct executable paths. My actual measurement on the review host at 2026-10-04T17:53:53.057822+00:00 gives:

| Path | Current bytes | Current SHA256 |
| --- | ---: | --- |
| /opt/homebrew/bin/tectonic | 16427072 | 38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95 |
| /opt/homebrew/bin/pdfinfo | 113048 | 8a48bb18e99c8f1add637ffae1d860c3cdabe11f4f1672f3c1b5ef4c3e6e8461 |
| /opt/homebrew/bin/pdftotext | 110856 | 52cb759b328134d667e0e9ba9142e952811473fba6caa3a053ff1e2605512fd9 |
| /opt/homebrew/bin/pdftoppm | 75488 | 504dd5b6efe73d7d23bc04c90d2cfd75962b8893df95de6db7f45ab54bf47fc1 |

The current pins do **not** establish historical native executable pins. The released receipt does not explain a common capture-driver referent, and the original native script/streams were not released to me. Therefore the historical program provenance is unverified as labeled, rather than a proof that four particular old binaries had today's hashes.

Required repair: inspect authentic prior build evidence, identify exactly what was hashed, and rename the field if it is the capture driver. Add separately measured historical executable fingerprints only if they genuinely exist. Otherwise state that those historical executable fingerprints were not captured. Preserve the old receipt/freeze. Do not substitute today's measurements as past measurements.

### R2 — Replace “unique” with ordered evaluations, or implement actual deduplication (P2, quantitative scope)

verify_priority_examples.py lines 63–68 increments determinant_count for every minor in every **ordered** A/B separation and performs no deduplication. Its result key at line 82 is unique_conditioning_2x2_minors_checked. SUPPLEMENT.md line 33 calls 6384 C6 checks “unique conditioning minors.”

I independently constructed each formal minor as a polynomial in the FULL joint-cell variables, marginalized leftover coordinates, collected equal monomials, and canonicalized its sign. The results are:

| Law/graph | Ordered separations | Ordered minor evaluations | Distinct formal minor polynomials up to sign |
| --- | ---: | ---: | ---: |
| Each supplied C4 law | 4 | 16 | 8 |
| Supplied C6 law | 252 | 6384 | 1176 |

Even without the more extensive canonical calculation, exchanging A and B necessarily evaluates a transposed copy of the same minor. Thus 6384 is an evaluation count, not a distinct-polynomial count. All evaluated minors vanish for the supplied laws; the reporting correction does not weaken their verified Markov status.

Required repair: preferably rename the field to ordered_conditioning_2x2_minors_checked and describe 6384 ordered evaluations in the supplement. If distinctness is to be claimed, define its equivalence convention and actually deduplicate. Regenerate expected outputs and rerun reproduction after any key change. The canonical count above is documented in independent_checks.py and INDEPENDENT_CHECK_RESULTS.json; a second reviewer should independently verify any unique count promoted into the package.

### R3 — Fix the direct-script usage filename (P3, usability)

verify_priority_examples.py line 4 advertises “python3 verify_laws.py --output new_results.json”, but verify_laws.py is not among the twelve packaged files. The README's top-level REPRODUCE.py command works.

Required small repair: make the docstring name verify_priority_examples.py. This is a direct-use documentation defect, not a failure of the portable top-level runner.

### Optional editorial suggestions, not material defects

The manuscript's reference to an “audited problem packet” and the supplement/code's internal “candidate” terminology can be made self-contained by referring directly to the included C4/C6 tables. The tables and comparisons are already checkable without that packet. Pin the arXiv link explicitly to v1 when citing that version. Picard–Queyranne's scanned cover uses EP-79-R-15, whereas the institutional repository catalogs EP-R-79-15; distinguishing the cover and catalog labels is optional because the linked source is unambiguous.

## Personal mathematical adjudication

### Definitions and literal source reduction

The independently downloaded Lauritzen report matches 600619 bytes and SHA256 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65. I personally visually read his entire contribution, printed 3125–3127, before the gate. His binary sample space, fixed finite simple graph, original-edge real factors, global Markov separation, whole-lattice MTP2 inequality, and zero semantics agree with the manuscript's source comparison.

A product of real factors representing a nonnegative density can be absolutized cell by cell without changing its product. The unary/edge theorem is an explicitly larger convention than the source's edge-only formula. The corollary correctly reduces back: when an edge exists, original-edge products are independent uniform in isolated bits; the nonisolated marginal remains a normalized edge-factor MTP2 law; unary factors can be absorbed into incident original edges, and the uniform-isolate scalar into any original edge. The source's nonempty edgeless literal model is empty because the empty product is unnormalized 1 on 2^|V| cells. The empty-vertex law is 1. The manuscript states the alternative tacit-normalizer convention separately.

Global Markov at zeros is justified by separator conditioning of positive mass, or equivalently the marginal polynomial equations. Null conditioning fibers require no division. The finite probability simplex, MTP2 inequalities, and all global Markov equations are closed. There is no appeal to positive-density equivalence to evade the boundary.

### Density/aggregate coupling bridge

For a finite local product, intersection of its ACTUAL unary and edge projection cylinders equals its positive support: every projected cell that occurs in the support has a positive local factor entry. This works with arbitrary supplied gauges and zeros.

Meet/join closure supplies both 00 and 11 on every active edge. Its allowed edge projection is therefore a square, an implication, or equality. Pins and original-edge implication constraints give the entire support. Strongly connected implication classes encode deterministic equalities; their quotient is a poset with support states its upsets. No unsupported all-pair graph replacement is used.

Finite local logarithms are taken only on positive factor cells. Extending missing cells arbitrarily gives an ordinary quadratic polynomial. After pin substitution and equality contraction, within-class and comparable-class pair terms are unary; incomparable-class coefficients are sums across the relevant ORIGINAL cross edges.

For two incomparable classes K,L, the union of their strict successors is an upset excluding K,L. The four states obtained by adding neither/either/both differ in exactly those two classes. Their log MTP2 second difference cancels every other term and equals B_KL. Thus the aggregate, rather than each originally supplied coefficient, is nonnegative. This resolves cancellation and negative supplied-potential traps at zeros.

Each aggregate is placed on an existing original cross edge; each field is placed on a representative coordinate. The lifted L agrees with log p minus a finite constant on the whole support. D counts pins and original-edge implications, is zero exactly on that support, and is at least 1 outside. Every implication penalty contributes a nonnegative quadratic coefficient to L−tD. Consequently each finite penalized law is positive and attractive on the unchanged graph. The normalizer tends to the positive support sum e^(−c), so the exact normalized limit is p. All-pinned, isolated, disconnected, and empty cases survive. I found no circular or unsupported bridge.

### Residual flow, original locality, and normalization

The oriented decomposition −J x_i x_j=J x_i(1−x_j)−J x_i uses nonnegative J. Terminal arcs encode each unary sign. Cut cost equals energy plus a scalar, with one vertex per original variable and two terminals only.

For any capacity-feasible maximum flow, r_uv=c_uv−f_uv+f_vu is nonnegative. Summing over a source–sink cut and using conservation gives residual cut cost C(U)−v. Max-flow/min-cut makes this E(x)−min E. Real finite capacities are allowed; compactness of the flow polytope supplies a maximum and standard max-flow/min-cut does not require integrality.

Nonterminal reverse residual arcs stay on ORIGINAL undirected edges. Terminal arcs are unary; arcs into the source or out of the sink do not contribute to such cuts. Exponentiating negative local residual costs bounds every factor entry in (0,1]. Their product W has maximum 1 and a normalizer in [1,2^|V|]. Along a subsequence, all finitely many entries converge in [0,1]. Product continuity and finite sums preserve Z_*≥1, so the normalized product is the given probability limit. No mass is lost, and no unbounded normalizing multiplier is silently absorbed. The empty case and unary scalar absorption are explicit.

Together the two lemmas prove equality with the closure of the positive attractive family, and hence closedness. The finite checks illustrate this argument; they are not its proof.

### Supplementary facial-support lemma

GMS's facial witness yields a finite original-edge energy H that is zero exactly on S and nonnegative everywhere. Submodularity is unnecessary. The meet/join support reduction to pins, tied classes, and a quotient poset is valid.

Two ideals differing exactly in one tied class give the class-connectedness argument. If that class split into sets with no original edge between them, fixed-exterior pairwise additivity and H≥0 force mixed assignments also to have zero energy, contradicting the tie.

For a quotient cover C<D, the displayed I is a downset: any obstruction would yield an intermediate class. Three permitted patterns 00,10,11 and forbidden 01 have the same exterior. Without an original cross edge the energy must be additive, forcing H(01)=0, a contradiction. Connected tied classes and original edges for every quotient cover enforce all equalities/order constraints. Original-edge projections enforce nonisolated pins, while a purely edge energy cannot constrain an isolate. Thus facial lattice support is feasible on the original edge design.

Continuity gives the toric equations for a limit of original-edge products. GMS Lemma A.2 gives faciality, MTP2 gives the lattice, the new lemma gives feasibility, and GMS Theorem 3.1 then gives finite original-edge factors. This is a valid second derivation of the closure consequence. I found no transferred unsupported central claim. My negative path example shows that the facial assumption cannot simply be dropped.

### Counterexamples and their attribution

The Gandolfi–Lenarda C4 law is exactly their published Lemma 5.2 table: x3=x4 support, weight 2 at 1111 and 1 at the other seven supported states, normalizer 9. Its lattice support and MTP2 are direct: an incomparable supported pair has both right-hand weights 1, and its meet/join weights are at least 1; off-support right sides vanish. The relevant conditioning fixes one side of each C4 separation. Independent global Markov polynomial enumeration agrees.

Each original edge's cell multiset balances in the manuscript's quartic, but its products are 1/9^4 and 2/9^4. The identity has no division and covers zeros and signed factors. On C4 every complete-subset factor is an edge, unary, or constant factor; the latter factors can be absorbed into incident edges. Thus it also refutes the two separate clique-factorization conjectures. It is not a counterexample to the closure theorem, because it violates an invariant satisfied by edge-factor limits.

The rotation preserves the C4 graph and matches every cell. The C6 lift has the claimed eight core states and independently passes all global Markov/MTP2 checks while failing its balanced quartic. The package makes no new-counterexample claim. KS Example 6.5 has the same equality-support obstruction. Its overlapping numerical sentence is accurately noted in the supplement; the corrected normalized 7:1 bottom/other table is verified directly, without pretending the literal sentence is well formed.

## Independent acquisition and citation review

All third-party PDFs, complete extracts, source images, search outputs, metadata, and raw command streams are inside private/, excluded by this review directory's private/ ignore rule. They must remain private. No copyrighted full source is inserted into the public package or this report.

Personally checked source scopes (PDF page numbering, not journal numbering):

| Source | Independent acquisition and personally inspected scope | SHA256 | Bytes |
| --- | --- | --- | ---: |
| Lauritzen | EMS original; entire contribution visually, PDF 5–7 | 56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65 | 600619 |
| GMS | arXiv math/0608054; Theorems 3.1–3.2, Appendix A.6/Lemma A.2 at 8–9,29–30; Examples 7–8 at 19–20; page 29 also visual | 06645785a2e2dcdc379673526dcf20654656437ca4cbc9cf57a61216149b3784 | 361663 |
| LUZ | arXiv 1905.00516 (current v3); Section 4.4/Lemma 4.9 and continuation at 18–19 | a74bc9a89f27008963a48e5750d44499e6f2bb2cdcb1cd2f41f8dce3d8a317c9 | 581115 |
| Fallat et al. | arXiv 1510.01290; Theorem 7.5 and positive-potential cancellation at 23–24 | f23ef1ec315f931f9af8bc270096efa5c09081e901b2224ff75e5f9004596b3f | 346936 |
| KS v1 | arXiv 2411.03139v1; Definition 2.4, Proposition 4.1, Lemma 5.4, Theorem 5.5, Example 6.5; relevant pages 3,5,7,13, plus contextual 9–10; 7 and 13 also visual | 45382694fde65d1c97399faac0d8d15a6049af198a6b4a16cc4fa228b11a3b6d | 240727 |
| GL | MSP print PDF; full Lemma 5.2 table/argument at 11–13; 11–12 also visual; contextual 14–15 | 77287aa615ac5291b927a91c3a7622b362ddf747cf529f7d3e1be74b237282d1 | 947061 |
| KZ | Oxford-hosted author paper; Theorem 4.1 and original-vertex quadratic construction at 4–5, also visual | c84942529525161e7c69eb5555792b64a759c16d6b8737cdbfef427db5c73884 | 470344 |
| PQ | institutional original report; March 1979 cover and minimum-cut/flow result, PDF 4–10 visually | 7cf4782459b58d5f43c41a1fd0fee2233c8fb013503ef436e4f082969a48d058 | 8310810 |
| KR | Microsoft-hosted author manuscript; submodular cut construction/reparameterization at 6–8; 7–8 also visual | 447685d9ff5acf753829bfd0db4c3654e70be12d59841f3bf9d3864fccb18096 | 245472 |

These are targeted cited-result reads, not claims of full reads of every third-party article. Source acquisition URLs and real argv are in private command captures. Final measured modes are in FINAL_SEAL_MANIFEST.json.

The GMS support-feasibility/toric-closure distinction, LUZ all-pair support reconstruction/extended-family compactness, and Fallat strictly-positive-potential theorem match the cited scopes. KS naturality excludes pins and repeated equal coordinates; its natural-support clique theorem is not literally the general edge statement. The supplement supplies the necessary original-edge connectivity and lifting steps and correctly labels this as an extension. KZ/PQ/KR support the classical cut/flow attribution. MSP's official metadata confirms the GL nominal-2016 volume and publication on April 13, 2017. Crossref, arXiv journal metadata, the IMS journal body, and Springer metadata support bibliography fields; retrieval failures/429 responses are retained.

Lauritzen's report is nominally 2022 and was published in 2023; the manuscript's report-year citation is conventional. No cited theorem is mistaken for full historical first priority. Bounded searches for related closure/Ising claims added no basis for a novelty certificate. The package's qualified comparison is acceptable within the inspected scopes. Historical “candidate_code_read=False” and prior independent-authoring metadata were not reconstructed from unreleased audit records; the root must authenticate such history if retained as an assertion. My newly written cross-check is independently authored in this review.

## Code, reproduction, and additional falsification evidence

A byte-identical copy of exactly the twelve named inputs was made at private/fresh_external_copy, distinct from the package directory. REPRODUCE.py was run there with the bundled Python 3.12.14, standard library only, assertions enabled, and a NEW external-to-package result directory private/fresh_external_results. The runner exited 0; both child jobs exited 0 with empty stderr. Actual argv/cwd/timestamps/source fingerprints and complete streams are retained. No original input changed.

I independently compared boundary JSON values and priority output bytes against expected inputs, outside the runner's own assertions. The priority bytes match SHA256 2f70112c513b0f9098b1c2813a465c0c1f939bb09c037a892dfd0ad7656a0357. I independently evaluated whole-lattice MTP2, graph separation by transitive closure, all marginal global-Markov equations (including leftover-coordinate marginalization and null fibers), exact normalization/invariant products, every expected edge balance, and all 16 coordinate-flip controls. C6 has 9408 directly checked global-Markov marginal equations in my alternative implementation. The expected separation arrays were fully decoded and compared against independent enumeration; I do not claim a manual line-by-line reading of all 65252 JSON bytes.

The supplied residual controls comprise 380 networks on all 76 labeled graphs of orders 0–4, with 5495 cuts and five deterministic integer samples per graph. I independently verified count arithmetic. They do not exhaust all parameters.

Further independent exact controls:
- 210 networks with rational capacities/fields and arbitrary edge orientation, on orders 0–6, checked on 3810 assignments: cut energy, conservation residual identity, max-flow/min-cut value, local exponent equality, minimum shift, and original-edge locality.
- 1420 sampled original-edge pairwise energies on all nonempty graphs of orders 2–4; 1336 minimizer supports were lattices, and every one equaled its original-edge projection-cylinder intersection.
- Negative laws: disconnected equality violates global Markov despite MTP2; a missing join violates whole-lattice MTP2; naive positive smoothing violates MTP2. Empty-vertex and arbitrary independent-isolate laws were also checked.
- Five additional independently selected density inputs tested two tied blocks with opposing individual cross coefficients, a diamond implication poset with an incomparable aggregate, pins/disconnected components/nonuniform isolate, a negative-comparable chain, and tied coordinates plus an isolate. These invoke the released density function and pass exact reconstruction, MTP2, and decreasing L1 checks.
- A uniform path support x0=x2 is a lattice but has four states versus eight allowed by its edge projections, showing why faciality cannot be omitted.

Four damaged-code mutants were caught: missing reverse-residual update; overwriting rather than summing aggregate coupling; wrong minimum-energy normalization shift; and an always-true MTP2 checker. Three runner negatives were caught: altered expected output, optimized assertions, and a preexisting output directory. Failures have actual exit 1 and full captured tracebacks/messages.

These are bounded controls, not an all-graph proof, formal certification, or novelty evidence. Test artifacts are INDEPENDENT_CHECK_RESULTS.json, MUTANT_AND_DENSITY_RESULTS.json, and ARTIFACT_COMPARISON_RESULTS.json, with their checkable scripts and captures.

## PDF, disclosure, and usability

All five PDF pages were newly rendered at 145 dpi and personally visually read completely. The title, author/ORCID, abstract, theorem, proofs, literal-source corollary, counterexample, disclosure, equations, page breaks, and all nine bibliography entries are legible. I found no clipping, overlapping text, missing glyphs, unresolved references, or missing pages. The extracted ten external links are the supplied ORCID and nine bibliography URLs, and the PDF carries the expected five-page/76891-byte fingerprint. Ordinary proof continuations across pages and the mostly-bibliography final page are acceptable.

The AI/unrefereed disclosure is clear and distinguishes AI adversarial review, exact finite computation, human peer review, and formal proof-assistant certification. The public recipe needs no checkout, credentials, network, absolute workspace path, or private source. The native receipt describes a historical build rather than a runtime dependency. License/author metadata are present. Aside from R1–R3 and optional wording, submission material is usable as a research note.

## Exact released input provenance and read scope

All inputs were independently measured at 2026-10-04T17:50:01.742661+00:00 and reauthenticated unchanged at 2026-10-04T18:08:06.933733+00:00. Every input has actual mode **0444**. Paths below are relative to the named preprint_package_v01 directory, not a permission to inspect any other files.

| Input | Bytes | SHA256 | Actual read scope |
| --- | ---: | --- | --- |
| BUILD_RECEIPT.json | 5614 | 9059298c2441f87261908a3916d352024a0154e502a87d65a40a0155649ce7f3 | Complete JSON personally read; unreleased native streams not accessed |
| LICENSE.txt | 506 | b7b167e6c727fcc23238fcea09cad50940552764aa2fdd8ec7d9343b4b662016 | Complete text personally read |
| MANIFEST.json | 1458 | 9f4548310b58d667279ae8964cea55eeb79c4ddb9f44ee32fb2435bbf3468228 | Complete JSON read; every payload hash/size independently checked |
| README.md | 3276 | 5b04125c456a631c36bc5b934dbeb87ecfffe928a3d4091405f8c9ac7fa6fccc | Complete text personally read |
| REPRODUCE.py | 2061 | 915f0b449fc383c43b5cdbe7a08675542684d1ecd558f416c2c9f2c861049c4b | Complete code personally read, fresh execution and negatives |
| SUPPLEMENT.md | 7482 | 7fda84e32d9e430093c87517e40c52ef8ec91655ff26651b54b2029828971171 | Complete text personally read and all arguments adjudicated |
| expected/boundary.json | 1911 | 1705ca835467d74eee28194473adbc50702b1cb37685f170171a841c9412f3b1 | Complete JSON read and independently compared |
| expected/priority_laws.json | 65252 | 2f70112c513b0f9098b1c2813a465c0c1f939bb09c037a892dfd0ad7656a0357 | Full byte/JSON read; all law tables and meaningful fields examined; arrays mechanically independently checked |
| mtp2_edge_closure.tex | 15589 | e10a6be7d61e61a03dd231b6df39e81888ea728a3f17aa8b61c19b6a22b6ec23 | Complete source personally read |
| output/pdf/mtp2_edge_closure.pdf | 76891 | c64228c64ce3ed187e2a58335926dbf29abe45b4468c24d1c457980bcd941ad3 | All five pages personally visually read |
| verify_boundary.py | 7745 | 83cea2fa1f1887ca1034dc25b5b836e59b0adb29bb67a6784e5c47bb5d55ed57 | Complete code personally read and tested |
| verify_priority_examples.py | 8594 | 6037980fa4a92fb969601619cb0a57b4350dfa97e46da1513ef59792c8a28934 | Complete code personally read, with tail reread after display truncation |

## Audit failures and remaining boundary

The initial bootstrap failed on Python 3.9's absent sys.orig_argv before its own timestamp record. The requested argv, returned stderr/stdout, and exit 1 are preserved; unavailable early start/end times are explicitly null. A wrong assumed rg binary path failed before child process launch; the complete returned traceback and requested argv are preserved separately, with no invented initial time. The retry used the actually available binary through /usr/bin/env. An indentation mistake in my mutant-driver attempt failed before copying its expected input; the original driver and partial directory are preserved, and a corrected NEW directory run passed. Several Crossref lookups returned 429, and some web DOI/XHTML openings failed; these failures remain recorded and successful alternative primary retrievals are identified.

Finished review files are sealed by SHA256/size and measured 0444 mode in the final manifest, with a separate verification receipt. Filesystem 0444 is a measured reversible mode, not immutable storage. No original package, shared Git/index/refs/QUEUE/native tree, other chat, individual, remote release, or external publication was changed or contacted. Raw/private artifacts remain Git-excluded.

Required next step: globally repair R1–R3 using authentic evidence, prepare a new frozen package, and obtain the user's SECOND NEW full adversarial review. This first review cannot replace that gate.

