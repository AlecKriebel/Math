# Independent audit of the simplicial core sampler

## Prose-edition and review scope

These AI-assisted authored documents are unrefereed. “Accepted” refers only to
the stated independent internal AI audit; no external human peer review,
journal acceptance, or formal proof-assistant certification is claimed.
The complete mathematical arguments are retained. This edition makes only
framing, attribution, and distribution-related editorial changes; no algorithm
or mathematical claim is changed.

Executable sampler and test programs, detailed test receipts, computational
certificates and raw datasets are omitted. Statements about implementation or
finite checks below record the review of the authenticated original artifacts;
they are not claims that this prose-only edition includes runnable code or
reproducible test receipts. Public verification metadata records the historical
checks and their limits. Hashes identify bytes and do not establish truth.

## Verdict

ACCEPTED AS A SCOPED PARTIAL RESULT. The constant-fiber simplicial-deletion
lemma, exact uniform reconstruction, residual-core exact sampler, exact
preservation of total-variation distance, and chordal specialization are
mathematically correct under the stated hypotheses. The supplied implementation
agrees with these constructions for valid plans produced by its preprocessing.
No blocking mathematical or implementation correction was found.

This acceptance does not establish novelty, an unrestricted efficient sampler,
a general FPAUS, a rapid-mixing theorem, or a sampling impossibility theorem.
The arbitrary-core fallback remains exponential. The chordal existence result
also follows from a stated 2022 theorem through the universal-sink construction;
its absent detailed appendix was not audited. The independently reviewed proof
here does not rely on that appendix.

## Authenticated original object and review method

The original reviewed mathematical manuscript, before this edition’s
explicitly recorded editorial changes, has SHA-256
93bc2e0d7e0b38e8922eb280c1caa6b28994865ba46ad06c1995e1f873924000
and 20,271 bytes. The reviewed implementation has SHA-256
36f0dbf1a69ba527553e88714d463704512ba22eb6b25f209ede23b8b24605de
and 7,231 bytes. The external inventory pin is
79b2579ca225849f67703fd9c728d6a8d46cc20655da8fa82a248265891cacb8.
Its exact 5,295 bytes describe 21 members. An independently written verifier
matched the complete actual file set, every size and every digest before
execution; authentication was repeated after the independent tests. A hash
establishes identity relative to the supplied anchor, not mathematical truth.

The review combines a line-by-line proof audit, direct source inspection,
independently written exhaustive tests, adversarial controls, and replay of the
candidate's checks. The mathematical arguments below, rather than finite tests,
justify the all-graph conclusions.

## Graph convention and parking correspondence

The scope is finite, connected, undirected, simple graphs, with an explicitly
specified root q retained throughout. The singleton graph is included. Loops,
parallel edges, disconnected graphs, empty vertex sets and invalid roots are
outside the implementation's domain and are rejected. No extension to
multigraphs is certified here.

For a parking function, start with q marked and successively mark a vertex
whose value is below its number of marked neighbors. The subset condition
prevents premature termination. Directing edges in the marking order produces
an acyclic orientation with unique source q, whose indegree-minus-one vector
g dominates the input coordinatewise. Its coordinate sum, including the
root's value -1, is m-n. Conversely, the earliest vertex of any nonempty
nonroot subset in a topological order has every incoming neighbor outside
that subset, so indegree minus one satisfies the original parking condition.

Consequently every parking function has sum at most m-n, every orientation
image is maximal, and every maximal parking function equals an orientation
image dominating it. This argument establishes maximality, rather than merely
assuming that maximum sum and coordinatewise maximality coincide.

An acyclic orientation is uniquely determined by its indegrees: zero-indegree
vertices have forced outgoing edges; deleting them determines the residual
indegrees, and induction reconstructs every edge. This proves injectivity.
Together these arguments establish the required bijection and ensure that
uniform orientations produce uniform maximal parking functions. For n=1,
the sole output is the vector (-1) and the empty orientation. These conclusions
agree with Theorem 3.1 and Corollary 3.2 of Benson, Chakrabarty and Tetali [2].

## One simplicial deletion

Let v differ from q and let C=N(v) be a clique of size d. Connectivity and
v!=q give d>=1. Deleting v preserves connectivity: any path segment a-v-b
can be replaced by a-b.

In a rooted acyclic orientation the induced clique on C union {v} has a unique
transitive order. Since all neighbors of v lie in this clique and v is not a
source, at least one member of C precedes v. The members preceding v form a
nonempty initial segment; its last member p is unique.

The only vertices that could become new sources under restriction are vertices
w with v->w. But p->v->w in the clique order implies the existing edge p->w.
Thus those vertices retain incoming edges. The root retains indegree zero,
and restriction cannot create a cycle. The image therefore belongs to the
rooted acyclic state space of the smaller connected graph.

For the inverse, fix a smaller-graph rooted acyclic orientation and any label
p in C. Place v immediately after p in any full topological order. The order
of C in that full order is its forced transitive clique order. Orient u->v
precisely for u=p or u->p, and orient v->u for the remaining neighbors. Every
edge is forward in the extended full order, proving global acyclicity, including
possible paths outside the clique. The edge p->v prevents a new source. Old
incoming edges remain. If q belongs to C, it is first in the clique order and
q->v; hence the root also remains a source. Restriction and selection of the
last incoming neighbor are inverse maps.

The fiber therefore has exactly d elements, independently of the smaller
orientation. The parameter is a fixed neighbor label, not a sampled total
order. Dropping simpliciality is invalid: deleting vertex 1 from the rooted
orientation 0->1->2->3, 0->3 of a four-cycle creates a new source at 2.

## Iteration and exact distribution

Fix the elimination certificate independently of the sampled orientations and
randomness. Iteration gives a bijection between the original state space and
the core state space times the fixed neighbor-label sets C_i. Each core state
has D=product d_i extensions. With a uniform core and independent uniform
pivots, every orientation and hence every maximal parking function has mass
1/(ZD), where Z is the number of valid core states.

Reverse reconstruction uses only already restored clique edges. Induction
ensures all those edges exist and have their final orientation before each
step. The implementation's reverse zip of deletion steps and pivots matches
this ordering. Choosing the pivot label uniformly is sufficient even though
its rank in the oriented clique depends on earlier random choices.

For an arbitrary probability law mu supported on valid core states, each of
its D extensions has mass mu(O)/D. The bijection to parking functions is
injective, so the total-variation half-sum over outputs is exactly

    (1/2) sum_O D |mu(O)/D - 1/(ZD)|
      = (1/2) sum_O |mu(O) - 1/Z|.

This is equality, not just contraction. Its premises include exactly uniform,
independent pivots and a law wholly supported on valid core orientations.
Failure symbols, invalid core states, adaptive biased certificates, or biased
pivots are not covered. The implementation is not advertised as an approximate
core API; the transfer statement is a mathematical lifting theorem.

## Enumeration, complexity and random bits

Each core-edge mask occurs once in enumeration. The unique-source check is
separate from the Kahn acyclicity check; having one source alone would not rule
out a directed cycle. A connected core always has a valid orientation: order
vertices by distance from q, break ties deterministically, and direct edges
forward. Each nonroot vertex then has an incoming edge from the previous
BFS layer. Thus 1<=Z<=2^b, including Z=1 when the core is a singleton.

The first enumeration counts Z; selecting a uniform valid-state rank and
replaying the enumeration selects exactly one uniformly distributed state.
The second pass can stop early without bias. Only the current orientation and
polynomial-sized counters are retained, so exponential output lists are not
required. The baseline cost is O(2^b(h+b)) graph operations.

Preprocessing maintains the number of nonedges in each active neighborhood.
When deleting v, only its active neighbors lose a neighbor. For each such u,
the disappearing missing pairs are precisely {v,w} where w is an active
neighbor of u not adjacent to v. The implementation subtracts exactly this
number. Initial computation is O(n^3); every update is at most O(n^2), for
at most n deletions. Choosing and sorting neighborhoods do not exceed this
O(n^3) bound. Independent full neighborhood recomputation matched every tested
plan. The root is explicitly excluded from eligible vertices.

Given a valid certificate and valid core, each deleted edge is restored once,
so unsorted reconstruction costs O(n+m) with constant-time direction queries.
The actual Python implementation also sorts its final m arcs, adding
O(m log(m+1)) comparison work. Python sets provide the stated expected hash
lookup model. A matrix can instead provide deterministic unit-cost adjacency
queries, with its O(n^2) storage and setup included in preprocessing. Neither
representation supports a claim of deterministic linear total Python runtime.
The combined graph-operation formula and conservative integer-arithmetic
allowance in the manuscript are adequate; large mask shifts and counters
must be interpreted in the stated bit model, not as free unbounded integers.

For a random integer in [0,r), let k=ceil(log2 r). For r>1, each k-bit trial
is accepted with probability r/2^k>1/2, and all accepted values have equal
probability. The exact expected fair-bit cost is k*2^k/r<2k. For r=1 the
implementation draws no bits. Since ceil(log2 Z)<=b and
ceil(log2 d_i)<=d_i for positive integers d_i, while sum d_i=m-b, the expected
sum is at most 2m bits. Independence of fair-bit trials and pivot calls is
necessary. A finite number of almost-surely terminating rejection calls
terminates almost surely, with exact output law. This is a Las Vegas expected
runtime statement, not a deterministic bound on the number of random trials.
SystemRandom is an implementation choice; the exact probability theorem uses
the explicitly ideal independent-fair-bit interface. Seeded PRNG executions
prove no statement about physical entropy.

The fallback is fixed-parameter tractable in the edge count b of the computed
core and polynomial for b=O(log(n+m+1)). This is not an algorithm for computing
a smallest possible core. Unrestricted residual cores can be as large as the
original graph, so the general bound remains exponential.

## Chordal case and source reading

The self-contained structural proof is valid. An inclusion-minimal separator
between two nonadjacent vertices in a connected chordal graph is a clique:
otherwise shortest paths joining two nonadjacent separator vertices through
the two separated components form an induced cycle of length at least four.
Every separator vertex reaches each chosen component by minimality. Induction
on the two smaller induced graphs gives one simplicial vertex in each
component, because a clique separator cannot contain both members of a
nonadjacent simplicial pair. These vertices are nonadjacent in the original
graph. Thus a noncomplete connected chordal graph has two nonadjacent
simplicial vertices; a complete graph has every vertex simplicial.

At least one eligible vertex differs from the prescribed root. Deletion
preserves chordality and connectivity, so greedy peeling reaches exactly q.
This proves the chordal exact polynomial-time result and its product count
without appealing to an uninspected external proof.

Adding a new universal vertex t and directing every new edge toward t is an
exact bijection from unique-source-q acyclic orientations of G to bipolar
(q,t)-orientations of the cone. Every old vertex acquires an outgoing edge,
t is the unique sink, and old indegrees do not change. Conversely a prescribed
sink forces all incident edges inward, so deletion preserves all old indegrees.
Coning preserves chordality and gives n+1 vertices and m+n edges. The state
space is nonempty by the distance-order construction.

Theorem 3 on page 11 of the authenticated 12-page Bezáková-Sun PDF states a
uniform linear-time bipolar sampler for connected chordal graphs and distinct
specified terminals [3]. Consequently the chordal existence claim was already
covered by that stated theorem, using the cone. The manuscript correctly
qualifies the linear-time attribution by the paper's model. Section 4 refers
detailed proofs to an appendix absent from the retrieved PDF, which ends with
references on page 12. This audit freshly rendered and inspected page 11 and
re-extracted the complete PDF text. It certifies the statement's presence and
the elementary reduction, not the absent proof or the external implementation.
The audit's fresh NSF and DOI web retrievals failed; source-content review used
the authenticated supplied PDF, and this limitation is recorded.

The AIM workshop notes pose the unrestricted sampling question as Problem 5
[1]. Their recorder says the entries summarize speakers rather than reproduce
verbatim quotations. A bounded search or this audit cannot establish that no
later general solution exists. No novelty or literature-exhaustiveness
acceptance is issued. The prior bridge/cycle/clique-block construction is not
newly claimed here.

## Historically recorded independent finite verification

All checks use explicit exceptions and were rerun under ordinary Python,
-O and -OO. The three final independently rebuilt receipts are byte-identical.
The independent orientation oracle enumerates full vertex orders with the root
first, filters the unique-source condition, and deduplicates orientations.
It never uses order multiplicities as sample weights. This is distinct from
the candidate's DFS/Kahn orientation oracle. The parking oracle applies every
nonempty subset and full coordinatewise dominance, independently of the
candidate's increment-based maximality check.

Coverage:

- All 772 connected labelled graphs on one through five vertices, all 3,807
  root instances, all 17,219 product outputs, and all 17,219 accepted-choice
  execution paths of the sample API.
- All 6,784 eligible one-step deletion fibers; full independent plan
  recomputation; source retention, surjectivity, inverse pivots and injectivity.
- Chordality checked independently by induced-cycle detection on the same
  graphs; all 582 connected chordal graphs peel to every prescribed root.
- All 1,285 valid deletion prefixes on connected graphs through four vertices,
  including empty, prematurely stopped and nongreedy certificates, with 2,748
  product outputs.
- Twenty additional deterministically chosen connected six-vertex graphs and
  ten seven-vertex graphs, using exhaustive orientation/product sets.
- All 167 universal-sink root instances on connected graphs through order four.
- Exact rational two-step TV equalities at distances 0, 1/6 and 2/3. A deliberately
  biased pivot rule instead gives distance 3/4 from uniform, detecting the
  necessity of the hypothesis.
- A four-cycle deletion that exposes a second source; a unique-source directed
  cycle rejected by the acyclicity check; malformed core support and pivots;
  ten invalid graph inputs; invalid integer bounds and bit-source returns;
  repeated rejected bit draws; the zero-bit singleton case; accepted integer
  outputs and exact bit-cost formulas for every bound from 1 through 256.
- The diamond's q-first order weights 1,1,2,2, detecting the familiar
  order-sampling bias. The pivot sampler has equal parameter fibers.

The candidate's own normal-mode suite was also replayed and matched its sealed
receipt byte for byte. Finite verification is corroboration and regression
coverage, never the proof of the unrestricted theorem.

## Acceptance boundary

The original candidate files were kept unchanged during the audit and this
edition’s preparation. This derivative has the editorial changes disclosed
above. The accepted surface is the authored,
self-contained partial theorem and implementation under the stated input,
certificate and random-source contract. The low-level lift and sample-from-plan
helpers trust a plan generated by peel or an independently valid certificate;
they are not full untrusted-certificate validators. Optional documentation
clarifications are listed separately. The acceptance is not contingent on them.

This prose-only edition includes authored mathematical reports and public
bibliographic or verification metadata. Source PDFs, extracted text, page
images, executable programs, detailed receipts, certificate contents and raw
datasets are excluded. The report records the audit’s historical scope; it
does not claim a new run of the omitted mathematical test programs.

## Public references

[1] S. Hopkins, recorder, Problems from the AIM chip-firing workshop (2013),
Problem 5. https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf

[2] B. Benson, D. Chakrabarty and P. Tetali, G-parking functions, acyclic
orientations and spanning trees, Discrete Mathematics 310 (2010), 1340-1353.
Theorem 3.1, Corollary 3.2 and Remark 3.1; primary preprint:
https://arxiv.org/abs/0801.1114 and https://arxiv.org/pdf/0801.1114.

[3] I. Bezáková and W. Sun, Counting and Sampling Orientations on Chordal
Graphs, WALCOM 2022, LNCS 13174, 352-364, Theorem 3.
https://doi.org/10.1007/978-3-030-96731-4_29 and
https://par.nsf.gov/servlets/purl/10355288.
