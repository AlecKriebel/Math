# Weighted centers in median graphs

Author-stage complete candidate for problem 30006605 / OWR-14299911-007 (rank 598), obtained in one substantive attempt. Independent audit pending. No historical-priority claim.

The proof reduces multiplicatively weighted center thresholds to nonnegative-integer additive eccentricities. Combining the existing Bergé–Ducoffe–Habib oracle with an implicit candidate search gives O(n log^5(2n)) time on every finite median graph, including bounded-cube-dimension graphs. The search mechanism is credited to Ducoffe's ESA 2026 decision-to-optimization result.

- `PROOF.md`: complete reduction, optimization proof, complexity, and precise limits
- `SOURCE_STATUS.md`: exact source, later literature, attribution, and source fingerprints
- `APPROACH_LOG.md`: one substantive attempt and its challenges
- `controls.py`: standard-library-only exact regression controls
- `CONTROL_RESULTS.json`: frozen output of the controls
- `RESULT.json`: machine-readable author disposition
- `SHA256SUMS`: hashes of the frozen public packet, excluding the manifest itself

Run `python3 controls.py`; compare the JSON output with `CONTROL_RESULTS.json`. The general additive oracle used by the controls is quadratic reference code. Only the separate tree oracle is fast. These tests support the reduction, not the BDH runtime theorem, and are not formal verification or human peer review.

Source PDFs, their full-text extracts, complete upstream corpora, and private coordination are excluded. No remote repository write is authorized by this packet. If accepted for publication, retain the full proof, attribution, control limitations, and independent audit together. OpenAI tools assisted the preparation of this research packet.
