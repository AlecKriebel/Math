# Conclusion of the bounded Hall experiment

Completed: 2026-07-24.

## Verdict

The experiment produced one genuine all-\(m\) structural lemma, but not a
proof of the Boolean down-set inequality or Erdős Problem 84.

For every \(P\ni1\), the two positive boundary families in the safe/unsafe
decomposition coincide setwise.  With

\[
\mathcal B_P=(\mathcal H_P\vee V(P))\setminus\mathcal H_P
\]

and

\[
d(P)=|\mathcal A_P|-|\mathcal A_P\vee V(P)|,
\]

the exact identity is

\[
g_m(P)=2|\mathcal B_P|-d(P).
\]

Moreover, \(A\mapsto A\cup\{m\}\) embeds every safe collision fibre
canonically into the corresponding unsafe fibre and commutes with union by
\(V(P)\).  This reduces the desired charge to congestion two on a single
underlying boundary family.

## What the matching test decided

The representation-aware one-local-edit graph is false.  Its exact maximum
matching shortfalls are \(20\) at \(m=6\) and \(268\) at \(m=7\).

The sole enlargement to row-selection Hamming radius two has exact full
matchings in both cases.  Incremental repairs have depth at most two and
three, respectively, and are dominated by double removals.  However, the
\(m=7\) repairs use 32 coarse templates and also require double additions.
No deterministic all-\(m\) injection or uniform alternating-depth lemma has
been extracted.

## Research classification

- **New internal theorem:** the twin-boundary identity and the
  join-commuting fibre embedding.
- **Sharp falsification:** one local representative edit is insufficient.
- **Viable conjecture:** the representation-aware Hamming-two graph may
  always have a saturating matching.
- **Not established:** a canonical all-\(m\) charge, a general bounded-depth
  theorem, the Boolean down-set inequality, or the Erdős problem.
- **Publication status:** not a standalone paper.  The all-\(m\) lemma is
  worth retaining as a component of a future proof or broader manuscript,
  but the present finite matching evidence should not be published as a
  theorem.

The prescribed stop was honored: no \(m>7\), parameter radius two in the
representation graph, row radius three, or second enlargement was tested.
Any future resumption should be theoretical and target a proof or
counterexample to the Hamming-two matching conjecture, not additional
enumeration.
