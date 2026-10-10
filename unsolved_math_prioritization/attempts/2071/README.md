# EP357: audit of prior distinct-block-sum partial bounds

Problem 2071 / Erdős Problem 357. For strictly increasing positive integers a_1<...<a_k<=n, every nonempty indexed consecutive block sum must be different. Let f(n) be the maximum k. Singleton blocks are included, and overlapping intervals and different block lengths are all compared.

The prior five-page manuscript by Paratelligent Research Agent and Jeff Pickhardt is accepted within this bounded audit for:

- liminf f(n)/sqrt(n) >= 4/sqrt(3)
- f(n) <= ceil(n/2)+floor(n/(2R))+R(R-1)/2 for every positive integer R
- consequently f(n) <= n/2+((3/2)2^(-2/3)+o(1))n^(2/3)

The residual f(n)=o(n) question is not established. No order-of-growth determination or f(n)~n/2 claim is made. These are credited prior partial results; this edition does not claim a new bound.

## Reading guide

- AUDIT.md: full elementary reconstruction of the lower construction, all-n limit passage, layer-packing lemma, exact finite upper bound and asymptotic coefficient, with historical-source and hypothesis qualifications
- ACCEPTANCE.md and ACCEPTANCE.json: exact accepted scope, prior attribution, exclusions and audit identity
- VERIFICATION.md and VALIDATION_SUMMARY.json: historical finite-check methods, aggregate counts, match results and reproduction limits
- SOURCE_METADATA.json: public scholarly-source titles and URLs, PDF hashes and sizes, authorship/date distinctions, and precise retrieval and inspection limits
- MANIFEST.json: exact eight-member inventory, hashing the other seven files; its own digest is pinned separately to avoid self-reference

The inspected Coppersmith–Phillips 1996 abstract assumes increasing order and supports f. Its application to arbitrary-order g is unverified, not disproved; the full CP96 proof was not inspected. No CP96 theorem is needed by the accepted main proofs. Weak increase plus uniqueness of every singleton already forces strict increase. Dropping order genuinely changes the class.

These AI-assisted authored documents and their independent internal AI audit are unrefereed. Acceptance here means the bounded mathematical assessment described below. No external human peer review, journal acceptance, formal proof-assistant certification, comprehensive priority search, novelty or priority certification is claimed. The two main bounds are prior results credited to Paratelligent Research Agent and Jeff Pickhardt.

Historical computational checks were completed on 10 October 2026. The three normal/-O/-OO outputs all passed and agree byte for byte. Edition preparation rechecks retained output identities but does not rerun those programs or inspect new scholarly sources. Full mathematical arguments are present; this is not an executable reproduction package.

Only authored mathematical audit/acceptance prose and public citation/verification metadata are included. Programs, copied third-party source documents or source text, raw datasets, detailed output files, certificate contents, private sources, private personal data and private coordination material are excluded. The additions-only proposal changes no existing repository file, including QUEUE.md. No release or DOI is created.
