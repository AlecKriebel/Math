# Focused reviewer packet

This packet is a short route into the load-bearing claims. It is not an
outreach message and asks no one to endorse, join, or review the entire
project.

Recommended order:

1. `two_page_summary.md` — statement and scope in two pages of prose.
2. `proof_roadmap.md` — how the scalar, operator, phase, and SOS steps fit.
3. `load_bearing_claims.md` — the few identities on which the paper depends.
4. `theorem_to_artifact_map.md` — exact theorem/check locations.
5. `focused_questions.md` — six bounded review questions.
6. `source_author_review.md` — source-claim comparison and convention notes.

Fast replay:

```sh
cd cyclic_bell_exact_values_and_randomness
python3 verification/verify_merged.py
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
```

The canonical manuscript is `../main.tex`; the built PDF is
`../output/pdf/cyclic_bell_exact_values_and_randomness.pdf`.
