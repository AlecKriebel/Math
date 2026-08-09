# Focused reviewer packet

This packet is a short route into version 1.1's load-bearing and restored
claims. It is not an outreach message and asks no one to endorse, join, or
review the entire project.

Recommended order:

1. `two_page_summary.md` — result, source credit, and exact scope.
2. `proof_roadmap.md` — the shortest analytic routes through the value,
   support-rigidity, permutation, SOS, and randomness arguments.
3. `load_bearing_claims.md` — concrete falsifiers for the central and
   secondary claims.
4. `theorem_to_artifact_map.md` — theorem, proof, and verifier locations.
5. `focused_questions.md` — six bounded core questions and two secondary
   benchmark checks.
6. `source_author_review.md` — source-claim comparison, normalization, and
   convention notes.

Fast mathematical replay:

```sh
cd cyclic_bell_exact_values_and_randomness
python3 verification/verify_merged.py
python3 verification/verify_rigidity.py
python3 verification/verify_exact_benchmarks.py
python3 verification/verify_private_mub_binary.py
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
```

The one-command replay, including builds, historical hashes, and website
checks, is:

```sh
cd cyclic_bell_exact_values_and_randomness
./reproduce.sh
```

The canonical manuscript is `../main.tex`; the built PDF is
`../output/pdf/cyclic_bell_exact_values_and_randomness.pdf`. Passing code is
regression evidence, not peer review and not a substitute for the analytic
$q_c$, support-rigidity, or all-dimensional arguments.
