# Preserved descriptor split-complement false positive

Status: reviewer implementation failure; not a primary-stream failure.

The first algebra pass rejected isomorphism state
`000281b9f1b340ee9017e13773c9487dcccf6c96de438c9fb6fe45fbbd35f1b3`
because two rooted presentations encoded opposite sides of one or more edge
splits.  For a zero-sum Fourier assignment, a descendant mask `A` and its
complement `A^c` have the same XOR and therefore the same JC edge factor.

The exact tensor evaluator was already correct because it evaluates only
zero-sum assignments.  The defect was confined to the auxiliary descriptor
equality normal form used for isomorphic states.  The corrected normal form
first replaces each retained mask by the lexicographically smaller of `A`
and `A^c`, then quotients reticulation ordering and parent-choice flips.
