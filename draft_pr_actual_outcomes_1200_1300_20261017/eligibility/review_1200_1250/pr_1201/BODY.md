## Accepted prior results and exact residual

This authored edition retains the complete repaired proof of Ema Skottová
and Raphael Steiner's 2025 prior result: for every k>=5 and every r>=1,
there exists a finite simple (k,r)-graph. Both appendices, the k=6,8
change-point and two-block bridge, vertex-deletion wraparound, gluing,
sparse critical scaffolds, and all-large-orders allocation are included.
Every correctness-relevant printed repair is explicit. The theorem
statements and parameter thresholds are unchanged. A focused independent
AI audit accepted the repaired proof with no further required correction.

Writing A=8(k-1)(18r+3), the progression orders are n>=A(6r+3)+1 with
n=1 modulo A; every order n>=A[2(k-2)A(6r+3)+2] is covered as well.
These give the square-root subsequence and cube-root all-large-orders
lower bounds for each fixed k>=5. The conventional lower proof is
self-contained and does not import Jensen's theorem or a finite computation.

Separately, two historically executed independent exact searches accept
Alex Chan's graph at commit 697307af42505b11490fdc74c04eda5c7ec76c51:
60 vertices, 180 edges, chromatic number 4, every vertex deletion
3-chromatic, and every single-edge deletion still 4-chromatic.
Its exact three-color defect is 2. It therefore gives k=4,r=1 only;
the family k=4,r>=2 is unresolved by these audited results.

The upper-bound implication separately imports Conlon–Fox Lemma 8.1.
Its source omits the lemma's proof; this edition does not re-prove it.
That dependency is not used in the lower bound.

## Verification and distribution boundary

The finite audit's first exhaustive search uses four verified edge
orbits of sizes 60,60,30,30, with 1230,1464,1207,1219 recursion nodes.
The second uses a distinct complete forward-checking search without
color or graph-orbit quotients: all 181 instances consisting of the graph
and every individual edge deletion were rejected, in 1,651,066 nodes.
Both solvers were checked against exhaustive coloring on 2,198 small-graph
cases each. Sixty graph automorphisms and sixty transported puncture
colorings were explicitly verified. Normal, -O and -OO historical outcomes
agreed. No author code, generated search certificate, or Lean project was
executed. Static Lean-semantic inspection is not formal replay, and the
source's all-k theorem retains its substantive inputs as hypotheses.

Exactly eight authored proof/audit/acceptance/provenance/verification files
are distributed. The complete conventional proof is retained. The finite
result is accepted at the disclosed historical exact-computation boundary;
this prose-only edition is not a computational reproduction package.
Programs, graph/generator/coordinate data, raw colorings and certificates,
copied source documents and images, and private coordination are excluded.
The omitted finite verification inputs and implementations are necessary
to reproduce that computation, but are not premises of the k>=5 proof.
Preparing this edition performed no new mathematical run, scholarly-source
retrieval, visual source inspection, or literature search.

## Attribution and review limits

- Ema Skottová and Raphael Steiner,
  [Critical edge sets in vertex-critical graphs](https://arxiv.org/abs/2508.08703v1),
  arXiv:2508.08703v1, 12 August 2025.
- Alex Chan,
  [fixed source repository](https://github.com/alexgocardinal/dirac-critical-graph/tree/697307af42505b11490fdc74c04eda5c7ec76c51).
- David Conlon and Jacob Fox,
  [Bounds for graph regularity and removal lemmas](https://www.its.caltech.edu/~dconlon/RegRem.pdf),
  Lemma 8.1 on printed p. 56 and proof-omission notice on p. 57.
- Paul Erdős,
  [On some aspects of my work with Gabriel Dirac](https://users.renyi.hu/~p_erdos/1989-19.pdf),
  printed p. 113, the original k>=4 every-r question.

This AI-assisted work is unrefereed. Acceptance means an internal
independent AI audit, not external human peer review, journal acceptance,
or formal proof-assistant certification. No novelty, priority, exhaustive
global current-literature status, or whole-problem resolution is claimed.
SOURCES.json records retained public-source status and historical
inspection scopes without asserting an updated peer-review status.

Only eight files are added under unsolved_math_prioritization/attempts/2398.
QUEUE.md and all unrelated paths are unchanged.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,436 bytes; SHA-256 `f331e06c266738cd16c686194ebf4f54a050a1aacb7df45d0c05a8a1ae340f6b`.
- `ACCEPTANCE.md`: 8,196 bytes; SHA-256 `7a0357f60eabc2db1a47f472de4ed1d3b898a2f9cc7b215262c73420cfe63026`.
- `AUDIT.md`: 45,580 bytes; SHA-256 `5342ae62dfa48a8f52667c89bf35b4217729f8648a2fa922a7ee729f1a3ac5a9`.
- `MANIFEST.json`: 1,362 bytes; SHA-256 `380c3d206ff640e5bb5744e8f61aac4010d4cf12386a060c651b3404dcd89222`.
- `PROOF.md`: 30,957 bytes; SHA-256 `fe18e57e2afa752e411f290a86627074a14f9cba69c7d7bc9d09df7a46aca4d5`.
- `README.md`: 2,846 bytes; SHA-256 `e9262d160bc4e94e6740d3df147c7b2fc4d48609f90254059d49604a1eb2c1d8`.
- `SOURCES.json`: 11,464 bytes; SHA-256 `c01a4916843139537404f7d11f62162f12e753672bdb917b1d6a4de274df68e6`.
- `VERIFICATION.json`: 12,714 bytes; SHA-256 `5f9437702ef4997c86cf91cde61b3fafa83444a00e50dde7761fcb0510f83c5d`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.
