# Independent binary compiler derivation

Written 2026-10-06 21:15 America/Los_Angeles (2026-10-07 04:15 UTC).
This note proves the encoding lemmas without assuming the upstream lower
bounds. The advertised stretched-exponential consequences in §7 are conditional
on the independent dependency audit. No upstream algebraic lower bound was
verified by the compiler tests.

## 1. Original source languages and conventions

I inspected the pinned clone at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
The determinization manuscript's Introduction, equation (1), and the
complementation manuscript's automata section, equation (17), both define the
same language on the full alphabet of all relations on `H=[h]={0,...,h-1}`:

`L_h = { R_1 ... R_m : R_1 ... R_m is nonempty }`.

The product is in path order: `(p,r)` belongs to `RS` iff there is `q` with
`(p,q)` in `R` and `(q,r)` in `S`. The empty product is the full identity, so
the empty word is live when `h>=1`. The two-way complementation input is
therefore independently compatible with exactly the same bit encoding; it
is not a different alphabet requiring unverified extra decoding. The actual
Lean file `OAI/Combinatorics/TwoWayAutomata/RelationBridge.lean` supplies an
explicit currying equivalence and proves
`relationProduct_map` and `sourceLanguage_map_iff`; I read the declarations
but did not independently build them for this compiler note.

Model for this note: finite state set `Q`, initial state `q_0`, accepting
subset `A`, head initially on a distinct left marker, transitions to
`Q x {-1,0,+1}`, no move beyond either endmarker. Missing transition is a
rejecting halt. Nondeterministic transitions are subsets. A word accepts iff
some finite run reaches an accepting state, including time zero unless
the alternative positive-transition convention is specified. Infinite runs
without a finite accepting prefix reject. All states are counted. A one-way
source has no left moves; the construction below has no interior stays and
one accepting stay at the right endmarker.

## 2. Binary language on every binary word

Fix `B=h^2`. Let `c(R)` have bit `ph+q` equal to the indicator of `(p,q) in R`,
for `0<=p,q<h`. Bit positions here are zero-based, in row-major order.
Extend `c` to words by concatenation, with `c(epsilon)=epsilon`.
This gives a bijection from `Sigma_h^*` onto

`V_h={u in {0,1}^*: B divides |u|}`.

Indeed every `B`-bit block is a unique relation, and a multiple-of-`B` length
has a unique block decomposition. Define `C_h=c(L_h)`. Thus a nonmultiple
length is rejected, while a multiple length is accepted precisely when the
decoded relation product is nonempty. Empty input is accepted.
This definition is total on all binary strings; there is no promise on the
input and no informal alignment assumption.

## 3. Explicit one-way source in `(3h^3-h)/2+2` states

States are the distinct states `in`, `acc`, and

* `U(p,t)`, for `0<=p<h` and `0<=t<(p+1)h`;
* `V(q,t)`, for `0<=q<h` and `q+1<=t<B`.

The initial state is `in`, and `acc` is the only accepting state. Unlisted
transitions are missing. Each transition on an interior bit moves right.

1. On the left marker, `in` moves right to any `U(p,0)`.
2. In `U(p,t)`, on either bit, if `t<(p+1)h-1`, it may move to `U(p,t+1)`.
   This is the option of postponing the edge choice.
3. In `U(p,t)`, if the bit is 1 and `floor(t/h)=p`, put `q=t mod h`.
   If `t=B-1`, it may move to `U(q,0)`; otherwise it may move to `V(q,t+1)`.
4. In `V(q,t)`, either bit leads to `V(q,t+1)` if `t<B-1`, and to `U(q,0)`
   if `t=B-1`.
5. On the right marker, `U(p,0)` has a stay transition into `acc`.
   All other source rows on that marker are empty. `acc` has no successors.

All destinations listed exist. In rule 3, `t=ph+q`, so `t+1>=q+1`; thus
`V(q,t+1)` is in its prescribed range whenever `t<B-1`.

At the first bit of a block `U(p,0)` records its chosen starting vertex.
Until choosing an edge it has `U(p,t)` at bit `t`, and it can choose only a
1-bit in row `p`, exactly an edge `(p,q)` of the decoded relation. The
postponement branch dies after the last bit of row `p` if it never chooses.
Once the edge is chosen, `V(q,t)` skips the remaining block retaining its
endpoint, and the next block starts in `U(q,0)`. Induction over blocks proves
that successful scans of `m` complete blocks correspond exactly to sequences
`p_0,...,p_m` with `(p_{i-1},p_i) in R_i`.

The only return to phase zero in an interior scan occurs upon consuming the
last bit of a complete block. Hence right-marker acceptance is impossible
at a malformed length. At a valid length the run accepts iff it has chosen
one edge per block, exactly iff the decoded product is nonempty. On empty
input the first move from the left marker reaches the right marker in
`U(p,0)` and the accepting stay succeeds. No accepting initial state is used,
so the language is unchanged under the positive-transition convention.
Every run has at most `|u|+2` transitions and the source never loops.

The number of states is exactly

`2 + sum_{p=0}^{h-1}(p+1)h + sum_{q=0}^{h-1}(B-q-1)`

`= 2 + h^2(h+1)/2 + hB - h(h+1)/2`

`= (3h^3-h)/2 + 2`.

The untrimmed variant has at most `2h^3+2` states, but the trim above is safe
and implemented. These are actual transition-based counts, not the original
triage estimate `O(h^4)`.

## 4. Cubic size is intrinsic to this total language for one-way NFAs

For `h>=2`, every one-way NFA recognizing this exact language needs at least
`hB=h^3` states, by a fooling set. Let `E_p={(p,p)}` and `I` be the full
identity, and for `0<=t<B` put

`x_{p,t}=c(E_p) prefix_t(c(I))`,

`y_{p,t}=suffix_t(c(I)) c(E_p)`.

Here the suffix starts at bit `t`, so its length is `B-t`.
Matching concatenation is `c(E_p)c(I)c(E_p)`, which is live. For distinct
pairs `(p,t)!=(q,u)`, if `t!=u`, the length of `x_{p,t}y_{q,u}` is
`3B+t-u`, which is not divisible by `B` because `0<|t-u|<B`. If `t=u` and
`p!=q`, the concatenation is `c(E_p)c(I)c(E_q)`, whose product is empty.
Thus every cross concatenation rejects.

To see the state lower bound, choose an accepting run for each matching
pair and its state at the cut between `x` and `y`. If two pairs shared a
state, splice the prefix of one run to the suffix of the other to accept
a cross concatenation, contradiction. This proof also covers epsilon/stay
moves under ordinary whole-word NFA acceptance. In our finite-configuration
model, any accepting run of a one-way recognizer of `C_h` must first reach
the right marker: otherwise extending its accepted word by one bit gives
a malformed word accepted by the same early run. Having reached the marker,
the head never returns left. Thus the same cut-and-splice argument applies
to the no-left, stay-permitting model in §1. The pairs have nonempty suffixes.

Consequently the explicit upper and lower bounds give

`h^3 <= minimal one-way source size <= (3h^3-h)/2+2`.

Kapoutsis's paper *Nondeterminism is essential in small two-way finite
automata with few reversals*, primary PDF
https://www.andrew.cmu.edu/user/cak/reads/2013-IAC/main.pdf,
Conclusion, printed page 29/PDF page 28, explicitly discusses natural
`h^2`-bit relation encoding and states an `O(h^2)` zero-reversal source
bound without giving its compiler. The known binary-encoding idea therefore
needs attribution. Its stated quadratic source bound cannot certify the
total language above: the fooling-set proof gives a cubic lower bound when
malformed lengths must reject. A promise on valid encodings avoids the
malformed cross tests, but the cited passage does not explicitly explain
such a promise. No unproved quadratic compiler is used here. This is a
quantitative/convention discrepancy to preserve in the priority audit,
not evidence that the unrestricted upstream breakthrough is valid.

## 5. Pullback of an arbitrary binary two-way target in exactly `sB` states

Let a binary 2NFA `M` have states `Q`, size `s`, initial `q_0`, accepting
set `A`, and transitions `delta`. A 2DFA is the single-successor special
case. Construct a relation-alphabet machine `P` with

`Q_P=Q x {0,...,B-1}`, initial `(q_0,0)`, accepting set
`A x {0,...,B-1}`.

At a relation letter `R` and state `(q,t)`, look up the bit `b=c(R)[t]`.
For every `(q',d)` in `delta(q,b)`, make exactly this transition:

| Binary move | Condition | Pullback next state | Pullback head move |
|---|---|---|---|
| `0` | any `t` | `(q',t)` | `0` |
| `+1` | `t<B-1` | `(q',t+1)` | `0` |
| `+1` | `t=B-1` | `(q',0)` | `+1` |
| `-1` | `t>0` | `(q',t-1)` | `0` |
| `-1` | `t=0` | `(q',B-1)` | `-1` |

On the left marker, ignore `t` when looking up `delta(q,left)`. A stay
goes to `(q',t)` with stay, and a right move goes to `(q',0)` with right.
On the right marker, similarly a stay goes to `(q',t)` with stay, and
a left move goes to `(q',B-1)` with left. There are no illegal outward
marker moves since the original target has none. A partial empty row stays
empty. Distinct original successor choices give distinct new transitions.
For `B=1` the table still applies.

For a relation input `w` of length `m`, project pullback configurations
as follows: at the left marker send any phase to position 0; at the right
marker send any phase to position `mB+1`; at relation cell `j` with phase
`t`, send to binary position `(j-1)B+t+1`. Always preserve state `q`.
The initial configuration projects to the original binary initial one.
Each transition in the table projects to exactly one original transition,
and conversely every original transition from a projected configuration
has its indicated pullback lift. At marker configurations the phase can
be arbitrary, but marker rows ignore it and reset it on entry to a block.

Induction yields correspondence of all finite runs from the initial
configuration, preserving accepting configurations and the number of
transitions. The same stepwise correspondence holds for infinite runs.
In particular nonaccepting infinite branches do not become accepting;
undefined rows remain rejecting halts. Time-zero acceptance and the
alternative positive-transition convention are both preserved because
each original step is exactly one pullback step, with no preprocessing.
For empty input both tapes consist of two adjacent marker cells, and the
marker rules give the same correspondence directly. It follows that

`L(P)=c^{-1}(L(M))` and `|Q_P|=s h^2`.

The compiler is uniform in the finite relation alphabet; its transition
table may be large because the source alphabet is large, but the theorem
measures states, not transition-table length. No exponential storage of a
relation is needed in a state: the current relation is a scanned symbol,
and its bit `t` is a transition-table lookup.

## 6. Exact complementation universe

By total-language definition,

`{0,1}^* \ C_h = ({0,1}^* \ V_h) union c(Sigma_h^* \ L_h)`.

The union is disjoint. Because `c(w)` is valid for every relation input,
for any binary machine recognizing that full complement, its pullback
recognizes exactly `Sigma_h^* \ L_h`. This remains true on empty input:
empty input is live on both alphabets, so both complements reject it.
No claim that the complement equals the image of the relation complement
alone is permissible; malformed strings form the additional term.

## 7. Conditional quantitative corollaries, not certified conclusions

If the upstream one-way-liveness deterministic inequality really holds
in §1's time-zero convention, any `s`-state binary 2DFA for `C_h` obeys

`4(s h^2 + 1)^2 >= 2^floor((h-2)/31)`.

Under positive-transition acceptance replace `+1` by `+2`. Equivalently
in the first convention,

`s >= (2^(floor((h-2)/31)/2-1)-1)/h^2`.

If the upstream nondeterministic complementation inequality holds, every
`s`-state binary 2NFA for the full complement of `C_h` obeys

`2(s h^2 + 1) >= 2^floor((h-2)/127)`,

or `s >= (2^(floor((h-2)/127)-1)-1)/h^2`.

In both cases this is `2^Omega(h)`. With the explicit source count
`N_h=(3h^3-h)/2+2`, the conditional binary lower bound is
`2^Omega(N_h^(1/3))`. It is not `2^Omega(N_h)`.
For every sufficiently large requested source count `n`, choose the largest
`h` with `N_h<=n` and add unreachable nonaccepting states. Then `h` is
`Theta(n^(1/3))`, so the same conditional bound is `2^Omega(n^(1/3))`.
Padding preserves the alphabet, language, and no-left property. No uniform
complexity class separation is claimed.

## 8. Checkable artifact and actual tests

`code/binary_compiler.py` implements the trimmed source, exact pullback,
configuration reachability for finite acceptance, both acceptance
conventions, and the fooling-set construction. Run from project root:

```text
python3 code/binary_compiler.py --output agent_notes/binary_compiler_check_results.json
```

The run completed successfully under Python 3.14.6. It checks all 1,534
binary words of lengths at most 8 for `h=1` and at most 9 for `h=2`, against
the direct matrix-product algorithm, under both acceptance conventions.
It checks all 288 one-state partial deterministic targets with legal
marker rules, and 128 reproducibly sampled two-/three-state nondeterministic
targets. Targets include partial rows, stays, left/right moves, accepting
initial states, marker loops and nonaccepting cycles. All relation words
of length at most 2 on `h=2` are used, under both conventions, for 227,136
pullback equivalence comparisons. It checks all cross pairs of the
fooling sets for `h=1,2,3,4` (100 pairs total), and actual source counts
for `h=1,...,8`. The receipt is
`agent_notes/binary_compiler_check_results.json`.

These exhaustive tiny-instance and reproducible sampled checks support
the compilers only; the proofs in §§2–6 are the uniform evidence.

## Source hashes actually inspected

SHA-256, paths relative to the pinned clone:

| Path | Hash |
|---|---|
| `preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/introduction.tex` | `2e9fef0dd56197a5bd6c3f0a2a744b9fee6d5d17672e883e6e3ab34c77907271` |
| same manuscript, `build/sections/machines.tex` | `1bd484da75a974633246a35d5681bbafead91bb0697bba625894185329a960bf` |
| `preprints/An-exponential-state-lower-bound-for-two-way-nondeterministic-complementation-September-25-2026/build/sections/introduction.tex` | `7ab624cb40e7343bb6ba7e0fb6f1d25bd91225db486fb50357659060ca01b7c7` |
| same manuscript, `build/sections/automata.tex` | `70818a2af431e07abb935f8a3faa25fa12c2d31fbeedfed7ac6da21b0c418765` |
| `lean/OAI/Combinatorics/TwoWayAutomata/RelationBridge.lean` | `82497efbaa3192d7f965abd0b643c110eb485da67acd842c53dbcd2da5dd60b3` |

## Checkpoint assessment

Encoding lemmas: mathematically complete, independently checkable proof and
tests available. Core unconditional binary separation: not assessed by
this work; pivotal upstream bounds remain dependencies. For this delegated
encoding work only, estimated mathematical completion 100%, artifact
completion 100%. These are task-progress estimates, not certifications of
the parent publication goal.
