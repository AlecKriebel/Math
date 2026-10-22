# Independent adversarial audit: random-graph biclique partition conjecture

## Verdict

ACCEPT as a credited prior negative result, with the nonblocking counting-wording
clarification below controlling the interpretation of the frozen candidate.
The proposed classification `already_solved`, one substantive attempt out of five,
is mathematically supported for ID 30002468, OWR-12861-019, queue rank 721.
The result is a consequence of Alon, Bohman and Huang's published Theorem 1.1,
not a new theorem or a claim of historical first recognition of this consequence.
No remote changes were made. The original nine-file directory was preserved.

## Frozen object and independent identity binding

The candidate has eight payload files totaling 26,212 bytes, plus MANIFEST.json
of 1,595 bytes, SHA-256
37454929779c07bff92cb3a3db3346560893aa9f43c9f4ee8250573d10caa5eb.
Every listed size and SHA-256 was independently recomputed, and the candidate's
verification script was inspected before execution. Its exact output matched.
BINDING.json records all payload identities without republishing the contents.

The public descriptor was independently parsed and hashed: 21,735,099 bytes,
SHA-256 891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566;
Git blob SHA-1 bd5c23e4e6c7e1901717a7e596477a7f6dc72425. Exactly one row has the
target ID and joins it to the OWR code, title, source DOI and rank. Its statement
and review hashes match the candidate metadata. Those are identity fields, not
proof that the inaccessible website or raw AI report was inspected.

A fresh request for the public statement-audit file at original queue revision
37e53eabe540fb458758e198be61634bd02ee008 returned 12,503,472 bytes with SHA-256
be250a6a3b996374b49b76fe4dea26dac9f221b5fde862fccfef566f8efad9a1. The code-keyed
record matches the primary question. Its editorial status is not primary-source
verification: its source_checked field is false. The independent primary-PDF
inspection supplies that missing step. The source record's input hash is not
silently equated with the descriptor's distinct statement hash.

## Primary-source match

The [OWR source](https://ems.press/content/serial-article-files/46491?nt=1),
printed page 80 (PDF index 75), was freshly downloaded, extracted, rendered and
read visually. The paragraph first discusses the older independence-number
conjecture and its partial refutation, then expressly proposes a revised
conjecture using the largest order of an induced complete bipartite subgraph.
The target is this revised equality at edge probability one half.

The quantity denoted tau there is the minimum number of edge-disjoint complete
bipartite subgraphs partitioning the edges. Pieces may share vertices; stars and
single edges are allowed. Pieces need not be induced. By contrast, the biclique
used for beta must include every cross-edge and no within-side edge. Replacing
beta by alpha, maximum ordinary biclique order, or an overlapping cover number
would change the question. No such replacement occurs in the candidate proof.

## Published input and proof-scope inspection

[Alon--Bohman--Huang](https://web.math.princeton.edu/~nalon/PDFS/biclique4.pdf),
Theorem 1.1, provides a fixed absolute positive c with
bp(G(n,1/2)) <= n-(2+2c)log_2(n) with high probability. Both its statement and the
[2014 v1](https://arxiv.org/pdf/1409.6165v1) were checked in extracted text and
rendered page 2. In v1, bc is explicitly defined as an exact edge partition.
[Institutional metadata](https://collaborate.princeton.edu/en/publications/more-on-the-bipartite-decomposition-of-random-graphs/)
confirms Journal of Graph Theory 84(1), 45--52, 2017, DOI 10.1002/jgt.22010.

Section 3 was read through its conclusion: induced structured bipartite graphs
admit few biclique pieces; outside vertices contribute stars. Its second-moment
calculation handles both small and large overlaps and finishes via Chebyshev.
The theorem is not restricted to a subsequence, balanced bicliques, star-free
partitions, or an alternative p-regime. Its logarithmic bound requires no
independence-number estimate in the present application.

Source-reading caveat: Claim 3.1 says graphs on a union, while its proof counts
compatible restrictions inside the two sets. Free edges between their exclusive
parts are irrelevant to the product of indicators and integrate to one. The
pattern-count interpretation used in the subsequent probability bound is sound.
This is not a full formal reproof of the published theorem or its bibliography.

## Independent verification of the mathematical implication

Let L=log_2(n), fix epsilon>0, and set k=ceil((2+epsilon)L). For sufficiently large
n, k lies between 2 and n. Each ordered assignment of a fixed k-set to two sides
specifies all k(k-1)/2 edge statuses. At p=1/2 its probability is
2^(-k(k-1)/2), regardless of the part sizes. There are at most 2^k assignments,
including both empty-side assignments. Thus the probability of at least one
qualifying k-set is at most

    choose(n,k) 2^k 2^(-k(k-1)/2)
    <= 2^[k(L+3/2-k/2)]
    <= 2^[k(3/2-epsilon L/2)].

This includes every balanced or unbalanced split; it is not a balanced-only
count and it does not count merely present cross-edges. When epsilon L>=6,
the last exponent is at most -epsilon(2+epsilon)L^2/4, so the bound tends to
zero. This explicit comparison verifies the asymptotic claim independently
of finite tests.

Any nonempty-sided induced biclique of order at least k contains one of order
exactly k: retain one vertex in each side and then k-2 others. Therefore beta<k
with high probability. Because beta is integral,

    beta <= ceil((2+epsilon)L)-1 < (2+epsilon)L,

including when the threshold is itself an integer. No off-by-one exception
occurs. The exact nonempty-sided count on a fixed k-set is 2^(k-1)-1: each
connected complete bipartite graph has a unique unordered bipartition.

Choose epsilon=c from the published theorem. The failure probability of the
intersection of the two good events is at most the sum of their failure
probabilities and hence tends to zero. Independence of these events is neither
known nor needed. On their intersection,

    n-beta+1-bp >= (2+2c)L-beta+1 > cL+1 > 0.

Consequently P(bp<n-beta+1) tends to one and P(bp=n-beta+1) tends to zero.
That refutes the whole revised probabilistic equality, rather than merely
producing occasional counterexamples or refuting the older alpha conjecture.
The proof uses a constant c independent of n. No explicit optimized c is needed.

## Controlling clarifications and boundary cases

1. Candidate PROOF.md lines 63--64 say there are fewer than 2^k divisions even
   if ordered and empty sides are allowed. The correct universally applicable
   phrase is AT MOST 2^k. Ordered divisions allowing empty sides number exactly
   2^k. The displayed inequality on line 67 already uses the correct bound, so
   the conclusion and every subsequent step are unchanged. Original bytes are
   preserved; this audit explicitly supplies the corrected reading.
2. The OWR paragraph does not specify an empty-part convention. Allowing empty
   sides can change finite beta: on an edgeless n-vertex graph, nonempty-sided
   beta is 0, whereas the enlarged convention gives n. It is incorrect to assert
   these values always agree. Nevertheless the enlarged family is already in
   the 2^k union bound. An independent set of order at least k contains one of
   order k, so the same hereditary argument applies, and the same refutation
   holds for either convention. No equality of the two beta values is needed.
3. For an empty edge set, bp=0. The candidate's beta=0 convention is explicit;
   the deterministic upper bound is true. With empty sides admitted the upper
   bound is true as well. Stars with no edges are omitted from the partition.
4. The deterministic n-beta+1 upper bound follows by taking the induced
   biclique as one piece and processing outside vertices in order. Every
   remaining edge is assigned once to its first processed endpoint. Edges
   inside the beta-set are already exhausted because it is induced.

## Independent executable controls

independent_controls.py imports no candidate code. It uses breadth-first
2-coloring and exact adjacency equality to recognize induced bicliques, and
ternary vertex assignments plus memoized exact edge-mask dynamic programming
to compute partition numbers. This is algorithmically separate from the
candidate's bipartition-enumeration recognizer.

All 1,100 labelled graphs with 0<=n<=5 were checked. The tests confirm 10 exact
nonempty-sided subset-expectation identities and their 10 empty-side analogues,
14,964 hereditary subgraph checks, 1,100 exact deterministic-bound checks and
1,100 explicit one-biclique-plus-stars constructions. Another 320 exact rational
checks cover rounding and exponent arithmetic. The three original negative
controls were rerun; five independent negative controls are documented in
NEGATIVE_CONTROLS.md. All pass. The controls are finite definition and arithmetic
checks only; none establishes a random-graph limit or proves the external theorem.

## Access, historical and scope limits

The exact numeric website remained inaccessible in an independent web attempt;
the candidate's direct-HTTP 403 limitation is retained. Its live text was not
read. The raw prior AI report was not inspected. The result does not require it,
but no claim about that report's correctness or absence is justified.

The candidate's repository-history search is bounded historical evidence; this
audit does not turn it into a universal no-prior-attempt claim. The inspected
descriptor records zero used turns; recording this completed substantive attempt
as one of five is consistent with that snapshot. Repository mutation is outside
this audit, and the current remote queue was not altered or independently
reconciled here.

No claim is made about an exact finite-n value, a sharp second-order asymptotic,
all p, the sparse/critical regimes, or a matching n-Theta(log n) result. The later
critical-probability paper is not a logical input. The classification is based
on the published theorem plus the fully checked elementary implication.

The safe audit contains authored analysis/code and verification metadata only.
Source PDFs, extracted text, page images, raw source records, ephemeral download
URLs and private coordination are excluded. Hashes establish byte identity and
reproducibility, not mathematical truth by themselves.
