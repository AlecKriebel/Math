# Complete-package adversarial review 02 — frozen candidate v2

Completed 2026-10-07T05:45:55.144810+00:00. Reviewer: independent internal AI agent `package_review_02`; fresh primary-source subreview `upstream_falsify`, with independent actual-Lean scope subreview. Automated review is not conventional human peer review.

**Verdict: REQUEST ONE REPRODUCTION REPAIR. No substantive mathematical or attribution gap identified. The exact v2 package has a substantive remaining reproduction issue and must not be published as passed.** All five earlier v1 repairs propagated. The sole new required repair is the documented-cwd self-copy defect below. This verdict does not apply to a future v3 package, which needs a new complete independent reviewer.

## Exact identity, custody and coverage

I began with actual `AGENTS.md` and `research/USER_REQUEST.txt`, then reconstructed the gadget/gluing/bit and sampler arguments from the current manuscript and primary sources. Every authored ZIP member, intended upload file, metadata field and resolution/priority statement was inspected. Independent findings were saved before opening prior complete-package review/response files. A concurrency inventory incidentally exposed earlier agents' short final verdict summaries; neither I nor the upstream subreview used them as proof. This was independent reasoning, but not a fully blinded review.

No external individual was contacted. No source-clone Git state, candidate file, manuscript or publication manifest was changed. Review writes are confined to this review folder and this report. The shared main branch/index were untouched. Render images and my third-party extracted reading text were hashed and removed; third-party formal-source reading snapshots in the child folder remain reading evidence and should stay outside the publication payload.

`READ_HASHES.json` independently records all my accessed file hashes; `ZIP_MEMBER_HASHES.json` hashes all 29 members, including the hash manifest itself. The child source receipts hash every primary file it read. All 28 declared payload hashes matched independently, and the ZIP has only safe relative regular-member paths. `FROZEN_V2_RECHECK.json` confirms the outer files and manuscript remained unchanged through the audit.

| Exact reviewed v2 file | SHA-256 |
| --- | --- |
| Candidate identity | `e44510e63558fab34a07f99575df20ff39619e4230e052144837b8b776f6da91` |
| `manuscript/main.tex` / archived `main.tex` | `25a9b9e5df03ea50c24812f5107bf3913ab352296faf6d5170e0372c4be8b9f4` |
| `manuscript/main.pdf` / uploaded and archived `paper.pdf` | `9e16fbfedfd1cb52a0ed8a1c3648bb06b1afffa4d9f4a1bfa596eb91330f3041` |
| `zenodo-deposit.json` | `fbc5934f75f6edb72e2092e17a359295e94747932ea13dbd2652ebefc67d2d69` |
| Source/verification ZIP | `cd63ad9d2a1ee591f49721d5b97150ee2bda9a116e8250a93ebc82bd0bafdd2c` |
| Uploaded/archived README | `0a86b02f122533380a8abbfeaa2df998132bb5da77121fc7dd6b5c4194ebbc26` |
| Defective v2 `reproduce.py` | `26e1eebf1559dbc82d94ca2f406d74a6f94b697859a33500fe2c74a363484160` |

Coverage includes the source/PDF, both full proof supplements, all six Python files including reproducer, all three saved finite-check reports, the payload digest manifest, README/licenses, theorem snapshot, approach/dependency tables, dependency-reference JSON, all three audit reports, optional inspector and original static receipt, and all three priority statement/search/BibTeX ledgers. Outer Zenodo metadata and the exact three intended upload files were checked. No practical upstream algorithm, third-party PDF/source closure, runtime or credential is advertised as being included.

## Required repair — P1: documented reproduction copies into itself

Archived `README.md:35` instructs the reader to extract the ZIP and run:

```text
python3 reproduce.py --output reproduction-receipt.json
```

Archived `reproduce.py:15–16` creates its temporary directory under `Path(args.output).resolve().parent`, then calls `shutil.copytree(ROOT, Path(td)/'package')`. In that documented working directory the output parent equals ROOT. The temporary directory is therefore already a descendant of the source being copied. Recursive copying encounters that same directory and its growing destination again, leading to storage exhaustion/path failure rather than the advertised clean check.

The root researcher alerted me to this boundary. I independently executed the exact frozen v2 script with only `shutil.copytree` instrumented to record ancestry and raise before copying. Its actual destination was `ROOT/hafnian-clean-3dso3_bh/package`, demonstrably within ROOT. Evidence is `REPRODUCTION_BOUNDARY_FAILURE.json`. No recursive copy was allowed to consume disk. This is a real defect in the documented default command; the successful check below used an external output receipt and therefore missed this boundary.

Repair copying so that it cannot traverse its own temporary destination, preferably by copying only the integrity-declared payload members plus the manifest rather than the entire source directory. Test **the exact documented invocation from extracted ROOT**, along with an external receipt path, and verify the original extraction stays intact. Refresh the affected ZIP/candidate hashes and provide a new full reviewer the exact repaired package. This finding needs no change to the mathematical proof. It blocks current v2 package readiness.

## Independently checked mathematics

The exact deduction is sound. In the Horner DAG each old path has two extensions and the optional source arc adds one, hence w↦2w+b. Topological creation order excludes cycles and duplicate arcs. Splitting each internal vertex makes a matching choose either its identity edge or one incoming/one outgoing arc. Thus chosen arcs are a terminal path plus potential cycles; acyclicity removes the latter. Both terminals removed leaves only the identity matching, and one terminal removed leaves odd order. This proves `(W,1,0,0)`, including W=1, with 4 bits(W)−2 vertices and at most 6 bits(W)−5 edges.

Global restrictions cover each gadget's even internal vertex set plus zero or two original endpoints by parity. They therefore select an original perfect matching, with independent local matching fibers of product W_e. W=1 terminal edges cannot collide because the support is simple. Arbitrary terminal orientations do not require the whole expansion to be bipartite. Product denominator D has O(L) bits; each integer W_e has O(L) bits; O(L) support edges give O(L²) graph size; vertex indices add a logarithmic encoding factor. D^m has O(mL+1) bits. No W-fold numerical expansion occurs.

Exact support witnesses decide zero independently of random estimates. On a positive integer count C≥1, any successful epsilon<1 estimate is strictly positive, so replacing a failed zero estimate by one does not change a successful tape. Division by D^m preserves relative error and polynomial bit size. Calling the cited theorem at min(delta,1/4) fits its confidence domain. Empty matrices, disconnected support, odd components, zero edges, weights below one, large denominators, arbitrarily small positives and ignored diagonals are correctly covered.

The sampler proof handles the full adaptive law. Exact child feasibility removes zero branches and keeps a witness on every tape. Current successful normalization costs at most alpha/(1−alpha) in TV. Fixed-bit cumulative flooring costs at most j/2^b, never accidentally choosing a zero interval. Fresh count tapes give conditional current failure at most j gamma for every preceding history. The failure event, including all-zero witness fallback or gross overestimates, costs discrepancy at most one. Coupling at common histories without conditioning final output on global success gives

`TV ≤ k alpha/(1−alpha)+k² gamma+k²/2^b <5 eta/6<eta`.

The ideal vertex-partner recursion is uniform. Termination is deterministic, at most k decisions, k² count calls, k²+1 witness calls and kb extra draw bits. Every failed oracle output has polynomial length from its every-execution runtime, and normalization/CDF/floor arithmetic stays polynomial. Fibers give exactly the rational weighted law, and deterministic pushforward contracts TV. No pointwise guarantee or logarithmic-in-eta runtime is claimed.

`INDEPENDENT_FINDINGS.md` preserves the more detailed reconstruction made before the prior response comparison. No substantive local mathematical defect was found.

## Primary upstream dependency and formal honesty

Fresh subreview `upstream_falsify/INDEPENDENT_REPORT.md` has SHA-256 `8047c5d293a7cadcc640dbc8537aad11233e4dea680007de774c8bcea5506a1c`. It starts from the actual pinned manuscript, not a prior favorable audit, and reconstructs four-hole injections, strong-path relocation/continuation, subdivision deleted-hole accounting, bottleneck capacity charge, signed cell identities, reversible multiset repairs, rare-guide cancellation, congestion, replicated ANOVA arbitrary-function gap, exact dynamic programming, annealing/scale restoration and every-failure-history bit bounds. It found no substantive upstream gap. Exact source locators and independent certificates are in that report.

Its checks passed 34,868 closed tree-label walks, 133,698 cells and 24,569 two-long-side error demands, including symbolic global identity, guide containment and isolated swap component. Generic weighted enumeration on a 100-vertex subdivided graph agreed with the deleted-hole formula for 1,767 hole sets, including subunit activities, and 189 ANOVA components were uniquely charged. These are finite falsification checks, not certification of the complete algorithm.

The genuine Lean theorem `OAI.MatchingFPRAS.thm_main` and actual Model definitions quantify one finite machine over all finite simple unweighted graphs and rational accuracy/confidence parameters, with every-tape time/output and one-way zero semantics. The actual proof differs from the comparator `sorry` stub. The fresh formal child checked the concrete ladder gap/mixing assumptions and where the local pair gap is discharged, traversed all 415 local modules, and verified 423 accessed primary files against the pin. I also ran the archived optional source inspector from extraction: its hashes/scope match the original receipt, it works with unavailable Lean, and it accurately reports no kernel check.

**No full upstream Lean kernel build, compiled axiom closure, successful comparator check or end-to-end upstream FPRAS run was reproduced.** The actual import probe cannot load missing compiled dependencies. Lexical token absence and directory names are not proof. All candidate claims preserve this limit, credit the external theorem, and make no weighted-follow-on formalization claim. The approximation conclusions rest on the cited theorem's independently scrutinized manuscript argument.

## Reproduction, data, executable attacks and PDF

With the receipt placed outside extracted ROOT, `reproduce.py` verified all 28 declared hashes and reran all three exact checks. `CLEAN_REPRODUCTION.json` records the run. The saved mathematical reports agree exactly after removing only gadget generation time/runtime fields. Saved upstream table output also matches. The test counts and limitations in manuscript, proof supplements, README and data agree.

My separate `independent_checks.py` imports only the candidate construction and imperative wrapper, not its matching counter or law integrator. Its own graph recurrence checked 262 signatures (1..256 plus 511,512,513,1023,1024,1025); all 64 terminal orientations of a weighted K4 gluing with 192 individual fibers; and the actual executable wrapper on all 37 feasible K4 supports with synthetic **gross nonzero failed overestimates**, every categorical tape and every oracle failure pattern. All 9,088 executed histories and exact resulting laws satisfy feasibility, call/bit caps and TV bounds. `INDEPENDENT_CHECKS.json` records maximum TV/eta `24753/229376`. This expands failure coverage beyond the packaged zero-estimate synthetic laws.

All six deposited PDF pages were rendered and visually inspected. Metadata matches the title and sole author; the PDF is unencrypted, has no JavaScript, uses embedded fonts and six letter pages. Formula symbols, bound displays, hyperlinks/citations, numbering and page breaks are legible with no clipped/overlapping content found. The deposited and manuscript/archived PDFs are byte-identical and the extracted mathematical text agrees with the standalone source. I did not claim an independent second-toolchain rebuild. Render PNGs were hashed and deleted rather than staged.

## Priority, metadata and earlier repair propagation

Actual Dell ECCC §3/Figure3 and McQuillan §7.2/Lemmas25–27 affirmatively establish logarithmic integer gadgets and binary rational weighted-to-simple-unweighted equivalence. JVV §6 is the classical count-to-generator framework; its generator definition is not confused with the separately analyzed always-feasible TV wrapper. Actual RSZ Theorems1.2/1.9, Barvinok Theorem2.1 and Yi Theorem1.1 have the stated restrictions. The actual entropy weighted bracket/512^n guarantee differs from FPRAS. Source READMEs supply the credited OpenAI author/title/year.

Fresh bounded searches and actual primary registry pages are recorded in `FRESH_PRIORITY_SEARCH.md`. The official OpenAI release page is October6,2026; manuscript September23 is not substituted for public priority. API refresh was rate-limited; a read-only remote-ref refresh independently still returned the exact pin. No identical complete current implementation note was found, but search absence is not a novelty certificate and recent indexing may lag.

The package explicitly says old reductions/self-reduction and the base breakthrough are inherited; no separate unresolved complexity theorem, first weighted FPRAS, new reduction or independent base solution is claimed. This attributed consequence/implementation framing meets the original request within the documented bounded no-identical-note evidence. An identified identical entire public note would reopen the no-duplicate condition. No stronger novel-result claim is justified.

Zenodo title/description, date, version, CC-BY-4.0 metadata, references and three intended uploads match the package. Only Alec Kriebel and the supplied ORCID appear as author metadata; no affiliation/coauthor was invented. Prose/data and code licenses are explicit, as are extensive AI use and absence of conventional human peer review. The manifest now uses path objects. This review neither created a remote deposit nor verified a public DOI/tracker entry.

Only after saving independent findings did I read `PACKAGE_REVIEW_01.md` and `RESPONSE_TO_REVIEW_01.md`. Each required v1 fix propagated: manifest objects, “project records” review wording, corrected primary locators/control character, accessible optional inspector/receipt with total missing-tool handling, and dated prepublication snapshot with separate later receipts. None remains a substantive issue in v2. The prior favorable mathematics was not used as proof replacement.

## Final disposition

Review coverage is 100% for the assigned mathematics, priority, metadata and complete-package scope; readiness is incomplete because the one documented reproduction defect remains. These completion estimates describe reviewed work, not a theorem-truth probability or completion of the user's publication objective.

**Latest exact reviewed candidate v2 still has one substantive remaining issue: its documented reproduction command recursively copies into itself. No other substantive concern was identified.** Preserve v2 and this finding, repair and checkpoint v3, then obtain a NEW full-package review before publication. A clean future reviewer verdict will be evidence, not a replacement for proofs or dependency checks.
