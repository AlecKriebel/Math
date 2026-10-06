# Converse unitary distinction: audited scoped nonresolution

Problem 30001737 / OWR-4804-005, rank 835. Status: **unsolved**, 3/5 substantive approaches used. No new distinction theorem, target counterexample, full resolution, or novelty is claimed.

Read [the corrected report](corrected/REPORT.md) and [the attribution-corrected independent AI audit](audited/audit/INDEPENDENT_AUDIT.md). The target is the complex/real pair GL_n(C)/U(p,q), with ordinary Galois pullback and character occurrences counted with multiplicity. The all-size counting formula expands a published upper bound; positivity of that bound does not establish distinction. Rank-one cases and radial twists are known or elementary consequences. Descent through the actual Langlands kernel remains unresolved.

## Files and corrections

- `author/` and the original author ZIP preserve the historical authored freeze byte-for-byte.
- `corrected/` and its ZIP contain the mandatory isolated-startup correction.
- `audited/` is the complete attribution-corrected audit archive, including the same corrected payload, mathematical audit, source-scope review, executable controls, and actual acceptance records.
- `audited/audit/ISOLATED_STARTUP_CORRECTION.patch` is the actual applied executable correction.
- `attribution/` records the actual attribution-only patch and fresh acceptance. It changes only the audit's review wording and manifest. Removed wording in the patch is superseded: the review was mathematical review by an independent AI auditor. No human review is claimed.
- The superseded audit ZIP remains preserved locally by its public fingerprint; it is not the operative audit and is not republished here.
- `PUBLICATION_MANIFEST.json` covers every published attempt file except itself. Archive hashes, member lists and external manifest pins are in `PUBLICATION_METADATA.json`.

## Startup safety and replay

The original direct startup was vulnerable to an unlisted local `argparse.py` executing before inventory rejection, in normal and optimized execution. A nonzero exit status did not mean rejection before code execution. Retaining that archive does not endorse its direct startup.

Use a trusted interpreter and an independently reviewed copy of `audited/audit/isolated_bootstrap.py`. Verify its SHA-256 against this separately supplied value before executing:

    1f1dae9e6a5123d86febe4d485dc5b29e7a43d1ff484a0915816acb4f18f0032

The corrected payload manifest pin is:

    4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703

From this directory:

    python -I -S -B audited/audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703
    python -I -S -B -O audited/audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703
    python -I -S -B audited/audit/isolated_bootstrap.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703 audit_checks.py
    python -I -S -B audited/audit/independent_counting.py corrected 4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703

The complete acceptance suite requires the exact public corpus snapshots identified in `audited/audit/CORPUS_ACCEPTANCE.json`. Dataset and source-document contents are deliberately excluded. With local paths CATALOG, PROBLEMS, REPORTS:

    python -I -S -B audited/audit/acceptance_checks.py author corrected CATALOG PROBLEMS REPORTS
    python -I -S -B -O audited/audit/acceptance_checks.py author corrected CATALOG PROBLEMS REPORTS

The bootstrap verifies inventory and all payload hashes before executing a private snapshot of those bytes. This is an integrity gate with a trusted interpreter, standard library, operating system, bootstrap and externally supplied manifest pin, not a hostile-code sandbox. Python must be launched with `-I -S -B`; direct-entry guards cannot undo interpreter startup hooks.

## Evidence and limitations

Normal, optimized and relocated replay covers 22 hostile-control families; the corrected author suite covers 13 semantic and 10 integrity mutation families. Independent bitmask counting agrees on 174 original patterns/1,266 signatures and 3,002 expanded multisets/23,594 signatures through n=8. Finite regression is not a general distinction theorem. Source inspection and prior-attempt searches are bounded; they do not certify exhaustive literature coverage or definitive openness.

Only the target queue row's Status and Turns cells are updated. All unrelated queue bytes and links are preserved. Publication is a draft PR, with no merge, release, DOI creation or outside outreach. An absence of CI runs or statuses is not a CI pass.
