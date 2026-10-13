# Complete independent package review 04 — frozen candidate v4

**Verdict: REQUIRED REPAIRS.** One required publication-scope repair: add **Nonnegative** to the title and propagate it through the rendered PDF, PDF title metadata, publication README and Zenodo metadata. I found no additional substantive mathematical, priority, implementation or reproduction defect in the full v4 audit. This is not publication clearance for changed candidate bytes; a fresh complete review must follow the repair.

## Required repair and exact basis

The current title is “Binary rational hafnians: an exact reduction and approximation and sampling consequences.” Binary rational entries can have either sign, while all proved conclusions require nonnegative off-diagonal entries. The original USER_REQUEST.txt §4 expressly requires the resolved scope to be unmistakable **in the title**, abstract, introduction and conclusions. The abstract, hypotheses and limitations already say nonnegative; the title does not. This is a scope-wording and instruction-compliance correction, not a counterexample to the stated lemmas or a discovered upstream proof failure. A suitable repaired title is “Nonnegative binary rational hafnians: an exact reduction and approximation and sampling consequences.” Update the source title, hypersetup pdftitle, exported PDF, source archive's main.tex/paper.pdf/README, kit README, Zenodo title, relevant project heading and new identity hashes. Preserve the exact old candidate and this review; do not edit the reviewed v4 snapshot. Re-render the repaired PDF and renew complete-package review.

Fresh upstream and priority final reports are complete and reconcile with this verdict. No other required repair was identified. In particular, the exact documented optional source-inspection command now works and leaves all declared payload bytes intact.

## Independence and scope

I read /Users/alec/Documents/Math/AGENTS.md and the full original research/USER_REQUEST.txt first. I reconstructed the gadget, gluing, binary arithmetic, FPRAS wrapper and adaptive sampler independently, and saved INDEPENDENT_RECONSTRUCTION.md before reading package audit conclusions. Two fresh internal reviewers independently reconstructed the actual pivotal upstream proof/formal scope and the primary-source priority record; each saved unprimed findings before comparing the candidate. I did not read previous complete-package favorable verdicts and did not use a prior review as evidence. The title issue was also raised by the root researcher and independently assessed against the original instruction.

Work was confined to this review's directory and the final report. The original upstream clone was read only. There was no external individual communication, publication, dependency installation, branch/index/commit/push mutation, or change to reviewed bytes. Internal AI tools are research tools, not human referees.

Complete reviewed scope: original targets and requested boundaries; manuscript's full main.tex and actual six-page PDF; both detailed proofs; every authored archive code, data, audit, reference, license, manifest and metadata member; all intended upload payloads and exact preserved v4 bytes; source correspondences; original primary-source theorem and pivotal proof; actual Lean Main and Model, source bridge declarations and closure checks; primary literature/version/citation statements; exact clean reproduction and optional commands. Full structured receipts were parsed and their identities checked; I do not claim to have semantically checked every proof line of all 415 imported Lean files.

## Strongest mathematical finding

The exact reduction is unconditional: every explicitly encoded even-order symmetric matrix with binary nonnegative rational off-diagonal entries maps in polynomial bit time to a finite simple graph H and positive integer D with #PM(H)=D^m haf(A). Fibers have exactly D^m product(A_e) lifts. The approximation and sampling conclusions are sound consequences **using the cited unweighted general-graph FPRAS**. They do not independently establish or formalize that breakthrough, cover signed/complex hafnians, or assert an unrestricted Gaussian-boson-sampling consequence.

### Gadget and global matching reconstruction

Starting with s→t, each new bit creates exactly two extensions of each prior path and precisely one extra direct path for bit one. Creation order with a before z makes every arc forward. Full split-graph matchings use a source-to-sink path plus off-path identity edges; any other selected arc component would be a directed cycle. Deleting both terminals similarly prohibits all arc components. One-terminal deletion has odd order. Hence the four signatures are (W,1,0,0), including W=1, with 4 bits(W)−2 vertices and at most 6 bits(W)−5 edges.

Fresh internal vertices and a unique original pair for each gadget exclude loops, parallel edges and ambiguous ownership. In a global matching all internal vertices of a gadget are covered within it; the number of covered original endpoints has even parity and is 0 or 2. The selected gadgets therefore form an original perfect matching. Local choices concatenate independently and reversibly, giving the complete fiber product. This remains valid under mixed terminal orientations; the global graph need not remain bipartite, and the cited theorem covers general simple graphs.

Taking D as the product of positive-support denominators gives O(L) bit length, each W_e=p_e(D/q_e) has O(L) bits, and summed gadget lengths are O(L²). Graph labels add only a logarithmic factor. D^m has O(mL+1) bits, and all multiplication, exact division, normalization and graph construction costs are polynomial. No numerical W-fold expansion occurs. Empty input has hafnian one, deleted zero weights give exact support, disconnected positive or infeasible cases are covered, weights below one and large denominators require no new promise, and positive hafnians are at least D^(−m).

### Relative approximation and exact zero

Edmonds feasibility supplies exact support zero detection. On a feasible input, expanded count C≥1. A successful estimate cannot be zero because epsilon<1; replacing a failed zero estimate by 1 therefore preserves every success event and makes the output positive on every tape. Exact division by D^m preserves relative error. Calling the upstream theorem with min(delta,1/4) covers all requested rational 0<delta<1 while preserving the logarithmic confidence dependence. The cited theorem's every-execution bit bound, including output length on failures, is precisely the required input interface.

### Adaptive sampler reconstruction

At every residual graph exact witnesses discard only zero branches and guarantee at least one feasible child. Forced choices are exact. All-zero estimates return a stored witness, and arbitrary failed nonzero estimates still select a feasible child. Each normal step removes two vertices; fallback immediately finishes.

For every fixed full past adaptive history, fresh counting tapes give bad-current-call probability at most j gamma. On all-good current calls normalization contributes TV at most alpha/(1−alpha); fixed-floor categorical boundaries contribute less than (j−1)2^(−b). Integrating good/bad transitions avoids bias from conditioning the final output on global success. Coupling until first disagreement and summing over at most k stages and k² outcomes gives k alpha/(1−alpha)+k² gamma+k² 2^(−b)<5 eta/6<eta for the displayed parameters. Every random draw has exactly b bits; there is no rejection/convergence stopping time. Rational estimate lengths on failed executions are bounded by the oracle's worst-case bit time, so normalized CDF and integer-floor arithmetic remain polynomial. Uniform expanded matching projects exactly to the desired weighted law, and TV contracts under that deterministic projection. m=0 returns the empty matching; infeasibility is reported exactly. No exact, pointwise-relative, or polynomial-in-log(eta inverse) sampling guarantee is claimed.

## Pivotal upstream proof and Lean trust boundary

The fresh primary reviewer read the actual pinned manuscript and reconstructed its logical-hole/relocation/bootstrap bounds, odd subdivision and puncture accounting, capacity lifting/inflation, fixed-label quadrangulation, signed cell identity with context errors, repaired **two-perfect-matching** encoding, rare-guide cancellation, additive pair energy, replicated-product ANOVA residual assignment, unit-activity DP, spectral sampling, adaptive annealing/balance restoration, conditional statistical error and unsuccessful-history bit bounds. The actual proof is not a Broder near-perfect-chain or canonical-path-congestion proof. No unsupported transfer of the central difficulty was found.

Notable checks were the exact inverse in the four-hole/relocation injections, below-one cross-center puncture factors, admissibility of recursive exteriors, the nonzero whole-cycle contribution of complementary gains, canceled rare-guide probability without a hidden lower bound, uniquely assigned last-two-slot ANOVA residuals, Metropolis comparison at unequal tiers, convolution rather than exponential DP tuples, and clipped scale/encoding bounds on every failed history. Independent exact corroboration checked 96 four-hole cases, 52,380 punctured path cases, 182 signed identities and 5,027 ANOVA assignment cases. These finite checks support the source reasoning; they do not certify the FPRAS.

Actual solution OAI.MatchingFPRAS.thm_main in OAI/Combinatorics/MatchingCount/Main.lean has type MainStatement and a real proof assembling LiteralPhysical.mainTime_bound, mainProgram_outputs and mainProgram_success. Model.lean quantifies one fixed finite-state machine, all finite simple graphs, rational epsilon/delta, all bounded fair tapes, nonnegative encoded rational output on every tape, certain zero on zero-count inputs, and a good-tape fraction ≥1−delta. I read these actual files directly, not merely the comparator stub or scope document. This is the full unweighted theorem statement, but no follow-on formalization.

The optional source inspector reproduced 415 local modules, 3,091,883 bytes, and 425 source/metadata hashes with zero pin mismatches and no listed lexical escape/hole tokens. Exact source Main/Model agree with the comparator definitions at the stated interface. The successful script's dependency probe failed at missing Mathlib; it is not a kernel rebuild. No successful actual kernel/comparator run or compiled axiom closure check was obtained. The configured permitted axioms are not themselves an axiom audit receipt. The package accurately discloses this limitation and relies on a cited theorem independently scrutinized mathematically, not a falsely asserted kernel certificate.

The entropy companion supplies deterministic 512^n-factor binary-multiplicity approximation and weighted entropy/log-partition brackets. It does not provide the requested relative FPRAS or weighted TV sampler. The main manuscript's explicit unweighted deletion sampler is already applicable after a valid reduction; this package's separate vertex-partner self-reduction gives the required explicit bit/error interface independently.

## Priority, attribution and duplicate condition

Fresh primary searches and exact TeX/PDF inspections affirm that logarithmic integer removal is inherited from Dell–Husfeldt–Wahlén 2010 and expanded Dell et al. 2012/2014. McQuillan arXiv:1301.2880v1 §7.2 Lemmas25/27 explicitly gives binary nonnegative rational weighted-to-simple-unweighted equivalence. JVV1986 §6 Theorem6.3 supplies classical count-to-generation, explicitly including undirected 1-factors. The new unweighted approximation breakthrough belongs to OpenAI. The package accurately calls its weighted conclusion an already implicit consequence and claims no first priority, new reduction, independent base solution, or new complexity classification.

The cited restricted comparators were checked at exact versions: RSZ1409.3905v2 structural/expansion and subexponential multiplicative errors; Barvinok1601.07518v5 fixed positive interval and quasipolynomial zero-free interpolation; Yi2609.04079v1 fixed positive bounds and dense support. Exact rendered statements reconcile with the source-version notes. Barvinok's internal TeX label differs from printed theorem number, but the candidate's printed Theorem2.1 attribution is correct. Cai–Liu1904.10493v1 PDF and TeX both cite McQuillan Proposition5 after their Theorem1.2. An erroneous 1510 identifier appeared only in my initial delegation label and was corrected; it is not a candidate bibliography error.

The fresh upstream main-ref check still returns the exact pin. Manuscript label September23 is distinguished from evidenced public repository disclosure October6. Bibliography preserves supplied OpenAI author/title/year and manuscript-specific source reference metadata. No exact duplicate of the entire current Horner proof/finite-bit wrapper/reproducibility note was found, but bounded searches and indexing absence cannot prove universal absence or novelty. The core implication and main mechanisms are already public and are explicitly credited. On available positive evidence, the user's no-duplicate-as-new-solution rule is respected by the modest consequence/exposition framing; no distinct previously unresolved theorem is claimed.

## Complete package, reproduction, and visual checks

Every one of the 29 ZIP members was read/parsed and hashed, all 28 declared payload hashes verified, and all 28 authored sources matched their archive identities. Actual kit payloads, metadata and CANDIDATE_IDENTITY were identical to preserved reviews/candidate_v4 bytes. CRC validation passed; member paths are internal and the package contains authored material and source identities, not third-party manuscript/proof trees, credentials or runtimes. Author, ORCID, October6 date, rights statement, AI-use and absent conventional-human-review disclosure agree across source/PDF/README/metadata, apart from the required title scope wording.

Executed the exact current README command in a fresh extraction:

```
python3 reproduce.py --output reproduction-receipt.json
```

All three checks passed. They reproduce 64 gadget signatures, 729 K4 integer assignments, 40 seeded K6 instances, 12 boundaries, three fiber checks; 203 sampler graph instances, 1827 exact law integrations, 1218 imperative runs, 243 all-zero fallbacks and 15 weighted pushforward scenarios; and the saved upstream cell/repair table. Saved data claims reconcile with regenerated deterministic mathematical outputs; timestamps and elapsed time naturally differ. The exact counters are clearly identified as exponential test tools and the wrapper requires supplied polynomial oracles.

Executed the exact optional source inspection with the real pinned source in place of the README placeholder:

```
python3 research/lean_source_inspection/audit_sources.py --source /Users/alec/Desktop/math/lean
```

It returned successfully, copied source only beside itself into pinned_lean/, wrote unlisted static_audit.json, preserved the archived STATIC_AUDIT_RECEIPT.json, and matched all 425 original source/metadata hashes. Then the exact main command with a different receipt name passed again. All 28 original payload bytes remained unchanged. Five bounded receipt collision attacks (payload, manifest, hardlink alias, symlink alias, directory) were correctly rejected without changing payload. The script excludes unlisted extra files from its verified copy and isolates child Python executions as documented.

Created rebuilt/ and executed the exact optional PDF command:

```
tectonic --outdir rebuilt main.tex
```

Tectonic0.16.9 returned successfully with only two underfull paragraph-box warnings. Python was3.14.6; Poppler26.08.0. The deposited PDF has six pages, correct author/title metadata, no encryption or JavaScript. All six pages were rendered and visually inspected: formulas, bounds, symbols, citations, margins, page numbers and bibliography are legible, with no clipping, overlap, missing glyphs or unresolved references. The clean rebuilt PDF's extracted mathematical text and all six 110dpi raster images are identical to the deposited PDF. Byte inequality from PDF creation metadata is expected.

Own bounded additional falsification mechanisms, INDEPENDENT_ATTACKS.json: all1098 forward DAGs on2..5 vertices have the predicted general signature, including zero-path and disconnected off-path cases; a cyclic negative control correctly gives (2,2,0,0), confirming acyclicity is essential. All64 gluing orientations of a weighted K4 give identical predicted fibers. Eight exact adaptive symbolic sampler laws allow zero or 256-bit huge/tiny failed values and prefix-dependent successful errors, all within the theorem bound. All256 actual first-draw values of the imperative K4 sampler reproduce the independent categorical law, including a zero-estimate interval and tiny positive mass. These were bounded attacks on meaningful mechanisms, not large optional sweeps or proof replacements.

## Evidence and exact custody

Owned receipts and reconstructions under package_review_04/:

- INITIAL_CUSTODY.json and V4_CUSTODY_SEAL.json: actual read hashes, all ZIP members, original/frozen agreement and source correspondence.
- INDEPENDENT_RECONSTRUCTION.md: local proof reconstruction before package audit conclusions.
- independent_attacks.py and INDEPENDENT_ATTACKS.json: bounded independent code and exact finite results.
- REPRODUCTION_AND_PDF_QA.json: actual documented commands, preserved payload, optional source hash comparison, collision cases and six-page rebuild equality.
- COVERAGE_AND_READ_HASHES.json: full authored member coverage, direct primary-file hashes and software versions.
- extracted/reproduction-receipt.json and extracted/after-inspection-receipt.json: clean standard checks.
- upstream_primary/: independent primary findings, checked derivations/code, exact receipts and final comparison report.
- priority_primary/: independently saved primary findings, exact source/version receipts and final comparison report. Third-party snapshots are only local ignored primary_reading/ or pinned_lean/ material, not publication payload.

Custody seal time: 2026-10-07T06:13:28.745598+00:00. These were the latest exact candidate bytes when inspection ended and were unchanged from initial reads. Root was informed only after the seal that candidate repair/regeneration could begin. Any later candidate, including a title-only PDF/source/metadata revision, is outside this v4 verdict and requires fresh review.

| Reviewed file | Bytes | SHA-256 |
|---|---:|---|
| `publication/CANDIDATE_IDENTITY.json` | 3539 | `f82788010a6303ccbf691d52e488cfa4e1d02f034ff3b52602a226697e1cd44e` |
| `zenodo-deposit.json` | 2959 | `fbc5934f75f6edb72e2092e17a359295e94747932ea13dbd2652ebefc67d2d69` |
| `publication/zenodo-upload-kit/paper.pdf` | 75606 | `9e16fbfedfd1cb52a0ed8a1c3648bb06b1afffa4d9f4a1bfa596eb91330f3041` |
| `publication/zenodo-upload-kit/source-and-verification.zip` | 183590 | `3c8bb5709cf81b443ad0496cfb4d34341da22b40ba77c4a54bf4cf78a62ff6b3` |
| `publication/zenodo-upload-kit/README.md` | 6226 | `f7c16c0171ca4ea270844e972ad0d7a2d7ab3d38f7f0cd287521610c023025d6` |

This review found one required scope repair and no other substantive issue. It is an automated adversarial evidence artifact, not proof replacement, human peer review, a successful kernel certificate, or authorization to publish changed bytes.

Completed 2026-10-07T06:18:22.342287+00:00 (frozen-v4 review; later v5 bytes are explicitly outside this verdict).
