# Source and prior-attempt audit

## Exact target and model

The authoritative problem is David Aldous's [one-dimensional drift-jump particle process](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html), posted February 2018, read October 1, 2026. Its finite-k system has strictly positive ordered positions, drift equal to position, and unit-rate space-time events moving the nearest particle to their right, if one exists. Finite-k events beyond the last particle are ignored. The request is for a fairly explicit stationary distribution. It is not a request only for existence, asymptotics, first marginals, or a simulation. Consistency in k is part of the page.

The queue's AMR-096-0040 / numeric9700040 is this exact model. The pinned UnsolvedMath revision is 37e53eabe540fb458758e198be61634bd02ee008. The imported upstream research report is source triage rather than an earlier campaign proof attempt. Its claimed lack of a published description is not treated as proof of novelty.

The finite-k source statement, rather than its introductory discussion of another Hammersley process, fixes the target here. All rates are exactly one, with no tunable reinforcement, immigration or random-walk convention.

## Classical primary inputs and credits

1. Aldous–Diaconis, *Longest increasing subsequences: from patience sorting to the Baik–Deift–Johansson theorem*, Bulletin AMS36 (1999),413–432. [Author PDF](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf). Section1.1 gives the pile-top/LIS identity. Section2.1, especially Proposition4 on printed419 and the preceding bijection on418, gives RSK and the first-row/LIS identification. Section5.2 on427 discusses the fixed-left-pile process and already gives c(1)=1,c(2)=e−1. These are classical inputs, not new campaign results.
2. Aldous–Diaconis, unfinished unpublished1993 notes, [author PDF](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf). Section4.1, printed36–38: model; equation(42) already represents stationary positions as independent Poisson arrival times at limiting pile-top ranks B(i); Lemma33 already supplies synchronous-coupling uniqueness. Section4.2, printed39: equations(45)–(48) already give the two-particle law. The proof rederives the exact coordinate transformation and does not rely on the rough draft's balance equation or unproved draft placeholders.
3. Okounkov–Reshetikhin, *Correlation function of Schur process with application to local geometry of a random 3-dimensional Young diagram*, JAMS16(2003),581–603; inspected [arXiv v3](https://arxiv.org/pdf/math/0107056v3). Section2.2.4, equation(7), gives the skew Jacobi–Trudi determinant in a complete-symmetric specialization; equation(8) the containment condition. The general Schur-process framework supplies context. Our particular finite joint weights are proved directly by finite RSK counting, not asserted from an unidentified kernel theorem.
4. Betea–Boutillier–Bouttier–Chapuy–Corteel–Vuletić, *Perfect sampling algorithms for Schur processes*, Markov Processes and Related Fields24(2018),381–418. [Author-hosted published PDF](https://www.math.umb.edu/~vuletic/Site/Research_files/PSASP.pdf). Section6.3, printed415, equation(6.6) gives exponential specialization s_(lambda/mu)=t^d f^(lambda/mu)/d!; pages415–416 discuss Poissonized RSK. Combined with item3 this gives PROOF.md(1)–(2).
5. Aldous–Diaconis, *Hammersley's interacting particle process and longest increasing subsequences*, Probability Theory and Related Fields103(1995),199–213. [Author PDF](https://www.stat.berkeley.edu/~aldous/Papers/me71.pdf). Historical/model context only; no new theorem in the packet depends on a difficult-to-extract scan of this paper.

The point process constructed in PROOF.md is related to Poissonized Plancherel growth through an exact finite-rectangle identity. It is not identified with the ordinary spatially stationary Hammersley Poisson configuration or with a later local multi-line scaling limit. Those have different processes or normalizations.

## Prior campaign and status gate

Checks on October1,2026 before publication: all-state repository PR searches for numeric9700040 and the drift-jump stationary title returned no result; branch search for9700040 returned none; main history of attempts/9700040 was empty. Local recovered all-ref searches likewise found no exact earlier target. These bounded searches support starting this campaign attempt, not an exhaustive historical-literature claim.

The source page still presents the problem as open. Targeted current searches for the exact page/model and drift-stationary-Schur combinations did not locate a primary publication explicitly closing the source question. No claim that the answer is historically new follows. The result is presented as a classical consequence with a source-scope check: a positive, fixed-matrix-size determinant series for all finite joint probabilities and certified rational error may meet the descriptive request, but an independent reviewer must assess that, separately from the formula's correctness.

Source PDFs, full text, screenshots and imported full records are reading copies outside this public packet. source_manifest.json records their public URLs and hashes without redistributing them.
