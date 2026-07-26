# Hostile review: anchor-canonical minimum signatures

Status: **ACCEPT EXACT FOUR-CUBE ORBIT REDUCTION**

This review covers
`math/lemmas/order12_k4_anchor_signature_symmetry.md` at SHA-256
`11d6fe9790083dcaecb196f1f175712b02e2bdfde5003454509ab3c6ee369acc`.
It does not certify the parent UNSAT, exclude the order-12 parameter-four
slice, or resolve the universal conjecture.

## Anchor and color action

The simultaneous action is sound when read as the standard push-forward:
old anchor \(i\) is sent to anchor \(\pi(i)\), and old color \(c\) is renamed
\(\pi(c)\). The new color on anchor \(\pi(i)\) is therefore \(\pi(i)\), so
the normalization \(c(j)=j\) is restored.

The independent probe first regenerated all 65,536 normalized coloring-bank
clauses and matched them to the exact frozen parent. It then checked every
one of the \(24\cdot65,536=1,572,864\) anchor-permutation/color-row actions.
In every case, relabeling the clause's vertices gave exactly the clause for
the transformed normalized row. Thus the complete bank, not merely its
colorability meaning, is preserved as a set.

The remaining pre-sort clause families are invariant under the induced
vertex action. In particular, although the connected-cut generator retains
the side containing vertex \(0\), the complementary side describes the same
crossing-edge clause; moving vertex \(0\) therefore does not break the set of
cut clauses.

## Re-sorting and lexicographic descent

Outer re-sorting is legitimate because the pre-sort formula has the full
outer \(S_8\) action. The probe checked all
\(7\cdot65,536=458,752\) adjacent outer swaps on the exact complete coloring
bank; the other clause families are set-indexed by vertices, states, attacks,
and witnesses and are equivariant. Adjacent swaps generate every required
outer permutation.

For the key descent, swapping adjacent anchor coordinates \(1,0\) in the old
minimum signature produces the corresponding signature \(0,1\), strictly
smaller at its first changed coordinate. The newly sorted minimum is no
larger than that transformed signature, so its first row—and hence the full
concatenated sorted word—is strictly smaller. No assumption about which
outer vertex becomes label \(4\) is needed.

An independent abstract search enumerated all
\(\binom{15+8-1}{8}=319,770\) eight-row signature multisets with no `1111`
row. It checked 91,044 adjacent-inversion descents and all 24 coordinate
actions per multiset. No counterexample was found: every orbit's least
sorted representative begins with exactly one of
`0000`, `0001`, `0011`, or `0111`.

The executable probe and canonical output are
`reviews/order12_k4_anchor_signature_symmetry_hostile_probe.py` and
`reviews/order12_k4_anchor_signature_symmetry_hostile_probe.json`.

## Claim boundary

The four zero-first cubes `0010`, `0100`, `0101`, and `0110` are discarded
only as labeled orbit-redundant cases; this review does not call them UNSAT.
By contrast, the separate connected minimum-signature lemma logically
excludes all eight `1***` cubes. The note keeps this distinction correct and
does not alter or infer statuses in the immutable 16-cube production run.
