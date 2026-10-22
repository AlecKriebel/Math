# Historical verification and edition limits

## Historical finite checks

The bounded audit's exact-integer/fraction checker completed normal Python, -O and -OO runs on 10 October 2026. Each reported PASS. All three retained output files are exactly 7,049 bytes with SHA-256 aea72257d458d534c9d19563dad88128163f675e3c677466cb5c99575b04a43f. Their byte equality and hash identities were checked again during edition preparation. The mathematical programs were not rerun during preparation.

The construction checks cover k=1 through 300 and six bases immediately above the stated threshold, for 1,800 sequences. A separate small-base range B=1 through 6 and k=1 through 80 checks 18,960 neighboring residue-layer pairs. The quadratic identity is tested in 45,150 cases. Exhaustive valid increasing-subset enumeration covers n through 22; direct subset enumeration independently agrees with incremental enumeration through n=10. The exact finite upper inequality is checked on 6,082,589 instances, for R=1 through n+3. The layer inequality is checked on 1,643,662 instances using half-integer endpoints in [0,n] for n through 10. Top-interval admissibility has 414 checks. Negative controls reject repeated singleton sums and detect sorting-induced collisions.

These are finite regression checks, not formal certificates. The historical implementation uses explicit runtime conditions rather than Python assertions. No source-supplied code was executed in the bounded audit. No Lean build or other proof-assistant verification is claimed.

## Mathematical and source scope

The infinite conclusions rest on the complete written elementary proofs in AUDIT.md. Finite checks cannot establish the limiting claims on their own. The exact target includes all nonempty consecutive blocks, singleton blocks, overlapping positions and collisions across lengths. Weakly increasing valid sequences are therefore automatically strictly increasing.

All five pages of the identified prior manuscript were text-read and visually inspected during the audit. Source metadata distinguishes full manuscript inspection, decisive original problem pages, abstract-only checks and bibliographic-only checks. CP96's increasing-order abstract supports f, while its attribution to arbitrary-order g remains unverified, not disproved. Its full proof was not inspected. Direct EP357 tracker access returned HTTP 403, so no fresh tracker-status claim is made. Edition preparation adds no scholarly-source retrieval or inspection.

## Distribution boundary

This edition contains the full authored proof reconstruction, audit and acceptance, plus public citations, PDF identities, retrieval/inspection history and aggregate historical verification metadata. It excludes programs, raw datasets, detailed outputs and witness lists, certificate contents, copied source documents or source text, private sources, private personal data and private coordination material. Readers can inspect or independently reconstruct the mathematics, but cannot execute the original finite checks from this prose-only edition alone.

The original audit's mathematical arguments and limitations are preserved. Only edition/review framing and historical-check references changed. Acceptance applies to credited prior partial bounds; f(n)=o(n), the order of growth of f, and a claim f(n)~n/2 are not established.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance here means the bounded mathematical assessment described below. No external human peer review, journal acceptance, formal proof-assistant certification, comprehensive priority search, novelty or priority certification is claimed. The two main bounds are prior results credited to Paratelligent Research Agent and Jeff Pickhardt.
