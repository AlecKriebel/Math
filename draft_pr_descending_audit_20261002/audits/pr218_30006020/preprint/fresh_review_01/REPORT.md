# First fresh sequential manuscript adversary: PR218 / 30006020

Review cutoff: 2026-10-15 UTC. This is the first NEW review of the finished preprint package, after its preparation, not a relabeling of the earlier mathematical or priority families. Work was restricted to fresh_review_01. No manuscript, current source, Git/index/ref, provider, deposit, tracker, or PR state was changed; no outreach was performed.

**Verdict: one repairable mathematical-precision issue must be fixed before the next fresh review. No counterexample or substantive gap was found in the geometric mesoscopic theorem under the finite-vector interpretation specified below.** This is not a clean frozen-byte verdict and does not authorize release. The required second/new manuscript adversary remains necessary after repair.

## Frozen exact review object

Before inspecting earlier acceptance verdicts, I actually checked the five submission files against FROZEN_INPUTS.json and checked all136 archive payload records. The137th ZIP member is its self-excluding PACKAGE_FILES.json. There are no duplicate, absolute or parent-traversal ZIP names. Metadata in deposit.json and metadata.json is identical. My initial verification harness incorrectly expected the payload list to include the manifest itself; it was corrected to the actual documented self-exclusion before any acceptance claim. This was a verifier assumption, not a package defect.

The reviewed manuscript has SHA-256 `db6d1ab043cf6bff42c1162534716586555b6688684ba9e5f8fb4f87e5f3e245`; its seven-page PDF has SHA-256 `4090da8217ae8cd051c9b2b5f3e4e8429b14dd91fa34f6bcd7e4250739ad8f20`. The reviewed ZIP has SHA-256 `94b5815e1826d4a8907a51a7aad2d77d075230462e13002177d99f5c7271d966`. These hashes, rather than a later filename with changed content, control this report. Full receipts are in FROZEN_PIN_VERIFICATION.json.

I read the complete LaTeX, actual PDF, metadata and deposit specification, top-level and verification READMEs, verification runner, evidence map, primary input records, preparation/provenance records, complete current CANDIDATE.md and current source/disposition documents. I checked the entire ZIP inventory, every payload hash, current/history manifests and actual historical source bytes. I read the archived final priority synthesis and assembly comparison only after reconstructing the proof and controlling source statements; their conclusions were not substituted for source reading.

## Mandatory finding M1: make Poisson conditioning finite

**Location:** cylinder_areas.tex line65, PDF page3, first paragraph. The explanation identifies composition counts with independent Poisson variables conditioned on an unindexed sum, immediately following the definition of an infinite sequence a_j.

Taken literally for independent Z_j~Poisson(a_j) for all j>=1, this is a zero-probability event: a_j>=1/(2j), sum P(Z_j>0)=infinity and independence imply infinitely many nonzero entries almost surely. Hence sum_{j>=1}jZ_j=infinity almost surely. The intended finite conditioning is valid and has positive probability, but it must be explicit in a submission-ready proof.

**Required repair:** say that if Z_1,...,Z_n are independent Poisson(a_j), then (C_1,...,C_n) has their conditional law given sum_{j=1}^n jZ_j=n; set C_j=0 for j>n if an infinite padded count vector is subsequently used. A separate phrase can retain the fact that the independent sequence used for ABT exists for all j; its conditioning relation always truncates at n. AT and ABT's actual primary statements support exactly this finite version.

This corrects an explanatory equivalence, not the ordered-composition definition or the theorem. The composition probabilities, exact factorial identity, all succeeding marked formulas and the argument are valid with this interpretation. Apply the precision change at every current presentation that states unindexed conditioning; rebuild the PDF and archive and regenerate all affected current/package/frozen manifests. Preserve the reviewed bytes or their exact frozen provenance and all historical originals; do not rewrite the old audit as a clean verdict for new inputs. Descriptions that never state the conditioning equivalence need no artificial wording change. No new theorem or proof strategy is needed.

## Mathematical/source attack and strongest verified conclusion

INDEPENDENT_DERIVATION.md supplies my reconstruction and exact checks of the potential failure points. I used actual primary PDF bytes whose eight package source pins all match, with a precise direct-read map in PRIMARY_PIN_AND_READ_MAP.json.

The original OWR contribution's full definitions, footnote, Theorem2, Problem2 and Problem3 support the principal holomorphic quadratic ensemble, uniform isomorphism-class sampling, maximal horizontal cylinders counted once, whole-surface normalized area and iterated square-count then genus limit. The literal example is the manuscript's window. Other strata and diagonal limits are separate. DGZZ's principal-stratum lattice-count passage and DL1.4 support the fixed-genus measure convention; no implicit primitive-cover or all-direction assertion is used.

DL's exact positive graph mixture, automorphism convention, uniform coefficients and the entire Lemma6.4 expansion give the stated latent Dirichlet mixture. The independently cancelled prefactor ratio is correct. Uniform coefficient control plus normalization gives an actual uniform RN derivative bound, not weak convergence of fixed macroscopic coordinates. Forgetting labels and applying the common kernel preserve it.

I checked DGZZ1.12 and its generating-function derivation and DGZZ5.2 with the full proof and its low-k regime split. The chosen .6log(2n) cutoff is within its stated range. The polynomial upper-cylinder tail and low-k multivertex excess are sufficient; the proof does not need DL's printed exponential logarithmic-tail estimate or DGZZ's subsequent unrestricted separating-graph corollary. Fixed exponential-count moments imply logarithmic K moments, and Cauchy–Schwarz kills all fixed bad-event count moments.

The analytic coefficient estimates follow from the actual zeta product and DL Lemma6.7. Removed mass in a fixed unmarked factorial moment is O(q)=o(n), and the harmonic mean tends to half log(b/a). AT Lemma5/(126)'s complete proof yields the selected-component identity. ABT Theorem3.1 and its proof cover every initial segment b_n=o(n); the exact Poisson means satisfy ULC with theta=1/2, e(j)=C/j and factorially summable tail constants. Those are correctly credited old results.

The Gamma comparison avoids a log(n) union bound. The middle range loses O(q^-1/2); the small-size range loses only O(log(q+2)exp(-cq)); the large-size range has exponential lower tails, including when the coefficient ratio is O(sqrt n) near n. This works for arbitrarily slow q->infinity and n/q->infinity. Gamma total concentration and continuous random dilation need no independence assertion.

All marked factorial moments are bounded by splitting removed mass at n/2. Large removed mass forces one selected Gamma shape of order n to enter an o(n) window, an exponentially small event. On the likely normalization event normalized counts are bounded by enlarged marked-window counts; the exceptional contribution is bounded by n^r exp(-cn). Higher moments therefore provide UI for all joint powers. The good-event RN comparison and bad-event moment control transfer these moments to geometry. TV alone is not used for this unbounded conclusion.

Finally, simplex densities for at least two components and the isolated one-cylinder atom at1 settle the fixed-genus window-endpoint issue. At each fixed genus counts are bounded by3g-3; thus the N-first weak law also transfers the relevant moments. I found no hidden exchange with a diagonal limit.

The strongest verified mathematical conclusion is the stated same-ensemble PPP(dx/(2x)) for every s_g->0, gs_g->infinity, with every fixed joint compact-window count moment, including the original Poisson(log(2)/2) count, mean, variance and zero probability. The whole-area TV comparison is supported. All statements remain conditional on the cited substantial geometric results, which this review does not independently reprove in their entirety.

## Actual reproduction and provenance checks

The actual runner extracted from the reviewed ZIP passed with only Python's standard library. PORTABLE_REPLAY_RECEIPT.json records7,100 counted exact assertions,46,233 labelled permutations and123 separate rational DVV composition cases. The floating DVV diagnostics are explicitly excluded from exact certification. A changed program in a separate private copy is rejected by the actual runner; WRAPPER_ADVERSARIAL_CHECK.json records that negative control.

I also wrote a new114-assertion rational checker using a Bernoulli recurrence, ordered compositions, exact binomial Beta CDFs and direct polynomial integration of two-coordinate Dirichlet rectangles. For n=1,...,8 it compares direct composition averages of normalized first and mixed two-window count moments with selected-component formulas, including the residual-shape-zero boundary. It also supplies exact sign witnesses for the Chernoff and cutoff constants. This is additional finite algebra evidence, not a limit theorem. See independent_exact_checks.py and INDEPENDENT_EXACT_RESULT.json.

All22 historical originals are actually byte-identical to the original submitted snapshot, all5 current source records match their manifest, and current mathematical core sections3–9 match the original core. Historical reviews refer to the historical hashes; no resealing deception was found. The archive includes authored reports and metadata rather than full third-party PDFs, extracted texts, rendered source pages or raw search payloads. Private source evidence and rendered review pages remain ignored.

## Priority, bibliography and disclosure review

The manuscript and current public descriptions credit the exact DGZZ weighted permutation law, DL/DGZZ geometric formulas and Aggarwal's underlying estimates, AT's factorial identity and ABT's all-rate unmarked approximation. The claimed contribution is the explicit geometric consequence and its marking/moment justification. It makes no new-enumeration, new-model, new-general-probability or universal-first-priority claim.

I checked the actual DL p5098 announcement, the full relevant thesis Remark1.5.9 and its continuation, and rendered thesis p22 plus Durham pages26/195. The all-multiplicity thesis formula and primitive slide formula are distinguished. A fixed microscopic window and an intensity tail do not supply moving-window uniformity. The note expressly retains the unavailable Small components manuscript as a priority uncertainty. That unavailable content is neither a positive prior-coverage theorem nor an excuse to claim exhaustive novelty. The qualified consequence framing is defensible on the bounded evidence described; this review does not certify absence of all undisclosed or unlocated overlap.

The literal OWR4g-4 and exact Gamma6g-6 microscopic scales remain distinct. Their difference is not silently ascribed to tile units or resolved by a false fixed-scale identification. The manuscript does not promote a new microscopic theorem. The source's intermediate window is unchanged.

Publisher metadata directly confirms DL's online7June2024 date and final JEMS27(2025)5093–5131 issue and OWR's14February2025 report publication. Crossref metadata verifies ABT's DOI/title/pages and Aggarwal's title/volume/pages; the eight bibliography entries match the source metadata read. The OWR41/2024 designation is a report identifier, not an invented publication date. No bibliography defect was found. Precise metadata receipts are in BIBLIOGRAPHY_METADATA_CHECK.json.

Alec Kriebel's supplied name/ORCID are correct. Extensive AI assistance is disclosed in the note and descriptions; the text says unrefereed, no external human peer review and no proof-assistant formalization. Internal AI checking is correctly distinguished from human review. No endorsement or participation by cited researchers is implied. Deposited metadata mirrors the intended scope and finite-evidence limits rather than claiming computation proves the theorem.

## Visual and process disposition

I rendered and actually inspected all seven PDF pages. No clipping, overlap, missing mathematical glyph, broken reference, black-square artifact or unreadable URL was found. The theorem's normal continuation across pages1–2 is legible. VISUAL_QA_RECEIPT.json seals the page renders and the exact reviewed PDF.

Completion estimate: **100% of this assigned first manuscript audit**. One mandatory precision repair remains in the reviewed package; the root publication goal is incomplete. After M1 is fixed globally and the affected outputs/manifests rebuilt, assign a NEW adversary to the new frozen package as required by the user. Do not treat this report, its finite checks or the existing priority gate as provider-release clearance.
