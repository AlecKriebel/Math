# 30000660: credited resolution of the literal2007 étale question

**Already solved, one substantive author turn (1/5), as a classical source-version resolution.** The smooth Russell-form family

    y^p=x+t x^p -> A¹_t

has all geometric fibers isomorphic to A¹ in characteristic p, but cannot become the trivial family after any dominant étale base change. A finite purely inseparable degree-p base change does trivialize it. This example is explicitly credited to Russell1970; no novelty claim is made.

**The later finite-degree question and the Q-bar case remain untouched.** The2007 report asks for an étale conclusion over arbitrary algebraically closed fields and specifically F_p-bar or Q-bar. The2014 published Kraft–Russell theorem has a finite-degree conclusion in general and separates the characteristic-zero étale case. Its remaining arbitrary-field finite-degree question is not answered by this example. SOURCE_GATE.md records the exact source comparison, including the imported lost overbars and closed-fiber convention.

Start with RESULT.md and TURN_1.md. The total space is integral and the morphism is smooth and dominant; the fibers are reduced and geometrically integral. The argument does not exploit a nonreduced-fiber loophole. A generic étale extension is finite separable, while a polynomial trivialization would force t to be a p-th power in it, contradicting separability and the t-adic valuation.

## Independent validation and preserved history

The full independent source/proof review is review/REVIEW.md: PASS without a mandatory correction. All10 frozen author and4 frozen review artifacts are preserved byte-for-byte. Historical review-pending states are retained; REVIEWED_STATUS.json gives the current disposition. No five-turn exhaustion is claimed.

Run `python3 verify_turn1.py` and compare with TURN_1_CHECKS.json:8,943 exact controls. The independent checker has2,096 controls including integrity checks. To run it portably, download the four primary PDFs from the URLs in SOURCE_MANIFEST.json, then run `python3 review/run_portable.py --source-dir /path/to/pdfs` and compare with review/INDEPENDENT_CHECKS.json. The wrapper changes only file locations; the frozen assertions remain unchanged.

Raw PDFs, renders, imported data and private coordination are excluded. This draft records a credited mathematical clarification, not human peer review or a merge/release request.
