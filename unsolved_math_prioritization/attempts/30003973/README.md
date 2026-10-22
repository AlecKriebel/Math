# Ramsey equivalence: five-turn partial results

**Problem 30003973 / OWR-16627-005 remains unsolved, 5/5 substantive turns.** No universally two-equivalent graph pair has been proved three-nonequivalent, and no universal implication has been proved. Independent full review passed the scoped results without mandatory correction.

The exact [source question](https://ems.press/content/serial-article-files/46764) is Question 6, printed p2736. It concerns all finite Ramsey-host graphs and ordinary monochromatic subgraph copies. It is stronger than equal numerical Ramsey numbers or agreement on bounded or restricted hosts. Record 30004035 repeats this implication and adds other variants; only the exact overlap is identified, and no other queue row is changed.

## Results

- Turn 1: exact isolated-vertex/core and Ramsey-threshold reduction
- Turn 2: a sufficient mixed asymmetric-Ramsey condition and necessary crossed witnesses for a genuine counterexample
- Turn 3: an exact seven-element abstract square/cube obstruction, with a proof that it cannot directly be a single graph-copy avoidance family
- Turn 4: an all-size star-forest-host threshold and canonical max-plus theorem, plus star/matching core rigidity
- Turn 5: two targets agree on every star-forest host for every color count q≥2, but a 53-vertex, 45-edge Ramsey-minimal host separates them already in two colors

[RESULT.md](RESULT.md) states the remaining gap. The abstract example and the restricted-host collision are not counterexamples to the original implication. Known even/additive and nested-target transfer results remain credited prior work. No novelty or priority is asserted.

## Review and replay

[Independent full review](final_review/ADVERSARIAL_REVIEW.md): PASS within scope. This is AI-assisted mathematical review, not formal certification or human peer review.

Run `python verify_turn1.py` through `python verify_turn5.py` from this directory and compare their outputs with the corresponding TURN_n_CHECKS.json files. All 198,182 author assertions replayed exactly. The scripts use the Python standard library only. Run `python final_review/independent_checks.py` for 942 separate controls, including all 45 deletion certificates. The review's copied certificate is byte-identical to the frozen author input.

The optional build_turn5_certificate.py reproduces the labeled-graph certificate; use a disposable copy to compare it without changing frozen artifacts. SciPy/HiGHS was used only for discovery of the abstract example and is not a replay dependency.

The final and historical manifests bind all frozen author files. The review manifest binds the separate review. Frozen records retain their historical pending-review wording; this README and the appended review give the subsequent disposition. Raw source PDFs, imported records, search experiments, private queue files and local receipts are excluded.
