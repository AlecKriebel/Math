# Problem 30001554: reviewed morphic-involution partials

**Original conjecture remains unsolved, 5/5. Full independent scoped review: PASS.**

The source asks whether n >= 3 tau forces equality of the longest theta-unbordered-factor length and the least alternating theta-period. Theta is morphic, may have fixed letters, and borders are nonempty and proper. [Original report, Conjecture 27, p. 2222](https://ems.press/content/serial-article-files/46296).

- [Result and sharp remaining gap](RESULT.md)
- [All five proof turns and replay instructions](FINAL_REVIEW_REQUEST.md)
- [Independent full source/proof review](final_review/REVIEW.md)
- [Frozen author integrity](FINAL_FROZEN_MANIFEST.json) and [review integrity](final_review/REVIEW_MANIFEST.json)

The frozen author files preserve their pending-review history; this additive wrapper records the completed PASS.

## Strongest scoped conclusions

The conjecture is proved for every finite alphabet, morphic involution and word length when tau <= 8. The complete tau = 8 certificate has 487,930 canonical terminal words; independent incremental Python and literal C++ agree on all counts and the full stream digest. This is an all-length theorem with bounded tau, not an inference from a bounded-length scan.

Equality is unconditional for tau <= 3. The exact optimal saturation lengths for tau = 4, 5, 6, 7, 8 are 9, 11, 15, 17, 21. Other scoped theorems give an exact three-run classification and n = 3 tau - 4 near-threshold examples, plus saturation at n >= 2 pi_alt - 1 for every morphic involution. No example reaches the source's threshold with unequal parameters. The unrestricted tau question remains unresolved.

Credit is explicit for the original source's signed Fine–Wilf assertion and asymmetric family, and for the ordinary Holub–Nowotka theorem used only in the orbit-period reduction. No novelty or priority claim is made. The contemporaneous Bischoff thesis was inaccessible and is not represented as audited.

## Replay

All prescribed author Python replays and the full C++ stream were independently rerun. Author scalar controls total 555,578; the independent review adds 7,770 checks including four source PDF hashes. See FINAL_REVIEW_REQUEST.md for exact commands. Python uses its standard library; optional C++ replay needs a C++17 compiler and sha256sum. Full tau = 8 replay may take several minutes.

Portable independent replay:

    python final_review/run_portable.py --math-only

This runs 7,766 checks, explicitly omitting the four source hashes. To reproduce the historical 7,770-check receipt, obtain the four PDFs with filenames and hashes listed in SOURCE_MANIFEST.json and run:

    python final_review/run_portable.py --sources /path/to/source-pdfs > /tmp/review.json
    cmp final_review/INDEPENDENT_CHECKS.json /tmp/review.json

The original review script is unchanged. Raw PDFs, imported records, large generated streams and private material are excluded.
