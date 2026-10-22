# Source review and exact circuit boundary

## Originating question and exact model

The [original problem](https://www.openproblemgarden.org/op/linear_size_circuits_for_stable_0_1_2_sorting)
asks whether stable compaction of ternary symbols, with 0 and 1 live and 2
garbage, has linear-size general circuits. The required output preserves the
original order of every live symbol and appends garbage. Fixed bounded-fan-in
Boolean gates are counted; growing-word arithmetic, arbitrary indexing and
variable shifts are not unit-cost operations. Unrestricted fan-out is
accounted for by an all-terminal O(S+n) conversion to bounded degrees.

The unconditional question remains unresolved in this work. The explicit
rank-parity construction proves O(n log n) size and O(log^2 n) depth. The
essential-variable argument proves only Omega(n) unconditionally.

## Conditional barrier and prior credit

Peyman Afshani, Casper Benjamin Freksen, Lior Kamma and Kasper Green Larsen,
*Lower Bounds for Multiplication via Network Coding*, ICALP 2019,
[official paper](https://doi.org/10.4230/LIPIcs.ICALP.2019.10), Theorem 2,
proves an Omega(n log n) lower bound for the actual bit-shift function under
their undirected k-pairs conjecture. The premise equates network-coding and
fractional multicommodity-flow rates in undirected networks. The theorem's
bounded input/output degree conditions are explicitly handled in this proof.

The O(n)-overhead restrictions in [PROOF.md](PROOF.md) yield Theta(n log n)
for ternary stable compaction only under that conjecture. They cover a single
contiguous garbage run for the unrestricted-length problem and an exactly
half-garbage promise at power-of-two lengths. Neither the conjecture nor an
unconditional superlinear general-circuit lower bound is proved here.

Gilad Asharov, Wei-Kai Lin and Elaine Shi, *Sorting Short Keys in Circuits of
Size o(n log n)*, [arXiv:2010.09884v2](https://arxiv.org/abs/2010.09884),
already discusses the conditional stable-compaction barrier, including its
AFKL attribution. No novelty or priority is claimed. Its Theorem 1.2 gives
nonstable compaction in the stated regimes; that does not preserve the live
subsequence required here.

Justin Holmgren and Ron Rothblum, *Linear-Size Boolean Circuits for
Multiselection*, [CCC 2024](https://doi.org/10.4230/LIPIcs.CCC.2024.11),
gives O(n+q log^3 n) for explicitly supplied query indices. Dense compaction
requires Theta(n) outputs and must derive its indices from a live mask.
Neither that dense parameter choice nor construction of the queries is free,
so the theorem alone does not give a linear circuit for this target.

## Exact source correction and surviving comparison result

Kenneth W. Regan, *A view of complexity theory, with a concrete open problem*,
July 11, 2007, [author PDF](https://www.cse.buffalo.edu/~regan/InfoFlow.pdf),
Theorem 1, asserts a network-stability conclusion that fails as written.
The binary-correct three-wire network (1,3), (1,2), (2,3), using the note's
locally stable comparator for 0,1<2, sends (2,0,1) to (1,0,2). The required
stable output is (0,1,2). This is an exact analytic counterexample to that
assertion, not a counterexample to the possibility of linear-size general
Boolean circuits.

The comparator lower bound survives separately: restriction to binary
inputs and the ordinary total-order 0–1 principle give a sorting network;
n! distinct input orders require at least log_2(n!) comparators.
That counting argument does not apply to general Boolean computation.
Regan's general-to-balanced reduction also requires the explicit output mask
preserved in the proof; merely truncating the balanced output is incorrect.

## Recorded inspection and publication limits

The audit records inspection of the full two-page Regan note and visual
inspection of both pages, plus AFKL's Theorem 2, definitions and Section 4,
with visual inspection of physical PDF pages 3, 7 and 8. It also records
inspection of Asharov–Lin–Shi's stable/nonstable distinction and
Holmgren–Rothblum's input/output parameterization. Public byte identities,
retrieval records and bounded-search limits are in
[SOURCE_METADATA.json](SOURCE_METADATA.json). A bounded search is not a
current-worldwide-open or priority certificate.

These are historical source observations. Edition preparation rechecked
frozen file identities for integrity, but performed no new scholarly
retrieval, source-text inspection, literature search, or mathematical test
rerun. Finite checks remain supplementary metadata only; the full analytic
proofs require no omitted program. Programs, raw outputs, datasets, source
bodies, PDFs, images and private coordination material are excluded. This
AI-assisted edition and accompanying audit are unrefereed.
