# Source, literature, and prior-work gate

Checked 2026-10-01; base main commit `2216543dd372ed5afd41f67da7ad638edf3d339f`.

## Prior work

- The campaign inventory records rank 281, status queued, 0/5, and no known prior user/campaign work. Its own qualification that this is not an independent proof of untouched status is retained.
- A fresh all-state GitHub PR search for the numeric ID, exact title, and source code returned no matches. A matching branch search returned none. The target attempt path has no remote main commit history and no local all-ref history.
- The queue row is queued, 0/5. Related-target groups contain no entry for this ID. No QUEUE generator was run and no shared main file was changed.
- The complete pinned record and its embedded 22 August 2026 literature triage were read. No separate `research_results.json` entry exists for this source code; that absence is not presented as a missing proof artifact.
- The individual review in `review_v2/reviews_5.json` recommends a summable infection-ray construction while warning that recoveries and fitness dependence must be controlled. It is a route suggestion, not a previous mathematical attempt or proof certificate.

## Primary literature checked

1. Official OWR PDF, full pp. 618–620 read; p. 619 rendered and visually verified. Exact model and question are recorded in TARGET.md.
2. Cardona–Tobón–Ortgiese, arXiv:2110.14537v4 (14 July 2026), full 41-page author manuscript. Definition 2.1, pp. 3–4, allows joint offspring/fitness laws and contains the original constant-fitness case. Section 3 gives the graphical construction. Theorem 3.2, p. 11, explicitly assumes finite offspring mean and proves that finite initial infections remain finite at all times. The page was visually verified. Published online 13 July 2026 in Advances in Applied Probability, DOI 10.1017/apr.2026.10066; the publisher's primary listing confirms the date. We did not need to assume that its broader fitness hypotheses were present in the 2022 question.
3. Bartha–Komjáthy–Valesin, Degree-penalized contact processes, Forum of Mathematics, Sigma 14 (2026), e6, full 85-page publisher PDF. Definition 3.1 and equation (19), p. 17, define the process via finite infection paths and allow explosion; visually verified. Definition 6.1 and Proposition 6.2, pp. 46–48, use downward infection rays with increasingly large degrees to prove global survival for heavy-tailed offspring. Their ray mechanism is credited; the proposition is not cited as a stated simultaneous-infection explosion theorem. The explicit time/recovery windows in PROOF.md establish that additional conclusion directly.

Fresh searches for contact-process explosion, infinite mean, and Galton–Watson trees found these relevant primary inputs. General explosive branching processes and first-passage percolation alone do not settle the recovery issue. The search is not a proof of novelty or of the absence of some earlier formulation.

## Readiness

The exact source question is available. There is no missing-data blocker. A complete first-turn candidate is frozen for independent review. No final status promotion or PR is justified until that review passes. The candidate is a source-scoped affirmative existence result with explicit classical-method credit and no novelty claim.
