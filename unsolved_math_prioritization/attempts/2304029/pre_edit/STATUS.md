# Function Theory 4.29: prior-resolution verification

## Conclusion

The conjecture in target 2304029 (catalog rank 678) is a previously disproved conjecture, not an unresolved problem suitable for a new-solution claim. Moshe Roitman's 1983 paper is the directly matching prior result. This packet verifies the attribution and exact statement match. It does **not** claim that the complete construction in the paper has been independently replayed.

## Exact scope

The target concerns monic complex polynomials P and Q. The zero sets of P and Q must agree, and the zero sets of their first derivatives must agree. These are sets: root multiplicities are not required to agree. The proposed conclusion is P^m = Q^n for some positive integers m,n.

Monicity matters. Without it, multiplying one polynomial by an arbitrary nonzero constant would give irrelevant normalization counterexamples. Roitman's reported witnesses are stronger than the target requires: they are monic and have integer coefficients. The claim therefore matches the complex-polynomial target with no change of field or normalization. A counterexample also excludes P^m = c Q^n with c nonzero: comparison of leading coefficients forces c=1.

## Verified evidence

1. Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2 (2018), printed p. 80. The statement of Problem 4.29 and its update are on the same page; the update attributes a counterexample to reference [669]. The page was read in text and visually inspected. Reference [669] identifies Roitman's paper below. The 2018 source describes itself as a draft.
   - https://arxiv.org/abs/1809.07200v2
   - https://arxiv.org/pdf/1809.07200v2
2. Moshe Roitman, *On Roots of Polynomials and of their Derivatives*, Journal of the London Mathematical Society (2) 27(2), 248–256 (1983), DOI 10.1112/jlms/s2-27.2.248. Its publisher abstract states the existence of monic integer polynomials with the required equal zero sets and no positive-power equality.
   - https://doi.org/10.1112/jlms/s2-27.2.248
   - https://academic.oup.com/jlms/article-abstract/s2-27/2/248/814337
3. The article transcription linked from Moshe Roitman's public Academia profile explicitly connects its Theorem 8 with Problem 4.29. This supports theorem identification, but missing or damaged displayed formulas prevent treating the transcription as a fully inspected proof.
   - https://independent.academia.edu/RoitmanMoshe
   - https://www.academia.edu/112407536/On_Roots_of_Polynomials_and_of_their_Derivatives
4. The University of Haifa institutional publication record independently confirms the article's bibliographic identity and publication status.
   - https://cris.haifa.ac.il/en/publications/on-roots-of-polynomials-and-of-their-derivatives/

## Proof-verification boundary

No complete original-paper PDF was obtained. The publisher displayed an access restriction; no login or paywall bypass was attempted. The author-linked public transcription was read, but its construction formulas are incomplete. An institute-hosted exposition returned HTTP 403 and was not retried through a bypass. A separately author-linked book endpoint encountered a certificate-validation failure; no security override was attempted. An accessible book transcription merely referred readers back to Roitman and did not close the construction gap.

An exploratory attempt to reconstruct a rational witness from the surviving formulas did not yield a certified counterexample. Numerical feasibility output was never accepted as proof: one approximate feasible output failed exact rational consistency. No purported witness is included.

`verify_factored_witness.py` is an exact algebraic verifier for future rational-factor witnesses. Its self-tests pass; this only validates the verifier on the stated tests, not Roitman's construction.

## Recommended disposition

Record the target as **prior-resolved: counterexample by Roitman (1983)**, with **exact target match verified; full proof/construction replay not completed**. Do not describe this packet as a new proof, a reproduced explicit witness, or a complete source-proof audit. The selected catalog record was checked against the primary target statement; no complete upstream-corpus match is claimed.

This is a fresh reconstruction, not recovery of the lost earlier audit. The source audit gives the bytes actually inspected in this pass. Only authored analysis, verification code, and public metadata are in this public directory.
