# Primitive set saturation game audit

Target: 2355 / EP-872. Disposition: accepted prior asymptotic bounds with explicit local proof clarifications; a stronger lower scale is conditional, and linear versus sublinear growth remains unresolved by this work.

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and explicitly retained classical dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete seven-section mathematical reconstruction and exact rational certificate proof are retained, including all corrections, analytic formulas, rational endpoints, necessary finite examples, assumptions and limitations. Executable code, raw calculation outputs or coefficient arrays, datasets, copied source documents or text, source images and private coordination material are not distributed. Hashes authenticate bytes; they do not prove mathematical correctness.

Retrieval, inspection and numerical-execution statements describe the original audit of October 11, 2026 UTC and its authenticated earlier source inspection. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. References to code, receipts and their execution describe historical private verification; those artifacts are not distributed in this edition.

## Accepted mathematical results

The board is {2,...,n}. The combined selected integers form a divisibility antichain, play stops at maximality, and the score is the total number of moves. Prolonger maximizes the score and Shortener minimizes it. Write L_P(n) when Prolonger starts and L_S(n) when Shortener starts.

- Jonas Silva and GPT 5.5 Pro: liminf L_P(n)/(n log log n/log n) >= 1/2. The activation proof requires explicitly separating earlier Prolonger moves from earlier Shortener moves. The full corrected legality argument is retained.
- Om Buddhdev: limsup L_P(n)/n <= W4/2, where rho(u)=1/((floor(1/u)+1)u), J_r=(1/r!) integral over positive u_i with sum u_i<=1 of product rho(u_i), and W4=1-J1+J2-J3+J4. The reconstructed upper proof includes a precise queued-prime matching clarification and the correct almost-prime control of floor errors.
- The independently authored exact rational audit certificate gives W4/2 < 0.189741239716434 < 0.19. Thus L_P(n)<0.19n eventually. The same upper result extends to L_S(n) by the checked turn-count observation. No effective finite threshold is supplied.
- Buddhdev's complete earlier 1/8 lower-bound proof is also accepted, although the 1/2 bound supersedes its constant for the Prolonger-first convention.

The manuscript's tighter decimal 0.1897123371 and narrow component intervals were not independently certified. The independent certificate verifies the strict 0.19 threshold without executing or transplanting the author's numerical code or relying on its FFT error model.

## Conditional and unresolved conclusions

The n(log log n)^2/log n lower scale depends on two safe-edge hypotheses for the actual strategy-generated states: the activation hypothesis and the subsequent rank-three slot-game hypothesis. All permitted replies, including unscored edge deletions, must remain in those assumptions. The unrestricted safe-edge statement is false; the complete audit retains the weighted 135-versus-144 obstruction and the arithmetic K4 fiber on small primes 13,17,19,23.

The fixed-positive-fraction upper bound is not o(n), while the accepted lower bound is itself o(n). Neither establishes whether the game length is linear or sublinear. No equality L_P=L_S or transfer of the 1/2 lower constant to Shortener first is claimed. The original Erdős passage does not specify the starting player.

## Complete documents

- AUDIT.md preserves the entire seven-section mathematical reconstruction, all three local clarifications, the finite obstructions, formalization boundary, full acceptance ledger and numerical limitations.
- PROOF.md preserves the complete independent certificate proof: rational cell bounds, reciprocal breakpoints, the positive 18-term logarithm series and remainder, lower/upper simplex containments, carry-free 256-bit integer convolution, and the exact rational endpoint.
- ACCEPTANCE.md and ACCEPTANCE.json separate accepted, conditional, uncertified and unresolved statements and bind the distributed authored documents.
- SOURCES.json records public scholarly citations, inspected PDF/text identities, retrieval history and text/visual inspection scopes. VERIFICATION.json records bounded historical execution and byte-authentication metadata. MANIFEST.json lists exactly eight files and hashes the other seven; its digest is independently pinned in the publication description.

## Attribution and source limits

The main written sources are Paul Erdős, Some of my forgotten problems in number theory, Hardy-Ramanujan Journal 15 (1992), 34-50, printed page 47 (https://hrj.episciences.org/125); Om Buddhdev, Improved Bounds for the Primitive-Set Saturation Game (Erdos Problem 872), manuscript dated April 21, 2026 (https://www.sensho.xyz/papers/erdos-872.pdf); and Jonas Silva and GPT 5.5 Pro, A Dyadic Semiprime Lower Bound for the Primitive-Set Saturation Game (https://github.com/jonaslsaa/maths/blob/main/872.pdf).

The complete 51-page Buddhdev and five-page Silva/GPT note texts were read. Only the original Erdős target passage was audited. Text reading is distinct from visual inspection: the fresh audit visually checked Buddhdev pages 29 and 46 and Silva pages 2 and 4; earlier authenticated visual checks are separately recorded. Neither website hosting, PDF metadata dates, reported submission, nor reported finite Lean cores establishes peer review or an end-to-end formal proof. Standard PNT, Mertens, Chebyshev and fixed-r almost-prime estimates remain classical inputs. This edition does not reprove their full dependency closure or claim an exhaustive literature survey.
