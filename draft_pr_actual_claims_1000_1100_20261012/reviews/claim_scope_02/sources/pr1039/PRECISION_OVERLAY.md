# Precision overlay for the frozen reconstructed report

Applies only to the 15061-byte report with SHA-256
`e5f6b869aac42975f0f2a05f9cd3e8ba57b20547377c142c2e9ab6c4ed22fcaa`.

This file leaves that report unchanged. It records one required scope clarification and one optional strengthening of an already valid collar argument. Neither introduces a new approach or proves the original problem.

## 1. Required clarification: surface shell versus ambient shell

Replace the interpretation of Section 7, item 3 with:

> The local obstruction rules out an ambient comparison that restricts to a pair homeomorphism of the original ball fixing its entire boundary sphere pointwise. For example, it rules out a comparison that is the identity on the ambient product shell `S^3 x [0,1]`. Being the identity only on the surface cobordism `S` does not imply that condition. A homeomorphism relative only to the outer boundary sphere may move the internal sphere or act nontrivially on it, and is not ruled out by this local argument.

The original term “shell” must mean the ambient shell for its stated implication about the full sphere to hold. The two-dimensional cobordism alone is insufficient. No internal seam marking is part of the original KP 4.31 problem.

## 2. Optional strengthening: one common collar and arbitrary extensions

For Section 5, choose one smooth extension `Psi` of `f` by the trace of a boundary isotopy stationary near both endpoints. On a fixed outer collar it is `f` times the normal identity, so it is the identity near the collared link `L`. The extensions `Psi^k`, for all integers `k`, then have a single common such collar.

If other extensions `Psi_k` are preferred, the distinction proof remains valid exactly as written. Two extensions of the same `f^k` produce boundary-relative diffeomorphic annular pairs, because the composite of one with the inverse of the other restricts to the identity on the boundary. Thus the collar choice does not affect the local equivalence classes.

## Status

The local nonextension theorem and exact-knot genus calculation are accepted. The original problem remains UNSOLVED at turn 3/5. The global topological-equivalence and smooth-distinction questions for the grafts remain unproved.
