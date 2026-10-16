# Complete package review 05 — frozen candidate v5

**Verdict: PASS — no substantive mathematical, priority, implementation, reproduction, metadata or layout concern identified in frozen candidate v5. No required repair.** The complete original target and full package were reviewed. The cited-theorem, formal-build and novelty limits below remain explicit; this is an automated adversarial evidence artifact, not proof substitution.

## Reviewed target, independence and custody

I read the original USER_REQUEST.txt and /Users/alec/Documents/Math/AGENTS.md first. This is a full review of the original rational hafnian FPRAS/sampling targets, not a title-only recheck. I reconstructed the current manuscript, both detailed proofs, exact gadget implementation and sampler before reading underlying package audit reports or earlier complete-review reports, and saved INDEPENDENT_RECONSTRUCTION.md. The current candidate README/metadata were read alongside the manuscript as objects under review, including their audit claims; those claims were treated as hypotheses, not certificates. The prior reports were read later only to check that known concerns had been addressed.

A separate primary reviewer received the original target and pin before those candidate reads, reconstructed the pivotal upstream proof and actual Lean semantics, saved its own findings before candidate comparison, and sealed its report. The first priority subreview saved direct primary findings before candidate comparison, but candidly disclosed an earlier agent inventory call exposing brief old Cai/title status summaries. Its evidence is retained, with that limit. A replacement priority reviewer was spawned with fork_turns=none, expressly prohibited status inventories/prior reports, and given original instructions and actual primary files only before comparison. The replacement saved its own primary findings at 2026-10-07T06:34:17.041600+00:00 before candidate exposure and sealed PASS at 06:38:31.587619+00:00. Its primary-only source reconstruction, rather than the exposed status summary, determines the final priority finding.

All writes were confined to package_review_05/ and the final PACKAGE_REVIEW_05.md. The original /Users/alec/Desktop/math clone was read only. No external individual communication, Git mutation, publication, tracker update, dependency installation or large rebuild occurred. Third-party reading material is confined to ignored primary_reading/ or pinned_lean/ directories.

Every actual upload file and manifest was hashed and matched preserved candidate_v5 bytes. The ZIP has exactly 29 unique internal members; every one was read and hashed. All 28 declared payload hashes match CANDIDATE_IDENTITY, the extracted bytes and current authored sources. The working manuscript PDF also equals the uploaded PDF. Initial and final custody receipts identify exactly what was reviewed; any later material candidate change requires renewed review.

## Exact mathematical reconstruction

The strongest unconditional result is a polynomial-bit exact reduction from any explicitly encoded even-order symmetric matrix with nonnegative binary rational off-diagonal entries to a finite simple graph H and positive integer D, with #PM(H)=D^m haf(A). Its complete matching fibers have size D^m product(A_e). The approximation and sampling results are valid consequences using the cited general-simple-graph unweighted FPRAS. They do not independently establish that breakthrough, formalize this weighted follow-on, extend to signed/complex inputs, or imply unrestricted Gaussian boson sampling.

The binary DAG starts with one source-sink arc. Each subsequent bit adds two fresh vertices: every previous path gets exactly two extensions, and bit one adds precisely one direct source-sink path. All arcs follow creation order. In the split graph, using an incoming arc at an internal vertex forces an outgoing arc, and conversely; selected arcs comprise a source-sink path plus possible directed cycles. Acyclicity excludes every hidden cycle. With both terminals removed the same reasoning allows only identity edges, uniquely. Removing one terminal leaves odd order. Thus the signature is exactly (W,1,0,0), including W=1, with 4 bits(W)-2 vertices and at most 6 bits(W)-5 edges.

Each glued gadget has even interior, all covered inside that gadget. Its restriction therefore covers zero or two original endpoints. Since each original vertex is covered once, the active gadgets form a perfect matching of the original support. Fresh interiors, unique original pairs and unique edge ownership prevent loops, parallel edges and ambiguous fibers. Conversely, chosen full gadget matchings and inactive identity matchings concatenate independently and reversibly. Mixed terminal orientations do not require the whole expanded graph to remain bipartite; the external theorem accepts general simple graphs.

Taking D as the product of positive-support denominators and W_e=p_e(D/q_e) makes each integer weight O(L) bits. Summed gadget lengths are O(L²), graph labels add O(log(L+2)), and D^m has O(mL+1) bits. Products, exact divisions, normalization, exponentiation and graph construction have polynomial operand lengths and bit costs. No step enumerates W copies. Empty input has hafnian one; zero weights are deleted; support feasibility decides zero exactly. Disconnected support, odd components, weights below one, large denominators, ignored diagonals and arbitrarily tiny positives are covered. On a positive input haf(A)>=D^-m.

The cited FPRAS returns nonnegative rational estimates on every tape and certain zero only when the true count is zero. Exact support feasibility supplies the stronger requested zero decision. On a feasible expanded graph C>=1, a successful relative estimate cannot be zero for epsilon<1; replacing a failed zero by one changes no successful event. Division by D^m preserves relative error. Calling with min(delta,1/4) covers rational delta<1 despite the base theorem's delta<1/2 range. Every-tape runtime bounds output length even on failures, so scaling is polynomial bit time.

The sampler tests every child exactly and stores witnesses; zero children are discarded, and every selected child is feasible. Forced branches are exact. All-zero estimates return the stored current witness; arbitrary nonnegative failed estimates still select a feasible branch. Ordinary steps remove two vertices; fallback terminates immediately. For expanded order 2s, at most s² count calls and s²+1 witness calls occur. Parameters are alpha=eta/(4s), gamma=eta/(4s²), and R=2^b>=4s²/eta; additional draw bits are at most sb.

At every full past adaptive history, fresh call randomness gives current failure mass <=j gamma. Successful normalization has TV<=alpha/(1-alpha); cumulative dyadic floors have TV<(j-1)/R. Integrating arbitrary failure mass directly avoids conditioning the final law on global success. Coupling until first disagreement and summing the per-history bounds gives s alpha/(1-alpha)+s² gamma+s²/R<5eta/6<eta. The ideal child-count recursion telescopes to the uniform matching law. Fixed-bit draws have no rejection loop; exact rational sums/CDFs/floors remain polynomial because failed output lengths are also bounded by the oracle's worst-case bit time. Fiber weights give exactly the normalized rational law under projection, and deterministic projection contracts TV. No exact/pointwise-relative sampling or time polynomial in log(eta^-1) is claimed.

## Pivotal external proof and actual formal semantics

The fresh upstream primary reviewer read the pinned 3,471-line manuscript and actual 45-page PDF theorem/proof text, source README/citation metadata and relevant entropy companion sources. Its reconstruction checked logical-hole injections/relocation/bootstrap, odd subdivision and deleted-hole accounting, virtual-edge inflation, fixed-label cells, the signed identity, legal two-matching demand repairs/inverses, rare-guide cancellation, additive energy, replicated-tier ANOVA residual assignment, unit-activity dynamic programming, mixing, adaptive balance restoration, statistical failures and every-tape finite-bit arithmetic. No central difficulty was transferred to an unsupported count or mixing oracle, and no material gap or circular inference was found.

Important attack points include the nonzero whole-cycle contribution of complementary arc gains, preservation of fixed original labels through recursion, cancellation of rare-guide probability without a hidden lower bound, uniquely assigned penultimate/last ANOVA coordinates, Metropolis comparison between unequal tiers, convolution rather than exponential interface tuples, and unconditional clipping/bit bounds on failed histories. The independent primary script passed 10,971 cycles, 56,148 cells and 82,458 legal/canonical encodings, including signed identities and guide persistence. These are finite falsification attempts, not certification of the full FPRAS.

I read actual Main.lean and Model.lean directly. OAI.MatchingFPRAS.thm_main has type MainStatement and assembles the actual LiteralPhysical machine runtime, output and success lemmas. Model quantifies one fixed finite-alphabet machine and polynomial constants before all finite simple graphs and rational epsilon/delta inputs. Its graph edges are a set of strictly increasing endpoint pairs, its count is ordinary perfect-matchings cardinality, its execution is a fold of physical tape ticks, all bounded fair tapes halt with nonnegative encoded rational outputs, and at least a 1-delta fraction give relative accuracy. Its zero clause is one-way and its endpoint is counting. The independently inspected execution/probability/cost bridges do not assume an FPRAS as a field or substitute a zero-time counting oracle.

The exact optional inspector reproduced 415 local modules, 3,091,883 bytes, and 425 source/metadata hashes, with zero pin mismatches. Its actual Main/Model match the comparator definition interface. No listed lexical proof-hole/escape tokens were found, but lexical scans are not elaboration or compiled axiom closure checks. Both the documented inspector's actual-Main probe and a separate actual-Model probe stop at missing Mathlib under installed Lean4.34.1. No successful full kernel build, #print axioms or comparator run is claimed. The candidate clearly discloses this, and does not claim the weighted follow-on is formalized. The comparator stub or configured permitted axioms were not treated as verification.

All 26 available source-manifest primary files match the reference hashes and exact pinned Git objects; all 425 fresh inspector hashes match the archived original receipt. The historical upstream-selected.tar is no longer locally present; its recorded hash is a capture identity, not independently reread TAR bytes. This causes no missing candidate payload or source-reconstruction gap because the actual pinned files were checked individually. Read-only source refresh still identifies the pin; no correction was silently substituted.

The entropy companion's weighted variational bracket and binary-multiplicity deterministic 512^n-factor estimate are distinct from a relative FPRAS and weighted normalized-law sampler. The source main has its own complete unweighted deletion sampler, while the follow-on independently specifies a vertex-partner self-reduction; no internal weighted sampler is mistaken for the requested theorem.

## Priority and attribution gate

The replacement primary-only reviewer directly inspected McQuillan1301.2880v1 §7.2 displayed Lemmas25–27 (binary nonnegative rational input and exact simple-graph reduction), Dell2010/ECCC original and expanded2012 actual Fig3 (logarithmic path removal), Cai–Liu1904.10493v1's precise McQuillan Proposition5 citation, and JVV1986 §6/Theorem6.3. Those are affirmative prior-art statements, not keyword-absence inferences. Dell's directed paths/identity loops translate to matching arcs/identities; the requested Horner form can be a reversal/reorientation of that mechanism. No distinct gadget novelty is supported. The candidate calls it classical machinery/a presentation variant and credits the reduction and sampling framework.

The exact mandatory/current restricted statements were independently inspected: RSZ1409.3905v1/v2 requires dense degree/strong expansion or stochastic large-variance conditions and gives subexponential multiplicative errors; Barvinok1601.07518v1/v5 requires a fixed positive lower bound and quasipolynomial time; Yi2609.04079v1 requires fixed weight bounds and dense support, with fixed-parameter polynomial time. Current version histories and main/source paths were refreshed. Source public priority is distinguished from manuscript dates: September23 is the upstream manuscript label, while public repository release is evidenced October6. Supplied corporate OpenAI author/title/year and manuscript-specific citations are preserved. The independently saved primary record initially confused TeX labels with displayed McQuillan/Barvinok numbers; actual PDFs were checked, the errors candidly corrected, and the candidate's displayed references confirmed correct.

The strongest justified contribution is the attributed consequence, explicit implementation, bit/TV analysis, boundaries and reproducibility artifacts. The weighted complexity conclusion was already implicit once the cited unweighted theorem became available; no separate unresolved classification is established here. No exact duplicate of the entire current note/artifact package was identified in bounded direct-primary searches. That observation does not establish universal absence or firstness. The current manuscript/README/metadata expressly deny a new reduction, first solution, independent base breakthrough or new complexity classification. Thus the user's no-duplicate-as-new-solution gate is respected by the actual consequence/exposition framing. A later discovered identical note or source correction must reopen the gate.

## Complete package, exact commands and PDF

All authored archive prose, proofs, code, data, audits, source-reference identities, licenses and structured receipts were read or parsed; mathematical outputs were regenerated and reconciled. The Python exact counters are correctly labeled exponential reference tools. The sampler requires supplied polynomial counting and witness oracles; no practical base FPRAS implementation or benchmark is included. Newly authored prose/data are CC BY4.0, code MIT; the archive excludes third-party manuscripts/proof trees, runtimes and credentials. Author Alec Kriebel, ORCID0009-0001-9320-500X and October6 date are consistent, with no invented affiliation/coauthor. Extensive AI use and absence of conventional human peer review are disclosed.

In the clean extracted ROOT I ran the exact README main command twice, the second run after unlisted optional source files had been generated:

```
python3 reproduce.py --output reproduction-receipt.json
```

Both passed all three checks. Mathematical data agree exactly with archived data apart from volatile timestamp/runtime/software-version fields: 64 signatures, 729 K4 assignments, 40 seeded K6 instances, 12 boundaries and three full fibers; 203 sampler graphs, 1827 law integrations, 1218 imperative runs, 243 all-zero fallbacks and 15 weighted pushforward scenarios; and the saved upstream cell table.

I ran the exact optional static inspection with the real pinned source replacing the placeholder:

```
python3 research/lean_source_inspection/audit_sources.py --source /Users/alec/Desktop/math/lean
```

It returned successfully; its bounded dependency probe failed as explicitly reported above. It writes only copied sources/new unlisted report beside itself and preserves the original archived receipt. The repeated main reproduction excludes those unlisted files. All 28 original payload bytes and the manifest remain intact. Six bounded receipt boundary checks reject payload, manifest, hardlink alias, symlink alias, nonexistent parent and directory paths without modifying protected bytes.

After creating rebuilt/, I ran:

```
tectonic --outdir rebuilt main.tex
```

Tectonic0.16.9 passed with only two underfull paragraph-box warnings. Python is3.14.6 and Poppler26.08.0. All six deposited pages were rendered and visually inspected: title, formulas, bounds, glyphs, citations, margins, page numbers and references are legible without clipping, overlap or unresolved references. The displayed title includes Nonnegative, and PDF title metadata agrees verbatim with TeX, README and Zenodo. The PDF has no encryption/JavaScript. Rebuilt extracted text and every one of the six 110dpi raster images are byte-identical to the deposit; PDF creation metadata can differ.

Own additional motivated finite attacks independently counted seven larger gadget signatures (65,66,85,127,128,129,255), every lift fiber of a rational nonbipartite K4, and malformed projection certificates. Four exact integrations of the actual imperative K4 sampler allowed zero, 256-bit huge, 256-bit tiny and mixed failed estimates, with endpoint successful errors; all remain within the theoretical TV and call/bit caps. A 4096-bit tiny/huge categorical example preserves internal zero masses and the fixed-grid TV budget. These tests are support for the proof, not universal guarantees or substitutes for primary validation.

## Evidence and limits

Primary evidence is in INDEPENDENT_RECONSTRUCTION.md, INITIAL_CUSTODY.json, COVERAGE_AND_READ_HASHES.json, CLAIM_CROSSCHECK.json, SOURCE_REFERENCE_CROSSCHECK.json, independent_attacks.py / INDEPENDENT_ATTACKS.json, REPRODUCTION_AND_PDF_QA.json, FIRST_REPRODUCTION_RECEIPT.json, extracted/reproduction-receipt.json and the sealed independent primary reports. DELIVERY_RECEIPT.json identifies report hashes and frozen candidate custody. The final independent gates are upstream_primary/REPORT.md + FINAL_RECEIPT.json and priority_fresh/REPORT.md + SEAL_SHA256.json; all referenced sealed artifact hashes were checked. The original exposed-status priority evidence remains separately sealed and explicitly superseded for the gate.

This automated adversarial review is evidence, not proof replacement, a successful kernel certificate, conventional human refereeing, or a universal novelty-absence certificate. It covers the exact frozen v5 note under its stated nonnegative rational and inherited-consequence scope. Any material revision after the final seal requires another fresh complete-package review.


## Final exact custody

Seal time: 2026-10-07T06:39:41.257943+00:00. Actual upload/manifest/identity bytes remained unchanged from the initial reads and match preserved candidate_v5. All 29 ZIP members, CRCs, 28 payload hashes and current-source correspondences were verified again at sealing.

| Reviewed file | Bytes | SHA-256 |
|---|---:|---|
| `publication/CANDIDATE_IDENTITY.json` | 3539 | `348fe001e2d79d3734e07eb9a9ed1904e3eea5304713a4776f8d14b80ef8b388` |
| `zenodo-deposit.json` | 2971 | `2fe834bdf2e5de74a92f7b9463fdc6917717c7e37ccf7ca58c9670065f3efa7d` |
| `publication/zenodo-upload-kit/paper.pdf` | 75751 | `8c93b0f14bc4fd935dbc3a489c5ecca63a8262ba4560a09822b7f65e1036bee7` |
| `publication/zenodo-upload-kit/source-and-verification.zip` | 183748 | `e79ba53de7b0d937189271d5941ee77eb8e1f10212fef33aa3bb4c4311c666fa` |
| `publication/zenodo-upload-kit/README.md` | 6238 | `a272e4bc9b525d60a9adfe3ba3a113e8c46c53f246ccd01f16b77eb8958cc1cd` |

Review completion estimate: 100% of the assigned mathematical and complete-package review scope. This is coverage, not a correctness/novelty probability or an estimate of completed production publication. No publication/tracker action occurred.
