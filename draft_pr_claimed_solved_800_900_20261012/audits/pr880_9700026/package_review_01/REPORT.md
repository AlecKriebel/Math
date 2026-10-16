# PR880 / 9700026 — new independent whole-package review 01

Review date: 15 October 2026 UTC. Target: AMR-096-0026, original effort 2/5. This review evaluates one sealed candidate, not the research program as a whole. It is an AI-assisted independent adversarial review; no outside person was contacted, no completed external human refereeing is claimed, and no formal proof-assistant certificate is supplied.

## Disposition and exact target

The finite claimed result is sound within its explicit assumptions, and the current proof, source interpretation, credits, PDF, metadata, inventories, archives, and active verification interfaces agree. No actionable repair was found in the reviewed sealed candidate. This finding must be read with the exact test and literature limits below; a fresh second whole-package review and the parent's publication workflow remain separate requirements.

The trust anchor is `PACKAGE_SEAL_R1.json`, with all eleven core entries independently checked against actual bytes before executing supplied code. The exact bindings are:

| Object | Count / bytes | SHA256 |
| --- | ---: | --- |
| Current outer `PUBLICATION_MANIFEST.json` | 215 files including manifest; manifest 43,756 bytes | `11258d48f5ba2c0c0d5bd1893c1aaba8ac2fe3c2c4cd042181ba22f25f8decc2` |
| Portable `package_index.json` | 161 members including index; index 28,008 bytes | `7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d` |
| Current PDF | 81,811 bytes; 5 pages | `dc870b5a0dfa4bb5977417675912570da447a7c635d06617ada7f0cd94d5a495` |
| Verification ZIP | 568,282 bytes; 161 members | `944e5d99825a3ef6689cff551f28bc9bb7aee04a1f58dbbceb6fd55bace4af2f` |
| Current outer startup wrapper | 19,010 bytes | `b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7` |
| Portable verifier | 9,852 bytes | `73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a` |
| Original-artifact checker | 22,093 bytes | `e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f` |
| Deterministic builder | 10,648 bytes | `a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca` |

`SEAL_AUTHENTICATION.json` includes the eleven exact core rows. `INDEPENDENT_INVENTORY.json` records independent closed-file-set and byte verification before the real candidate replay. This decision applies only to those bindings. The original snapshot is anchored at `fba74a301786f9648e48722e76f440097b0746c2`.

## Independence and source-first sequence

Before opening the candidate proof or any previous auditor verdict, I read the primary 2007 Conjecture 32 and model scope, the 2012v1 model and complete paper text, original Lemma 3 on p.9, and unfinished Proposition 30 on pp.36–37. I then wrote `INDEPENDENT_MEMO.md` with a disk-capture proof, scalar comparison, regular-level-set mechanism for local Lipschitzness, continuation argument, scope exclusions, and likely failure routes. The memo is a genuine prior checkpoint of this review, not a paraphrase of the candidate.

Only afterward did I read `preprint/note.tex`, the original `source/author/PROOF.md`, current README/priority/metadata/deposit files, and the earlier bounded priority reports. I independently read the first two scanned pages of Aurenhammer–Edelsbrunner visually, and Ferudun's relevant complete sections/pages. Previous mathematical or tooling verdicts were not treated as proof authority. Actual fresh sealed-tree executions and new controls are recorded here; historical counts are not promoted into new executions.

## Exact source target and domain

The full record/report pair was independently located at catalog index 933, problems index 4479, and report key `AMR-096-0026`. Its standard sorted-key serialization is exactly 4,409 bytes with SHA256 `7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193`; the exact statement digest is `5544971834bd618005b3fdf611f753b4cf41bab24b857d0e96a7a067ee3f7b7e`. Both catalog bindings match. This used the complete records, including surrounding context, rather than a shortened mathematical projection. Their raw contents are not redistributed.

The primary 2007 notes, p.2, allow all positive alpha and beta. Page 40 freezes finitely many city sites, removes founding, writes exactly `z_i'=area(S_i)-z_i`, defines spheres by the hard maximum of `z_i^alpha |y-x_i|^-beta`, and states the collapse clause with the disjunction alpha>1 OR 0<beta<2alpha. The general-position phrase applies to positions and positive initial data but is not defined there. The candidate faithfully refutes the literal unrestricted alpha>1 alternative on alpha>1, beta>2alpha; it does not silently repair that alternative and then claim to have refuted a different one.

The 2012 arXiv v1, p.2, explicitly restricts 0<alpha<=1 and models stochastic founding. It does not state Conjecture 32. A fixed-city persistence proof neither refutes that parameter declaration nor proves stochastic coexistence. The candidate consistently separates these scopes. Taking a positive beta-th root of all influences changes no winning set and therefore no time variable: only alpha/beta enters this fixed ODE.

## Analytic proof audit

The theorem is for every fixed finite n>=2, every collection of distinct interior sites, every positive initial probability vector, and positive alpha,beta. Global positive existence and uniqueness are stated without the beta>2alpha restriction. The quantitative persistence conclusion adds beta>2alpha. Interiority and distinctness are used exactly to choose positive geometric constants; no genericity or cell-combinatorics assumption is smuggled in.

### Null ties and local Lipschitzness

For two distinct foci a,b, the candidate uses `F_lambda(y)=|y-a|^2-lambda|y-b|^2`. At lambda=1 this is a nonconstant line; otherwise its zero set is an Apollonius circle. Thus pairwise ties are planar-null and a finite union remains null. The finitely many sites are also null. The full cells cover the square almost everywhere, so their areas sum to one regardless of conventions at sites and ties. Strict-winner persistence and dominated convergence give area continuity on the positive orthant.

I checked the stronger quantitative argument, including its constants. Direct expansion gives `|grad F|^2=4(lambda d^2+(1-lambda)F)`, where d=|a-b|. With lambda in [m,M], m>0, and the stated epsilon restriction, `|grad F|^2>=2 m d^2`. At least one coordinate derivative therefore has magnitude at least `sqrt(m)d`. Along any slice a quadratic has at most two intervals with that derivative magnitude and constant sign. Intersecting with the band gives total length at most `4 epsilon/(sqrt(m)d)` in that coordinate. Summing the two coordinate estimates gives the stated band-area bound `8 epsilon/(sqrt(m)d)`.

A changed dominance test satisfies `|F_lambda|<=|lambda-mu||y-b|^2<=2|lambda-mu|` on the unit square. This gives the stated local pairwise area estimate with constant 16; a finite union bounds full-cell symmetric differences. Smooth positive ratios `(z_i/z_j)^(2alpha/beta)` complete the proof. Equal weights, crossing a square edge or corner, multiple ties, and changing cell topology do not invalidate this slice argument. It does not divide by lambda-1 or assume transverse intersection with the square boundary. My new sparse-polynomial checker verifies the general gradient identity symbolically, with zero residual terms, rather than checking only selected numerical substitutions.

### Positive global continuation

Local Lipschitzness supplies a unique local classical solution in the open positive orthant. Summing the ODE gives `s'=1-s`, preserving s=1. Nonnegative areas give `z_i'>=-z_i`, so `z_i(t)>=z_i(0)e^-t`. Before any hypothetical finite maximal time, every coordinate stays uniformly positive, all stay at most one, and the derivatives are bounded by one in absolute value. The state has a positive limiting value and can be extended locally there. This rules out a finite maximal time. No boundary uniqueness theorem is assumed. The possible singular behavior of z^p at zero for p<1 is immaterial to local Lipschitzness on the positive orthant.

### Simultaneous all-competitor capture

Write q=alpha/beta and p=2q. Choose h_i>0 with the displayed site-square containment and `8h_i^2<=|x_i-x_j|^2` for every j!=i. For y in the scaled square of halfwidth `h_i z_i^q`, the own distance is at most `sqrt(2)h_i z_i^q`, while every competitor distance is at least `2sqrt(2)h_i-sqrt(2)h_i z_i^q>=sqrt(2)h_i`. Because all competing simplex weights are at most one, this yields the exact dominance inequality against every competitor at once. It is not merely pairwise dominance over the nearest site. The square is wholly inside the domain; no clipped-area approximation is used.

The resulting bound `A_i>=K_i z_i^p`, K_i=4h_i^2, is valid on the full positive simplex, not just near an equilibrium or within a chosen basin. This also explains why a symmetric-equilibrium objection is ineffective. My pre-proof disk reconstruction gives the same mechanism independently, with different valid constants.

### Scalar inequality and conclusion

For p<1, set `u_i=z_i^(1-p)`. Positivity justifies differentiating, and the exact inequality is `u_i'>=(1-p)(K_i-u_i)`. Integrating gives the candidate's bracket and exponent. The bracket is a positive convex combination of K_i and the initial transformed value, so no invalid power or reversed comparison occurs. Each coordinate has the all-time bound `min(z_i(0),K_i^(1/(1-p)))`; the limiting inferior is at least the latter constant independently of the initial state. Summing the other coordinates' bounds yields the stated upper bound below one. This directly refutes collapse without assuming the conjecture's convergence clause, avoiding a circular ratio-invariance argument.

The theorem does not prove convergence, uniqueness of an equilibrium, or independence of a limiting state. As p approaches 1 from below the geometric persistence constant can tend to zero; there is no uniform passage to the critical case. Constants also deteriorate as separation or boundary distance tends to zero. Zero coordinates, coincident sites, boundary sites, n=1, and p>=1 remain outside this persistence theorem. Collinear distinct sites and equal positive weights are allowed by the analytic proof.

## Exact witness, degeneracies, and finite checks

Independent rational arithmetic recovers squared distances `557/1800`, `137/400`, `49/144`, determinant `343/1200`, h=1/16, K=1/64, lower bound 1/4096 and upper bound 2047/2048. Every initial coordinate exceeds the lower constant. The all-time statement follows from the proof, not a finite grid.

`exact_checks.py`, run normally and under -O, adds a general sparse-polynomial identity check and 1,836 exact actual-influence comparisons per mode. Supporting configurations include the original triangle, a two-site case attaining geometric separation equality with the unscaled square touching the domain boundary, a collinear three-site case, and five sites with one competitor holding nearly all remaining mass. Exponent ratios q=1/3,1/4,1/8 and tiny positive states are checked exactly. Scalar exponent arithmetic also includes p=1/1000000 and p=999999/1000000. These are explicitly bounded diagnostics. They do not establish the universal geometric inclusion or replace the differential inequality.

The exact theorem covers all distinct interior configurations and all positive starts; it therefore supplies an open class of counterexamples relative to the source's data domain. An ordinary general-position condition that removes lower-dimensional or measure-zero exceptional configurations cannot eliminate that class. The rational triangle's scalene/noncollinear properties are illustrative and are not used to assert a complete formal definition of general position.

## Priority and source transfer audit

Aurenhammer–Edelsbrunner, printed pp.251–252, define the exact multiplicatively weighted distance and its regions, explain weight-ratio dependence, and give Apollonius disks and line degeneracy. The current note credits these static geometric facts. Aldous's 2007 Lemma 3 uses the exponent 2alpha/beta, and the unfinished Proposition 30 discussion already inscribes a protected neighborhood and obtains a lower growth power with that exponent under additional stochastic/environmental conditions. The present note does not claim those ideas or the Bernoulli/integrating-factor step are new. Their use in a uniform normalized finite-system inequality is the actual finite theorem being checked.

I independently read Ferudun's §4 pp.6–9 and §8 p.13, including the every-exponent derivative lemma and position-continuity estimate. The explicit open-interval counterexamples for 1<=p<sqrt(3) are genuinely about this same deterministic map when applied in §8. The positive-beta root yields `z'=f_x(z)-z` exactly, without a clock change. More strongly, the proved derivative formula holds for every p>0; for a=1/4 its slope is 7p/12. For 0<p<1 the derivative of f-z at one half is strictly negative. Differentiability gives inward signs at two nearby endpoints; reflection gives the opposite endpoint sign, and Lemma 4.3 preserves strict signs under small site perturbations. Hence those proved lemmas already imply a qualitative open-basin two-city counterexample in the candidate's regime. Calling the proposed quantitative strip extension a sketch would not erase that proved qualitative implication. The current note, README, priority text, and metadata all credit this stronger overlap correctly.

The direct primary web page and its metadata were freshly opened during this review. They currently assert version 1.0, an online/manuscript date of 14 October 2026, unrefereed status, the advertised DOI, and PDF SHA256 `319a8f49e0c4de0247e76da33f6476d4085e21267002ee02484f73cee6992e5a`, matching the inspected local PDF. These are current primary assertions, not an independent archival-time or firstness certificate. [Current primary page](https://eulersolve.org/papers/amr-096-0023/), [current metadata](https://eulersolve.org/papers/amr-096-0023/metadata.json?v=a7220c38084f).

After my independent memo and source reading, I checked both existing priority-family reports and their explicit transfer distinctions. They acknowledge classical permanence boundary-hypothesis gaps, soft-to-hard allocation/continuum-limit gaps, moving-site power-cell differences, and clipped discrete tree-growth differences. Those bounded searches did not identify a ready all-n, all-positive-start quantitative theorem. Their inaccessible-source and discovery-service limitations remain stated. I did not independently rerun their entire search campaign, inspect every general-framework primary text, or audit Ferudun's stochastic theorems. No worldwide novelty, firstness, or present-openness inference follows. The current narrative is appropriately limited even though original frozen negative-search observations remain present as dated historical artifacts. The current notices explicitly supersede those observations.

The recorded PR creation/commit chronology supports an original 6 October repository record, but neither timestamps nor the other paper's claimed release date establishes independent discovery or global priority. No such claim is made. The note's title and abstracts describe a specific theorem rather than a complete solution of the city-growth problem.

## Whole-package consistency, trust, and actual replay

Before any supplied-script execution, I independently authenticated the externally supplied outer wrapper, index, verifier, checker and builder digests. I personally read the complete active execution chain, including the original author checker, independent audit checker and optional source checker. The current wrapper never executes the historical root wrapper. Candidate data and child startup bytes are authenticated before copying into fresh relocated directories; child commands use isolated, no-site, no-bytecode Python. Fixed-pin consistency is not confused with pre-execution trust: the external startup authentication remains mandatory.

Independent inventory enumeration confirms 215 outer files and 161 portable members, with no extra files, every declared byte count and digest matching, and no aliases. All eleven core files match their seal. The ZIP's independently read members match the portable files exactly. The current wrapper additionally validates sorted member names, ordinary regular-file metadata, fixed timestamps, central/local boundaries, lack of prefix/trailer/gaps, and expected payload size before bounded reads. Those checks constrain representation boundaries; they do not prove a unique compressed DEFLATE bitstream for all runtimes.

Fresh executions actually run for this review were:

| Execution | Observed result |
| --- | --- |
| Real sealed outer `--full`, normal Python | PASS, 215 outer / 11 core / 161 portable, 8 finite receipts, source replay NOT_RUN |
| Real sealed outer `--full`, optimized Python | PASS, same counts and 8 finite receipts, source replay NOT_RUN |
| Real sealed outer `--full` with three complete corpora and both PDFs | PASS, normal outer, 10 receipts; source checker runs normal and optimized |
| Builder from the real sealed portable tree into a fresh reviewer output, normal | PASS; archive bytes identical to sealed ZIP |
| Same fresh build under optimized Python | PASS; archive bytes identical to sealed ZIP |
| New independent guards, normal and optimized | PASS per mode: 31 intended rejections, 5 positive controls |
| New exact algebra/boundary diagnostics, normal and optimized | PASS per mode; zero symbolic residual, exact witness, 1,836 influence diagnostics |

The builds report Python 3.14.6 and zlib runtime 1.2.12. Same-runtime compressed-byte reproducibility was verified; no cross-runtime compressed-byte claim is tested or accepted. The optional full-input path uses authenticated ordinary-file hardlinks, and the inspected legacy source checker only reads them. No large corpus copies were made. Input paths are all-or-none; the explicit 2012 PDF override correctly maps its local basename. Source-free replay truthfully leaves provenance NOT_RUN. Authentication with verify-only would not be counted as child replay.

The new negative controls cover duplicate/nonfinite/overflow JSON, unsafe relative paths, boolean sizes, duplicate and parent/child inventory collisions, leaf symlinks, a FIFO, wrong byte count, extra file and empty directory, internal directory alias, wrong external index pin, complete-source leaf alias, ZIP prefix/trailer/truncation/huge declared size, preprint/inner divergence, canonical metadata divergence, wrong deposit filename, and invalid CLI source-option combinations. Helper-level archive/copy tests are identified as such; actual CLI option guards and full real-tree replays are separate observations. No hostile concurrent-filesystem attack or cryptographic implementation audit is claimed.

I did not reassert the historical 106 rejection tests. Historical receipts, family decisions, earlier fixture probes and original wrappers remain authenticated historical evidence, not automatically fresh execution events. The review's test code and outputs enumerate its own actual work.

## Complete packaged-code static coverage

A new internal static-only reviewer read every packaged Python body and the full TeX source, without importing or executing inherited code. I inspected its authored report and coverage evidence. `STATIC_CODE_REVIEW.md` and `STATIC_CODE_COVERAGE.json` record all 19 unique Python bodies, 23 physical paths, 4,015 unique source lines, all 192 TeX lines, and six recursively archived Python occurrences that duplicate inspected flat files. Its own independently pinned index/member check matched all 160 payload rows and the exact 161-file tree. All active-chain code had also been personally read before my real replay. This new static review is separate from old packaged tooling verdicts.

No unexpected network, external outreach, opaque execution, or source/corpus mutation mechanism was found in the active chain. The only socket use in ancillary code creates a local Unix-domain socket as a nonregular-file fixture and never communicates. Ancillary audit/diagnostic scripts can write their own results, several perform work on import, and older optional provenance paths depend on the original repository/private inputs. Some historical harnesses require checking their JSON success field in addition to process exit status. Those scripts were not freshly executed here and are not children of current `--full`. Reproducing them directly inside the sealed tree could change its seal; the safe report explicitly distinguishes their direct-run behavior from the supported current verification interface. None is represented as a fresh dynamic result or a mathematical certificate. These preserved historical/ancillary limits do not create a gap in the current, explicitly scoped replay.

## PDF, metadata, archive privacy, and publication boundaries

All five rendered page PNGs match the exact `ROOT_PDF_QA.json` pins; the current source/PDF hashes match that QA record and the seal. I visually read every complete page. Text, displays, inequality signs, theorem flow, footnote disclosure, references, URLs and page numbers are legible. No clipping, overlapping content, unresolved citations, missing characters, or actionable layout defect was observed. I reused the verified stable render and did not regenerate the PDF or execute an authoring marker.

The title, date, version, author ORCID, result scope and caveats agree among PDF/source, current metadata, portable metadata, current root publication record, README, priority note and deposit metadata. The deposit binds exactly `output/pdf/note.pdf` as `city-ode-persistence-note.pdf` and `verification.zip` as `city-ode-persistence-verification.zip`. The current root explicitly says the package awaits independent whole-package reviews; it does not falsely claim those later events or release already happened. Original unchanged artifacts are clearly separated as historical. The all-time versus initial-independent asymptotic bounds are consistently distinguished.

The archive inventory and all nested original archives were inspected without extraction. The only PDF payload is the authored current note. Complete source PDFs, extracted primary text, page images, raw complete corpora, target-record dumps and private review files are absent. The accompanying source/version/pin locators and authored summaries are appropriate evidence. Public attribution/author identifiers are not private credentials. My review's own public allowlist excludes itself and everything under `private/`, including renders, rebuilt ZIPs, and internal static-review working files.

No Git branch, index or worktree operation, candidate edit, PR mutation, release, Zenodo mutation, sheet change, or communication with another individual was performed by this review. Internal code-inspection delegation was confined to this review and is not external outreach.

## Remaining limits

There is no identified actionable mathematical, source-scope, credit, artifact, metadata, layout or active-tooling gap in this seal. Open research questions and assurance limits remain exactly those stated above: no convergence or stochastic conclusion, no closed-boundary uniqueness theorem, no p>=1 persistence result, no formal proof-assistant verification, no external human refereeing, no exhaustive priority certificate, no reconstruction of historical 106 controls, no full independent rerun of all old search/test campaigns, and no hostile concurrent-filesystem sandbox guarantee. Optional complete-input outer replay under -O was not separately run; its source checker did run under both modes, and the source-free outer replay and both builders ran in both modes.

Completion estimate: 100% of this bounded whole-package review. Original proof-search effort remains 2/5. The research problem's broader phase classification remains outside this review.
