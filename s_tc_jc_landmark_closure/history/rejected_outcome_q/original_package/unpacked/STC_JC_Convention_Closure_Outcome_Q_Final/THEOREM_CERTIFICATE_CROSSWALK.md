# Theorem-to-certificate crosswalk

| Claim | Primary evidence | Independent evidence |
|---|---|---|
| Frozen `sd0` classification | `baseline/SD0_BASELINE_MANUSCRIPT.pdf`; `baseline/BASELINE_PROVENANCE.json` | Exact active commit and blob hashes in the provenance file |
| Root zipper structural lemma | `src/verify_root_zipper_structure.py`; `certificates/root_zipper_structure.json` | `review/independent_frontier.cpp`; `certificates/independent_frontier.json` |
| Complete parallel-theta frontier | `src/primary_convention_frontier.py`; `certificates/primary_convention_frontier.json` | `review/independent_frontier.cpp`; fibre profiles in `certificates/independent_frontier.json` |
| Strict difference between strong rooting classes | primary strict witness and exact rooting census in `primary_convention_frontier.json` | `review/independent_rooting_fibres.cpp`; `independent_rooting_fibres.json` |
| Exact JC zipper tensor and strict section | `src/verify_cleanup_jc.py`; `cleanup_jc_map.json` | `review/independent_cleanup_model.py`; `independent_cleanup_model.json` |
| Convention/class reconciliation | `docs/THEOREM_Q_PROOF.md` | `review/review_convention_equivalence.py`; `independent_convention_review.json` |
| Sharpness survives cleanup | primary Theta pair records in `primary_convention_frontier.json` | independent rooting counts in `independent_rooting_fibres.json`; frozen baseline Section 9 |
| Mutation sensitivity | `review/run_mutation_suite.py` | `certificates/mutation_suite.json` |
| Final release integrity | `reproducibility/verify_release.py` | clean-clone transcripts |
