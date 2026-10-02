# Problem 30005767: credited negative answer

**Reviewed disposition: already_solved, 1/5 substantive turns.** The original two-radical-field question is answered negatively by the proper subclass Av(2341,2413,3142). The exact generating function is established in Callan–Mansour–Shattuck (2017), Theorem 11; no novelty or priority claim is made.

- [Complete proof and primary references](TURN_1.md): a direct/skew grammar, ordinary generating function, and exact exclusion from the requested biquadratic field
- [Independent full review](final_review/REVIEW.md): PASS, including the original question, known enumeration, all-length grammar and noncancellation argument
- [Frozen author integrity](FINAL_FROZEN_MANIFEST.json) and [frozen review integrity](final_review/REVIEW_MANIFEST.json)

The source field is Q(z, sqrt(1−4z), sqrt(1−6z+5z²)). The counterexample has minimal field Q(z,sqrt(P)) for P=1−8z+20z²−24z³+16z⁴−4z⁵. Four exact square-class obstructions and the nonzero radical coefficient establish nonmembership. Including or excluding the empty permutation does not affect the conclusion.

The immutable author files record their pre-review candidate status. This additive wrapper and the independent review record the accepted final disposition. Other questions in the report are outside scope.

## Reproduce

Python 3 standard library suffices for the author controls:

    python verify_turn1.py > /tmp/separable-author.json
    cmp TURN_1_CHECKS.json /tmp/separable-author.json

This replays 143,023 exact controls, including all permutations through length 8 and grammar coefficients through degree 80. For the independent controls, Python 3 plus SymPy is required:

    python final_review/run_portable.py --math-only

That runs 5,937 assertions, explicitly omitting the seven source-PDF hash checks. To reproduce the full historical 5,944-assertion receipt, obtain the seven primary PDFs specified in SOURCE_MANIFEST.json into one directory using the listed local filenames, then run:

    python final_review/run_portable.py --sources /path/to/source-pdfs > /tmp/separable-review.json
    cmp final_review/INDEPENDENT_CHECKS.json /tmp/separable-review.json

The original review script and receipt are unchanged. The additive portable wrapper adapts only file location and the explicitly selected source-hash mode. The written all-length proofs remain the mathematical certificate; bounded enumeration cannot replace them. Raw sources and imported records are not redistributed.
