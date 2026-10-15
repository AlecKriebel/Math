# Independent complete-package adversarial review 03

Candidate: frozen **v3**. Date: 2026-10-07 UTC / 2026-10-06 America/Los_Angeles.

## Verdict

**REQUIRED REPAIRS.** The optional static-inspector invocation in the archived README is not executable as written. Add `python3` before its script path, propagate that correction to the intended README and archive, rebuild identities, rerun the exact documented commands, and commission a fresh complete-package review of the resulting candidate. No substantive mathematical, attribution, metadata, PDF, or primary finite-reproduction defect was found in this review. The upstream primary-source subreview is completing its written report; this draft is not the final custody seal.

### Required repair: literal optional command fails

The README's optional-inspection paragraph says to run

```text
research/lean_source_inspection/audit_sources.py --source /path/to/math/lean
```

The ZIP sets that member to mode 0644; the fresh extraction also has mode 0644. From the clean extraction, the same command with the actual read-only upstream path exits **126**, with `permission denied`. A shebang does not make a non-executable file executable. The corrected invocation is

```text
python3 research/lean_source_inspection/audit_sources.py --source /path/to/math/lean
```

Adding the optional `--lean` argument works with this interpreter prefix. I ran the explicit-Python version and reproduced the inspector's 415 modules, all source hashes, zero pinned mismatches, semantic definition comparison, and correctly failed dependency probe. This does not repair the frozen candidate: it demonstrates the specific documentation defect and a working correction. Evidence: `OPTIONAL_DOCUMENTATION_FAILURE.json` and `OPTIONAL_INSPECTOR_RECEIPT.json`. The main reproduction command already works exactly as printed.

## Exact reviewed identities and custody

The files actually read, hashed and tested were the current intended upload-kit files and project-local deposit manifest. They are byte-identical to the separately preserved `reviews/candidate_v3/` files.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `paper.pdf` | 75,606 | `9e16fbfedfd1cb52a0ed8a1c3648bb06b1afffa4d9f4a1bfa596eb91330f3041` |
| `source-and-verification.zip` | 183,584 | `b49a3eaacd7d89024d8b43e9a37b74c68b9f235d3b26ff8dd5c2540e85562b5e` |
| `README.md` | 6,218 | `6c715cdfb4f375ea6fe36490573b9282caa3af357e7616a35e5fee106340ab60` |
| `zenodo-deposit.json` | 2,959 | `fbc5934f75f6edb72e2092e17a359295e94747932ea13dbd2652ebefc67d2d69` |
| `CANDIDATE_IDENTITY.json` | 3,539 | `c4e4fa1ec9e85ff98d7dc5370cf3a78f1caa6f17f15cbc0d9028f5965e24603e` |

Every one of the 29 ZIP members passed CRC, safe-path/type checks, uniqueness checks and SHA-256 verification. Its 28 declared authored payload files agree exactly with `authored_payload` in the candidate identity and with the current working sources; the remaining member is their manifest. There is no undeclared member, third-party reading manuscript, source tree, runtime, cache or credential in the ZIP. The embedded paper equals the separate uploaded PDF; `main.tex` equals the current manuscript, SHA-256 `25a9b9e5df03ea50c24812f5107bf3913ab352296faf6d5170e0372c4be8b9f4`. See `READ_HASHES.json`, `ZIP_MEMBER_HASHES.json` and `CURRENT_SOURCE_IDENTITIES.json`.

All review writes stayed in `reviews/package_review_03/`, apart from the expressly requested final report. The upstream clone and frozen candidate were read only. No individual was contacted; no publication, Git mutation, or tracker update was performed by this reviewer. Third-party review reading files belong under `primary_reading/` and `priority_primary/**/primary_reading/`; exclude those directories from public evidence commits and upload payloads.

## Independent mathematical reconstruction

I read AGENTS.md and the complete original USER_REQUEST first, then the complete current manuscript and both supplemental proofs. I saved `INDEPENDENT_RECONSTRUCTION.md` before reading package audit conclusions; I did not use earlier complete-package verdicts. Distinct independent subreviewers separately read the primary upstream proof and priority sources without prior review conclusions.

**Target alignment.** The note treats every explicitly encoded symmetric even-order nonnegative rational off-diagonal input, with no connectivity, density, denominator-size or positive-weight floor. It gives exact zero detection and the order-zero convention, relative epsilon approximation with logarithmic confidence dependence, and a sampler within eta TV whose output is always feasible and whose time is polynomial in full input and eta inverse. Rational requested accuracies express the finite input model. It does not import a stronger pointwise sampling, exact sampling, log-eta running time, signed/complex hafnian or unrestricted boson-sampling conclusion.

**Local signature.** Horner recurrence `w -> 2w+b` gives precisely W source-sink paths. The construction creates only forward arcs and fresh intermediate vertices. In a full split-vertex matching, each internal vertex either uses its identity edge or has one incoming and one outgoing arc. The selected components are a single terminal path plus possible cycles; acyclicity eliminates those hidden cycles. With both terminals removed every selected arc component would be cyclic, so only all identities remain. One removed terminal gives odd order. This proves `(W,1,0,0)`, including W=1 and the empty residual. The asserted `4 bits(W)-2` vertices and at most `6 bits(W)-5` edges follow directly.

**Global fibers.** Every gadget's even number of internal vertices is covered within that gadget. Its matching restriction therefore covers either zero or both original endpoints, not one. Since each original vertex is covered once, full gadgets form a support perfect matching. Their independent choices, and the unique inactive restrictions, give a bijection whose fiber is the product of integer weights. Edge ownership remains unique even when a direct terminal edge is present. Arbitrary original orientation does not require the global graph to be bipartite; it remains simple.

**Rational/bit bounds.** Product denominators D and each `p_e(D/q_e)` have O(L) bits. At most O(L) support edges yield O(L^2) graph order/size and O(L^2 log(L+2)) explicit encoding. `D^m` has O(mL+1) bits and scales every fiber because every original matching has exactly m edges. Construction and rational scaling use polynomial operand lengths, never W copies. Extremely small positive hafnians are at least `D^-m`. Exact support feasibility detects zero. On a feasible input replacing only a failed zero unweighted estimate by 1 does not alter any successful relative estimate and guarantees positive output on every tape.

**Sampling/failure arithmetic.** Exact child witnesses remove zero branches and make all possible outputs feasible even on failed estimates. Successful count normalization has TV at most `alpha/(1-alpha)`; cumulative floor rounding costs at most `j 2^-b`. Fresh tapes after any adaptive history permit the unconditional `j gamma` failure charge. Coupling until histories first differ and summing at most k stages and k^2 outcomes/calls gives

```text
k alpha/(1-alpha) + k^2 gamma + k^2 2^-b < 5 eta/6 < eta.
```

This does not condition the final output on all estimates succeeding. Failed estimates may be zero, very large, or tiny positive rationals: only nonnegativity and the upstream every-execution output-length/time bound are used. Fixed-bit draws have no rejection loop, all-zero fallback terminates with a stored witness, and exact normalization/floor arithmetic has polynomial length. The uniform matching law pushes forward to the desired product-weight law by exact fibers; TV contracts under that projection.

No central difficulty has been transferred to a stronger uncited premise: the count oracle is the exact external simple-graph FPRAS, and the witness primitive is standard Edmonds matching feasibility. The unweighted theorem is a pivotal external input and must be credited; this is not an independently discovered base FPRAS.

## Implementation, finite evidence and clean reproduction

Read the full gadget/sampling implementations, both test suites, upstream finite-cell checker, reproducibility helper, optional source inspector, all included audit prose/bibliography/metadata, licenses and declarations. Parsed all saved data and static receipt fields and compared their semantic values against fresh outputs.

From a fresh ZIP extraction I ran the **exact** primary README command:

```text
python3 reproduce.py --output reproduction-receipt.json
```

It passed all 28 declared payload hashes and all three checks with Python 3.14.6. The receipt is genuinely inside the extraction; no substitute absolute path was used for this required test. Original payload bytes and the manifest stayed unchanged. Gadget and sampling report semantics match the archived data after removing time/software-version fields; the upstream-cell stdout matches its archived report exactly. The expected suite counts are reproduced: 64 signatures, 729 exhaustive K4 assignments, 40 seeded K6 assignments, 12 boundaries, 3 fibers; 203 graph instances, 1,827 integrated output laws, 1,218 executions, and 243 fallback events. Evidence: `CLEAN_REPRODUCTION.json` plus `clean_package/reproduction-receipt.json`.

Independent finite checks use an independently written perfect-matching enumerator and transition-law integration: 300 generic DAGs; 132 integer signatures (1 through 129 plus 255, 256, 257); 48 integer/rational full-fiber instances; and 84 exact output laws with successful relative-error endpoints and independently failing zero, huge, and tiny positive outputs. The maximum observed TV was exactly `42911/5537792`, below eta=1/13 and the proved budget. Direct all-failure outputs with 8,193-bit operands still return legal matchings within count/witness/bit caps. A deliberate separate directed cycle produces `(2,2,0,0)`, correctly demonstrating why acyclicity is essential. These checks support the proof and wrapper, not the base FPRAS. Evidence: `independent_checks.py` and `INDEPENDENT_CHECKS.json`.

Receipt collision attempts against a payload path, the manifest, hardlink/symlink aliases, a missing parent directory, and a directory itself all fail without modifying protected files. An unlisted ambient file is excluded from the isolated test copy. Evidence: `REPRODUCTION_BOUNDARY_CHECKS.json`. An initially oversized optional fiber workload was terminated and replaced by bounded explicit integer/rational fixtures; the final exact assertions and counts above were completed.

The source code openly marks exhaustive counters and witness helpers as exponential small-instance tools. It does not misrepresent them as an implementation/benchmark of the external FPRAS or as polynomial witness routines. This meets the requested transparent construction and supporting sampling validation deliverable.

## Primary dependency and formal scope

The actual declaration is `OAI.MatchingFPRAS.thm_main : MainStatement`, not the ComparatorChallenges placeholder. I read Main, Model and comparator configuration directly in the read-only source clone. Its graph structure is finite simple undirected; its finite-alphabet machine has one uniform transition table; MainStatement bounds every random tape and returns a nonnegative rational with relative-success probability at least 1-delta. Its exact-zero property is only the infeasible-to-zero direction, which the follow-on fixes through exact feasibility. The formal theorem does not supply the follow-on weighted sampler.

The authored inspector independently reproduced 415 local modules / 3,091,883 bytes, no source-pin mismatches, no critical lexical tokens, and equality of real/comparator model definitions modulo whitespace. The pinned Lean import-header parser succeeds, but the full kernel/axiom probe fails for missing compiled dependencies. **No independent kernel build, actual compiled axiom closure, or comparator certificate was reproduced.** The package consistently discloses this and claims no formalization of the weighted follow-on. Static inspection is evidence, not kernel certification.

The separate primary proof reconstruction covers logical hole injections and relocation, finite homotopy capacity, odd subdivisions/hole accounting and inflation, fixed-label cells, signed energy telescoping and rare-guide cancellation, bounded reversible demand tags, replicated arbitrary-function ANOVA gap, tree refresh/mixing, adaptive scale statistics, and every-history bit costs. Its completed independent finite attacks record 9,958 cycles, 50,686 cells/switch encodings, and 11,554 error encodings, all passed. The full written report will be incorporated before this draft is finalized. Absence of a Lean rebuild alone is not a discovered mathematical gap; these conclusions rest on source-level mathematical reconstruction and the explicit cited theorem.

## Priority, metadata and PDF

Fresh primary-source checking confirms that McQuillan already gives the binary rational weighted-to-simple-unweighted exact equivalence; Dell and earlier path constructions supply compact positive-integer machinery; JVV supplies the classical count-to-generate framework. The rational FPRAS/sampler existence claims are therefore inherited consequences once the new unweighted theorem is accepted. Main/entropy comparison is accurate: the entropy companion's binary-multiplicity estimate has exponential factor, not the target relative FPRAS. RSZ, Barvinok and current Yi results have genuine structural/weight promises and do not cover this unrestricted target.

No identical full standalone proof/package was found in the bounded current primary-source search. That is not a novelty or first-priority certificate. The paper, metadata and README explicitly decline first-publication, new reduction, new complexity classification and independent base-breakthrough claims. This honest attributed consequence/implementation framing is compatible with the original project request; no distinct novel mathematical classification is certified here. Public upstream release is evidenced October 6, whereas September 23 is manuscript metadata. Current remote main remains the cited pin.

An auxiliary review initially alleged that Cai–Liu's v1 omitted the McQuillan credit. Direct versioned HTML, actual v1 PDF, and active TeX source falsified that allegation. The paragraph after Theorem 1.2 contains the attribution. No candidate citation/version repair is warranted; the reviewer error and its correction are preserved in `priority_primary/CAI_RECONCILIATION.md` and manifests. Review verdicts are themselves subject to falsification.

Manifest title, single author/ORCID, date, preprint type, license split, description, related source identifiers and intended three-file set agree with the actual note. No invented affiliation/coauthor, new-result framing, human peer-review claim, signed/complex extension or unrestricted Gaussian-boson-sampling consequence appears. AI use and lack of conventional human review are explicit.

Rendered and visually inspected **all six deposited PDF pages**: formulas, glyphs, margins, paragraph transitions, references, links, page numbering and author/title are legible without clipping, overlap, undefined reference placeholders or missing glyphs. All listed fonts are embedded. A clean Tectonic rebuild from the extraction succeeds and its full extracted mathematical text is byte-identical to the deposited PDF text; differing PDF timestamps explain a differing binary hash. Two underfull bibliography warnings have no substantive visual defect. Evidence: `PDF_TEXT.txt`, `PDF_BUILD_AND_QA.json`, and review render files.

## Final scope and disposition

The strongest unconditional local result is the exact polynomial-bit reduction with full weighted matching fibers and exact feasibility/zero handling. The relative FPRAS and always-feasible TV sampler are fully specified consequences of the expressly cited general-graph theorem; no substantive gap was found in their local proofs or the fresh upstream manuscript reconstruction. Formal kernel verification remains unverified and disclosed; finite tests do not certify the upstream algorithm.

Do not publish frozen v3 as the final reviewed package because its optional documented invocation fails literally. Correct that command, preserve this review/response and all v3 identities, rebuild/test the new package, and obtain a new independent complete-package verdict. A clean review is evidence, not a proof substitute. No publication action was taken by this reviewer.
