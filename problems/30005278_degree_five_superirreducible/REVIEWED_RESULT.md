# Reviewed result: 30005278 / OWR-11695860-018

**Original existence question unsolved, 5/5. Full independent scoped review: PASS, with no mandatory correction.** This packet does not certify a degree-five 2-superirreducible polynomial or an integer quadratic counterexample to Du's candidate.

The exact target is Wooley's Question 9, OWR 50/2022, printed 2945: https://ems.press/content/serial-article-files/46986 . The report year is 2022 and the publication date is 27 July 2023. Later explicit primary definitions exclude constant substitutions and test irreducibility in Q[x]. The candidate X^5+2X+1 and its prior ax²+c theorem are credited to Lara Du; no historical novelty is asserted.

The five-turn packet proves an exact dyadic obstruction, global sparsity restrictions and an explicit remaining rational curve, a Galois-theoretic prime-certificate boundary, three infinite discriminant-band irreducibility results, and an odd-degree norm/CRT theorem equating integer and rational quadratic substitution properties for each fixed monic odd-degree polynomial. The remaining curve has points in every completion; its rational points remain undetermined.

The exact scopes are essential. Local splitting is not global reducibility. Square norm is not sufficient for a square in the root field. A prime-certificate obstruction is not a factorization theorem. The odd-degree descent requires monicity and does not cover arbitrary nonmonic candidates. The three discriminant bands do not exhaust all quadratics. All-completions points do not imply a rational point.

Read FINAL_RESULT.md, all five TURN_n.md, and independent_review/ADVERSARIAL_REVIEW.md. Frozen progress states saying review pending remain unchanged; this wrapper records the completed review. Turn 5 explicitly closes the earlier Turn 2 integrality substep while retaining the global rational-point gap.

## Verification

All five author receipts replay byte-exactly: 78,440 assertions. Separate independent controls add 6,044 exact assertions. The 600-row initial certificate is complete and paired with an analytic infinite-tail proof. Other bounded boxes and prime samples are labelled diagnostics. Author turns 2, 3 and 5 and the independent checker require Python 3 plus SymPy; author turns 1 and 4 use the standard library. Run the independent checker with `python independent_review/independent_checks.py --packet .` from this target directory.

All 36 author files and 12 public review files are preserved byte-for-byte. This wrapper and PUBLICATION_MANIFEST.json are additive. Raw source PDFs/images/text, imports, retrieval logs and review working notes are excluded.

Author head: 3a6e2e6ae4dbcf266140ae22a16f4b8d49de5a4e. Author manifest SHA256: 5bed4b4e5e34969f73a03505d5106eb008caaed3682511ba53edec253c449c7e. Review report SHA256: 6530678086401a52f8c3fbda889c7c12b9c16ba2a433aed8641e12bf06044307. Final review manifest SHA256: baea733124434dc16e1b8285f5ec8c32b0c662b17a8a4884d763cd7f35166f6c. The additive remote binding is retained with the original review manifest.

This is a scoped research checkpoint, not formal certification or human peer review. The original degree-five existence problem remains unresolved.
