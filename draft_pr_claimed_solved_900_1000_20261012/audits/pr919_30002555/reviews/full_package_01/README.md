# First new whole-package review of PR919

Read AUDIT.md and RESULT.json for the verdict: mathematics passes as an attributed application; two package/workflow corrections are required. The reviewed original author record remains1/5, with no audit proof-search turn added.

The exact candidate is preserved in `publication/reviewed_candidates/candidate01/`, relative to the audit root. The default scripts use that stable preserved candidate. An explicit `--candidate` option permits the same original candidate bytes to be placed elsewhere. A later repaired active candidate will have different anchors and is intentionally not accepted by these historical scripts.

On this audited macOS workspace, use the existing Python interpreter recorded in REPRODUCE.py:

```
/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python -I -B /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr919_30002555/reviews/full_package_01/VERIFY.py --expected-manifest INDEPENDENTLY_OBTAINED_AUDIT_MANIFEST_SHA256
/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python -I -B /Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr919_30002555/reviews/full_package_01/REPRODUCE.py --expected-manifest INDEPENDENTLY_OBTAINED_AUDIT_MANIFEST_SHA256
```

This research-audit reproducer needs the original repository's Git objects and this workspace layout. It is not the portable release entry point. It reruns actual four-mode release verification, current guard suites and independently authored controls, with all scratch confined to this review's ignored tmp. If Tectonic and Poppler are installed, it also repeats source compilation and all three raster comparisons. No package, future-helper, Git/index, PR, publication, tracker or external-person write is performed. Preserved helper copies are authenticated against checkpoint44 Git objects; current live helpers may be repaired without invalidating this review.

The explicit MANIFEST.json public map excludes itself and all raw third-party bodies, extracted texts, rendered source pages and private scratch. The helper copies are the project's own authored source, not third-party materials. Hash verification is an integrity check, not mathematical or priority certification.
