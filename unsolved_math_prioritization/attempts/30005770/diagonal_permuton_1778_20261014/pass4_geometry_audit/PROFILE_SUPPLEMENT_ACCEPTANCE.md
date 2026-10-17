# Review of the final two-ended and small-width profile supplements

Shared PASS4, 14 October 2026. Accepted proof pins:

- `pass4_adaptive_profiles/TWO_ENDED_CERTIFICATE_OBSTRUCTION.md`: `94f85ecc86ea8d2e43b2009751be442c0a1a986677d82c5a7c0425566b89229f`.
- `pass4_adaptive_profiles/SMALL_WINDOW_TRUE_GAPS.md`: `997f5b9f8f5bc95a6459e7fb8a8154e648572e45dc8588d06e5a63398a791b13`.

**Both supplements are accepted within their deterministic scope.** No new canonical realization is required; they use the already accepted finite increasing-state mountains.

The symmetric ratio-two test vector has total weight T_(2h)=2(2^h-1) or T_(2h+1)=3*2^h-2. Every nonendpoint directional penalty is negative, while an endpoint realizes gamma/T_K. Thus the displayed upper envelope on the two-ended certificate is valid, including K=1 and K=2.

For a centered mountain window, balancing its two extents minimizes s=2^(-u)+2^(-v); the function s/(3-s) is increasing. The exact minimum boundary ratio is therefore 2H(1/2)/T_K. It strictly exceeds the certificate because 2H(1/2)>gamma. A one-sided window retains an inward neighbor twice its endpoint, even under outward clipping, and has ratio greater than H(1/2)>gamma. Thus every bounded-width location is covered. Appending zeros cannot increase the two-ended minimax, so the larger-cap statement is also valid.

For the true one-cell gap, the accepted exact growth g_1=4 and primary lambda<=27/2 give delta_1<=log(27/8). Every mountain singleton has boundary ratio at least 2H(1/2)=log(27/4), leaving margin at least log 2. This includes terminal singletons, whose inward edge alone supplies that cost.

For width two, a centered window has exact ratio H(1/2), and a one-sided window has ratio at least (4/3)H(1/2), even with outward clipping. Both exceed log 2, which bounds the true delta_2 using the independently accepted g_2=27/4. The m>B and B>=2 qualifications ensure the centered neighbors exist whenever that case is used.

These conclusions may be combined with the two-ended certificate at larger widths. They do not upper-bound the true delta_K at every K>=3, disprove the conditional divergence criterion, or give nonnegligible uniform probability to the mountain family. The existing exact-law and canonical input pins remain unchanged.
