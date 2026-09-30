# 3800014: all shortest exact-count intervals

[KNOWN_ALGORITHM.md](KNOWN_ALGORITHM.md) gives a complete O(n²/log(2+n)) real-RAM algorithm, recovering the source's requested faster-than-quadratic alternative from the established2006/2014 min-plus-convolution method. The supplied implementation retains interval witnesses and handles repeated coordinates and infeasible exact counts.

This is a **credited known resolution**, with1/5 validation/reconstruction families recorded. No genuinely polynomial subquadratic bound, superlinear lower bound, bit-time speedup or novelty is claimed.

- 10,388 exact assertions pass:845 interval implementation runs,192 generic min-plus runs and41 dominance instances
- algorithm.py implements the reconstructed dominance method using exact scalars when provided
- Run verify.py with Python3's standard library to print the receipt
- The asymptotic bound is proved analytically, not inferred from benchmark timing
- Separate adversarial review pending; no human peer review
- The coordinating task owns queue changes
