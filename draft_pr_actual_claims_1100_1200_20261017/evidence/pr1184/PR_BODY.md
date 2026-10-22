## Accepted prior fixed-r matching order

The prior STARFLEET Math result for Erdős Problem 538 is accepted as a
conventional mathematical proof. For every fixed integer r>=2,

    E_r(N)=Theta_r(log N/log log N).

E_r(N) maximizes S(A)=sum_{a in A}1/a over positive a<=N, with at most r
ordered pairs (p,a), p prime, a in A, m=pa, for every integer m.
The cap includes products above N. Arbitrary admissible sets need not be
squarefree; squarefreeness is used only in the constructed lower witnesses.
This is an audit of a prior public claim, credited to STARFLEET Math, with
no novelty claim.

The accepted finite inequalities are

    log(log(N+1)) S(A) <= 2r(1+log(N^2)), for r>=2 and N>=2,
    log(N+1) <= 4+8192(ell(N)+1) S(A_N), for every natural N,

where A_N has global cap two. Put L(0)=0, L(N)=floor(log_2 N) for N>=1,
and ell(N)=floor(log_2 L(N)) when L(N)>=1, otherwise ell(N)=0.
All unsubscripted logarithms are natural. No real logarithm of zero occurs.
The lower witness also applies to every cap r>=2. No sharp finite extremum,
sharp leading constant or matching growing-r dependence is established.

Sources: [STARFLEET Math, section 10](https://www.starfleetmath.com/),
[verification archive](https://www.starfleetmath.com/downloads/verify/erdos-538/erdos-538-solution.zip),
and [Erdős, Problems and Results on Combinatorial Number Theory (1973),
section 4, printed p.124, equation (4.5)](https://www.renyi.hu/~p_erdos/1973-21.pdf).

## Complete written audit and focused independent check

AUDIT.md retains the complete primary general derivation: incidence upper
bound; favorable-child bijection; exact 1/q^2 outside danger fraction;
one common safe palette; odd-characteristic isotropic-plane cap; weighted
rainbow transfer; all repeated-color patterns; squarefree and nonsquarefree
products; the k=1 endpoint; exact Omega-layer union; harmonic truncation;
the coefficient 8192; and fixed-r asymptotic deduction.

FOCUSED_AUDIT.md independently retains the complete safe-kernel lower-bound
and all-m transfer proof, including common-labeling and unit/tail details.
Its accepted scope is focused; the upper estimate is outside that second
review. No mathematical correction was needed for the accepted scope.

Optional primary finite toy examples, numerical computational witnesses and
finite test ranges are omitted; historical-check wording and one metadata
filename are clarified. These edits are editorial only. All general
mathematical arguments, theorem constants, quantifiers and boundaries remain.
No new proof attempt or publication-stage mathematical tests were made.
Historical independently authored exact checks passed normal/-O/-OO modes
with byte-identical outputs; finite checks do not prove universal results.

## Formal evidence and review boundaries

The archive READMEs point to an absent experiment_1_formal_statement path.
The actual pinned statement is under experiment_24_safe_kernel_arithmetic:
Problem538.lean is 1,923 bytes, SHA-256
`2095828c87994722fc02195edfd08c5a89e9768f96d2a9e7b02a86e4ca5177c3`.
The final Proof.lean and FinalMatchingOrder.lean are byte-identical,
1,656 bytes, SHA-256
`3edd0e3113677c0f3490df253ed93b3f09b0f8b7956bd6aead86a31a5e13f35e`.
The website's schematic signature is not treated as the actual theorem type;
the final source states the two finite inequalities directly.

The project requests mathlib through the movable stable label; the retained
manifest pins `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, and its toolchain
specifies Lean 4.31.0. No dependency refresh was attempted. The publisher's
successful-build and standard-axiom claims were not independently reproduced
by a local Lean build, kernel replay or transitive axiom computation.
Static inspection and local import closure are not a formal certificate.

Acceptance means independent internal AI mathematical review of the written
arguments. This AI-assisted work is unrefereed. No external human peer
review, journal acceptance, local proof-assistant certification, exhaustive
novelty search, current tracker status or community-wide resolution is claimed.

## Source and publication boundaries

SOURCES.json records public citations, source hash/byte identities, matches,
historical inspection and retrieval limitations. The original 22-page PDF
was authenticated and the target page visually inspected; unrelated survey
topics were not fully audited. The complete STARFLEET #538 prose and selected
load-bearing source modules and statements were historically inspected.
No fresh publication-stage source inspection or redownload is claimed.

Exactly eight authored-prose/public-verification-metadata files are added
under attempts/2166. Source bodies, PDFs, code, datasets, raw certificates,
numerical computational witnesses, private sources and private coordination
are excluded. Analytic constants and their general written proofs remain.
This is not an executable reproduction package. Original sealed audit
packets, QUEUE.md and all unrelated repository content remain unchanged.
Preparation verifies exact bytes, editorial scope and native addition-only
structure, and executes no third-party source program.

## Exact public-file identities

- `ACCEPTANCE.json`: 3,203 bytes; SHA-256 `f1fb46672d9ba24cbb5bfc29a180c9651746801b1c02ab91d558df8053a7e577`.
- `ACCEPTANCE.md`: 5,098 bytes; SHA-256 `759bd83920cf81b14f6746eb07521d6111472a8d6f2ae36d07fd7c74a5ebe1d4`.
- `AUDIT.md`: 19,925 bytes; SHA-256 `303bd09bca23c0fdda45738092cddb2126d429585bb94cea5269726f1ed1169f`.
- `FOCUSED_AUDIT.md`: 14,006 bytes; SHA-256 `2d4219c46ee7e48a8741033a3dfb3806657643d6f329788f9fceef2f291b8cce`.
- `MANIFEST.json`: 1,599 bytes; SHA-256 `1f808e086461cef3d8a5c578872a6fe3f75b2f97401876c941f523ef13f5919d`.
- `README.md`: 3,510 bytes; SHA-256 `e7be141825d3b053a564b8d3f022ce5de799a1bb029ad5ae9808a05754475de7`.
- `SOURCES.json`: 4,533 bytes; SHA-256 `1219b02d52bad28737f1a2c1a1900f7ef2824922d45e96864b4c5205a7f780c9`.
- `VERIFICATION.json`: 2,562 bytes; SHA-256 `d400e00c1cd481bf23002a117e37e2f11311a2493d9dc00cb1c21c6a9782552f`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.

