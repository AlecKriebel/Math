# Post-FIRST comparative check: even-crossing prior ingredients

ROOT suggested this comparative route after my sealed independent first conclusion and original v1 packet verdict. It is an additive post-FIRST check, not evidence for the earlier independence claim. FIRST_CONCLUSION and all four v1 packet inputs remain unchanged. The complete v2 packet is included in this final expanded audit.

**Verdict: the prior-ingredient corollary is correct for every classical knot diagram of even crossing count, including all small cases.** This does not authenticate an earlier explicit printed exact even formula or certify novelty of the tournament mechanism.

I independently downloaded Stoimenow, *Positive Knots, Closed Braids and the Jones Polynomial*, Ann. Scuola Norm. Sup. Pisa (5), II (2003), 237–285. I read the actual title and complete printed page 245 / PDF page 9 as text and pixels. Lemma 3.2 gives even intersection valence for any chord in a classical Gauss diagram and invokes the Jordan curve theorem. It has no positivity or bireducedness restriction. Those hypotheses occur in the separate following Lemma 3.3. [Primary repository PDF](https://numdam.org/item/ASNSP_2003_5_2_2_237_0.pdf).

An independent reason for the valence condition is that smoothing a chosen crossing splits the underlying immersed plane circle into two closed plane curves. Their mutual transverse crossings correspond precisely to chords intersecting the chosen chord. Two closed plane curves have an even mod-2 intersection count, by decomposing them into Jordan curves (or planar mod-2 homology). Thus every chord-intersection degree is even. The argument concerns ordinary classical plane diagrams and imposes no crossing-sign assumption.

Let m be the number of intersecting chord pairs in an n-chord classical Gauss diagram. The previously inspected Fiedler–Stoimenow formula (1), once per unordered subset, gives

    4|v3| = |vt3| <= binomial(n,3)+m.

Its triple supports are disjoint and have absolute weights at most 1. Its two-crossing support consists of intersecting pairs and has weight (wp+wq)/2, of absolute value at most 1. Hence the linked-pair total is bounded by m, rather than by all binomial(n,2) pairs. Arbitrary positive/negative crossing signs are allowed.

For even n>=2, every graph degree d_i is even and at most the odd number n-1. Therefore d_i<=n-2, and the handshake identity gives

    m = (1/2) sum_i d_i <= n(n-2)/2.

Consequently

    |v3| <= (1/4)[n(n-1)(n-2)/6+n(n-2)/2]
         = n(n-2)(n+2)/24
         = n(n^2-4)/24.

At n=2, no linked pairs or triples remain, so v3=0. At n=0, the empty diagram is directly zero. For n=2k the final expression is k(k-1)(k+1)/3, an integer. No flooring, minimality, positive-diagram theorem, or stronger page-8 extremality assertion is used. A finite exact-arithmetic table n=2,4,...,20 confirms the transcription; the universal argument is the displayed degree bound and algebra.

I read CURRENT_RESULT.md, CURRENT_PRIORITY_SPECIALIZATION.md, PR_BODY.md, DISPOSITION_PROPOSAL.json, and MANIFEST.json in the v2 directory completely. All four v2 pins match, all four v1 pins still match, and every pre-existing v1 disposition field is retained in v2. The three new flags appropriately record a checked even prior-ingredient corollary, no located earlier explicit even formula, and no established distinct tournament-mechanism novelty. No material repair is required. V2 also replaces the ambiguous “new tournament proof” phrasing with “alternate tournament proof,” resolving my optional v1 wording suggestion.

V2's authoritative created_utc in its manifest is 2026-10-04T17:18:53.219413+00:00. Its disposition's generic utc field retains the original v1 value 2026-10-04T17:01:43.157152+00:00; it must be understood as the original proposal timestamp, not the time the even corollary was checked or v2 created. This review does not invent or overwrite either value.

The assessed final v2 pins are:

- CURRENT_RESULT.md: 3385 bytes, `ae1b68f5b3cdefa3e6108c9c472758b6a0c305397a00645f00d9799d1fe7517d`.
- CURRENT_PRIORITY_SPECIALIZATION.md: 5802 bytes, `84da9d0f95477a21643d033ba360372078a9d2042df4f6d8deeefd3c837e4a33`.
- PR_BODY.md: 2295 bytes, `5ffeaba2aac0a5373f81a11c2ce947a4a64b785a9d9ef15b6d10ae38c5ddf0b8`.
- DISPOSITION_PROPOSAL.json: 1334 bytes, `1f0aa8a341379de386aa2019732431c9340366d4fc6791d7be48fc7fca08942f`.

The original-target prior implication remains independently supported by the earlier binomial display and normalization. This addition strengthens the attribution assessment of the even estimate without delaying or changing that verdict. Exact 2000 printed-body authentication, earliest priority, and tournament-mechanism novelty remain outside the affirmative conclusion. No promotion authority or native mutation is granted or recorded.
