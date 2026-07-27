# Hostile review: exact mixed-witness local synthesis

## Verdict

**PASS WITH MINOR DOCUMENTATION CORRECTIONS.**

Commit `a997ced3` correctly establishes the stated **OBSERVED,
exhaustive-labeled** exclusions at orders 8 and 9.  In the precise labeled
mixed-\(P_4\) universe, there is no graph with
\(\gamma=\alpha=3\) admitting an arbitrary proper one-guard eternal
three-family with the six required and six forbidden direct responses.

The numerical results, checkpoint contents, proper-family fixed-point
argument, base-orderability CEGAR result, disjunctive counterexample, and
the `HDzruf]` replay all passed an independently implemented full audit.
This is finite evidence only.  It is not an order-\(10+\) exclusion and
does not prove the universal \(\gamma\)-\(\theta\) conjecture.

Two documentation corrections are recommended:

1. Section 8's claim that a completed-checkpoint resume reproduces
   identical output bytes is generally false because `completed_at` is
   regenerated.  A replay changed only that timestamp and therefore also
   changed the file hash.  The mathematical content reproduced exactly.
2. In section 3, qualify the row “nonempty safe family after all six
   negative swaps are banned: 0” by “among the
   \(\gamma=\alpha=3\) frontier.”  Read over all labeled masks, the
   unqualified sentence is contradicted by the same note's gamma-2 graph
   `HDzruf]`, whose banned-state kernel has 46 states.

Neither issue affects the finite mathematical conclusion.

## Independent audit method

The review checker imports no code from the synthesis source.  It
independently implements:

- the labeled graph-mask universe;
- exact domination and independence searches;
- a synchronous greatest-safe-family deletion procedure;
- a separate literal one-guard obligation checker;
- a lexicographic, rather than frequency-ordered, base-cube CEGAR;
- Graph6 encoding and decoding; and
- direct reconstruction of every stored family in the two named graph
  replays.

The checker is
`reviews/mixed_witness_local_synthesis_hostile/hostile_audit.py`.
Its complete machine-readable output is
`reviews/mixed_witness_local_synthesis_hostile/hostile-evidence.json`.

## Coverage audit

The nine fixed edges and eight fixed nonedges are disjoint.  Together
with the unknown edges they partition every unordered vertex pair:

| order | total pairs | fixed edges | fixed nonedges | unknown edges | masks |
|---:|---:|---:|---:|---:|---:|
| 8 | 28 | 9 | 8 | 11 | 2,048 |
| 9 | 36 | 9 | 8 | 19 | 524,288 |

Every mask was visited exactly once.  No isomorphism rejection or
symmetry breaking is used.  This is sufficient: a graph realizing the
pattern already comes with the eight distinguished vertices
\(a,b,c,x_0,x_1,x_2,x_3,w\); at order 9 the remaining vertex is the
arbitrary vertex \(y\).

The independent run reproduced the exact stored mask lists and their
SHA-256 digests for:

- the \(\gamma=\alpha=3\) frontier;
- the all-required-states-dominating frontier;
- the unrestricted eternal-equality frontier; and
- the 18 disjunctive-response masks.

It also reproduced all family-size, response-pattern, deletion-wave,
initial-state, forced-adjacency, and required-frontier histograms.  Every
graph on the \(\gamma=\alpha=3\) frontier was independently confirmed
connected.

## Exact numerical replay

| condition | order 8 | order 9 |
|---|---:|---:|
| masks | 2,048 | 524,288 |
| \(S\) and six positive states dominate | 576 | 87,552 |
| preceding condition and \(\alpha=3\) | 552 | 68,688 |
| \(\gamma=\alpha=3\) | 62 | 8,985 |
| all required states dominate | 0 | 96 |
| unrestricted eternal equality | 9 | 1,150 |
| unrestricted family has all six positives | 0 | 0 |
| exact banned-state kernel nonempty within equality frontier | 0 | 0 |
| exact realizations | **0** | **0** |

The independent counts agree with every count stored in both JSON results
and checkpoints, including the literal-family totals of 45 and 6,140 and
the literal attack-obligation totals of 4,050 and 977,808.

At order 9, all 96 static candidates have an empty exact kernel.  Their
synchronous extinction profiles match exactly.  Forty-two have a
nonempty unrestricted eternal family, and the maximum number of required
positive swaps surviving unrestricted closure is four.  The independently
recovered closest masks are

\[
89928,\quad106372,\quad352072,\quad368516.
\]

## Parameter and one-guard audit

The parameter predicates are exact:

- \(S=\{a,b,c\}\) is fixed independent, and every independent 4-set is
  excluded, so \(\alpha=3\);
- \(S\) dominates, while every 1- and 2-subset is checked and fails to
  dominate, so \(\gamma=3\); and
- a nonempty closed family of dominating triples proves
  \(\gamma^\infty\leq3\), while \(\alpha\leq\gamma^\infty\) gives equality.

The transition checker considers only attacked vertices outside the
current state.  A response replaces exactly one guard, requires that guard
to be adjacent to the attacked vertex, and requires the successor to be a
dominating triple in the same family.  No all-guards move, occupied attack,
or complement-edge interpretation appears.

## Proper-family fixed point

Let \(\mathcal U\) be the dominating triples excluding the six banned
states.  The deletion operator removes a state having an unoccupied
attack with no supported one-edge successor.

For any eternal family \(\mathcal F\subseteq\mathcal U\), induction over
the synchronous deletion waves gives
\(\mathcal F\subseteq\Psi^j(\mathcal U)\) for every \(j\).  Hence every
proper eternal family avoiding the six states lies in the final kernel
\(\mathcal K\).  Conversely, nonempty \(\mathcal K\) is itself an eternal
family.  If all required positive states and \(S,T\) survive, that same
kernel is the desired exact-list family.

Thus the source's safe-kernel criterion covers arbitrary proper families;
it does not assume that a target family is the unrestricted greatest
family.

## Base-orderability CEGAR

For each of the six bijections \(S\to T\), the checker constructs the six
interior states of the associated subset-compatible cube.  If a current
safe kernel contains a full cube, every non-base-orderable subfamily
inside it must omit at least one interior state of that cube.  Branching
on all six omissions is therefore exhaustive.  If \(S\) or \(T\) is
deleted, the branch cannot contain the target family; if no live cube
remains, the kernel itself is a counterexample.

The independent checker used a lexicographic live-cube choice, not the
source's frequency heuristic.  It nevertheless reproduced:

| order | graphs | fixed points | maximum for one graph | maximum ban depth | counterexamples |
|---:|---:|---:|---:|---:|---:|
| 8 | 9 | 63 | 7 | 1 | 0 |
| 9 | 1,150 | 8,914 | 31 | 2 | 0 |

This validates the bounded CEGAR claim, not universal base-orderability.

## Named-graph hostile replays

### `HCxrs`c`

Independent Graph6 decoding recovers mask 39588 and

\[
(\gamma,\alpha,\gamma^\infty)=(3,3,3).
\]

The unrestricted greatest family has 39 states and all 234 literal
attack obligations pass.  Banning all six negative direct swaps gives an
empty kernel.  Banning each negative state separately gives a nonempty
kernel.  The three distinct stored family records, sizes, hashes, and
states all match the independent reconstruction.

Therefore the graph is a valid counterexample to the proposed
family-independent selection of one unavoidable extra response.

### `HDzruf]`

Independent Graph6 decoding and exhaustive parameter search give

\[
(\gamma,\alpha,\gamma^\infty)=(2,3,3).
\]

The dominating pair is \(\{a,x_1\}\).  The two-guard safe kernel is empty.
After banning the six negative triple states, the three-guard kernel has
initial size 68, deletion waves \(16,6\), and final size 46.  All
\(46\cdot6=276\) literal obligations pass.  The stored 46 states match
exactly, as do the lists

\[
\begin{aligned}
L(x_0)&=\{a\},&
L(x_1)&=\{a,c\},&
L(x_2)&=\{b,c\},\\
L(x_3)&=\{b\},&
L(w)&=\{a,b\},&
L(y)&=\{a,b\}.
\end{aligned}
\]

The graph is correctly scoped as a gamma-2 stress model and not an
equality realization.

## Checkpoint and artifact audit

All seven frozen SHA-256 values in section 8 of the note match the
committed bytes.  Each checkpoint has the correct format and source hash,
has `next_mask == stop_mask`, covers the full mask interval, and contains
counters and retained mask lists exactly matching the result JSON.

A completed resume was also executed.  It regenerated an otherwise
identical result except for `completed_at`; consequently the byte hash
changed.  Resume state integrity is sound, but the byte-identical wording
should be corrected or the timestamp should be made deterministic.

## Final classification

- **Accepted:** exhaustive order-8/order-9 labeled nonexistence for the
  exact mixed pattern under \(\gamma=\alpha=3\).
- **Accepted:** proper-family coverage by the banned-state greatest safe
  kernel.
- **Accepted:** bounded absence of a base-orderability counterexample.
- **Accepted:** `HCxrs`c` disjunctive-response counterexample.
- **Accepted:** `HDzruf]` gamma-2 stress replay.
- **Not claimed / not established:** any order-\(10+\) exclusion,
  universal mixed-pattern lemma, or resolution of the
  \(\gamma\)-\(\theta\) conjecture.
- **Correction requested:** timestamp byte-reproducibility sentence and
  one table-row scope qualifier.

## Addendum — corrections closed

Reinspection at 2026-07-26 17:50 PDT confirms that both requested
documentation corrections have been applied correctly:

1. The count-table row now explicitly restricts the zero safe-family count
   to the \(\gamma=\alpha=3\) frontier, both in `NOTE.md` and in
   `RESEARCH_LOG.md`.
2. The resume paragraph now states accurately that every mathematical
   field reproduces, while the regenerated `completed_at` timestamp changes
   the output bytes and hash.

No synthesis source, result, checkpoint, or certificate byte changed.
The corrected documentation hashes are:

| artifact | corrected SHA-256 |
|---|---|
| `math/working/mixed_witness_local_synthesis/NOTE.md` | `9ca4ab839d1453c6debba937f3fed7c3af61b81f49accbdd6ad742e57847ea8d` |
| `math/working/mixed_witness_local_synthesis/RESEARCH_LOG.md` | `592f8220edc83acb8b38e2802eadeba74f1bde8612667c50925fb458572f42ed` |

**The two hostile-review issues are closed.  The revised artifact receives
an unconditional PASS for its stated bounded, observed claims.**
