# Additive clarification: deterministic chaining base point

The frozen TURN_4.md uses the symbol u_0 twice. In §1 it denotes an empty-pattern unit vector, which can depend on the network. In §2 the chaining base point must instead be a fixed deterministic vector, and must not refer to that earlier choice.

Read §2 with S_0={e_1}, where e_1 is the first standard basis vector, and choose every finite net S_j deterministically before observing inputs or labels. Replace the occurrences of Z(u_0) in that section by Z(e_1). The empty-pattern vector in §1 has no role in the probabilistic construction.

All link lengths, cardinalities, centered moment bounds, telescoping estimates and constants are unchanged. Conditioning on the label vector still leaves the same fixed nets and base point. This clarification is required for the stated uniform probability argument, not a new author turn. The original five-turn files and FINAL_AUTHOR_MANIFEST.json remain unchanged; this correction is bound separately and must accompany the final packet and review.
