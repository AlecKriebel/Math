# Qualified acceptance of the periodic Lefschetz public reader

Date: 13 October 2026 UTC.

## Verdict

ACCEPTED for the bounded preservation, editorial, and standalone-replay review described below. No finite correction is required. This verdict applies only to the pinned reader and archive identified here. It does not add a new mathematical result, reopen the accepted proof, certify novelty, or authorize publication.

- MANIFEST.json: 2,257 bytes; SHA-256 057549ffe07d6a7789d0359b1c319ca4e18b74bd47742b4671d9074014f4b277.
- PUBLIC_READER.tar.gz: 17,791 bytes; SHA-256 b8390e61e54480821c0c4930d8748be6647f8923d3746dc774dfe729733c142f.
- PROOF.md: 5,026 bytes; SHA-256 bbd42519c66c1a74004b3edfafbf9c0cdb9d46af1c5798367240bc9b1f97e5db.
- AUDIT.md: 11,887 bytes; SHA-256 e16ee9f351ee36a8c4b114ea68ca6af02b3778e58e5c488d3a1cd2a9afb17014.

## Preserved conclusion and editorial scope

The reader consistently presents one fixed prime p, the fixed infinite field K = F_p(t), and the fixed row count c = 2. For n >= 2, both WLP and SLP hold if and only if p does not divide n-1; at n = 1 both hold. Thus both truth values occur at arbitrarily large widths in one compatible chain, giving a negative answer to each original eventual dichotomy in the standard-graded, unrestricted-characteristic, arbitrary-fixed-row formulation.

The characteristic-zero and c = 1 variants remain untouched. The displayed chain itself has both properties at every width in characteristic zero. No novelty, exhaustive priority, or exhaustive openness claim is made.

All public files and the packaging report were read. The public priority summary accurately preserves the existing bounded-search account, including the failed author-search request, the limits of the nearby-paper comparisons, and the absence of a full proof audit of those papers. This review performed no new literature-search pass. The accepted proof and primary audit, and both historical JSON result files, are byte-identical to their originals.

## Source and publication boundary

The archive contains exactly 17 regular-file members: the 16 public files, including MANIFEST.json, plus EXTERNAL_PIN.json. Every archived member's bytes match the candidate. No source PDF, source-text extraction, source image, dataset contents, or private coordination file is included.

The public citations identify scholarly sources and public URLs. Source-PDF byte counts, hashes, and retrieval times match the retained retrieval records and source bytes. Dataset pins match the prior recovery records; this editorial review did not reparse the full datasets. Inspection-history statements are preserved as historical records rather than represented as new page inspections. Relative Markdown links resolve. A scoped scan found no private filesystem paths, private conversation links, or task-coordination identifiers in the public files. The example output pathname in README.md is an ordinary placeholder.

## Computation preservation and finite replay

The exact published diffs and both original/new checker byte pins were verified. The changes are confined to argument parsing, exclusive optional output creation, comparison against historical result bytes, and replacement of the independent checker's nine asserts by explicit runtime checks of the same conditions. There are no changed mathematical helpers, ranges, formulas, expected values, or computation optimizations.

The existing packaging harness was read and rerun in a separate archive-derived copy against the original checker files. Both AST comparisons passed: every original helper and the entire main computation through result construction agree after the documented assert-to-require mapping. The added CLI prefix and revised output suffix are intentionally outside that comparison.

All 36 finite process cases passed again with Python 3.12.14 and SymPy 1.14.0:

- Both full checkers and the clean manifest check succeed in normal, -O, and -OO modes, from an unrelated working directory, without PYTHONPATH, with no changes to the isolated public files.
- Successful checker replays reproduce the historical UTF-8 JSON bytes exactly. The modular checker retains 44 witness cases and 7,707 exhaustive linear-form cases; the independent checker retains 7 Smith cases, 5 symbolic cases, 65 modular cases, and 152 injections.
- Each checker creates a new optional output with exact bytes, then refuses to overwrite that existing output, leaving it unchanged.
- One deliberately false mathematical expectation in each checker is rejected in normal, -O, and -OO modes.
- Corrupted historical-result bytes are rejected under -OO without rewriting them.
- The manifest rejects a content flip, missing file, unexpected file, wrong externally supplied pin, and wrong declared byte count in all three modes.

The declared Python 3.9 minimum is consistent with the scripts' syntax/API use and SymPy 1.14.0's declared requirement. Actual executions in this review used Python 3.12.14; this is not a multi-version or cross-platform runtime certification.

## Limits and disposition

These are finite preservation, replay, and ordinary byte-inventory checks. They are not general program-equivalence, origin-authentication, malicious-runtime, or hostile-filesystem guarantees. The all-width mathematical acceptance remains the accepted proof and audit, not extrapolation from finite computations.

The sealed candidate and its packaging records were unchanged. No queue edit, remote repository write, publication, or external contact was performed by this review. The suggested later claimed_solved disposition is consistent with the accepted scope, provided all field, row-count, initial-case, and non-novelty qualifications are retained. Turn accounting remains separate from this zero-new-mathematics editorial review.
