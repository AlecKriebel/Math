# Finite-universe completeness

## Completion-count lemma

For a primitive target core `H`, let `m_H` be its directed core-segment
count, `q_H` its path-sink count, and `r_H` its number of minimum-repair
choices in the target grammar.  The exact tuples are

```text
cycle (2,1,1), theta0 (5,1,2), theta1 (5,1,2),
theta2 (6,2,4), theta3 (6,2,2).
```

For `k` physical selected boundaries and `epsilon=1` when the incoming
boundary is selected (`epsilon=0` when it is the incoming dummy), the number
of target completions is

\[
C(k,\epsilon)=\sum_H r_H\sum_{j=0}^{q_H}
 \binom{q_H}{j}
 \binom{k-\epsilon-j+m_H-1}{m_H-1}.
\]

Indeed, choose `j` selected path sinks and weakly distribute the remaining
`k-epsilon-j` selected boundaries over the `m_H` directed segments.  Empty
repair segments receive their uniquely named dummy boundaries and do not
change the count.  Each minimum repair remains a distinct directed target
record.  Physical label permutations are applied only afterward.

| Case | `k` | Incoming selected | Core subtotals | Total |
|---|---:|---:|---|---:|
| `four_port_selected_incoming` | 4 | true | cycle=7, theta0=100, theta1=100, theta2=416, theta3=208 | 831 |
| `four_port_marginalized_incoming` | 4 | false | cycle=9, theta0=210, theta1=210, theta2=1036, theta3=518 | 1,983 |
| `five_port_selected_incoming` | 5 | true | cycle=9, theta0=210, theta1=210, theta2=1036, theta3=518 | 1,983 |
| `five_port_marginalized_incoming` | 5 | false | cycle=11, theta0=392, theta1=392, theta2=2240, theta3=1120 | 4,155 |
| `three_port_selected_incoming` | 3 | true | cycle=5, theta0=40, theta1=40, theta2=136, theta3=68 | 289 |
| `three_port_marginalized_incoming` | 3 | false | cycle=7, theta0=100, theta1=100, theta2=416, theta3=208 | 831 |

Consequently,

\[
6(831+1983)4!=405{,}216,
\]

for the six four-port theta source repairs,

\[
4(1983+4155)5!=2{,}946{,}240,
\]

for the four minimum-repaired five-port `theta2` sources, and

\[
2(289+831)3!=13{,}440
\]

for the two three-port cycle source supports.

## Exhaustiveness boundary

This derivation compresses the arithmetic of the frozen primitive grammar.
The script parses the locked `CORES` literal directly from the atlas, requires
the exact five primitive arc/sink/repair encodings, and independently enumerates
every unique `(core, incoming mode, sink mask, weak composition, repair)` key.
It relies on, and does not re-prove, the frozen primitive-core theorem.  The
cycle target grammar has one repair choice; its two minimum source supports are
counted separately in the leading source factor.  Physical label permutations
are applied only after target enumeration.  No source-target reversal,
ordinary-triangle quotient, inheritance complement, pole exchange, or
uncertified graph symmetry is used in the count.

The uniqueness claim is for directed completion records/presentations, not for
unlabelled graphs.  When a repaired arc is already occupied, different repair
records can construct the same graph.  The record key retains the core,
incoming mode, repair index and arc set, sink mask, ordered segment words,
deterministic dummy roles, and then the exact physical port permutation.

The derived totals agree exactly with the authoritative corrected composite
ledgers bound by baseline payload `cac8186363802b68c419874eb67543699dc3f71345228c068f89a31bd74de674`.
