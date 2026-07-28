# Deletion-rank anatomy of complementary exchanges at order nine

## Status and scope

Date: 2026-07-28 (PDT)

This is a mechanism probe for the open greatest-family reciprocity
conjecture.  It is classified as **OBSERVED** pending an independent
implementation and coverage audit.  It proves no all-order reciprocity
statement, no complete \(k=3\) theorem, and no resolution of the
\(\gamma\)--\(\theta\) conjecture.

The input was the `geng -cq 9` stream of 261,080 connected unlabeled graphs
of order nine.  The checker retained the graphs satisfying

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and computed synchronous deletion ranks in the literal greatest fixed point
of dominating triples.

For maximum independent triples \(S,T\), \(u\in S-T\), and \(x\in T-S\),
the paired configurations are

\[
 A=S-u+x,\qquad B=T-x+u.
\]

Rank zero means that a configuration does not dominate, a positive integer
is its fixed-point deletion round, and `S` means that it survives in the
greatest eternal family.

## Exact discovery output

Among the order-nine input graphs:

- 2,949 satisfy the static conditions \(\gamma=\alpha=3\);
- 1,380 also have a nonempty greatest eternal triple-family;
- those families contain 35,299 states in total;
- the scan examined 90,103 unordered pairs of maximum independent triples
  and 392,155 complementary exchange instances.

There are 12,522 exchange instances for which exactly one of \(A,B\)
dominates.  Thus **static complementary-exchange reciprocity is false even
under**

\[
 \gamma=\alpha=\gamma^\infty=3.
\]

The first displayed control is `HCOceRy`, with

\[
 S=012,\quad T=578,\quad u=0,\quad x=7.
\]

Here \(S-u+x\) is non-dominating while \(T-x+u\) is deleted in the first
kernel round.

Every one of the 12,522 static asymmetries is repaired dynamically: the
dominating member is deleted in round one or two.  More generally, the
complete rank-pair table contains many unequal finite ranks, including
rounds one through three, but the only rank pair involving a survivor is

```text
S,S : 179,773
```

No complementary exchange has one surviving state and one finite-rank or
non-dominating state.

## Consequence for the proof route

This sharply narrows the possible proof mechanism.

1. Reciprocity cannot be established at the initial set of dominating
   configurations and then carried through the fixed-point recursion.
   The initial static statement is false thousands of times.
2. Deletion ranks are not equal between paired configurations, so a
   round-by-round rank-preserving induction is also false.
3. The observed invariant is only **simultaneous infinite survival**.
   A proof must therefore construct a coinductive simulation or show that
   any one-sided winning strategy yields a dominating pair, contradicting
   \(\gamma=3\).

This is consistent with the separately proved `GEjbug` boundary:
greatestness without \(\gamma=\alpha\) permits one-sided survival.  The
order-nine equality census suggests that the no-dominating-pair condition
repairs asymmetry through the game dynamics, not through static domination.

## Reproduction

From the repository root:

```text
gamma_theta_eternal_domination/tools/nauty2_9_3/geng -cq 9 \
  | python3 -I -B -W error \
      gamma_theta_eternal_domination/math/working/\
greatest_family_reciprocity_rank_probe/probe_rank_pairs.py
```

The deterministic JSON output must match `order9_result.json`.  The nauty
coverage premise, graph6 decoder, parameter filters, kernel implementation,
and counts still require a clean-room audit before promotion beyond
`OBSERVED`.
