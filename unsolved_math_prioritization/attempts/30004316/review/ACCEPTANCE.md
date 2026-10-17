# Four-point quantum symmetrizer reader: final bounded acceptance

13 October 2026. Independent editorial, preservation, and portability review of the 14-file reader for problem `/30004316`, queue row 1773.

## Verdict

**Accepted without a required correction within the requested bounded review.** The candidate contains exactly 14 files totaling 69,900 bytes. The accepted mathematical proof and independent mathematical audit remain byte-exact. The documented checker edits preserve the original computations and exact result bytes, including under Python optimization. The reader consistently states the accepted scope, prior credit, and characteristic-3 qualification.

This acceptance does not replace the earlier mathematical audit or add a new mathematical proof pass. No candidate file, repository, queue, or remote service was changed by this review.

## Candidate identity

The supplied packaging report and full-reader manifest were read and their external pins independently verified:

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| `PACKAGING_REPORT.md` | 6806 | `d7364601125e8adb8f9b10759ba79179c006fe1e8c505effd104064b3e9896bf` |
| `FULL_READER_MANIFEST.json` | 2202 | `6738767c5afcf14ac64c48bda617621be0401fed93d0916651f7c5e58e057d7d` |
| `reader/MANIFEST.json` | 2161 | `4934144c521c4595f5b2bf50f0862cd649643cd1605dc2ff29e87995c207097d` |
| `reader/REPORT.md` | 20601 | `a4eaf79e0a5fbd1929bc31b26754831d344474a23577a2f2803cea3a78554767` |
| `reader/audit/AUDIT.md` | 12883 | `ce70dc4664abd11270688a024049d01ffd5a6e70032f34e62a888cffa4030735` |

Every entry of the full-reader manifest matches the actual reader file, byte count, and SHA256. Its complete inventory also matches. The reader has no symbolic links.

The five publication-eligible proof inputs and four authored audit inputs were independently checked against their respective source manifests. Seven distributed files are byte-for-byte identical to those inputs: the proof, audit, both result records, both source-metadata records, and the original run-environment record. The remaining two source-derived files are the explicitly documented portable checkers.

## Portability and computational preservation

An independent AST comparison checked all 18 proof-checker assertions and all 9 audit-checker assertions against their corresponding explicit `require` calls. Every original condition expression is unchanged. Every supplied failure-detail expression is unchanged; checks without a supplied detail identify the correct original line number. No `assert` statement remains in either portable checker.

A second comparison normalized just those assertion conversions and removed the documented module-documentation, `argparse`, explicit-check wrapper, and output-file plumbing. The complete remaining computational ASTs are identical. In particular, no mathematical formula, matrix, iteration range, exact-arithmetic operation, finite field, or result schema changed.

The explicit wrapper raises `AssertionError` when its condition is false. Eager evaluation of existing failure-detail arguments is documented. Those details contain already-computed values, tuples, and a deterministic finite-field formula calculation; inspection found no state-changing operation in them. Both scripts now print their JSON results and write a file only when `--output` is supplied. The manifest verifier also uses explicit checks.

## Independent execution and finite negative controls

Test environment: Python 3.12.14, SymPy 1.14.0, matching the recorded versions. Each replay used a standalone temporary copy containing only the reader, invoked by absolute script path from a separate unrelated working directory. No source package or sibling file was required.

For each checker in normal Python, `-O`, and `-OO`, both the default stdout-only invocation and the explicit relative `--output requested.json` invocation passed: **12 full runs**. All exited 0 with empty stderr. Standard output and each requested output file exactly matched the accepted result bytes:

| Result | Bytes | SHA256 reproduced in every mode |
| --- | ---: | --- |
| `check_results.json` | 998 | `e8163fcb60b3b4156236ea4dbb9196ccba00d0956e7156f9c79924429085d767` |
| `audit/independent_results.json` | 2439 | `f66b1e4cea2f1a2e050601d5e3671a326ca592577e6e57ef7066850c92704b6b` |

Default runs left the caller directory empty. Explicit-output runs created exactly the requested caller-relative result file. Every standalone reader copy retained its complete original inventory and byte identity.

Additional tests passed in each of the three modes:

- The intact manifest verified its 13 payload files and complete 14-file inventory: 3 positive controls.
- A same-size one-byte report mutation, deletion of `requirements.txt`, and addition of an unexpected file were each rejected: 9 integrity negative controls.
- One representative original check was forced false in a temporary copy of each checker; every invocation exited nonzero with `AssertionError`: 6 validation negative controls.

The actual candidate was rehashed after all tests and is unchanged. These are finite validation and ordinary file-integrity controls, not exhaustive fault injection, arbitrary-hostile-runtime guarantees, an authenticity certificate, or broad manifest-schema certification.

## Editorial scope and credit

All 14 public files were read, including code, JSON, and metadata. The README, accepted reports, results, and portability record agree on the following boundaries:

1. The example is `X = Z/4`, `r(x,y) = (y,x+1)`, with characteristic 2 excluded.
2. The negative FGG Question 44 image-resolution result and zero-character `k0` factoring-quotient obstruction are explicitly credited to Ferudun's existing core claims. The negative `k0` claim is not transferred to every constant-character quotient.
3. The positive `k1` all-sum-line quotient is stated only for the same example after fixing that coefficient module. It is an ordinary chain-complex quotient. No algebra-ideal, Hopf-ideal, coefficient-independent, or universal construction is asserted.
4. Exactly two degree-2, weight-3 homology classes is a rational computation. The independent characteristic-3 result is dimension three with `rank(Q3) = 46`. The all-permitted-characteristics assertion is at least the two exhibited independent classes.
5. The original terse OWR problem retains its coefficient/quotient source-scope qualification. There is no full original OWR resolution, novelty certification, exhaustive priority/literature claim, complete Ferudun census acceptance, or characteristic-two theorem.
6. The retained run command, retrieval history, and inspection-page fields are historical provenance. The README explicitly distinguishes them from packaging-time source retrieval. JKV/CJKV metadata are not promoted to dependencies of the elementary arguments.

## Links, source status, and publication boundary

All 9 Markdown links to local reader files resolve within the reader. The 20 distinct public URLs have well-formed HTTPS targets and consistent paper/record identifiers. No private chat URL, local absolute path, private handoff, or coordination link occurs in the reader.

A bounded public bibliographic link check confirmed the named arXiv landing-page identities for FGG, Lebed's idempotent-braiding and plactic papers, JKV, and CJKV. The [EMS landing page](https://ems.press/journals/owr/articles/17294) identifies OWR Report 51/2019. Ferudun's [author landing page](https://eulersolve.org/papers/owr-17294-017/) confirms his name, the 1 October 2026 manuscript date, the cited Zenodo DOI, and the publicly stated unrefereed and AI-assisted status. Those status descriptions are attributed to the source.

Direct access through the web tool was unavailable for the four journal/corrigendum DOI links and for the Zenodo record and DOI. This is disclosed as an access limitation, not treated as evidence of a broken or incorrect citation. Publisher records independently corroborated the [FGG journal DOI](https://www.sciencedirect.com/science/article/pii/S0022404916300184) and [plactic journal DOI](https://www.sciencedirect.com/science/article/pii/S002186932030418X); the [Jespers author bibliography](https://ericjespers.github.io/) corroborated the corrigendum DOI; and a [published scholarly bibliography](https://www.sciencedirect.com/science/article/pii/S0022404919301835) corroborated the idempotent-braiding DOI. Direct PDF/API byte retrieval was not repeated, so no fresh equivalence with current remote PDF bytes or universal live-link-availability claim is made.

The reader contains authored proof/audit prose, authored scripts, computed result records, and public verification metadata. It contains no copied source PDF, image, archive, extracted third-party source-text file, corpus/dataset content, private source, private personal data, private coordination file, or hidden extra file. The accepted proof's existing short attributed OWR question quotation is retained; no new source excerpt was added. No source archive program was executed or imported by the checkers or this review.

## Reproducibility record

`VERIFICATION.json` records the input pin checks, 27 check comparisons, whole-computation AST equivalence, local links, public URL inventory, six mode/checker cases with both invocation forms, and all 18 integrity/negative-control records. `review_checks.py` is the independently written harness; its logs are separate from the candidate. `REVIEW_MANIFEST.json` pins this acceptance and the review artifacts without a recursive self-hash.

**Required corrections: none.** Publication or any later change must retain the stated scope and be verified against these accepted candidate identities; this review itself performs no publication action.
