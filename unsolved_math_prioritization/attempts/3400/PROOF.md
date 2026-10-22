# Stable ternary compaction: accepted partial and exact remaining gap

Problem identity: 3400 / OPG-474, **Linear-size circuits for stable 0,1 < 2 sorting?**

## Result and status

**Review status:** accepted as a proved partial by the accompanying [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript and audit are unrefereed. Acceptance does not mean external human peer review, journal acceptance, or formal proof-assistant certification.

The unconditional question remains open in this report. No linear-size construction and no unconditional superlinear lower bound is proved. The proved results are:

1. An elementary, explicitly Boolean, stable-compaction construction of size O(n log n), using recursive separation of even- and odd-ranked live symbols. It does not rely on tagging each item by a log n-bit address or treating an arithmetic operation as one gate.
2. A linear-overhead reduction from bit shifting to this exact ternary function. Consequently the undirected k-pairs conjecture, together with Afshani–Freksen–Kamma–Larsen (AFKL), implies a matching Omega(n log n) lower bound. This is conditional, not a resolution of OPG-474.
3. The same conditional obstruction applies to the power-of-two, exactly-half-garbage promise. In the unrestricted-input problem it already applies when all 2s occur in a single contiguous run.
4. A counterexample to the stability assertion in Theorem 1 of Regan's 2007 note. Its comparator lower-bound corollary remains valid by a different, standard argument.

These constructions and checks are an authored derivation; no novelty relative to all prior literature is claimed. The conditional stable-compaction barrier was already discussed by Asharov–Lin–Shi; the present bit-level reduction does not claim priority. The exact lower/upper gap without an additional conjecture is Omega(n) versus O(n log n).

## 1. Exact model

For x in {0,1,2}^n let F_n(x) be the subsequence of entries unequal to 2, in their original order, followed by enough 2s to restore length n.

Use the two-bit encoding

    0 = (live,value) = (1,0),
    1 = (live,value) = (1,1),
    2 = (live,value) = (0,0).

The input (0,1) is outside the ternary promise. Our explicit circuit first replaces value by live AND value, so it also gives a specified extension on that fourth code. This extension is not an extra requirement of the problem.

Size counts Boolean computational gates. Inputs, constants, and wires are free; counting O(n) input/output terminals instead changes none of the bounds. The explicit basis is {AND_2, OR_2, NOT}. General circuits may use any fixed finite bounded-fan-in basis, with one bit per wire. No n-bit word, array access, variable shift, count, or comparator on growing-width keys is a unit-cost gate. Arbitrary constant-arity trit gates can be translated into Boolean gates with a constant size factor, and conversely the encoded model is within the intended general-circuit model.

Fan-out is initially unrestricted. This does not avoid the conditional lower bound: a circuit of S gates, fan-in at most b, and M output taps has at most bS+M uses of computed/input bits. Replace every high-fan-out vertex by a binary tree of identity gates serving its uses. The total added size is O(bS+M), and the new in- and out-degrees are bounded. Identity can instead be implemented by two NOT gates. Thus, for M=O(n), size becomes O(S+n). This includes uses of input bits, constants, and output wires; no input is allowed an uncharged high-degree exception when applying AFKL.

There is an elementary unconditional Omega(n) bound. The value bit of the first output depends essentially on each of the n input value bits: make that position the sole live input. A fan-in-b circuit cone with t gates can contain at most 1+(b-1)t distinct input sources. Hence t >= (n-1)/(b-1). This reasoning uses pairs of valid ternary inputs and does not depend on behavior outside the promise.

## 2. An O(n log n) construction by rank parity

First let n be a power of two. Number the live symbols by their zero-based rank in the original sequence. At one recursive stage, group adjacent input positions into n/2 pairs. For pair k, let q_k be the parity of the number of live inputs in all preceding pairs.

The live bits of pair k are a,c, its canonical value bits are b,d. Define:

    u = a OR c,                  v = a AND c,
    first = b OR ((NOT a) AND d),
    second = a AND d.

The pair (u,first) is its first live symbol, or garbage if none. The pair (v,second) is its second live symbol, or garbage if fewer than two. If q_k=0, send these two symbols respectively to slots k of arrays E and O. If q_k=1, exchange them. Thus E receives exactly the globally even-ranked live symbols, and O exactly the odd-ranked live symbols. Each array has n/2 slots; within each array the original relative order is preserved.

Recursively compact E and O. Interleave their results, starting with E. If there were m live inputs, the two recursive outputs have respectively ceil(m/2) and floor(m/2) live entries. Interleaving therefore produces the original m-symbol live subsequence followed only by garbage. In particular, no internal garbage remains between the last live symbols. The base case n=1 is the identity on canonical codes. This proves correctness by induction.

### Gate and depth accounting

The parity of the two live bits is

    p_k = u AND (NOT v),

using two additional gates once u,v are available. Compute all exclusive prefix XORs q_k of the p_k by a balanced upsweep/downsweep tree. On m=n/2 pair parities, this needs at most 2(m-1) XORs: m-1 subtree totals, and one new right-child prefix per internal node. An XOR is four basis gates, for example (r OR s) AND NOT(r AND s). The resulting prefix network has O(log m) depth.

The four pair fields u,v,first,second take six gates. Swapping the two live fields and two value fields uses four two-input multiplexers controlled by q_k. Sharing NOT q_k, those four multiplexers take 13 gates. Including the two gates for p_k, all local work costs 21m gates. Prefix work costs at most 8(m-1). Therefore

    T(n) <= 2 T(n/2) + 29n/2 - 8 <= 2 T(n/2) + 15n,
    T(1)=0.

The initial canonicalization costs n AND gates. Total size is at most 15 n log_2(n)+n for powers of two. Depth is O(log^2 n), since each stage costs O(log n) depth. The implementation intentionally does not need constant folding or dead-gate elimination for this upper bound.

For general n, pad with 2s to N=2^ceil(log_2 n), apply the N-input construction, and retain the first n outputs. Since N<2n for n>1, size remains O(n log n). All movement here is between fixed wire locations; the notation E,O and interleaving is a description of fixed wiring, not a run-time memory operation.

## 3. Linear-size control gadgets

Two standard gadgets are made explicit to prevent hidden word-RAM costs.

**Binary-to-one-hot and thresholds.** Given h=ceil(log_2(n+1)) bits encoding k in {0,...,n}, decode them with the full binary decision tree: from a prefix indicator r, create r AND bit and r AND NOT bit. There are O(2^h)=O(n) gates and h shared bit negations. Leaf indicators are [k=j]. A prefix/suffix OR scan of the leaves gives every threshold [i<k], [i>=k], or its reflected counterpart in O(n) additional gates. The simple sequential scan suffices for size. No n separate h-bit comparisons are used.

**Counting.** A balanced sum tree counts n live bits in O(n) Boolean gates. At height h, there are O(n/2^h) additions of O(h)-bit integers; ripple-carry addition takes O(h) fixed-basis gates. Summing O(n h/2^h) over all h gives O(n). Padding to a power of two and the extra carry bit change only constants. Adding/subtracting a fixed O(log n)-bit integer costs O(log n) gates. These operations are not unit-cost arithmetic assumptions.

## 4. Shift is a restriction of ternary compaction

Define Shift_n(x,k), for x in {0,1}^n and 0<=k<n, to be the 2n-bit string

    0^k x 0^(n-k).

This is AFKL's shift function with their one-based shift index equal to k+1. Construct a length-2n ternary string

    z = 0^k 2^(n-k) x.

Its first n slots are formed by the threshold controls from Section 3; the last n slots contain the input data bits. This costs O(n) Boolean gates. Correct compaction gives

    F_(2n)(z) = 0^k x 2^(n-k).

Read the value bit of each output code, which maps 0 and 2 to zero and 1 to one. The result is exactly Shift_n(x,k). Hence, writing S(N) for the size of any family computing F_N,

    size(Shift_n) <= S(2n)+O(n).

For non-power-of-two n, the decoder still has fewer than 2(n+1) leaves; the promised range 0<=k<n is enough. The reduction uses the full n independent bits of x and all n possible shifts. It is not a single fixed permutation.

Notably, the 2s in z form just one contiguous block (possibly with zero-length prefix). The reduction therefore rules out a linear circuit for even this restricted promise, **if** the conditional shift lower bound applies. This is not an unconditional claim about one-run inputs.

### Balanced power-of-two version

For n a power of two, form the length-4n string

    z* = (0^k 2^(n-k)) x (0^(n-k) 2^k) 2^n.

It has exactly 2n live symbols and 2n garbage symbols. Its length is a power of two. Its compacted output is

    F_(4n)(z*) = 0^k x 0^(n-k) 2^(2n).

Reading the first 2n value bits therefore computes Shift_n. The two variable padding blocks use O(n) threshold gates. This gives the same conditional barrier even on Regan's balanced promise. There are at most two nonempty garbage runs, since the final 2^k and 2^n are adjacent.

## 5. Conditional matching lower bound

The assumption is the **undirected k-pairs conjecture**, in the precise form used by AFKL: the achievable network-coding rate in an undirected network equals its fractional multicommodity-flow rate. We do not prove or assume as fact that the conjecture is true.

AFKL, *Lower Bounds for Multiplication via Network Coding*, ICALP 2019, Theorem 2, states that under this conjecture every Boolean circuit with arbitrary gates and bounded in- and out-degrees computing Shift_n has size Omega(n log n). See the [official paper](https://doi.org/10.4230/LIPIcs.ICALP.2019.10), physical PDF page 3; Section 4 on physical pages 7–8 supplies the argument.

Combining the linear-overhead reduction with the fan-out conversion in Section 1 gives

    O(S(2n)+n) >= c n log n,

so S(2n)=Omega(n log n). For any length m, set n=floor(m/2), use the shift reduction at length 2n, and pad with m-2n garbage symbols before invoking F_m. Reading the first 2n outputs yields the same shift. Thus S(m)=Omega(m log m) for all sufficiently large m. For balanced lengths N=4n, the second reduction gives the corresponding bound directly on all sufficiently large power-of-two lengths.

This proof does not infer a lower bound for a one-bit payload from a theorem that silently requires a large payload. It reduces the actual bit-shift problem to the exact three-symbol function. It also handles unbounded fan-out explicitly, rather than overlooking AFKL's degree restriction.

Together with Section 2, the conditional complexity is Theta(n log n). Unconditionally, the interval in Section 1 remains open. In particular, a linear-size family for OPG-474 would refute the stated network-coding conjecture, but the lack of such a family does not prove the conjecture or prove a lower bound.

## 6. Regan's balanced reduction, with output masking explicit

For completeness, let n>=1, let m be the least power of two with m>=n, let c be the number of 2s in x, and let g=n-c. Define

    z = x 1^(m+c-n) 2^(m-c).

Its length is 2m, with m live and m garbage symbols. Both exponents are nonnegative. The count and unary padding circuitry cost O(n), by Section 3. If U is the original good subsequence, the balanced circuit returns

    U 1^(m-g) 2^m.

For each output position j<n, retain the balanced output when j<g, and output 2 otherwise. Threshold generation and these n constant-width multiplexers cost O(n). This recovers U 2^c exactly. Simply taking the first n outputs without this mask would be incorrect; Regan's informal final extraction must include this step. Thus linear circuits for the balanced promise would imply linear circuits for the full problem. Since n is fixed for each circuit, choosing m itself is offline circuit construction, not an input-dependent arithmetic gate.

## 7. Source correction: local stability does not imply network stability

Regan's note, Theorem 1, claims that a comparator network correct on {0,2}^n remains a stable topological sorter for every partial order when its comparators are replaced by the corresponding locally stable comparators. That assertion fails even for the particular partial order 0,1<2.

Consider this fixed three-wire network, with lower wire index receiving the smaller element:

    compare wires (1,3), then (1,2), then (2,3).

It sorts every binary {0,2}^3 input. One can check all eight cases; alternatively it sorts arbitrary totally ordered triples by first ordering the extremes and then correcting the two neighboring pairs.

Now use the note's partial-order comparator, which swaps (a,b) exactly when b<a and otherwise keeps them. Starting from (2,0,1), the first comparator swaps the 2 and the 1, producing (1,0,2). The remaining comparators do nothing. The original good subsequence (0,1) has become (1,0). This violates stability. The correct F_3 output is (0,1,2).

The note's proposed ordering by original index among incomparable elements is not a valid way to justify that assertion: a nonadjacent comparator can move an item across incomparable items that it never compares. For some general partial orders that proposed relation need not even be transitive. The explicit three-wire counterexample is enough here; no general-poset premise is needed.

**What survives.** Any comparator network computing F_n necessarily sorts binary inputs {0,2}^n. By the ordinary 0–1 principle for total orders, its wiring is a sorting network for n distinct totally ordered items. At most 2^s comparison-outcome patterns are available with s comparators, whereas n! input orders must be distinguished. Hence s>=log_2(n!)=n log_2(n)-O(n). Thus the comparator lower bound survives. It is still not a lower bound for unrestricted Boolean circuits. Our upper bound and shift reduction never invoke the incorrect stability assertion.

## 8. Why the recent cited results do not close the gap

Asharov–Lin–Shi, arXiv:2010.09884v2, Theorem 1.2, achieves linear size for certain payload regimes, including constant payload length, for **nonstable** compaction. Section 1 explicitly distinguishes stability and discusses conditional barriers. For example both 012 and 102 have the same multiset and satisfy ordinary compactness, while their required good subsequences differ. A count or an arbitrary permutation of marked values cannot determine the required stable output. Adding log n-bit identity tags changes the bit-level cost and does not produce an O(n) circuit for this target.

Holmgren–Rothblum, CCC 2024, gives multiselection size O(n+q log^3 n), from an explicit list of query indices. Its O(n) range has q<=O(n/log^3 n). Dense balanced compaction requires Theta(n) output bits and must derive selected indices from the live mask. Substituting q=Theta(n) is not linear, and neither the ordered list of indices nor its construction is free. Thus that theorem alone does not solve OPG-474. It also does not contradict the conditional barrier, because it gives a different input/output problem and parameter range.

## 9. Exact remaining work

The parity-split proof performs a linear amount of work at each of log n recursive scales. Nothing here removes those scales or amortizes them into O(n) total gates. A valid positive solution must replace that total accounting, and would also overcome the conditional shift obstruction by disproving the stated network-coding conjecture. A valid unconditional negative solution must obtain a superlinear lower bound for general Boolean computation; comparison outcomes, movement-only payload arguments, and indivisibility are insufficient.

The accompanying audit records finite checks of the explicitly built circuits and reductions, including the source counterexample. Those checks are supplementary implementation evidence only. The analytic arguments above require no omitted program or raw output. Finite checks are not evidence of an asymptotic lower bound, a proof of the network-coding conjecture, or a full resolution of OPG-474. The independent mathematical audit has accepted exactly the partial results stated here.

## Sources and verification scope

- [Original problem](https://www.openproblemgarden.org/op/linear_size_circuits_for_stable_0_1_2_sorting).
- Kenneth W. Regan, *A view of complexity theory, with a “concrete” open problem*, July 11, 2007: [author PDF](https://www.cse.buffalo.edu/~regan/InfoFlow.pdf).
- Gilad Asharov, Wei-Kai Lin, Elaine Shi, *Sorting Short Keys in Circuits of Size o(n log n)*, arXiv:2010.09884v2: [paper](https://arxiv.org/abs/2010.09884).
- Justin Holmgren, Ron Rothblum, *Linear-Size Boolean Circuits for Multiselection*, CCC 2024: [official paper](https://doi.org/10.4230/LIPIcs.CCC.2024.11).
- Peyman Afshani, Casper Benjamin Freksen, Lior Kamma, Kasper Green Larsen, *Lower Bounds for Multiplication via Network Coding*, ICALP 2019: [official paper](https://doi.org/10.4230/LIPIcs.ICALP.2019.10).

The accompanying audit records matching normal and optimized checks using explicit failures rather than removable assertions. Those historical checks built and evaluated elementary Boolean gate lists, tested exhaustive finite and deterministic larger cases, checked reduction formulas, and rejected deliberate negative controls. [ACCEPTANCE.json](ACCEPTANCE.json) records aggregate verification metadata; [SOURCE_METADATA.json](SOURCE_METADATA.json) records public source identities and the scope of earlier inspection. Programs, raw outputs, source bodies, PDFs, images and datasets are not distributed in this proof-only edition. Edition preparation rechecked frozen byte identities and publication integrity, but performed no new scholarly retrieval, source-text inspection, literature search, or mathematical computation rerun.
