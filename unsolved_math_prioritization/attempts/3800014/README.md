# 3800014: all shortest exact-count intervals

[KNOWN_ALGORITHM.md](KNOWN_ALGORITHM.md) gives a complete O(n²/log(2+n)) real-RAM algorithm, recovering the source's requested faster-than-quadratic alternative from the established 2006/2014 min-plus-convolution method. The supplied implementation retains interval witnesses and handles repeated coordinates and infeasible exact counts.

This is a **credited known resolution**, with 1/5 validation/reconstruction families recorded. No genuinely polynomial subquadratic bound, superlinear lower bound, bit-time speedup or novelty is claimed.

- 10,388 exact assertions pass: 845 interval implementation runs, 192 generic min-plus runs and 41 dominance instances
- algorithm.py implements the reconstructed dominance method using exact scalars when provided
- Run verify.py with Python 3's standard library to print the receipt
- The asymptotic bound is proved analytically, not inferred from benchmark timing
- Separate adversarial AI review passed: [report](review/REVIEW.md), including 22,962 independent exact controls; no human peer review. The frozen proof’s earlier review-status header is superseded by this record
- The coordinating task owns queue changes
