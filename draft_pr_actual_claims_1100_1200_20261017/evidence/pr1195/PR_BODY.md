## Accepted restricted-class result

This corrected authored edition proves

    h_out(n) - log_2 n -> infinity,

where h_out(n) is the minimum excess |E|-n among outerplanar pancyclic
n-vertex graphs. The weighted-tree theorem is complete: interval-complete
positive-integer weighted trees satisfying w(v)>=deg(v)-2 and W->infinity
have W/2^q->0. Its proof retains the centroid/matching bound, bounded
nonleaf core, finite-coordinate subsequence extraction, fixed-M choice,
and collision argument. The polygon-dissection reduction, face-weight
identities, cycle-to-connected-face direction, and minimizer quantifier
for every n>=3 are included.

For star weak duals and every integer k>=3, the edition proves
n<=4k^2-19k+34 and supplies the explicit algebraic construction
n=4k^2-19k+31 with excess k. Central and leaf weights, adjacent subset-sum
intervals, simplicity, all cycle lengths, and the k=3 empty-list endpoint
are fully proved. These results identify the leading coefficient 4 in
that subclass, not its exact finite extremum.

## Internal candidate correction

The unpublished internal candidate's c=k substitution was k^2+6; the
correct expression is k^2+4. The corrected successive differences are
2(k-3)(k-4), (k-2)(k-3), and (k-1)(k-2)/2. At k=3 the four bounds are
13,13,13,12. This repairs the endpoint argument without changing the final
theorem, construction, hypotheses, or integer-k range. AUDIT.md explains
the correction completely. The Erdős title's omitted word “Some” was
also restored. No published paper is alleged to contain either error.

## Proof and verification boundary

The complete mathematical proof is self-contained. Finite exact controls
are supporting validation, not omitted premises. All 1,442 labelled trees
through order 6, 40,780 weighted assignments, 1,122,150 selected-subset
collision inequalities, and 5,439 noncrossing polygon dissections through
order 9 were checked independently. Of the weighted assignments, 40,375
satisfy the degree condition and 14,913 of these are interval-complete.
Constructed star graphs were checked for k=3,...,11; corrected arithmetic
was checked for k=3,...,10,000. The all-k result follows from the written
factorization rather than the finite test interval.

Independent normal, -O, and -OO runs passed with byte-identical substantive
receipts. The independent checker was derived from definitions using
labelled edge-set enumeration and cycle-space parity enumeration, without
reusing, importing, or executing candidate code. Negative controls tested
removed structural assumptions, loss of integrality, and malformed graphs.
Raw code, certificate contents, and copied source documents are omitted.
This edition is not a computational reproduction package. Its universal
results rest on the complete written proofs.

## Sources and remaining gap

P. Erdős, [*Some Unsolved Problems in Graph Theory and Combinatorial Analysis*](https://www.renyi.hu/~p_erdos/1971-25.pdf)
(1971), Problem 10, printed page 101 / PDF page 5, supplies the original
unrestricted divergence question. Sean Griffin,
[*Minimal Pancyclicity*](https://arxiv.org/abs/1312.0274), arXiv:1312.0274v1
(2013), supplies the standard lower bound h(n)>=log_2(n-1)-1 and the binary
log-star convention. These are context sources, not external proof
dependencies for the results proved here. SOURCES.json records retained
PDF identities and historical reading/visual inspection. Preparing this
edition performed no new scholarly-source retrieval, visual inspection,
literature search, or mathematical experiment.

The unrestricted crossing-chord divergence question and coefficient-one
log-star lower bound remain unresolved by this work. No novelty, priority,
or exhaustive literature-status claim is made. This AI-assisted work is
unrefereed. Acceptance means an independent internal AI audit. No external
human peer review, journal acceptance, or formal proof-assistant
certification is claimed.

Only eight authored proof/audit/acceptance/provenance/verification files
are added under unsolved_math_prioritization/attempts/2440. QUEUE.md and
all unrelated paths are unchanged. Private coordination material is excluded.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,567 bytes; SHA-256 `4d736816fd2dd6466ec3a0f5baf8a527c9122e1c6dba3be043500dedce164b2c`.
- `ACCEPTANCE.md`: 4,768 bytes; SHA-256 `c148d27a8b697ac0d983fd2eb07746831f18ccad37d08ab54331fb060ffbcc5f`.
- `AUDIT.md`: 18,549 bytes; SHA-256 `cf110440dec9d45148c9b69f0bff379f2d021f38efef1cb8d8859bee159fe1d9`.
- `MANIFEST.json`: 1,367 bytes; SHA-256 `6b924d4cf231f57875477ea28377d534ed72923404ad13f91cef0afd4e7c9584`.
- `PROOF.md`: 17,022 bytes; SHA-256 `41fe9a4344c79885c63439aa058b962ae12da44e64523a409854067781e56fad`.
- `README.md`: 2,221 bytes; SHA-256 `78cf31d811a698fafb92d3424ddb06827f9cc1cbd6ceb1df111af70751503170`.
- `SOURCES.json`: 3,811 bytes; SHA-256 `dcbadcfc1f9a36e0077419e5d609bc6ffb16fa064ac53529d3a7c523d5f56189`.
- `VERIFICATION.json`: 3,475 bytes; SHA-256 `879421cfde9b17abbae217502b87d5c551230462cad91133604306482d595669`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.

