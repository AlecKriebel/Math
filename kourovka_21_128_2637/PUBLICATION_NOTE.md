# Publication state: independently checked partial results

KOU-21.128 remains **unsolved after 5/5 substantive attempts**. A fresh independent audit passed the stated partial conclusions. The original author status, README, control summary and audit-scope files are preserved unchanged as historical input; their “audit pending” wording is superseded for current publication status by this note and PUBLICATION_STATUS.json.

Read [the full independent audit](audit/AUDIT_REPORT.md) and [additive editorial clarifications](EDITORIAL_NOTES.md). No mathematical result in the frozen original was removed or strengthened.

The independent scripts use different constructions from the author scripts. Run `python -B audit/independent_controls.py` and `python -B audit/reflection_arithmetic_controls.py` from any working directory after installing the requirements in audit/requirements.txt. Both scripts are included with complete derived JSON and logs; portable replays are also supplied. The principal independent rank calculation reaches 901 modulo both 101 and 103 after spanning-tree reduction. It proves rational first-homology vanishing only for the displayed cover.

For portability, the independent control's absolute workspace root was replaced by a path relative to its own file, and its original-file verification now reads the public author MANIFEST.json. The full mathematical code and all numerical output are preserved. The audit report's local filesystem reference was replaced by the public package description. These are packaging adaptations, not a new mathematical review.

No full resolution, novelty certificate, human peer review, paper publication or DOI is claimed. Primary PDFs, source screenshots, raw corpus and private bookkeeping are excluded.
