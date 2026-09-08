# Independent proofreading and referee follow-up: v1.0.11

**Paper:** *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*

**Author:** Alec Kriebel

**Reviewed target:** `137ffa9f1a340f621651395ad0236cf1bdadb51c`, tag `maximally-collective-stable-turing-v1.0.11`.

**Review date:** 7 September 2026, America/Los_Angeles (8 September UTC).

## Recommendation

**The current preprint is ready for publication within the scope of this review. No correction to the shipped manuscript, supplement, standalone mathematical exports, or SIADS PDFs is required. Both v1.0.10 findings, C1 and J1, are closed.**

One additional low-priority software issue is documented below: noncanonical coefficient input can be accepted numerically and printed incorrectly. Every coefficient actually shipped in v1.0.11 is correct and uses the canonical encoding. I recommend fixing this input-format inconsistency during future code maintenance; I would not delay publication of the current frozen PDFs for it.

This is a fresh proofreading and repair-verification round. It checks the revised source, mathematical preservation, rendered pages, supporting certificate boundaries, current replay, and actual release assets. The preceding round's exhaustive mathematical reconstructions were not counted as newly rerun here. No new mathematical gap, unsupported strengthening, attribution error, or document typo requiring revision was established.

## C1 closed: explicit coefficient fields agree across generation and readers

The generator explicitly selects U for the 22-term homogeneous table and A for the 84-term spatial table. It and both mathematical readers reject conflicting recognized coefficient fields. The exact prior witness, adding `coefficient_in_U_ascending: ["1"]` to the spatial row `[6,1,0]` with its correct A coefficient retained, now produces the intended rejection.

Independent tests cover 21 cases and 63 direct reader/generator calls, including both conflicting-field directions, identical-valued competing fields, wrong or missing parameter fields, swapped variables, coefficient changes, and harmless metadata. The two actual regeneration commands with dual-field mutants reject before changing any of their three generated outputs. A formatter is not claimed to replace the mathematical readers' equality checks; the report distinguishes their roles.

All 26 relevant current unpacked implementations and 12 reader copies in the seven current ZIP bundles match the corrected implementations. A separate exact-rational parser checks all 218 table rows against the coefficient data. Those rows are unchanged from v1.0.10, and all five current TeX table copies agree. The previous unambiguous rational-parameter notation is preserved.

Evidence: [certificate review](certificates/CERTIFICATE_REVIEW.md), [repair cases](certificates/REPAIR_RESULTS.json), and [independent shipped-coefficient comparison](certificates/SHIPPED_COEFFICIENT_RESULTS.json).

## J1 closed: all five journal overflows repaired and the gate covers acceptance points

The five previously affected locations now fit: SIADS manuscript pages 17 and 19, and supplement pages 14, 20, and 23. The command paths wrap visibly, the contrast table uses narrower column spacing, and the long polynomial/rational and function-space displays are split without changing their mathematics.

Fresh detached builds have zero occurrences of the shared policy's undefined-reference/citation and overfull horizontal/vertical-box warnings. The six main/supplement final logs and the fresh cover-letter log pass. Independent measurements confirm the former four material overflow endpoints lie inside the journal's right text edge at 522 PDF points:

| Repaired content | Previous endpoint | Current matched endpoint |
|---|---:|---:|
| Main verifier command | 557.31 | 397.20 |
| Supplement verifier command | 581.11 | 387.07 |
| Contrast-table last column | 538.77 | 516.19 |
| Reference-coefficient rational display | 570.80 | 382.34 |

The fifth, previously small overflow is removed by splitting the operator and constrained-space definitions. All repaired pages were also inspected visually.

The shared log checker is applied before canonical, journal, and cover-letter PDF acceptance; it is also present in portable replay and detached source-build checks. Independent mutations through the actual package-refresh script confirm that the exact old journal overflow, a journal vertical overflow, a cover-letter overflow, and a canonical overflow all reject before the relevant bad PDF is accepted or any of the seven sealed bundle bytes change. These tests establish the real call sequence, beyond the supplied synthetic parser test. They do not claim that a failed build leaves no disposable files.

Evidence: [release report](release/RELEASE_REPORT.md), [fresh final logs](release/DETACHED_FINAL_LOG_WARNINGS.json), [measured layout repairs](release/JOURNAL_REPAIR_COORDINATES.json), and the retained `*_RESULT.json` mutation records under `release/`.

## One low-priority follow-up: normalize scalar coefficients before rendering

**Disposition: software maintenance; no required change to the current preprint.**

At `computation/generate_tables.py:18–23`, scalar coefficients are converted directly to strings for TeX. The mathematical reader at `independent_verifier/verify_mode_isolation.py:32`, its duplicate, and the corresponding exposition reader instead parse them as exact rationals. This differs for some noncanonical inputs.

The minimal witness changes `homogeneous.terms[0].coefficient` in `improved_modulus_certificate.json` from the string `"1"` to JSON Boolean `true`. The row has powers `[10,0]`. All three direct reader calls interpret it as rational 1 and accept. Regeneration prints `10 & 0 & $True$` at line 9 of the TeX table. The complete symbolic aggregate and manuscript source audit accept, including the source audit's conditional release/submission checks. The rebuilt 19-page supplement passes the canonical `--profile full` PDF audit with no selected TeX warnings; the other audited PDFs were copied unchanged from the target. The parent reviewer inspected its complete page 11: the coefficient is visibly the italic letters “True.” The scalar string `"1e0"` gives a similar direct-reader/generator mismatch; that second spelling was not separately carried through the full PDF build.

Independent expansion confirms that the defining homogeneous polynomial's x^10 coefficient is exactly 1. The issue concerns the representation displayed to a reader. The numeric polynomial used by the proof checks remains correct. Canonical integer/fraction strings are the convention used by every shipped coefficient, but that individual-scalar convention is not enforced by the outer certificate schema.

The test does not establish acceptance by an entire altered-release refresh. It establishes direct-reader, generation, symbolic, source-audit, and canonical PDF-audit behavior on disposable copies, as documented in the [scalar note](certificates/SCALAR_RENDERING_NOTE.md). Before regeneration, the table-freshness check rejects the changed JSON against the unchanged shipped table. The unchanged published hashes detect changes to the JSON, table, and PDF. No current release asset contains this malformed value.

**Suggested repair:** render the parsed exact rational in canonical numerator/denominator form, with an explicit Boolean policy, or require canonical rational strings consistently in readers and generator. Retain the Boolean and scientific-string examples as two focused regressions. No theorem, coefficient value, or broad parser redesign is needed. This closes a real input-format inconsistency without imposing a new publication condition on the correctly rendered release.

Evidence: [scalar experiment](certificates/SCALAR_RENDERING_RESULTS.json), [independent mathematical cross-review](algebra/SCALAR_REPRESENTATION_CROSSREVIEW.md), and the reproducer and logs named in the scalar note.

## Mathematical and document proofreading

Independent source comparisons preserve the previously reviewed mathematical content. After selecting the canonical layout and ignoring whitespace, the main body before its availability paragraph is unchanged, as is the supplement. The standalone theorem summary and proof skeleton are byte-identical to v1.0.10 and retain the singular-J and positive-diagonal-D assumptions. Both newly split mathematical displays preserve every coefficient, sign, denominator, operator, and integrated-mass constraint. No nonlinear coefficient, endpoint, diffusion profile, or numerical datum changed.

The algebra and PDE reviewers reread the affected expressions in context. The localization quantifier, homogeneous-stability assumption, stationary/wave distinction, nonattained contrast infimum, local PDE stability, and exponent-only optimality qualification remain consistent. The exposition review found 22 bibliography entries and 22 distinct cited keys, no missing or duplicate bibliography key, and no unresolved main-document label. The current claims and bibliography are unchanged from the preceding primary-literature review, so another broad literature search was not represented as necessary or performed here.

The parent reviewer freshly rendered and viewed every page of all seven PDFs: canonical manuscript 19, canonical supplement 19, theorem summary 3, proof skeleton 6, SIADS manuscript 24, SIADS supplement 24, and cover letter 1. Total: **96 pages on 26 contact sheets**. No new clipping, overlap, illegible coefficient row, broken reference, or unexpected blank page was found. The five repaired journal locations additionally have fresh log and coordinate evidence, avoiding reliance on the page overview alone.

Detailed reports: [algebra](algebra/ALGEBRA_PROOFREAD.md), [nonlinear/PDE](pde/PDE_PROOFREADING_REPORT.md), [document review](documents/DOCUMENT_REVIEW.md), and [exposition/metadata](positioning/POSITIONING_REPORT.md).

## Reproducibility, identity, and limits

The immutable source snapshot contains 1,868 files and 24,371,262 bytes, recorded in `SOURCE_INVENTORY.json`. Its archive SHA-256 is `6bb6333c1f27ab9a70c67e424419a6bbf1ae52c058e333d30737da91e32ef839`. The tracked release manifest correctly contains 1,867 entries, excluding itself. Source identity was rechecked after the independent experiments.

Fresh validation passed 39 tests with no skips, all 39 direct verifier entrypoints, all 39 optimized-Python rejection controls, the complete symbolic suite, minimal replay, and full current portable replay. The portable run included all 15 existing numerical base/refinement cases and provenance. Its original 216-entry baseline remained unchanged; its regenerated 218-entry self-manifest verifies. All seven rebuilt ZIPs match the released bytes, three detached source builds compile cleanly, and all six main/supplement rendered-text streams match their intended PDFs. The nine downloaded assets match both their declared digests and the target source; the remote tag resolves to the reviewed commit. See the [public release](https://github.com/AlecKriebel/Math/releases/tag/maximally-collective-stable-turing-v1.0.11) and retained release evidence.

The optional historical-lineage replay still lacks five external archival inputs. Only its nonmutating failure preflight was verified, not a successful historical replay. The complete current portable replay needs none of those inputs. Google Drive contents, a live submission portal, and a preprint server's own TeX environment were not inspected. Previously confirmed author declarations are retained and were not reopened.

Current release references and the explicitly preceding v1.0.10 DOI are accurate. The September 6 release date agrees with the public September 7 UTC publication timestamp in the author's local time zone. No additional DOI update is required to close this proofreading round.

`recreate_snapshot.py` reconstructs the ignored snapshot; `check_audit_evidence.py` verifies its identity, retained evidence syntax, and local report links. Each lane retains its own scripts, results, and scope. Only this independent audit folder was changed and published by the review. The manuscripts and frozen release were left intact.
