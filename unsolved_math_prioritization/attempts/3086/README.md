# Unit-square covering: audited partial results

**Unsolved, 4/5 substantive approaches. Independent AI audit PASS within the stated partial scope.** The original all-n conjecture remains unresolved. No novelty, human peer review, journal acceptance or priority is claimed.

The main result is an exact counterexample to the unrestricted local grid-length estimate in Lemma 2 of [arXiv:2609.15876v1](https://arxiv.org/abs/2609.15876v1). It identifies a gap in the proposed n=4 proof. It does not refute the n=4 conclusion or the all-n conjecture, and constructs no 17-tile covering. The independent audit also constructs a 32-tile cover making the offending tile indispensable.

The packet additionally proves the n=1 and axis-parallel exclusions, a necessary lower bound of 2n rotated tiles, and a coarse grid-length estimate. Its scalar relaxation is feasible for all n>=2; this is not a geometric covering construction.

## Read and reproduce

- [Exact authored proof](author/PROOF.md) and [four-approach log](author/RESEARCH_LOG.md)
- [Complete independent audit](audit/AUDIT_REPORT.md) and [claim boundaries](audit/CORRECTIONS.md)
- [Current verdict and delivery metadata](VERDICT.json)

Run with Python 3.9 or newer, using only its standard library:

```sh
python3 -B verify_publication.py
python3 -O -B verify_publication.py
```

The wrapper resolves paths relative to itself and also works from an unrelated working directory after relocation. It checks exact recursive inventory, SHA-256 and byte counts, both original ZIPs and all 17 extracted-file matches, both frozen manifests, author output, and independent output in normal and optimized modes. The author verifier and author manifest checker always run with assertions enabled in isolated non-optimized child interpreters, even when the wrapper is launched with -O or PYTHONOPTIMIZE.

To verify the precise queue update as well, add `--queue /path/to/unsolved_math_prioritization/QUEUE.md`. Only this row's Status and Turns change to unsolved and 4/5. Every other byte, including Findings, links and the existing stale embedded header, is preserved. No queue generator was run.

The original author and audit files and their safe archives are unchanged. Historical pending-audit/no-remote-write statements remain creation-time records. This wrapper records the later PASS; no mandatory author correction was required.

## Literature and publication limits

The 2009 n=2 and n=3 statements were checked on original page 174, not by auditing the full original proof. S(6)=2 remains a conjecture in the inspected Dosa-Langi-Tuza preprint. Source inspection and public hash identities are recorded in the frozen packages; source PDFs, extracts, images, raw datasets and private coordination files are excluded.

This draft preserves a research checkpoint. No merge, release, DOI deposit or third-party outreach is included. The exact arithmetic checks supplement the written scoped proofs; they do not prove the original all-n conjecture.
