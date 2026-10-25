# Page-12 interpretation note — not a substantive defect disposition

The initial broad reading of the sentence after Theorem 12 produced a valid counterexample to a stronger necessity statement. The contextual reading below withdraws the provisional DEFER. Full analytic review subsequently resumed and is completed in `REVIEW.md`. The chronological research log preserves the earlier decision and its correction; the current disposition is PASS within the paper's stated scope.

Exact publication binding: main PDF SHA256 `7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f`, p.12; main TeX SHA256 `e4876619a27cdd7e91e051c89b0827da418d6d201a40400c2bc3c31e2f1f9a9a`, lines 414–422. The paragraph follows Theorem 12 and equation (17).

The displayed ansatz is

`U=(1,b*tau,b,tau), V=(1,b,b*tau,tau), S=(1,kappa*d,d,e), T=(1,d,kappa*d,e)`.

Under **general** core factorization, tau=1/3 does not force e/d=6/5. Let h>0 satisfy 5h⁴=1, and take b=h, kappa=3h², d=e=1/4. Set

`P=(1,(5h³+h)/4,(5h³+h)/4,h²)` and `B=(1,h²/2,h²/2,5h²/12)`.

Then all sixteen equations `M_yz=P_(y+z)B_yB_z` hold exactly with e/d=1. With the paper's common K and topology, all edge eigenvalues, transition entries and leaf probabilities meet the strict stochastic conditions. `counterexample_ratio.py` verifies 225 exact assertions without importing published code or certificates. Structurally, rescaling the common T-character value e in S and T can be absorbed by rescaling B_T, so unconstrained factorization cannot determine e/d.

The **strongest plausible contextual reading** retains equation (17)'s equal nontrivial B entries. On the stated positive branch, `M_CC=4d²/5` and `M_TT=5e²/9`. Equal B_C and B_T imply equal diagonal entries, hence `(e/d)²=36/25` and therefore e/d=6/5. The preceding displayed B makes that restriction available in the published context.

The broad-reading counterexample is a precision/boundary note, not a refutation of the selected witness, Theorem 12, or subsequent rank, continuation and grafting conclusions. Full review independently verifies those conclusions. The result JSON's original mathematical-check labels must be read with this qualification. No alternative publication construction or paper repair was attempted.
