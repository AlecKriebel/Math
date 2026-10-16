# PR885 / PID9700042: final whole-package adversarial review 01

**Verdict: CLEAR for the exact sealed candidate identified below.** No unresolved mathematical, attribution, preprint-layout, metadata or reproducibility defect was found. This is the first eligible new whole-package review, and counts as one review only. The second new successive whole-package review must examine the identical final mathematical/publication core. A later substantive counterexample or core change invalidates this clearance for the changed core. Nothing here authorizes publication or repository mutation by this reviewer.

The strongest verified conclusion is the original edge-capacity theorem

\[
\lim_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}=1,
\]

where n tends to infinity at each fixed q before q tends to zero, paths may share vertices, and sources/sinks and normalization are exactly Aldous's prescribed square. The note correctly presents the whole asymptotic as an attributed corollary of BGT's older estimates after the explicit directed-model comparison. It establishes no novelty, first recognition, exhaustive priority or continued openness claim.

## Scope, independence and immutable candidate

At 04:38:31 UTC on 16 October 2026 I read the complete canonical native pair, then the full saved Aldous primary model. SOURCE_FIRST_FREEZE was recorded at 04:39:01 before reading the candidate or prior verdicts. I then read the complete actual note TeX, BGT §§2.2–2.5 and 3.1–3.4 in the primary extraction, and visually inspected actual BGT pages 16/23/24. ANALYTIC_FREEZE at 04:40:18 records the independent short-proof assessment before any prior current audit conclusion was read.

The archived clarified C1 and revised C4 bodies were read next. After this initial independent analysis I read preserved mathematical and classical/recent/completion priority reports, incident receipts and the initial V4 format report for comparison. Those are inherited evidence after exposure; I do not claim continued blind discovery. I did not receive a verdict from or communicate with the separate current primitive adversary. The parent may integrate any subsequently available report and must resolve any adverse result before promotion.

The externally supplied current-manifest SHA256 is
`bd07582e02490a57d5edd3f4438659b57b0fef8b5397f5865e3fe53220b5ec2a`.
It closes 197 files including the manifest itself. The independent portable-index pin is
`a45d6799b5770cd51cfb4e0bdbcd4461d981f13be733dfb1f57236ad838f51b9`.
It closes 159 archive members including the index. This review independently authenticated both, rather than treating a self-consistent candidate seal as its trust root.

| Core item | Bytes | SHA256 |
|---|---:|---|
| portable.py, both copies | 41629 | 8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c |
| note.tex, both copies | 19535 | 493e7b3756487bd47c2eb0f804e5bf253082b63e86f54c661c0ffbf40b7d39ea |
| oriented-flow-note.pdf | 82047 | e8ef086a61d1425c0e4892279a42f64079be1216c7936fff81628471c1ed2fba |
| oriented-flow-verification.zip | 388193 | 824b7f037be72f7c7337dba4ea00c6d72b11be5a8cf026e928e4e1b751753f3b |

AUTHENTICATION.json contains every one of the 197 checked file pins and the archive-member metadata. The frozen source manifest's independently supplied SHA256 is `6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d`. All 30 originals, totaling 214980 bytes, match SHA256 and computed Git blob identities. Head `4b1ef9bbeb723a4171949a6c3934db98962ac615` and original effort 5/5 match the pinned manifest. The 28 historical outer copies are exact; the active README/log deliberately supersede historical language. This reviewer made no Git or remote query and relies on the supplied current eligibility/head gate, not a fabricated fresh remote check.

## Checkable mathematics and falsification result

The full independent derivation is ANALYTIC_FREEZE.md. Its main checks are summarized here so that CLEAR does not rest on finite test success.

1. **Finite directed cut.** With N=n−2, the two forced source-to-sink edges contribute c_L+c_B. Every cut gives a balanced oriented interface at bounded faces, including checkerboard faces; the sole exterior degree imbalances force an interface route. Only outward crossings incur primal cut capacity. Conversely a simple dual crosscut separates the source and sink arcs and gives the reverse inequality. Nonnegative arbitrary capacities suffice. Thus V_n=c_L+c_B+T_N, including n=2. For Bernoulli capacities D_N=2N−T_N=max(k−b). Cycles have nonpositive reward; no monotone-cut substitution is permitted.
2. **Exact density and lower comparison.** Boundary terms are bounded, hence g(q)=lim E D_N/(2N)=1−v(1−q). The L¹ source result is an explicit premise; diagonal expectation superadditivity also supplies the expectation limit used by the proof. Grouping each pair of outgoing marked edges gives independent site indicators with r=2q−q². Each strict site chain in [0,N)² can choose a marked outgoing edge and connect monotonically inside Q_N. BGT's site score therefore provides D_N≥A_r(N) and σ_r/√r→2.
3. **Origin, terminal, local competitor.** The auxiliary terminal (N+1,N+1) makes every actual path site strictly below the counting boundary. The real terminal is excluded because the simple path makes no subsequent traversal from it. The origin indicator cancels exactly between k≤p+I₀ and A_r(M)≥a−1+I₀. Each nonlast segment is cost-minimizing: replacement intersections are harmless because nonnegative-cost loops can subsequently be erased. Strict anchor separation permits a monotone competitor that takes a marked first edge, giving b_j≤ell_j. The terminal gap uses the auxiliary boundary directly and needs no exterior competitor.
4. **Correct increment quantity.** The source's equation (19) and Lemma 19 contain a sum of individual negative parts in the other coordinate. Direct backward-variation charging gives X≤2b for this exact stronger quantity; replacing it by a net negative part is unnecessary and would misstate the source. Along with D_N−A_r(M)≤L−b, an excessive path satisfies the m=0 Item 5 with threshold τ=2δ and satisfies the overshoot predicate.
5. **Numerical sum and site normalization.** The m=0 slice of BGT's positive counting sum does not require an actual path without doubly marked sites. It simply weights each distinct open-site list by r^p. A deterministic choice of a distinguished coordinate makes its encoding injective; summing both choices only enlarges the bound. The displayed B₀/B₁ factors agree with the printed numerical kernel after independently naming the threshold τM√r. Choosing γ, then α, then small r yields B₁→0, B₀→4e²/(βγ) and a summable 2B₀/(1−B₁) geometric series. The resulting fixed-r tail is at most Cτ r⁻¹ exp(−M√r). No ordinary-FPP event is silently substituted.
6. **Ordered limits.** At each sufficiently small fixed q, N→∞ removes the exceptional expectation using 0≤D_N≤2N. This yields σ_r/2≤g(q)≤σ_r/2+δ√r/2. Then q→0 uses r/(2q)→1 and σ_r/√r→2; finally δ→0. This proves the full source target. Constants may depend on δ; no unsupported simultaneous-limit or uniform finite-size conclusion is claimed.

The ordinary symmetric-FPP theorem alone remains a blocked shortcut: its path deficit is k_f+k_b−2b, whereas the target deficit is k_f−b, so their difference is b−k_b≥0. The note correctly uses the larger numerical list estimate instead of this insufficient comparison.

Independent finite controls in check_package.py passed 961 arbitrary-capacity cases, including all 81 n=2 assignments from {0,1/2,2} and seeded nonnegative fractional/integer assignments through n=5. They also passed 28672 list/coupling cases covering all 4096 Q₂ internal Bernoulli edge fields, each with empty/full/single-flip boundary extensions. The latter check the selected minimum path's reward identity, cancellation inequality, distinguished-coordinate overshoot and X≤2b. Three stable kernel samples satisfy the convergence threshold. These are falsification checks and do not prove universal inequalities or the limiting theorem; the source inspection and deductions above do.

The archived clarified C1 bound e/2 has the expected first-moment loss and states its exact remaining gap at that historical stage. Revised C4 supplies a different complete longer proof: its stronger mark/backtracking tail, sparse finite-box rate-two Poisson limit, exponential uniform integrability, positive-excess Poisson tail-to-moment conversion, first-hitting rectangles and bad-perimeter budget, finite skeleton entropy, and disjoint original-edge witnesses support its full ordered-limit conclusion. I checked the primary DZ constant/upper-tail statement on actual pages 1 and 9 and the BK primary-author definition/product theorem on pages 2–3. Overlapping rectangles do not require independent fields: witnesses are disjoint original path marks, while padding costs no reward. I found no substantive contradiction with the short proof. Prior reports were read after my main analytic freeze and supply corroboration rather than substitute for the main derivation.

## Priority and presentation

BGT's 2021 primary estimates supply the entire asymptotic after the explicit directed-model map. This is strong evidence against claiming a new central rare-defect or detour estimate. The note states this fact in its abstract, introduction and scope, credits classical Poisson-chain/BK inputs and Verges's earlier related decomposition mechanism for the alternative proof, and accurately limits equation-level checking to arXiv v1. I did not inspect the final journal body or the Verges body in this review; those source/coverage limits are preserved in the earlier ledgers and are not converted to fresh verification claims here.

Preserved bounded searches not locating an earlier explicit flow statement do not prove firstness or present-day openness. The note and current metadata make neither assertion. Historical source-corpus “open” language and older audit statuses are exact archival records, clearly superseded by the active note/README/metadata. No weakening to site or vertex-disjoint flow has occurred.

The actual 82047-byte PDF has six A4 pages and the intended title, Alec Kriebel, ORCID 0009-0001-9320-500X, 16 October 2026 and version 1.0.0. Every page was inspected visually. No clipped text, overlapping equations, broken references or unreadable area was found. Fresh 100dpi rendering of the authenticated actual PDF matched all six existing final PNG hashes exactly. VISUAL_AND_SOURCE_RECEIPT records those hashes without publishing the renders. No new LaTeX compilation was performed.

The outer/inner TeX, tool, metadata and deposit copies match. Metadata has exactly 12 fields with the intended preprint/title/date/version, sole author and ORCID, open access and CC-BY-4.0. The nested deposit metadata matches it and lists exactly the separate PDF and verification ZIP assets. Description, note and README disclose extensive AI use, AI-agent adversarial reviews, unrefereed status and absence of completed human review or formal verification. They do not imply a DOI or completed final acceptance.

## Executed verification and negative controls

I fully read the complete current portable tool, exact original root including bootstrap, all five original checker bodies, and my own control code before executing them. Private scratch was directed into this review folder. The original checkers are run unchanged and compile with optimize=0; no candidate file was edited.

| Actual current command | Exit/stderr | Root/nested execution | Before/after |
|---|---|---|---|
| normal isolated current | 0 / zero bytes | 1 root, 64 nested; 20 positive,20 assertion-negative,20 corrupt,4 patch | all197 unchanged |
| optimized isolated current | 0 / zero bytes | 1 root, 64 nested; 20 positive,20 assertion-negative,20 corrupt,4 patch | all197 unchanged |

The elapsed times were 67.223 and 69.865 seconds. Full stdout, empty stderr, process receipts and independently checked summaries are preserved. Measured root optimize was 0/1 respectively; root and checker compilation optimize remained 0. Each child has actual isolated/no-site/no-bytecode flags; historical requested labels retain their distinct meaning. Corrupt scripts failed before checker execution, forced assertions failed under every requested optimization mode, and every positive generated JSON matched original bytes. The original root's output agreed semantically except for its explicit Python-version field.

Independent archive checking verified all members' bytes, sorted names, regular0644 metadata, fixed epoch, local records, raw compressed-stream complete consumption and EOCD extent, then separately rebuilt the ZIP byte for byte using the same Python/zlib runtime. The authenticated current CLI independently validates its raw central-directory representation as well. Same-runtime compressed reproducibility is accurately qualified; no cross-runtime promise is implied.

Fourteen complementary controls reject typed byte booleans/floats/negative/excessive counts, overflowing JSON numbers, directory case aliases, ZIP trailers, unlisted empty directories, symlinks, and a self-consistently rehashed/rebuilt wrong nested ORCID that reaches the intended creator validator. A pin-order spy proves third-corpus whole-pin rejection precedes any target parsing. Actual CLI wrong external pin, incomplete source list and attempted build verify-only bypass each reject with measured zero archival Popen calls. The separate actual source-only CLI passed all three full corpus pins before extracting the exact 5104-byte pair and 145-byte statement; it reads/executes zero archival code and copies no raw corpus. Full primary hashes were separately checked, not treated as mathematical interpretation certificates.

The text scan found no machine-private paths or obvious credential patterns in candidate textual files. No third-party HTML/PDF bodies or raw native corpora are present among the portable members. Original mathematical/audit prose is preserved as authored history, while primary-source bodies and renders remain private.

## Incident honesty, remaining limits and decision boundary

The earlier optimized build is an actual recorded failure, not retroactively a PASS. Its reported checker-status mismatch occurred during observed storage exhaustion; the exact failed child/cause was not captured, so ENOSPC causation remains an inference. The subsequent parent normal outside build succeeded and created the exact sealed ZIP. The parent current normal/optimized commands succeeded; a later print-only summary used the wrong result path and raised KeyError after receipts were saved, as corrected readback documents. My own two current executions above independently succeeded; they do not erase prior failures. Earlier artifact-audit incidents and clean retries remain accurately dated historical records.

No unresolved proof or package gap was identified for the pinned candidate. Remaining limits are explicit: fallible AI review, cited classical inputs, no exhaustive priority census, no human/formal verification, no hostile concurrent-filesystem sandbox, same-runtime ZIP compression scope, and dependence on the supplied fresh remote eligibility gate. A second new whole-package CLEAR on identical core is still required; neither initial mechanism/priority/tooling reports nor this one report substitutes for both reviews.

All work is confined to package_review_01. No other individual, chat or shard was contacted; only the parent agent received progress. No Git/index/remote, PR, merge, release, DOI, GWS or publication action occurred. Original 5/5 proof-search effort is unchanged. SAFE_FILES_MANIFEST.json explicitly selects this review's safe authored files, excluding private scratch, raw source bodies, renders and credentials; it excludes itself from hashing and grants no recursive publication authority.

Completion estimate: **100% of this assigned whole-package audit**, with one eligible CLEAR review completed on the exact pinned core.
