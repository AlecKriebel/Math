# Problem 30000417: reviewed five-turn path list-labeling partials

**Original conjecture remains unsolved, 5/5. Independent full scoped review: PASS.**

The original OWR 7/2006, p.416, Conjecture2 uses **floor(3d(1−1/n))+1**, for n>=3 vertices and d>=1. The imported ceiling is a transcription error. Labels are arbitrary natural numbers and must differ by at least d at path distance1 or2. [Official original source](https://ems.press/content/serial-article-files/46037?nt=1).

Read [RESULT.md](RESULT.md), the five TURN_n.md files, and the [full independent review](final_review/ADVERSARIAL_REVIEW.md). Frozen historical files retain their pending-review wording; this additive wrapper records the accepted review.

## Strongest scoped theorem and remaining gap

For **every path length**, d=2 six-element lists whose union contains at most nine labels admit a labeling. The complete finite-state closure has4,087,257 states and343,329,588 transitions. Python and independently written packed C++ implementations agree on the entire state-set digest. This is an all-length computer-assisted theorem, not an inference from a bounded-n scan. The explicit five-list P6 obstruction makes six sharp in this restricted-union family for all n>=6.

Other proved results include exact gap compression for each fixed(n,d,k), a weighted path deficit lemma, sufficient common/variable-anchor criteria, and unbounded-palette local-extremum families. Explicit feasible instances show limitations of the anchor method and a particular global palette-recoding method. None is a counterexample to the original conjecture. The all-n, all-d, arbitrary-palette question remains unresolved.

## Runtime qualification

The theoretical Bellman comparison bound O(nk³) assumes precomputed local anchor incidence. The frozen Python implementation scans all anchors when constructing geometry and can add **O(n²) preprocessing overhead**. Its correctness and termination are unaffected. This qualification is carried additively in the independent review; frozen author files are unchanged.

## Replay

All Python checks require only the standard library:

    python verify_turn1.py
    python verify_turn2.py
    python verify_turn3.py
    python verify_turn4.py
    python verify_turn5.py
    python final_review/check_independent.py --packet .

Compare each author output byte-for-byte with TURN_n_CHECKS.json and the independent output with final_review/INDEPENDENT_CHECKS.json. Turn5 is the full uncapped closure and may take around two minutes and several hundred megabytes. Optional crosschecks require a C++17 compiler; turn5 additionally uses unsigned128-bit integers. See FINAL_REVIEW_REQUEST.md and final_review/README.md for exact replay instructions. Independent review added98,448 assertions and reran both full closures.

Credit is explicit for the primary Kohl/Schreyer/Tuza/Voigt and dissertation results, including classical boundary cases and common-extremum machinery. No priority or novelty claim is made. Source PDFs, imported records, and the45MB state binary are excluded.
