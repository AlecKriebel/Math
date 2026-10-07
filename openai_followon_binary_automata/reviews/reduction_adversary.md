# Independent adversarial review of the binary reduction

Checkpoint: 2026-10-06 21:17 America/Los_Angeles (2026-10-07 04:17 UTC).
Reviewer: delegated adversarial agent `reduction_adversary`.
No external individuals were contacted; no source-clone or Git changes were made.

## Verdict and exact scope

I found no substantive defect in the strict fixed-block binary reduction,
the endmarked source count `(3h^3-h)/2+2`, the exact `sh^2` pullback, or
the `h^3` source-size fooling set. The exponential consequences remain
dependent on the two upstream lower-bound theorems: I checked their source
language and automaton conventions, not their entire algebraic proofs or
Lean builds. This review therefore does **not** independently certify the
unconditional core separation, novelty of a full paper, or a publication
package. No complete package existed in my review scope.

One useful sharpening is an ordinary epsilon-free, single-initial-state
NFA with at most `(3h^3-h)/2+1` states, given explicitly below. The
endmarked `+2` construction is already a valid source for the stated
two-way-model theorem, but a paper advertising an *ordinary 1NFA* should
also give this conventional compiler. Raw outward marker rules must be
discarded before using the compiler if the chosen presentation disables
illegal moves rather than prohibiting their transition-table entries.
This normalization uses zero new states and changes no language.

## Original sources actually checked

Read-only clone: `/Users/alec/Desktop/math`, advertised pin
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

I inspected the determinization manuscript's `build/sections/machines.tex`
and `build/sections/separation.tex`, the complementation manuscript's
`build/sections/introduction.tex` and `build/sections/automata.tex`, and
`lean/docs/129.md`. Both inputs use the language of *nonempty products*
of arbitrary relations on a nonempty `h`-point set. The empty product is
the identity and hence live. The complementation target recognizes
product emptiness on every relation word. Its original model includes
zero-step acceptance, partial transitions, distinct endmarkers, left,
right and stay moves, initial head on the left marker, and finite-run
acceptance; infinite branches without an accepting finite prefix reject.

The automaton-semantic constructions read are compatible with the
pullback. I did not independently reprove the pivotal rank-loss,
transport, nesting or amplification lemmas; those are separate upstream
dependency audits. Comparator declarations were not used as evidence.

The candidate proof reviewed was
`agent_notes/binary_compiler.md` SHA-256
`d3b05e01561529df582b496f7d8ae5b6a892124e7381403bcf7c917e812a08fa`.
The candidate executable tested was `code/binary_compiler.py` SHA-256
`013a096ca48a8a8123d6f28adf32b6e6d517ef7bd9d125450e6950ee772b49d0`.

## Independent uniform checks

Write `b=h^2` and let `E` concatenate row-major adjacency matrices.
Every `b`-bit block is exactly one relation, so `E` is a bijection from
relation words onto binary words of length divisible by `b`. With
`B_h=E(L_h)`, all nonmultiple lengths reject and the empty word accepts.
There is no hidden promise on the source language.

### Source invariant and trimmed counts

Before an edge has been selected in a block, `U(p,t)` retains its source
vertex `p` and phase `t`. It may wait until the chosen row, then select
exactly a 1-bit `(p,q)`. It cannot postpone past the final bit of row `p`.
After selection, `V(q,t)` retains endpoint `q` and skips to the block end.
The earliest possible chosen column `q` is in the first row, so phases
`t>=q+1` suffice for `V(q,t)`. The ranges of both state types and every
destination are therefore valid. Phase zero is reached again only after
a complete block; this proves rejection of every malformed final block.

The count is

    |U|=h^2(h+1)/2,
    |V|=h^3-h(h+1)/2,
    2+|U|+|V|=(3h^3-h)/2+2.

The initial marker step guesses the initial vertex. The right-marker
accepting stay exists only in `U(p,0)`. Empty input uses those two steps;
all runs have at most input length plus two steps. Thus both zero-step
and positive-step acceptance conventions recognize the same source.

For an ordinary NFA whose accepting run must consume the whole word,
delete the original `in` and `acc`. Retain all `U,V` states, make all
`U(p,0)` final, and add one accepting initial state `S`. On bit `a`,
the successors of `S` are the union over `p` of the successors of
`U(p,0)` on `a`; these are the existing rules above. All transitions
consume one bit, so no epsilon transitions or markers are needed.
The empty word accepts in `S`; every nonempty run is the corresponding
endmarked body scan. This gives `(3h^3-h)/2+1` states. For `h=1` the
redundant `S` can be removed, but no special optimization is needed.

### Fooling set, including endmarked any-position acceptance

Let `e_p={(p,p)}` and `I` be the full identity. For `p<h,t<b`, take

    x_(p,t)=E(e_p) prefix_t(E(I)),
    y_(p,t)=suffix_from_t(E(I)) E(e_p).

There are `h b=h^3` pairs. Every diagonal is live. If `t!=u`, the
cross-concatenation has length `3b+t-u`, which is nonmultiple since
`0<|t-u|<b`. If `t=u` but `p!=q`, the decoded product is
`e_p I e_q=empty`. Thus every off-diagonal cross rejects.
Recording the state at the cut in one accepting run for each diagonal
and splicing two runs if their cut state coincides proves the ordinary
NFA lower bound, including multiple initial states and epsilon moves.

For a no-left, stay-permitting endmarked recognizer that can accept at
any position, an accepting run cannot end before reaching the right
marker: that finite run could be replayed on the same accepted word
with one appended bit, which is malformed for `h>=2`. Therefore every
accepting run has crossed the `x/y` cut. Choose its first configuration
on the first suffix cell; every suffix here is nonempty. The pre-cut
run depends only on the left marker and prefix; the post-cut run depends
only on its state, suffix and right marker. With no left moves the
suffix run cannot consult the discarded prefix. Splicing therefore
works with stays and acceptance at any configuration as well. For
`h=1` the asserted lower bound is just one state.

Consequently the cubic source-size order is a proved property of this
*strict alignment language*. It does not imply a source lower bound for
other encodings or promise languages.

### Target pullback and acceptance

The states `(q,t)` with `q` a target state and `0<=t<b` give exactly
`s b` states. At a relation cell with phase `t`, the transition reads
the target bit `E(R)[t]`. An internal bit-to-bit target move changes
phase and uses a relation-cell stay; a move across a block boundary
changes both relation cell and phase as prescribed. Target stays retain
the phase. Left-marker right moves reset phase zero; right-marker left
moves reset phase `b-1`. Marker stays retain phase, while marker rows
ignore it.

At relation cell `j` the projection sends `(q,t)` to target position
`(j-1)b+t+1`; marker projections ignore phase. Every compiled transition
projects to one target transition, and every target transition has one
lift from the current compiled configuration. This remains true even
when a marker is reached with a noncanonical stored phase. Reachable
markers need not all have phase zero; the proof correctly does not
assume this. Finite runs correspond step-for-step, preserving run length
and accepting states. Hence positive versus zero-step acceptance is
preserved exactly. Infinite nonaccepting runs cannot acquire an accepting
finite prefix under the projection. Undefined rows remain undefined.
On empty input, the tapes both consist of the adjacent two markers and
the same statement applies. Determinism is preserved.

If outward marker rules are present in a raw table but disabled by the
model, delete them before compilation. They were never executable and
their deletion does not alter accepting configurations or introduce a
new state. The candidate executable intentionally asserts legal marker
rows, so its public interface should state that normalization.

### Complement universe and quantitative consequence

There is a disjoint union

    {0,1}* minus B_h
      = {nonmultiple lengths} union E(Sigma_h* minus L_h).

Therefore `E^(-1)({0,1}* minus B_h)=Sigma_h* minus L_h`, including
empty input (which neither complement contains). Malformed words are
indeed accepted by the binary complement; the pullback's inability to
see them is immaterial because it recognizes product emptiness on
*every* relation word. It would be false to identify the binary
complement with the second union term alone.

If the upstream initial-configuration bounds are valid, the exact
consequences are

    2^floor((h-2)/31) <= 4(s h^2+1)^2,
    2^floor((h-2)/127) <= 2(s h^2+1).

The first has `+2` instead of `+1` under the upstream positive-step
convention. These give `2^Omega(h)/h^2`, hence
`2^Omega(n^(1/3))` for the cubic-size source family (and for all
sufficiently large requested source counts after unreachable padding).
They do not give `2^Omega(n)` or any uniform complexity-class separation.

## Actual exhaustive checks

I independently wrote `reviews/reduction_adversary_check.py` rather than
using the candidate's acceptance routine as an oracle. Its simulator
uses explicit configuration reachability, disables raw outward rules,
and tests both finite-acceptance conventions. Its source truth oracle
composes the full relations. Its separate ordinary NFA compiler uses
whole-word acceptance and no markers. The candidate compiler is called
only as the object being tested.

Python 3.14.6 produced `reduction_adversary_independent_receipt.json`:

- 16,382 ordinary-source words: all binary words of lengths 0 through 12
  for each `h=1,2`, including malformed strings.
- 32,764 independent endmarked-source checks on those words under both
  acceptance conventions.
- 20,515 fooling-set cross checks for every pair for each `h=1,...,5`.
- All 8,192 one-state raw nondeterministic machines (all subsets of the
  three moves in all four symbol rows, and both accepting-state choices),
  including raw illegal marker rules discarded before compilation.
- 4,472,832 independent pullback comparisons on every `h=2` relation
  word of lengths 0 through 2, under both acceptance conventions.
- 4,369 complement-identity checks on all `h=2` relation words of lengths
  0 through 3.

Every check passed. I also reproduced the candidate's own complete run:
288 one-state deterministic machines, 128 sampled multi-state machines,
227,136 pullback comparisons and 1,534 source words passed. Its receipt
is saved separately as `reduction_adversary_existing_code_receipt.json`.
These checks support the compilers; the uniform proofs above do the
mathematical work. They do not test the exponential input bounds.

Independent script SHA-256:
`bff7d0d7bb6338421e4632231792d003aa019e34e3020c869a638d5427861bdf`.

## Source-size novelty and attribution caution

I separately inspected the primary author-hosted PDF of Kapoutsis,
*Nondeterminism is essential in small two-way finite automata with few
reversals*, especially Section 2's promise-language definitions and
Conclusion, PDF page 28 / printed page 29:
https://www.andrew.cmu.edu/user/cak/reads/2013-IAC/main.pdf .
The conclusion already discusses natural `h^2`-bit coding and states an
`O(h^2)` zero-reversal source claim, with a lower bound only for
few-reversal deterministic targets. It supplies neither an explicit
compiler there nor a definition of behavior on malformed binary words.
The cubic fooling set rules out such a quadratic bound for the strict
total language audited here. A promise or a different off-promise
completion removes the malformed cross tests. That distinction should
be stated cautiously; this review does not establish an error in the
older paper, priority of the cubic observation, or absence of other
public binary encodings. Alphabet reduction itself is established
machinery and must be attributed. The new unrestricted exponential
input is inherited rather than independently solved by this conversion.

## Remaining gap and checkpoint percentages

Strongest independently verified result here: the total strict-block
language has an explicit cubic ordinary/endmarked one-way source,
needs at least `h^3` ordinary/no-left source states, and admits an exact
`s h^2` pullback for arbitrary binary 2NFAs or 2DFAs. This is a complete
uniform encoding theorem independent of the unreviewed algebraic input.

Exact remaining gap for an unconditional core theorem: independently
validated upstream exponential bounds, their semantic formal checks,
and final-package priority/claim/reproducibility reviews. This is an
upstream dependency gap, not a blocked binary reduction mechanism.
For this delegated reduction task: mathematical completion 100%,
review-artifact completion 100%. For the entire publication objective,
this reviewer makes no completion estimate; the parent tracks it.
