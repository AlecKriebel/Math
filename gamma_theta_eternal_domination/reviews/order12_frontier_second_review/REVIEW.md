# Second independent review of the order-12 frontier

## Verdict

**`ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE`.**

The frozen target
`math/lemmas/order12_frontier.md`, SHA-256
`adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75`,
correctly proves that no counterexample has order at most \(12\), relative
to the published MacGillivray--Mynhardt--Virgile through-order-\(11\)
computation.  No mathematical, exact-model, certificate, citation,
coverage, or scope defect was found.

The target was not edited.  No SAT solver was run.

## Exact parameter-four lane

An independent strict parse reproduced the exact DoubleLex formula census:

\[
(v,c,\ell)=(18{,}381,115{,}507,1{,}190{,}774),
\qquad |D|=4{,}030{,}657,
\]

with SHA-256
`14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.
The exact parent body is the prefix of \(D\).  A reviewer-side reconstruction
of the three adjacent eight-bit comparators reproduced the 765-clause,
10,758-literal, 37,710-byte suffix byte for byte, including SHA-256
`328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0`.

The clean-room constructor and DoubleLex probes both passed afresh.  In
particular, the constructor check confirmed that attacks are only at
unoccupied vertices, each response replaces exactly one named guard along a
\(G\)-edge, the successor remains in the selected dominating family, and
the complete complement-coloring bank has the correct sign.  All seven
model mutation probes were killed.

The normalized RUP and LRAT hashes and sizes match the target.  The retained
forward and backward transcripts each report `s VERIFIED` and zero RAT
lemmas.  I also ran a fresh, lightweight `lrat-check` replay against the
exact formula and retained 228,381,671-byte LRAT.  It exited zero with empty
stderr and exactly one `c VERIFIED`.

The proof transfer is complete and correctly separated:

1. the exact-CNF hostile verdict is
   `ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY`;
2. C-045 gives parent-SAT iff DoubleLex-SAT;
3. C-037 realizes every connected order-12
   \(\gamma=\alpha=\gamma^\infty=4<\theta\) graph in the exact parent; and
4. equality collapse supplies \(\alpha=4\) from the target hypothesis.

Thus exact \(D\)-UNSAT proves the complete connected \(k=4\) exclusion.  The
frozen producer metadata still says
`UNSAT_LRAT_VERIFIED_PENDING_INDEPENDENT_HOSTILE_REVIEW`; this is historical
package state.  The later hash-bound hostile review supplies the required
acceptance and is cited explicitly, so this is not a defect.

## Structural and coverage audit

The lower-order published premise makes any hypothetical order-12
counterexample minimum-order.  Component additivity then makes it connected;
the simplicial closed-neighborhood theorem removes simplicial vertices and
gives minimum degree at least two.

The official retained Henning--Schiermeyer--Yeo PDF explicitly restates the
McCuaig--Shepherd theorem as
\(\gamma(G)\leq2n/5\) outside
\(\mathcal F_4\cup\mathcal F_7\), identifies
\(\mathcal F_4=\{C_4\}\), and displays six graphs in \(\mathcal F_7\).
Hence all seven exceptions have order four or seven.  Since a minimum
counterexample has order at least \(12\), the bound applies.  For \(k=5\)
it requires \(n\geq\lceil25/2\rceil=13\), excluding order \(12\).

The complete order-12 parameter bookkeeping is exact:

- the accepted minimum-parameter theorem gives \(k\geq3\);
- the connected half-order theorem gives \(12\geq2k+1\);
- therefore \(k\in\{3,4,5\}\);
- C-035 excludes \(k=3\), explicitly including disconnected graphs;
- the exact DoubleLex chain excludes connected \(k=4\); and
- McCuaig--Shepherd plus the simplicial/minimum-order reduction excludes
  \(k=5\).

No disconnected case is omitted: under the published lower-order premise an
order-12 counterexample cannot have a smaller counterexample component.

## Published versus campaign evidence

The retained official MMV TeX uses the same unoccupied-attack, one-guard
model and states Observation 5.6: no counterexample has order at most \(11\).
It also records the order-10 and order-11 census and the 56/55/0 appendix
summary.

The target correctly does **not** promote the campaign's replay of the 56
listed graphs into exhaustive order-10/11 coverage.  It states that campaign
connected enumeration stops at order \(9\), that the original coverage at
orders \(10\) and \(11\) has not been reproduced to campaign certificate
standards, and that the final frontier depends on the published computation.
This published-versus-campaign boundary is explicit in the theorem statement,
proof, and reporting language.

## Omission and scope ledger

- Blocking omissions: **none**.
- The missing campaign-grade all-graph certificate for orders \(10\) and
  \(11\) is an explicit external premise, not a hidden omission.
- No claim follows for order \(13\) or larger.
- No universal proof or counterexample is claimed.

Machine-readable evidence and the reproducible solver-free audit are in
`evidence.json` and `audit.py` in this directory.
