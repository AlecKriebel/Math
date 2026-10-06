# Final result: gap-one line configurations are ACM

Target 30002792 / OWR-13494-011. Status: `claimed_solved`, two recovered substantive research turns out of five, after separate full AI mathematical review. This is not human peer review, formal proof-assistant certification, or a novelty/priority claim.

## The answer

Over every algebraically closed field, a nonempty finite reduced union L of lines in projective three-space satisfying alpha(I(L)^(2)) = alpha(I(L)) + 1 is coplanar or a pseudostar. Hence it is arithmetically Cohen–Macaulay. The answer to Janssen's question asking for a non-ACM example is **no**.

Read [PUBLIC_TURN_2.md](PUBLIC_TURN_2.md) for the complete characteristic-free proof and [the independent final review](final_review/ADVERSARIAL_REVIEW.md) for adversarial verification. The central adjoint bound follows from surface resolution, Picard–Albanese geometry, the algebraic Hodge index theorem and Riemann–Roch. No characteristic-zero vanishing theorem is used in the final proof.

## Scope and history

The existing first-turn files, including README.md, are preserved byte-for-byte as a historical partial checkpoint. Their characteristic-zero limitation describes that earlier stage. The second turn explicitly closes the arbitrary-characteristic gap; this final README and final review give the current disposition. The original field convention, coplanar exception, reduced-union assumption, and credits for classical pseudostar/ACM results are preserved. The separate question about arbitrary reduced curves is not claimed.

No prior saved author-turn count was recovered; the ledger records two substantive recovered turns and does not claim unknown earlier work never existed. The current completion estimate is 100% of the stated proof target following separate AI review. That is a planning estimate, not a probability of correctness or a novelty certificate.

## Supplemental exact checks

From this directory:

    python final_review/check_small_characteristics.py --proof PUBLIC_TURN_2.md

The 3,888 assertions include 24 exact initial-degree examples over characteristics 2, 3 and 5, Hilbert–Burch minor identities, derivative-kernel boundaries and Riemann–Roch signs. These finite controls do not replace the geometric proof or its independent review.

Primary source: https://arxiv.org/pdf/1306.4387, section 1 field convention and Question 3.1; Oberwolfach printed page 514: https://ems.press/content/serial-article-files/46557 . See SOURCES.md and the final proof/review for attribution and exact auxiliary references. No external researcher was contacted, and no journal submission, merge, release or DOI publication is included.
