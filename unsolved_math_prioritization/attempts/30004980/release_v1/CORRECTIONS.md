# Corrected release v1: localized wording and attribution repairs

Original frozen commit: ab502620095141f19e983d835c5ca3ac885ed21c.
Original manifest SHA-256: 67aa8bdbea3c4991d4206978fd5944dc3ae822b47b8198f615adc872e2383756.

The original 17-file package remains unchanged. This is a separate corrected copy responding to the independent audit's H1 hold. The exact target remains unsolved after five substantive attempts. These edits are corrections and attribution, not a sixth proof-search turn.

## H1: own endpoints excluded

Attempt 2 now explicitly defines D_i using vertices outside P_i. The original wording could include both endpoints of an adjacent pair; K2 would then wrongly give an initial disagreement size 2 when the contraction actually creates no red edge. The corrected definition gives 0. The implementation already excluded both endpoints, so all existing program and output bytes are unchanged.

## Bundled clarifications

- The numeric base size is h_i, avoiding reuse of b_i as both an endpoint and a scalar.
- The empty maximum over pair-orbits is 0, making the n=1 case explicit.
- Ahn, Hendrey, Kim, and Oum, v2, Lemma 4.3 is directly credited for the existing additive pair-scheduling mechanism.
- Kajal Das, arXiv:2309.05297, is cited for the existing six-vertex upper bound 2. The small-order computation remains a reproduction, with no novelty claim.

README, the research log, and the bibliographic source manifest reflect these corrections. The five attempt count, all source-file hashes, every solver/check script, and all four generated result files are unchanged. This corrected copy requires narrow re-review; it does not inherit a full PASS from the original HOLD report.
