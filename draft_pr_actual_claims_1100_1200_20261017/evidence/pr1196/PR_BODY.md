## Accepted restricted theorem

This authored edition proves a certifying halting algorithm for connected,
loopless directed-cycle block cacti with independent positive binary-encoded
weights on their cycle blocks. It uses O(n²) exact integer arithmetic
operations and polynomial intermediate bit length. Every independently
weighted bidirected tree is included. A bidirected triangle is excluded by
the exact block definition; arbitrary Eulerian multigraph halting remains
unresolved by this work.

The complete analytical algorithm and self-contained proof are included.
The halting certificate is a signed stable upper bound with a nonnegative
integer firing-bound vector, not a claimed reachable endpoint. The
nonhalting certificate is a nonnegative integrally equivalent configuration
and a legal once-per-vertex recurrent sequence. Signed least action,
Eulerian equivalence shifts, block-potential telescoping, both decision
directions, class recognition, O(n²) arithmetic counts, polynomial bit
bounds, and the literal degree-zero singleton convention are retained.
The excluded triangle's lattice obstruction and the exponentially long
terminating-play family are proved analytically.

No required mathematical correction was found. This edition applies the
optional precision: each unfinalized aggregate lies in [-C,N]; finalized
coordinates separately satisfy 0<=y_v<=d_v-1; all stored coordinates lie in
[-C,max(N,C)]. The theorem, hypotheses, algorithm and complexity are unchanged.

## Historical verification and distribution

Historical independent finite checks covered 177 weighted cacti, 1,208
complete fixed-total state spaces, 53,422 configurations, and 71,257 legal
transitions. They agreed with the candidate's 15,693 halting and 37,729
nonhalting outcomes, including 3,328 signed-root halting certificates.
Additional controls included 359 reduced-Laplacian solves, 18 root choices,
96 relabelings, 4,841 complete small-matrix recognition comparisons, and
inputs up to 24,001 bits. Normal, -O, and -OO outcomes agreed. The audit
used independently written checks and reviewed candidate code statically;
it did not execute or import the candidate implementation.

These are historical supporting checks, not omitted computational premises.
This is not a computational reproduction package. Exactly eight authored
proof/audit/acceptance/provenance/verification files are distributed. Programs,
raw certificate contents, copied sources, and private coordination material
are excluded. Preparing the edition performed no new mathematical test run,
scholarly-source retrieval, visual source inspection, or literature search.

## Sources and review limits

The public sources are Hujter–Kiss–Tóthmérész,
[*On the complexity of the chip-firing reachability problem*](https://arxiv.org/abs/1507.03209v4)
(Problem 22 versus prescribed-endpoint reachability in Theorem 11);
Björner–Lovász,
[*Chip-firing games on directed graphs*](http://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf)
(the multiplicity-dependent numerical firing bound); Farrell–Levine,
[*CoEulerian graphs*](https://arxiv.org/abs/1502.04690)
(the known unweighted directed-cactus subclass); and the retained
[EGRES Eulerian-multigraph halting question](https://oldlemon.cs.elte.hu/egres/open/Complexity_of_the_halting_problem_for_Eulerian_multigraphs).
SOURCES.json records public source identities and limited historical
reading and visual inspection. These sources supply context, not external
proof dependencies for the theorem here.

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI audit. No external human peer review, journal acceptance, formal
proof-assistant certification, novelty, priority, or exhaustive current
literature-status claim is made. The general Eulerian-multigraph target
remains unresolved by this work.

Only eight files are added under unsolved_math_prioritization/attempts/3000017.
QUEUE.md and all unrelated paths are unchanged.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,696 bytes; SHA-256 `03fb1ce0e7ba2fa9ae9eb3cfc8c5d09cd62e20cfc8274f0cec8946d3927d78a0`.
- `ACCEPTANCE.md`: 2,976 bytes; SHA-256 `75b0a22d8ea762a8afe746369a8ddf17e2efcc07286cb5842fd40c5f80ae05c8`.
- `AUDIT.md`: 15,457 bytes; SHA-256 `a511863935ab8d93ecff3f49ceec1f8dc7f606f24b40dcd500c1e062f9c68064`.
- `MANIFEST.json`: 1,379 bytes; SHA-256 `5e00b3ab8019f33c5a0756ebcd0d9a39cc996abc726209833e4216406e0a3d04`.
- `PROOF.md`: 17,091 bytes; SHA-256 `adebf5499e75c44887a6a60b3976522b540803afdd17d3df6f473664363ec525`.
- `README.md`: 2,548 bytes; SHA-256 `22d0b0713e93d871c1c11af06973e7bda7035caae1ae21eaf7c5f286c8a5b3e2`.
- `SOURCES.json`: 4,664 bytes; SHA-256 `11ef92942c3db31b9c330b4bb80c6d258bce51f6bf8e83d22657d2e318f3060c`.
- `VERIFICATION.json`: 6,090 bytes; SHA-256 `bcb3216d77470566675985880ba2e9e720fa9f40ca26cec5ae7e7186cd5a29ec`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

