# Root resolution of round-one findings

Resolved 2026-09-30T21:07:43.381736-07:00. The independent round-one reports bind their historical frozen target and are preserved without rewriting their findings.

1. The package builder now explicitly excludes web_results_archive.json, web_results_archive_addendum.json, and search_responses.json at every nested location. Raw captures remain ignored local evidence. The previously tracked citation response file is removed from the current public Git tree while retained locally. No history rewrite is performed.
2. The equivalent-results report, citation-subaudit report, and priority synthesis now distinguish public query/source evidence from local-only raw responses, PDFs, extracts, OCR, and renders.
3. The rebuilt archive includes the completed fresh round-one reports, independent stress-check code/results, and concise archive integrity/reproduction evidence. Historical candidate artifacts remain immutable.

The PDF, mathematical statements, exact check scripts/results, and canonical publication metadata are unchanged. Rebuild and exclusion/inventory checks precede a new independent round-two adversary. Current PR9 publication readiness estimated **75%**; mathematical certainty and historical first priority are not assigned percentages.
