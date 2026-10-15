# Acceptance and exact scope of the finite bound

12 October 2026. The independent mathematical audit accepts the following theorem: every ternary-digit or base-four-digit sign assignment, with every original factor present and all indicated digit signs free, has a total product coefficient outside \(\{-1,0,1\}\) at some degree \(1\le n\le150\,994\,944\). This bound is explicit and nonsharp. The [complete proof](FINITE_COEFFICIENT_OBSTRUCTIONS.md) and [full substantive review](REVIEW_FINITE_COEFFICIENT_OBSTRUCTIONS.md) accompany this acceptance.

## What is established

For \(n\ge1\), the proof obtains \(p(n)\le e^{3\sqrt n}\) from the elementary bound \(\log E(e^{-t})\le2/t\). Since every total coefficient satisfies \(|A_n|\le p(n)\), the squared-norm contribution above \(N_*=36\cdot2048^2\) is strictly less than \(2^{-73717}\) at each selected radius \(r=(b-1)/b\).

The exact radius denominators are
\[
\{2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048\}.
\]
The ternary upper envelope is \(1/(1-r^2)\). The base-four envelope uses the exact partition parity through degree 512 and a geometric upper tail starting at degree 513. Both may be enlarged by \(\eta=2^{-32768}\) under the finite good-prefix hypothesis.

The full truncation domains, including profiles never reached by the searches, give the ternary bounds \(K\le44\), \(S\le711\) and base-four bounds \(K\le33\), \(S\le902\). The base-four rational margin is strictly greater than \(2^{-31780}\); the ternary algebraic-norm margin is strictly greater than \(2^{-31318}\). Both exceed \(\eta\).

The enlarged tests retain precisely the same complete histories as the original searches. The historical direct exact replays and independent fresh sanitized replays confirmed complete-stream equality. The searches contain 831,371 ternary states and 11,151,089 base-four states. Their last nonempty levels are 58 and 76, followed by empty combined frontiers at 59 and 77. A hypothetical good coefficient prefix through \(N_*\) would yield a retained path through every searched level, giving a contradiction.

## Verification that supports acceptance

The independent audit checked the universal coefficient bound, analyticity without an infinite good-prefix assumption, persistence of block zeros with multiplicity, Parseval and Jensen applicability, all 21 tail and denominator bounds, the exact parity-envelope inflation, and both uniform strict-margin proofs. It verified the even golden-ratio power recurrence and its integer norm, although the final ternary separation does not require a bound on \(K\).

It also checked that replay changes were confined to the specified envelope inflation and output destinations. Coefficient recurrences, sign domains, stage choices, deferred choices, pool realization, active-zero selection and profile caching were unchanged. Every complete ternary frontier and the entire base-four tree matched the earlier accepted exhaustive data. Equal aggregate counts alone were not used to establish completeness.

Independent checks in normal Python and both optimized modes produced byte-identical reports. Four intentionally uncertified parameter choices were rejected. Both inflated programs were freshly compiled and executed with undefined-behavior sanitization and produced the same complete states and diagnostic output, with no sanitizer errors. These are the historical audit's results; preparation of this prose edition did not repeat the exhaustive enumerations.

## Dependencies and limits

Acceptance relies on the preceding independently accepted general-zero, full-ternary and full-base-four results. The full audit gives the dependency logic and preserves their original scope. The explicit finite bound is an additional theorem; it does not relabel either 59 or 77 as the largest possible good coefficient prefix or a sharp coefficient-only failure degree.

The result neither solves nor obstructs the arbitrary independent-sign partition problem. It does not prove that every product in either digit family has unbounded coefficients. No novelty, priority or unrestricted computational record is asserted. The review is independent AI-assisted verification, not external human peer review or proof-assistant certification.

The distributed [acceptance summary](ACCEPTANCE_REPORT.json) is descriptive, and the [manifest](MANIFEST.json) authenticates distributed bytes only. Programs, raw certificates and copied source documents are not part of this prose appendix.
